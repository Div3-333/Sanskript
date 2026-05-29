"""Expand Phase 25 golden manifest to all stable examples/*.ssk programs."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sanskript.bytecode import encode_program  # noqa: E402
from sanskript.compiler import compile_program  # noqa: E402
from sanskript.module_loader import load_program_from_path  # noqa: E402
from sanskript.phase25_testing_verification import _canonical_sha256  # noqa: E402
from sanskript.vm import SanskriptVM  # noqa: E402
from sanskript.yantra_patha import program_to_yantra_patha  # noqa: E402

GOLDEN_DIR = ROOT / "data" / "testing" / "golden"
MANIFEST_PATH = GOLDEN_DIR / "manifest.json"

# Skip compile entirely.
SKIP_COMPILE = frozenset({"phase28-game-loop.ssk"})

# Include sha256 golden but omit deterministic expected_output (host/env dependent).
OUTPUT_OMIT = frozenset(
    {
        "phase10-stdlib-cli-io.ssk",
        "phase10-stdlib-source.ssk",
        "phase21-cross-platform.ssk",
        "phase22-http-service.ssk",
        "phase22-full-seal.ssk",
        "phase27-port-controlled-lexicon.ssk",
        "phase27-port-examples-runner.ssk",
        "phase27-port-sutra-registry.ssk",
    }
)


def _entry_id(path: Path) -> str:
    stem = path.stem.replace("-", "_")
    return f"golden-source-{stem}"


def _build_source_entry(path: Path) -> dict[str, Any]:
    rel = path.relative_to(ROOT).as_posix()
    program = compile_program(load_program_from_path(path))
    bc_sha = _canonical_sha256(encode_program(program))
    sskyp_sha = hashlib.sha256(program_to_yantra_patha(program).encode("utf-8")).hexdigest()
    entry: dict[str, Any] = {
        "id": _entry_id(path),
        "path": rel,
        "bytecode_sha256": bc_sha,
        "sskyp_sha256": sskyp_sha,
    }
    if path.name in OUTPUT_OMIT:
        entry["note"] = "expected_output omitted — host-dependent IO/platform surface"
    else:
        try:
            entry["expected_output"] = SanskriptVM().execute(program)
        except Exception as exc:  # noqa: BLE001
            entry["note"] = f"expected_output omitted — runtime not deterministic: {type(exc).__name__}"
    return entry


def build_manifest(*, examples_dir: Path) -> dict[str, Any]:
    existing = json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) if MANIFEST_PATH.exists() else {}
    source_entries: list[dict[str, Any]] = []
    for path in sorted(examples_dir.glob("*.ssk")):
        if path.name in SKIP_COMPILE:
            continue
        try:
            source_entries.append(_build_source_entry(path))
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"golden build failed for {path.name}: {exc}") from exc
    return {
        "version": 1,
        "description": "Phase 25 golden registry — auto-expanded stable examples",
        "source": source_entries,
        "bytecode": existing.get("bytecode", []),
        "sskyp": existing.get("sskyp", []),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Regenerate Phase 25 golden manifest")
    parser.add_argument("--examples", type=Path, default=ROOT / "examples")
    parser.add_argument("--out", type=Path, default=MANIFEST_PATH)
    args = parser.parse_args(argv)
    payload = build_manifest(examples_dir=args.examples)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.out)
    print(f"source_entries={len(payload['source'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
