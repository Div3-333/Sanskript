"""Write Phase 25 coverage map JSON (parser / compiler / opcode inventory)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sanskript.phase25_testing_verification import (  # noqa: E402
    COVERAGE_MAP_PATH,
    build_coverage_map,
    write_coverage_map,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Emit Phase 25 coverage map JSON")
    parser.add_argument(
        "--out",
        type=Path,
        default=COVERAGE_MAP_PATH,
        help="output path (default: data/verification/coverage_map.json)",
    )
    args = parser.parse_args(argv)
    path = write_coverage_map(args.out)
    print(json.dumps(build_coverage_map(), ensure_ascii=False, indent=2))
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
