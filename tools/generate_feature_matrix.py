"""Generate the language feature matrix (JSON + markdown)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.phase0_common import (  # noqa: E402
    CATALOG_PATH,
    DOCS_GENERATED,
    FEATURE_MATRIX_JSON,
    FEATURE_MATRIX_MD,
    ast_statement_nodes,
    ensure_output_dirs,
    feature_status_from_artifacts,
    opcode_enum_members,
    python_vm_opcodes,
    read_text,
    rel,
    rust_vm_opcodes,
    search_repo_tokens,
    utc_now_iso,
    write_json,
    write_markdown,
)

SRC = ROOT / "src" / "sanskript"

# Map AST statement nodes to parser entry points (heuristic from parser.py structure).
PARSER_RULES: dict[str, str] = {
    "Assign": "parse_sentence → assignment / nidhāna",
    "Increase": "parse_sentence → vṛddhi",
    "Decrease": "parse_sentence → hrasva",
    "Multiply": "parse_sentence → guṇana",
    "Display": "parse_sentence → darśana",
    "If": "parse_sentence → yadi",
    "While": "parse_sentence → yāvat",
    "FunctionDef": "parse_program → vidhāna",
    "Call": "parse_sentence → āhvāna",
    "Return": "parse_sentence → pratyāgama",
    "TextConcat": "parse_sentence → vākya-saṃyoga",
    "ListInit": "parse_sentence → samūha-ārambha",
    "MapInit": "parse_sentence → kośa-ārambha",
    "RecordInit": "parse_sentence → vastu-ārambha",
    "UnsafeEnter": "parse_sentence → arakṣita-praveśa",
    "UnsafeExit": "parse_sentence → arakṣita-nirgama",
    "HeapAlloc": "parse_sentence → kṣetra-ārambha",
}

COMPILER_LOWERING: dict[str, str] = {
    "Assign": "_lower_instruction → IRStore",
    "Increase": "_lower_instruction → IRIncrease",
    "Display": "_lower_instruction → IREmit",
    "If": "_lower_instruction → IRIf",
    "While": "_lower_instruction → IRWhile",
    "FunctionDef": "compile_program → function table",
    "Call": "_lower_instruction → IRCall",
    "Return": "_lower_instruction → IRReturn",
}

DOC_PATHS = {
    "bytecode": ["docs/bytecode-v2.md", "docs/bytecode-v1.md"],
    "types": ["docs/type-system.md"],
    "source": ["docs/language-design.md", "docs/language-paradigms.md"],
}

SEARCH_GLOBS = ("tests/test_*.py", "examples/*.ssk", "src/sanskript/*.py", "data/bytecode/conformance/*.json")


def _opcode_features() -> list[dict[str, Any]]:
    vm_source = read_text(SRC / "vm.py")
    yantra_source = read_text(SRC / "yantra_patha.py")
    compiler_source = read_text(SRC / "compiler.py")
    handled_py = python_vm_opcodes(vm_source)
    rust_source = ""
    rust_vm_path = ROOT / "ssk-vm" / "src" / "vm.rs"
    if rust_vm_path.exists():
        rust_source = read_text(rust_vm_path)
    handled_rust = rust_vm_opcodes(rust_source) if rust_source else set()

    features: list[dict[str, Any]] = []
    for member, value in opcode_enum_members(read_text(SRC / "bytecode.py")):
        enum_name = f"OpCode.{member}"
        has_vm = value in handled_py
        has_yantra = f"OpCode.{member}" in yantra_source or f'opcode == OpCode.{member}' in yantra_source
        has_compiler = value in compiler_source or enum_name in compiler_source
        tests = search_repo_tokens(value, globs=SEARCH_GLOBS)
        if not tests:
            tests = search_repo_tokens(enum_name, globs=("tests/test_*.py",))
        examples = [p for p in search_repo_tokens(value, globs=("examples/*.ssk",)) if p.startswith("examples/")]
        docs = list(DOC_PATHS["bytecode"])
        if value in {"heap_alloc", "heap_store", "heap_load", "heap_free", "unsafe_enter", "unsafe_exit"}:
            docs.append("docs/language-paradigms.md")

        status = feature_status_from_artifacts(
            has_vm=has_vm,
            has_compiler=has_compiler,
            has_docs=bool(docs),
            has_tests=bool(tests),
            has_examples=bool(examples),
        )
        features.append(
            {
                "id": f"opcode:{value}",
                "feature": value,
                "category": "bytecode_opcode",
                "status": status,
                "owning_file": "src/sanskript/bytecode.py",
                "parser_rule": None,
                "compiler_lowering": "src/sanskript/compiler.py" if has_compiler else None,
                "vm_handler": "src/sanskript/vm.py" if has_vm else None,
                "yantra_patha": "src/sanskript/yantra_patha.py" if has_yantra else None,
                "rust_vm_handler": "ssk-vm/src/vm.rs" if value in handled_rust else None,
                "docs": docs,
                "examples": examples,
                "tests": tests,
            }
        )
    return features


def _ast_features() -> list[dict[str, Any]]:
    features: list[dict[str, Any]] = []
    for node in ast_statement_nodes():
        token = node
        parser_rule = PARSER_RULES.get(node, "parse_sentence / parse_program")
        compiler = COMPILER_LOWERING.get(node, f"compile_statements → IR{node}")
        tests = search_repo_tokens(node, globs=SEARCH_GLOBS)
        examples = search_repo_tokens(node, globs=("examples/*.ssk",))
        has_compiler = (SRC / "compiler.py").exists() and node in read_text(SRC / "compiler.py")
        has_vm = bool(tests)  # source features reach VM through compiler tests
        status = feature_status_from_artifacts(
            has_vm=has_vm,
            has_compiler=has_compiler,
            has_docs=True,
            has_tests=bool(tests),
            has_examples=bool(examples),
        )
        features.append(
            {
                "id": f"ast:{node}",
                "feature": node,
                "category": "source_construct",
                "status": status,
                "owning_file": "src/sanskript/ast.py",
                "parser_rule": parser_rule,
                "compiler_lowering": f"src/sanskript/compiler.py ({compiler})",
                "vm_handler": "src/sanskript/vm.py (via lowered bytecode)",
                "yantra_patha": "src/sanskript/yantra_patha.py",
                "docs": DOC_PATHS["source"],
                "examples": examples,
                "tests": tests,
            }
        )
    return features


def _catalog_type_features() -> list[dict[str, Any]]:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    features: list[dict[str, Any]] = []
    for entry in catalog.get("types", []):
        name = entry["name"]
        impl = entry.get("implementation", "planned")
        tag = entry.get("bytecode_tag")
        tests = search_repo_tokens(name, globs=("tests/test_*.py", "tests/test_type_catalog.py"))
        if tag:
            tests = sorted(set(tests + search_repo_tokens(str(tag), globs=SEARCH_GLOBS)))
        examples = search_repo_tokens(name, globs=("examples/*.ssk",))
        docs = DOC_PATHS["types"]
        has_vm = impl in {"implemented", "partial"} and tag is not None
        status_map = {
            "implemented": "foundation",
            "partial": "partial",
            "planned": "planned",
        }
        status = status_map.get(impl, "planned")
        features.append(
            {
                "id": f"type:{entry['id']}",
                "feature": name,
                "category": "type_catalog",
                "status": status,
                "implementation_catalog": impl,
                "owning_file": "data/types/catalog.json",
                "parser_rule": None,
                "compiler_lowering": None,
                "vm_handler": "src/sanskript/vm.py" if has_vm else None,
                "bytecode_tag": tag,
                "docs": docs,
                "examples": examples,
                "tests": tests,
            }
        )
    return features


def build_feature_matrix() -> dict[str, Any]:
    features = _opcode_features() + _ast_features() + _catalog_type_features()
    status_counts: dict[str, int] = {}
    for item in features:
        status_counts[item["status"]] = status_counts.get(item["status"], 0) + 1
    return {
        "generated_at": utc_now_iso(),
        "generator": rel(Path(__file__)),
        "feature_count": len(features),
        "status_counts": status_counts,
        "features": features,
    }


def render_markdown(matrix: dict[str, Any]) -> str:
    lines = [
        "# Generated Feature Matrix",
        "",
        f"_Generated at {matrix['generated_at']} by `{matrix['generator']}`._",
        "",
        f"Total features: **{matrix['feature_count']}**.",
        "",
        "## Status summary",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for status, count in sorted(matrix["status_counts"].items()):
        lines.append(f"| {status} | {count} |")
    lines.extend(
        [
            "",
            "## Bytecode opcodes",
            "",
            "| Opcode | Status | VM | Compiler | Yantra | Tests | Examples |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in matrix["features"]:
        if item["category"] != "bytecode_opcode":
            continue
        lines.append(
            "| {feature} | {status} | {vm} | {comp} | {yantra} | {tests} | {examples} |".format(
                feature=item["feature"],
                status=item["status"],
                vm="yes" if item.get("vm_handler") else "—",
                comp="yes" if item.get("compiler_lowering") else "—",
                yantra="yes" if item.get("yantra_patha") else "—",
                tests=len(item.get("tests") or []),
                examples=len(item.get("examples") or []),
            )
        )

    lines.extend(
        [
            "",
            "## Source constructs (AST)",
            "",
            "| Construct | Status | Parser | Tests | Examples |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in matrix["features"]:
        if item["category"] != "source_construct":
            continue
        lines.append(
            f"| {item['feature']} | {item['status']} | {item.get('parser_rule', '—')} | "
            f"{len(item.get('tests') or [])} | {len(item.get('examples') or [])} |"
        )

    lines.extend(
        [
            "",
            "## Type catalog entries (implemented / partial)",
            "",
            "| Type | Catalog impl | Status | Tests |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for item in matrix["features"]:
        if item["category"] != "type_catalog":
            continue
        if item.get("implementation_catalog") not in {"implemented", "partial"}:
            continue
        lines.append(
            f"| {item['feature']} | {item.get('implementation_catalog')} | {item['status']} | "
            f"{len(item.get('tests') or [])} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ensure_output_dirs()
    matrix = build_feature_matrix()
    write_json(FEATURE_MATRIX_JSON, matrix)
    write_markdown(FEATURE_MATRIX_MD, render_markdown(matrix))
    print(f"Wrote {rel(FEATURE_MATRIX_JSON)} ({matrix['feature_count']} features)")
    print(f"Wrote {rel(FEATURE_MATRIX_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
