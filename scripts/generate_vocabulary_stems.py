#!/usr/bin/env python3
"""Thin wrapper: validate per-pattern corpus or regenerate legacy monolith."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    corpus_script = ROOT / "scripts" / "build_vocabulary_corpus.py"
    if (ROOT / "data" / "vocabulary" / "nouns").is_dir():
        return subprocess.call([sys.executable, str(corpus_script)])
    legacy = ROOT / "scripts" / "_generate_vocabulary_stems_legacy.py"
    if legacy.exists():
        return subprocess.call([sys.executable, str(legacy)])
    print("Run scripts/migrate_vocabulary_to_corpus.py first.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
