"""Phase 28: honest independence milestone evaluation (M0–M20).

Evaluates milestone status from executable evidence only. Host-replay (Phase 19
S0) and host-fallback VM bootstrap (Phase 18) must never satisfy M13–M15.
An empty program corpus must never satisfy M14.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from .bytecode import BytecodeProgram, Instruction, OpCode
from .compiler import compile_program
from .module_loader import load_program_from_path
from .phase17_toolchain import opcode_machine_prose_evidence
from .phase18_vm_runtime import (
    phase18_honesty_gate_report,
    retirement_readiness_report,
    write_phase18_bootstrap_evidence,
)
from .phase20_native_evidence import Phase20EvidenceRequest, generate_phase20_evidence
from .phase28_milestones import MILESTONE_EVALUATORS
from .self_hosting import STAGE_ID as HOST_REPLAY_STAGE, verify_host_vs_self_compile

MilestoneStatus = Literal["not_met", "bootstrap", "met"]

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLES_DIR = REPO_ROOT / "examples"
MODULE_INVENTORY_PATH = REPO_ROOT / "data" / "meta" / "module_inventory.json"

HIGH_MILESTONES = tuple(f"M{n}" for n in range(13, 21))
HOST_REPLAY_BLOCKED_MILESTONES = frozenset({"M13", "M14", "M15"})
SCAFFOLD_NATIVE_BLOCKED = frozenset({"M16", "M17", "M18"})

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
    "M9": "Sanskript can implement the VM core in rakshita",
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
class MilestoneEvaluation:
    milestone_id: str
    title: str
    status: MilestoneStatus
    claim_allowed: bool
    blocked_reasons: tuple[str, ...]
    evidence_refs: tuple[str, ...]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_corpus_programs() -> list[BytecodeProgram]:
    """Minimal reproducible corpus used for VM retirement gates."""

    return [
        BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
    ]


def load_corpus_from_paths(paths: list[Path]) -> list[BytecodeProgram]:
    programs: list[BytecodeProgram] = []
    for path in paths:
        if path.suffix == ".sskbc":
            from .bytecode import load_bytecode_file

            programs.append(load_bytecode_file(path))
        elif path.suffix == ".ssk":
            programs.append(compile_program(load_program_from_path(path)))
        elif path.suffix == ".sskyp":
            from .yantra_patha import program_from_yantra_patha

            programs.append(program_from_yantra_patha(path.read_text(encoding="utf-8")))
    return programs


def _inventory_summary() -> dict[str, Any]:
    if not MODULE_INVENTORY_PATH.exists():
        return {"module_count": 0, "python_count": 0, "rust_count": 0}
    payload = json.loads(MODULE_INVENTORY_PATH.read_text(encoding="utf-8"))
    return {
        "module_count": payload.get("module_count", 0),
        "python_count": payload.get("python_count", 0),
        "rust_count": payload.get("rust_count", 0),
    }


def _host_replay_active(*, phase19_rows: list[Any] | None) -> bool:
    if phase19_rows:
        return any(not row.independent_self_compile for row in phase19_rows)
    return True


def _evaluate_m13(*, host_replay: bool, phase19_seed: dict[str, Any] | None) -> MilestoneEvaluation:
    blockers: list[str] = []
    refs: list[str] = []
    s1_ok = False
    if phase19_seed:
        refs.append("phase19/bootstrap_seed.json")
        contract = phase19_seed.get("determinism_contract", {})
        porting = phase19_seed.get("porting_path", {})
        s1_ok = (
            contract.get("independent_self_hosting")
            and contract.get("claim_level") == "s1-self-host-subset"
            and porting.get("current_stage") != HOST_REPLAY_STAGE
        )
    if s1_ok:
        return MilestoneEvaluation(
            "M13",
            MILESTONE_TITLES["M13"],
            "bootstrap",
            False,
            (),
            tuple(refs),
        )
    if host_replay:
        blockers.append("S0-host-replay cannot claim M13 (independent compiler self-compile required)")
    if phase19_seed:
        contract = phase19_seed.get("determinism_contract", {})
        if contract.get("claim_level") == "host-replay-only":
            blockers.append("determinism_contract.claim_level=host-replay-only")
        if not contract.get("independent_self_hosting"):
            blockers.append("independent_self_hosting=false")
        porting = phase19_seed.get("porting_path", {})
        if porting.get("current_stage") == HOST_REPLAY_STAGE:
            blockers.append(f"porting_path.current_stage={HOST_REPLAY_STAGE}")
    else:
        blockers.append("no Phase 19 bootstrap seed with S1+ independent self-compile evidence")
    return MilestoneEvaluation(
        "M13",
        MILESTONE_TITLES["M13"],
        "not_met",
        False,
        tuple(blockers),
        tuple(refs),
    )


def _evaluate_m14(*, corpus_size: int, phase18_gates: dict[str, Any]) -> MilestoneEvaluation:
    blockers: list[str] = []
    refs = ["phase18/vm-runtime-self-hosting"]
    if corpus_size == 0:
        blockers.append("empty program corpus: M14 requires a non-empty reproducible corpus")
    if phase18_gates.get("allow_independence_claim"):
        return MilestoneEvaluation(
            "M14",
            MILESTONE_TITLES["M14"],
            "bootstrap",
            False,
            (),
            tuple(refs),
        )
    if not phase18_gates.get("allow_independence_claim"):
        blockers.extend(phase18_gates.get("unresolved_reasons", ()))
        if not blockers:
            blockers.append("phase18 honesty gates disallow independence claim")
    return MilestoneEvaluation(
        "M14",
        MILESTONE_TITLES["M14"],
        "not_met",
        False,
        tuple(blockers),
        tuple(refs),
    )


def _evaluate_m15(*, host_replay: bool, inventory: dict[str, Any]) -> MilestoneEvaluation:
    scope_path = REPO_ROOT / "data" / "meta" / "development_scope.json"
    bootstrap_ok = False
    if scope_path.is_file():
        scope = json.loads(scope_path.read_text(encoding="utf-8"))
        ordinary = scope.get("ordinary_development", {})
        bootstrap_ok = (
            int(ordinary.get("required_python_modules", -1)) == 0
            and (REPO_ROOT / str(ordinary.get("bootstrap_runner", ""))).is_file()
        )
    if bootstrap_ok:
        return MilestoneEvaluation(
            "M15",
            MILESTONE_TITLES["M15"],
            "bootstrap",
            False,
            (),
            ("examples/self-host/test-runner.ssk", "data/bootstrap/vm-runner.sskbc"),
        )
    blockers: list[str] = []
    if host_replay:
        blockers.append("host-replay cannot claim M15 (native Sanskript build+test loop required)")
    if inventory.get("python_count", 0) > 0:
        blockers.append(
            f"host pytest/tooling still required ({inventory['python_count']} Python modules inventoried)"
        )
    blockers.append("native Sanskript test runner not yet executing the full regression matrix")
    return MilestoneEvaluation(
        "M15",
        MILESTONE_TITLES["M15"],
        "not_met",
        False,
        tuple(blockers),
        tuple(("tests/", "tools/generate_module_inventory.py")),
    )


def _phase20_functional_linked(row: dict[str, Any]) -> bool:
    if row.get("backend") != "native-object":
        return False
    if row.get("implementation_state") != "functional":
        return False
    linked = row.get("linked_output_path")
    return bool(linked) and Path(str(linked)).is_file()


def _evaluate_m16_m17(*, phase20_rows: list[dict[str, Any]] | None) -> tuple[MilestoneEvaluation, MilestoneEvaluation]:
    blockers_common: list[str] = []
    linked = False
    if phase20_rows:
        linked = any(_phase20_functional_linked(row) for row in phase20_rows)
    if linked:
        m16 = MilestoneEvaluation(
            "M16",
            MILESTONE_TITLES["M16"],
            "bootstrap",
            False,
            (),
            ("phase20/native-backends",),
        )
    else:
        blockers_common = [
            "Phase 20 native-object backend remains scaffold/plan-only",
            "no functional linked native executable on any target",
        ]
        m16 = MilestoneEvaluation(
            "M16",
            MILESTONE_TITLES["M16"],
            "not_met",
            False,
            tuple(blockers_common),
            ("phase20/native-backends",),
        )
    cross_targets = {"windows", "linux", "darwin"}
    seen = set()
    if phase20_rows:
        for row in phase20_rows:
            target = str(row.get("target", ""))
            for token in cross_targets:
                if token in target:
                    seen.add(token)
    cross_linked = set()
    if phase20_rows:
        for row in phase20_rows:
            if not _phase20_functional_linked(row):
                continue
            target = str(row.get("target", ""))
            for token in cross_targets:
                if token in target:
                    cross_linked.add(token)
    if len(cross_linked) >= 3:
        m17 = MilestoneEvaluation(
            "M17",
            MILESTONE_TITLES["M17"],
            "bootstrap",
            False,
            (),
            ("phase20/native-backends",),
        )
    else:
        m17_blockers = list(blockers_common)
        m17_blockers.append(
            f"linked native binaries required for Windows/macOS/Linux (targets seen: {sorted(cross_linked)})"
        )
        m17 = MilestoneEvaluation(
            "M17",
            MILESTONE_TITLES["M17"],
            "not_met",
            False,
            tuple(m17_blockers),
            ("phase20/native-backends",),
        )
    return m16, m17


def _executable_status(*, passed: bool, claim_allowed: bool) -> MilestoneStatus:
    if passed and claim_allowed:
        return "met"
    if passed:
        return "bootstrap"
    return "not_met"


def _from_executable_evidence(
    row: Any,
    *,
    extra_blockers: tuple[str, ...] = (),
    extra_refs: tuple[str, ...] = (),
) -> MilestoneEvaluation:
    blockers = tuple(row.blockers) + extra_blockers
    refs = (row.proof_method,) + extra_refs
    return MilestoneEvaluation(
        row.milestone_id,
        row.title,
        _executable_status(passed=row.passed, claim_allowed=False),
        False,
        blockers,
        refs,
    )


def _evaluate_lower_milestones(*, root: Path, inventory: dict[str, Any]) -> list[MilestoneEvaluation]:
    rows: list[MilestoneEvaluation] = []
    for mid in (f"M{n}" for n in range(13)):
        rows.append(_from_executable_evidence(MILESTONE_EVALUATORS[mid](root)))

    opcode_evidence = opcode_machine_prose_evidence()
    if opcode_evidence.unsupported:
        m2 = rows[2]
        rows[2] = MilestoneEvaluation(
            m2.milestone_id,
            m2.title,
            "not_met" if m2.status == "bootstrap" else m2.status,
            False,
            m2.blocked_reasons
            + (f"{len(opcode_evidence.unsupported)} opcodes lack bijective .sskyp mapping",),
            m2.evidence_refs + ("src/sanskript/phase17_toolchain.py",),
        )

    py = int(inventory.get("python_count", 0))
    rs = int(inventory.get("rust_count", 0))
    for mid in ("M18", "M19", "M20"):
        ev = MILESTONE_EVALUATORS[mid](root)
        extra: tuple[str, ...] = ()
        if mid == "M19" and (py or rs):
            extra = (f"{py} Python + {rs} Rust modules still inventoried",)
        if mid == "M20" and not ev.passed:
            extra = ("host languages are still mandatory for ordinary development workflows",)
        rows.append(_from_executable_evidence(ev, extra_blockers=extra))
    return rows


def detect_milestone_inflation(report: dict[str, Any]) -> list[str]:
    """Return human-readable inflation violations (empty list == honest)."""

    issues: list[str] = []
    corpus_size = int(report.get("corpus", {}).get("program_count", 0))
    host_replay = bool(report.get("evidence_bundle", {}).get("host_replay_active", True))

    for row in report.get("milestones", []):
        mid = row.get("milestone_id")
        status = row.get("status")
        claim_allowed = row.get("claim_allowed")

        if status == "met" and not claim_allowed:
            issues.append(f"{mid}: status=met but claim_allowed=false")
        if status == "met" and mid not in HIGH_MILESTONES:
            issues.append(f"{mid}: host-bootstrap milestone marked met (only M13–M20 may be met)")
        if status == "met" and mid in HIGH_MILESTONES:
            issues.append(f"{mid}: high milestone marked met without independence proof")
        if mid == "M14" and status in {"met", "bootstrap"} and claim_allowed and corpus_size == 0:
            issues.append("M14: claim allowed with empty corpus")
        if mid in HOST_REPLAY_BLOCKED_MILESTONES and status == "met" and host_replay:
            issues.append(f"{mid}: met while host-replay evidence is active")
        if mid in HOST_REPLAY_BLOCKED_MILESTONES and claim_allowed and host_replay:
            issues.append(f"{mid}: claim_allowed while host-replay evidence is active")
        if mid in HOST_REPLAY_BLOCKED_MILESTONES and status == "bootstrap" and host_replay:
            issues.append(f"{mid}: bootstrap while host-replay evidence is active")
        if mid in SCAFFOLD_NATIVE_BLOCKED and status in {"met", "bootstrap"} and claim_allowed:
            issues.append(f"{mid}: native/web milestone claim without functional linked/native proof")
        if mid in SCAFFOLD_NATIVE_BLOCKED and status == "met":
            issues.append(f"{mid}: high native/web milestone marked met without functional proof")

    gates = report.get("honesty_gates", {})
    if gates.get("high_milestones_all_not_met") is False:
        issues.append("honesty_gates.high_milestones_all_not_met is false")
    return issues


def phase28_honesty_gates(report: dict[str, Any]) -> dict[str, Any]:
    inflation = detect_milestone_inflation(report)
    high_rows = [row for row in report.get("milestones", []) if row.get("milestone_id") in HIGH_MILESTONES]
    high_not_met = all(row.get("status") != "met" for row in high_rows)
    corpus_size = int(report.get("corpus", {}).get("program_count", 0))
    host_replay = bool(report.get("evidence_bundle", {}).get("host_replay_active", True))
    return {
        "seal_ready": len(inflation) == 0 and high_not_met,
        "empty_corpus_blocks_m14": corpus_size == 0
        or all(
            row.get("milestone_id") != "M14" or not row.get("claim_allowed")
            for row in report.get("milestones", [])
        ),
        "host_replay_blocks_m13_m14_m15": host_replay
        or all(
            row.get("milestone_id") not in HOST_REPLAY_BLOCKED_MILESTONES or not row.get("claim_allowed")
            for row in report.get("milestones", [])
        ),
        "high_milestones_all_not_met": high_not_met,
        "inflation_issues": inflation,
        "policy": (
            "Phase 28 seal-ready means milestone reporting is honest, not that M13–M20 are achieved. "
            "Host-replay and empty corpora must never satisfy M13–M15 claims."
        ),
    }


def _milestone_to_dict(row: MilestoneEvaluation) -> dict[str, Any]:
    return {
        "milestone_id": row.milestone_id,
        "title": row.title,
        "status": row.status,
        "claim_allowed": row.claim_allowed,
        "blocked_reasons": list(row.blocked_reasons),
        "evidence_refs": list(row.evidence_refs),
    }


def build_phase28_report(
    *,
    repo_root: Path | None = None,
    corpus_programs: list[BytecodeProgram] | None = None,
    corpus_paths: list[Path] | None = None,
    phase19_seed_path: Path | None = None,
    phase19_sources: list[Path] | None = None,
    artifact_dir: Path | None = None,
    include_phase20_probe: bool = True,
) -> dict[str, Any]:
    root = repo_root or REPO_ROOT
    examples_dir = root / "examples"
    example_ssk_count = len(list(examples_dir.glob("*.ssk"))) if examples_dir.exists() else 0
    phase10_examples = len(list(examples_dir.glob("phase10-stdlib-*.ssk"))) if examples_dir.exists() else 0

    if corpus_programs is None and corpus_paths:
        corpus_programs = load_corpus_from_paths(corpus_paths)
    if corpus_programs is None:
        corpus_programs = default_corpus_programs()

    corpus_size = len(corpus_programs)
    out_dir = artifact_dir or (root / "artifacts" / "phase28")
    out_dir.mkdir(parents=True, exist_ok=True)

    phase18_report = write_phase18_bootstrap_evidence(corpus_programs, out_dir / "phase18-probe")
    phase18_gates = phase18_report.get("honesty_gates") or phase18_honesty_gate_report(phase18_report)

    phase19_seed: dict[str, Any] | None = None
    if phase19_seed_path and phase19_seed_path.exists():
        phase19_seed = json.loads(phase19_seed_path.read_text(encoding="utf-8"))
    phase19_rows = []
    if phase19_sources:
        probe_dir = out_dir / "phase19-probe"
        for src in phase19_sources:
            phase19_rows.append(verify_host_vs_self_compile(src, probe_dir))

    host_replay = _host_replay_active(phase19_rows=phase19_rows or None)
    if phase19_seed and phase19_seed.get("determinism_contract", {}).get("claim_level") == "host-replay-only":
        host_replay = True

    opcode_evidence = opcode_machine_prose_evidence()
    inventory = _inventory_summary()

    phase20_rows: list[dict[str, Any]] | None = None
    if include_phase20_probe and corpus_programs:
        phase20_payload = generate_phase20_evidence(
            corpus_programs[0],
            request=Phase20EvidenceRequest(out_dir=out_dir / "phase20-probe"),
        )
        phase20_rows = phase20_payload.get("rows", [])

    evaluations = _evaluate_lower_milestones(root=root, inventory=inventory)
    evaluations.append(_evaluate_m13(host_replay=host_replay, phase19_seed=phase19_seed))
    evaluations.append(_evaluate_m14(corpus_size=corpus_size, phase18_gates=phase18_gates))
    evaluations.append(_evaluate_m15(host_replay=host_replay, inventory=inventory))
    m16, m17 = _evaluate_m16_m17(phase20_rows=phase20_rows)
    evaluations.extend((m16, m17))

    # Replace generic M18/M19/M20 from lower evaluator with precise rows already added
    by_id = {row.milestone_id: row for row in evaluations}
    ordered = [_milestone_to_dict(by_id[f"M{n}"]) for n in range(21)]

    report = {
        "phase": 28,
        "title": "independence-milestones-evidence",
        "generated_at": utc_now_iso(),
        "corpus": {
            "program_count": corpus_size,
            "retirement_ready": phase18_report["retirement_report"]["retirement_ready"],
            "policy": retirement_readiness_report(corpus_programs)["policy"],
        },
        "evidence_bundle": {
            "host_replay_active": host_replay,
            "phase18_honesty_gates": phase18_gates,
            "phase19_stage": (
                phase19_seed.get("porting_path", {}).get("current_stage")
                if phase19_seed
                else (phase19_rows[0].stage if phase19_rows else HOST_REPLAY_STAGE)
            ),
            "inventory": inventory,
        },
        "milestones": ordered,
    }
    report["honesty_gates"] = phase28_honesty_gates(report)
    return report


def write_phase28_report(out_path: Path, **kwargs: Any) -> dict[str, Any]:
    payload = build_phase28_report(**kwargs)
    issues = detect_milestone_inflation(payload)
    if issues:
        raise ValueError("Milestone inflation detected: " + "; ".join(issues))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload["report_path"] = str(out_path)
    return payload
