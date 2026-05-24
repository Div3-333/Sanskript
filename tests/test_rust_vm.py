"""Rust ssk-vm must match Python bytecode conformance fixtures."""

from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE_DIR = ROOT / "data" / "bytecode" / "conformance"
SSK_VM_DIR = ROOT / "ssk-vm"


@unittest.skipUnless(shutil.which("cargo"), "cargo not installed")
class RustVmConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run(
            ["cargo", "test", "--quiet"],
            cwd=SSK_VM_DIR,
            check=True,
        )

    def test_each_fixture_via_ssk_vm_binary(self) -> None:
        binary = SSK_VM_DIR / "target" / "debug" / ("ssk-vm.exe" if _is_windows() else "ssk-vm")
        if not binary.exists():
            subprocess.run(["cargo", "build", "--quiet"], cwd=SSK_VM_DIR, check=True)
        for path in sorted(CONFORMANCE_DIR.glob("*.json")):
            with self.subTest(fixture=path.name):
                payload = json.loads(path.read_text(encoding="utf-8"))
                completed = subprocess.run(
                    [str(binary), str(path)],
                    cwd=ROOT,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                expected_lines = payload.get("expected_output", [])
                actual_lines = [line for line in completed.stdout.splitlines() if line.strip()]
                self.assertEqual(actual_lines, expected_lines)


def _is_windows() -> bool:
    import sys

    return sys.platform.startswith("win")


if __name__ == "__main__":
    unittest.main()
