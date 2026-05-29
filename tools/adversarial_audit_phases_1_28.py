"""Adversarial integration audit for Phases 1–28 and global gates."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "artifacts" / "adversarial-audit"


@dataclass
class StepResult:
    name: str
    command: list[str]
    exit_code: int
    ok: bool
    stdout_tail: str
    stderr_tail: str
    timed_out: bool = False
    timeout_seconds: int = 300


def _tail(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    return "\n".join(value.splitlines()[-20:])


def _run(name: str, cmd: list[str], *, cwd: Path = ROOT, timeout_seconds: int = 300) -> StepResult:
    env = dict(**{k: v for k, v in __import__("os").environ.items()})
    env["PYTHONPATH"] = str(ROOT / "src")
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        return StepResult(
            name=name,
            command=cmd,
            exit_code=124,
            ok=False,
            stdout_tail=_tail(exc.stdout),
            stderr_tail=_tail(exc.stderr) or f"timed out after {timeout_seconds}s",
            timed_out=True,
            timeout_seconds=timeout_seconds,
        )
    return StepResult(
        name=name,
        command=cmd,
        exit_code=proc.returncode,
        ok=proc.returncode == 0,
        stdout_tail=_tail(proc.stdout),
        stderr_tail=_tail(proc.stderr),
        timeout_seconds=timeout_seconds,
    )


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    steps: list[StepResult] = []

    gates = [
        ("gate_no_placeholder", [py, "tools/check_no_placeholder_completion.py"]),
        ("gate_feature_completion", [py, "tools/check_feature_completion.py"]),
        ("gate_register_docs", [py, "-m", "pytest", "tests/test_register_docs.py", "-q"]),
        ("gate_completion", [py, "-m", "pytest", "tests/test_completion_gate.py", "-q"]),
        ("gate_phase0_truth", [py, "-m", "pytest", "tests/test_phase0_truth_gates.py", "-q"]),
    ]
    for name, cmd in gates:
        steps.append(_run(name, cmd))

    phase_batches = [
        ("phases_1_5", "tests/test_phase1_source_surface.py tests/test_phase2_core_syntax.py tests/test_phase3_data_types.py tests/test_phase4_type_system.py tests/test_phase5_control_flow.py"),
        ("phases_6_10", "tests/test_phase6_functions.py tests/test_phase7_oop.py tests/test_phase8_functional_declarative.py tests/test_phase9_modules.py tests/test_phase10_stdlib_core.py tests/test_phase_examples.py"),
        ("phases_11_15", "tests/test_phase11_algorithms_data_structures.py tests/test_phase12_diagnostics.py tests/test_phase13_memory_model.py tests/test_phase14_surakshita.py tests/test_phase15_rakshita_systems.py"),
        ("phases_16_20", "tests/test_phase16_arakshita.py tests/test_phase17_toolchain.py tests/test_phase18_vm_runtime.py tests/test_phase19_self_hosting.py tests/test_phase20_native_backends.py tests/test_native_backends.py tests/test_native_levels.py tests/test_vm_numeric_heap.py"),
        ("phases_21_28", "tests/test_phase21_cross_platform.py tests/test_phase22_web_apps_games_research_ml.py tests/test_phase22_web_apps_games_research.py tests/test_phase23_concurrency_async.py tests/test_phase24_tooling.py tests/test_phase25_testing_verification.py tests/test_phase25_exhaustive_coverage.py tests/test_phase25_borrow_negatives.py tests/test_phase26_documentation.py tests/test_phase27_migration.py tests/test_phase28_independence_milestones.py"),
        ("supporting_core", "tests/test_cli_toolchain.py tests/test_compiler_vm.py tests/test_bytecode_conformance.py tests/test_errors.py tests/test_performance_baseline.py tests/test_webapp_export.py"),
    ]
    for name, targets in phase_batches:
        cmd = [py, "-m", "pytest", *targets.split(), "-q", "--tb=no"]
        steps.append(_run(name, cmd))

    cli_seals = [
        ("cli_phase21_seal", [py, "-m", "sanskript.cli", "phase21-seal-check"]),
        ("cli_phase23_seal", [py, "-m", "sanskript.cli", "phase23-seal"]),
        ("cli_phase24_check", [py, "-m", "sanskript.cli", "phase24-check", "--out-dir", "artifacts/phase24", "--sample-source", "examples/phase24-tooling.ssk"]),
        ("cli_phase25_evidence", [py, "-m", "sanskript.cli", "phase25-evidence"]),
        ("cli_phase26_evidence", [py, "-m", "sanskript.cli", "phase26-evidence"]),
        ("cli_migration_report", [py, "-m", "sanskript.cli", "migration-report"]),
        ("cli_migration_seal", [py, "-m", "sanskript.cli", "migration-seal"]),
        (
            "cli_milestone_check_partial_honesty",
            [
                py,
                "-m",
                "sanskript.cli",
                "milestone-check",
                "--artifact-dir",
                "artifacts/phase28",
                "--allow-partial",
            ],
        ),
        ("cli_self_host_check", [py, "-m", "sanskript.cli", "self-host-check", "examples/phase3-data-types.ssk", "--allow-host-replay"]),
        (
            "cli_phase18_vm_check",
            [
                py,
                "-m",
                "sanskript.cli",
                "phase18-vm-check",
                "examples/phase3-data-types.ssk",
                "--artifact-dir",
                "artifacts/phase18",
                "--allow-host-fallback",
            ],
        ),
        ("cli_phase20_evidence", [py, "-m", "sanskript.cli", "phase20-evidence", "examples/phase6-functions.ssk", "--out-dir", "artifacts/phase20/evidence", "--plan-json", "artifacts/phase20/evidence/phase20-evidence.json"]),
    ]
    for name, cmd in cli_seals:
        steps.append(_run(name, cmd))

    adversarial = [
        ("adv_phase21_anti_fake", [py, "-m", "pytest", "tests/test_phase21_cross_platform.py::Phase21AntiFakeTests", "-q"]),
        ("adv_phase22_seal_run", [py, "-m", "sanskript.cli", "run", "examples/phase22-full-seal.ssk"]),
        ("adv_phase23_full_seal", [py, "-m", "sanskript.cli", "run", "examples/phase23-full-seal.ssk"]),
        (
            "adv_phase24_anti_fake",
            [py, "-m", "pytest", "tests/test_phase24_tooling.py::Phase24ChecklistSealTests", "-q"],
        ),
        ("adv_phase25_exhaustive", [py, "-m", "pytest", "tests/test_phase25_exhaustive_coverage.py", "-q", "--maxfail=1"]),
        (
            "adv_phase27_no_ported",
            [
                py,
                "-m",
                "pytest",
                "tests/test_phase27_migration.py::Phase27MigrationReportTests::test_no_component_marked_ported",
                "-q",
            ],
        ),
        ("adv_phase28_inflation", [py, "-m", "pytest", "tests/test_phase28_independence_milestones.py", "-q"]),
        ("adv_all_examples_compile", [py, "-m", "pytest", "tests/test_cli_toolchain.py::CliToolchainTests::test_all_examples_compile_to_portable_bytecode", "-q"]),
    ]
    for name, cmd in adversarial:
        steps.append(_run(name, cmd))

    steps.append(_run("full_pytest_suite", [py, "-m", "pytest", "-q", "--tb=line"], timeout_seconds=900))

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(ROOT),
        "summary": {
            "total": len(steps),
            "passed": sum(1 for s in steps if s.ok),
            "failed": sum(1 for s in steps if not s.ok),
        },
        "steps": [asdict(s) for s in steps],
        "failures": [asdict(s) for s in steps if not s.ok],
    }
    json_path = OUT_DIR / "report.json"
    md_path = OUT_DIR / "report.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Adversarial Audit Phases 1–28",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        f"**Passed:** {payload['summary']['passed']}/{payload['summary']['total']}",
        "",
    ]
    if payload["failures"]:
        lines.append("## Failures")
        lines.append("")
        for f in payload["failures"]:
            lines.append(f"### {f['name']} (exit {f['exit_code']})")
            lines.append(f"```")
            lines.append(f["command"])
            lines.append("```")
            if f["stderr_tail"]:
                lines.append("stderr tail:")
                lines.append("```")
                lines.append(f["stderr_tail"])
                lines.append("```")
            lines.append("")
    else:
        lines.append("All steps passed.")
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(payload["summary"], indent=2))
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0 if payload["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
