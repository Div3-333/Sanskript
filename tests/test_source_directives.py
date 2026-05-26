"""End-to-end tests: Sanskrit source directives → parse → compile → VM."""

from __future__ import annotations

import unittest
from pathlib import Path

from sanskript.ast import Call, Display, FunctionDef, If, While
from sanskript.compiler import compile_source
from sanskript.parser import parse_program
from sanskript.vm import SanskriptVM

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


class SourceDirectiveTests(unittest.TestCase):
    def test_parse_if_while_function_and_module(self) -> None:
        program = parse_program(
            (EXAMPLES / "shashṭha-if.ssk").read_text(encoding="utf-8")
        )
        self.assertGreaterEqual(len(program.statements), 2)
        if_stmts = [s for s in program.statements if isinstance(s, If)]
        self.assertEqual(len(if_stmts), 1)
        self.assertIsInstance(program.statements[-1], Display)

        while_program = parse_program(
            (EXAMPLES / "saptama-while.ssk").read_text(encoding="utf-8")
        )
        while_stmts = [s for s in while_program.statements if isinstance(s, While)]
        self.assertEqual(len(while_stmts), 1)

        fn_program = parse_program(
            (EXAMPLES / "aṣṭama-vidhānam.ssk").read_text(encoding="utf-8")
        )
        self.assertEqual(len(fn_program.functions), 1)
        self.assertEqual(fn_program.functions[0].name, "vṛddhi")

        mod_program = parse_program(
            (EXAMPLES / "navama-kṣetram.ssk").read_text(encoding="utf-8")
        )
        self.assertEqual(len(mod_program.modules), 1)
        self.assertEqual(mod_program.modules[0][0], "gaṇita")
        calls = [s for s in mod_program.statements if isinstance(s, Call)]
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].module, "gaṇita")

    def test_if_from_source_runs(self) -> None:
        source = (EXAMPLES / "shashṭha-if.ssk").read_text(encoding="utf-8")
        self.assertEqual(SanskriptVM().execute(compile_source(source)), ["13"])

    def test_while_from_source_runs(self) -> None:
        source = (EXAMPLES / "saptama-while.ssk").read_text(encoding="utf-8")
        self.assertEqual(SanskriptVM().execute(compile_source(source)), ["2"])

    def test_function_from_source_runs(self) -> None:
        source = (EXAMPLES / "aṣṭama-vidhānam.ssk").read_text(encoding="utf-8")
        self.assertEqual(SanskriptVM().execute(compile_source(source)), ["11"])

    def test_module_call_from_source_runs(self) -> None:
        source = (EXAMPLES / "navama-kṣetram.ssk").read_text(encoding="utf-8")
        self.assertEqual(SanskriptVM().execute(compile_source(source)), ["11"])

    def test_inline_if_and_call_directives(self) -> None:
        source = """
        gaṇakaḥ pañca phale nidadhāti.
        yadi phalaṃ samam pañca.
        gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
        antam.
        gaṇakaḥ phalaṃ darśayati.
        """
        self.assertEqual(SanskriptVM().execute(compile_source(source)), ["7"])

        fn_source = """
        vidhānam set.
        gaṇakaḥ pañca phale nidadhāti.
        samāpanam.
        āhvānam set.
        """
        program = parse_program(fn_source)
        self.assertEqual(len(program.functions), 1)
        self.assertIsInstance(program.functions[0], FunctionDef)
        self.assertEqual(program.functions[0].name, "set")

    def test_function_parameters_from_source_run(self) -> None:
        source = """
        vidhānam sthāpaya balaṃ.
        gaṇakaḥ balaṃ phale nidadhāti.
        samāpanam.
        āhvānam sthāpaya pañca.
        gaṇakaḥ phalaṃ darśayati.
        """
        program = parse_program(source)

        self.assertEqual(program.functions[0].params, ("bala",))
        self.assertEqual(SanskriptVM().execute(compile_source(source)), ["5"])

    def test_module_function_parameters_from_source_run(self) -> None:
        source = """
        kṣetram gaṇita.
        vidhānam sthāpaya balaṃ.
        gaṇakaḥ balaṃ phale nidadhāti.
        samāpanam.
        samāpanam.
        āhvānam gaṇita sthāpaya sapta.
        gaṇakaḥ phalaṃ darśayati.
        """
        program = parse_program(source)
        function = program.modules[0][1][0]

        self.assertEqual(function.params, ("bala",))
        self.assertEqual(SanskriptVM().execute(compile_source(source)), ["7"])

    def test_function_text_parameter_from_source_runs(self) -> None:
        source = """
        vidhānam likha balaṃ.
        gaṇakaḥ balaṃ phale nidadhāti.
        samāpanam.
        āhvānam likha vākyam svāgatam mitra iti.
        gaṇakaḥ phalaṃ darśayati.
        """

        self.assertEqual(SanskriptVM().execute(compile_source(source)), ["svāgatam mitra"])


if __name__ == "__main__":
    unittest.main()
