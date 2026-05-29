"""Phase 27: migration report honesty and auditable port tracking."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sanskript.phase27_migration_report import (  # noqa: E402
    ALLOWED_PORT_STATUSES,
    MIGRATION_REPORT_JSON,
    TEST_MANIFEST_JSON,
    TEST_MANIFEST_SSK,
    audit_fake_ported_claims,
    audit_phase27_checklist_honesty,
    build_migration_report,
    load_test_manifest,
    parse_authored_manifest_surface,
    probe_host_wrapper_surfaces,
    run_manifest_regression_evidence,
    validate_report_schema,
    verify_phase27_full_seal,
    write_migration_report,
)
from sanskript.phase18_vm_runtime import SanskriptPortedVM  # noqa: E402
from sanskript.phase27_ports import (  # noqa: E402
    PORT_MODULES,
    canonical_lexicon_entry_count,
    canonical_manifest_regression_count,
    verify_all_ports,
)


class Phase27MigrationReportTests(unittest.TestCase):
    def test_manifest_json_and_ssk_paths_align(self) -> None:
        manifest = load_test_manifest()
        self.assertEqual(manifest["phase"], 27)
        self.assertTrue((ROOT / manifest["authored_surface"]).exists())
        for row in manifest["regression_sources"]:
            self.assertTrue((ROOT / row["path"]).exists(), msg=row["path"])
        self.assertIn("migration-report", manifest.get("host_only_commands", []))

    def test_manifest_ssk_parses_without_errors(self) -> None:
        surface = parse_authored_manifest_surface(TEST_MANIFEST_SSK)
        self.assertEqual(surface["statement_count"], 0)
        json_paths = [row["path"] for row in load_test_manifest()["regression_sources"]]
        self.assertEqual(surface["regression_paths"], json_paths)

    def test_no_component_marked_ported(self) -> None:
        """Anti-fake seal: fail if any component claims port_status=ported."""
        report = build_migration_report()
        ported = [row["id"] for row in report["components"] if row["port_status"] == "ported"]
        self.assertEqual(ported, [])
        self.assertFalse(report["seal"]["any_ported_claims"])

    def test_no_component_claims_ported_while_host_modules_remain(self) -> None:
        report = build_migration_report()
        for row in report["components"]:
            self.assertIn(row["port_status"], ALLOWED_PORT_STATUSES)
            self.assertNotEqual(row["port_status"], "ported")
            if row["python_module_count"] or row["rust_module_count"]:
                self.assertIn(row["implementation_host"], {"python", "rust", "mixed"})
            self.assertEqual(audit_fake_ported_claims([row]), [])

    def test_truth_baseline_records_host_toolchain(self) -> None:
        report = build_migration_report()
        baseline = report["truth_baseline"]
        self.assertTrue(baseline["compiler_vm_parser_still_host"])
        self.assertFalse(baseline["independent_native_toolchain"])
        self.assertFalse(baseline["phase27_checklist_closed"])
        self.assertEqual(baseline["fake_ported_claim_issues"], [])

    def test_seal_ready_for_honest_tracking_with_explicit_blockers(self) -> None:
        report = build_migration_report()
        seal = report["seal"]
        self.assertTrue(seal["ready_for_honest_tracking"])
        self.assertTrue(seal["full_seal_ready"])
        self.assertEqual(seal["status"], "full_seal")
        self.assertFalse(seal["phase27_complete"])
        self.assertGreater(len(report["port_blockers"]), 5)
        self.assertIn("SanskriptPortedVM", "\n".join(report["port_blockers"]))

    def test_verify_phase27_full_seal_passes(self) -> None:
        self.assertEqual(verify_phase27_full_seal(), [])

    def test_manifest_regression_evidence_all_ok(self) -> None:
        evidence = run_manifest_regression_evidence()
        self.assertTrue(evidence["all_ok"])
        self.assertEqual(evidence["passed"], evidence["count"])
        self.assertGreater(evidence["count"], 0)

    def test_phase27_checklist_only_report_item_checked(self) -> None:
        self.assertEqual(audit_phase27_checklist_honesty(), [])

    def test_probe_host_wrapper_surfaces_honest(self) -> None:
        self.assertEqual(probe_host_wrapper_surfaces(), [])

    def test_gatekeeper_in_migration_report(self) -> None:
        report = build_migration_report()
        self.assertTrue(report["gatekeeper"]["full_seal_ready"])
        self.assertEqual(report["gatekeeper"]["violations"], [])
        self.assertTrue(report["manifest_regression"]["all_ok"])

    def test_validate_report_schema_accepts_honest_report(self) -> None:
        report = build_migration_report()
        self.assertEqual(validate_report_schema(report), [])

    def test_rejects_fake_ported_status(self) -> None:
        report = build_migration_report()
        row = dict(report["components"][0])
        row["port_status"] = "ported"
        row["python_module_count"] = 3
        issues = audit_fake_ported_claims([row])
        self.assertTrue(issues)

    def test_write_migration_report_rejects_ported_tamper(self) -> None:
        report = build_migration_report()
        tampered = dict(report)
        tampered["components"] = [dict(report["components"][0])]
        tampered["components"][0]["port_status"] = "ported"
        with self.assertRaises(ValueError):
            write_migration_report(report=tampered)

    def test_committed_migration_report_json_has_no_ported(self) -> None:
        if not MIGRATION_REPORT_JSON.exists():
            self.skipTest("run migration-report CLI first")
        payload = json.loads(MIGRATION_REPORT_JSON.read_text(encoding="utf-8"))
        self.assertEqual(validate_report_schema(payload), [])
        self.assertFalse(any(row.get("port_status") == "ported" for row in payload["components"]))

    def test_write_migration_report_emits_json_and_markdown(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "migration_report.json"
            md_custom = Path(tmp) / "report.md"
            payload = write_migration_report(json_path, markdown_path=md_custom)
            self.assertTrue(json_path.exists())
            self.assertTrue(md_custom.exists())
            self.assertEqual(payload["phase"], 27)

    def test_cli_migration_report_command(self) -> None:
        import os

        env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
        result = subprocess.run(
            [sys.executable, "-m", "sanskript.cli", "migration-report"],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertTrue(MIGRATION_REPORT_JSON.exists())
        payload = json.loads(MIGRATION_REPORT_JSON.read_text(encoding="utf-8"))
        self.assertTrue(payload["seal"]["ready_for_honest_tracking"])
        self.assertTrue(payload["seal"]["full_seal_ready"])

    def test_cli_migration_seal_command(self) -> None:
        import os

        env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
        result = subprocess.run(
            [sys.executable, "-m", "sanskript.cli", "migration-seal"],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("full_seal_ready", result.stdout)

    def test_three_native_ports_execute_with_conformance(self) -> None:
        audit = verify_all_ports(root=ROOT)
        self.assertTrue(audit["all_ok"], msg=audit)
        self.assertEqual(len(PORT_MODULES), 3)
        self.assertEqual(canonical_manifest_regression_count(), 7)
        self.assertGreater(canonical_lexicon_entry_count(), 1000)

    def test_migration_report_average_port_progress_above_five_percent(self) -> None:
        report = build_migration_report(skip_gatekeeper=True)
        avg = report["truth_baseline"]["average_component_percent_complete"]
        self.assertGreater(avg, 5.0)
        in_progress = [row["id"] for row in report["components"] if row["port_status"] == "in_progress"]
        self.assertIn("grammar_loaders", in_progress)
        self.assertIn("sutra_registry", in_progress)
        self.assertIn("examples_runner", in_progress)
        self.assertEqual(len(report["native_ports"]), 3)
        self.assertTrue(all(row["canonical_execution"] for row in report["native_ports"]))

    def test_ported_vm_facade_not_independent(self) -> None:
        from sanskript.bytecode import BytecodeProgram, Instruction, OpCode

        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        evidence = SanskriptPortedVM().execute(program)
        self.assertFalse(evidence.independent_vm)
        self.assertIn("vm-dispatch:python-host", evidence.host_fallbacks)


if __name__ == "__main__":
    unittest.main()
