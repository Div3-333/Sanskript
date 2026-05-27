"""Identifier grammar for Sanskript source names.

Identifiers are not avyaya and must not enter the controlled morphology
register just to make examples compile.  This module owns the source-name
surface accepted by parser directives.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import unicodedata

from .grammar import PartOfSpeech


class IdentifierKind(str, Enum):
    MORPHOLOGICAL = "morphological"
    SURFACE = "surface"


class IdentifierError(ValueError):
    """Raised when a source token cannot be used as an identifier."""


@dataclass(frozen=True)
class IdentifierAnalysis:
    surface: str
    canonical: str
    kind: IdentifierKind


_CONNECTORS = frozenset({"_", "-", "."})


def analyze_identifier(token: str, *, facade=None) -> IdentifierAnalysis:
    """Validate and canonicalize one source identifier token.

    Known nominal/pronominal forms reduce to their lemma.  Unknown names are
    accepted only when they follow the explicit source-name grammar:

    - first character: Unicode letter or underscore;
    - later characters: Unicode letters, combining marks, digits, underscore,
      hyphen, or dot;
    - connectors cannot start/end a segment, except underscore-led internal
      names used by compiler-generated destructuring helpers.
    """

    surface = token.strip()
    normalized = _normalize(surface, facade=facade)
    if not normalized:
        raise IdentifierError("identifier is empty")

    if facade is not None:
        try:
            analysis = facade.analyze_token(normalized)
        except Exception:
            analysis = None
        if analysis is not None:
            if analysis.value is not None:
                _validate_surface(surface)
                return IdentifierAnalysis(surface, surface, IdentifierKind.SURFACE)
            if analysis.pos in {PartOfSpeech.NOUN, PartOfSpeech.PRONOUN}:
                return IdentifierAnalysis(normalized, analysis.lemma, IdentifierKind.MORPHOLOGICAL)

    _validate_surface(surface)
    return IdentifierAnalysis(surface, surface, IdentifierKind.SURFACE)


def canonical_identifier(token: str, *, facade=None) -> str:
    return analyze_identifier(token, facade=facade).canonical


def is_identifier(token: str, *, facade=None) -> bool:
    try:
        analyze_identifier(token, facade=facade)
    except IdentifierError:
        return False
    return True


def _normalize(token: str, *, facade=None) -> str:
    if facade is not None:
        return facade.normalize_token(token)
    return token.lower()


def _validate_surface(token: str) -> None:
    if token[0] in {"-", "."} or token[-1] in {"-", "."}:
        raise IdentifierError(f"{token!r} has a dangling identifier connector")
    if token[0].isdigit():
        raise IdentifierError(f"{token!r} starts with a digit")

    previous_connector = False
    for char in token:
        if char in _CONNECTORS:
            if previous_connector and char != "_":
                raise IdentifierError(f"{token!r} has adjacent identifier connectors")
            previous_connector = char != "_"
            continue
        previous_connector = False
        if char.isdigit():
            continue
        category = unicodedata.category(char)
        if char == "_" or char.isalpha() or category in {"Mn", "Mc"}:
            continue
        raise IdentifierError(f"{token!r} contains illegal identifier character {char!r}")
