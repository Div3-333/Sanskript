from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .source_context import SourceSpan


class SanskriptError(Exception):
    """Base class for user-facing Sanskript errors."""

    code = "SANSKRIPT_ERROR"

    def __init__(
        self,
        message: str,
        *,
        hint: str | None = None,
        code: str | None = None,
        category: str | None = None,
        recoverable: bool | None = None,
        span: SourceSpan | None = None,
        original_script: str | None = None,
        stack_trace: tuple[str, ...] = (),
        notes: tuple[str, ...] = (),
        suggestions: tuple[str, ...] = (),
        fixes: tuple[str, ...] = (),
    ) -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint
        self.code = code or self.code
        self.category = category or "error"
        self.recoverable = bool(recoverable) if recoverable is not None else True
        self.span = span
        self.original_script = original_script
        self.stack_trace = stack_trace
        self.notes = notes
        # `fixes` is the canonical remediation field; `suggestions` stays as a
        # compatibility alias for existing callers.
        merged_fixes: tuple[str, ...] = fixes or suggestions
        self.fixes = merged_fixes
        self.suggestions = merged_fixes

    def with_context(
        self,
        *,
        span: SourceSpan | None = None,
        original_script: str | None = None,
        stack_trace: tuple[str, ...] | None = None,
        notes: tuple[str, ...] | None = None,
        suggestions: tuple[str, ...] | None = None,
        fixes: tuple[str, ...] | None = None,
    ) -> "SanskriptError":
        if span is not None and self.span is None:
            self.span = span
        if original_script is not None and self.original_script is None:
            self.original_script = original_script
        if stack_trace is not None:
            self.stack_trace = stack_trace
        if notes is not None:
            self.notes = notes
        if suggestions is not None:
            self.suggestions = suggestions
            self.fixes = suggestions
        if fixes is not None:
            self.fixes = fixes
            self.suggestions = fixes
        return self

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "code": self.code,
            "message": self.message,
            "category": self.category,
            "recoverable": self.recoverable,
            "notes": list(self.notes),
            "stack_trace": list(self.stack_trace),
            "fixes": list(self.fixes),
            "suggestions": list(self.suggestions),
        }
        if self.hint:
            payload["hint"] = self.hint
        if self.original_script:
            payload["script"] = self.original_script
        if self.span is not None:
            payload["span"] = {
                "start": self.span.start,
                "end": self.span.end,
                "line": self.span.line,
                "column": self.span.column,
                "snippet": self.span.snippet,
            }
        return payload

    def __str__(self) -> str:
        text = self.message
        if self.span is not None:
            text = f"{text} (at {self.span})"
        if self.original_script:
            text = f"{text} [script={self.original_script}]"
        if self.notes:
            text = f"{text} Notes: {' | '.join(self.notes)}"
        if self.stack_trace:
            text = f"{text} Stack: {' -> '.join(self.stack_trace)}"
        if self.hint:
            text = f"{text} Hint: {self.hint}"
        return f"{text} [{self.code}]"


class MorphologyError(SanskriptError):
    """Raised when a word cannot be analyzed in the controlled subset."""

    code = "SANSKRIPT_MORPHOLOGY"


class ParseError(SanskriptError):
    """Raised when analyzed words do not satisfy a verb frame."""

    code = "SANSKRIPT_PARSE"


class CompileError(SanskriptError):
    """Raised when a program fails static checks before bytecode emission."""

    code = "SANSKRIPT_COMPILE"


class RuntimeSanskriptError(SanskriptError):
    """Raised when a grammatical program fails during execution."""

    code = "SANSKRIPT_RUNTIME"


class TypeCheckError(SanskriptError):
    """Raised when static type validation fails before compilation."""

    code = "SANSKRIPT_TYPE"


class PanicError(SanskriptError):
    """Raised by vipattim — unrecoverable, cannot be caught by āgrahītvā."""

    code = "SANSKRIPT_PANIC"

    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(message, recoverable=False, category="panic", **kwargs)


class ThrownError(SanskriptError):
    """Raised by vikṣepaḥ — catchable by āgrahītvā."""

    code = "SANSKRIPT_THROW"

    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(message, recoverable=True, category="throw", **kwargs)
