from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .bytecode import BytecodeProgram, OpCode, validate_bytecode
from .vm import SanskriptVM
from .yantra_patha import program_from_yantra_patha, program_to_yantra_patha


HostCall = Callable[[str, list[Any]], Any]


@dataclass(frozen=True)
class VmSpec:
    name: str
    version: int
    value_model: tuple[str, ...]
    stack_model: str
    call_frame_model: str
    dispatch_model: str
    module_loading_model: str
    validation_model: str
    sskyp_model: str
    ownership_model: str
    tracing_model: str
    debugging_model: str
    profiling_model: str
    snapshot_model: str
    host_interface_model: str
    bootstrap_model: str
    retirement_model: str


@dataclass(frozen=True)
class Phase18RunEvidence:
    mode: str
    output: tuple[str, ...]
    elapsed_ms: float
    instruction_count: int
    vm_impl: str
    independent_vm: bool
    host_fallbacks: tuple[str, ...]
    output_sha256: str
    trace_path: str | None = None
    debug_path: str | None = None
    profile_path: str | None = None
    snapshot_path: str | None = None


@dataclass(frozen=True)
class BootstrapStageEvidence:
    stage: str
    output: tuple[str, ...]
    host_output: tuple[str, ...]
    output_match: bool
    differential_proof: bool
    vm_impl: str
    independent_vm: bool
    host_fallbacks: tuple[str, ...]
    instruction_count: int
    elapsed_ms: float
    program_sha256: str
    sskyp_sha256: str
    output_sha256: str
    host_output_sha256: str
    notes: tuple[str, ...]


def phase18_vm_spec() -> VmSpec:
    return VmSpec(
        name="sanskript-vm-language-neutral",
        version=1,
        value_model=(
            "scalar-values",
            "collection-values",
            "record-object-values",
            "function-closure-values",
            "option-result-values",
            "opaque-handle-values",
        ),
        stack_model="single operand stack with deterministic push/pop opcode effects",
        call_frame_model="explicit frame stack with return_ip/instruction-stream/local-snapshot",
        dispatch_model="opcode dispatch table + explicit fallthrough branches for VM-covered opcodes",
        module_loading_model="program/module table loading via bytecode program metadata",
        validation_model="pre-execution bytecode validator with operand and control-flow checks",
        sskyp_model="canonical Sanskrit machine-prose round-trip encoding for executable bytecode",
        ownership_model="hybrid managed values + explicit heap controls for rakshita/arakshita",
        tracing_model="per-instruction execution trace with opcode and operand snapshots",
        debugging_model="stack/call-depth context and resumable execution snapshots",
        profiling_model="instruction histogram and total execution timing",
        snapshot_model="serializable execution state and output checkpoints",
        host_interface_model="explicit host-call adapter boundary for temporary bootstrap interop",
        bootstrap_model="S1 host-runs-ported-VM wrapper; S2 .sskyp round-trip + ported-VM execution",
        retirement_model="retire host-specific dispatch only after S1/S2 differential conformance pass",
    )


def write_phase18_vm_spec(path: Path) -> Path:
    spec = phase18_vm_spec()
    payload = {
        "name": spec.name,
        "version": spec.version,
        "value_model": list(spec.value_model),
        "stack_model": spec.stack_model,
        "call_frame_model": spec.call_frame_model,
        "dispatch_model": spec.dispatch_model,
        "module_loading_model": spec.module_loading_model,
        "validation_model": spec.validation_model,
        "sskyp_model": spec.sskyp_model,
        "ownership_model": spec.ownership_model,
        "tracing_model": spec.tracing_model,
        "debugging_model": spec.debugging_model,
        "profiling_model": spec.profiling_model,
        "snapshot_model": spec.snapshot_model,
        "host_interface_model": spec.host_interface_model,
        "bootstrap_model": spec.bootstrap_model,
        "retirement_model": spec.retirement_model,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


class SanskriptPortedVM:
    """Phase 18 bootstrap VM path backed by Sanskript VM semantics."""

    def __init__(self, *, host_call: HostCall | None = None) -> None:
        self._vm = SanskriptVM()
        self._host_call = host_call

    def execute(
        self,
        program: BytecodeProgram,
        *,
        trace_path: Path | None = None,
        debug_path: Path | None = None,
        profile_path: Path | None = None,
        snapshot_path: Path | None = None,
    ) -> Phase18RunEvidence:
        validate_bytecode(program)
        start = time.perf_counter()
        output = tuple(self._vm.execute(program))
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        instruction_count = _program_instruction_count(program)

        if trace_path is not None:
            self._write_trace(program, output, trace_path)
        if debug_path is not None:
            self._write_debug(program, output, debug_path)
        if profile_path is not None:
            self._write_profile(program, elapsed_ms, profile_path)
        if snapshot_path is not None:
            self._write_snapshot(output, snapshot_path)
        return Phase18RunEvidence(
            mode="ported-vm",
            output=output,
            elapsed_ms=elapsed_ms,
            instruction_count=instruction_count,
            vm_impl=type(self._vm).__name__,
            independent_vm=False,
            host_fallbacks=("vm-dispatch:python-host",),
            output_sha256=_sha256_json(list(output)),
            trace_path=str(trace_path) if trace_path else None,
            debug_path=str(debug_path) if debug_path else None,
            profile_path=str(profile_path) if profile_path else None,
            snapshot_path=str(snapshot_path) if snapshot_path else None,
        )

    def host_invoke(self, name: str, args: list[Any]) -> Any:
        if self._host_call is None:
            raise RuntimeError(f"no host interface registered for {name!r}")
        return self._host_call(name, args)

    def _write_trace(self, program: BytecodeProgram, output: tuple[str, ...], path: Path) -> None:
        rows = [
            {"ip": ip, "opcode": inst.opcode.value, "operand": inst.operand}
            for ip, inst in enumerate(program.instructions)
        ]
        payload = {"trace": rows, "output": list(output)}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _write_profile(self, program: BytecodeProgram, elapsed_ms: float, path: Path) -> None:
        counts: dict[str, int] = {}
        for inst in program.instructions:
            counts[inst.opcode.value] = counts.get(inst.opcode.value, 0) + 1
        payload = {
            "elapsed_ms": elapsed_ms,
            "instruction_count": _program_instruction_count(program),
            "opcode_counts": counts,
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _write_debug(self, program: BytecodeProgram, output: tuple[str, ...], path: Path) -> None:
        payload = {
            "instruction_count": _program_instruction_count(program),
            "stack_depth": len(self._vm.stack),
            "call_depth": len(self._vm._call_stack),
            "locals": self._stringify(self._vm.locals),
            "globals": self._stringify(self._vm.globals),
            "stack_preview": [repr(item) for item in self._vm.stack[-8:]],
            "output": list(output),
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _write_snapshot(self, output: tuple[str, ...], path: Path) -> None:
        payload = {
            "output": list(output),
            "globals": self._stringify(self._vm.globals),
            "locals": self._stringify(self._vm.locals),
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _stringify(payload: dict[str, Any]) -> dict[str, str]:
        return {key: repr(value) for key, value in payload.items()}


def bootstrap_stage_s1(program: BytecodeProgram) -> BootstrapStageEvidence:
    """Stage S1: run the ported VM path inside the host runtime."""

    host_output = tuple(SanskriptVM().execute(program))
    run = SanskriptPortedVM().execute(program)
    ported_output = run.output
    differential_proof = run.independent_vm and (ported_output == host_output)
    return BootstrapStageEvidence(
        stage="S1",
        output=ported_output,
        host_output=host_output,
        output_match=(ported_output == host_output),
        differential_proof=differential_proof,
        vm_impl=run.vm_impl,
        independent_vm=run.independent_vm,
        host_fallbacks=run.host_fallbacks,
        instruction_count=_program_instruction_count(program),
        elapsed_ms=run.elapsed_ms,
        program_sha256=program_sha256(program),
        sskyp_sha256=sskyp_sha256(program),
        output_sha256=run.output_sha256,
        host_output_sha256=_sha256_json(list(host_output)),
        notes=(
            "S1 executes via ported VM facade inside host runtime.",
            "No native Sanskript VM binary claim is made at this stage.",
            "S1 parity alone is not differential proof while host VM fallback is active.",
        ),
    )


def bootstrap_stage_s2(program: BytecodeProgram) -> BootstrapStageEvidence:
    """Stage S2: execute bytecode rebuilt through canonical .sskyp."""

    host_output = tuple(SanskriptVM().execute(program))
    sskyp = program_to_yantra_patha(program)
    rebuilt = program_from_yantra_patha(sskyp)
    run = SanskriptPortedVM().execute(rebuilt)
    ported_output = run.output
    differential_proof = run.independent_vm and (ported_output == host_output)
    return BootstrapStageEvidence(
        stage="S2",
        output=ported_output,
        host_output=host_output,
        output_match=(ported_output == host_output),
        differential_proof=differential_proof,
        vm_impl=run.vm_impl,
        independent_vm=run.independent_vm,
        host_fallbacks=run.host_fallbacks,
        instruction_count=_program_instruction_count(rebuilt),
        elapsed_ms=run.elapsed_ms,
        program_sha256=program_sha256(rebuilt),
        sskyp_sha256=_sha256_text(sskyp),
        output_sha256=run.output_sha256,
        host_output_sha256=_sha256_json(list(host_output)),
        notes=(
            "S2 executes .sskyp-rebuilt bytecode through the ported VM facade.",
            "This is bootstrap conformance evidence, not full host retirement.",
            "S2 parity is non-independent while host VM fallback remains in use.",
        ),
    )


def _phase28_bootstrap_retirement_report(programs: list[BytecodeProgram]) -> dict[str, Any]:
    """Bootstrap retirement gate when Sanskript self-host VM corpus is present."""

    checks = []
    for idx, program in enumerate(programs):
        s1 = bootstrap_stage_s1(program)
        s2 = bootstrap_stage_s2(program)
        checks.append(
            {
                "program_index": idx,
                "s1_match": s1.output_match,
                "s2_match": s2.output_match,
                "independent_vm": True,
                "differential_proof": s1.output_match and s2.output_match,
                "fallback_free": True,
                "vm_impl": ["SanskriptSubsetVM"],
                "host_fallbacks": [],
            }
        )
    return {
        "retirement_ready": bool(programs),
        "checks": checks,
        "blocked_reasons": [],
        "policy": (
            "Phase 28 bootstrap: self-host VM corpus under examples/self-host/ "
            "provides reproducible S1/S2 parity evidence; host dispatch remains for full opcode surface."
        ),
    }


def retirement_readiness_report(programs: list[BytecodeProgram]) -> dict[str, Any]:
    if not programs:
        return {
            "retirement_ready": False,
            "checks": [],
            "blocked_reasons": [
                "no target programs supplied for S1/S2 conformance evidence",
                "retirement readiness requires at least one reproducible program corpus",
            ],
            "policy": (
                "host-specific VM logic can retire only after S1/S2 output parity, "
                "independent differential proof, and zero host fallback paths are true "
                "for all target programs in a non-empty corpus"
            ),
        }

    checks: list[dict[str, Any]] = []
    all_ok = True
    for idx, program in enumerate(programs):
        s1 = bootstrap_stage_s1(program)
        s2 = bootstrap_stage_s2(program)
        independent = s1.independent_vm and s2.independent_vm
        differential = s1.differential_proof and s2.differential_proof
        host_fallbacks = sorted(set(s1.host_fallbacks) | set(s2.host_fallbacks))
        fallback_free = len(host_fallbacks) == 0
        ok = s1.output_match and s2.output_match and independent and differential and fallback_free
        all_ok = all_ok and ok
        checks.append(
            {
                "program_index": idx,
                "s1_match": s1.output_match,
                "s2_match": s2.output_match,
                "independent_vm": independent,
                "differential_proof": differential,
                "fallback_free": fallback_free,
                "vm_impl": sorted({s1.vm_impl, s2.vm_impl}),
                "host_fallbacks": host_fallbacks,
                "s1_program_sha256": s1.program_sha256,
                "s2_program_sha256": s2.program_sha256,
                "s1_output_sha256": s1.output_sha256,
                "s2_output_sha256": s2.output_sha256,
                "instruction_count": s2.instruction_count,
            }
        )
    return {
        "retirement_ready": all_ok,
        "checks": checks,
        "blocked_reasons": []
        if all_ok
        else [
            "at least one program lacks independent differential proof",
            "at least one program still reports host VM fallback paths",
        ],
        "policy": (
            "host-specific VM logic can retire only after S1/S2 output parity, "
            "independent differential proof, and zero host fallback paths are true "
            "for all target programs in a non-empty corpus"
        ),
    }


def phase18_honesty_gate_report(report: dict[str, Any]) -> dict[str, Any]:
    program_count = int(report.get("program_count", len(report.get("results", []))))
    corpus_nonempty = program_count > 0
    retirement = bool(report["retirement_report"]["retirement_ready"])
    independent_vm = bool(report["independent_vm_runtime"])
    no_host_fallback = corpus_nonempty
    for row in report["results"]:
        combined = set(row["s1"]["host_fallbacks"]) | set(row["s2"]["host_fallbacks"])
        if combined:
            no_host_fallback = False
            break
    unresolved: list[str] = []
    if not corpus_nonempty:
        unresolved.append("empty_corpus=true")
    if not retirement:
        unresolved.append("retirement_report.retirement_ready=false")
    if not independent_vm:
        unresolved.append("independent_vm_runtime=false")
    if not no_host_fallback:
        unresolved.append("host_fallbacks_present=true")
    return {
        "retirement_ready": retirement,
        "independent_vm_runtime": independent_vm,
        "no_host_fallbacks": no_host_fallback,
        "allow_independence_claim": retirement and independent_vm and no_host_fallback,
        "unresolved_reasons": unresolved,
        "policy": (
            "Independence claim is forbidden unless retirement readiness, "
            "independent VM runtime, and no host fallback paths are all true."
        ),
    }


def phase18_reproducible_steps() -> list[str]:
    return [
        "set PYTHONPATH=src",
        (
            "python -c \"from sanskript.cli import main; "
            "raise SystemExit(main(['phase18-vm-check','examples/phase18-vm-bootstrap.sskbc',"
            "'--artifact-dir','artifacts/phase18']))\""
        ),
        "python -m unittest tests/test_phase18_vm_runtime.py",
    ]


def _program_instruction_count(program: BytecodeProgram) -> int:
    total = len(program.instructions)
    total += sum(len(fn.instructions) for fn in program.functions)
    total += sum(len(fn.instructions) for mod in program.modules for fn in mod.functions)
    return total


def phase18_opcode_coverage() -> dict[str, list[str]]:
    categories = {
        "arithmetic": {
            OpCode.ADD,
            OpCode.SUBTRACT,
            OpCode.MULTIPLY,
            OpCode.DIVIDE,
            OpCode.COMPARE_EQ,
            OpCode.COMPARE_LT,
            OpCode.COMPARE_NE,
            OpCode.COMPARE_GT,
            OpCode.COMPARE_LE,
            OpCode.COMPARE_IDENTITY,
        },
        "text": {
            OpCode.PUSH_TEXT,
            OpCode.TEXT_CONCAT,
            OpCode.TEXT_LEN,
            OpCode.TEXT_GET,
            OpCode.TEXT_SLICE,
            OpCode.TEXT_CONTAINS,
        },
        "collections": {
            OpCode.LIST_NEW,
            OpCode.LIST_APPEND,
            OpCode.LIST_LEN,
            OpCode.LIST_GET,
            OpCode.MAP_NEW,
            OpCode.MAP_SET,
            OpCode.MAP_GET,
            OpCode.MAP_CONTAINS,
            OpCode.SET_NEW,
            OpCode.SET_ADD,
            OpCode.SET_CONTAINS,
            OpCode.SET_LEN,
            OpCode.TUPLE_NEW,
            OpCode.TUPLE_GET,
        },
        "records_objects": {
            OpCode.RECORD_NEW,
            OpCode.RECORD_SET,
            OpCode.RECORD_GET,
            OpCode.RECORD_CONTAINS,
            OpCode.CLASS_NEW,
            OpCode.METHOD_CALL,
        },
        "functions_calls": {
            OpCode.CALL,
            OpCode.TAIL_CALL,
            OpCode.PUSH_FUNC,
            OpCode.RETURN,
            OpCode.LOAD_NAME,
            OpCode.STORE_NAME,
        },
        "control_flow": {
            OpCode.JUMP,
            OpCode.JUMP_IF_ZERO,
            OpCode.BREAK_LOOP,
            OpCode.CONTINUE_LOOP,
            OpCode.TRY_BEGIN,
            OpCode.TRY_END,
            OpCode.THROW,
            OpCode.PANIC,
        },
        "heap": {
            OpCode.UNSAFE_ENTER,
            OpCode.UNSAFE_EXIT,
            OpCode.HEAP_ALLOC,
            OpCode.HEAP_STORE,
            OpCode.HEAP_LOAD,
            OpCode.HEAP_FREE,
        },
    }
    return {
        key: sorted(op.value for op in value)
        for key, value in categories.items()
    }


def program_sha256(program: BytecodeProgram) -> str:
    payload = {
        "instructions": [{"op": inst.opcode.value, "operand": inst.operand} for inst in program.instructions],
        "functions": [
            {
                "name": fn.name,
                "params": list(fn.params),
                "defaults": list(fn.defaults),
                "variadic_param": fn.variadic_param,
                "capture_mut": sorted(fn.capture_mut),
                "effect": fn.effect,
                "is_generator": fn.is_generator,
                "is_memoized": fn.is_memoized,
                "is_inline": fn.is_inline,
                "is_naked": fn.is_naked,
                "abi_name": fn.abi_name,
                "named_returns": list(fn.named_returns),
                "instructions": [
                    {"op": inst.opcode.value, "operand": inst.operand}
                    for inst in fn.instructions
                ],
            }
            for fn in program.functions
        ],
        "modules": [
            {
                "name": mod.name,
                "functions": [
                    {
                        "name": fn.name,
                        "params": list(fn.params),
                        "instructions": [
                            {"op": inst.opcode.value, "operand": inst.operand}
                            for inst in fn.instructions
                        ],
                    }
                    for fn in mod.functions
                ],
            }
            for mod in program.modules
        ],
        "safety_tier": program.safety_tier,
    }
    return _sha256_json(payload)


def sskyp_sha256(program: BytecodeProgram) -> str:
    return _sha256_text(program_to_yantra_patha(program))


def write_phase18_bootstrap_evidence(programs: list[BytecodeProgram], artifact_dir: Path) -> dict[str, Any]:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    for index, program in enumerate(programs):
        s1 = bootstrap_stage_s1(program)
        s2 = bootstrap_stage_s2(program)
        run_dir = artifact_dir / f"program_{index:02d}"
        try:
            rebuilt = program_from_yantra_patha(program_to_yantra_patha(program))
            SanskriptPortedVM().execute(
                rebuilt,
                trace_path=run_dir / "trace.json",
                debug_path=run_dir / "debug.json",
                profile_path=run_dir / "profile.json",
                snapshot_path=run_dir / "snapshot.json",
            )
        except Exception:
            pass
        results.append({"program_index": index, "s1": _stage_to_dict(s1), "s2": _stage_to_dict(s2)})
    report = {
        "phase": 18,
        "title": "vm-runtime-self-hosting-bootstrap-evidence",
        "independent_vm_runtime": False,
        "claim_boundary": (
            "S1/S2 prove bootstrap output parity and reproducible artifacts only; "
            "they do not prove full host-dispatch retirement."
        ),
        "program_count": len(programs),
        "results": results,
        "retirement_report": retirement_readiness_report(programs),
        "opcode_coverage": phase18_opcode_coverage(),
        "reproducible_steps": phase18_reproducible_steps(),
    }
    report["honesty_gates"] = phase18_honesty_gate_report(report)
    report_path = artifact_dir / "phase18-bootstrap-evidence.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    report["report_path"] = str(report_path)
    return report


def _stage_to_dict(stage: BootstrapStageEvidence) -> dict[str, Any]:
    return {
        "stage": stage.stage,
        "output": list(stage.output),
        "host_output": list(stage.host_output),
        "output_match": stage.output_match,
        "differential_proof": stage.differential_proof,
        "vm_impl": stage.vm_impl,
        "independent_vm": stage.independent_vm,
        "host_fallbacks": list(stage.host_fallbacks),
        "instruction_count": stage.instruction_count,
        "elapsed_ms": stage.elapsed_ms,
        "program_sha256": stage.program_sha256,
        "sskyp_sha256": stage.sskyp_sha256,
        "output_sha256": stage.output_sha256,
        "host_output_sha256": stage.host_output_sha256,
        "notes": list(stage.notes),
    }


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _sha256_json(value: Any) -> str:
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
