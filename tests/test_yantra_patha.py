import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode, dump_bytecode_file, load_bytecode_file
from sanskript.cli import main
from sanskript.compiler import compile_source
from sanskript.vm import SanskriptVM
from sanskript.yantra_patha import program_from_yantra_patha, program_to_yantra_patha


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


class YantraPathaTests(unittest.TestCase):
    def test_hand_written_prose_assembles_and_runs(self) -> None:
        source = """
        saṃskaraṇam dvitīyam.
        mukhyaḥ pāṭhaḥ ārabhyate.
        pañca iti pūrṇāṅkaḥ nikṣipyate.
        phala iti nāma sthāpyate.
        phala iti nāma āhriyate.
        darśanam kriyate.
        virāmaḥ kriyate.
        pāṭhaḥ samāpyate.
        """

        program = program_from_yantra_patha(source)

        self.assertEqual(SanskriptVM().execute(program), ["5"])

    def test_compiled_program_round_trips_through_prose_bytecode(self) -> None:
        program = compile_source((EXAMPLES / "navama-kṣetram.ssk").read_text(encoding="utf-8"))
        prose = program_to_yantra_patha(program)

        self.assertIn("gaṇita iti kṣetram ārabhyate.", prose)
        self.assertIn("gaṇita iti kṣetre vṛddhi iti vidhānam āhūyate.", prose)
        self.assertNotRegex(prose, r"[{}\\[\\]();:=<>]")

        restored = program_from_yantra_patha(prose)

        self.assertEqual(SanskriptVM().execute(restored), SanskriptVM().execute(program))

    def test_all_v2_opcodes_have_prose_forms(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 5),
                Instruction(OpCode.PUSH_INT, 2),
                Instruction(OpCode.ADD),
                Instruction(OpCode.PUSH_INT, 3),
                Instruction(OpCode.MULTIPLY),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.SUBTRACT),
                Instruction(OpCode.PUSH_INT, 2),
                Instruction(OpCode.DIVIDE),
                Instruction(OpCode.PUSH_INT, 10),
                Instruction(OpCode.COMPARE_LT),
                Instruction(OpCode.JUMP_IF_ZERO, 16),
                Instruction(OpCode.PUSH_INT, 7),
                Instruction(OpCode.STORE_NAME, "phala"),
                Instruction(OpCode.JUMP, 18),
                Instruction(OpCode.PUSH_INT, 0),
                Instruction(OpCode.STORE_NAME, "phala"),
                Instruction(OpCode.LOAD_NAME, "phala"),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )

        restored = program_from_yantra_patha(program_to_yantra_patha(program))

        self.assertEqual(restored.instructions, program.instructions)

    def test_cli_disassemble_assemble_and_run_yantra_patha(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bytecode_path = Path(tmp) / "program.sskbc"
            prose_path = Path(tmp) / "program.sskyp"
            restored_path = Path(tmp) / "restored.sskbc"
            program = compile_source((EXAMPLES / "prathama.ssk").read_text(encoding="utf-8"))
            dump_bytecode_file(program, bytecode_path)

            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["disassemble", str(bytecode_path), "-o", str(prose_path)]), 0)
                self.assertEqual(main(["assemble", str(prose_path), "-o", str(restored_path)]), 0)

            self.assertEqual(
                SanskriptVM().execute(load_bytecode_file(restored_path)),
                SanskriptVM().execute(program),
            )

            run_stdout = io.StringIO()
            with redirect_stdout(run_stdout):
                self.assertEqual(main(["run", str(prose_path)]), 0)
            self.assertEqual(run_stdout.getvalue().strip().splitlines(), ["7"])


if __name__ == "__main__":
    unittest.main()
