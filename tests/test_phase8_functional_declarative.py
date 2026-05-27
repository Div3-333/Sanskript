"""Phase 8: functional and declarative programming."""

from __future__ import annotations

import unittest

from sanskript.ast import (
    Assign,
    BinaryValue,
    Call,
    CompareGt,
    Display,
    FunctionDef,
    If,
    ImmutableListAppend,
    ImmutableListInit,
    ListAll,
    ListAny,
    ListAppend,
    ListComprehension,
    ListEnumerate,
    ListFilter,
    ListGet,
    ListInit,
    ListMap,
    ListReduce,
    ListScan,
    ListZip,
    Literal,
    PipelineChain,
    Program,
    Reference,
    Return,
)
from sanskript.bytecode import Instruction, OpCode, decode_program, encode_program
from sanskript.compiler import compile_program, compile_source
from sanskript.errors import RuntimeSanskriptError, TypeCheckError
from sanskript.parser import parse_program
from sanskript.vm import SanskriptVM
from sanskript.yantra_patha import _render_instruction


def _run(program: Program) -> list[str]:
    return SanskriptVM().execute(compile_program(program))


class FunctionalCoreTests(unittest.TestCase):
    def test_map_filter_reduce_pipeline(self) -> None:
        prog = Program(
            (
                ListInit("items"),
                ListAppend("items", Literal(1)),
                ListAppend("items", Literal(2)),
                ListAppend("items", Literal(3)),
                ListAppend("items", Literal(4)),
                ListMap("doubled", "items", "double"),
                ListFilter("large", "doubled", "greater_than_four"),
                ListReduce("sum", "large", "add_pair", Literal(0)),
                Display(Reference("sum")),
            ),
            functions=(
                FunctionDef(
                    "double",
                    (Return(BinaryValue("multiply", Reference("x"), Literal(2))),),
                    params=("x",),
                    param_types=("i32",),
                ),
                FunctionDef(
                    "greater_than_four",
                    (
                        If(
                            CompareGt(Reference("x"), Literal(4)),
                            (Return(Literal(1)),),
                            (Return(Literal(0)),),
                        ),
                    ),
                    params=("x",),
                    param_types=("i32",),
                ),
                FunctionDef(
                    "add_pair",
                    (Return(BinaryValue("add", Reference("a"), Reference("b"))),),
                    params=("a", "b"),
                    param_types=("i32", "i32"),
                ),
            ),
        )
        self.assertEqual(_run(prog), ["14"])

    def test_all_and_any(self) -> None:
        prog = Program(
            (
                ListInit("items"),
                ListAppend("items", Literal(3)),
                ListAppend("items", Literal(5)),
                ListAll("ok", "items", "always_true"),
                ListAny("some", "items", "never_true"),
                Display(Reference("ok")),
                Display(Reference("some")),
            ),
            functions=(
                FunctionDef(
                    "always_true",
                    (Return(Literal(1)),),
                    params=("x",),
                ),
                FunctionDef(
                    "never_true",
                    (Return(Literal(0)),),
                    params=("x",),
                ),
            ),
        )
        self.assertEqual(_run(prog), ["1", "0"])

    def test_scan_zip_enumerate(self) -> None:
        prog = Program(
            (
                ListInit("a"),
                ListAppend("a", Literal(1)),
                ListAppend("a", Literal(2)),
                ListInit("b"),
                ListAppend("b", Literal(10)),
                ListAppend("b", Literal(20)),
                ListScan("scans", "a", "add_pair", Literal(0)),
                ListZip("pairs", "a", "b"),
                ListEnumerate("numbered", "a"),
                Display(Reference("scans")),
                Display(Reference("pairs")),
                Display(Reference("numbered")),
            ),
            functions=(
                FunctionDef(
                    "add_pair",
                    (Return(BinaryValue("add", Reference("a"), Reference("b"))),),
                    params=("a", "b"),
                ),
            ),
        )
        out = _run(prog)
        self.assertEqual(len(out), 3)
        self.assertIn("3", out[0])

    def test_map_does_not_mutate_input(self) -> None:
        prog = Program(
            (
                ListInit("items"),
                ListAppend("items", Literal(10)),
                ListMap("mapped", "items", "double"),
                ListGet("first_original", "items", Literal(0)),
                ListGet("first_mapped", "mapped", Literal(0)),
                Display(Reference("first_original")),
                Display(Reference("first_mapped")),
            ),
            functions=(
                FunctionDef(
                    "double",
                    (Return(BinaryValue("multiply", Reference("x"), Literal(2))),),
                    params=("x",),
                ),
            ),
        )
        self.assertEqual(_run(prog), ["10", "20"])


class FunctionalSourceTests(unittest.TestCase):
    def test_parse_phase8_directives_from_source(self) -> None:
        src = """
samūhaḥ saṅkhyāḥ.
yojanam saṅkhyāḥ eka.
yojanam saṅkhyāḥ dvi.
yojanam saṅkhyāḥ tri.
vidhānam dviguṇa x.
pratyāvartanam x guṇanam dvi.
samāpanam.
vidhānam saṅkalanam a b.
pratyāvartanam a yoga b.
samāpanam.
vidhānam satyam-asti x.
pratyāvartanam x.
samāpanam.
māpanam phalam saṅkhyāḥ dviguṇa.
śodhanam cayanam phalam satyam-asti.
saṅkocanam saṅkṣepaḥ cayanam saṅkalanam śūnya.
darśanam saṅkṣepaḥ.
"""
        out = SanskriptVM().execute(compile_source(src))
        self.assertEqual(out, ["12"])
        prog = parse_program(src)
        self.assertGreaterEqual(len(prog.statements), 1)

    def test_immutable_list_and_comprehension_ast(self) -> None:
        prog = Program(
            (
                ImmutableListInit("n1"),
                ImmutableListAppend("n2", "n1", Literal(1)),
                ImmutableListAppend("n3", "n2", Literal(2)),
                ListComprehension("out", "n3", "always_true", "double"),
                Display(Reference("out")),
            ),
            functions=(
                FunctionDef("always_true", (Return(Literal(1)),), params=("x",)),
                FunctionDef(
                    "double",
                    (Return(BinaryValue("multiply", Reference("x"), Literal(2))),),
                    params=("x",),
                ),
            ),
        )
        self.assertEqual(_run(prog), ["[2, 4]"])

    def test_pipeline_scan_any_ast(self) -> None:
        prog = Program(
            (
                ListInit("items"),
                ListAppend("items", Literal(1)),
                ListAppend("items", Literal(2)),
                PipelineChain("out", "items", ("double",)),
                ListScan("scans", "items", "add_pair", Literal(0)),
                ListAny("any_ok", "out", "always_true"),
                Display(Reference("scans")),
                Display(Reference("any_ok")),
            ),
            functions=(
                FunctionDef(
                    "double",
                    (Return(BinaryValue("multiply", Reference("x"), Literal(2))),),
                    params=("x",),
                ),
                FunctionDef(
                    "add_pair",
                    (Return(BinaryValue("add", Reference("a"), Reference("b"))),),
                    params=("a", "b"),
                ),
                FunctionDef("always_true", (Return(Literal(1)),), params=("x",)),
            ),
        )
        out = _run(prog)
        self.assertEqual(len(out), 2)

    def test_pure_function_rejects_emit(self) -> None:
        prog = Program(
            statements=(),
            functions=(
                FunctionDef(
                    "bad",
                    (Display(Literal(1)),),
                    effect="pure",
                ),
            ),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(
                Program(
                    (Call("bad"),),
                    functions=prog.functions,
                )
            )


class FunctionalNegativeTests(unittest.TestCase):
    def test_map_requires_list_container(self) -> None:
        prog = Program(
            (
                Assign("not_list", Literal(3)),
                ListMap("out", "not_list", "double"),
            ),
            functions=(
                FunctionDef(
                    "double",
                    (Return(BinaryValue("multiply", Reference("x"), Literal(2))),),
                    params=("x",),
                ),
            ),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(prog)

    def test_reduce_arity_mismatch_raises_runtime_error(self) -> None:
        prog = Program(
            (
                ListInit("items"),
                ListAppend("items", Literal(1)),
                ListReduce("sum", "items", "bad_reduce", Literal(0)),
            ),
            functions=(
                FunctionDef(
                    "bad_reduce",
                    (Return(Reference("x")),),
                    params=("x",),
                ),
            ),
        )
        with self.assertRaises(RuntimeSanskriptError):
            _run(prog)


class FunctionalBytecodeRoundTripTests(unittest.TestCase):
    def test_phase8_opcodes_have_yantra_patha(self) -> None:
        for op in (
            OpCode.LIST_SCAN,
            OpCode.LIST_ZIP,
            OpCode.IMMUTABLE_LIST_NEW,
            OpCode.PIPELINE_CHAIN,
            OpCode.GENERATOR_YIELD,
        ):
            prose = _render_instruction(Instruction(OpCode(op), "fn"))
            self.assertTrue(prose.endswith("."))

    def test_bytecode_round_trip_list_map(self) -> None:
        prog = compile_program(
            Program(
                (ListInit("x"), ListAppend("x", Literal(1)), ListMap("y", "x", "id")),
                functions=(FunctionDef("id", (Return(Reference("v")),), params=("v",)),),
            ),
        )
        payload = encode_program(prog)
        restored = decode_program(payload)
        self.assertEqual(restored.instructions[0].opcode, OpCode.LIST_NEW)


if __name__ == "__main__":
    unittest.main()
