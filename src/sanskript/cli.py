from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .errors import SanskriptError
from .interpreter import run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sanskript")
    parser.add_argument("source", type=Path, help="Path to a .ssk source file")
    args = parser.parse_args(argv)

    try:
        output = run(args.source.read_text(encoding="utf-8"))
    except SanskriptError as exc:
        print(f"sanskript: {exc}", file=sys.stderr)
        return 1

    for line in output:
        print(line)
    return 0

