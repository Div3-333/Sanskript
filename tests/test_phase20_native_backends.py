from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode
from sanskript.cli import main
from sanskript.native_backends import build_native_artifacts, host_target_triple
from sanskript.phase20_native_evidence import (
    Phase20EvidenceRequest,
    generate_phase20_evidence,
)


class Phase20NativeBackendEvidenceTests(unittest.TestCase):
    def test_wasm_backend_rejects_shared_library_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "does not support shared artifacts"):
                build_native_artifacts(
                    program=BytecodeProgram((Instruction(OpCode.HALT),)),
                    out_dir=Path(tmp),
                    target=host_target_triple(),
                    backend="web-wasm-plan",
                    artifact_kind="shared",
                )

    def test_evidence_matrix_generates_cross_target_rows_and_files(self) -> None:
        program = BytecodeProgram((Instruction(OpCode.HALT),))
        with tempfile.TemporaryDirectory() as tmp:
            payload = generate_phase20_evidence(
                program,
                request=Phase20EvidenceRequest(out_dir=Path(tmp)),
            )
            self.assertEqual(payload["phase"], 20)
            self.assertGreaterEqual(len(payload["targets"]), 6)
            self.assertTrue(any(row["target"] != payload["host_target"] for row in payload["rows"]))
            self.assertTrue(any(row["backend"] == "native-object" for row in payload["rows"]))
            self.assertTrue(any(row["artifact_kind"] == "shared" for row in payload["rows"]))
            self.assertTrue(all(row["evidence_files_exist"]["stack_map"] for row in payload["rows"]))
            self.assertTrue(all(row["evidence_files_exist"]["debug_symbols"] for row in payload["rows"]))
            native_rows = [row for row in payload["rows"] if row["backend"] == "native-object"]
            self.assertTrue(native_rows)
            self.assertTrue(all(row["implementation_state"] == "scaffold" for row in native_rows))
            self.assertTrue(
                all(
                    row["truth_claims"]["native_link_success_requires_real_object_writer"]
                    for row in native_rows
                )
            )
            self.assertTrue((Path(tmp) / "phase20-evidence.json").exists())

    def test_cli_phase20_evidence_emits_json_and_writes_plan_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "simple.ssk"
            out_dir = Path(tmp) / "artifacts"
            plan_json = Path(tmp) / "phase20.json"
            source.write_text("gaṇakaḥ ekaṃ darśayati.\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "phase20-evidence",
                        str(source),
                        "--out-dir",
                        str(out_dir),
                        "--plan-json",
                        str(plan_json),
                    ]
                )
            self.assertEqual(code, 0)
            self.assertTrue(plan_json.exists())
            payload = json.loads(plan_json.read_text(encoding="utf-8"))
            self.assertEqual(payload["phase"], 20)
            self.assertIn('"rows"', stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
