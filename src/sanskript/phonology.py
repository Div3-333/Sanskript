from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from .grammar import Analysis


class SoundKind(str, Enum):
    VOWEL = "vowel"
    SEMIVOWEL = "semivowel"
    STOP = "stop"
    SIBILANT = "sibilant"
    ASPIRATE = "aspirate"


class VowelLength(str, Enum):
    SHORT = "hrasva"      # 1 mora
    LONG = "dīrgha"       # 2 moras
    PLUTA = "pluta"       # 3 moras
    DIPHTHONG = "diphthong" # Treated as dīrgha in duration (2 moras)


class Accent(str, Enum):
    UDATTA = "udātta"     # high pitch (1.2.29)
    ANUDATTA = "anudātta" # low pitch (1.2.30)
    SVARITA = "svarita"   # combined pitch (1.2.31)


class ArticulationPlace(str, Enum):
    GUTTURAL = "guttural"
    PALATAL = "palatal"
    RETROFLEX = "retroflex"
    DENTAL = "dental"
    LABIAL = "labial"
    GUTTURO_PALATAL = "gutturo-palatal"  # for e, ai
    GUTTURO_LABIAL = "gutturo-labial"    # for o, au
    DENTO_LABIAL = "dento-labial"        # for v


class Effort(str, Enum):
    SPRSTA = "spṛṣṭa"  # Complete contact (stops)
    ISA_SPRSTA = "īṣat-spṛṣṭa"  # Slight contact (semivowels)
    VIVRTA = "vivṛta"  # Open (vowels)
    SAMVRTA = "saṃvṛta"  # Closed (short 'a' in usage)
    ISA_VIVRTA = "īṣat-vivṛta"  # Slightly open (sibilants/aspirates)


@dataclass(frozen=True)
class Sound:
    symbol: str
    kind: SoundKind
    place: ArticulationPlace | None = None
    effort: Effort | None = None
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

IK_SOUNDS = frozenset({"i", "ī", "u", "ū", "ṛ", "ṝ", "ḷ"})

IK_GUNA_REPLACEMENTS = {
    "i": "e",
    "ī": "e",
    "u": "o",
    "ū": "o",
    "ṛ": "ar",
    "ṝ": "ar",
    "ḷ": "al",
}

IK_VRDDHI_REPLACEMENTS = {
    "i": "ai",
    "ī": "ai",
    "u": "au",
    "ū": "au",
    "ṛ": "ār",
    "ṝ": "ār",
    "ḷ": "āl",
}

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
    "a": Sound("a", SoundKind.VOWEL, ArticulationPlace.GUTTURAL, Effort.VIVRTA, VowelLength.SHORT),
    "ā": Sound("ā", SoundKind.VOWEL, ArticulationPlace.GUTTURAL, Effort.VIVRTA, VowelLength.LONG),
    "i": Sound("i", SoundKind.VOWEL, ArticulationPlace.PALATAL, Effort.VIVRTA, VowelLength.SHORT),
    "ī": Sound("ī", SoundKind.VOWEL, ArticulationPlace.PALATAL, Effort.VIVRTA, VowelLength.LONG),
    "u": Sound("u", SoundKind.VOWEL, ArticulationPlace.LABIAL, Effort.VIVRTA, VowelLength.SHORT),
    "ū": Sound("ū", SoundKind.VOWEL, ArticulationPlace.LABIAL, Effort.VIVRTA, VowelLength.LONG),
    "ṛ": Sound("ṛ", SoundKind.VOWEL, ArticulationPlace.RETROFLEX, Effort.VIVRTA, VowelLength.SHORT),
    "ṝ": Sound("ṝ", SoundKind.VOWEL, ArticulationPlace.RETROFLEX, Effort.VIVRTA, VowelLength.LONG),
    "ḷ": Sound("ḷ", SoundKind.VOWEL, ArticulationPlace.DENTAL, Effort.VIVRTA, VowelLength.SHORT),
    "e": Sound("e", SoundKind.VOWEL, ArticulationPlace.GUTTURO_PALATAL, Effort.VIVRTA, VowelLength.LONG),
    "ai": Sound("ai", SoundKind.VOWEL, ArticulationPlace.GUTTURO_PALATAL, Effort.VIVRTA, VowelLength.DIPHTHONG),
    "o": Sound("o", SoundKind.VOWEL, ArticulationPlace.GUTTURO_LABIAL, Effort.VIVRTA, VowelLength.LONG),
    "au": Sound("au", SoundKind.VOWEL, ArticulationPlace.GUTTURO_LABIAL, Effort.VIVRTA, VowelLength.DIPHTHONG),
    "k": Sound("k", SoundKind.STOP, ArticulationPlace.GUTTURAL, Effort.SPRSTA, voiced=False, aspirated=False),
    "kh": Sound("kh", SoundKind.STOP, ArticulationPlace.GUTTURAL, Effort.SPRSTA, voiced=False, aspirated=True),
    "g": Sound("g", SoundKind.STOP, ArticulationPlace.GUTTURAL, Effort.SPRSTA, voiced=True, aspirated=False),
    "gh": Sound("gh", SoundKind.STOP, ArticulationPlace.GUTTURAL, Effort.SPRSTA, voiced=True, aspirated=True),
    "ṅ": Sound("ṅ", SoundKind.STOP, ArticulationPlace.GUTTURAL, Effort.SPRSTA, voiced=True, aspirated=False, nasal=True),
    "c": Sound("c", SoundKind.STOP, ArticulationPlace.PALATAL, Effort.SPRSTA, voiced=False, aspirated=False),
    "ch": Sound("ch", SoundKind.STOP, ArticulationPlace.PALATAL, Effort.SPRSTA, voiced=False, aspirated=True),
    "j": Sound("j", SoundKind.STOP, ArticulationPlace.PALATAL, Effort.SPRSTA, voiced=True, aspirated=False),
    "jh": Sound("jh", SoundKind.STOP, ArticulationPlace.PALATAL, Effort.SPRSTA, voiced=True, aspirated=True),
    "ñ": Sound("ñ", SoundKind.STOP, ArticulationPlace.PALATAL, Effort.SPRSTA, voiced=True, aspirated=False, nasal=True),
    "ṭ": Sound("ṭ", SoundKind.STOP, ArticulationPlace.RETROFLEX, Effort.SPRSTA, voiced=False, aspirated=False),
    "ṭh": Sound("ṭh", SoundKind.STOP, ArticulationPlace.RETROFLEX, Effort.SPRSTA, voiced=False, aspirated=True),
    "ḍ": Sound("ḍ", SoundKind.STOP, ArticulationPlace.RETROFLEX, Effort.SPRSTA, voiced=True, aspirated=False),
    "ḍh": Sound("ḍh", SoundKind.STOP, ArticulationPlace.RETROFLEX, Effort.SPRSTA, voiced=True, aspirated=True),
    "ṇ": Sound("ṇ", SoundKind.STOP, ArticulationPlace.RETROFLEX, Effort.SPRSTA, voiced=True, aspirated=False, nasal=True),
    "t": Sound("t", SoundKind.STOP, ArticulationPlace.DENTAL, Effort.SPRSTA, voiced=False, aspirated=False),
    "th": Sound("th", SoundKind.STOP, ArticulationPlace.DENTAL, Effort.SPRSTA, voiced=False, aspirated=True),
    "d": Sound("d", SoundKind.STOP, ArticulationPlace.DENTAL, Effort.SPRSTA, voiced=True, aspirated=False),
    "dh": Sound("dh", SoundKind.STOP, ArticulationPlace.DENTAL, Effort.SPRSTA, voiced=True, aspirated=True),
    "n": Sound("n", SoundKind.STOP, ArticulationPlace.DENTAL, Effort.SPRSTA, voiced=True, aspirated=False, nasal=True),
    "p": Sound("p", SoundKind.STOP, ArticulationPlace.LABIAL, Effort.SPRSTA, voiced=False, aspirated=False),
    "ph": Sound("ph", SoundKind.STOP, ArticulationPlace.LABIAL, Effort.SPRSTA, voiced=False, aspirated=True),
    "b": Sound("b", SoundKind.STOP, ArticulationPlace.LABIAL, Effort.SPRSTA, voiced=True, aspirated=False),
    "bh": Sound("bh", SoundKind.STOP, ArticulationPlace.LABIAL, Effort.SPRSTA, voiced=True, aspirated=True),
    "m": Sound("m", SoundKind.STOP, ArticulationPlace.LABIAL, Effort.SPRSTA, voiced=True, aspirated=False, nasal=True),
    "y": Sound("y", SoundKind.SEMIVOWEL, ArticulationPlace.PALATAL, Effort.ISA_SPRSTA),
    "r": Sound("r", SoundKind.SEMIVOWEL, ArticulationPlace.RETROFLEX, Effort.ISA_SPRSTA),
    "l": Sound("l", SoundKind.SEMIVOWEL, ArticulationPlace.DENTAL, Effort.ISA_SPRSTA),
    "v": Sound("v", SoundKind.SEMIVOWEL, ArticulationPlace.DENTO_LABIAL, Effort.ISA_SPRSTA),
    "ś": Sound("ś", SoundKind.SIBILANT, ArticulationPlace.PALATAL, Effort.ISA_VIVRTA),
    "ṣ": Sound("ṣ", SoundKind.SIBILANT, ArticulationPlace.RETROFLEX, Effort.ISA_VIVRTA),
    "s": Sound("s", SoundKind.SIBILANT, ArticulationPlace.DENTAL, Effort.ISA_VIVRTA),
    "h": Sound("h", SoundKind.ASPIRATE, ArticulationPlace.GUTTURAL, Effort.ISA_VIVRTA),
}


def pratyahara(name: str, use_first_n: bool = False) -> tuple[str, ...]:
    """
    1.1.71 ādirantyena sahetā
    A pratyāhāra is formed by an initial sound and a final it-marker.

    Special case: marker 'ṇ' occurs twice (sutra 1 and sutra 6).
    - 'aṇ' in 1.1.69 uses the first 'ṇ'.
    - 'iṇ' and most other 'aṇ' uses refer to the second 'ṇ'.
    """
    marker = name[-1]
    remainder = name[:-1]

    # Try to find the start sound
    if remainder in SOUNDS:
        start = remainder
    elif remainder.endswith("a") and remainder[:-1] in SOUNDS:
        start = remainder[:-1]
    else:
        # Longest match fallback
        symbols = sorted(SOUNDS.keys(), key=len, reverse=True)
        start = None
        for symbol in symbols:
            if remainder.startswith(symbol):
                start = symbol
                break
        if not start:
             raise ValueError(f"Invalid pratyāhāra name: {name!r}")

    # Most pratyāhāras using 'ṇ' use the first occurrence (like 'yaṇ', 'aṇ' in 1.1.69).
    # 'iṇ' is the only one that always uses the second 'ṇ'.
    # 'aṇ' is ambiguous but 'use_first_n' can control it.
    is_in = (name == "iṇ")
    return sounds_between(start, marker, use_first_occurrence=(marker != "ṇ" or (not is_in and (use_first_n or name != "iṇ"))))


def best_substitute(target: str, candidates: Iterable[str]) -> str:
    """
    1.1.50 sthāne'ntaratamaḥ
    Among multiple candidates, the most similar one is chosen.
    Similarity is based on ArticulationPlace and Effort.
    """
    t_sound = SOUNDS.get(target)
    if not t_sound:
        return next(iter(candidates))

    best = None
    min_diff = float("inf")

    for cand in candidates:
        c_sound = SOUNDS.get(cand)
        if not c_sound:
            continue

        t_places = _place_parts(t_sound.place)
        c_places = _place_parts(c_sound.place)

        # Intersection of places (higher is better)
        place_match = len(t_places & c_places)
        # Difference in place count (lower is better)
        place_diff = abs(len(t_places) - len(c_places))

        # Total Place score (lower is better)
        # We use a large penalty for no match at all
        place_score = (10 - place_match * 5) + place_diff * 2

        effort_score = 0 if c_sound.effort == t_sound.effort else 1

        total_score = place_score + effort_score

        if total_score < min_diff:
            min_diff = total_score
            best = cand

    return best if best else next(iter(candidates))


def _place_parts(place: ArticulationPlace | None) -> set[str]:
    if place is None:
        return set()
    return set(place.value.split("-"))


def _enum_value(value: object) -> object:
    return getattr(value, "value", value)


def sounds_between(start: str, marker: str, use_first_occurrence: bool = False) -> tuple[str, ...]:
    tokens = [token for sutra in SHIVA_SUTRAS for token in sutra]
    start_index = next((index for index, token in enumerate(tokens) if not token.marker and token.symbol == start), None)
    if start_index is None:
        raise ValueError(f"Unknown pratyāhāra start sound: {start!r}")

    sounds: list[str] = []
    seen: set[str] = set()
    found_marker_count = 0
    for token in tokens[start_index:]:
        if token.marker and token.symbol == marker:
            found_marker_count += 1
            if use_first_occurrence or found_marker_count == 2 or marker != "ṇ":
                return tuple(sounds)
            continue

        if token.marker:
            continue

        if token.symbol not in seen:
            sounds.append(token.symbol)
            seen.add(token.symbol)

    if found_marker_count > 0:
        return tuple(sounds)

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


def is_ik(symbol: str) -> bool:
    return symbol in IK_SOUNDS


def guna_replacement_for_ik(symbol: str) -> str:
    """
    1.1.3 iko guṇavṛddhī: when guṇa applies by this rule, its target is an ik sound.
    """
    try:
        return IK_GUNA_REPLACEMENTS[symbol]
    except KeyError as exc:
        raise ValueError(f"Guṇa replacement under 1.1.3 requires an ik sound: {symbol!r}") from exc


def vrddhi_replacement_for_ik(symbol: str) -> str:
    """
    1.1.3 iko guṇavṛddhī: when vṛddhi applies by this rule, its target is an ik sound.
    """
    try:
        return IK_VRDDHI_REPLACEMENTS[symbol]
    except KeyError as exc:
        raise ValueError(f"Vṛddhi replacement under 1.1.3 requires an ik sound: {symbol!r}") from exc


def is_samyoga(sounds: list[str]) -> bool:
    """
    1.1.7 halo'nantarāḥ saṃyogaḥ
    A sequence of consonants (hal) without intervening vowels is called saṃyoga.
    """
    if len(sounds) < 2:
        return False
    return all(is_consonant(s) for s in sounds)


def is_anunasika(symbol: str) -> bool:
    """
    1.1.8 mukhanāsikāvacano'nunāsikaḥ
    Sounds pronounced with both mouth and nose are anunāsika.
    """
    sound = SOUNDS.get(symbol)
    return bool(sound and sound.nasal)


def is_savarna(left: str, right: str) -> bool:
    """
    1.1.9 tulya-āsya-prayatnaṃ savarṇam
    Sounds with the same place of articulation and internal effort are savarṇa.

    1.1.10 na-aj-jhalau
    Vowels (ac) and consonants (hal) are never savarṇa.

    Vārttika: ṛḷvarṇayormithaḥ sāvarṇyaṃ vācyam
    ṛ and ḷ are considered savarṇa despite different places.
    """
    if (left in {"ṛ", "ṝ"} and right == "ḷ") or (left == "ḷ" and right in {"ṛ", "ṝ"}):
        return True

    if is_vowel(left) != is_vowel(right):
        return False

    l_sound = SOUNDS.get(left)
    r_sound = SOUNDS.get(right)

    if not l_sound or not r_sound:
        return False

    # 1.1.9: same place and effort
    # Diphthongs e/ai and o/au share places but have different internal efforts
    # (vivṛta vs saṃvṛta vs other nuances in traditional phonetics,
    # but practically they are never savarṇa in the Aṣṭādhyāyī context).
    # Panini specifically groups them by effort in the Shiva Sutras.
    if left in {"e", "ai", "o", "au"} or right in {"e", "ai", "o", "au"}:
        return left == right

    return l_sound.place == r_sound.place and l_sound.effort == r_sound.effort


def savarna_class(symbol: str) -> tuple[str, ...]:
    """
    1.1.69 aṇudit savarṇasya cāpratyayaḥ.
    Return the known sound inventory members that are savarṇa with `symbol`.
    """
    if symbol not in SOUNDS:
        return ()
    return tuple(candidate for candidate in SOUNDS if is_savarna(symbol, candidate))


def savarna_reference(symbol: str, is_pratyaya: bool = False) -> tuple[str, ...]:
    """1.1.69 aṇudit savarṇasya cāpratyayaḥ with the apratyaya condition explicit."""
    if is_pratyaya:
        return ()
    return savarna_class(symbol)


def tapara_matches_duration(symbol: str, candidate: str) -> bool:
    """1.1.70 taparas tatkālasya: a t-marked sound refers only to the same duration."""
    left = SOUNDS.get(symbol)
    right = SOUNDS.get(candidate)
    if not left or not right:
        return False
    return left.length == right.length


def is_pragrhya(token: Analysis | str) -> bool:
    """
    1.1.11 īdūded-dvivacanam pragṛhyam
    1.1.12 adaso māt
    1.1.13 śe
    1.1.14 nipāta ekājanāṅ
    1.1.15 ot
    1.1.16 sambuddhau śākalyasyetāv-anārṣe
    1.1.17 uñ
    1.1.18 ūm
    1.1.19 īdūtau ca saptamyarthe

    Identifies if a word/form is pragṛhya (prohibits sandhi).
    """
    if isinstance(token, str):
        # Basic particle checks
        if token in {"e", "o", "u", "ū"}:  # 1.1.14, 1.1.15, 1.1.17, 1.1.18
            return True
        return False

    # Morphological checks
    if hasattr(token, "number") and _enum_value(token.number) == "dual":
        if token.surface.endswith(("ī", "ū", "e")):  # 1.1.11
            return True

    if hasattr(token, "lemma") and token.lemma == "adas" and token.surface.endswith(("mī", "mū")):  # 1.1.12
        return True

    if hasattr(token, "pos") and _enum_value(token.pos) == "indeclinable":
        if token.surface in {"e", "o", "i", "u", "ū"}:  # 1.1.14-1.1.18
            return True

    if hasattr(token, "case") and _enum_value(token.case) == "locative" and token.surface.endswith(("ī", "ū")):  # 1.1.19
        return True

    return False


def is_ti(word: str) -> str:
    """
    1.1.64 acyantyādi ṭi
    The last vowel and any following consonants in a word are called ṭi.
    """
    sounds = tokenize_sounds(word)
    vowel_positions = [index for index, sound in enumerate(sounds) if is_vowel(sound)]
    if not vowel_positions:
        return word
    last_vowel_idx = vowel_positions[-1]
    return "".join(sounds[last_vowel_idx:])


def is_upadha(word: str) -> str | None:
    """
    1.1.65 alo'ntyāt pūrva upadhā
    The second to last sound in a word is called upadhā.
    """
    sounds = tokenize_sounds(word)
    if len(sounds) < 2:
        return None
    return sounds[-2]


def is_aprkta(token: Analysis) -> bool:
    """
    1.2.41 apṛkta ekāl pratyayaḥ (Note: index says 1.1.67 or similar context for definitions)
    A suffix consisting of a single sound is called apṛkta.
    """
    # 1.2.41 is the actual definition, but it's often grouped here.
    # Let's check if the surface is a single sound and it's a suffix.
    sounds = tokenize_sounds(token.surface)
    return len(sounds) == 1


def first_vowel(word: str) -> str | None:
    for sound in tokenize_sounds(word):
        if is_vowel(sound):
            return sound
    return None


def is_vrddha_word(word: str, eastern_name: bool = False, tyadadi: bool = False) -> bool:
    """
    1.1.73-1.1.75 vṛddha-saṃjñā.
    Context switches keep tyadādi and eastern e/o names explicit rather than
    smuggling them into ordinary sound classification.
    """
    if tyadadi:
        return True
    vowel = first_vowel(word)
    if vowel is None:
        return False
    if is_vrddhi(vowel):
        return True
    return eastern_name and vowel in {"e", "o"}


def hrasva_substitute_for_ec(symbol: str) -> str:
    """
    1.1.48 eca iṅ hrasvādeśe.
    Short replacements for ec vowels use the i/u channel.
    """
    mapping = {"e": "i", "ai": "i", "o": "u", "au": "u"}
    try:
        return mapping[symbol]
    except KeyError as exc:
        raise ValueError(f"hrasva replacement under 1.1.48 requires an ec vowel: {symbol!r}") from exc


def rapara_substitute_for_ur(symbol: str, replacement: str) -> str:
    """
    1.1.51 uraṇ raparaḥ.
    When ṛ/ṝ/ḷ take an a/ā-type substitute, r/l is placed after it.
    """
    if symbol in {"ṛ", "ṝ"} and replacement in {"a", "ā"}:
        return f"{replacement}r"
    if symbol == "ḷ" and replacement in {"a", "ā"}:
        return f"{replacement}l"
    return replacement


def tokenize_sounds(word: str) -> list[str]:
    # Robust sound tokenizer using the SOUNDS registry
    sounds: list[str] = []
    i = 0
    # Sort symbols by length descending to match longest first (e.g., 'ai' before 'a')
    symbols = sorted(SOUNDS.keys(), key=len, reverse=True)
    while i < len(word):
        match = False
        for symbol in symbols:
            if word.startswith(symbol, i):
                sounds.append(symbol)
                i += len(symbol)
                match = True
                break
        if not match:
            # Fallback for unknown characters (e.g., punctuation)
            sounds.append(word[i])
            i += 1
    return sounds


def is_simple_vowel_savarna(left: str, right: str) -> bool:
    if not is_vowel(left) or not is_vowel(right):
        return False
    return is_savarna(left, right)


def sounds_by_place(place: ArticulationPlace) -> tuple[str, ...]:
    return tuple(
        symbol for symbol, sound in SOUNDS.items()
        if sound.place is not None and place.value in sound.place.value
    )
