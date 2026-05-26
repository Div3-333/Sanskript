"""Source directives for samūha (list) and kośa (map) surakṣita collections."""

from __future__ import annotations

import unittest
from pathlib import Path

from sanskript.ast import ListAppend, ListInit, MapContains, MapGet, MapInit, MapPut
from sanskript.compiler import compile_source
from sanskript.parser import parse_program
from sanskript.vm import SanskriptVM

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


class SourceCollectionTests(unittest.TestCase):
    def test_parse_collection_directives(self) -> None:
        program = parse_program(
            """
            samūhaḥ phale.
            yojanam phale pañca.
            kośaḥ mūlye.
            sthāpanam mūlye phala pañca.
            āharaṇam parināmam mūlye phala.
            asti tattvam mūlye phala.
            """
        )
        kinds = [type(s).__name__ for s in program.statements]
        self.assertEqual(
            kinds,
            ["ListInit", "ListAppend", "MapInit", "MapPut", "MapGet", "MapContains"],
        )
        self.assertIsInstance(program.statements[0], ListInit)
        self.assertIsInstance(program.statements[1], ListAppend)
        self.assertIsInstance(program.statements[2], MapInit)
        self.assertIsInstance(program.statements[3], MapPut)
        self.assertIsInstance(program.statements[4], MapGet)
        self.assertIsInstance(program.statements[5], MapContains)

    def test_map_contains_drives_if_branch(self) -> None:
        source = """
        kośaḥ mūlye.
        sthāpanam mūlye phala pañca.
        asti tattvam mūlye phala.
        yadi tattvam samam ekaṃ.
        gaṇakaḥ pañca darśayati.
        antam.
        """
        self.assertEqual(SanskriptVM().execute(compile_source(source)), ["5"])

    def test_example_program_runs(self) -> None:
        source = (EXAMPLES / "ekadasha-samūha.ssk").read_text(encoding="utf-8")
        self.assertEqual(
            SanskriptVM().execute(compile_source(source)),
            ["[5, 10]", "5"],
        )

    def test_surakshita_tier_blocks_heap(self) -> None:
        from sanskript.bytecode import BytecodeProgram, Instruction, OpCode
        from sanskript.errors import RuntimeSanskriptError

        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.HALT),
            ),
            safety_tier="surakshita",
        )
        with self.assertRaises(RuntimeSanskriptError):
            SanskriptVM().execute(program)


if __name__ == "__main__":
    unittest.main()
