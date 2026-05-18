from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .grammar import Analysis, GrammaticalNumber, Lakara, Pada, PartOfSpeech, Person


@dataclass(frozen=True)
class TinEnding:
    lakara: Lakara
    pada: Pada
    person: Person
    number: GrammaticalNumber
    ending: str


@dataclass(frozen=True)
class Dhatu:
    lemma: str
    present_stem: str
    pada: Pada
    gloss: str


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
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "te"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.THIRD, GrammaticalNumber.DUAL, "ete"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.THIRD, GrammaticalNumber.PLURAL, "ante"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.SECOND, GrammaticalNumber.SINGULAR, "se"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.SECOND, GrammaticalNumber.DUAL, "ethe"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.SECOND, GrammaticalNumber.PLURAL, "dhve"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.FIRST, GrammaticalNumber.SINGULAR, "e"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.FIRST, GrammaticalNumber.DUAL, "vahe"),
    TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.FIRST, GrammaticalNumber.PLURAL, "mahe"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "tu"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.DUAL, "tām"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.PLURAL, "ntu"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.SINGULAR, ""),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.DUAL, "tam"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.PLURAL, "ta"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.SINGULAR, "āni"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.DUAL, "āva"),
    TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.PLURAL, "āma"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "et"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.DUAL, "etām"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.PLURAL, "eyuḥ"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.SINGULAR, "eḥ"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.DUAL, "etam"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.PLURAL, "eta"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.SINGULAR, "eyam"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.DUAL, "eva"),
    TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.PLURAL, "ema"),
)


DHATUS: tuple[Dhatu, ...] = (
    Dhatu("bhū", "bhava", Pada.PARASMAIPADA, "become, be"),
    Dhatu("dṛś", "darśaya", Pada.PARASMAIPADA, "show"),
    Dhatu("vṛdh", "vardhaya", Pada.PARASMAIPADA, "increase"),
    Dhatu("nyūnaya", "nyūnaya", Pada.PARASMAIPADA, "lessen"),
    Dhatu("labh", "labha", Pada.ATMANEPADA, "obtain"),
)


def tin_ending(lakara: Lakara, pada: Pada, person: Person, number: GrammaticalNumber) -> str:
    for ending in TIN_ENDINGS:
        if ending.lakara == lakara and ending.pada == pada and ending.person == person and ending.number == number:
            return ending.ending
    raise ValueError(f"No tiṅ ending for {lakara.value}/{pada.value}/{person.value}/{number.value}")


def conjugate(dhatu: Dhatu, lakara: Lakara) -> dict[tuple[Person, GrammaticalNumber], str]:
    forms: dict[tuple[Person, GrammaticalNumber], str] = {}
    for ending in TIN_ENDINGS:
        if ending.lakara != lakara or ending.pada != dhatu.pada:
            continue
        forms[(ending.person, ending.number)] = join_stem_ending(dhatu.present_stem, ending)
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


def join_stem_ending(stem: str, ending: TinEnding) -> str:
    if ending.lakara == Lakara.VIDHILING and ending.pada == Pada.PARASMAIPADA:
        return stem[:-1] + ending.ending

    if ending.lakara == Lakara.LOT and ending.pada == Pada.PARASMAIPADA:
        if ending.person == Person.FIRST:
            return stem[:-1] + ending.ending
        if ending.ending == "":
            return stem

    if ending.lakara == Lakara.LAT and ending.pada == Pada.PARASMAIPADA:
        if ending.person == Person.FIRST:
            return stem[:-1] + "ā" + ending.ending

    if ending.lakara == Lakara.LAT and ending.pada == Pada.ATMANEPADA:
        if ending.ending == "e":
            return stem[:-1] + "e"

    return stem + ending.ending
