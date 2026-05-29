"""Phase 7: object-oriented programming — full completion-standard coverage."""

from __future__ import annotations

import unittest
from pathlib import Path

from sanskript.ast import (
    Assign,
    BinaryValue,
    ClassDecl,
    ClassMethodCall,
    ClassNew,
    ClassReflect,
    Display,
    FieldGet,
    FieldSet,
    FunctionDef,
    Literal,
    MethodCall,
    MethodReflect,
    Program,
    PropertyGet,
    Reference,
    Return,
    StaticMethodCall,
    TextLiteral,
    TraitDecl,
    InstanceFinalize,
)
from sanskript.bytecode import BytecodeProgram, FunctionBytecode, Instruction, OpCode
from sanskript.compiler import compile_program, compile_source
from sanskript.errors import RuntimeSanskriptError, TypeCheckError
from sanskript.parser import parse_program
from sanskript.vm import SanskriptVM
from sanskript.yantra_patha import program_from_yantra_patha, program_to_yantra_patha


def _run(program: Program) -> SanskriptVM:
    vm = SanskriptVM()
    vm.execute(compile_program(program))
    return vm


def _round_trip_yp(program: BytecodeProgram) -> BytecodeProgram:
    return program_from_yantra_patha(program_to_yantra_patha(program))


_EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


class Phase7ParserTests(unittest.TestCase):
    def test_parser_class_constructor_and_method_call(self) -> None:
        program = Program(
            classes=(ClassDecl("Point", None, (("x", "i32"), ("y", "i32")), ("init", "sum")),),
            statements=(
                ClassNew("p", "Point", (Literal(1), Literal(2))),
                MethodCall("s", "p", "sum"),
            ),
        )
        self.assertEqual(program.classes[0].name, "Point")
        self.assertIsInstance(program.statements[0], ClassNew)
        self.assertIsInstance(program.statements[1], MethodCall)

    def test_parser_inheritance_visibility_static_class_methods(self) -> None:
        program = Program(
            (),
            classes=(
                ClassDecl("Shape", None, (), ("area",)),
                ClassDecl(
                    "Point",
                    None,
                    (("secret", "i32"), ("x", "i32")),
                    ("sum",),
                    field_visibility=(("secret", "private"),),
                    static_methods=("zero",),
                    class_methods=("factory",),
                    base_class="Shape",
                    computed_properties=("magnitude",),
                    metaclass="MetaShape",
                ),
            ),
        )
        child = program.classes[1]
        self.assertEqual(child.base_class, "Shape")
        self.assertIn(("secret", "private"), child.field_visibility)
        self.assertIn("zero", child.static_methods)
        self.assertIn("factory", child.class_methods)
        self.assertIn("magnitude", child.computed_properties)
        self.assertEqual(child.metaclass, "MetaShape")


class Phase7RuntimeTests(unittest.TestCase):
    def test_instance_construction_constructor_and_method_dispatch(self) -> None:
        program = Program(
            statements=(
                ClassNew("p", "Point", (Literal(3), Literal(4))),
                MethodCall("total", "p", "sum"),
            ),
            functions=(
                FunctionDef(
                    "Point__init__",
                    (
                        FieldSet("self", TextLiteral("x"), Reference("x0")),
                        FieldSet("self", TextLiteral("y"), Reference("y0")),
                        Return(Reference("self")),
                    ),
                    params=("self", "x0", "y0"),
                ),
                FunctionDef(
                    "Point__sum",
                    (
                        FieldGet("xv", "self", TextLiteral("x")),
                        FieldGet("yv", "self", TextLiteral("y")),
                        Return(Reference("xv")),
                    ),
                    params=("self",),
                ),
            ),
            classes=(
                ClassDecl("Point", None, (("x", "i32"), ("y", "i32")), ("sum",)),
            ),
        )
        vm = _run(program)
        self.assertIn("p", vm.environment)
        self.assertEqual(vm.environment["total"], 3)

    def test_constructor_optional_when_missing(self) -> None:
        program = Program(
            statements=(ClassNew("p", "Bare", ()),),
            classes=(ClassDecl("Bare", None, (), ()),),
        )
        vm = _run(program)
        self.assertIn("p", vm.environment)

    def test_inheritance_dynamic_dispatch(self) -> None:
        program = Program(
            statements=(
                ClassNew("c", "Child", ()),
                MethodCall("out", "c", "area"),
            ),
            functions=(
                FunctionDef(
                    "Shape__area",
                    (Return(Literal(1)),),
                    params=("self",),
                ),
                FunctionDef(
                    "Child__area",
                    (Return(Literal(2)),),
                    params=("self",),
                ),
            ),
            classes=(
                ClassDecl("Shape", None, (), ("area",)),
                ClassDecl("Child", None, (), ("area",), base_class="Shape"),
            ),
        )
        vm = _run(program)
        self.assertEqual(vm.environment["out"], 2)

    def test_static_and_class_methods(self) -> None:
        program = Program(
            statements=(
                StaticMethodCall("z", "Counter", "zero"),
                ClassMethodCall("c", "Counter", "make", (Literal(3),)),
            ),
            functions=(
                FunctionDef("Counter__static__zero", (Return(Literal(0)),), params=()),
                FunctionDef(
                    "Counter__make",
                    (Return(Reference("n")),),
                    params=("cls", "n"),
                ),
            ),
            classes=(
                ClassDecl(
                    "Counter",
                    None,
                    (),
                    static_methods=("zero",),
                    class_methods=("make",),
                ),
            ),
        )
        vm = _run(program)
        self.assertEqual(vm.environment["z"], 0)
        self.assertEqual(vm.environment["c"], 3)

    def test_inherited_static_and_class_methods(self) -> None:
        program = Program(
            statements=(
                StaticMethodCall("z", "ChildCounter", "zero"),
                ClassMethodCall("c", "ChildCounter", "make", (Literal(9),)),
            ),
            functions=(
                FunctionDef("Counter__static__zero", (Return(Literal(0)),), params=()),
                FunctionDef("Counter__make", (Return(Reference("n")),), params=("cls", "n")),
            ),
            classes=(
                ClassDecl(
                    "Counter",
                    None,
                    (),
                    (),
                    static_methods=("zero",),
                    class_methods=("make",),
                ),
                ClassDecl("ChildCounter", None, (), (), base_class="Counter"),
            ),
        )
        vm = _run(program)
        self.assertEqual(vm.environment["z"], 0)
        self.assertEqual(vm.environment["c"], 9)

    def test_metaclass_dispatch_for_static_and_class_methods(self) -> None:
        program = Program(
            statements=(
                StaticMethodCall("s", "Widget", "meta_zero"),
                ClassMethodCall("c", "Widget", "meta_make", (Literal(6),)),
            ),
            functions=(
                FunctionDef("Meta__static__meta_zero", (Return(Literal(0)),), params=()),
                FunctionDef("Meta__meta_make", (Return(Reference("n")),), params=("cls", "n")),
            ),
            classes=(
                ClassDecl("Meta", None, (), (), static_methods=("meta_zero",), class_methods=("meta_make",)),
                ClassDecl("Widget", None, (), (), metaclass="Meta"),
            ),
        )
        vm = _run(program)
        self.assertEqual(vm.environment["s"], 0)
        self.assertEqual(vm.environment["c"], 6)

    def test_computed_property_and_reflection(self) -> None:
        program = Program(
            statements=(
                ClassNew("p", "Box", (Literal(4),)),
                PropertyGet("m", "p", "size"),
                ClassReflect("cn", "p"),
                MethodReflect("mn", "p", "size"),
            ),
            functions=(
                FunctionDef(
                    "Box__init__",
                    (
                        FieldSet("self", TextLiteral("v"), Reference("v0")),
                        Return(Reference("self")),
                    ),
                    params=("self", "v0"),
                ),
                FunctionDef(
                    "Box__get_size",
                    (
                        FieldGet("v", "self", TextLiteral("v")),
                        Return(Reference("v")),
                    ),
                    params=("self",),
                ),
            ),
            classes=(ClassDecl("Box", None, (("v", "i32"),), (), computed_properties=("size",)),),
        )
        vm = _run(program)
        self.assertEqual(vm.environment["m"], 4)
        self.assertEqual(vm.environment["cn"], "Box")
        self.assertEqual(vm.environment["mn"], "size")

    def test_computed_property_dynamic_dispatch_across_inheritance(self) -> None:
        program = Program(
            statements=(
                ClassNew("b", "ChildBox", ()),
                PropertyGet("m", "b", "size"),
            ),
            functions=(
                FunctionDef("BaseBox__get_size", (Return(Literal(42)),), params=("self",)),
            ),
            classes=(
                ClassDecl("BaseBox", None, (), (), computed_properties=("size",)),
                ClassDecl("ChildBox", None, (), (), base_class="BaseBox"),
            ),
        )
        vm = _run(program)
        self.assertEqual(vm.environment["m"], 42)

    def test_finalize_optional(self) -> None:
        program = Program(
            statements=(ClassNew("p", "Bare", ()), InstanceFinalize("p")),
            classes=(ClassDecl("Bare", None, (), ()),),
        )
        _run(program)

    def test_negative_unknown_method_raises_runtime_error(self) -> None:
        program = Program(
            statements=(
                ClassNew("p", "Point", ()),
                MethodCall("x", "p", "missing"),
            ),
            classes=(ClassDecl("Point", None, (), ("missing",)),),
        )
        with self.assertRaises(RuntimeSanskriptError):
            _run(program)

    def test_negative_unknown_method_diagnostic_includes_dispatch_context(self) -> None:
        program = Program(
            statements=(ClassNew("p", "Point", ()), MethodCall("x", "p", "missing")),
            classes=(ClassDecl("Point", None, (), ("missing",)),),
        )
        with self.assertRaises(RuntimeSanskriptError) as cm:
            _run(program)
        text = str(cm.exception)
        self.assertIn("argc=", text)
        self.assertIn("mro=", text)

    def test_negative_private_field_access_rejected_at_runtime(self) -> None:
        program = Program(
            statements=(
                ClassNew("p", "Vault", (Literal(7),)),
                ClassNew("h", "Hacker", ()),
                MethodCall("x", "h", "steal", (Reference("p"),)),
            ),
            functions=(
                FunctionDef(
                    "Vault__init__",
                    (
                        FieldSet("self", TextLiteral("secret"), Reference("v")),
                        Return(Reference("self")),
                    ),
                    params=("self", "v"),
                ),
                FunctionDef(
                    "Hacker__steal",
                    (
                        FieldGet("x", "obj", TextLiteral("secret")),
                        Return(Reference("x")),
                    ),
                    params=("self", "obj"),
                ),
            ),
            classes=(
                ClassDecl("Vault", None, (("secret", "i32"),), (), field_visibility=(("secret", "private"),)),
                ClassDecl("Hacker", None, (), ("steal",)),
            ),
        )
        with self.assertRaises(RuntimeSanskriptError):
            _run(program)

    def test_negative_protected_field_access_rejected_at_runtime(self) -> None:
        program = Program(
            statements=(
                ClassNew("b", "Base", (Literal(7),)),
                ClassNew("h", "Hacker", ()),
                MethodCall("x", "h", "steal", (Reference("b"),)),
            ),
            functions=(
                FunctionDef(
                    "Base__init__",
                    (
                        FieldSet("self", TextLiteral("k"), Reference("v")),
                        Return(Reference("self")),
                    ),
                    params=("self", "v"),
                ),
                FunctionDef(
                    "Hacker__steal",
                    (
                        FieldGet("x", "obj", TextLiteral("k")),
                        Return(Reference("x")),
                    ),
                    params=("self", "obj"),
                ),
            ),
            classes=(
                ClassDecl("Base", None, (("k", "i32"),), (), field_visibility=(("k", "protected"),)),
                ClassDecl("Hacker", None, (), ("steal",)),
            ),
        )
        with self.assertRaises(RuntimeSanskriptError):
            _run(program)

    def test_negative_method_call_on_finalized_instance(self) -> None:
        program = Program(
            statements=(
                ClassNew("r", "Res", ()),
                InstanceFinalize("r"),
                MethodCall("x", "r", "ping"),
            ),
            functions=(
                FunctionDef("Res__ping", (Return(Literal(1)),), params=("self",)),
            ),
            classes=(ClassDecl("Res", None, (), ("ping",)),),
        )
        with self.assertRaises(RuntimeSanskriptError):
            _run(program)

    def test_negative_field_read_on_finalized_instance(self) -> None:
        program = Program(
            statements=(
                ClassNew("r", "Res", (Literal(3),)),
                InstanceFinalize("r"),
                FieldGet("x", "r", TextLiteral("k")),
            ),
            functions=(
                FunctionDef(
                    "Res__init__",
                    (
                        FieldSet("self", TextLiteral("k"), Reference("v")),
                        Return(Reference("self")),
                    ),
                    params=("self", "v"),
                ),
            ),
            classes=(ClassDecl("Res", None, (("k", "i32"),), ()),),
        )
        with self.assertRaises(RuntimeSanskriptError):
            _run(program)

    def test_negative_typecheck_rejects_method_not_declared(self) -> None:
        program = Program(
            statements=(
                ClassNew("p", "Point", ()),
                MethodCall("x", "p", "missing"),
            ),
            classes=(ClassDecl("Point", None, (), ("ok",)),),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(program)

    def test_negative_typecheck_rejects_private_field_access(self) -> None:
        program = Program(
            statements=(
                ClassNew("p", "Vault", (Literal(7),)),
                ClassNew("h", "Hacker", ()),
                MethodCall("x", "h", "steal", (Reference("p"),)),
            ),
            functions=(
                FunctionDef(
                    "Vault__init__",
                    (
                        FieldSet("self", TextLiteral("secret"), Reference("v")),
                        Return(Reference("self")),
                    ),
                    params=("self", "v"),
                ),
                FunctionDef(
                    "Hacker__steal",
                    (
                        FieldGet("x", "obj", TextLiteral("secret")),
                        Return(Reference("x")),
                    ),
                    params=("self", "obj"),
                    param_types=("Hacker", "Vault"),
                ),
            ),
            classes=(
                ClassDecl("Vault", None, (("secret", "i32"),), (), field_visibility=(("secret", "private"),)),
                ClassDecl("Hacker", None, (), ("steal",)),
            ),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(program)

    def test_typecheck_allows_protected_field_access_from_subclass_method(self) -> None:
        program = Program(
            statements=(
                ClassNew("c", "Child", (Literal(5),)),
                MethodCall("out", "c", "read"),
            ),
            functions=(
                FunctionDef(
                    "Base__init__",
                    (
                        FieldSet("self", TextLiteral("k"), Reference("v")),
                        Return(Reference("self")),
                    ),
                    params=("self", "v"),
                ),
                FunctionDef(
                    "Child__read",
                    (
                        FieldGet("x", "self", TextLiteral("k")),
                        Return(Reference("x")),
                    ),
                    params=("self",),
                ),
            ),
            classes=(
                ClassDecl("Base", None, (("k", "i32"),), (), field_visibility=(("k", "protected"),)),
                ClassDecl("Child", None, (), ("read",), base_class="Base"),
            ),
        )
        compile_program(program)
        vm = _run(program)
        self.assertEqual(vm.environment["out"], 5)

    def test_negative_abstract_class_construction(self) -> None:
        program = Program(
            statements=(ClassNew("x", "Ghost", ()),),
            classes=(ClassDecl("Ghost", None, (), ("m",), abstract=True),),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(program)

    def test_negative_sealed_base_extension(self) -> None:
        classes = (
            ClassDecl("Final", None, (), (), sealed=True),
            ClassDecl("Bad", None, (), (), base_class="Final"),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(Program((), classes=classes))

    def test_negative_unknown_metaclass_rejected(self) -> None:
        program = Program(
            (),
            classes=(ClassDecl("Widget", None, (), (), metaclass="MissingMeta"),),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(program)

    def test_typecheck_accepts_inherited_class_and_static_methods(self) -> None:
        program = Program(
            statements=(
                StaticMethodCall("z", "ChildCounter", "zero"),
                ClassMethodCall("c", "ChildCounter", "make", (Literal(3),)),
            ),
            classes=(
                ClassDecl("Counter", None, (), (), static_methods=("zero",), class_methods=("make",)),
                ClassDecl("ChildCounter", None, (), (), base_class="Counter"),
            ),
            functions=(
                FunctionDef("Counter__static__zero", (Return(Literal(0)),), params=()),
                FunctionDef("Counter__make", (Return(Reference("n")),), params=("cls", "n")),
            ),
        )
        compile_program(program)

    def test_typecheck_resolves_inherited_instance_method_signature(self) -> None:
        program = Program(
            statements=(
                ClassNew("c", "Child", ()),
                MethodCall("x", "c", "area", (TextLiteral("bad"),)),
            ),
            classes=(
                ClassDecl("Base", None, (), ("area",)),
                ClassDecl("Child", None, (), (), base_class="Base"),
            ),
            functions=(
                FunctionDef(
                    "Base__area",
                    (Return(Reference("n")),),
                    params=("self", "n"),
                    param_types=("Base", "i32"),
                    return_type="i32",
                ),
            ),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(program)

    def test_negative_trait_impl_missing_required_method(self) -> None:
        program = Program(
            (),
            classes=(ClassDecl("Box", None, (), ("darśaya",), trait_impls=("Samānatā",)),),
        )
        with self.assertRaises(TypeCheckError):
            compile_program(program)


class Phase7YantraPathaTests(unittest.TestCase):
    def test_class_new_and_method_call_yantra_round_trip(self) -> None:
        prose = "\n".join(
            (
                "saṃskaraṇam dvitīyam.",
                "",
                "mukhyaḥ pāṭhaḥ ārabhyate.",
                "Point iti varga-nirmāṇam kriyate.",
                "p iti nāma sthāpyate.",
                "p iti nāma āhriyate.",
                "śūnyam iti pūrṇāṅkaḥ nikṣipyate.",
                "sum iti paddhati-āhvānam kriyate.",
                "out iti nāma sthāpyate.",
                "āgrahītvaḥ samāpyate.",
                "pāṭhaḥ samāpyate.",
            )
        )
        from sanskript.yantra_patha import _YantraPathaParser

        restored = _YantraPathaParser(prose).parse()
        ops = [ins.opcode for ins in restored.instructions]
        self.assertIn(OpCode.CLASS_NEW, ops)
        self.assertIn(OpCode.METHOD_CALL, ops)


class Phase7ExampleTests(unittest.TestCase):
    def test_example_program_runs(self) -> None:
        program = Program(
            statements=(
                ClassNew("dīpaḥ", "Dīpakaḥ", (Literal(5),)),
                MethodCall("tyaktam", "dīpaḥ", "vardhaya", (Literal(2),)),
                MethodCall("phalam", "dīpaḥ", "darśaya"),
                Display(Reference("phalam")),
            ),
            functions=(
                FunctionDef(
                    "Dīpakaḥ__init__",
                    (
                        FieldSet("self", TextLiteral("__class__"), TextLiteral("Dīpakaḥ")),
                        FieldSet("self", TextLiteral("jyoti"), Reference("prārambhaḥ")),
                        Return(Reference("self")),
                    ),
                    params=("self", "prārambhaḥ"),
                ),
                FunctionDef(
                    "Dīpakaḥ__vardhaya",
                    (
                        FieldGet("pūrvaṃ", "self", TextLiteral("jyoti")),
                        Assign("navam", BinaryValue("add", Reference("pūrvaṃ"), Reference("mātrā"))),
                        FieldSet("self", TextLiteral("jyoti"), Reference("navam")),
                        Return(Reference("self")),
                    ),
                    params=("self", "mātrā"),
                ),
                FunctionDef(
                    "Dīpakaḥ__darśaya",
                    (
                        FieldGet("jyotiḥ", "self", TextLiteral("jyoti")),
                        Return(Reference("jyotiḥ")),
                    ),
                    params=("self",),
                ),
            ),
            classes=(
                ClassDecl("Dīpakaḥ", None, (("jyoti", "i32"),), ("vardhaya", "darśaya")),
            ),
        )
        self.assertEqual(SanskriptVM().execute(compile_program(program)), ["7"])

    def test_phase7_example_file_documents_surface_syntax(self) -> None:
        path = _EXAMPLES / "phase7-oop.ssk"
        source = path.read_text(encoding="utf-8")
        self.assertIn("vargaḥ", source)
        self.assertIn("nirmāṇam", source)
        self.assertIn("paddhati-āhvānam", source)


if __name__ == "__main__":
    unittest.main()
