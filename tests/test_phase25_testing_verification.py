"""Phase 25 testing and verification harness tests."""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode
from sanskript.cli import main as cli_main
from sanskript.compiler import compile_program
from sanskript.module_loader import load_program_from_path
from sanskript.phase25_testing_verification import (
    FUZZ_SMOKE_TRIAL_BUDGET,
    GOLDEN_DIR,
    MIN_OPCODE_DEDICATED_TEST_RATIO,
    PRODUCTION_FUZZ_MIN_TRIALS,
    Phase25EvidenceRequest,
    audit_opcode_coverage,
    audit_parser_rule_coverage,
    build_coverage_map,
    coverage_thresholds_met,
    differential_host_compiler_scaffold,
    differential_host_vm_scaffold,
    differential_scaffolds_deterministic,
    fuzz_non_overclaim_metadata,
    generate_phase25_evidence,
    phase25_seal_verdict,
    run_bytecode_verifier_fuzz,
    run_parser_fuzz,
    run_property_collections,
    run_property_compare_eq,
    run_property_list_get,
    run_property_map_roundtrip,
    run_property_multiply,
    run_property_numeric,
    run_property_subtract,
    run_property_text,
    run_sskyp_fuzz,
    roundtrip_bytecode_serialization,
    roundtrip_sskyp_assembly,
    security_review_checklist,
    verify_golden_bytecode_entries,
    verify_golden_hashes_stable,
    verify_golden_source_entries,
    verify_golden_sskyp_entries,
    write_coverage_map,
)
from sanskript.vm import SanskriptVM
from sanskript.yantra_patha import program_from_yantra_patha

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


class Phase25GoldenTests(unittest.TestCase):
    def test_golden_manifest_paths_exist(self) -> None:
        manifest = json.loads((GOLDEN_DIR / "manifest.json").read_text(encoding="utf-8"))
        for entry in manifest.get("bytecode", []):
            self.assertTrue((ROOT / entry["path"]).exists(), entry["path"])
        for entry in manifest.get("sskyp", []):
            self.assertTrue((ROOT / entry["path"]).exists(), entry["path"])

    def test_golden_source_sha256_matches_host_compile(self) -> None:
        rows = verify_golden_source_entries()
        self.assertTrue(rows)
        self.assertTrue(all(row["bytecode_match"] for row in rows))
        self.assertTrue(all(row["sskyp_match"] for row in rows))

    def test_golden_prathama_output(self) -> None:
        rows = {row["id"]: row for row in verify_golden_source_entries()}
        source = EXAMPLES / "prathama.ssk"
        program = compile_program(load_program_from_path(source))
        self.assertEqual(SanskriptVM().execute(program), ["7"])
        self.assertTrue(rows["golden-source-prathama"]["output_match"])

    def test_golden_phase6_phase7_output(self) -> None:
        rows = {row["id"]: row for row in verify_golden_source_entries()}
        self.assertTrue(rows["golden-source-phase6_functions"]["bytecode_match"])
        self.assertTrue(rows["golden-source-phase6_functions"]["output_match"])
        self.assertTrue(rows["golden-source-phase7_oop"]["bytecode_match"])
        self.assertTrue(rows["golden-source-phase7_oop"]["output_match"])

    def test_golden_phase10_cli_io_bytecode_only(self) -> None:
        rows = {row["id"]: row for row in verify_golden_source_entries()}
        row = rows["golden-source-phase10_stdlib_cli_io"]
        self.assertTrue(row["bytecode_match"])
        self.assertTrue(row["sskyp_match"])
        self.assertIsNone(row["output_match"])

    def test_golden_bytecode_fixture_executes(self) -> None:
        rows = verify_golden_bytecode_entries()
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["output_match"])

    def test_golden_sskyp_fixture_roundtrips(self) -> None:
        rows = verify_golden_sskyp_entries()
        self.assertTrue(rows[0]["sskyp_match"])
        self.assertTrue(rows[0]["output_match"])
        path = ROOT / "data/testing/golden/sskyp/minimal_emit_halt.sskyp"
        program = program_from_yantra_patha(path.read_text(encoding="utf-8"))
        self.assertEqual(SanskriptVM().execute(program), ["7"])

    def test_golden_hashes_stable_across_repeat_verification(self) -> None:
        payload = verify_golden_hashes_stable()
        self.assertTrue(payload["stable"])
        self.assertEqual(payload["mismatched_categories"], [])
        self.assertGreaterEqual(payload["source_count"], 40)


class Phase25FuzzAndPropertyTests(unittest.TestCase):
    def test_parser_fuzz_has_zero_crashes(self) -> None:
        report = run_parser_fuzz(seed=2505, trials=32)
        self.assertEqual(report.crashes, 0)
        self.assertTrue(report.production_fuzz_claim_rejected)
        self.assertEqual(report.trial_budget_class, "smoke-harness")

    def test_bytecode_verifier_fuzz_rejects_mutations(self) -> None:
        report = run_bytecode_verifier_fuzz(seed=2505, trials=32)
        self.assertEqual(report.crashes, 0)
        self.assertEqual(report.rejected, report.trials)
        self.assertTrue(report.production_fuzz_claim_rejected)

    def test_sskyp_fuzz_has_zero_crashes(self) -> None:
        report = run_sskyp_fuzz(seed=2505, trials=32)
        self.assertEqual(report.crashes, 0)
        self.assertGreater(report.rejected, 0)
        self.assertTrue(report.production_fuzz_claim_rejected)

    def test_default_fuzz_trials_are_smoke_not_production(self) -> None:
        meta = fuzz_non_overclaim_metadata(trials=FUZZ_SMOKE_TRIAL_BUDGET)
        self.assertTrue(meta["production_fuzz_claim_rejected"])
        self.assertFalse(meta["continuous_fuzz_ci"])
        self.assertLess(FUZZ_SMOKE_TRIAL_BUDGET, PRODUCTION_FUZZ_MIN_TRIALS)
        payload = run_parser_fuzz(trials=FUZZ_SMOKE_TRIAL_BUDGET).as_dict()
        self.assertIn("Smoke harness", payload["notes"][0])

    def test_property_numeric_collections_text(self) -> None:
        self.assertEqual(run_property_numeric(trials=32).failures, 0)
        self.assertEqual(run_property_subtract(trials=32).failures, 0)
        self.assertEqual(run_property_multiply(trials=32).failures, 0)
        self.assertEqual(run_property_compare_eq(trials=32).failures, 0)
        self.assertEqual(run_property_collections(trials=32).failures, 0)
        self.assertEqual(run_property_list_get(trials=32).failures, 0)
        self.assertEqual(run_property_map_roundtrip(trials=32).failures, 0)
        self.assertEqual(run_property_text(trials=32).failures, 0)


class Phase25RoundTripAndDifferentialTests(unittest.TestCase):
    def test_bytecode_binary_roundtrip(self) -> None:
        program = BytecodeProgram(
            (Instruction(OpCode.PUSH_INT, 4), Instruction(OpCode.EMIT), Instruction(OpCode.HALT))
        )
        payload = roundtrip_bytecode_serialization(program)
        self.assertTrue(payload["serialize_roundtrip"])
        self.assertTrue(payload["output_match"])

    def test_sskyp_roundtrip(self) -> None:
        program = BytecodeProgram(
            (Instruction(OpCode.PUSH_INT, 9), Instruction(OpCode.EMIT), Instruction(OpCode.HALT))
        )
        payload = roundtrip_sskyp_assembly(program)
        self.assertTrue(payload["sskyp_roundtrip"])
        self.assertTrue(payload["output_match"])

    def test_differential_host_vm_scaffold_matches_conformance(self) -> None:
        payload = differential_host_vm_scaffold()
        self.assertTrue(payload["all_python_match"])
        self.assertFalse(payload["rows"][0]["independent_differential_proof"])

    def test_differential_host_compiler_is_host_replay_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = differential_host_compiler_scaffold(
                (EXAMPLES / "prathama.ssk",),
                artifact_root=Path(tmp),
            )
            self.assertTrue(payload["all_bytecode_match"])
            self.assertFalse(payload["rows"][0]["independent_self_compile"])
            self.assertEqual(payload["rows"][0]["source"], "examples/prathama.ssk")

    def test_differential_scaffolds_are_deterministic(self) -> None:
        payload = differential_scaffolds_deterministic(
            compiler_sources=(EXAMPLES / "prathama.ssk", EXAMPLES / "phase6-functions.ssk"),
        )
        self.assertTrue(payload["deterministic"])
        self.assertEqual(payload["fingerprint"], payload["fingerprint_repeat"])


class Phase25EvidenceMatrixTests(unittest.TestCase):
    def test_coverage_audits_meet_seal_thresholds_when_generated(self) -> None:
        exhaustive = ROOT / "tests" / "test_phase25_exhaustive_coverage.py"
        self.assertTrue(exhaustive.exists(), "run tools/generate_phase25_tests.py first")
        parser_audit = audit_parser_rule_coverage()
        opcode_audit = audit_opcode_coverage()
        self.assertTrue(parser_audit["per_rule_unit_tests"])
        self.assertTrue(opcode_audit["per_opcode_dedicated_unit_tests"])
        self.assertGreaterEqual(opcode_audit["dedicated_test_ratio"], MIN_OPCODE_DEDICATED_TEST_RATIO)
        self.assertGreater(parser_audit["ast_statement_nodes"], 50)
        self.assertGreater(opcode_audit["opcode_enum_count"], 150)
        self.assertTrue(coverage_thresholds_met()["met"])

    def test_evidence_matrix_writes_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = generate_phase25_evidence(
                request=Phase25EvidenceRequest(
                    out_dir=Path(tmp),
                    fuzz_trials=16,
                    property_trials=16,
                )
            )
            self.assertEqual(payload["phase"], 25)
            self.assertGreater(payload["pytest_test_functions_estimated"], 500)
            self.assertTrue(payload["non_overclaim"]["per_opcode_unit_tests"])
            self.assertTrue(payload["non_overclaim"]["per_parser_rule_unit_tests"])
            self.assertTrue(payload["non_overclaim"]["per_lowering_unit_tests"])
            self.assertFalse(payload["non_overclaim"]["production_continuous_fuzz"])
            self.assertTrue((Path(tmp) / "phase25-evidence.json").exists())
            fuzz = payload["fuzz"]["bytecode_verifier"]
            self.assertEqual(fuzz["rejected"], fuzz["trials"])
            self.assertTrue(payload["fuzz_non_overclaim"]["production_fuzz_claim_rejected"])
            self.assertTrue(payload["golden_stability"]["stable"])
            self.assertTrue(payload["differential_determinism"]["deterministic"])
            golden = payload["golden"]["source"]
            self.assertTrue(all(row["bytecode_match"] for row in golden))

    def test_security_checklist_is_honest(self) -> None:
        items = security_review_checklist()
        self.assertTrue(any(item["status"] == "not_met" for item in items))
        self.assertTrue(any(item["status"] == "partial" for item in items))

    def test_coverage_map_written(self) -> None:
        path = write_coverage_map()
        self.assertTrue(path.exists())
        payload = build_coverage_map()
        self.assertEqual(payload["phase"], 25)
        self.assertGreater(payload["vm_opcodes"]["opcode_enum_count"], 150)

    def test_coverage_proof_passed_and_seal_gatekeeper(self) -> None:
        exhaustive = ROOT / "tests" / "test_phase25_exhaustive_coverage.py"
        self.assertTrue(exhaustive.exists())
        with tempfile.TemporaryDirectory() as tmp:
            payload = generate_phase25_evidence(
                request=Phase25EvidenceRequest(out_dir=Path(tmp), fuzz_trials=12, property_trials=12)
            )
            verdict = payload["seal_verdict"]
            proof = payload["coverage_proof"]
            self.assertTrue(proof["passed"], proof.get("failures"))
            self.assertTrue(verdict["coverage_proof_passed"])
            self.assertTrue(verdict["coverage_thresholds_met"])
            self.assertTrue(verdict["exhaustive_suites_ready"])
            self.assertTrue(verdict["harness_ready"])
            self.assertTrue(verdict["seal_ready"], verdict.get("blockers"))
            self.assertTrue(any("independent" in warning.lower() for warning in verdict.get("warnings", [])))

    def test_harness_green_matches_seal_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = generate_phase25_evidence(
                request=Phase25EvidenceRequest(out_dir=Path(tmp), fuzz_trials=12, property_trials=12)
            )
            verdict = payload["seal_verdict"]
            self.assertTrue(verdict["harness_ready"])
            self.assertEqual(verdict["harness_ready"], verdict["harness_green"])
            self.assertTrue(verdict["seal_ready"])

    def test_cli_phase25_evidence_emits_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "phase25.json"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = cli_main(
                    [
                        "phase25-evidence",
                        "--out-dir",
                        str(Path(tmp) / "out"),
                        "--plan-json",
                        str(plan),
                        "--fuzz-trials",
                        "12",
                    ]
                )
            self.assertTrue(plan.exists())
            payload = json.loads(plan.read_text(encoding="utf-8"))
            self.assertEqual(payload["phase"], 25)
            self.assertTrue(payload["coverage_proof"]["passed"])
            self.assertIn('"checklist_truth"', stdout.getvalue())
            self.assertEqual(code, 0 if payload["seal_verdict"]["seal_ready"] else 1)


if __name__ == "__main__":
    unittest.main()
