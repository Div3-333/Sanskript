"""CLI entry points for Sanskript."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .bytecode import BYTECODE_LATEST, dump_bytecode_file, load_bytecode_file, validate_bytecode
from .compiler import compile_source
from .errors import SanskriptError
from .grammar_register import register_entries
from .interpreter import run
from .morphology_facade import MorphologyFacade
from .morphology_lexicon import build_lexicon_artifact
from .morphology_synth import synthesize
from .performance import main as performance_main
from .webapp import load_program_for_web, write_web_app
from .yantra_patha import program_from_yantra_patha, program_to_yantra_patha


def main(argv: list[str] | None = None) -> int:
    _ensure_utf8_stdio()
    argv = list(sys.argv[1:] if argv is None else argv)

    # Backward-compatible invocation: `sanskript examples/foo.ssk`
    if len(argv) == 1 and Path(argv[0]).suffix in {".ssk", ".sskbc", ".sskyp"}:
        return _run_file(Path(argv[0]))

    parser = argparse.ArgumentParser(prog="sanskript")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser(
        "run",
        help="Execute a .ssk source, .sskbc bytecode, or .sskyp yantra-pāṭha file",
    )
    run_parser.add_argument("source", type=Path)

    compile_parser = subparsers.add_parser("compile", help="Compile a .ssk source file to .sskbc bytecode")
    compile_parser.add_argument("source", type=Path)
    compile_parser.add_argument("-o", "--output", type=Path)
    compile_parser.add_argument("--version", type=int, default=BYTECODE_LATEST, choices=(1, 2))

    disassemble_parser = subparsers.add_parser(
        "disassemble",
        help="Render .sskbc bytecode as Sanskrit-prose yantra-pāṭha",
    )
    disassemble_parser.add_argument("source", type=Path)
    disassemble_parser.add_argument("-o", "--output", type=Path)

    assemble_parser = subparsers.add_parser(
        "assemble",
        help="Assemble Sanskrit-prose yantra-pāṭha into .sskbc bytecode",
    )
    assemble_parser.add_argument("source", type=Path)
    assemble_parser.add_argument("-o", "--output", type=Path)

    web_parser = subparsers.add_parser(
        "web",
        help="Compile .ssk, .sskbc, or .sskyp into a static browser app",
    )
    web_parser.add_argument("source", type=Path)
    web_parser.add_argument("-o", "--output", type=Path)
    web_parser.add_argument("--title", default="Sanskript App")

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
        if command == "compile":
            return _compile_file(args.source, args.output, version=args.version)
        if command == "disassemble":
            return _disassemble_file(args.source, args.output)
        if command == "assemble":
            return _assemble_file(args.source, args.output)
        if command == "web":
            return _web_file(args.source, args.output, title=args.title)
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


def _ensure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")


def _run_file(source: Path) -> int:
    if source.suffix == ".sskbc":
        program = load_bytecode_file(source)
        from .vm import SanskriptVM

        output = SanskriptVM().execute(program)
    elif source.suffix == ".sskyp":
        program = program_from_yantra_patha(source.read_text(encoding="utf-8"))
        from .vm import SanskriptVM

        output = SanskriptVM().execute(program)
    else:
        output = run(source.read_text(encoding="utf-8"))
    for line in output:
        print(line)
    return 0


def _compile_file(source: Path, output: Path | None = None, *, version: int = BYTECODE_LATEST) -> int:
    target = output or source.with_suffix(".sskbc")
    program = compile_source(source.read_text(encoding="utf-8"))
    validate_bytecode(program, version=version)
    dump_bytecode_file(program, target, version=version)
    print(target)
    return 0


def _disassemble_file(source: Path, output: Path | None = None) -> int:
    target = output or source.with_suffix(".sskyp")
    program = load_bytecode_file(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(program_to_yantra_patha(program), encoding="utf-8")
    print(target)
    return 0


def _assemble_file(source: Path, output: Path | None = None) -> int:
    target = output or source.with_suffix(".sskbc")
    program = program_from_yantra_patha(source.read_text(encoding="utf-8"))
    dump_bytecode_file(program, target)
    print(target)
    return 0


def _web_file(source: Path, output: Path | None = None, *, title: str) -> int:
    target = output or source.with_suffix(".html")
    program = load_program_for_web(source)
    write_web_app(program, target, title=title)
    print(target)
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
