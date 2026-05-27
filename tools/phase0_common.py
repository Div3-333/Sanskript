"""Shared helpers for Phase 0 truth gates and project inventory."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "sanskript"
DATA_META = ROOT / "data" / "meta"
DOCS_GENERATED = ROOT / "docs" / "generated"

FEATURE_MATRIX_JSON = DATA_META / "feature_matrix.json"
MODULE_INVENTORY_JSON = DATA_META / "module_inventory.json"
FEATURE_MATRIX_MD = DOCS_GENERATED / "feature-matrix.md"
MODULE_INVENTORY_MD = DOCS_GENERATED / "module-inventory.md"
INDEPENDENCE_DASHBOARD_MD = DOCS_GENERATED / "independence-dashboard.md"
CATALOG_PATH = ROOT / "data" / "types" / "catalog.json"

COMPLETE_STATUSES = frozenset({"complete"})
FOUNDATION_STATUSES = frozenset({"foundation", "partial"})

# Milestones M0–M20 from docs/native-sanskript-independence-checklist.md
MILESTONES = tuple(f"M{n}" for n in range(21))

MIGRATION_LABELS = (
    "keep_temporarily",
    "port_directly",
    "redesign",
    "remove",
    "replace_with_native_primitive",
)

MODULE_ROLES = (
    "compiler",
    "runtime",
    "vm",
    "stdlib",
    "tooling",
    "docs",
    "tests",
    "web",
    "grammar_engine",
    "migration",
    "other",
)

DASHBOARD_AXES = (
    "authoring",
    "compiling",
    "execution",
    "testing",
    "documentation",
    "packaging",
    "deployment",
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_output_dirs() -> None:
    DATA_META.mkdir(parents=True, exist_ok=True)
    DOCS_GENERATED.mkdir(parents=True, exist_ok=True)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    ensure_output_dirs()
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_markdown(path: Path, body: str) -> None:
    ensure_output_dirs()
    path.write_text(body, encoding="utf-8")


def discover_python_modules() -> list[Path]:
    roots = [SRC, ROOT / "tools", ROOT / "scripts", ROOT / "tests"]
    modules: list[Path] = []
    for base in roots:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.py")):
            if path.name == "__init__.py" and path.parent.name == "sanskript":
                continue
            modules.append(path)
    return modules


def discover_rust_modules() -> list[Path]:
    rust_root = ROOT / "ssk-vm"
    if not rust_root.exists():
        return []
    return sorted(rust_root.rglob("*.rs"))


def search_repo_tokens(token: str, *, globs: Iterable[str]) -> list[str]:
    """Return relative paths whose text contains token (case-sensitive)."""
    hits: list[str] = []
    pattern = re.compile(re.escape(token))
    for glob in globs:
        for path in ROOT.glob(glob):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if pattern.search(text):
                hits.append(rel(path))
    return sorted(set(hits))


def python_vm_opcodes(vm_source: str) -> set[str]:
    members = re.findall(r"opcode == OpCode\.([A-Z0-9_]+)", vm_source)
    members += re.findall(r"instruction\.opcode == OpCode\.([A-Z0-9_]+)", vm_source)
    return {member.lower() for member in members}


def opcode_enum_members(bytecode_source: str) -> list[tuple[str, str]]:
    """Return (enum_member, opcode_value) pairs from OpCode enum."""
    members: list[tuple[str, str]] = []
    in_enum = False
    for line in bytecode_source.splitlines():
        if line.strip().startswith("class OpCode"):
            in_enum = True
            continue
        if in_enum:
            if not line.strip() or line.startswith(" " * 4) is False and "=" not in line:
                if members and not line.startswith(" "):
                    break
            match = re.match(r"\s+([A-Z_]+)\s*=\s*\"([^\"]+)\"", line)
            if match:
                members.append((match.group(1), match.group(2)))
    return members


def rust_vm_opcodes(vm_source: str) -> set[str]:
    handled: set[str] = set()
    for match in re.finditer(r"OpCode::([A-Za-z]+)\s*=>", vm_source):
        handled.add(_rust_variant_to_snake(match.group(1)))
    return handled


def _rust_variant_to_snake(name: str) -> str:
    parts: list[str] = []
    current = name[0].lower()
    for char in name[1:]:
        if char.isupper():
            parts.append(current)
            current = char.lower()
        else:
            current += char
    parts.append(current)
    return "_".join(parts)


@dataclass(frozen=True)
class ModuleClassification:
    role: str
    milestone: str
    migration_label: str
    replaceability_score: int
    notes: str


def classify_python_module(path: Path) -> ModuleClassification:
    name = path.name
    parts = path.parts
    rel_parts = path.relative_to(ROOT).parts if path.is_relative_to(ROOT) else parts

    if "tests" in rel_parts:
        return ModuleClassification("tests", "M15", "keep_temporarily", 25, "Host test harness until Sanskript test runner (M15).")

    if "tools" in rel_parts or "scripts" in rel_parts:
        label = "remove" if name.startswith("_") or "migrate" in name else "keep_temporarily"
        return ModuleClassification("tooling", "M15", label, 55, "Build/inventory scripts; replace incrementally.")

    role_rules: list[tuple[str, str, str, int, str]] = [
        ("compiler", "M11", "port_directly", 45, "Compiler frontend/backend host implementation."),
        ("vm", "M9", "port_directly", 50, "Bytecode VM host implementation."),
        ("runtime", "M3", "port_directly", 40, "Runtime value model and interpreter."),
        ("web", "M5", "redesign", 35, "Web playground/export; target Sanskript web tier."),
        ("docs", "M26", "port_directly", 60, "Documentation generators."),
        ("grammar_engine", "M11", "redesign", 15, "Paninian grammar engine; large redesign surface."),
        ("migration", "M27", "keep_temporarily", 70, "Migration/catalog support until native types."),
    ]

    name_role_map = {
        "parser.py": "compiler",
        "compiler.py": "compiler",
        "ast.py": "compiler",
        "ir.py": "compiler",
        "grammar.py": "compiler",
        "syntax.py": "compiler",
        "bytecode.py": "vm",
        "vm.py": "vm",
        "yantra_patha.py": "vm",
        "runtime_values.py": "runtime",
        "interpreter.py": "runtime",
        "cli.py": "tooling",
        "webapp.py": "web",
        "type_catalog.py": "migration",
        "register_docs.py": "docs",
        "predicate_audit.py": "tooling",
        "performance.py": "tooling",
    }

    if name in name_role_map:
        role = name_role_map[name]
        for entry in role_rules:
            if entry[0] == role:
                return ModuleClassification(entry[0], entry[1], entry[2], entry[3], entry[4])

    grammar_markers = (
        "morphology",
        "paninian",
        "sutra",
        "adhyaya",
        "sandhi",
        "phonology",
        "tinanta",
        "subanta",
        "derivation",
        "samasa",
        "karaka",
        "avyaya",
        "accent",
        "anga",
        "metarules",
        "transliteration",
        "vocabulary",
    )
    if any(marker in name for marker in grammar_markers):
        return ModuleClassification("grammar_engine", "M11", "redesign", 12, "Paninian/morphology subsystem.")

    if name == "errors.py":
        return ModuleClassification("runtime", "M3", "port_directly", 65, "Shared error types.")

    return ModuleClassification("other", "M19", "port_directly", 30, "Unclassified support module.")


def classify_rust_module(path: Path) -> ModuleClassification:
    name = path.name
    if "tests" in path.parts or name.endswith("_test.rs") or path.parent.name == "tests":
        return ModuleClassification("tests", "M15", "keep_temporarily", 30, "Rust conformance tests.")
    if name == "vm.rs":
        return ModuleClassification("vm", "M9", "port_directly", 48, "Reference Rust VM subset.")
    if name == "bytecode.rs":
        return ModuleClassification("vm", "M10", "port_directly", 50, "Bytecode loader/validator in Rust.")
    if name == "main.rs" or name == "lib.rs":
        return ModuleClassification("tooling", "M4", "keep_temporarily", 55, "Rust CLI entry for conformance.")
    return ModuleClassification("vm", "M9", "port_directly", 40, "Rust VM support.")


def ast_statement_nodes() -> list[str]:
    text = read_text(SRC / "ast.py")
    match = re.search(r"^Statement = Union\[(.*?)\]\s*$", text, re.MULTILINE | re.DOTALL)
    if not match:
        return []
    return sorted(set(re.findall(r"\b([A-Z][A-Za-z0-9]+)\b", match.group(1))))


def feature_status_from_artifacts(
    *,
    has_vm: bool,
    has_compiler: bool,
    has_docs: bool,
    has_tests: bool,
    has_examples: bool,
    declared: str | None = None,
) -> str:
    if declared == "complete":
        return "complete"
    if declared in {"planned", "foundation"}:
        return declared
    if has_vm and has_compiler and has_docs and has_tests and has_examples:
        return "complete"
    if has_vm and has_compiler:
        return "foundation"
    if has_vm or has_compiler:
        return "partial"
    return "planned"
