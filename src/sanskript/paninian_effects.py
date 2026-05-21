"""Map truth-gate assigned tags and fixture context into coordinator state effects."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .anga import DerivationContext, Suffix, guna, vrddhi
from .grammar import Case, Gender, GrammaticalNumber, Lakara, Pada, Person, Role, Samjna
from .samasa import SamasaType


SAMJNA_TAG_TO_ENUM: dict[str, Samjna] = {
    "ghu": Samjna.GHU,
    "gha": Samjna.GHA,
    "samkhya": Samjna.SAMKHYA,
    "sankhya": Samjna.SAMKHYA,
    "sat": Samjna.SAT,
    "nistha": Samjna.NISTHA,
    "sarvanama": Samjna.SARVANAMA,
    "nadī": Samjna.NADII,
    "nadi": Samjna.NADII,
    "ghī": Samjna.GHI,
    "ghi": Samjna.GHI,
    "bha": Samjna.BHA,
    "pada": Samjna.PADA,
    "anga": Samjna.ANGA,
    "laghu": Samjna.LAGHU,
    "guru": Samjna.GURU,
    "pratipadika": Samjna.PRATIPADIKA,
    "avyaya": Samjna.AVYAYA,
    "nipata": Samjna.NIPATA,
    "upasarga": Samjna.UPASARGA,
    "gati": Samjna.GATI,
    "karmapravacaniya": Samjna.KARMAPRAVACANIIYA,
}

PHONOLOGICAL_LABELS = frozenset(
    {
        "vrddhi",
        "vrddha",
        "guna",
        "samyoga",
        "anunasika",
        "savarna",
        "pragrhya",
        "lopa",
        "luk",
        "slu",
        "lup",
        "ti",
        "upadha",
        "samprasārana",
        "samprasarana",
        "kit",
        "ngit",
        "aprkta",
        "samhita",
        "avasana",
        "accent",
        "udatta",
        "anudatta",
        "svarita",
        "ekasruti",
    }
)

META_TAG_EFFECTS: dict[str, str] = {
    "substitution-site": "reference_case",
    "final-substitution": "substitution_index",
    "following-initial": "substitution_index",
    "whole-replacement": "target_scope",
    "augment-boundary": "augment_boundary",
    "mid-augment": "substitution_index",
    "single-boundary": "target_scope",
    "savarna-reference": "savarna_class",
    "duration": "tapara_match",
    "pratyahara": "pratyahara",
    "closest-substitute": "substitute",
    "case-reference": "reference_case",
    "sva-rupa": "refers_to_own_form",
    "tadanta": "apply_tadanta",
    "adjective-agreement": "is_adjective",
    "convention": "convention",
    "lup-inference": "lup_inference",
    "suffix-meaning": "suffix_meaning",
    "yathasamkhya": "list_correspondence",
    "adhikara-inheritance": "adhikara_inherited",
    "samjna-priority": "samjna_priority",
    "rule-priority": "rule_priority",
    "adhikara": "adhikara_scope",
    "gati-position": "gati_position",
    "gati-position-optional": "gati_position",
}

KARAKA_TAG_TO_ROLE: dict[str, Role] = {
    "apadana": Role.APADANA,
    "apādāna": Role.APADANA,
    "sampradana": Role.SAMPRADANA,
    "sampradāna": Role.SAMPRADANA,
    "karana": Role.KARANA,
    "karaṇa": Role.KARANA,
    "adhikarana": Role.ADHIKARANA,
    "adhikaraṇa": Role.ADHIKARANA,
    "karman": Role.KARMAN,
    "kartr": Role.KARTR,
    "kartṛ": Role.KARTR,
}

METARULE_CONTEXT_KEYS: tuple[str, ...] = (
    "ref_case",
    "operation_target",
    "refers_to_own_form",
    "is_samjna_use",
    "apply_tadanta",
    "operation_specifier",
    "target_final",
    "verb",
    "context",
    "in_compound",
    "is_first_named",
    "in_range_to_kadara",
    "competing_samjnas",
    "selected_count",
    "is_in_dhatupatha",
    "is_sarvanama_stem",
    "following_suffix",
    "duration",
    "is_adjective",
    "is_jati",
    "left_list",
    "right_list",
    "mapping",
    "suffix_class",
    "person_label",
    "position",
    "yoga_pramana",
    "absent",
    "adhikara_scope",
    "rule_precedence",
    "list_correspondence",
    "samasa_role",
    "root_class",
    "karaka_context",
    "gati_position",
    "optional_sarvanama",
    "is_conventional_samjna",
    "aśiṣya",
    "convention",
    "is_principal_suffix",
    "provides_meaning",
    "suffix_meaning",
    "rule_marker",
    "is_adhikara",
    "adhikara_inherited",
    "rules_conflict",
    "selected",
    "rule_priority",
)

CONTEXT_STATE_KEYS: tuple[str, ...] = (
    "upapada",
    "suffix",
    "dhatu_lemma",
    "dhatu_type",
    "pada",
    "lakara",
    "role",
    "compound_type",
    "sandhi_rule",
    "accent_domain",
    "accent_pattern",
    "substitute",
    "marker",
    "sound",
    "stem",
    "source",
    "semantic",
    "vidhi_class",
    "operation",
    "redup_target",
    "left",
    "right",
    "expected_rule",
    "is_taddhita",
    "strict_engine",
    "assigns_samjna",
    "domain",
    "asiddha_rule",
    "rule_blocked",
    "blocks_rule",
    "sandhi_operation",
    "expected_surface",
    "scope",
    "varga",
    "vikarana",
    "kind",
    "accent",
    "pitch",
    *METARULE_CONTEXT_KEYS,
)

MEANINGFUL_STATE_KEYS: tuple[str, ...] = (
    "samjnas",
    "phonological_labels",
    "blocked_operations",
    "case",
    "role",
    "blocked_sutras",
    "compound_type",
    "gender",
    "lakara",
    "person",
    "number",
    "pada",
    "semantic",
    "substitute",
    "marker",
    "suffix",
    "upapada",
    "dhatu_lemma",
    "accent_domain",
    "sandhi_rule",
    "form",
    "surface",
    "assigns_samjna",
    "vidhi_class",
    "operation",
    "domain",
    "asiddha_scope",
    "derivation_operations",
    "engine_operation",
    "applied_suffix",
    "active_rule",
    "active_semantic",
    "derivation_family",
    "accent_output",
    "engine_operation",
    "reference_case",
    "substitution_index",
    "target_scope",
    "augment_boundary",
    "optional",
    "blocked_operations",
    "phonological_labels",
    "upadesha",
    "scope",
    "varga",
    "vikarana",
    "kind",
    "lemma",
    "accent",
    "pitch",
    "karaka",
    "reference_target",
    "root_class",
    "allowed_cases",
    "assigned_case",
    "case_basis",
    "case_rule",
    "anabhihita_gate",
    "boundary_roles",
    "governance_effect",
    "target_sound",
    "replacement",
    "root_substitution",
    "derivation_domain",
    "optional_substitution",
    "tin_replacement",
    "suffix_position",
    "suffix_alternation",
    "suffix_class",
    *METARULE_CONTEXT_KEYS,
)


def _normalize_tag_tail(tail: str) -> str:
    return tail.replace("ā", "a").replace("ī", "i").replace("ū", "u").replace("ṛ", "r").replace("ṇ", "n")


def _enum_from_value(enum_type, value: Any):
    if isinstance(value, enum_type):
        return value
    for item in enum_type:
        if value in {item.value, item.name, item.name.lower()}:
            return item
    return None


def _parse_assigned_tag(tag: str) -> tuple[str, str] | None:
    if ":" not in tag or tag.startswith("sutra:"):
        return None
    head, _, tail = tag.partition(":")
    return head, tail


def effects_from_assigned(
    assigned: tuple[str, ...],
    *,
    existing_samjnas: frozenset[Samjna] = frozenset(),
    existing_labels: frozenset[str] = frozenset(),
    existing_blocked_ops: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    """Turn registry assigned tags into feature/state updates."""
    samjnas = set(existing_samjnas)
    labels = set(existing_labels)
    blocked_ops = set(existing_blocked_ops)
    blocked_sutras: list[str] = []
    updates: dict[str, Any] = {}

    for tag in assigned:
        parsed = _parse_assigned_tag(tag)
        if parsed is None:
            continue
        head, tail = parsed
        if head == "samjna":
            if tail in SAMJNA_TAG_TO_ENUM:
                samjnas.add(SAMJNA_TAG_TO_ENUM[tail])
            elif tail in PHONOLOGICAL_LABELS or tail in {"duration", "dhatu", "person", "sup", "vibhakti"}:
                labels.add(tail)
            elif tail == "sarvanama-optional":
                updates["optional_sarvanama"] = True
            elif tail == "upasarjana":
                updates["samasa_role"] = "upasarjana"
        elif head == "karaka":
            role = KARAKA_TAG_TO_ROLE.get(tail) or KARAKA_TAG_TO_ROLE.get(_normalize_tag_tail(tail))
            if role is not None:
                updates["role"] = role
                updates["karaka"] = role.value
        elif head == "block":
            blocked_ops.add(tail)
        elif head == "vibhakti":
            case = _enum_from_value(Case, tail)
            if case is not None:
                updates["case"] = case
        elif head == "samasa":
            samasa_type = _enum_from_value(SamasaType, tail)
            if samasa_type is not None:
                updates["compound_type"] = samasa_type
        elif head == "suffix":
            updates["suffix"] = tail
        elif head == "derived":
            updates["form"] = tail
            updates["surface"] = tail
        elif head == "dhatu-type":
            updates["dhatu_type"] = tail
            updates["kind"] = tail
        elif head == "lakara":
            lakara = _enum_from_value(Lakara, tail)
            if lakara is not None:
                updates["lakara"] = lakara
        elif head == "scope":
            updates["scope"] = tail
        elif head == "vikarana":
            updates["vikarana"] = tail
        elif head == "gender":
            gender = _enum_from_value(Gender, tail)
            if gender is not None:
                updates["gender"] = gender
        elif head == "pada":
            pada = _enum_from_value(Pada, tail)
            if pada is not None:
                updates["pada"] = pada
        elif head == "blocked":
            blocked_sutras.append(tail)
        elif head == "meta":
            state_key = META_TAG_EFFECTS.get(tail)
            if tail == "substitution-site":
                updates["reference_case"] = Case.GENITIVE
            elif state_key in {
                "convention",
                "suffix_meaning",
                "adhikara_inherited",
                "samjna_priority",
                "rule_priority",
                "lup_inference",
                "refers_to_own_form",
                "apply_tadanta",
                "is_adjective",
                "list_correspondence",
                "adhikara_scope",
                "gati_position",
                "tapara_match",
                "pratyahara",
            }:
                updates[state_key] = True
            elif state_key:
                updates.setdefault(state_key, True)
            if tail == "gati-position-optional":
                updates["optional"] = True
        elif head == "target":
            if tail == "ik":
                labels.add("ik")
        elif head == "substitute":
            updates["substitute_channel"] = tail
        elif head == "operation":
            updates["operation"] = tail
        elif head == "operator" and tail == "vibhasha":
            updates["optional"] = True
        elif head == "sense":
            updates["semantic"] = tail

    if samjnas:
        updates["samjnas"] = frozenset(samjnas)
    if labels:
        updates["phonological_labels"] = frozenset(labels)
    if blocked_ops:
        updates["blocked_operations"] = frozenset(blocked_ops)
    if blocked_sutras:
        updates.setdefault("blocked_sutras", tuple(blocked_sutras))
    return updates


def contextual_features(context: Mapping[str, Any]) -> dict[str, Any]:
    """Copy derivationally relevant fixture keys into coordinator state."""
    copied: dict[str, Any] = {}
    for key in CONTEXT_STATE_KEYS:
        value = context.get(key)
        if value in (None, "", ()):
            continue
        if key == "case":
            case = _enum_from_value(Case, value)
            if case is not None:
                copied["case"] = case
            continue
        if key == "role":
            role = _enum_from_value(Role, value)
            if role is not None:
                copied["role"] = role
            continue
        if key == "gender":
            gender = _enum_from_value(Gender, value)
            if gender is not None:
                copied["gender"] = gender
            continue
        if key == "lakara":
            lakara = _enum_from_value(Lakara, value)
            if lakara is not None:
                copied["lakara"] = lakara
            continue
        if key == "pada":
            pada = _enum_from_value(Pada, value)
            if pada is not None:
                copied["pada"] = pada
            continue
        if key == "compound_type":
            compound_type = _enum_from_value(SamasaType, value)
            if compound_type is not None:
                copied["compound_type"] = compound_type
            continue
        if key == "person":
            person = _enum_from_value(Person, value)
            if person is not None:
                copied["person"] = person
            continue
        if key == "number":
            number = _enum_from_value(GrammaticalNumber, value)
            if number is not None:
                copied["number"] = number
            continue
        copied[key] = value
    copied.update(metarule_context_features(context))
    return copied


def metarule_context_features(context: Mapping[str, Any]) -> dict[str, Any]:
    """Copy Adhyāya 1 paribhāṣā / kāraka fixture fields into coordinator state."""
    copied: dict[str, Any] = {}
    for key in METARULE_CONTEXT_KEYS:
        value = context.get(key)
        if value in (None, "", ()):
            continue
        copied[key] = value

    if context.get("ref_case"):
        copied["reference_case"] = context["ref_case"]
    if context.get("operation_target"):
        copied["reference_target"] = context["operation_target"]
    if context.get("is_in_dhatupatha"):
        copied["root_class"] = "dhatu"
    if context.get("in_compound") and context.get("is_first_named"):
        copied["samasa_role"] = "upasarjana"
    if context.get("is_sarvanama_stem") and context.get("following_suffix"):
        copied["optional_sarvanama"] = True
    if context.get("context") and not copied.get("role"):
        copied["karaka_context"] = context["context"]
    if context.get("verb"):
        copied["karaka_verb"] = context["verb"]
    if context.get("duration"):
        copied.setdefault("phonological_labels", frozenset({str(context["duration"])}))
    if context.get("suffix_class"):
        copied["suffix_class"] = context["suffix_class"]
    if context.get("person_label"):
        copied["person_label"] = context["person_label"]
    if context.get("position"):
        copied["gati_position"] = context["position"]
    if context.get("samjna") == "gati":
        copied.setdefault("samjnas", frozenset({Samjna.GATI}))
    if context.get("mapping") == "index_wise":
        copied["list_correspondence"] = True
    if context.get("competing_samjnas"):
        copied["samjna_priority"] = True
    if context.get("yoga_pramana") and context.get("absent"):
        copied["lup_inference"] = True
    return copied


def _derivation_context_from_features(features: Mapping[str, Any]) -> DerivationContext:
    suffix_surface = features.get("suffix")
    marker = features.get("marker")
    markers = frozenset({str(marker)}) if marker else frozenset()
    suffix = None
    if isinstance(suffix_surface, str) and suffix_surface:
        suffix = Suffix(
            suffix_surface,
            markers=markers,
            is_ardhadhatuka=bool(features.get("ardhadhatuka")),
        )
    return DerivationContext(
        root_lemma=str(features.get("root_lemma") or features.get("dhatu_lemma") or "") or None,
        suffix=suffix,
        has_dhatu_lopa=bool(features.get("dhatu_lopa")),
        is_it_augment=bool(features.get("it_augment")),
    )


def apply_phonological_to_form(
    form: str,
    features: Mapping[str, Any],
    assigned: tuple[str, ...],
) -> tuple[str, str | None]:
    """Apply guṇa/vṛddhi to a single sound or the last vowel of a form when tagged."""
    sound = features.get("sound")
    context = _derivation_context_from_features(features)
    labels: set[str] = set()
    for tag in assigned:
        parsed = _parse_assigned_tag(tag)
        if parsed is None:
            continue
        head, tail = parsed
        if not tail:
            continue
        if head == "samjna" or tail in PHONOLOGICAL_LABELS:
            labels.add(tail)

    if isinstance(sound, str) and sound:
        if "vrddhi" in labels or "vrddha" in labels:
            replacement = vrddhi(sound, context)
            if replacement != sound:
                if sound in form:
                    return form.replace(sound, replacement, 1), f"vrddhi:{sound}>{replacement}"
                return replacement, f"vrddhi:{sound}>{replacement}"
        if "guna" in labels:
            replacement = guna(sound, context)
            if replacement != sound:
                if sound in form:
                    return form.replace(sound, replacement, 1), f"guna:{sound}>{replacement}"
                return replacement, f"guna:{sound}>{replacement}"

    if form and ("vrddhi" in labels or "guna" in labels):
        from .phonology import tokenize_sounds, is_vowel

        sounds = tokenize_sounds(form)
        for index in range(len(sounds) - 1, -1, -1):
            if not is_vowel(sounds[index]):
                continue
            replacement = (
                vrddhi(sounds[index], context)
                if "vrddhi" in labels or "vrddha" in labels
                else guna(sounds[index], context)
            )
            if replacement == sounds[index]:
                continue
            sounds[index] = replacement
            new_form = "".join(sounds)
            op = "vrddhi" if "vrddhi" in labels or "vrddha" in labels else "guna"
            return new_form, f"{op}:final-vowel"
    return form, None


def features_from_adhyaya45_result(
    result: Any,
    *,
    context: Mapping[str, Any],
    sutra_id: str,
    existing_features: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Merge Adhyaya 4/5 engine output into coordinator state features."""
    base = dict(existing_features or {})
    merged = dict(contextual_features(context))
    surface = getattr(result, "surface", "") or ""
    if surface:
        merged["form"] = surface
        merged["surface"] = surface
    semantic = getattr(result, "semantic", None)
    if isinstance(semantic, str) and semantic:
        merged.setdefault("semantic", semantic)
    suffix = getattr(result, "suffix", None)
    if suffix is not None:
        merged["suffix"] = suffix.value if hasattr(suffix, "value") else suffix
    source = getattr(result, "source", None)
    if isinstance(source, str) and source:
        merged["source"] = source
    operations = tuple(getattr(result, "operations", ()) or ())
    if operations:
        merged["derivation_operations"] = operations
        merged["engine_operation"] = " + ".join(operations)
    family = getattr(result, "family", None)
    if isinstance(family, str) and family:
        merged["derivation_family"] = family
    for key, value in getattr(result, "state_features", ()) or ():
        merged[key] = value
    for key, value in merged.items():
        if key not in base or base.get(key) in (None, "", frozenset(), ()):
            base[key] = value
        elif key == "phonological_labels" and isinstance(value, frozenset):
            base[key] = frozenset(set(base.get(key) or ()) | set(value))
        elif key == "blocked_sutras":
            base[key] = tuple(dict.fromkeys(tuple(base.get(key) or ()) + tuple(value)))
    base["last_sutra"] = sutra_id
    return base


def features_from_engine_result(
    result: Any,
    *,
    context: Mapping[str, Any],
    assigned: tuple[str, ...] = (),
    existing_features: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Merge Adhyaya 6–8 engine output into coordinator state features."""
    base = dict(existing_features or {})
    merged = dict(contextual_features(context))
    merged.update(
        effects_from_assigned(
            assigned,
            existing_samjnas=base.get("samjnas") or frozenset(),
            existing_labels=base.get("phonological_labels") or frozenset(),
            existing_blocked_ops=base.get("blocked_operations") or frozenset(),
        )
    )
    output = getattr(result, "output", "") or ""
    if output:
        merged["form"] = output
        merged["surface"] = output
    operations = tuple(getattr(result, "operations", ()) or ())
    if operations:
        merged["engine_operation"] = " + ".join(operations)
        if not merged.get("sandhi_rule"):
            for op in operations:
                if op not in {"governance", "sandhi", "asiddha-tripadi", "tripadi-governance", "identity"}:
                    merged.setdefault("sandhi_rule", op)
                    break
    if "asiddha-tripadi" in operations or "tripadi-governance" in operations:
        merged["asiddha_scope"] = "tripadi"
    profile = getattr(result, "profile", None)
    if profile is not None:
        merged.setdefault("accent_domain", getattr(profile, "sutra_range", None))
        primary = getattr(profile, "primary", None)
        if primary is not None:
            merged["accent_output"] = f"{primary.token}:{primary.accent.value}"
    samjna = context.get("assigns_samjna")
    if isinstance(samjna, str) and samjna:
        merged.setdefault("assigns_samjna", samjna)
        if tail := SAMJNA_TAG_TO_ENUM.get(samjna):
            merged["samjnas"] = frozenset(set(base.get("samjnas") or ()) | {tail})
    blocked_by = tuple(getattr(result, "blocked_by", ()) or ())
    if blocked_by:
        merged["blocked_sutras"] = tuple(dict.fromkeys(tuple(base.get("blocked_sutras") or ()) + blocked_by))
    if context.get("rule_blocked") or context.get("blocks_rule"):
        merged.setdefault("blocked_operations", frozenset(set(base.get("blocked_operations") or ()) | {"tripadi-block"}))
    for key, value in merged.items():
        if key not in base or base.get(key) in (None, "", frozenset(), ()):
            base[key] = value
        elif key == "blocked_sutras":
            base[key] = tuple(dict.fromkeys(tuple(base.get(key) or ()) + tuple(value)))
    base["last_sutra"] = getattr(result, "sutra_id", None)
    return base


def merge_step_effects(
    *,
    assigned: tuple[str, ...],
    context: Mapping[str, Any],
    form: str = "",
    existing_features: Mapping[str, Any] | None = None,
) -> tuple[str, dict[str, Any], str | None]:
    """Combine assigned tags, context keys, and optional phonological surface change."""
    base = dict(existing_features or {})
    assigned_effects = effects_from_assigned(
        assigned,
        existing_samjnas=base.get("samjnas") or frozenset(),
        existing_labels=base.get("phonological_labels") or frozenset(),
        existing_blocked_ops=base.get("blocked_operations") or frozenset(),
    )
    context_effects = contextual_features(context)
    merged = {**context_effects, **assigned_effects}
    for key, value in context_effects.items():
        if key not in base:
            merged[key] = value
    after, phon_op = apply_phonological_to_form(form, {**context, **merged}, assigned)
    if phon_op:
        merged["form"] = after
        merged["surface"] = after
    return after, merged, phon_op


def has_meaningful_effect(
    *,
    before: str,
    after: str,
    features: Mapping[str, Any],
    blocked_by: tuple[str, ...] = (),
) -> bool:
    if before != after:
        return True
    if blocked_by:
        return True
    for key in MEANINGFUL_STATE_KEYS:
        value = features.get(key)
        if value in (None, "", frozenset(), ()):
            continue
        if key in {"samjnas", "phonological_labels", "blocked_operations"} and not value:
            continue
        return True
    return False


__all__ = [
    "CONTEXT_STATE_KEYS",
    "MEANINGFUL_STATE_KEYS",
    "apply_phonological_to_form",
    "contextual_features",
    "effects_from_assigned",
    "features_from_adhyaya45_result",
    "features_from_engine_result",
    "has_meaningful_effect",
    "merge_step_effects",
    "metarule_context_features",
    "METARULE_CONTEXT_KEYS",
]
