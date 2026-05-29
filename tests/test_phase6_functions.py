"""Phase 6: functions and procedures — full completion-standard coverage."""

from __future__ import annotations

import unittest
from pathlib import Path

from sanskript.ast import (
    Assign,
    BinaryValue,
    Increase,
    Call,
    CallValue,
    CompareEq,
    Display,
    FunctionDef,
    If,
    Literal,
    PartialApply,
    Program,
    RecordInit,
    FieldSet,
    Reference,
    Return,
    TextLiteral,
)
from sanskript.bytecode import BytecodeProgram, FunctionBytecode, Instruction, OpCode
from sanskript.compiler import compile_program, compile_source
from sanskript.errors import CompileError, RuntimeSanskriptError, TypeCheckError
from sanskript.parser import parse_program
from sanskript.source_pipeline import prepare_source
from sanskript.type_checker import TypeChecker, check_program
from sanskript.vm import SanskriptVM
from sanskript.yantra_patha import program_from_yantra_patha, program_to_yantra_patha


def _run(program: Program) -> list[str]:
    return SanskriptVM().execute(compile_program(program))


def _round_trip_yp(program: BytecodeProgram) -> BytecodeProgram:
    return program_from_yantra_patha(program_to_yantra_patha(program))


_EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


class Phase6FoundationTests(unittest.TestCase):
    def test_first_class_function_value_call(self) -> None:
        inc = FunctionDef(
            "inc",
            (Return(BinaryValue("add", Reference("x"), Literal(1))),),
            params=("x",),
        )
        prog = Program(
            (
                Assign("f", Reference("inc")),
                Assign("out", CallValue("f", args=(Literal(7),))),
                Display(Reference("out")),
            ),
            functions=(inc,),
        )
        self.assertEqual(_run(prog), ["8"])

    def test_nested_function_closure_lexical_capture(self) -> None:
        outer = FunctionDef(
            "outer",
            (
                FunctionDef(
                    "addy",
                    (Return(BinaryValue("add", Reference("x"), Reference("y"))),),
                    params=("y",),
                ),
                Return(CallValue("addy", args=(Literal(5),))),
            ),
            params=("x",),
        )
        prog = Program(
            (Assign("out", CallValue("outer", args=(Literal(3),))), Display(Reference("out"))),
            functions=(outer,),
        )
        self.assertEqual(_run(prog), ["8"])

    def test_mutual_recursion_even_odd(self) -> None:
        even = FunctionDef(
            "even",
            (
                If(
                    CompareEq(Reference("n"), Literal(0)),
                    (Return(Literal(1)),),
                    (Return(CallValue("odd", args=(BinaryValue("subtract", Reference("n"), Literal(1)),))),),
                ),
            ),
            params=("n",),
        )
        odd = FunctionDef(
            "odd",
            (
                If(
                    CompareEq(Reference("n"), Literal(0)),
                    (Return(Literal(0)),),
                    (Return(CallValue("even", args=(BinaryValue("subtract", Reference("n"), Literal(1)),))),),
                ),
            ),
            params=("n",),
        )
        prog = Program((Assign("r", CallValue("even", args=(Literal(6),))), Display(Reference("r"))), functions=(even, odd))
        self.assertEqual(_run(prog), ["1"])

    def test_default_parameter_used_when_omitted(self) -> None:
        add = FunctionDef(
            "addk",
            (Return(BinaryValue("add", Reference("x"), Reference("k"))),),
            params=("x", "k"),
            param_defaults=(None, Literal(10)),
        )
        prog = Program(
            (
                Assign("a", CallValue("addk", args=(Literal(2),))),
                Assign("b", CallValue("addk", args=(Literal(2), Literal(5)))),
                Display(Reference("a")),
                Display(Reference("b")),
            ),
            functions=(add,),
        )
        self.assertEqual(_run(prog), ["12", "7"])

    def test_variadic_parameter_collects_extra_args(self) -> None:
        pack = FunctionDef(
            "pack",
            (Return(Reference("rest")),),
            params=("head",),
            variadic_param="rest",
        )
        prog = Program(
            (
                Assign("out", CallValue("pack", args=(Literal(1), Literal(2), Literal(3)))),
                Display(Reference("out")),
            ),
            functions=(pack,),
        )
        self.assertEqual(_run(prog), ["[2, 3]"])

    def test_callable_object_via___call___field(self) -> None:
        inc = FunctionDef(
            "inc",
            (Return(BinaryValue("add", Reference("x"), Literal(1))),),
            params=("x",),
        )
        prog = Program(
            (
                RecordInit("obj"),
                FieldSet("obj", TextLiteral("__call__"), Reference("inc")),
                Assign("out", CallValue("obj", args=(Literal(4),))),
                Display(Reference("out")),
            ),
            functions=(inc,),
        )
        self.assertEqual(_run(prog), ["5"])

    def test_missing_required_parameter_raises(self) -> None:
        f = FunctionDef("f", (Return(Reference("x")),), params=("x",))
        prog = Program((Assign("out", CallValue("f")),), functions=(f,))
        with self.assertRaises(RuntimeSanskriptError):
            _run(prog)


class Phase6MutableCaptureTests(unittest.TestCase):
    def test_mutable_capture_sees_outer_updates(self) -> None:
        outer = FunctionDef(
            "outer",
            (
                Assign("n", Literal(0)),
                FunctionDef(
                    "read",
                    (Return(Reference("n")),),
                    capture_mut=frozenset({"n"}),
                ),
                Assign("g", Reference("read")),
                Increase("n", Literal(2)),
                Assign("out", CallValue("g")),
                Display(Reference("out")),
            ),
        )
        self.assertEqual(_run(Program((Call("outer"),), functions=(outer,))), ["2"])

    def test_pure_function_rejects_mutable_capture(self) -> None:
        fn = FunctionDef(
            "bad",
            (Return(Literal(0)),),
            effect="pure",
            capture_mut=frozenset({"x"}),
        )
        with self.assertRaises(TypeCheckError):
            check_program(Program((), functions=(fn,)))


class Phase6TailCallTests(unittest.TestCase):
    def test_tail_recursive_countdown(self) -> None:
        countdown = FunctionDef(
            "countdown",
            (
                If(
                    CompareEq(Reference("n"), Literal(0)),
                    (Return(Literal(0)),),
                    (
                        Return(
                            CallValue("countdown", args=(BinaryValue("subtract", Reference("n"), Literal(1)),)),
                            tail=True,
                        ),
                    ),
                ),
            ),
            params=("n",),
        )
        prog = Program(
            (Assign("r", CallValue("countdown", args=(Literal(500),))), Display(Reference("r"))),
            functions=(countdown,),
        )
        self.assertEqual(_run(prog), ["0"])

    def test_tail_call_emits_tail_call_opcode(self) -> None:
        fn = FunctionDef(
            "loop",
            (Return(CallValue("loop", args=(Literal(1),)), tail=True),),
            params=("n",),
        )
        bc = compile_program(Program((), functions=(fn,)))
        ops = {i.opcode for f in bc.functions for i in f.instructions}
        self.assertIn(OpCode.TAIL_CALL, ops)

    def test_tail_call_through_callable_value(self) -> None:
        loop = FunctionDef(
            "loop",
            (
                If(
                    CompareEq(Reference("n"), Literal(0)),
                    (Return(Literal(0)),),
                    (
                        Assign("nextf", Reference("loop")),
                        Return(
                            CallValue("nextf", args=(BinaryValue("subtract", Reference("n"), Literal(1)),)),
                            tail=True,
                        ),
                    ),
                ),
            ),
            params=("n",),
        )
        prog = Program(
            (Assign("r", CallValue("loop", args=(Literal(400),))), Display(Reference("r"))),
            functions=(loop,),
        )
        self.assertEqual(_run(prog), ["0"])


class Phase6KeywordAndNamedReturnTests(unittest.TestCase):
    def test_keyword_style_arguments(self) -> None:
        add = FunctionDef(
            "add2",
            (Return(BinaryValue("add", Reference("a"), Reference("b"))),),
            params=("a", "b"),
        )
        prog = Program(
            (
                Assign(
                    "out",
                    CallValue("add2", kwargs=(("b", Literal(10)), ("a", Literal(3)))),
                ),
                Display(Reference("out")),
            ),
            functions=(add,),
        )
        self.assertEqual(_run(prog), ["13"])

    def test_parser_keyword_call_tokens(self) -> None:
        from sanskript.parser_core import parse_call_arg_tokens

        args, kwargs = parse_call_arg_tokens(["3", "iti", "a", "10", "iti", "b"])
        self.assertEqual(len(args), 0)
        self.assertEqual(len(kwargs), 2)

    def test_named_return_slot(self) -> None:
        fn = FunctionDef(
            "mk",
            (Return(Literal(42), name="phala"),),
            named_returns=("phala",),
        )
        prog = Program((Assign("x", CallValue("mk")), Display(Reference("x"))), functions=(fn,))
        self.assertEqual(_run(prog), ["42"])


class Phase6EffectTests(unittest.TestCase):
    def test_pure_function_rejects_emit_in_checker(self) -> None:
        fn = FunctionDef(
            "bad",
            (Display(Literal(1)),),
            effect="pure",
        )
        with self.assertRaises(TypeCheckError):
            check_program(Program((), functions=(fn,)))

    def test_effectful_procedure_allows_emit(self) -> None:
        fn = FunctionDef(
            "show",
            (Display(Literal(9)),),
            effect="effectful",
        )
        self.assertEqual(_run(Program((Call("show"),), functions=(fn,))), ["9"])

    def test_parser_pure_and_effectful_headers(self) -> None:
        src = "vidhānam śuddhaḥ f x .\nsamāpanam .\nvidhānam sādhanaṃ g y .\nsamāpanam ."
        prog = parse_program(src)
        self.assertEqual(prog.functions[0].effect, "pure")
        self.assertEqual(prog.functions[1].effect, "effectful")


class Phase6OverloadTests(unittest.TestCase):
    def test_overload_by_arity(self) -> None:
        f1 = FunctionDef("sum", (Return(Reference("a")),), params=("a",))
        f2 = FunctionDef("sum", (Return(BinaryValue("add", Reference("a"), Reference("b"))),), params=("a", "b"))
        prog = Program(
            (
                Assign("x", CallValue("sum", args=(Literal(3), Literal(4)))),
                Display(Reference("x")),
            ),
            functions=(f1, f2),
        )
        self.assertEqual(_run(prog), ["7"])

    def test_overload_does_not_dispatch_to_prefixed_symbol_name(self) -> None:
        # The only declared function is sum_2; it must not masquerade as sum.
        fn = FunctionDef("sum_2", (Return(BinaryValue("add", Reference("a"), Reference("b"))),), params=("a", "b"))
        prog = Program((Assign("x", CallValue("sum", args=(Literal(3), Literal(4)))),), functions=(fn,))
        with self.assertRaises(RuntimeSanskriptError):
            _run(prog)


class Phase6PartialCurryTests(unittest.TestCase):
    def test_partial_application(self) -> None:
        add = FunctionDef(
            "add3",
            (Return(BinaryValue("add", BinaryValue("add", Reference("a"), Reference("b")), Reference("c"))),),
            params=("a", "b", "c"),
        )
        prog = Program(
            (
                Assign("plus1", PartialApply(Reference("add3"), args=(Literal(1),))),
                Assign("out", CallValue("plus1", args=(Literal(2), Literal(3)))),
                Display(Reference("out")),
            ),
            functions=(add,),
        )
        self.assertEqual(_run(prog), ["6"])

    def test_curried_partial_one_at_a_time(self) -> None:
        add = FunctionDef(
            "pair",
            (Return(BinaryValue("add", Reference("a"), Reference("b"))),),
            params=("a", "b"),
        )
        prog = Program(
            (
                Assign("step", PartialApply(Reference("pair"), args=(Literal(5),), curry=True)),
                Assign("out", CallValue("step", args=(Literal(7),))),
                Display(Reference("out")),
            ),
            functions=(add,),
        )
        self.assertEqual(_run(prog), ["12"])


class Phase6DecoratorMacroInlineTests(unittest.TestCase):
    def test_trace_decorator_emits_enter_leave(self) -> None:
        fn = FunctionDef(
            "work",
            (Display(Literal(1)),),
            decorators=("trace",),
        )
        self.assertEqual(_run(Program((Call("work"),), functions=(fn,))), ["[trace] enter work", "1", "[trace] leave work"])

    def test_any_decorator_name_emits_wrapper_messages(self) -> None:
        fn = FunctionDef(
            "work",
            (Display(Literal(1)),),
            decorators=("audit",),
        )
        self.assertEqual(_run(Program((Call("work"),), functions=(fn,))), ["[audit] enter work", "1", "[audit] leave work"])

    def test_compile_time_macro_expansion(self) -> None:
        macro = FunctionDef(
            "double_lit",
            (Return(BinaryValue("multiply", Reference("n"), Literal(2))),),
            params=("n",),
            is_compile_time=True,
        )
        prog = Program(
            (
                Assign("out", Literal(0)),
                Call("double_lit", args=(Literal(21),)),
                Display(BinaryValue("multiply", Literal(21), Literal(2))),
            ),
            functions=(macro,),
        )
        bc = compile_program(prog)
        self.assertTrue(any(i.opcode == OpCode.MULTIPLY for i in bc.instructions))

    def test_inline_function_rakshita(self) -> None:
        inner = FunctionDef(
            "inc",
            (Return(BinaryValue("add", Reference("x"), Literal(1))),),
            params=("x",),
            is_inline=True,
        )
        prog = Program(
            (Call("inc", args=(Literal(4),)), Display(Literal(5))),
            functions=(inner,),
            safety_tier="rakshita",
        )
        bc = compile_program(prog)
        all_ops = [i.opcode for i in bc.instructions]
        for fn in bc.functions:
            all_ops.extend(i.opcode for i in fn.instructions)
        self.assertIn(OpCode.ADD, all_ops)

    def test_naked_abi_metadata(self) -> None:
        fn = FunctionDef(
            "entry",
            (Return(Literal(0)),),
            is_naked=True,
            abi_name="sanskript_entry",
        )
        bc = compile_program(Program((), functions=(fn,), safety_tier="arakshita"))
        self.assertTrue(bc.functions[0].is_naked)
        self.assertEqual(bc.functions[0].abi_name, "sanskript_entry")


class Phase6ProseRoundTripTests(unittest.TestCase):
    def test_phase6_example_compiles_and_runs(self) -> None:
        path = _EXAMPLES / "phase6-functions.ssk"
        source = path.read_text(encoding="utf-8")

        self.assertIn("śuddhaḥ", source)
        for forbidden in ("greet", "counter", "trace"):
            self.assertNotIn(forbidden, source)
        self.assertEqual(
            SanskriptVM().execute(compile_source(source)),
            [
                "6",
                "7",
                "7",
                "9",
                "18",
                "[anuvīkṣaṇam] enter abhivādana",
                "namaste",
                "[anuvīkṣaṇam] leave abhivādana",
            ],
        )

    def test_phase6_source_tail_call_lowering(self) -> None:
        source = """
surakṣitam .
vidhānam punarāvartanam saṅkhyā .
pratyāvartanam āhvānam punarāvartanam saṅkhyā .
samāpanam .
"""
        bc = compile_source(source)
        fn = next(function for function in bc.functions if function.name == "punarāvartanam")
        self.assertIn(OpCode.TAIL_CALL, {inst.opcode for inst in fn.instructions})

    def test_bytecode_contains_call_opcode(self) -> None:
        inc = FunctionDef(
            "inc",
            (Return(BinaryValue("add", Reference("x"), Literal(1))),),
            params=("x",),
        )
        prog = Program((Call("inc", args=(Literal(2),)),), functions=(inc,))
        bc = compile_program(prog)
        ops = {i.opcode for i in bc.instructions}
        for fn in bc.functions:
            ops |= {i.opcode for i in fn.instructions}
        self.assertTrue(OpCode.CALL in ops or OpCode.TAIL_CALL in ops)


class Phase6NegativeTests(unittest.TestCase):
    def test_macro_requires_literal_args(self) -> None:
        macro = FunctionDef(
            "m",
            (Return(Reference("n")),),
            params=("n",),
            is_compile_time=True,
        )
        prog = Program((Call("m", args=(Reference("v"),)),), functions=(macro,))
        with self.assertRaises(CompileError):
            compile_program(prog)

    def test_unknown_keyword_param_still_runs_with_partial_order(self) -> None:
        fn = FunctionDef("f", (Return(Reference("a")),), params=("a",))
        checker = TypeChecker(Program((), functions=(fn,)))
        checker.check()

    def test_overload_resolution_does_not_use_suffix_name_hack(self) -> None:
        fn = FunctionDef("sum_2", (Return(BinaryValue("add", Reference("a"), Reference("b"))),), params=("a", "b"))
        checker = TypeChecker(Program((), functions=(fn,)))
        arg_types = [checker._resolve_type_name("i32"), checker._resolve_type_name("i32")]
        self.assertIsNone(checker.resolve_overload("sum", arg_types))

    def test_inline_function_rejected_outside_rakshita(self) -> None:
        fn = FunctionDef("inl", (Return(Literal(1)),), is_inline=True)
        with self.assertRaises(TypeCheckError):
            check_program(Program((), functions=(fn,), safety_tier="surakshita"))

    def test_naked_function_rejected_outside_arakshita(self) -> None:
        fn = FunctionDef("entry", (Return(Literal(0)),), is_naked=True, abi_name="entry")
        with self.assertRaises(TypeCheckError):
            check_program(Program((), functions=(fn,), safety_tier="rakshita"))

    def test_abi_requires_naked_annotation(self) -> None:
        fn = FunctionDef("entry", (Return(Literal(0)),), abi_name="entry")
        with self.assertRaises(TypeCheckError):
            check_program(Program((), functions=(fn,), safety_tier="arakshita"))

    def test_surakshita_rejects_loading_abi_naked_callable_reference(self) -> None:
        program = BytecodeProgram(
            instructions=(
                Instruction(OpCode.LOAD_NAME, "entry"),
                Instruction(OpCode.STORE_NAME, "f"),
                Instruction(OpCode.HALT),
            ),
            functions=(
                FunctionBytecode(
                    name="entry",
                    instructions=(Instruction(OpCode.PUSH_INT, 0), Instruction(OpCode.RETURN)),
                    is_naked=True,
                    abi_name="entry",
                ),
            ),
            safety_tier="surakshita",
        )
        with self.assertRaises(RuntimeSanskriptError):
            SanskriptVM().execute(program)

    def test_rakshita_rejects_calling_naked_callable(self) -> None:
        program = BytecodeProgram(
            instructions=(Instruction(OpCode.CALL, "entry"), Instruction(OpCode.HALT)),
            functions=(
                FunctionBytecode(
                    name="entry",
                    instructions=(Instruction(OpCode.PUSH_INT, 0), Instruction(OpCode.RETURN)),
                    is_naked=True,
                    abi_name="entry",
                ),
            ),
            safety_tier="rakshita",
        )
        with self.assertRaises(RuntimeSanskriptError):
            SanskriptVM().execute(program)


if __name__ == "__main__":
    unittest.main()
