from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DerivationFamily(str, Enum):
    KRT = "kṛt"
    TADDHITA = "taddhita"


class KrtSuffix(str, Enum):
    KTVA = "ktvā"
    TUMUN = "tumun"
    KTA = "kta"
    KTAVATU = "ktavatu"
    TAVYA = "tavya"
    ANIYA = "anīya"
    SHATR = "śatṛ"
    SHANAC = "śānac"
    GHAN = "ghañ"


class TaddhitaSuffix(str, Enum):
    APATYA = "apatya"
    MATUP = "matu̐p"
    ATISHAYANA = "atiśāyana"


@dataclass(frozen=True)
class DerivedForm:
    source: str
    suffix: KrtSuffix | TaddhitaSuffix
    family: DerivationFamily
    surface: str
    gloss: str


KRT_FORMS: tuple[DerivedForm, ...] = (
    DerivedForm("bhū", KrtSuffix.KTVA, DerivationFamily.KRT, "bhūtvā", "having become"),
    DerivedForm("bhū", KrtSuffix.TUMUN, DerivationFamily.KRT, "bhavitum", "to become"),
    DerivedForm("bhū", KrtSuffix.KTA, DerivationFamily.KRT, "bhūta", "become, been"),
    DerivedForm("bhū", KrtSuffix.TAVYA, DerivationFamily.KRT, "bhavitavya", "to be become or to be"),
    DerivedForm("dṛś", KrtSuffix.TUMUN, DerivationFamily.KRT, "draṣṭum", "to see"),
    DerivedForm("dṛś", KrtSuffix.KTA, DerivationFamily.KRT, "dṛṣṭa", "seen"),
    DerivedForm("nī", KrtSuffix.ANIYA, DerivationFamily.KRT, "nayanīya", "to be led"),
    DerivedForm("pac", KrtSuffix.SHATR, DerivationFamily.KRT, "pacat", "cooking"),
    DerivedForm("labh", KrtSuffix.SHANAC, DerivationFamily.KRT, "labhamāna", "obtaining"),
    DerivedForm("kṛ", KrtSuffix.GHAN, DerivationFamily.KRT, "kāra", "doing, making"),
)


TADDHITA_FORMS: tuple[DerivedForm, ...] = (
    DerivedForm("bala", TaddhitaSuffix.MATUP, DerivationFamily.TADDHITA, "balavān", "possessing strength"),
    DerivedForm("go", TaddhitaSuffix.MATUP, DerivationFamily.TADDHITA, "gomān", "possessing cattle"),
    DerivedForm("upagu", TaddhitaSuffix.APATYA, DerivationFamily.TADDHITA, "aupagava", "descendant of Upagu"),
    DerivedForm("laghu", TaddhitaSuffix.ATISHAYANA, DerivationFamily.TADDHITA, "laghiṣṭha", "lightest"),
)


def derive(source: str, suffix: KrtSuffix | TaddhitaSuffix) -> DerivedForm:
    for form in KRT_FORMS + TADDHITA_FORMS:
        if form.source == source and form.suffix == suffix:
            return form
    raise ValueError(f"No controlled derived form for {source!r} with suffix {suffix.value!r}")


def forms_by_family(family: DerivationFamily) -> tuple[DerivedForm, ...]:
    return tuple(form for form in KRT_FORMS + TADDHITA_FORMS if form.family == family)
