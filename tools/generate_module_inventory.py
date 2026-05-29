"""Inventory Python and Rust modules with migration metadata."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.phase0_common import (  # noqa: E402
    DOCS_GENERATED,
    MODULE_INVENTORY_JSON,
    MODULE_INVENTORY_MD,
    classify_python_module,
    classify_rust_module,
    discover_python_modules,
    discover_rust_modules,
    ensure_output_dirs,
    rel,
    utc_now_iso,
    write_json,
    write_markdown,
)


def _module_record(path: Path, language: str, classification: Any) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8", errors="replace") as handle:
            line_count = sum(1 for _ in handle)
    except OSError:
        line_count = 0
    return {
        "path": rel(path),
        "language": language,
        "role": classification.role,
        "milestone": classification.milestone,
        "migration_label": classification.migration_label,
        "replaceability_score": classification.replaceability_score,
        "notes": classification.notes,
        "lines": line_count,
    }


def build_inventory() -> dict[str, Any]:
    python_modules = [
        _module_record(path, "python", classify_python_module(path))
        for path in discover_python_modules()
    ]
    rust_modules = [
        _module_record(path, "rust", classify_rust_module(path))
        for path in discover_rust_modules()
    ]
    modules = python_modules + rust_modules

    role_counts: dict[str, int] = {}
    milestone_counts: dict[str, int] = {}
    label_counts: dict[str, int] = {}
    for item in modules:
        role_counts[item["role"]] = role_counts.get(item["role"], 0) + 1
        milestone_counts[item["milestone"]] = milestone_counts.get(item["milestone"], 0) + 1
        label_counts[item["migration_label"]] = label_counts.get(item["migration_label"], 0) + 1

    avg_score = round(sum(m["replaceability_score"] for m in modules) / max(len(modules), 1), 1)

    return {
        "generated_at": utc_now_iso(),
        "generator": rel(Path(__file__)),
        "module_count": len(modules),
        "python_count": len(python_modules),
        "rust_count": len(rust_modules),
        "average_replaceability_score": avg_score,
        "role_counts": role_counts,
        "milestone_counts": milestone_counts,
        "migration_label_counts": label_counts,
        "modules": modules,
    }


def render_markdown(inventory: dict[str, Any]) -> str:
    lines = [
        "# Generated Module Inventory",
        "",
        f"_Generated at {inventory['generated_at']} by `{inventory['generator']}`._",
        "",
        f"**{inventory['module_count']}** modules "
        f"({inventory['python_count']} Python, {inventory['rust_count']} Rust). "
        f"Average replaceability score: **{inventory['average_replaceability_score']}** / 100.",
        "",
        "## By role",
        "",
        "| Role | Modules |",
        "| --- | ---: |",
    ]
    for role, count in sorted(inventory["role_counts"].items()):
        lines.append(f"| {role} | {count} |")

    lines.extend(["", "## By milestone", "", "| Milestone | Modules |", "| --- | ---: |"])
    for milestone, count in sorted(inventory["milestone_counts"].items(), key=lambda x: (int(x[0][1:]), x[0])):
        lines.append(f"| {milestone} | {count} |")

    lines.extend(
        [
            "",
            "## By migration label",
            "",
            "_`port_directly` is a replacement strategy, not evidence that logic already runs in native Sanskript. "
            "See `data/meta/migration_report.json` (Phase 27) for honest port status._",
            "",
            "| Label | Modules |",
            "| --- | ---: |",
        ]
    )
    for label, count in sorted(inventory["migration_label_counts"].items()):
        lines.append(f"| {label} | {count} |")

    lines.extend(
        [
            "",
            "## All modules",
            "",
            "| Path | Lang | Role | Milestone | Migration | Score | Lines |",
            "| --- | --- | --- | --- | --- | ---: | ---: |",
        ]
    )
    for item in sorted(inventory["modules"], key=lambda m: m["path"]):
        lines.append(
            f"| `{item['path']}` | {item['language']} | {item['role']} | {item['milestone']} | "
            f"{item['migration_label']} | {item['replaceability_score']} | {item['lines']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ensure_output_dirs()
    inventory = build_inventory()
    write_json(MODULE_INVENTORY_JSON, inventory)
    write_markdown(MODULE_INVENTORY_MD, render_markdown(inventory))
    print(f"Wrote {rel(MODULE_INVENTORY_JSON)} ({inventory['module_count']} modules)")
    print(f"Wrote {rel(MODULE_INVENTORY_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
