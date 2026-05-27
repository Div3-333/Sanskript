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
        span: SourceSpan | None = None,
        original_script: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint
        self.code = code or self.code
        self.span = span
        self.original_script = original_script

    def __str__(self) -> str:
        text = self.message
        if self.span is not None:
            text = f"{text} (at {self.span})"
        if self.original_script:
            text = f"{text} [script={self.original_script}]"
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


class CompileError(SanskriptError):
    """Raised when a program cannot be compiled due to a semantic error."""

    code = "SANSKRIPT_COMPILE"


class TypeCheckError(SanskriptError):
    """Raised when static type validation fails before compilation."""

    code = "SANSKRIPT_TYPE"


class PanicError(SanskriptError):
    """Raised by vipattim — unrecoverable, cannot be caught by āgrahītvā."""

    code = "SANSKRIPT_PANIC"


class ThrownError(SanskriptError):
    """Raised by vikṣepaḥ — catchable by āgrahītvā."""

    code = "SANSKRIPT_THROW"
