"""Generate independence progress dashboard markdown."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.phase0_common import (  # noqa: E402
    DASHBOARD_AXES,
    DOCS_GENERATED,
    FEATURE_MATRIX_JSON,
    INDEPENDENCE_DASHBOARD_MD,
    MODULE_INVENTORY_JSON,
    ensure_output_dirs,
    rel,
    utc_now_iso,
    write_markdown,
)

CHECKLIST = ROOT / "docs" / "native-sanskript-independence-checklist.md"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _checklist_phase0_progress() -> dict[str, Any]:
    text = CHECKLIST.read_text(encoding="utf-8")
    phase0 = re.search(
        r"## Phase 0: Truth Gates And Project Inventory\n\n(.*?)\n\n## Phase 1:",
        text,
        re.DOTALL,
    )
    if not phase0:
        return {"done": 0, "total": 0, "percent": 0.0}
    block = phase0.group(1)
    items = re.findall(r"^- \[[ x]\]", block, re.MULTILINE)
    done = sum(1 for item in items if item == "- [x]")
    total = len(items)
    percent = round(100.0 * done / total, 1) if total else 0.0
    return {"done": done, "total": total, "percent": percent}


def _axis_from_matrix(matrix: dict[str, Any]) -> dict[str, float]:
    features = matrix.get("features", [])
    if not features:
        return {axis: 0.0 for axis in DASHBOARD_AXES}

    def pct(predicate) -> float:
        matched = sum(1 for f in features if predicate(f))
        return round(100.0 * matched / len(features), 1)

    return {
        "authoring": pct(lambda f: f.get("category") == "source_construct" and f.get("status") != "planned"),
        "compiling": pct(
            lambda f: f.get("compiler_lowering") or f.get("category") == "bytecode_opcode" and f.get("status") != "planned"
        ),
        "execution": pct(lambda f: f.get("vm_handler") or f.get("rust_vm_handler")),
        "testing": pct(lambda f: bool(f.get("tests"))),
        "documentation": pct(lambda f: bool(f.get("docs"))),
        "packaging": 5.0,  # host packaging only until M15
        "deployment": 5.0,  # web export foundation only until M5/M18
    }


def _axis_from_inventory(inventory: dict[str, Any]) -> dict[str, float]:
    modules = inventory.get("modules", [])
    if not modules:
        return {axis: 0.0 for axis in DASHBOARD_AXES}
    avg_replace = inventory.get("average_replaceability_score", 0)
    port_ready = sum(1 for m in modules if m.get("migration_label") == "port_directly")
    return {
        "authoring": round(100.0 * port_ready / len(modules) * 0.3, 1),
        "compiling": round(avg_replace * 0.5, 1),
        "execution": round(avg_replace * 0.6, 1),
        "testing": round(100.0 * sum(1 for m in modules if m.get("role") == "tests") / len(modules), 1),
        "documentation": round(100.0 * sum(1 for m in modules if m.get("role") == "docs") / len(modules) * 5, 1),
        "packaging": 8.0,
        "deployment": 6.0,
    }


def _blend(a: float, b: float) -> float:
    return round((a + b) / 2, 1)


def build_dashboard() -> dict[str, Any]:
    matrix = _load_json(FEATURE_MATRIX_JSON)
    inventory = _load_json(MODULE_INVENTORY_JSON)
    feature_axes = _axis_from_matrix(matrix)
    module_axes = _axis_from_inventory(inventory)
    blended = {axis: _blend(feature_axes[axis], module_axes[axis]) for axis in DASHBOARD_AXES}
    overall = round(sum(blended.values()) / len(DASHBOARD_AXES), 1)
    phase0 = _checklist_phase0_progress()
    return {
        "generated_at": utc_now_iso(),
        "overall_percent": overall,
        "phase0_checklist": phase0,
        "axes": blended,
        "feature_axes": feature_axes,
        "module_axes": module_axes,
        "matrix_summary": matrix.get("status_counts", {}),
        "inventory_summary": {
            "module_count": inventory.get("module_count", 0),
            "average_replaceability_score": inventory.get("average_replaceability_score", 0),
        },
    }


def render_markdown(dashboard: dict[str, Any]) -> str:
    lines = [
        "# Sanskript Independence Dashboard",
        "",
        f"_Generated at {dashboard['generated_at']} by `tools/generate_independence_dashboard.py`._",
        "",
        f"**Overall independence readiness: {dashboard['overall_percent']}%** (blended feature + module signals).",
        "",
        "## Phase 0 checklist",
        "",
        f"- Items complete: **{dashboard['phase0_checklist']['done']} / {dashboard['phase0_checklist']['total']}** "
        f"({dashboard['phase0_checklist']['percent']}%)",
        "",
        "## Progress by axis",
        "",
        "| Axis | % complete |",
        "| --- | ---: |",
    ]
    for axis in DASHBOARD_AXES:
        lines.append(f"| {axis} | {dashboard['axes'][axis]} |")

    lines.extend(
        [
            "",
            "## Feature matrix signals",
            "",
            "| Status | Count |",
            "| --- | ---: |",
        ]
    )
    for status, count in sorted(dashboard.get("matrix_summary", {}).items()):
        lines.append(f"| {status} | {count} |")

    inv = dashboard.get("inventory_summary", {})
    lines.extend(
        [
            "",
            "## Module inventory signals",
            "",
            f"- Modules inventoried: **{inv.get('module_count', 0)}**",
            f"- Average replaceability score: **{inv.get('average_replaceability_score', 0)}** / 100",
            "",
            "## How to refresh",
            "",
            "```powershell",
            "$env:PYTHONPATH='src'",
            "python tools/generate_feature_matrix.py",
            "python tools/generate_module_inventory.py",
            "python tools/generate_independence_dashboard.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    ensure_output_dirs()
    dashboard = build_dashboard()
    write_markdown(INDEPENDENCE_DASHBOARD_MD, render_markdown(dashboard))
    print(f"Wrote {rel(INDEPENDENCE_DASHBOARD_MD)} (overall {dashboard['overall_percent']}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
