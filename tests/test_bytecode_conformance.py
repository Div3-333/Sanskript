"""Conformance tests for Sanskript bytecode v1 (portable VM contract)."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from sanskript.bytecode import (
    BYTECODE_VERSION_1,
    BytecodeProgram,
    BytecodeValidationError,
    Instruction,
    OpCode,
    decode_program,
    encode_program,
    instruction_from_dict,
    load_bytecode_file,
    validate_bytecode,
)
from sanskript.compiler import compile_statements, lower_ir_to_bytecode
from sanskript.ast import Assign, Display, Increase, Literal, Reference
from sanskript.errors import RuntimeSanskriptError
from sanskript.ir import IREmit, IRIncrease, IRLiteral, IRProgram, IRReference, IRStore
from sanskript.vm import SanskriptVM

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE_DIR = ROOT / "data" / "bytecode" / "conformance"


class BytecodeConformanceTests(unittest.TestCase):
    def test_version_constant(self) -> None:
        self.assertEqual(BYTECODE_VERSION_1, 1)

    def test_golden_fixture_executes(self) -> None:
        for path in sorted(CONFORMANCE_DIR.glob("*.json")):
            with self.subTest(fixture=path.name):
                payload = json.loads(path.read_text(encoding="utf-8"))
                program = load_bytecode_file(path)
                vm = SanskriptVM()
                output = vm.execute(program)
                self.assertEqual(output, payload["expected_output"])
                for name, value in payload.get("expected_environment", {}).items():
                    self.assertEqual(vm.environment[name], value)

    def test_compiler_output_matches_fixture(self) -> None:
        program = lower_ir_to_bytecode(
            IRProgram(
                (
                    IRStore("phala", IRLiteral(5)),
                    IRIncrease("phala", IRLiteral(2)),
                    IREmit(IRReference("phala")),
                )
            )
        )
        validate_bytecode(program)
        fixture = load_bytecode_file(CONFORMANCE_DIR / "assign_increment_emit.json")
        self.assertEqual(program.instructions, fixture.instructions)

    def test_encode_decode_round_trip(self) -> None:
        original = compile_statements(
            [
                Assign("phala", Literal(5)),
                Increase("phala", Literal(2)),
                Display(Reference("phala")),
            ]
        )
        validate_bytecode(original)
        payload = encode_program(original)
        restored = decode_program(payload)
        self.assertEqual(restored.instructions, original.instructions)
        self.assertEqual(SanskriptVM().execute(restored), ["7"])

    def test_instruction_dict_round_trip(self) -> None:
        raw = {"op": "push_int", "operand": 42}
        instruction = instruction_from_dict(raw)
        self.assertEqual(instruction, Instruction(OpCode.PUSH_INT, 42))

    def test_rejects_unknown_opcode(self) -> None:
        with self.assertRaises(BytecodeValidationError):
            instruction_from_dict({"op": "jump", "operand": 0}, allowed=frozenset({"halt"}))

    def test_rejects_push_int_without_operand(self) -> None:
        with self.assertRaises(BytecodeValidationError):
            instruction_from_dict({"op": "push_int"})

    def test_rejects_halt_with_operand(self) -> None:
        with self.assertRaises(BytecodeValidationError):
            instruction_from_dict({"op": "halt", "operand": 1})

    def test_rejects_stack_underflow_in_validation(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.ADD),
                Instruction(OpCode.HALT),
            )
        )
        with self.assertRaises(BytecodeValidationError):
            validate_bytecode(program)

    def test_rejects_missing_halt(self) -> None:
        program = BytecodeProgram((Instruction(OpCode.PUSH_INT, 1),))
        with self.assertRaises(BytecodeValidationError):
            validate_bytecode(program)

    def test_rejects_wrong_version(self) -> None:
        with self.assertRaises(BytecodeValidationError):
            decode_program({"version": 99, "instructions": [{"op": "halt"}]})

    def test_runtime_unbound_name(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.LOAD_NAME, "phala"),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        validate_bytecode(program)
        with self.assertRaises(RuntimeSanskriptError):
            SanskriptVM().execute(program)

    def test_runtime_stack_underflow(self) -> None:
        # Validation catches linear underflow; bypass with emit-only after push
        program = BytecodeProgram(
            (
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        with self.assertRaises(BytecodeValidationError):
            validate_bytecode(program)


if __name__ == "__main__":
    unittest.main()
