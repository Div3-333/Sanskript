"""Phase 3/4 example programs must be substantive, not copies of prathama.ssk."""

from __future__ import annotations

import unittest
from pathlib import Path

from sanskript.cli import main
from sanskript.compiler import compile_source
from sanskript.vm import SanskriptVM

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


class PhaseExampleTests(unittest.TestCase):
    def test_phase3_example_compiles_and_shows_phase3_directives(self) -> None:
        path = EXAMPLES / "phase3-data-types.ssk"
        source = path.read_text(encoding="utf-8")
        self.assertIn("vikalpam", source)
        self.assertIn("ati-pūrṇāṅka", source)
        self.assertNotEqual(
            source.strip(),
            (EXAMPLES / "prathama.ssk").read_text(encoding="utf-8").strip(),
        )
        output = SanskriptVM().execute(compile_source(source))
        self.assertIn("some(7)", output)
        self.assertIn("i8(127)", output)
        self.assertIn("ok(42)", output)

    def test_phase4_example_compiles_and_parses_type_directives(self) -> None:
        path = EXAMPLES / "phase4-types.ssk"
        source = path.read_text(encoding="utf-8")
        self.assertIn("prakāraḥ", source)
        self.assertIn("vastu-prakāraḥ", source)
        from sanskript.parser import parse_program

        program = parse_program(source)
        self.assertGreaterEqual(len(program.type_aliases), 1)
        self.assertGreaterEqual(len(program.record_types), 1)

    def test_phase_examples_compile_via_cli(self) -> None:
        for name in ("phase3-data-types.ssk", "phase4-types.ssk", "phase6-functions.ssk", "phase7-oop.ssk"):
            with self.subTest(example=name):
                self.assertEqual(main(["compile", str(EXAMPLES / name)]), 0)

    def test_phase6_example_runs(self) -> None:
        path = EXAMPLES / "phase6-functions.ssk"
        source = path.read_text(encoding="utf-8")
        self.assertIn("yogaḥ", source)
        self.assertIn("kālavyāpāre", source)
        output = SanskriptVM().execute(compile_source(source))
        self.assertEqual(
            output,
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

    def test_phase7_example_runs(self) -> None:
        path = EXAMPLES / "phase7-oop.ssk"
        source = path.read_text(encoding="utf-8")
        self.assertIn("vargaḥ", source)
        self.assertIn("nirmāṇam", source)
        output = SanskriptVM().execute(compile_source(source))
        self.assertEqual(output, ["7", "śūnyam", "6"])


if __name__ == "__main__":
    unittest.main()
