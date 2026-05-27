"""Phase 3 VM opcode dispatch table (fixed-width, collections, numerics)."""

from __future__ import annotations

import math
from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING, Any, Callable

from .bytecode import Instruction, OpCode
from .errors import RuntimeSanskriptError
from .fixed_width import (
    SPEC_BY_ADD_CHECKED,
    SPEC_BY_ADD_SATURATING,
    SPEC_BY_ADD_WRAPPING,
    SPEC_BY_PUSH_OPCODE,
    ArithmeticMode,
    FixedIntValue,
    FixedWidthSpec,
    apply_add,
)
from .phase3_values import (
    ComplexValue,
    CounterValue,
    DecimalValue,
    DefaultMapValue,
    EnumValue,
    FrozenSetValue,
    GraphValue,
    MinHeapValue,
    NamedTupleValue,
    OrderedMapValue,
    PriorityQueueValue,
    QueueValue,
    RationalValue,
    ResourceHandle,
    ScalarValue,
    StackValue,
    TaggedUnionValue,
    TreeNode,
    TreeValue,
    TypedErrorValue,
    text_grapheme_len,
)
from .runtime_values import (
    BigIntValue,
    ByteArrayValue,
    BytesValue,
    DequeValue,
    I32Value,
    OptionValue,
    OpaqueHandle,
    ResultValue,
    SetValue,
    TupleValue,
    U32Value,
    set_add_unique,
    values_equal,
)

if TYPE_CHECKING:
    from .vm import SanskriptVM


Handler = Callable[["SanskriptVM", Instruction], None]


def _pop_fixed(vm: SanskriptVM, spec: FixedWidthSpec) -> int:
    value = vm._pop()
    if isinstance(value, FixedIntValue):
        if value.spec.name != spec.name:
            raise RuntimeSanskriptError(
                f"expected {spec.name}, got {value.spec.name}"
            )
        return value.value
    if isinstance(value, I32Value) and spec.name == "i32":
        return value.value
    if isinstance(value, U32Value) and spec.name == "u32":
        return value.value
    raise RuntimeSanskriptError(f"expected {spec.name}, got {type(value).__name__}")


def _make_push(spec: FixedWidthSpec) -> Handler:
    def handler(vm: SanskriptVM, instruction: Instruction) -> None:
        value = vm._expect_int(instruction.operand, _op(spec.push_opcode))
        try:
            spec.validate_literal(value)
        except ValueError as exc:
            raise RuntimeSanskriptError(str(exc)) from exc
        vm.stack.append(FixedIntValue(spec, value))

    return handler


def _make_add(spec: FixedWidthSpec, mode: ArithmeticMode) -> Handler:  # noqa: E302
    def handler(vm: SanskriptVM, instruction: Instruction) -> None:
        right = _pop_fixed(vm, spec)
        left = _pop_fixed(vm, spec)
        try:
            result = apply_add(spec, left, right, mode)
        except OverflowError as exc:
            raise RuntimeSanskriptError(str(exc)) from exc
        vm.stack.append(FixedIntValue(spec, result))

    return handler


def _legacy_push_i32(vm: SanskriptVM, instruction: Instruction) -> None:
    from .fixed_width import I32_SPEC

    value = vm._expect_int(instruction.operand, _op("push_i32"))
    try:
        I32_SPEC.validate_literal(value)
    except ValueError as exc:
        raise RuntimeSanskriptError(str(exc)) from exc
    vm.stack.append(I32Value(value))


def _legacy_push_u32(vm: SanskriptVM, instruction: Instruction) -> None:
    from .fixed_width import U32_SPEC

    value = vm._expect_int(instruction.operand, _op("push_u32"))
    try:
        U32_SPEC.validate_literal(value)
    except ValueError as exc:
        raise RuntimeSanskriptError(str(exc)) from exc
    vm.stack.append(U32Value(value))


def _legacy_i32_add(vm: SanskriptVM, instruction: Instruction, mode: ArithmeticMode) -> None:
    from .fixed_width import I32_SPEC

    right = vm._pop()
    left = vm._pop()
    lv = left.value if isinstance(left, (I32Value, FixedIntValue)) else int(left)  # type: ignore[arg-type]
    rv = right.value if isinstance(right, (I32Value, FixedIntValue)) else int(right)  # type: ignore[arg-type]
    try:
        result = apply_add(I32_SPEC, lv, rv, mode)
    except OverflowError as exc:
        raise RuntimeSanskriptError(str(exc)) from exc
    vm.stack.append(I32Value(result))


def _op(name: str) -> OpCode:
    return OpCode(name)


def build_phase3_dispatch() -> dict[OpCode, Handler]:
    table: dict[OpCode, Handler] = {}

    for spec in SPEC_BY_PUSH_OPCODE.values():
        table[_op(spec.push_opcode)] = _make_push(spec)
    for spec in SPEC_BY_ADD_CHECKED.values():
        table[_op(spec.add_checked_opcode)] = _make_add(spec, ArithmeticMode.CHECKED)
    for spec in SPEC_BY_ADD_WRAPPING.values():
        table[_op(spec.add_wrapping_opcode)] = _make_add(spec, ArithmeticMode.WRAPPING)
    for spec in SPEC_BY_ADD_SATURATING.values():
        table[_op(spec.add_saturating_opcode)] = _make_add(spec, ArithmeticMode.SATURATING)

    table[_op("push_i32")] = _legacy_push_i32
    table[_op("push_u32")] = _legacy_push_u32
    table[_op("i32_add_checked")] = lambda vm, i: _legacy_i32_add(vm, i, ArithmeticMode.CHECKED)
    table[_op("u32_add_checked")] = lambda vm, i: _legacy_u32_add(vm, i, ArithmeticMode.CHECKED)
    table[_op("i32_add_wrapping")] = lambda vm, i: _legacy_i32_add(vm, i, ArithmeticMode.WRAPPING)
    table[_op("u32_add_wrapping")] = lambda vm, i: _legacy_u32_add(vm, i, ArithmeticMode.WRAPPING)
    table[_op("i32_add_saturating")] = lambda vm, i: _legacy_i32_add(vm, i, ArithmeticMode.SATURATING)
    table[_op("u32_add_saturating")] = lambda vm, i: _legacy_u32_add(vm, i, ArithmeticMode.SATURATING)

    # Numerics
    table[_op("push_rational")] = _push_rational
    table[_op("rational_add")] = _rational_add
    table[_op("push_decimal")] = _push_decimal
    table[_op("decimal_add")] = _decimal_add
    table[_op("push_complex")] = _push_complex
    table[_op("complex_add")] = _complex_add
    table[_op("push_scalar")] = _push_scalar
    table[_op("text_scalar_at")] = _text_scalar_at
    table[_op("text_grapheme_len")] = _text_grapheme_len_op

    # Collections / ADTs
    table[_op("frozen_set_new")] = _frozen_set_new
    table[_op("frozen_set_add")] = _frozen_set_add
    table[_op("frozen_set_len")] = _frozen_set_len
    table[_op("ordered_map_new")] = _ordered_map_new
    table[_op("ordered_map_set")] = _ordered_map_set
    table[_op("ordered_map_get")] = _ordered_map_get
    table[_op("default_map_new")] = _default_map_new
    table[_op("default_map_set")] = _default_map_set
    table[_op("default_map_get")] = _default_map_get
    table[_op("counter_new")] = _counter_new
    table[_op("counter_add")] = _counter_add
    table[_op("counter_get")] = _counter_get
    table[_op("queue_new")] = _queue_new
    table[_op("queue_enqueue")] = _queue_enqueue
    table[_op("queue_dequeue")] = _queue_dequeue
    table[_op("stack_new")] = _stack_new
    table[_op("stack_push")] = _stack_push
    table[_op("stack_pop")] = _stack_pop
    table[_op("heap_new")] = _heap_new
    table[_op("heap_push")] = _heap_push
    table[_op("heap_pop")] = _heap_pop
    table[_op("pq_new")] = _pq_new
    table[_op("pq_push")] = _pq_push
    table[_op("pq_pop")] = _pq_pop
    table[_op("tree_new")] = _tree_new
    table[_op("tree_insert")] = _tree_insert
    table[_op("tree_contains")] = _tree_contains
    table[_op("graph_new")] = _graph_new
    table[_op("graph_add_edge")] = _graph_add_edge
    table[_op("graph_has_edge")] = _graph_has_edge
    table[_op("enum_new")] = _enum_new
    table[_op("tagged_union_new")] = _tagged_union_new
    table[_op("tagged_union_tag")] = _tagged_union_tag
    table[_op("tagged_union_payload")] = _tagged_union_payload
    table[_op("typed_error_new")] = _typed_error_new
    table[_op("named_tuple_new")] = _named_tuple_new
    table[_op("named_tuple_get")] = _named_tuple_get
    table[_op("handle_new")] = _handle_new

    return table


def _legacy_u32_add(vm: SanskriptVM, instruction: Instruction, mode: ArithmeticMode) -> None:
    from .fixed_width import U32_SPEC

    right = vm._pop()
    left = vm._pop()
    lv = left.value if isinstance(left, (U32Value, FixedIntValue)) else int(left)  # type: ignore[arg-type]
    rv = right.value if isinstance(right, (U32Value, FixedIntValue)) else int(right)  # type: ignore[arg-type]
    try:
        result = apply_add(U32_SPEC, lv, rv, mode)
    except OverflowError as exc:
        raise RuntimeSanskriptError(str(exc)) from exc
    vm.stack.append(U32Value(result))


def _push_rational(vm: SanskriptVM, instruction: Instruction) -> None:
    denom = vm._pop_int()
    numer = vm._pop_int()
    try:
        vm.stack.append(RationalValue(numer, denom))
    except ValueError as exc:
        raise RuntimeSanskriptError(str(exc)) from exc


def _rational_add(vm: SanskriptVM, instruction: Instruction) -> None:
    r = vm._pop()
    l = vm._pop()
    if not isinstance(l, RationalValue) or not isinstance(r, RationalValue):
        raise RuntimeSanskriptError("rational_add expects rational values")
    result = l.as_fraction() + r.as_fraction()
    vm.stack.append(RationalValue(result.numerator, result.denominator))


def _push_decimal(vm: SanskriptVM, instruction: Instruction) -> None:
    text = vm._expect_text(instruction.operand, _op("push_decimal"))
    vm.stack.append(DecimalValue(Decimal(text)))


def _decimal_add(vm: SanskriptVM, instruction: Instruction) -> None:
    r = vm._pop()
    l = vm._pop()
    if not isinstance(l, DecimalValue) or not isinstance(r, DecimalValue):
        raise RuntimeSanskriptError("decimal_add expects decimal values")
    vm.stack.append(DecimalValue(l.value + r.value))


def _push_complex(vm: SanskriptVM, instruction: Instruction) -> None:
    imag = vm._pop()
    real = vm._pop()
    if not isinstance(real, (int, float)) or not isinstance(imag, (int, float)):
        raise RuntimeSanskriptError("push_complex expects numeric real/imag")
    vm.stack.append(ComplexValue(float(real), float(imag)))


def _complex_add(vm: SanskriptVM, instruction: Instruction) -> None:
    r = vm._pop()
    l = vm._pop()
    if not isinstance(l, ComplexValue) or not isinstance(r, ComplexValue):
        raise RuntimeSanskriptError("complex_add expects complex values")
    c = l.as_complex() + r.as_complex()
    vm.stack.append(ComplexValue(c.real, c.imag))


def _push_scalar(vm: SanskriptVM, instruction: Instruction) -> None:
    cp = vm._expect_int(instruction.operand, _op("push_scalar"))
    try:
        vm.stack.append(ScalarValue(cp))
    except ValueError as exc:
        raise RuntimeSanskriptError(str(exc)) from exc


def _text_scalar_at(vm: SanskriptVM, instruction: Instruction) -> None:
    from .runtime_values import expect_text

    index = vm._pop_int()
    text = expect_text(vm._pop())
    if index < 0 or index >= len(text):
        raise RuntimeSanskriptError(f"scalar index out of range: {index}")
    vm.stack.append(ScalarValue(ord(text[index])))


def _text_grapheme_len_op(vm: SanskriptVM, instruction: Instruction) -> None:
    from .runtime_values import expect_text

    vm.stack.append(text_grapheme_len(expect_text(vm._pop())))


def _frozen_set_new(vm: SanskriptVM, instruction: Instruction) -> None:
    vm.stack.append(FrozenSetValue(items=()))


def _frozen_set_add(vm: SanskriptVM, instruction: Instruction) -> None:
    item = vm._pop()
    target = vm._pop()
    if not isinstance(target, FrozenSetValue):
        raise RuntimeSanskriptError("expected frozen set")
    items = list(target.items)
    if not any(values_equal(item, existing) for existing in items):
        items.append(item)
    vm.stack.append(FrozenSetValue(items=tuple(items)))


def _frozen_set_len(vm: SanskriptVM, instruction: Instruction) -> None:
    target = vm._pop()
    if not isinstance(target, FrozenSetValue):
        raise RuntimeSanskriptError("expected frozen set")
    vm.stack.append(len(target.items))


def _ordered_map_new(vm: SanskriptVM, instruction: Instruction) -> None:
    vm.stack.append(OrderedMapValue())


def _ordered_map_set(vm: SanskriptVM, instruction: Instruction) -> None:
    from .runtime_values import expect_text, map_key_from_value

    val = vm._pop()
    key = map_key_from_value(vm._pop())
    target = vm._pop()
    if not isinstance(target, OrderedMapValue):
        raise RuntimeSanskriptError("expected ordered map")
    target.entries[key] = val
    vm.stack.append(target)


def _ordered_map_get(vm: SanskriptVM, instruction: Instruction) -> None:
    from .runtime_values import map_key_from_value

    key = map_key_from_value(vm._pop())
    target = vm._pop()
    if not isinstance(target, OrderedMapValue):
        raise RuntimeSanskriptError("expected ordered map")
    if key not in target.entries:
        raise RuntimeSanskriptError(f"ordered map key not found: {key!r}")
    vm.stack.append(target.entries[key])


def _default_map_new(vm: SanskriptVM, instruction: Instruction) -> None:
    default = vm._pop()
    vm.stack.append(DefaultMapValue(default=default))


def _default_map_set(vm: SanskriptVM, instruction: Instruction) -> None:
    from .runtime_values import map_key_from_value

    val = vm._pop()
    key = map_key_from_value(vm._pop())
    target = vm._pop()
    if not isinstance(target, DefaultMapValue):
        raise RuntimeSanskriptError("expected default map")
    target.entries[key] = val
    vm.stack.append(target)


def _default_map_get(vm: SanskriptVM, instruction: Instruction) -> None:
    from .runtime_values import map_key_from_value

    key = map_key_from_value(vm._pop())
    target = vm._pop()
    if not isinstance(target, DefaultMapValue):
        raise RuntimeSanskriptError("expected default map")
    vm.stack.append(target.entries.get(key, target.default))


def _counter_new(vm: SanskriptVM, instruction: Instruction) -> None:
    vm.stack.append(CounterValue())


def _counter_add(vm: SanskriptVM, instruction: Instruction) -> None:
    item = vm._pop()
    target = vm._pop()
    if not isinstance(target, CounterValue):
        raise RuntimeSanskriptError("expected counter")
    target.counts[item] += 1
    vm.stack.append(target)


def _counter_get(vm: SanskriptVM, instruction: Instruction) -> None:
    item = vm._pop()
    target = vm._pop()
    if not isinstance(target, CounterValue):
        raise RuntimeSanskriptError("expected counter")
    vm.stack.append(target.counts[item])


def _queue_new(vm: SanskriptVM, instruction: Instruction) -> None:
    vm.stack.append(QueueValue())


def _queue_enqueue(vm: SanskriptVM, instruction: Instruction) -> None:
    item = vm._pop()
    target = vm._pop()
    if not isinstance(target, QueueValue):
        raise RuntimeSanskriptError("expected queue")
    target.items.append(item)
    vm.stack.append(target)


def _queue_dequeue(vm: SanskriptVM, instruction: Instruction) -> None:
    target = vm._pop()
    if not isinstance(target, QueueValue):
        raise RuntimeSanskriptError("expected queue")
    if not target.items:
        raise RuntimeSanskriptError("queue_dequeue on empty queue")
    vm.stack.append(target.items.popleft())


def _stack_new(vm: SanskriptVM, instruction: Instruction) -> None:
    vm.stack.append(StackValue())


def _stack_push(vm: SanskriptVM, instruction: Instruction) -> None:
    item = vm._pop()
    target = vm._pop()
    if not isinstance(target, StackValue):
        raise RuntimeSanskriptError("expected stack")
    target.items.append(item)
    vm.stack.append(target)


def _stack_pop(vm: SanskriptVM, instruction: Instruction) -> None:
    target = vm._pop()
    if not isinstance(target, StackValue):
        raise RuntimeSanskriptError("expected stack")
    if not target.items:
        raise RuntimeSanskriptError("stack_pop on empty stack")
    vm.stack.append(target.items.pop())


def _heap_new(vm: SanskriptVM, instruction: Instruction) -> None:
    vm.stack.append(MinHeapValue())


def _heap_push(vm: SanskriptVM, instruction: Instruction) -> None:
    item = vm._pop()
    target = vm._pop()
    if not isinstance(target, MinHeapValue):
        raise RuntimeSanskriptError("expected heap")
    target.push(item)
    vm.stack.append(target)


def _heap_pop(vm: SanskriptVM, instruction: Instruction) -> None:
    target = vm._pop()
    if not isinstance(target, MinHeapValue):
        raise RuntimeSanskriptError("expected heap")
    if not target._heap:
        raise RuntimeSanskriptError("heap_pop on empty heap")
    vm.stack.append(target.pop())


def _pq_new(vm: SanskriptVM, instruction: Instruction) -> None:
    vm.stack.append(PriorityQueueValue())


def _pq_push(vm: SanskriptVM, instruction: Instruction) -> None:
    item = vm._pop()
    priority = vm._pop_int()
    target = vm._pop()
    if not isinstance(target, PriorityQueueValue):
        raise RuntimeSanskriptError("expected priority queue")
    target.push(priority, item)
    vm.stack.append(target)


def _pq_pop(vm: SanskriptVM, instruction: Instruction) -> None:
    target = vm._pop()
    if not isinstance(target, PriorityQueueValue):
        raise RuntimeSanskriptError("expected priority queue")
    if not target._heap:
        raise RuntimeSanskriptError("pq_pop on empty priority queue")
    vm.stack.append(target.pop())


def _tree_new(vm: SanskriptVM, instruction: Instruction) -> None:
    vm.stack.append(TreeValue())


def _tree_insert(vm: SanskriptVM, instruction: Instruction) -> None:
    key = vm._pop()
    target = vm._pop()
    if not isinstance(target, TreeValue):
        raise RuntimeSanskriptError("expected tree")

    def insert(node: TreeNode | None, k: Any) -> TreeNode:
        if node is None:
            return TreeNode(k)
        if k < node.key:
            node.left = insert(node.left, k)
        elif k > node.key:
            node.right = insert(node.right, k)
        return node

    target.root = insert(target.root, key)
    vm.stack.append(target)


def _tree_contains(vm: SanskriptVM, instruction: Instruction) -> None:
    key = vm._pop()
    target = vm._pop()
    if not isinstance(target, TreeValue):
        raise RuntimeSanskriptError("expected tree")

    def contains(node: TreeNode | None, k: Any) -> bool:
        if node is None:
            return False
        if k == node.key:
            return True
        if k < node.key:
            return contains(node.left, k)
        return contains(node.right, k)

    vm.stack.append(1 if contains(target.root, key) else 0)


def _graph_new(vm: SanskriptVM, instruction: Instruction) -> None:
    vm.stack.append(GraphValue())


def _graph_add_edge(vm: SanskriptVM, instruction: Instruction) -> None:
    to_node = vm._pop()
    from_node = vm._pop()
    target = vm._pop()
    if not isinstance(target, GraphValue):
        raise RuntimeSanskriptError("expected graph")
    target.nodes.add(from_node)
    target.nodes.add(to_node)
    target.edges.add((from_node, to_node))
    vm.stack.append(target)


def _graph_has_edge(vm: SanskriptVM, instruction: Instruction) -> None:
    to_node = vm._pop()
    from_node = vm._pop()
    target = vm._pop()
    if not isinstance(target, GraphValue):
        raise RuntimeSanskriptError("expected graph")
    vm.stack.append(1 if (from_node, to_node) in target.edges else 0)


def _enum_new(vm: SanskriptVM, instruction: Instruction) -> None:
    from .runtime_values import expect_text

    type_name = vm._expect_name(instruction.operand, _op("enum_new"))
    payload = vm._pop()
    variant = expect_text(vm._pop())
    vm.stack.append(EnumValue(type_name, variant, payload))


def _tagged_union_new(vm: SanskriptVM, instruction: Instruction) -> None:
    tag = vm._expect_name(instruction.operand, _op("tagged_union_new"))
    payload = vm._pop()
    vm.stack.append(TaggedUnionValue(tag, payload))


def _tagged_union_tag(vm: SanskriptVM, instruction: Instruction) -> None:
    value = vm._pop()
    if not isinstance(value, TaggedUnionValue):
        raise RuntimeSanskriptError("expected tagged union")
    vm.stack.append(value.tag)


def _tagged_union_payload(vm: SanskriptVM, instruction: Instruction) -> None:
    value = vm._pop()
    if not isinstance(value, TaggedUnionValue):
        raise RuntimeSanskriptError("expected tagged union")
    vm.stack.append(value.payload)


def _typed_error_new(vm: SanskriptVM, instruction: Instruction) -> None:
    code = vm._expect_name(instruction.operand, _op("typed_error_new"))
    message = vm._pop()
    vm.stack.append(TypedErrorValue(code, str(message)))


def _named_tuple_new(vm: SanskriptVM, instruction: Instruction) -> None:
    arity = vm._expect_int(instruction.operand, _op("named_tuple_new"))
    names = [
        vm._expect_name(vm._pop(), _op("named_tuple_new")) for _ in range(arity)
    ]
    names.reverse()
    items = [vm._pop() for _ in range(arity)]
    items.reverse()
    vm.stack.append(NamedTupleValue(field_names=tuple(names), items=tuple(items)))


def _named_tuple_get(vm: SanskriptVM, instruction: Instruction) -> None:
    field = vm._expect_name(instruction.operand, _op("named_tuple_get"))
    value = vm._pop()
    if not isinstance(value, NamedTupleValue):
        raise RuntimeSanskriptError("expected named tuple")
    try:
        index = value.field_names.index(field)
    except ValueError as exc:
        raise RuntimeSanskriptError(f"named tuple has no field {field!r}") from exc
    vm.stack.append(value.items[index])


def _handle_new(vm: SanskriptVM, instruction: Instruction) -> None:
    kind = vm._expect_name(instruction.operand, _op("handle_new"))
    handle_id = vm._pop_int()
    vm.stack.append(ResourceHandle(kind, handle_id))


PHASE3_DISPATCH: dict[OpCode, Handler] = build_phase3_dispatch()
