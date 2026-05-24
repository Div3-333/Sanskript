from __future__ import annotations

from pathlib import Path

from .grammar import Analysis
from .morphology_lexicon import (
    DEFAULT_LEXICON_PATH,
    load_controlled_lexicon,
    merge_lexicon_with_overrides,
    store_preferred,
)
from .morphology_text import normalize, split_sentences, tokenize as _tokenize_words


def tokenize(sentence: str) -> list[str]:
    from .morphology_facade import MorphologyFacade

    facade = MorphologyFacade()
    return _tokenize_words(sentence, normalize_token=facade.normalize_token)


def build_lexicon(path: Path | None = None) -> dict[str, Analysis]:
    """Load the controlled lexicon artifact, synthesizing from register if missing."""
    lexicon_path = path or DEFAULT_LEXICON_PATH
    artifact = load_controlled_lexicon(lexicon_path) if lexicon_path.exists() else {}
    if artifact:
        return artifact

    from .grammar_register import register_entries
    from .morphology_synth import MorphologySynthesizer

    synthesizer = MorphologySynthesizer()
    lexicon: dict[str, Analysis] = {}
    for entry in register_entries():
        result = synthesizer.synthesize(entry.intent)
        store_preferred(lexicon, result.analysis, force=entry.authoritative)
    return merge_lexicon_with_overrides(lexicon)


def analyze_token(token: str) -> Analysis:
    from .morphology_facade import get_default_facade

    return get_default_facade().analyze_token(token)


def analyze_sentence(sentence: str) -> list[Analysis]:
    from .morphology_facade import get_default_facade

    return get_default_facade().analyze_sentence(sentence)


LEXICON = build_lexicon()


__all__ = [
    "LEXICON",
    "analyze_sentence",
    "analyze_token",
    "build_lexicon",
    "normalize",
    "split_sentences",
    "tokenize",
]
