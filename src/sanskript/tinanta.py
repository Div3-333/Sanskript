from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional

from .grammar import Analysis, GrammaticalNumber, Lakara, Pada, PartOfSpeech, Person


@dataclass(frozen=True)
class TinEnding:
    lakara: Lakara
    pada: Pada
    person: Person
    number: GrammaticalNumber
    ending: str


class TimeContext(str, Enum):
    PRESENT = "present"
    PAST = "past"
    FUTURE = "future"
    PAST_BEFORE_TODAY = "past_before_today"
    FUTURE_AFTER_TODAY = "future_after_today"
    CONDITIONAL = "conditional"
    IMPERATIVE = "imperative"
    POTENTIAL = "potential"


def is_sarvadhatuka(lakara: Lakara) -> bool:
    """
    3.4.113: tiṅ-śit sārvadhātukam.
    (In our model, LAT, LOT, LAN, VIDHILING are Sārvadhātuka).
    """
    return lakara in {Lakara.LAT, Lakara.LOT, Lakara.LAN, Lakara.VIDHILING}


def is_ardhadhatuka(lakara: Lakara) -> bool:
    """
    3.4.114: ārdhadhātukaṃ śeṣaḥ.
    3.4.115: liṭ ca.
    """
    if lakara == Lakara.LIT: return True
    return not is_sarvadhatuka(lakara)


def get_lakara_for_time(time: TimeContext) -> Lakara:
    """
    Partial lakāra selection scaffold for selected 3.2/3.3 contexts.
    """
    if time == TimeContext.PRESENT:
        # 3.2.123: vartamāne laṭ
        return Lakara.LAT
    elif time == TimeContext.PAST:
        # 3.2.110: luṅ
        return Lakara.LUN
    elif time == TimeContext.PAST_BEFORE_TODAY:
        # 3.2.111: anadyatane laṅ
        return Lakara.LAN
    elif time == TimeContext.FUTURE:
        # 3.3.15: lṛṭ śeṣe ca
        return Lakara.LRT
    elif time == TimeContext.FUTURE_AFTER_TODAY:
        # 3.3.33: anadyatane luṭ
        return Lakara.LUT
    elif time == TimeContext.CONDITIONAL:
        # 3.3.139: liṅ-nimitte lṛṅ-kriyātipattau
        return Lakara.LRN
    elif time == TimeContext.IMPERATIVE:
        # 3.3.162: loṭ ca
        return Lakara.LOT
    elif time == TimeContext.POTENTIAL:
        # 3.3.161: vidhi-nimantraṇa... liṅ-ca
        return Lakara.VIDHILING

    # 3.3.163: praiṣātisar-gaprāptakāleṣu kṛtyāśca (Kṛtya suffixes in command/permission)
    # This is a semantic mapping that allows Kṛtya (Tavya/Anīya) to act like Imperative.

    return Lakara.LAT


class DhatuType(str, Enum):
    BASIC = "basic"
    DESIDERATIVE = "san"
    INTENSIVE = "yaṅ"
    CAUSATIVE = "ṇic"
    DENOMINATIVE = "kyac"


@dataclass(frozen=True)
class Dhatu:
    lemma: str
    present_stem: str
    pada: Pada
    gloss: str
    varga: int = 1 # 1 to 10 (Gana)
    markers: frozenset[str] = frozenset()
    type: DhatuType = DhatuType.BASIC
    base_dhatu: Optional[Dhatu] = None


def get_vikarana(varga: int) -> str:
    """
    Partial vikarana scaffold for selected 3.1.68-3.1.81 behavior.
    """
    if varga == 1: return "a"   # 3.1.68: kartari śap
    if varga == 2: return ""    # 2.4.72: adiprabhṛtibhyaḥ śapaḥ (luk)
    if varga == 3: return ""    # 2.4.75: juhotyādibhyaḥ śluḥ
    if varga == 4: return "ya"  # 3.1.69: divādibhyaḥ śyan
    if varga == 5: return "nu"  # 3.1.73: svādibhyaḥ śnu
    if varga == 6: return "a"   # 3.1.77: tudādibhyaḥ śa
    if varga == 7: return "na"  # 3.1.78: rudhādibhyaḥ śnam (infix logic simplified here)
    if varga == 8: return "u"   # 3.1.79: tanādikṛñbhya uḥ
    if varga == 9: return "nā"  # 3.1.81: kryādibhyaḥ śnā
    if varga == 10: return "aya" # 3.1.25: curādibhyo ṇic
    return "a"

def create_derived_dhatu(base: Dhatu, type: DhatuType) -> Dhatu:
    """
    Partial sanādi-dhātu scaffold for selected 3.1.5-3.1.32 behavior.
    """
    if type == DhatuType.DESIDERATIVE:
        # 3.1.5: san
        stem = "bubhūṣa" if base.lemma == "bhū" else f"di{base.lemma}sa"
        return Dhatu(f"{base.lemma}-san", stem, base.pada, f"desire to {base.gloss}", type=type, base_dhatu=base)
    elif type == DhatuType.CAUSATIVE:
        # 3.1.25: ṇic
        stem = "bhāvaya" if base.lemma == "bhū" else f"{base.lemma}aya"
        return Dhatu(f"{base.lemma}-ṇic", stem, base.pada, f"cause to {base.gloss}", type=type, base_dhatu=base, varga=10)
    elif type == DhatuType.INTENSIVE:
        # 3.1.22: yaṅ
        return Dhatu(f"{base.lemma}-yaṅ", "bobhūya", Pada.ATMANEPADA, f"repeatedly {base.gloss}", type=type, base_dhatu=base)
    elif type == DhatuType.DENOMINATIVE:
        # 3.1.8: kyac
        return Dhatu(f"{base.lemma}-kyac", f"{base.lemma}īya", base.pada, f"act like {base.lemma}", type=type, base_dhatu=base)
    return base


TIN_ENDINGS: tuple[TinEnding, ...] = (
    TinEnding(Lakara.LAT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "ti"),
    TinEnding(Lakara.LAT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.DUAL, "taḥ"),
    TinEnding(Lakara.LAT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.PLURAL, "nti"),
    TinEnding(Lakara.LAT, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.SINGULAR, "si"),
    TinEnding(Lakara.LAT, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.DUAL, "thaḥ"),
    TinEnding(Lakara.LAT, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.PLURAL, "tha"),
    TinEnding(Lakara.LAT, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.SINGULAR, "mi"),
    TinEnding(Lakara.LAT, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.DUAL, "vaḥ"),
    TinEnding(Lakara.LAT, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.PLURAL, "maḥ"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "ta"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.THIRD, GrammaticalNumber.PLURAL, "jha"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.SECOND, GrammaticalNumber.SINGULAR, "thās"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.SECOND, GrammaticalNumber.PLURAL, "dhvam"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.FIRST, GrammaticalNumber.SINGULAR, "iḍ"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.FIRST, GrammaticalNumber.DUAL, "vahi"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.FIRST, GrammaticalNumber.PLURAL, "mahi"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "ti"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.DUAL, "taḥ"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.PLURAL, "nti"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.SINGULAR, "si"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.DUAL, "thaḥ"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.PLURAL, "tha"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.SINGULAR, "mi"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.DUAL, "vaḥ"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.PLURAL, "maḥ"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "ti"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.DUAL, "taḥ"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.PLURAL, "nti"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.SINGULAR, "si"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.DUAL, "thaḥ"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.PLURAL, "tha"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.SINGULAR, "mi"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.DUAL, "vaḥ"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.PLURAL, "maḥ"),

    # LRT (Future) - same basic endings as LAT
    TinEnding(Lakara.LRT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "ti"),
    TinEnding(Lakara.LRT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.DUAL, "taḥ"),
    TinEnding(Lakara.LRT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.PLURAL, "nti"),

    # LUT (Distant Future) - 3.4.94 specific endings for 3rd person
    TinEnding(Lakara.LUT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "ā"),
    TinEnding(Lakara.LUT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.DUAL, "ārau"),
    TinEnding(Lakara.LUT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.PLURAL, "āraḥ"),

    # LRN (Conditional) - LAN endings + sya
    TinEnding(Lakara.LRN, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "t"),
)


DHATUS: tuple[Dhatu, ...] = (
    Dhatu("bhū", "bhava", Pada.PARASMAIPADA, "become, be"),
    Dhatu("dṛś", "darśaya", Pada.PARASMAIPADA, "show"),
    Dhatu("vṛdh", "vardhaya", Pada.PARASMAIPADA, "increase"),
    Dhatu("nyūnaya", "nyūnaya", Pada.PARASMAIPADA, "lessen"),
    # 1.3.12 example: labh (labha~ṅ) -> ṅit -> Atmanepada
    Dhatu("labh", "labha", Pada.ATMANEPADA, "obtain", markers=frozenset({"ṅ"})),
    # 1.3.72 example: kṛ (ḍukṛñ) -> ñit -> Ubhayapada
    Dhatu("kṛ", "kuru", Pada.PARASMAIPADA, "do, make", markers=frozenset({"ñ"})),
    Dhatu("kṛ", "kuru", Pada.ATMANEPADA, "do, make", markers=frozenset({"ñ"})),
)


def tin_ending(lakara: Lakara, pada: Pada, person: Person, number: GrammaticalNumber) -> str:
    for ending in TIN_ENDINGS:
        if ending.lakara == lakara and ending.pada == pada and ending.person == person and ending.number == number:
            return ending.ending
    raise ValueError(f"No tiṅ ending for {lakara.value}/{pada.value}/{person.value}/{number.value}")


def get_substituted_dhatu(dhatu: Dhatu, lakara: Lakara) -> Dhatu:
    """
    Partial root-substitution scaffold for selected 2.4.35-2.4.57 behavior.
    """
    ardhadhatuka_lakaras = {Lakara.LIT, Lakara.LUN, Lakara.LRT, Lakara.LUT, Lakara.ASHIRLING, Lakara.LRN}

    # 2.4.36: ad -> jagdh
    if dhatu.lemma == "ad" and lakara in ardhadhatuka_lakaras:
        return Dhatu("jagdh", "jagdha", dhatu.pada, "eat")

    # 2.4.37: hano vadha liṅi
    if dhatu.lemma == "han" and lakara == Lakara.ASHIRLING:
        return Dhatu("vadh", "vadha", dhatu.pada, "kill")

    # 2.4.42: hano vadha luṅi
    if dhatu.lemma == "han" and lakara == Lakara.LUN:
        return Dhatu("vadh", "vadha", dhatu.pada, "kill")

    # 2.4.45: iṇo gā luṅi
    if dhatu.lemma == "i" and lakara == Lakara.LUN:
        return Dhatu("gā", "gā", dhatu.pada, "go")

    # 2.4.47: khyāñ-cakṣiṅaḥ
    if dhatu.lemma == "cakṣ":
        return Dhatu("khyā", "khyā", dhatu.pada, "see")

    # 2.4.48: iṅo gāṅ liṅi
    if dhatu.lemma == "i" and lakara == Lakara.ASHIRLING:
        return Dhatu("gā", "gā", dhatu.pada, "go")

    # 2.4.52: aster-bhūḥ
    if dhatu.lemma == "as" and lakara in ardhadhatuka_lakaras:
        return Dhatu("bhū", "bhava", dhatu.pada, "become, be")

    return dhatu

def apply_luk_elision(dhatu: Dhatu, ending: TinEnding) -> bool:
    """
    2.4.72: adiprabhṛtibhyaḥ śapaḥ (luk elision of śap for ad-ādi roots)
    In our simple model, this means no middle vowel 'a'.
    """
    # Simulate ad-ādi (Class 2) roots
    class_2_roots = {"as", "ad", "han", "vid"}
    return dhatu.lemma in class_2_roots

def conjugate(dhatu: Dhatu, lakara: Lakara) -> dict[tuple[Person, GrammaticalNumber], str]:
    forms: dict[tuple[Person, GrammaticalNumber], str] = {}

    # 2.4.35-57 substitutions
    effective_dhatu = get_substituted_dhatu(dhatu, lakara)

    # Ardhadhatuka Lakaras start from lemma, not present_stem (which includes śap)
    base_stem = effective_dhatu.lemma if is_ardhadhatuka(lakara) else effective_dhatu.present_stem

    for ending in TIN_ENDINGS:
        if ending.lakara != lakara or ending.pada != effective_dhatu.pada:
            continue
        forms[(ending.person, ending.number)] = join_stem_ending(base_stem, ending, effective_dhatu)
    return forms


def iter_tinanta_analyses() -> Iterable[Analysis]:
    for dhatu in DHATUS:
        for lakara in (Lakara.LAT, Lakara.LOT, Lakara.VIDHILING):
            for (person, number), surface in conjugate(dhatu, lakara).items():
                yield Analysis(
                    surface=surface,
                    lemma=dhatu.lemma,
                    pos=PartOfSpeech.VERB,
                    number=number,
                    person=person,
                    pada=dhatu.pada,
                    lakara=lakara,
                )


def join_stem_ending(stem: str, ending: TinEnding, dhatu: Dhatu | None = None) -> str:
    """
    Combines stem and ending with selected tiṅanta transformations.
    """
    effective_ending = ending.ending

    # 3.4.101: tas-tas-tha-mipāṃ tām-taṃ-ta-amaḥ (for ṅit lakaras and LOT)
    nit_lakaras = {Lakara.LAN, Lakara.LRN, Lakara.VIDHILING, Lakara.LUN}
    if (ending.lakara in nit_lakaras or ending.lakara == Lakara.LOT) and ending.pada == Pada.PARASMAIPADA:
        if effective_ending == "taḥ": effective_ending = "tām"
        elif effective_ending == "thaḥ": effective_ending = "tam"
        elif effective_ending == "tha": effective_ending = "ta"
        elif effective_ending == "mi":
             effective_ending = "ni" if ending.lakara == Lakara.LOT else "am"

        # 3.4.100: itaśca (elision of final i in ṅit lakaras)
        elif ending.lakara in nit_lakaras:
            if effective_ending == "ti": effective_ending = "t"
            elif effective_ending == "si": effective_ending = "s"
            # 3.4.108: jher-jus (jhi/nti -> jus in VIDHILING)
            elif effective_ending == "nti" and ending.lakara == Lakara.VIDHILING:
                effective_ending = "jus"

    # Simple Guna for Ardhadhatuka
    if is_ardhadhatuka(ending.lakara):
        if stem == "bhū": stem = "bhav"
        elif stem == "i": stem = "ay"
        elif stem == "kṛ": stem = "kar"

    # 3.1.33: syatāsi lṛ-luṭoḥ (sya for LRT/LRN, tasi for LUT)
    if ending.lakara in {Lakara.LRT, Lakara.LRN, Lakara.LUT}:
        # Elide final 'a' if it's there (e.g. from bhava)
        if stem.endswith("a") and len(stem) > 1:
             stem = stem[:-1]

        if not stem.endswith("i"):
            stem += "i"

        if ending.lakara in {Lakara.LRT, Lakara.LRN}:
            stem += "ṣya"
        elif ending.lakara == Lakara.LUT:
            if ending.person == Person.THIRD:
                 stem += "t"
            else:
                 stem += "tāsi"

    # 2.4.72: luk elision for ad-ādi roots (Class 2)
    if dhatu and apply_luk_elision(dhatu, ending):
        if stem.endswith("a") and len(stem) > 1:
             stem = stem[:-1]

    # 3.4.79: ṭit-ātmanepadānāṃ ṭere (Replacement of last vowel+consonant with 'e' in LAT, LRT, LOT)
    if ending.lakara in {Lakara.LAT, Lakara.LRT, Lakara.LOT} and ending.pada == Pada.ATMANEPADA:
        # 3.4.80: thāsas-se
        if effective_ending == "thās": effective_ending = "se"
        # 7.1.3/5: jha -> ante (simplified)
        elif effective_ending == "jha": effective_ending = "ante"
        elif effective_ending == "iḍ": effective_ending = "e"
        elif effective_ending == "dhvam": effective_ending = "dhve"
        elif effective_ending == "ta": effective_ending = "te"
        elif effective_ending.endswith("i"): # vahi, mahi
            effective_ending = effective_ending[:-1] + "e"

    # LOT specific transformations
    if ending.lakara == Lakara.LOT and ending.pada == Pada.PARASMAIPADA:
        # 3.4.86: er uḥ (i -> u for LOT endings)
        if effective_ending == "ti": effective_ending = "tu"
        elif effective_ending == "nti": effective_ending = "ntu"

        # 3.4.87: ser hiḥ (si -> hi for LOT)
        elif effective_ending == "si":
            # 3.4.88: ato heḥ (luk elision of hi after 'a')
            if stem.endswith("a"): return stem
            effective_ending = "hi"

        # 3.4.92: āḍ-uttamasya pic-ca (ā augment for 1st person)
        if ending.person == Person.FIRST:
            if stem.endswith("a"): stem = stem[:-1]
            stem += "ā"
            if effective_ending == "ni": pass
            elif effective_ending == "vaḥ": effective_ending = "va"
            elif effective_ending == "maḥ": effective_ending = "ma"

    if ending.lakara == Lakara.VIDHILING and ending.pada == Pada.PARASMAIPADA:
        # VIDHILING usually has 'iy' or 'y' infix, simplified here
        if stem.endswith("a"): stem = stem[:-1]
        if not effective_ending.startswith("e"): stem += "e"

    if ending.lakara == Lakara.LAT and ending.pada == Pada.PARASMAIPADA:
        if ending.person == Person.FIRST:
            if stem.endswith("a"): stem = stem[:-1] + "ā"

    if ending.lakara == Lakara.LAT and ending.pada == Pada.ATMANEPADA:
        if effective_ending == "e":
            if stem.endswith("a"): stem = stem[:-1] + "e"
            return stem
        # 6.1.97: ato guṇe (elision of a before vowel)
        if stem.endswith("a") and effective_ending.startswith(("a", "e")):
            stem = stem[:-1]

    return stem + effective_ending
