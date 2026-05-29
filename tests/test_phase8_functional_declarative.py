"""Phase 8: functional and declarative programming."""

from __future__ import annotations

import unittest

from sanskript.ast import (
    Assign,
    BinaryValue,
    Call,
    CompareGt,
    DataQuery,
    Display,
    FunctionDef,
    GeneratorNew,
    GeneratorNext,
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
    RuleDecl,
    RuleInvoke,
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

    def test_memoized_function_caches_repeated_calls(self) -> None:
        prog = Program(
            statements=(
                Assign("counter", Literal(0)),
                Call("gaṇanam", args=(Literal(3),)),
                Call("gaṇanam", args=(Literal(3),)),
                Display(Reference("counter")),
            ),
            functions=(
                FunctionDef(
                    "gaṇanam",
                    (
                        Assign("counter", BinaryValue("add", Reference("counter"), Literal(1))),
                        Return(BinaryValue("multiply", Reference("x"), Literal(2))),
                    ),
                    params=("x",),
                    decorators=("smaraṇa",),
                ),
            ),
        )
        self.assertEqual(_run(prog)[-1], "1")

    def test_memoized_effectful_function_rejected(self) -> None:
        src = """
saṃskāraṃ smaraṇa.
vidhānam sādhanaṃ doṣaḥ x.
pratyāvartanam x.
samāpanam.
āhvānam phalam doṣaḥ eka.
"""
        with self.assertRaises(TypeCheckError):
            compile_source(src)

    def test_lazy_iterator_and_generator_source(self) -> None:
        src = """
samūhaḥ saṅkhyāḥ.
yojanam saṅkhyāḥ eka.
yojanam saṅkhyāḥ dvi.
alasaḥ it saṅkhyāḥ.
alasāt adhika mūlya it.
darśanam adhika.
darśanam mūlya.
alasāt adhika2 mūlya2 it.
darśanam adhika2.
darśanam mūlya2.
alasāt adhika3 mūlya3 it.
darśanam adhika3.
darśanam mūlya3.

saṃskāraṃ utpadaka.
vidhānam krama.
pradānam eka.
pradānam dvi.
samāpanam.
utpādakaḥ g krama.
utpādakāt asti v g.
darśanam asti.
darśanam v.
utpādakāt asti2 v2 g.
darśanam asti2.
darśanam v2.
utpādakāt asti3 v3 g.
darśanam asti3.
darśanam v3.
"""
        out = SanskriptVM().execute(compile_source(src))
        self.assertTrue(out[:5] == ["1", "1", "1", "2", "0"])
        self.assertEqual(out[-2:], ["0", "0"])


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

    def test_reduce_arity_mismatch_rejected_by_type_checker(self) -> None:
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
        with self.assertRaises(TypeCheckError):
            compile_program(prog)

    def test_generator_requires_parameterless_function(self) -> None:
        prog = Program(
            (
                GeneratorNew("g", "make"),
                GeneratorNext("has_more", "value", "g"),
            ),
            functions=(
                FunctionDef("make", (Return(Literal(0)),), params=("x",)),
            ),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(prog)

    def test_match_expression_initializes_target_with_subject(self) -> None:
        src = """
yathā-artham phalam tri.
yathā pañca.
darśanam śūnya.
antam.
darśanam phalam.
"""
        out = SanskriptVM().execute(compile_source(src))
        self.assertEqual(out, ["3"])

    def test_rule_query_and_bind_end_to_end(self) -> None:
        prog = Program(
            statements=(
                ListInit("rows"),
                DataQuery("hits", "rows", "score", "gt4"),
                RuleInvoke("x", "raise-rule", Literal(3)),
                Display(Reference("hits")),
                Display(Reference("x")),
            ),
            functions=(
                FunctionDef(
                    "gt4",
                    (Return(Literal(1)),),
                    params=("x",),
                ),
                FunctionDef(
                    "when_small",
                    (Return(Literal(1)),),
                    params=("ctx",),
                ),
                FunctionDef(
                    "raise_score",
                    (
                        Return(Literal(8)),
                    ),
                    params=("ctx",),
                ),
            ),
            rules=(RuleDecl("raise-rule", "when_small", "raise_score"),),
        )
        out = _run(prog)
        self.assertEqual(len(out), 2)

    def test_pipeline_step_requires_unary_function(self) -> None:
        prog = Program(
            statements=(
                ListInit("items"),
                ListAppend("items", Literal(1)),
                PipelineChain("out", "items", ("needs_two",)),
            ),
            functions=(
                FunctionDef(
                    "needs_two",
                    (Return(BinaryValue("add", Reference("a"), Reference("b"))),),
                    params=("a", "b"),
                ),
            ),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(prog)

    def test_data_query_predicate_requires_unary_function(self) -> None:
        prog = Program(
            statements=(
                ListInit("rows"),
                ListAppend("rows", Literal({"score": 1})),
                DataQuery("hits", "rows", "score", "bad_pred"),
            ),
            functions=(
                FunctionDef(
                    "bad_pred",
                    (Return(Literal(1)),),
                    params=("x", "y"),
                ),
            ),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(prog)

    def test_rule_invoke_requires_declared_rule(self) -> None:
        prog = Program(
            statements=(
                RuleInvoke("out", "missing-rule", Literal({"x": 1})),
            ),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(prog)

    def test_duplicate_rule_id_rejected(self) -> None:
        prog = Program(
            statements=(Display(Literal(1)),),
            functions=(
                FunctionDef("when_true", (Return(Literal(1)),), params=("ctx",)),
                FunctionDef("then_same", (Return(Reference("ctx")),), params=("ctx",)),
            ),
            rules=(
                RuleDecl("r1", "when_true", "then_same"),
                RuleDecl("r1", "when_true", "then_same"),
            ),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(prog)

    def test_adt_enum_variant_must_be_declared(self) -> None:
        src = """
prakāra-vikalpaḥ phalam sat asat.
gaṇavikalpaḥ x phalam anyat eka.
"""
        with self.assertRaises(TypeCheckError):
            compile_source(src)

    def test_adt_enum_type_must_be_declared(self) -> None:
        src = """
gaṇavikalpaḥ x ajñāta sat eka.
"""
        with self.assertRaises(TypeCheckError):
            compile_source(src)

    def test_adt_enum_valid_variant_round_trip(self) -> None:
        src = """
prakāra-vikalpaḥ phalam sat asat.
gaṇavikalpaḥ x phalam sat eka.
darśanam x.
"""
        program = compile_source(src)
        payload = encode_program(program)
        restored = decode_program(payload)
        out = SanskriptVM().execute(restored)
        self.assertEqual(len(out), 1)
        self.assertIn("enum(phalam.sat)", out[0])


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

    def test_bytecode_round_trip_memoized_function_metadata(self) -> None:
        src = """
saṃskāraṃ smaraṇa.
vidhānam śuddhaḥ dvi-guṇa x.
pratyāvartanam x guṇanam dvi.
samāpanam.
āhvānam phalam dvi-guṇa tri.
darśanam phalam.
"""
        program = compile_source(src)
        payload = encode_program(program)
        restored = decode_program(payload)
        self.assertTrue(any(getattr(f, "is_memoized", False) for f in restored.functions))


if __name__ == "__main__":
    unittest.main()
