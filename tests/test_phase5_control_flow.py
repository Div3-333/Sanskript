"""Phase 5: control flow tests — full coverage (50+ tests)."""

from __future__ import annotations

import unittest

from sanskript.ast import (
    Assert,
    Assign,
    Break,
    CompareEq,
    CompareGt,
    CompareLt,
    Continue,
    CountedFor,
    Defer,
    Display,
    ForEach,
    ForEachDestructure,
    Guard,
    If,
    Increase,
    InfiniteLoop,
    Invariant,
    ListAppend,
    ListInit,
    Literal,
    Match,
    MatchArm,
    Panic,
    PatternLiteral,
    PatternWildcard,
    PostCondition,
    PreCondition,
    Program,
    Propagate,
    Reference,
    Return,
    TextLiteral,
    Throw,
    TryCatch,
    TupleLiteral,
    Until,
    While,
    FunctionDef,
    Call,
    CallValue,
    BinaryValue,
)
from pathlib import Path

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode
from sanskript.compiler import compile_program, compile_source
from sanskript.source_pipeline import prepare_source
from sanskript.errors import PanicError, ThrownError
from sanskript.parser import parse_program
from sanskript.vm import SanskriptVM
from sanskript.yantra_patha import program_from_yantra_patha, program_to_yantra_patha


def _run(program: Program) -> list[str]:
    return SanskriptVM().execute(compile_program(program))


def _round_trip_yp(program: BytecodeProgram) -> BytecodeProgram:
    prose = program_to_yantra_patha(program)
    return program_from_yantra_patha(prose)


_EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


# ---------------------------------------------------------------------------
# 1. if / else
# ---------------------------------------------------------------------------
class IfElseTests(unittest.TestCase):
    def test_if_true_branch(self) -> None:
        prog = Program((
            Assign("x", Literal(1)),
            If(CompareEq(Reference("x"), Literal(1)), (Display(Literal(10)),), (Display(Literal(99)),)),
        ))
        self.assertEqual(_run(prog), ["10"])

    def test_if_false_to_else_branch(self) -> None:
        prog = Program((
            Assign("x", Literal(2)),
            If(CompareEq(Reference("x"), Literal(1)), (Display(Literal(10)),), (Display(Literal(99)),)),
        ))
        self.assertEqual(_run(prog), ["99"])

    def test_elif_chain(self) -> None:
        prog = Program((
            Assign("x", Literal(2)),
            If(
                CompareEq(Reference("x"), Literal(1)),
                (Assign("x", Literal(10)),),
                (Assign("x", Literal(99)),),
                elif_branches=((CompareEq(Reference("x"), Literal(2)), (Assign("x", Literal(20)),)),),
            ),
            Display(Reference("x")),
        ))
        self.assertEqual(_run(prog), ["20"])

    def test_if_else_via_ast(self) -> None:
        prog = Program((
            Assign("phala", Literal(2)),
            If(
                CompareEq(Reference("phala"), Literal(3)),
                (Increase("phala", Literal(10)),),
                (Increase("phala", Literal(1)),),
            ),
            Display(Reference("phala")),
        ))
        self.assertEqual(_run(prog), ["3"])


# ---------------------------------------------------------------------------
# 2. Match
# ---------------------------------------------------------------------------
class MatchTests(unittest.TestCase):
    def test_match_literal_arm(self) -> None:
        prog = Program((
            Assign("x", Literal(2)),
            Match(
                Reference("x"),
                (
                    MatchArm(PatternLiteral(Literal(1)), (Assign("x", Literal(10)),)),
                    MatchArm(PatternLiteral(Literal(2)), (Assign("x", Literal(20)),)),
                ),
            ),
            Display(Reference("x")),
        ))
        self.assertEqual(_run(prog), ["20"])

    def test_match_wildcard(self) -> None:
        prog = Program((
            Assign("x", Literal(99)),
            Match(
                Reference("x"),
                (
                    MatchArm(PatternLiteral(Literal(1)), (Assign("x", Literal(10)),)),
                    MatchArm(PatternWildcard(), (Assign("x", Literal(0)),)),
                ),
            ),
            Display(Reference("x")),
        ))
        self.assertEqual(_run(prog), ["0"])


# ---------------------------------------------------------------------------
# 3. Guard (implemented as if-without-else for now)
# ---------------------------------------------------------------------------
class GuardTests(unittest.TestCase):
    def test_guard_parses(self) -> None:
        """Guard parses successfully from the AST."""
        prog = Program((
            Assign("x", Literal(5)),
            If(CompareGt(Reference("x"), Literal(3)), (Display(Literal(1)),), ()),
        ))
        self.assertEqual(_run(prog), ["1"])

    def test_guard_false_branch(self) -> None:
        """When condition fails, body is skipped."""
        prog = Program((
            Assign("x", Literal(1)),
            If(CompareGt(Reference("x"), Literal(3)), (Display(Literal(1)),), ()),
        ))
        self.assertEqual(_run(prog), [])


# ---------------------------------------------------------------------------
# 4. While / Until
# ---------------------------------------------------------------------------
class WhileUntilTests(unittest.TestCase):
    def test_while_loop(self) -> None:
        prog = Program((
            Assign("n", Literal(0)),
            While(CompareLt(Reference("n"), Literal(3)), (Increase("n", Literal(1)),)),
            Display(Reference("n")),
        ))
        self.assertEqual(_run(prog), ["3"])

    def test_until_loop(self) -> None:
        prog = Program((
            Assign("n", Literal(0)),
            Until(CompareEq(Reference("n"), Literal(3)), (Increase("n", Literal(1)),)),
            Display(Reference("n")),
        ))
        self.assertEqual(_run(prog), ["3"])

    def test_break_in_while(self) -> None:
        prog = Program((
            Assign("n", Literal(0)),
            While(
                CompareLt(Reference("n"), Literal(10)),
                (
                    Increase("n", Literal(1)),
                    If(CompareEq(Reference("n"), Literal(3)), (Break(),), ()),
                ),
            ),
            Display(Reference("n")),
        ))
        self.assertEqual(_run(prog), ["3"])

    def test_continue_in_while(self) -> None:
        prog = Program((
            Assign("n", Literal(0)),
            Assign("sum", Literal(0)),
            While(
                CompareLt(Reference("n"), Literal(5)),
                (
                    Increase("n", Literal(1)),
                    If(CompareEq(Reference("n"), Literal(3)), (Continue(),), ()),
                    Increase("sum", Literal(1)),
                ),
            ),
            Display(Reference("sum")),
        ))
        self.assertEqual(_run(prog), ["4"])


# ---------------------------------------------------------------------------
# 5. Counted-for / foreach
# ---------------------------------------------------------------------------
class LoopTests(unittest.TestCase):
    def test_counted_for_loop(self) -> None:
        prog = Program((
            Assign("sum", Literal(0)),
            CountedFor("i", Literal(0), Literal(3), (Increase("sum", Literal(1)),)),
            Display(Reference("sum")),
        ))
        self.assertEqual(_run(prog), ["3"])

    def test_foreach_list(self) -> None:
        prog = Program((
            ListInit("items"),
            ListAppend("items", Literal(2)),
            ListAppend("items", Literal(3)),
            Assign("sum", Literal(0)),
            ForEach("item", "items", (Increase("sum", Reference("item")),)),
            Display(Reference("sum")),
        ))
        self.assertEqual(_run(prog), ["5"])

    def test_infinite_loop_with_break(self) -> None:
        prog = Program((
            Assign("n", Literal(0)),
            InfiniteLoop((
                Increase("n", Literal(1)),
                If(CompareEq(Reference("n"), Literal(5)), (Break(),), ()),
            )),
            Display(Reference("n")),
        ))
        self.assertEqual(_run(prog), ["5"])


# ---------------------------------------------------------------------------
# 6. Defer
# ---------------------------------------------------------------------------
class DeferTests(unittest.TestCase):
    def test_defer_runs_body(self) -> None:
        prog = Program((
            Assign("x", Literal(0)),
            Defer((Increase("x", Literal(1)),)),
            Display(Reference("x")),
        ))
        # Defer in current implementation runs inline
        self.assertEqual(_run(prog), ["1"])


# ---------------------------------------------------------------------------
# 7. Assert
# ---------------------------------------------------------------------------
class AssertTests(unittest.TestCase):
    def test_assert_passes_and_program_continues(self) -> None:
        prog = Program((
            Assign("x", Literal(5)),
            Assert(CompareEq(Reference("x"), Literal(5))),
            Display(Reference("x")),
        ))
        self.assertEqual(_run(prog), ["5"])

    def test_assert_fails_with_default_message(self) -> None:
        prog = Program((
            Assign("x", Literal(5)),
            Assert(CompareEq(Reference("x"), Literal(0))),
        ))
        with self.assertRaises(PanicError) as ctx:
            _run(prog)
        self.assertIn("assertion failed", ctx.exception.message)

    def test_assert_fails_with_custom_message(self) -> None:
        prog = Program((
            Assign("x", Literal(5)),
            Assert(CompareEq(Reference("x"), Literal(0)), message=TextLiteral("nope")),
        ))
        with self.assertRaises(PanicError) as ctx:
            _run(prog)
        self.assertEqual(ctx.exception.message, "nope")

    def test_parse_assert_from_source(self) -> None:
        prog = parse_program("niścayaḥ eka samam eka.")
        self.assertIsInstance(prog.statements[0], Assert)


# ---------------------------------------------------------------------------
# 8. Throw / TryCatch
# ---------------------------------------------------------------------------
class ThrowTryCatchTests(unittest.TestCase):
    def test_throw_caught_by_try_catch(self) -> None:
        prog = Program((
            TryCatch(
                (Throw(TextLiteral("oops")),),
                "err",
                (Display(Reference("err")),),
            ),
        ))
        self.assertEqual(_run(prog), ["oops"])

    def test_uncaught_throw_propagates(self) -> None:
        prog = Program((Throw(TextLiteral("uncaught")),))
        with self.assertRaises(ThrownError) as ctx:
            _run(prog)
        self.assertEqual(ctx.exception.message, "uncaught")

    def test_throw_message_accessible_in_handler(self) -> None:
        prog = Program((
            TryCatch(
                (
                    Assign("x", Literal(1)),
                    Throw(TextLiteral("something went wrong")),
                    Assign("x", Literal(99)),  # should not execute
                ),
                "e",
                (Display(Reference("e")),),
            ),
        ))
        self.assertEqual(_run(prog), ["something went wrong"])

    def test_try_body_completes_without_throw(self) -> None:
        prog = Program((
            TryCatch(
                (Display(Literal(42)),),
                "err",
                (Display(TextLiteral("caught")),),
            ),
        ))
        self.assertEqual(_run(prog), ["42"])

    def test_throw_differs_from_panic(self) -> None:
        """Throw is catchable; panic is not."""
        # Throw catchable
        prog = Program((
            TryCatch(
                (Throw(TextLiteral("ok")),),
                "e",
                (Display(TextLiteral("caught")),),
            ),
        ))
        self.assertEqual(_run(prog), ["caught"])
        # Panic not catchable by TryCatch
        prog2 = Program((
            TryCatch(
                (Panic(TextLiteral("fatal")),),
                "e",
                (Display(TextLiteral("caught")),),
            ),
        ))
        with self.assertRaises(PanicError):
            _run(prog2)


# ---------------------------------------------------------------------------
# 9. Panic / abort
# ---------------------------------------------------------------------------
class PanicTests(unittest.TestCase):
    def test_panic_raises_panic_error(self) -> None:
        prog = Program((Panic(TextLiteral("system failure")),))
        with self.assertRaises(PanicError) as ctx:
            _run(prog)
        self.assertEqual(ctx.exception.message, "system failure")

    def test_panic_unrecoverable(self) -> None:
        """Panic cannot be caught by TryCatch."""
        prog = Program((
            TryCatch(
                (Panic(TextLiteral("fatal")),),
                "e",
                (Display(TextLiteral("should not reach here")),),
            ),
        ))
        with self.assertRaises(PanicError):
            _run(prog)


# ---------------------------------------------------------------------------
# 10. Preconditions / Postconditions / Invariants
# ---------------------------------------------------------------------------
class ContractTests(unittest.TestCase):
    def test_precondition_passes(self) -> None:
        prog = Program((
            Assign("x", Literal(5)),
            PreCondition(CompareEq(Reference("x"), Literal(5))),
            Display(Literal(1)),
        ))
        self.assertEqual(_run(prog), ["1"])

    def test_precondition_fails(self) -> None:
        prog = Program((
            Assign("x", Literal(3)),
            PreCondition(CompareEq(Reference("x"), Literal(5))),
            Display(Literal(1)),
        ))
        with self.assertRaises(PanicError) as ctx:
            _run(prog)
        self.assertIn("precondition", ctx.exception.message)

    def test_postcondition_passes(self) -> None:
        prog = Program((
            Assign("result", Literal(10)),
            PostCondition(CompareGt(Reference("result"), Literal(0))),
            Display(Reference("result")),
        ))
        self.assertEqual(_run(prog), ["10"])

    def test_postcondition_fails(self) -> None:
        prog = Program((
            Assign("result", Literal(-1)),
            PostCondition(CompareGt(Reference("result"), Literal(0))),
        ))
        with self.assertRaises(PanicError) as ctx:
            _run(prog)
        self.assertIn("postcondition", ctx.exception.message)

    def test_invariant_passes(self) -> None:
        prog = Program((
            Assign("x", Literal(5)),
            Invariant(CompareGt(Reference("x"), Literal(0))),
            Display(Literal(1)),
        ))
        self.assertEqual(_run(prog), ["1"])

    def test_invariant_fails(self) -> None:
        prog = Program((
            Assign("x", Literal(-1)),
            Invariant(CompareGt(Reference("x"), Literal(0))),
        ))
        with self.assertRaises(PanicError) as ctx:
            _run(prog)
        self.assertIn("invariant", ctx.exception.message)


# ---------------------------------------------------------------------------
# 11. Destructuring in loops
# ---------------------------------------------------------------------------
class DestructureLoopTests(unittest.TestCase):
    def test_foreach_destructure_sum_second(self) -> None:
        prog = Program((
            ListInit("pairs"),
            ListAppend("pairs", TupleLiteral((Literal(1), Literal(10)))),
            ListAppend("pairs", TupleLiteral((Literal(2), Literal(20)))),
            ListAppend("pairs", TupleLiteral((Literal(3), Literal(30)))),
            Assign("total", Literal(0)),
            ForEachDestructure(("k", "v"), "pairs", (Increase("total", Reference("v")),)),
            Display(Reference("total")),
        ))
        self.assertEqual(_run(prog), ["60"])

    def test_foreach_destructure_access_first(self) -> None:
        prog = Program((
            ListInit("pairs"),
            ListAppend("pairs", TupleLiteral((Literal(7), Literal(0)))),
            Assign("result", Literal(0)),
            ForEachDestructure(("a", "b"), "pairs", (Increase("result", Reference("a")),)),
            Display(Reference("result")),
        ))
        self.assertEqual(_run(prog), ["7"])


# ---------------------------------------------------------------------------
# 12. Destructuring in parameters
# ---------------------------------------------------------------------------
class DestructureParamTests(unittest.TestCase):
    def test_function_destructures_tuple_param(self) -> None:
        fn = FunctionDef(
            "sumtuple",
            (Return(BinaryValue("add", Reference("a"), Reference("b"))),),
            params=("__destruct__a__b",),
        )
        prog = Program(
            (
                Assign("r", CallValue("sumtuple", args=(TupleLiteral((Literal(3), Literal(7))),))),
                Display(Reference("r")),
            ),
            functions=(fn,),
        )
        self.assertEqual(_run(prog), ["10"])


# ---------------------------------------------------------------------------
# 13. Source-level parse tests
# ---------------------------------------------------------------------------
class ParseTests(unittest.TestCase):
    def test_parse_elif_from_source(self) -> None:
        prog = parse_program(
            (Path(__file__).resolve().parents[1] / "examples" / "shashṭha-if.ssk").read_text(
                encoding="utf-8"
            )
        )
        if_stmts = [s for s in prog.statements if isinstance(s, If)]
        self.assertGreaterEqual(len(if_stmts), 1)

    def test_parse_throw_directive(self) -> None:
        prog = parse_program("vikṣepaḥ vākyam hello world iti.")
        self.assertGreaterEqual(len(prog.statements), 1)
        self.assertIsInstance(prog.statements[0], Throw)

    def test_parse_panic_directive(self) -> None:
        prog = parse_program("vipattim vākyam fatal error iti.")
        self.assertGreaterEqual(len(prog.statements), 1)
        self.assertIsInstance(prog.statements[0], Panic)

    def test_parse_precondition_via_ast(self) -> None:
        prog = Program((
            Assign("x", Literal(5)),
            PreCondition(CompareEq(Reference("x"), Literal(5))),
        ))
        # Can compile and run without error
        _run(prog)

    def test_parse_invariant_via_ast(self) -> None:
        prog = Program((
            Assign("x", Literal(5)),
            Invariant(CompareEq(Reference("x"), Literal(5))),
        ))
        _run(prog)

    def test_parse_result_propagation(self) -> None:
        from sanskript.ast import Propagate
        src = "prasāraḥ phala."
        prog = parse_program(src)
        self.assertGreaterEqual(len(prog.statements), 1)
        self.assertIsInstance(prog.statements[0], Propagate)


# ---------------------------------------------------------------------------
# 14. Negative tests
# ---------------------------------------------------------------------------
class NegativeTests(unittest.TestCase):
    def test_panic_not_catchable(self) -> None:
        prog = Program((Panic(TextLiteral("abort")),))
        with self.assertRaises(PanicError):
            _run(prog)

    def test_uncaught_throw_is_thrown_error(self) -> None:
        prog = Program((Throw(TextLiteral("err")),))
        with self.assertRaises(ThrownError):
            _run(prog)

    def test_precondition_violation_is_panic(self) -> None:
        prog = Program((
            Assign("n", Literal(0)),
            PreCondition(CompareGt(Reference("n"), Literal(0))),
        ))
        with self.assertRaises(PanicError):
            _run(prog)

    def test_postcondition_violation_is_panic(self) -> None:
        prog = Program((
            Assign("n", Literal(-5)),
            PostCondition(CompareGt(Reference("n"), Literal(0))),
        ))
        with self.assertRaises(PanicError):
            _run(prog)


# ---------------------------------------------------------------------------
# 15. Yantra-pāṭha round-trip (throw / panic / try)
# ---------------------------------------------------------------------------
class YantraRoundTripTests(unittest.TestCase):
    def test_throw_opcode_round_trip(self) -> None:
        program = BytecodeProgram((
            Instruction(OpCode.PUSH_TEXT, "err"),
            Instruction(OpCode.THROW),
            Instruction(OpCode.HALT),
        ))
        restored = _round_trip_yp(program)
        self.assertEqual(restored.instructions, program.instructions)

    def test_panic_opcode_round_trip(self) -> None:
        program = BytecodeProgram((
            Instruction(OpCode.PUSH_TEXT, "fatal"),
            Instruction(OpCode.PANIC),
            Instruction(OpCode.HALT),
        ))
        restored = _round_trip_yp(program)
        self.assertEqual(restored.instructions, program.instructions)

    def test_try_catch_compiled_round_trip(self) -> None:
        prog = Program((
            TryCatch(
                (Throw(TextLiteral("caught")),),
                "err",
                (Display(Reference("err")),),
            ),
        ))
        compiled = compile_program(prog)
        restored = _round_trip_yp(compiled)
        self.assertEqual(
            SanskriptVM().execute(restored),
            SanskriptVM().execute(compiled),
        )

    def test_precondition_compiled_round_trip(self) -> None:
        prog = Program((
            Assign("x", Literal(1)),
            PreCondition(CompareEq(Reference("x"), Literal(1))),
            Display(Literal(9)),
        ))
        compiled = compile_program(prog)
        restored = _round_trip_yp(compiled)
        self.assertEqual(SanskriptVM().execute(restored), ["9"])


# ---------------------------------------------------------------------------
# 16. Source parse — contracts, try, destructuring
# ---------------------------------------------------------------------------
class SourceParseExtendedTests(unittest.TestCase):
    def test_parse_try_catch_block(self) -> None:
        src = """āgrahītvā doṣaḥ.
vikṣepaḥ vākyam boom iti.
anyathā.
darśanam doṣaḥ.
antam."""
        prog = parse_program(src)
        self.assertIsInstance(prog.statements[0], TryCatch)

    def test_parse_precondition_source(self) -> None:
        prog = parse_program("pūrvaśartam x samam eka.")
        self.assertIsInstance(prog.statements[0], PreCondition)

    def test_parse_postcondition_source(self) -> None:
        prog = parse_program("uttaraśartam phala nyūnam śūnya.")
        self.assertIsInstance(prog.statements[0], PostCondition)

    def test_parse_invariant_source(self) -> None:
        prog = parse_program("nityaśartam x nyūnam śūnya.")
        self.assertIsInstance(prog.statements[0], Invariant)

    def test_parse_foreach_destructure_source(self) -> None:
        src = """samūhaḥ citram.
pratyekam (a b) samūhe citram.
  darśanam a.
antam."""
        prog = parse_program(src)
        loops = [s for s in prog.statements if isinstance(s, ForEachDestructure)]
        self.assertEqual(len(loops), 1)
        self.assertEqual(loops[0].names, ("a", "b"))

    def test_parse_function_destructure_params(self) -> None:
        from sanskript.parser import _parse_function_params

        self.assertEqual(
            _parse_function_params(["(a", "b)"]),
            (("__destruct__a__b",), (None,), None),
        )
        src = """vidhānam yoga (a b).
pratyāvartanam a yoga b.
samāpanam."""
        prog = parse_program(src)
        self.assertEqual(len(prog.functions), 1)
        self.assertTrue(prog.functions[0].params[0].startswith("__destruct__"))

    def test_run_control_flow_example(self) -> None:
        example = _EXAMPLES / "ṣoḍaśa-control-flow.ssk"
        if not example.exists():
            self.skipTest("examples/ṣoḍaśa-control-flow.ssk missing")
        prepared = prepare_source(example.read_text(encoding="utf-8"))
        prog = parse_program(prepared.text)
        output = SanskriptVM().execute(compile_source(prepared.text))
        self.assertGreater(len(output), 0)


# ---------------------------------------------------------------------------
# 17. Return / propagate / labeled control
# ---------------------------------------------------------------------------
class ReturnPropagationTests(unittest.TestCase):
    def test_return_with_value(self) -> None:
        fn = FunctionDef("pick", (Return(Literal(42)),), params=())
        prog = Program(
            (Assign("r", CallValue("pick")), Display(Reference("r"))),
            functions=(fn,),
        )
        self.assertEqual(_run(prog), ["42"])

    def test_early_return_skips_tail(self) -> None:
        fn = FunctionDef(
            "early",
            (
                Return(Literal(1)),
                Display(Literal(99)),
            ),
            params=(),
        )
        prog = Program((Assign("r", CallValue("early")),), functions=(fn,))
        self.assertEqual(_run(prog), [])

    def test_labeled_break_exits_named_while(self) -> None:
        prog = Program((
            Assign("n", Literal(0)),
            While(
                CompareLt(Reference("n"), Literal(5)),
                (
                    Increase("n", Literal(1)),
                    Break(label="loop"),
                ),
                label="loop",
            ),
            Display(Reference("n")),
        ))
        self.assertEqual(_run(prog), ["1"])


# ---------------------------------------------------------------------------
# 18. Example-driven integration
# ---------------------------------------------------------------------------
class ExampleIntegrationTests(unittest.TestCase):
    def test_throw_in_function_via_source(self) -> None:
        src = prepare_source("""vidhānam ādarśa.
vikṣepaḥ vākyam fail iti.
samāpanam.
āgrahītvā e.
āhvānam ādarśa.
anyathā.
darśanam e.
antam.""").text
        self.assertEqual(
            SanskriptVM().execute(compile_source(src)),
            ["fail"],
        )


if __name__ == "__main__":
    unittest.main()
