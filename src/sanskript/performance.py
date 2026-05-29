"""Small performance baseline for the controlled-language hot path."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter

from .compiler import compile_source
from .errors import SanskriptError
from .vm import SanskriptVM


DEFAULT_EXAMPLE_BUDGET_MS = 25.0


@dataclass(frozen=True)
class PerformanceBaseline:
    example_count: int
    iterations: int
    total_runs: int
    total_ms: float
    average_ms: float
    budget_ms: float
    within_budget: bool


def collect_performance_baseline(
    example_dir: Path | None = None,
    *,
    iterations: int = 20,
    budget_ms: float = DEFAULT_EXAMPLE_BUDGET_MS,
) -> PerformanceBaseline:
    root = Path(__file__).resolve().parents[2]
    example_paths = sorted((example_dir or root / "examples").glob("*.ssk"))
    sources: list[str] = []
    for path in example_paths:
        if "manifest" in path.name or "milestones" in path.name or "port-" in path.name:
            continue
        source = path.read_text(encoding="utf-8")
        if "__P22_PORT__" in source:
            continue
        try:
            compile_source(source)
        except SanskriptError:
            continue
        sources.append(source)
    if not sources:
        return PerformanceBaseline(0, iterations, 0, 0.0, 0.0, budget_ms, False)

    def _run_quiet(source: str) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            SanskriptVM().execute(compile_source(source))

    for source in sources:
        _run_quiet(source)

    started = perf_counter()
    for _ in range(iterations):
        for source in sources:
            _run_quiet(source)
    total_ms = (perf_counter() - started) * 1000
    total_runs = len(sources) * iterations
    average_ms = total_ms / total_runs
    return PerformanceBaseline(
        example_count=len(sources),
        iterations=iterations,
        total_runs=total_runs,
        total_ms=round(total_ms, 3),
        average_ms=round(average_ms, 3),
        budget_ms=budget_ms,
        within_budget=average_ms <= budget_ms,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sanskript-performance")
    parser.add_argument("--examples", type=Path, default=None)
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--budget-ms", type=float, default=DEFAULT_EXAMPLE_BUDGET_MS)
    args = parser.parse_args(argv)

    baseline = collect_performance_baseline(
        args.examples,
        iterations=args.iterations,
        budget_ms=args.budget_ms,
    )
    print(json.dumps(asdict(baseline), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if baseline.within_budget else 1


__all__ = [
    "DEFAULT_EXAMPLE_BUDGET_MS",
    "PerformanceBaseline",
    "collect_performance_baseline",
    "main",
]
