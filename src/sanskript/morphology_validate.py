"""Validate synthesized Sanskrit surfaces before they enter the lexicon."""

from __future__ import annotations

import re
import unicodedata

from .errors import MorphologyError


# Practical IAST letters used in the controlled register (plus digits not allowed).
_IAST_CHARS = frozenset(
    "abcdefghijklmnopqrstuvwxyz"
    "āīūṛṝḷḹēōṃḥ"
    "ṅñṭḍṇśṣ"
    "ĀĪŪṚṜḶḸĒŌṂḤ"
    "ṬḌṆŚṢ"
)

MAX_SURFACE_LENGTH = 48
MIN_SURFACE_LENGTH = 1


def normalize_surface(surface: str) -> str:
    return unicodedata.normalize("NFC", surface.strip())


def validate_surface(
    surface: str,
    *,
    expected: str | None = None,
    register_id: str = "",
) -> str:
    """Return normalized surface or raise MorphologyError for garbage/invalid forms."""
    text = normalize_surface(surface)
    label = register_id or surface

    if expected is not None and text != expected:
        raise MorphologyError(
            f"Synthesis for {label!r} expected surface {expected!r}, got {text!r}"
        )

    if not (MIN_SURFACE_LENGTH <= len(text) <= MAX_SURFACE_LENGTH):
        raise MorphologyError(
            f"Surface {text!r} for {label!r} has invalid length {len(text)} "
            f"(allowed {MIN_SURFACE_LENGTH}..{MAX_SURFACE_LENGTH})"
        )

    if not all(ch in _IAST_CHARS for ch in text):
        bad = sorted({ch for ch in text if ch not in _IAST_CHARS})
        raise MorphologyError(
            f"Surface {text!r} for {label!r} contains non-IAST characters: {bad!r}"
        )

    if _has_runaway_repetition(text):
        raise MorphologyError(
            f"Surface {text!r} for {label!r} looks like runaway derivation (repeated chunks)"
        )

    if re.search(r"(.)\1{5,}", text):
        raise MorphologyError(
            f"Surface {text!r} for {label!r} has excessive character repetition"
        )

    return text


def _has_runaway_repetition(text: str) -> bool:
    length = len(text)
    for size in range(3, min(9, length // 3 + 1)):
        for start in range(0, length - size * 3 + 1):
            chunk = text[start : start + size]
            if not chunk.strip("aāiīuū"):
                continue
            repeats = 1
            index = start + size
            while text[index : index + size] == chunk:
                repeats += 1
                index += size
                if repeats >= 3:
                    return True
    return False


__all__ = ["MAX_SURFACE_LENGTH", "normalize_surface", "validate_surface"]
