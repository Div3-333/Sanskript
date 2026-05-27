"""Linter for choppy or ungrammatical-looking Sanskript source."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .grammar import PartOfSpeech
from .morphology_facade import get_default_facade
from .morphology_text import tokenize
from .source_pipeline import prepare_source


@dataclass(frozen=True)
class LintFinding:
    code: str
    message: str
    line: int
    column: int = 1
    severity: str = "warning"


_MIN_SENTENCE_WORDS = 3
_CHOPPY_MAX_WORDS = 2


def lint_source(source: str) -> list[LintFinding]:
    prepared = prepare_source(source)
    facade = get_default_facade()
    findings: list[LintFinding] = []
    line_no = 1
    for raw_line in prepared.text.splitlines():
        line = raw_line.strip()
        if not line:
            line_no += 1
            continue
        for sentence in re.split(r"[.?]+", line):
            sentence = sentence.strip()
            if not sentence:
                continue
            findings.extend(_lint_sentence(sentence, facade, line_no))
        line_no += 1
    return findings


def _lint_sentence(sentence: str, facade, line: int) -> list[LintFinding]:
    findings: list[LintFinding] = []
    tokens = tokenize(sentence, normalize_token=facade.normalize_token)
    if len(tokens) <= _CHOPPY_MAX_WORDS:
        findings.append(
            LintFinding(
                code="CHOPPY_SENTENCE",
                message=f"Sentence {sentence!r} is very short; prose programs read better as full vākyas.",
                line=line,
            )
        )
    if len(tokens) < _MIN_SENTENCE_WORDS:
        findings.append(
            LintFinding(
                code="SPARSE_SENTENCE",
                message=f"Sentence {sentence!r} has fewer than {_MIN_SENTENCE_WORDS} words.",
                line=line,
            )
        )
    try:
        analyses = facade.analyze_sentence(sentence)
    except Exception:
        return findings
    verbs = [item for item in analyses if item.pos == PartOfSpeech.VERB]
    if not verbs:
        findings.append(
            LintFinding(
                code="MISSING_VERB",
                message=f"Sentence {sentence!r} has no finite verb; executable vākyas need a verbal predicate.",
                line=line,
            )
        )
    elif len(verbs) > 1:
        findings.append(
            LintFinding(
                code="MULTIPLE_VERBS",
                message=f"Sentence {sentence!r} has {len(verbs)} verbs; prefer one main predicate per vākya.",
                line=line,
            )
        )
    return findings


__all__ = ["LintFinding", "lint_source"]
