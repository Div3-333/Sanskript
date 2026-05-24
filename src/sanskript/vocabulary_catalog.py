"""Graduate-tier Sanskrit vocabulary stems for controlled lexicon expansion."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .derivation import KRT_FORMS, TADDHITA_FORMS
from .grammar import CONTROLLED_NOUNS, Gender
from .subanta import (
    SUBANTA_STEMS,
    DeclensionStem,
    StemPattern,
    infer_stem_pattern,
    valid_lemma_for_pattern,
)
from .tinanta import DHATUS, Dhatu, Pada

ROOT = Path(__file__).resolve().parents[2]
VOCABULARY_DIR = ROOT / "data" / "vocabulary"
NOUNS_DIR = VOCABULARY_DIR / "nouns"
VERBS_PATH = VOCABULARY_DIR / "verbs" / "dhatu_catalog.json"
LEGACY_VOCABULARY_PATH = ROOT / "data" / "vocabulary_stems.json"

_PATTERN_BY_VALUE = {pattern.value: pattern for pattern in StemPattern}

_GENDER_BY_VALUE = {
    "masculine": Gender.MASCULINE,
    "feminine": Gender.FEMININE,
    "neuter": Gender.NEUTER,
}

_PADA_BY_VALUE = {
    "parasmaipada": Pada.PARASMAIPADA,
    "atmanepada": Pada.ATMANEPADA,
}

_CORE_VERB_LEMMAS = frozenset({"bhū", "dṛś", "vṛdh", "nyūnaya", "labh", "kṛ"})


@dataclass(frozen=True)
class VerbStem:
    lemma: str
    present_stem: str
    pada: Pada = Pada.PARASMAIPADA
    gloss: str = ""
    gana: int = 1
    markers: frozenset[str] = frozenset()


def _resolve_pattern(lemma: str, gender: Gender, pattern: StemPattern | None) -> StemPattern | None:
    if pattern is not None and valid_lemma_for_pattern(lemma, pattern):
        return pattern
    inferred = infer_stem_pattern(lemma, gender)
    if inferred is not None and valid_lemma_for_pattern(lemma, inferred):
        return inferred
    return pattern if pattern is not None and valid_lemma_for_pattern(lemma, pattern) else inferred


def _stem_from_noun_record(
    lemma: str,
    gender: Gender,
    gloss: str,
    *,
    pattern: StemPattern | None = None,
) -> DeclensionStem | None:
    resolved = _resolve_pattern(lemma, gender, pattern)
    if resolved is None:
        return None
    return DeclensionStem(lemma, resolved, gender, gloss)


def _load_pattern_file(path: Path) -> list[dict]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return list(payload.get("entries", []))


@lru_cache(maxsize=1)
def _load_legacy_payload() -> dict:
    if not LEGACY_VOCABULARY_PATH.exists():
        return {"nouns": [], "verbs": []}
    return json.loads(LEGACY_VOCABULARY_PATH.read_text(encoding="utf-8"))


def _corpus_noun_records() -> list[dict]:
    records: list[dict] = []
    if NOUNS_DIR.is_dir():
        for path in sorted(NOUNS_DIR.glob("*.json")):
            records.extend(_load_pattern_file(path))
    return records


def _corpus_verb_records() -> list[dict]:
    if VERBS_PATH.exists():
        payload = json.loads(VERBS_PATH.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return payload
        return list(payload.get("entries", []))
    return []


def load_corpus_report() -> dict:
    """Summarize per-pattern noun counts and gaṇa distribution for CI/build scripts."""
    by_pattern: dict[str, dict] = {}
    for pattern in StemPattern:
        path = NOUNS_DIR / f"{pattern.value}.json"
        entries = _load_pattern_file(path) if path.exists() else []
        by_pattern[pattern.value] = {"count": len(entries), "file": path.name if path.exists() else None}

    by_gana: dict[int, int] = {}
    for raw in _corpus_verb_records():
        gana = int(raw.get("gana", 1))
        by_gana[gana] = by_gana.get(gana, 0) + 1

    return {
        "nouns_by_pattern": by_pattern,
        "verbs_by_gana": by_gana,
        "total_noun_entries": sum(info["count"] for info in by_pattern.values()),
        "total_verb_entries": sum(by_gana.values()),
    }


def _imported_noun_stems() -> tuple[DeclensionStem, ...]:
    stems: list[DeclensionStem] = list(SUBANTA_STEMS)

    for stem in CONTROLLED_NOUNS:
        item = _stem_from_noun_record(stem.lemma, stem.gender, stem.gloss)
        if item is not None:
            stems.append(item)

    for form in KRT_FORMS + TADDHITA_FORMS:
        item = _stem_from_noun_record(form.source, Gender.NEUTER, form.gloss)
        if item is not None:
            stems.append(item)

    return tuple(stems)


def _json_noun_stems() -> tuple[DeclensionStem, ...]:
    stems: list[DeclensionStem] = []
    for raw in _corpus_noun_records() or _load_legacy_payload().get("nouns", []):
        gender = _GENDER_BY_VALUE.get(str(raw.get("gender", "")))
        if gender is None:
            continue
        pattern_value = str(raw.get("pattern", ""))
        pattern = _PATTERN_BY_VALUE.get(pattern_value) if pattern_value else None
        item = _stem_from_noun_record(
            str(raw["lemma"]),
            gender,
            str(raw.get("gloss", "")),
            pattern=pattern,
        )
        if item is not None:
            stems.append(item)
    return tuple(stems)


def _imported_verb_stems() -> tuple[VerbStem, ...]:
    return tuple(
        VerbStem(dhatu.lemma, dhatu.present_stem, dhatu.pada, dhatu.gloss, dhatu.varga)
        for dhatu in DHATUS
    )


def _json_verb_stems() -> tuple[VerbStem, ...]:
    records = _corpus_verb_records() or _load_legacy_payload().get("verbs", [])
    items: list[VerbStem] = []
    for raw in records:
        pada = _PADA_BY_VALUE.get(str(raw.get("pada", "")))
        if pada is None:
            continue
        markers = frozenset(str(m) for m in raw.get("markers", []))
        items.append(
            VerbStem(
                str(raw["lemma"]),
                str(raw["present_stem"]),
                pada,
                str(raw.get("gloss", "")),
                int(raw.get("gana", 1)),
                markers,
            )
        )
    return tuple(items)


@lru_cache(maxsize=1)
def graduate_noun_stems() -> tuple[DeclensionStem, ...]:
    seen: set[str] = set()
    unique: list[DeclensionStem] = []
    for stem in (*_imported_noun_stems(), *_json_noun_stems()):
        if stem.lemma in seen:
            continue
        seen.add(stem.lemma)
        unique.append(stem)
    return tuple(unique)


@lru_cache(maxsize=1)
def graduate_verb_dhatus() -> tuple[Dhatu, ...]:
    seen: set[tuple[str, str]] = set()
    dhatus: list[Dhatu] = []
    for item in (*_imported_verb_stems(), *_json_verb_stems()):
        if item.lemma in _CORE_VERB_LEMMAS:
            continue
        key = (item.lemma, item.pada.value)
        if key in seen:
            continue
        seen.add(key)
        dhatus.append(
            Dhatu(
                item.lemma,
                item.present_stem,
                item.pada,
                item.gloss,
                varga=item.gana,
                markers=item.markers,
            )
        )
    return tuple(dhatus)


def vocabulary_stats() -> dict[str, int]:
    nouns = graduate_noun_stems()
    verbs = graduate_verb_dhatus()
    return {
        "noun_stems": len(nouns),
        "verb_roots": len(verbs),
        "stem_patterns": len({stem.pattern for stem in nouns}),
    }


__all__ = [
    "LEGACY_VOCABULARY_PATH",
    "VOCABULARY_DIR",
    "VerbStem",
    "graduate_noun_stems",
    "graduate_verb_dhatus",
    "load_corpus_report",
    "vocabulary_stats",
]
