from __future__ import annotations

import re
import unicodedata


TOKEN_RE = re.compile(r"[\w\u0900-\u097fāīūṛṝḷḹṅñṭḍṇśṣṃḥĀĪŪṚṜḶḸṄÑṬḌṆŚṢṂḤ]+", re.UNICODE)


def normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text)
    normalized = normalized.replace("ṁ", "ṃ").replace("Ṁ", "Ṃ")
    normalized = normalized.replace("।", ".")
    return normalized


_PATH_DOT = "\uE000"


def split_sentences(text: str) -> list[str]:
    normalized = normalize(text)
    protected = re.sub(r"(?<=\s)\./", f" {_PATH_DOT}/", normalized)
    protected = re.sub(r"(?<=\s)\.\./", f" {_PATH_DOT}{_PATH_DOT}/", protected)
    parts = re.split(r"[.?]+", protected)
    return [
        part.strip().replace(_PATH_DOT, ".")
        for part in parts
        if part.strip()
    ]


def tokenize(sentence: str, *, normalize_token) -> list[str]:
    return [normalize_token(match.group(0)) for match in TOKEN_RE.finditer(normalize(sentence))]


__all__ = ["normalize", "split_sentences", "tokenize", "TOKEN_RE"]
