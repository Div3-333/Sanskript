"""VM tests for push_float, mixed arithmetic, and arakṣita heap opcodes."""

from __future__ import annotations

import unittest

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode
from sanskript.errors import RuntimeSanskriptError
from sanskript.vm import SanskriptVM


class VmNumericHeapTests(unittest.TestCase):
    def test_push_float_and_add(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_FLOAT, 1.5),
                Instruction(OpCode.PUSH_FLOAT, 2.5),
                Instruction(OpCode.ADD),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        self.assertEqual(SanskriptVM().execute(program), ["4.0"])

    def test_heap_in_arakshita_tier(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.STORE_NAME, "addr"),
                Instruction(OpCode.LOAD_NAME, "addr"),
                Instruction(OpCode.PUSH_INT, 42),
                Instruction(OpCode.HEAP_STORE),
                Instruction(OpCode.LOAD_NAME, "addr"),
                Instruction(OpCode.HEAP_LOAD),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            ),
            safety_tier="arakshita",
        )
        self.assertEqual(SanskriptVM().execute(program), ["42"])

    def test_heap_in_rakshita_requires_unsafe(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.HALT),
            ),
            safety_tier="rakshita",
        )
        with self.assertRaises(RuntimeSanskriptError):
            SanskriptVM().execute(program)

    def test_heap_in_rakshita_inside_unsafe(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.UNSAFE_ENTER),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.UNSAFE_EXIT),
                Instruction(OpCode.HALT),
            ),
            safety_tier="rakshita",
        )
        SanskriptVM().execute(program)


if __name__ == "__main__":
    unittest.main()
