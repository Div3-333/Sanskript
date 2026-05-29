"""Phase 28 independence milestone evaluator tests."""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from sanskript.cli import main as cli_main
from sanskript.phase28_milestones import (
    MILESTONE_EVALUATORS,
    MILESTONE_TITLES,
    evaluate_all_milestones,
    evaluate_m0_host_examples,
    evaluate_m1_bytecode_source_parity,
    evaluate_m2_sskyp_roundtrip,
    format_checklist_phase28_markers,
    phase28_honesty_gate_report,
    write_phase28_evidence,
)

ROOT = Path(__file__).resolve().parents[1]


class Phase28IndependenceMilestoneTests(unittest.TestCase):
    def test_all_milestone_ids_registered(self) -> None:
        self.assertEqual(len(MILESTONE_EVALUATORS), 21)
        self.assertEqual(set(MILESTONE_EVALUATORS), set(MILESTONE_TITLES))

    def test_m0_host_examples_compile_and_run(self) -> None:
        evidence = evaluate_m0_host_examples(ROOT)
        self.assertTrue(evidence.passed, evidence.blockers)
        skipped = [row for row in evidence.evidence["rows"] if row.get("skipped")]
        self.assertGreaterEqual(evidence.evidence.get("skipped", 0), 1)
        for row in skipped:
            self.assertIn("skip_reason", row)
        platform_skipped = [row for row in skipped if "platform-gated" in row["skip_reason"]]
        self.assertGreaterEqual(len(platform_skipped), 1)

    def test_m1_bytecode_source_parity_with_honest_exclusions(self) -> None:
        evidence = evaluate_m1_bytecode_source_parity(ROOT)
        self.assertTrue(evidence.passed, evidence.blockers)
        excluded = [row for row in evidence.evidence["rows"] if row.get("excluded")]
        self.assertGreaterEqual(evidence.evidence.get("excluded_artifacts", 0), 1)
        rels = {row["bytecode"] for row in excluded}
        self.assertIn("examples/phase18-vm-bootstrap.sskbc", rels)
        for row in excluded:
            self.assertIn("exclusion_reason", row)

    def test_m2_sskyp_roundtrip_passes_for_example_corpus(self) -> None:
        evidence = evaluate_m2_sskyp_roundtrip(ROOT)
        self.assertTrue(evidence.passed, evidence.blockers)
        self.assertTrue(evidence.claim_allowed)

    def test_full_independence_claim_remains_blocked_by_bootstrap_rows(self) -> None:
        report = evaluate_all_milestones(ROOT)
        gates = phase28_honesty_gate_report(report)
        self.assertFalse(gates["allow_full_independence_claim"])
        self.assertIn("M13=bootstrap_or_scaffold_only", gates["unresolved_reasons"])
        self.assertIn("M14=bootstrap_or_scaffold_only", gates["unresolved_reasons"])
        self.assertIn("M20=bootstrap_or_scaffold_only", gates["unresolved_reasons"])

    def test_m13_m14_self_hosting_bootstrap_does_not_claim_full_independence(self) -> None:
        report = evaluate_all_milestones(ROOT)
        by_id = {row["milestone_id"]: row for row in report["milestones"]}
        self.assertTrue(by_id["M13"]["passed"])
        self.assertTrue(by_id["M14"]["passed"])
        self.assertFalse(by_id["M13"]["claim_allowed"])
        self.assertFalse(by_id["M14"]["claim_allowed"])
        self.assertIn("S1", by_id["M13"]["evidence"].get("stage", ""))
        self.assertIn("claim_boundary", by_id["M13"]["evidence"])
        self.assertIn("claim_boundary", by_id["M14"]["evidence"])

    def test_write_evidence_payload_contains_paths_and_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = write_phase28_evidence(Path(tmp), root=ROOT)
            self.assertEqual(payload["phase"], 28)
            self.assertEqual(payload["milestone_count"], 21)
            self.assertLess(
                len(payload["honesty_gates"]["independence_milestones_proven"]),
                12,
            )
            self.assertFalse(payload["honesty_gates"]["allow_full_independence_claim"])
            self.assertTrue(Path(payload["report_path"]).is_file())
            self.assertTrue(Path(payload["checklist_markers_path"]).is_file())
            on_disk = json.loads(Path(payload["report_path"]).read_text(encoding="utf-8"))
            self.assertEqual(on_disk["passed"], payload["passed"])

    def test_checklist_markers_use_partial_marker_for_bootstrap_rows(self) -> None:
        report = evaluate_all_milestones(ROOT)
        text = format_checklist_phase28_markers(report)
        for mid in ("M13", "M14", "M15", "M19", "M20"):
            self.assertIn(f"- [~] {mid}:", text)
        self.assertIn("full independence allowed: False", text)

    def test_cli_milestone_check_requires_allow_partial_until_independence_is_real(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "phase28"
            code = cli_main(["milestone-check", "--artifact-dir", str(out_dir)])
            self.assertEqual(code, 2)
            report = json.loads((out_dir / "phase28-milestone-evidence.json").read_text(encoding="utf-8"))
            self.assertFalse(report["honesty_gates"]["allow_full_independence_claim"])

    def test_cli_allow_partial_still_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "phase28"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = cli_main(
                    ["milestone-check", "--artifact-dir", str(out_dir), "--allow-partial"]
                )
            self.assertEqual(code, 0)
            self.assertIn("phase28-milestone-evidence.json", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
