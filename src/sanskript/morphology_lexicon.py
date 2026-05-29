"""Serialize and load controlled lexicon artifacts."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from collections.abc import Iterable
from typing import Any

from .grammar import (
    Analysis,
    Case,
    Gender,
    GrammaticalNumber,
    IndeclinableKind,
    Lakara,
    Pada,
    PartOfSpeech,
    Person,
    Role,
)


DEFAULT_LEXICON_PATH = Path(__file__).resolve().parents[2] / "data" / "controlled_lexicon.json"
DEFAULT_OVERRIDES_PATH = Path(__file__).resolve().parents[2] / "data" / "lexicon_overrides.json"


@dataclass(frozen=True)
class LexiconRecord:
    surface: str
    lemma: str
    pos: str
    case: str | None = None
    role: str | None = None
    gender: str | None = None
    number: str | None = None
    person: str | None = None
    pada: str | None = None
    lakara: str | None = None
    indeclinable_kind: str | None = None
    value: int | None = None
    register_id: str = ""
    recipe_id: str = ""
    engine: str = ""


def _enum_value(value: Any) -> Any:
    return value.value if hasattr(value, "value") else value


def analysis_to_record(
    analysis: Analysis,
    *,
    register_id: str = "",
    recipe_id: str = "",
    engine: str = "",
) -> LexiconRecord:
    return LexiconRecord(
        surface=analysis.surface,
        lemma=analysis.lemma,
        pos=_enum_value(analysis.pos),
        case=_enum_value(analysis.case),
        role=_enum_value(analysis.role),
        gender=_enum_value(analysis.gender),
        number=_enum_value(analysis.number),
        person=_enum_value(analysis.person),
        pada=_enum_value(analysis.pada),
        lakara=_enum_value(analysis.lakara),
        indeclinable_kind=_enum_value(analysis.indeclinable_kind),
        value=analysis.value,
        register_id=register_id,
        recipe_id=recipe_id,
        engine=engine,
    )


def record_to_analysis(record: LexiconRecord) -> Analysis:
    return Analysis(
        surface=record.surface,
        lemma=record.lemma,
        pos=PartOfSpeech(record.pos),
        case=Case(record.case) if record.case else None,
        role=Role(record.role) if record.role else None,
        gender=Gender(record.gender) if record.gender else None,
        number=GrammaticalNumber(record.number) if record.number else None,
        person=Person(record.person) if record.person else None,
        pada=Pada(record.pada) if record.pada else None,
        lakara=Lakara(record.lakara) if record.lakara else None,
        indeclinable_kind=IndeclinableKind(record.indeclinable_kind) if record.indeclinable_kind else None,
        value=record.value,
    )


def lexicon_to_json(entries: dict[str, Analysis], metadata: dict[str, Any]) -> str:
    payload = {
        "version": 1,
        "generated_at": metadata.get("generated_at") or datetime.now(UTC).isoformat(),
        "entry_count": len(entries),
        "metadata": metadata,
        "entries": {
            surface: asdict(
                analysis_to_record(
                    analysis,
                    register_id=str(metadata.get("register_ids", {}).get(surface, "")),
                    recipe_id=str(metadata.get("recipe_ids", {}).get(surface, "")),
                    engine=str(metadata.get("engines", {}).get(surface, "")),
                )
            )
            for surface, analysis in sorted(entries.items())
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def lexicon_from_json(text: str) -> dict[str, Analysis]:
    payload = json.loads(text)
    entries = payload.get("entries", {})
    lexicon: dict[str, Analysis] = {}
    for surface, raw in entries.items():
        record = LexiconRecord(**raw)
        store_preferred(lexicon, record_to_analysis(record))
    return lexicon


def load_lexicon_overrides(path: Path | None = None) -> dict[str, Analysis]:
    """Load hand-maintained lexicon overrides merged on top of synthesized entries."""
    override_path = path or DEFAULT_OVERRIDES_PATH
    if not override_path.exists():
        return {}
    payload = json.loads(override_path.read_text(encoding="utf-8"))
    entries = payload.get("entries", payload)
    overrides: dict[str, Analysis] = {}
    for surface, raw in entries.items():
        record = LexiconRecord(**raw)
        store_preferred(overrides, record_to_analysis(record), force=True)
    return overrides


def merge_lexicon_with_overrides(
    lexicon: dict[str, Analysis],
    overrides: dict[str, Analysis] | None = None,
) -> dict[str, Analysis]:
    merged = dict(lexicon)
    for surface, analysis in (overrides or load_lexicon_overrides()).items():
        store_preferred(merged, analysis, force=True)
    return merged


def load_controlled_lexicon(path: Path | None = None, *, apply_overrides: bool = True) -> dict[str, Analysis]:
    lexicon_path = path or DEFAULT_LEXICON_PATH
    if not lexicon_path.exists():
        base: dict[str, Analysis] = {}
    else:
        base = lexicon_from_json(lexicon_path.read_text(encoding="utf-8"))
    if apply_overrides:
        return merge_lexicon_with_overrides(base)
    return base


def lexicon_entry_count_manifest() -> int:
    """Canonical entry_count via Phase 27 Sanskript bytecode port (not Python JSON parsing)."""
    from .phase27_ports import canonical_lexicon_entry_count

    return canonical_lexicon_entry_count()


def save_controlled_lexicon(
    entries: dict[str, Analysis],
    path: Path | None = None,
    *,
    metadata: dict[str, Any] | None = None,
) -> Path:
    lexicon_path = path or DEFAULT_LEXICON_PATH
    lexicon_path.parent.mkdir(parents=True, exist_ok=True)
    lexicon_path.write_text(
        lexicon_to_json(entries, metadata or {}),
        encoding="utf-8",
    )
    return lexicon_path


def build_lexicon_artifact(output: Path | None = None, *, entries: Iterable[Any] | None = None) -> Path:
    """Build data/controlled_lexicon.json from grammar-register synthesis intents."""
    import hashlib

    from .grammar_register import register_digest, register_entries
    from .morphology_synth import MorphologySynthesizer, expected_catalog_surface
    from .morphology_validate import validate_surface

    synthesizer = MorphologySynthesizer()
    lexicon: dict[str, Analysis] = {}
    register_ids: dict[str, str] = {}
    recipe_ids: dict[str, str] = {}
    engines: dict[str, str] = {}
    active_entries = tuple(entries) if entries is not None else register_entries()

    for entry in active_entries:
        result = synthesizer.synthesize(entry.intent)
        expected = expected_catalog_surface(entry.intent)
        surface = validate_surface(
            result.surface,
            expected=expected,
            register_id=entry.register_id,
        )
        analysis = result.analysis
        if surface != result.analysis.surface:
            from dataclasses import replace

            analysis = replace(result.analysis, surface=surface)
        store_preferred(lexicon, analysis, force=entry.authoritative)
        register_ids[surface] = entry.register_id
        recipe_ids[surface] = result.recipe_id
        engines[surface] = result.engine

    lexicon = merge_lexicon_with_overrides(lexicon)

    digest = hashlib.sha256(
        "".join(
            f"{surface}:{analysis.lemma}:{analysis.pos.value}"
            for surface, analysis in sorted(lexicon.items())
        ).encode("utf-8")
    ).hexdigest()
    metadata = {
        "register_ids": register_ids,
        "recipe_ids": recipe_ids,
        "engines": engines,
        "content_digest": digest,
        "register_digest": register_digest(active_entries),
        "recipe_catalog_size": len(active_entries),
    }
    return save_controlled_lexicon(lexicon, output or DEFAULT_LEXICON_PATH, metadata=metadata)


def store_preferred(lexicon: dict[str, Analysis], analysis: Analysis, *, force: bool = False) -> None:
    existing = lexicon.get(analysis.surface)
    if force or existing is None or _case_priority(analysis) > _case_priority(existing):
        lexicon[analysis.surface] = analysis


def _case_priority(analysis: Analysis) -> int:
    if analysis.case is None:
        return 0
    priority = {
        Case.VOCATIVE: 1,
        Case.NOMINATIVE: 2,
        Case.GENITIVE: 3,
        Case.LOCATIVE: 4,
        Case.DATIVE: 5,
        Case.ABLATIVE: 6,
        Case.INSTRUMENTAL: 7,
        Case.ACCUSATIVE: 8,
    }
    return priority.get(analysis.case, 0)


__all__ = [
    "DEFAULT_LEXICON_PATH",
    "DEFAULT_OVERRIDES_PATH",
    "LexiconRecord",
    "analysis_to_record",
    "build_lexicon_artifact",
    "load_controlled_lexicon",
    "load_lexicon_overrides",
    "merge_lexicon_with_overrides",
    "record_to_analysis",
    "save_controlled_lexicon",
    "store_preferred",
]
