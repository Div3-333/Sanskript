"""Audit the generated predicate-only weak-sūtra report."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


ROW_RE = re.compile(r"^\| `(?P<sutra>\d+\.\d+\.\d+)` \| `(?P<reason>[^`]+)` \|", re.MULTILINE)
SUMMARY_RE = re.compile(r"^- (?P<label>.+): (?P<count>\d+)$", re.MULTILINE)


@dataclass(frozen=True)
class PredicateWeakAudit:
    row_count: int
    predicate_only_weak: int
    dispatcher_errors: int
    reason_counts: dict[str, int]
    adhyaya_counts: dict[str, int]
    errors: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


def audit_predicate_weak_doc(path: Path | None = None) -> PredicateWeakAudit:
    root = Path(__file__).resolve().parents[2]
    report = path or root / "docs" / "predicate-only-weak-sutras.md"
    text = report.read_text(encoding="utf-8")

    reason_counts: Counter[str] = Counter()
    adhyaya_counts: Counter[str] = Counter()
    for match in ROW_RE.finditer(text):
        sutra = match.group("sutra")
        reason = match.group("reason")
        reason_counts[reason] += 1
        adhyaya_counts[sutra.split(".", 1)[0]] += 1

    summary = {match.group("label"): int(match.group("count")) for match in SUMMARY_RE.finditer(text)}
    row_count = sum(reason_counts.values())
    dispatcher_errors = reason_counts.get("dispatcher-error", 0)
    predicate_only = row_count - dispatcher_errors

    errors: list[str] = []
    _expect(summary, "Predicate-only / weak", predicate_only, errors)
    _expect(summary, "Dispatcher errors", dispatcher_errors, errors)
    _expect(summary, "Total requiring upgrade", row_count, errors)
    for adhyaya, count in sorted(adhyaya_counts.items(), key=lambda item: int(item[0])):
        _expect(summary, f"Adhyaya {adhyaya}", count, errors)
    for reason, count in sorted(reason_counts.items()):
        _expect(summary, f"`{reason}`", count, errors)

    return PredicateWeakAudit(
        row_count=row_count,
        predicate_only_weak=predicate_only,
        dispatcher_errors=dispatcher_errors,
        reason_counts=dict(sorted(reason_counts.items())),
        adhyaya_counts=dict(sorted(adhyaya_counts.items(), key=lambda item: int(item[0]))),
        errors=tuple(errors),
    )


def _expect(summary: dict[str, int], label: str, actual: int, errors: list[str]) -> None:
    declared = summary.get(label)
    if declared is None:
        errors.append(f"missing summary label {label!r}")
    elif declared != actual:
        errors.append(f"{label}: summary says {declared}, table has {actual}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="predicate-weak-audit")
    parser.add_argument("path", nargs="?", type=Path)
    args = parser.parse_args(argv)

    audit = audit_predicate_weak_doc(args.path)
    print(json.dumps(asdict(audit), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if audit.ok else 1


__all__ = ["PredicateWeakAudit", "audit_predicate_weak_doc", "main"]
