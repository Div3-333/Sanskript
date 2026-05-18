from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Case(str, Enum):
    NOMINATIVE = "nominative"
    ACCUSATIVE = "accusative"
    INSTRUMENTAL = "instrumental"
    LOCATIVE = "locative"


class Gender(str, Enum):
    MASCULINE = "masculine"
    NEUTER = "neuter"


class GrammaticalNumber(str, Enum):
    SINGULAR = "singular"
    DUAL = "dual"
    PLURAL = "plural"


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
    gender: Gender | None = None
    number: GrammaticalNumber | None = None
    value: int | None = None


@dataclass(frozen=True)
class NominalForm:
    surface: str
    case: Case
    number: GrammaticalNumber


@dataclass(frozen=True)
class NominalStem:
    lemma: str
    gender: Gender
    forms: tuple[NominalForm, ...]
    gloss: str


@dataclass(frozen=True)
class NumeralForm:
    surface: str
    lemma: str
    value: int
    case: Case
    number: GrammaticalNumber | None
    gender: Gender | None = None


@dataclass(frozen=True)
class VerbFrame:
    surface: str
    lemma: str
    gloss: str
    required_roles: frozenset[Role]
    construction_id: str


@dataclass(frozen=True)
class Construction:
    id: str
    name: str
    status: str
    description: str


CONTROLLED_NOUNS: tuple[NominalStem, ...] = (
    NominalStem(
        lemma="gaṇaka",
        gender=Gender.MASCULINE,
        gloss="calculator, reckoner",
        forms=(
            NominalForm("gaṇakaḥ", Case.NOMINATIVE, GrammaticalNumber.SINGULAR),
        ),
    ),
    NominalStem(
        lemma="phala",
        gender=Gender.NEUTER,
        gloss="fruit, result, outcome",
        forms=(
            NominalForm("phalaṃ", Case.ACCUSATIVE, GrammaticalNumber.SINGULAR),
            NominalForm("phalam", Case.ACCUSATIVE, GrammaticalNumber.SINGULAR),
            NominalForm("phale", Case.LOCATIVE, GrammaticalNumber.SINGULAR),
        ),
    ),
    NominalStem(
        lemma="mūlya",
        gender=Gender.NEUTER,
        gloss="value",
        forms=(
            NominalForm("mūlyaṃ", Case.ACCUSATIVE, GrammaticalNumber.SINGULAR),
            NominalForm("mūlyam", Case.ACCUSATIVE, GrammaticalNumber.SINGULAR),
            NominalForm("mūlye", Case.LOCATIVE, GrammaticalNumber.SINGULAR),
        ),
    ),
    NominalStem(
        lemma="pada",
        gender=Gender.NEUTER,
        gloss="step, word, place",
        forms=(
            NominalForm("padaṃ", Case.ACCUSATIVE, GrammaticalNumber.SINGULAR),
            NominalForm("padam", Case.ACCUSATIVE, GrammaticalNumber.SINGULAR),
            NominalForm("pade", Case.LOCATIVE, GrammaticalNumber.SINGULAR),
        ),
    ),
)


NUMERAL_FORMS: tuple[NumeralForm, ...] = (
    NumeralForm("śūnyaṃ", "śūnya", 0, Case.ACCUSATIVE, GrammaticalNumber.SINGULAR, Gender.NEUTER),
    NumeralForm("śūnyam", "śūnya", 0, Case.ACCUSATIVE, GrammaticalNumber.SINGULAR, Gender.NEUTER),
    NumeralForm("śūnyena", "śūnya", 0, Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR, Gender.NEUTER),
    NumeralForm("ekaṃ", "eka", 1, Case.ACCUSATIVE, GrammaticalNumber.SINGULAR, Gender.NEUTER),
    NumeralForm("ekam", "eka", 1, Case.ACCUSATIVE, GrammaticalNumber.SINGULAR, Gender.NEUTER),
    NumeralForm("ekena", "eka", 1, Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR, Gender.NEUTER),
    NumeralForm("dve", "dvi", 2, Case.ACCUSATIVE, GrammaticalNumber.DUAL, Gender.NEUTER),
    NumeralForm("dvābhyāṃ", "dvi", 2, Case.INSTRUMENTAL, GrammaticalNumber.DUAL),
    NumeralForm("dvābhyām", "dvi", 2, Case.INSTRUMENTAL, GrammaticalNumber.DUAL),
    NumeralForm("trīṇi", "tri", 3, Case.ACCUSATIVE, GrammaticalNumber.PLURAL, Gender.NEUTER),
    NumeralForm("tribhiḥ", "tri", 3, Case.INSTRUMENTAL, GrammaticalNumber.PLURAL),
    NumeralForm("catvāri", "catur", 4, Case.ACCUSATIVE, GrammaticalNumber.PLURAL, Gender.NEUTER),
    NumeralForm("caturbhiḥ", "catur", 4, Case.INSTRUMENTAL, GrammaticalNumber.PLURAL),
    NumeralForm("pañca", "pañcan", 5, Case.ACCUSATIVE, GrammaticalNumber.PLURAL),
    NumeralForm("pañcabhiḥ", "pañcan", 5, Case.INSTRUMENTAL, GrammaticalNumber.PLURAL),
    NumeralForm("ṣaṭ", "ṣaṣ", 6, Case.ACCUSATIVE, GrammaticalNumber.PLURAL),
    NumeralForm("ṣaḍbhiḥ", "ṣaṣ", 6, Case.INSTRUMENTAL, GrammaticalNumber.PLURAL),
    NumeralForm("sapta", "saptan", 7, Case.ACCUSATIVE, GrammaticalNumber.PLURAL),
    NumeralForm("saptabhiḥ", "saptan", 7, Case.INSTRUMENTAL, GrammaticalNumber.PLURAL),
    NumeralForm("aṣṭa", "aṣṭan", 8, Case.ACCUSATIVE, GrammaticalNumber.PLURAL),
    NumeralForm("aṣṭabhiḥ", "aṣṭan", 8, Case.INSTRUMENTAL, GrammaticalNumber.PLURAL),
    NumeralForm("nava", "navan", 9, Case.ACCUSATIVE, GrammaticalNumber.PLURAL),
    NumeralForm("navabhiḥ", "navan", 9, Case.INSTRUMENTAL, GrammaticalNumber.PLURAL),
    NumeralForm("daśa", "daśan", 10, Case.ACCUSATIVE, GrammaticalNumber.PLURAL),
    NumeralForm("daśabhiḥ", "daśan", 10, Case.INSTRUMENTAL, GrammaticalNumber.PLURAL),
)


VERB_FRAMES: dict[str, VerbFrame] = {
    "nidadhāti": VerbFrame(
        surface="nidadhāti",
        lemma="nidhā",
        gloss="places, puts down",
        required_roles=frozenset({Role.KARMAN, Role.ADHIKARANA}),
        construction_id="VF-001",
    ),
    "vardhayati": VerbFrame(
        surface="vardhayati",
        lemma="vṛdh",
        gloss="increases, augments",
        required_roles=frozenset({Role.KARMAN, Role.KARANA}),
        construction_id="VF-002",
    ),
    "darśayati": VerbFrame(
        surface="darśayati",
        lemma="dṛś",
        gloss="shows, displays",
        required_roles=frozenset({Role.KARMAN}),
        construction_id="VF-003",
    ),
}


CONSTRUCTIONS: dict[str, Construction] = {
    "NF-001": Construction(
        id="NF-001",
        name="controlled nominal forms",
        status="experimental",
        description="Approved noun forms are declared explicitly before the compiler accepts them.",
    ),
    "NUM-001": Construction(
        id="NUM-001",
        name="small cardinal numerals",
        status="experimental",
        description="Cardinal numerals 0 through 10 are accepted in object and instrumental roles.",
    ),
    "VF-001": Construction(
        id="VF-001",
        name="locative assignment with nidadhāti",
        status="experimental",
        description="A karman value is placed in an adhikaraṇa storage location.",
    ),
    "VF-002": Construction(
        id="VF-002",
        name="instrumental increase with vardhayati",
        status="experimental",
        description="A karman stored value is increased by a karaṇa amount.",
    ),
    "VF-003": Construction(
        id="VF-003",
        name="object display with darśayati",
        status="experimental",
        description="A karman value is shown as program output.",
    ),
}
