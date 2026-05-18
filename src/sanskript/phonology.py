from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SoundKind(str, Enum):
    VOWEL = "vowel"
    SEMIVOWEL = "semivowel"
    STOP = "stop"
    SIBILANT = "sibilant"
    ASPIRATE = "aspirate"


class VowelLength(str, Enum):
    SHORT = "short"
    LONG = "long"
    DIPHTHONG = "diphthong"


class ArticulationPlace(str, Enum):
    GUTTURAL = "guttural"
    PALATAL = "palatal"
    RETROFLEX = "retroflex"
    DENTAL = "dental"
    LABIAL = "labial"


@dataclass(frozen=True)
class Sound:
    symbol: str
    kind: SoundKind
    place: ArticulationPlace | None = None
    length: VowelLength | None = None
    voiced: bool | None = None
    aspirated: bool | None = None
    nasal: bool = False


@dataclass(frozen=True)
class ShivaToken:
    symbol: str
    marker: bool = False


SHIVA_SUTRAS: tuple[tuple[ShivaToken, ...], ...] = (
    tuple(ShivaToken(symbol) for symbol in ("a", "i", "u")) + (ShivaToken("ṇ", marker=True),),
    tuple(ShivaToken(symbol) for symbol in ("ṛ", "ḷ")) + (ShivaToken("k", marker=True),),
    tuple(ShivaToken(symbol) for symbol in ("e", "o")) + (ShivaToken("ṅ", marker=True),),
    tuple(ShivaToken(symbol) for symbol in ("ai", "au")) + (ShivaToken("c", marker=True),),
    tuple(ShivaToken(symbol) for symbol in ("h", "y", "v", "r")) + (ShivaToken("ṭ", marker=True),),
    (ShivaToken("l"), ShivaToken("ṇ", marker=True)),
    tuple(ShivaToken(symbol) for symbol in ("ñ", "m", "ṅ", "ṇ", "n")) + (ShivaToken("m", marker=True),),
    tuple(ShivaToken(symbol) for symbol in ("jh", "bh")) + (ShivaToken("ñ", marker=True),),
    tuple(ShivaToken(symbol) for symbol in ("gh", "ḍh", "dh")) + (ShivaToken("ṣ", marker=True),),
    tuple(ShivaToken(symbol) for symbol in ("j", "b", "g", "ḍ", "d")) + (ShivaToken("ś", marker=True),),
    tuple(ShivaToken(symbol) for symbol in ("kh", "ph", "ch", "ṭh", "th", "c", "ṭ", "t")) + (ShivaToken("v", marker=True),),
    tuple(ShivaToken(symbol) for symbol in ("k", "p")) + (ShivaToken("y", marker=True),),
    tuple(ShivaToken(symbol) for symbol in ("ś", "ṣ", "s")) + (ShivaToken("r", marker=True),),
    (ShivaToken("h"), ShivaToken("l", marker=True)),
)


COMMON_PRATYAHARAS = {
    "aṇ": ("a", "ṇ"),
    "ac": ("a", "c"),
    "al": ("a", "l"),
    "ec": ("e", "c"),
    "hal": ("h", "l"),
    "ik": ("i", "k"),
    "yaṇ": ("y", "ṇ"),
}


GUNA_SOUNDS = frozenset({"a", "e", "o"})
VRDDHI_SOUNDS = frozenset({"ā", "ai", "au"})

VOWEL_SAVARNA_BASE = {
    "a": "a",
    "ā": "a",
    "i": "i",
    "ī": "i",
    "u": "u",
    "ū": "u",
    "ṛ": "ṛ",
    "ṝ": "ṛ",
    "ḷ": "ḷ",
}


SOUNDS: dict[str, Sound] = {
    "a": Sound("a", SoundKind.VOWEL, ArticulationPlace.GUTTURAL, VowelLength.SHORT),
    "ā": Sound("ā", SoundKind.VOWEL, ArticulationPlace.GUTTURAL, VowelLength.LONG),
    "i": Sound("i", SoundKind.VOWEL, ArticulationPlace.PALATAL, VowelLength.SHORT),
    "ī": Sound("ī", SoundKind.VOWEL, ArticulationPlace.PALATAL, VowelLength.LONG),
    "u": Sound("u", SoundKind.VOWEL, ArticulationPlace.LABIAL, VowelLength.SHORT),
    "ū": Sound("ū", SoundKind.VOWEL, ArticulationPlace.LABIAL, VowelLength.LONG),
    "ṛ": Sound("ṛ", SoundKind.VOWEL, ArticulationPlace.RETROFLEX, VowelLength.SHORT),
    "ṝ": Sound("ṝ", SoundKind.VOWEL, ArticulationPlace.RETROFLEX, VowelLength.LONG),
    "ḷ": Sound("ḷ", SoundKind.VOWEL, ArticulationPlace.DENTAL, VowelLength.SHORT),
    "e": Sound("e", SoundKind.VOWEL, ArticulationPlace.PALATAL, VowelLength.LONG),
    "ai": Sound("ai", SoundKind.VOWEL, ArticulationPlace.PALATAL, VowelLength.DIPHTHONG),
    "o": Sound("o", SoundKind.VOWEL, ArticulationPlace.LABIAL, VowelLength.LONG),
    "au": Sound("au", SoundKind.VOWEL, ArticulationPlace.LABIAL, VowelLength.DIPHTHONG),
    "k": Sound("k", SoundKind.STOP, ArticulationPlace.GUTTURAL, voiced=False, aspirated=False),
    "kh": Sound("kh", SoundKind.STOP, ArticulationPlace.GUTTURAL, voiced=False, aspirated=True),
    "g": Sound("g", SoundKind.STOP, ArticulationPlace.GUTTURAL, voiced=True, aspirated=False),
    "gh": Sound("gh", SoundKind.STOP, ArticulationPlace.GUTTURAL, voiced=True, aspirated=True),
    "ṅ": Sound("ṅ", SoundKind.STOP, ArticulationPlace.GUTTURAL, voiced=True, aspirated=False, nasal=True),
    "c": Sound("c", SoundKind.STOP, ArticulationPlace.PALATAL, voiced=False, aspirated=False),
    "ch": Sound("ch", SoundKind.STOP, ArticulationPlace.PALATAL, voiced=False, aspirated=True),
    "j": Sound("j", SoundKind.STOP, ArticulationPlace.PALATAL, voiced=True, aspirated=False),
    "jh": Sound("jh", SoundKind.STOP, ArticulationPlace.PALATAL, voiced=True, aspirated=True),
    "ñ": Sound("ñ", SoundKind.STOP, ArticulationPlace.PALATAL, voiced=True, aspirated=False, nasal=True),
    "ṭ": Sound("ṭ", SoundKind.STOP, ArticulationPlace.RETROFLEX, voiced=False, aspirated=False),
    "ṭh": Sound("ṭh", SoundKind.STOP, ArticulationPlace.RETROFLEX, voiced=False, aspirated=True),
    "ḍ": Sound("ḍ", SoundKind.STOP, ArticulationPlace.RETROFLEX, voiced=True, aspirated=False),
    "ḍh": Sound("ḍh", SoundKind.STOP, ArticulationPlace.RETROFLEX, voiced=True, aspirated=True),
    "ṇ": Sound("ṇ", SoundKind.STOP, ArticulationPlace.RETROFLEX, voiced=True, aspirated=False, nasal=True),
    "t": Sound("t", SoundKind.STOP, ArticulationPlace.DENTAL, voiced=False, aspirated=False),
    "th": Sound("th", SoundKind.STOP, ArticulationPlace.DENTAL, voiced=False, aspirated=True),
    "d": Sound("d", SoundKind.STOP, ArticulationPlace.DENTAL, voiced=True, aspirated=False),
    "dh": Sound("dh", SoundKind.STOP, ArticulationPlace.DENTAL, voiced=True, aspirated=True),
    "n": Sound("n", SoundKind.STOP, ArticulationPlace.DENTAL, voiced=True, aspirated=False, nasal=True),
    "p": Sound("p", SoundKind.STOP, ArticulationPlace.LABIAL, voiced=False, aspirated=False),
    "ph": Sound("ph", SoundKind.STOP, ArticulationPlace.LABIAL, voiced=False, aspirated=True),
    "b": Sound("b", SoundKind.STOP, ArticulationPlace.LABIAL, voiced=True, aspirated=False),
    "bh": Sound("bh", SoundKind.STOP, ArticulationPlace.LABIAL, voiced=True, aspirated=True),
    "m": Sound("m", SoundKind.STOP, ArticulationPlace.LABIAL, voiced=True, aspirated=False, nasal=True),
    "y": Sound("y", SoundKind.SEMIVOWEL, ArticulationPlace.PALATAL),
    "r": Sound("r", SoundKind.SEMIVOWEL, ArticulationPlace.RETROFLEX),
    "l": Sound("l", SoundKind.SEMIVOWEL, ArticulationPlace.DENTAL),
    "v": Sound("v", SoundKind.SEMIVOWEL, ArticulationPlace.LABIAL),
    "ś": Sound("ś", SoundKind.SIBILANT, ArticulationPlace.PALATAL),
    "ṣ": Sound("ṣ", SoundKind.SIBILANT, ArticulationPlace.RETROFLEX),
    "s": Sound("s", SoundKind.SIBILANT, ArticulationPlace.DENTAL),
    "h": Sound("h", SoundKind.ASPIRATE, ArticulationPlace.GUTTURAL),
}


def pratyahara(name: str) -> tuple[str, ...]:
    try:
        start, marker = COMMON_PRATYAHARAS[name]
    except KeyError as exc:
        raise ValueError(f"Unknown pratyāhāra in the controlled phonology set: {name!r}") from exc
    return sounds_between(start, marker)


def sounds_between(start: str, marker: str) -> tuple[str, ...]:
    tokens = [token for sutra in SHIVA_SUTRAS for token in sutra]
    start_index = next((index for index, token in enumerate(tokens) if not token.marker and token.symbol == start), None)
    if start_index is None:
        raise ValueError(f"Unknown pratyāhāra start sound: {start!r}")

    sounds: list[str] = []
    seen: set[str] = set()
    for token in tokens[start_index:]:
        if token.marker and token.symbol == marker:
            return tuple(sounds)
        if token.marker:
            continue
        if token.symbol not in seen:
            sounds.append(token.symbol)
            seen.add(token.symbol)

    raise ValueError(f"Marker {marker!r} does not occur after start sound {start!r}")


def is_vowel(symbol: str) -> bool:
    sound = SOUNDS.get(symbol)
    return bool(sound and sound.kind == SoundKind.VOWEL)


def is_consonant(symbol: str) -> bool:
    sound = SOUNDS.get(symbol)
    return bool(sound and sound.kind != SoundKind.VOWEL)


def is_guna(symbol: str) -> bool:
    return symbol in GUNA_SOUNDS


def is_vrddhi(symbol: str) -> bool:
    return symbol in VRDDHI_SOUNDS


def is_simple_vowel_savarna(left: str, right: str) -> bool:
    left_base = VOWEL_SAVARNA_BASE.get(left)
    right_base = VOWEL_SAVARNA_BASE.get(right)
    return left_base is not None and left_base == right_base


def sounds_by_place(place: ArticulationPlace) -> tuple[str, ...]:
    return tuple(symbol for symbol, sound in SOUNDS.items() if sound.place == place)
