"""Source spans and token provenance for Sanskrit diagnostics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceSpan:
    """Half-open byte offset range in the prepared (comment-stripped) source."""

    start: int
    end: int
    line: int = 1
    column: int = 1
    snippet: str = ""

    def __str__(self) -> str:
        if self.line:
            return f"line {self.line}, column {self.column}"
        return f"bytes {self.start}..{self.end}"


@dataclass(frozen=True)
class TokenProvenance:
    """Maps a normalized compile token back to user-facing text."""

    token: str
    span: SourceSpan
    original: str
    script: str = "iast"

    def display_token(self) -> str:
        return self.original or self.token


def span_at(text: str, start: int, end: int) -> SourceSpan:
    line = text.count("\n", 0, start) + 1
    line_start = text.rfind("\n", 0, start) + 1
    column = start - line_start + 1
    return SourceSpan(start=start, end=end, line=line, column=column, snippet=text[start:end])


__all__ = ["SourceSpan", "TokenProvenance", "span_at"]
