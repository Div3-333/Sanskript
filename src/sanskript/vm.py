from __future__ import annotations

from dataclasses import dataclass

from .bytecode import (
    BytecodeProgram,
    Instruction,
    OpCode,
    resolve_call_target,
)
from .errors import RuntimeSanskriptError

SanskriptValue = int | str


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

    def execute(self, program: BytecodeProgram) -> list[str]:
        self.globals = {}
        self.locals = {}
        self.output = []
        self.stack = []
        self._call_stack = []
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

        if opcode == OpCode.LOAD_NAME:
            self.stack.append(self._lookup_name(self._expect_name(operand, opcode)))
            return None

        if opcode == OpCode.STORE_NAME:
            name = self._expect_name(operand, opcode)
            self._store_name(name, self._pop())
            return None

        if opcode == OpCode.ADD:
            right = self._pop_int()
            left = self._pop_int()
            self.stack.append(left + right)
            return None

        if opcode == OpCode.SUBTRACT:
            right = self._pop_int()
            left = self._pop_int()
            self.stack.append(left - right)
            return None

        if opcode == OpCode.MULTIPLY:
            right = self._pop_int()
            left = self._pop_int()
            self.stack.append(left * right)
            return None

        if opcode == OpCode.DIVIDE:
            right = self._pop_int()
            if right == 0:
                raise RuntimeSanskriptError("Division by zero")
            left = self._pop_int()
            self.stack.append(left // right)
            return None

        if opcode == OpCode.COMPARE_EQ:
            right = self._pop()
            left = self._pop()
            self.stack.append(1 if left == right else 0)
            return None

        if opcode == OpCode.COMPARE_LT:
            right = self._pop_int()
            left = self._pop_int()
            self.stack.append(1 if left < right else 0)
            return None

        if opcode == OpCode.EMIT:
            self.output.append(str(self._pop()))
            return None

        if opcode == OpCode.JUMP:
            return self._expect_int(operand, opcode)

        if opcode == OpCode.JUMP_IF_ZERO:
            value = self._pop_int()
            if value == 0:
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
