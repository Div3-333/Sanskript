"""Reject placeholder completion in language-runtime scope (narrow gate)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from sanskript.bytecode import OpCode  # noqa: E402

from tools.phase0_common import (  # noqa: E402
    CATALOG_PATH,
    FEATURE_MATRIX_JSON,
    python_vm_opcodes,
    read_text,
    rel,
)

SRC = ROOT / "src" / "sanskript"


def _compiler_required_opcodes() -> set[str]:
    """Opcodes the host compiler may emit — must have VM handlers."""
    compiler_source = read_text(SRC / "compiler.py")
    members = set(re.findall(r"OpCode\.([A-Z0-9_]+)", compiler_source))
    required: set[str] = set()
    for member in members:
        try:
            required.add(OpCode[member].value)
        except KeyError:
            continue
    return required


def opcodes_without_vm_handler() -> list[str]:
    vm_source = read_text(SRC / "vm.py")
    handled = python_vm_opcodes(vm_source)
    required = _compiler_required_opcodes()
    missing: list[str] = []
    for opcode in OpCode:
        if opcode.value in required and opcode.value not in handled:
            missing.append(opcode.value)
    return sorted(missing)


def catalog_implemented_without_tests() -> list[str]:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    violations: list[str] = []
    tests_dir = ROOT / "tests"
    test_text = ""
    for path in tests_dir.glob("test_*.py"):
        test_text += path.read_text(encoding="utf-8", errors="replace")
    for entry in catalog.get("types", []):
        if entry.get("implementation") != "implemented":
            continue
        name = entry["name"]
        tag = entry.get("bytecode_tag") or ""
        if name not in test_text and tag not in test_text:
            violations.append(f"{entry['id']} ({name}): catalog says implemented but no test reference")
    return violations


def matrix_complete_without_runtime(matrix_path: Path) -> list[str]:
    if not matrix_path.exists():
        return []
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    issues: list[str] = []
    for item in matrix.get("features", []):
        if item.get("status") != "complete":
            continue
        if item["category"] == "bytecode_opcode" and not item.get("vm_handler"):
            issues.append(f"{item['id']}: complete without VM handler")
        if item["category"] == "type_catalog" and item.get("implementation_catalog") == "implemented":
            if not item.get("tests"):
                issues.append(f"{item['id']}: catalog-implemented type marked complete without tests")
    return issues


def pass_through_vm_handlers() -> list[str]:
    """Detect VM branches that only re-raise or contain TODO/pass placeholders."""
    vm_source = read_text(SRC / "vm.py")
    issues: list[str] = []
    if re.search(r"\bpass\b", vm_source):
        issues.append("vm.py contains bare pass (placeholder body)")
    if "TODO" in vm_source or "NotImplemented" in vm_source:
        issues.append("vm.py contains TODO/NotImplemented placeholder")
    return issues


def main() -> int:
    violations: list[str] = []
    violations.extend(f"opcode {op}: no VM handler in vm.py" for op in opcodes_without_vm_handler())
    violations.extend(catalog_implemented_without_tests())
    violations.extend(matrix_complete_without_runtime(FEATURE_MATRIX_JSON))
    violations.extend(pass_through_vm_handlers())

    print("No-placeholder completion gate (language runtime scope)")
    if violations:
        print(f"BLOCKED: {len(violations)} placeholder or hollow completion issue(s):")
        for line in violations:
            print(f"  - {line}")
        return 1
    print("OK: bytecode opcodes have VM handlers; catalog 'implemented' types have test references.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
