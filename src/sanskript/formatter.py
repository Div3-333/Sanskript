"""Canonical Sanskript source formatter (layout is not semantic)."""

from __future__ import annotations

import re

from .comments import strip_comments
from .morphology_text import normalize, split_sentences
from .script_normalize import normalize_to_iast


def format_source(source: str, *, script: str = "iast") -> str:
    """Format to one sentence per line with normalized whitespace."""
    stripped = strip_comments(source).text
    canonical = normalize_to_iast(stripped).text
    sentences = split_sentences(canonical)
    lines: list[str] = []
    for sentence in sentences:
        line = _format_sentence(sentence)
        if line:
            lines.append(line)
    body = "\n".join(lines)
    if body and not body.endswith("\n"):
        body += "\n"
    return body


def _format_sentence(sentence: str) -> str:
    text = normalize(sentence)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ""
    if not text.endswith(".") and not text.endswith("।"):
        text += "."
    return text


__all__ = ["format_source"]
