#!/usr/bin/env python3
"""Migrate legacy data/vocabulary_stems.json into data/vocabulary/nouns/*.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sanskript.subanta import StemPattern  # noqa: E402

LEGACY = ROOT / "data" / "vocabulary_stems.json"
OUT_DIR = ROOT / "data" / "vocabulary" / "nouns"
VERB_OUT = ROOT / "data" / "vocabulary" / "verbs" / "dhatu_catalog.json"


def main() -> int:
    if not LEGACY.exists():
        print(f"No legacy file at {LEGACY}")
        return 1

    payload = json.loads(LEGACY.read_text(encoding="utf-8"))
    by_pattern: dict[str, list[dict]] = {p.value: [] for p in StemPattern}
    seen: dict[str, set[str]] = {p.value: set() for p in StemPattern}

    for raw in payload.get("nouns", []):
        pattern = str(raw.get("pattern", ""))
        lemma = str(raw.get("lemma", ""))
        if pattern not in by_pattern or lemma in seen[pattern]:
            continue
        seen[pattern].add(lemma)
        entry = dict(raw)
        entry.setdefault("source", "legacy vocabulary_stems.json")
        by_pattern[pattern].append(entry)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for pattern, entries in by_pattern.items():
        if not entries:
            continue
        path = OUT_DIR / f"{pattern}.json"
        path.write_text(
            json.dumps(
                {
                    "pattern": pattern,
                    "target_count": 100,
                    "entries": sorted(entries, key=lambda e: e["lemma"]),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"Wrote {len(entries)} entries to {path.name}")

    verbs = payload.get("verbs", [])
    if verbs and not VERB_OUT.exists():
        VERB_OUT.parent.mkdir(parents=True, exist_ok=True)
        catalog = []
        for raw in verbs:
            catalog.append(
                {
                    "lemma": raw["lemma"],
                    "gana": raw.get("gana", 1),
                    "pada": raw["pada"],
                    "present_stem": raw["present_stem"],
                    "gloss": raw.get("gloss", ""),
                    "markers": raw.get("markers", []),
                    "source": raw.get("source", "legacy vocabulary_stems.json"),
                }
            )
        VERB_OUT.write_text(
            json.dumps({"version": 1, "entries": catalog}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Wrote {len(catalog)} verbs to {VERB_OUT}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
