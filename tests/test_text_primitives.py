import unittest

from sanskript.ast import Display, Program, Reference, TextConcat, TextContains, TextGet, TextLength, TextLiteral, TextSlice
from sanskript.bytecode import BytecodeProgram, Instruction, OpCode, decode_program, encode_program
from sanskript.compiler import compile_program, compile_source
from sanskript.vm import SanskriptVM
from sanskript.yantra_patha import program_from_yantra_patha, program_to_yantra_patha


class TextPrimitiveTests(unittest.TestCase):
    def test_text_bytecode_primitives(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_TEXT, "sva"),
                Instruction(OpCode.PUSH_TEXT, "gata"),
                Instruction(OpCode.TEXT_CONCAT),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.PUSH_TEXT, "svāgatam"),
                Instruction(OpCode.TEXT_LEN),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.PUSH_TEXT, "svāgatam"),
                Instruction(OpCode.PUSH_INT, 2),
                Instruction(OpCode.TEXT_GET),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.PUSH_TEXT, "svāgatam"),
                Instruction(OpCode.PUSH_INT, 0),
                Instruction(OpCode.PUSH_INT, 3),
                Instruction(OpCode.TEXT_SLICE),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.PUSH_TEXT, "svāgatam"),
                Instruction(OpCode.PUSH_TEXT, "gata"),
                Instruction(OpCode.TEXT_CONTAINS),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )

        self.assertEqual(SanskriptVM().execute(program), ["svagata", "8", "ā", "svā", "1"])

    def test_text_ast_and_source_forms(self) -> None:
        ast_program = Program(
            (
                TextConcat("phala", TextLiteral("sva"), TextLiteral("gata")),
                Display(Reference("phala")),
                TextLength("māna", Reference("phala")),
                Display(Reference("māna")),
                TextGet("akṣara", Reference("phala"), TextLiteral("2")),
                TextSlice("bhāga", Reference("phala"), TextLiteral("0"), TextLiteral("3")),
                TextContains("asti", Reference("phala"), TextLiteral("gata")),
            )
        )

        # Use source for numeric indices; the AST above checks lowering types only.
        compile_program(ast_program)
        program = compile_source(
            """
            vākyasaṃyogaḥ phale vākyam sva iti vākyam gata iti.
            gaṇakaḥ phalaṃ darśayati.
            vākyaparimāṇam māna phala.
            darśanam māna.
            vākyāharaṇam akṣara phala dvi.
            darśanam akṣara.
            vākyacchedaḥ bhāga phala śūnya tri.
            darśanam bhāga.
            vākyāsti tattvam phala vākyam gata iti.
            darśanam tattvam.
            """
        )

        self.assertEqual(SanskriptVM().execute(program), ["svagata", "7", "a", "sva", "1"])

    def test_text_primitives_round_trip_through_json_and_prose_machine_text(self) -> None:
        program = compile_source(
            """
            vākyasaṃyogaḥ phale vākyam sva iti vākyam gata iti.
            vākyaparimāṇam māna phala.
            darśanam māna.
            """
        )
        restored_json = decode_program(encode_program(program))
        prose = program_to_yantra_patha(program)
        restored_prose = program_from_yantra_patha(prose)

        self.assertIn("vākyayoḥ saṃyogaḥ kriyate.", prose)
        self.assertIn("vākyasya parimāṇam gṛhyate.", prose)
        self.assertEqual(restored_json.instructions, program.instructions)
        self.assertEqual(restored_prose.instructions, program.instructions)
        self.assertEqual(SanskriptVM().execute(restored_prose), ["7"])


if __name__ == "__main__":
    unittest.main()
