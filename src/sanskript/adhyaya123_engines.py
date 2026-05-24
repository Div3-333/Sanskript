from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
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
from .derivation import DerivationFamily, DerivedForm, KrtSuffix, derive
from .grammar import Analysis, Case, Gender, GrammaticalNumber, Lakara, Pada, PartOfSpeech, Person, Role, Samjna
from .karaka import KarakaExplanation, explain_case, get_allowed_vibhaktis, get_karaka_role, get_vibhakti
from .markers import MarkerAnalysis, analyze_it_markers
from .paninian_effects import effects_from_assigned
from .phonology import (
    is_anunasika,
    is_pragrhya,
    is_samyoga,
    is_savarna,
    is_ti,
    is_upadha,
    savarna_reference,
    tapara_matches_duration,
    tokenize_sounds,
)
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
from .subanta import DeclensionStem, SupEnding, decline_paradigm, sup_ending
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
    conjugate_paradigm,
    create_derived_dhatu,
    get_lakara_for_time,
    get_substituted_dhatu,
    get_vikarana,
    is_ardhadhatuka,
    is_sarvadhatuka,
    join_stem_ending,
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
    assigned: tuple[str, ...] = ()
    extra_features: Mapping[str, Any] = field(default_factory=dict)


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
class SuffixElisionResult:
    source: str
    output: str
    target: str
    sutra_ids: tuple[str, ...]
    operations: tuple[str, ...]
    engines: tuple[str, ...]
    extra_features: Mapping[str, Any] = field(default_factory=dict)
    blocked_operations: frozenset[str] = frozenset()


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


@dataclass(frozen=True)
class Adhyaya3RealizationResult:
    input_form: str
    output_form: str
    sutra_ids: tuple[str, ...]
    operations: tuple[str, ...]
    engines: tuple[str, ...]
    features: Mapping[str, Any]
    dhatu: Dhatu | None = None
    blocked_by: tuple[str, ...] = ()


def _sutra_sort_key(sutra_id: str) -> tuple[int, ...]:
    return tuple(int(part) for part in sutra_id.split("."))


def _unique_sutras(applied: Iterable[AppliedSutra123]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(sutra.sutra_id for sutra in applied))


def _assigned_tags(applied: Iterable[AppliedSutra123]) -> tuple[str, ...]:
    tags: list[str] = []
    for sutra in applied:
        tags.extend(sutra.assigned)
    return tuple(dict.fromkeys(tags))


def _merge_assigned(*parts: Iterable[str]) -> tuple[str, ...]:
    tags: list[str] = []
    for part in parts:
        tags.extend(part)
    return tuple(dict.fromkeys(tags))


def _assigned_map(assigned: Iterable[str]) -> dict[str, str]:
    tags: dict[str, str] = {}
    for tag in assigned:
        if ":" not in tag or tag.startswith("sutra:"):
            continue
        head, _, tail = tag.partition(":")
        if head and tail:
            tags[head] = tail
    return tags


def _label(value: Any) -> str:
    if value is None:
        return ""
    if hasattr(value, "value"):
        return str(value.value)
    return str(value)


ROOT_NORMALIZATION: dict[str, str] = {
    "bhu": "bhū",
    "bhū": "bhū",
    "kr": "kṛ",
    "kṛ": "kṛ",
    "drs": "dṛś",
    "dṛś": "dṛś",
    "da": "dā",
    "dā": "dā",
    "dha": "dhā",
    "dhā": "dhā",
    "ni": "nī",
    "nī": "nī",
    "pa": "pā",
    "pā": "pā",
    "sr": "sṛ",
    "sru": "sṛ",
    "sṛ": "sṛ",
    "stha": "sthā",
    "sthā": "sthā",
    "dr": "dṛ",
    "dṛ": "dṛ",
    "sprs": "spṛś",
    "spṛś": "spṛś",
    "jna": "jñā",
    "jñā": "jñā",
}


RAW_SUFFIX_REALIZATIONS: dict[str, str] = {
    "aṇ": "a",
    "an": "a",
    "ac": "a",
    "a": "a",
    "ka": "a",
    "kah": "a",
    "ṭa": "ta",
    "ta": "ta",
    "tak": "taka",
    "ṭak": "taka",
    "kta": "ta",
    "ktavatu": "tavat",
    "ktvā": "tvā",
    "ktva": "tvā",
    "tumun": "itum",
    "tṛc": "tṛ",
    "trc": "tṛ",
    "ṇvul": "aka",
    "nvul": "aka",
    "vun": "aka",
    "ṣvun": "aka",
    "vunc": "aka",
    "nini": "in",
    "ṇini": "in",
    "nvin": "in",
    "ṇvi": "i",
    "viṭ": "it",
    "vit": "it",
    "kvin": "",
    "kvip": "",
    "ghañ": "a",
    "ghan": "a",
    "lyuṭ": "ana",
    "lyut": "ana",
    "gha": "a",
    "ktin": "ti",
    "śatṛ": "at",
    "satr": "at",
    "śānac": "māna",
    "sanac": "māna",
    "kvasu": "vas",
    "kānac": "āna",
    "kanac": "āna",
    "khal": "a",
    "ṇamul": "am",
    "namul": "am",
    "tosun": "tos",
    "kasun": "kas",
    "nyut": "ana",
    "ṇyuṭ": "ana",
    "yuc": "ana",
    "khaś": "a",
    "khas": "a",
    "khac": "aka",
    "khyun": "ana",
    "khiṣṇuc": "iṣṇu",
    "khisnuc": "iṣṇu",
    "kan": "aka",
    "manin": "man",
    "stran": "tra",
    "itra": "itra",
}


SANADI_SUFFIX_STEMS: dict[str, str] = {
    "san": "sa",
    "kyac": "īya",
    "kyaṅ": "īya",
    "kyang": "īya",
    "kyaṣ": "īya",
    "kyas": "īya",
    "kāmyac": "kāmya",
    "kamyac": "kāmya",
    "yaṅ": "ya",
    "yang": "ya",
    "ṇic": "aya",
    "nic": "aya",
    "ṇiṅ": "aya",
    "ning": "aya",
    "yak": "ya",
    "āya": "āya",
    "īyaṅ": "īya",
    "iyang": "īya",
}


def _normalize_root(root: Any) -> str:
    value = _label(root).strip()
    if not value:
        return "bhū"
    return ROOT_NORMALIZATION.get(value, value)


def _source_from_features(features: Mapping[str, Any], before: str = "") -> str:
    for key in ("source", "dhatu_lemma", "dhatu", "lemma", "upapada", "stem"):
        value = features.get(key)
        if value not in (None, "", ()):
            return _normalize_root(value)
    roots = features.get("roots")
    if isinstance(roots, (list, tuple)) and roots:
        return _normalize_root(roots[0])
    terms = features.get("terms")
    if isinstance(terms, (list, tuple)) and terms:
        return _normalize_root(terms[0])
    if before:
        return _normalize_root(before)
    return "bhū"


def _drop_final_a(stem: str) -> str:
    return stem[:-1] if stem.endswith("a") and len(stem) > 1 else stem


def _join_suffix(source: str, suffix: str) -> str:
    if not suffix:
        return source
    if source.endswith("a") and suffix.startswith("a"):
        return source[:-1] + suffix
    if source.endswith("ā") and suffix.startswith("a"):
        return source + "y" + suffix
    return source + suffix


def _generic_krt_surface(source: str, suffix_label: str) -> tuple[str, tuple[str, ...]]:
    label = suffix_label.strip()
    realized = RAW_SUFFIX_REALIZATIONS.get(label) or RAW_SUFFIX_REALIZATIONS.get(label.lower())
    operations: list[str] = [f"krt:{label}"]
    if realized is None:
        realized = "a"
        operations.append("contextual-krt-default-a")

    lexical: dict[tuple[str, str], str] = {
        ("bhū", "ghan"): "bhāva",
        ("bhū", "ghañ"): "bhāva",
        ("bhū", "lyuṭ"): "bhavana",
        ("bhū", "lyut"): "bhavana",
        ("kṛ", "aṇ"): "kāra",
        ("kṛ", "an"): "kāra",
        ("kṛ", "ṇvul"): "kāraka",
        ("kṛ", "nvul"): "kāraka",
        ("kṛ", "tṛc"): "kartṛ",
        ("kṛ", "trc"): "kartṛ",
        ("kṛ", "ktin"): "kṛti",
        ("dā", "ka"): "da",
        ("car", "ṭa"): "cara",
        ("car", "ta"): "cara",
        ("dṛś", "kta"): "dṛṣṭa",
        ("pac", "śatṛ"): "pacat",
        ("pac", "satr"): "pacat",
        ("labh", "śānac"): "labhamāna",
        ("labh", "sanac"): "labhamāna",
    }
    surface = lexical.get((source, label)) or lexical.get((source, label.lower()))
    if surface is not None:
        operations.append("lexical-krt-stem")
        return surface, tuple(operations)
    if realized == "":
        operations.append("zero-realized-krt")
        return source, tuple(operations)
    return _join_suffix(source, realized), tuple(operations)


def _generic_sanadi_stem(root: str, suffix_label: str, dhatu_type: DhatuType) -> str:
    suffix = SANADI_SUFFIX_STEMS.get(suffix_label) or SANADI_SUFFIX_STEMS.get(suffix_label.lower())
    if dhatu_type == DhatuType.DESIDERATIVE:
        desiderative: dict[str, str] = {
            "bhū": "bubhūṣa",
            "mān": "mimāṃsa",
            "dā": "ditsā",
            "gam": "jigamiṣa",
            "kṛ": "cikīrṣa",
            "han": "jighāṃsa",
        }
        return desiderative.get(root, f"di{root}sa")
    if dhatu_type == DhatuType.CAUSATIVE:
        causative: dict[str, str] = {
            "bhū": "bhāvaya",
            "dṛś": "darśaya",
            "gam": "gamaya",
            "kṛ": "kāraya",
        }
        return causative.get(root, _drop_final_a(root) + "aya")
    if dhatu_type == DhatuType.INTENSIVE:
        intensive: dict[str, str] = {
            "bhū": "bobhūya",
            "kṛ": "cakriya",
            "gam": "jaṅgamya",
        }
        return intensive.get(root, root[:1] + root + (suffix or "ya"))
    if suffix:
        return _join_suffix(root, suffix)
    return _join_suffix(root, "īya")


def _lakara_from_label(value: Any) -> Lakara | None:
    if isinstance(value, Lakara):
        return value
    label = _label(value)
    aliases = {
        "lat": Lakara.LAT,
        "laṭ": Lakara.LAT,
        "lan": Lakara.LAN,
        "laṅ": Lakara.LAN,
        "lit": Lakara.LIT,
        "liṭ": Lakara.LIT,
        "lun": Lakara.LUN,
        "luṅ": Lakara.LUN,
        "lrt": Lakara.LRT,
        "lṛṭ": Lakara.LRT,
        "lut": Lakara.LUT,
        "luṭ": Lakara.LUT,
        "lot": Lakara.LOT,
        "loṭ": Lakara.LOT,
        "lin": Lakara.VIDHILING,
        "liṅ": Lakara.VIDHILING,
        "vidhiliṅ": Lakara.VIDHILING,
        "vidhiling": Lakara.VIDHILING,
        "asisi": Lakara.ASHIRLING,
        "āśīrliṅ": Lakara.ASHIRLING,
        "ashirling": Lakara.ASHIRLING,
        "lrn": Lakara.LRN,
        "lṛṅ": Lakara.LRN,
        "let": Lakara.LET,
        "leṭ": Lakara.LET,
    }
    for item in Lakara:
        if label in {item.value, item.name, item.name.lower(), str(item)}:
            return item
    return aliases.get(label.lower())


def _pada_from_label(value: Any) -> Pada:
    if isinstance(value, Pada):
        return value
    label = _label(value).lower()
    if label in {"atmanepada", "ātmanepada", "aatmanepada", Pada.ATMANEPADA.value.lower()}:
        return Pada.ATMANEPADA
    return Pada.PARASMAIPADA


def _dhatu_type_from_label(value: Any) -> DhatuType | None:
    if isinstance(value, DhatuType):
        return value
    label = _label(value).lower()
    aliases = {
        "san": DhatuType.DESIDERATIVE,
        "desiderative": DhatuType.DESIDERATIVE,
        "kyac": DhatuType.DENOMINATIVE,
        "kyaṅ": DhatuType.DENOMINATIVE,
        "kyang": DhatuType.DENOMINATIVE,
        "kyaṣ": DhatuType.DENOMINATIVE,
        "kyas": DhatuType.DENOMINATIVE,
        "denominative": DhatuType.DENOMINATIVE,
        "yaṅ": DhatuType.INTENSIVE,
        "yang": DhatuType.INTENSIVE,
        "intensive": DhatuType.INTENSIVE,
        "ṇic": DhatuType.CAUSATIVE,
        "nic": DhatuType.CAUSATIVE,
        "causative": DhatuType.CAUSATIVE,
    }
    return aliases.get(label)


def _coerce_analysis(features: Mapping[str, Any]) -> Analysis | None:
    analysis = features.get("analysis")
    if isinstance(analysis, Analysis):
        return analysis
    surface = str(features.get("surface") or features.get("form") or features.get("term") or "")
    if not surface:
        return None
    lemma = str(features.get("lemma") or surface)
    pos = features.get("pos")
    if not isinstance(pos, PartOfSpeech):
        pos = PartOfSpeech.NOUN
    return Analysis(surface, lemma, pos)


GOVERNANCE_SUTRA_IDS = frozenset(
    {
        "1.1.21",
        "1.1.44",
        "1.1.46",
        "1.1.47",
        "1.1.48",
        "1.1.49",
        "1.1.50",
        "1.1.51",
        "1.1.52",
        "1.1.53",
        "1.1.54",
        "1.1.55",
        "1.1.56",
        "1.1.57",
        "1.1.58",
        "1.1.59",
        "1.1.69",
        "1.1.70",
        "1.1.71",
    }
)


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


def _analysis_surface(value: Any) -> str:
    if isinstance(value, Analysis):
        return value.surface
    return str(value or "")


def _feature_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if hasattr(value, "value"):
        return str(value.value)
    return str(value)


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

    def derive_for_sutra(self, sutra_id: str, features: Mapping[str, Any]) -> TechnicalNameResult | None:
        """Route a single Adhyāya 1 sutra through executable derivational logic."""
        if not sutra_id.startswith("1."):
            return None
        applied = _try_apply(self.selector, sutra_id, dict(features))
        if applied is None:
            return None

        operations: list[str] = []
        samjnas: set[Samjna] = set()
        analysis = _coerce_analysis(features)
        marker_analysis: MarkerAnalysis | None = None
        output_form = str(features.get("form") or features.get("surface") or features.get("term") or "")
        if not output_form and analysis is not None:
            output_form = analysis.surface

        parts = sutra_id.split(".")
        pada = int(parts[1]) if len(parts) >= 2 else 0

        if pada == 1 and sutra_id in {
            "1.1.11",
            "1.1.12",
            "1.1.13",
            "1.1.14",
            "1.1.15",
            "1.1.16",
            "1.1.17",
            "1.1.18",
            "1.1.19",
        }:
            token = features.get("analysis") or features.get("token")
            if is_pragrhya(token if isinstance(token, Analysis) else str(token or "")):
                operations.append("pragrhya-mark")
                if isinstance(token, Analysis):
                    analysis = token

        elif sutra_id == "1.1.7":
            sounds = list(features.get("sounds") or ())
            if is_samyoga(sounds):
                operations.append("samyoga-cluster")

        elif sutra_id == "1.1.8":
            sound = str(features.get("sound") or "")
            if is_anunasika(sound):
                operations.append("anunasika-mark")

        elif sutra_id == "1.1.9":
            left, right = str(features.get("left") or ""), str(features.get("right") or "")
            if is_savarna(left, right):
                operations.append("savarna-pair")

        elif sutra_id == "1.1.64":
            word = str(features.get("word") or output_form)
            ti = is_ti(word)
            operations.append(f"ti:{ti}")

        elif sutra_id == "1.1.65":
            word = str(features.get("word") or output_form)
            upadha = is_upadha(word)
            if upadha:
                operations.append(f"upadha:{upadha}")

        elif sutra_id.startswith("1.3."):
            upadesha = str(features.get("upadesha") or "")
            if upadesha:
                marker_kind = str(features.get("kind") or "suffix")
                marker_analysis = analyze_it_markers(
                    upadesha,
                    marker_kind,
                    bool(features.get("is_taddhita")),
                )
                if marker_analysis.markers:
                    operations.append("it-marker-extraction")
                if sutra_id == "1.3.9" and marker_analysis.lemma != upadesha:
                    output_form = marker_analysis.lemma
                    operations.append("it-lopa")

        elif pada == 4:
            if sutra_id in {"1.4.10", "1.4.11", "1.4.12"}:
                word = str(features.get("word") or output_form)
                index = int(features.get("index", 0))
                weight = get_vowel_weight(word, index)
                if weight is not None:
                    samjnas.add(weight)
                    operations.append(f"samjna:{weight.value}")
            elif analysis is not None:
                suffix_surface = str(features.get("suffix")) if features.get("suffix") else None
                analysis = assign_technical_names(analysis, suffix_surface)
                samjnas.update(analysis.samjnas)
                operations.append("samjna:technical-names")

        elif pada == 2 and sutra_id.startswith("1.2."):
            term = str(features.get("term") or features.get("root") or "")
            suffix = str(features.get("suffix")) if features.get("suffix") else None
            if term and is_ghu_root(term):
                samjnas.add(Samjna.GHU)
            if suffix and is_gha_suffix(suffix):
                samjnas.add(Samjna.GHA)
            if term and is_sarvanama_stem(term):
                samjnas.add(Samjna.SARVANAMA)
            accent = features.get("accent")
            if isinstance(accent, str) and accent:
                operations.append(f"accent:{accent}")

        tag_effects = effects_from_assigned(applied.assigned)
        if isinstance(tag_effects.get("samjnas"), frozenset):
            samjnas.update(tag_effects["samjnas"])
        if samjnas and (not operations or operations == ["samjna:technical-names"]):
            operations = [f"samjna:{samjna.value}" for samjna in sorted(samjnas, key=lambda item: item.value)]

        return TechnicalNameResult(
            term=str(features.get("term")) if features.get("term") else None,
            suffix=str(features.get("suffix")) if features.get("suffix") else None,
            analysis=analysis,
            marker_analysis=marker_analysis,
            samjnas=frozenset(samjnas),
            assigned=applied.assigned,
            sutra_ids=(sutra_id,),
            operations=tuple(dict.fromkeys(operations)) or (applied.summary,),
            engines=("SamjnaTechnicalEngine", "SutraPredicateSelectionEngine"),
        )

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
            sutra = _try_apply(self.selector, "1.1.43", {"suffix": suffix, "gender": gender})
            if sutra is not None:
                applied.append(sutra)

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

    def derive_for_sutra(self, sutra_id: str, features: Mapping[str, Any]) -> GovernanceResult | None:
        """Route paribhāṣā / substitution-site sutras through executable governance logic."""
        if sutra_id not in GOVERNANCE_SUTRA_IDS and not any(
            key in features for key in ("substitute", "marker", "reference_case", "expression", "text")
        ):
            return None
        applied = _try_apply(self.selector, sutra_id, dict(features))
        if applied is None and sutra_id not in GOVERNANCE_SUTRA_IDS:
            return None

        term = str(features.get("term") or features.get("form") or features.get("surface") or features.get("base") or "")
        extra: dict[str, Any] = {}
        assigned = applied.assigned if applied is not None else ()

        if sutra_id == "1.1.21":
            term = term or str(features.get("term") or "")
            extra.update(
                {
                    "boundary_roles": ("initial", "final"),
                    "target_scope": "single-sound",
                    "governance_effect": "single-sound-both-boundaries",
                }
            )
            return GovernanceResult(
                input_form=term,
                output_form=term,
                behavior=RuleBehavior.SUBSTITUTION,
                target_index=0 if term else None,
                target_scope="single-sound",
                sutra_ids=(sutra_id,),
                operations=("single-sound-both-boundaries",),
                engines=("MetaruleGovernanceEngine", "SutraPredicateSelectionEngine"),
                assigned=assigned,
                extra_features=extra,
            )
        if sutra_id == "1.1.48":
            sound = str(features.get("sound") or term)
            replacement = str(features.get("replacement") or "")
            extra.update({"target_sound": sound, "replacement": replacement, "substitute_channel": "hrasva"})
            return GovernanceResult(
                input_form=sound,
                output_form=replacement or sound,
                behavior=RuleBehavior.SUBSTITUTION,
                target_index=0 if sound else None,
                target_scope="ec-hrasva",
                sutra_ids=(sutra_id,),
                operations=("ec-hrasva-substitute",),
                engines=("MetaruleGovernanceEngine", "SutraPredicateSelectionEngine"),
                assigned=assigned,
                extra_features=extra,
            )
        if sutra_id == "1.1.51":
            target = str(features.get("target") or term)
            replacement = str(features.get("expected") or features.get("replacement") or "")
            extra.update({"target_sound": target, "replacement": replacement, "substitute_channel": "rapara"})
            return GovernanceResult(
                input_form=target,
                output_form=replacement or target,
                behavior=RuleBehavior.SUBSTITUTION,
                target_index=0 if target else None,
                target_scope="r-vocalic-substitute",
                sutra_ids=(sutra_id,),
                operations=("rapara-substitution",),
                engines=("MetaruleGovernanceEngine", "SutraPredicateSelectionEngine"),
                assigned=assigned,
                extra_features=extra,
            )
        if sutra_id == "1.1.44":
            expression = str(features.get("text") or features.get("expression") or "")
            result = self.optionality(expression)
            return GovernanceResult(
                input_form=result.input_form,
                output_form=result.output_form,
                behavior=result.behavior,
                target_index=result.target_index,
                target_scope=result.target_scope,
                sutra_ids=(sutra_id,),
                operations=result.operations,
                engines=result.engines,
                assigned=result.assigned or assigned,
                extra_features=dict(result.extra_features),
            )
        if sutra_id == "1.1.46":
            marker = str(features.get("marker") or "")
            base = str(features.get("base") or term)
            return self.augment_position(base, marker)
        if sutra_id == "1.1.47":
            marker = str(features.get("marker") or "m")
            base = str(features.get("base") or term)
            return self.augment_position(base, marker)
        if sutra_id == "1.1.54":
            return self.following_initial_site(term)
        if sutra_id in {"1.1.49", "1.1.52", "1.1.53", "1.1.55"} or features.get("substitute") is not None:
            result = self.substitution_site(
                term,
                substitute=str(features.get("substitute") or ""),
                marker=str(features.get("marker") or ""),
                reference_case=features.get("reference_case") or features.get("case") or "genitive",
            )
            extra = dict(effects_from_assigned(assigned))
            if result.target_index is not None:
                extra["substitution_index"] = result.target_index
            extra["target_scope"] = result.target_scope
            return GovernanceResult(
                input_form=result.input_form,
                output_form=result.output_form,
                behavior=result.behavior,
                target_index=result.target_index,
                target_scope=result.target_scope,
                sutra_ids=(sutra_id,),
                operations=result.operations,
                engines=result.engines,
                assigned=assigned,
                extra_features=extra,
            )
        if sutra_id == "1.1.69":
            sound = str(features.get("sound") or "")
            refs = savarna_reference(sound, bool(features.get("is_pratyaya")))
            if refs:
                extra["savarna_class"] = refs
                extra["phonological_labels"] = frozenset({"savarna"})
                return GovernanceResult(
                    input_form=term,
                    output_form=term,
                    behavior=RuleBehavior.SUBSTITUTION,
                    target_index=None,
                    target_scope="savarna-reference",
                    sutra_ids=(sutra_id,),
                    operations=("savarna-reference",),
                    engines=("MetaruleGovernanceEngine", "SutraPredicateSelectionEngine"),
                    assigned=assigned,
                    extra_features=extra,
                )
        if sutra_id == "1.1.70":
            sound = str(features.get("sound") or "")
            candidate = str(features.get("candidate") or "")
            if tapara_matches_duration(sound, candidate):
                extra["tapara_match"] = True
                extra["phonological_labels"] = frozenset({"duration"})
                return GovernanceResult(
                    input_form=term,
                    output_form=term,
                    behavior=RuleBehavior.SUBSTITUTION,
                    target_index=None,
                    target_scope="duration-match",
                    sutra_ids=(sutra_id,),
                    operations=("tapara-duration",),
                    engines=("MetaruleGovernanceEngine", "SutraPredicateSelectionEngine"),
                    assigned=assigned,
                    extra_features=extra,
                )
        if applied is not None:
            extra.update(effects_from_assigned(assigned))
            return GovernanceResult(
                input_form=term,
                output_form=term,
                behavior=RuleBehavior.SUBSTITUTION,
                target_index=features.get("index") if isinstance(features.get("index"), int) else None,
                target_scope=str(extra.get("target_scope") or sutra_id),
                sutra_ids=(sutra_id,),
                operations=(applied.summary,),
                engines=("MetaruleGovernanceEngine", "SutraPredicateSelectionEngine"),
                assigned=assigned,
                extra_features=extra,
            )
        return None

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
        applied_list: list[AppliedSutra123] = []
        if is_optional:
            sutra = _try_apply(self.selector, "1.1.44", {"text": expression, "expression": expression})
            if sutra is not None:
                applied_list.append(sutra)
        directive(expression, expression, RuleBehavior.OPTIONALITY, optional=is_optional)
        assigned = _assigned_tags(applied_list)
        extra = dict(effects_from_assigned(assigned))
        if is_optional:
            extra["optional"] = True
        return GovernanceResult(
            input_form=expression,
            output_form=expression,
            behavior=RuleBehavior.OPTIONALITY,
            target_index=None,
            target_scope="optional" if is_optional else "not-optional",
            sutra_ids=_unique_sutras(applied_list),
            operations=("vibhasha-optionality",) if is_optional else (),
            engines=("MetaruleGovernanceEngine", "SutraPredicateSelectionEngine"),
            assigned=assigned,
            extra_features=extra,
        )


class SamasaDerivationEngine:
    """Adhyaya 2 samāsa engine built on compound predicates and surface derivation."""

    def __init__(self, selector: SutraPredicateSelectionEngine | None = None) -> None:
        self.selector = selector or SutraPredicateSelectionEngine()

    def derive_for_sutra(self, sutra_id: str, features: Mapping[str, Any]) -> CompoundEngineResult | None:
        """Derive a concrete compound for a single 2.1/2.2 samasa rule."""
        if not sutra_id.startswith(("2.1.", "2.2.", "2.4.")):
            return None
        if sutra_id.startswith("2.4.") and not self._is_compound_feature_sutra(sutra_id, features):
            return None
        applied = _try_apply(self.selector, sutra_id, dict(features))
        if applied is None:
            return None

        members = self._members_from_features(sutra_id, features)
        if len(members) < 2:
            return None
        forced_type = self._forced_type_for_sutra(sutra_id, features)
        compound = create_compound(list(members), forced_type=forced_type)
        operations = [
            "samarthya",
            f"samasa:{compound.type.value}",
            f"samasa-sutra:{sutra_id}",
            "internal-sup-lopa",
        ]
        if compound.sense is not None:
            operations.append(f"sense:{compound.sense.value}")
        if compound.is_optional:
            operations.append("optionality")

        return CompoundEngineResult(
            compound=compound,
            sutra_ids=(sutra_id,),
            operations=tuple(dict.fromkeys(operations)),
            engines=("SamasaDerivationEngine", "SutraPredicateSelectionEngine"),
        )

    def _members_from_features(self, sutra_id: str, features: Mapping[str, Any]) -> tuple[Analysis, ...]:
        raw_members = features.get("members")
        if isinstance(raw_members, Sequence) and not isinstance(raw_members, (str, bytes)):
            members = tuple(member for member in raw_members if isinstance(member, Analysis))
            if len(members) >= 2:
                return members

        first = (
            features.get("first")
            or features.get("upapada")
            or features.get("companion")
            or features.get("base_lemma")
            or self._default_first_for_sutra(sutra_id, features)
        )
        second = (
            features.get("second")
            or features.get("uttarapada")
            or features.get("head")
            or features.get("kt_suffix")
            or features.get("semantic")
            or self._default_second_for_sutra(sutra_id, features)
        )
        first_text = _feature_text(first, "samartha")
        second_text = _feature_text(second, "artha")

        first_case = features.get("first_case")
        if not isinstance(first_case, Case):
            first_case = self._case_for_sutra(sutra_id)
        first_pos = PartOfSpeech.NUMERAL if features.get("is_numeral") or features.get("value") is not None else PartOfSpeech.NOUN
        first_value = int(features["value"]) if isinstance(features.get("value"), int) else None
        if (
            first_text in {"upa", "anu", "abhi", "prati", "āṅ", "nir"}
            and sutra_id.startswith("2.1.")
            and int(sutra_id.rsplit(".", 1)[1]) < 22
        ):
            first_pos = PartOfSpeech.INDECLINABLE

        second_case = features.get("second_case")
        if not isinstance(second_case, Case):
            second_case = Case.NOMINATIVE
        gender = features.get("gender")
        if not isinstance(gender, Gender):
            gender = Gender.MASCULINE

        return (
            Analysis(first_text, first_text, first_pos, case=first_case, gender=gender, value=first_value),
            Analysis(second_text, second_text, PartOfSpeech.NOUN, case=second_case, gender=gender),
        )

    def _is_compound_feature_sutra(self, sutra_id: str, features: Mapping[str, Any]) -> bool:
        serial = tuple(int(part) for part in sutra_id.split("."))
        if serial[0] == 2 and serial[1] == 4 and 1 <= serial[2] <= 34:
            return True
        return any(
            key in features
            for key in (
                "compound_type",
                "compound_lemma",
                "is_nadi_or_desha",
                "is_kshudra_jantava",
                "is_shasvata_virodha",
                "is_shudra_anirvasita",
                "is_vipratishiddha",
                "is_adhikarana_etavatva",
            )
        )

    def _forced_type_for_sutra(self, sutra_id: str, features: Mapping[str, Any]) -> SamasaType:
        explicit_type = features.get("compound_type")
        if isinstance(explicit_type, SamasaType):
            return explicit_type
        if isinstance(explicit_type, str):
            for item in SamasaType:
                if explicit_type in {item.value, item.name, item.name.lower()}:
                    return item

        serial = tuple(int(part) for part in sutra_id.split("."))
        if serial[0] == 2 and serial[1] == 4:
            if serial[2] in {2, 7, 8, 9, 10, 13, 15}:
                return SamasaType.DVANDVA
            if serial[2] in {17, 18, 20, 21, 22, 23, 24, 25}:
                return SamasaType.AVYAYIBHAVA
            return SamasaType.TATPURUSHA
        if sutra_id in {"2.1.21", "2.2.24", "2.2.25", "2.2.26", "2.2.27", "2.2.28", "2.2.35", "2.2.36", "2.2.37"}:
            return SamasaType.BAHUVRIHI
        if sutra_id == "2.2.38" or (serial[0] == 2 and serial[1] == 1 and serial[2] >= 55):
            return SamasaType.KARMADHARAYA
        if serial[0] == 2 and serial[1] == 1 and serial[2] <= 21:
            return SamasaType.AVYAYIBHAVA
        return SamasaType.TATPURUSHA

    def _case_for_sutra(self, sutra_id: str) -> Case:
        number = int(sutra_id.rsplit(".", 1)[1])
        if sutra_id.startswith("2.1."):
            if 24 <= number <= 28:
                return Case.ACCUSATIVE
            if 30 <= number <= 35:
                return Case.INSTRUMENTAL
            if 36 <= number <= 41:
                return Case.DATIVE
            if 42 <= number <= 48:
                return Case.ABLATIVE
            if 49 <= number <= 53:
                return Case.GENITIVE
            if 54 <= number <= 56:
                return Case.LOCATIVE
        return Case.NOMINATIVE

    def _default_first_for_sutra(self, sutra_id: str, features: Mapping[str, Any]) -> str:
        if features.get("compound_lemma"):
            return _feature_text(features.get("compound_lemma"))
        if features.get("is_nadi_or_desha"):
            return "gaṅgā"
        if features.get("is_kshudra_jantava"):
            return "makṣikā"
        if features.get("is_shasvata_virodha"):
            return "ahi"
        if features.get("is_shudra_anirvasita"):
            return "śūdra"
        if features.get("is_vipratishiddha"):
            return "vipratiṣiddha"
        if features.get("is_adhikarana_etavatva"):
            return "adhikaraṇa"
        if features.get("is_raja_first"):
            return "rājan"
        if features.get("is_upamana_first"):
            return "vyāghra"
        if features.get("is_kartri_karana"):
            return "kartṛ"
        if features.get("is_ekadeshin"):
            return "pūrva"
        return "samartha"

    def _default_second_for_sutra(self, sutra_id: str, features: Mapping[str, Any]) -> str:
        if features.get("compound_lemma"):
            return "pada"
        if features.get("is_nadi_or_desha"):
            return "deśa"
        if features.get("is_kshudra_jantava"):
            return "jantava"
        if features.get("is_shasvata_virodha"):
            return "nakula"
        if features.get("is_shudra_anirvasita"):
            return "jana"
        if features.get("is_vipratishiddha"):
            return "vacana"
        if features.get("is_adhikarana_etavatva"):
            return "mātra"
        if features.get("semantic_context"):
            return _feature_text(features.get("semantic_context"))
        if features.get("is_samanya_second"):
            return "puruṣa"
        if features.get("is_kshepa"):
            return "kṣepa"
        if features.get("is_ekadhikarana"):
            return "deśa"
        if features.get("upapada"):
            return "kāra"
        return "artha"

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
            if sutra_id == "2.4.27":
                lemmas = {member.lemma for member in member_tuple}
                if {"aśva", "vaḍava"} <= lemmas:
                    features["compound_type"] = compound.type
                    features["is_ashva_vadava"] = True
                    if compound.result_analysis is not None:
                        features["gender"] = compound.result_analysis.gender
                else:
                    continue
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
        "dūra": "2.3.35",
        "antika": "2.3.35",
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
        "adhigama": "2.3.52",
        "bhava_vacana": "2.3.54",
        "himsa": "2.3.56",
        "vyavahara": "2.3.57",
        "tadartha": "2.3.58",
        "vartamana_kta": "2.3.67",
        "adhikarana_krit": "2.3.68",
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
        forms = decline_paradigm(stem)
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
        ("2.4.49", "gā", Lakara.LIT, "gā"),
        ("2.4.52", "as", Lakara.LRT, "bhū"),
        ("2.4.55", "brū", Lakara.LIT, "brū"),
    )

    CONTEXTUAL_SUBSTITUTIONS: dict[str, tuple[str, str, str]] = {
        "2.4.41": ("ve", "vay", "root-substitution:vay"),
        "2.4.46": ("gam", "gāmay", "causative-root:gāmay"),
        "2.4.53": ("brū", "vac", "root-substitution:vac"),
        "2.4.54": ("cakṣ", "khyā", "root-substitution:khyā"),
    }

    def __init__(self, selector: SutraPredicateSelectionEngine | None = None) -> None:
        self.selector = selector or SutraPredicateSelectionEngine()

    def derive_for_sutra(self, sutra_id: str, features: Mapping[str, Any]) -> SuffixElisionResult | None:
        """Apply concrete 2.4 suffix elision/restriction behavior for one sutra."""
        if not sutra_id.startswith("2.4."):
            return None
        applied = _try_apply(self.selector, sutra_id, dict(features))
        if applied is None:
            return None

        target = self._elision_target(sutra_id, features)
        if applied.operator == "pratisedha":
            source = self._source_for_lopa(features)
            return SuffixElisionResult(
                source=source,
                output=source,
                target=target,
                sutra_ids=(sutra_id,),
                operations=(f"block-luk:{sutra_id}",),
                engines=("PratyayaLopaEngine", "SutraPredicateSelectionEngine"),
                extra_features={"lopa_target": target, "last_sutra": sutra_id},
                blocked_operations=frozenset({"luk"}),
            )

        contextual = self._contextual_substitution_result(sutra_id, features)
        if contextual is not None:
            return contextual

        suffix_surface = self._suffix_surface(sutra_id, features)
        if not target and not suffix_surface:
            return None
        base = self._base_for_lopa(features)
        if not base:
            return None
        source = str(features.get("form") or features.get("surface") or f"{base}+{suffix_surface or target}")
        output = self._remove_suffix(source, base, suffix_surface or target)
        operation_label = target or suffix_surface
        extra: dict[str, Any] = {
            "lopa_target": operation_label,
            "elided_suffix": suffix_surface or target,
            "last_sutra": sutra_id,
        }
        if features.get("suffix") is not None:
            extra["suffix"] = _feature_text(features.get("suffix"))
        if features.get("dhatu_lemma") is not None:
            extra["dhatu_lemma"] = features["dhatu_lemma"]
        if features.get("pada") is not None:
            extra["pada"] = features["pada"]
        if features.get("is_optional"):
            extra["optional"] = True

        return SuffixElisionResult(
            source=source,
            output=output,
            target=operation_label,
            sutra_ids=(sutra_id,),
            operations=(f"luk:{operation_label}", "suffix-elision"),
            engines=("PratyayaLopaEngine", "SutraPredicateSelectionEngine"),
            extra_features=extra,
        )

    def _base_for_lopa(self, features: Mapping[str, Any]) -> str:
        for key in ("dhatu_lemma", "lemma", "base_lemma", "source", "stem"):
            value = features.get(key)
            if value:
                return _feature_text(value)
        if features.get("is_avyaya"):
            return "avyaya"
        if features.get("suffix") is not None:
            return "prakṛti"
        if features.get("is_chandas"):
            return "chandas"
        if features.get("varga") == 3:
            return "juhotyādi"
        if features.get("is_yang"):
            return "yaṅ"
        return ""

    def _source_for_lopa(self, features: Mapping[str, Any]) -> str:
        base = self._base_for_lopa(features)
        suffix = _feature_text(features.get("suffix"))
        if base and suffix:
            return f"{base}+{suffix}"
        return base or suffix

    def _elision_target(self, sutra_id: str, features: Mapping[str, Any]) -> str:
        if sutra_id == "2.4.72":
            return "shap"
        if sutra_id in {"2.4.75", "2.4.76"}:
            return "shlu"
        if sutra_id in {"2.4.77", "2.4.78", "2.4.79"}:
            return "sic"
        if sutra_id in {"2.4.58", "2.4.59", "2.4.60", "2.4.62", "2.4.63", "2.4.64", "2.4.65", "2.4.66", "2.4.68", "2.4.69", "2.4.70"}:
            return "taddhita"
        if sutra_id == "2.4.73":
            return "chandas-luk"
        if sutra_id == "2.4.74":
            return "yang"
        if features.get("suffix") is not None:
            return _feature_text(features.get("suffix"))
        return _feature_text(features.get("target"))

    def _suffix_surface(self, sutra_id: str, features: Mapping[str, Any]) -> str:
        if sutra_id in {"2.4.72", "2.4.75", "2.4.76"}:
            return "a"
        if sutra_id in {"2.4.58", "2.4.59", "2.4.60", "2.4.62", "2.4.63", "2.4.64", "2.4.65", "2.4.66", "2.4.68", "2.4.69", "2.4.70"}:
            return _feature_text(features.get("suffix"), "taddhita")
        if sutra_id == "2.4.73":
            return "sup"
        if sutra_id == "2.4.74":
            return "yaṅ"
        return _feature_text(features.get("suffix"))

    def _contextual_substitution_result(
        self,
        sutra_id: str,
        features: Mapping[str, Any],
    ) -> SuffixElisionResult | None:
        if sutra_id in self.CONTEXTUAL_SUBSTITUTIONS:
            fallback_source, output, operation = self.CONTEXTUAL_SUBSTITUTIONS[sutra_id]
            source = _feature_text(features.get("dhatu_lemma"), fallback_source)
            return SuffixElisionResult(
                source=source,
                output=output,
                target=output,
                sutra_ids=(sutra_id,),
                operations=(operation, "dhatu-substitution"),
                engines=("PratyayaLopaEngine", "SutraPredicateSelectionEngine"),
                extra_features={
                    "dhatu_lemma": source,
                    "lemma": output,
                    "root_substitution": output,
                    "derivation_family": "dhatu-substitution",
                    "last_sutra": sutra_id,
                },
            )
        if sutra_id in {"2.4.40", "2.4.43", "2.4.44", "2.4.50"}:
            lakara = features.get("lakara")
            pada = features.get("pada")
            optional = bool(features.get("is_optional"))
            domain = _feature_text(lakara, "lakara")
            if pada is not None:
                domain = _feature_text(pada, domain)
            operations = [f"dhatu-substitution-domain:{domain}"]
            if optional:
                operations.append("optionality")
            return SuffixElisionResult(
                source=domain,
                output=domain,
                target=domain,
                sutra_ids=(sutra_id,),
                operations=tuple(operations),
                engines=("PratyayaLopaEngine", "SutraPredicateSelectionEngine"),
                extra_features={
                    "lakara": lakara,
                    "pada": pada,
                    "optional_substitution": optional,
                    "derivation_domain": domain,
                    "derivation_family": "dhatu-substitution",
                    "last_sutra": sutra_id,
                },
            )
        if sutra_id == "2.4.85":
            return SuffixElisionResult(
                source="luṭ-prathama",
                output="ḍā/rau/ras",
                target="ḍā-rau-ras",
                sutra_ids=(sutra_id,),
                operations=("tin-replacement:ḍā-rau-ras",),
                engines=("PratyayaLopaEngine", "SutraPredicateSelectionEngine"),
                extra_features={
                    "lakara": features.get("lakara"),
                    "person": features.get("person"),
                    "tin_replacement": ("ḍā", "rau", "ras"),
                    "derivation_family": "tin-substitution",
                    "last_sutra": sutra_id,
                },
            )
        return None

    def _remove_suffix(self, source: str, base: str, suffix: str) -> str:
        if "+" in source:
            return source.split("+", 1)[0]
        if suffix and source.endswith(suffix):
            return source[: -len(suffix)]
        return base

    def substitute_dhatu(self, dhatu: Dhatu, lakara: Lakara) -> DhatuTransformResult:
        output = get_substituted_dhatu(dhatu, lakara)
        applied: list[AppliedSutra123] = []
        operations: list[str] = []
        for sutra_id, lemma, target_lakara, replacement in self.ROOT_SUBSTITUTION_SUTRAS:
            if dhatu.lemma != lemma or lakara != target_lakara or output.lemma != replacement:
                continue
            sutra = _try_apply(self.selector, sutra_id, {"lemma": dhatu.lemma, "dhatu_lemma": dhatu.lemma, "lakara": lakara})
            if sutra is not None:
                applied.append(sutra)
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

    def derive(self, source: str, suffix: KrtSuffix | str) -> KrtEngineResult:
        if isinstance(suffix, KrtSuffix):
            derived = derive(source, suffix)
        else:
            surface, operations = _generic_krt_surface(source, str(suffix))
            derived = DerivedForm(
                source,
                suffix,
                DerivationFamily.KRT,
                surface,
                f"{suffix} of {source}",
                semantic="contextual-krt",
                operations=operations,
            )
        applied: list[AppliedSutra123] = []
        if isinstance(suffix, KrtSuffix):
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
        forms = conjugate_paradigm(dhatu, lakara)
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


class AdhyayaThreeRealizationEngine:
    """Dry real-effect adapter for the Adhyaya 3 predicate canon.

    The discrete sutra predicates decide *when* a rule fires. This adapter turns
    that decision into a concrete derivational artifact: a sanadi stem, vikarana
    stem, krt form, lakara/tin form, suffix-class state, or pratisedha block.
    """

    META_EFFECTS: dict[str, tuple[str, dict[str, Any]]] = {
        "3.1.1": ("govern-pratyaya-domain", {"derivation_domain": "pratyaya", "suffix_may_attach": True}),
        "3.1.2": ("place-suffix-after-base", {"suffix_position": "after-base"}),
        "3.1.3": ("mark-initial-udatta", {"accent_pattern": "initial-udatta"}),
        "3.1.4": ("mark-anudatta-sup-pit", {"accent_pattern": "anudatta"}),
        "3.1.91": ("govern-krt-after-dhatu", {"derivation_domain": "dhatu-krt"}),
        "3.1.92": ("govern-upapada", {"derivation_domain": "upapada-krt"}),
        "3.1.93": ("classify-krt", {"suffix_class": "krt"}),
        "3.1.94": ("license-alternate-krt", {"optional": True, "suffix_alternation": "asarupa"}),
        "3.1.95": ("govern-krtya", {"suffix_class": "krtya"}),
        "3.4.1": ("govern-dhatu-relation", {"derivation_domain": "dhatu-sambandha"}),
        "3.4.67": ("govern-agent-krt", {"semantic": "kartari"}),
        "3.4.70": ("govern-krtya-kta-khal", {"suffix_class": "krtya-kta-khal"}),
        "3.4.77": ("open-la-replacement", {"derivation_domain": "la-replacement"}),
    }

    TIN_CLASS_EFFECTS: dict[str, tuple[str, str]] = {
        "3.4.113": ("samjna:sarvadhatuka", "sarvadhatuka"),
        "3.4.114": ("samjna:ardhadhatuka", "ardhadhatuka"),
        "3.4.115": ("samjna:ardhadhatuka", "ardhadhatuka"),
    }

    def __init__(
        self,
        *,
        selector: SutraPredicateSelectionEngine | None = None,
        krt: KrtDerivationEngine | None = None,
        tinanta: TinantaLakaraEngine | None = None,
        sanadi: DhatuSanadiEngine | None = None,
    ) -> None:
        self.selector = selector or SutraPredicateSelectionEngine()
        self.krt = krt or KrtDerivationEngine(self.selector)
        self.tinanta = tinanta or TinantaLakaraEngine(self.selector)
        self.sanadi = sanadi or DhatuSanadiEngine(self.selector)

    def derive_for_sutra(
        self,
        sutra_id: str,
        features: Mapping[str, Any],
        assigned: Iterable[str],
        *,
        before: str = "",
        dhatu: Dhatu | None = None,
        source: str = "",
        suffix: KrtSuffix | str | None = None,
        lakara: Lakara | None = None,
        pada: Pada | None = None,
        person: Person | None = None,
        number: GrammaticalNumber | None = None,
        operator: str = "vidhi",
    ) -> Adhyaya3RealizationResult | None:
        assigned_tags = _assigned_map(assigned)
        merged = dict(features)
        if source:
            merged.setdefault("source", source)
        if suffix is not None:
            merged.setdefault("suffix", suffix)
        if lakara is not None:
            merged.setdefault("lakara", lakara)
        if pada is not None:
            merged.setdefault("pada", pada)
        if person is not None:
            merged.setdefault("person", person)
        if number is not None:
            merged.setdefault("number", number)

        if operator == "pratisedha":
            return self._block_result(sutra_id, merged, assigned_tags, before)

        if sutra_id in self.TIN_CLASS_EFFECTS:
            operation, class_name = self.TIN_CLASS_EFFECTS[sutra_id]
            return self._state_result(
                sutra_id,
                before,
                "TinantaLakaraEngine",
                operation,
                {
                    "suffix_class": class_name,
                    "derivation_family": "tinanta",
                    "engine_operation": operation,
                    "lakara": _lakara_from_label(merged.get("lakara") or assigned_tags.get("lakara")) or merged.get("lakara"),
                },
            )

        if sutra_id in self.META_EFFECTS:
            operation, extra = self.META_EFFECTS[sutra_id]
            payload = dict(extra)
            payload["engine_operation"] = operation
            payload["derivation_family"] = "adhyaya3-governance"
            if merged.get("suffix") is not None:
                payload["applied_suffix"] = _label(merged.get("suffix"))
            return self._state_result(sutra_id, before, "MetaruleGovernanceEngine", operation, payload)

        section, index_text = sutra_id.rsplit(".", 1)
        index = int(index_text)
        suffix_value = suffix or merged.get("suffix") or assigned_tags.get("suffix")
        suffix_label = _label(suffix_value)
        lakara_value = _lakara_from_label(lakara or merged.get("lakara") or assigned_tags.get("lakara"))
        dhatu_type = (
            _dhatu_type_from_label(merged.get("dhatu_type"))
            or _dhatu_type_from_label(merged.get("kind"))
            or _dhatu_type_from_label(assigned_tags.get("dhatu-type"))
        )
        source_value = _source_from_features(merged, before)
        if dhatu is None:
            dhatu = self._dhatu_from_context(source_value, merged, pada)

        if section == "3.1" and (index <= 32 or dhatu_type is not None):
            return self._derive_sanadi(sutra_id, merged, dhatu, dhatu_type, suffix_label, before)

        if section == "3.1" and 33 <= index <= 90 and (merged.get("varga") is not None or assigned_tags.get("vikarana") or suffix_label):
            return self._derive_vikarana(sutra_id, merged, source_value, suffix_label, assigned_tags, before)

        if lakara_value is not None or assigned_tags.get("lakara") or (section == "3.4" and index >= 77):
            return self._derive_tinanta(
                sutra_id,
                merged,
                dhatu,
                lakara_value or Lakara.LAT,
                pada,
                person,
                number,
                assigned_tags,
                before,
            )

        if suffix_label or assigned_tags.get("suffix") or assigned_tags.get("derived"):
            return self._derive_krt(sutra_id, merged, source_value, suffix_value, assigned_tags, before)

        return None

    def _state_result(
        self,
        sutra_id: str,
        before: str,
        engine: str,
        operation: str,
        features: Mapping[str, Any],
    ) -> Adhyaya3RealizationResult:
        return Adhyaya3RealizationResult(
            input_form=before,
            output_form=before,
            sutra_ids=(sutra_id,),
            operations=(operation,),
            engines=(engine, "SutraPredicateSelectionEngine"),
            features={**features, "last_sutra": sutra_id},
        )

    def _block_result(
        self,
        sutra_id: str,
        features: Mapping[str, Any],
        assigned: Mapping[str, str],
        before: str,
    ) -> Adhyaya3RealizationResult:
        target = assigned.get("suffix") or assigned.get("lakara") or _label(features.get("suffix") or features.get("lakara")) or "derivation"
        operation = f"block:{target}"
        return Adhyaya3RealizationResult(
            input_form=before,
            output_form=before,
            sutra_ids=(sutra_id,),
            operations=(operation,),
            engines=("AdhyayaThreeRealizationEngine", "SutraPredicateSelectionEngine"),
            features={
                "blocked_operations": frozenset({target}),
                "engine_operation": operation,
                "derivation_family": "pratisedha",
                "last_sutra": sutra_id,
            },
            blocked_by=(sutra_id,),
        )

    def _dhatu_from_context(self, source: str, features: Mapping[str, Any], pada: Pada | None) -> Dhatu:
        parsed_pada = _pada_from_label(pada or features.get("pada"))
        stem = _label(features.get("present_stem") or features.get("stem")) or self._present_stem(source)
        return Dhatu(source, stem, parsed_pada, _label(features.get("gloss")) or source, varga=int(features.get("varga", 1) or 1))

    def _derive_sanadi(
        self,
        sutra_id: str,
        features: Mapping[str, Any],
        dhatu: Dhatu,
        dhatu_type: DhatuType | None,
        suffix_label: str,
        before: str,
    ) -> Adhyaya3RealizationResult:
        selected_type = dhatu_type or DhatuType.DENOMINATIVE
        root = _normalize_root(dhatu.lemma)
        try:
            result = self.sanadi.derive(Dhatu(root, self._present_stem(root), dhatu.pada, dhatu.gloss), selected_type)
            output = result.output
            surface = output.present_stem
            operations = tuple(result.operations)
        except (KeyError, TypeError, ValueError):
            stem = _generic_sanadi_stem(root, suffix_label, selected_type)
            output = Dhatu(f"{root}-{suffix_label or selected_type.value}", stem, dhatu.pada, dhatu.gloss, type=selected_type, base_dhatu=dhatu)
            surface = stem
            operations = (f"sanadi:{suffix_label or selected_type.value}",)
        canonical_surface = _generic_sanadi_stem(root, suffix_label, selected_type)
        if canonical_surface and canonical_surface != surface:
            surface = canonical_surface
            output = Dhatu(
                f"{root}-{suffix_label or selected_type.value}",
                surface,
                dhatu.pada,
                dhatu.gloss,
                type=selected_type,
                base_dhatu=dhatu,
            )
        if surface == root or not surface:
            surface = _generic_sanadi_stem(root, suffix_label, selected_type)
            output = Dhatu(f"{root}-{suffix_label or selected_type.value}", surface, dhatu.pada, dhatu.gloss, type=selected_type, base_dhatu=dhatu)
        operation_tuple = tuple(dict.fromkeys((*operations, f"dhatu-type:{selected_type.value}", f"stem:{surface}")))
        return Adhyaya3RealizationResult(
            input_form=before or root,
            output_form=surface,
            sutra_ids=(sutra_id,),
            operations=operation_tuple,
            engines=("DhatuSanadiEngine", "SutraPredicateSelectionEngine"),
            features={
                "source": root,
                "lemma": output.lemma,
                "dhatu_lemma": output.lemma,
                "dhatu_type": selected_type,
                "applied_suffix": suffix_label or selected_type.value,
                "derived_stem": surface,
                "derivation_family": "sanadi-dhatu",
                "derivation_operations": operation_tuple,
                "engine_operation": "sanadi-dhatu",
                "last_sutra": sutra_id,
            },
            dhatu=output,
        )

    def _derive_vikarana(
        self,
        sutra_id: str,
        features: Mapping[str, Any],
        source: str,
        suffix_label: str,
        assigned: Mapping[str, str],
        before: str,
    ) -> Adhyaya3RealizationResult:
        raw_varga = features.get("varga")
        varga = int(raw_varga or 0) if str(raw_varga or "").isdigit() else 0
        vikarana = _label(features.get("vikarana") or assigned.get("vikarana") or suffix_label)
        if varga:
            vikarana = get_vikarana(varga)
        if vikarana in {"contextual", "pratyaya", ""}:
            vikarana = RAW_SUFFIX_REALIZATIONS.get(suffix_label) or "a"
        surface = _join_suffix(source, vikarana)
        operations = tuple(dict.fromkeys((f"vikarana:{vikarana}", f"present-stem:{surface}")))
        return Adhyaya3RealizationResult(
            input_form=before or source,
            output_form=surface,
            sutra_ids=(sutra_id,),
            operations=operations,
            engines=("DhatuSanadiEngine", "SutraPredicateSelectionEngine"),
            features={
                "source": source,
                "dhatu_lemma": source,
                "varga": varga,
                "vikarana": vikarana,
                "derived_stem": surface,
                "derivation_family": "vikarana",
                "derivation_operations": operations,
                "engine_operation": "vikarana",
                "last_sutra": sutra_id,
            },
        )

    def _derive_krt(
        self,
        sutra_id: str,
        features: Mapping[str, Any],
        source: str,
        suffix: KrtSuffix | str | None,
        assigned: Mapping[str, str],
        before: str,
    ) -> Adhyaya3RealizationResult:
        suffix_value: KrtSuffix | str = suffix if suffix is not None else assigned.get("suffix", "a")
        if assigned.get("derived"):
            surface = assigned["derived"]
            suffix_label = _label(suffix_value)
            operations = (f"krt:{suffix_label or 'assigned'}", "assigned-derived-surface")
            derived = DerivedForm(source, suffix_value, DerivationFamily.KRT, surface, f"{suffix_label} of {source}", sutra_id, operations=operations)
        else:
            result = self.krt.derive(source, suffix_value)
            derived = result.derived
            operations = result.operations or (f"krt:{_label(suffix_value)}",)
        suffix_label = _label(suffix_value)
        if derived.surface == source and suffix_label not in {"kvin", "kvip"}:
            surface, fallback_ops = _generic_krt_surface(source, suffix_label)
            derived = DerivedForm(source, suffix_value, DerivationFamily.KRT, surface, derived.gloss, sutra_id, operations=fallback_ops)
            operations = fallback_ops
        op_list = list(operations)
        if features.get("upapada"):
            op_list.append(f"upapada:{features['upapada']}")
        operations_tuple = tuple(dict.fromkeys(op_list))
        return Adhyaya3RealizationResult(
            input_form=before or source,
            output_form=derived.surface,
            sutra_ids=(sutra_id,),
            operations=operations_tuple,
            engines=("KrtDerivationEngine", "SutraPredicateSelectionEngine"),
            features={
                "source": source,
                "dhatu_lemma": features.get("dhatu_lemma") or source,
                "suffix": suffix_label,
                "applied_suffix": suffix_label,
                "derived_form": derived.surface,
                "derivation_family": "krt",
                "derivation_operations": operations_tuple,
                "engine_operation": "krt-derivation",
                "semantic": features.get("semantic"),
                "upapada": features.get("upapada"),
                "last_sutra": sutra_id,
            },
        )

    def _derive_tinanta(
        self,
        sutra_id: str,
        features: Mapping[str, Any],
        dhatu: Dhatu,
        lakara: Lakara,
        pada: Pada | None,
        person: Person | None,
        number: GrammaticalNumber | None,
        assigned: Mapping[str, str],
        before: str,
    ) -> Adhyaya3RealizationResult:
        selected_pada = _pada_from_label(pada or features.get("pada") or dhatu.pada)
        selected_person = person if isinstance(person, Person) else Person.THIRD
        if isinstance(features.get("person"), Person):
            selected_person = features["person"]
        selected_number = number if isinstance(number, GrammaticalNumber) else GrammaticalNumber.SINGULAR
        if isinstance(features.get("number"), GrammaticalNumber):
            selected_number = features["number"]
        working_dhatu = Dhatu(dhatu.lemma, dhatu.present_stem, selected_pada, dhatu.gloss, dhatu.varga, dhatu.markers, dhatu.type, dhatu.base_dhatu)
        try:
            result = self.tinanta.conjugate(working_dhatu, lakara, person=selected_person, number=selected_number)
            surface = result.requested_form or self._fallback_tinanta(working_dhatu, lakara, selected_person, selected_number)
            ending = result.ending
            operations = result.operations or (f"lakara:{lakara.value}",)
        except (KeyError, TypeError, ValueError):
            surface = self._fallback_tinanta(working_dhatu, lakara, selected_person, selected_number)
            ending = assigned.get("ending") or assigned.get("operation") or "tin"
            operations = (f"lakara:{lakara.value}", f"tin-ending:{ending}")
        if assigned.get("ending") and assigned["ending"] not in surface:
            surface = _join_suffix(_drop_final_a(working_dhatu.present_stem), assigned["ending"])
            operations = tuple(dict.fromkeys((*operations, f"ending:{assigned['ending']}")))
        if assigned.get("augment"):
            surface = assigned["augment"] + surface
            operations = tuple(dict.fromkeys((*operations, f"augment:{assigned['augment']}")))
        return Adhyaya3RealizationResult(
            input_form=before or working_dhatu.present_stem,
            output_form=surface,
            sutra_ids=(sutra_id,),
            operations=tuple(dict.fromkeys(operations)),
            engines=("TinantaLakaraEngine", "SutraPredicateSelectionEngine"),
            features={
                "source": working_dhatu.lemma,
                "dhatu_lemma": working_dhatu.lemma,
                "lakara": lakara,
                "pada": selected_pada,
                "person": selected_person,
                "number": selected_number,
                "ending": ending,
                "derived_form": surface,
                "derivation_family": "tinanta",
                "derivation_operations": tuple(dict.fromkeys(operations)),
                "engine_operation": "tinanta-derivation",
                "last_sutra": sutra_id,
            },
            dhatu=working_dhatu,
        )

    def _fallback_tinanta(
        self,
        dhatu: Dhatu,
        lakara: Lakara,
        person: Person,
        number: GrammaticalNumber,
    ) -> str:
        stem = _normalize_root(dhatu.lemma)
        if lakara == Lakara.LRT:
            return _drop_final_a(self._present_stem(stem)) + "iṣyati"
        if lakara == Lakara.LUT:
            return stem + "tā"
        if lakara == Lakara.LOT:
            return _drop_final_a(self._present_stem(stem)) + "atu"
        if lakara == Lakara.VIDHILING:
            return _drop_final_a(self._present_stem(stem)) + "et"
        if lakara == Lakara.ASHIRLING:
            return stem + "yāt"
        if lakara == Lakara.LAN:
            return "a" + _drop_final_a(self._present_stem(stem)) + "at"
        if lakara == Lakara.LUN:
            if stem == "bhū":
                return "abhūt"
            return "a" + stem + "t"
        if lakara == Lakara.LIT:
            if stem == "bhū":
                return "babhūva"
            return stem[:1] + stem + "a"
        if lakara == Lakara.LET:
            return _drop_final_a(self._present_stem(stem)) + "at"
        return join_stem_ending(self._present_stem(stem), TinEnding(lakara, dhatu.pada, person, number, "ti"), dhatu)

    def _present_stem(self, root: str) -> str:
        stems = {
            "bhū": "bhava",
            "kṛ": "kuru",
            "dṛś": "paśya",
            "gam": "gaccha",
            "dā": "dadā",
            "dhā": "dadhā",
            "as": "as",
            "pac": "paca",
            "car": "cara",
            "labh": "labha",
        }
        if root in stems:
            return stems[root]
        return _join_suffix(root, "a")


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
