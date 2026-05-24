"""Morphology compiler backend: intent → recipe → surface + Analysis."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from typing import Any

from .adhyaya123_engines import (
    KrtDerivationEngine,
    SamasaDerivationEngine,
    SubantaSupEngine,
    TinantaLakaraEngine,
)
from .adhyaya678_engines import SAVARNA_DIRGHA, SandhiDerivationEngine
from .derivation import KRT_FORMS, KrtSuffix, TADDHITA_FORMS, TaddhitaSuffix, derive_taddhita
from .errors import MorphologyError
from .grammar import (
    Analysis,
    CASE_TO_ROLE,
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
from .paninian_engine import PaninianDerivationEngine, PaninianState
from .samasa import SamasaType
from .subanta import SUBANTA_STEMS, DeclensionStem, StemPattern, decline_paradigm, infer_stem_pattern
from .tinanta import DHATUS, Dhatu, conjugate_paradigm
from .vocabulary_catalog import graduate_noun_stems, graduate_verb_dhatus


class DerivationKind(str, Enum):
    TINANTA = "tinanta"
    SUBANTA = "subanta"
    KRT = "krt"
    TADDHITA = "taddhita"
    SAMASA = "samasa"
    SANDHI = "sandhi"
    FIXED = "fixed"
    AVYAYA = "avyaya"
    PRONOUN = "pronoun"
    NUMERAL = "numeral"


TINANTA_AUTO_PREFIXES: tuple[str, ...] = ("1.3.", "2.4.", "3.1.", "3.4.", "6.", "7.", "8.")
SUBANTA_AUTO_PREFIXES: tuple[str, ...] = ("1.4.", "6.", "7.", "8.")
KRT_AUTO_PREFIXES: tuple[str, ...] = ("3.1.", "3.2.", "3.3.", "3.4.", "6.", "7.", "8.")
TADDHITA_AUTO_PREFIXES: tuple[str, ...] = ("4.", "5.", "6.", "7.", "8.")
SAMASA_AUTO_PREFIXES: tuple[str, ...] = ("2.1.", "2.2.", "2.4.", "6.", "7.", "8.")
SANDHI_AUTO_PREFIXES: tuple[str, ...] = ("6.", "7.", "8.")


@dataclass(frozen=True)
class DerivationIntent:
    kind: DerivationKind
    lemma: str = ""
    surface: str = ""
    pos: PartOfSpeech = PartOfSpeech.NOUN
    case: Case | None = None
    number: GrammaticalNumber | None = None
    gender: Gender | None = None
    person: Person | None = None
    pada: Pada | None = None
    lakara: Lakara | None = None
    indeclinable_kind: IndeclinableKind | None = None
    role: Role | None = None
    value: int | None = None
    suffix: str = ""
    semantic: str = ""
    source: str = ""
    left: str = ""
    right: str = ""
    compound_type: SamasaType | None = None
    member_lemmas: tuple[str, ...] = ()
    register_id: str = ""
    gloss: str = ""
    sutra_ids: tuple[str, ...] = ()
    features: Mapping[str, Any] = field(default_factory=dict)

    @staticmethod
    def tinanta(
        *,
        lemma: str,
        lakara: Lakara,
        person: Person,
        number: GrammaticalNumber,
        pada: Pada = Pada.PARASMAIPADA,
        register_id: str = "",
        gloss: str = "",
    ) -> DerivationIntent:
        return DerivationIntent(
            kind=DerivationKind.TINANTA,
            lemma=lemma,
            lakara=lakara,
            person=person,
            number=number,
            pada=pada,
            pos=PartOfSpeech.VERB,
            register_id=register_id,
            gloss=gloss,
        )

    @staticmethod
    def subanta(
        *,
        lemma: str,
        case: Case,
        number: GrammaticalNumber,
        gender: Gender | None = None,
        register_id: str = "",
        gloss: str = "",
    ) -> DerivationIntent:
        return DerivationIntent(
            kind=DerivationKind.SUBANTA,
            lemma=lemma,
            case=case,
            number=number,
            gender=gender,
            pos=PartOfSpeech.NOUN,
            register_id=register_id,
            gloss=gloss,
        )

    @staticmethod
    def krt(
        *,
        source: str,
        suffix: KrtSuffix | str,
        register_id: str = "",
        gloss: str = "",
    ) -> DerivationIntent:
        suffix_value = suffix.value if isinstance(suffix, KrtSuffix) else suffix
        return DerivationIntent(
            kind=DerivationKind.KRT,
            source=source,
            suffix=suffix_value,
            pos=PartOfSpeech.NOUN,
            register_id=register_id,
            gloss=gloss,
        )

    @staticmethod
    def taddhita(
        *,
        source: str,
        semantic: str,
        suffix: TaddhitaSuffix | str = "",
        register_id: str = "",
        gloss: str = "",
        sutra_ids: tuple[str, ...] = (),
    ) -> DerivationIntent:
        suffix_value = suffix.value if isinstance(suffix, TaddhitaSuffix) else suffix
        return DerivationIntent(
            kind=DerivationKind.TADDHITA,
            source=source,
            semantic=semantic,
            suffix=suffix_value,
            pos=PartOfSpeech.NOUN,
            register_id=register_id,
            gloss=gloss,
            sutra_ids=sutra_ids,
        )

    @staticmethod
    def samasa(
        *,
        member_lemmas: Sequence[str],
        compound_type: SamasaType,
        register_id: str = "",
        gloss: str = "",
        sutra_ids: tuple[str, ...] = ("2.1.22", "2.4.71"),
        features: Mapping[str, Any] | None = None,
    ) -> DerivationIntent:
        return DerivationIntent(
            kind=DerivationKind.SAMASA,
            member_lemmas=tuple(member_lemmas),
            compound_type=compound_type,
            pos=PartOfSpeech.NOUN,
            register_id=register_id,
            gloss=gloss,
            sutra_ids=sutra_ids,
            features=dict(features or {}),
        )

    @staticmethod
    def sandhi(
        *,
        left: str,
        right: str,
        register_id: str = "",
        gloss: str = "",
        sutra_ids: tuple[str, ...] = ("6.1.101",),
    ) -> DerivationIntent:
        return DerivationIntent(
            kind=DerivationKind.SANDHI,
            left=left,
            right=right,
            register_id=register_id,
            gloss=gloss,
            sutra_ids=sutra_ids,
        )

    @staticmethod
    def fixed(
        *,
        surface: str,
        lemma: str,
        pos: PartOfSpeech,
        register_id: str = "",
        gloss: str = "",
        case: Case | None = None,
        number: GrammaticalNumber | None = None,
        gender: Gender | None = None,
        person: Person | None = None,
        pada: Pada | None = None,
        lakara: Lakara | None = None,
        indeclinable_kind: IndeclinableKind | None = None,
        role: Role | None = None,
        value: int | None = None,
    ) -> DerivationIntent:
        return DerivationIntent(
            kind=DerivationKind.FIXED,
            surface=surface,
            lemma=lemma,
            pos=pos,
            case=case,
            number=number,
            gender=gender,
            person=person,
            pada=pada,
            lakara=lakara,
            indeclinable_kind=indeclinable_kind,
            role=role,
            value=value,
            register_id=register_id,
            gloss=gloss,
        )


TADDHITA_SUTRA_BY_SEMANTIC: dict[str, str] = {
    "possession": "5.2.94",
    "apatya": "4.1.92",
    "atishayana": "5.3.55",
}

CATALOG_KINDS = frozenset(
    {
        DerivationKind.FIXED,
        DerivationKind.AVYAYA,
        DerivationKind.PRONOUN,
        DerivationKind.NUMERAL,
    }
)

FAMILY_DERIVE_KINDS = frozenset(
    {
        DerivationKind.TINANTA,
        DerivationKind.SUBANTA,
        DerivationKind.KRT,
        DerivationKind.TADDHITA,
    }
)

DEFAULT_FAMILY_STEPS = 64


@dataclass(frozen=True)
class DerivationRecipe:
    id: str
    kind: DerivationKind
    engine: str
    sutra_prefixes: tuple[str, ...] = ()
    sutra_ids: tuple[str, ...] = ()
    use_family_derive: bool = False
    description: str = ""


@dataclass(frozen=True)
class SynthesisResult:
    analysis: Analysis
    surface: str
    recipe_id: str
    engine: str
    operations: tuple[str, ...] = ()
    sutra_ids: tuple[str, ...] = ()


class RecipePlanner:
    """Map derivation intents to engine recipes (not global sūtra search)."""

    def plan(self, intent: DerivationIntent) -> DerivationRecipe:
        register = intent.register_id or f"{intent.kind.value}:{intent.lemma or intent.surface or intent.source}"
        if intent.kind == DerivationKind.TINANTA:
            return DerivationRecipe(
                id=register,
                kind=intent.kind,
                engine="PaninianDerivationEngine",
                sutra_prefixes=TINANTA_AUTO_PREFIXES,
                description="dhātu + lakāra + tiṅ ending",
            )
        if intent.kind == DerivationKind.SUBANTA:
            return DerivationRecipe(
                id=register,
                kind=intent.kind,
                engine="PaninianDerivationEngine",
                sutra_prefixes=SUBANTA_AUTO_PREFIXES,
                description="prātipadika + sup ending",
            )
        if intent.kind == DerivationKind.TADDHITA:
            return DerivationRecipe(
                id=register,
                kind=intent.kind,
                engine="TaddhitaCatalogEngine",
                sutra_ids=self.resolve_sutra_ids(intent),
                description="stem + taddhita suffix via curated catalog",
            )
        if intent.kind == DerivationKind.KRT:
            return DerivationRecipe(
                id=register,
                kind=intent.kind,
                engine="KrtDerivationEngine",
                description="stem + kṛt suffix via curated catalog",
            )
        if intent.kind == DerivationKind.SAMASA:
            sutra_ids = intent.sutra_ids or ("2.1.22", "2.4.71")
            return DerivationRecipe(
                id=register,
                kind=intent.kind,
                engine="PaninianDerivationEngine",
                sutra_prefixes=SAMASA_AUTO_PREFIXES,
                sutra_ids=sutra_ids,
                description="compound formation",
            )
        if intent.kind == DerivationKind.SANDHI:
            return DerivationRecipe(
                id=register,
                kind=intent.kind,
                engine="PaninianDerivationEngine",
                sutra_prefixes=SANDHI_AUTO_PREFIXES,
                sutra_ids=intent.sutra_ids or ("6.1.101",),
                description="padaccheda sandhi join",
            )
        return DerivationRecipe(
            id=register,
            kind=intent.kind,
            engine="RegisterCatalog",
            description="curated register surface",
        )

    def resolve_sutra_ids(self, intent: DerivationIntent) -> tuple[str, ...]:
        if intent.sutra_ids:
            return intent.sutra_ids
        if intent.kind == DerivationKind.SANDHI:
            return ("6.1.101",)
        if intent.kind == DerivationKind.TADDHITA and intent.semantic:
            sutra = TADDHITA_SUTRA_BY_SEMANTIC.get(intent.semantic)
            if sutra:
                return (sutra,)
        return ()


class MorphologySynthesizer:
    """Execute derivation intents through PaninianDerivationEngine recipes."""

    def __init__(
        self,
        *,
        tinanta: TinantaLakaraEngine | None = None,
        subanta: SubantaSupEngine | None = None,
        krt: KrtDerivationEngine | None = None,
        samasa: SamasaDerivationEngine | None = None,
        sandhi: SandhiDerivationEngine | None = None,
        paninian: PaninianDerivationEngine | None = None,
    ) -> None:
        self.tinanta = tinanta or TinantaLakaraEngine()
        self.subanta = subanta or SubantaSupEngine()
        self.krt = krt or KrtDerivationEngine()
        self.samasa = samasa or SamasaDerivationEngine()
        self.sandhi = sandhi or SandhiDerivationEngine()
        self.paninian = paninian or PaninianDerivationEngine()
        self.planner = RecipePlanner()

    def synthesize(self, intent: DerivationIntent, *, max_steps: int = DEFAULT_FAMILY_STEPS) -> SynthesisResult:
        recipe = self.planner.plan(intent)
        if _is_catalog_intent(intent):
            return self._catalog_result(intent, recipe)
        if intent.kind in {DerivationKind.TINANTA, DerivationKind.SUBANTA}:
            return self._synthesize_via_engine_and_sequence(intent, recipe)
        if intent.kind == DerivationKind.KRT:
            return self._synthesize_krt(intent, recipe)
        if intent.kind == DerivationKind.TADDHITA:
            return self._synthesize_taddhita(intent, recipe)
        final = self._execute_paninian(intent, recipe, max_steps=max_steps)
        return self._result_from_state(intent, recipe, final)

    def _synthesize_via_engine_and_sequence(
        self,
        intent: DerivationIntent,
        recipe: DerivationRecipe,
    ) -> SynthesisResult:
        """Directed tiṅ/sup: domain engine surface + PaninianDerivationEngine.derive_sequence()."""
        operations: list[str] = ()
        sutra_ids: tuple[str, ...] = ()
        if intent.kind == DerivationKind.TINANTA:
            dhatu = _find_dhatu(intent.lemma, intent.pada or Pada.PARASMAIPADA)
            lakara = intent.lakara or Lakara.LAT
            person = intent.person or Person.THIRD
            number = intent.number or GrammaticalNumber.SINGULAR
            engine_result = self.tinanta.conjugate(dhatu, lakara, person=person, number=number)
            surface = engine_result.requested_form or conjugate_paradigm(dhatu, lakara)[(person, number)]
            operations = list(engine_result.operations)
            sutra_ids = engine_result.sutra_ids
            state = _paninian_state_from_intent(intent)
            from dataclasses import replace

            state = replace(state, form=surface, dhatu=dhatu)
        else:
            stem = _find_declension_stem(intent.lemma, intent.gender)
            case = intent.case or Case.NOMINATIVE
            number = intent.number or GrammaticalNumber.SINGULAR
            engine_result = self.subanta.decline(stem, case=case, number=number)
            surface = engine_result.requested_form or decline_paradigm(stem)[(case, number)]
            operations = list(engine_result.operations)
            sutra_ids = engine_result.sutra_ids
            from dataclasses import replace

            analysis = Analysis(
                surface=surface,
                lemma=stem.lemma,
                pos=PartOfSpeech.NOUN,
                case=case,
                role=intent.role or CASE_TO_ROLE.get(case),
                gender=stem.gender,
                number=number,
            )
            base_state = _paninian_state_from_intent(intent)
            state = replace(
                base_state,
                form=surface,
                stem=stem,
                features={**base_state.features, "analysis": analysis},
            )
        if sutra_ids:
            try:
                final = self.paninian.derive_sequence(state, sutra_ids=sutra_ids)
            except (AttributeError, KeyError, TypeError, ValueError):
                final = state
        else:
            final = state
        if intent.kind == DerivationKind.TINANTA:
            analysis = Analysis(
                surface=surface,
                lemma=dhatu.lemma,
                pos=PartOfSpeech.VERB,
                number=number,
                person=person,
                pada=dhatu.pada,
                lakara=lakara,
            )
        else:
            analysis = Analysis(
                surface=surface,
                lemma=stem.lemma,
                pos=PartOfSpeech.NOUN,
                case=case,
                role=intent.role or CASE_TO_ROLE.get(case),
                gender=stem.gender,
                number=number,
            )
        merged_ops = tuple(dict.fromkeys((*operations, *(step.operation for step in final.history if step.operation))))
        merged_sutras = tuple(dict.fromkeys((*sutra_ids, *(step.sutra_id for step in final.history))))
        return SynthesisResult(
            analysis=analysis,
            surface=surface,
            recipe_id=recipe.id,
            engine="PaninianDerivationEngine",
            operations=merged_ops,
            sutra_ids=merged_sutras,
        )

    def _synthesize_krt(self, intent: DerivationIntent, recipe: DerivationRecipe) -> SynthesisResult:
        suffix = _parse_krt_suffix(intent.suffix)
        engine_result = self.krt.derive(intent.source, suffix)
        surface = engine_result.derived.surface
        analysis = Analysis(
            surface=surface,
            lemma=surface,
            pos=PartOfSpeech.NOUN,
        )
        return SynthesisResult(
            analysis=analysis,
            surface=surface,
            recipe_id=recipe.id,
            engine="KrtDerivationEngine",
            operations=engine_result.operations,
            sutra_ids=engine_result.sutra_ids,
        )

    def _synthesize_taddhita(self, intent: DerivationIntent, recipe: DerivationRecipe) -> SynthesisResult:
        if intent.suffix:
            suffix = _parse_taddhita_suffix(intent.suffix)
            derived = derive_taddhita(intent.source, suffix=suffix)
        elif recipe.sutra_ids:
            derived = derive_taddhita(intent.source, sutra_id=recipe.sutra_ids[0])
        elif intent.semantic:
            suffix = _taddhita_suffix_for_semantic(intent.semantic)
            derived = derive_taddhita(intent.source, suffix=suffix)
        else:
            raise MorphologyError(f"Taddhita intent {recipe.id!r} needs suffix, semantic, or sūtra id")
        analysis = Analysis(
            surface=derived.surface,
            lemma=derived.surface,
            pos=PartOfSpeech.NOUN,
        )
        return SynthesisResult(
            analysis=analysis,
            surface=derived.surface,
            recipe_id=recipe.id,
            engine="TaddhitaCatalogEngine",
            operations=derived.operations,
            sutra_ids=(derived.sutra_id,) if derived.sutra_id else recipe.sutra_ids,
        )

    def _execute_paninian(
        self,
        intent: DerivationIntent,
        recipe: DerivationRecipe,
        *,
        max_steps: int,
    ) -> PaninianState:
        state = _paninian_state_from_intent(intent)
        sequenced: PaninianState | None = None
        if recipe.sutra_ids:
            sequenced = self.paninian.derive_sequence(state, sutra_ids=recipe.sutra_ids)
            if _meaningful_derivation(sequenced, intent):
                return sequenced
        if recipe.use_family_derive and recipe.sutra_prefixes:
            final = self.paninian.derive(state, prefixes=recipe.sutra_prefixes, max_steps=max_steps).final
            if _meaningful_derivation(final, intent):
                return final
        if sequenced is not None and sequenced.form:
            return sequenced
        raise MorphologyError(
            f"Paninian derivation produced no surface for {intent.kind.value} intent {recipe.id!r}"
        )

    def _catalog_result(self, intent: DerivationIntent, recipe: DerivationRecipe) -> SynthesisResult:
        role = intent.role
        if role is None and intent.case is not None:
            role = CASE_TO_ROLE.get(intent.case)
        analysis = Analysis(
            surface=intent.surface,
            lemma=intent.lemma,
            pos=intent.pos,
            case=intent.case,
            role=role,
            gender=intent.gender,
            number=intent.number,
            person=intent.person,
            pada=intent.pada,
            lakara=intent.lakara,
            indeclinable_kind=intent.indeclinable_kind,
            value=intent.value,
        )
        return SynthesisResult(
            analysis=analysis,
            surface=intent.surface,
            recipe_id=recipe.id,
            engine=recipe.engine,
        )

    def _result_from_state(
        self,
        intent: DerivationIntent,
        recipe: DerivationRecipe,
        final: PaninianState,
        *,
        surface_override: str | None = None,
    ) -> SynthesisResult:
        surface = surface_override or final.form or intent.surface or intent.source
        if not surface:
            raise MorphologyError(f"Derivation for {recipe.id!r} did not produce a surface")
        analysis = _analysis_from_paninian_state(intent, final, surface)
        operations = tuple(step.operation for step in final.history if step.operation)
        sutra_ids = final.applied_sutras or recipe.sutra_ids
        return SynthesisResult(
            analysis=analysis,
            surface=surface,
            recipe_id=recipe.id,
            engine="PaninianDerivationEngine",
            operations=operations,
            sutra_ids=sutra_ids,
        )


def synthesize(intent: DerivationIntent, *, max_steps: int = DEFAULT_FAMILY_STEPS) -> SynthesisResult:
    """Public morphology backend: intent → recipe → PaninianDerivationEngine → Analysis."""
    return MorphologySynthesizer().synthesize(intent, max_steps=max_steps)


def auto_derive(
    intent: DerivationIntent,
    *,
    max_steps: int = DEFAULT_FAMILY_STEPS,
) -> SynthesisResult:
    """Family-scoped Paninian auto-derive (prefix-scoped when no explicit sūtra list)."""
    return synthesize(intent, max_steps=max_steps)


def _meaningful_derivation(final: PaninianState, intent: DerivationIntent) -> bool:
    if not final.form:
        return False
    if any(step.changed for step in final.history):
        return True
    baseline = intent.surface or intent.source or intent.left or ""
    if baseline and final.form != baseline:
        return True
    if intent.kind in {DerivationKind.TINANTA, DerivationKind.SUBANTA} and final.applied_sutras:
        return True
    return False


def _is_catalog_intent(intent: DerivationIntent) -> bool:
    if intent.kind in CATALOG_KINDS:
        return bool(intent.surface)
    if intent.kind == DerivationKind.FIXED:
        return bool(intent.surface)
    return False


def _paninian_state_from_intent(intent: DerivationIntent) -> PaninianState:
    features = dict(intent.features)
    if intent.source:
        features.setdefault("source", intent.source)
    if intent.semantic:
        features.setdefault("semantic", intent.semantic)
    if intent.suffix:
        features.setdefault("suffix", intent.suffix)
    if intent.kind == DerivationKind.SANDHI:
        features.update(
            {
                "left": intent.left,
                "right": intent.right,
                "strict_engine": True,
                "expected_rule": SAVARNA_DIRGHA,
            }
        )
    if intent.compound_type is not None:
        features.setdefault("compound_type", intent.compound_type)

    members: tuple[Analysis, ...] = ()
    if intent.kind == DerivationKind.SAMASA:
        member_specs = features.get("member_specs")
        if member_specs:
            members = tuple(_analysis_from_member_spec(spec) for spec in member_specs)
        elif intent.member_lemmas:
            members = tuple(
                Analysis(lemma, lemma, PartOfSpeech.NOUN, gender=Gender.MASCULINE)
                for lemma in intent.member_lemmas
            )

    dhatu = None
    stem = None
    suffix = None
    if intent.kind == DerivationKind.TINANTA:
        dhatu = _find_dhatu(intent.lemma, intent.pada or Pada.PARASMAIPADA)
    if intent.kind == DerivationKind.SUBANTA:
        stem = _find_declension_stem(intent.lemma, intent.gender)
    if intent.kind == DerivationKind.KRT and intent.suffix:
        suffix = _parse_krt_suffix(intent.suffix)
    if intent.kind == DerivationKind.TADDHITA and intent.suffix:
        suffix = _parse_taddhita_suffix(intent.suffix)

    initial_form = ""
    if intent.kind in CATALOG_KINDS or (intent.kind == DerivationKind.FIXED and intent.surface):
        initial_form = intent.surface or intent.source or ""

    return PaninianState(
        form=initial_form,
        features=features,
        members=members,
        source=intent.source or "",
        dhatu=dhatu,
        stem=stem,
        suffix=suffix,
        case=intent.case,
        number=intent.number,
        person=intent.person,
        lakara=intent.lakara,
        pada=intent.pada or (dhatu.pada if dhatu is not None else None),
        gender=intent.gender or (stem.gender if stem is not None else None),
        role=intent.role,
    )


def _analysis_from_member_spec(spec: Mapping[str, Any]) -> Analysis:
    case = spec.get("case")
    if isinstance(case, str):
        case = Case(case)
    gender = spec.get("gender")
    if isinstance(gender, str):
        gender = Gender(gender)
    number = spec.get("number")
    if isinstance(number, str):
        number = GrammaticalNumber(number)
    return Analysis(
        surface=str(spec.get("surface") or spec.get("lemma") or ""),
        lemma=str(spec.get("lemma") or ""),
        pos=PartOfSpeech.NOUN,
        case=case if isinstance(case, Case) else None,
        gender=gender if isinstance(gender, Gender) else None,
        number=number if isinstance(number, GrammaticalNumber) else None,
    )


def _analysis_from_paninian_state(intent: DerivationIntent, final: PaninianState, surface: str) -> Analysis:
    role = intent.role
    case = intent.case
    gender = intent.gender
    number = intent.number
    person = intent.person
    pada = intent.pada
    lakara = intent.lakara
    lemma = intent.lemma or intent.source or surface

    if intent.kind == DerivationKind.TINANTA and final.dhatu is not None:
        lemma = final.dhatu.lemma
        pada = final.dhatu.pada
        lakara = intent.lakara or final.lakara or lakara
        person = final.person or person
        number = final.number or number
    if intent.kind == DerivationKind.SUBANTA and final.stem is not None:
        lemma = final.stem.lemma
        gender = final.stem.gender
        case = final.case or case
        number = final.number or number
        role = role or (CASE_TO_ROLE.get(case) if case is not None else None)
    if intent.kind in {DerivationKind.KRT, DerivationKind.TADDHITA, DerivationKind.SAMASA, DerivationKind.SANDHI}:
        lemma = surface
    if isinstance(final.features.get("analysis"), Analysis):
        return final.features["analysis"]

    return Analysis(
        surface=surface,
        lemma=lemma,
        pos=intent.pos,
        case=case,
        role=role,
        gender=gender,
        number=number,
        person=person,
        pada=pada,
        lakara=lakara,
        indeclinable_kind=intent.indeclinable_kind,
        value=intent.value,
    )


def _find_dhatu(lemma: str, pada: Pada) -> Dhatu:
    exact, by_lemma = _dhatu_indexes()
    if (lemma, pada) in exact:
        return exact[(lemma, pada)]
    if lemma in by_lemma:
        return by_lemma[lemma]
    raise MorphologyError(f"No dhātu registered for lemma {lemma!r}")


def _find_declension_stem(lemma: str, gender: Gender | None) -> DeclensionStem:
    resolved_gender = gender or Gender.MASCULINE
    exact, by_lemma = _declension_stem_indexes()
    if gender is not None and (lemma, gender) in exact:
        return exact[(lemma, gender)]
    if lemma in by_lemma:
        return by_lemma[lemma]
    pattern = infer_stem_pattern(lemma, resolved_gender)
    if pattern is not None:
        return DeclensionStem(lemma, pattern, resolved_gender, lemma)
    return DeclensionStem(lemma, StemPattern.A_MASCULINE, resolved_gender, lemma)


@lru_cache(maxsize=1)
def _dhatu_indexes() -> tuple[dict[tuple[str, Pada], Dhatu], dict[str, Dhatu]]:
    exact: dict[tuple[str, Pada], Dhatu] = {}
    by_lemma: dict[str, Dhatu] = {}
    for dhatu in (*DHATUS, *graduate_verb_dhatus()):
        exact.setdefault((dhatu.lemma, dhatu.pada), dhatu)
        by_lemma.setdefault(dhatu.lemma, dhatu)
    return exact, by_lemma


@lru_cache(maxsize=1)
def _declension_stem_indexes() -> tuple[dict[tuple[str, Gender], DeclensionStem], dict[str, DeclensionStem]]:
    exact: dict[tuple[str, Gender], DeclensionStem] = {}
    by_lemma: dict[str, DeclensionStem] = {}
    for stem in (*SUBANTA_STEMS, *graduate_noun_stems()):
        exact.setdefault((stem.lemma, stem.gender), stem)
        by_lemma.setdefault(stem.lemma, stem)
    return exact, by_lemma


def _parse_krt_suffix(value: str) -> KrtSuffix:
    for item in KrtSuffix:
        if value in {item.value, item.name, item.name.lower()}:
            return item
    raise MorphologyError(f"Unknown kṛt suffix {value!r}")


def _parse_taddhita_suffix(value: str) -> TaddhitaSuffix:
    for item in TaddhitaSuffix:
        if value in {item.value, item.name, item.name.lower()}:
            return item
    raise MorphologyError(f"Unknown taddhita suffix {value!r}")


def _taddhita_suffix_for_semantic(semantic: str) -> TaddhitaSuffix:
    mapping = {
        "possession": TaddhitaSuffix.MATUP,
        "apatya": TaddhitaSuffix.APATYA,
        "atishayana": TaddhitaSuffix.ATISHAYANA,
    }
    suffix = mapping.get(semantic)
    if suffix is None:
        raise MorphologyError(f"Unknown taddhita semantic {semantic!r}")
    return suffix


def expected_catalog_surface(intent: DerivationIntent) -> str | None:
    """Return curated catalog surface when intent maps to KRT_FORMS / TADDHITA_FORMS."""
    if intent.kind == DerivationKind.KRT and intent.suffix:
        suffix = intent.suffix
        for form in KRT_FORMS:
            if form.source == intent.source and form.suffix.value == suffix:
                return form.surface
    if intent.kind == DerivationKind.TADDHITA:
        for form in TADDHITA_FORMS:
            if form.source != intent.source:
                continue
            if intent.semantic and form.semantic == intent.semantic:
                return form.surface
            if intent.suffix and form.suffix.value == intent.suffix:
                return form.surface
    return None


def _intent_to_paninian_state(intent: DerivationIntent) -> PaninianState:
    return _paninian_state_from_intent(intent)


def _analysis_from_intent(intent: DerivationIntent, surface: str) -> Analysis:
    return _analysis_from_paninian_state(intent, PaninianState(form=surface), surface)


__all__ = [
    "DerivationIntent",
    "DerivationKind",
    "DerivationRecipe",
    "MorphologySynthesizer",
    "RecipePlanner",
    "SynthesisResult",
    "auto_derive",
    "synthesize",
]
