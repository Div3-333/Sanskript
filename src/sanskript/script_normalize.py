"""Normalize accepted Sanskrit scripts to canonical IAST for compilation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from .morphology_text import normalize as normalize_unicode
from .transliteration import devanagari_to_iast, iast_to_devanagari


class Script(str, Enum):
    IAST = "iast"
    DEVANAGARI = "devanagari"
    SLP1 = "slp1"
    HARVARD_KYOTO = "harvard_kyoto"
    MIXED = "mixed"
    UNKNOWN = "unknown"


# Harvard-Kyoto: longest keys first (ASCII letters only in source).
_HK_MULTI = (
    ("ai", "ai"),
    ("au", "au"),
    ("aa", "ā"),
    ("ii", "ī"),
    ("uu", "ū"),
    ("R^i", "ṛ"),
    ("R^I", "ṝ"),
    ("L^i", "ḷ"),
    ("kh", "kh"),
    ("gh", "gh"),
    ("ch", "ch"),
    ("jh", "jh"),
    ("Th", "ṭh"),
    ("Dh", "ḍh"),
    ("th", "th"),
    ("dh", "dh"),
    ("ph", "ph"),
    ("bh", "bh"),
    ("~n", "ñ"),
    ("~N", "ṅ"),
    ("~m", "ṃ"),
    ("~h", "ḥ"),
    ("Sh", "ṣ"),
)
_HK_MULTI_KEYS = {k: v for k, v in _HK_MULTI}
_HK_SINGLE = {
    "a": "a",
    "A": "ā",
    "i": "i",
    "I": "ī",
    "u": "u",
    "U": "ū",
    "R": "ṛ",
    "L": "ḷ",
    "e": "e",
    "o": "o",
    "k": "k",
    "g": "g",
    "c": "c",
    "j": "j",
    "T": "ṭ",
    "D": "ḍ",
    "N": "ṇ",
    "t": "t",
    "d": "d",
    "n": "n",
    "p": "p",
    "b": "b",
    "m": "m",
    "y": "y",
    "r": "r",
    "l": "l",
    "v": "v",
    "w": "v",
    "S": "ś",
    "s": "s",
    "h": "h",
    "M": "ṃ",
    "H": "ḥ",
}

# SLP1: period-prefixed specials; capitals for length/retroflex.
_SLP1_MULTI = (
    (".ai", "ai"),
    (".au", "au"),
    (".aa", "ā"),
    (".ii", "ī"),
    (".uu", "ū"),
    (".r", "ṛ"),
    (".l", "ḷ"),
    (".m", "ṃ"),
    (".h", "ḥ"),
    (".n", "ṇ"),
    (".t", "ṭ"),
    (".d", "ḍ"),
    (".s", "ṣ"),
    ("kh", "kh"),
    ("gh", "gh"),
    ("ch", "ch"),
    ("jh", "jh"),
    ("th", "th"),
    ("dh", "dh"),
    ("ph", "ph"),
    ("bh", "bh"),
)
_SLP1_SINGLE = {
    "a": "a",
    "A": "ā",
    "i": "i",
    "I": "ī",
    "u": "u",
    "U": "ū",
    "r": "r",
    "R": "ṛ",
    "e": "e",
    "o": "o",
    "k": "k",
    "g": "g",
    "c": "c",
    "j": "j",
    "t": "t",
    "d": "d",
    "n": "n",
    "p": "p",
    "b": "b",
    "m": "m",
    "y": "y",
    "w": "v",
    "v": "v",
    "h": "h",
    "z": "ś",
    "S": "ṣ",
    "M": "ṃ",
    "H": "ḥ",
    "G": "ṅ",
    "J": "ñ",
    "T": "ṭ",
    "D": "ḍ",
    "N": "ṇ",
}


@dataclass(frozen=True)
class NormalizedSource:
    """Prepared source for the parser pipeline."""

    text: str
    original: str
    script: Script
    offset_map: tuple[tuple[int, int], ...] = ()

    def slice_original(self, start: int, end: int) -> str:
        if not self.offset_map:
            return self.original[start:end]
        parts: list[str] = []
        for norm_start, norm_end in self.offset_map:
            if norm_end <= start or norm_start >= end:
                continue
            overlap_start = max(start, norm_start)
            overlap_end = min(end, norm_end)
            orig_start = self._norm_to_orig(overlap_start)
            orig_end = self._norm_to_orig(overlap_end)
            parts.append(self.original[orig_start:orig_end])
        return "".join(parts) if parts else self.original[start:end]

    def _norm_to_orig(self, index: int) -> int:
        if index <= 0:
            return 0
        if index >= len(self.text):
            return len(self.original)
        for norm_i, orig_i in self.offset_map:
            if norm_i == index:
                return orig_i
        return self.offset_map[-1][1] if self.offset_map else index


def detect_script(text: str) -> Script:
    has_dev = any("\u0900" <= ch <= "\u097f" for ch in text)
    has_iast = bool(re.search(r"[āīūṛṝḷḹṅñṭḍṇśṣṃḥ]", text))
    has_hk = bool(re.search(r"[TDN]|~[nmhN]|R\^", text))
    has_slp1 = "." in text and bool(re.search(r"\.[ntdsmh]", text))
    flags = sum((has_dev, has_iast, has_hk, has_slp1))
    if flags > 1:
        return Script.MIXED
    if has_dev:
        return Script.DEVANAGARI
    if has_slp1 and not has_iast:
        return Script.SLP1
    if has_hk and not has_iast:
        return Script.HARVARD_KYOTO
    if has_iast or re.search(r"[a-zA-Z]", text):
        return Script.IAST
    return Script.UNKNOWN


def harvard_kyoto_to_iast(text: str) -> str:
    output: list[str] = []
    index = 0
    keys = sorted(set(_HK_MULTI_KEYS) | set(_HK_SINGLE), key=len, reverse=True)
    while index < len(text):
        if not text[index].isalpha() and text[index] not in "~^":
            output.append(text[index])
            index += 1
            continue
        matched = False
        for key in keys:
            if text.startswith(key, index):
                replacement = _HK_MULTI_KEYS.get(key) or _HK_SINGLE.get(key)
                if replacement:
                    output.append(replacement)
                    index += len(key)
                    matched = True
                    break
        if not matched:
            output.append(text[index])
            index += 1
    return "".join(output)


def slp1_to_iast(text: str) -> str:
    output: list[str] = []
    index = 0
    keys = sorted({k for k, _ in _SLP1_MULTI} | set(_SLP1_SINGLE), key=len, reverse=True)
    while index < len(text):
        ch = text[index]
        if not (ch.isalpha() or ch == "."):
            output.append(ch)
            index += 1
            continue
        matched = False
        for key in keys:
            if text.startswith(key, index):
                replacement = dict(_SLP1_MULTI).get(key) or _SLP1_SINGLE.get(key)
                if replacement:
                    output.append(replacement)
                    index += len(key)
                    matched = True
                    break
        if not matched:
            output.append(ch)
            index += 1
    return "".join(output)


def iast_to_harvard_kyoto(text: str) -> str:
    pairs = (
        ("ai", "ai"),
        ("au", "au"),
        ("ā", "A"),
        ("ī", "I"),
        ("ū", "U"),
        ("ṛ", "R"),
        ("ṝ", "R"),
        ("ḷ", "L"),
        ("ṃ", "M"),
        ("ḥ", "H"),
        ("kh", "kh"),
        ("gh", "gh"),
        ("ch", "ch"),
        ("jh", "jh"),
        ("ṭh", "Th"),
        ("ḍh", "Dh"),
        ("th", "th"),
        ("dh", "dh"),
        ("ph", "ph"),
        ("bh", "bh"),
        ("ñ", "~n"),
        ("ṅ", "~N"),
        ("ṭ", "T"),
        ("ḍ", "D"),
        ("ṇ", "N"),
        ("ś", "S"),
        ("ṣ", "Sh"),
    )
    out: list[str] = []
    index = 0
    keys = sorted((k for k, _ in pairs), key=len, reverse=True)
    mapping = dict(pairs)
    while index < len(text):
        matched = False
        for key in keys:
            if text.startswith(key, index):
                out.append(mapping[key])
                index += len(key)
                matched = True
                break
        if not matched:
            out.append(text[index])
            index += 1
    return "".join(out)


def iast_to_slp1(text: str) -> str:
    pairs = (
        ("ai", ".ai"),
        ("au", ".au"),
        ("ā", "A"),
        ("ī", "I"),
        ("ū", "U"),
        ("ṛ", ".r"),
        ("ḷ", ".l"),
        ("ṃ", ".m"),
        ("ḥ", ".h"),
        ("kh", "kh"),
        ("gh", "gh"),
        ("ch", "ch"),
        ("jh", "jh"),
        ("ṭh", "th"),
        ("ḍh", "dh"),
        ("ph", "ph"),
        ("bh", "bh"),
        ("ñ", "J"),
        ("ṅ", "G"),
        ("ṭ", "T"),
        ("ḍ", "D"),
        ("ṇ", ".n"),
        ("ś", "z"),
        ("ṣ", "S"),
    )
    out: list[str] = []
    index = 0
    keys = sorted((k for k, _ in pairs), key=len, reverse=True)
    mapping = dict(pairs)
    while index < len(text):
        matched = False
        for key in keys:
            if text.startswith(key, index):
                out.append(mapping[key])
                index += len(key)
                matched = True
                break
        if not matched:
            out.append(text[index])
            index += 1
    return "".join(out)


def transliterate_for_diagnostics(text: str, *, target: Script) -> str:
    """Reversible transliteration helpers for error messages and tooling."""
    script = detect_script(text)
    iast = normalize_to_iast(text, script=script).text
    if target == Script.DEVANAGARI:
        return iast_to_devanagari(iast)
    if target == Script.HARVARD_KYOTO:
        return iast_to_harvard_kyoto(iast)
    if target == Script.SLP1:
        return iast_to_slp1(iast)
    return iast


def normalize_to_iast(text: str, *, script: Script | None = None) -> NormalizedSource:
    detected = script or detect_script(text)
    normalized_input = normalize_unicode(text)
    mapping: list[tuple[int, int]] = []
    if detected == Script.DEVANAGARI:
        canonical = devanagari_to_iast(normalized_input)
        for index, _ in enumerate(canonical):
            mapping.append((index, min(index, len(normalized_input) - 1)))
    elif detected == Script.HARVARD_KYOTO:
        canonical = harvard_kyoto_to_iast(normalized_input)
    elif detected == Script.SLP1:
        canonical = slp1_to_iast(normalized_input)
    else:
        canonical = normalized_input
    canonical = normalize_unicode(canonical)
    return NormalizedSource(
        text=canonical,
        original=normalized_input,
        script=detected,
        offset_map=tuple(mapping),
    )


__all__ = [
    "NormalizedSource",
    "Script",
    "detect_script",
    "harvard_kyoto_to_iast",
    "iast_to_harvard_kyoto",
    "iast_to_slp1",
    "normalize_to_iast",
    "slp1_to_iast",
    "transliterate_for_diagnostics",
]
