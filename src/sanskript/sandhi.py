from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


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


def split_joined_token(token: str) -> tuple[str, str] | None:
    """Recover one sandhi boundary from a joined token.

    The splitter is conservative: it only returns a pair when re-joining through
    ``join_words`` reproduces the exact token and uses a non-identity rule.
    """
    if len(token) < 4 or " " in token:
        return None

    return _split_joined_token_with_validator(token)


def _split_joined_token_with_validator(
    token: str,
    *,
    part_validator: Callable[[str], bool] | None = None,
) -> tuple[str, str] | None:
    candidates: list[tuple[tuple[str, str], str]] = []
    for candidate in _iter_inverse_vowel_candidates(token):
        if len(candidate[0]) < 2 or len(candidate[1]) < 2:
            continue
        joined = join_words(candidate[0], candidate[1])
        if joined.rule != "identity" and joined.value == token:
            candidates.append((candidate, joined.rule))

    for candidate in _iter_inverse_visarga_candidates(token):
        if len(candidate[0]) < 2 or len(candidate[1]) < 2:
            continue
        joined = join_words(candidate[0], candidate[1])
        if joined.rule != "identity" and joined.value == token:
            candidates.append((candidate, joined.rule))

    if not candidates:
        return None
    if part_validator is not None:
        validated = [item for item in candidates if part_validator(item[0][0]) or part_validator(item[0][1])]
        if not validated:
            return None
        candidates = validated
    scored = sorted(
        candidates,
        key=lambda item: _score_split_candidate(
            item[0][0],
            item[0][1],
            rule=item[1],
            part_validator=part_validator,
        ),
        reverse=True,
    )
    return scored[0][0]


def split_joined_token_chain(
    token: str,
    *,
    max_splits: int = 4,
    part_validator: Callable[[str], bool] | None = None,
) -> list[str]:
    """Recover multiple conservative sandhi boundaries from one token.

    Each boundary must be individually valid according to ``split_joined_token``,
    which already guarantees exact reconstruction through ``join_words`` with a
    non-identity sandhi rule.
    """
    if max_splits <= 0:
        return [token]

    parts: list[str] = [token]
    splits = 0
    while splits < max_splits:
        changed = False
        for index, part in enumerate(parts):
            if "ḥ" in part:
                continue
            recovered = _split_joined_token_with_validator(
                part,
                part_validator=part_validator,
            )
            if recovered is None:
                continue
            left, right = recovered
            parts[index:index + 1] = [left, right]
            splits += 1
            changed = True
            break
        if not changed:
            break
    return parts


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


def _iter_inverse_vowel_candidates(token: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    maps = (SAVARNA_DIRGHA, GUNA_SANDHI, VRDDHI_SANDHI, AYAVAYAVA)
    for mapping in maps:
        for (left_vowel, right_vowel), replacement in mapping.items():
            start = 0
            while True:
                index = token.find(replacement, start)
                if index < 0:
                    break
                left = token[:index] + left_vowel
                right = right_vowel + token[index + len(replacement) :]
                pairs.append((left, right))
                start = index + 1
    return pairs


def _iter_inverse_visarga_candidates(token: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []

    for right_vowel, replacement in VISARGA_BEFORE_VOICED.items():
        start = 0
        while True:
            index = token.find(replacement, start)
            if index < 0:
                break
            left = token[:index] + "aḥ"
            right = right_vowel + token[index + len(replacement) :]
            pairs.append((left, right))
            start = index + 1

    for sibilant in ("ś", "ṣ", "s"):
        doubled = sibilant + sibilant
        start = 0
        while True:
            index = token.find(doubled, start)
            if index < 0:
                break
            left = token[:index] + "ḥ"
            right = sibilant + token[index + len(doubled) :]
            pairs.append((left, right))
            start = index + 1

    return pairs


def _score_split_candidate(
    left: str,
    right: str,
    *,
    rule: str,
    part_validator: Callable[[str], bool] | None,
) -> tuple[int, int, int, int]:
    # Prefer boundaries with plausible lexical parts and balanced lengths.
    valid_left = part_validator(left) if part_validator is not None else False
    valid_right = part_validator(right) if part_validator is not None else False
    validity = int(valid_left) + int(valid_right)
    rule_priority = {
        "visarga-vowel": 3,
        "visarga-sibilant": 3,
        "vṛddhi": 2,
        "guṇa": 2,
        "savarṇa-dīrgha": 1,
        "ayavāyāva": 1,
    }.get(rule, 0)
    balance = -abs(len(left) - len(right))
    left_size = len(left)
    return (validity, rule_priority, balance, left_size)


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
