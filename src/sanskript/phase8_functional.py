"""Phase 8 runtime values and VM dispatch helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable

from .errors import RuntimeSanskriptError
from .runtime_values import SanskriptValue, is_truthy, values_equal

if TYPE_CHECKING:
    from .bytecode import Instruction
    from .vm import SanskriptVM


@dataclass(frozen=True)
class ImmutableListValue:
    """Persistent (copy-on-write) list — append returns a new value."""

    items: tuple[SanskriptValue, ...] = ()

    def append(self, item: SanskriptValue) -> ImmutableListValue:
        return ImmutableListValue(self.items + (item,))


@dataclass
class LazyIteratorValue:
    """Lazy view over a materialized sequence."""

    items: tuple[SanskriptValue, ...]
    index: int = 0

    def exhausted(self) -> bool:
        return self.index >= len(self.items)


@dataclass
class GeneratorValue:
    """Suspended generator with resumable bytecode offset."""

    function_name: str
    params: tuple[str, ...]
    bound: dict[str, SanskriptValue]
    ip: int = 0
    done: bool = False


@dataclass
class RuleValue:
    """Grammar-engine rule: when predicate, then action."""

    rule_id: str
    when_name: str
    then_name: str


# Module-level rule registry (surakṣita tier).
_RULE_REGISTRY: dict[str, RuleValue] = {}

# Memoization caches keyed by function name.
_MEMO_CACHES: dict[str, dict[tuple[Any, ...], SanskriptValue]] = {}


def register_rule(rule: RuleValue) -> None:
    _RULE_REGISTRY[rule.rule_id] = rule


def get_rule(rule_id: str) -> RuleValue | None:
    return _RULE_REGISTRY.get(rule_id)


def clear_phase8_runtime_state() -> None:
    _RULE_REGISTRY.clear()
    _MEMO_CACHES.clear()


def materialize_sequence(value: SanskriptValue) -> list[SanskriptValue]:
    if isinstance(value, ImmutableListValue):
        return list(value.items)
    if isinstance(value, list):
        return value
    if isinstance(value, LazyIteratorValue):
        return list(value.items)
    raise RuntimeSanskriptError(
        f"Expected list or immutable list, got {type(value).__name__}",
    )


def expect_sequence(value: SanskriptValue) -> list[SanskriptValue]:
    return materialize_sequence(value)


def immutable_from_sequence(value: SanskriptValue) -> ImmutableListValue:
    if isinstance(value, ImmutableListValue):
        return value
    return ImmutableListValue(tuple(materialize_sequence(value)))


def build_phase8_dispatch() -> dict[str, Callable[["SanskriptVM", "Instruction"], None]]:
    from .bytecode import OpCode

    def _op(name: str) -> str | None:
        member = getattr(OpCode, name, None)
        return member.value if member is not None else None

    entries = (
        ("IMMUTABLE_LIST_NEW", _immutable_list_new),
        ("IMMUTABLE_LIST_APPEND", _immutable_list_append),
        ("IMMUTABLE_LIST_LEN", _immutable_list_len),
        ("IMMUTABLE_LIST_GET", _immutable_list_get),
        ("LIST_SCAN", _list_scan),
        ("LIST_ZIP", _list_zip),
        ("LIST_ENUMERATE", _list_enumerate),
        ("LIST_ANY", _list_any),
        ("LIST_COMPREHENSION", _list_comprehension),
        ("LAZY_ITER_NEW", _lazy_iter_new),
        ("LAZY_ITER_NEXT", _lazy_iter_next),
        ("GENERATOR_NEW", _generator_new),
        ("GENERATOR_NEXT", _generator_next),
        ("GENERATOR_YIELD", _generator_yield),
        ("PIPELINE_CHAIN", _pipeline_chain),
        ("RESULT_BIND", _result_bind),
        ("DATA_QUERY", _data_query),
        ("RULE_REGISTER", _rule_register),
        ("RULE_INVOKE", _rule_invoke),
        ("MEMO_CALL", _memo_call),
    )
    dispatch: dict[str, Callable[["SanskriptVM", "Instruction"], None]] = {}
    for name, handler in entries:
        opcode = _op(name)
        if opcode is not None:
            dispatch[opcode] = handler
    return dispatch


def _immutable_list_new(vm: SanskriptVM, _instruction: Instruction) -> None:
    vm.stack.append(ImmutableListValue())


def _immutable_list_append(vm: SanskriptVM, _instruction: Instruction) -> None:
    item = vm._pop()
    seq = vm._pop()
    base = immutable_from_sequence(seq)
    vm.stack.append(base.append(item))


def _immutable_list_len(vm: SanskriptVM, _instruction: Instruction) -> None:
    seq = vm._pop()
    vm.stack.append(len(immutable_from_sequence(seq).items))


def _immutable_list_get(vm: SanskriptVM, _instruction: Instruction) -> None:
    index = vm._pop_int()
    seq = immutable_from_sequence(vm._pop())
    items = seq.items
    if index < 0 or index >= len(items):
        raise RuntimeSanskriptError(f"Index {index} out of range for immutable list length {len(items)}")
    vm.stack.append(items[index])


def _list_scan(vm: SanskriptVM, instruction: Instruction) -> None:
    function_name = vm._expect_name(instruction.operand, instruction.opcode)
    initial = vm._pop()
    items = expect_sequence(vm._pop())
    acc = initial
    scans: list[SanskriptValue] = []
    for item in items:
        acc = vm._invoke_function(function_name, [acc, item])
        scans.append(acc)
    vm.stack.append(scans)


def _list_zip(vm: SanskriptVM, _instruction: Instruction) -> None:
    right = expect_sequence(vm._pop())
    left = expect_sequence(vm._pop())
    length = min(len(left), len(right))
    vm.stack.append([tuple([left[i], right[i]]) for i in range(length)])


def _list_enumerate(vm: SanskriptVM, _instruction: Instruction) -> None:
    items = expect_sequence(vm._pop())
    vm.stack.append([(i, items[i]) for i in range(len(items))])


def _list_any(vm: SanskriptVM, instruction: Instruction) -> None:
    function_name = vm._expect_name(instruction.operand, instruction.opcode)
    items = expect_sequence(vm._pop())
    result = 0
    for item in items:
        if is_truthy(vm._invoke_function(function_name, [item])):
            result = 1
            break
    vm.stack.append(result)


def _list_comprehension(vm: SanskriptVM, instruction: Instruction) -> None:
    """Operand packs 'where_fn,with_fn' as comma-separated names."""
    operand = vm._expect_name(instruction.operand, instruction.opcode)
    parts = [p.strip() for p in operand.split(",") if p.strip()]
    if len(parts) != 2:
        raise RuntimeSanskriptError("list_comprehension operand must be 'where_fn,with_fn'")
    where_fn, with_fn = parts
    items = expect_sequence(vm._pop())
    out: list[SanskriptValue] = []
    for item in items:
        if is_truthy(vm._invoke_function(where_fn, [item])):
            out.append(vm._invoke_function(with_fn, [item]))
    vm.stack.append(out)


def _lazy_iter_new(vm: SanskriptVM, _instruction: Instruction) -> None:
    items = tuple(expect_sequence(vm._pop()))
    vm.stack.append(LazyIteratorValue(items=items))


def _lazy_iter_next(vm: SanskriptVM, _instruction: Instruction) -> None:
    from .runtime_values import NIL

    it = vm._pop()
    if not isinstance(it, LazyIteratorValue):
        raise RuntimeSanskriptError("lazy_iter_next expects lazy iterator")
    if it.exhausted():
        vm.stack.append(0)
        vm.stack.append(NIL)
        return
    value = it.items[it.index]
    it.index += 1
    vm.stack.append(1)
    vm.stack.append(value)


def _generator_new(vm: SanskriptVM, instruction: Instruction) -> None:
    function_name = vm._expect_name(instruction.operand, instruction.opcode)
    if vm._program is None:
        raise RuntimeSanskriptError("generator_new requires program context")
    from .bytecode import resolve_call_target

    function = resolve_call_target(vm._program, function_name)
    vm.stack.append(
        GeneratorValue(
            function_name=function_name,
            params=function.params,
            bound={},
        ),
    )


def _generator_next(vm: SanskriptVM, _instruction: Instruction) -> None:
    gen = vm._pop()
    if not isinstance(gen, GeneratorValue):
        raise RuntimeSanskriptError("generator_next expects generator")
    if gen.done:
        vm.stack.append(0)
        from .runtime_values import NIL

        vm.stack.append(NIL)
        return
    value = vm._resume_generator(gen)
    if gen.done:
        vm.stack.append(0)
        vm.stack.append(value)
    else:
        vm.stack.append(1)
        vm.stack.append(value)


def _generator_yield(vm: SanskriptVM, _instruction: Instruction) -> None:
    vm._generator_yield_value = vm._pop()


def _pipeline_chain(vm: SanskriptVM, instruction: Instruction) -> None:
    operand = vm._expect_name(instruction.operand, instruction.opcode)
    steps = [s.strip() for s in operand.split(",") if s.strip()]
    items = expect_sequence(vm._pop())
    current: list[SanskriptValue] = items
    for step in steps:
        current = [vm._invoke_function(step, [item]) for item in current]
    vm.stack.append(current)


def _result_bind(vm: SanskriptVM, instruction: Instruction) -> None:
    from .runtime_values import ResultValue, expect_result

    function_name = vm._expect_name(instruction.operand, instruction.opcode)
    result = expect_result(vm._pop())
    if not result.ok:
        vm.stack.append(result)
        return
    bound = vm._invoke_function(function_name, [result.value])
    vm.stack.append(ResultValue(ok=True, value=bound))


def _data_query(vm: SanskriptVM, instruction: Instruction) -> None:
    """Operand: 'field_name,predicate_fn'."""
    operand = vm._expect_name(instruction.operand, instruction.opcode)
    parts = [p.strip() for p in operand.split(",") if p.strip()]
    if len(parts) != 2:
        raise RuntimeSanskriptError("data_query operand must be 'field,predicate_fn'")
    field_name, predicate_fn = parts
    items = expect_sequence(vm._pop())
    matches: list[SanskriptValue] = []
    for item in items:
        if isinstance(item, dict):
            payload = item.get(field_name)
        elif hasattr(item, "fields"):
            payload = item.fields.get(field_name)  # type: ignore[attr-defined]
        else:
            payload = None
        if payload is not None and is_truthy(vm._invoke_function(predicate_fn, [payload])):
            matches.append(item)
    vm.stack.append(matches)


def _rule_register(vm: SanskriptVM, instruction: Instruction) -> None:
    operand = vm._expect_name(instruction.operand, instruction.opcode)
    parts = [p.strip() for p in operand.split(",") if p.strip()]
    if len(parts) != 3:
        raise RuntimeSanskriptError("rule_register operand must be 'id,when_fn,then_fn'")
    rule_id, when_name, then_name = parts
    register_rule(RuleValue(rule_id=rule_id, when_name=when_name, then_name=then_name))


def _rule_invoke(vm: SanskriptVM, instruction: Instruction) -> None:
    rule_id = vm._expect_name(instruction.operand, instruction.opcode)
    context = vm._pop()
    rule = get_rule(rule_id)
    if rule is None:
        raise RuntimeSanskriptError(f"Unknown rule {rule_id!r}")
    if is_truthy(vm._invoke_function(rule.when_name, [context])):
        vm.stack.append(vm._invoke_function(rule.then_name, [context]))
    else:
        vm.stack.append(context)


def _memo_call(vm: SanskriptVM, instruction: Instruction) -> None:
    function_name = vm._expect_name(instruction.operand, instruction.opcode)
    args = vm._pop()
    if not isinstance(args, list):
        args = [args]
    key = (function_name, tuple(args))
    cache = _MEMO_CACHES.setdefault(function_name, {})
    if key in cache:
        vm.stack.append(cache[key])
        return
    result = vm._invoke_function(function_name, list(args))
    cache[key] = result
    vm.stack.append(result)


PHASE8_DISPATCH = build_phase8_dispatch()
