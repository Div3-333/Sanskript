"""Emit Phase 25 test-matrix evidence JSON (host toolchain)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from sanskript.phase25_testing_verification import (  # noqa: E402
    Phase25EvidenceRequest,
    generate_phase25_evidence,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Phase 25 testing evidence matrix")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "artifacts" / "phase25" / "evidence",
    )
    parser.add_argument(
        "--plan-json",
        type=Path,
        default=ROOT / "artifacts" / "phase25" / "evidence" / "phase25-evidence.json",
    )
    parser.add_argument("--fuzz-trials", type=int, default=48)
    parser.add_argument("--property-trials", type=int, default=64)
    parser.add_argument("--fuzz-seed", type=int, default=2505)
    args = parser.parse_args(argv)

    payload = generate_phase25_evidence(
        request=Phase25EvidenceRequest(
            out_dir=args.out_dir,
            fuzz_trials=args.fuzz_trials,
            property_trials=args.property_trials,
            fuzz_seed=args.fuzz_seed,
        )
    )
    args.plan_json.parent.mkdir(parents=True, exist_ok=True)
    args.plan_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print(args.plan_json)
    seal = payload.get("seal_verdict", {})
    return 0 if seal.get("seal_ready") else 1


if __name__ == "__main__":
    raise SystemExit(main())
