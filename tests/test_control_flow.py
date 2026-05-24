import unittest

from sanskript.ast import Assign, CompareEq, Display, If, Increase, Literal, Program, Reference, While
from sanskript.bytecode import OpCode, decode_program, encode_program
from sanskript.compiler import compile_program
from sanskript.vm import SanskriptVM


class ControlFlowTests(unittest.TestCase):
    def test_if_branch_via_ast(self) -> None:
        program = Program(
            (
                Assign("phala", Literal(3)),
                If(
                    CompareEq(Reference("phala"), Literal(3)),
                    (Increase("phala", Literal(10)),),
                    (Increase("phala", Literal(1)),),
                ),
                Display(Reference("phala")),
            )
        )
        output = SanskriptVM().execute(compile_program(program))
        self.assertEqual(output, ["13"])

    def test_if_else_branch_via_ast(self) -> None:
        program = Program(
            (
                Assign("phala", Literal(2)),
                If(
                    CompareEq(Reference("phala"), Literal(3)),
                    (Increase("phala", Literal(10)),),
                    (Increase("phala", Literal(1)),),
                ),
                Display(Reference("phala")),
            )
        )
        output = SanskriptVM().execute(compile_program(program))
        self.assertEqual(output, ["3"])

    def test_while_loop_via_ast(self) -> None:
        program = Program(
            (
                Assign("phala", Literal(0)),
                While(
                    CompareEq(Reference("phala"), Literal(0)),
                    (Increase("phala", Literal(1)),),
                ),
                Display(Reference("phala")),
            )
        )
        # Loop runs once: 0 == 0, increments to 1, then exits
        output = SanskriptVM().execute(compile_program(program))
        self.assertEqual(output, ["1"])

    def test_bytecode_v2_round_trip_with_jumps(self) -> None:
        program = compile_program(
            Program(
                (
                    Assign("x", Literal(1)),
                    If(
                        CompareEq(Reference("x"), Literal(1)),
                        (Assign("x", Literal(9)),),
                        (),
                    ),
                    Display(Reference("x")),
                )
            )
        )
        payload = encode_program(program, version=2)
        restored = decode_program(payload)
        self.assertEqual(SanskriptVM().execute(restored), ["9"])
        ops = {inst.opcode for inst in restored.instructions}
        self.assertIn(OpCode.JUMP_IF_ZERO, ops)
