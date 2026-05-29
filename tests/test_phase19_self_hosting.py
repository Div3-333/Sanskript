"""Phase 19 self-hosting differential and bootstrap evidence tests."""

from __future__ import annotations

import json
import hashlib
import tempfile
import unittest
from pathlib import Path

from sanskript.bytecode import encode_program
from sanskript.cli import main as cli_main
from sanskript.compiler import compile_program
from sanskript.module_loader import load_program_from_path
from sanskript.self_hosting import verify_host_vs_self_compile, write_bootstrap_seed

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


class Phase19SelfHostingTests(unittest.TestCase):
    def test_verify_host_vs_self_compile_matches_on_known_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp) / "artifacts"
            for source in (EXAMPLES / "phase3-data-types.ssk",):
                with self.subTest(source=source.name):
                    evidence = verify_host_vs_self_compile(source, artifact_dir)
                    self.assertEqual(evidence.stage, "S0-host-replay")
                    self.assertEqual(
                        evidence.proof_method,
                        "sha256-canonical-bytecode-and-sskyp",
                    )
                    self.assertFalse(evidence.independent_self_compile)
                    self.assertTrue(evidence.bytecode_match)
                    self.assertTrue(evidence.sskyp_match)
                    self.assertTrue(evidence.host_repeat_match)
                    self.assertTrue(evidence.self_repeat_match)

    def test_seed_records_porting_path_repro_steps_and_equivalence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            seed_path = temp_root / "bootstrap seed" / "phase19" / "bootstrap_seed.json"
            artifact_dir = temp_root / "artifacts phase19" / "run output"
            sources = [EXAMPLES / "phase3-data-types.ssk"]
            payload = write_bootstrap_seed(seed_path, sources, artifact_dir)
            self.assertEqual(payload["phase"], 19)
            self.assertEqual(payload["porting_path"]["current_stage"], "S0-host-replay")
            self.assertFalse(payload["porting_path"]["independent_self_hosting"])
            self.assertEqual(payload["determinism_contract"]["claim_level"], "host-replay-only")
            self.assertFalse(payload["determinism_contract"]["independent_self_hosting"])
            self.assertGreaterEqual(len(payload["determinism_contract"]["independence_blockers"]), 2)
            self.assertGreaterEqual(len(payload["porting_path"]["stages"]), 3)
            self.assertIn("python -m sanskript.cli self-host-check", payload["reproducible_steps"][1])
            self.assertIn("--allow-host-replay", payload["reproducible_steps"][1])
            self.assertIn(json.dumps(str(artifact_dir), ensure_ascii=False), payload["reproducible_steps"][1])
            self.assertIn(json.dumps(str(seed_path), ensure_ascii=False), payload["reproducible_steps"][1])
            self.assertEqual(payload["evidence"][0]["source"], str(sources[0]))
            self.assertIsNotNone(payload["evidence"][0]["source_sha256"])
            self.assertTrue(payload["equivalence_proof"]["all_match"])
            self.assertEqual(payload["equivalence_proof"]["sources_verified"], len(sources))
            self.assertEqual(payload["equivalence_proof"]["mismatch_count"], 0)
            self.assertEqual(payload["equivalence_proof"]["mismatches"], [])
            self.assertTrue(payload["equivalence_proof"]["overall_equivalence_sha256"])
            on_disk = json.loads(seed_path.read_text(encoding="utf-8"))
            self.assertEqual(on_disk["equivalence_proof"], payload["equivalence_proof"])

    def test_seed_proof_is_stable_under_source_ordering(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            artifact_dir = temp_root / "artifacts" / "phase19"
            src_a = EXAMPLES / "phase3-data-types.ssk"
            src_b = EXAMPLES / "phase6-functions.ssk"
            seed_a = temp_root / "a.json"
            seed_b = temp_root / "b.json"
            payload_a = write_bootstrap_seed(seed_a, [src_a, src_b], artifact_dir)
            payload_b = write_bootstrap_seed(seed_b, [src_b, src_a], artifact_dir)
            self.assertEqual(payload_a["sources"], payload_b["sources"])
            self.assertEqual(
                payload_a["equivalence_proof"]["overall_equivalence_sha256"],
                payload_b["equivalence_proof"]["overall_equivalence_sha256"],
            )

    def test_cli_blocks_nonindependent_overclaim_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = EXAMPLES / "phase3-data-types.ssk"
            code = cli_main(
                [
                    "self-host-check",
                    str(source),
                    "--artifact-dir",
                    str(root / "artifacts"),
                    "--seed",
                    str(root / "bootstrap_seed.json"),
                ]
            )
            self.assertEqual(code, 2)

    def test_cli_allows_explicit_host_replay_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = EXAMPLES / "phase3-data-types.ssk"
            code = cli_main(
                [
                    "self-host-check",
                    str(source),
                    "--artifact-dir",
                    str(root / "artifacts"),
                    "--seed",
                    str(root / "bootstrap_seed.json"),
                    "--allow-host-replay",
                ]
            )
            self.assertEqual(code, 0)

    def test_equivalence_hash_matches_direct_host_compile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = EXAMPLES / "phase3-data-types.ssk"
            evidence = verify_host_vs_self_compile(source, Path(tmp))
            host_program = compile_program(load_program_from_path(source))
            host_payload = json.dumps(
                encode_program(host_program),
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
            expected_hash = hashlib.sha256(host_payload).hexdigest()
            self.assertEqual(evidence.host_bytecode_sha256, expected_hash)

if __name__ == "__main__":
    unittest.main()
