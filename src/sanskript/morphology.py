from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
import unicodedata

from .errors import MorphologyError


class Case(str, Enum):
    NOMINATIVE = "nominative"
    ACCUSATIVE = "accusative"
    INSTRUMENTAL = "instrumental"
    LOCATIVE = "locative"


class Role(str, Enum):
    KARTR = "kartṛ"
    KARMAN = "karman"
    KARANA = "karaṇa"
    ADHIKARANA = "adhikaraṇa"


class PartOfSpeech(str, Enum):
    NOUN = "noun"
    NUMERAL = "numeral"
    VERB = "verb"


CASE_TO_ROLE = {
    Case.NOMINATIVE: Role.KARTR,
    Case.ACCUSATIVE: Role.KARMAN,
    Case.INSTRUMENTAL: Role.KARANA,
    Case.LOCATIVE: Role.ADHIKARANA,
}


@dataclass(frozen=True)
class Analysis:
    surface: str
    lemma: str
    pos: PartOfSpeech
    case: Case | None = None
    role: Role | None = None
    value: int | None = None


LEXICON: dict[str, Analysis] = {
    "gaṇakaḥ": Analysis(
        surface="gaṇakaḥ",
        lemma="gaṇaka",
        pos=PartOfSpeech.NOUN,
        case=Case.NOMINATIVE,
        role=Role.KARTR,
    ),
    "phalaṃ": Analysis(
        surface="phalaṃ",
        lemma="phala",
        pos=PartOfSpeech.NOUN,
        case=Case.ACCUSATIVE,
        role=Role.KARMAN,
    ),
    "phalam": Analysis(
        surface="phalam",
        lemma="phala",
        pos=PartOfSpeech.NOUN,
        case=Case.ACCUSATIVE,
        role=Role.KARMAN,
    ),
    "phale": Analysis(
        surface="phale",
        lemma="phala",
        pos=PartOfSpeech.NOUN,
        case=Case.LOCATIVE,
        role=Role.ADHIKARANA,
    ),
    "dvābhyāṃ": Analysis(
        surface="dvābhyāṃ",
        lemma="dvi",
        pos=PartOfSpeech.NUMERAL,
        case=Case.INSTRUMENTAL,
        role=Role.KARANA,
        value=2,
    ),
    "dvābhyām": Analysis(
        surface="dvābhyām",
        lemma="dvi",
        pos=PartOfSpeech.NUMERAL,
        case=Case.INSTRUMENTAL,
        role=Role.KARANA,
        value=2,
    ),
    "pañca": Analysis(
        surface="pañca",
        lemma="pañcan",
        pos=PartOfSpeech.NUMERAL,
        case=Case.ACCUSATIVE,
        role=Role.KARMAN,
        value=5,
    ),
    "sapta": Analysis(
        surface="sapta",
        lemma="saptan",
        pos=PartOfSpeech.NUMERAL,
        case=Case.ACCUSATIVE,
        role=Role.KARMAN,
        value=7,
    ),
    "nava": Analysis(
        surface="nava",
        lemma="navan",
        pos=PartOfSpeech.NUMERAL,
        case=Case.ACCUSATIVE,
        role=Role.KARMAN,
        value=9,
    ),
    "nidadhāti": Analysis(surface="nidadhāti", lemma="nidhā", pos=PartOfSpeech.VERB),
    "vardhayati": Analysis(surface="vardhayati", lemma="vṛdh", pos=PartOfSpeech.VERB),
    "darśayati": Analysis(surface="darśayati", lemma="dṛś", pos=PartOfSpeech.VERB),
}


TOKEN_RE = re.compile(r"[\w\u0900-\u097fāīūṛṝḷḹṅñṭḍṇśṣṃḥĀĪŪṚṜḶḸṄÑṬḌṆŚṢṂḤ]+", re.UNICODE)


def normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text)
    normalized = normalized.replace("ṁ", "ṃ").replace("Ṁ", "Ṃ")
    normalized = normalized.replace("।", ".")
    return normalized


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

