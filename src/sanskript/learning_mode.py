"""Relaxed learning mode: suggestions without changing canonical compilation."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

from .errors import MorphologyError, ParseError, SanskriptError
from .script_normalize import Script, transliterate_for_diagnostics

_SHIKSHA_DIRECTIVE = re.compile(
    r"^\s*(?:śikṣām|shiksham|shikṣām)\s*\.?\s*$",
    re.IGNORECASE | re.MULTILINE,
)


@dataclass
class LearningSettings:
    enabled: bool = False
    suggestions: bool = True
    notes: list[str] = field(default_factory=list)

    def strip_directives(self, text: str) -> str:
        return _SHIKSHA_DIRECTIVE.sub(" ", text)


def parse_learning_directive(source: str) -> LearningSettings:
    if _SHIKSHA_DIRECTIVE.search(source):
        return LearningSettings(enabled=True, suggestions=True)
    return LearningSettings()


def learning_mode_from_env() -> bool:
    return os.environ.get("SANSKRIPT_LEARNING", "").strip().lower() in {"1", "true", "yes"}


def enrich_error(error: SanskriptError, *, original: str, script: Script) -> SanskriptError:
    """Attach learning suggestions to an error without altering strict behavior."""
    if not isinstance(error, (MorphologyError, ParseError)):
        return error
    settings = parse_learning_directive(original)
    if not settings.enabled and not learning_mode_from_env():
        return error
    suggestions = suggest_for_error(error, original=original, script=script)
    if not suggestions:
        return error
    hint = error.hint or ""
    extra = " ".join(suggestions)
    error.hint = f"{hint} {extra}".strip() if hint else extra
    return error


def suggest_for_error(
    error: SanskriptError,
    *,
    original: str,
    script: Script,
) -> list[str]:
    suggestions: list[str] = []
    if isinstance(error, MorphologyError):
        suggestions.append(
            "Check spelling in the controlled register or add the form to the grammar register."
        )
        if script != Script.IAST:
            iast = transliterate_for_diagnostics(original, target=Script.IAST)
            suggestions.append(f"Canonical IAST for this region: {iast!r}.")
    if isinstance(error, ParseError) and "participant role" in error.message.lower():
        suggestions.append("Try an explicit case role (karma, karaṇa, adhikaraṇa) matching the verb frame.")
    if isinstance(error, ParseError) and "finite verb" in error.message.lower():
        suggestions.append("Each vākya should contain exactly one main verb form.")
    return suggestions


__all__ = [
    "LearningSettings",
    "enrich_error",
    "learning_mode_from_env",
    "parse_learning_directive",
    "suggest_for_error",
]
