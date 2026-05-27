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
                ),
            ),
        )
        child = program.classes[1]
        self.assertEqual(child.base_class, "Shape")
        self.assertIn(("secret", "private"), child.field_visibility)
        self.assertIn("zero", child.static_methods)
        self.assertIn("factory", child.class_methods)
        self.assertIn("magnitude", child.computed_properties)


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
