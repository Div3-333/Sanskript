from __future__ import annotations

import re
import unicodedata


TOKEN_RE = re.compile(r"[\w\u0900-\u097fāīūṛṝḷḹṅñṭḍṇśṣṃḥĀĪŪṚṜḶḸṄÑṬḌṆŚṢṂḤ]+", re.UNICODE)


def normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text)
    normalized = normalized.replace("ṁ", "ṃ").replace("Ṁ", "Ṃ")
    normalized = normalized.replace("।", ".")
    return normalized


def split_sentences(text: str) -> list[str]:
    normalized = normalize(text)
    return [part.strip() for part in re.split(r"[.?]+", normalized) if part.strip()]


def tokenize(sentence: str, *, normalize_token) -> list[str]:
    return [normalize_token(match.group(0)) for match in TOKEN_RE.finditer(normalize(sentence))]


__all__ = ["normalize", "split_sentences", "tokenize", "TOKEN_RE"]
