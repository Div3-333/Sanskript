from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from .errors import MorphologyError
from .grammar import (
    CASE_TO_ROLE,
    CONTROLLED_NOUNS,
    NUMERAL_FORMS,
    VERB_FRAMES,
    Analysis,
    PartOfSpeech,
)
from .avyaya import iter_avyaya_analyses
from .subanta import iter_nominal_analyses, iter_pronoun_analyses
from .tinanta import iter_tinanta_analyses


from .phonology import tokenize_sounds, is_vowel, SoundKind


@dataclass(frozen=True)
class NominalStem:
    surface: str
    is_meaningful: bool = True
    is_root: bool = False
    is_suffix: bool = False
    gender: str | None = None # 'masculine', 'feminine', 'neuter'
    is_upasarjana: bool = False


def is_pratipadika(stem: NominalStem) -> bool:
    """
    1.2.45 arthavad-adhātur-apratyayaḥ prātipadikam
    A meaningful form that is neither a root nor a suffix is a prātipadika.

    1.2.46 kṛत्तद्धितसमासाश्च
    Forms ending in kṛt/taddhita and compounds are also prātipadika.
    """
    if not stem.is_meaningful:
        return False

    # 1.2.45 check
    if not stem.is_root and not stem.is_suffix:
        return True
    return False


def get_shortened_stem(stem: str, gender: str, is_upasarjana: bool = False) -> str:
    """
    1.2.47 hrasvo napuṃsake prātipadikasya
    A nominal stem is shortened in neuter.

    1.2.48 go-striyor-upasarjanasya
    A nominal stem ending in 'go' or a feminine suffix is shortened when upasarjana.
    """
    sounds = tokenize_sounds(stem)
    if not sounds:
        return stem

    last = sounds[-1]

    should_shorten = False
    if gender == "neuter":
        should_shorten = True
    elif is_upasarjana:
        if stem.endswith("go") or last in {"ā", "ī", "ū", "ai", "au", "e", "o"}:
             should_shorten = True

    if should_shorten:
        # ai -> i, au -> u per 1.1.48 logic for shortening
        short_map = {
            "ā": "a", "ī": "i", "ū": "u", "ṝ": "ṛ", "ḷ": "ḷ",
            "ai": "i", "au": "u", "e": "i", "o": "u",
            "aī": "i", "aū": "u" # handling potential IAST macron combinations
        }
        if last in short_map:
            sounds[-1] = short_map[last]
            return "".join(sounds)

    return stem


TOKEN_RE = re.compile(r"[\w\u0900-\u097fāīūṛṝḷḹṅñṭḍṇśṣṃḥĀĪŪṚṜḶḸṄÑṬḌṆŚṢṂḤ]+", re.UNICODE)


def normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text)
    normalized = normalized.replace("ṁ", "ṃ").replace("Ṁ", "Ṃ")
    normalized = normalized.replace("।", ".")
    return normalized


def build_lexicon() -> dict[str, Analysis]:
    lexicon: dict[str, Analysis] = {}

    for analysis in iter_avyaya_analyses():
        lexicon[analysis.surface] = analysis

    for analysis in iter_nominal_analyses():
        store_preferred_analysis(lexicon, analysis)

    for analysis in iter_pronoun_analyses():
        store_preferred_analysis(lexicon, analysis)

    for analysis in iter_tinanta_analyses():
        lexicon[analysis.surface] = analysis

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


def store_preferred_analysis(lexicon: dict[str, Analysis], analysis: Analysis) -> None:
    existing = lexicon.get(analysis.surface)
    if existing is None or case_priority(analysis) > case_priority(existing):
        lexicon[analysis.surface] = analysis


def case_priority(analysis: Analysis) -> int:
    if analysis.case is None:
        return 0
    priority = {
        "vocative": 1,
        "nominative": 2,
        "genitive": 3,
        "locative": 4,
        "dative": 5,
        "ablative": 6,
        "instrumental": 7,
        "accusative": 8,
    }
    return priority[analysis.case.value]


LEXICON = build_lexicon()


def split_sentences(text: str) -> list[str]:
    normalized = normalize(text)
    return [part.strip() for part in re.split(r"[.?]+", normalized) if part.strip()]


def tokenize(sentence: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(normalize(sentence))]


def analyze_token(token: str) -> Analysis:
    try:
        return LEXICON[token]
    except KeyError as exc:
        raise MorphologyError(f"Unknown Sanskrit form in the controlled subset: {token!r}") from exc


def analyze_sentence(sentence: str) -> list[Analysis]:
    return [analyze_token(token) for token in tokenize(sentence)]
