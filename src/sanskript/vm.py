from __future__ import annotations

from .bytecode import BytecodeProgram, Instruction, OpCode
from .errors import RuntimeSanskriptError


class SanskriptVM:
    """Executes Sanskript bytecode.

    The VM is hosted by Python for now, but it consumes only Sanskript-owned
    instructions. It is the first runtime boundary that can later be ported
    to Rust, C, Zig, or WASM without changing language semantics.
    """

    def __init__(self) -> None:
        self.environment: dict[str, int] = {}
        self.output: list[str] = []
        self.stack: list[int] = []

    def execute(self, program: BytecodeProgram) -> list[str]:
        ip = 0
        instructions = program.instructions
        while ip < len(instructions):
            instruction = instructions[ip]
            if instruction.opcode == OpCode.HALT:
                break
            self.execute_instruction(instruction)
            ip += 1
        return self.output

    def execute_instruction(self, instruction: Instruction) -> None:
        opcode = instruction.opcode
        operand = instruction.operand

        if opcode == OpCode.PUSH_INT:
            if not isinstance(operand, int):
                raise RuntimeSanskriptError(f"push_int expected an integer operand, got {operand!r}")
            self.stack.append(operand)
            return

        if opcode == OpCode.LOAD_NAME:
            name = self._expect_name(operand, opcode)
            try:
                self.stack.append(self.environment[name])
            except KeyError as exc:
                raise RuntimeSanskriptError(
                    f"Unknown stored value: {name!r}",
                    hint="Assign a value with an adhikaraṇa frame before reading it.",
                ) from exc
            return

        if opcode == OpCode.STORE_NAME:
            name = self._expect_name(operand, opcode)
            self.environment[name] = self._pop()
            return

        if opcode == OpCode.ADD:
            right = self._pop()
            left = self._pop()
            self.stack.append(left + right)
            return

        if opcode == OpCode.SUBTRACT:
            right = self._pop()
            left = self._pop()
            self.stack.append(left - right)
            return

        if opcode == OpCode.EMIT:
            self.output.append(str(self._pop()))
            return

        raise RuntimeSanskriptError(f"Unknown bytecode instruction: {instruction!r}")

    def _pop(self) -> int:
        try:
            return self.stack.pop()
        except IndexError as exc:
            raise RuntimeSanskriptError("Sanskript VM stack underflow") from exc

    def _expect_name(self, operand: object, opcode: OpCode) -> str:
        if not isinstance(operand, str):
            raise RuntimeSanskriptError(f"{opcode.value} expected a name operand, got {operand!r}")
        return operand
