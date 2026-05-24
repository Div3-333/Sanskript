#!/usr/bin/env python3
"""Validate and report on the per-pattern vocabulary corpus under data/vocabulary/."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sanskript.subanta import StemPattern, valid_lemma_for_pattern  # noqa: E402
from sanskript.vocabulary_catalog import (  # noqa: E402
    VOCABULARY_DIR,
    graduate_noun_stems,
    graduate_verb_dhatus,
    load_corpus_report,
)

COMMON_PATTERNS = frozenset(
    {
        StemPattern.A_MASCULINE,
        StemPattern.A_NEUTER,
        StemPattern.AA_FEMININE,
        StemPattern.I_MASCULINE,
        StemPattern.I_FEMININE,
        StemPattern.II_FEMININE,
        StemPattern.U_MASCULINE,
        StemPattern.R_MASCULINE,
    }
)

TIERED_PATTERNS = frozenset(
    {
        StemPattern.I_NEUTER,
        StemPattern.U_NEUTER,
        StemPattern.UU_FEMININE,
        StemPattern.R_FEMININE,
        StemPattern.RR_FEMININE,
        StemPattern.L_STEM,
        StemPattern.E_STEM,
        StemPattern.AI_STEM,
        StemPattern.O_MASCULINE,
        StemPattern.AU_STEM,
    }
)

COMMON_TARGET = 100
RARE_MINIMUM = 1


def main() -> int:
    report = load_corpus_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))

    errors: list[str] = []
    for pattern_value, info in report.get("nouns_by_pattern", {}).items():
        count = info.get("count", 0)
        try:
            pattern = StemPattern(pattern_value)
        except ValueError:
            errors.append(f"unknown pattern file: {pattern_value}")
            continue
        if pattern in COMMON_PATTERNS and count < COMMON_TARGET:
            errors.append(f"{pattern_value}: {count} < {COMMON_TARGET}")
        elif pattern in TIERED_PATTERNS:
            continue
        elif count < RARE_MINIMUM:
            errors.append(f"{pattern_value}: {count} < {RARE_MINIMUM}")

    nouns = graduate_noun_stems()
    verbs = graduate_verb_dhatus()
    print(f"\nLoaded {len(nouns)} noun stems, {len(verbs)} verb roots from {VOCABULARY_DIR}")

    if errors:
        print("\nValidation warnings:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
