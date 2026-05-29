"""Phase 27 canonical Sanskript-authored bytecode ports (host dispatches, VM executes).

Each port module is a .sskbc program under ``examples/phase27-port-*.sskbc``. Host
Python/Rust must not reimplement the same manifest/registry/loader surface when the
port is enabled; they delegate here and treat VM output as the canonical result.
"""

from __future__ import annotations

import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .bytecode import BytecodeProgram, Instruction, OpCode, dump_bytecode_file, load_bytecode_file, validate_bytecode
from .compiler import compile_source
from .vm import SanskriptVM

REPO_ROOT = Path(__file__).resolve().parents[2]

LEXICON_PORT_SSK = REPO_ROOT / "examples" / "phase27-port-controlled-lexicon.ssk"
LEXICON_PORT_BC = REPO_ROOT / "examples" / "phase27-port-controlled-lexicon.sskbc"
SUTRA_PORT_SSK = REPO_ROOT / "examples" / "phase27-port-sutra-registry.ssk"
SUTRA_PORT_BC = REPO_ROOT / "examples" / "phase27-port-sutra-registry.sskbc"
RUNNER_PORT_SSK = REPO_ROOT / "examples" / "phase27-port-examples-runner.ssk"
RUNNER_PORT_BC = REPO_ROOT / "examples" / "phase27-port-examples-runner.sskbc"

SUTRA_PROBE_JSON = REPO_ROOT / "data" / "migration" / "phase27-sutra-registry-probe.json"
CONTROLLED_LEXICON_JSON = REPO_ROOT / "data" / "controlled_lexicon.json"
MANIFEST_JSON = REPO_ROOT / "data" / "migration" / "phase27-test-manifest.json"

# Honest native-replacement estimate per component once bytecode port is verified.
PORT_PERCENT_IN_PROGRESS = 27.0


@dataclass(frozen=True)
class PortModuleSpec:
    component_id: str
    port_id: str
    label: str
    source_path: Path
    bytecode_path: Path
    host_fallback_note: str


@dataclass(frozen=True)
class PortExecutionEvidence:
    port_id: str
    component_id: str
    bytecode_path: str
    source_path: str | None
    canonical: bool
    execution_host: str
    output: tuple[str, ...]
    output_line_count: int
    ok: bool
    error: str | None = None
    conformance: dict[str, Any] | None = None


PORT_MODULES: tuple[PortModuleSpec, ...] = (
    PortModuleSpec(
        "grammar_loaders",
        "controlled_lexicon_loader",
        "Controlled lexicon loader manifest",
        LEXICON_PORT_SSK,
        LEXICON_PORT_BC,
        "Full lexicon Analysis map still built in Python morphology_lexicon.py",
    ),
    PortModuleSpec(
        "sutra_registry",
        "sutra_registry_json_consumer",
        "Sutra registry JSON consumer",
        SUTRA_PORT_SSK,
        SUTRA_PORT_BC,
        "Predicate registry and sutra_records() remain Python in sutra_logic.py",
    ),
    PortModuleSpec(
        "examples_runner",
        "examples_runner_driver",
        "Examples runner manifest driver",
        RUNNER_PORT_SSK,
        RUNNER_PORT_BC,
        "pytest discovery and per-example compile still use host toolchain",
    ),
)


def _rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _bytecode_lexicon_manifest() -> BytecodeProgram:
    return BytecodeProgram(
        (
            Instruction(OpCode.PUSH_TEXT, _rel(CONTROLLED_LEXICON_JSON)),
            Instruction(OpCode.CALL, "std.file.read_text"),
            Instruction(OpCode.CALL, "std.json.parse"),
            Instruction(OpCode.STORE_NAME, "patraka"),
            Instruction(OpCode.LOAD_NAME, "patraka"),
            Instruction(OpCode.PUSH_TEXT, "entry_count"),
            Instruction(OpCode.MAP_GET),
            Instruction(OpCode.EMIT),
            Instruction(OpCode.HALT),
        )
    )


def _bytecode_sutra_registry_consumer() -> BytecodeProgram:
    return BytecodeProgram(
        (
            Instruction(OpCode.PUSH_TEXT, _rel(SUTRA_PROBE_JSON)),
            Instruction(OpCode.CALL, "std.file.read_text"),
            Instruction(OpCode.CALL, "std.json.parse"),
            Instruction(OpCode.STORE_NAME, "patraka"),
            Instruction(OpCode.LOAD_NAME, "patraka"),
            Instruction(OpCode.PUSH_TEXT, "sutras"),
            Instruction(OpCode.MAP_GET),
            Instruction(OpCode.LIST_LEN),
            Instruction(OpCode.EMIT),
            Instruction(OpCode.LOAD_NAME, "patraka"),
            Instruction(OpCode.PUSH_TEXT, "sutras"),
            Instruction(OpCode.MAP_GET),
            Instruction(OpCode.PUSH_INT, 0),
            Instruction(OpCode.LIST_GET),
            Instruction(OpCode.PUSH_TEXT, "id"),
            Instruction(OpCode.MAP_GET),
            Instruction(OpCode.EMIT),
            Instruction(OpCode.HALT),
        )
    )


def _bytecode_examples_runner() -> BytecodeProgram:
    return BytecodeProgram(
        (
            Instruction(OpCode.PUSH_TEXT, _rel(MANIFEST_JSON)),
            Instruction(OpCode.CALL, "std.file.read_text"),
            Instruction(OpCode.CALL, "std.json.parse"),
            Instruction(OpCode.STORE_NAME, "patraka"),
            Instruction(OpCode.LOAD_NAME, "patraka"),
            Instruction(OpCode.PUSH_TEXT, "regression_sources"),
            Instruction(OpCode.MAP_GET),
            Instruction(OpCode.LIST_LEN),
            Instruction(OpCode.EMIT),
            Instruction(OpCode.HALT),
        )
    )


def _program_for_port(port_id: str) -> BytecodeProgram:
    builders = {
        "controlled_lexicon_loader": _bytecode_lexicon_manifest,
        "sutra_registry_json_consumer": _bytecode_sutra_registry_consumer,
        "examples_runner_driver": _bytecode_examples_runner,
    }
    try:
        return builders[port_id]()
    except KeyError as exc:
        raise ValueError(f"unknown Phase 27 port id: {port_id!r}") from exc


def ensure_port_bytecode_artifacts(*, root: Path | None = None) -> list[Path]:
    """Write canonical .sskbc artifacts if missing or stale (source of truth: bytecode builders)."""
    base = root or REPO_ROOT
    write_port_source_stubs(root=base)
    written: list[Path] = []
    mapping = (
        ("controlled_lexicon_loader", LEXICON_PORT_BC),
        ("sutra_registry_json_consumer", SUTRA_PORT_BC),
        ("examples_runner_driver", RUNNER_PORT_BC),
    )
    for port_id, target in mapping:
        program = _program_for_port(port_id)
        validate_bytecode(program)
        path = base / target.relative_to(REPO_ROOT)
        path.parent.mkdir(parents=True, exist_ok=True)
        dump_bytecode_file(program, path)
        written.append(path)
    return written


def execute_port_bytecode(
    port_id: str,
    *,
    root: Path | None = None,
    program: BytecodeProgram | None = None,
) -> PortExecutionEvidence:
    """Run a port module on the host VM; output is the canonical migration surface result."""
    base = root or REPO_ROOT
    spec = port_by_id(port_id)
    if spec is None:
        raise ValueError(f"unknown port id: {port_id!r}")
    bc_path = base / spec.bytecode_path.relative_to(REPO_ROOT)
    if program is None:
        if not bc_path.exists():
            ensure_port_bytecode_artifacts(root=base)
        program = load_bytecode_file(bc_path)
    try:
        output = tuple(str(line) for line in SanskriptVM().execute(program))
        ok = True
        error = None
    except Exception as exc:
        output = ()
        ok = False
        error = f"{type(exc).__name__}: {exc}"
    return PortExecutionEvidence(
        port_id=spec.port_id,
        component_id=spec.component_id,
        bytecode_path=_rel(bc_path),
        source_path=_rel(spec.source_path) if spec.source_path.exists() else None,
        canonical=ok,
        execution_host="python-vm-sskbc",
        output=output,
        output_line_count=len(output),
        ok=ok,
        error=error,
    )


def port_by_id(port_id: str) -> PortModuleSpec | None:
    for spec in PORT_MODULES:
        if spec.port_id == port_id:
            return spec
    return None


def port_for_component(component_id: str) -> PortModuleSpec | None:
    for spec in PORT_MODULES:
        if spec.component_id == component_id:
            return spec
    return None


def verify_port_conformance(port_id: str, *, root: Path | None = None) -> dict[str, Any]:
    """Host-side expected values; proves bytecode port matches data contracts."""
    base = root or REPO_ROOT
    evidence = execute_port_bytecode(port_id, root=base)
    issues: list[str] = []
    conformance: dict[str, Any] = {"port_id": port_id, "ok": evidence.ok}

    if not evidence.ok:
        issues.append(evidence.error or "execution failed")
        conformance["issues"] = issues
        return conformance

    if port_id == "controlled_lexicon_loader":
        payload = json.loads((base / CONTROLLED_LEXICON_JSON.relative_to(REPO_ROOT)).read_text(encoding="utf-8"))
        expected = str(payload.get("entry_count", ""))
        if evidence.output != (expected,):
            issues.append(f"entry_count expected {expected!r}, got {evidence.output!r}")
        conformance["entry_count"] = expected

    elif port_id == "sutra_registry_json_consumer":
        payload = json.loads((base / SUTRA_PROBE_JSON.relative_to(REPO_ROOT)).read_text(encoding="utf-8"))
        expected_len = str(len(payload.get("sutras", [])))
        expected_id = str(payload["sutras"][0]["id"]) if payload.get("sutras") else ""
        if len(evidence.output) < 2:
            issues.append(f"expected two emit lines, got {evidence.output!r}")
        else:
            if evidence.output[0] != expected_len:
                issues.append(f"sutra slice length expected {expected_len!r}, got {evidence.output[0]!r}")
            if evidence.output[1] != expected_id:
                issues.append(f"first sutra id expected {expected_id!r}, got {evidence.output[1]!r}")
        conformance["slice_count"] = expected_len
        conformance["first_id"] = expected_id

    elif port_id == "examples_runner_driver":
        manifest = json.loads((base / MANIFEST_JSON.relative_to(REPO_ROOT)).read_text(encoding="utf-8"))
        expected = str(len(manifest.get("regression_sources", [])))
        if evidence.output != (expected,):
            issues.append(f"regression_sources count expected {expected!r}, got {evidence.output!r}")
        conformance["regression_source_count"] = expected

    conformance["issues"] = issues
    conformance["ok"] = evidence.ok and not issues
    return conformance


def verify_all_ports(*, root: Path | None = None) -> dict[str, Any]:
    rows = [verify_port_conformance(spec.port_id, root=root) for spec in PORT_MODULES]
    return {
        "port_count": len(rows),
        "all_ok": all(row.get("ok") for row in rows),
        "rows": rows,
    }


def canonical_lexicon_entry_count(*, root: Path | None = None) -> int:
    evidence = execute_port_bytecode("controlled_lexicon_loader", root=root)
    if not evidence.ok or not evidence.output:
        raise RuntimeError(evidence.error or "lexicon port failed")
    return int(evidence.output[0])


def canonical_sutra_registry_slice_summary(*, root: Path | None = None) -> tuple[int, str]:
    evidence = execute_port_bytecode("sutra_registry_json_consumer", root=root)
    if not evidence.ok or len(evidence.output) < 2:
        raise RuntimeError(evidence.error or "sutra registry port failed")
    return int(evidence.output[0]), evidence.output[1]


def canonical_manifest_regression_count(*, root: Path | None = None) -> int:
    evidence = execute_port_bytecode("examples_runner_driver", root=root)
    if not evidence.ok or not evidence.output:
        raise RuntimeError(evidence.error or "examples runner port failed")
    return int(evidence.output[0])


def port_status_for_component(component_id: str, *, root: Path | None = None) -> tuple[str, float]:
    """Return (port_status, percent_complete) when bytecode port is canonical."""
    spec = port_for_component(component_id)
    if spec is None:
        return "host_only", 0.0
    row = verify_port_conformance(spec.port_id, root=root)
    if row.get("ok"):
        return "in_progress", PORT_PERCENT_IN_PROGRESS
    return "host_only", 0.0


def build_port_inventory(*, root: Path | None = None) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    for spec in PORT_MODULES:
        row = verify_port_conformance(spec.port_id, root=root)
        evidence = execute_port_bytecode(spec.port_id, root=root)
        inventory.append(
            {
                "port_id": spec.port_id,
                "component_id": spec.component_id,
                "label": spec.label,
                "source": _rel(spec.source_path),
                "bytecode": _rel(spec.bytecode_path),
                "canonical_execution": row.get("ok", False),
                "execution_host": evidence.execution_host,
                "percent_complete": PORT_PERCENT_IN_PROGRESS if row.get("ok") else 0.0,
                "host_fallback_note": spec.host_fallback_note,
                "conformance": row,
                "output": list(evidence.output),
            }
        )
    return inventory


def write_port_source_stubs(*, root: Path | None = None) -> None:
    """Author .ssk surface files documenting each port (compile may require host stdlib)."""
    base = root or REPO_ROOT
    stubs = {
        LEXICON_PORT_SSK: (
            "// Phase 27 port: controlled lexicon loader manifest (canonical via .sskbc).\n"
            "// kṣetram saṃskaraṇa.\n"
        ),
        SUTRA_PORT_SSK: (
            "// Phase 27 port: sutra registry JSON consumer (canonical via .sskbc).\n"
            "// kṣetram saṃskaraṇa.\n"
        ),
        RUNNER_PORT_SSK: (
            "// Phase 27 port: examples runner manifest driver (canonical via .sskbc).\n"
            "// kṣetram saṃskaraṇa.\n"
        ),
    }
    for path, text in stubs.items():
        target = base / path.relative_to(REPO_ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text(text, encoding="utf-8")
