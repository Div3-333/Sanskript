from .grammar import Samjna, Gender, Analysis, PartOfSpeech
from .phonology import tokenize_sounds, is_vowel, is_consonant, SOUNDS, VowelLength

GHU_ROOTS = frozenset({"dā", "dhā"})
GHU_EXCLUSIONS = frozenset({"dāp", "daip"})
GHA_SUFFIXES = frozenset({"tarap", "tamap"})
SANKHYA_TERMS = frozenset({"bahu", "gaṇa", "vatu", "ḍati"})
SHAT_NUMERALS = frozenset({"ṣaṣ", "pañcan", "saptan", "aṣṭan", "navan", "daśan"})
NISTHA_SUFFIXES = frozenset({"kta", "ktavatū"})
SARVANAMA_STEMS = frozenset(
    {
        "sarva",
        "viśva",
        "ubha",
        "ubhaya",
        "anya",
        "anyatara",
        "itara",
        "tad",
        "yad",
        "etad",
        "idam",
        "adas",
        "eka",
        "dvi",
        "yūṣmad",
        "asmad",
        "bhavat",
        "kim",
    }
)


def is_ghu_root(lemma: str) -> bool:
    """1.1.20 dādhā ghvadāp: dā/dhā roots receive ghu-saṃjñā, excluding dāp/daip."""
    return lemma in GHU_ROOTS and lemma not in GHU_EXCLUSIONS


def has_single_sound_boundary(term: str) -> bool:
    """1.1.21 ādyantavad ekasmin: a single sound is treated as both beginning and end."""
    return len(tokenize_sounds(term)) == 1


def is_gha_suffix(suffix: str) -> bool:
    """1.1.22 taraptamapau ghaḥ."""
    return suffix in GHA_SUFFIXES


def is_sankhya_term(term: str) -> bool:
    """1.1.23 bahugaṇavatuḍati saṃkhyā."""
    return term in SANKHYA_TERMS


def is_shat_numeral(term: str) -> bool:
    """1.1.24 ṣṇāntā ṣaṭ, with 1.1.25 ḍati ca handled by the controlled term set."""
    return term in SHAT_NUMERALS or term == "ḍati"


def is_nistha_suffix(suffix: str) -> bool:
    """1.1.26 ktaktavatū niṣṭhā."""
    return suffix in NISTHA_SUFFIXES


def is_sarvanama_stem(stem: str) -> bool:
    """1.1.27 sarvādīni sarvanāmāni."""
    return stem in SARVANAMA_STEMS


def assign_technical_names(analysis: Analysis, suffix_surface: str | None = None) -> Analysis:
    """
    Partial saṃjñā scaffold for selected 1.4 rules.

    1.4.1: ā kaḍārād ekā saṃjñā
    1.4.2: vipratiṣedhe paraṃ kāryam
    """
    samjnas = set(analysis.samjnas)
    lemma = analysis.lemma
    sounds = tokenize_sounds(lemma)
    if not sounds:
        return analysis

    last_sound = sounds[-1]

    # 1.4.3: yūstryākhyau nadī
    if analysis.gender == Gender.FEMININE:
        if last_sound in {"ī", "ū"}:
            samjnas.add(Samjna.NADII)

    # 1.4.7: śeṣo ghyasakhi
    if last_sound in {"i", "u"} and lemma != "sakhi":
        if Samjna.NADII not in samjnas:
            samjnas.add(Samjna.GHI)

    # 1.4.13: yasmāt pratyayavidhis-tadādi pratyaye'ṅgam
    # If there is a suffix, the preceding part is an aṅga.
    if suffix_surface is not None:
        samjnas.add(Samjna.ANGA)

    # 1.4.14: suptiṅantaṃ padam
    if is_pada(analysis):
        # 1.4.17: svādiṣvasarvanāmasthāne (pada before certain suffixes)
        # 1.4.18: yaci bham (bha before suffixes starting with y or ac)
        if suffix_surface:
             s_sounds = tokenize_sounds(suffix_surface)
             if s_sounds and (s_sounds[0] == "y" or is_vowel(s_sounds[0])):
                  samjnas.add(Samjna.BHA)
             else:
                  samjnas.add(Samjna.PADA)
        else:
             samjnas.add(Samjna.PADA)

    return Analysis(**{**analysis.__dict__, "samjnas": frozenset(samjnas)})

def is_samhita(word: str) -> bool:
    """
    1.4.109: paraḥ sannikarṣaḥ saṃhitā
    Close proximity of sounds is samhita.
    """
    return bool(tokenize_sounds(word))

def is_avasana(word: str, index: int) -> bool:
    """
    1.4.110: virāmo'vasānam
    Cessation of sound is avasana.
    """
    sounds = tokenize_sounds(word)
    return index >= len(sounds)

def is_pada(analysis: Analysis) -> bool:
    """
    1.4.14: suptiṅantaṃ padam
    A term ending in a sup or tiṅ suffix is a pada.
    In our Analysis, if it has a case (sup) or lakara/person (tiṅ), it's a pada.
    """
    if analysis.pos == PartOfSpeech.NOUN and analysis.case is not None:
        return True
    if analysis.pos == PartOfSpeech.VERB and (analysis.person is not None or analysis.lakara is not None):
        return True
    if analysis.pos == PartOfSpeech.PRONOUN and analysis.case is not None:
        return True
    if analysis.pos == PartOfSpeech.INDECLINABLE:
        # Avyayas are padas (their sup suffixes are elided by luk)
        return True
    return False

def get_vowel_weight(word: str, vowel_index: int) -> Samjna:
    """
    Determines if a vowel in a word is laghu (light) or guru (heavy).
    1.4.10 - 1.4.12
    """
    sounds = tokenize_sounds(word)
    if vowel_index >= len(sounds):
        return None

    vowel = sounds[vowel_index]
    if not is_vowel(vowel):
        return None

    sound_obj = SOUNDS.get(vowel)

    # 1.4.11: saṃyoge guru (followed by conjunct)
    if vowel_index + 2 < len(sounds):
        if is_consonant(sounds[vowel_index+1]) and is_consonant(sounds[vowel_index+2]):
            return Samjna.GURU

    # 1.4.12: dīrghaṃ ca
    if sound_obj and sound_obj.length in {VowelLength.LONG, VowelLength.DIPHTHONG}:
        return Samjna.GURU

    # 1.4.10: hrasvaṃ laghu
    return Samjna.LAGHU
