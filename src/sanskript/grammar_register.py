"""Single source of controlled-register synthesis intents and recipe catalog."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from functools import lru_cache
from collections.abc import Iterable

from .avyaya import AVYAYA_FORMS, UPASARGAS, iter_avyaya_analyses
from .grammar import (
    CONTROLLED_NOUNS,
    NUMERAL_FORMS,
    VERB_FRAMES,
    CASE_TO_ROLE,
    Case,
    Gender,
    GrammaticalNumber,
    Lakara,
    Pada,
    PartOfSpeech,
    Person,
    Role,
)
from .derivation import KRT_FORMS, TADDHITA_FORMS
from .morphology_synth import DerivationIntent, DerivationKind
from .samasa import SamasaType
from .subanta import SUBANTA_STEMS, decline_paradigm, iter_pronoun_analyses
from .tinanta import DHATUS, conjugate_paradigm, has_tin_endings
from .vocabulary_catalog import graduate_noun_stems, graduate_verb_dhatus


CONTROLLED_LEMMAS = frozenset(stem.lemma for stem in CONTROLLED_NOUNS) | frozenset({"deva"})

# Extra finite verb surfaces used in morphology tests but not tied to program frames.
REGISTER_TINANTA_FORMS: tuple[tuple[str, Lakara, Person, GrammaticalNumber, Pada], ...] = (
    ("dṛś", Lakara.LOT, Person.THIRD, GrammaticalNumber.SINGULAR, Pada.PARASMAIPADA),
    ("dṛś", Lakara.VIDHILING, Person.THIRD, GrammaticalNumber.SINGULAR, Pada.PARASMAIPADA),
    ("labh", Lakara.LAT, Person.THIRD, GrammaticalNumber.SINGULAR, Pada.ATMANEPADA),
)


@dataclass(frozen=True)
class RegisterEntry:
    """One grammar-register item with its synthesis intent and recipe metadata."""

    register_id: str
    intent: DerivationIntent
    construction_id: str = ""
    status: str = "experimental"
    description: str = ""
    authoritative: bool = False


def _explicit_noun_surfaces() -> frozenset[str]:
    return frozenset(form.surface for stem in CONTROLLED_NOUNS for form in stem.forms)


def _avyaya_gloss(surface: str) -> str:
    for form in AVYAYA_FORMS + UPASARGAS:
        if form.surface == surface:
            return form.gloss
    return "indeclinable"


def register_entries(*, include_vocabulary: bool = True) -> tuple[RegisterEntry, ...]:
    return _register_entries(include_vocabulary)


def runtime_register_entries() -> tuple[RegisterEntry, ...]:
    """Small hot-path register for parser/facade lookup, excluding graduate vocabulary."""
    return register_entries(include_vocabulary=False)


@lru_cache(maxsize=2)
def _register_entries(include_vocabulary: bool = True) -> tuple[RegisterEntry, ...]:
    entries: list[RegisterEntry] = []
    explicit_surfaces = _explicit_noun_surfaces()

    for stem in SUBANTA_STEMS:
        if stem.lemma not in CONTROLLED_LEMMAS:
            continue
        for (case, number), surface in decline_paradigm(stem).items():
            if surface in explicit_surfaces:
                continue
            register_id = f"NF-PARADIGM:{stem.lemma}:{case.value}:{number.value}"
            entries.append(
                RegisterEntry(
                    register_id=register_id,
                    intent=DerivationIntent(
                        kind=DerivationKind.SUBANTA,
                        lemma=stem.lemma,
                        case=case,
                        number=number,
                        gender=stem.gender,
                        role=CASE_TO_ROLE.get(case),
                        pos=PartOfSpeech.NOUN,
                        register_id=register_id,
                        gloss=stem.gloss,
                    ),
                    construction_id="NF-001",
                    description=f"{stem.lemma} {case.value} {number.value} via SubantaSupEngine",
                )
            )

    for stem in CONTROLLED_NOUNS:
        for form in stem.forms:
            register_id = f"NF-001:{stem.lemma}:{form.surface}"
            entries.append(
                RegisterEntry(
                    register_id=register_id,
                    intent=DerivationIntent(
                        kind=DerivationKind.SUBANTA,
                        lemma=stem.lemma,
                        case=form.case,
                        number=form.number,
                        gender=stem.gender,
                        role=CASE_TO_ROLE.get(form.case),
                        pos=PartOfSpeech.NOUN,
                        register_id=register_id,
                        gloss=stem.gloss,
                    ),
                    construction_id="NF-001",
                    description=f"{stem.lemma} → {form.surface} via SubantaSupEngine",
                    authoritative=True,
                )
            )

    for numeral in NUMERAL_FORMS:
        register_id = f"NUM-001:{numeral.surface}"
        role = Role.KARANA if numeral.case.value == "instrumental" else Role.KARMAN
        entries.append(
            RegisterEntry(
                register_id=register_id,
                intent=DerivationIntent.fixed(
                    surface=numeral.surface,
                    lemma=numeral.lemma,
                    pos=PartOfSpeech.NUMERAL,
                    case=numeral.case,
                    number=numeral.number,
                    gender=numeral.gender,
                    role=role,
                    value=numeral.value,
                    register_id=register_id,
                ),
                construction_id="NUM-001",
                description=f"cardinal {numeral.value} as {numeral.case.value}",
                authoritative=True,
            )
        )

    for surface, frame in VERB_FRAMES.items():
        register_id = f"{frame.construction_id}:{surface}"
        entries.append(
            RegisterEntry(
                register_id=register_id,
                intent=DerivationIntent.fixed(
                    surface=frame.surface,
                    lemma=frame.lemma,
                    pos=PartOfSpeech.VERB,
                    number=frame.number,
                    person=frame.person,
                    pada=frame.pada,
                    lakara=frame.lakara,
                    register_id=register_id,
                    gloss=frame.gloss,
                ),
                construction_id=frame.construction_id,
                description=frame.gloss,
                authoritative=True,
            )
        )

    for lemma, lakara, person, number, pada in REGISTER_TINANTA_FORMS:
        register_id = f"TIN-001:{lemma}:{lakara.value}:{person.value}:{number.value}"
        entries.append(
            RegisterEntry(
                register_id=register_id,
                intent=DerivationIntent.tinanta(
                    lemma=lemma,
                    lakara=lakara,
                    person=person,
                    number=number,
                    pada=pada,
                    register_id=register_id,
                ),
                construction_id="TIN-001",
                description=f"{lemma} {lakara.value} {person.value} {number.value}",
            )
        )

    for analysis in iter_pronoun_analyses():
        register_id = f"PRO-001:{analysis.surface}"
        entries.append(
            RegisterEntry(
                register_id=register_id,
                intent=DerivationIntent.fixed(
                    surface=analysis.surface,
                    lemma=analysis.lemma,
                    pos=PartOfSpeech.PRONOUN,
                    case=analysis.case,
                    number=analysis.number,
                    person=analysis.person,
                    role=analysis.role,
                    register_id=register_id,
                ),
                construction_id="PRO-001",
                description=f"pronoun {analysis.surface}",
            )
        )

    for analysis in iter_avyaya_analyses():
        register_id = f"AVYAYA:{analysis.surface}"
        entries.append(
            RegisterEntry(
                register_id=register_id,
                intent=DerivationIntent.fixed(
                    surface=analysis.surface,
                    lemma=analysis.lemma,
                    pos=PartOfSpeech.INDECLINABLE,
                    indeclinable_kind=analysis.indeclinable_kind,
                    register_id=register_id,
                    gloss=_avyaya_gloss(analysis.surface),
                ),
                construction_id="AVYAYA",
                description="indeclinable",
            )
        )

    if include_vocabulary:
        entries.extend(_register_vocabulary_entries())
    entries.extend(_register_derivation_entries())

    return tuple(entries)


REGISTER_LAKARAS: tuple[Lakara, ...] = (
    Lakara.LAT,
    Lakara.LAN,
    Lakara.LIT,
    Lakara.LUN,
    Lakara.LRT,
    Lakara.LUT,
    Lakara.LOT,
    Lakara.VIDHILING,
    Lakara.LRN,
)


def _register_vocabulary_entries() -> list[RegisterEntry]:
    """Graduate-tier noun and verb paradigms via directed sup/tiṅ synthesis only."""
    entries: list[RegisterEntry] = []
    explicit_surfaces = _explicit_noun_surfaces()
    skip_nouns = CONTROLLED_LEMMAS

    for stem in graduate_noun_stems():
        if stem.lemma in skip_nouns:
            continue
        for (case, number), surface in decline_paradigm(stem).items():
            if surface in explicit_surfaces:
                continue
            register_id = f"VOC-NOUN:{stem.lemma}:{case.value}:{number.value}"
            entries.append(
                RegisterEntry(
                    register_id=register_id,
                    intent=DerivationIntent(
                        kind=DerivationKind.SUBANTA,
                        lemma=stem.lemma,
                        case=case,
                        number=number,
                        gender=stem.gender,
                        role=CASE_TO_ROLE.get(case),
                        pos=PartOfSpeech.NOUN,
                        register_id=register_id,
                        gloss=stem.gloss,
                    ),
                    construction_id="VOC-NOUN",
                    description=f"{stem.lemma} {case.value} {number.value}",
                )
            )

    core_dhatus = {(dhatu.lemma, dhatu.pada) for dhatu in DHATUS}
    for dhatu in graduate_verb_dhatus():
        if (dhatu.lemma, dhatu.pada) in core_dhatus:
            continue
        for lakara in REGISTER_LAKARAS:
            if not has_tin_endings(lakara, dhatu.pada):
                continue
            paradigm = conjugate_paradigm(dhatu, lakara)
            if not paradigm:
                continue
            for (person, number), _surface in paradigm.items():
                register_id = f"VOC-VERB:{dhatu.lemma}:{lakara.value}:{person.value}:{number.value}"
                entries.append(
                    RegisterEntry(
                        register_id=register_id,
                        intent=DerivationIntent.tinanta(
                            lemma=dhatu.lemma,
                            lakara=lakara,
                            person=person,
                            number=number,
                            pada=dhatu.pada,
                            register_id=register_id,
                            gloss=dhatu.gloss,
                        ),
                        construction_id="VOC-VERB",
                        description=f"{dhatu.lemma} {lakara.value} {person.value} {number.value}",
                    )
                )
    return entries


def _register_derivation_entries() -> list[RegisterEntry]:
    """Kṛt, taddhita, samāsa, and sandhi forms built through curated or sequenced synthesis."""
    items: list[RegisterEntry] = []

    for form in KRT_FORMS:
        register_id = f"KRT-001:{form.surface}"
        items.append(
            RegisterEntry(
                register_id=register_id,
                intent=DerivationIntent.krt(
                    source=form.source,
                    suffix=form.suffix,
                    register_id=register_id,
                    gloss=form.gloss,
                ),
                construction_id="KRT-001",
                description=f"{form.source} + {form.suffix.value} via KrtDerivationEngine",
            )
        )

    for form in TADDHITA_FORMS:
        register_id = f"TAD-001:{form.surface}"
        items.append(
            RegisterEntry(
                register_id=register_id,
                intent=DerivationIntent.taddhita(
                    source=form.source,
                    semantic=form.semantic,
                    suffix=form.suffix,
                    register_id=register_id,
                    gloss=form.gloss,
                    sutra_ids=(form.sutra_id,) if form.sutra_id else (),
                ),
                construction_id="TAD-001",
                description=f"{form.source} + {form.suffix.value} taddhita",
            )
        )

    items.extend(
        [
            RegisterEntry(
                register_id="SAM-001:devapurusa",
                intent=DerivationIntent.samasa(
                    member_lemmas=("deva", "purusa"),
                    compound_type=SamasaType.TATPURUSHA,
                    register_id="SAM-001:devapurusa",
                    gloss="son of a god",
                    features={
                        "member_specs": (
                            {
                                "surface": "devasya",
                                "lemma": "deva",
                                "case": Case.GENITIVE,
                                "gender": Gender.MASCULINE,
                                "number": GrammaticalNumber.SINGULAR,
                            },
                            {
                                "surface": "purusah",
                                "lemma": "purusa",
                                "case": Case.NOMINATIVE,
                                "gender": Gender.MASCULINE,
                                "number": GrammaticalNumber.SINGULAR,
                            },
                        )
                    },
                ),
                construction_id="SAM-001",
                description="tatpuruṣa deva+purusa",
            ),
            RegisterEntry(
                register_id="SND-001:devātra",
                intent=DerivationIntent.sandhi(
                    left="deva",
                    right="atra",
                    register_id="SND-001:devātra",
                    gloss="here (with sandhi)",
                ),
                construction_id="SND-001",
                description="savarna dīrgha sandhi join",
            ),
        ]
    )
    return items


def register_digest(
    entries: Iterable[RegisterEntry] | None = None,
    *,
    include_vocabulary: bool = True,
) -> str:
    """Stable digest of register entry ids and intent signatures for CI validation."""
    active_entries = tuple(entries) if entries is not None else register_entries(include_vocabulary=include_vocabulary)
    payload = "".join(
        f"{entry.register_id}:{entry.intent.kind.value}:{entry.intent.lemma}:{entry.intent.surface}"
        for entry in active_entries
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def register_intents() -> tuple[DerivationIntent, ...]:
    return tuple(entry.intent for entry in register_entries())


def recipe_catalog() -> dict[str, str]:
    """Map register ids to human-readable recipe descriptions."""
    from .morphology_synth import RecipePlanner

    planner = RecipePlanner()
    catalog: dict[str, str] = {}
    for entry in register_entries():
        recipe = planner.plan(entry.intent)
        catalog[entry.register_id] = f"{recipe.engine}: {recipe.description}"
    return catalog


__all__ = [
    "RegisterEntry",
    "REGISTER_TINANTA_FORMS",
    "recipe_catalog",
    "register_digest",
    "register_entries",
    "register_intents",
    "runtime_register_entries",
]
