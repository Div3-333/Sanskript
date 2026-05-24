from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .grammar import Analysis, CASE_TO_ROLE, Case, Gender, GrammaticalNumber, PartOfSpeech, Person


class StemPattern(str, Enum):
    A_MASCULINE = "a_masculine"
    A_NEUTER = "a_neuter"
    AA_FEMININE = "ā_feminine"
    I_MASCULINE = "i_masculine"
    I_FEMININE = "i_feminine"
    I_NEUTER = "i_neuter"
    II_FEMININE = "ī_feminine"
    U_MASCULINE = "u_masculine"
    U_NEUTER = "u_neuter"
    UU_FEMININE = "ū_feminine"
    R_MASCULINE = "ṛ_masculine"
    R_FEMININE = "ṛ_feminine"
    RR_FEMININE = "ṝ_feminine"
    L_STEM = "ḷ_stem"
    E_STEM = "e_stem"
    AI_STEM = "ai_stem"
    O_MASCULINE = "o_masculine"
    AU_STEM = "au_stem"


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


def infer_stem_pattern(lemma: str, gender: Gender) -> StemPattern | None:
    """Infer declension class from lemma ending and gender."""
    if lemma.endswith("au"):
        return StemPattern.AU_STEM
    if lemma.endswith("ai"):
        return StemPattern.AI_STEM
    if lemma.endswith("e"):
        return StemPattern.E_STEM
    if lemma.endswith("o"):
        return StemPattern.O_MASCULINE
    if lemma.endswith("ḷ"):
        return StemPattern.L_STEM
    if lemma.endswith("ṝ"):
        return StemPattern.RR_FEMININE
    if lemma.endswith("ṛ"):
        return StemPattern.R_FEMININE if gender == Gender.FEMININE else StemPattern.R_MASCULINE
    if lemma.endswith("ū"):
        return StemPattern.UU_FEMININE
    if lemma.endswith("u"):
        return StemPattern.U_NEUTER if gender == Gender.NEUTER else StemPattern.U_MASCULINE
    if lemma.endswith("ī"):
        return StemPattern.II_FEMININE
    if lemma.endswith("i"):
        if gender == Gender.NEUTER:
            return StemPattern.I_NEUTER
        if gender == Gender.FEMININE:
            return StemPattern.I_FEMININE
        return StemPattern.I_MASCULINE
    if lemma.endswith("ā"):
        return StemPattern.AA_FEMININE
    if lemma.endswith("a"):
        return StemPattern.A_NEUTER if gender == Gender.NEUTER else StemPattern.A_MASCULINE
    return None


def valid_lemma_for_pattern(lemma: str, pattern: StemPattern) -> bool:
    checks: dict[StemPattern, tuple[str, ...]] = {
        StemPattern.A_MASCULINE: ("a",),
        StemPattern.A_NEUTER: ("a",),
        StemPattern.AA_FEMININE: ("ā",),
        StemPattern.I_MASCULINE: ("i",),
        StemPattern.I_FEMININE: ("i",),
        StemPattern.I_NEUTER: ("i",),
        StemPattern.II_FEMININE: ("ī",),
        StemPattern.U_MASCULINE: ("u",),
        StemPattern.U_NEUTER: ("u",),
        StemPattern.UU_FEMININE: ("ū",),
        StemPattern.R_MASCULINE: ("ṛ",),
        StemPattern.R_FEMININE: ("ṛ",),
        StemPattern.RR_FEMININE: ("ṝ",),
        StemPattern.L_STEM: ("ḷ",),
        StemPattern.E_STEM: ("e",),
        StemPattern.AI_STEM: ("ai",),
        StemPattern.O_MASCULINE: ("o",),
        StemPattern.AU_STEM: ("au",),
    }
    suffixes = checks.get(pattern)
    if not suffixes:
        return False
    if pattern in {StemPattern.A_MASCULINE, StemPattern.A_NEUTER}:
        return lemma.endswith("a") and not lemma.endswith("ā")
    return any(lemma.endswith(suffix) for suffix in suffixes)


def decline_paradigm(stem: DeclensionStem) -> dict[tuple[Case, GrammaticalNumber], str]:
    from . import subanta_paradigms as paradigms

    dispatch: dict[StemPattern, object] = {
        StemPattern.A_MASCULINE: decline_a_masculine,
        StemPattern.A_NEUTER: decline_a_neuter,
        StemPattern.AA_FEMININE: decline_aa_feminine,
        StemPattern.I_MASCULINE: paradigms.decline_i_masculine,
        StemPattern.I_FEMININE: paradigms.decline_i_masculine,
        StemPattern.I_NEUTER: paradigms.decline_i_neuter,
        StemPattern.II_FEMININE: paradigms.decline_ii_feminine,
        StemPattern.U_MASCULINE: paradigms.decline_u_masculine,
        StemPattern.U_NEUTER: paradigms.decline_u_neuter,
        StemPattern.UU_FEMININE: paradigms.decline_uu_feminine,
        StemPattern.R_MASCULINE: paradigms.decline_r_masculine,
        StemPattern.R_FEMININE: paradigms.decline_r_masculine,
        StemPattern.RR_FEMININE: paradigms.decline_rr_feminine,
        StemPattern.L_STEM: paradigms.decline_l_stem,
        StemPattern.E_STEM: paradigms.decline_e_stem,
        StemPattern.AI_STEM: paradigms.decline_ai_stem,
        StemPattern.O_MASCULINE: paradigms.decline_o_masculine,
        StemPattern.AU_STEM: paradigms.decline_au_stem,
    }
    handler = dispatch.get(stem.pattern)
    if handler is None:
        raise ValueError(f"Unknown stem pattern: {stem.pattern}")
    return handler(stem.lemma)  # type: ignore[operator]


def decline(stem: DeclensionStem) -> dict[tuple[Case, GrammaticalNumber], str]:
    """Return full nominal paradigms from sup tables (used by tests and engine fallbacks)."""
    return decline_paradigm(stem)


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
