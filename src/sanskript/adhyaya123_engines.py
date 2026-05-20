from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .categories import (
    assign_technical_names,
    get_vowel_weight,
    is_gha_suffix,
    is_ghu_root,
    is_nistha_suffix,
    is_sankhya_term,
    is_sarvanama_stem,
    is_sarvanamasthana_suffix,
    is_shat_numeral,
)
from .derivation import DerivedForm, KrtSuffix, derive
from .grammar import Analysis, Case, Gender, GrammaticalNumber, Lakara, Pada, PartOfSpeech, Person, Role, Samjna
from .karaka import KarakaExplanation, explain_case, get_allowed_vibhaktis, get_karaka_role, get_vibhakti
from .markers import MarkerAnalysis, analyze_it_markers
from .metarules import (
    RuleBehavior,
    augment_boundary,
    default_final_substitution_index,
    directive,
    following_initial_substitution_index,
    genitive_marks_substitution_site,
    is_vibhasha_expression,
    mid_augment_index,
    whole_term_replacement_applies,
)
from .samasa import Compound, SamasaType, create_compound
from .subanta import DeclensionStem, SupEnding, decline, sup_ending
from .sutra_logic import (
    SutraContext,
    evaluate_sutra,
    implemented_logic_ids,
    positive_context_for,
)
from .tinanta import (
    Dhatu,
    DhatuType,
    TimeContext,
    TinEnding,
    apply_luk_elision,
    conjugate,
    create_derived_dhatu,
    get_lakara_for_time,
    get_substituted_dhatu,
    get_vikarana,
    is_ardhadhatuka,
    is_sarvadhatuka,
    tin_ending,
)


FeatureMap = Mapping[str, Any]


@dataclass(frozen=True)
class AppliedSutra123:
    sutra_id: str
    context: dict[str, Any]
    operator: str
    summary: str
    assigned: tuple[str, ...]
    module: str = "sanskript.sutra_logic"


@dataclass(frozen=True)
class TechnicalNameResult:
    term: str | None
    suffix: str | None
    analysis: Analysis | None
    marker_analysis: MarkerAnalysis | None
    samjnas: frozenset[Samjna]
    assigned: tuple[str, ...]
    sutra_ids: tuple[str, ...]
    operations: tuple[str, ...]
    engines: tuple[str, ...]


@dataclass(frozen=True)
class GovernanceResult:
    input_form: str
    output_form: str
    behavior: RuleBehavior
    target_index: int | None
    target_scope: str
    sutra_ids: tuple[str, ...]
    operations: tuple[str, ...]
    engines: tuple[str, ...]


@dataclass(frozen=True)
class CompoundEngineResult:
    compound: Compound
    sutra_ids: tuple[str, ...]
    operations: tuple[str, ...]
    engines: tuple[str, ...]


@dataclass(frozen=True)
class CaseSelectionResult:
    role: Role | None
    case: Case
    allowed_cases: frozenset[Case]
    explanation: KarakaExplanation
    sutra_ids: tuple[str, ...]
    operations: tuple[str, ...]
    engines: tuple[str, ...]


@dataclass(frozen=True)
class SubantaEngineResult:
    stem: DeclensionStem
    forms: Mapping[tuple[Case, GrammaticalNumber], str]
    requested_form: str | None
    sup: str | None
    sutra_ids: tuple[str, ...]
    operations: tuple[str, ...]
    engines: tuple[str, ...]


@dataclass(frozen=True)
class DhatuTransformResult:
    source: Dhatu
    output: Dhatu
    lakara: Lakara | None
    luk_applies: bool
    sutra_ids: tuple[str, ...]
    operations: tuple[str, ...]
    engines: tuple[str, ...]


@dataclass(frozen=True)
class DhatuDerivationResult:
    source: Dhatu
    output: Dhatu
    dhatu_type: DhatuType
    sutra_ids: tuple[str, ...]
    operations: tuple[str, ...]
    engines: tuple[str, ...]


@dataclass(frozen=True)
class VikaranaResult:
    varga: int
    vikarana: str
    sutra_ids: tuple[str, ...]
    operations: tuple[str, ...]
    engines: tuple[str, ...]


@dataclass(frozen=True)
class KrtEngineResult:
    derived: DerivedForm
    sutra_ids: tuple[str, ...]
    operations: tuple[str, ...]
    engines: tuple[str, ...]


@dataclass(frozen=True)
class TinantaEngineResult:
    dhatu: Dhatu
    lakara: Lakara
    pada: Pada
    forms: Mapping[tuple[Person, GrammaticalNumber], str]
    requested_form: str | None
    ending: str | None
    sutra_ids: tuple[str, ...]
    operations: tuple[str, ...]
    engines: tuple[str, ...]


def _sutra_sort_key(sutra_id: str) -> tuple[int, ...]:
    return tuple(int(part) for part in sutra_id.split("."))


def _unique_sutras(applied: Iterable[AppliedSutra123]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(sutra.sutra_id for sutra in applied))


def _assigned_tags(applied: Iterable[AppliedSutra123]) -> tuple[str, ...]:
    tags: list[str] = []
    for sutra in applied:
        tags.extend(sutra.assigned)
    return tuple(dict.fromkeys(tags))


def _merge_features(
    base: Mapping[str, Any],
    overrides: Mapping[str, Any] | None,
    *,
    strict: bool,
) -> dict[str, Any] | None:
    context = dict(base)
    for key, value in (overrides or {}).items():
        if strict and key in context and context[key] != value:
            raise ValueError(f"Feature {key!r} conflicts with sutra fixture: {context[key]!r} != {value!r}")
        if not strict and key in context and context[key] != value:
            return None
        context[key] = value
    return context


def _context_contains_query(context: Mapping[str, Any], query: Mapping[str, Any]) -> bool:
    if not query:
        return False
    return any(key in context and context[key] == query[key] for key in query)


def _try_apply(
    selector: "SutraPredicateSelectionEngine",
    sutra_id: str,
    features: Mapping[str, Any],
) -> AppliedSutra123 | None:
    try:
        return selector.apply(sutra_id, features, allow_reject=True)
    except ValueError:
        return None


def _technical_case_name(case: Case | None) -> str:
    if case == Case.GENITIVE:
        return "ṣaṣṭhī"
    if case is None:
        return ""
    return case.value


class SutraPredicateSelectionEngine:
    """Bridge existing truth-gated sutra predicates into reusable engines."""

    def __init__(self, prefixes: Sequence[str] = ("1.", "2.", "3.")) -> None:
        self.prefixes = tuple(prefixes)

    def implemented_ids(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                (sutra_id for sutra_id in implemented_logic_ids() if sutra_id.startswith(self.prefixes)),
                key=_sutra_sort_key,
            )
        )

    def fixture(
        self,
        sutra_id: str,
        overrides: Mapping[str, Any] | None = None,
        *,
        strict: bool = True,
    ) -> AppliedSutra123:
        base = positive_context_for(sutra_id)
        features = _merge_features(base.features, overrides, strict=strict)
        if features is None:
            raise ValueError(f"{sutra_id} fixture conflicts with the supplied query")
        return self.apply(sutra_id, features)

    def apply(
        self,
        sutra_id: str,
        features: Mapping[str, Any] | None = None,
        *,
        allow_reject: bool = False,
    ) -> AppliedSutra123:
        if features is None:
            context = positive_context_for(sutra_id)
            merged_features = dict(context.features)
        else:
            context = SutraContext(dict(features), sutra_id=sutra_id)
            merged_features = dict(features)
        decision = evaluate_sutra(sutra_id, context)
        if not decision.applies and not allow_reject:
            raise ValueError(f"{sutra_id} rejected context {merged_features!r}: {decision.reason}")
        if not decision.applies:
            return None  # type: ignore[return-value]
        return AppliedSutra123(
            sutra_id=sutra_id,
            context=merged_features,
            operator=decision.operator.value,
            summary=decision.action,
            assigned=decision.assigned,
        )

    def select(
        self,
        query: Mapping[str, Any],
        *,
        prefixes: Sequence[str] | None = None,
        allowed: Callable[[str], bool] | None = None,
    ) -> tuple[AppliedSutra123, ...]:
        matches: list[AppliedSutra123] = []
        active_prefixes = tuple(prefixes or self.prefixes)
        for sutra_id in self.implemented_ids():
            if not sutra_id.startswith(active_prefixes):
                continue
            if allowed is not None and not allowed(sutra_id):
                continue
            base = positive_context_for(sutra_id)
            if not _context_contains_query(base.features, query):
                continue
            features = _merge_features(base.features, query, strict=False)
            if features is None:
                continue
            applied = _try_apply(self, sutra_id, features)
            if applied is not None:
                matches.append(applied)
        return tuple(matches)


class SamjnaTechnicalEngine:
    """Adhyaya 1 technical-name, pada, and it-marker engine."""

    def __init__(self, selector: SutraPredicateSelectionEngine | None = None) -> None:
        self.selector = selector or SutraPredicateSelectionEngine()

    def classify(
        self,
        term: str | None = None,
        *,
        suffix: str | None = None,
        analysis: Analysis | None = None,
        suffix_surface: str | None = None,
        gender: Gender | None = None,
        marker_upadesha: str | None = None,
        marker_kind: str = "suffix",
        is_taddhita_marker: bool = False,
    ) -> TechnicalNameResult:
        samjnas: set[Samjna] = set()
        operations: list[str] = []
        applied: list[AppliedSutra123] = []
        marker_analysis: MarkerAnalysis | None = None

        if term is not None and is_ghu_root(term):
            samjnas.add(Samjna.GHU)
            operations.append("samjna:ghu")
            applied.append(self.selector.apply("1.1.20", {"root": term}))
        if suffix is not None and is_gha_suffix(suffix):
            samjnas.add(Samjna.GHA)
            operations.append("samjna:gha")
            applied.append(self.selector.apply("1.1.22", {"suffix": suffix}))
        if term is not None and is_sankhya_term(term):
            samjnas.add(Samjna.SAMKHYA)
            operations.append("samjna:samkhya")
            applied.append(self.selector.apply("1.1.23", {"term": term}))
        if term is not None and is_shat_numeral(term):
            samjnas.add(Samjna.SAT)
            operations.append("samjna:sat")
            sutra_id = "1.1.25" if term == "ḍati" else "1.1.24"
            applied.append(self.selector.apply(sutra_id, {"term": term}))
        if suffix is not None and is_nistha_suffix(suffix):
            samjnas.add(Samjna.NISTHA)
            operations.append("samjna:nistha")
            applied.append(self.selector.apply("1.1.26", {"suffix": suffix}))
        if term is not None and is_sarvanama_stem(term):
            samjnas.add(Samjna.SARVANAMA)
            operations.append("samjna:sarvanama")
            applied.append(self.selector.apply("1.1.27", {"stem": term}))
        if suffix is not None and is_sarvanamasthana_suffix(suffix, gender):
            operations.append("samjna:sarvanamasthana")
            applied.append(self.selector.fixture("1.1.43", {"suffix": suffix}, strict=False))

        if marker_upadesha is not None:
            marker_analysis = analyze_it_markers(marker_upadesha, marker_kind, is_taddhita_marker)
            if marker_analysis.markers:
                operations.append("it-marker-extraction")
            for sutra_id in ("1.3.2", "1.3.3", "1.3.4", "1.3.5", "1.3.6", "1.3.7", "1.3.8"):
                fixture = _merge_features(
                    positive_context_for(sutra_id).features,
                    {"upadesha": marker_upadesha, "kind": marker_kind},
                    strict=False,
                )
                if fixture is None:
                    continue
                sutra = _try_apply(self.selector, sutra_id, fixture)
                if sutra is not None:
                    applied.append(sutra)
            sutra = _try_apply(self.selector, "1.3.9", {"upadesha": marker_upadesha, "lemma": marker_analysis.lemma})
            if sutra is not None:
                applied.append(sutra)
                operations.append("it-lopa")

        result_analysis = analysis
        if analysis is not None:
            result_analysis = assign_technical_names(analysis, suffix_surface)
            samjnas.update(result_analysis.samjnas)
            if suffix_surface is not None:
                sutra = _try_apply(self.selector, "1.4.13", {"analysis": analysis, "suffix": suffix_surface})
                if sutra is not None:
                    applied.append(sutra)
                    operations.append("samjna:anga")
            for sutra_id, op in (
                ("1.4.14", "samjna:pada"),
                ("1.4.17", "samjna:pada-before-svadi"),
                ("1.4.18", "samjna:bha"),
            ):
                features: dict[str, Any] = {"analysis": analysis}
                if suffix_surface is not None:
                    features["suffix"] = suffix_surface
                sutra = _try_apply(self.selector, sutra_id, features)
                if sutra is not None:
                    applied.append(sutra)
                    operations.append(op)

        return TechnicalNameResult(
            term=term,
            suffix=suffix,
            analysis=result_analysis,
            marker_analysis=marker_analysis,
            samjnas=frozenset(samjnas),
            assigned=_assigned_tags(applied),
            sutra_ids=_unique_sutras(applied),
            operations=tuple(dict.fromkeys(operations)),
            engines=("SamjnaTechnicalEngine", "SutraPredicateSelectionEngine"),
        )

    def vowel_weight(self, word: str, index: int) -> TechnicalNameResult:
        weight = get_vowel_weight(word, index)
        applied: list[AppliedSutra123] = []
        operations: list[str] = []
        if weight == Samjna.LAGHU:
            applied.append(self.selector.apply("1.4.10", {"word": word, "index": index}))
            operations.append("samjna:laghu")
        elif weight == Samjna.GURU:
            for sutra_id in ("1.4.11", "1.4.12"):
                sutra = _try_apply(self.selector, sutra_id, {"word": word, "index": index})
                if sutra is not None:
                    applied.append(sutra)
            operations.append("samjna:guru")
        return TechnicalNameResult(
            term=word,
            suffix=None,
            analysis=None,
            marker_analysis=None,
            samjnas=frozenset({weight} if weight is not None else ()),
            assigned=_assigned_tags(applied),
            sutra_ids=_unique_sutras(applied),
            operations=tuple(operations),
            engines=("SamjnaTechnicalEngine", "SutraPredicateSelectionEngine"),
        )


class MetaruleGovernanceEngine:
    """Adhyaya 1 paribhāṣā engine for substitution, optionality, and augment placement."""

    def __init__(self, selector: SutraPredicateSelectionEngine | None = None) -> None:
        self.selector = selector or SutraPredicateSelectionEngine()

    def substitution_site(
        self,
        term: str,
        *,
        substitute: str = "",
        marker: str = "",
        reference_case: str | Case = "genitive",
    ) -> GovernanceResult:
        applied: list[AppliedSutra123] = []
        operations: list[str] = []
        case_name = _technical_case_name(reference_case) if isinstance(reference_case, Case) else reference_case

        if genitive_marks_substitution_site(case_name):
            applied.append(self.selector.apply("1.1.49", {"case": "genitive"}))
            operations.append("genitive-marks-substitution-site")

        target_index = default_final_substitution_index(term)
        if target_index is not None:
            applied.append(self.selector.apply("1.1.52", {"term": term, "index": target_index}))
            operations.append("default-final-substitution")

        target_scope = "sound"
        if whole_term_replacement_applies(substitute, marker):
            target_scope = "whole-term"
            sutra_id = "1.1.53" if marker in {"ṅ", "ś"} else "1.1.55"
            applied.append(self.selector.apply(sutra_id, {"substitute": substitute, "marker": marker}))
            operations.append("whole-term-replacement")

        directive(term, substitute or term, RuleBehavior.SUBSTITUTION)
        return GovernanceResult(
            input_form=term,
            output_form=substitute or term,
            behavior=RuleBehavior.SUBSTITUTION,
            target_index=target_index,
            target_scope=target_scope,
            sutra_ids=_unique_sutras(applied),
            operations=tuple(dict.fromkeys(operations)),
            engines=("MetaruleGovernanceEngine", "SutraPredicateSelectionEngine"),
        )

    def following_initial_site(self, term: str) -> GovernanceResult:
        index = following_initial_substitution_index(term)
        applied = [self.selector.apply("1.1.54", {"term": term, "index": index})]
        return GovernanceResult(
            input_form=term,
            output_form=term,
            behavior=RuleBehavior.SUBSTITUTION,
            target_index=index,
            target_scope="following-initial",
            sutra_ids=_unique_sutras(applied),
            operations=("following-initial-substitution",),
            engines=("MetaruleGovernanceEngine", "SutraPredicateSelectionEngine"),
        )

    def augment_position(self, base: str, marker: str) -> GovernanceResult:
        applied: list[AppliedSutra123] = []
        operations: list[str] = []
        boundary = augment_boundary(marker)
        target_index: int | None = None
        target_scope = "unmarked"
        if boundary is not None:
            applied.append(self.selector.apply("1.1.46", {"marker": marker, "boundary": boundary}))
            target_scope = boundary
            operations.append(f"{boundary}-augment")
        if marker == "m":
            target_index = mid_augment_index(base)
            if target_index is not None:
                applied.append(self.selector.apply("1.1.47", {"base": base, "index": target_index}))
                target_scope = "after-last-vowel"
                operations.append("mit-after-last-vowel")
        return GovernanceResult(
            input_form=base,
            output_form=base,
            behavior=RuleBehavior.SUBSTITUTION,
            target_index=target_index,
            target_scope=target_scope,
            sutra_ids=_unique_sutras(applied),
            operations=tuple(operations),
            engines=("MetaruleGovernanceEngine", "SutraPredicateSelectionEngine"),
        )

    def optionality(self, expression: str) -> GovernanceResult:
        is_optional = is_vibhasha_expression(expression)
        applied = [self.selector.apply("1.1.44", {"expression": expression})] if is_optional else []
        directive(expression, expression, RuleBehavior.OPTIONALITY, optional=is_optional)
        return GovernanceResult(
            input_form=expression,
            output_form=expression,
            behavior=RuleBehavior.OPTIONALITY,
            target_index=None,
            target_scope="optional" if is_optional else "not-optional",
            sutra_ids=_unique_sutras(applied),
            operations=("vibhasha-optionality",) if is_optional else (),
            engines=("MetaruleGovernanceEngine", "SutraPredicateSelectionEngine"),
        )


class SamasaDerivationEngine:
    """Adhyaya 2 samāsa engine built on compound predicates and surface derivation."""

    def __init__(self, selector: SutraPredicateSelectionEngine | None = None) -> None:
        self.selector = selector or SutraPredicateSelectionEngine()

    def derive(self, members: Sequence[Analysis], forced_type: SamasaType | None = None) -> CompoundEngineResult:
        member_list = list(members)
        compound = create_compound(member_list, forced_type=forced_type)
        member_tuple = tuple(member_list)
        applied: list[AppliedSutra123] = []
        operations: list[str] = ["samarthya", f"samasa:{compound.type.value}"]

        for sutra_id in ("2.1.1", "2.2.30"):
            features: dict[str, Any] = {"members": member_tuple}
            if sutra_id == "2.2.30" and member_tuple:
                features["first_lemma"] = member_tuple[0].lemma
            sutra = _try_apply(self.selector, sutra_id, features)
            if sutra is not None:
                applied.append(sutra)

        type_sutras = {
            SamasaType.AVYAYIBHAVA: ("2.1.5", "2.4.17", "2.4.18"),
            SamasaType.TATPURUSHA: ("2.1.22", "2.4.26"),
            SamasaType.DVIGU: ("2.1.23", "2.4.1"),
            SamasaType.KARMADHARAYA: ("2.1.57",),
            SamasaType.DVANDVA: ("2.2.29",),
        }
        for sutra_id in type_sutras.get(compound.type, ()):
            features = {"members": member_tuple}
            if sutra_id == "2.4.26" and compound.result_analysis is not None:
                features["gender"] = compound.result_analysis.gender
            sutra = _try_apply(self.selector, sutra_id, features)
            if sutra is not None:
                applied.append(sutra)

        sutra = _try_apply(self.selector, "2.4.71", {"members": member_tuple, "surface": compound.surface})
        if sutra is not None:
            applied.append(sutra)
            operations.append("internal-sup-lopa")

        return CompoundEngineResult(
            compound=compound,
            sutra_ids=_unique_sutras(applied),
            operations=tuple(dict.fromkeys(operations)),
            engines=("SamasaDerivationEngine", "SutraPredicateSelectionEngine"),
        )


class KarakaVibhaktiEngine:
    """Adhyaya 1.4 kāraka plus Adhyaya 2.3 vibhakti selection."""

    KARAKA_SUTRAS: dict[tuple[str, str], str] = {
        ("", "separation_point"): "1.4.24",
        ("bhī", "cause_of_fear"): "1.4.25",
        ("trā", "cause_of_fear"): "1.4.25",
        ("", "intended_recipient"): "1.4.32",
        ("ruc", "pleased_one"): "1.4.33",
        ("", "most_effective_means"): "1.4.42",
        ("", "substratum"): "1.4.45",
        ("", "most_desired"): "1.4.49",
        ("", "ipsitatama"): "1.4.49",
        ("", "independent_agent"): "1.4.54",
    }

    ROLE_SUTRAS: dict[Role, str] = {
        Role.KARMAN: "2.3.2",
        Role.KARTR: "2.3.13",
        Role.KARANA: "2.3.14",
        Role.APADANA: "2.3.28",
        Role.SAMPRADANA: "2.3.36",
    }

    COMPANION_SUTRAS: dict[str, str] = {
        "antarā": "2.3.5",
        "antareṇa": "2.3.5",
        "namas": "2.3.16",
        "svasti": "2.3.16",
        "saha": "2.3.19",
    }

    SEMANTIC_SUTRAS: dict[str, str] = {
        "defective_limb": "2.3.20",
        "cause": "2.3.23",
        "between_karakas": "2.3.7",
        "excess_reference": "2.3.9",
        "motion_goal": "2.3.12",
        "tumun_purpose": "2.3.15",
        "disrespect_inanimate_manyate": "2.3.17",
        "agent_or_instrument": "2.3.18",
        "characteristic_mark": "2.3.21",
        "name_object": "2.3.22",
        "debt_without_agent": "2.3.24",
        "quality_relation": "2.3.25",
        "cause_genitive": "2.3.26",
        "pronoun_instrumental": "2.3.27",
        "stock_measure": "2.3.33",
    }

    def __init__(self, selector: SutraPredicateSelectionEngine | None = None) -> None:
        self.selector = selector or SutraPredicateSelectionEngine()

    def select_case(
        self,
        *,
        verb_lemma: str = "",
        semantic_role_context: str | None = None,
        role: Role | None = None,
        companion_lemma: str | None = None,
        is_already_expressed: bool = False,
        semantic_context: str | None = None,
    ) -> CaseSelectionResult:
        applied: list[AppliedSutra123] = []
        operations: list[str] = []

        resolved_role = role
        if resolved_role is None and semantic_role_context is not None:
            resolved_role = get_karaka_role(verb_lemma, semantic_role_context)
            sutra_id = self.KARAKA_SUTRAS.get((verb_lemma, semantic_role_context)) or self.KARAKA_SUTRAS.get(
                ("", semantic_role_context)
            )
            if sutra_id is not None:
                sutra = _try_apply(self.selector, sutra_id, {"verb": verb_lemma, "context": semantic_role_context})
                if sutra is not None:
                    applied.append(sutra)
                    operations.append(f"karaka:{resolved_role.value if resolved_role else 'none'}")

        case = get_vibhakti(resolved_role, companion_lemma, is_already_expressed, semantic_context)
        allowed = get_allowed_vibhaktis(resolved_role, companion_lemma, is_already_expressed, semantic_context)

        if is_already_expressed:
            applied.append(self.selector.apply("2.3.1", {"expressed": True, "case": Case.NOMINATIVE}))
            operations.append("anabhihite-blocked")
        elif resolved_role in self.ROLE_SUTRAS:
            sutra = _try_apply(self.selector, self.ROLE_SUTRAS[resolved_role], {"role": resolved_role})
            if sutra is not None:
                applied.append(sutra)
                operations.append(f"vibhakti:{case.value}")
        elif companion_lemma in self.COMPANION_SUTRAS:
            sutra = _try_apply(self.selector, self.COMPANION_SUTRAS[companion_lemma], {"companion": companion_lemma})
            if sutra is not None:
                applied.append(sutra)
                operations.append(f"upapada-vibhakti:{case.value}")
        elif semantic_context in self.SEMANTIC_SUTRAS:
            features: dict[str, Any] = {"semantic": semantic_context}
            if case in {Case.ACCUSATIVE, Case.ABLATIVE, Case.GENITIVE, Case.LOCATIVE}:
                features["case"] = case
            sutra = _try_apply(self.selector, self.SEMANTIC_SUTRAS[semantic_context], features)
            if sutra is not None:
                applied.append(sutra)
                operations.append(f"semantic-vibhakti:{case.value}")
        else:
            sutra = _try_apply(self.selector, "2.3.50", {"role": None})
            if sutra is not None:
                applied.append(sutra)
                operations.append("residual-genitive")

        return CaseSelectionResult(
            role=resolved_role,
            case=case,
            allowed_cases=allowed,
            explanation=explain_case(case),
            sutra_ids=_unique_sutras(applied),
            operations=tuple(dict.fromkeys(operations)),
            engines=("KarakaVibhaktiEngine", "SutraPredicateSelectionEngine"),
        )


class SubantaSupEngine:
    """Adhyaya 1.4/2 nominal sup engine."""

    def __init__(self, selector: SutraPredicateSelectionEngine | None = None) -> None:
        self.selector = selector or SutraPredicateSelectionEngine()

    def decline(
        self,
        stem: DeclensionStem,
        *,
        case: Case | None = None,
        number: GrammaticalNumber | None = None,
    ) -> SubantaEngineResult:
        forms = decline(stem)
        applied = [
            self.selector.apply("1.4.103", {"suffix_class": "sup"}),
            self.selector.apply("1.4.104", {"suffix_class": "sup", "is_vibhakti": True}),
        ]
        operations = ["sup-endings", f"declension:{stem.pattern.value}"]

        requested_form = None
        ending = None
        if case is not None and number is not None:
            requested_form = forms[(case, number)]
            if case != Case.VOCATIVE:
                ending = sup_ending(case, number)
            analysis = Analysis(
                surface=requested_form,
                lemma=stem.lemma,
                pos=PartOfSpeech.NOUN,
                case=case,
                gender=stem.gender,
                number=number,
            )
            sutra = _try_apply(self.selector, "1.4.14", {"analysis": analysis})
            if sutra is not None:
                applied.append(sutra)
                operations.append("pada-by-sup")

        return SubantaEngineResult(
            stem=stem,
            forms=forms,
            requested_form=requested_form,
            sup=ending,
            sutra_ids=_unique_sutras(applied),
            operations=tuple(dict.fromkeys(operations)),
            engines=("SubantaSupEngine", "SutraPredicateSelectionEngine"),
        )


class PratyayaLopaEngine:
    """Adhyaya 2.4 lopa/luk and root-substitution adapter."""

    ROOT_SUBSTITUTION_SUTRAS: tuple[tuple[str, str, Lakara, str], ...] = (
        ("2.4.36", "ad", Lakara.LRT, "jagdh"),
        ("2.4.37", "han", Lakara.ASHIRLING, "vadh"),
        ("2.4.42", "han", Lakara.LUN, "vadh"),
        ("2.4.45", "i", Lakara.LUN, "gā"),
        ("2.4.47", "cakṣ", Lakara.LAT, "khyā"),
        ("2.4.48", "i", Lakara.ASHIRLING, "gā"),
        ("2.4.52", "as", Lakara.LRT, "bhū"),
    )

    def __init__(self, selector: SutraPredicateSelectionEngine | None = None) -> None:
        self.selector = selector or SutraPredicateSelectionEngine()

    def substitute_dhatu(self, dhatu: Dhatu, lakara: Lakara) -> DhatuTransformResult:
        output = get_substituted_dhatu(dhatu, lakara)
        applied: list[AppliedSutra123] = []
        operations: list[str] = []
        for sutra_id, lemma, target_lakara, replacement in self.ROOT_SUBSTITUTION_SUTRAS:
            if dhatu.lemma != lemma or lakara != target_lakara or output.lemma != replacement:
                continue
            applied.append(self.selector.apply(sutra_id, {"lemma": dhatu.lemma, "lakara": lakara}))
            operations.append(f"dhatu-substitution:{replacement}")
            break

        return DhatuTransformResult(
            source=dhatu,
            output=output,
            lakara=lakara,
            luk_applies=False,
            sutra_ids=_unique_sutras(applied),
            operations=tuple(operations),
            engines=("PratyayaLopaEngine", "SutraPredicateSelectionEngine"),
        )

    def luk(self, dhatu: Dhatu, ending: TinEnding) -> DhatuTransformResult:
        applies = apply_luk_elision(dhatu, ending)
        applied = [self.selector.apply("2.4.72", {"lemma": dhatu.lemma})] if applies else []
        return DhatuTransformResult(
            source=dhatu,
            output=dhatu,
            lakara=ending.lakara,
            luk_applies=applies,
            sutra_ids=_unique_sutras(applied),
            operations=("luk-elision",) if applies else (),
            engines=("PratyayaLopaEngine", "SutraPredicateSelectionEngine"),
        )


class DhatuSanadiEngine:
    """Adhyaya 3.1 sanādi-dhātu and vikaraṇa engine."""

    TYPE_SUTRAS: dict[DhatuType, tuple[str, str]] = {
        DhatuType.DESIDERATIVE: ("3.1.5", "san"),
        DhatuType.DENOMINATIVE: ("3.1.8", "kyac"),
        DhatuType.INTENSIVE: ("3.1.22", "yaṅ"),
        DhatuType.CAUSATIVE: ("3.1.25", "ṇic"),
    }

    VIKARANA_SUTRAS: dict[int, tuple[str, str]] = {
        1: ("3.1.68", "a"),
        4: ("3.1.69", "ya"),
        5: ("3.1.73", "nu"),
        6: ("3.1.77", "a"),
        7: ("3.1.78", "na"),
        8: ("3.1.79", "u"),
        9: ("3.1.81", "nā"),
    }

    def __init__(self, selector: SutraPredicateSelectionEngine | None = None) -> None:
        self.selector = selector or SutraPredicateSelectionEngine()

    def derive(self, base: Dhatu, dhatu_type: DhatuType) -> DhatuDerivationResult:
        output = create_derived_dhatu(base, dhatu_type)
        applied: list[AppliedSutra123] = []
        operations: list[str] = [f"dhatu-type:{dhatu_type.value}"]
        if dhatu_type in self.TYPE_SUTRAS:
            sutra_id, kind = self.TYPE_SUTRAS[dhatu_type]
            applied.append(self.selector.apply(sutra_id, {"kind": kind}))
        return DhatuDerivationResult(
            source=base,
            output=output,
            dhatu_type=dhatu_type,
            sutra_ids=_unique_sutras(applied),
            operations=tuple(operations),
            engines=("DhatuSanadiEngine", "SutraPredicateSelectionEngine"),
        )

    def vikarana(self, varga: int) -> VikaranaResult:
        vikarana = get_vikarana(varga)
        applied: list[AppliedSutra123] = []
        if varga in self.VIKARANA_SUTRAS:
            sutra_id, _expected = self.VIKARANA_SUTRAS[varga]
            applied.append(self.selector.apply(sutra_id, {"varga": varga}))
        return VikaranaResult(
            varga=varga,
            vikarana=vikarana,
            sutra_ids=_unique_sutras(applied),
            operations=(f"vikarana:{vikarana}",),
            engines=("DhatuSanadiEngine", "SutraPredicateSelectionEngine"),
        )


class KrtDerivationEngine:
    """Adhyaya 3 kṛt suffix derivation engine."""

    KRT_SUTRA_CANDIDATES: tuple[str, ...] = (
        "3.1.91",
        "3.1.93",
        "3.2.1",
        "3.2.3",
        "3.2.16",
        "3.2.102",
        "3.2.135",
        "3.3.18",
        "3.3.94",
        "3.3.115",
        "3.3.121",
        "3.4.69",
        "3.4.71",
        "3.4.72",
    )

    def __init__(self, selector: SutraPredicateSelectionEngine | None = None) -> None:
        self.selector = selector or SutraPredicateSelectionEngine()

    def derive(self, source: str, suffix: KrtSuffix) -> KrtEngineResult:
        derived = derive(source, suffix)
        applied: list[AppliedSutra123] = []
        for sutra_id in self.KRT_SUTRA_CANDIDATES:
            sutra = _try_apply(self.selector, sutra_id, {"source": source, "suffix": suffix})
            if sutra is not None:
                applied.append(sutra)
                break
        return KrtEngineResult(
            derived=derived,
            sutra_ids=_unique_sutras(applied),
            operations=derived.operations or (f"krt:{suffix.value}",),
            engines=("KrtDerivationEngine", "SutraPredicateSelectionEngine"),
        )


class TinantaLakaraEngine:
    """Adhyaya 3 lakāra, tiṅ-ending, and conjugation engine."""

    TIME_SUTRAS: dict[TimeContext, str] = {
        TimeContext.PRESENT: "3.2.123",
        TimeContext.PAST: "3.2.110",
        TimeContext.PAST_BEFORE_TODAY: "3.2.111",
        TimeContext.FUTURE: "3.3.15",
        TimeContext.FUTURE_AFTER_TODAY: "3.3.33",
        TimeContext.CONDITIONAL: "3.3.139",
        TimeContext.POTENTIAL: "3.3.161",
        TimeContext.IMPERATIVE: "3.3.162",
    }

    def __init__(self, selector: SutraPredicateSelectionEngine | None = None) -> None:
        self.selector = selector or SutraPredicateSelectionEngine()

    def lakara_for_time(self, time: TimeContext) -> tuple[Lakara, AppliedSutra123 | None]:
        lakara = get_lakara_for_time(time)
        sutra_id = self.TIME_SUTRAS.get(time)
        sutra = self.selector.apply(sutra_id, {"time": time}) if sutra_id is not None else None
        return lakara, sutra

    def conjugate(
        self,
        dhatu: Dhatu,
        lakara: Lakara,
        *,
        person: Person | None = None,
        number: GrammaticalNumber | None = None,
    ) -> TinantaEngineResult:
        forms = conjugate(dhatu, lakara)
        applied: list[AppliedSutra123] = []
        operations: list[str] = []

        if is_sarvadhatuka(lakara):
            sutra = _try_apply(self.selector, "3.4.113", {"lakara": lakara})
            if sutra is not None:
                applied.append(sutra)
                operations.append("samjna:sarvadhatuka")
        if is_ardhadhatuka(lakara):
            sutra_id = "3.4.115" if lakara == Lakara.LIT else "3.4.114"
            sutra = _try_apply(self.selector, sutra_id, {"lakara": lakara})
            if sutra is not None:
                applied.append(sutra)
                operations.append("samjna:ardhadhatuka")

        if dhatu.pada == Pada.PARASMAIPADA:
            applied.append(
                self.selector.apply("1.4.99", {"label_origin": "l_substitute", "pada": "parasmaipada"})
            )
        elif dhatu.pada == Pada.ATMANEPADA:
            applied.append(self.selector.apply("1.4.100", {"ending_class": "tan", "pada": "atmanepada"}))

        requested_form = None
        ending_value = None
        if person is not None and number is not None:
            requested_form = forms[(person, number)]
            ending_value = tin_ending(lakara, dhatu.pada, person, number)
            label = "prathama" if person == Person.THIRD else "madhyama" if person == Person.SECOND else "uttama"
            sutra = _try_apply(self.selector, "1.4.101", {"suffix_class": "tin", "person_label": label})
            if sutra is not None:
                applied.append(sutra)
            sutra = _try_apply(self.selector, "1.4.102", {"suffix_class": "tin", "number": number.value})
            if sutra is not None:
                applied.append(sutra)
            operations.append(f"tin-ending:{ending_value}")

            surface_features = {"stem": dhatu.present_stem, "surface": requested_form}
            for sutra_id in ("3.4.79", "3.4.80", "3.4.86", "3.4.87", "3.4.88", "3.4.92", "3.4.100", "3.4.101", "3.4.108"):
                sutra = _try_apply(self.selector, sutra_id, surface_features)
                if sutra is not None:
                    applied.append(sutra)
                    operations.append(sutra.summary)

        return TinantaEngineResult(
            dhatu=dhatu,
            lakara=lakara,
            pada=dhatu.pada,
            forms=forms,
            requested_form=requested_form,
            ending=ending_value,
            sutra_ids=_unique_sutras(applied),
            operations=tuple(dict.fromkeys(operations)),
            engines=("TinantaLakaraEngine", "SutraPredicateSelectionEngine"),
        )


def classify_technical_names(*args: Any, **kwargs: Any) -> TechnicalNameResult:
    return SamjnaTechnicalEngine().classify(*args, **kwargs)


def derive_compound123(members: Sequence[Analysis], forced_type: SamasaType | None = None) -> CompoundEngineResult:
    return SamasaDerivationEngine().derive(members, forced_type=forced_type)


def select_vibhakti123(**kwargs: Any) -> CaseSelectionResult:
    return KarakaVibhaktiEngine().select_case(**kwargs)


def decline_subanta123(
    stem: DeclensionStem,
    *,
    case: Case | None = None,
    number: GrammaticalNumber | None = None,
) -> SubantaEngineResult:
    return SubantaSupEngine().decline(stem, case=case, number=number)


def derive_dhatu123(base: Dhatu, dhatu_type: DhatuType) -> DhatuDerivationResult:
    return DhatuSanadiEngine().derive(base, dhatu_type)


def derive_krt123(source: str, suffix: KrtSuffix) -> KrtEngineResult:
    return KrtDerivationEngine().derive(source, suffix)


def conjugate_tinanta123(
    dhatu: Dhatu,
    lakara: Lakara,
    *,
    person: Person | None = None,
    number: GrammaticalNumber | None = None,
) -> TinantaEngineResult:
    return TinantaLakaraEngine().conjugate(dhatu, lakara, person=person, number=number)

