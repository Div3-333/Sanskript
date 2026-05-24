"""CLI entry points for Sanskript."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .errors import SanskriptError
from .grammar_register import register_entries
from .interpreter import run
from .morphology_facade import MorphologyFacade
from .morphology_lexicon import build_lexicon_artifact
from .morphology_synth import synthesize
from .performance import main as performance_main


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    # Backward-compatible invocation: `sanskript examples/foo.ssk`
    if len(argv) == 1 and argv[0].endswith(".ssk"):
        return _run_file(Path(argv[0]))

    parser = argparse.ArgumentParser(prog="sanskript")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Execute a .ssk source file")
    run_parser.add_argument("source", type=Path)

    subparsers.add_parser("build-lexicon", help="Build data/controlled_lexicon.json")

    synth_parser = subparsers.add_parser("synthesize", help="Synthesize one register entry by id")
    synth_parser.add_argument("register_id")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze one token")
    analyze_parser.add_argument("token")

    bench_parser = subparsers.add_parser("performance", help="Measure example parse/compile/run speed")
    bench_parser.add_argument("--iterations", type=int, default=20)
    bench_parser.add_argument("--budget-ms", type=float, default=25.0)

    args = parser.parse_args(argv)
    command = args.command or "run"

    try:
        if command == "run":
            return _run_file(args.source)
        if command == "build-lexicon":
            path = build_lexicon_artifact()
            print(path)
            return 0
        if command == "synthesize":
            return _synthesize_command(args.register_id)
        if command == "analyze":
            return _analyze_command(args.token)
        if command == "performance":
            return performance_main(["--iterations", str(args.iterations), "--budget-ms", str(args.budget_ms)])
    except SanskriptError as exc:
        print(f"sanskript: {exc}", file=sys.stderr)
        return 1

    parser.print_help()
    return 2


def _run_file(source: Path) -> int:
    output = run(source.read_text(encoding="utf-8"))
    for line in output:
        print(line)
    return 0


def _synthesize_command(register_id: str) -> int:
    for entry in register_entries():
        if entry.register_id == register_id:
            result = synthesize(entry.intent)
            payload = {
                "register_id": entry.register_id,
                "surface": result.surface,
                "lemma": result.analysis.lemma,
                "engine": result.engine,
                "recipe_id": result.recipe_id,
                "operations": list(result.operations),
                "sutra_ids": list(result.sutra_ids),
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0
    print(f"sanskript: unknown register id {register_id!r}", file=sys.stderr)
    return 1


def _analyze_command(token: str) -> int:
    analysis = MorphologyFacade().analyze_token(token)
    payload = {
        "surface": analysis.surface,
        "lemma": analysis.lemma,
        "pos": analysis.pos.value,
        "case": analysis.case.value if analysis.case else None,
        "role": analysis.role.value if analysis.role else None,
        "number": analysis.number.value if analysis.number else None,
        "gender": analysis.gender.value if analysis.gender else None,
        "person": analysis.person.value if analysis.person else None,
        "lakara": analysis.lakara.value if analysis.lakara else None,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0
