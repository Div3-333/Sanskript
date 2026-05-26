import unittest

from sanskript.ast import Assign, Call, Display, FunctionDef, Literal, Program, Reference, Return
from sanskript.bytecode import decode_program, encode_program, qualified_function_name
from sanskript.compiler import compile_program
from sanskript.vm import SanskriptVM


class FunctionModuleTests(unittest.TestCase):
    def test_top_level_function_call(self) -> None:
        program = Program(
            statements=(
                Assign("phala", Literal(0)),
                Call("vṛddhi"),
                Display(Reference("phala")),
            ),
            functions=(
                FunctionDef(
                    "vṛddhi",
                    (
                        Assign("phala", Literal(5)),
                        Assign("phala", Literal(7)),
                    ),
                ),
            ),
        )
        output = SanskriptVM().execute(compile_program(program))
        self.assertEqual(output, ["7"])

    def test_module_qualified_call(self) -> None:
        program = Program(
            statements=(
                Assign("phala", Literal(0)),
                Call("vṛddhi", module="gaṇita"),
                Display(Reference("phala")),
            ),
            modules=(
                (
                    "gaṇita",
                    (
                        FunctionDef(
                            "vṛddhi",
                            (Assign("phala", Literal(11)),),
                            module="gaṇita",
                        ),
                    ),
                ),
            ),
        )
        bytecode = compile_program(program)
        target = qualified_function_name("gaṇita", "vṛddhi")
        self.assertEqual(len(bytecode.modules), 1)
        output = SanskriptVM().execute(bytecode)
        self.assertEqual(output, ["11"])

    def test_procedure_mutates_global_state(self) -> None:
        program = Program(
            statements=(
                Assign("phala", Literal(1)),
                Call("set"),
                Display(Reference("phala")),
            ),
            functions=(
                FunctionDef(
                    "set",
                    (Assign("phala", Literal(99)),),
                ),
            ),
        )
        output = SanskriptVM().execute(compile_program(program))
        self.assertEqual(output, ["99"])

    def test_function_bytecode_round_trips_through_json_payload(self) -> None:
        program = Program(
            statements=(Call("set"), Display(Reference("phala"))),
            functions=(FunctionDef("set", (Assign("phala", Literal(99)),)),),
        )
        bytecode = compile_program(program)
        restored = decode_program(encode_program(bytecode))

        self.assertEqual(SanskriptVM().execute(restored), ["99"])

    def test_function_parameters_bind_as_local_values(self) -> None:
        program = Program(
            statements=(
                Call("sthāpaya", args=(Literal(12),)),
                Display(Reference("phala")),
            ),
            functions=(
                FunctionDef(
                    "sthāpaya",
                    (Assign("phala", Reference("mūlya")),),
                    params=("mūlya",),
                ),
            ),
        )

        output = SanskriptVM().execute(compile_program(program))

        self.assertEqual(output, ["12"])

    def test_function_parameters_shadow_globals_without_overwriting_them(self) -> None:
        program = Program(
            statements=(
                Assign("mūlya", Literal(1)),
                Call("sthāpaya", args=(Literal(8),)),
                Display(Reference("mūlya")),
                Display(Reference("phala")),
            ),
            functions=(
                FunctionDef(
                    "sthāpaya",
                    (
                        Assign("mūlya", Literal(9)),
                        Assign("phala", Reference("mūlya")),
                    ),
                    params=("mūlya",),
                ),
            ),
        )

        output = SanskriptVM().execute(compile_program(program))

        self.assertEqual(output, ["1", "9"])

    def test_function_params_round_trip_through_json_payload(self) -> None:
        program = Program(
            statements=(Call("sthāpaya", args=(Literal(12),)), Display(Reference("phala"))),
            functions=(
                FunctionDef(
                    "sthāpaya",
                    (Assign("phala", Reference("mūlya")), Return(Reference("mūlya"))),
                    params=("mūlya",),
                ),
            ),
        )
        bytecode = compile_program(program)
        restored = decode_program(encode_program(bytecode))

        self.assertEqual(restored.functions[0].params, ("mūlya",))
        self.assertEqual(SanskriptVM().execute(restored), ["12"])
