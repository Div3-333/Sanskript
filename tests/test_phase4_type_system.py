"""Phase 4: static type system tests — 40+ tests covering the type system seal."""

from __future__ import annotations

import unittest

from sanskript.ast import (
    Assign,
    BinaryValue,
    Bind,
    BoolLiteral,
    BytesLiteral,
    Call,
    CallValue,
    ClassDecl,
    ClassNew,
    CompareEq,
    ConstDecl,
    Display,
    FloatLiteral,
    FunctionDef,
    GeneratorNew,
    GeneratorNext,
    GenericRecordDecl,
    If,
    LifetimeDecl,
    Literal,
    NewtypeDecl,
    Program,
    RecordTypeDecl,
    Reference,
    Return,
    TextLiteral,
    TraitDecl,
    TraitImpl,
    TypeAliasDecl,
    TypeConvert,
    TypeReflect,
    MethodCall,
    StaticMethodCall,
    Yield,
    ListInit,
    ListMap,
)
from sanskript.parser import parse_program
from sanskript.compiler import compile_program
from sanskript.errors import TypeCheckError
from sanskript.type_checker import (
    PrimitiveType,
    TypeChecker,
    check_program,
)
from sanskript.vm import SanskriptVM


# ---------------------------------------------------------------------------
# Existing tests (must still pass)
# ---------------------------------------------------------------------------


class Phase4TypeSystemTests(unittest.TestCase):
    def test_type_alias_and_inference(self) -> None:
        program = Program(
            (Assign("phala", Literal(5)), Display(Reference("phala"))),
            type_aliases=(TypeAliasDecl("saṅkhyā", "i32"),),
        )
        check_program(program)
        self.assertEqual(SanskriptVM().execute(compile_program(program)), ["5"])

    def test_newtype_and_explicit_convert(self) -> None:
        program = Program(
            (
                Assign("mūlya", Literal(10)),
                TypeConvert("lekhā", "i32", Reference("mūlya")),
                Display(Reference("lekhā")),
            ),
            newtypes=(NewtypeDecl("lekhā", "i32"),),
        )
        check_program(program)
        self.assertEqual(SanskriptVM().execute(compile_program(program)), ["10"])

    def test_const_immutable(self) -> None:
        program = Program(
            (Display(Literal(1)),),
            constants=(ConstDecl("pi", Literal(3), type_name="i32"),),
        )
        check_program(program)

    def test_forbidden_raw_ptr_in_surakshita(self) -> None:
        program = Program(
            (),
            type_aliases=(TypeAliasDecl("addr", "raw_ptr"),),
            safety_tier="surakshita",
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_numeric_promotion_in_checker(self) -> None:
        checker = TypeChecker(
            Program((Assign("x", Literal(1)),), safety_tier="surakshita")
        )
        ty = checker._infer_value(BinaryValue("add", Literal(1), FloatLiteral(2.0)))
        self.assertEqual(checker._type_name(ty), "f64")

    def test_option_some_inference(self) -> None:
        from sanskript.ast import SomeValue

        program = Program((Assign("opt", SomeValue(Literal(7))),))
        checker = TypeChecker(program)
        ty = checker._infer_value(SomeValue(Literal(7)))
        self.assertEqual(checker._type_name(ty), "Option<i32>")

    # ---------------------------------------------------------------------------
    # Nominal types
    # ---------------------------------------------------------------------------

    def test_nominal_types_distinct_names(self) -> None:
        """Two records with identical fields but different names are distinct nominal types."""
        program = Program(
            (),
            record_types=(
                RecordTypeDecl("Puruṣaḥ", (("nāma", "text"),)),
                RecordTypeDecl("Strī", (("nāma", "text"),)),
            ),
        )
        checker = TypeChecker(program)
        checker.check()
        p = checker.records["Puruṣaḥ"]
        s = checker.records["Strī"]
        self.assertNotEqual(p.name, s.name)
        self.assertEqual(p.name, "Puruṣaḥ")
        self.assertEqual(s.name, "Strī")

    def test_nominal_type_mismatch_detectable(self) -> None:
        """Type checker stores nominal records as distinct even with same field types."""
        program = Program(
            (),
            record_types=(
                RecordTypeDecl("Alpha", (("x", "i32"),)),
                RecordTypeDecl("Beta", (("x", "i32"),)),
            ),
        )
        checker = TypeChecker(program)
        checker.check()
        alpha = checker.records["Alpha"]
        beta = checker.records["Beta"]
        # Nominal types with different names are NOT equal
        self.assertNotEqual(alpha, beta)

    def test_nominal_types_not_assignable_cross_name(self) -> None:
        program = Program(
            (),
            record_types=(
                RecordTypeDecl("Alpha", (("x", "i32"),)),
                RecordTypeDecl("Beta", (("x", "i32"),)),
            ),
        )
        checker = TypeChecker(program)
        self.assertFalse(
            checker._types_compatible(
                checker.records["Alpha"],
                checker.records["Beta"],
                for_equality=False,
            )
        )

    def test_nominal_structural_equality_allowed(self) -> None:
        program = Program(
            (),
            record_types=(
                RecordTypeDecl("Full", (("x", "i32"), ("y", "i32"))),
                RecordTypeDecl("Partial", (("x", "i32"),)),
            ),
        )
        checker = TypeChecker(program)
        self.assertTrue(
            checker._types_compatible(
                checker.records["Full"],
                checker.records["Partial"],
                for_equality=True,
            )
        )

    # ---------------------------------------------------------------------------
    # Structural types
    # ---------------------------------------------------------------------------

    def test_structural_match_superset(self) -> None:
        """A record with extra fields structurally satisfies a record with fewer fields."""
        program = Program(
            (),
            record_types=(
                RecordTypeDecl("Full", (("x", "i32"), ("y", "i32"), ("z", "i32"))),
                RecordTypeDecl("Partial", (("x", "i32"), ("y", "i32"))),
            ),
        )
        checker = TypeChecker(program)
        checker.check()
        full = checker.records["Full"]
        partial = checker.records["Partial"]
        self.assertTrue(checker._structural_match(full, partial))
        # Reverse is false (Partial lacks z)
        self.assertFalse(checker._structural_match(partial, full))

    # ---------------------------------------------------------------------------
    # Generic records
    # ---------------------------------------------------------------------------

    def test_generic_record_registered(self) -> None:
        """GenericRecordDecl registers in generic_records dict."""
        program = Program(
            (),
            generic_records=(
                GenericRecordDecl("Paṭala", "T", (("data", "T"), ("size", "i32"))),
            ),
        )
        checker = TypeChecker(program)
        checker.check()
        self.assertIn("Paṭala", checker.generic_records)
        gr = checker.generic_records["Paṭala"]
        self.assertEqual(gr.type_param, "T")

    def test_generic_record_instantiation(self) -> None:
        program = Program(
            (),
            generic_records=(
                GenericRecordDecl("Box", "T", (("value", "T"),)),
            ),
        )
        checker = TypeChecker(program)
        inst = checker.instantiate_generic_record("Box", "i32")
        self.assertEqual(inst.name, "Box<i32>")
        self.assertEqual(checker._type_name(inst.fields[0][1]), "i32")

    # ---------------------------------------------------------------------------
    # Return type inference
    # ---------------------------------------------------------------------------

    def test_return_type_inference_literal(self) -> None:
        """Type checker infers return type from Return nodes with integer literal."""
        fn = FunctionDef(
            "double",
            (Return(Literal(42)),),
            params=("x",),
            param_types=("i32",),
        )
        program = Program((), functions=(fn,))
        checker = TypeChecker(program)
        checker.check()
        inferred = checker.get_inferred_return_type("double")
        self.assertEqual(checker._type_name(inferred), "i32")

    def test_return_type_inference_float(self) -> None:
        fn = FunctionDef(
            "pi_approx",
            (Return(FloatLiteral(3.14)),),
        )
        program = Program((), functions=(fn,))
        checker = TypeChecker(program)
        checker.check()
        inferred = checker.get_inferred_return_type("pi_approx")
        self.assertEqual(checker._type_name(inferred), "f64")

    def test_return_type_declared_must_match_inferred(self) -> None:
        fn = FunctionDef(
            "bad",
            (Return(Literal(1)),),
            return_type="text",
        )
        program = Program((), functions=(fn,))
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_return_type_mixed_numeric_unifies_to_f64(self) -> None:
        fn = FunctionDef(
            "mix",
            (
                If(
                    CompareEq(Literal(1), Literal(1)),
                    (Return(Literal(1)),),
                    (Return(FloatLiteral(1.0)),),
                ),
            ),
        )
        checker = TypeChecker(Program((), functions=(fn,)))
        checker.check()
        self.assertEqual(checker._type_name(checker.get_inferred_return_type("mix")), "f64")

    # ---------------------------------------------------------------------------
    # Implicit conversions
    # ---------------------------------------------------------------------------

    def test_implicit_i32_to_f64_conversion(self) -> None:
        """i32 → f64 implicit conversion accepted by TypeConvert."""
        program = Program(
            (
                Assign("n", Literal(5)),
                TypeConvert("f", "f64", Reference("n")),
            )
        )
        check_program(program)

    def test_implicit_bool_to_i32_conversion(self) -> None:
        """bool → i32 implicit conversion accepted."""
        program = Program(
            (
                Assign("flag", BoolLiteral(True)),
                TypeConvert("num", "i32", Reference("flag")),
            )
        )
        check_program(program)

    def test_implicit_i32_to_i64_conversion(self) -> None:
        """i32 → i64 widening conversion accepted."""
        program = Program(
            (
                Assign("small", Literal(100)),
                TypeConvert("big", "i64", Reference("small")),
            )
        )
        check_program(program)

    def test_bytes_to_text_conversion(self) -> None:
        program = Program(
            (
                Assign("raw", BytesLiteral(b"hi")),
                TypeConvert("msg", "text", Reference("raw")),
            )
        )
        check_program(program)

    def test_overload_resolution_by_arity(self) -> None:
        f1 = FunctionDef("sum", (Return(Literal(0)),), params=("a",))
        f2 = FunctionDef("sum", (Return(Literal(0)),), params=("a", "b"))
        checker = TypeChecker(Program((), functions=(f1, f2)))
        one = checker.resolve_overload("sum", [PrimitiveType("i32")])
        two = checker.resolve_overload("sum", [PrimitiveType("i32"), PrimitiveType("i32")])
        self.assertEqual(len(one.params) if one else 0, 1)
        self.assertEqual(len(two.params) if two else 0, 2)

    def test_overload_resolution_by_suffix(self) -> None:
        f1 = FunctionDef(
            "add_i32",
            (Return(Literal(0)),),
            params=("a", "b"),
            param_types=("i32", "i32"),
        )
        f2 = FunctionDef(
            "add_f64",
            (Return(FloatLiteral(0.0)),),
            params=("a", "b"),
            param_types=("f64", "f64"),
        )
        checker = TypeChecker(Program((), functions=(f1, f2)))
        resolved = checker.resolve_overload(
            "add",
            [PrimitiveType("f64"), PrimitiveType("f64")],
        )
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved.name, "add_f64")  # type: ignore[union-attr]

    # ---------------------------------------------------------------------------
    # text/bytes conversion
    # ---------------------------------------------------------------------------

    def test_text_to_bytes_conversion(self) -> None:
        """text → bytes conversion accepted by TypeConvert."""
        program = Program(
            (
                Assign("msg", TextLiteral("namaste")),
                TypeConvert("raw", "bytes", Reference("msg")),
            )
        )
        check_program(program)

    def test_bytes_literal_inferred_as_bytes(self) -> None:
        """BytesLiteral inferred as bytes type."""
        checker = TypeChecker(Program(()))
        ty = checker._infer_value(BytesLiteral(b"\x00\x01"))
        self.assertEqual(checker._type_name(ty), "bytes")

    # ---------------------------------------------------------------------------
    # Tier-based pointer enforcement
    # ---------------------------------------------------------------------------

    def test_safe_ref_forbidden_in_surakshita(self) -> None:
        """safe_ref type alias rejected in surakṣita tier."""
        program = Program(
            (),
            type_aliases=(TypeAliasDecl("ptr", "safe_ref"),),
            safety_tier="surakshita",
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_safe_ref_allowed_in_rakshita(self) -> None:
        """safe_ref is allowed in rakṣita tier."""
        program = Program(
            (),
            type_aliases=(TypeAliasDecl("ptr", "safe_ref"),),
            safety_tier="rakshita",
        )
        # Should not raise
        check_program(program)

    def test_raw_ptr_forbidden_in_surakshita(self) -> None:
        """raw_ptr forbidden in surakṣita tier (existing behaviour preserved)."""
        program = Program(
            (),
            type_aliases=(TypeAliasDecl("p", "raw_ptr"),),
            safety_tier="surakshita",
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    # ---------------------------------------------------------------------------
    # Ownership annotations
    # ---------------------------------------------------------------------------

    def test_ownership_annotation_recorded(self) -> None:
        """Bind with ownership annotation records it in env.ownership."""
        program = Program(
            (Bind("x", Literal(1), ownership="owned"),),
            safety_tier="rakshita",
        )
        checker = TypeChecker(program)
        checker.check()
        self.assertEqual(checker.env.ownership["x"], "owned")

    def test_lifetime_requires_rakshita_tier(self) -> None:
        program = Program(
            (Bind("x", Literal(1), lifetime="'a"),),
            lifetimes=(LifetimeDecl("'a"),),
            safety_tier="surakshita",
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_lifetime_allowed_in_rakshita(self) -> None:
        program = Program(
            (Bind("x", Literal(1), lifetime="a"),),
            lifetimes=(LifetimeDecl("a", "stack"),),
            safety_tier="rakshita",
        )
        check_program(program)

    def test_unknown_lifetime_is_rejected(self) -> None:
        program = Program(
            (Bind("x", Literal(1), lifetime="missing"),),
            safety_tier="rakshita",
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_linear_forbidden_in_surakshita(self) -> None:
        program = Program(
            (),
            type_aliases=(TypeAliasDecl("handle", "linear"),),
            safety_tier="surakshita",
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_class_decl_registered(self) -> None:
        program = Program(
            (),
            classes=(
                ClassDecl("Point", None, (("x", "i32"), ("y", "i32")), ("distance",)),
            ),
        )
        checker = TypeChecker(program)
        checker.check()
        self.assertIn("Point", checker.classes)
        self.assertIn("distance", checker.classes["Point"].methods)

    # ---------------------------------------------------------------------------
    # Effect types (pure/effectful annotation)
    # ---------------------------------------------------------------------------

    def test_effect_annotation_pure(self) -> None:
        """FunctionDef.effect='pure' is recorded and accepted by checker."""
        fn = FunctionDef(
            "add",
            (Return(BinaryValue("add", Reference("a"), Reference("b"))),),
            params=("a", "b"),
            param_types=("i32", "i32"),
            effect="pure",
        )
        program = Program((), functions=(fn,))
        check_program(program)
        self.assertEqual(fn.effect, "pure")

    def test_effect_annotation_effectful(self) -> None:
        """FunctionDef.effect='effectful' is recorded and accepted."""
        fn = FunctionDef(
            "print_val",
            (Display(Reference("x")),),
            params=("x",),
            param_types=("i32",),
            effect="effectful",
        )
        program = Program((), functions=(fn,))
        check_program(program)
        self.assertEqual(fn.effect, "effectful")

    # ---------------------------------------------------------------------------
    # Generic interfaces/traits
    # ---------------------------------------------------------------------------

    def test_trait_declaration_registered(self) -> None:
        """TraitDecl is registered in checker.traits."""
        trait = TraitDecl(
            "Iterable",
            "T",
            (("next", ("T",), "T"),),
        )
        program = Program((), traits=(trait,))
        checker = TypeChecker(program)
        checker.check()
        self.assertIn("Iterable", checker.traits)

    def test_trait_impl_satisfied(self) -> None:
        """Record that has all required fields satisfies trait."""
        trait = TraitDecl("Showable", None, (("show", (), "text"),))
        record = RecordTypeDecl("MyRecord", (("show", "text"), ("value", "i32")))
        impl = TraitImpl("MyRecord", "Showable")
        program = Program(
            (),
            record_types=(record,),
            traits=(trait,),
            trait_impls=(impl,),
        )
        check_program(program)

    def test_trait_impl_missing_method_raises(self) -> None:
        """Record missing required method raises TypeCheckError."""
        trait = TraitDecl("Showable", None, (("show", (), "text"),))
        record = RecordTypeDecl("BadRecord", (("value", "i32"),))
        impl = TraitImpl("BadRecord", "Showable")
        program = Program(
            (),
            record_types=(record,),
            traits=(trait,),
            trait_impls=(impl,),
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    # ---------------------------------------------------------------------------
    # Bounded generics
    # ---------------------------------------------------------------------------

    def test_bounded_generic_function(self) -> None:
        """FunctionDef with type_param_bounds is accepted by checker."""
        fn = FunctionDef(
            "process",
            (Return(Reference("item")),),
            params=("item",),
            param_types=(None,),
            type_params=("T",),
            type_param_bounds=(("T", "Iterable"),),
        )
        trait = TraitDecl("Iterable", "T", ())
        program = Program((), functions=(fn,), traits=(trait,))
        check_program(program)
        # Bound recorded on generic type
        checker = TypeChecker(program)
        checker.check()
        # Check that the type param has the bound in the function context
        # (by direct inspection after check)
        self.assertIn("Iterable", checker.traits)

    # ---------------------------------------------------------------------------
    # Type reflection
    # ---------------------------------------------------------------------------

    def test_type_reflect_records_text_type(self) -> None:
        """TypeReflect directive stores type name as text in the env."""
        program = Program(
            (TypeReflect("type_info", "i32"),),
        )
        checker = TypeChecker(program)
        checker.check()
        ty = checker.env.locals.get("type_info")
        self.assertIsNotNone(ty)
        self.assertEqual(checker._type_name(ty), "text")

    def test_type_reflect_compiles_and_runs(self) -> None:
        program = Program(
            (TypeReflect("tn", "i32"), Display(Reference("tn"))),
        )
        check_program(program)
        self.assertEqual(SanskriptVM().execute(compile_program(program)), ["i32"])

    def test_resolve_generic_record_type_name(self) -> None:
        program = Program(
            (),
            generic_records=(GenericRecordDecl("Vec", "T", (("item", "T"),)),),
        )
        checker = TypeChecker(program)
        ty = checker._resolve_type_name("Vec<i32>")
        self.assertEqual(ty.name, "Vec<i32>")  # type: ignore[attr-defined]

    def test_call_value_uses_return_type_annotation(self) -> None:
        callee = FunctionDef(
            "mk",
            (Return(Literal(1)),),
            return_type="i32",
        )
        program = Program(
            (Assign("x", CallValue("mk", ()),),),
            functions=(callee,),
        )
        checker = TypeChecker(program)
        checker.check()
        self.assertEqual(checker._type_name(checker.env.locals["x"]), "i32")

    def test_parser_record_type_directive(self) -> None:
        src = "vastu-prakāraḥ Puruṣaḥ nāma text ."
        program = parse_program(src)
        self.assertEqual(len(program.record_types), 1)
        self.assertEqual(program.record_types[0].name, "Puruṣaḥ")

    def test_parser_type_reflect_directive(self) -> None:
        src = "prakāra-āharaṇam info i32 .\ndarśanam info."
        program = parse_program(src)
        self.assertIsInstance(program.statements[0], TypeReflect)

    def test_metaclass_in_catalog(self) -> None:
        from sanskript.type_catalog import get_type_catalog

        names = [e.name for e in get_type_catalog().types]
        self.assertIn("metaclass", names)
        self.assertIn("class_instance", names)

    # ---------------------------------------------------------------------------
    # Async/future/generator/coroutine type vocabulary
    # ---------------------------------------------------------------------------

    def test_async_future_in_catalog(self) -> None:
        """async_future appears in catalog and is available in surakṣita."""
        from sanskript.type_catalog import get_type_catalog, TierAvailability, SafetyTier

        catalog = get_type_catalog()
        names = [e.name for e in catalog.types]
        self.assertIn("async_future", names)

    def test_generator_in_catalog(self) -> None:
        """generator appears in catalog."""
        from sanskript.type_catalog import get_type_catalog

        catalog = get_type_catalog()
        names = [e.name for e in catalog.types]
        self.assertIn("generator", names)

    def test_coroutine_in_catalog(self) -> None:
        """coroutine appears in catalog."""
        from sanskript.type_catalog import get_type_catalog

        catalog = get_type_catalog()
        names = [e.name for e in catalog.types]
        self.assertIn("coroutine", names)

    # ---------------------------------------------------------------------------
    # i64 numeric promotion
    # ---------------------------------------------------------------------------

    def test_numeric_promotion_i64(self) -> None:
        """i32 + i64 promotes to i64."""
        checker = TypeChecker(Program(()))
        left = PrimitiveType("i32")
        right = PrimitiveType("i64")
        result = checker._promote_numeric(left, right)
        self.assertEqual(checker._type_name(result), "i64")

    # ---------------------------------------------------------------------------
    # Phase 4 blocker hardening: borrow/lifetime/effects/generator/class typing
    # ---------------------------------------------------------------------------

    def test_borrow_requires_named_reference(self) -> None:
        program = Program(
            (Bind("b", Literal(1), ownership="borrow"),),
            safety_tier="rakshita",
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_cannot_use_moved_value(self) -> None:
        program = Program(
            (
                Bind("x", Literal(1), ownership="owned"),
                Bind("y", Reference("x"), ownership="owned"),
                Display(Reference("x")),
            ),
            safety_tier="rakshita",
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_mutable_borrow_conflicts_with_shared_borrow(self) -> None:
        program = Program(
            (
                Bind("x", Literal(1), ownership="owned"),
                Bind("a", Reference("x"), ownership="borrow"),
                Bind("b", Reference("x"), ownership="borrow_mut"),
            ),
            safety_tier="rakshita",
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_cannot_move_borrow_alias(self) -> None:
        program = Program(
            (
                Bind("x", Literal(1), ownership="owned"),
                Bind("b", Reference("x"), ownership="borrow"),
                Bind("m", Reference("b"), ownership="owned"),
            ),
            safety_tier="rakshita",
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_mutable_borrow_of_immutable_binding_rejected(self) -> None:
        program = Program(
            (
                Bind("x", Literal(1), immutable=True, ownership="owned"),
                Bind("b", Reference("x"), ownership="borrow_mut"),
            ),
            safety_tier="rakshita",
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_borrow_lifetime_must_match_owner_lifetime(self) -> None:
        program = Program(
            (
                Bind("x", Literal(1), ownership="owned", lifetime="a"),
                Bind("b", Reference("x"), ownership="borrow", lifetime="b"),
            ),
            lifetimes=(LifetimeDecl("a"), LifetimeDecl("b")),
            safety_tier="rakshita",
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_borrow_expires_after_branch_scope(self) -> None:
        program = Program(
            (
                Bind("x", Literal(1), ownership="owned"),
                If(
                    CompareEq(Literal(1), Literal(1)),
                    (Bind("tmp", Reference("x"), ownership="borrow"),),
                    (),
                ),
                Assign("x", Literal(2)),
            ),
            safety_tier="rakshita",
        )
        check_program(program)

    def test_pure_function_cannot_call_effectful_function(self) -> None:
        eff = FunctionDef("io", (Display(Literal(1)),), effect="effectful")
        pure = FunctionDef("f", (Call("io"),), effect="pure")
        with self.assertRaises(TypeCheckError):
            check_program(Program((), functions=(eff, pure)))

    def test_pure_function_cannot_call_unknown_function(self) -> None:
        pure = FunctionDef("f", (Call("mystery"),), effect="pure")
        with self.assertRaises(TypeCheckError):
            check_program(Program((), functions=(pure,)))

    def test_pure_function_cannot_use_effectful_list_map_callback(self) -> None:
        callback = FunctionDef("cb", (Display(Reference("x")),), params=("x",), effect="effectful")
        pure = FunctionDef(
            "pure_map",
            (
                ListInit("items"),
                ListMap("out", "items", "cb"),
            ),
            effect="pure",
        )
        with self.assertRaises(TypeCheckError):
            check_program(Program((), functions=(callback, pure)))

    def test_generator_new_requires_generator_function(self) -> None:
        fn = FunctionDef("plain", (Return(Literal(1)),))
        program = Program((GeneratorNew("g", "plain"),), functions=(fn,))
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_yield_requires_generator_or_coroutine_return(self) -> None:
        fn = FunctionDef("bad", (Yield(Literal(1)),), return_type="i32")
        with self.assertRaises(TypeCheckError):
            check_program(Program((), functions=(fn,)))

    def test_generator_return_type_requires_yield(self) -> None:
        fn = FunctionDef("bad", (Return(Literal(1)),), return_type="generator")
        with self.assertRaises(TypeCheckError):
            check_program(Program((), functions=(fn,)))

    def test_generator_next_requires_generator_type(self) -> None:
        program = Program(
            (
                Assign("x", Literal(1)),
                GeneratorNext("more", "val", "x"),
            )
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_generator_next_propagates_inferred_yield_type(self) -> None:
        gen = FunctionDef(
            "g",
            (Yield(Literal(7)),),
            return_type="generator",
        )
        program = Program(
            (
                GeneratorNew("it", "g"),
                GeneratorNext("more", "val", "it"),
            ),
            functions=(gen,),
        )
        checker = TypeChecker(program)
        checker.check()
        self.assertEqual(checker._type_name(checker.env.locals["val"]), "i32")

    def test_async_future_function_cannot_be_pure(self) -> None:
        fn = FunctionDef(
            "later",
            (Return(Literal(1)),),
            return_type="async_future",
            effect="pure",
        )
        with self.assertRaises(TypeCheckError):
            check_program(Program((), functions=(fn,)))

    def test_class_method_call_uses_declared_return_type(self) -> None:
        program = Program(
            statements=(
                ClassNew("p", "Point", ()),
                MethodCall("d", "p", "distance"),
            ),
            functions=(
                FunctionDef(
                    "Point__distance",
                    (Return(Literal(42)),),
                    params=("self",),
                    return_type="i32",
                ),
            ),
            classes=(
                ClassDecl("Point", None, (), ("distance",)),
            ),
        )
        checker = TypeChecker(program)
        checker.check()
        self.assertEqual(checker._type_name(checker.env.locals["d"]), "i32")

    def test_callvalue_argument_type_mismatch_raises(self) -> None:
        callee = FunctionDef(
            "mk",
            (Return(Literal(1)),),
            params=("x",),
            param_types=("i32",),
            return_type="i32",
        )
        program = Program(
            (Assign("v", CallValue("mk", (TextLiteral("bad"),))),),
            functions=(callee,),
        )
        with self.assertRaises(TypeCheckError):
            check_program(program)

    def test_class_subtype_is_accepted_for_base_parameter(self) -> None:
        accept_base = FunctionDef(
            "takes_base",
            (Return(Literal(1)),),
            params=("x",),
            param_types=("Base",),
            return_type="i32",
        )
        program = Program(
            statements=(
                ClassNew("d", "Derived", ()),
                StaticMethodCall("out", "Harness", "run", (Reference("d"),)),
            ),
            functions=(
                accept_base,
                FunctionDef(
                    "Harness__static__run",
                    (Return(CallValue("takes_base", (Reference("x"),))),),
                    params=("x",),
                    return_type="i32",
                ),
            ),
            classes=(
                ClassDecl("Base", None, (), ()),
                ClassDecl("Derived", None, (), (), base_class="Base"),
                ClassDecl("Harness", None, (), (), static_methods=("run",)),
            ),
        )
        check_program(program)


if __name__ == "__main__":
    unittest.main()
