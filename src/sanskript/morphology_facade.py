"""Hot-path morphology: cache-first lexicon lookup with bounded synthesis fallback."""

from __future__ import annotations

from dataclasses import dataclass

from .adhyaya123_engines import KarakaVibhaktiEngine
from .errors import MorphologyError, ParseError
from .grammar import VERB_FRAMES, Analysis, CASE_TO_ROLE, Case, PartOfSpeech, Role
from .grammar_register import runtime_register_entries
from .morphology_text import normalize, split_sentences, tokenize as _tokenize_words
from .morphology_lexicon import DEFAULT_LEXICON_PATH, load_controlled_lexicon, merge_lexicon_with_overrides, store_preferred
from .morphology_synth import MorphologySynthesizer, synthesize
from .transliteration import devanagari_to_iast


MAX_UNKNOWN_CANDIDATES = 64


@dataclass
class MorphologyFacade:
    """Single morphology entry point for parser and CLI."""

    strict: bool = True
    lexicon_path: str | None = None

    def __post_init__(self) -> None:
        from pathlib import Path

        path = DEFAULT_LEXICON_PATH if self.lexicon_path is None else Path(self.lexicon_path)
        artifact = load_controlled_lexicon(path, apply_overrides=False) if path.exists() else {}
        if not artifact:
            synthesizer = MorphologySynthesizer()
            artifact = {}
            for entry in runtime_register_entries():
                result = synthesizer.synthesize(entry.intent)
                store_preferred(artifact, result.analysis, force=entry.authoritative)
        self._lexicon = merge_lexicon_with_overrides(dict(artifact))
        self._session_cache: dict[str, Analysis] = {}
        self._synthesizer = MorphologySynthesizer()
        self._karaka = KarakaVibhaktiEngine()
        self._register_by_surface = _index_register_by_surface()

    def analyze_token(self, token: str) -> Analysis:
        normalized = self.normalize_token(token)
        if normalized in self._session_cache:
            return self._session_cache[normalized]
        if normalized in self._lexicon:
            analysis = self._lexicon[normalized]
            self._session_cache[normalized] = analysis
            return analysis
        matches = self._analyze_unknown(normalized)
        if not matches:
            raise MorphologyError(
                f"Form {normalized!r} is not in the controlled Sanskrit register. "
                "Add it to the grammar register and rebuild the lexicon.",
                hint="Run `python scripts/build_controlled_lexicon.py` after adding the form.",
            )
        if len(matches) > 1:
            options = ", ".join(sorted({item.lemma for item in matches}))
            raise MorphologyError(
                f"Form {normalized!r} is ambiguous in the controlled register ({options}).",
                hint="Use a less ambiguous registered form or add parser context for this frame.",
            )
        analysis = matches[0]
        self._session_cache[normalized] = analysis
        self._lexicon[normalized] = analysis
        return analysis

    def analyze_sentence(self, sentence: str) -> list[Analysis]:
        return [self.analyze_token(token) for token in _tokenize_words(sentence, normalize_token=self.normalize_token)]

    def normalize_token(self, token: str) -> str:
        text = normalize(token)
        if _contains_devanagari(text):
            text = devanagari_to_iast(text)
        return text.lower()

    def validate_karaka(self, analyses: list[Analysis], verb: Analysis) -> None:
        frame = VERB_FRAMES.get(verb.surface)
        if frame is None:
            raise ParseError(
                f"No verb frame has been declared for {verb.surface!r}",
                hint="Declare the surface in data/verb_frames.json and rebuild the lexicon.",
            )

        roles_present = _roles_by_type(item for item in analyses if item.pos != PartOfSpeech.VERB)
        missing = frame.required_roles - roles_present.keys()
        if missing:
            missing_text = ", ".join(role.value for role in sorted(missing, key=lambda role: role.value))
            raise ParseError(f"{verb.surface} needs participant role(s): {missing_text}")

        for item in analyses:
            if item.role is None or item.pos == PartOfSpeech.VERB:
                continue

            if item.case is not None:
                case_role = CASE_TO_ROLE.get(item.case)
                if case_role is not None and case_role != item.role:
                    raise ParseError(
                        f"{item.surface!r} has role {item.role.value}, "
                        f"but {item.case.value} case assigns {case_role.value}"
                    )

            if item.role not in frame.required_roles:
                continue

            if item.role == Role.KARTR and item.case == Case.NOMINATIVE:
                continue

            semantic = "companion" if item.role == Role.KARMAN and item.pos == PartOfSpeech.NOUN else None
            selection = self._karaka.select_case(
                role=item.role,
                companion_lemma=item.lemma if semantic else None,
                semantic_context=semantic,
            )
            if item.case is not None and selection.case != item.case:
                raise ParseError(
                    f"{item.surface!r} has case {item.case.value}, "
                    f"but kāraka selection expects {selection.case.value} for {item.role.value}"
                )

    def _analyze_unknown(self, surface: str) -> list[Analysis]:
        candidates = self._register_by_surface.get(surface, ())
        if len(candidates) > MAX_UNKNOWN_CANDIDATES:
            candidates = candidates[:MAX_UNKNOWN_CANDIDATES]
        matches: list[Analysis] = []
        for entry in candidates:
            result = self._synthesizer.synthesize(entry.intent)
            if result.surface == surface:
                matches.append(result.analysis)
        return matches


def _index_register_by_surface() -> dict[str, tuple]:
    from .grammar_register import RegisterEntry

    by_surface: dict[str, list[RegisterEntry]] = {}
    for entry in runtime_register_entries():
        target = _expected_surface(entry)
        if target:
            by_surface.setdefault(target, []).append(entry)
    return {surface: tuple(items) for surface, items in by_surface.items()}


def _expected_surface(entry) -> str:
    intent = entry.intent
    if intent.surface:
        return intent.surface
    if intent.kind.value == "subanta":
        from .morphology_synth import synthesize as synth

        try:
            return synth(intent).surface
        except MorphologyError:
            return ""
    if intent.kind.value == "tinanta":
        from .morphology_synth import synthesize as synth

        try:
            return synth(intent).surface
        except MorphologyError:
            return ""
    return ""


def _contains_devanagari(text: str) -> bool:
    return any("\u0900" <= char <= "\u097f" for char in text)


def _roles_by_type(items) -> dict[Role, list[Analysis]]:
    roles: dict[Role, list[Analysis]] = {}
    for item in items:
        if item.role is None:
            continue
        roles.setdefault(item.role, []).append(item)
    return roles


_DEFAULT_FACADE: MorphologyFacade | None = None


def get_default_facade() -> MorphologyFacade:
    global _DEFAULT_FACADE
    if _DEFAULT_FACADE is None:
        _DEFAULT_FACADE = MorphologyFacade()
    return _DEFAULT_FACADE


def analyze_token(token: str) -> Analysis:
    return get_default_facade().analyze_token(token)


def analyze_sentence(sentence: str) -> list[Analysis]:
    return get_default_facade().analyze_sentence(sentence)


__all__ = [
    "MorphologyFacade",
    "analyze_sentence",
    "analyze_token",
    "get_default_facade",
]
