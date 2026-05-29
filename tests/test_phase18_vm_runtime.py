from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode
from sanskript.cli import main as cli_main
from sanskript.phase18_vm_runtime import (
    SanskriptPortedVM,
    bootstrap_stage_s1,
    bootstrap_stage_s2,
    retirement_readiness_report,
    write_phase18_bootstrap_evidence,
)


def _program_emit_one() -> BytecodeProgram:
    return BytecodeProgram(
        (
            Instruction(OpCode.PUSH_INT, 1),
            Instruction(OpCode.EMIT),
            Instruction(OpCode.HALT),
        )
    )


class Phase18VmRuntimeTests(unittest.TestCase):
    def test_ported_vm_evidence_explicitly_records_host_fallback(self) -> None:
        program = _program_emit_one()
        with tempfile.TemporaryDirectory() as tmp:
            trace = Path(tmp) / "trace.json"
            profile = Path(tmp) / "profile.json"
            snap = Path(tmp) / "snapshot.json"
            evidence = SanskriptPortedVM().execute(
                program,
                trace_path=trace,
                profile_path=profile,
                snapshot_path=snap,
            )
            self.assertEqual(evidence.output, ("1",))
            self.assertEqual(evidence.vm_impl, "SanskriptVM")
            self.assertFalse(evidence.independent_vm)
            self.assertIn("vm-dispatch:python-host", evidence.host_fallbacks)
            self.assertTrue(trace.exists())
            self.assertTrue(profile.exists())
            self.assertTrue(snap.exists())

    def test_bootstrap_stages_do_not_claim_independent_differential_proof(self) -> None:
        program = _program_emit_one()
        s1 = bootstrap_stage_s1(program)
        s2 = bootstrap_stage_s2(program)
        self.assertTrue(s1.output_match)
        self.assertTrue(s2.output_match)
        self.assertFalse(s1.independent_vm)
        self.assertFalse(s2.independent_vm)
        self.assertFalse(s1.differential_proof)
        self.assertFalse(s2.differential_proof)
        self.assertIn("vm-dispatch:python-host", s1.host_fallbacks)
        self.assertIn("vm-dispatch:python-host", s2.host_fallbacks)

    def test_retirement_report_requires_independent_differential_proof(self) -> None:
        report = retirement_readiness_report([_program_emit_one()])
        self.assertFalse(report["retirement_ready"])
        self.assertEqual(len(report["checks"]), 1)
        check = report["checks"][0]
        self.assertTrue(check["s1_match"])
        self.assertTrue(check["s2_match"])
        self.assertFalse(check["independent_vm"])
        self.assertFalse(check["differential_proof"])
        self.assertFalse(check["fallback_free"])
        self.assertIn("SanskriptVM", check["vm_impl"])
        self.assertIn("vm-dispatch:python-host", check["host_fallbacks"])
        self.assertTrue(report["blocked_reasons"])

    def test_retirement_report_rejects_empty_program_corpus(self) -> None:
        report = retirement_readiness_report([])
        self.assertFalse(report["retirement_ready"])
        self.assertEqual(report["checks"], [])
        self.assertTrue(report["blocked_reasons"])
        self.assertIn("non-empty corpus", report["policy"])

    def test_phase18_evidence_payload_never_overclaims_readiness_for_empty_corpus(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = write_phase18_bootstrap_evidence([], Path(tmp))
        self.assertEqual(payload["program_count"], 0)
        self.assertEqual(payload["results"], [])
        self.assertFalse(payload["retirement_report"]["retirement_ready"])
        self.assertTrue(payload["retirement_report"]["blocked_reasons"])
        gates = payload["honesty_gates"]
        self.assertFalse(gates["allow_independence_claim"])
        self.assertIn("empty_corpus=true", gates["unresolved_reasons"])

    def test_phase18_evidence_payload_contains_honesty_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = write_phase18_bootstrap_evidence([_program_emit_one()], Path(tmp))
        gates = payload["honesty_gates"]
        self.assertFalse(gates["allow_independence_claim"])
        self.assertFalse(gates["independent_vm_runtime"])
        self.assertFalse(gates["no_host_fallbacks"])
        self.assertIn("independent_vm_runtime=false", gates["unresolved_reasons"])
        self.assertIn("host_fallbacks_present=true", gates["unresolved_reasons"])
        self.assertGreaterEqual(len(payload["reproducible_steps"]), 3)

    def test_cli_blocks_nonindependent_phase18_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code = cli_main(
                [
                    "phase18-vm-check",
                    str(Path(__file__).resolve().parents[1] / "examples" / "phase18-vm-bootstrap.sskbc"),
                    "--artifact-dir",
                    str(Path(tmp) / "phase18"),
                ]
            )
        self.assertEqual(code, 2)

    def test_cli_allows_explicit_parity_mode_for_phase18(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code = cli_main(
                [
                    "phase18-vm-check",
                    str(Path(__file__).resolve().parents[1] / "examples" / "phase18-vm-bootstrap.sskbc"),
                    "--artifact-dir",
                    str(Path(tmp) / "phase18"),
                    "--allow-host-fallback",
                ]
            )
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
