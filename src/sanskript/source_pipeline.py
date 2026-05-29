"""Prepare raw Sanskript source for parsing (comments, scripts, modes)."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from functools import lru_cache

from .comments import strip_comments
from .learning_mode import LearningSettings, parse_learning_directive
from .morphology_text import TOKEN_RE
from .sandhi import split_joined_token_chain
from .script_normalize import NormalizedSource, Script, normalize_to_iast

_STRICT_DIRECTIVE = re.compile(
    r"^\s*(?:paninianam|pāṇinianam|paaninianam)\s*\.?\s*$",
    re.IGNORECASE | re.MULTILINE,
)
_SANDHI_STRICT = re.compile(
    r"^\s*(?:sandhīnam|sandhinam)\s*\.?\s*$",
    re.IGNORECASE | re.MULTILINE,
)


@dataclass(frozen=True)
class PreparedSource:
    text: str
    original: str
    normalized: NormalizedSource
    learning: LearningSettings
    strict_paninian: bool
    strict_sandhi: bool


def prepare_source(source: str) -> PreparedSource:
    stripped = strip_comments(source)
    learning = parse_learning_directive(stripped.text)
    if os.environ.get("SANSKRIPT_LEARNING", "").strip().lower() in {"1", "true", "yes"}:
        learning = LearningSettings(enabled=True, suggestions=True)

    body = learning.strip_directives(stripped.text)
    strict_paninian = bool(_STRICT_DIRECTIVE.search(body)) or os.environ.get(
        "SANSKRIPT_STRICT", ""
    ).strip().lower() in {"1", "true", "yes"}
    strict_sandhi = bool(_SANDHI_STRICT.search(body)) or strict_paninian
    body = _STRICT_DIRECTIVE.sub(" ", body)
    body = _SANDHI_STRICT.sub(" ", body)

    normalized = normalize_to_iast(body)
    if strict_sandhi:
        normalized = NormalizedSource(
            text=_apply_sandhi_segmentation(normalized.text),
            original=normalized.original,
            script=normalized.script,
            offset_map=normalized.offset_map,
        )

    return PreparedSource(
        text=normalized.text,
        original=stripped.text,
        normalized=normalized,
        learning=learning,
        strict_paninian=strict_paninian,
        strict_sandhi=strict_sandhi,
    )


def _apply_sandhi_segmentation(text: str) -> str:
    """Split over-joined tokens when sandhi boundaries are recoverable."""
    lines_out: list[str] = []
    for line in text.splitlines():
        if not line.strip():
            lines_out.append(line)
            continue
        parts: list[str] = []
        last = 0
        for match in TOKEN_RE.finditer(line):
            parts.append(line[last : match.start()])
            parts.append(_split_token_at_sandhi(match.group(0)))
            last = match.end()
        parts.append(line[last:])
        lines_out.append("".join(parts))
    return "\n".join(lines_out)


def _split_token_at_sandhi(token: str) -> str:
    if len(token) < 6 or " " in token:
        return token
    if _is_registered_surface(token):
        return token
    segmented = split_joined_token_chain(token, part_validator=_is_registered_surface)
    if len(segmented) <= 1:
        return token
    return " ".join(segmented)


@lru_cache(maxsize=1)
def _strict_sandhi_facade():
    from .morphology_facade import get_default_facade

    return get_default_facade()


def _is_registered_surface(token: str) -> bool:
    facade = _strict_sandhi_facade()
    try:
        facade.analyze_token(token)
    except Exception:
        return False
    return True


__all__ = ["PreparedSource", "prepare_source"]
