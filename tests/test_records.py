import unittest

from sanskript.ast import Display, FieldContains, FieldGet, FieldSet, Literal, Program, RecordInit, Reference, TextLiteral
from sanskript.bytecode import BytecodeProgram, Instruction, OpCode, decode_program, encode_program
from sanskript.compiler import compile_program, compile_source
from sanskript.runtime_values import RecordValue
from sanskript.vm import SanskriptVM
from sanskript.yantra_patha import program_from_yantra_patha, program_to_yantra_patha


class RecordRuntimeTests(unittest.TestCase):
    def test_record_bytecode_sets_gets_and_checks_fields(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.RECORD_NEW),
                Instruction(OpCode.PUSH_TEXT, "nāma"),
                Instruction(OpCode.PUSH_TEXT, "rāma"),
                Instruction(OpCode.RECORD_SET),
                Instruction(OpCode.STORE_NAME, "jana"),
                Instruction(OpCode.LOAD_NAME, "jana"),
                Instruction(OpCode.PUSH_TEXT, "nāma"),
                Instruction(OpCode.RECORD_GET),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.LOAD_NAME, "jana"),
                Instruction(OpCode.PUSH_TEXT, "nāma"),
                Instruction(OpCode.RECORD_CONTAINS),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )

        vm = SanskriptVM()
        output = vm.execute(program)

        self.assertEqual(output, ["rāma", "1"])
        self.assertIsInstance(vm.globals["jana"], RecordValue)

    def test_record_ast_compiles_to_runtime_object_substrate(self) -> None:
        program = Program(
            (
                RecordInit("jana"),
                FieldSet("jana", TextLiteral("nāma"), TextLiteral("rāma")),
                FieldSet("jana", TextLiteral("aṅka"), Literal(5)),
                FieldGet("phala", "jana", TextLiteral("aṅka")),
                Display(Reference("phala")),
                FieldContains("phala", "jana", TextLiteral("nāma")),
                Display(Reference("phala")),
            )
        )

        output = SanskriptVM().execute(compile_program(program))

        self.assertEqual(output, ["5", "1"])

    def test_record_source_uses_prose_field_frames(self) -> None:
        program = compile_source(
            """
            vastuḥ jane.
            aṅgasthāpanam jane nāma vākyam rāma iti.
            aṅgāharaṇam phala jane nāma.
            gaṇakaḥ phalaṃ darśayati.
            aṅgāsti phala jane nāma.
            gaṇakaḥ phalaṃ darśayati.
            """
        )

        self.assertEqual(SanskriptVM().execute(program), ["rāma", "1"])

    def test_record_bytecode_round_trips_through_json_and_prose_machine_text(self) -> None:
        program = compile_program(
            Program(
                (
                    RecordInit("jana"),
                    FieldSet("jana", TextLiteral("nāma"), TextLiteral("rāma")),
                    FieldGet("phala", "jana", TextLiteral("nāma")),
                    Display(Reference("phala")),
                )
            )
        )

        restored_json = decode_program(encode_program(program))
        restored_prose = program_from_yantra_patha(program_to_yantra_patha(program))

        self.assertEqual(restored_json.instructions, program.instructions)
        self.assertEqual(restored_prose.instructions, program.instructions)
        self.assertEqual(SanskriptVM().execute(restored_prose), ["rāma"])


if __name__ == "__main__":
    unittest.main()
