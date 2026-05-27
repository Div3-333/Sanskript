"""Strip and record Sanskrit prose comments from source text."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .source_context import SourceSpan, span_at

# Line comments: //, #, or व्याख्या at line start (after optional whitespace).
_LINE_COMMENT = re.compile(
    r"^\s*(?://|#|व्याख्या[:：]?\s*)(.+)$",
    re.MULTILINE,
)
_BLOCK_COMMENT = re.compile(r"\(\*.*?\*\)", re.DOTALL)
_VYAKHYA_INLINE = re.compile(r"व्याख्या[:：]\s*(.+?)(?=\.|।|$)")


@dataclass(frozen=True)
class SourceComment:
    text: str
    span: SourceSpan
    kind: str = "line"


@dataclass(frozen=True)
class StrippedSource:
    text: str
    comments: tuple[SourceComment, ...]


def strip_comments(source: str) -> StrippedSource:
    """Remove comments while preserving executable text and provenance."""
    comments: list[SourceComment] = []
    working = source

    for match in _BLOCK_COMMENT.finditer(working):
        comments.append(
            SourceComment(
                text=match.group(0)[2:-2].strip(),
                span=span_at(source, match.start(), match.end()),
                kind="block",
            )
        )
    working = _BLOCK_COMMENT.sub(" ", working)

    for match in _LINE_COMMENT.finditer(working):
        comments.append(
            SourceComment(
                text=match.group(1).strip(),
                span=span_at(source, match.start(), match.end()),
                kind="line",
            )
        )
    working = _LINE_COMMENT.sub(" ", working)

    for match in _VYAKHYA_INLINE.finditer(working):
        comments.append(
            SourceComment(
                text=match.group(1).strip(),
                span=span_at(source, match.start(), match.end()),
                kind="vyakhya",
            )
        )
    working = _VYAKHYA_INLINE.sub(" ", working)

    # Collapse blank lines introduced by comment removal.
    working = re.sub(r"[ \t]+\n", "\n", working)
    working = re.sub(r"\n{3,}", "\n\n", working)
    return StrippedSource(text=working, comments=tuple(comments))


__all__ = ["SourceComment", "StrippedSource", "strip_comments"]
