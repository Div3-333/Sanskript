class SanskriptError(Exception):
    """Base class for user-facing Sanskript errors."""


class MorphologyError(SanskriptError):
    """Raised when a word cannot be analyzed in the controlled subset."""


class ParseError(SanskriptError):
    """Raised when analyzed words do not satisfy a verb frame."""


class RuntimeSanskriptError(SanskriptError):
    """Raised when a grammatical program fails during execution."""

