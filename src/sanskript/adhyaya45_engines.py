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
        return SelectedPratyaya(source, selected_suffix, semantic, sutra)


class TaddhitaSurfaceEngine:
    """Realize selected taddhita suffixes and stem operations as surfaces."""

    def derive(self, selection: SelectedPratyaya) -> EngineDerivation:
        surface, operations = self._surface(selection.source, selection.suffix, selection.sutra.context)
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
        selection = self.selector.select(
            source,
            sutra_id=sutra_id,
            features=features,
            allowed=self._is_stri_sutra,
        )
        surface, operations = self._surface(source, selection.suffix, selection.sutra.context)
        return EngineDerivation(
            source=source,
            surface=surface,
            suffix=selection.suffix,
            semantic="stri",
            family="strī-pratyaya",
            sutra_ids=(selection.sutra.sutra_id,),
            operations=operations,
            gloss=f"feminine stem formation: {source} -> {surface}",
            engines=("TaddhitaSelectionEngine", "SemanticRelationEngine", "StriPratyayaEngine"),
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
        compound = source if source is not None else "".join(members or ())
        if not compound:
            raise ValueError("SamasantaEngine requires source or members")
        selection = self.selector.select(
            compound,
            sutra_id=sutra_id,
            features=features,
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
    selector = TaddhitaSelectionEngine()
    surface = TaddhitaSurfaceEngine()
    selection = selector.select(source, sutra_id=sutra_id, suffix=suffix, features=features)
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
]
