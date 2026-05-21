from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from .grammar import Analysis, GrammaticalNumber, PartOfSpeech, Samjna, Case, Gender

class SamasaType(str, Enum):
    KEVALA = "kevala"
    AVYAYIBHAVA = "avyayībhāva"
    TATPURUSHA = "tatpuruṣa"
    DVIGU = "dvigu"
    KARMADHARAYA = "karmadhāraya"
    BAHUVRIHI = "bahuvrīhi"
    DVANDVA = "dvandva"

class SamasaSense(str, Enum):
    VIBHAKTI = "vibhakti"
    SAMIPA = "samīpa"
    SAMRDDHI = "samṛddhi"
    ARTHABHAVA = "arthābhāva"
    YATHA = "yathā"
    AVADHARANA = "avadhāraṇa"
    MATRA = "mātrā"
    PARINA = "pariṇā"
    PANCAMI_AVYAYIBHAVA = "pañcamī-avyayībhāva"
    MARYADA_ABHIVIDHI = "maryādā-abhividhi"
    ABHIMUKHYA = "ābhimukhya"
    ANU_SAMAYA = "anu-samaya"
    AYAMA = "āyāma"
    LEXICAL_AVYAYIBHAVA = "lexical-avyayībhāva"
    VAMSHYA = "vaṃśya"
    NADI = "nadī"
    UPAMANA = "upamāna"
    SHASH_TAT = "ṣaṣṭhī-tatpuruṣa"
    DVIT_TAT = "dvitīyā-tatpuruṣa"
    TRT_TAT = "tṛtīyā-tatpuruṣa"
    CAT_TAT = "caturthī-tatpuruṣa"
    PAN_TAT = "pañcamī-tatpuruṣa"
    SAP_TAT = "saptamī-tatpuruṣa"

@dataclass(frozen=True)
class Compound:
    type: SamasaType
    members: tuple[Analysis, ...]
    surface: str
    gloss: str
    sense: SamasaSense | None = None
    is_optional: bool = False
    result_analysis: Analysis | None = None


@dataclass(frozen=True)
class CompoundExample:
    surface: str
    samasa_type: SamasaType
    members: tuple[str, ...]
    gloss: str


COMPOUND_EXAMPLES: tuple[CompoundExample, ...] = (
    CompoundExample("upagrāmam", SamasaType.AVYAYIBHAVA, ("upa", "grāmam"), "near the village"),
    CompoundExample("rājapuruṣaḥ", SamasaType.TATPURUSHA, ("rājñaḥ", "puruṣaḥ"), "king's man"),
    CompoundExample("pītāmbaraḥ", SamasaType.BAHUVRIHI, ("pīta", "ambara"), "one whose garment is yellow"),
    CompoundExample("rāmalakṣmaṇau", SamasaType.DVANDVA, ("rāmaḥ", "lakṣmaṇaḥ"), "Rāma and Lakṣmaṇa"),
)


def classify_compound(surface: str) -> SamasaType:
    for example in COMPOUND_EXAMPLES:
        if example.surface == surface:
            return example.samasa_type
    raise ValueError(f"Unknown controlled compound example: {surface!r}")


def examples_for(samasa_type: SamasaType) -> tuple[CompoundExample, ...]:
    return tuple(example for example in COMPOUND_EXAMPLES if example.samasa_type == samasa_type)

def is_samartha(analyses: list[Analysis]) -> bool:
    """
    2.1.1: samarthaḥ padavidhiḥ.
    Padas must have a syntactic-semantic relationship (ekārthībhāva).
    """
    if len(analyses) < 2:
        return False
    # Paninian requirement: semantic connection.
    # In a computational engine, we check if they are part of a valid syntactic tree.
    # For now, we assume explicit compounding requests imply samarthya.
    return True

def create_compound(members: list[Analysis], forced_type: SamasaType | None = None) -> Compound:
    """
    Partial samāsa derivation scaffold for selected 2.1/2.2 contexts.
    """
    if not is_samartha(members):
        raise ValueError("Members are not samartha (2.1.1)")

    samasa_type = forced_type or SamasaType.KEVALA
    sense = None
    is_optional = False

    # 2.4.71: supo dhātu-prātipadikayoḥ (Elision of internal suffixes)
    # We use lemmas (bases) for the internal members.
    base_members = []
    for i, m in enumerate(members):
        # 1.2.43: prathamā-nirdiṣṭaṃ samāsa upasarjanam
        # 2.2.30: upasarjanaṃ pūrvam (Upasarjana comes first)
        # In our engine, we assume order is provided, but we flag the first as upasarjana usually.
        base_members.append(m.lemma)

    # 2.1.5: avyayaṃ vibhakti...
    if members[0].pos == PartOfSpeech.INDECLINABLE:
        samasa_type = SamasaType.AVYAYIBHAVA
        first = members[0].lemma
        second = members[1].lemma if len(members) > 1 else ""
        if first == "upa": sense = SamasaSense.SAMIPA
        elif first == "yathā": sense = SamasaSense.YATHA
        elif first == "yāvat": sense = SamasaSense.AVADHARANA
        elif first == "supprati": sense = SamasaSense.MATRA
        elif first in {"akṣa", "śalākā", "saṃkhyā"} and second == "pariṇā": sense = SamasaSense.PARINA
        elif first in {"apa", "pari", "bahir", "añc"} and members[1].case == Case.ABLATIVE: sense = SamasaSense.PANCAMI_AVYAYIBHAVA
        elif first == "āṅ": sense = SamasaSense.MARYADA_ABHIVIDHI
        elif first in {"abhi", "prati"}: sense = SamasaSense.ABHIMUKHYA
        elif first == "anu": sense = SamasaSense.ANU_SAMAYA
        elif first == "yasya" and second == "āyāma": sense = SamasaSense.AYAMA
        elif first in {"tiṣṭhadgu", "prabhṛti"}: sense = SamasaSense.LEXICAL_AVYAYIBHAVA
        elif first == "nir": sense = SamasaSense.ARTHABHAVA

    # 2.1.22: tatpuruṣaḥ
    if not forced_type and samasa_type == SamasaType.KEVALA:
         m0, m1 = members[0], (members[1] if len(members) > 1 else None)
         is_numeral = m0.pos == PartOfSpeech.NUMERAL or m0.value is not None

         if m0.case == Case.ACCUSATIVE:
              samasa_type = SamasaType.TATPURUSHA
              sense = SamasaSense.DVIT_TAT
         elif m0.case == Case.INSTRUMENTAL:
              samasa_type = SamasaType.TATPURUSHA
              sense = SamasaSense.TRT_TAT
         elif m0.case == Case.DATIVE:
              samasa_type = SamasaType.TATPURUSHA
              sense = SamasaSense.CAT_TAT
         elif m0.case == Case.ABLATIVE:
              samasa_type = SamasaType.TATPURUSHA
              sense = SamasaSense.PAN_TAT
         elif m0.case == Case.GENITIVE:
              samasa_type = SamasaType.TATPURUSHA
              sense = SamasaSense.SHASH_TAT
              if m0.lemma in {"pāra", "madhya"}: is_optional = True
         elif m0.case == Case.LOCATIVE:
              samasa_type = SamasaType.TATPURUSHA
              sense = SamasaSense.SAP_TAT

         if is_numeral and samasa_type == SamasaType.TATPURUSHA:
              samasa_type = SamasaType.DVIGU
         if is_numeral and m1 and m1.lemma == "vaṃśya":
              samasa_type = SamasaType.TATPURUSHA
              sense = SamasaSense.VAMSHYA
         if m1 and m0.lemma in {"gaṅgā", "yamunā", "sarasvatī"} and m1.lemma in {"gaṅgā", "yamunā", "sarasvatī"}:
              samasa_type = SamasaType.TATPURUSHA
              sense = SamasaSense.NADI
         if m1 and m0.case == m1.case and m0.gender == m1.gender:
              if samasa_type != SamasaType.DVIGU:
                   samasa_type = SamasaType.KARMADHARAYA
                   is_optional = True
         if m1 and m0.case == m1.case and samasa_type == SamasaType.KEVALA:
              samasa_type = SamasaType.DVANDVA

    if forced_type == SamasaType.BAHUVRIHI:
         samasa_type = SamasaType.BAHUVRIHI

    # 2.4.71: Elide suffixes. Compound surface is Base1 + Base2 + FinalSuffix
    # We use the surface of the last member for the final suffix representation.
    surface = "".join(base_members[:-1]) + members[-1].surface

    # 2.4.17: avyayībhāvaśca (Avyayibhava is neuter)
    # 2.4.18: sa napuṃsakam (It is neuter singular)
    result_analysis = None
    if samasa_type == SamasaType.AVYAYIBHAVA:
        result_analysis = Analysis(
            surface=surface,
            lemma=surface,
            pos=PartOfSpeech.NOUN,
            gender=Gender.NEUTER,
            number=GrammaticalNumber.SINGULAR,
            samjnas=frozenset({Samjna.AVYAYA, Samjna.PADA})
        )
    elif samasa_type == SamasaType.DVIGU:
        # 2.4.1: dviguś-caikam-vacanam (Dvigu is singular)
        result_analysis = Analysis(
            surface=surface,
            lemma=surface,
            pos=PartOfSpeech.NOUN,
            gender=members[-1].gender,
            number=GrammaticalNumber.SINGULAR,
            samjnas=frozenset({Samjna.PADA})
        )
    elif samasa_type == SamasaType.DVANDVA:
        # 2.4.2: dvandvaś-ca prāṇi-tūrya-senāṅgānām (Samahara-Dvandva)
        # For simplicity, if we detect semantic roles matching these, we'd make it singular neuter.
        # Otherwise, 2.4.26: paraval-liṅgaṃ dvandva-tatpuruṣayoḥ
        # 2.4.27: pūrvavad aśvavaḍavau — aśva+vaḍava follow the first member's gender.
        lemmas = {member.lemma for member in members}
        if {"aśva", "vaḍava"} <= lemmas:
            gender_member = members[0]
        else:
            gender_member = members[-1]
        result_analysis = Analysis(
            surface=surface,
            lemma=surface,
            pos=gender_member.pos,
            gender=gender_member.gender,
            number=_get_compound_number(members),
            case=gender_member.case,
            samjnas=frozenset({Samjna.PADA})
        )
    else:
        # 2.4.26: paraval-liṅgaṃ dvandva-tatpuruṣayoḥ
        last = members[-1]
        result_analysis = Analysis(
            surface=surface,
            lemma=surface,
            pos=last.pos,
            gender=last.gender,
            number=last.number if samasa_type != SamasaType.DVIGU else GrammaticalNumber.SINGULAR,
            case=last.case,
            samjnas=frozenset({Samjna.PADA})
        )

    return Compound(
        type=samasa_type,
        members=tuple(members),
        surface=surface,
        gloss=" + ".join(m.lemma for m in members),
        sense=sense,
        is_optional=is_optional,
        result_analysis=result_analysis
    )

def _get_compound_number(members: list[Analysis]) -> GrammaticalNumber:
    count = len(members)
    if count == 1: return GrammaticalNumber.SINGULAR
    if count == 2: return GrammaticalNumber.DUAL
    return GrammaticalNumber.PLURAL

def apply_ekashesha(analyses: list[Analysis]) -> Analysis | None:
    """
    1.2.64 - 1.2.73 Ekashesha (Single Remainder) Rules.
    Reduces a list of related analyses to a single 'remainder' analysis.
    """
    if not analyses:
        return None
    if len(analyses) == 1:
        return analyses[0]

    # Rule 1.2.72: Pronouns (tyadādi) always remain
    pronouns = [a for a in analyses if a.lemma in {"tad", "etad", "yad", "idam"}]
    if pronouns:
        remainder = pronouns[0]
        return _update_number(remainder, len(analyses))

    # Rule 1.2.65: vṛddho yūnā (elder remains over younger)
    if any(a.lemma.endswith("ya") for a in analyses) and any(a.lemma.endswith("yaṇa") for a in analyses):
        remainder = next(a for a in analyses if a.lemma.endswith("ya"))
        return _update_number(remainder, len(analyses))

    # Rule 1.2.68: bhrātṛ remains over svasṛ; putra remains over duhitṛ
    if all(a.lemma in {"bhrātṛ", "svasṛ"} for a in analyses):
        remainder = next((a for a in analyses if a.lemma == "bhrātṛ"), analyses[0])
        return _update_number(remainder, len(analyses))
    if all(a.lemma in {"putra", "duhitṛ"} for a in analyses):
        remainder = next((a for a in analyses if a.lemma == "putra"), analyses[0])
        return _update_number(remainder, len(analyses))

    # Rule 1.2.70: pitṛ remains over mātṛ
    if all(a.lemma in {"pitṛ", "mātṛ"} for a in analyses):
        remainder = next((a for a in analyses if a.lemma == "pitṛ"), analyses[0])
        return _update_number(remainder, len(analyses))

    # Rule 1.2.71: śvaśura remains over śvaśrū
    if all(a.lemma in {"śvaśura", "śvaśrū"} for a in analyses):
        remainder = next((a for a in analyses if a.lemma == "śvaśura"), analyses[0])
        return _update_number(remainder, len(analyses))

    # Rule 1.2.73: grāmya-paśu-saṃgheṣu ataruṇeṣu strī.
    animal_lemmas = {"go", "avi", "aja", "paśu", "aśva", "uṣṭra"}
    feminine_animals = [a for a in analyses if _has_gender(a, Gender.FEMININE) and a.lemma in animal_lemmas]
    if feminine_animals and all(a.lemma in animal_lemmas for a in analyses):
        return _update_number(feminine_animals[0], len(analyses))

    # Rule 1.2.67: Masculine remains over feminine
    masculine = [a for a in analyses if _has_gender(a, Gender.MASCULINE)]
    feminine = [a for a in analyses if _has_gender(a, Gender.FEMININE)]
    if masculine and feminine:
        remainder = masculine[0]
        return _update_number(remainder, len(analyses))

    # Rule 1.2.69: Neuter remains over non-neuter
    neuter = [a for a in analyses if _has_gender(a, Gender.NEUTER)]
    if neuter and (masculine or feminine):
        remainder = neuter[0]
        return _update_number(remainder, len(analyses))

    # Rule 1.2.64: Homonyms (same form)
    if all(a.surface == analyses[0].surface for a in analyses):
        return _update_number(analyses[0], len(analyses))

    return _update_number(analyses[0], len(analyses))

def _update_number(analysis: Analysis, count: int) -> Analysis:
    new_number = GrammaticalNumber.SINGULAR
    if count == 2:
        new_number = GrammaticalNumber.DUAL
    elif count > 2:
        new_number = GrammaticalNumber.PLURAL

    return Analysis(**{**analysis.__dict__, "number": new_number})


def _has_gender(analysis: Analysis, gender: Gender) -> bool:
    return analysis.gender in {gender, gender.value, gender.name}
