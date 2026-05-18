from dataclasses import dataclass
from typing import Set, Tuple
from .phonology import tokenize_sounds, is_consonant, is_vowel

@dataclass(frozen=True)
class MarkerAnalysis:
    lemma: str
    markers: frozenset[str]

def analyze_it_markers(upadesha: str, kind: str = "suffix", is_taddhita: bool = False) -> MarkerAnalysis:
    """
    Analyzes an upadesha (raw teaching form) and extracts its 'it' markers
    according to sutras 1.3.2 - 1.3.8.
    """
    sounds = tokenize_sounds(upadesha)
    if not sounds:
        return MarkerAnalysis("", frozenset())

    markers: Set[str] = set()
    to_remove: Set[int] = set()

    # 1.3.2: upadeśe'janunāsika it (Nasalized vowels marked with ~)
    i = 0
    while i < len(sounds):
        if is_vowel(sounds[i]) and i + 1 < len(sounds) and sounds[i+1] == "~":
            markers.add(sounds[i])
            to_remove.add(i)
            to_remove.add(i+1)
            i += 2
        else:
            i += 1

    # 1.3.3: halantyam (Final consonant is 'it')
    if is_consonant(sounds[-1]) and (len(sounds)-1) not in to_remove:
        # 1.3.4: na vibhaktau tusmāḥ
        if kind == "vibhakti" and sounds[-1] in {"t", "th", "d", "dh", "n", "s", "m"}:
            pass
        else:
            markers.add(sounds[-1])
            to_remove.add(len(sounds) - 1)

    # 1.3.5: ādirñituḍavaḥ (Initial ñi, tu, du - usually in roots)
    if kind == "root" and len(sounds) >= 2:
        if sounds[0] == "ñ" and sounds[1] == "i":
            markers.add("ñi")
            to_remove.add(0)
            to_remove.add(1)
        elif sounds[0] == "ṭ" and sounds[1] == "u":
            markers.add("ṭu")
            to_remove.add(0)
            to_remove.add(1)
        elif sounds[0] == "ḍ" and sounds[1] == "u":
            markers.add("ḍu")
            to_remove.add(0)
            to_remove.add(1)

    # Suffix-specific initial rules
    if kind in {"suffix", "vibhakti"} and 0 not in to_remove:
        # 1.3.6: ṣaḥ pratyayasya (Initial ṣ)
        if sounds[0] == "ṣ":
            markers.add("ṣ")
            to_remove.add(0)

        # 1.3.7: cuṭū (Initial palatals and cerebrals)
        palatals = {"c", "ch", "j", "jh", "ñ"}
        cerebrals = {"ṭ", "ṭh", "ḍ", "ḍh", "ṇ"}
        if sounds[0] in palatals or sounds[0] in cerebrals:
            if 0 not in to_remove:
                markers.add(sounds[0])
                to_remove.add(0)

        # 1.3.8: laśakvataddhite (Initial l, ś, k-varga, except in taddhita)
        k_varga = {"k", "kh", "g", "gh", "ṅ"}
        if not is_taddhita and (sounds[0] in {"l", "ś"} or sounds[0] in k_varga):
            # Special check for 'l' in lakaras: 'laṭ', 'liṭ' etc.
            is_lakara = (sounds[0] == "l" and len(sounds) >= 2 and is_vowel(sounds[1]))
            if not is_lakara:
                if 0 not in to_remove:
                    markers.add(sounds[0])
                    to_remove.add(0)

    # 1.3.9: tasya lopaḥ (The lemma is what remains)
    lemma_sounds = [sounds[i] for i in range(len(sounds)) if i not in to_remove]
    lemma = "".join(lemma_sounds)

    return MarkerAnalysis(lemma, frozenset(markers))
