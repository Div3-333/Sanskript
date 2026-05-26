"""Bytecode-level tests for surakṣita list and map values."""

from __future__ import annotations

import unittest

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode, encode_program, decode_program
from sanskript.vm import SanskriptVM


def _run(*instructions: Instruction) -> tuple[list[str], SanskriptVM]:
    vm = SanskriptVM()
    output = vm.execute(BytecodeProgram((*instructions, Instruction(OpCode.HALT))))
    return output, vm


class CollectionRuntimeTests(unittest.TestCase):
    def test_bool_push_and_truthy_jump(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_BOOL, 1),
                Instruction(OpCode.JUMP_IF_ZERO, 4),
                Instruction(OpCode.PUSH_TEXT, "yes"),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        self.assertEqual(SanskriptVM().execute(program), ["yes"])

    def test_list_build_and_index(self) -> None:
        _, vm = _run(
            Instruction(OpCode.LIST_NEW),
            Instruction(OpCode.PUSH_INT, 10),
            Instruction(OpCode.LIST_APPEND),
            Instruction(OpCode.PUSH_INT, 20),
            Instruction(OpCode.LIST_APPEND),
            Instruction(OpCode.STORE_NAME, "items"),
            Instruction(OpCode.LOAD_NAME, "items"),
            Instruction(OpCode.PUSH_INT, 1),
            Instruction(OpCode.LIST_GET),
            Instruction(OpCode.EMIT),
        )
        self.assertEqual(vm.environment["items"], [10, 20])
        self.assertEqual(vm.output, ["20"])

    def test_map_set_get_and_contains(self) -> None:
        _, vm = _run(
            Instruction(OpCode.MAP_NEW),
            Instruction(OpCode.PUSH_TEXT, "phala"),
            Instruction(OpCode.PUSH_INT, 7),
            Instruction(OpCode.MAP_SET),
            Instruction(OpCode.STORE_NAME, "table"),
            Instruction(OpCode.LOAD_NAME, "table"),
            Instruction(OpCode.PUSH_TEXT, "phala"),
            Instruction(OpCode.MAP_CONTAINS),
            Instruction(OpCode.EMIT),
            Instruction(OpCode.LOAD_NAME, "table"),
            Instruction(OpCode.PUSH_TEXT, "phala"),
            Instruction(OpCode.MAP_GET),
            Instruction(OpCode.EMIT),
        )
        self.assertEqual(vm.environment["table"], {"phala": 7})
        self.assertEqual(vm.output, ["1", "7"])

    def test_map_integer_key(self) -> None:
        _, vm = _run(
            Instruction(OpCode.MAP_NEW),
            Instruction(OpCode.PUSH_INT, 3),
            Instruction(OpCode.PUSH_INT, 9),
            Instruction(OpCode.MAP_SET),
            Instruction(OpCode.STORE_NAME, "table"),
            Instruction(OpCode.LOAD_NAME, "table"),
            Instruction(OpCode.PUSH_INT, 3),
            Instruction(OpCode.MAP_GET),
            Instruction(OpCode.EMIT),
        )
        self.assertEqual(vm.environment["table"], {"3": 9})
        self.assertEqual(vm.output, ["9"])

    def test_collection_bytecode_round_trip(self) -> None:
        original = BytecodeProgram(
            (
                Instruction(OpCode.LIST_NEW),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.LIST_APPEND),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        restored = decode_program(encode_program(original))
        self.assertEqual(SanskriptVM().execute(restored), ["[1]"])


if __name__ == "__main__":
    unittest.main()
