import unittest

from sanskript.ast import Assign, Display, Increase, Literal, Reference
from sanskript.bytecode import Instruction, OpCode
from sanskript.compiler import compile_source, compile_statements, compile_statements_to_ir, lower_ir_to_bytecode
from sanskript.interpreter import Interpreter
from sanskript.ir import IREmit, IRIncrease, IRLiteral, IRProgram, IRReference, IRStore
from sanskript.vm import SanskriptVM


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

    def test_source_compiles_to_bytecode(self) -> None:
        source = """
        gaṇakaḥ pañca phale nidadhāti.
        gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
        gaṇakaḥ phalaṃ darśayati.
        """

        bytecode = compile_source(source)

        self.assertEqual(bytecode.instructions[-1], Instruction(OpCode.HALT))
        self.assertEqual(SanskriptVM().execute(bytecode), ["7"])

    def test_legacy_interpreter_facade_is_vm_backed(self) -> None:
        interpreter = Interpreter()

        interpreter.execute_statement(Assign("phala", Literal(3)))
        interpreter.execute_statement(Display(Reference("phala")))

        self.assertEqual(interpreter.output, ["3"])
        self.assertEqual(interpreter.environment, {"phala": 3})


if __name__ == "__main__":
    unittest.main()
