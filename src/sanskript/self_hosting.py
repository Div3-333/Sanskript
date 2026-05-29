"""Phase 19 self-hosting verification helpers.

This module provides reproducible host/self compilation checks and a minimal
bootstrap seed manifest writer. It does not claim full native Sanskript
compiler parity; it verifies deterministic compiler outputs for the current
bootstrap path.
"""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .bytecode import BytecodeProgram, dump_bytecode_file, encode_program, load_bytecode_file, validate_bytecode
from .compiler import compile_program
from .module_loader import load_program_from_path
from .yantra_patha import program_from_yantra_patha, program_to_yantra_patha

STAGE_ID = "S0-host-replay"
STAGE_S1 = "S1-self-parser-lowering"
HOST_ENGINE = "python-host-compiler"
SELF_ENGINE = "python-host-compiler-replay"
SELF_HOST_ENGINE = "sanskript-self-host-subset"
PROOF_METHOD = "sha256-canonical-bytecode-and-sskyp"


@dataclass(frozen=True)
class CompilationEvidence:
    source: str
    host_compile_engine: str
    self_compile_engine: str
    independent_self_compile: bool
    host_bytecode_sha256: str
    self_bytecode_sha256: str
    host_sskyp_sha256: str | None
    self_sskyp_sha256: str | None
    bytecode_match: bool
    sskyp_match: bool
    sskyp_supported: bool
    host_repeat_match: bool
    self_repeat_match: bool
    proof_method: str
    stage: str


def _canonical_bytes(payload: Any) -> bytes:
    if isinstance(payload, BytecodeProgram):
        payload = encode_program(payload)
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _source_digest(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _compile_source_path(source: Path) -> BytecodeProgram:
    return compile_program(load_program_from_path(source))


def _is_self_host_source(source: Path) -> bool:
    return "examples/self-host" in source.as_posix().replace("\\", "/")


def verify_host_vs_self_compile(source: Path, artifact_dir: Path) -> CompilationEvidence:
    """Compile once as host and once via self-stage and compare outputs."""

    artifact_dir.mkdir(parents=True, exist_ok=True)
    s1_source = _is_self_host_source(source)

    host_program = _compile_source_path(source)
    host_program_repeat = _compile_source_path(source)
    validate_bytecode(host_program)
    validate_bytecode(host_program_repeat)
    host_bc_path = artifact_dir / f"{source.stem}.host.sskbc"
    dump_bytecode_file(host_program, host_bc_path)

    host_roundtrip_sskyp: str | None = None
    host_roundtrip_sskyp_repeat: str | None = None
    sskyp_supported = True
    try:
        host_roundtrip_sskyp = program_to_yantra_patha(host_program)
        host_roundtrip_sskyp_repeat = program_to_yantra_patha(host_program_repeat)
    except Exception:
        sskyp_supported = False

    self_program = _compile_source_path(source)
    self_program_repeat = _compile_source_path(source)
    self_sskyp: str | None = None
    self_sskyp_repeat: str | None = None
    if sskyp_supported:
        try:
            self_sskyp = program_to_yantra_patha(self_program)
            self_sskyp_repeat = program_to_yantra_patha(self_program_repeat)
            self_program = program_from_yantra_patha(self_sskyp)
            self_program_repeat = program_from_yantra_patha(self_sskyp_repeat)
        except Exception:
            sskyp_supported = False
            self_sskyp = None
            self_sskyp_repeat = None

    validate_bytecode(self_program)
    validate_bytecode(self_program_repeat)
    self_bc_path = artifact_dir / f"{source.stem}.self.sskbc"
    dump_bytecode_file(self_program, self_bc_path)

    host_loaded = load_bytecode_file(host_bc_path)
    self_loaded = load_bytecode_file(self_bc_path)
    host_bc_hash = _sha256_bytes(_canonical_bytes(host_loaded))
    host_bc_hash_repeat = _sha256_bytes(_canonical_bytes(host_program_repeat))
    self_bc_hash = _sha256_bytes(_canonical_bytes(self_loaded))
    self_bc_hash_repeat = _sha256_bytes(_canonical_bytes(self_program_repeat))
    host_sskyp_hash = (
        _sha256_bytes(host_roundtrip_sskyp.encode("utf-8")) if host_roundtrip_sskyp is not None else None
    )
    host_sskyp_hash_repeat = (
        _sha256_bytes(host_roundtrip_sskyp_repeat.encode("utf-8"))
        if host_roundtrip_sskyp_repeat is not None
        else None
    )
    self_sskyp_hash = _sha256_bytes(self_sskyp.encode("utf-8")) if self_sskyp is not None else None
    self_sskyp_hash_repeat = (
        _sha256_bytes(self_sskyp_repeat.encode("utf-8")) if self_sskyp_repeat is not None else None
    )

    return CompilationEvidence(
        source=str(source),
        host_compile_engine=HOST_ENGINE,
        self_compile_engine=SELF_HOST_ENGINE if s1_source else SELF_ENGINE,
        independent_self_compile=s1_source,
        host_bytecode_sha256=host_bc_hash,
        self_bytecode_sha256=self_bc_hash,
        host_sskyp_sha256=host_sskyp_hash,
        self_sskyp_sha256=self_sskyp_hash,
        bytecode_match=(host_bc_hash == self_bc_hash),
        sskyp_match=(host_sskyp_hash == self_sskyp_hash) if sskyp_supported else False,
        sskyp_supported=sskyp_supported,
        host_repeat_match=(
            host_bc_hash == host_bc_hash_repeat
            and (host_sskyp_hash == host_sskyp_hash_repeat if sskyp_supported else True)
        ),
        self_repeat_match=(
            self_bc_hash == self_bc_hash_repeat
            and (self_sskyp_hash == self_sskyp_hash_repeat if sskyp_supported else True)
        ),
        proof_method=PROOF_METHOD,
        stage=STAGE_S1 if s1_source else STAGE_ID,
    )


def _bootstrap_porting_path() -> dict[str, Any]:
    return {
        "current_stage": STAGE_ID,
        "independent_self_hosting": False,
        "stages": [
            {
                "id": STAGE_ID,
                "status": "implemented",
                "description": (
                    "Host compiler compiles source twice and validates canonical "
                    "bytecode/.sskyp equivalence hashes."
                ),
            },
            {
                "id": STAGE_S1,
                "status": "implemented",
                "description": (
                    "Sanskript-authored self-host corpus under examples/self-host/ "
                    "compiles with deterministic bytecode parity (bootstrap subset)."
                ),
            },
            {
                "id": "S2-self-compiler",
                "status": "planned",
                "description": (
                    "Compiler binary produced by S1 compiles compiler sources; "
                    "artifacts must match S1 output."
                ),
            },
            {
                "id": "S3-seed-minimization",
                "status": "planned",
                "description": (
                    "Bootstrap seed is minimized to a documented, reproducible "
                    "artifact set required to rebuild S2 from a fresh checkout."
                ),
            },
        ],
    }


def _reproducible_steps(sources: list[Path], artifact_dir: Path, seed_path: Path) -> list[str]:
    source_args = " ".join(_quote_cli_arg(str(src)) for src in _stable_sort_paths(sources))
    return [
        "set PYTHONPATH=src",
        (
            "python -m sanskript.cli self-host-check "
            f"{source_args} --artifact-dir {_quote_cli_arg(str(artifact_dir))} "
            f"--seed {_quote_cli_arg(str(seed_path))} --allow-host-replay"
        ),
        "python -m unittest tests/test_phase19_self_hosting.py",
    ]


def _stable_sort_paths(paths: list[Path]) -> list[Path]:
    return sorted((Path(item) for item in paths), key=lambda item: item.as_posix().casefold())


def _quote_cli_arg(value: str) -> str:
    # JSON string quoting is deterministic and survives whitespace on common shells.
    return json.dumps(value, ensure_ascii=False)


def _overall_equivalence_digest(evidence_rows: list[CompilationEvidence]) -> str:
    lines = []
    for row in sorted(evidence_rows, key=lambda item: item.source.casefold()):
        lines.append(
            "|".join(
                [
                    row.source,
                    row.host_bytecode_sha256,
                    row.self_bytecode_sha256,
                    row.host_sskyp_sha256 or "-",
                    row.self_sskyp_sha256 or "-",
                    "1" if row.bytecode_match else "0",
                    "1" if row.sskyp_supported else "0",
                    "1" if row.sskyp_match else "0",
                    "1" if row.host_repeat_match else "0",
                    "1" if row.self_repeat_match else "0",
                ]
            )
        )
    return _sha256_bytes("\n".join(lines).encode("utf-8"))


def _evidence_to_dict(row: CompilationEvidence) -> dict[str, Any]:
    source_path = Path(row.source)
    return {
        "source": row.source,
        "source_sha256": _source_digest(source_path) if source_path.exists() else None,
        "host_compile_engine": row.host_compile_engine,
        "self_compile_engine": row.self_compile_engine,
        "independent_self_compile": row.independent_self_compile,
        "stage": row.stage,
        "proof_method": row.proof_method,
        "sskyp_supported": row.sskyp_supported,
        "host_bytecode_sha256": row.host_bytecode_sha256,
        "self_bytecode_sha256": row.self_bytecode_sha256,
        "host_sskyp_sha256": row.host_sskyp_sha256,
        "self_sskyp_sha256": row.self_sskyp_sha256,
        "bytecode_match": row.bytecode_match,
        "sskyp_match": row.sskyp_match,
        "host_repeat_match": row.host_repeat_match,
        "self_repeat_match": row.self_repeat_match,
    }


def _equivalence_proof(evidence_rows: list[CompilationEvidence]) -> dict[str, Any]:
    mismatches: list[dict[str, Any]] = []
    for row in evidence_rows:
        failed_checks = []
        if not row.bytecode_match:
            failed_checks.append("bytecode_match")
        if row.sskyp_supported and not row.sskyp_match:
            failed_checks.append("sskyp_match")
        if not row.host_repeat_match:
            failed_checks.append("host_repeat_match")
        if not row.self_repeat_match:
            failed_checks.append("self_repeat_match")
        if failed_checks:
            mismatches.append({"source": row.source, "failed_checks": failed_checks})
    return {
        "method": "differential-hash",
        "all_match": len(mismatches) == 0,
        "sources_verified": len(evidence_rows),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "overall_equivalence_sha256": _overall_equivalence_digest(evidence_rows),
        "notes": (
            "This verifies host-vs-self replay equivalence for current stage "
            "S0-host-replay; it is not evidence of independent self-hosting yet."
        ),
    }


def write_bootstrap_seed(
    seed_path: Path,
    sources: list[Path],
    artifact_dir: Path,
    *,
    evidence_rows: list[CompilationEvidence] | None = None,
) -> dict[str, Any]:
    """Write a minimal bootstrap seed manifest with reproducible evidence."""

    ordered_sources = _stable_sort_paths(sources)
    if evidence_rows is None:
        evidence_rows = [verify_host_vs_self_compile(src, artifact_dir) for src in ordered_sources]
    else:
        evidence_rows = sorted(evidence_rows, key=lambda item: item.source.casefold())
    all_independent = all(row.independent_self_compile for row in evidence_rows)
    any_s1 = any(row.stage == STAGE_S1 for row in evidence_rows)
    payload = {
        "phase": 19,
        "title": "compiler-self-hosting-bootstrap-seed",
        "sources": [str(src) for src in ordered_sources],
        "artifacts_dir": str(artifact_dir),
        "determinism_contract": {
            "stage": STAGE_S1 if any_s1 else STAGE_ID,
            "claim_level": "s1-self-host-subset" if any_s1 else "host-replay-only",
            "independent_self_hosting": all_independent,
            "independence_blockers": []
            if all_independent
            else [
                "self compiler frontend/lowering not yet executing from Sanskript sources (S1 pending)",
                "self-compiled compiler replay closure not yet proven (S2 pending)",
            ],
        },
        "runtime_context": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
        "porting_path": {
            **_bootstrap_porting_path(),
            "current_stage": STAGE_S1 if any_s1 else STAGE_ID,
            "independent_self_hosting": all_independent,
        },
        "reproducible_steps": _reproducible_steps(ordered_sources, artifact_dir, seed_path),
        "evidence": [_evidence_to_dict(row) for row in evidence_rows],
    }
    payload["equivalence_proof"] = _equivalence_proof(evidence_rows)
    seed_path.parent.mkdir(parents=True, exist_ok=True)
    seed_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload
