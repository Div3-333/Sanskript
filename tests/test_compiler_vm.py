import unittest
from pathlib import Path

from sanskript.ast import Assign, Display, Increase, Literal, Reference, TextLiteral
from sanskript.bytecode import Instruction, OpCode, encode_program, validate_bytecode
from sanskript.compiler import compile_source, compile_statements, compile_statements_to_ir, lower_ir_to_bytecode
from sanskript.interpreter import Interpreter
from sanskript.ir import IREmit, IRIncrease, IRLiteral, IRProgram, IRReference, IRStore, IRTextLiteral
from sanskript.vm import SanskriptVM


ROOT = Path(__file__).resolve().parents[1]


class CompilerVmTests(unittest.TestCase):
    def test_ast_compiles_to_sanskript_ir(self) -> None:
        program = compile_statements_to_ir(
            [
                Assign("phala", Literal(5)),
                Increase("phala", Literal(2)),
                Display(Reference("phala")),
            ]
        )

        self.assertEqual(
            program,
            IRProgram(
                (
                    IRStore("phala", IRLiteral(5)),
                    IRIncrease("phala", IRLiteral(2)),
                    IREmit(IRReference("phala")),
                )
            ),
        )

    def test_ir_lowers_to_sanskript_bytecode(self) -> None:
        bytecode = lower_ir_to_bytecode(
            IRProgram(
                (
                    IRStore("phala", IRLiteral(5)),
                    IRIncrease("phala", IRLiteral(2)),
                    IREmit(IRReference("phala")),
                )
            )
        )

        self.assertEqual(
            bytecode.instructions,
            (
                Instruction(OpCode.PUSH_INT, 5),
                Instruction(OpCode.STORE_NAME, "phala"),
                Instruction(OpCode.LOAD_NAME, "phala"),
                Instruction(OpCode.PUSH_INT, 2),
                Instruction(OpCode.ADD),
                Instruction(OpCode.STORE_NAME, "phala"),
                Instruction(OpCode.LOAD_NAME, "phala"),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            ),
        )
        from sanskript.bytecode import BYTECODE_VERSION_1

        validate_bytecode(bytecode, version=BYTECODE_VERSION_1)
        self.assertEqual(encode_program(bytecode, version=BYTECODE_VERSION_1)["version"], 1)

    def test_vm_executes_bytecode_without_ast_interpreter_semantics(self) -> None:
        bytecode = compile_statements(
            [
                Assign("phala", Literal(5)),
                Increase("phala", Literal(2)),
                Display(Reference("phala")),
            ]
        )

        vm = SanskriptVM()

        self.assertEqual(vm.execute(bytecode), ["7"])
        self.assertEqual(vm.environment["phala"], 7)
        self.assertEqual(vm.stack, [])

    def test_text_values_compile_and_execute(self) -> None:
        program = compile_statements_to_ir(
            [
                Assign("vākya", TextLiteral("svāgatam mitra")),
                Display(Reference("vākya")),
            ]
        )

        self.assertEqual(
            program.instructions,
            (
                IRStore("vākya", IRTextLiteral("svāgatam mitra")),
                IREmit(IRReference("vākya")),
            ),
        )

        bytecode = lower_ir_to_bytecode(program)
        self.assertIn(Instruction(OpCode.PUSH_TEXT, "svāgatam mitra"), bytecode.instructions)
        vm = SanskriptVM()
        self.assertEqual(vm.execute(bytecode), ["svāgatam mitra"])
        self.assertEqual(vm.environment["vākya"], "svāgatam mitra")

    def test_text_source_uses_iti_prose_not_quote_syntax(self) -> None:
        source = """
        vākyam svāgatam mitra iti phale nidadhāti.
        gaṇakaḥ phalaṃ darśayati.
        vākyam punaḥ svāgatam iti darśayati.
        """

        self.assertEqual(SanskriptVM().execute(compile_source(source)), ["svāgatam mitra", "punaḥ svāgatam"])

    def test_source_compiles_to_bytecode(self) -> None:
        source = """
        gaṇakaḥ pañca phale nidadhāti.
        gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
        gaṇakaḥ phalaṃ darśayati.
        """

        bytecode = compile_source(source)

        self.assertEqual(bytecode.instructions[-1], Instruction(OpCode.HALT))
        self.assertEqual(SanskriptVM().execute(bytecode), ["7"])

    def test_new_frame_examples_execute_through_same_runtime(self) -> None:
        expected = {
            "caturtha.ssk": ["7"],
            "pancama.ssk": ["7"],
            "shashṭha-if.ssk": ["13"],
            "saptama-while.ssk": ["2"],
            "aṣṭama-vidhānam.ssk": ["11"],
            "navama-kṣetram.ssk": ["11"],
            "dashama-vakyam.ssk": ["svāgatam mitra"],
        }
        for filename, output in expected.items():
            with self.subTest(filename=filename):
                source = (ROOT / "examples" / filename).read_text(encoding="utf-8")
                self.assertEqual(SanskriptVM().execute(compile_source(source)), output)

    def test_legacy_interpreter_facade_is_vm_backed(self) -> None:
        interpreter = Interpreter()

        interpreter.execute_statement(Assign("phala", Literal(3)))
        interpreter.execute_statement(Display(Reference("phala")))

        self.assertEqual(interpreter.output, ["3"])
        self.assertEqual(interpreter.environment, {"phala": 3})


if __name__ == "__main__":
    unittest.main()
