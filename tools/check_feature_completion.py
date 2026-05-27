"""Fail CI when a feature is marked complete without required artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.phase0_common import COMPLETE_STATUSES, FEATURE_MATRIX_JSON, rel  # noqa: E402

REQUIRED_FOR_COMPLETE = ("docs", "tests", "examples")


def load_matrix(path: Path | None = None) -> dict:
    matrix_path = path or FEATURE_MATRIX_JSON
    if not matrix_path.exists():
        raise FileNotFoundError(
            f"Missing {rel(matrix_path)} — run tools/generate_feature_matrix.py first."
        )
    return json.loads(matrix_path.read_text(encoding="utf-8"))


def find_incomplete_complete_features(matrix: dict) -> list[str]:
    violations: list[str] = []
    for item in matrix.get("features", []):
        if item.get("status") not in COMPLETE_STATUSES:
            continue
        missing = [field for field in REQUIRED_FOR_COMPLETE if not item.get(field)]
        if item["category"] == "bytecode_opcode" and not item.get("vm_handler"):
            missing.append("vm_handler")
        if item["category"] == "source_construct" and not item.get("compiler_lowering"):
            missing.append("compiler_lowering")
        if missing:
            violations.append(f"{item['id']}: marked complete but missing {', '.join(missing)}")
    return violations


def main() -> int:
    matrix = load_matrix()
    violations = find_incomplete_complete_features(matrix)
    print("Feature completion gate")
    print(f"Features: {matrix.get('feature_count', 0)}")
    if violations:
        print(f"BLOCKED: {len(violations)} feature(s) marked complete without required artifacts:")
        for line in violations:
            print(f"  - {line}")
        return 1
    print("OK: no feature is marked complete without docs, tests, examples, and handlers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
