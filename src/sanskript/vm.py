from __future__ import annotations

from dataclasses import dataclass

from .bytecode import (
    BytecodeProgram,
    Instruction,
    OpCode,
    resolve_call_target,
)
from .errors import RuntimeSanskriptError
from .runtime_values import (
    SanskriptValue,
    expect_list,
    expect_map,
    is_truthy,
    map_key_from_value,
    to_display_string,
    values_equal,
)


@dataclass
class _CallFrame:
    return_ip: int
    instructions: tuple[Instruction, ...]
    locals_snapshot: dict[str, SanskriptValue]


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

    def execute(self, program: BytecodeProgram) -> list[str]:
        self.globals = {}
        self.locals = {}
        self.output = []
        self.stack = []
        self._call_stack = []
        self._heap = {}
        self._heap_next = 1
        self._unsafe_depth = 0
        self._program = program
        self._instructions = program.instructions
        self._run(0)
        return self.output

    def _run(self, start_ip: int) -> None:
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
            next_ip = self._execute_instruction(instruction, ip)
            ip = next_ip if next_ip is not None else ip + 1

    def _execute_instruction(self, instruction: Instruction, ip: int) -> int | None:
        opcode = instruction.opcode
        operand = instruction.operand

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
            self.stack.append(1 if values_equal(left, right) else 0)
            return None

        if opcode == OpCode.COMPARE_LT:
            right = self._pop_int()
            left = self._pop_int()
            self.stack.append(1 if left < right else 0)
            return None

        if opcode == OpCode.EMIT:
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
            if self._program is None:
                raise RuntimeSanskriptError("CALL requires a full BytecodeProgram context")
            function = resolve_call_target(self._program, target)
            args = [self._pop() for _ in function.params]
            args.reverse()
            self._call_stack.append(_CallFrame(ip + 1, self._instructions, dict(self.locals)))
            self.locals = dict(zip(function.params, args))
            self._instructions = function.instructions
            return 0

        if opcode == OpCode.RETURN:
            value = self._pop()
            if not self._call_stack:
                raise RuntimeSanskriptError("RETURN outside of a function call")
            frame = self._call_stack.pop()
            self._instructions = frame.instructions
            self.locals = frame.locals_snapshot
            self.stack.append(value)
            return frame.return_ip

        if opcode == OpCode.POP:
            self._pop()
            return None

        raise RuntimeSanskriptError(f"Unknown bytecode instruction: {instruction!r}")

    @staticmethod
    def _check_index(items: list[SanskriptValue], index: int) -> None:
        if index < 0 or index >= len(items):
            raise RuntimeSanskriptError(
                f"List index {index} out of range for length {len(items)}"
            )

    def _lookup_name(self, name: str) -> SanskriptValue:
        if name in self.locals:
            return self.locals[name]
        if name in self.globals:
            return self.globals[name]
        raise RuntimeSanskriptError(
            f"Unknown stored value: {name!r}",
            hint="Assign a value before reading it, or check the function scope.",
        )

    def _store_name(self, name: str, value: SanskriptValue) -> None:
        if name in self.locals:
            self.locals[name] = value
        else:
            self.globals[name] = value

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
