"""Phase 27 migration report: honest host-vs-native port tracking.

The report lists remaining Python/Rust implementation files, maps them to
migration components, and records port status without claiming native closure
while the compiler, VM, and parser still run on the host.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPORT_SCHEMA_VERSION = 1
PHASE = 27

ALLOWED_PORT_STATUSES = frozenset({"host_only", "extraction_boundary", "in_progress", "ported"})
# Phase 27 anti-fake seal: never emit or accept port_status=ported while host implements logic.
PHASE27_FORBIDS_PORTED_CLAIMS = True

REPO_ROOT = Path(__file__).resolve().parents[2]

CHECKLIST_PATH = REPO_ROOT / "docs" / "native-sanskript-independence-checklist.md"
PHASE27_ALLOWED_CHECKED_PREFIXES = (
    "Add a report showing which Python/Rust files remain and why.",
)
PHASE18_SECTION_START = "## Phase 18:"
PHASE27_SECTION_START = "## Phase 27:"
PHASE28_SECTION_START = "## Phase 28:"
MODULE_INVENTORY_PATH = REPO_ROOT / "data" / "meta" / "module_inventory.json"
MIGRATION_REPORT_JSON = REPO_ROOT / "data" / "meta" / "migration_report.json"
MIGRATION_REPORT_MD = REPO_ROOT / "docs" / "generated" / "migration-report.md"
TEST_MANIFEST_JSON = REPO_ROOT / "data" / "migration" / "phase27-test-manifest.json"
TEST_MANIFEST_SSK = REPO_ROOT / "examples" / "phase27-migration-test-manifest.ssk"

KNOWN_HOST_DEPENDENCIES: dict[str, str] = {
    "python_compiler": "src/sanskript/compiler.py",
    "python_parser": "src/sanskript/parser.py",
    "python_vm": "src/sanskript/vm.py",
    "python_cli": "src/sanskript/cli.py",
    "python_bytecode": "src/sanskript/bytecode.py",
    "python_ast": "src/sanskript/ast.py",
    "rust_vm_crate": "ssk-vm/Cargo.toml",
}

REQUIRED_TOP_LEVEL_KEYS = frozenset(
    {
        "schema_version",
        "phase",
        "generated_at",
        "truth_baseline",
        "summary",
        "components",
        "remaining_files",
        "known_host_dependencies",
        "test_manifest",
        "staged_port_plan",
        "extraction_boundaries",
        "seal",
        "port_blockers",
        "gatekeeper",
        "manifest_regression",
        "native_ports",
    }
)

REQUIRED_COMPONENT_KEYS = frozenset(
    {
        "id",
        "label",
        "port_status",
        "percent_complete",
        "host_language",
        "why_host_remains",
        "primary_modules",
        "native_artifacts",
        "next_steps",
        "implementation_host",
    }
)


@dataclass(frozen=True)
class ComponentSpec:
    id: str
    label: str
    path_markers: tuple[str, ...]
    native_artifacts: tuple[str, ...] = ()
    extraction_percent: float = 0.0
    port_status: str = "host_only"
    why_host_remains: str = ""
    next_steps: tuple[str, ...] = ()


COMPONENT_SPECS: tuple[ComponentSpec, ...] = (
    ComponentSpec(
        "grammar_loaders",
        "Grammar data loaders",
        (
            "controlled_lexicon",
            "grammar_canon",
            "grammar_register",
            "morphology_lexicon",
            "build_lexicon",
            "grammar.py",
            "lexicon",
        ),
        native_artifacts=("data/controlled_lexicon.json", "data/grammar_canon.json"),
        why_host_remains="JSON loaders and lexicon builders are still Python host tools.",
        next_steps=("Port catalog loaders to Sanskript file I/O + parsing.", "Keep data files; port loader code."),
    ),
    ComponentSpec(
        "sutra_registry",
        "Sutra registry",
        ("ashtadhyayi", "sutra", "register.py", "predicate_audit"),
        native_artifacts=("data/ashtadhyayi_sutras.json",),
        why_host_remains="Sutra tables are data; registry/query code is Python.",
        next_steps=("Express registry queries in rakṣita subset.", "Diff host vs Sanskript registry outputs."),
    ),
    ComponentSpec(
        "sutra_predicate_engine",
        "Sutra predicate engine",
        ("predicate", "paninian", "adhyaya", "derivation_engine", "engines.py"),
        why_host_remains="Paninian predicate evaluation remains in large Python grammar engines.",
        next_steps=("Carve predicate API boundary.", "Port one adhyāya slice with conformance tests."),
    ),
    ComponentSpec(
        "derivational_engines",
        "Derivational engines",
        ("derivation", "tinanta", "subanta", "samasa", "dhatu"),
        why_host_remains="Morphology/derivation engines are Python-only and high-churn.",
        next_steps=("Freeze derivational I/O contract.", "Port smallest derivational path used by examples."),
    ),
    ComponentSpec(
        "morphology_helpers",
        "Morphology helpers",
        ("morphology", "sandhi", "phonology", "accent", "script_normalize", "transliteration"),
        why_host_remains="Surface pipeline helpers run on the Python host.",
        next_steps=("Mirror morphology facade in Sanskript.", "Add host/self morphology diff tests."),
    ),
    ComponentSpec(
        "source_tokenizer",
        "Source tokenizer",
        ("source_pipeline", "tokenizer", "script_normalize"),
        why_host_remains="Tokenization and normalization precede the parser on the host.",
        next_steps=("Extract tokenizer IR.", "Port tokenizer for one example corpus."),
    ),
    ComponentSpec(
        "parser",
        "Parser",
        ("parser.py", "parser_core"),
        why_host_remains="All parsing is implemented in Python.",
        next_steps=("S1 self-parser-lowering (Phase 19 path).", "Bytecode diff tests per example."),
    ),
    ComponentSpec(
        "ast",
        "AST model",
        ("ast.py",),
        why_host_remains="AST nodes are Python dataclasses/types.",
        next_steps=("Define AST schema in Sanskript types.", "Round-trip AST serialization tests."),
    ),
    ComponentSpec(
        "compiler",
        "Compiler",
        ("compiler.py", "ir.py"),
        why_host_remains="Lowering and IR passes are Python-only.",
        next_steps=("Port expression lowering subset.", "Compare host vs self bytecode hashes."),
    ),
    ComponentSpec(
        "bytecode",
        "Bytecode schema",
        ("bytecode.py",),
        native_artifacts=("data/bytecode/schema-v2.json",),
        why_host_remains="Schema is documented in JSON; encoder/validator is Python.",
        next_steps=("Port bytecode writer subset to Sanskript.", "Keep schema JSON as shared contract."),
    ),
    ComponentSpec(
        "vm",
        "VM",
        ("vm.py", "vm_", "phase18_vm_runtime", "ssk-vm"),
        native_artifacts=("examples/phase18-vm-bootstrap.sskbc",),
        extraction_percent=2.0,
        port_status="extraction_boundary",
        why_host_remains="Execution is Python VM + Rust conformance crate; Phase 18 bootstrap is evidence only.",
        next_steps=("Expand Sanskript-authored VM subset.", "Host/self VM output conformance."),
    ),
    ComponentSpec(
        "sskyp",
        ".sskyp assembler/disassembler",
        ("yantra_patha",),
        why_host_remains="Machine-prose encode/decode is Python.",
        next_steps=("Port round-trip for implemented opcode subset."),
    ),
    ComponentSpec(
        "cli",
        "CLI",
        ("cli.py", "__main__.py"),
        why_host_remains="All toolchain commands dispatch through Python argparse.",
        next_steps=("migration-report is host command today.", "Port run/compile subset to native driver."),
    ),
    ComponentSpec(
        "docs_gen",
        "Docs generator",
        ("register_docs", "generate_feature", "generate_module", "generate_independence"),
        why_host_remains="Markdown/JSON generators are Python scripts under tools/.",
        next_steps=("Port inventory generator logic after test runner exists."),
    ),
    ComponentSpec(
        "examples_runner",
        "Examples runner",
        ("test_phase_examples", "phase_examples", "examples/"),
        native_artifacts=("examples/",),
        extraction_percent=3.0,
        port_status="extraction_boundary",
        why_host_remains="Examples are Sanskript source but discovery/execution is pytest + Python CLI.",
        next_steps=("Wire phase27 manifest into native example runner.", "Keep examples as golden sources."),
    ),
    ComponentSpec(
        "test_harness",
        "Test harness",
        ("tests/", "unittest", "pytest"),
        native_artifacts=(
            "data/migration/phase27-test-manifest.json",
            "examples/phase27-migration-test-manifest.ssk",
        ),
        extraction_percent=5.0,
        port_status="extraction_boundary",
        why_host_remains="pytest/unittest remain the gate; manifest is an extraction boundary only.",
        next_steps=("Parse Sanskript manifest surface.", "Native test runner (M15) executing manifest rows."),
    ),
    ComponentSpec(
        "web_playground",
        "Web playground core",
        ("webapp", "web"),
        why_host_remains="Static web export is generated by Python host.",
        next_steps=("Port HTML/JS shell emission to Sanskript web tier."),
    ),
    ComponentSpec(
        "browser_runtime",
        "Browser runtime core",
        ("web", "wasm", "browser"),
        why_host_remains="No Sanskript-authored browser runtime; WASM plans are scaffold-only (Phase 20).",
        next_steps=("Define browser ABI boundary.", "Ship minimal WASM interpreter slice."),
    ),
    ComponentSpec(
        "build_release_scripts",
        "Build/release scripts",
        ("tools/", "scripts/", "phase21_platform", "native_backends", "package_"),
        why_host_remains="Build, inventory, packaging, and release flows are Python scripts.",
        next_steps=("Replace inventory scripts after migration-report is native.", "Document bootstrap-only scripts."),
    ),
)


def repo_root() -> Path:
    return REPO_ROOT


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _load_module_inventory() -> list[dict[str, Any]]:
    if not MODULE_INVENTORY_PATH.exists():
        return []
    payload = json.loads(MODULE_INVENTORY_PATH.read_text(encoding="utf-8"))
    return list(payload.get("modules", []))


def _discover_fallback_modules() -> list[dict[str, Any]]:
    modules: list[dict[str, Any]] = []
    roots = [
        REPO_ROOT / "src" / "sanskript",
        REPO_ROOT / "tools",
        REPO_ROOT / "tests",
        REPO_ROOT / "ssk-vm",
    ]
    for base in roots:
        if not base.exists():
            continue
        pattern = "*.rs" if base.name == "ssk-vm" else "*.py"
        for path in sorted(base.rglob(pattern)):
            if path.name == "__init__.py":
                continue
            language = "rust" if path.suffix == ".rs" else "python"
            modules.append(
                {
                    "path": _rel(path),
                    "language": language,
                    "role": "other",
                    "migration_label": "keep_temporarily",
                    "lines": _line_count(path),
                }
            )
    return modules


def _line_count(path: Path) -> int:
    try:
        with path.open(encoding="utf-8", errors="replace") as handle:
            return sum(1 for _ in handle)
    except OSError:
        return 0


def _module_matches_component(module_path: str, markers: tuple[str, ...]) -> bool:
    lowered = module_path.replace("\\", "/").casefold()
    return any(marker.casefold() in lowered for marker in markers)


def _assign_modules(
    modules: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    assigned: dict[str, list[dict[str, Any]]] = {spec.id: [] for spec in COMPONENT_SPECS}
    seen: set[str] = set()
    for module in modules:
        path = str(module.get("path", ""))
        if not path or path in seen:
            continue
        for spec in COMPONENT_SPECS:
            if _module_matches_component(path, spec.path_markers):
                assigned[spec.id].append(module)
                seen.add(path)
                break
    return assigned


def load_test_manifest() -> dict[str, Any]:
    if not TEST_MANIFEST_JSON.exists():
        raise FileNotFoundError(f"Missing Phase 27 test manifest: {TEST_MANIFEST_JSON}")
    return json.loads(TEST_MANIFEST_JSON.read_text(encoding="utf-8"))


def parse_authored_manifest_surface(path: Path | None = None) -> dict[str, Any]:
    """Parse the Sanskript-authored manifest surface (comments + optional empty program)."""
    target = path or TEST_MANIFEST_SSK
    if not target.exists():
        raise FileNotFoundError(f"Missing Phase 27 authored manifest: {target}")
    text = target.read_text(encoding="utf-8")
    from .parser import parse_program

    program = parse_program(text)
    regression_paths = _manifest_surface_lines_from_text(text)
    return {
        "path": _rel(target),
        "statement_count": len(program.statements),
        "regression_paths": regression_paths,
    }


def _manifest_surface_lines_from_text(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("// parīkṣā:"):
            lines.append(stripped.split(":", 1)[1].strip())
    return lines


def _manifest_surface_lines() -> list[str]:
    if not TEST_MANIFEST_SSK.exists():
        return []
    return _manifest_surface_lines_from_text(TEST_MANIFEST_SSK.read_text(encoding="utf-8"))


def _validate_test_manifest(manifest: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for key in ("schema_version", "phase", "authored_surface", "regression_sources"):
        if key not in manifest:
            issues.append(f"missing manifest key: {key}")
    surface = manifest.get("authored_surface")
    if surface and not (REPO_ROOT / str(surface)).exists():
        issues.append(f"authored_surface missing: {surface}")
    if surface:
        try:
            parse_authored_manifest_surface(REPO_ROOT / str(surface))
        except Exception as exc:
            issues.append(f"authored_surface parse error: {exc}")
    surface_paths = _manifest_surface_lines()
    json_paths = [row["path"] for row in manifest.get("regression_sources", [])]
    if surface_paths and json_paths and surface_paths != json_paths:
        issues.append("ssk manifest paths diverge from JSON regression_sources")
    for row in manifest.get("regression_sources", []):
        rel_path = row.get("path")
        if rel_path and not (REPO_ROOT / rel_path).exists():
            issues.append(f"regression source missing: {rel_path}")
    return issues


def _effective_port_status(spec: ComponentSpec, primary_modules: list[str]) -> str:
    """Never claim ported while host modules still implement component logic."""
    if primary_modules:
        if spec.extraction_percent > 0 and spec.port_status == "extraction_boundary":
            return "extraction_boundary"
        return "host_only"
    if PHASE27_FORBIDS_PORTED_CLAIMS and spec.port_status == "ported":
        return "host_only"
    return spec.port_status


def _component_row(
    spec: ComponentSpec,
    modules: list[dict[str, Any]],
    *,
    port_overrides: dict[str, tuple[str, float]] | None = None,
) -> dict[str, Any]:
    python_modules = [m["path"] for m in modules if m.get("language") == "python"]
    rust_modules = [m["path"] for m in modules if m.get("language") == "rust"]
    if python_modules and rust_modules:
        host_language = "mixed"
    elif rust_modules:
        host_language = "rust"
    else:
        host_language = "python"

    native_artifacts = [
        artifact
        for artifact in spec.native_artifacts
        if (REPO_ROOT / artifact).exists() or artifact.endswith("/")
    ]

    primary_modules = sorted({*python_modules, *rust_modules})
    implementation_host = host_language if primary_modules else "none"
    port_status = _effective_port_status(spec, primary_modules)
    percent_complete = spec.extraction_percent

    override = (port_overrides or {}).get(spec.id)
    if override:
        port_status, percent_complete = override
        from . import phase27_ports as _ports

        spec_port = _ports.port_for_component(spec.id)
        if spec_port is not None:
            native_artifacts = sorted(
                {
                    *native_artifacts,
                    _rel(spec_port.source_path),
                    _rel(spec_port.bytecode_path),
                }
            )

    return {
        "id": spec.id,
        "label": spec.label,
        "port_status": port_status,
        "percent_complete": percent_complete,
        "host_language": host_language,
        "implementation_host": implementation_host,
        "why_host_remains": spec.why_host_remains,
        "primary_modules": primary_modules,
        "python_module_count": len(python_modules),
        "rust_module_count": len(rust_modules),
        "native_artifacts": native_artifacts,
        "next_steps": list(spec.next_steps),
        "inventory_note": (
            "module_inventory migration_label=port_directly is a replacement strategy, "
            "not evidence that logic already runs in native Sanskript."
        ),
    }


def staged_port_plan(components: list[dict[str, Any]]) -> list[dict[str, Any]]:
    order = [spec.id for spec in COMPONENT_SPECS]
    by_id = {row["id"]: row for row in components}
    plan: list[dict[str, Any]] = []
    for index, component_id in enumerate(order, start=1):
        row = by_id[component_id]
        plan.append(
            {
                "stage": index,
                "component_id": component_id,
                "label": row["label"],
                "percent_complete": row["percent_complete"],
                "port_status": row["port_status"],
                "blocked_by": _blocked_by(component_id),
            }
        )
    return plan


def _blocked_by(component_id: str) -> list[str]:
    blockers: dict[str, list[str]] = {
        "compiler": ["parser", "ast", "bytecode"],
        "vm": ["bytecode", "compiler"],
        "cli": ["compiler", "vm"],
        "test_harness": ["cli", "vm"],
        "examples_runner": ["cli", "compiler"],
        "docs_gen": ["test_harness"],
        "build_release_scripts": ["cli", "test_harness"],
        "web_playground": ["vm", "compiler"],
        "browser_runtime": ["vm", "bytecode"],
    }
    return blockers.get(component_id, [])


def audit_fake_ported_claims(components: list[dict[str, Any]]) -> list[str]:
    """Reject labels that claim native port while host modules still implement logic."""
    issues: list[str] = []
    for row in components:
        component_id = row.get("id", "?")
        port_status = row.get("port_status")
        if port_status not in ALLOWED_PORT_STATUSES:
            issues.append(f"{component_id}: unknown port_status {port_status!r}")
        percent = row.get("percent_complete", 0)
        python_count = row.get("python_module_count", 0)
        rust_count = row.get("rust_module_count", 0)
        host_impl = row.get("implementation_host", "python")
        primary_modules = list(row.get("primary_modules") or [])

        if PHASE27_FORBIDS_PORTED_CLAIMS and port_status == "ported":
            issues.append(
                f"{component_id}: port_status=ported forbidden in Phase 27 "
                "(host toolchain still implements logic)"
            )
        if port_status == "ported" and (python_count or rust_count or primary_modules):
            issues.append(
                f"{component_id}: port_status=ported but host modules remain "
                f"(python={python_count}, rust={rust_count}, modules={len(primary_modules)})"
            )
        if port_status == "ported" and any(
            mod.endswith(".py") or mod.endswith(".rs") for mod in primary_modules
        ):
            issues.append(f"{component_id}: port_status=ported but primary_modules lists host code")
        if percent >= 100 and port_status != "ported":
            issues.append(f"{component_id}: percent_complete=100 without port_status=ported")
        if host_impl in {"python", "rust", "mixed"} and port_status == "ported":
            issues.append(f"{component_id}: implementation_host={host_impl} conflicts with ported")
    return issues


def _extract_markdown_section(text: str, start_heading: str, end_heading: str | None) -> str:
    start = text.find(start_heading)
    if start < 0:
        return ""
    start += len(start_heading)
    if end_heading:
        end = text.find(end_heading, start)
        if end < 0:
            return text[start:]
        return text[start:end]
    return text[start:]


def audit_phase27_checklist_honesty(path: Path | None = None) -> list[str]:
    """Fail if Phase 27 marks port items complete while only the report item may be [x]."""
    target = path or CHECKLIST_PATH
    if not target.exists():
        return [f"missing independence checklist: {target}"]
    section = _extract_markdown_section(
        target.read_text(encoding="utf-8"),
        PHASE27_SECTION_START,
        PHASE28_SECTION_START,
    )
    issues: list[str] = []
    for line in section.splitlines():
        if not line.startswith("- [x]"):
            continue
        item = line[5:].strip()
        if any(item.startswith(prefix) for prefix in PHASE27_ALLOWED_CHECKED_PREFIXES):
            continue
        issues.append(f"Phase 27 checklist must not mark complete: {item[:120]}")
    return issues


def audit_phase18_wrapper_honesty_documented(path: Path | None = None) -> list[str]:
    """Require Phase 18 to document host VM facade before checked 'Port … to Sanskript' rows."""
    target = path or CHECKLIST_PATH
    if not target.exists():
        return []
    section = _extract_markdown_section(
        target.read_text(encoding="utf-8"),
        PHASE18_SECTION_START,
        "## Phase 19:",
    )
    issues: list[str] = []
    port_rows = [line for line in section.splitlines() if line.startswith("- [x] Port ")]
    if not port_rows:
        return issues
    lowered = " ".join(section.split()).casefold()
    for needle in ("sanskriptportedvm", "facade", "independent sanskript vm runtime"):
        if needle not in lowered:
            issues.append(
                f"Phase 18 has {len(port_rows)} checked Port rows but lacks honesty note: {needle!r}"
            )
    return issues


def probe_host_wrapper_surfaces() -> list[str]:
    """Runtime probes: wrappers must record non-independence and host fallbacks."""
    import tempfile

    from .bytecode import BytecodeProgram, Instruction, OpCode
    from .phase18_vm_runtime import SanskriptPortedVM
    from .self_hosting import HOST_ENGINE, STAGE_ID, verify_host_vs_self_compile

    issues: list[str] = []
    program = BytecodeProgram(
        (
            Instruction(OpCode.PUSH_INT, 1),
            Instruction(OpCode.EMIT),
            Instruction(OpCode.HALT),
        )
    )
    evidence = SanskriptPortedVM().execute(program)
    if evidence.independent_vm:
        issues.append("SanskriptPortedVM reports independent_vm=True but still wraps host SanskriptVM")
    if evidence.vm_impl != "SanskriptVM":
        issues.append(f"SanskriptPortedVM vm_impl must remain SanskriptVM, got {evidence.vm_impl!r}")
    if "vm-dispatch:python-host" not in evidence.host_fallbacks:
        issues.append("SanskriptPortedVM must list vm-dispatch:python-host in host_fallbacks")
    if "python-host" not in HOST_ENGINE:
        issues.append(f"self_hosting HOST_ENGINE must remain a host engine label, got {HOST_ENGINE!r}")
    if not str(STAGE_ID).startswith("S0"):
        issues.append(f"self_hosting STAGE_ID must remain an S0 host-replay stage, got {STAGE_ID!r}")
    sample = REPO_ROOT / "examples" / "prathama.ssk"
    if sample.exists():
        with tempfile.TemporaryDirectory() as tmp:
            row = verify_host_vs_self_compile(sample, Path(tmp))
        if row.independent_self_compile:
            issues.append("verify_host_vs_self_compile must not claim independent_self_compile=True at S0")
    return issues


def run_manifest_regression_evidence(root: Path | None = None) -> dict[str, Any]:
    """Execute manifest golden sources on the host toolchain (honest regression, not a native port)."""
    from .bytecode import load_bytecode_file
    from .compiler import compile_source
    from .phase27_ports import canonical_manifest_regression_count
    from .vm import SanskriptVM

    base = root or REPO_ROOT
    manifest = load_test_manifest()
    canonical_count = canonical_manifest_regression_count()
    rows: list[dict[str, Any]] = []
    for entry in manifest.get("regression_sources", []):
        rel_path = str(entry.get("path", ""))
        source_path = base / rel_path
        row: dict[str, Any] = {
            "id": entry.get("id", rel_path),
            "path": rel_path,
            "purpose": entry.get("purpose"),
            "ok": False,
            "execution_host": "python",
            "output_line_count": 0,
            "error": None,
        }
        if not source_path.exists():
            row["error"] = "missing file"
            rows.append(row)
            continue
        try:
            if source_path.suffix == ".sskbc":
                program = load_bytecode_file(source_path)
            else:
                program = compile_source(source_path.read_text(encoding="utf-8"))
            output = tuple(SanskriptVM().execute(program))
            row["ok"] = True
            row["output_line_count"] = len(output)
        except Exception as exc:
            row["error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    all_ok = all(item["ok"] for item in rows)
    return {
        "all_ok": all_ok,
        "count": len(rows),
        "passed": sum(1 for item in rows if item["ok"]),
        "canonical_source_count": canonical_count,
        "canonical_count_matches": canonical_count == len(rows),
        "rows": rows,
        "note": (
            "Host pytest/CLI still owns discovery; canonical manifest row count comes from "
            "examples/phase27-port-examples-runner.sskbc."
        ),
    }


def verify_phase27_full_seal(*, root: Path | None = None) -> list[str]:
    """FULL SEAL gatekeeper: no fake ported claims, no silent host wrappers, manifest runs."""
    violations: list[str] = []
    report = build_migration_report(skip_gatekeeper=True)
    violations.extend(validate_report_schema(report))
    seal = report.get("seal", {})
    if not seal.get("ready_for_honest_tracking"):
        violations.append("migration report seal is not ready_for_honest_tracking")
    if seal.get("any_ported_claims"):
        violations.append("migration report lists port_status=ported")
    violations.extend(audit_phase27_checklist_honesty())
    violations.extend(audit_phase18_wrapper_honesty_documented())
    violations.extend(probe_host_wrapper_surfaces())
    from .phase27_ports import verify_all_ports

    port_audit = verify_all_ports(root=root or REPO_ROOT)
    if not port_audit.get("all_ok"):
        for row in port_audit.get("rows", []):
            if not row.get("ok"):
                violations.append(f"native port {row.get('port_id')}: {row.get('issues')}")
    manifest_evidence = run_manifest_regression_evidence(root)
    if not manifest_evidence["all_ok"]:
        for row in manifest_evidence["rows"]:
            if not row["ok"]:
                violations.append(
                    f"manifest regression {row['id']}: {row.get('error', 'failed')}"
                )
    return violations


def phase27_full_seal_payload(*, root: Path | None = None) -> dict[str, Any]:
    manifest_evidence = run_manifest_regression_evidence(root)
    violations = verify_phase27_full_seal(root=root)
    return {
        "phase": PHASE,
        "full_seal_ready": not violations,
        "violations": violations,
        "wrapper_probes_ok": not any("SanskriptPortedVM" in item for item in violations),
        "manifest_regression": manifest_evidence,
    }


def build_port_blockers(
    *,
    components: list[dict[str, Any]],
    python_remaining: list[str],
    rust_remaining: list[str],
    host_deps: dict[str, str],
) -> list[str]:
    blockers: list[str] = [
        f"{len(python_remaining)} Python modules still implement host logic (see remaining_files.python).",
        f"{len(rust_remaining)} Rust modules remain for conformance/reference (see remaining_files.rust).",
        "Phase 27 checklist is open: no compiler/parser/VM/CLI component is natively ported end-to-end.",
        "SanskriptPortedVM (Phase 18) is a host-dispatched facade; independent_vm=False.",
        "module_inventory migration_label=port_directly must not be read as already ported.",
    ]
    for key, path in sorted(host_deps.items()):
        blockers.append(f"known_host_dependency:{key} -> {path}")
    for row in components:
        if row.get("port_status") == "extraction_boundary":
            blockers.append(
                f"extraction_boundary:{row['id']} ({row['percent_complete']}% native; host still runs logic)"
            )
        if row.get("port_status") == "in_progress":
            blockers.append(
                f"in_progress:{row['id']} ({row['percent_complete']}% via Sanskript .sskbc; host modules remain)"
            )
    return blockers


def _canonical_manifest_regression_count() -> int:
    from .phase27_ports import canonical_manifest_regression_count

    return canonical_manifest_regression_count()


def _port_overrides_for_components() -> dict[str, tuple[str, float]]:
    from .phase27_ports import PORT_PERCENT_IN_PROGRESS, port_status_for_component

    overrides: dict[str, tuple[str, float]] = {}
    for spec in COMPONENT_SPECS:
        status, percent = port_status_for_component(spec.id)
        if status == "in_progress":
            overrides[spec.id] = (status, percent)
    if overrides.get("examples_runner", ("", 0))[0] == "in_progress":
        overrides["test_harness"] = ("in_progress", PORT_PERCENT_IN_PROGRESS)
    return overrides


def build_migration_report(*, skip_gatekeeper: bool = False) -> dict[str, Any]:
    from .phase27_ports import build_port_inventory, ensure_port_bytecode_artifacts

    ensure_port_bytecode_artifacts()
    native_ports = build_port_inventory()
    port_overrides = _port_overrides_for_components()

    inventory_modules = _load_module_inventory()
    modules = inventory_modules or _discover_fallback_modules()
    assigned = _assign_modules(modules)

    components = [
        _component_row(spec, assigned[spec.id], port_overrides=port_overrides) for spec in COMPONENT_SPECS
    ]
    python_remaining = sorted(m["path"] for m in modules if m.get("language") == "python")
    rust_remaining = sorted(m["path"] for m in modules if m.get("language") == "rust")

    manifest = load_test_manifest()
    manifest_issues = _validate_test_manifest(manifest)
    fake_port_issues = audit_fake_ported_claims(components)

    host_deps = {
        key: path for key, path in KNOWN_HOST_DEPENDENCIES.items() if (REPO_ROOT / path).exists()
    }

    avg_percent = round(
        sum(row["percent_complete"] for row in components) / max(len(components), 1),
        2,
    )
    port_blockers = build_port_blockers(
        components=components,
        python_remaining=python_remaining,
        rust_remaining=rust_remaining,
        host_deps=host_deps,
    )
    tracking_honest = not manifest_issues and not fake_port_issues
    manifest_regression = run_manifest_regression_evidence()
    gatekeeper_violations: list[str] = []
    if not skip_gatekeeper:
        gatekeeper_violations = verify_phase27_full_seal(root=REPO_ROOT)
    full_seal_ready = tracking_honest and not gatekeeper_violations and manifest_regression["all_ok"]

    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "phase": PHASE,
        "generated_at": utc_now_iso(),
        "truth_baseline": {
            "phase27_checklist_closed": False,
            "compiler_vm_parser_still_host": True,
            "independent_native_toolchain": False,
            "average_component_percent_complete": avg_percent,
            "fake_ported_claim_issues": fake_port_issues,
            "notes": (
                "Percentages track native Sanskript implementation replacement, "
                "not feature completeness of the host toolchain. "
                "port_directly in module_inventory is strategy only, not port completion."
            ),
        },
        "summary": {
            "python_file_count": len(python_remaining),
            "rust_file_count": len(rust_remaining),
            "inventory_source": _rel(MODULE_INVENTORY_PATH) if inventory_modules else "inline-discovery",
            "module_count": len(modules),
            "components_at_zero_percent": sum(1 for row in components if row["percent_complete"] == 0),
            "components_with_extraction_boundary": sum(
                1 for row in components if row["port_status"] == "extraction_boundary"
            ),
            "components_in_progress": sum(1 for row in components if row["port_status"] == "in_progress"),
            "native_port_modules": len(native_ports),
        },
        "components": components,
        "remaining_files": {
            "python": python_remaining,
            "rust": rust_remaining,
        },
        "known_host_dependencies": host_deps,
        "test_manifest": {
            "json": _rel(TEST_MANIFEST_JSON),
            "authored_surface": manifest.get("authored_surface"),
            "regression_source_count": len(manifest.get("regression_sources", [])),
            "regression_source_count_canonical": _canonical_manifest_regression_count(),
            "validation_issues": manifest_issues,
            "valid": not manifest_issues,
        },
        "staged_port_plan": staged_port_plan(components),
        "extraction_boundaries": [
            {
                "id": "phase27-test-manifest",
                "description": (
                    "Sanskript-authored regression manifest lists golden sources; "
                    "execution still uses host pytest/CLI."
                ),
                "artifacts": [
                    _rel(TEST_MANIFEST_JSON),
                    _rel(TEST_MANIFEST_SSK),
                ],
            },
            {
                "id": "migration-report-cli",
                "description": "Host CLI emits machine-readable migration-report JSON.",
                "artifacts": ["src/sanskript/phase27_migration_report.py"],
            },
        ],
        "port_blockers": port_blockers,
        "native_ports": native_ports,
        "manifest_regression": manifest_regression,
        "gatekeeper": {
            "full_seal_ready": full_seal_ready,
            "violations": gatekeeper_violations,
            "wrapper_probes_required": True,
            "checklist_audit_required": True,
        },
        "seal": {
            "ready_for_honest_tracking": tracking_honest,
            "full_seal_ready": full_seal_ready,
            "phase27_complete": False,
            "anti_fake_ported_banned": PHASE27_FORBIDS_PORTED_CLAIMS,
            "any_ported_claims": any(row["port_status"] == "ported" for row in components),
            "status": (
                "full_seal"
                if full_seal_ready
                else ("tracking_ready" if tracking_honest else "blocked")
            ),
            "blocked_reason": None if tracking_honest else "audit_failed",
        },
    }


def validate_report_schema(report: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    missing = REQUIRED_TOP_LEVEL_KEYS - set(report)
    if missing:
        issues.extend(f"missing top-level key: {key}" for key in sorted(missing))
    if report.get("schema_version") != REPORT_SCHEMA_VERSION:
        issues.append("schema_version mismatch")
    if report.get("phase") != PHASE:
        issues.append("phase mismatch")
    baseline = report.get("truth_baseline", {})
    if baseline.get("compiler_vm_parser_still_host") is not True:
        issues.append("truth_baseline must record host compiler/vm/parser")
    issues.extend(audit_fake_ported_claims(list(report.get("components", []))))
    if any(row.get("port_status") == "ported" for row in report.get("components", [])):
        issues.append("components must not use port_status=ported during Phase 27")
    seal = report.get("seal", {})
    if seal.get("phase27_complete") is True:
        issues.append("seal.phase27_complete must remain false until native toolchain ships")
    if seal.get("ready_for_honest_tracking") and seal.get("status") == "blocked":
        issues.append("seal: ready_for_honest_tracking conflicts with blocked status")
    gatekeeper = report.get("gatekeeper")
    if gatekeeper is not None:
        if gatekeeper.get("full_seal_ready") and gatekeeper.get("violations"):
            issues.append("gatekeeper: full_seal_ready conflicts with non-empty violations")
    manifest_regression = report.get("manifest_regression")
    if manifest_regression is not None and manifest_regression.get("all_ok") is False:
        if seal.get("full_seal_ready"):
            issues.append("seal.full_seal_ready requires manifest_regression.all_ok")
    for row in report.get("components", []):
        missing_component = REQUIRED_COMPONENT_KEYS - set(row)
        if missing_component:
            issues.append(f"component {row.get('id')}: missing {sorted(missing_component)}")
        percent = row.get("percent_complete")
        if not isinstance(percent, (int, float)) or percent < 0 or percent > 100:
            issues.append(f"component {row.get('id')}: invalid percent_complete")
        if percent == 100 and row.get("port_status") != "ported":
            issues.append(f"component {row.get('id')}: 100% without ported status")
    return issues


def render_migration_report_markdown(report: dict[str, Any]) -> str:
    summary = report.get("summary", {})
    seal = report.get("seal", {})
    lines = [
        "# Phase 27 Migration Report",
        "",
        f"_Generated at {report.get('generated_at', '')} by `phase27_migration_report`._",
        "",
        f"**Seal status:** `{seal.get('status', 'unknown')}` "
        f"(honest tracking: **{seal.get('ready_for_honest_tracking', False)}**, "
        f"full seal: **{seal.get('full_seal_ready', False)}**).",
        "",
        "## Summary",
        "",
        f"- Python files remaining: **{summary.get('python_file_count', 0)}**",
        f"- Rust files remaining: **{summary.get('rust_file_count', 0)}**",
        f"- Average native replacement: **{report.get('truth_baseline', {}).get('average_component_percent_complete', 0)}%**",
        "",
        "## Port blockers",
        "",
    ]
    for blocker in report.get("port_blockers", []):
        lines.append(f"- {blocker}")
    lines.extend(["", "## Components", "", "| Component | Status | % native | Host impl |", "| --- | --- | ---: | --- |"])
    for row in report.get("components", []):
        lines.append(
            f"| {row.get('label', row.get('id'))} | {row.get('port_status')} | "
            f"{row.get('percent_complete')} | {row.get('implementation_host')} |"
        )
    lines.extend(
        [
            "",
            "## Refresh",
            "",
            "```powershell",
            "$env:PYTHONPATH='src'",
            "python -m sanskript.cli migration-report",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def write_migration_report(
    out_path: Path | None = None,
    *,
    report: dict[str, Any] | None = None,
    markdown_path: Path | None = None,
) -> dict[str, Any]:
    payload = report or build_migration_report()
    issues = validate_report_schema(payload)
    if issues:
        raise ValueError("Invalid migration report: " + "; ".join(issues))
    json_target = out_path or MIGRATION_REPORT_JSON
    json_target.parent.mkdir(parents=True, exist_ok=True)
    json_target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_target = markdown_path or MIGRATION_REPORT_MD
    md_target.parent.mkdir(parents=True, exist_ok=True)
    md_target.write_text(render_migration_report_markdown(payload) + "\n", encoding="utf-8")
    return payload
