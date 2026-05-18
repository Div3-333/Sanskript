from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .grammar import Analysis, CASE_TO_ROLE, Case, Gender, GrammaticalNumber, PartOfSpeech, Person


class StemPattern(str, Enum):
    A_MASCULINE = "a_masculine"
    A_NEUTER = "a_neuter"
    AA_FEMININE = "ā_feminine"


@dataclass(frozen=True)
class SupEnding:
    case: Case
    number: GrammaticalNumber
    technical: str


@dataclass(frozen=True)
class DeclensionStem:
    lemma: str
    pattern: StemPattern
    gender: Gender
    gloss: str


@dataclass(frozen=True)
class PronounForm:
    surface: str
    lemma: str
    case: Case
    number: GrammaticalNumber
    person: Person | None


SUP_ENDINGS: tuple[SupEnding, ...] = (
    SupEnding(Case.NOMINATIVE, GrammaticalNumber.SINGULAR, "su"),
    SupEnding(Case.NOMINATIVE, GrammaticalNumber.DUAL, "au"),
    SupEnding(Case.NOMINATIVE, GrammaticalNumber.PLURAL, "jas"),
    SupEnding(Case.ACCUSATIVE, GrammaticalNumber.SINGULAR, "am"),
    SupEnding(Case.ACCUSATIVE, GrammaticalNumber.DUAL, "auṭ"),
    SupEnding(Case.ACCUSATIVE, GrammaticalNumber.PLURAL, "śas"),
    SupEnding(Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR, "ṭā"),
    SupEnding(Case.INSTRUMENTAL, GrammaticalNumber.DUAL, "bhyām"),
    SupEnding(Case.INSTRUMENTAL, GrammaticalNumber.PLURAL, "bhis"),
    SupEnding(Case.DATIVE, GrammaticalNumber.SINGULAR, "ṅe"),
    SupEnding(Case.DATIVE, GrammaticalNumber.DUAL, "bhyām"),
    SupEnding(Case.DATIVE, GrammaticalNumber.PLURAL, "bhyas"),
    SupEnding(Case.ABLATIVE, GrammaticalNumber.SINGULAR, "ṅasi"),
    SupEnding(Case.ABLATIVE, GrammaticalNumber.DUAL, "bhyām"),
    SupEnding(Case.ABLATIVE, GrammaticalNumber.PLURAL, "bhyas"),
    SupEnding(Case.GENITIVE, GrammaticalNumber.SINGULAR, "ṅas"),
    SupEnding(Case.GENITIVE, GrammaticalNumber.DUAL, "os"),
    SupEnding(Case.GENITIVE, GrammaticalNumber.PLURAL, "ām"),
    SupEnding(Case.LOCATIVE, GrammaticalNumber.SINGULAR, "ṅi"),
    SupEnding(Case.LOCATIVE, GrammaticalNumber.DUAL, "os"),
    SupEnding(Case.LOCATIVE, GrammaticalNumber.PLURAL, "sup"),
)


SUBANTA_STEMS: tuple[DeclensionStem, ...] = (
    DeclensionStem("gaṇaka", StemPattern.A_MASCULINE, Gender.MASCULINE, "calculator, reckoner"),
    DeclensionStem("deva", StemPattern.A_MASCULINE, Gender.MASCULINE, "deity, luminous one"),
    DeclensionStem("phala", StemPattern.A_NEUTER, Gender.NEUTER, "fruit, result, outcome"),
    DeclensionStem("mūlya", StemPattern.A_NEUTER, Gender.NEUTER, "value"),
    DeclensionStem("pada", StemPattern.A_NEUTER, Gender.NEUTER, "step, word, place"),
    DeclensionStem("latā", StemPattern.AA_FEMININE, Gender.FEMININE, "creeper"),
)


PRONOUN_FORMS: tuple[PronounForm, ...] = (
    PronounForm("aham", "asmad", Case.NOMINATIVE, GrammaticalNumber.SINGULAR, Person.FIRST),
    PronounForm("āvām", "asmad", Case.NOMINATIVE, GrammaticalNumber.DUAL, Person.FIRST),
    PronounForm("vayam", "asmad", Case.NOMINATIVE, GrammaticalNumber.PLURAL, Person.FIRST),
    PronounForm("mām", "asmad", Case.ACCUSATIVE, GrammaticalNumber.SINGULAR, Person.FIRST),
    PronounForm("asmān", "asmad", Case.ACCUSATIVE, GrammaticalNumber.PLURAL, Person.FIRST),
    PronounForm("mayā", "asmad", Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR, Person.FIRST),
    PronounForm("asmābhiḥ", "asmad", Case.INSTRUMENTAL, GrammaticalNumber.PLURAL, Person.FIRST),
    PronounForm("tvam", "yuṣmad", Case.NOMINATIVE, GrammaticalNumber.SINGULAR, Person.SECOND),
    PronounForm("yuvām", "yuṣmad", Case.NOMINATIVE, GrammaticalNumber.DUAL, Person.SECOND),
    PronounForm("yūyam", "yuṣmad", Case.NOMINATIVE, GrammaticalNumber.PLURAL, Person.SECOND),
    PronounForm("tvām", "yuṣmad", Case.ACCUSATIVE, GrammaticalNumber.SINGULAR, Person.SECOND),
    PronounForm("yuṣmān", "yuṣmad", Case.ACCUSATIVE, GrammaticalNumber.PLURAL, Person.SECOND),
    PronounForm("tvayā", "yuṣmad", Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR, Person.SECOND),
    PronounForm("yuṣmābhiḥ", "yuṣmad", Case.INSTRUMENTAL, GrammaticalNumber.PLURAL, Person.SECOND),
    PronounForm("saḥ", "tad", Case.NOMINATIVE, GrammaticalNumber.SINGULAR, Person.THIRD),
    PronounForm("tat", "tad", Case.NOMINATIVE, GrammaticalNumber.SINGULAR, Person.THIRD),
    PronounForm("tam", "tad", Case.ACCUSATIVE, GrammaticalNumber.SINGULAR, Person.THIRD),
    PronounForm("tena", "tad", Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR, Person.THIRD),
)


def sup_ending(case: Case, number: GrammaticalNumber) -> str:
    for ending in SUP_ENDINGS:
        if ending.case == case and ending.number == number:
            return ending.technical
    raise ValueError(f"No sup ending for {case.value}/{number.value}")


def decline(stem: DeclensionStem) -> dict[tuple[Case, GrammaticalNumber], str]:
    if stem.pattern == StemPattern.A_MASCULINE:
        return decline_a_masculine(stem.lemma)
    if stem.pattern == StemPattern.A_NEUTER:
        return decline_a_neuter(stem.lemma)
    if stem.pattern == StemPattern.AA_FEMININE:
        return decline_aa_feminine(stem.lemma)
    raise ValueError(f"Unknown stem pattern: {stem.pattern}")


def iter_nominal_analyses() -> Iterable[Analysis]:
    for stem in SUBANTA_STEMS:
        for (case, number), surface in decline(stem).items():
            yield Analysis(
                surface=surface,
                lemma=stem.lemma,
                pos=PartOfSpeech.NOUN,
                case=case,
                role=CASE_TO_ROLE.get(case),
                gender=stem.gender,
                number=number,
            )


def iter_pronoun_analyses() -> Iterable[Analysis]:
    for form in PRONOUN_FORMS:
        yield Analysis(
            surface=form.surface,
            lemma=form.lemma,
            pos=PartOfSpeech.PRONOUN,
            case=form.case,
            role=CASE_TO_ROLE.get(form.case),
            number=form.number,
            person=form.person,
        )


def decline_a_masculine(lemma: str) -> dict[tuple[Case, GrammaticalNumber], str]:
    base = lemma[:-1]
    return {
        (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): base + "aḥ",
        (Case.NOMINATIVE, GrammaticalNumber.DUAL): base + "au",
        (Case.NOMINATIVE, GrammaticalNumber.PLURAL): base + "āḥ",
        (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): base + "am",
        (Case.ACCUSATIVE, GrammaticalNumber.DUAL): base + "au",
        (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): base + "ān",
        (Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR): base + "ena",
        (Case.INSTRUMENTAL, GrammaticalNumber.DUAL): base + "ābhyām",
        (Case.INSTRUMENTAL, GrammaticalNumber.PLURAL): base + "aiḥ",
        (Case.DATIVE, GrammaticalNumber.SINGULAR): base + "āya",
        (Case.DATIVE, GrammaticalNumber.DUAL): base + "ābhyām",
        (Case.DATIVE, GrammaticalNumber.PLURAL): base + "ebhyaḥ",
        (Case.ABLATIVE, GrammaticalNumber.SINGULAR): base + "āt",
        (Case.ABLATIVE, GrammaticalNumber.DUAL): base + "ābhyām",
        (Case.ABLATIVE, GrammaticalNumber.PLURAL): base + "ebhyaḥ",
        (Case.GENITIVE, GrammaticalNumber.SINGULAR): base + "asya",
        (Case.GENITIVE, GrammaticalNumber.DUAL): base + "ayoḥ",
        (Case.GENITIVE, GrammaticalNumber.PLURAL): base + "ānām",
        (Case.LOCATIVE, GrammaticalNumber.SINGULAR): base + "e",
        (Case.LOCATIVE, GrammaticalNumber.DUAL): base + "ayoḥ",
        (Case.LOCATIVE, GrammaticalNumber.PLURAL): base + "eṣu",
        (Case.VOCATIVE, GrammaticalNumber.SINGULAR): lemma,
        (Case.VOCATIVE, GrammaticalNumber.DUAL): base + "au",
        (Case.VOCATIVE, GrammaticalNumber.PLURAL): base + "āḥ",
    }

def decline_a_neuter(lemma: str) -> dict[tuple[Case, GrammaticalNumber], str]:
    base = lemma[:-1]
    forms = decline_a_masculine(lemma)
    forms.update(
        {
            (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): lemma,
            (Case.NOMINATIVE, GrammaticalNumber.DUAL): base + "e",
            (Case.NOMINATIVE, GrammaticalNumber.PLURAL): base + "āni",
            (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): base + "aṃ",
            (Case.ACCUSATIVE, GrammaticalNumber.DUAL): base + "e",
            (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): base + "āni",
            (Case.VOCATIVE, GrammaticalNumber.SINGULAR): lemma,
            (Case.VOCATIVE, GrammaticalNumber.DUAL): base + "e",
            (Case.VOCATIVE, GrammaticalNumber.PLURAL): base + "āni",
        }
    )
    return forms


def decline_aa_feminine(lemma: str) -> dict[tuple[Case, GrammaticalNumber], str]:
    base = lemma[:-1]
    return {
        (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): lemma,
        (Case.NOMINATIVE, GrammaticalNumber.DUAL): base + "e",
        (Case.NOMINATIVE, GrammaticalNumber.PLURAL): base + "āḥ",
        (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): base + "ām",
        (Case.ACCUSATIVE, GrammaticalNumber.DUAL): base + "e",
        (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): base + "āḥ",
        (Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR): base + "ayā",
        (Case.INSTRUMENTAL, GrammaticalNumber.DUAL): base + "ābhyām",
        (Case.INSTRUMENTAL, GrammaticalNumber.PLURAL): base + "ābhiḥ",
        (Case.DATIVE, GrammaticalNumber.SINGULAR): base + "āyai",
        (Case.DATIVE, GrammaticalNumber.DUAL): base + "ābhyām",
        (Case.DATIVE, GrammaticalNumber.PLURAL): base + "ābhyaḥ",
        (Case.ABLATIVE, GrammaticalNumber.SINGULAR): base + "āyāḥ",
        (Case.ABLATIVE, GrammaticalNumber.DUAL): base + "ābhyām",
        (Case.ABLATIVE, GrammaticalNumber.PLURAL): base + "ābhyaḥ",
        (Case.GENITIVE, GrammaticalNumber.SINGULAR): base + "āyāḥ",
        (Case.GENITIVE, GrammaticalNumber.DUAL): base + "ayoḥ",
        (Case.GENITIVE, GrammaticalNumber.PLURAL): base + "ānām",
        (Case.LOCATIVE, GrammaticalNumber.SINGULAR): base + "āyām",
        (Case.LOCATIVE, GrammaticalNumber.DUAL): base + "ayoḥ",
        (Case.LOCATIVE, GrammaticalNumber.PLURAL): base + "āsu",
        (Case.VOCATIVE, GrammaticalNumber.SINGULAR): base + "e",
        (Case.VOCATIVE, GrammaticalNumber.DUAL): base + "e",
        (Case.VOCATIVE, GrammaticalNumber.PLURAL): base + "āḥ",
    }
