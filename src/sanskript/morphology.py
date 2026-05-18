from __future__ import annotations

import re
import unicodedata

from .errors import MorphologyError
from .grammar import (
    CASE_TO_ROLE,
    CONTROLLED_NOUNS,
    NUMERAL_FORMS,
    VERB_FRAMES,
    Analysis,
    PartOfSpeech,
)


TOKEN_RE = re.compile(r"[\w\u0900-\u097fāīūṛṝḷḹṅñṭḍṇśṣṃḥĀĪŪṚṜḶḸṄÑṬḌṆŚṢṂḤ]+", re.UNICODE)


def normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text)
    normalized = normalized.replace("ṁ", "ṃ").replace("Ṁ", "Ṃ")
    normalized = normalized.replace("।", ".")
    return normalized


def build_lexicon() -> dict[str, Analysis]:
    lexicon: dict[str, Analysis] = {}

    for stem in CONTROLLED_NOUNS:
        for form in stem.forms:
            lexicon[form.surface] = Analysis(
                surface=form.surface,
                lemma=stem.lemma,
                pos=PartOfSpeech.NOUN,
                case=form.case,
                role=CASE_TO_ROLE.get(form.case),
                gender=stem.gender,
                number=form.number,
            )

    for numeral in NUMERAL_FORMS:
        lexicon[numeral.surface] = Analysis(
            surface=numeral.surface,
            lemma=numeral.lemma,
            pos=PartOfSpeech.NUMERAL,
            case=numeral.case,
            role=CASE_TO_ROLE[numeral.case],
            gender=numeral.gender,
            number=numeral.number,
            value=numeral.value,
        )

    for frame in VERB_FRAMES.values():
        lexicon[frame.surface] = Analysis(
            surface=frame.surface,
            lemma=frame.lemma,
            pos=PartOfSpeech.VERB,
            number=frame.number,
            person=frame.person,
            pada=frame.pada,
            lakara=frame.lakara,
        )

    return lexicon


LEXICON = build_lexicon()


def split_sentences(text: str) -> list[str]:
    normalized = normalize(text)
    return [part.strip() for part in normalized.split(".") if part.strip()]


def tokenize(sentence: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(normalize(sentence))]


def analyze_token(token: str) -> Analysis:
    try:
        return LEXICON[token]
    except KeyError as exc:
        raise MorphologyError(f"Unknown Sanskrit form in the controlled subset: {token!r}") from exc


def analyze_sentence(sentence: str) -> list[Analysis]:
    return [analyze_token(token) for token in tokenize(sentence)]
