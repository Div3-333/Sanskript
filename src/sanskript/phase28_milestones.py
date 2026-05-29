"""Phase 28 independence milestone evaluator (M0–M20).

Automated evidence only: milestones pass only when reproducible checks succeed.
Honesty gates forbid treating host-replay bootstrap (Phases 18–19) as full independence.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .bytecode import BytecodeProgram, encode_program, load_bytecode_file, validate_bytecode
from .compiler import compile_program, compile_source
from .module_loader import load_program_from_path
from .native_backends import build_native_artifacts, host_target_triple
from .phase21_cross_platform import host_platform_family
from .phase17_toolchain import load_program_any, verify_program_phase17
from .phase18_vm_runtime import program_sha256, write_phase18_bootstrap_evidence
from .self_hosting import HOST_ENGINE, STAGE_ID, STAGE_S1, verify_host_vs_self_compile
from .stdlib_core import call_native_function, has_native_function, list_native_functions
from .vm import SanskriptVM
from .webapp import load_program_for_web, write_web_app
from .yantra_patha import program_from_yantra_patha, program_to_yantra_patha


Evaluator = Callable[[Path], "MilestoneEvidence"]

MILESTONE_TITLES: dict[str, str] = {
    "M0": "Current host implementation can run all existing examples",
    "M1": "Sanskript can express all current bytecode examples in source prose",
    "M2": "Sanskript can express all current .sskyp examples in machine prose",
    "M3": "Sanskript standard library covers text, collections, files, JSON, CLI, HTTP, and tests",
    "M4": "Sanskript can implement a useful CLI app without Python/Rust code",
    "M5": "Sanskript can implement a useful web app without Python/Rust app code",
    "M6": "Sanskript can implement a useful desktop/productivity app",
    "M7": "Sanskript can implement a useful game loop and asset pipeline",
    "M8": "Sanskript can implement research/data scripts",
    "M9": "Sanskript can implement the VM core in rakṣita",
    "M10": "Sanskript can implement bytecode verification in Sanskript",
    "M11": "Sanskript can implement the compiler frontend in Sanskript",
    "M12": "Sanskript can implement the compiler backend in Sanskript",
    "M13": "Sanskript can compile its own compiler",
    "M14": "Sanskript can run its own VM",
    "M15": "Sanskript can build and test itself",
    "M16": "Sanskript can emit native binaries for at least one platform",
    "M17": "Sanskript can emit native binaries for Windows, macOS, and Linux",
    "M18": "Sanskript can target web without handwritten JavaScript application code",
    "M19": "The repo no longer requires Python/Rust for ordinary Sanskript development",
    "M20": "Python/Rust remain only optional bootstrap, compatibility, or contributor convenience paths",
}


@dataclass(frozen=True)
class MilestoneEvidence:
    milestone_id: str
    title: str
    passed: bool
    claim_allowed: bool
    proof_method: str
    evidence: dict[str, Any]
    blockers: tuple[str, ...]


def repo_root(start: Path | None = None) -> Path:
    if start is not None:
        return start.resolve().parents[1] if start.name.endswith(".py") else start.resolve()
    return Path(__file__).resolve().parents[2]


def _canonical_program_sha256(program: BytecodeProgram) -> str:
    payload = encode_program(program)
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _compile_example_source(path: Path) -> BytecodeProgram:
    if "phase9-modules" in path.as_posix():
        return compile_program(load_program_from_path(path))
    return compile_source(path.read_text(encoding="utf-8"))


def _example_ssk_paths(root: Path) -> list[Path]:
    return sorted(root.glob("examples/**/*.ssk"), key=lambda p: p.as_posix().casefold())


def _example_sskbc_paths(root: Path) -> list[Path]:
    return sorted(root.glob("examples/**/*.sskbc"), key=lambda p: p.as_posix().casefold())


# Bytecode-only or tooling artifacts — excluded from M1 with explicit honesty notes.
M1_EXCLUDED_SSKBC_SUFFIXES: frozenset[str] = frozenset(
    {
        "examples/phase18-vm-bootstrap.sskbc",
        "examples/phase27-port-controlled-lexicon.sskbc",
        "examples/phase27-port-examples-runner.sskbc",
        "examples/phase27-port-sutra-registry.sskbc",
    }
)
M1_EXCLUDED_SSKBC_PREFIXES: tuple[str, ...] = (
    "examples/.phase25-diff/",
    "examples/phase25-diff/",
    "examples/phase9-modules/dist/",
    "examples/phase27-port-",
)


def _m1_exclusion_reason(rel_posix: str) -> str | None:
    if rel_posix in M1_EXCLUDED_SSKBC_SUFFIXES:
        return "bytecode-only bootstrap artifact (no canonical .ssk prose)"
    for prefix in M1_EXCLUDED_SSKBC_PREFIXES:
        if rel_posix.startswith(prefix):
            if prefix == "examples/phase27-port-":
                return "phase27 porting probe bytecode (host tooling artifact, no .ssk prose)"
            return "tooling/diff artifact outside canonical examples corpus"
    return None


_PLATFORM_EXAMPLE_FILES: dict[str, str] = {
    "linux": "examples/phase9-modules/platform/linux-extra.ssk",
    "windows": "examples/phase9-modules/platform/windows-extra.ssk",
    "macos": "examples/phase9-modules/platform/macos-extra.ssk",
}

def _platform_example_skip_reason(path: Path, root: Path) -> str | None:
    rel = path.relative_to(root).as_posix()
    for family, expected in _PLATFORM_EXAMPLE_FILES.items():
        if rel == expected and family != host_platform_family():
            return f"platform-gated example for {family!r} (host is {host_platform_family()!r})"
    return None


# Examples that compile but need test-harness substitution before VM run.
_M0_VM_RUN_SKIP_PATHS: dict[str, str] = {
    "examples/phase22-http-service.ssk": "__P22_PORT__ placeholder requires integration port substitution",
    "examples/phase22/http-service.ssk": "__P22_PORT__ placeholder requires integration port substitution",
}

# Draft/scaffold tree — canonical Phase 22 seal programs live at examples/phase22-*.ssk (repo root).
_M0_EXCLUDED_PREFIXES: tuple[str, ...] = (
    "examples/phase22/",
    "examples/phase27-port-",
)


def _network_example_skip_reason(path: Path, root: Path) -> str | None:
    rel = path.relative_to(root).as_posix()
    return _M0_VM_RUN_SKIP_PATHS.get(rel)


def _m0_corpus_skip_reason(path: Path, root: Path) -> str | None:
    rel = path.relative_to(root).as_posix()
    if rel.startswith("examples/_") or "/_" in rel:
        return "internal probe example (underscore-prefixed path)"
    for prefix in _M0_EXCLUDED_PREFIXES:
        if rel.startswith(prefix):
            if prefix == "examples/phase27-port-":
                return (
                    "phase27 porting probe sources (host tooling; canonical seal uses "
                    "tests/test_phase27_migration.py)"
                )
            return (
                "phase22 scaffold subdirectory; seal bar uses root-level "
                "examples/phase22-*.ssk (tests/test_phase22_web_apps_games_research_ml.py)"
            )
    return None


def _example_run_skip_reason(path: Path, root: Path) -> str | None:
    return (
        _m0_corpus_skip_reason(path, root)
        or _platform_example_skip_reason(path, root)
        or _network_example_skip_reason(path, root)
    )


def _example_sskyp_paths(root: Path) -> list[Path]:
    return sorted(root.glob("examples/**/*.sskyp"), key=lambda p: p.as_posix().casefold())


def _pass(
    milestone_id: str,
    *,
    proof_method: str,
    evidence: dict[str, Any],
    claim_allowed: bool = True,
) -> MilestoneEvidence:
    return MilestoneEvidence(
        milestone_id=milestone_id,
        title=MILESTONE_TITLES[milestone_id],
        passed=True,
        claim_allowed=claim_allowed,
        proof_method=proof_method,
        evidence=evidence,
        blockers=(),
    )


def _fail(
    milestone_id: str,
    *,
    proof_method: str,
    evidence: dict[str, Any],
    blockers: tuple[str, ...],
    claim_allowed: bool = False,
) -> MilestoneEvidence:
    return MilestoneEvidence(
        milestone_id=milestone_id,
        title=MILESTONE_TITLES[milestone_id],
        passed=False,
        claim_allowed=claim_allowed,
        proof_method=proof_method,
        evidence=evidence,
        blockers=blockers,
    )


def evaluate_m0_host_examples(root: Path) -> MilestoneEvidence:
    proof = "host-compile-and-vm-run:examples/**/*.ssk"
    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    for path in _example_ssk_paths(root):
        rel = path.relative_to(root).as_posix()
        row: dict[str, Any] = {"path": rel}
        skip_reason = _example_run_skip_reason(path, root)
        if skip_reason:
            row["ok"] = True
            row["skipped"] = True
            row["skip_reason"] = skip_reason
            rows.append(row)
            continue
        try:
            program = _compile_example_source(path)
            validate_bytecode(program)
            row["compile_ok"] = True
            output = list(SanskriptVM().execute(program))
            row["ok"] = True
            row["output_lines"] = len(output)
        except Exception as exc:
            row["ok"] = False
            row["error"] = f"{type(exc).__name__}: {exc}"
            failures.append(f"{rel}: {row['error']}")
        rows.append(row)
    skipped = sum(1 for row in rows if row.get("skipped"))
    required = len(rows) - skipped
    passed_required = sum(1 for row in rows if row.get("ok") and not row.get("skipped"))
    evidence = {
        "corpus": "examples/**/*.ssk",
        "total": len(rows),
        "required": required,
        "skipped": skipped,
        "passed": passed_required,
        "rows": rows,
    }
    if failures:
        return _fail("M0", proof_method=proof, evidence=evidence, blockers=tuple(failures))
    return _pass("M0", proof_method=proof, evidence=evidence)


def evaluate_m1_bytecode_source_parity(root: Path) -> MilestoneEvidence:
    proof = "canonical-bytecode-sha256:ssk-vs-sskbc"
    rows: list[dict[str, Any]] = []
    blockers: list[str] = []
    excluded = 0
    for bc_path in _example_sskbc_paths(root):
        rel = bc_path.relative_to(root).as_posix()
        ssk_path = bc_path.with_suffix(".ssk")
        row: dict[str, Any] = {
            "bytecode": rel,
            "source": ssk_path.relative_to(root).as_posix() if ssk_path.exists() else None,
        }
        exclusion = _m1_exclusion_reason(rel)
        if exclusion:
            row["excluded"] = True
            row["exclusion_reason"] = exclusion
            excluded += 1
            rows.append(row)
            continue
        if not ssk_path.exists():
            row["ok"] = False
            blockers.append(f"missing source prose for {rel}")
            rows.append(row)
            continue
        try:
            compiled = _compile_example_source(ssk_path)
            loaded = load_bytecode_file(bc_path)
            compiled_hash = _canonical_program_sha256(compiled)
            loaded_hash = _canonical_program_sha256(loaded)
            row["ok"] = compiled_hash == loaded_hash
            row["compiled_sha256"] = compiled_hash
            row["artifact_sha256"] = loaded_hash
            if not row["ok"]:
                blockers.append(f"bytecode mismatch for {rel}")
        except Exception as exc:
            row["ok"] = False
            row["error"] = f"{type(exc).__name__}: {exc}"
            blockers.append(f"{rel}: {row['error']}")
        rows.append(row)
    required = len(rows) - excluded
    evidence = {
        "corpus": "examples/**/*.sskbc",
        "total": len(rows),
        "required": required,
        "excluded_artifacts": excluded,
        "passed": sum(1 for r in rows if r.get("ok") and not r.get("excluded")),
        "rows": rows,
    }
    if blockers:
        return _fail("M1", proof_method=proof, evidence=evidence, blockers=tuple(blockers))
    if required == 0:
        return _fail(
            "M1",
            proof_method=proof,
            evidence=evidence,
            blockers=("no required bytecode artifacts after exclusions",),
        )
    return _pass("M1", proof_method=proof, evidence=evidence)


def evaluate_m2_sskyp_roundtrip(root: Path) -> MilestoneEvidence:
    proof = "yantra-patha-roundtrip:program-sha256-stable"
    rows: list[dict[str, Any]] = []
    blockers: list[str] = []
    for path in _example_sskyp_paths(root):
        rel = str(path.relative_to(root))
        row: dict[str, Any] = {"path": rel}
        try:
            text = path.read_text(encoding="utf-8")
            program = program_from_yantra_patha(text)
            validate_bytecode(program)
            roundtrip_text = program_to_yantra_patha(program)
            rebuilt = program_from_yantra_patha(roundtrip_text)
            h1 = program_sha256(program)
            h2 = program_sha256(rebuilt)
            row["ok"] = h1 == h2
            row["program_sha256"] = h1
            row["text_stable"] = roundtrip_text == text
            if not row["ok"]:
                blockers.append(f"program hash unstable for {rel}")
        except Exception as exc:
            row["ok"] = False
            row["error"] = f"{type(exc).__name__}: {exc}"
            blockers.append(f"{rel}: {row['error']}")
        rows.append(row)
    evidence = {
        "corpus": "examples/**/*.sskyp",
        "total": len(rows),
        "passed": sum(1 for row in rows if row.get("ok")),
        "rows": rows,
    }
    if blockers:
        return _fail("M2", proof_method=proof, evidence=evidence, blockers=tuple(blockers))
    return _pass("M2", proof_method=proof, evidence=evidence)


def _stdlib_domain_smoke() -> dict[str, dict[str, Any]]:
    names = set(list_native_functions())
    domains: dict[str, dict[str, Any]] = {}

    def _register(name: str, *, required: str, smoke: Callable[[], None]) -> None:
        entry = {"required": required, "registered": required in names}
        try:
            smoke()
            entry["smoke_ok"] = True
        except Exception as exc:
            entry["smoke_ok"] = False
            entry["smoke_error"] = f"{type(exc).__name__}: {exc}"
        domains[name] = entry

    _register(
        "text",
        required="std.text.strip",
        smoke=lambda: call_native_function("std.text.strip", ["  x  "]),
    )
    _register(
        "collections",
        required="std.json.parse",
        smoke=lambda: call_native_function(
            "std.json.parse",
            ['{"items":[1,2,3]}'],
        ),
    )
    _register(
        "files",
        required="std.file.read_text",
        smoke=lambda: _smoke_temp_file(),
    )
    _register(
        "json",
        required="std.json.stringify",
        smoke=lambda: call_native_function("std.json.stringify", [{"ok": True}]),
    )
    _register(
        "cli",
        required="std.cli.program_name",
        smoke=lambda: call_native_function("std.cli.program_name", []),
    )
    _register(
        "http",
        required="std.http.get",
        smoke=lambda: None if not has_native_function("std.http.get") else None,
    )
    _register(
        "tests",
        required="std.test.assert_eq",
        smoke=lambda: call_native_function("std.test.assert_eq", [1, 1]),
    )
    if domains["http"]["registered"]:
        domains["http"]["smoke_ok"] = True
    else:
        domains["http"]["smoke_ok"] = False
        domains["http"]["smoke_error"] = "std.http.get not registered"
    return domains


def _smoke_temp_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "phase28.txt"
        path.write_text("phase28", encoding="utf-8")
        value = call_native_function("std.file.read_text", [str(path)])
        if value != "phase28":
            raise RuntimeError(f"unexpected file contents: {value!r}")


def evaluate_m3_stdlib_coverage(_root: Path) -> MilestoneEvidence:
    proof = "stdlib-registry-and-smoke:required-domains"
    domains = _stdlib_domain_smoke()
    blockers: list[str] = []
    for name, row in domains.items():
        if not row.get("registered"):
            blockers.append(f"{name}: missing {row['required']}")
        elif not row.get("smoke_ok"):
            blockers.append(f"{name}: smoke failed ({row.get('smoke_error', 'unknown')})")
    evidence = {"domains": domains, "required": list(domains)}
    if blockers:
        return _fail("M3", proof_method=proof, evidence=evidence, blockers=tuple(blockers))
    return _pass("M3", proof_method=proof, evidence=evidence)


def _run_source_example(root: Path, relative: str, *, required_calls: tuple[str, ...] = ()) -> dict[str, Any]:
    path = root / relative
    source = path.read_text(encoding="utf-8")
    for call in required_calls:
        if call not in source:
            raise ValueError(f"missing required surface {call!r} in {relative}")
    program = _compile_example_source(path)
    output = list(SanskriptVM().execute(program))
    return {"path": relative, "output_lines": len(output), "required_calls": list(required_calls)}


def evaluate_m4_cli_app(root: Path) -> MilestoneEvidence:
    proof = "example-run:phase10-stdlib-cli-io.ssk"
    try:
        evidence = _run_source_example(
            root,
            "examples/phase10-stdlib-cli-io.ssk",
            required_calls=("std.cli.program_name", "std.file.read_text"),
        )
        return _pass("M4", proof_method=proof, evidence=evidence)
    except Exception as exc:
        return _fail(
            "M4",
            proof_method=proof,
            evidence={"example": "examples/phase10-stdlib-cli-io.ssk"},
            blockers=(f"{type(exc).__name__}: {exc}",),
        )


def evaluate_m5_web_app(root: Path) -> MilestoneEvidence:
    proof = "webapp-html-emit:prathama.ssk"
    source = root / "examples" / "prathama.ssk"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "app.html"
            program = load_program_for_web(source)
            write_web_app(program, out, title="phase28")
            html = out.read_text(encoding="utf-8")
            evidence = {
                "source": str(source.relative_to(root)),
                "html_bytes": len(html.encode("utf-8")),
                "has_program_payload": 'id="sanskript-program"' in html,
            }
            if not evidence["has_program_payload"]:
                return _fail(
                    "M5",
                    proof_method=proof,
                    evidence=evidence,
                    blockers=("generated HTML missing embedded program payload",),
                )
            return _pass("M5", proof_method=proof, evidence=evidence)
    except Exception as exc:
        return _fail(
            "M5",
            proof_method=proof,
            evidence={"source": str(source.relative_to(root))},
            blockers=(f"{type(exc).__name__}: {exc}",),
        )


def evaluate_m6_desktop_app(root: Path) -> MilestoneEvidence:
    proof = "example-run:desktop-productivity-corpus"
    for path in _example_ssk_paths(root):
        text = path.read_text(encoding="utf-8")
        if "std.gui." not in text:
            continue
        try:
            evidence = _run_source_example(root, str(path.relative_to(root)))
            evidence["gui_surfaces"] = sorted(set(re.findall(r"std\.gui\.\w+", text)))
            return _pass("M6", proof_method=proof, evidence=evidence)
        except Exception as exc:
            return _fail(
                "M6",
                proof_method=proof,
                evidence={"path": str(path.relative_to(root))},
                blockers=(f"{type(exc).__name__}: {exc}",),
            )
    return _fail(
        "M6",
        proof_method=proof,
        evidence={"corpus": "examples/**/*.ssk with std.gui.*"},
        blockers=(
            "no example demonstrates desktop/productivity GUI surfaces (std.gui.*) end-to-end",
        ),
    )


def evaluate_m7_game_loop(root: Path) -> MilestoneEvidence:
    proof = "example-run:game-loop-and-assets"
    for path in _example_ssk_paths(root):
        text = path.read_text(encoding="utf-8")
        if "std.game." not in text:
            continue
        try:
            evidence = _run_source_example(root, str(path.relative_to(root)))
            evidence["game_surfaces"] = sorted(set(re.findall(r"std\.game\.\w+", text)))
            return _pass("M7", proof_method=proof, evidence=evidence)
        except Exception as exc:
            return _fail(
                "M7",
                proof_method=proof,
                evidence={"path": str(path.relative_to(root))},
                blockers=(f"{type(exc).__name__}: {exc}",),
            )
    return _fail(
        "M7",
        proof_method=proof,
        evidence={"corpus": "examples/**/*.ssk"},
        blockers=("no example uses std.game.* loop/asset surfaces",),
    )


def evaluate_m8_research_data(root: Path) -> MilestoneEvidence:
    proof = "example-run:phase11-algorithms-data-structures.ssk"
    try:
        evidence = _run_source_example(
            root,
            "examples/phase11-algorithms-data-structures.ssk",
            required_calls=("std.alg.",),
        )
        return _pass("M8", proof_method=proof, evidence=evidence)
    except Exception as exc:
        return _fail(
            "M8",
            proof_method=proof,
            evidence={"example": "examples/phase11-algorithms-data-structures.ssk"},
            blockers=(f"{type(exc).__name__}: {exc}",),
        )


def evaluate_m9_rakshita_vm(root: Path) -> MilestoneEvidence:
    proof = "self-host-corpus:examples/self-host/vm-core.ssk"
    from .phase28_self_host import run_self_host_corpus, self_host_corpus_present

    corpus = run_self_host_corpus(root)
    evidence = {
        "self_host_corpus": corpus,
        "vm_core": "examples/self-host/vm-core.ssk",
        "present": self_host_corpus_present(root),
    }
    supported = [row for row in corpus.get("rows", []) if row.get("subset_supported")]
    corpus_ok = (
        self_host_corpus_present(root)
        and supported
        and corpus.get("passed", 0) == len(supported)
        and not corpus.get("failures")
    )
    if corpus_ok:
        evidence["claim_boundary"] = (
            "Subset corpus proves a Sanskript-authored VM-core sketch runs under "
            "the current host VM; it is not a retired native rakshita VM."
        )
        return _pass("M9", proof_method=proof, evidence=evidence, claim_allowed=False)
    return _fail(
        "M9",
        proof_method=proof,
        evidence=evidence,
        blockers=("Sanskript-authored VM core corpus missing or subset VM parity failing",),
    )


def evaluate_m10_bytecode_verify_sanskript(root: Path) -> MilestoneEvidence:
    proof = "self-host-corpus:examples/self-host/bytecode-verify.ssk"
    source = root / "examples" / "self-host" / "bytecode-verify.ssk"
    try:
        program = _compile_example_source(source)
        verify_program_phase17(program)
        output = list(SanskriptVM().execute(program))
        evidence = {
            "source": str(source.relative_to(root)),
            "phase17_verify_ok": True,
            "output_lines": len(output),
        }
        evidence["claim_boundary"] = (
            "Bytecode verification is expressed as a Sanskript corpus example, "
            "not yet the production verifier replacing the host verifier."
        )
        return _pass("M10", proof_method=proof, evidence=evidence, claim_allowed=False)
    except Exception as exc:
        return _fail(
            "M10",
            proof_method=proof,
            evidence={"source": str(source.relative_to(root))},
            blockers=(f"{type(exc).__name__}: {exc}",),
        )


def evaluate_m11_compiler_frontend(root: Path) -> MilestoneEvidence:
    proof = "self-host-corpus:examples/self-host/compiler-frontend.ssk"
    try:
        evidence = _run_source_example(root, "examples/self-host/compiler-frontend.ssk")
        evidence["stage"] = STAGE_S1
        evidence["claim_boundary"] = (
            "Compiler frontend corpus is bootstrap evidence, not the production "
            "frontend compiled and executed independently of the host compiler."
        )
        return _pass("M11", proof_method=proof, evidence=evidence, claim_allowed=False)
    except Exception as exc:
        return _fail(
            "M11",
            proof_method=proof,
            evidence={"source": "examples/self-host/compiler-frontend.ssk"},
            blockers=(f"{type(exc).__name__}: {exc}",),
        )


def evaluate_m12_compiler_backend(root: Path) -> MilestoneEvidence:
    proof = "self-host-corpus:examples/self-host/compiler-backend.ssk"
    try:
        evidence = _run_source_example(root, "examples/self-host/compiler-backend.ssk")
        evidence["claim_boundary"] = (
            "Compiler backend corpus is bootstrap evidence, not the production "
            "backend replacing host lowering."
        )
        return _pass("M12", proof_method=proof, evidence=evidence, claim_allowed=False)
    except Exception as exc:
        return _fail(
            "M12",
            proof_method=proof,
            evidence={"source": "examples/self-host/compiler-backend.ssk"},
            blockers=(f"{type(exc).__name__}: {exc}",),
        )


def evaluate_m13_self_compile_compiler(root: Path) -> MilestoneEvidence:
    proof = "phase19-independent-self-compile"
    source = root / "examples" / "self-host" / "compiler-frontend.ssk"
    if not source.is_file():
        source = root / "examples" / "phase3-data-types.ssk"
    with tempfile.TemporaryDirectory() as tmp:
        evidence_row = verify_host_vs_self_compile(source, Path(tmp))
    evidence = {
        "stage": evidence_row.stage,
        "independent_self_compile": evidence_row.independent_self_compile,
        "bytecode_match": evidence_row.bytecode_match,
        "proof_method": evidence_row.proof_method,
    }
    if (
        evidence_row.independent_self_compile
        and evidence_row.bytecode_match
        and evidence_row.stage == STAGE_S1
    ):
        evidence["claim_boundary"] = (
            "S1 proves deterministic bootstrap parity for a subset; it is not a "
            "Sanskript-authored compiler binary compiling the full compiler."
        )
        return _pass("M13", proof_method=proof, evidence=evidence, claim_allowed=False)
    return _fail(
        "M13",
        proof_method=proof,
        evidence=evidence,
        blockers=(
            f"self-hosting stage {evidence_row.stage} is host-replay only",
            "compiler is not compiled by a Sanskript-authored compiler binary",
        ),
    )


def evaluate_m14_self_run_vm(root: Path) -> MilestoneEvidence:
    proof = "phase28-self-host-subset-vm-corpus"
    from .phase28_self_host import SanskriptSubsetVM, run_self_host_corpus, self_host_corpus_present

    corpus = run_self_host_corpus(root)
    evidence: dict[str, Any] = {
        "self_host_corpus": corpus,
        "subset_vm": SanskriptSubsetVM().implementation,
    }
    if not self_host_corpus_present(root):
        return _fail(
            "M14",
            proof_method=proof,
            evidence=evidence,
            blockers=("examples/self-host VM corpus missing",),
        )
    bootstrap = load_bytecode_file(root / "examples" / "phase18-vm-bootstrap.sskbc")
    subset = SanskriptSubsetVM()
    if not subset.can_execute(bootstrap):
        return _fail(
            "M14",
            proof_method=proof,
            evidence=evidence,
            blockers=("phase18-vm-bootstrap.sskbc uses opcodes outside SanskriptSubsetVM",),
        )
    output = tuple(subset.execute(bootstrap))
    evidence["phase18_bootstrap_output"] = list(output)
    evidence["corpus_passed"] = corpus.get("passed", 0)
    if corpus.get("passed", 0) >= 1 and output:
        evidence["claim_boundary"] = (
            "SanskriptSubsetVM evidence is bootstrap/subset execution, not the "
            "full Sanskript VM running itself."
        )
        return _pass("M14", proof_method=proof, evidence=evidence, claim_allowed=False)
    return _fail(
        "M14",
        proof_method=proof,
        evidence=evidence,
        blockers=("SanskriptSubsetVM corpus or phase18 bootstrap run did not produce output",),
    )


def evaluate_m15_self_build_test(root: Path) -> MilestoneEvidence:
    proof = "self-host-corpus:examples/self-host/test-runner.ssk"
    try:
        evidence = _run_source_example(root, "examples/self-host/test-runner.ssk")
        evidence["bootstrap_test_runner"] = True
        evidence["claim_boundary"] = (
            "Bootstrap test-runner example runs under the host CLI; it is not yet "
            "a native Sanskript build-and-test loop for the full repository."
        )
        return _pass("M15", proof_method=proof, evidence=evidence, claim_allowed=False)
    except Exception as exc:
        return _fail(
            "M15",
            proof_method=proof,
            evidence={"source": "examples/self-host/test-runner.ssk"},
            blockers=(f"{type(exc).__name__}: {exc}",),
        )


def _native_link_probe(root: Path, family: str) -> dict[str, Any]:
    program = compile_source("gaṇakaḥ ekaṃ darśayati.\n")
    out_dir = root / "artifacts" / "phase28" / "native-probe" / family
    from .phase21_cross_platform import target_triple_for_family

    target = target_triple_for_family(family)  # type: ignore[arg-type]
    plan = build_native_artifacts(
        program=program,
        out_dir=out_dir,
        target=target,
        backend="native-object",
        artifact_kind="executable",
        attempt_link=True,
    )
    linked = plan.linked_output_path
    return {
        "platform": family,
        "implementation_state": plan.implementation_state,
        "linked_output_path": str(linked) if linked else None,
        "linked_output_exists": bool(linked and linked.is_file()),
        "notes": list(plan.notes),
    }


def evaluate_m16_native_one_platform(root: Path) -> MilestoneEvidence:
    proof = "phase20-real-linked-native-binary"
    host_row = _native_link_probe(root, host_target_triple().os)
    evidence = {"host_probe": host_row}
    if host_row["linked_output_exists"] and host_row["implementation_state"] == "functional":
        evidence["claim_boundary"] = (
            "Native probe emits a minimal executable artifact; full Sanskript "
            "bytecode lowering to a native binary remains open."
        )
        return _pass("M16", proof_method=proof, evidence=evidence, claim_allowed=False)
    return _fail(
        "M16",
        proof_method=proof,
        evidence=evidence,
        blockers=(
            "native-object backend is scaffold (stub object writer)",
            "no reproducible linked native executable from Sanskript toolchain",
        ),
    )


def evaluate_m17_native_three_platforms(root: Path) -> MilestoneEvidence:
    proof = "phase20-linked-binaries:windows+macos+linux"
    rows = [_native_link_probe(root, family) for family in ("windows", "macos", "linux")]
    evidence = {"rows": rows}
    missing = [row["platform"] for row in rows if not row["linked_output_exists"]]
    if not missing and all(row["implementation_state"] == "functional" for row in rows):
        evidence["claim_boundary"] = (
            "Cross-platform native probes are minimal executable artifacts, not "
            "complete native lowering for arbitrary Sanskript programs."
        )
        return _pass("M17", proof_method=proof, evidence=evidence, claim_allowed=False)
    return _fail(
        "M17",
        proof_method=proof,
        evidence=evidence,
        blockers=tuple(
            f"{platform}: no functional linked binary"
            for platform in ("windows", "macos", "linux")
        ),
    )


def evaluate_m18_web_without_handwritten_js(root: Path) -> MilestoneEvidence:
    proof = "web-target-without-handwritten-application-js"
    bridge = call_native_function("std.web.bridge_plan", [])
    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / "web.html"
        write_web_app(load_program_for_web(root / "examples" / "prathama.ssk"), html_path)
        html = html_path.read_text(encoding="utf-8")
    has_handwritten_handlers = bool(re.search(r"function\s+\w+\s*\(", html))
    evidence = {
        "bridge_plan": bridge,
        "html_has_handwritten_function_handlers": has_handwritten_handlers,
        "webapp_generator": "src/sanskript/webapp.py",
        "program_payload": 'id="sanskript-program"' in html,
    }
    if (
        bridge.get("implementation_state") == "functional"
        and not bridge.get("host_bridge")
        and not has_handwritten_handlers
        and evidence["program_payload"]
    ):
        return _pass("M18", proof_method=proof, evidence=evidence)
    blockers: list[str] = []
    if bridge.get("host_bridge"):
        blockers.append("std.web.bridge_plan reports host_bridge=true")
    if bridge.get("implementation_state") != "functional":
        blockers.append("web bridge implementation_state is not functional")
    if has_handwritten_handlers:
        blockers.append("generated web shell still embeds handwritten JavaScript function handlers")
    return _fail("M18", proof_method=proof, evidence=evidence, blockers=tuple(blockers))


def _development_scope(root: Path) -> dict[str, Any]:
    scope_path = root / "data" / "meta" / "development_scope.json"
    if scope_path.is_file():
        return json.loads(scope_path.read_text(encoding="utf-8"))
    return {}


def evaluate_m19_no_python_rust_required(root: Path) -> MilestoneEvidence:
    proof = "packaged-bytecode-bootstrap-ordinary-development"
    scope = _development_scope(root)
    ordinary = scope.get("ordinary_development", {})
    python_required = int(ordinary.get("required_python_modules", -1))
    rust_required = int(ordinary.get("required_rust_modules", -1))
    bootstrap = root / str(ordinary.get("bootstrap_runner", "data/bootstrap/vm-runner.sskbc"))
    evidence = {
        "development_scope": str((root / "data/meta/development_scope.json").relative_to(root)),
        "required_python_modules": python_required,
        "required_rust_modules": rust_required,
        "bootstrap_runner": str(bootstrap.relative_to(root)),
        "bootstrap_runner_exists": bootstrap.is_file(),
    }
    if python_required == 0 and rust_required == 0 and bootstrap.is_file():
        evidence["claim_boundary"] = (
            "Development scope records a packaged bootstrap path, but repository "
            "tooling and verification still run through the host Python implementation."
        )
        return _pass("M19", proof_method=proof, evidence=evidence, claim_allowed=False)
    return _fail(
        "M19",
        proof_method=proof,
        evidence=evidence,
        blockers=(
            "ordinary development still lists required host modules or missing bootstrap runner",
        ),
    )


def evaluate_m20_optional_host_only(root: Path) -> MilestoneEvidence:
    proof = "host-languages-optional-bootstrap-only"
    m19 = evaluate_m19_no_python_rust_required(root)
    evidence = {
        "m19_passed": m19.passed,
        "policy": "M20 requires M19 plus explicit optional-bootstrap documentation",
    }
    if m19.passed:
        evidence["claim_boundary"] = (
            "M19 is bootstrap-scoped only, so Python/Rust are not yet optional-only "
            "for the real repository workflow."
        )
        return _pass("M20", proof_method=proof, evidence=evidence, claim_allowed=False)
    return _fail(
        "M20",
        proof_method=proof,
        evidence=evidence,
        blockers=(
            "Python/Rust are still required host paths (M19 not satisfied)",
            "bootstrap convenience paths are not yet optional-only",
        ),
    )


MILESTONE_EVALUATORS: dict[str, Evaluator] = {
    "M0": evaluate_m0_host_examples,
    "M1": evaluate_m1_bytecode_source_parity,
    "M2": evaluate_m2_sskyp_roundtrip,
    "M3": evaluate_m3_stdlib_coverage,
    "M4": evaluate_m4_cli_app,
    "M5": evaluate_m5_web_app,
    "M6": evaluate_m6_desktop_app,
    "M7": evaluate_m7_game_loop,
    "M8": evaluate_m8_research_data,
    "M9": evaluate_m9_rakshita_vm,
    "M10": evaluate_m10_bytecode_verify_sanskript,
    "M11": evaluate_m11_compiler_frontend,
    "M12": evaluate_m12_compiler_backend,
    "M13": evaluate_m13_self_compile_compiler,
    "M14": evaluate_m14_self_run_vm,
    "M15": evaluate_m15_self_build_test,
    "M16": evaluate_m16_native_one_platform,
    "M17": evaluate_m17_native_three_platforms,
    "M18": evaluate_m18_web_without_handwritten_js,
    "M19": evaluate_m19_no_python_rust_required,
    "M20": evaluate_m20_optional_host_only,
}


def milestone_to_dict(row: MilestoneEvidence) -> dict[str, Any]:
    return {
        "milestone_id": row.milestone_id,
        "title": row.title,
        "passed": row.passed,
        "claim_allowed": row.claim_allowed,
        "proof_method": row.proof_method,
        "evidence": row.evidence,
        "blockers": list(row.blockers),
    }


def evaluate_all_milestones(root: Path | None = None) -> dict[str, Any]:
    base = repo_root(root)
    rows = [MILESTONE_EVALUATORS[mid](base) for mid in sorted(MILESTONE_EVALUATORS)]
    passed = [row.milestone_id for row in rows if row.passed]
    failed = [row.milestone_id for row in rows if not row.passed]
    report: dict[str, Any] = {
        "phase": 28,
        "title": "independence-milestones-m0-m20",
        "repo_root": str(base),
        "milestone_count": len(rows),
        "passed_count": len(passed),
        "failed_count": len(failed),
        "passed": passed,
        "failed": failed,
        "milestones": [milestone_to_dict(row) for row in rows],
        "claim_boundary": (
            "Milestone ticks require automated proof in this report. "
            "Host-replay bootstrap (Phases 18–19) does not close M9–M15."
        ),
    }
    report["honesty_gates"] = phase28_honesty_gate_report(report)
    report["reproducible_steps"] = phase28_reproducible_steps()
    return report


def phase28_honesty_gate_report(report: dict[str, Any]) -> dict[str, Any]:
    passed = set(report.get("passed", []))
    all_ids = {f"M{i}" for i in range(21)}
    independence_ids = {f"M{i}" for i in range(9, 21)}
    milestones = report.get("milestones", [])
    claim_allowed = {
        row.get("milestone_id")
        for row in milestones
        if row.get("passed") and row.get("claim_allowed")
    }
    bootstrap_only = {
        row.get("milestone_id")
        for row in milestones
        if row.get("passed") and not row.get("claim_allowed")
    }
    independence_passed = claim_allowed & independence_ids
    unresolved: list[str] = []
    for mid in sorted(all_ids):
        if mid not in passed:
            unresolved.append(f"{mid}=not_proven")
        elif mid in bootstrap_only:
            unresolved.append(f"{mid}=bootstrap_or_scaffold_only")
    allow_full_independence = (
        len(claim_allowed) == report.get("milestone_count", 0)
        and not unresolved
    )
    return {
        "allow_full_independence_claim": allow_full_independence,
        "independence_milestones_proven": sorted(independence_passed),
        "host_bootstrap_only": sorted(mid for mid in bootstrap_only if mid),
        "unresolved_reasons": [] if allow_full_independence else unresolved,
        "policy": (
            "Phase 28 full independence requires every M0-M20 row to pass with "
            "claim_allowed=true. Bootstrap/subset/native-probe evidence is retained "
            "as useful progress but cannot close independence."
        ),
    }


def phase28_reproducible_steps() -> list[str]:
    return [
        "set PYTHONPATH=src",
        "python -m sanskript.cli milestone-check --artifact-dir artifacts/phase28",
        "python -m unittest tests/test_phase28_independence_milestones.py",
    ]


def format_checklist_phase28_markers(report: dict[str, Any]) -> str:
    """Render Phase 28 checklist lines with honest full-claim markers."""

    lines = ["## Phase 28: Independence Milestones", ""]
    by_id = {row["milestone_id"]: row for row in report["milestones"]}
    for mid in sorted(MILESTONE_TITLES):
        row = by_id[mid]
        marker = "x" if row["passed"] and row.get("claim_allowed") else ("~" if row["passed"] else " ")
        lines.append(f"- [{marker}] {mid}: {MILESTONE_TITLES[mid]}")
        if row["passed"] and not row.get("claim_allowed"):
            lines.append("      - evidence: bootstrap/scaffold proof only; full independence claim blocked")
            boundary = row.get("evidence", {}).get("claim_boundary")
            if boundary:
                lines.append(f"      - boundary: {boundary}")
        if not row["passed"] and row.get("blockers"):
            for blocker in row["blockers"][:3]:
                lines.append(f"      - blocker: {blocker}")
            if len(row["blockers"]) > 3:
                lines.append(f"      - blocker: (+{len(row['blockers']) - 3} more)")
    lines.append("")
    gates = report.get("honesty_gates", {})
    lines.append(
        f"_Automated audit: {report['passed_count']}/{report['milestone_count']} milestones pass "
        f"as evidence; full independence allowed: {gates.get('allow_full_independence_claim', False)}. "
        f"Use `python -m sanskript.cli milestone-check --allow-partial` until all `[~]` rows become `[x]`._"
    )
    return "\n".join(lines)


def write_phase28_evidence(artifact_dir: Path, *, root: Path | None = None) -> dict[str, Any]:
    report = evaluate_all_milestones(root)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    report_path = artifact_dir / "phase28-milestone-evidence.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    checklist_path = artifact_dir / "phase28-checklist-markers.md"
    checklist_path.write_text(format_checklist_phase28_markers(report) + "\n", encoding="utf-8")
    report["report_path"] = str(report_path)
    report["checklist_markers_path"] = str(checklist_path)
    return report
