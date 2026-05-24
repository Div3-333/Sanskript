class SanskriptError(Exception):
    """Base class for user-facing Sanskript errors."""

    code = "SANSKRIPT_ERROR"

    def __init__(self, message: str, *, hint: str | None = None, code: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint
        self.code = code or self.code

    def __str__(self) -> str:
        text = self.message
        if self.hint:
            text = f"{text} Hint: {self.hint}"
        return f"{text} [{self.code}]"


class MorphologyError(SanskriptError):
    """Raised when a word cannot be analyzed in the controlled subset."""

    code = "SANSKRIPT_MORPHOLOGY"


class ParseError(SanskriptError):
    """Raised when analyzed words do not satisfy a verb frame."""

    code = "SANSKRIPT_PARSE"


class RuntimeSanskriptError(SanskriptError):
    """Raised when a grammatical program fails during execution."""

    code = "SANSKRIPT_RUNTIME"
