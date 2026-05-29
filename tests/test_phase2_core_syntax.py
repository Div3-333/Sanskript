"""Phase 2: core syntax and semantics — parse, compile, VM."""

from __future__ import annotations

import unittest
from pathlib import Path

from sanskript.ast import (
    Bind,
    FieldSet,
    RecordInit,
)
from sanskript.compiler import compile_program, compile_source
from sanskript.errors import CompileError, MorphologyError, ParseError, RuntimeSanskriptError
from sanskript.parser import parse_program
from sanskript.bytecode import OpCode
from sanskript.vm import SanskriptVM

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def _run(source: str) -> list[str]:
    return SanskriptVM().execute(compile_source(source))


class Phase2CoreSyntaxTests(unittest.TestCase):
    # ------------------------------------------------------------------
    # Nil / zero
    # ------------------------------------------------------------------

    def test_nil_literal_distinct_from_zero(self) -> None:
        source = """
        gaṇitam phala śūnyam.
        gaṇakaḥ phalaṃ darśayati.
        """
        self.assertEqual(_run(source), ["śūnyam"])

    def test_nil_roundtrip_output(self) -> None:
        source = "gaṇitam phala śūnyam.\ndarśanam phala."
        self.assertEqual(_run(source), ["śūnyam"])

    def test_integer_zero_roundtrip_output(self) -> None:
        source = "gaṇitam phala śūnya.\ndarśanam phala."
        self.assertEqual(_run(source), ["0"])

    # ------------------------------------------------------------------
    # Immutable binding
    # ------------------------------------------------------------------

    def test_immutable_binding_rejected_on_reassign(self) -> None:
        source = """
        acalachihnam phala pañca.
        gaṇitam phala daśa.
        """
        with self.assertRaises(CompileError):
            compile_source(source)

    def test_immutable_nityam_rejected_on_reassign(self) -> None:
        source = "nityam phala pañca.\ngaṇitam phala daśa."
        with self.assertRaises(CompileError):
            compile_source(source)

    def test_immutable_binding_can_be_read(self) -> None:
        source = "acalachihnam phala pañca.\ndarśanam phala."
        self.assertEqual(_run(source), ["5"])

    # ------------------------------------------------------------------
    # Block scope
    # ------------------------------------------------------------------

    def test_shadowing_duplicate_bind_in_block(self) -> None:
        source = """
        khaṇḍaḥ.
        gaṇitam phala pañca.
        gaṇitam phala daśa.
        antam.
        """
        with self.assertRaises(CompileError):
            compile_source(source)

    def test_block_scope(self) -> None:
        source = """
        gaṇitam phala śūnyam.
        khaṇḍaḥ.
        gaṇitam phala pañca.
        antam.
        gaṇakaḥ phalaṃ darśayati.
        """
        self.assertEqual(_run(source), ["śūnyam"])

    def test_block_scope_outer_unchanged_directive(self) -> None:
        source = "gaṇitam phala pañca.\nkhaṇḍaḥ.\ngaṇitam phala daśa.\nantam.\ndarśanam phala."
        self.assertEqual(_run(source), ["5"])

    # ------------------------------------------------------------------
    # Boolean short-circuit
    # ------------------------------------------------------------------

    def test_boolean_short_circuit_parse(self) -> None:
        source = """
        gaṇitam phala śūnya.
        gaṇitam mitra pañca.
        yadi phalaṃ samam śūnya ca mitraṃ samam pañca.
        gaṇitam phala eka.
        antam.
        """
        program = parse_program(source)
        if_stmts = [s for s in program.statements if s.__class__.__name__ == "If"]
        self.assertEqual(len(if_stmts), 1)
        self.assertEqual(if_stmts[0].condition.__class__.__name__, "BoolAndCond")

    def test_boolean_or_parse(self) -> None:
        source = "yadi phalaṃ samam eka vā mitraṃ samam pañca."
        program = parse_program(source)
        if_stmt = next(s for s in program.statements if s.__class__.__name__ == "If")
        self.assertEqual(if_stmt.condition.__class__.__name__, "BoolOrCond")

    def test_boolean_and_produces_and_ast_node(self) -> None:
        # Verify BoolAndCond is produced for 'ca' compound condition
        source = "gaṇitam phala pañca.\nyadi phalaṃ samam pañca ca phalaṃ mahattaram tri.\ndarśanam phala.\nantam."
        program = parse_program(source)
        ifs = [s for s in program.statements if s.__class__.__name__ == "If"]
        self.assertEqual(ifs[0].condition.__class__.__name__, "BoolAndCond")

    def test_boolean_or_produces_or_ast_node(self) -> None:
        # Verify BoolOrCond is produced for 'vā' compound condition
        source = "gaṇitam phala pañca.\nyadi phalaṃ samam eka vā phalaṃ samam pañca.\ndarśanam phala.\nantam."
        program = parse_program(source)
        ifs = [s for s in program.statements if s.__class__.__name__ == "If"]
        self.assertEqual(ifs[0].condition.__class__.__name__, "BoolOrCond")

    # ------------------------------------------------------------------
    # Comparisons
    # ------------------------------------------------------------------

    def test_comparisons_asamam_mahattaram(self) -> None:
        source = """
        gaṇitam phala pañca.
        yadi phalaṃ asamam daśa.
        gaṇakaḥ phalaṃ ekena vardhayati.
        antam.
        yadi phalaṃ mahattaram tri.
        gaṇakaḥ phalaṃ ekena vardhayati.
        antam.
        gaṇakaḥ phalaṃ darśayati.
        """
        self.assertEqual(_run(source), ["7"])

    def test_comparison_samam_taken(self) -> None:
        source = """
        gaṇitam phala pañca.
        yadi phalaṃ samam pañca.
        gaṇakaḥ phalaṃ ekena vardhayati.
        antam.
        gaṇakaḥ phalaṃ darśayati.
        """
        self.assertEqual(_run(source), ["6"])

    def test_comparison_laghutaram_taken(self) -> None:
        source = """
        gaṇitam phala tri.
        yadi phalaṃ laghutaram pañca.
        gaṇakaḥ phalaṃ ekena vardhayati.
        antam.
        gaṇakaḥ phalaṃ darśayati.
        """
        self.assertEqual(_run(source), ["4"])

    def test_comparison_tulyam_taken(self) -> None:
        source = """
        gaṇitam phala pañca.
        yadi phalaṃ tulyam pañca.
        gaṇakaḥ phalaṃ ekena vardhayati.
        antam.
        gaṇakaḥ phalaṃ darśayati.
        """
        self.assertEqual(_run(source), ["6"])

    def test_comparison_not_taken_gives_no_output(self) -> None:
        source = """
        gaṇitam phala pañca.
        yadi phalaṃ samam daśa.
        gaṇakaḥ phalaṃ darśayati.
        antam.
        """
        self.assertEqual(_run(source), [])

    # ------------------------------------------------------------------
    # Literal forms
    # ------------------------------------------------------------------

    def test_list_and_map_literal_directives(self) -> None:
        source = """
        samūhalakṣaṇaḥ items eka dvi tri.
        kośalakṣaṇaḥ table phala pañca dṛṣṭa daśa.
        darśanam table.
        """
        program = parse_program(source)
        binds = [s for s in program.statements if isinstance(s, Bind)]
        self.assertEqual(len(binds), 2)

    def test_list_literal_vm(self) -> None:
        source = "samūhalakṣaṇaḥ items eka dvi tri.\ndarśanam items."
        output = _run(source)
        self.assertEqual(len(output), 1)
        self.assertIn("1", output[0])
        self.assertIn("3", output[0])

    def test_map_literal_vm(self) -> None:
        source = "kośalakṣaṇaḥ table eka pañca.\ndarśanam table."
        output = _run(source)
        self.assertEqual(len(output), 1)
        self.assertIn("5", output[0])

    def test_bytes_literal_directive(self) -> None:
        source = """
        akṣarāṇi data 48656c6c6f.
        darśanam data.
        """
        output = _run(source)
        self.assertEqual(len(output), 1)
        self.assertTrue("Hello" in output[0] or "48656c6c6f" in output[0])

    def test_record_literal_parses_to_record_init_and_field_sets(self) -> None:
        source = "vastulakṣaṇaḥ vastu nāma pañca vayaḥ daśa."
        program = parse_program(source)
        stmts = program.statements
        self.assertIsInstance(stmts[0], RecordInit)
        self.assertEqual(stmts[0].record, "vastu")
        field_sets = [s for s in stmts if isinstance(s, FieldSet)]
        self.assertEqual(len(field_sets), 2)

    def test_record_literal_vm_field_value(self) -> None:
        source = (
            "vastulakṣaṇaḥ vastu nāma pañca vayaḥ daśa.\n"
            "aṅgāharaṇam phala vastu nāma.\n"
            "darśanam phala."
        )
        self.assertEqual(_run(source), ["5"])

    def test_record_literal_second_field(self) -> None:
        source = (
            "vastulakṣaṇaḥ vastu nāma pañca vayaḥ daśa.\n"
            "aṅgāharaṇam phala vastu vayaḥ.\n"
            "darśanam phala."
        )
        self.assertEqual(_run(source), ["10"])

    def test_grouped_literal_combinations_cover_ast_bytecode_and_vm(self) -> None:
        source = """
        samūhalakṣaṇaḥ items pariveṣṭanam pañca antam sapta.
        kośalakṣaṇaḥ table pariveṣṭanam eka antam pariveṣṭanam daśa antam.
        vastulakṣaṇaḥ vastu vākyam pūrṇa nāma iti pariveṣṭanam daśa antam.
        aṅgāharaṇam name_value vastu vākyam pūrṇa nāma iti.
        darśanam items.
        darśanam table.
        darśanam name_value.
        """
        program = parse_program(source)
        list_bind = next(stmt for stmt in program.statements if isinstance(stmt, Bind) and stmt.target == "items")
        map_bind = next(stmt for stmt in program.statements if isinstance(stmt, Bind) and stmt.target == "table")
        record_init = next(stmt for stmt in program.statements if isinstance(stmt, RecordInit))

        self.assertEqual(list_bind.value.__class__.__name__, "ListLiteral")
        self.assertEqual(list_bind.value.elements[0].__class__.__name__, "GroupValue")
        self.assertEqual(map_bind.value.__class__.__name__, "MapLiteral")
        self.assertEqual(map_bind.value.entries[0][0].__class__.__name__, "GroupValue")
        self.assertIsInstance(record_init, RecordInit)

        bytecode = compile_program(program)
        opcodes = [inst.opcode for inst in bytecode.instructions]
        self.assertIn(OpCode.LIST_NEW, opcodes)
        self.assertIn(OpCode.MAP_NEW, opcodes)
        self.assertIn(OpCode.MAP_SET, opcodes)
        self.assertIn(OpCode.RECORD_NEW, opcodes)
        self.assertIn(OpCode.RECORD_SET, opcodes)
        self.assertIn(OpCode.RECORD_GET, opcodes)

        self.assertEqual(SanskriptVM().execute(bytecode), ["[5, 7]", "{1:10}", "10"])

    def test_module_scope_with_grouped_literals_runs_through_vm(self) -> None:
        source = """
        kṣetram gaṇita.
        vidhānam nirmā.
        kośalakṣaṇaḥ table pariveṣṭanam eka antam pariveṣṭanam sapta antam.
        vastulakṣaṇaḥ vastu nāma vākyam śubha iti.
        aṅgāharaṇam phala vastu nāma.
        pratyāvartanam phala.
        samāpanam.
        niḥsāram nirmā.
        samāpanam.
        āhvānam gaṇita nirmā phale nidadhāti.
        darśanam phala.
        """
        program = parse_program(source)
        self.assertEqual(program.modules[0].name, "gaṇita")
        self.assertEqual(program.modules[0].exports, frozenset({"nirmā"}))
        self.assertEqual(SanskriptVM().execute(compile_program(program)), ["śubha"])

    def test_record_and_map_missing_member_raise_runtime_errors(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            _run("kośalakṣaṇaḥ table eka pañca.\nāharaṇam phala table dvi.")
        with self.assertRaises(RuntimeSanskriptError):
            _run("vastulakṣaṇaḥ vastu nāma pañca.\naṅgāharaṇam phala vastu vayaḥ.")

    def test_grouped_literal_matrix_compiles_and_runs_across_directives(self) -> None:
        cases = (
            (
                "samūhalakṣaṇaḥ",
                "samūhalakṣaṇaḥ items pariveṣṭanam pañca antam sapta.\ndarśanam items.",
                Bind,
                "items",
                OpCode.LIST_NEW,
                "[5, 7]",
            ),
            (
                "kośalakṣaṇaḥ",
                "kośalakṣaṇaḥ table pariveṣṭanam eka antam pariveṣṭanam daśa antam.\ndarśanam table.",
                Bind,
                "table",
                OpCode.MAP_NEW,
                "{1:10}",
            ),
            (
                "vastulakṣaṇaḥ",
                (
                    "vastulakṣaṇaḥ vastu vākyam nāma iti pariveṣṭanam daśa antam.\n"
                    "aṅgāharaṇam out vastu vākyam nāma iti.\n"
                    "darśanam out."
                ),
                RecordInit,
                "vastu",
                OpCode.RECORD_NEW,
                "10",
            ),
        )
        for directive_name, source, stmt_type, target, required_opcode, expected in cases:
            with self.subTest(directive=directive_name):
                program = parse_program(source)
                first = program.statements[0]
                self.assertIsInstance(first, stmt_type)
                if isinstance(first, Bind):
                    self.assertEqual(first.target, target)
                    self.assertEqual(first.value.__class__.__name__, "ListLiteral" if directive_name == "samūhalakṣaṇaḥ" else "MapLiteral")
                else:
                    self.assertEqual(first.record, target)
                bytecode = compile_program(program)
                opcodes = [inst.opcode for inst in bytecode.instructions]
                self.assertIn(required_opcode, opcodes)
                self.assertEqual(SanskriptVM().execute(bytecode), [expected])

    def test_nested_grouped_literals_across_list_map_record_and_module_scope(self) -> None:
        source = """
        kṣetram gaṇita.
        vidhānam nirmā.
        samūhalakṣaṇaḥ items pariveṣṭanam pariveṣṭanam eka antam antam sapta.
        kośalakṣaṇaḥ table pariveṣṭanam pariveṣṭanam eka antam antam pariveṣṭanam daśa antam.
        vastulakṣaṇaḥ vastu nāma pariveṣṭanam pariveṣṭanam daśa antam antam.
        aṅgāharaṇam name_value vastu nāma.
        pratyāvartanam name_value.
        samāpanam.
        niḥsāram nirmā.
        samāpanam.
        āhvānam gaṇita nirmā phale nidadhāti.
        darśanam phala.
        """
        program = parse_program(source)
        module = program.modules[0]
        self.assertEqual(module.name, "gaṇita")
        function = module.functions[0]
        list_bind = next(stmt for stmt in function.body if isinstance(stmt, Bind) and stmt.target == "items")
        map_bind = next(stmt for stmt in function.body if isinstance(stmt, Bind) and stmt.target == "table")
        self.assertEqual(list_bind.value.elements[0].__class__.__name__, "GroupValue")
        self.assertEqual(map_bind.value.entries[0][0].__class__.__name__, "GroupValue")

        bytecode = compile_program(program)
        module_opcodes = [inst.opcode for inst in bytecode.modules[0].functions[0].instructions]
        self.assertIn(OpCode.LIST_NEW, module_opcodes)
        self.assertIn(OpCode.MAP_NEW, module_opcodes)
        self.assertIn(OpCode.RECORD_NEW, module_opcodes)
        self.assertIn(OpCode.RECORD_GET, module_opcodes)
        self.assertEqual(SanskriptVM().execute(bytecode), ["10"])

    def test_grouping_and_literal_directive_negatives(self) -> None:
        invalid_sources = (
            "kośalakṣaṇaḥ table eka pañca dvi.\ndarśanam table.",
            "vastulakṣaṇaḥ vastu pariveṣṭanam pañca antam.\ndarśanam vastu.",
            "samūhalakṣaṇaḥ items pariveṣṭanam pañca.\ndarśanam items.",
            "kośalakṣaṇaḥ table pariveṣṭanam eka antam.\ndarśanam table.",
            "samūhalakṣaṇaḥ items pariveṣṭanam pariveṣṭanam eka antam antam antam.\ndarśanam items.",
            "kośalakṣaṇaḥ table pariveṣṭanam pariveṣṭanam eka antam antam pariveṣṭanam daśa antam antam.\ndarśanam table.",
            "vastulakṣaṇaḥ vastu nāma pariveṣṭanam pariveṣṭanam daśa antam antam antam.\ndarśanam vastu.",
            "samūhalakṣaṇaḥ items pariveṣṭanam pariveṣṭanam eka antam.\ndarśanam items.",
        )
        for source in invalid_sources:
            with self.subTest(source=source):
                with self.assertRaises((ParseError, CompileError, MorphologyError)):
                    compile_source(source)

    # ------------------------------------------------------------------
    # void / tyāgaḥ
    # ------------------------------------------------------------------

    def test_void_tyagah_discards_value(self) -> None:
        source = "tyāgaḥ pañca.\ndarśanam pañca."
        self.assertEqual(_run(source), ["5"])

    # ------------------------------------------------------------------
    # Export directive
    # ------------------------------------------------------------------

    def test_export_directive_parses(self) -> None:
        source = (EXAMPLES / "dvādaśa-phase2-kṣetram.ssk").read_text(encoding="utf-8")
        program = parse_program(source)
        self.assertEqual(program.modules[0].exports, frozenset({"vṛddhi"}))

    # ------------------------------------------------------------------
    # Negative: undefined name
    # ------------------------------------------------------------------

    def test_undefined_name_raises_at_runtime(self) -> None:
        source = "darśanam phala."
        with self.assertRaises(RuntimeSanskriptError):
            _run(source)

    # ------------------------------------------------------------------
    # Realistic example
    # ------------------------------------------------------------------

    def test_phase2_example_runs(self) -> None:
        path = EXAMPLES / "dvādaśa-phase2-boolean.ssk"
        self.assertEqual(
            SanskriptVM().execute(compile_program(parse_program(path.read_text(encoding="utf-8")))),
            ["5"],
        )

    def test_phase2_grouped_literal_example_runs(self) -> None:
        path = EXAMPLES / "dvādaśa-phase2-grouping-matrix.ssk"
        self.assertEqual(
            SanskriptVM().execute(compile_program(parse_program(path.read_text(encoding="utf-8")))),
            ["10"],
        )


if __name__ == "__main__":
    unittest.main()
