#!/usr/bin/env python3
"""Build the controlled lexicon artifact from grammar-register synthesis intents."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sanskript.morphology_lexicon import build_lexicon_artifact  # noqa: E402


def main() -> int:
    path = build_lexicon_artifact()
    print(f"Wrote controlled lexicon to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
