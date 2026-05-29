from __future__ import annotations

from dataclasses import dataclass

from .errors import SanskriptError
from .linter import LintFinding


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str
    severity: str = "error"
    category: str = "error"
    source: str = "sanskript"
    hint: str | None = None
    recoverable: bool = True
    notes: tuple[str, ...] = ()
    fixes: tuple[str, ...] = ()
    suggestions: tuple[str, ...] = ()
    stack_trace: tuple[str, ...] = ()
    line: int | None = None
    column: int | None = None
    end_line: int | None = None
    end_column: int | None = None
    snippet: str | None = None
    script: str | None = None

    def to_machine_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "source": self.source,
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "category": self.category,
            "recoverable": self.recoverable,
            "notes": list(self.notes),
            "fixes": list(self.fixes),
            "suggestions": list(self.suggestions),
            "stack_trace": list(self.stack_trace),
        }
        if self.hint:
            payload["hint"] = self.hint
        if self.script:
            payload["script"] = self.script
        if self.line is not None and self.column is not None:
            payload["range"] = {
                "start": {"line": self.line, "column": self.column},
                "end": {
                    "line": self.end_line if self.end_line is not None else self.line,
                    "column": self.end_column if self.end_column is not None else self.column,
                },
            }
        if self.snippet:
            payload["snippet"] = self.snippet
        return payload

    def to_ide_dict(self) -> dict[str, object]:
        severity_map = {"error": 1, "warning": 2, "information": 3, "hint": 4}
        line = (self.line or 1) - 1
        col = (self.column or 1) - 1
        end_line = (self.end_line or self.line or 1) - 1
        end_col = (self.end_column or self.column or 1) - 1
        ide: dict[str, object] = {
            "range": {
                "start": {"line": line, "character": col},
                "end": {"line": end_line, "character": end_col},
            },
            "severity": severity_map.get(self.severity, 1),
            "code": self.code,
            "source": self.source,
            "message": self.message,
            "data": {
                "category": self.category,
                "recoverable": self.recoverable,
                "notes": list(self.notes),
                "fixes": list(self.fixes),
                "suggestions": list(self.suggestions),
                "stack_trace": list(self.stack_trace),
            },
        }
        if self.hint:
            ide["data"]["hint"] = self.hint  # type: ignore[index]
        if self.script:
            ide["data"]["script"] = self.script  # type: ignore[index]
        if self.snippet:
            ide["data"]["snippet"] = self.snippet  # type: ignore[index]
        return ide


def diagnostic_from_error(exc: SanskriptError) -> Diagnostic:
    span = exc.span
    end_line: int | None = None
    end_column: int | None = None
    if span is not None:
        end_line, end_column = _derive_span_end(
            line=span.line,
            column=span.column,
            snippet=span.snippet,
        )
    fixes = exc.fixes or exc.suggestions or ((exc.hint,) if exc.hint else ())
    return Diagnostic(
        code=exc.code,
        message=exc.message,
        severity="error",
        category=exc.category,
        hint=exc.hint,
        recoverable=exc.recoverable,
        notes=exc.notes,
        fixes=fixes,
        suggestions=fixes,
        stack_trace=exc.stack_trace,
        line=span.line if span else None,
        column=span.column if span else None,
        end_line=end_line,
        end_column=end_column,
        snippet=span.snippet if span else None,
        script=exc.original_script,
    )


def diagnostic_from_lint(finding: LintFinding) -> Diagnostic:
    category = f"lint.{finding.code.lower()}"
    return Diagnostic(
        code=f"SANSKRIPT_LINT_{finding.code}",
        message=finding.message,
        severity=finding.severity,
        category=category,
        source="sanskript.linter",
        recoverable=True,
        line=finding.line,
        column=finding.column,
    )


def _derive_span_end(*, line: int, column: int, snippet: str) -> tuple[int, int]:
    if not snippet:
        return line, column + 1
    end_line = line
    end_column = column
    for char in snippet:
        if char == "\n":
            end_line += 1
            end_column = 1
            continue
        end_column += 1
    return end_line, end_column
