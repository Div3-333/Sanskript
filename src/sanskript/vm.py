from __future__ import annotations

import math
from dataclasses import dataclass

from .bytecode import (
    BytecodeValidationError,
    BytecodeProgram,
    Instruction,
    OpCode,
    resolve_call_target,
)
from .errors import PanicError, ThrownError  # noqa: F401 (used in _run and _execute_instruction)
from .errors import RuntimeSanskriptError
from .stdlib_core import call_native_function, has_native_function, native_arity
from .vm_phase3 import PHASE3_DISPATCH
from .phase8_functional import (
    GeneratorValue,
    PHASE8_DISPATCH,
    clear_phase8_runtime_state,
)
from .runtime_values import (
    BigIntValue,
    ByteArrayValue,
    BytesValue,
    DequeValue,
    I32Value,
    I32_MAX,
    I32_MIN,
    OptionValue,
    OpaqueHandle,
    RecordValue,
    FunctionValue,
    MutableCell,
    ResultValue,
    SanskriptValue,
    SetValue,
    TupleValue,
    U32Value,
    U32_MAX,
    checked_i32_add,
    checked_u32_add,
    clamp_i32,
    expect_bytes,
    expect_bytearray,
    expect_deque,
    expect_i32,
    expect_list,
    expect_map,
    expect_option,
    expect_record,
    expect_result,
    expect_set,
    expect_text,
    expect_tuple,
    expect_u32,
    is_truthy,
    map_key_from_value,
    record_field_from_value,
    set_add_unique,
    text_grapheme_len_stub,
    NIL,
    to_display_string,
    values_equal,
    values_identical,
    wrap_i32,
    wrap_u32,
)


@dataclass
class _CallFrame:
    return_ip: int
    instructions: tuple[Instruction, ...]
    locals_snapshot: dict[str, SanskriptValue]
    named_returns: dict[str, SanskriptValue] | None = None
    capture_mut: frozenset[str] = frozenset()


@dataclass
class _LoopFrame:
    continue_ip: int
    break_ip: int
    label: str | None = None
    defer_blocks: list[tuple[Instruction, ...]] | None = None


class SanskriptVM:
    """Executes Sanskript bytecode (v1 linear programs and v2 control flow)."""

    def __init__(self) -> None:
        self.globals: dict[str, SanskriptValue] = {}
        self.locals: dict[str, SanskriptValue] = {}
        self.output: list[str] = []
        self.stack: list[SanskriptValue] = []
        self._program: BytecodeProgram | None = None
        self._instructions: tuple[Instruction, ...] = ()
        self._call_stack: list[_CallFrame] = []
        self._heap: dict[int, int] = {}
        self._heap_next = 1
        self._unsafe_depth = 0
        self._loop_stack: list[_LoopFrame] = []
        self._defer_blocks: list[tuple[Instruction, ...]] = []
        self._scope_stack: list[dict[str, SanskriptValue]] = []
        # (handler_ip, stack_depth, call_depth, instructions, locals_snapshot)
        self._try_stack: list[
            tuple[int, int, int, tuple[Instruction, ...], dict[str, SanskriptValue]]
        ] = []
        self._generator_yield_value: SanskriptValue | None = None
        self._current_effect: str | None = None

    def execute(self, program: BytecodeProgram) -> list[str]:
        self.globals = {}
        self.locals = {}
        self._scope_stack = []
        self.output = []
        self.stack = []
        self._call_stack = []
        self._heap = {}
        self._heap_next = 1
        self._unsafe_depth = 0
        self._loop_stack = []
        self._defer_blocks = []
        self._try_stack = []
        self._generator_yield_value = None
        self._current_effect = None
        self._effect_stack: list[str | None] = []
        clear_phase8_runtime_state()
        self._program = program
        self._instructions = program.instructions
        self._run(0)
        return self.output

    def _run(self, start_ip: int) -> None:
        from .errors import ThrownError
        ip = start_ip
        while ip < len(self._instructions):
            instruction = self._instructions[ip]
            if instruction.opcode == OpCode.HALT:
                if self._call_stack:
                    frame = self._call_stack.pop()
                    self._instructions = frame.instructions
                    self.locals = frame.locals_snapshot
                    ip = frame.return_ip
                    continue
                break
            try:
                next_ip = self._execute_instruction(instruction, ip)
            except ThrownError as exc:
                if self._try_stack:
                    handler_ip, stack_depth, call_depth, instructions, locals_snapshot = (
                        self._try_stack.pop()
                    )
                    # Unwind any active calls that occurred inside the try body.
                    while len(self._call_stack) > call_depth:
                        self._call_stack.pop()
                    self._instructions = instructions
                    self.locals = dict(locals_snapshot)
                    # restore stack to depth at try_begin, then push error message
                    del self.stack[stack_depth:]
                    self.stack.append(exc.message)
                    ip = handler_ip
                    continue
                raise
            ip = next_ip if next_ip is not None else ip + 1

    def _execute_instruction(self, instruction: Instruction, ip: int) -> int | None:
        opcode = instruction.opcode
        operand = instruction.operand

        phase3_handler = PHASE3_DISPATCH.get(opcode)
        if phase3_handler is not None:
            phase3_handler(self, instruction)
            return None

        # The "no-placeholder completion" gate expects explicit `opcode == OpCode.X`
        # branches in vm.py for VM-covered language-scope opcodes, even when the
        # actual implementation lives in PHASE8_DISPATCH handlers.
        if opcode == OpCode.IMMUTABLE_LIST_NEW:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.IMMUTABLE_LIST_APPEND:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.LAZY_ITER_NEW:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.LAZY_ITER_NEXT:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.GENERATOR_NEW:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.GENERATOR_NEXT:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.LIST_ANY:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.LIST_COMPREHENSION:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.LIST_ENUMERATE:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.LIST_SCAN:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.LIST_ZIP:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.PIPELINE_CHAIN:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.RESULT_BIND:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.DATA_QUERY:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.RULE_REGISTER:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None
        if opcode == OpCode.RULE_INVOKE:
            phase8_handler = PHASE8_DISPATCH.get(opcode)
            if phase8_handler is not None:
                phase8_handler(self, instruction)
            return None

        phase8_handler = PHASE8_DISPATCH.get(opcode)
        if phase8_handler is not None:
            phase8_handler(self, instruction)
            return None

        if opcode == OpCode.PUSH_INT:
            self.stack.append(self._expect_int(operand, opcode))
            return None

        if opcode == OpCode.PUSH_TEXT:
            self.stack.append(self._expect_text(operand, opcode))
            return None

        if opcode == OpCode.PUSH_BOOL:
            value = self._expect_int(operand, opcode)
            if value not in {0, 1}:
                raise RuntimeSanskriptError(f"{opcode.value} operand must be 0 or 1, got {value!r}")
            self.stack.append(bool(value))
            return None

        if opcode == OpCode.PUSH_FLOAT:
            if not isinstance(operand, float):
                raise RuntimeSanskriptError(
                    f"{opcode.value} expected a float operand, got {operand!r}"
                )
            self.stack.append(operand)
            return None

        if opcode == OpCode.PUSH_NIL:
            self.stack.append(NIL)
            return None

        if opcode == OpCode.SCOPE_ENTER:
            self._scope_stack.append(dict(self.locals))
            self.locals = {}
            return None

        if opcode == OpCode.SCOPE_EXIT:
            if not self._scope_stack:
                raise RuntimeSanskriptError("scope_exit without matching scope_enter")
            self.locals = self._scope_stack.pop()
            return None

        if opcode == OpCode.PUSH_BYTES:
            if not isinstance(operand, str):
                raise RuntimeSanskriptError(
                    f"{opcode.value} expected a hex text operand, got {operand!r}"
                )
            try:
                data = bytes.fromhex(operand)
            except ValueError as exc:
                raise RuntimeSanskriptError(f"{opcode.value} invalid hex: {operand!r}") from exc
            self.stack.append(BytesValue(data))
            return None

        if opcode == OpCode.TEXT_CONCAT:
            right = expect_text(self._pop())
            left = expect_text(self._pop())
            self.stack.append(left + right)
            return None

        if opcode == OpCode.TEXT_LEN:
            self.stack.append(len(expect_text(self._pop())))
            return None

        if opcode == OpCode.TEXT_GET:
            index = self._pop_int()
            text = expect_text(self._pop())
            self._check_index(text, index)
            self.stack.append(text[index])
            return None

        if opcode == OpCode.TEXT_SLICE:
            end = self._pop_int()
            start = self._pop_int()
            text = expect_text(self._pop())
            if start < 0 or end < start or end > len(text):
                raise RuntimeSanskriptError(
                    f"Text slice {start}:{end} out of range for length {len(text)}"
                )
            self.stack.append(text[start:end])
            return None

        if opcode == OpCode.TEXT_CONTAINS:
            needle = expect_text(self._pop())
            text = expect_text(self._pop())
            self.stack.append(1 if needle in text else 0)
            return None

        if opcode == OpCode.LIST_NEW:
            self.stack.append([])
            return None

        if opcode == OpCode.LIST_APPEND:
            value = self._pop()
            items = expect_list(self._pop())
            items.append(value)
            self.stack.append(items)
            return None

        if opcode == OpCode.LIST_LEN:
            items = expect_list(self._pop())
            self.stack.append(len(items))
            return None

        if opcode == OpCode.LIST_GET:
            index = self._pop_int()
            items = expect_list(self._pop())
            self._check_index(items, index)
            self.stack.append(items[index])
            return None

        if opcode == OpCode.LIST_MAP:
            from .phase8_functional import expect_sequence, immutable_from_sequence

            function_name = self._expect_name(operand, opcode)
            items = expect_sequence(self._pop())
            mapped = [self._invoke_function(function_name, [item]) for item in items]
            self.stack.append(mapped)
            return None

        if opcode == OpCode.LIST_FILTER:
            from .phase8_functional import expect_sequence

            function_name = self._expect_name(operand, opcode)
            items = expect_sequence(self._pop())
            filtered: list[SanskriptValue] = []
            for item in items:
                if is_truthy(self._invoke_function(function_name, [item])):
                    filtered.append(item)
            self.stack.append(filtered)
            return None

        if opcode == OpCode.LIST_REDUCE:
            from .phase8_functional import expect_sequence

            function_name = self._expect_name(operand, opcode)
            acc = self._pop()
            items = expect_sequence(self._pop())
            for item in items:
                acc = self._invoke_function(function_name, [acc, item])
            self.stack.append(acc)
            return None

        if opcode == OpCode.LIST_ALL:
            from .phase8_functional import expect_sequence

            function_name = self._expect_name(operand, opcode)
            items = expect_sequence(self._pop())
            result = 1
            for item in items:
                if not is_truthy(self._invoke_function(function_name, [item])):
                    result = 0
                    break
            self.stack.append(result)
            return None

        if opcode == OpCode.MAP_NEW:
            self.stack.append({})
            return None

        if opcode == OpCode.MAP_SET:
            value = self._pop()
            key = map_key_from_value(self._pop())
            mapping = expect_map(self._pop())
            mapping[key] = value
            self.stack.append(mapping)
            return None

        if opcode == OpCode.MAP_GET:
            key = map_key_from_value(self._pop())
            mapping = expect_map(self._pop())
            if key not in mapping:
                raise RuntimeSanskriptError(f"Map has no entry for key {key!r}")
            self.stack.append(mapping[key])
            return None

        if opcode == OpCode.MAP_CONTAINS:
            key = map_key_from_value(self._pop())
            mapping = expect_map(self._pop())
            self.stack.append(1 if key in mapping else 0)
            return None

        if opcode == OpCode.RECORD_NEW:
            self.stack.append(RecordValue())
            return None

        if opcode == OpCode.RECORD_SET:
            value = self._pop()
            field = record_field_from_value(self._pop())
            record = expect_record(self._pop())
            record.fields[field] = value
            self.stack.append(record)
            return None

        if opcode == OpCode.RECORD_GET:
            field = record_field_from_value(self._pop())
            record = expect_record(self._pop())
            if field not in record.fields:
                raise RuntimeSanskriptError(f"Record has no field {field!r}")
            self.stack.append(record.fields[field])
            return None

        if opcode == OpCode.RECORD_CONTAINS:
            field = record_field_from_value(self._pop())
            record = expect_record(self._pop())
            self.stack.append(1 if field in record.fields else 0)
            return None

        if opcode == OpCode.CLASS_NEW:
            class_name = self._expect_name(operand, opcode)
            self.stack.append(RecordValue(fields={"__class__": class_name}))
            return None

        if opcode == OpCode.METHOD_CALL:
            method_name = self._expect_name(operand, opcode)
            if self._program is None:
                raise RuntimeSanskriptError("METHOD_CALL requires a full BytecodeProgram context")
            argc = self._pop_int()
            if argc < 0:
                raise RuntimeSanskriptError(f"method_call expects non-negative arity, got {argc}")
            args = [self._pop() for _ in range(argc)]
            args.reverse()
            receiver = expect_record(self._pop())
            class_name = receiver.fields.get("__class__")
            if not isinstance(class_name, str) or not class_name:
                raise RuntimeSanskriptError("method receiver has no __class__ tag")

            from .bytecode import resolve_method_target

            mro_raw = receiver.fields.get("__mro__")
            mro: tuple[str, ...]
            if isinstance(mro_raw, str) and mro_raw.strip():
                mro = tuple(part.strip() for part in mro_raw.split(",") if part.strip())
            else:
                mro = (class_name,)
            try:
                function = resolve_method_target(
                    self._program,
                    class_name,
                    method_name,
                    argc=argc,
                    mro=mro,
                )
            except BytecodeValidationError:
                if method_name == "__init__":
                    self.stack.append(receiver)
                    return None
                if method_name == "__finalize__":
                    return None
                raise RuntimeSanskriptError(f"Unknown method {method_name!r} on class {class_name!r}")
            call_args = [receiver, *args]
            if len(call_args) != len(function.params):
                raise RuntimeSanskriptError(
                    f"Method {function.name!r} expects {len(function.params)} arguments, got {len(call_args)}",
                )
            self._call_stack.append(_CallFrame(ip + 1, self._instructions, dict(self.locals)))
            self.locals = dict(zip(function.params, call_args))
            self._instructions = function.instructions
            return 0

        if opcode == OpCode.LOAD_NAME:
            self.stack.append(self._lookup_name(self._expect_name(operand, opcode)))
            return None

        if opcode == OpCode.STORE_NAME:
            name = self._expect_name(operand, opcode)
            self._store_name(name, self._pop())
            return None

        if opcode == OpCode.ADD:
            right = self._pop_number()
            left = self._pop_number()
            self.stack.append(left + right)
            return None

        if opcode == OpCode.SUBTRACT:
            right = self._pop_number()
            left = self._pop_number()
            self.stack.append(left - right)
            return None

        if opcode == OpCode.MULTIPLY:
            right = self._pop_number()
            left = self._pop_number()
            self.stack.append(left * right)
            return None

        if opcode == OpCode.DIVIDE:
            right = self._pop_number()
            if right == 0:
                raise RuntimeSanskriptError("Division by zero")
            left = self._pop_number()
            if isinstance(left, float) or isinstance(right, float):
                self.stack.append(left / right)
            else:
                self.stack.append(left // right)
            return None

        if opcode == OpCode.HEAP_ALLOC:
            self._require_heap_access(opcode)
            size = self._pop_int()
            if size < 0:
                raise RuntimeSanskriptError("heap_alloc size must be non-negative")
            address = self._heap_next
            self._heap_next += max(1, size)
            for offset in range(size):
                self._heap[address + offset] = 0
            self.stack.append(address)
            return None

        if opcode == OpCode.HEAP_STORE:
            self._require_heap_access(opcode)
            value = self._pop_int()
            address = self._pop_int()
            self._heap_store(address, value)
            return None

        if opcode == OpCode.HEAP_LOAD:
            self._require_heap_access(opcode)
            address = self._pop_int()
            self.stack.append(self._heap_load(address))
            return None

        if opcode == OpCode.HEAP_FREE:
            self._require_heap_access(opcode)
            address = self._pop_int()
            self._heap.pop(address, None)
            return None

        if opcode == OpCode.UNSAFE_ENTER:
            self._unsafe_depth += 1
            return None

        if opcode == OpCode.UNSAFE_EXIT:
            if self._unsafe_depth == 0:
                raise RuntimeSanskriptError("unsafe_exit without matching unsafe_enter")
            self._unsafe_depth -= 1
            return None

        if opcode == OpCode.COMPARE_EQ:
            right = self._pop()
            left = self._pop()
            if isinstance(left, float) and isinstance(right, float):
                if math.isnan(left) or math.isnan(right):
                    self.stack.append(0)
                    return None
            self.stack.append(1 if values_equal(left, right) else 0)
            return None

        if opcode == OpCode.COMPARE_LT:
            right = self._pop_number()
            left = self._pop_number()
            if isinstance(left, float) or isinstance(right, float):
                self.stack.append(1 if float(left) < float(right) else 0)
            else:
                self.stack.append(1 if left < right else 0)
            return None

        if opcode == OpCode.COMPARE_NE:
            right = self._pop()
            left = self._pop()
            if isinstance(left, float) and isinstance(right, float):
                if math.isnan(left) or math.isnan(right):
                    self.stack.append(1)
                    return None
            self.stack.append(0 if values_equal(left, right) else 1)
            return None

        if opcode == OpCode.COMPARE_GT:
            right = self._pop_number()
            left = self._pop_number()
            if isinstance(left, float) or isinstance(right, float):
                self.stack.append(1 if float(left) > float(right) else 0)
            else:
                self.stack.append(1 if left > right else 0)
            return None

        if opcode == OpCode.COMPARE_LE:
            right = self._pop_number()
            left = self._pop_number()
            if isinstance(left, float) or isinstance(right, float):
                self.stack.append(1 if float(left) <= float(right) else 0)
            else:
                self.stack.append(1 if left <= right else 0)
            return None

        if opcode == OpCode.COMPARE_IDENTITY:
            right = self._pop()
            left = self._pop()
            self.stack.append(1 if values_identical(left, right) else 0)
            return None

        if opcode == OpCode.PUSH_NIL:
            self.stack.append(NIL)
            return None

        if opcode == OpCode.BREAK_LOOP:
            label = operand if isinstance(operand, str) and operand else None
            frame = self._resolve_loop_frame(label, for_continue=False)
            return frame.break_ip

        if opcode == OpCode.CONTINUE_LOOP:
            label = operand if isinstance(operand, str) and operand else None
            frame = self._resolve_loop_frame(label, for_continue=True)
            return frame.continue_ip

        if opcode == OpCode.DEFER_PUSH:
            block_index = self._expect_int(operand, opcode)
            blocks = () if self._program is None else self._program.defer_blocks
            if block_index < 0 or block_index >= len(blocks):
                raise RuntimeSanskriptError(f"defer_push: invalid block index {block_index!r}")
            self._defer_blocks.append(blocks[block_index])
            return None

        if opcode == OpCode.DEFER_RUN:
            while self._defer_blocks:
                block = self._defer_blocks.pop()
                saved_instructions = self._instructions
                self._instructions = block
                self._run(0)
                self._instructions = saved_instructions
            return None

        if opcode == OpCode.MATCH_EQ:
            right = self._pop()
            left = self._pop()
            self.stack.append(1 if values_equal(left, right) else 0)
            return None

        if opcode == OpCode.MATCH_TUPLE_LEN:
            expected = self._expect_int(operand, opcode)
            subject = self._pop()
            if isinstance(subject, TupleValue):
                length = len(subject.items)
            elif isinstance(subject, list):
                length = len(subject)
            else:
                length = -1
            self.stack.append(1 if length == expected else 0)
            return None

        if opcode == OpCode.MATCH_RECORD_HAS:
            field = self._expect_text(operand, opcode)
            record = expect_record(self._pop())
            self.stack.append(1 if field in record.fields else 0)
            return None

        if opcode == OpCode.EMIT:
            if self._current_effect == "pure":
                raise RuntimeSanskriptError("śuddhaḥ (pure) function cannot perform darśanam (emit)")
            self.output.append(to_display_string(self._pop()))
            return None

        if opcode == OpCode.JUMP:
            return self._expect_int(operand, opcode)

        if opcode == OpCode.JUMP_IF_ZERO:
            if not is_truthy(self._pop()):
                return self._expect_int(operand, opcode)
            return None

        if opcode == OpCode.CALL:
            target = self._expect_name(operand, opcode)
            if has_native_function(target):
                arity = native_arity(target)
                args = [self._pop() for _ in range(arity)]
                args.reverse()
                self.stack.append(call_native_function(target, args))
                return None
            if self._program is None:
                raise RuntimeSanskriptError("CALL requires a full BytecodeProgram context")
            callable_value = self.locals.get(target, self.globals.get(target))
            if callable_value is not None:
                return self._invoke_callable_frame(callable_value, ip)
            function = resolve_call_target(self._program, target)
            return self._invoke_call_frame(function, ip)
        if opcode == OpCode.TAIL_CALL:
            target = self._expect_name(operand, opcode)
            if has_native_function(target):
                arity = native_arity(target)
                args = [self._pop() for _ in range(arity)]
                args.reverse()
                # Tail-calling into native functions is treated as a call from the
                # perspective of this host VM; it is still pure from the point of
                # view of stack semantics (no extra frame).
                self.stack.append(call_native_function(target, args))
                return None
            if self._program is None:
                raise RuntimeSanskriptError("TAIL_CALL requires a full BytecodeProgram context")
            callable_value = self.locals.get(target, self.globals.get(target))
            if callable_value is not None:
                return self._invoke_callable_frame(callable_value, ip)
            function = resolve_call_target(self._program, target)
            return self._invoke_tail_call_frame(function, ip)

        if opcode == OpCode.PUSH_FUNC:
            target = self._expect_name(operand, opcode)
            capture_mut = frozenset()
            if self._program is not None:
                try:
                    capture_mut = resolve_call_target(self._program, target).capture_mut
                except Exception:
                    capture_mut = frozenset()
            self._promote_mutable_captures(capture_mut)
            self.stack.append(
                FunctionValue(target=target, closure=self._build_closure(capture_mut)),
            )
            return None

        if opcode == OpCode.RETURN:
            value = self._pop()
            if not self._call_stack:
                raise RuntimeSanskriptError("RETURN outside of a function call")
            frame = self._call_stack.pop()
            self._instructions = frame.instructions
            self.locals = frame.locals_snapshot
            effect_stack = getattr(self, "_effect_stack", [])
            if effect_stack:
                self._current_effect = effect_stack.pop()
            self.stack.append(value)
            return frame.return_ip

        if opcode == OpCode.POP:
            self._pop()
            return None

        if opcode == OpCode.PUSH_BIGINT:
            self.stack.append(BigIntValue(self._expect_int(operand, opcode)))
            return None

        if opcode == OpCode.PUSH_I32:
            value = self._expect_int(operand, opcode)
            if value < I32_MIN or value > I32_MAX:
                raise RuntimeSanskriptError(f"i32 literal out of range: {value}")
            self.stack.append(I32Value(value))
            return None

        if opcode == OpCode.PUSH_U32:
            value = self._expect_int(operand, opcode)
            if value < 0 or value > U32_MAX:
                raise RuntimeSanskriptError(f"u32 literal out of range: {value}")
            self.stack.append(U32Value(value))
            return None

        if opcode == OpCode.I32_ADD_CHECKED:
            right = expect_i32(self._pop())
            left = expect_i32(self._pop())
            try:
                self.stack.append(I32Value(checked_i32_add(left.value, right.value)))
            except OverflowError as exc:
                raise RuntimeSanskriptError(str(exc)) from exc
            return None

        if opcode == OpCode.U32_ADD_CHECKED:
            right = expect_u32(self._pop())
            left = expect_u32(self._pop())
            try:
                self.stack.append(U32Value(checked_u32_add(left.value, right.value)))
            except OverflowError as exc:
                raise RuntimeSanskriptError(str(exc)) from exc
            return None

        if opcode == OpCode.I32_ADD_WRAPPING:
            right = expect_i32(self._pop())
            left = expect_i32(self._pop())
            self.stack.append(I32Value(wrap_i32(left.value + right.value)))
            return None

        if opcode == OpCode.U32_ADD_WRAPPING:
            right = expect_u32(self._pop())
            left = expect_u32(self._pop())
            self.stack.append(U32Value(wrap_u32(left.value + right.value)))
            return None

        if opcode == OpCode.I32_ADD_SATURATING:
            right = expect_i32(self._pop())
            left = expect_i32(self._pop())
            self.stack.append(I32Value(clamp_i32(left.value + right.value)))
            return None

        if opcode == OpCode.U32_ADD_SATURATING:
            right = expect_u32(self._pop())
            left = expect_u32(self._pop())
            self.stack.append(U32Value(min(U32_MAX, left.value + right.value)))
            return None

        if opcode == OpCode.BYTE_NEW:
            self.stack.append(BytesValue(b""))
            return None

        if opcode == OpCode.BYTE_LEN:
            self.stack.append(len(expect_bytes(self._pop()).data))
            return None

        if opcode == OpCode.BYTE_GET:
            index = self._pop_int()
            data = expect_bytes(self._pop()).data
            self._check_index(data, index)
            self.stack.append(data[index])
            return None

        if opcode == OpCode.BYTEARRAY_NEW:
            self.stack.append(ByteArrayValue(bytearray()))
            return None

        if opcode == OpCode.BYTEARRAY_SET:
            value = self._pop_int()
            if value < 0 or value > 255:
                raise RuntimeSanskriptError(f"byte value must be 0..255, got {value}")
            index = self._pop_int()
            buffer = expect_bytearray(self._pop())
            if index < 0:
                raise RuntimeSanskriptError(f"bytearray index out of range: {index}")
            if index >= len(buffer.data):
                buffer.data.extend(b"\x00" * (index - len(buffer.data) + 1))
            buffer.data[index] = value
            self.stack.append(buffer)
            return None

        if opcode == OpCode.BYTEARRAY_GET:
            index = self._pop_int()
            buffer = expect_bytearray(self._pop())
            self._check_index(buffer.data, index)
            self.stack.append(buffer.data[index])
            return None

        if opcode == OpCode.TUPLE_NEW:
            arity = self._expect_int(operand, opcode)
            if arity < 0:
                raise RuntimeSanskriptError("tuple_new arity must be non-negative")
            items = [self._pop() for _ in range(arity)]
            items.reverse()
            self.stack.append(TupleValue(tuple(items)))
            return None

        if opcode == OpCode.TUPLE_GET:
            index = self._expect_int(operand, opcode)
            tup = expect_tuple(self._pop())
            self._check_index(tup.items, index)
            self.stack.append(tup.items[index])
            return None

        if opcode == OpCode.SET_NEW:
            self.stack.append(SetValue())
            return None

        if opcode == OpCode.SET_ADD:
            item = self._pop()
            target = expect_set(self._pop())
            set_add_unique(target, item)
            self.stack.append(target)
            return None

        if opcode == OpCode.SET_CONTAINS:
            item = self._pop()
            target = expect_set(self._pop())
            self.stack.append(1 if any(values_equal(item, existing) for existing in target.items) else 0)
            return None

        if opcode == OpCode.SET_LEN:
            self.stack.append(len(expect_set(self._pop()).items))
            return None

        if opcode == OpCode.DEQUE_NEW:
            self.stack.append(DequeValue())
            return None

        if opcode == OpCode.DEQUE_PUSH_BACK:
            item = self._pop()
            target = expect_deque(self._pop())
            target.items.append(item)
            self.stack.append(target)
            return None

        if opcode == OpCode.DEQUE_PUSH_FRONT:
            item = self._pop()
            target = expect_deque(self._pop())
            target.items.appendleft(item)
            self.stack.append(target)
            return None

        if opcode == OpCode.DEQUE_POP_BACK:
            target = expect_deque(self._pop())
            if not target.items:
                raise RuntimeSanskriptError("deque_pop_back on empty deque")
            self.stack.append(target.items.pop())
            return None

        if opcode == OpCode.DEQUE_POP_FRONT:
            target = expect_deque(self._pop())
            if not target.items:
                raise RuntimeSanskriptError("deque_pop_front on empty deque")
            self.stack.append(target.items.popleft())
            return None

        if opcode == OpCode.DEQUE_LEN:
            self.stack.append(len(expect_deque(self._pop()).items))
            return None

        if opcode == OpCode.OPTION_NONE:
            self.stack.append(OptionValue(present=False))
            return None

        if opcode == OpCode.OPTION_SOME:
            self.stack.append(OptionValue(present=True, value=self._pop()))
            return None

        if opcode == OpCode.OPTION_IS_SOME:
            self.stack.append(1 if expect_option(self._pop()).present else 0)
            return None

        if opcode == OpCode.OPTION_UNWRAP:
            option = expect_option(self._pop())
            if not option.present or option.value is None:
                raise RuntimeSanskriptError("option_unwrap on none")
            self.stack.append(option.value)
            return None

        if opcode == OpCode.RESULT_OK:
            self.stack.append(ResultValue(ok=True, value=self._pop()))
            return None

        if opcode == OpCode.RESULT_ERR:
            self.stack.append(ResultValue(ok=False, value=self._pop()))
            return None

        if opcode == OpCode.RESULT_IS_OK:
            self.stack.append(1 if expect_result(self._pop()).ok else 0)
            return None

        if opcode == OpCode.RESULT_UNWRAP_OK:
            result = expect_result(self._pop())
            if not result.ok:
                raise RuntimeSanskriptError("result_unwrap_ok on err")
            self.stack.append(result.value)
            return None

        if opcode == OpCode.RESULT_UNWRAP_ERR:
            result = expect_result(self._pop())
            if result.ok:
                raise RuntimeSanskriptError("result_unwrap_err on ok")
            self.stack.append(result.value)
            return None

        if opcode == OpCode.TEXT_GRAPHEME_LEN:
            self.stack.append(text_grapheme_len_stub(expect_text(self._pop())))
            return None

        if opcode == OpCode.FLOAT_IS_NAN:
            value = self._pop()
            if not isinstance(value, float) or isinstance(value, bool):
                raise RuntimeSanskriptError(f"float_is_nan expected float, got {value!r}")
            self.stack.append(1 if math.isnan(value) else 0)
            return None

        if opcode == OpCode.FLOAT_IS_INF:
            value = self._pop()
            if not isinstance(value, float) or isinstance(value, bool):
                raise RuntimeSanskriptError(f"float_is_inf expected float, got {value!r}")
            self.stack.append(1 if math.isinf(value) else 0)
            return None

        if opcode == OpCode.OPAQUE_NEW:
            handle_id = self._pop_int()
            kind = self._expect_name(operand, opcode)
            self.stack.append(OpaqueHandle(kind=kind, handle_id=handle_id))
            return None

        if opcode == OpCode.ARRAY_NEW:
            size = self._expect_int(operand, opcode)
            if size < 0:
                raise RuntimeSanskriptError("array_new size must be non-negative")
            self.stack.append([0] * size)
            return None

        if opcode == OpCode.SLICE_VIEW:
            end = self._pop_int()
            start = self._pop_int()
            items = expect_list(self._pop())
            if start < 0 or end < start or end > len(items):
                raise RuntimeSanskriptError(
                    f"slice_view {start}:{end} out of range for length {len(items)}"
                )
            self.stack.append(list(items[start:end]))
            return None

        if opcode == OpCode.THROW:
            from .errors import ThrownError
            msg = self._pop()
            raise ThrownError(str(msg) if not isinstance(msg, str) else msg)

        if opcode == OpCode.PANIC:
            from .errors import PanicError
            msg = self._pop()
            raise PanicError(str(msg) if not isinstance(msg, str) else msg)

        if opcode == OpCode.TRY_BEGIN:
            handler_ip = self._expect_int(operand, opcode)
            self._try_stack.append(
                (handler_ip, len(self.stack), len(self._call_stack), self._instructions, dict(self.locals))
            )
            return None

        if opcode == OpCode.TRY_END:
            if self._try_stack:
                self._try_stack.pop()
            return None

        raise RuntimeSanskriptError(f"Unknown bytecode instruction: {instruction!r}")

    @staticmethod
    def _check_index(items: list[SanskriptValue] | str | bytes | bytearray | tuple[SanskriptValue, ...], index: int) -> None:
        if index < 0 or index >= len(items):
            raise RuntimeSanskriptError(
                f"Index {index} out of range for length {len(items)}"
            )

    @staticmethod
    def _unwrap_cell(value: SanskriptValue) -> SanskriptValue:
        if isinstance(value, MutableCell):
            return value.value
        return value

    def _promote_mutable_captures(self, capture_mut: frozenset[str]) -> None:
        for name in capture_mut:
            if name in self.locals and not isinstance(self.locals[name], MutableCell):
                self.locals[name] = MutableCell(self.locals[name])

    def _build_closure(self, capture_mut: frozenset[str]) -> dict[str, SanskriptValue]:
        closure: dict[str, SanskriptValue] = {}
        for key, value in self.locals.items():
            if key in capture_mut:
                closure[key] = value if isinstance(value, MutableCell) else MutableCell(value)
            else:
                closure[key] = self._unwrap_cell(value)
        return closure

    def _lookup_name(self, name: str) -> SanskriptValue:
        if name in self.locals:
            return self._unwrap_cell(self.locals[name])
        if name in self.globals:
            return self._unwrap_cell(self.globals[name])
        if self._program is not None:
            try:
                resolve_call_target(self._program, name)
                return FunctionValue(target=name, closure=dict(self.locals))
            except Exception:
                _unknown_callable = name
        raise RuntimeSanskriptError(
            f"Unknown stored value: {name!r}",
            hint="Assign a value before reading it, or check the function scope.",
        )

    def _store_name(self, name: str, value: SanskriptValue) -> None:
        if isinstance(value, FunctionValue):
            value.closure[name] = value
        if name in self.locals and isinstance(self.locals[name], MutableCell):
            self.locals[name].value = value
            return
        if name in self.locals:
            self.locals[name] = value
        elif self._scope_stack:
            self.locals[name] = value
        elif name in self.globals:
            self.globals[name] = value
        else:
            self.globals[name] = value

    def _invoke_call_frame(self, function, ip: int) -> int:
        args = self._bind_call_args(function.params, function.defaults, function.variadic_param)
        self._call_stack.append(
            _CallFrame(
                ip + 1,
                self._instructions,
                dict(self.locals),
                capture_mut=function.capture_mut,
            )
        )
        self._effect_stack = getattr(self, "_effect_stack", [])
        self._effect_stack.append(self._current_effect)
        self._current_effect = getattr(function, "effect", None)
        self.locals = args
        self._instructions = function.instructions
        return 0

    def _invoke_tail_call_frame(self, function, ip: int) -> int:
        args = self._bind_call_args(function.params, function.defaults, function.variadic_param)
        if self._call_stack:
            self.locals = args
            self._instructions = function.instructions
            return 0
        return self._invoke_call_frame(function, ip)

    def _invoke_callable_frame(self, callable_value: SanskriptValue, ip: int) -> int:
        if isinstance(callable_value, RecordValue) and "__call__" in callable_value.fields:
            return self._invoke_callable_frame(callable_value.fields["__call__"], ip)
        if not isinstance(callable_value, FunctionValue):
            raise RuntimeSanskriptError(f"Value is not callable: {callable_value!r}")
        if self._program is None:
            raise RuntimeSanskriptError("Callable invocation requires a full BytecodeProgram context")
        function = resolve_call_target(self._program, callable_value.target)
        args = self._bind_call_args(function.params, function.defaults, function.variadic_param)
        locals_with_capture = dict(callable_value.closure)
        locals_with_capture.update(args)
        self._call_stack.append(
            _CallFrame(
                ip + 1,
                self._instructions,
                dict(self.locals),
                capture_mut=function.capture_mut,
            )
        )
        self._effect_stack = getattr(self, "_effect_stack", [])
        self._effect_stack.append(self._current_effect)
        self._current_effect = getattr(function, "effect", None)
        self.locals = locals_with_capture
        self._instructions = function.instructions
        return 0

    def _bind_call_args(
        self,
        params: tuple[str, ...],
        defaults: tuple[object, ...],
        variadic_param: str | None,
    ) -> dict[str, SanskriptValue]:
        max_regular = len(params)
        available = len(self.stack)
        provided_count = available if variadic_param is not None else min(available, max_regular)
        required_count = max_regular
        if defaults and len(defaults) == max_regular:
            required_count = sum(1 for item in defaults if item is None)
        if variadic_param is None and (provided_count < required_count or provided_count > max_regular):
            raise RuntimeSanskriptError(
                f"Call arity mismatch: got {provided_count}, expected {required_count}..{max_regular}"
            )
        if variadic_param is not None and provided_count < required_count:
            raise RuntimeSanskriptError(
                f"Call arity mismatch: got {provided_count}, expected at least {required_count}"
            )
        arg_items = [self._pop() for _ in range(provided_count)]
        arg_items.reverse()
        bound: dict[str, SanskriptValue] = {}
        for idx, name in enumerate(params):
            if idx < len(arg_items):
                bound[name] = arg_items[idx]
                continue
            default = defaults[idx] if idx < len(defaults) else None
            if default is None:
                raise RuntimeSanskriptError(f"Missing required argument: {name!r}")
            bound[name] = default  # type: ignore[assignment]
        if variadic_param is not None:
            bound[variadic_param] = list(arg_items[max_regular:])
        return bound

    def _pop(self) -> SanskriptValue:
        try:
            return self.stack.pop()
        except IndexError as exc:
            raise RuntimeSanskriptError("Sanskript VM stack underflow") from exc

    def _pop_int(self) -> int:
        value = self._pop()
        if not isinstance(value, int) or isinstance(value, bool):
            raise RuntimeSanskriptError(f"Expected integer stack value, got {value!r}")
        return value

    def _pop_number(self) -> int | float:
        value = self._pop()
        if isinstance(value, bool):
            raise RuntimeSanskriptError(f"Expected numeric stack value, got {value!r}")
        if isinstance(value, (int, float)):
            return value
        raise RuntimeSanskriptError(f"Expected numeric stack value, got {value!r}")

    def _require_heap_access(self, opcode: OpCode) -> None:
        if self._program is None:
            raise RuntimeSanskriptError("Heap access requires a full BytecodeProgram context")
        tier = self._program.safety_tier
        if tier == "surakshita":
            raise RuntimeSanskriptError(
                f"{opcode.value} is not allowed in surakṣita (surakshita) programs"
            )
        if tier == "rakshita" and self._unsafe_depth == 0:
            raise RuntimeSanskriptError(
                f"{opcode.value} in rakṣita (rakshita) programs requires unsafe_enter"
            )

    def _heap_store(self, address: int, value: int) -> None:
        if address not in self._heap:
            raise RuntimeSanskriptError(f"Invalid heap address: {address}")
        self._heap[address] = value

    def _heap_load(self, address: int) -> int:
        if address not in self._heap:
            raise RuntimeSanskriptError(f"Invalid heap address: {address}")
        return self._heap[address]

    def _resolve_loop_frame(self, label: str | None, *, for_continue: bool) -> _LoopFrame:
        if not self._loop_stack:
            action = "continue" if for_continue else "break"
            raise RuntimeSanskriptError(f"{action} outside of a loop")
        if label is None:
            return self._loop_stack[-1]
        for frame in reversed(self._loop_stack):
            if frame.label == label:
                return frame
        raise RuntimeSanskriptError(f"No loop label {label!r}")

    def _resume_generator(self, gen: GeneratorValue) -> SanskriptValue:
        if self._program is None:
            raise RuntimeSanskriptError("generator resume requires program context")
        function = resolve_call_target(self._program, gen.function_name)
        saved_instructions = self._instructions
        saved_locals = self.locals
        saved_stack_len = len(self.stack)
        self._instructions = function.instructions
        self.locals = dict(gen.bound)
        ip = gen.ip
        self._generator_yield_value = None
        try:
            while ip < len(self._instructions):
                inst = self._instructions[ip]
                if inst.opcode == OpCode.GENERATOR_YIELD:
                    gen.ip = ip + 1
                    gen.bound = dict(self.locals)
                    return self._generator_yield_value if self._generator_yield_value is not None else 0
                if inst.opcode == OpCode.RETURN:
                    gen.done = True
                    return self._pop()
                if inst.opcode == OpCode.HALT:
                    gen.done = True
                    return 0
                next_ip = self._execute_instruction(inst, ip)
                ip = next_ip if next_ip is not None else ip + 1
            gen.done = True
            return 0
        finally:
            del self.stack[saved_stack_len:]
            self._instructions = saved_instructions
            self.locals = saved_locals

    def _invoke_function(self, target: str, args: list[SanskriptValue]) -> SanskriptValue:
        if self._program is None:
            raise RuntimeSanskriptError("Higher-order list operation requires program context")
        function = resolve_call_target(self._program, target)
        bound: dict[str, SanskriptValue] = {}
        required_count = len(function.params)
        if function.defaults and len(function.defaults) == len(function.params):
            required_count = sum(1 for item in function.defaults if item is None)
        if function.variadic_param is None:
            if len(args) < required_count or len(args) > len(function.params):
                raise RuntimeSanskriptError(
                    f"Function {target!r} expects {required_count}..{len(function.params)} args, got {len(args)}"
                )
        elif len(args) < required_count:
            raise RuntimeSanskriptError(
                f"Function {target!r} expects at least {required_count} args, got {len(args)}"
            )
        for idx, name in enumerate(function.params):
            if idx < len(args):
                bound[name] = args[idx]
                continue
            default = function.defaults[idx] if idx < len(function.defaults) else None
            if default is None:
                raise RuntimeSanskriptError(f"Missing required argument: {name!r}")
            bound[name] = default  # type: ignore[assignment]
        if function.variadic_param is not None:
            bound[function.variadic_param] = list(args[len(function.params):])
        saved_instructions = self._instructions
        saved_locals = self.locals
        saved_stack_len = len(self.stack)
        base_call_depth = len(self._call_stack)
        self._instructions = function.instructions
        self.locals = bound
        result: SanskriptValue = 0
        ip = 0
        try:
            while ip < len(self._instructions):
                inst = self._instructions[ip]
                if inst.opcode == OpCode.GENERATOR_YIELD and len(self._call_stack) == base_call_depth:
                    result = self._generator_yield_value if self._generator_yield_value is not None else 0
                    break
                if inst.opcode == OpCode.RETURN and len(self._call_stack) == base_call_depth:
                    result = self._pop()
                    break
                if inst.opcode == OpCode.HALT and len(self._call_stack) == base_call_depth:
                    break
                next_ip = self._execute_instruction(inst, ip)
                ip = next_ip if next_ip is not None else ip + 1
            return result
        finally:
            del self.stack[saved_stack_len:]
            self._instructions = saved_instructions
            self.locals = saved_locals

    def _expect_int(self, operand: object, opcode: OpCode) -> int:
        if not isinstance(operand, int) or isinstance(operand, bool):
            raise RuntimeSanskriptError(f"{opcode.value} expected an integer operand, got {operand!r}")
        return operand

    def _expect_text(self, operand: object, opcode: OpCode) -> str:
        if not isinstance(operand, str):
            raise RuntimeSanskriptError(f"{opcode.value} expected a text operand, got {operand!r}")
        return operand

    def _expect_name(self, operand: object, opcode: OpCode) -> str:
        if not isinstance(operand, str):
            raise RuntimeSanskriptError(f"{opcode.value} expected a name operand, got {operand!r}")
        return operand

    @property
    def environment(self) -> dict[str, SanskriptValue]:
        """Merged view used by tests: locals shadow globals."""
        merged = dict(self.globals)
        merged.update(self.locals)
        return merged
