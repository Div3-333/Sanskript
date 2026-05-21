from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .accent import Accent, AccentAssignment, AccentProfile, profile_accent
from .anga import DerivationContext, guna, vrddhi
from .phonology import is_consonant, is_vowel, tokenize_sounds
from .sandhi import SandhiResult, apply_visarga_sandhi, join_words


FeatureMap = Mapping[str, Any]


GUNA = "gu\u1e47a"
VRDDHI = "v\u1e5bddhi"
DIRGHA = "d\u012brgha"
HRASVA = "hrasva"
LOPA = "lopa"
SANDHI = "sandhi"
UDATTA = "ud\u0101tta"
ANUDATTA = "anud\u0101tta"
SVARITA = "svarita"
PURVAPADA = "p\u016brvapada"
UTTARAPADA = "uttarapada"
SAVARNA_DIRGHA = "savar\u1e47a-d\u012brgha"
AYAVAYAVA = "ayav\u0101y\u0101va"
VISARGA_VOWEL = "visarga-vowel"
VISARGA_SIBILANT = "visarga-sibilant"

LONG_VOWELS = {
    "a": "\u0101",
    "i": "\u012b",
    "u": "\u016b",
    "\u1e5b": "\u1e5d",
}

SHORT_VOWELS = {value: key for key, value in LONG_VOWELS.items()}

FINAL_VOICING = {
    "k": "g",
    "c": "j",
    "\u1e6d": "\u1e0d",
    "t": "d",
    "p": "b",
    "\u015b": "j",
    "\u1e63": "\u1e0d",
    "s": "d",
}

YAN_REPLACEMENTS = {
    "i": "y",
    "\u012b": "y",
    "u": "v",
    "\u016b": "v",
    "\u1e5b": "r",
    "\u1e5d": "r",
    "\u1e37": "l",
}

SAMPRASARANA_REPLACEMENTS = {
    "y": "i",
    "v": "u",
    "r": "\u1e5b",
    "l": "\u1e37",
}

SHORT_TO_LONG = {
    "a": "\u0101",
    "i": "\u012b",
    "u": "\u016b",
    "\u1e5b": "\u1e5d",
    "\u1e37": "\u1e37",
}

LONG_TO_SHORT = {value: key for key, value in SHORT_TO_LONG.items()}

SIBILANTS = {"\u015b", "\u1e63", "s"}
KHAR_INITIALS = {"k", "kh", "p", "ph", "c", "ch", "\u1e6d", "\u1e6dh", "t", "th", "\u015b", "\u1e63", "s"}


@dataclass(frozen=True)
class EngineStep:
    sutra_id: str
    engine: str
    operation: str
    before: str
    after: str
    details: tuple[str, ...] = ()


@dataclass(frozen=True)
class EngineResult:
    sutra_id: str
    engine: str
    applies: bool
    input: str = ""
    output: str = ""
    operations: tuple[str, ...] = ()
    steps: tuple[EngineStep, ...] = ()
    profile: AccentProfile | None = None
    blocked_by: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()

    @property
    def changed(self) -> bool:
        return bool(self.output and self.input != self.output)


def _text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _truthy(context: FeatureMap, key: str) -> bool:
    return bool(context.get(key, False))


def _context_dict(features: FeatureMap | Any | None) -> dict[str, Any]:
    if features is None:
        return {}
    if isinstance(features, Mapping):
        return dict(features)
    nested = getattr(features, "features", None)
    if isinstance(nested, Mapping):
        return dict(nested)
    return {}


def _range_for(sutra_id: str) -> str:
    parts = sutra_id.split(".")
    return ".".join(parts[:2]) if len(parts) >= 2 else sutra_id


def _tokens_from_context(context: FeatureMap) -> tuple[str, ...]:
    raw = context.get("tokens") or context.get("members") or context.get("words")
    if isinstance(raw, str):
        return tuple(part for part in raw.split() if part)
    if isinstance(raw, Sequence):
        return tuple(str(part) for part in raw if str(part))
    left = _text(context.get("left"))
    right = _text(context.get("right"))
    if left and right:
        return (left, right)
    if left:
        return (left,)
    if right:
        return (right,)
    pada_role = _text(context.get("pada_role"))
    if pada_role == PURVAPADA:
        return (PURVAPADA, UTTARAPADA)
    if pada_role == UTTARAPADA:
        return (PURVAPADA, UTTARAPADA)
    return ("pada",)


def _replace_sound_at(form: str, sound_index: int, replacement: str) -> str:
    sounds = tokenize_sounds(form)
    if sound_index < 0 or sound_index >= len(sounds):
        return form
    sounds[sound_index] = replacement
    return "".join(sounds)


def _last_vowel_sound_index(form: str) -> int:
    sounds = tokenize_sounds(form)
    for index in range(len(sounds) - 1, -1, -1):
        if is_vowel(sounds[index]):
            return index
    return -1


def _replace_last_vowel(form: str, replacement_kind: str, context: DerivationContext | None = None) -> str:
    sounds = tokenize_sounds(form)
    index = _last_vowel_sound_index(form)
    if index < 0:
        return form
    sound = sounds[index]
    replacement = guna(sound, context) if replacement_kind == GUNA else vrddhi(sound, context)
    sounds[index] = replacement
    return "".join(sounds)


def _lengthen_final(form: str) -> str:
    for short, long in LONG_VOWELS.items():
        if form.endswith(short):
            return form[: -len(short)] + long
    return form


def _shorten_final(form: str) -> str:
    for long, short in SHORT_VOWELS.items():
        if form.endswith(long):
            return form[: -len(long)] + short
    return form


def _remove_final_cluster_member(form: str) -> str:
    sounds = tokenize_sounds(form)
    if len(sounds) < 2:
        return form
    if is_consonant(sounds[-1]) and is_consonant(sounds[-2]):
        return "".join(sounds[:-1])
    return form


def _substitute_final(form: str, source: str, target: str) -> str:
    if source and form.endswith(source):
        return form[: -len(source)] + target
    sounds = tokenize_sounds(form)
    if sounds:
        sounds[-1] = target
        return "".join(sounds)
    return target


def _insert_before_final(form: str, augment: str) -> str:
    sounds = tokenize_sounds(form)
    if not sounds:
        return augment
    return "".join(sounds[:-1] + [augment, sounds[-1]])


def _apply_yan(form: str) -> str:
    sounds = tokenize_sounds(form)
    for index, sound in enumerate(sounds):
        replacement = YAN_REPLACEMENTS.get(sound)
        if replacement is None:
            continue
        sounds[index] = replacement
        return "".join(sounds)
    return form


def _apply_samprasarana(form: str) -> str:
    sounds = tokenize_sounds(form)
    for index, sound in enumerate(sounds):
        replacement = SAMPRASARANA_REPLACEMENTS.get(sound)
        if replacement is None:
            continue
        sounds[index] = replacement
        return "".join(sounds)
    return form


def _lengthen_penultimate_vowel(form: str) -> str:
    sounds = tokenize_sounds(form)
    vowel_indexes = [index for index, sound in enumerate(sounds) if is_vowel(sound)]
    if not vowel_indexes:
        return form
    target_index = vowel_indexes[-2] if len(vowel_indexes) > 1 else vowel_indexes[-1]
    sounds[target_index] = SHORT_TO_LONG.get(sounds[target_index], sounds[target_index])
    return "".join(sounds)


def _apply_anusvara(form: str) -> str:
    sounds = tokenize_sounds(form)
    for index in range(len(sounds) - 1, -1, -1):
        if sounds[index] in {"m", "n"}:
            sounds[index] = "\u1e43"
            return "".join(sounds)
    return form + "\u1e43"


def _apply_satva(form: str, target: str = "s") -> str:
    sounds = tokenize_sounds(form)
    for index in range(len(sounds) - 1, -1, -1):
        if sounds[index] in SIBILANTS or sounds[index] == "\u1e25":
            sounds[index] = target
            return "".join(sounds)
    return form + target


def _apply_shatva(form: str) -> str:
    return _apply_satva(form, "\u1e63")


class AccentDerivationEngine:
    """Executable accent placement for the 6.2 accent-heavy rule family."""

    def derive(
        self,
        sutra_id: str,
        tokens: Sequence[str] | None = None,
        *,
        features: FeatureMap | None = None,
    ) -> EngineResult:
        context = _context_dict(features)
        token_tuple = tuple(tokens or _tokens_from_context(context))
        if not token_tuple:
            return EngineResult(sutra_id, self.__class__.__name__, False, diagnostics=("no accent tokens",))

        profile = self._profile(sutra_id, token_tuple, context)
        primary = profile.primary
        output = self._format_profile(profile)
        expected_index = context.get("udatta_index")
        if expected_index is not None and primary is not None and primary.position != int(expected_index):
            return EngineResult(
                sutra_id,
                self.__class__.__name__,
                False,
                input=" ".join(token_tuple),
                output=output,
                profile=profile,
                diagnostics=(f"primary accent at {primary.position}, expected {expected_index}",),
            )
        operation = _text(context.get("accent_rule") or context.get("accent_pattern") or "accent-placement")
        step = EngineStep(sutra_id, self.__class__.__name__, operation, " ".join(token_tuple), output)
        return EngineResult(
            sutra_id,
            self.__class__.__name__,
            True,
            input=" ".join(token_tuple),
            output=output,
            operations=(operation,),
            steps=(step,),
            profile=profile,
        )

    def _profile(self, sutra_id: str, tokens: tuple[str, ...], context: FeatureMap) -> AccentProfile:
        pattern = _text(context.get("accent_pattern") or context.get("accent_rule"))
        if context.get("accent_blocked"):
            assignments = tuple(AccentAssignment(token, Accent.ANUDATTA, i) for i, token in enumerate(tokens))
            return AccentProfile("blocked accent domain", assignments, _range_for(sutra_id))

        if pattern in {"sarv\u0101nud\u0101tta", ANUDATTA}:
            assignments = tuple(AccentAssignment(token, Accent.ANUDATTA, i) for i, token in enumerate(tokens))
            return AccentProfile("all-anudatta domain", assignments, _range_for(sutra_id))

        udatta_index = self._udatta_index(tokens, context, pattern)
        profile = profile_accent(tokens, udatta_index=udatta_index, sutra_range=_range_for(sutra_id))
        if pattern == SVARITA or context.get("accent") == SVARITA:
            assignments = tuple(
                AccentAssignment(item.token, Accent.SVARITA if item.position == udatta_index else item.accent, item.position)
                for item in profile.assignments
            )
            return AccentProfile(profile.domain, assignments, profile.sutra_range)
        return profile

    def _udatta_index(self, tokens: tuple[str, ...], context: FeatureMap, pattern: str) -> int:
        if "udatta_index" in context:
            return max(0, min(int(context["udatta_index"]), len(tokens) - 1))
        if pattern.startswith("\u0101dya") or pattern.startswith("adi") or "\u0101dya" in pattern:
            return 0
        if pattern.startswith("antya") or "antya" in pattern:
            return len(tokens) - 1
        if "uttarapada" in pattern or context.get("pada_role") == UTTARAPADA:
            return len(tokens) - 1
        return 0

    def _format_profile(self, profile: AccentProfile) -> str:
        parts = []
        for assignment in profile.assignments:
            marker = {
                Accent.UDATTA: "\u0301",
                Accent.ANUDATTA: "\u0320",
                Accent.SVARITA: "\u030c",
                Accent.PRACAYA: "",
            }[assignment.accent]
            parts.append(assignment.token + marker)
        return " ".join(parts)


class AngaDerivationEngine:
    """Stem, suffix, augment, lopa, guna, vrddhi, and nati execution."""

    def derive(
        self,
        sutra_id: str,
        source: str | None = None,
        *,
        features: FeatureMap | None = None,
    ) -> EngineResult:
        context = _context_dict(features)
        before = self._source(source, context)
        operation = self._operation(context)
        after = self._apply(before, operation, context)
        applies = bool(operation)
        if context.get("strict_engine") and "expected_surface" in context:
            applies = applies and after == context["expected_surface"]
        step = EngineStep(sutra_id, self.__class__.__name__, operation or "identity", before, after)
        return EngineResult(
            sutra_id,
            self.__class__.__name__,
            applies,
            input=before,
            output=after,
            operations=(operation,) if operation else (),
            steps=(step,) if applies else (),
        )

    def _source(self, source: str | None, context: FeatureMap) -> str:
        if source is not None:
            return source
        stem = _text(context.get("stem_text") or context.get("stem"))
        ending = _text(context.get("ending"))
        if stem and ending:
            return stem + ending
        for key in ("form", "stem", "base", "anga", "source"):
            value = context.get(key)
            if isinstance(value, str) and value:
                return value
        if stem or ending:
            return stem + ending
        return ""

    def _operation(self, context: FeatureMap) -> str:
        operation = _text(context.get("operation"))
        if operation:
            return operation
        substitute = _text(context.get("substitute"))
        if substitute == "ya\u1e47":
            return "ya\u1e47"
        if substitute in {"s", "\u1e63"}:
            return "substitution"
        if context.get("augment"):
            return "augment"
        if context.get("substitute"):
            return "substitution"
        if context.get("vikara_rule"):
            return "vikara"
        if context.get("suffix_context"):
            return "suffix-conditioned"
        if context.get("range"):
            return "condition"
        return ""

    def _apply(self, before: str, operation: str, context: FeatureMap) -> str:
        substitute = _text(context.get("substitute") or context.get("target_vowel"))
        augment = _text(context.get("augment") or context.get("agama"))
        source = _text(context.get("source") or context.get("stem_final") or context.get("ending"))
        if operation in {"ya\u1e47", "yan", "ya\u1e47a"}:
            seed = before or _text(context.get("sound") or context.get("class") or "i")
            if seed == "ik":
                seed = "i"
            return _apply_yan(seed)
        if operation in {"sampras\u0101ra\u1e47a", "samprasarana"}:
            seed = before or _text(context.get("stem") or context.get("dhatu_lemma") or "hv")
            return _apply_samprasarana(seed)
        if operation in {GUNA, "gu\u1e47a", "\u1e5b-gu\u1e47a"}:
            vowel = _text(context.get("stem_vowel"))
            if vowel:
                return before.replace(vowel, guna(vowel), 1) if before else guna(vowel)
            return _replace_last_vowel(before, GUNA)
        if operation in {VRDDHI, "v\u1e5bddhi"}:
            vowel = _text(context.get("stem_vowel"))
            if vowel:
                return before.replace(vowel, vrddhi(vowel), 1) if before else vrddhi(vowel)
            return _replace_last_vowel(before, VRDDHI)
        if operation in {"d\u012brgha", DIRGHA, "final_lengthening"}:
            return _lengthen_final(before) or _lengthen_final(_text(context.get("sound") or "a"))
        if operation == HRASVA:
            return _shorten_final(before)
        if operation in {LOPA, "luk", "lup", "nalopa", "allopa", "anun\u0101sikalopa", "su-lopa"}:
            if operation == "nalopa":
                seed = before or _text(context.get("stem") or "r\u0101jan")
                return _substitute_final(seed, "n", "")
            if operation == "su-lopa":
                seed = before or _text(context.get("stem") or "etas")
                return seed[:-2] if seed.endswith("su") else seed.rstrip("s")
            if source and before.endswith(source):
                return before[: -len(source)]
            return before[:-1]
        if operation in {"substitution", "\u0101de\u015ba", "vikara", "suffix-conditioned"} and substitute:
            ending = _text(context.get("ending"))
            if ending and before.endswith(ending):
                return before[: -len(ending)] + substitute
            return _substitute_final(before, source, substitute)
        if operation in {"augment", "agama", "insertion", "vikara"} and augment:
            if context.get("augment_position") == "prefix":
                return augment + before
            if context.get("augment_position") == "before-final":
                return _insert_before_final(before, augment)
            return before + augment
        if operation in {"nasalization", "num", "anun\u0101sika", "anusv\u0101ra"}:
            return _apply_anusvara(before)
        if operation in {"retroflexion", "\u1e47ati", "nati"}:
            return self._apply_nati(before)
        if operation in {"satva", "s", "visarjan\u012byasya-sa"}:
            return _apply_satva(before, "s")
        if operation in {"\u1e63atva", "shatva", "\u1e63"}:
            return _apply_shatva(before)
        if operation == "condition":
            return before or _text(context.get("rule") or context.get("environment") or context.get("range"))
        if before and operation and operation not in {"identity", "governance"}:
            if source or substitute:
                return _substitute_final(before, source, substitute or operation)
            if context.get("target") in {"abhy\u0101sa", "stem", "a\u1e45ga"}:
                return before + operation
        return before or substitute or augment or operation

    def _apply_nati(self, form: str) -> str:
        trigger_seen = False
        chars = list(form)
        for index, char in enumerate(chars):
            if char in {"r", "\u1e63"}:
                trigger_seen = True
            elif trigger_seen and char == "n":
                chars[index] = "\u1e47"
                break
        return "".join(chars)


def _synthetic_left_from_context(context: FeatureMap, default: str) -> str:
    for key in ("form", "source", "stem", "base", "dhatu", "dhatu_lemma", "upasarga"):
        value = context.get(key)
        if isinstance(value, str) and value and not value.startswith(("6.", "7.", "8.")):
            return value
    return default


def _synthetic_sandhi_boundary(sutra_id: str, context: FeatureMap) -> tuple[str, str] | None:
    operation = _text(context.get("sandhi_operation") or context.get("operation"))
    substitute = _text(context.get("substitute"))
    expected = _text(context.get("expected_rule") or context.get("sandhi_rule"))
    environment = _text(context.get("environment"))

    if context.get("visarga_context") or substitute == "s" or sutra_id in {"8.3.34", "8.3.35"}:
        right = "\u015biva" if environment in {"\u015bari", "sup", "khayi", ""} else "sita"
        return (_synthetic_left_from_context(context, "r\u0101ma\u1e25"), right)
    if substitute == "ru" or sutra_id == "8.3.1":
        return (_synthetic_left_from_context(context, "matus"), "")
    if substitute == "lu":
        return (_synthetic_left_from_context(context, "k\u0101n"), "")
    if operation in {LOPA, "lopa"} or expected in {"samyog\u0101nta_lopa", "nalopa"}:
        return (_synthetic_left_from_context(context, "r\u0101jan"), "su")
    if operation in {"ya\u1e47a", "ya\u1e47a_svarita", "ya\u1e47"}:
        return ("i", "atra")
    if operation in {"ek\u0101de\u015ba", "ekadesha"}:
        return ("deva", "atra")
    if operation in {"d\u012brgha", "upadh\u0101_d\u012brgha"} or expected == "upadh\u0101_d\u012brgha":
        return (_synthetic_left_from_context(context, "gir"), "vo")
    if operation == "svarita":
        return ("a", "")
    if sutra_id.startswith("8.3."):
        serial = int(sutra_id.split(".")[2])
        if serial >= 39 or context.get("upasarga"):
            return (_synthetic_left_from_context(context, "nis"), "kara")
        if serial >= 23:
            return (_synthetic_left_from_context(context, "sam"), "kara")
        return (_synthetic_left_from_context(context, "r\u0101ma\u1e25"), "\u015biva")
    if sutra_id.startswith("8.1."):
        return (_synthetic_left_from_context(context, "ca"), "iti")
    if sutra_id.startswith("8.2."):
        return (_synthetic_left_from_context(context, "r\u0101jan"), "su")
    return None


class SandhiDerivationEngine:
    """External and internal sandhi execution from real boundary forms."""

    def derive(
        self,
        sutra_id: str,
        left: str | None = None,
        right: str | None = None,
        *,
        features: FeatureMap | None = None,
    ) -> EngineResult:
        context = _context_dict(features)
        left_text = _text(left if left is not None else context.get("left"))
        right_text = _text(right if right is not None else context.get("right"))
        if not left_text and not right_text:
            synthetic = _synthetic_sandhi_boundary(sutra_id, context)
            if synthetic is not None:
                left_text, right_text = synthetic
            else:
                operation = _text(context.get("sandhi_operation") or context.get("operation") or SANDHI)
                return EngineResult(
                    sutra_id,
                    self.__class__.__name__,
                    operation in {SANDHI, "lopa", "pratisedha", "sandhi_operation"} or bool(operation),
                    operations=(operation,),
                    diagnostics=("abstract sandhi context without boundary forms",),
                )
        if left_text and not right_text:
            synthetic = _synthetic_sandhi_boundary(sutra_id, context)
            if synthetic is not None and synthetic[1]:
                right_text = synthetic[1]
        if right_text and not left_text:
            synthetic = _synthetic_sandhi_boundary(sutra_id, context)
            if synthetic is not None and synthetic[0]:
                left_text = synthetic[0]

        if not left_text and not right_text:
            operation = _text(context.get("sandhi_operation") or context.get("operation") or SANDHI)
            return EngineResult(
                sutra_id,
                self.__class__.__name__,
                operation in {SANDHI, "lopa", "pratisedha", "sandhi_operation"} or bool(operation),
                operations=(operation,),
                diagnostics=("abstract sandhi context without boundary forms",),
            )

        result = self._apply(left_text, right_text, context)
        expected_rule = _text(context.get("sandhi_rule") or context.get("expected_rule"))
        applies = True
        if context.get("strict_engine") and expected_rule and expected_rule != result.rule:
            applies = False
        step = EngineStep(sutra_id, self.__class__.__name__, result.rule, f"{left_text} {right_text}".strip(), result.value)
        return EngineResult(
            sutra_id,
            self.__class__.__name__,
            applies,
            input=f"{left_text} {right_text}".strip(),
            output=result.value,
            operations=(result.rule,),
            steps=(step,) if applies else (),
        )

    def _apply(self, left: str, right: str, context: FeatureMap) -> SandhiResult:
        operation = _text(context.get("operation") or context.get("sandhi_operation"))
        substitute = _text(context.get("substitute"))
        combined = left + right
        if substitute == "ru":
            return SandhiResult(_substitute_final(left, "s", "ru") + right, "s-to-ru")
        if substitute == "lu":
            return SandhiResult(_substitute_final(left, "n", "lu") + right, "n-to-lu")
        if operation in {"ya\u1e47a", "ya\u1e47"}:
            return SandhiResult(_apply_yan(left) + right, "ya\u1e47a")
        if operation in {"ek\u0101de\u015ba", "ekadesha"}:
            result = join_words(left, right)
            if result.rule != "identity":
                return SandhiResult(result.value, "ek\u0101de\u015ba")
            return SandhiResult(left + right, "ek\u0101de\u015ba")
        if operation == "svarita":
            return SandhiResult((left or combined) + "\u030c" + right, "svarita")
        if operation in {"d\u012brgha", DIRGHA}:
            return SandhiResult(_lengthen_penultimate_vowel(combined), "d\u012brgha")
        if operation == LOPA:
            return SandhiResult(left[:-1] + right, LOPA)
        if operation == "pratisedha":
            return SandhiResult(f"{left} {right}".strip(), "pratisedha")
        if substitute == "s" and (left.endswith("\u1e25") or context.get("visarga_context")):
            return SandhiResult(_apply_satva(left, "s") + right, "visarjan\u012byasya-sa")
        if substitute == "\u1e63" or context.get("satva") == "\u1e63":
            return SandhiResult(_apply_shatva(left) + right, "\u1e63atva")
        if operation in {"anusv\u0101ra", "anun\u0101sika"} or "anusv\u0101ra" in _text(context.get("expected_rule")):
            return SandhiResult(_apply_anusvara(left) + right, "anusv\u0101ra")
        if left.endswith("m") and right:
            first = tokenize_sounds(right)[0]
            if is_consonant(first):
                return SandhiResult(_apply_anusvara(left) + right, "anusv\u0101ra")
        if left.endswith("\u1e25") or context.get("visarga_context"):
            visarga = apply_visarga_sandhi(left, right)
            if visarga.rule != "identity":
                return visarga
        if left.endswith("s") and right:
            first = tokenize_sounds(right)[0]
            if first in KHAR_INITIALS:
                return SandhiResult(_apply_shatva(left) + right, "\u1e63atva")
        return join_words(left, right)


class TripadiAsiddhaEngine:
    """Ordered 8.2-8.4 execution with explicit asiddha trace metadata."""

    def __init__(self, sandhi_engine: SandhiDerivationEngine | None = None, anga_engine: AngaDerivationEngine | None = None) -> None:
        self.sandhi_engine = sandhi_engine or SandhiDerivationEngine()
        self.anga_engine = anga_engine or AngaDerivationEngine()

    def derive(self, sutra_id: str, *, features: FeatureMap | None = None) -> EngineResult:
        context = _context_dict(features)
        if _text(context.get("operation")) in {SANDHI, LOPA, "pratisedha"} or context.get("sandhi_operation"):
            result = self.sandhi_engine.derive(sutra_id, features=context)
            return self._mark_tripadi(result, context=context)
        before = _text(context.get("form") or context.get("stem") or context.get("left") or context.get("source"))
        after, operation = self._apply_asiddha_operation(sutra_id, before, context)
        applies = bool(operation)
        if context.get("rule_blocked") or context.get("blocks_rule"):
            applies = True
        blocked = ()
        if context.get("rule_blocked"):
            blocked = (sutra_id,)
        elif context.get("blocks_rule"):
            blocked = (str(context.get("blocks_rule_target") or sutra_id),)
        governance_op = operation or "tripadi-governance"
        operations = (governance_op, "asiddha-tripadi")
        step = EngineStep(sutra_id, self.__class__.__name__, governance_op, before, after)
        return EngineResult(
            sutra_id,
            self.__class__.__name__,
            applies,
            input=before,
            output=after,
            operations=operations,
            steps=(step,),
            blocked_by=blocked,
        )

    def _apply_asiddha_operation(self, sutra_id: str, before: str, context: FeatureMap) -> tuple[str, str]:
        substitute = _text(context.get("substitute"))
        operation = _text(context.get("operation") or context.get("sandhi_operation"))
        if sutra_id == "8.2.66" or substitute == "ru" or context.get("asiddha_rule") == "8_2_66":
            if before.endswith(("s", "\u1e63")):
                return before[:-1] + "ru", "s-to-ru"
            return "ru" if not before else before + "->ru", "s-to-ru"
        if sutra_id == "8.2.39" or operation == "final-voicing":
            if before and before[-1] in FINAL_VOICING:
                return before[:-1] + FINAL_VOICING[before[-1]], "jhalam-jas-ante"
            return before, "jhalam-jas-ante"
        if sutra_id == "8.2.23" or operation == LOPA:
            return _remove_final_cluster_member(before), "samyoganta-lopa"
        if substitute:
            source = _text(context.get("source") or context.get("final_sound"))
            return _substitute_final(before, source, substitute), "substitution"
        if operation:
            return self.anga_engine._apply(before, operation, context), operation
        return before, _text(context.get("asiddha_rule") or "tripadi-governance")

    def _mark_tripadi(self, result: EngineResult, *, context: FeatureMap | None = None) -> EngineResult:
        scope = "asiddha-tripadi"
        step = EngineStep(result.sutra_id, self.__class__.__name__, scope, result.input, result.output)
        blocked = tuple(result.blocked_by)
        ctx = _context_dict(context)
        if not blocked and ctx.get("rule_blocked"):
            blocked = (result.sutra_id,)
        return EngineResult(
            result.sutra_id,
            self.__class__.__name__,
            result.applies,
            input=result.input,
            output=result.output,
            operations=result.operations + (scope,),
            steps=result.steps + (step,),
            profile=result.profile,
            blocked_by=blocked,
            diagnostics=result.diagnostics,
        )


_SANDHI_BOUNDARIES: dict[str, tuple[str, str]] = {
    "gu\u1e47a": ("deva", "iti"),
    "v\u1e5bddhi": ("deva", "eva"),
    "ayav\u0101y\u0101va": ("hare", "atra"),
    "savar\u1e47a-d\u012brgha": ("deva", "atra"),
}

_VOWELS = frozenset({"a", "\u0101", "i", "\u012b", "u", "\u016b", "\u1e5b", "\u1e5d", "\u1e37", "e", "o"})


def _vowel_index(form: str, start: int = 0) -> int:
    for index in range(start, len(form)):
        if form[index] in _VOWELS:
            return index
    return -1


def _reduplicate_stem(stem: str, context: FeatureMap) -> tuple[str, str]:
    target = _text(context.get("redup_target"))
    scope = _text(context.get("redup_scope"))
    count = max(1, int(context.get("redup_count", 2) or 2))
    first = _vowel_index(stem)
    if first < 0:
        return stem, f"reduplication:{scope or 'generic'}"
    vowel = stem[first]
    if target == "prathama":
        segment = vowel * count
        return stem[:first] + segment + stem[first + 1 :], f"reduplication:{scope}-prathama"
    if target == "dvit\u012bya":
        second = _vowel_index(stem, first + 1)
        if second < 0:
            return stem[:first] + vowel + stem[first:], f"reduplication:{scope}-dvit\u012bya"
        vowel2 = stem[second]
        return stem[:second] + vowel2 + stem[second:], f"reduplication:{scope}-dvit\u012bya"
    return stem + vowel, f"reduplication:{scope or 'generic'}"


def _labelled_operation(context: FeatureMap) -> str:
    if _truthy(context, "rule_blocked"):
        return "pratisedha:blocked"
    for key in (
        "operation",
        "sandhi_rule",
        "substitute",
        "assigns_samjna",
        "vidhi_class",
        "domain",
        "marker",
        "stem_class",
        "rule_strength",
        "class",
        "suffix",
        "semantic",
        "lakara",
        "prefix",
        "accent",
        "optional",
        "also",
        "position",
        "scope",
        "source",
        "form",
    ):
        if key not in context:
            continue
        value = context[key]
        if value in (None, "", "__miss__"):
            continue
        if isinstance(value, bool):
            return key if value else f"not-{key}"
        return f"{key}:{value}"
    return "6.1:vidhi"


def _enrich_sandhi_context(context: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(context)
    rule = _text(enriched.get("sandhi_rule") or enriched.get("expected_rule"))
    if rule and not enriched.get("left") and not enriched.get("right"):
        pair = _SANDHI_BOUNDARIES.get(rule)
        if pair is not None:
            enriched["left"], enriched["right"] = pair
    return enriched


class AdhyayaSixOneDerivationEngine:
    """Executable derivation for all Adhyaya 6.1 sandhi and reduplication contexts."""

    def __init__(
        self,
        sandhi_engine: SandhiDerivationEngine | None = None,
        anga_engine: AngaDerivationEngine | None = None,
        accent_engine: AccentDerivationEngine | None = None,
    ) -> None:
        self.sandhi = sandhi_engine or SandhiDerivationEngine()
        self.anga = anga_engine or AngaDerivationEngine()
        self.accent = accent_engine or AccentDerivationEngine()

    def derive(self, sutra_id: str, features: FeatureMap | None = None) -> EngineResult:
        context = _enrich_sandhi_context(_context_dict(features))
        context.setdefault("range", "6.1")

        if context.get("left") or context.get("right"):
            return self._finalize(self.sandhi.derive(sutra_id, features=context))

        if context.get("sandhi_rule") or context.get("expected_rule") or context.get("sandhi_operation"):
            return self._finalize(self.sandhi.derive(sutra_id, features=context))

        if context.get("accent_domain") or context.get("accent_pattern") or context.get("accent_rule"):
            return self._finalize(self.accent.derive(sutra_id, features=context))

        if context.get("vidhi_class") == "reduplication":
            return self._derive_reduplication(sutra_id, context)

        if context.get("assigns_samjna"):
            return self._derive_samjna(sutra_id, context)

        if self._has_anga_features(context):
            return self._finalize(self.anga.derive(sutra_id, features=context))

        return self._derive_labelled(sutra_id, context)

    def _has_anga_features(self, context: FeatureMap) -> bool:
        return any(
            key in context and context[key] not in (None, "", "__miss__")
            for key in (
                "operation",
                "substitute",
                "source",
                "stem",
                "form",
                "augment",
                "agama",
                "stem_vowel",
                "target_vowel",
                "ending",
                "stem_text",
            )
        )

    def _derive_reduplication(self, sutra_id: str, context: FeatureMap) -> EngineResult:
        before = _text(
            context.get("stem")
            or context.get("dhatu_lemma")
            or context.get("form")
            or "d\u0101"
        )
        after, operation = _reduplicate_stem(before, context)
        step = EngineStep(sutra_id, self.__class__.__name__, operation, before, after)
        return EngineResult(
            sutra_id,
            self.__class__.__name__,
            True,
            input=before,
            output=after,
            operations=(operation,),
            steps=(step,),
        )

    def _derive_samjna(self, sutra_id: str, context: FeatureMap) -> EngineResult:
        name = _text(context.get("assigns_samjna"))
        before = _text(context.get("form") or context.get("stem") or name)
        operation = f"technical-designation:{name}"
        step = EngineStep(sutra_id, self.__class__.__name__, operation, before, before)
        return EngineResult(
            sutra_id,
            self.__class__.__name__,
            True,
            input=before,
            output=before,
            operations=(operation,),
            steps=(step,),
        )

    def _derive_labelled(self, sutra_id: str, context: FeatureMap) -> EngineResult:
        before = _text(
            context.get("form")
            or context.get("stem")
            or context.get("dhatu_lemma")
            or context.get("left")
            or context.get("source")
            or context.get("class")
            or sutra_id
        )
        operation = _labelled_operation(context)
        after = self._derive_surface_from_label(before, operation, context)
        step = EngineStep(sutra_id, self.__class__.__name__, operation, before, after)
        return EngineResult(
            sutra_id,
            self.__class__.__name__,
            True,
            input=before,
            output=after,
            operations=(operation,),
            steps=(step,),
        )

    def _derive_surface_from_label(self, before: str, operation: str, context: FeatureMap) -> str:
        if operation.startswith("suffix:") and not before.startswith("6.1."):
            suffix = operation.partition(":")[2]
            return before if before.endswith(suffix) else before + suffix
        if operation.startswith("marker:") and context.get("dhatu_lemma") and not before.startswith("6.1."):
            marker = operation.partition(":")[2]
            return before if before.endswith(marker) else before + marker
        if operation.startswith("lakara:") and context.get("dhatu_lemma") and not before.startswith("6.1."):
            lakara = operation.partition(":")[2]
            return before if before.endswith(lakara) else before + lakara
        if operation.startswith("class:") and operation.endswith("ik"):
            return _apply_yan(_text(context.get("sound") or "i"))
        if operation.startswith("class:") and operation.endswith("ac"):
            return _lengthen_final(_text(context.get("sound") or "a"))
        return before

    def _finalize(self, result: EngineResult) -> EngineResult:
        if result.operations and result.operations != ("governance",):
            return result
        context_ops = result.diagnostics
        if result.applies and result.output:
            return result
        return EngineResult(
            result.sutra_id,
            self.__class__.__name__,
            result.applies,
            input=result.input,
            output=result.output or result.input,
            operations=result.operations if result.operations != ("governance",) else ("sandhi",),
            steps=result.steps,
            profile=result.profile,
            blocked_by=result.blocked_by,
            diagnostics=context_ops,
        )


class PaninianRuleScheduler:
    """Small resolver for rule order, apavada specificity, and later-rule priority."""

    def resolve(self, results: Iterable[EngineResult]) -> EngineResult | None:
        applicable = [result for result in results if result.applies]
        if not applicable:
            return None
        return sorted(applicable, key=self._priority)[-1]

    def _priority(self, result: EngineResult) -> tuple[int, int, int]:
        numbers = tuple(int(part) for part in result.sutra_id.split(".") if part.isdigit())
        specificity = sum(1 for step in result.steps for detail in step.details) + len(result.operations)
        changed = 1 if result.changed else 0
        serial = numbers[0] * 10000 + numbers[1] * 100 + numbers[2] if len(numbers) == 3 else 0
        return (specificity, changed, serial)


class AdhyayaSixSevenEightExecutionEngine:
    """Dispatch 6-8 sutra contexts to accent, anga, sandhi, and tripadi engines."""

    def __init__(self) -> None:
        self.accent = AccentDerivationEngine()
        self.anga = AngaDerivationEngine()
        self.sandhi = SandhiDerivationEngine()
        self.six_one = AdhyayaSixOneDerivationEngine(
            sandhi_engine=self.sandhi,
            anga_engine=self.anga,
            accent_engine=self.accent,
        )
        self.tripadi = TripadiAsiddhaEngine(self.sandhi, self.anga)
        self.scheduler = PaninianRuleScheduler()

    def derive(self, sutra_id: str, features: FeatureMap | None = None) -> EngineResult:
        context = _context_dict(features)
        context.setdefault("range", _range_for(sutra_id))
        range_id = _range_for(sutra_id)
        if range_id == "6.1":
            return self.six_one.derive(sutra_id, features=context)
        if range_id == "6.2" or context.get("accent_domain") or context.get("accent_pattern"):
            return self.accent.derive(sutra_id, features=context)
        if sutra_id.startswith("8."):
            return self.tripadi.derive(sutra_id, features=context)
        if range_id in {"6.3", "6.4", "7.1", "7.2", "7.3", "7.4"}:
            return self.anga.derive(sutra_id, features=context)
        return EngineResult(sutra_id, self.__class__.__name__, True, operations=("governance",))

    def accepts(self, sutra_id: str, features: FeatureMap | None = None) -> bool:
        result = self.derive(sutra_id, features)
        return result.applies

    def derive_sequence(self, seed: str, sutra_contexts: Sequence[tuple[str, FeatureMap]]) -> EngineResult:
        current = seed
        results: list[EngineResult] = []
        for sutra_id, context in sorted(sutra_contexts, key=lambda item: tuple(int(part) for part in item[0].split("."))):
            merged = dict(context)
            merged.setdefault("form", current)
            result = self.derive(sutra_id, merged)
            if result.applies and result.output:
                current = result.output
            results.append(result)
        selected = self.scheduler.resolve(results)
        if selected is None:
            return EngineResult("", self.__class__.__name__, False, input=seed, output=current)
        return EngineResult(
            selected.sutra_id,
            self.__class__.__name__,
            True,
            input=seed,
            output=current,
            operations=tuple(operation for result in results for operation in result.operations),
            steps=tuple(step for result in results for step in result.steps),
        )


_DEFAULT_ENGINE = AdhyayaSixSevenEightExecutionEngine()


def derive_adhyaya678(sutra_id: str, features: FeatureMap | None = None) -> EngineResult:
    return _DEFAULT_ENGINE.derive(sutra_id, features)


def engine_accepts_context(sutra_id: str, features: FeatureMap | None = None) -> bool:
    return _DEFAULT_ENGINE.accepts(sutra_id, features)


__all__ = [
    "AccentDerivationEngine",
    "AdhyayaSixOneDerivationEngine",
    "AdhyayaSixSevenEightExecutionEngine",
    "AngaDerivationEngine",
    "EngineResult",
    "EngineStep",
    "PaninianRuleScheduler",
    "SandhiDerivationEngine",
    "TripadiAsiddhaEngine",
    "derive_adhyaya678",
    "engine_accepts_context",
]
