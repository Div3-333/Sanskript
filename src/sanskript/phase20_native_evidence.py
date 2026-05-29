from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .bytecode import BytecodeProgram
from .native_backends import (
    ArtifactKind,
    BackendKind,
    TargetTriple,
    build_native_artifacts,
    host_target_triple,
    plan_to_dict,
)


@dataclass(frozen=True)
class Phase20EvidenceRequest:
    out_dir: Path
    attempt_link_host: bool = False


def phase20_default_cross_targets() -> tuple[TargetTriple, ...]:
    return (
        TargetTriple("x86_64", "pc", "windows", "msvc"),
        TargetTriple("x86_64", "unknown", "linux", "gnu"),
        TargetTriple("x86_64", "apple", "darwin", "gnu"),
        TargetTriple("aarch64", "pc", "windows", "msvc"),
        TargetTriple("aarch64", "unknown", "linux", "gnu"),
        TargetTriple("aarch64", "apple", "darwin", "gnu"),
    )


def generate_phase20_evidence(
    program: BytecodeProgram,
    *,
    request: Phase20EvidenceRequest,
) -> dict[str, Any]:
    host = host_target_triple()
    all_targets = [host]
    for target in phase20_default_cross_targets():
        if target.text != host.text:
            all_targets.append(target)

    rows: list[dict[str, Any]] = []
    for target in all_targets:
        rows.extend(_target_rows(program, target, request))

    payload = {
        "phase": 20,
        "host_target": host.text,
        "targets": [target.text for target in all_targets],
        "rows": rows,
    }
    request.out_dir.mkdir(parents=True, exist_ok=True)
    (request.out_dir / "phase20-evidence.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return payload


def _target_rows(
    program: BytecodeProgram,
    target: TargetTriple,
    request: Phase20EvidenceRequest,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    backend_kinds: tuple[BackendKind, ...] = (
        "portable-bytecode",
        "web-wasm-plan",
        "native-object",
    )
    for backend in backend_kinds:
        kinds: tuple[ArtifactKind, ...]
        if backend == "web-wasm-plan":
            kinds = ("executable",)
        else:
            kinds = ("executable", "shared")
        for artifact_kind in kinds:
            out_dir = request.out_dir / target.text / backend / artifact_kind
            attempt_link = (
                request.attempt_link_host
                and backend == "native-object"
                and target.text == host_target_triple().text
            )
            plan = build_native_artifacts(
                program=program,
                out_dir=out_dir,
                target=target,
                backend=backend,
                artifact_kind=artifact_kind,
                attempt_link=attempt_link,
            )
            row = plan_to_dict(plan)
            row["evidence_files_exist"] = {
                "stack_map": Path(row["stack_map_path"]).exists(),
                "debug_symbols": Path(row["debug_symbols_path"]).exists(),
                "symbol_table": Path(row["symbol_table_path"]).exists(),
                "relocations": Path(row["relocations_path"]).exists(),
                "linker_io": Path(row["linker_io_path"]).exists(),
                "linker_stdout": bool(row["linker_stdout_path"])
                and Path(str(row["linker_stdout_path"])).exists(),
                "linker_stderr": bool(row["linker_stderr_path"])
                and Path(str(row["linker_stderr_path"])).exists(),
                "object": bool(row["object_path"]) and Path(str(row["object_path"])).exists(),
                "wasm_plan": bool(row["wasm_plan_path"]) and Path(str(row["wasm_plan_path"])).exists(),
                "bytecode": bool(row["bytecode_path"]) and Path(str(row["bytecode_path"])).exists(),
                "linked_output": bool(row["linked_output_path"])
                and Path(str(row["linked_output_path"])).exists(),
            }
            rows.append(row)
    return rows
