from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .derivation import (
    DerivationFamily,
    TADDHITA_RULES,
    TaddhitaSuffix,
    _apply_initial_vrddhi,
    _derive_apatya,
    _derive_atishayana,
    _derive_matup,
)


FeatureMap = Mapping[str, Any]


@dataclass(frozen=True)
class AppliedSutra:
    sutra_id: str
    context: dict[str, Any]
    operator: str
    summary: str
    module: str


@dataclass(frozen=True)
class SelectedPratyaya:
    source: str
    suffix: str | TaddhitaSuffix | None
    semantic: str
    sutra: AppliedSutra


@dataclass(frozen=True)
class EngineDerivation:
    source: str
    surface: str
    suffix: str | TaddhitaSuffix | None
    semantic: str
    family: str
    sutra_ids: tuple[str, ...]
    operations: tuple[str, ...]
    gloss: str
    engines: tuple[str, ...]
    state_features: tuple[tuple[str, Any], ...] = ()


@dataclass(frozen=True)
class ContinuationAnuvritti:
    inherited_from: str
    suffix: str | TaddhitaSuffix | None = None
    operation: str | None = None


_INLINE_STRI_SUTRAS = frozenset({"4.1.2"})

_UNRELIABLE_SOURCE_TOKENS = frozenset(
    {
        "ordinary",
        "different",
        "non",
        "samjna",
        "saṃjñā",
        "semantic",
        "taddhita",
        "continuation",
    }
)

_SEMANTIC_SOURCE_HINTS: dict[str, str] = {
    "kaumāra": "kumāra",
    "tasmai": "bala",
    "tasya": "deva",
    "asya": "deva",
    "tena": "daṇḍa",
    "tatra": "grāma",
    "tadartha": "artha",
    "tada": "deva",
    "tam": "deva",
    "kāla": "māsa",
    "samūha": "jana",
    "bhāva": "śukla",
    "arha": "rāja",
    "tulya": "sama",
}


def _source_token(value: str) -> str:
    token = value.split("_")[0]
    stripped_adi = False
    for ending in ("ādi", "adi"):
        if token.endswith(ending) and len(token) > len(ending):
            token = token[: -len(ending)]
            stripped_adi = True
            break
    if token in _UNRELIABLE_SOURCE_TOKENS:
        return ""
    if stripped_adi and token and not token.endswith(("a", "ā", "i", "ī", "u", "ū", "e", "o", "ṛ", "ṝ")):
        return token + "a"
    return token


def resolve_adhyaya45_source(features: Mapping[str, Any] | None) -> str:
    """Pick a reliable derivational base from explicit or structural state keys.

    This deliberately does not mine arbitrary semantic labels such as
    ``tasmai_hita`` for a stem. Semantic-only continuation rules get a
    representative source later, where the rule id and inherited suffix are
    available and the operation can be marked as anuvṛtti-driven.
    """
    if not features:
        return ""
    for key in ("source", "stem", "lemma", "form", "surface", "term"):
        value = features.get(key)
        if isinstance(value, str) and value:
            return value
    purva = features.get("purva_pada")
    stem = features.get("stem")
    if isinstance(purva, str) and purva and isinstance(stem, str) and stem:
        return purva + stem
    for key in ("stem_final", "purva_pada", "stem_class"):
        value = features.get(key)
        if not isinstance(value, str) or not value:
            continue
        token = _source_token(value)
        if token:
            return token
    return ""


def _derive_inline_stri(
    source: str,
    *,
    sutra_id: str,
    features: Mapping[str, Any] | None,
) -> EngineDerivation | None:
    if sutra_id not in _INLINE_STRI_SUTRAS:
        return None
    from .grammar import Case, GrammaticalNumber
    from .subanta import decline_aa_feminine

    lemma = str((features or {}).get("lemma") or (features or {}).get("stem") or source or "latā")
    if lemma.endswith("a") and not lemma.endswith("ā"):
        lemma = lemma[:-1] + "ā"
    surface = decline_aa_feminine(lemma)[(Case.NOMINATIVE, GrammaticalNumber.SINGULAR)]
    return EngineDerivation(
        source=lemma,
        surface=surface,
        suffix="ṭāp",
        semantic="stri",
        family="strī-pratyaya",
        sutra_ids=(sutra_id,),
        operations=("ṭāp-feminine-long-a", "decline-aa-feminine"),
        gloss=f"feminine stem formation: {lemma} -> {surface}",
        engines=("StriPratyayaEngine", "subanta.decline_aa_feminine"),
        state_features=(("applied_suffix", "ṭāp"), ("derivation_family", "strī-pratyaya")),
    )


def _state_features_for_derivation(
    *,
    context: Mapping[str, Any],
    operations: tuple[str, ...],
    suffix: str | TaddhitaSuffix | None,
    family: str,
) -> tuple[tuple[str, Any], ...]:
    items: list[tuple[str, Any]] = [("derivation_family", family)]
    if operations:
        items.append(("derivation_operations", operations))
        items.append(("engine_operation", " + ".join(operations)))
    if suffix is not None:
        items.append(("applied_suffix", suffix.value if isinstance(suffix, TaddhitaSuffix) else suffix))
    operation = context.get("operation")
    if isinstance(operation, str) and operation:
        items.append(("phonological_labels", frozenset({operation.replace("_", "-")})))
    rule = context.get("rule")
    if isinstance(rule, str) and rule:
        items.append(("active_rule", rule))
    semantic = context.get("semantic")
    if isinstance(semantic, str) and semantic:
        items.append(("active_semantic", semantic))
    source_basis = context.get("source_basis")
    if isinstance(source_basis, str) and source_basis:
        items.append(("source_basis", source_basis))
    inherited_from = context.get("anuvritti_from")
    if isinstance(inherited_from, str) and inherited_from:
        items.append(("anuvritti_from", inherited_from))
    inherited_suffix = context.get("anuvritti_suffix")
    if inherited_suffix:
        items.append(("anuvritti_suffix", inherited_suffix))
    return tuple(items)


def _sutra_sort_key(sutra_id: str) -> tuple[int, ...]:
    return tuple(int(part) for part in sutra_id.split("."))


def _merge_features(
    base: Mapping[str, Any],
    overrides: Mapping[str, Any] | None,
    *,
    strict: bool,
) -> dict[str, Any] | None:
    context = dict(base)
    for key, value in (overrides or {}).items():
        if key in {"source", "surface", "expected_surface"}:
            context[key] = value
            continue
        if strict and key in context and context[key] != value:
            raise ValueError(f"Feature {key!r} conflicts with sutra fixture: {context[key]!r} != {value!r}")
        if not strict and key in context and context[key] != value:
            return None
        context[key] = value
    return context


def _module_for_sutra(sutra_id: str):
    from . import sutra_impl_4, sutra_impl_5

    if sutra_id in sutra_impl_4.IMPLEMENTED_IDS:
        return sutra_impl_4
    if sutra_id in sutra_impl_5.IMPLEMENTED_IDS:
        return sutra_impl_5
    return None


def _representative_source_for_context(sutra_id: str | None, context: Mapping[str, Any] | None) -> tuple[str, str]:
    """Return a derivable representative base only when no explicit base exists."""
    context = context or {}
    direct = resolve_adhyaya45_source(context)
    if direct:
        return direct, "explicit-or-structural-source"

    semantic = context.get("semantic")
    if isinstance(semantic, str) and semantic:
        first = semantic.split("_")[0]
        hinted = _SEMANTIC_SOURCE_HINTS.get(first)
        if hinted:
            return hinted, f"semantic-source:{first}"
        token = _source_token(first)
        if token:
            return token, f"semantic-source:{first}"

    domain = context.get("domain")
    if isinstance(domain, str) and domain:
        if domain in {"samjna", "saṃjñā"}:
            return "nāman", f"domain-source:{domain}"
        if domain == "chandas":
            return "mantra", f"domain-source:{domain}"
        token = _source_token(domain)
        if token:
            return token, f"domain-source:{domain}"

    if context.get("is_vedic"):
        return "vaidika", "vedic-representative-source"
    if sutra_id:
        return "artha", f"representative-source:{sutra_id}"
    return "", ""


def _positive_features_for_sutra(sutra_id: str) -> dict[str, Any]:
    module = _module_for_sutra(sutra_id)
    if module is None:
        return {}
    return dict(module.positive_features(sutra_id))


def _continuation_anuvritti(sutra_id: str, context: Mapping[str, Any]) -> ContinuationAnuvritti | None:
    """Recover the overt effect inherited by a compact ``rule: continuation`` row."""
    if context.get("rule") != "continuation":
        return None
    current = _sutra_sort_key(sutra_id)
    pada = ".".join(sutra_id.split(".")[:2])
    for candidate_id in reversed(_implemented_adhyaya45_ids()):
        if not candidate_id.startswith(pada + "."):
            continue
        if _sutra_sort_key(candidate_id) >= current:
            continue
        candidate = _positive_features_for_sutra(candidate_id)
        if not candidate or candidate.get("rule") == "continuation":
            continue
        suffix = candidate.get("suffix") or candidate.get("suffix_class")
        if suffix:
            return ContinuationAnuvritti(candidate_id, suffix=suffix)
        operation = candidate.get("operation")
        if isinstance(operation, str) and operation:
            return ContinuationAnuvritti(candidate_id, operation=operation)
        samjna = candidate.get("samjna")
        if isinstance(samjna, str) and samjna:
            return ContinuationAnuvritti(candidate_id, operation=f"samjna:{samjna}")
        section = candidate.get("section")
        if isinstance(section, str) and section:
            return ContinuationAnuvritti(candidate_id, operation=f"section:{section}")
    return None


def _implemented_adhyaya45_ids() -> tuple[str, ...]:
    from . import sutra_impl_4, sutra_impl_5

    return tuple(sorted(sutra_impl_4.IMPLEMENTED_IDS | sutra_impl_5.IMPLEMENTED_IDS, key=_sutra_sort_key))


def _context_contains_query(context: Mapping[str, Any], query: Mapping[str, Any]) -> bool:
    useful_keys = set(query) - {"source", "surface", "expected_surface"}
    if not useful_keys:
        return False
    return any(key in context and context[key] == query[key] for key in useful_keys)


def _metadata_for(module: Any, sutra_id: str) -> tuple[str, str]:
    meta = getattr(module, "META", {}).get(sutra_id)
    if meta is None:
        return ("vidhi", f"Adhyaya 4/5 rule {sutra_id}")
    return (meta.operator, meta.summary)


def _clean_suffix_marker(suffix: str) -> str:
    cleaned = suffix
    for marker in ("ṭ", "ḍ", "ṇ", "ñ", "ṅ", "ś", "p", "c"):
        cleaned = cleaned.replace(marker, "")
    return cleaned or suffix


def _join_suffix(source: str, suffix_surface: str) -> str:
    if not suffix_surface:
        return source
    if source.endswith("a") and suffix_surface.startswith("a"):
        return source + suffix_surface[1:]
    return source + suffix_surface


class SemanticRelationEngine:
    """Interpret the meaning contributed by Adhyaya 4/5 rule contexts."""

    DESCRIPTIONS: dict[str, str] = {
        "apatya": "descendant, offspring, lineage, or patronymic relation",
        "gotra": "clan, ancestral, or lineage identity",
        "possession": "possessing, endowed with, or characterized by the source",
        "atishayana": "surpassing degree, comparison, or superlative force",
        "degree": "comparative, superlative, deictic, or measured degree",
        "samāsānta": "compound-final derivational ending",
        "stri": "feminine stem formation",
        "taddhita": "secondary nominal derivation",
    }

    def relation_for(self, sutra_id: str, context: FeatureMap) -> str:
        if sutra_id in TADDHITA_RULES:
            return TADDHITA_RULES[sutra_id].semantic
        semantic = context.get("semantic")
        if isinstance(semantic, str) and semantic not in {"ordinary", "non_gotra"}:
            return semantic
        if sutra_id.startswith("4.1."):
            number = int(sutra_id.split(".")[2])
            if number <= 75:
                return "stri"
            if number >= 76:
                return "apatya" if number <= 92 else "gotra"
        if sutra_id.startswith(("4.2.", "4.3.", "4.4.", "5.1.")):
            return "taddhita"
        if sutra_id.startswith("5.2."):
            return "possession"
        if sutra_id.startswith("5.3."):
            return "degree"
        if sutra_id.startswith("5.4."):
            return "samāsānta"
        return "taddhita"

    def describe(self, semantic: str) -> str:
        return self.DESCRIPTIONS.get(semantic, semantic.replace("_", " "))


class TaddhitaSelectionEngine:
    """Select a suffix-bearing rule by running existing discrete predicates."""

    def __init__(self, semantic_engine: SemanticRelationEngine | None = None) -> None:
        self.semantic_engine = semantic_engine or SemanticRelationEngine()

    def select(
        self,
        source: str,
        *,
        sutra_id: str | None = None,
        suffix: str | TaddhitaSuffix | None = None,
        features: Mapping[str, Any] | None = None,
        allowed: Callable[[str], bool] | None = None,
    ) -> SelectedPratyaya:
        if sutra_id is not None:
            return self._select_explicit(source, sutra_id, suffix=suffix, features=features)
        if suffix is None and not features:
            raise ValueError("TaddhitaSelectionEngine requires sutra_id, suffix, or discriminating features")
        if isinstance(suffix, TaddhitaSuffix):
            for candidate_id, rule in TADDHITA_RULES.items():
                if rule.suffix != suffix:
                    continue
                if allowed is not None and not allowed(candidate_id):
                    continue
                selection = self._candidate(source, candidate_id, suffix=suffix, features=features)
                if selection is not None:
                    return selection

        candidates: list[SelectedPratyaya] = []
        for candidate_id in _implemented_adhyaya45_ids():
            if allowed is not None and not allowed(candidate_id):
                continue
            selection = self._candidate(source, candidate_id, suffix=suffix, features=features)
            if selection is not None:
                candidates.append(selection)
        for candidate_id in TADDHITA_RULES:
            if allowed is not None and not allowed(candidate_id):
                continue
            selection = self._candidate(source, candidate_id, suffix=suffix, features=features)
            if selection is not None:
                candidates.append(selection)
        if not candidates:
            raise ValueError("No Adhyaya 4/5 predicate selected a derivational rule")
        return sorted(candidates, key=lambda item: _sutra_sort_key(item.sutra.sutra_id))[-1]

    def _select_explicit(
        self,
        source: str,
        sutra_id: str,
        *,
        suffix: str | TaddhitaSuffix | None,
        features: Mapping[str, Any] | None,
    ) -> SelectedPratyaya:
        selection = self._candidate(source, sutra_id, suffix=suffix, features=features, strict=True)
        if selection is None:
            raise ValueError(f"{sutra_id} did not accept its merged derivation context")
        return selection

    def _candidate(
        self,
        source: str,
        sutra_id: str,
        *,
        suffix: str | TaddhitaSuffix | None,
        features: Mapping[str, Any] | None,
        strict: bool = False,
    ) -> SelectedPratyaya | None:
        if sutra_id in TADDHITA_RULES:
            rule = TADDHITA_RULES[sutra_id]
            if suffix is not None and suffix != rule.suffix and str(suffix) != rule.suffix.value:
                if strict:
                    raise ValueError(f"{sutra_id} derives {rule.suffix.value}, not {suffix!r}")
                return None
            context = _merge_features(
                {"semantic": rule.semantic, "suffix": rule.suffix, "source": source},
                features,
                strict=strict,
            )
            if context is None:
                return None
            sutra = AppliedSutra(
                sutra_id=sutra_id,
                context=context,
                operator="vidhi",
                summary=rule.source_gloss,
                module="sanskript.derivation.TADDHITA_RULES",
            )
            return SelectedPratyaya(source, rule.suffix, rule.semantic, sutra)

        module = _module_for_sutra(sutra_id)
        if module is None:
            if strict:
                raise ValueError(f"No Adhyaya 4/5 predicate module owns {sutra_id!r}")
            return None

        base = module.positive_features(sutra_id)
        if not strict and features is not None and not _context_contains_query(base, features):
            return None
        context = _merge_features(base, features, strict=strict)
        if context is None:
            return None
        if suffix is not None:
            suffix_value = suffix.value if isinstance(suffix, TaddhitaSuffix) else suffix
            if not strict and "suffix" not in context and "suffix_class" not in context:
                return None
            if "suffix" in context and context["suffix"] != suffix_value:
                if strict:
                    raise ValueError(f"{sutra_id} fixture has suffix {context['suffix']!r}, not {suffix_value!r}")
                return None
            context["suffix"] = suffix_value

        if not module.handler_for(sutra_id)(context):
            if strict:
                raise ValueError(f"{sutra_id} predicate rejected the merged derivation context")
            return None

        operator, summary = _metadata_for(module, sutra_id)
        semantic = self.semantic_engine.relation_for(sutra_id, context)
        sutra = AppliedSutra(sutra_id, context, operator, summary, module.__name__)
        selected_suffix = context.get("suffix")
        if selected_suffix is None and "suffix_class" in context:
            selected_suffix = context["suffix_class"]
        if selected_suffix is None:
            anuvritti = _continuation_anuvritti(sutra_id, context)
            if anuvritti is not None:
                context["anuvritti_from"] = anuvritti.inherited_from
                if anuvritti.suffix is not None:
                    selected_suffix = anuvritti.suffix
                    context["suffix"] = anuvritti.suffix
                    context["anuvritti_suffix"] = anuvritti.suffix
                if anuvritti.operation is not None:
                    context["operation"] = anuvritti.operation
        return SelectedPratyaya(source, selected_suffix, semantic, sutra)


class TaddhitaSurfaceEngine:
    """Realize selected taddhita suffixes and stem operations as surfaces."""

    def derive(self, selection: SelectedPratyaya) -> EngineDerivation:
        context = selection.sutra.context
        surface, operations = self._surface(selection.source, selection.suffix, context)
        inherited_from = context.get("anuvritti_from")
        if isinstance(inherited_from, str) and inherited_from and not any(
            operation.startswith("anuvritti:") for operation in operations
        ):
            operations = (f"anuvritti:{inherited_from}", *operations)
        semantic = selection.semantic
        description = SemanticRelationEngine().describe(semantic)
        return EngineDerivation(
            source=selection.source,
            surface=surface,
            suffix=selection.suffix,
            semantic=semantic,
            family=DerivationFamily.TADDHITA.value,
            sutra_ids=(selection.sutra.sutra_id,),
            operations=operations,
            gloss=f"{description}: {selection.source} -> {surface}",
            engines=("TaddhitaSelectionEngine", "SemanticRelationEngine", "TaddhitaSurfaceEngine"),
            state_features=_state_features_for_derivation(
                context=context,
                operations=operations,
                suffix=selection.suffix,
                family=DerivationFamily.TADDHITA.value,
            ),
        )

    def _surface(
        self,
        source: str,
        suffix: str | TaddhitaSuffix | None,
        context: Mapping[str, Any],
    ) -> tuple[str, tuple[str, ...]]:
        operation = context.get("operation")
        if operation in {"luk", "lup", "lopa", "ataddhita_luk", "yat_n_lopa"}:
            return self._apply_operation(source, operation, context)
        if suffix == TaddhitaSuffix.APATYA:
            return _derive_apatya(source)
        if suffix == TaddhitaSuffix.MATUP:
            return _derive_matup(source)
        if suffix == TaddhitaSuffix.ATISHAYANA:
            return _derive_atishayana(source)
        if suffix is None:
            if operation is not None:
                return source, (str(operation).replace("_", "-"),)
            if context.get("rule") == "continuation":
                semantic = context.get("semantic")
                label = f"continuation:{semantic}" if semantic else "continuation-domain"
                return source, (label,)
            return source, ("no-overt-suffix",)

        suffix_text = str(suffix)
        if suffix_text in {"matup", "ḍmatup", "matu̐p"}:
            return _derive_matup(source)
        if suffix_text in {"tarap", "tar"}:
            return source + "tara", ("tarap-comparative",)
        if suffix_text in {"tamap", "tama"}:
            return source + "tama", ("tamap-superlative",)
        if suffix_text in {"iṣṭhan", "iṣṭha"}:
            return _derive_atishayana(source)
        if suffix_text in {"aṇ", "añ"}:
            stem, strengthened = _apply_initial_vrddhi(source)
            operations = ["initial-vrddhi"] if strengthened else []
            operations.append(f"{suffix_text}-taddhita")
            return (stem if stem.endswith("a") else stem + "a"), tuple(operations)
        if suffix_text in {"iñ", "phiñ", "yañ", "yan"}:
            stem, strengthened = _apply_initial_vrddhi(source)
            operations = ["initial-vrddhi"] if strengthened else []
            operations.append(f"{suffix_text}-taddhita")
            return _join_suffix(stem, "ya"), tuple(operations)
        if suffix_text in {"ṭhak", "ṭhañ", "ḍhak", "ḍhañ", "ḍhakañ"}:
            return _join_suffix(source, "ika"), (f"{suffix_text}-realized-as-ika",)
        if suffix_text in {"cha", "chan", "chaṇ"}:
            return _join_suffix(source, "īya"), (f"{suffix_text}-realized-as-īya",)
        if suffix_text in {"yat", "ya", "yak", "yap"}:
            return _join_suffix(source, "ya"), (f"{suffix_text}-realized-as-ya",)
        if suffix_text in {"kan", "ka", "akañ", "airak", "kap"}:
            return _join_suffix(source, "ka"), (f"{suffix_text}-realized-as-ka",)
        if suffix_text == "vati":
            return _join_suffix(source, "vat"), ("vati-realized-as-vat",)
        if suffix_text == "tva":
            return _join_suffix(source, "tva"), ("tva-abstract-noun",)
        if suffix_text == "tal":
            surface = source[:-1] + "tā" if source.endswith("a") else source + "tā"
            return surface, ("tal-realized-as-tā",)
        cleaned = _clean_suffix_marker(suffix_text)
        return _join_suffix(source, cleaned), (f"{suffix_text}-generic-taddhita-surface",)

    def _apply_operation(
        self,
        source: str,
        operation: Any,
        context: Mapping[str, Any],
    ) -> tuple[str, tuple[str, ...]]:
        if operation in {"luk", "lup", "ataddhita_luk"}:
            return source, (str(operation).replace("_", "-"),)
        if operation in {"lopa", "yat_n_lopa"}:
            stem_final = context.get("stem_final")
            if isinstance(stem_final, str) and source.endswith(stem_final):
                return source[: -len(stem_final)], (str(operation).replace("_", "-"),)
            if source:
                return source[:-1], (str(operation).replace("_", "-"),)
        return source, (str(operation),)


class StriPratyayaEngine:
    """Derive feminine stems from the 4.1 strī-pratyaya predicates."""

    def __init__(self, selector: TaddhitaSelectionEngine | None = None) -> None:
        self.selector = selector or TaddhitaSelectionEngine()

    def derive(
        self,
        source: str,
        *,
        sutra_id: str | None = None,
        features: Mapping[str, Any] | None = None,
    ) -> EngineDerivation:
        context_features = dict(features or {})
        if sutra_id is not None:
            inline = _derive_inline_stri(source, sutra_id=sutra_id, features=context_features)
            if inline is not None:
                return inline
        resolved = resolve_adhyaya45_source(context_features) or source
        if not resolved:
            resolved, source_basis = _representative_source_for_context(sutra_id, context_features)
            if source_basis:
                context_features["source_basis"] = source_basis
        selection = self.selector.select(
            resolved,
            sutra_id=sutra_id,
            features=context_features,
            allowed=self._is_stri_sutra,
        )
        surface, operations = self._surface(resolved, selection.suffix, selection.sutra.context)
        return EngineDerivation(
            source=resolved,
            surface=surface,
            suffix=selection.suffix,
            semantic="stri",
            family="strī-pratyaya",
            sutra_ids=(selection.sutra.sutra_id,),
            operations=operations,
            gloss=f"feminine stem formation: {resolved} -> {surface}",
            engines=("TaddhitaSelectionEngine", "SemanticRelationEngine", "StriPratyayaEngine"),
            state_features=_state_features_for_derivation(
                context=selection.sutra.context,
                operations=operations,
                suffix=selection.suffix,
                family="strī-pratyaya",
            ),
        )

    def _is_stri_sutra(self, sutra_id: str) -> bool:
        if not sutra_id.startswith("4.1."):
            return False
        number = int(sutra_id.split(".")[2])
        return number <= 75

    def _surface(
        self,
        source: str,
        suffix: str | TaddhitaSuffix | None,
        context: Mapping[str, Any],
    ) -> tuple[str, tuple[str, ...]]:
        suffix_text = str(suffix or context.get("suffix") or "ṭāp")
        if suffix_text in {"ṭāp", "ḍāp", "cāp", "nyap_or_ap"}:
            surface = source[:-1] + "ā" if source.endswith("a") else source + "ā"
            return surface, (f"{suffix_text}-feminine-long-a",)
        if suffix_text in {"ṅīp", "ṅīṣ", "ṅīn"}:
            if source == "rājan":
                return "rājñī", (f"{suffix_text}-feminine-ī", "rājan-to-rājñī")
            if source.endswith("an"):
                return source[:-2] + "nī", (f"{suffix_text}-feminine-ī",)
            if source.endswith("a"):
                return source[:-1] + "ī", (f"{suffix_text}-feminine-ī",)
            return source + "ī", (f"{suffix_text}-feminine-ī",)
        if suffix_text == "ūṅ":
            surface = source[:-1] + "ū" if source.endswith("u") else source + "ū"
            return surface, ("ūṅ-feminine-ū",)
        if context.get("operation") == "luk":
            return source, ("stri-pratyaya-luk",)
        return _join_suffix(source, _clean_suffix_marker(suffix_text)), (f"{suffix_text}-stri-surface",)


class SamasantaEngine:
    """Derive compound-final endings from the 5.4 samāsānta predicates."""

    def __init__(
        self,
        selector: TaddhitaSelectionEngine | None = None,
        surface_engine: TaddhitaSurfaceEngine | None = None,
    ) -> None:
        self.selector = selector or TaddhitaSelectionEngine()
        self.surface_engine = surface_engine or TaddhitaSurfaceEngine()

    def derive(
        self,
        source: str | None = None,
        *,
        members: Sequence[str] | None = None,
        sutra_id: str | None = None,
        features: Mapping[str, Any] | None = None,
    ) -> EngineDerivation:
        merged = dict(features or {})
        compound = source if source is not None else "".join(members or ())
        if not compound:
            compound = resolve_adhyaya45_source(merged)
        if not compound:
            compound, source_basis = _representative_source_for_context(sutra_id, merged)
            if source_basis:
                merged["source_basis"] = source_basis
        if not compound:
            raise ValueError("SamasantaEngine requires source, members, or discriminating features")
        selection = self.selector.select(
            compound,
            sutra_id=sutra_id,
            features=merged,
            allowed=lambda sid: sid.startswith("5.4."),
        )
        surface, operations = self._surface(compound, selection)
        return EngineDerivation(
            source=compound,
            surface=surface,
            suffix=selection.suffix,
            semantic=selection.semantic,
            family="samāsānta",
            sutra_ids=(selection.sutra.sutra_id,),
            operations=operations,
            gloss=f"compound-final derivation: {compound} -> {surface}",
            engines=("TaddhitaSelectionEngine", "SemanticRelationEngine", "SamasantaEngine"),
            state_features=_state_features_for_derivation(
                context=selection.sutra.context,
                operations=operations,
                suffix=selection.suffix,
                family="samāsānta",
            ),
        )

    def _surface(self, source: str, selection: SelectedPratyaya) -> tuple[str, tuple[str, ...]]:
        context = selection.sutra.context
        operation = context.get("operation")
        if operation is not None:
            return self.surface_engine._apply_operation(source, operation, context)
        suffix_text = str(selection.suffix or context.get("suffix") or "")
        if suffix_text in {"ac", "ṭac"}:
            if source.endswith("an"):
                return source[:-2] + "a", (f"{suffix_text}-samāsānta-a",)
            return (source if source.endswith("a") else source + "a"), (f"{suffix_text}-samāsānta-a",)
        if suffix_text in {"kap", "kan"}:
            return _join_suffix(source, "ka"), (f"{suffix_text}-samāsānta-ka",)
        if suffix_text in {"ṣac", "ṣa"}:
            return _join_suffix(source, "ṣa"), (f"{suffix_text}-samāsānta-ṣa",)
        if suffix_text:
            return _join_suffix(source, _clean_suffix_marker(suffix_text)), (f"{suffix_text}-samāsānta-surface",)
        return source, ("samāsānta-zero-surface",)


def derive_stri(source: str, *, sutra_id: str | None = None, features: Mapping[str, Any] | None = None) -> EngineDerivation:
    return StriPratyayaEngine().derive(source, sutra_id=sutra_id, features=features)


def derive_adhyaya45_taddhita(
    source: str,
    *,
    sutra_id: str | None = None,
    suffix: str | TaddhitaSuffix | None = None,
    features: Mapping[str, Any] | None = None,
) -> EngineDerivation:
    context_features = dict(features or {})
    resolved = resolve_adhyaya45_source(context_features) or source
    if not resolved:
        resolved, source_basis = _representative_source_for_context(sutra_id, context_features)
        if source_basis:
            context_features["source_basis"] = source_basis
    selector = TaddhitaSelectionEngine()
    surface = TaddhitaSurfaceEngine()
    selection = selector.select(resolved, sutra_id=sutra_id, suffix=suffix, features=context_features)
    return surface.derive(selection)


def derive_samasanta(
    source: str | None = None,
    *,
    members: Sequence[str] | None = None,
    sutra_id: str | None = None,
    features: Mapping[str, Any] | None = None,
) -> EngineDerivation:
    return SamasantaEngine().derive(source, members=members, sutra_id=sutra_id, features=features)


__all__ = [
    "AppliedSutra",
    "EngineDerivation",
    "SelectedPratyaya",
    "SemanticRelationEngine",
    "SamasantaEngine",
    "StriPratyayaEngine",
    "TaddhitaSelectionEngine",
    "TaddhitaSurfaceEngine",
    "derive_adhyaya45_taddhita",
    "derive_samasanta",
    "derive_stri",
    "resolve_adhyaya45_source",
]
