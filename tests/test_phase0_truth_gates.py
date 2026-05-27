"""Tests for Phase 0 generators and truth-gate checkers."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from tools.check_feature_completion import find_incomplete_complete_features, load_matrix  # noqa: E402
from tools.check_no_placeholder_completion import (  # noqa: E402
    catalog_implemented_without_tests,
    opcodes_without_vm_handler,
)
from tools.generate_feature_matrix import build_feature_matrix  # noqa: E402
from tools.generate_module_inventory import build_inventory  # noqa: E402
from tools.phase0_common import (  # noqa: E402
    FEATURE_MATRIX_JSON,
    MODULE_INVENTORY_JSON,
    ast_statement_nodes,
)
from sanskript.bytecode import OpCode  # noqa: E402


def _run_tool(script: str) -> subprocess.CompletedProcess[str]:
    import os

    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    return subprocess.run(
        [sys.executable, str(ROOT / "tools" / script)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


class Phase0GeneratorTests(unittest.TestCase):
    def test_feature_matrix_has_opcodes_and_types(self) -> None:
        matrix = build_feature_matrix()
        ids = {item["id"] for item in matrix["features"]}
        self.assertIn("opcode:push_int", ids)
        self.assertIn("opcode:halt", ids)
        self.assertTrue(any(item["id"].startswith("type:") for item in matrix["features"]))
        self.assertTrue(any(item["id"].startswith("ast:") for item in matrix["features"]))
        self.assertGreater(matrix["feature_count"], len(OpCode))

    def test_ast_statement_nodes_excludes_value_literals(self) -> None:
        nodes = ast_statement_nodes()
        self.assertIn("Assign", nodes)
        self.assertIn("Display", nodes)
        self.assertNotIn("Literal", nodes)

    def test_module_inventory_covers_python_and_rust(self) -> None:
        inventory = build_inventory()
        langs = {item["language"] for item in inventory["modules"]}
        self.assertIn("python", langs)
        self.assertIn("rust", langs)
        self.assertGreater(inventory["python_count"], 50)
        self.assertGreaterEqual(inventory["rust_count"], 4)
        for item in inventory["modules"]:
            self.assertIn(item["migration_label"], {
                "keep_temporarily",
                "port_directly",
                "redesign",
                "remove",
                "replace_with_native_primitive",
            })
            self.assertRegex(item["milestone"], r"^M\d+$")
            self.assertGreaterEqual(item["replaceability_score"], 0)
            self.assertLessEqual(item["replaceability_score"], 100)

    def test_cli_generators_write_artifacts(self) -> None:
        for script in (
            "generate_feature_matrix.py",
            "generate_module_inventory.py",
            "generate_independence_dashboard.py",
        ):
            result = _run_tool(script)
            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertTrue(FEATURE_MATRIX_JSON.exists())
        self.assertTrue(MODULE_INVENTORY_JSON.exists())
        matrix = json.loads(FEATURE_MATRIX_JSON.read_text(encoding="utf-8"))
        self.assertIn("features", matrix)
        self.assertIn("generated_at", matrix)


class Phase0CheckerTests(unittest.TestCase):
    def test_all_opcodes_have_vm_handlers(self) -> None:
        self.assertEqual(opcodes_without_vm_handler(), [])

    def test_catalog_implemented_types_have_test_references(self) -> None:
        self.assertEqual(catalog_implemented_without_tests(), [])

    def test_no_feature_marked_complete_without_artifacts(self) -> None:
        if not FEATURE_MATRIX_JSON.exists():
            build = _run_tool("generate_feature_matrix.py")
            self.assertEqual(build.returncode, 0, msg=build.stderr)
        matrix = load_matrix()
        self.assertEqual(find_incomplete_complete_features(matrix), [])

    def test_check_scripts_exit_zero(self) -> None:
        for script in ("check_feature_completion.py", "check_no_placeholder_completion.py"):
            result = _run_tool(script)
            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
