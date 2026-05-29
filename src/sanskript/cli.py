"""CLI entry points for Sanskript."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import shutil
import sys
import traceback
import zipfile
from pathlib import Path

from .diagnostics import diagnostic_from_error, diagnostic_from_lint
from .bytecode import BYTECODE_LATEST, BytecodeProgram, dump_bytecode_file, load_bytecode_file, validate_bytecode
from .compiler import compile_program, compile_source
from .formatter import format_source
from .errors import SanskriptError
from .grammar_register import register_entries
from .morphology_facade import MorphologyFacade
from .morphology_lexicon import build_lexicon_artifact
from .morphology_synth import synthesize
from .module_loader import load_program_from_path
from .linter import lint_source
from .package_lock import build_lock_from_manifest, write_lock
from .package_manifest import find_manifest_path, load_manifest
from .native_backends import (
    build_native_artifacts,
    parse_target_triple,
    plan_to_dict,
)
from .phase20_native_evidence import (
    Phase20EvidenceRequest,
    generate_phase20_evidence,
)
from .phase25_testing_verification import (
    Phase25EvidenceRequest,
    generate_phase25_evidence,
)
from .phase21_cross_platform import (
    Phase21EvidenceRequest,
    generate_phase21_evidence,
    phase21_seal_verdict,
)
from .phase26_docs import write_phase26_evidence
from .phase23_concurrency import phase23_full_seal_payload
from .phase27_migration_report import (
    MIGRATION_REPORT_JSON,
    build_migration_report,
    phase27_full_seal_payload,
    write_migration_report,
)
from .phase18_vm_runtime import SanskriptPortedVM, write_phase18_bootstrap_evidence
from .phase28_milestones import write_phase28_evidence
from .phase28_independence_milestones import build_phase28_report, write_phase28_report
from .performance import main as performance_main
from .self_hosting import verify_host_vs_self_compile, write_bootstrap_seed
from .vm import SanskriptVM
from .webapp import load_program_for_web, write_web_app
from .yantra_patha import program_from_yantra_patha, program_to_yantra_patha
from .phase17_toolchain import (
    freeze_phase17_spec,
    link_programs_phase17,
    load_program_any,
    optimize_program_phase17,
    roundtrip_conformance,
    save_program_any,
    verify_program_phase17,
)
from .phase24_tooling import (
    Phase24EvidenceRequest,
    build_installer,
    build_project,
    build_release,
    collect_coverage,
    create_project,
    debug_trace,
    editor_integration_bundle,
    freeze_phase24_spec,
    generate_phase24_evidence,
    inspect_bytecode,
    inspect_sskyp,
    language_server_capabilities,
    migrate_python_module,
    migrate_rust_module,
    profile_program,
    run_benchmark,
    run_language_server_stdio,
    run_tests,
    textmate_grammar,
    update_dependencies,
    vendor_install_dependency,
    write_playground,
    write_trace_view,
)


def main(argv: list[str] | None = None) -> int:
    _ensure_utf8_stdio()
    argv = list(sys.argv[1:] if argv is None else argv)

    # Backward-compatible invocation: `sanskript examples/foo.ssk`
    if len(argv) == 1 and Path(argv[0]).suffix in {".ssk", ".sskbc", ".sskyp"}:
        return _run_file(Path(argv[0]))

    parser = argparse.ArgumentParser(prog="sanskript")
    parser.add_argument(
        "--diagnostics-format",
        choices=("text", "json", "ide"),
        default="text",
        help="Diagnostics output format",
    )
    parser.add_argument(
        "--crash-report",
        type=Path,
        help="Write uncaught exceptions to a machine-readable crash report path",
    )
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser(
        "run",
        help="Execute a .ssk source, .sskbc bytecode, or .sskyp yantra-pāṭha file",
    )
    run_parser.add_argument("source", type=Path)
    run_parser.add_argument(
        "--lint-level",
        choices=("off", "warning", "error"),
        default="off",
        help="Run lint warnings before execution",
    )

    compile_parser = subparsers.add_parser("compile", help="Compile a .ssk source file to .sskbc bytecode")
    compile_parser.add_argument("source", type=Path)
    compile_parser.add_argument("-o", "--output", type=Path)
    compile_parser.add_argument("--version", type=int, default=BYTECODE_LATEST, choices=(1, 2))
    compile_parser.add_argument(
        "--lint-level",
        choices=("off", "warning", "error"),
        default="off",
        help="Run lint warnings before compilation",
    )

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

    verify_parser = subparsers.add_parser(
        "phase17-verify",
        help="Run Phase 17 verifier/roundtrip conformance on .sskbc/.sskyp/.sskypb",
    )
    verify_parser.add_argument("source", type=Path)

    optimize_parser = subparsers.add_parser(
        "phase17-optimize",
        help="Optimize bytecode and write .sskbc/.sskyp/.sskypb output",
    )
    optimize_parser.add_argument("source", type=Path)
    optimize_parser.add_argument("-o", "--output", type=Path, required=True)

    link_parser = subparsers.add_parser(
        "phase17-link",
        help="Link multiple bytecode/prose inputs into one program",
    )
    link_parser.add_argument("sources", nargs="+", type=Path)
    link_parser.add_argument("-o", "--output", type=Path, required=True)

    subparsers.add_parser("phase17-spec", help="Print frozen Phase 17 spec JSON")

    web_parser = subparsers.add_parser(
        "web",
        help="Compile .ssk, .sskbc, or .sskyp into a static browser app",
    )
    web_parser.add_argument("source", type=Path)
    web_parser.add_argument("-o", "--output", type=Path)
    web_parser.add_argument("--title", default="Sanskript App")

    repl_parser = subparsers.add_parser("repl", help="Run an interactive Sanskript REPL")
    repl_parser.add_argument("--prompt", default="ssk> ")

    docs_parser = subparsers.add_parser("docs", help="Generate simple markdown docs from source")
    docs_parser.add_argument("source", type=Path)
    docs_parser.add_argument("-o", "--output", type=Path)

    install_parser = subparsers.add_parser("install", help="Install a local package path into vendor/")
    install_parser.add_argument("dependency", type=Path)
    install_parser.add_argument("--name")

    pack_parser = subparsers.add_parser("pack", help="Bundle a source tree into a zip artifact")
    pack_parser.add_argument("source", type=Path)
    pack_parser.add_argument("-o", "--output", type=Path)

    subparsers.add_parser("build-lexicon", help="Build data/controlled_lexicon.json")

    synth_parser = subparsers.add_parser("synthesize", help="Synthesize one register entry by id")
    synth_parser.add_argument("register_id")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze one token")
    analyze_parser.add_argument("token")
    lint_parser = subparsers.add_parser("lint", help="Run source diagnostics/lint checks")
    lint_parser.add_argument("source", type=Path)
    lint_parser.add_argument(
        "--lint-level",
        choices=("warning", "error"),
        default="warning",
        help="Treat lint findings as warnings or errors",
    )

    bench_parser = subparsers.add_parser("performance", help="Measure example parse/compile/run speed")
    bench_parser.add_argument("--examples", type=Path)
    bench_parser.add_argument("--iterations", type=int, default=20)
    bench_parser.add_argument("--budget-ms", type=float, default=25.0)

    self_host_parser = subparsers.add_parser(
        "self-host-check",
        help="Run Phase 19 host/self compile parity checks and write bootstrap seed",
    )
    self_host_parser.add_argument(
        "sources",
        nargs="+",
        type=Path,
        help="One or more .ssk sources to verify",
    )
    self_host_parser.add_argument(
        "--artifact-dir",
        type=Path,
        default=Path("artifacts/phase19"),
    )
    self_host_parser.add_argument(
        "--seed",
        type=Path,
        default=Path("bootstrap/phase19/bootstrap_seed.json"),
    )
    self_host_parser.add_argument(
        "--allow-host-replay",
        action="store_true",
        help="allow success exit for S0 host-replay parity checks",
    )
    phase18_parser = subparsers.add_parser(
        "phase18-vm-check",
        help="Run Phase 18 S1/S2 VM bootstrap checks and emit evidence artifacts",
    )
    phase18_parser.add_argument(
        "sources",
        nargs="+",
        type=Path,
        help="One or more .ssk/.sskbc/.sskyp programs to verify",
    )
    phase18_parser.add_argument(
        "--artifact-dir",
        type=Path,
        default=Path("artifacts/phase18"),
    )
    phase18_parser.add_argument(
        "--allow-host-fallback",
        action="store_true",
        help="allow success exit for parity-only checks even when independence gates are unresolved",
    )

    phase28_parser = subparsers.add_parser(
        "independence-milestones",
        help="Evaluate Phase 28 M0–M20 milestones with honesty gates (no inflation)",
    )
    phase28_parser.add_argument(
        "--corpus",
        nargs="*",
        type=Path,
        help="optional .ssk/.sskbc/.sskyp programs for VM retirement corpus (default: minimal emit-one)",
    )
    phase28_parser.add_argument(
        "--phase19-seed",
        type=Path,
        help="optional Phase 19 bootstrap seed JSON for compiler self-host evidence",
    )
    phase28_parser.add_argument(
        "--phase19-source",
        nargs="*",
        type=Path,
        help="optional .ssk sources to probe host-replay (default: none)",
    )
    phase28_parser.add_argument(
        "--artifact-dir",
        type=Path,
        default=Path("artifacts/phase28"),
    )
    phase28_parser.add_argument(
        "--report-json",
        type=Path,
        default=Path("artifacts/phase28/phase28-milestones.json"),
    )

    native_parser = subparsers.add_parser(
        "native-build",
        help="Build Phase 20 backend artifacts from .ssk or .sskbc input",
    )
    native_parser.add_argument("source", type=Path)
    native_parser.add_argument(
        "--backend",
        choices=("portable-bytecode", "web-wasm-plan", "native-object"),
        default="portable-bytecode",
    )
    native_parser.add_argument(
        "--artifact-kind",
        choices=("executable", "shared"),
        default="executable",
    )
    native_parser.add_argument(
        "--target",
        help="target triple (arch-vendor-os-abi), defaults to host",
    )
    native_parser.add_argument(
        "--format",
        choices=("coff", "elf", "macho"),
        help="force object format",
    )
    native_parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("artifacts/phase20"),
    )
    native_parser.add_argument(
        "--link",
        action="store_true",
        help="attempt platform linker invocation",
    )
    native_parser.add_argument(
        "--plan-json",
        type=Path,
        help="optional output path for machine-readable build plan",
    )
    native_evidence_parser = subparsers.add_parser(
        "phase20-evidence",
        help="Generate executable Phase 20 backend evidence matrix",
    )
    native_evidence_parser.add_argument("source", type=Path)
    native_evidence_parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("artifacts/phase20/evidence"),
    )
    native_evidence_parser.add_argument(
        "--plan-json",
        type=Path,
        default=Path("artifacts/phase20/evidence/phase20-evidence.json"),
    )
    native_evidence_parser.add_argument(
        "--link-host",
        action="store_true",
        help="attempt linker invocation for host native-object rows",
    )

    phase21_parser = subparsers.add_parser(
        "phase21-evidence",
        help="Generate Phase 21 cross-platform capability evidence matrix",
    )
    phase21_parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("artifacts/phase21/evidence"),
    )
    phase21_parser.add_argument(
        "--plan-json",
        type=Path,
        default=Path("artifacts/phase21/evidence/phase21-evidence.json"),
    )
    subparsers.add_parser(
        "phase21-seal-check",
        help="Verify Phase 21 full seal (23 checklist rows, zero inflation)",
    )
    phase25_parser = subparsers.add_parser(
        "phase25-evidence",
        help="Generate Phase 25 testing and verification evidence matrix",
    )
    phase25_parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("artifacts/phase25/evidence"),
    )
    phase25_parser.add_argument(
        "--plan-json",
        type=Path,
        default=Path("artifacts/phase25/evidence/phase25-evidence.json"),
    )
    phase25_parser.add_argument(
        "--fuzz-trials",
        type=int,
        default=48,
        help="Smoke harness trial budget (not production/continuous fuzz; see phase25_testing_verification.FUZZ_SMOKE_TRIAL_BUDGET)",
    )
    phase25_parser.add_argument("--property-trials", type=int, default=64)
    phase25_parser.add_argument("--fuzz-seed", type=int, default=2505)
    phase26_parser = subparsers.add_parser(
        "phase26-evidence",
        help="Generate Phase 26 documentation seal evidence",
    )
    phase26_parser.add_argument(
        "--plan-json",
        type=Path,
        default=Path("artifacts/phase26/evidence/phase26-evidence.json"),
    )
    format_parser = subparsers.add_parser("format", help="Format .ssk source (layout not semantic)")
    format_parser.add_argument("source", type=Path)
    format_parser.add_argument("-o", "--output", type=Path)
    format_parser.add_argument("--check", action="store_true", help="exit 1 when formatting would change the file")
    format_parser.add_argument("--stdout", action="store_true", help="write formatted source to stdout")

    test_parser = subparsers.add_parser("test", help="Run Sanskript tests (std.test.* discovery)")
    test_parser.add_argument("root", type=Path, nargs="?", default=Path("."))

    bench_parser = subparsers.add_parser("bench", help="Benchmark parse/compile/run over examples")
    bench_parser.add_argument("--examples", type=Path)
    bench_parser.add_argument("--iterations", type=int, default=20)
    bench_parser.add_argument("--budget-ms", type=float, default=25.0)

    build_parser = subparsers.add_parser("build", help="Compile project .ssk files to dist/bytecode")
    build_parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    build_parser.add_argument("-o", "--out-dir", type=Path)

    coverage_parser = subparsers.add_parser("coverage", help="Opcode/IP coverage for a program")
    coverage_parser.add_argument("source", type=Path)

    profile_parser = subparsers.add_parser("profile", help="Wall-clock opcode profile (estimate)")
    profile_parser.add_argument("source", type=Path)
    profile_parser.add_argument("--iterations", type=int, default=5)

    debug_parser = subparsers.add_parser("debug", help="Record execution trace or Phase 18 debug artifacts")
    debug_parser.add_argument("source", type=Path)
    debug_parser.add_argument("--max-steps", type=int, default=64)
    debug_parser.add_argument(
        "--breakpoints",
        type=int,
        nargs="*",
        default=[],
        help="instruction IPs that pause execution (tracing VM)",
    )
    debug_parser.add_argument(
        "--step",
        action="store_true",
        help="pause after the first executed instruction",
    )
    debug_parser.add_argument("--trace", type=Path, help="write ported-VM trace artifact")
    debug_parser.add_argument("--debug", type=Path, help="write ported-VM debug artifact")
    debug_parser.add_argument("--profile", type=Path, help="write ported-VM profile artifact")
    debug_parser.add_argument("--snapshot", type=Path, help="write ported-VM snapshot artifact")

    lsp_parser = subparsers.add_parser("lsp", help="Language server (stdio JSON-RPC or capabilities JSON)")
    lsp_parser.add_argument("--stdio", action="store_true", help="Run stdio JSON-RPC loop (initialize, hover stub)")
    lsp_parser.add_argument("--capabilities", action="store_true", help="Print capabilities JSON (default)")

    highlight_parser = subparsers.add_parser("highlight", help="Emit TextMate grammar JSON")
    highlight_parser.add_argument("-o", "--output", type=Path)

    editor_parser = subparsers.add_parser(
        "editor-integration",
        help="Write editor integration bundle (grammar + VS Code LSP launch)",
    )
    editor_parser.add_argument("-o", "--output", type=Path, default=Path("artifacts/phase24/editor"))

    new_parser = subparsers.add_parser("new", help="Create a project from a template")
    new_parser.add_argument("template", choices=("app", "lib"))
    new_parser.add_argument("target", type=Path)
    new_parser.add_argument("--name")

    deps_parser = subparsers.add_parser("deps-update", help="Refresh ssk.lock from ssk.toml")
    deps_parser.add_argument("root", type=Path, nargs="?", default=Path("."))

    release_parser = subparsers.add_parser("release", help="Build a release zip from a project tree")
    release_parser.add_argument("root", type=Path)
    release_parser.add_argument("-o", "--output", type=Path, required=True)

    installer_parser = subparsers.add_parser(
        "installer",
        help="Build cross-platform installer zip artifact",
    )
    installer_parser.add_argument("target", choices=("windows", "linux", "macos"))
    installer_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Installer zip path (default: artifacts/phase24/installer-<target>.zip)",
    )

    playground_parser = subparsers.add_parser("playground", help="Write a local HTML playground")
    playground_parser.add_argument("source", type=Path)
    playground_parser.add_argument("-o", "--output", type=Path)
    playground_parser.add_argument("--title", default="Sanskript Playground")

    web_playground_parser = subparsers.add_parser(
        "web-playground",
        help="Alias for browser playground bundle (same as web)",
    )
    web_playground_parser.add_argument("source", type=Path)
    web_playground_parser.add_argument("-o", "--output", type=Path)
    web_playground_parser.add_argument("--title", default="Sanskript Web Playground")

    trace_view_parser = subparsers.add_parser("trace-view", help="Render trace JSON as HTML")
    trace_view_parser.add_argument("trace", type=Path)
    trace_view_parser.add_argument("-o", "--output", type=Path)

    inspect_bc_parser = subparsers.add_parser("inspect-bytecode", help="Structured bytecode report")
    inspect_bc_parser.add_argument("source", type=Path)
    inspect_bc_parser.add_argument("-o", "--output", type=Path)

    inspect_sskyp_parser = subparsers.add_parser("inspect-sskyp", help="Inspect .sskyp yantra-pāṭha")
    inspect_sskyp_parser.add_argument("source", type=Path)
    inspect_sskyp_parser.add_argument("-o", "--output", type=Path)

    migrate_py_parser = subparsers.add_parser("migrate-python", help="Python→Sanskript migration hints")
    migrate_py_parser.add_argument("source", type=Path)
    migrate_py_parser.add_argument("-o", "--output", type=Path)

    migrate_rs_parser = subparsers.add_parser("migrate-rust", help="Rust→Sanskript migration hints")
    migrate_rs_parser.add_argument("source", type=Path)
    migrate_rs_parser.add_argument("-o", "--output", type=Path)

    subparsers.add_parser("phase24-spec", help="Print frozen Phase 24 tooling spec JSON")

    phase24_check_parser = subparsers.add_parser(
        "phase24-check",
        help="Run Phase 24 tooling smoke checks and emit evidence JSON",
    )
    phase24_check_parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("artifacts/phase24"),
    )
    phase24_check_parser.add_argument("--sample-source", type=Path)

    migration_report_parser = subparsers.add_parser(
        "migration-report",
        help="Emit Phase 27 migration report (honest host-vs-native port tracking)",
    )
    migration_report_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=MIGRATION_REPORT_JSON,
        help="JSON report path (markdown written alongside in docs/generated/)",
    )

    migration_seal_parser = subparsers.add_parser(
        "migration-seal",
        help="Phase 27 FULL SEAL gatekeeper (anti-fake ports, wrapper probes, manifest regression)",
    )

    phase23_seal_parser = subparsers.add_parser(
        "phase23-seal",
        help="Phase 23 FULL SEAL gatekeeper (dual-tier host seal; atomics/channels; no fake async)",
    )

    milestone_parser = subparsers.add_parser(
        "milestone-check",
        help="Evaluate Phase 28 independence milestones M0–M20 and emit evidence",
    )
    milestone_parser.add_argument(
        "--artifact-dir",
        type=Path,
        default=Path("artifacts/phase28"),
    )
    milestone_parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="exit 0 when the evidence report is written even if milestones remain open",
    )

    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 2
    command = args.command

    try:
        if command == "run":
            return _run_file(args.source, lint_level=args.lint_level, diagnostics_format=args.diagnostics_format)
        if command == "compile":
            return _compile_file(
                args.source,
                args.output,
                version=args.version,
                lint_level=args.lint_level,
                diagnostics_format=args.diagnostics_format,
            )
        if command == "disassemble":
            return _disassemble_file(args.source, args.output)
        if command == "assemble":
            return _assemble_file(args.source, args.output)
        if command == "phase17-verify":
            return _phase17_verify(args.source)
        if command == "phase17-optimize":
            return _phase17_optimize(args.source, args.output)
        if command == "phase17-link":
            return _phase17_link(args.sources, args.output)
        if command == "phase17-spec":
            print(json.dumps(dict(freeze_phase17_spec()), ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        if command == "web":
            return _web_file(args.source, args.output, title=args.title)
        if command == "repl":
            return _repl(args.prompt)
        if command == "docs":
            return _generate_docs(args.source, args.output)
        if command == "install":
            return _install_package(args.dependency, args.name)
        if command == "pack":
            return _pack_artifact(args.source, args.output)
        if command == "build-lexicon":
            path = build_lexicon_artifact()
            print(path)
            return 0
        if command == "synthesize":
            return _synthesize_command(args.register_id)
        if command == "analyze":
            return _analyze_command(args.token)
        if command == "lint":
            return _lint_file(args.source, lint_level=args.lint_level, diagnostics_format=args.diagnostics_format)
        if command == "format":
            return _format_file(
                args.source,
                output=args.output,
                check=args.check,
                to_stdout=args.stdout,
            )
        if command == "debug":
            if args.trace or args.debug or args.profile or args.snapshot:
                return _debug_file(
                    args.source,
                    trace_path=args.trace,
                    debug_path=args.debug,
                    profile_path=args.profile,
                    snapshot_path=args.snapshot,
                )
            breakpoints = tuple(int(ip) for ip in args.breakpoints) or None
            print(
                json.dumps(
                    debug_trace(
                        args.source,
                        max_steps=args.max_steps,
                        breakpoints=breakpoints,
                        step=args.step,
                    ),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        if command == "test":
            payload = run_tests(args.root)
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return 0 if payload["ok"] else 1
        if command == "bench":
            payload = run_benchmark(
                examples=args.examples,
                iterations=args.iterations,
                budget_ms=args.budget_ms,
            )
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return 0 if payload["ok"] else 1
        if command == "build":
            payload = build_project(args.root, out_dir=args.out_dir)
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return 0 if payload.get("compiled", 0) > 0 else 1
        if command == "coverage":
            print(json.dumps(collect_coverage(args.source), ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        if command == "profile":
            print(
                json.dumps(
                    profile_program(args.source, iterations=args.iterations),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        if command == "lsp":
            if args.stdio:
                return run_language_server_stdio()
            print(
                json.dumps(
                    language_server_capabilities(),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        if command == "highlight":
            target = args.output or Path("artifacts/phase24/sanskript.tmLanguage.json")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(textmate_grammar(), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(target)
            return 0
        if command == "editor-integration":
            print(editor_integration_bundle(args.output))
            return 0
        if command == "new":
            payload = create_project(args.template, args.target, name=args.name)
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        if command == "deps-update":
            print(
                json.dumps(
                    update_dependencies(args.root),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        if command == "release":
            print(
                json.dumps(
                    build_release(args.root, args.output),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        if command == "installer":
            target_path = args.output or Path(f"artifacts/phase24/installer-{args.target}.zip")
            print(
                json.dumps(
                    build_installer(args.target, target_path),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        if command == "playground":
            target = args.output or args.source.with_suffix(".playground.html")
            print(write_playground(args.source, target, title=args.title))
            return 0
        if command == "web-playground":
            return _web_file(args.source, args.output, title=args.title)
        if command == "trace-view":
            target = args.output or args.trace.with_suffix(".html")
            print(write_trace_view(args.trace, target))
            return 0
        if command == "inspect-bytecode":
            payload = inspect_bytecode(args.source)
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                print(args.output)
            else:
                print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        if command == "inspect-sskyp":
            payload = inspect_sskyp(args.source)
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                print(args.output)
            else:
                print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        if command == "migrate-python":
            payload = migrate_python_module(args.source, output=args.output)
            if args.output:
                print(payload["skeleton_file"])
            else:
                print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        if command == "migrate-rust":
            payload = migrate_rust_module(args.source, output=args.output)
            if args.output:
                print(payload["skeleton_file"])
            else:
                print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        if command == "phase24-spec":
            print(json.dumps(freeze_phase24_spec(), ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        if command == "phase24-check":
            payload = generate_phase24_evidence(
                request=Phase24EvidenceRequest(
                    out_dir=args.out_dir,
                    sample_source=args.sample_source,
                )
            )
            print(args.out_dir / "phase24-evidence.json")
            blocked = [row["id"] for row in payload["rows"] if not row.get("smoke_ok")]
            anti_fake = payload.get("anti_fake_violations") or []
            return 0 if not blocked and not anti_fake else 1
        if command == "performance":
            perf_argv = ["--iterations", str(args.iterations), "--budget-ms", str(args.budget_ms)]
            if args.examples is not None:
                perf_argv.extend(["--examples", str(args.examples)])
            return performance_main(perf_argv)
        if command == "self-host-check":
            return _self_host_check(
                args.sources,
                args.artifact_dir,
                args.seed,
                allow_host_replay=args.allow_host_replay,
            )
        if command == "phase18-vm-check":
            return _phase18_vm_check(
                args.sources,
                args.artifact_dir,
                allow_host_fallback=args.allow_host_fallback,
            )
        if command == "independence-milestones":
            return _independence_milestones_command(
                corpus=args.corpus,
                phase19_seed=args.phase19_seed,
                phase19_sources=args.phase19_source,
                artifact_dir=args.artifact_dir,
                report_json=args.report_json,
            )
        if command == "native-build":
            return _native_build_command(
                args.source,
                backend=args.backend,
                artifact_kind=args.artifact_kind,
                target=args.target,
                object_format=args.format,
                out_dir=args.out_dir,
                attempt_link=args.link,
                plan_json=args.plan_json,
            )
        if command == "phase20-evidence":
            return _phase20_evidence_command(
                args.source,
                out_dir=args.out_dir,
                plan_json=args.plan_json,
                link_host=args.link_host,
            )
        if command == "phase21-evidence":
            return _phase21_evidence_command(
                out_dir=args.out_dir,
                plan_json=args.plan_json,
            )
        if command == "phase21-seal-check":
            return _phase21_seal_check_command()
        if command == "phase25-evidence":
            return _phase25_evidence_command(
                out_dir=args.out_dir,
                plan_json=args.plan_json,
                fuzz_trials=args.fuzz_trials,
                property_trials=args.property_trials,
                fuzz_seed=args.fuzz_seed,
            )
        if command == "phase26-evidence":
            return _phase26_evidence_command(plan_json=args.plan_json)
        if command == "migration-report":
            return _migration_report_command(output=args.output)
        if command == "migration-seal":
            return _migration_seal_command()
        if command == "phase23-seal":
            return _phase23_seal_command()
        if command == "milestone-check":
            return _milestone_check_command(
                args.artifact_dir,
                allow_partial=args.allow_partial,
            )
    except SanskriptError as exc:
        _print_error(exc, fmt=args.diagnostics_format)
        return 1
    except Exception as exc:  # pragma: no cover - emergency path
        _handle_crash(exc, report_path=args.crash_report, fmt=args.diagnostics_format)
        return 1

    parser.print_help()
    return 2


def _ensure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")


def _run_file(source: Path, *, lint_level: str = "off", diagnostics_format: str = "text") -> int:
    if source.suffix == ".ssk":
        lint_result = _lint_source_file(source, lint_level=lint_level, diagnostics_format=diagnostics_format)
        if lint_result != 0 and lint_level == "error":
            return lint_result
    if source.suffix == ".sskbc":
        program = load_bytecode_file(source)
        output = SanskriptVM().execute(program)
    elif source.suffix == ".sskyp":
        program = program_from_yantra_patha(source.read_text(encoding="utf-8"))
        output = SanskriptVM().execute(program)
    else:
        output = SanskriptVM().execute(compile_program(load_program_from_path(source)))
    for line in output:
        print(line)
    return 0


def _compile_file(
    source: Path,
    output: Path | None = None,
    *,
    version: int = BYTECODE_LATEST,
    lint_level: str = "off",
    diagnostics_format: str = "text",
) -> int:
    target = output or source.with_suffix(".sskbc")
    if source.suffix == ".ssk":
        lint_result = _lint_source_file(source, lint_level=lint_level, diagnostics_format=diagnostics_format)
        if lint_result != 0 and lint_level == "error":
            return lint_result
        program = compile_program(load_program_from_path(source))
    else:
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


def _phase17_verify(source: Path) -> int:
    program = load_program_any(source)
    report = verify_program_phase17(program)
    if not report.ok:
        for item in report.errors:
            print(item, file=sys.stderr)
        return 1
    roundtrip_conformance(program)
    for item in report.warnings:
        print(f"warning: {item}", file=sys.stderr)
    print("phase17 verify ok")
    return 0


def _phase17_optimize(source: Path, output: Path) -> int:
    program = load_program_any(source)
    optimized = optimize_program_phase17(program)
    save_program_any(optimized, output)
    print(output)
    return 0


def _phase17_link(sources: list[Path], output: Path) -> int:
    linked = link_programs_phase17([load_program_any(path) for path in sources])
    save_program_any(linked, output)
    print(output)
    return 0


def _web_file(source: Path, output: Path | None = None, *, title: str) -> int:
    target = output or source.with_suffix(".html")
    program = load_program_for_web(source)
    write_web_app(program, target, title=title)
    print(target)
    return 0


def _repl(prompt: str) -> int:
    print("Sanskript REPL. Enter :quit to exit.")
    while True:
        try:
            line = input(prompt)
        except EOFError:
            print()
            return 0
        if line.strip() in {":q", ":quit", "exit"}:
            return 0
        if not line.strip():
            continue
        source = line if line.strip().endswith(".") else line.strip() + "."
        try:
            output = SanskriptVM().execute(compile_source(source))
            for item in output:
                print(item)
        except SanskriptError as exc:
            print(f"sanskript: {exc}", file=sys.stderr)


def _generate_docs(source: Path, output: Path | None = None) -> int:
    from .phase26_docs import render_source_api_markdown

    target = output or source.with_suffix(".docs.md")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_source_api_markdown(source), encoding="utf-8")
    print(target)
    return 0


def _install_package(dependency: Path, name: str | None = None) -> int:
    try:
        payload = vendor_install_dependency(Path.cwd(), dependency, name=name)
    except FileNotFoundError as exc:
        print(f"sanskript: {exc}", file=sys.stderr)
        return 1
    print(payload["vendor_path"])
    return 0


def _pack_artifact(source: Path, output: Path | None = None) -> int:
    src = source.resolve()
    if not src.exists():
        print(f"sanskript: source not found: {src}", file=sys.stderr)
        return 1
    target = output or src.with_suffix(".bundle.zip")
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        if src.is_file():
            archive.write(src, arcname=src.name)
        else:
            for path in src.rglob("*"):
                if path.is_file():
                    archive.write(path, arcname=str(path.relative_to(src)))
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


def _load_executable_program(source: Path) -> BytecodeProgram:
    if source.suffix == ".sskbc":
        return load_bytecode_file(source)
    if source.suffix == ".sskyp":
        return program_from_yantra_patha(source.read_text(encoding="utf-8"))
    if source.suffix == ".ssk":
        return compile_program(load_program_from_path(source))
    raise SanskriptError(
        f"unsupported input {source.name!r}; expected .ssk, .sskbc, or .sskyp"
    )


def _format_file(
    source: Path,
    *,
    output: Path | None = None,
    check: bool = False,
    to_stdout: bool = False,
) -> int:
    if source.suffix != ".ssk":
        raise SanskriptError(f"format supports .ssk input, got {source.name!r}")
    load_program_from_path(source)
    original = source.read_text(encoding="utf-8")
    formatted = format_source(original)
    if check:
        return 1 if formatted != original else 0
    if to_stdout:
        sys.stdout.write(formatted)
        return 0
    target = output or source
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(formatted, encoding="utf-8")
    print(target)
    return 0


def _debug_file(
    source: Path,
    *,
    trace_path: Path | None = None,
    debug_path: Path | None = None,
    profile_path: Path | None = None,
    snapshot_path: Path | None = None,
) -> int:
    program = _load_executable_program(source)
    evidence = SanskriptPortedVM().execute(
        program,
        trace_path=trace_path,
        debug_path=debug_path,
        profile_path=profile_path,
        snapshot_path=snapshot_path,
    )
    payload = {
        "source": str(source),
        "output": list(evidence.output),
        "instruction_count": evidence.instruction_count,
        "elapsed_ms": evidence.elapsed_ms,
        "trace_path": evidence.trace_path,
        "debug_path": evidence.debug_path,
        "profile_path": evidence.profile_path,
        "snapshot_path": evidence.snapshot_path,
    }
    if not any((trace_path, debug_path, profile_path, snapshot_path)):
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    for path in (trace_path, debug_path, profile_path, snapshot_path):
        if path is not None:
            print(path)
    return 0


def _lint_file(source: Path, *, lint_level: str = "warning", diagnostics_format: str = "text") -> int:
    return _lint_source_file(source, lint_level=lint_level, diagnostics_format=diagnostics_format)


def _lint_source_file(source: Path, *, lint_level: str, diagnostics_format: str) -> int:
    if lint_level == "off":
        return 0
    findings = lint_source(source.read_text(encoding="utf-8"))
    if not findings:
        return 0
    diagnostics = [diagnostic_from_lint(item) for item in findings]
    for item in diagnostics:
        if lint_level == "error":
            item = item.__class__(**{**item.__dict__, "severity": "error"})
        _print_diagnostic(item, fmt=diagnostics_format, stream="stderr")
    return 1 if lint_level == "error" else 0


def _print_error(exc: SanskriptError, *, fmt: str) -> None:
    diagnostic = diagnostic_from_error(exc)
    _print_diagnostic(diagnostic, fmt=fmt, stream="stderr")


def _print_diagnostic(diagnostic, *, fmt: str, stream: str = "stderr") -> None:
    output = sys.stderr if stream == "stderr" else sys.stdout
    if fmt == "json":
        print(json.dumps(diagnostic.to_machine_dict(), ensure_ascii=False, sort_keys=True), file=output)
        return
    if fmt == "ide":
        print(json.dumps(diagnostic.to_ide_dict(), ensure_ascii=False, sort_keys=True), file=output)
        return
    print(f"sanskript: {diagnostic.message} [{diagnostic.code}]", file=output)
    if diagnostic.hint:
        print(f"hint: {diagnostic.hint}", file=output)
    for note in diagnostic.notes:
        print(f"note: {note}", file=output)
    for fix in diagnostic.fixes:
        print(f"fix: {fix}", file=output)
    for frame in diagnostic.stack_trace:
        print(f"stack: {frame}", file=output)


def _handle_crash(exc: Exception, *, report_path: Path | None, fmt: str) -> None:
    timestamp = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
    stack = traceback.format_exception(type(exc), exc, exc.__traceback__)
    payload = {
        "kind": "sanskript-crash-report",
        "timestamp": timestamp,
        "exception_type": type(exc).__name__,
        "message": str(exc),
        "stack": stack,
    }
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    if fmt == "text":
        print(f"sanskript: internal crash: {type(exc).__name__}: {exc}", file=sys.stderr)
        if report_path:
            print(f"crash report: {report_path}", file=sys.stderr)
        return
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True), file=sys.stderr)


def _self_host_check(
    sources: list[Path],
    artifact_dir: Path,
    seed: Path,
    *,
    allow_host_replay: bool = False,
) -> int:
    source_paths = sorted((Path(src) for src in sources), key=lambda item: item.as_posix().casefold())
    evidence_rows = []
    for src in source_paths:
        evidence = verify_host_vs_self_compile(src, artifact_dir)
        evidence_rows.append(evidence)
        print(
            json.dumps(
                {
                    "source": evidence.source,
                    "stage": evidence.stage,
                    "proof_method": evidence.proof_method,
                    "independent_self_compile": evidence.independent_self_compile,
                    "sskyp_supported": evidence.sskyp_supported,
                    "bytecode_match": evidence.bytecode_match,
                    "sskyp_match": evidence.sskyp_match,
                    "host_repeat_match": evidence.host_repeat_match,
                    "self_repeat_match": evidence.self_repeat_match,
                    "host_bytecode_sha256": evidence.host_bytecode_sha256,
                    "self_bytecode_sha256": evidence.self_bytecode_sha256,
                    "host_sskyp_sha256": evidence.host_sskyp_sha256,
                    "self_sskyp_sha256": evidence.self_sskyp_sha256,
                },
                ensure_ascii=False,
            )
        )
    seed_payload = write_bootstrap_seed(seed, source_paths, artifact_dir, evidence_rows=evidence_rows)
    print(seed)
    all_match = all(
        row["bytecode_match"]
        and ((not row["sskyp_supported"]) or row["sskyp_match"])
        and row["host_repeat_match"]
        and row["self_repeat_match"]
        for row in seed_payload["evidence"]
    )
    if not all_match:
        return 1
    if not allow_host_replay and any(not row.independent_self_compile for row in evidence_rows):
        print(
            "self-host-check: refusing success for non-independent S0 host-replay evidence; "
            "pass --allow-host-replay for parity-only checks.",
            file=sys.stderr,
        )
        return 2
    return 0


def _phase18_vm_check(
    sources: list[Path],
    artifact_dir: Path,
    *,
    allow_host_fallback: bool = False,
) -> int:
    programs = [load_program_any(src) if src.suffix in {".sskbc", ".sskyp"} else compile_program(load_program_from_path(src)) for src in sources]
    payload = write_phase18_bootstrap_evidence(programs, artifact_dir)
    report_path = payload.get("report_path")
    if report_path:
        print(report_path)
    for row in payload["results"]:
        print(
            json.dumps(
                {
                    "program_index": row["program_index"],
                    "s1_match": row["s1"]["output_match"],
                    "s2_match": row["s2"]["output_match"],
                    "independent_vm": row["s2"]["independent_vm"],
                    "host_fallbacks": row["s2"]["host_fallbacks"],
                    "s1_program_sha256": row["s1"]["program_sha256"],
                    "s2_program_sha256": row["s2"]["program_sha256"],
                },
                ensure_ascii=False,
            )
        )
    if payload["retirement_report"]["retirement_ready"]:
        return 0
    if allow_host_fallback:
        return 0
    print(
        "phase18-vm-check: refusing success for non-independent VM bootstrap evidence; "
        "pass --allow-host-fallback for parity-only checks.",
        file=sys.stderr,
    )
    return 2


def _independence_milestones_command(
    *,
    corpus: list[Path] | None,
    phase19_seed: Path | None,
    phase19_sources: list[Path] | None,
    artifact_dir: Path,
    report_json: Path,
) -> int:
    corpus_paths = list(corpus) if corpus else None
    payload = write_phase28_report(
        report_json,
        corpus_paths=corpus_paths,
        phase19_seed_path=phase19_seed,
        phase19_sources=list(phase19_sources) if phase19_sources else None,
        artifact_dir=artifact_dir,
    )
    print(report_json)
    for row in payload["milestones"]:
        if row["milestone_id"] in {"M13", "M14", "M15", "M16", "M17", "M18", "M19", "M20"}:
            print(
                json.dumps(
                    {
                        "milestone_id": row["milestone_id"],
                        "status": row["status"],
                        "claim_allowed": row["claim_allowed"],
                        "blocked_reasons": row["blocked_reasons"][:2],
                    },
                    ensure_ascii=False,
                )
            )
    gates = payload["honesty_gates"]
    print(json.dumps({"seal_ready": gates["seal_ready"], "inflation_issues": gates["inflation_issues"]}, ensure_ascii=False))
    if not gates["seal_ready"]:
        print("independence-milestones: refusing success — milestone inflation detected", file=sys.stderr)
        return 2
    return 0


def _native_build_command(
    source: Path,
    *,
    backend: str,
    artifact_kind: str,
    target: str | None,
    object_format: str | None,
    out_dir: Path,
    attempt_link: bool,
    plan_json: Path | None,
) -> int:
    if source.suffix == ".sskbc":
        program = load_bytecode_file(source)
    elif source.suffix == ".ssk":
        program = compile_program(load_program_from_path(source))
    else:
        raise SanskriptError(
            f"native-build supports .ssk or .sskbc input, got {source.name!r}"
        )
    plan = build_native_artifacts(
        program=program,
        out_dir=out_dir,
        target=parse_target_triple(target),
        backend=backend,
        artifact_kind=artifact_kind,
        requested_format=object_format,
        attempt_link=attempt_link,
    )
    payload = plan_to_dict(plan)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if plan_json:
        plan_json.parent.mkdir(parents=True, exist_ok=True)
        plan_json.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(plan_json)
    return 0


def _migration_report_command(*, output: Path) -> int:
    payload = write_migration_report(output)
    seal = payload.get("seal", {})
    print(output)
    print(
        f"migration-report: seal={seal.get('status')} "
        f"honest_tracking={seal.get('ready_for_honest_tracking')} "
        f"full_seal={seal.get('full_seal_ready')} "
        f"python_files={payload.get('summary', {}).get('python_file_count', 0)} "
        f"blockers={len(payload.get('port_blockers', []))}"
    )
    return 0


def _migration_seal_command() -> int:
    payload = phase27_full_seal_payload()
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    violations = payload.get("violations", [])
    seal_ready = payload.get("full_seal_ready", False)
    print(
        f"migration-seal: full_seal_ready={seal_ready} "
        f"violations={len(violations)} "
        f"manifest_passed={payload.get('manifest_regression', {}).get('passed', 0)}/"
        f"{payload.get('manifest_regression', {}).get('count', 0)}"
    )
    if violations:
        for issue in violations:
            print(f"  - {issue}", file=sys.stderr)
    return 0 if seal_ready else 1


def _phase23_seal_command() -> int:
    payload = phase23_full_seal_payload()
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    violations = payload.get("violations", [])
    seal_ready = payload.get("full_seal_ready", False)
    verdict = payload.get("verdict", {})
    host = verdict.get("host_tier", {})
    print(
        f"phase23-seal: full_seal_ready={seal_ready} "
        f"status={payload.get('status')} "
        f"atomics_thread_safe={host.get('atomics_thread_safe')} "
        f"channels_thread_safe={host.get('channels_thread_safe')} "
        f"violations={len(violations)}"
    )
    if violations:
        for issue in violations:
            print(f"  - {issue}", file=sys.stderr)
    return 0 if seal_ready else 1


def _phase26_evidence_command(*, plan_json: Path) -> int:
    path = write_phase26_evidence(plan_json)
    payload = json.loads(path.read_text(encoding="utf-8"))
    seal = payload.get("seal_verdict", {})
    print(json.dumps(seal, ensure_ascii=False, indent=2))
    print(path)
    return 0 if seal.get("seal_ready") else 1


def _phase25_evidence_command(
    *,
    out_dir: Path,
    plan_json: Path,
    fuzz_trials: int,
    property_trials: int,
    fuzz_seed: int,
) -> int:
    payload = generate_phase25_evidence(
        request=Phase25EvidenceRequest(
            out_dir=out_dir,
            fuzz_trials=fuzz_trials,
            property_trials=property_trials,
            fuzz_seed=fuzz_seed,
        )
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    plan_json.parent.mkdir(parents=True, exist_ok=True)
    plan_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(plan_json)
    seal = payload.get("seal_verdict", {})
    coverage_proof = payload.get("coverage_proof", {})
    if not coverage_proof.get("passed"):
        print("phase25-evidence: coverage proof failed — seal_ready rejected", file=sys.stderr)
    elif not seal.get("seal_ready"):
        print("phase25-evidence: seal blockers remain", file=sys.stderr)
    return 0 if seal.get("seal_ready") else 1


def _milestone_check_command(artifact_dir: Path, *, allow_partial: bool = False) -> int:
    payload = write_phase28_evidence(artifact_dir)
    report_path = payload.get("report_path")
    if report_path:
        print(report_path)
    for row in payload["milestones"]:
        print(
            json.dumps(
                {
                    "milestone_id": row["milestone_id"],
                    "passed": row["passed"],
                    "claim_allowed": row["claim_allowed"],
                    "blockers": row["blockers"][:2],
                },
                ensure_ascii=False,
            )
        )
    gates = payload["honesty_gates"]
    if gates["allow_full_independence_claim"]:
        return 0
    if allow_partial:
        return 0
    print(
        "milestone-check: refusing success while independence milestones remain open; "
        "pass --allow-partial to record evidence without claiming closure.",
        file=sys.stderr,
    )
    return 2


def _phase20_evidence_command(
    source: Path,
    *,
    out_dir: Path,
    plan_json: Path,
    link_host: bool,
) -> int:
    if source.suffix == ".sskbc":
        program = load_bytecode_file(source)
    elif source.suffix == ".ssk":
        program = compile_program(load_program_from_path(source))
    else:
        raise SanskriptError(
            f"phase20-evidence supports .ssk or .sskbc input, got {source.name!r}"
        )
    payload = generate_phase20_evidence(
        program,
        request=Phase20EvidenceRequest(
            out_dir=out_dir,
            attempt_link_host=link_host,
        ),
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    plan_json.parent.mkdir(parents=True, exist_ok=True)
    plan_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(plan_json)
    return 0


def _phase21_evidence_command(*, out_dir: Path, plan_json: Path) -> int:
    payload = generate_phase21_evidence(
        request=Phase21EvidenceRequest(out_dir=out_dir),
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    plan_json.parent.mkdir(parents=True, exist_ok=True)
    plan_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(plan_json)
    return 0


def _phase21_seal_check_command() -> int:
    verdict = phase21_seal_verdict()
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    if not verdict.get("seal_ready"):
        print("phase21-seal-check: refusing success — seal blockers remain", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


if __name__ == "__main__":
    raise SystemExit(main())
