from __future__ import annotations

from dataclasses import dataclass


VOWELS = ("ai", "au", "ā", "ī", "ū", "ṛ", "ṝ", "ḷ", "a", "i", "u", "e", "o")

SAVARNA_DIRGHA = {
    ("a", "a"): "ā",
    ("a", "ā"): "ā",
    ("ā", "a"): "ā",
    ("ā", "ā"): "ā",
    ("i", "i"): "ī",
    ("i", "ī"): "ī",
    ("ī", "i"): "ī",
    ("ī", "ī"): "ī",
    ("u", "u"): "ū",
    ("u", "ū"): "ū",
    ("ū", "u"): "ū",
    ("ū", "ū"): "ū",
    ("ṛ", "ṛ"): "ṝ",
    ("ṛ", "ṝ"): "ṝ",
    ("ṝ", "ṛ"): "ṝ",
}

GUNA_SANDHI = {
    ("a", "i"): "e",
    ("a", "ī"): "e",
    ("ā", "i"): "e",
    ("ā", "ī"): "e",
    ("a", "u"): "o",
    ("a", "ū"): "o",
    ("ā", "u"): "o",
    ("ā", "ū"): "o",
    ("a", "ṛ"): "ar",
    ("ā", "ṛ"): "ar",
}

VRDDHI_SANDHI = {
    ("a", "e"): "ai",
    ("a", "ai"): "ai",
    ("ā", "e"): "ai",
    ("ā", "ai"): "ai",
    ("a", "o"): "au",
    ("a", "au"): "au",
    ("ā", "o"): "au",
    ("ā", "au"): "au",
}

AYAVAYAVA = {
    ("e", "a"): "aya",
    ("e", "i"): "ayi",
    ("e", "u"): "ayu",
    ("o", "a"): "ava",
    ("o", "i"): "avi",
    ("o", "u"): "avu",
    ("ai", "a"): "āya",
    ("au", "a"): "āva",
}

VISARGA_BEFORE_VOICED = {"a": "o", "ā": "ā", "i": "i", "ī": "ī", "u": "u", "ū": "ū"}


@dataclass(frozen=True)
class SandhiResult:
    value: str
    rule: str


def join_words(left: str, right: str) -> SandhiResult:
    if not left or not right:
        return SandhiResult(left + right, "identity")

    if left.endswith("ḥ"):
        result = apply_visarga_sandhi(left, right)
        if result.rule != "identity":
            return result

    left_vowel = final_vowel(left)
    right_vowel = initial_vowel(right)
    if left_vowel and right_vowel:
        return apply_vowel_sandhi(left, right, left_vowel, right_vowel)

    return SandhiResult(f"{left} {right}", "identity")


def join_sentence(words: list[str]) -> list[SandhiResult]:
    if not words:
        return []
    results: list[SandhiResult] = []
    current = words[0]
    for word in words[1:]:
        result = join_words(current, word)
        results.append(result)
        current = result.value
    return results


def apply_vowel_sandhi(left: str, right: str, left_vowel: str, right_vowel: str) -> SandhiResult:
    pair = (left_vowel, right_vowel)
    replacement = SAVARNA_DIRGHA.get(pair)
    rule = "savarṇa-dīrgha"
    if replacement is None:
        replacement = GUNA_SANDHI.get(pair)
        rule = "guṇa"
    if replacement is None:
        replacement = VRDDHI_SANDHI.get(pair)
        rule = "vṛddhi"
    if replacement is None:
        replacement = AYAVAYAVA.get(pair)
        rule = "ayavāyāva"

    if replacement is None:
        return SandhiResult(f"{left} {right}", "identity")

    return SandhiResult(
        left[: -len(left_vowel)] + replacement + right[len(right_vowel) :],
        rule,
    )


def apply_visarga_sandhi(left: str, right: str) -> SandhiResult:
    right_vowel = initial_vowel(right)
    if left.endswith("aḥ") and right_vowel:
        replacement = VISARGA_BEFORE_VOICED.get(right_vowel)
        if replacement:
            return SandhiResult(left[:-2] + replacement + right[len(right_vowel) :], "visarga-vowel")

    if left.endswith("ḥ") and right and right[0] in {"ś", "ṣ", "s"}:
        return SandhiResult(left[:-1] + right[0] + right, "visarga-sibilant")

    return SandhiResult(f"{left} {right}", "identity")


def final_vowel(word: str) -> str | None:
    for vowel in VOWELS:
        if word.endswith(vowel):
            return vowel
    return None


def initial_vowel(word: str) -> str | None:
    for vowel in VOWELS:
        if word.startswith(vowel):
            return vowel
    return None
