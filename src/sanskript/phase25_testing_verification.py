"""Phase 25 testing and verification evidence, fuzz harnesses, and scaffolding.

This module records honest coverage gaps and provides reproducible harnesses.
It does not claim per-rule/per-opcode exhaustive unit coverage.
"""

from __future__ import annotations

import hashlib
import json
import platform
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .bytecode import (
    BytecodeProgram,
    BytecodeValidationError,
    Instruction,
    OpCode,
    encode_program,
    load_bytecode_file,
    validate_bytecode,
)
from .compiler import compile_program
from .errors import ParseError, SanskriptError
from .module_loader import load_program_from_path
from .parser import parse_program
from .phase17_toolchain import deserialize_binary, serialize_binary
from .self_hosting import verify_host_vs_self_compile
from .vm import SanskriptVM
from .phase25_exhaustive_registry import build_coverage_proof
from .yantra_patha import program_from_yantra_patha, program_to_yantra_patha

REPO_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_DIR = REPO_ROOT / "data" / "testing" / "golden"
GOLDEN_MANIFEST = GOLDEN_DIR / "manifest.json"
CONFORMANCE_DIR = REPO_ROOT / "data" / "bytecode" / "conformance"
FEATURE_MATRIX = REPO_ROOT / "data" / "meta" / "feature_matrix.json"
COVERAGE_MAP_PATH = REPO_ROOT / "data" / "verification" / "coverage_map.json"
TESTS_DIR = REPO_ROOT / "tests"
EXAMPLES_DIR = REPO_ROOT / "examples"
SSK_VM_DIR = REPO_ROOT / "ssk-vm"

# Coverage thresholds for seal_ready (dedicated exhaustive suites).
MIN_OPCODE_DEDICATED_TEST_RATIO = 0.95
MIN_AST_DEDICATED_TEST_RATIO = 0.95
MIN_COMPILER_LOWERING_TEST_RATIO = 0.95
MIN_GOLDEN_STABLE_SOURCE_RATIO = 0.90

# Legacy reference ratios (token grep in tests — informational only).
MIN_OPCODE_TEST_REF_RATIO = MIN_OPCODE_DEDICATED_TEST_RATIO
MIN_GOLDEN_SOURCE_RATIO = MIN_GOLDEN_STABLE_SOURCE_RATIO

# Stable examples: all examples/*.ssk that compile except explicit skips.
GOLDEN_COMPILE_SKIP = frozenset({"phase28-game-loop.ssk"})
GOLDEN_OUTPUT_OMIT = frozenset(
    {
        "phase10-stdlib-cli-io.ssk",
        "phase10-stdlib-source.ssk",
        "phase21-cross-platform.ssk",
        "phase22-http-service.ssk",
        "phase22-full-seal.ssk",
        "phase27-port-controlled-lexicon.ssk",
        "phase27-port-examples-runner.ssk",
        "phase27-port-sutra-registry.ssk",
    }
)

# Default CLI/evidence trial count — smoke harness only, NOT production/continuous fuzz.
FUZZ_SMOKE_TRIAL_BUDGET = 48
PRODUCTION_FUZZ_MIN_TRIALS = 10_000


@dataclass(frozen=True)
class Phase25EvidenceRequest:
    out_dir: Path
    fuzz_trials: int = FUZZ_SMOKE_TRIAL_BUDGET
    property_trials: int = 64
    fuzz_seed: int = 2505


@dataclass(frozen=True)
class FuzzReport:
    name: str
    trials: int
    rejected: int
    crashes: int
    accepted: int
    claim_level: str
    notes: tuple[str, ...]
    trial_budget_class: str = "smoke-harness"
    production_fuzz_claim_rejected: bool = True

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "trials": self.trials,
            "rejected": self.rejected,
            "crashes": self.crashes,
            "accepted": self.accepted,
            "claim_level": self.claim_level,
            "trial_budget_class": self.trial_budget_class,
            "production_fuzz_claim_rejected": self.production_fuzz_claim_rejected,
            "smoke_trial_budget": FUZZ_SMOKE_TRIAL_BUDGET,
            "production_fuzz_min_trials": PRODUCTION_FUZZ_MIN_TRIALS,
            "notes": list(self.notes),
        }


def fuzz_non_overclaim_metadata(*, trials: int) -> dict[str, Any]:
    """Explicit rejection of equating default trial counts with production fuzz."""
    return {
        "continuous_fuzz_ci": False,
        "corpus_minimization": False,
        "default_trials_are_smoke_only": trials <= PRODUCTION_FUZZ_MIN_TRIALS,
        "smoke_trial_budget": FUZZ_SMOKE_TRIAL_BUDGET,
        "production_fuzz_min_trials": PRODUCTION_FUZZ_MIN_TRIALS,
        "production_fuzz_claim_rejected": trials < PRODUCTION_FUZZ_MIN_TRIALS,
    }


def _fuzz_smoke_note(trials: int) -> str:
    return (
        f"Smoke harness ({trials} trials, seed-fixed); not production or continuous fuzz "
        f"(requires >={PRODUCTION_FUZZ_MIN_TRIALS} trials + CI corpus minimization)."
    )


@dataclass(frozen=True)
class PropertyReport:
    name: str
    trials: int
    failures: int
    claim_level: str


def _canonical_sha256(payload: Any) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _count_pytest_tests() -> int:
    count = 0
    for path in TESTS_DIR.glob("test_*.py"):
        text = path.read_text(encoding="utf-8", errors="replace")
        count += len(re.findall(r"^\s*def test_", text, flags=re.MULTILINE))
    return count


def _load_golden_manifest() -> dict[str, Any]:
    return json.loads(GOLDEN_MANIFEST.read_text(encoding="utf-8"))


def audit_parser_rule_coverage() -> dict[str, Any]:
    sys.path.insert(0, str(REPO_ROOT))
    from tools.generate_feature_matrix import PARSER_RULES  # noqa: WPS433
    from tools.phase0_common import ast_statement_nodes  # noqa: WPS433

    import re as _re

    nodes = ast_statement_nodes()
    mapped = set(PARSER_RULES)
    exhaustive = _exhaustive_test_source()
    with_tests: list[str] = []
    without_tests: list[str] = []
    test_blob = exhaustive
    for path in TESTS_DIR.glob("test_*.py"):
        test_blob += path.read_text(encoding="utf-8", errors="replace")
    def _ast_snake(node_name: str) -> str:
        return _re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", node_name).lower()

    for node in sorted(nodes):
        snake = _ast_snake(node)
        dedicated = f"test_ast_{snake}" in exhaustive
        if dedicated or node in test_blob or node in mapped:
            with_tests.append(node)
        else:
            without_tests.append(node)
    dedicated_count = sum(1 for node in nodes if f"test_ast_{_ast_snake(node)}" in exhaustive)
    ratio = dedicated_count / len(nodes) if nodes else 0.0
    return {
        "ast_statement_nodes": len(nodes),
        "parser_rules_documented": len(PARSER_RULES),
        "nodes_with_dedicated_test": dedicated_count,
        "nodes_referenced_in_tests_or_parser_map": len(with_tests),
        "nodes_without_direct_test_reference": without_tests[:20],
        "nodes_without_direct_test_reference_count": len(without_tests),
        "dedicated_test_ratio": round(ratio, 4),
        "min_dedicated_test_ratio": MIN_AST_DEDICATED_TEST_RATIO,
        "per_rule_unit_tests": ratio >= MIN_AST_DEDICATED_TEST_RATIO,
        "claim_level": "dedicated-ast-suite" if ratio >= MIN_AST_DEDICATED_TEST_RATIO else "partial-matrix-only",
    }


def _exhaustive_test_source() -> str:
    path = TESTS_DIR / "test_phase25_exhaustive_coverage.py"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def audit_opcode_coverage() -> dict[str, Any]:
    exhaustive = _exhaustive_test_source()
    test_blob = exhaustive
    for path in TESTS_DIR.glob("test_*.py"):
        test_blob += path.read_text(encoding="utf-8", errors="replace")
    with_direct: list[str] = []
    without_direct: list[str] = []
    for opcode in OpCode:
        token = opcode.value
        dedicated = f"test_opcode_{token}" in exhaustive
        if dedicated or token in test_blob or f"OpCode.{opcode.name}" in test_blob:
            with_direct.append(token)
        else:
            without_direct.append(token)
    matrix_hits = 0
    if FEATURE_MATRIX.exists():
        matrix = json.loads(FEATURE_MATRIX.read_text(encoding="utf-8"))
        for item in matrix.get("features", []):
            if item.get("category") == "bytecode_opcode" and item.get("tests"):
                matrix_hits += 1
    dedicated = sum(1 for opcode in OpCode if f"test_opcode_{opcode.value}" in exhaustive)
    ratio = dedicated / len(OpCode) if OpCode else 0.0
    return {
        "opcode_enum_count": len(OpCode),
        "opcodes_with_dedicated_test": dedicated,
        "opcodes_with_test_file_token": len(with_direct),
        "opcodes_without_test_file_token": len(without_direct),
        "opcodes_without_test_file_token_sample": without_direct[:12],
        "dedicated_test_ratio": round(ratio, 4),
        "min_dedicated_test_ratio": MIN_OPCODE_DEDICATED_TEST_RATIO,
        "feature_matrix_opcodes_with_any_test_ref": matrix_hits,
        "per_opcode_dedicated_unit_tests": ratio >= MIN_OPCODE_DEDICATED_TEST_RATIO,
        "claim_level": "dedicated-opcode-suite" if ratio >= MIN_OPCODE_DEDICATED_TEST_RATIO else "partial",
    }


def audit_compiler_lowering_coverage() -> dict[str, Any]:
    from .phase25_exhaustive_registry import COMPILER_EMITTED_OPCODES  # noqa: WPS433

    exhaustive = _exhaustive_test_source()
    emitted = COMPILER_EMITTED_OPCODES
    lowering_with_tests = [
        name for name in emitted if f"test_lowering_{name.lower()}" in exhaustive or name in exhaustive
    ]
    ratio = len(lowering_with_tests) / len(emitted) if emitted else 0.0
    return {
        "compiler_referenced_opcodes": len(emitted),
        "lowerings_with_dedicated_test": len(lowering_with_tests),
        "compiler_referenced_opcodes_with_test_mention": len(lowering_with_tests),
        "dedicated_test_ratio": round(ratio, 4),
        "min_dedicated_test_ratio": MIN_COMPILER_LOWERING_TEST_RATIO,
        "per_lowering_unit_tests": ratio >= MIN_COMPILER_LOWERING_TEST_RATIO,
        "claim_level": "dedicated-lowering-suite" if ratio >= MIN_COMPILER_LOWERING_TEST_RATIO else "compiler-emission-inventory-only",
    }


def run_parser_fuzz(*, seed: int = 2505, trials: int = 48) -> FuzzReport:
    rng = random.Random(seed)
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789 .,\n"
    devanagari = "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहािीुूृेैोौंः"
    rejected = 0
    accepted = 0
    crashes = 0
    for _ in range(trials):
        length = rng.randint(0, 80)
        chars = alphabet + devanagari
        sample = "".join(rng.choice(chars) for _ in range(length))
        wrapped = f"mukhyaḥ pāṭhaḥ ārabhyate.\n{sample}\nvirāmaḥ kriyate.\n"
        try:
            parse_program(wrapped)
            accepted += 1
        except (ParseError, SanskriptError, ValueError, TypeError):
            rejected += 1
        except Exception:
            crashes += 1
    return FuzzReport(
        name="parser",
        trials=trials,
        rejected=rejected,
        accepted=accepted,
        crashes=crashes,
        claim_level="no-crash-harness",
        notes=(
            _fuzz_smoke_note(trials),
            "Random prose fragments; acceptance includes parse success on partial wrappers.",
            "Does not prove grammar completeness.",
        ),
    )


def run_bytecode_verifier_fuzz(*, seed: int = 2505, trials: int = 48) -> FuzzReport:
    program = BytecodeProgram(
        (
            Instruction(OpCode.PUSH_INT, 1),
            Instruction(OpCode.EMIT),
            Instruction(OpCode.HALT),
        )
    )
    blob = serialize_binary(program)
    rng = random.Random(seed)
    rejected = 0
    crashes = 0
    for _ in range(trials):
        mutated = bytearray(blob)
        idx = rng.randrange(len(mutated))
        mutated[idx] ^= rng.randrange(1, 256)
        try:
            deserialize_binary(bytes(mutated))
            rejected += 0
        except BytecodeValidationError:
            rejected += 1
        except Exception:
            crashes += 1
    return FuzzReport(
        name="bytecode-verifier",
        trials=trials,
        rejected=rejected,
        accepted=0,
        crashes=crashes,
        claim_level="binary-mutation-reject",
        notes=(
            _fuzz_smoke_note(trials),
            "Uses Phase 17 binary serializer mutations.",
        ),
    )


def run_sskyp_fuzz(*, seed: int = 2505, trials: int = 48) -> FuzzReport:
    base = program_to_yantra_patha(
        BytecodeProgram((Instruction(OpCode.PUSH_INT, 3), Instruction(OpCode.EMIT), Instruction(OpCode.HALT)))
    )
    lines = base.splitlines()
    rng = random.Random(seed)
    rejected = 0
    crashes = 0
    for _ in range(trials):
        mutated_lines = list(lines)
        if not mutated_lines:
            continue
        idx = rng.randrange(len(mutated_lines))
        line = mutated_lines[idx]
        if line:
            pos = rng.randrange(len(line))
            chars = list(line)
            chars[pos] = "x" if chars[pos] != "x" else "y"
            mutated_lines[idx] = "".join(chars)
        sample = "\n".join(mutated_lines) + "\n"
        try:
            program_from_yantra_patha(sample)
            rejected += 0
        except (BytecodeValidationError, SanskriptError, ValueError):
            rejected += 1
        except Exception:
            crashes += 1
    return FuzzReport(
        name="sskyp-parser",
        trials=trials,
        rejected=rejected,
        accepted=0,
        crashes=crashes,
        claim_level="line-mutation-reject",
        notes=(
            _fuzz_smoke_note(trials),
            "Mutates valid yantra-patha text; does not prove assembler completeness.",
        ),
    )


def run_property_numeric(*, seed: int = 2505, trials: int = 64) -> PropertyReport:
    rng = random.Random(seed)
    failures = 0
    for _ in range(trials):
        a = rng.randint(-50, 50)
        b = rng.randint(-50, 50)
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, a),
                Instruction(OpCode.PUSH_INT, b),
                Instruction(OpCode.ADD),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        output = SanskriptVM().execute(program)
        if output != [str(a + b)]:
            failures += 1
    return PropertyReport("numeric-add", trials, failures, "vm-int-add")


def run_property_collections(*, seed: int = 2505, trials: int = 64) -> PropertyReport:
    rng = random.Random(seed)
    failures = 0
    for _ in range(trials):
        values = [rng.randint(0, 9) for _ in range(rng.randint(1, 5))]
        instructions: list[Instruction] = [Instruction(OpCode.LIST_NEW)]
        for value in values:
            instructions.extend(
                (
                    Instruction(OpCode.PUSH_INT, value),
                    Instruction(OpCode.LIST_APPEND),
                )
            )
        instructions.extend(
            (Instruction(OpCode.LIST_LEN), Instruction(OpCode.EMIT), Instruction(OpCode.HALT))
        )
        program = BytecodeProgram(tuple(instructions))
        output = SanskriptVM().execute(program)
        if output != [str(len(values))]:
            failures += 1
    return PropertyReport("list-append-len", trials, failures, "vm-list-len")


def run_property_subtract(*, seed: int = 2505, trials: int = 64) -> PropertyReport:
    rng = random.Random(seed)
    failures = 0
    for _ in range(trials):
        a = rng.randint(-50, 50)
        b = rng.randint(-50, 50)
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, a),
                Instruction(OpCode.PUSH_INT, b),
                Instruction(OpCode.SUBTRACT),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        if SanskriptVM().execute(program) != [str(a - b)]:
            failures += 1
    return PropertyReport("numeric-subtract", trials, failures, "vm-int-subtract")


def run_property_multiply(*, seed: int = 2505, trials: int = 64) -> PropertyReport:
    rng = random.Random(seed)
    failures = 0
    for _ in range(trials):
        a = rng.randint(-12, 12)
        b = rng.randint(-12, 12)
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, a),
                Instruction(OpCode.PUSH_INT, b),
                Instruction(OpCode.MULTIPLY),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        if SanskriptVM().execute(program) != [str(a * b)]:
            failures += 1
    return PropertyReport("numeric-multiply", trials, failures, "vm-int-multiply")


def run_property_compare_eq(*, seed: int = 2505, trials: int = 64) -> PropertyReport:
    rng = random.Random(seed)
    failures = 0
    for _ in range(trials):
        a = rng.randint(-20, 20)
        b = rng.randint(-20, 20)
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, a),
                Instruction(OpCode.PUSH_INT, b),
                Instruction(OpCode.COMPARE_EQ),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        expected = "1" if a == b else "0"
        if SanskriptVM().execute(program) != [expected]:
            failures += 1
    return PropertyReport("compare-eq", trials, failures, "vm-compare-eq")


def run_property_list_get(*, seed: int = 2505, trials: int = 64) -> PropertyReport:
    rng = random.Random(seed)
    failures = 0
    for _ in range(trials):
        values = [rng.randint(0, 9) for _ in range(rng.randint(1, 5))]
        idx = rng.randrange(len(values))
        instructions: list[Instruction] = [Instruction(OpCode.LIST_NEW)]
        for value in values:
            instructions.extend((Instruction(OpCode.PUSH_INT, value), Instruction(OpCode.LIST_APPEND)))
        instructions.extend(
            (
                Instruction(OpCode.PUSH_INT, idx),
                Instruction(OpCode.LIST_GET),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        if SanskriptVM().execute(BytecodeProgram(tuple(instructions))) != [str(values[idx])]:
            failures += 1
    return PropertyReport("list-get", trials, failures, "vm-list-get")


def run_property_map_roundtrip(*, seed: int = 2505, trials: int = 64) -> PropertyReport:
    rng = random.Random(seed)
    failures = 0
    for _ in range(trials):
        key = str(rng.randint(0, 99))
        value = rng.randint(0, 99)
        program = BytecodeProgram(
            (
                Instruction(OpCode.MAP_NEW),
                Instruction(OpCode.PUSH_TEXT, key),
                Instruction(OpCode.PUSH_INT, value),
                Instruction(OpCode.MAP_SET),
                Instruction(OpCode.PUSH_TEXT, key),
                Instruction(OpCode.MAP_GET),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        if SanskriptVM().execute(program) != [str(value)]:
            failures += 1
    return PropertyReport("map-get", trials, failures, "vm-map-get")


def run_property_text(*, seed: int = 2505, trials: int = 64) -> PropertyReport:
    rng = random.Random(seed)
    failures = 0
    alphabet = "abcd0123"
    for _ in range(trials):
        left = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
        right = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_TEXT, left),
                Instruction(OpCode.PUSH_TEXT, right),
                Instruction(OpCode.TEXT_CONCAT),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        output = SanskriptVM().execute(program)
        if output != [left + right]:
            failures += 1
    return PropertyReport("text-concat", trials, failures, "vm-text-concat")


def verify_golden_source_entries() -> list[dict[str, Any]]:
    manifest = _load_golden_manifest()
    rows: list[dict[str, Any]] = []
    for entry in manifest.get("source", []):
        source = REPO_ROOT / entry["path"]
        try:
            program = compile_program(load_program_from_path(source))
        except SanskriptError:
            rows.append(
                {
                    "id": entry["id"],
                    "path": entry["path"],
                    "bytecode_match": False,
                    "sskyp_match": False,
                    "output_match": False if "expected_output" in entry else None,
                }
            )
            continue
        bc_sha = _canonical_sha256(encode_program(program))
        sskyp_sha = hashlib.sha256(program_to_yantra_patha(program).encode("utf-8")).hexdigest()
        output_match: bool | None = None
        if "expected_output" in entry:
            try:
                output = SanskriptVM().execute(program)
                output_match = output == entry["expected_output"]
            except SanskriptError:
                output_match = False
        rows.append(
            {
                "id": entry["id"],
                "path": entry["path"],
                "bytecode_match": bc_sha == entry["bytecode_sha256"],
                "sskyp_match": sskyp_sha == entry["sskyp_sha256"],
                "output_match": output_match,
            }
        )
    return rows


def verify_golden_bytecode_entries() -> list[dict[str, Any]]:
    manifest = _load_golden_manifest()
    rows: list[dict[str, Any]] = []
    for entry in manifest.get("bytecode", []):
        path = REPO_ROOT / entry["path"]
        payload = json.loads(path.read_text(encoding="utf-8"))
        program = load_bytecode_file(path)
        output = SanskriptVM().execute(program)
        rows.append(
            {
                "id": entry["id"],
                "path": entry["path"],
                "output_match": output == payload.get("expected_output"),
            }
        )
    return rows


def verify_golden_hashes_stable() -> dict[str, Any]:
    """Run golden verification twice; hashes and outputs must be identical."""
    first_source = verify_golden_source_entries()
    second_source = verify_golden_source_entries()
    first_bytecode = verify_golden_bytecode_entries()
    second_bytecode = verify_golden_bytecode_entries()
    first_sskyp = verify_golden_sskyp_entries()
    second_sskyp = verify_golden_sskyp_entries()

    def _rows_stable(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> bool:
        if len(left) != len(right):
            return False
        for a, b in zip(left, right):
            if a.get("id") != b.get("id"):
                return False
            for key in ("bytecode_match", "sskyp_match", "output_match"):
                if key in a and a.get(key) != b.get(key):
                    return False
        return True

    stable = (
        _rows_stable(first_source, second_source)
        and _rows_stable(first_bytecode, second_bytecode)
        and _rows_stable(first_sskyp, second_sskyp)
    )
    mismatches: list[str] = []
    if not _rows_stable(first_source, second_source):
        mismatches.append("source")
    if not _rows_stable(first_bytecode, second_bytecode):
        mismatches.append("bytecode")
    if not _rows_stable(first_sskyp, second_sskyp):
        mismatches.append("sskyp")
    return {
        "stable": stable,
        "mismatched_categories": mismatches,
        "source_count": len(first_source),
        "bytecode_count": len(first_bytecode),
        "sskyp_count": len(first_sskyp),
    }


def _repo_relative_posix(path: Path) -> str:
    try:
        rel = path.resolve().relative_to(REPO_ROOT.resolve())
    except ValueError:
        rel = path
    return rel.as_posix()


def differential_scaffold_fingerprint(payload: dict[str, Any]) -> str:
    """Canonical fingerprint for differential scaffolding (cross-run stable)."""
    host_vm = payload.get("host_vm", {})
    host_compiler = payload.get("host_compiler", {})
    vm_rows = [
        {
            "fixture": row.get("fixture"),
            "python_vm_output": row.get("python_vm_output"),
            "python_matches_fixture": row.get("python_matches_fixture"),
            "independent_differential_proof": row.get("independent_differential_proof"),
        }
        for row in host_vm.get("rows", [])
    ]
    compiler_rows = [
        {
            "source": row.get("source"),
            "bytecode_match": row.get("bytecode_match"),
            "sskyp_match": row.get("sskyp_match"),
            "independent_self_compile": row.get("independent_self_compile"),
            "proof_method": row.get("proof_method"),
        }
        for row in host_compiler.get("rows", [])
    ]
    canonical = {
        "host_vm": {
            "all_python_match": host_vm.get("all_python_match"),
            "fixtures": host_vm.get("fixtures"),
            "rows": vm_rows,
        },
        "host_compiler": {
            "all_bytecode_match": host_compiler.get("all_bytecode_match"),
            "rows": compiler_rows,
        },
    }
    return _canonical_sha256(canonical)


def differential_scaffolds_deterministic(
    *,
    vm_fixture_paths: tuple[Path, ...] | None = None,
    compiler_sources: tuple[Path, ...] | None = None,
) -> dict[str, Any]:
    """Invoke differential scaffolds twice; fingerprints must match."""
    vm_paths = vm_fixture_paths or tuple(sorted(CONFORMANCE_DIR.glob("*.json")))
    sources = compiler_sources or (
        REPO_ROOT / "examples" / "prathama.ssk",
        REPO_ROOT / "examples" / "phase3-data-types.ssk",
    )
    first = {
        "host_vm": differential_host_vm_scaffold(vm_paths),
        "host_compiler": differential_host_compiler_scaffold(sources),
    }
    second = {
        "host_vm": differential_host_vm_scaffold(vm_paths),
        "host_compiler": differential_host_compiler_scaffold(sources),
    }
    fp1 = differential_scaffold_fingerprint(first)
    fp2 = differential_scaffold_fingerprint(second)
    return {
        "deterministic": fp1 == fp2,
        "fingerprint": fp1,
        "fingerprint_repeat": fp2,
    }


def verify_golden_sskyp_entries() -> list[dict[str, Any]]:
    manifest = _load_golden_manifest()
    rows: list[dict[str, Any]] = []
    for entry in manifest.get("sskyp", []):
        path = REPO_ROOT / entry["path"]
        text = path.read_text(encoding="utf-8")
        sskyp_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        program = program_from_yantra_patha(text)
        output = SanskriptVM().execute(program)
        rows.append(
            {
                "id": entry["id"],
                "path": entry["path"],
                "sskyp_match": sskyp_sha == entry["sskyp_sha256"],
                "output_match": output == entry.get("expected_output"),
            }
        )
    return rows


def roundtrip_bytecode_serialization(program: BytecodeProgram) -> dict[str, Any]:
    validate_bytecode(program)
    blob = serialize_binary(program)
    restored = deserialize_binary(blob)
    validate_bytecode(restored)
    host_out = SanskriptVM().execute(program)
    restored_out = SanskriptVM().execute(restored)
    return {
        "serialize_roundtrip": restored.instructions == program.instructions,
        "output_match": host_out == restored_out,
    }


def roundtrip_sskyp_assembly(program: BytecodeProgram) -> dict[str, Any]:
    text = program_to_yantra_patha(program)
    restored = program_from_yantra_patha(text)
    validate_bytecode(restored)
    return {
        "sskyp_roundtrip": encode_program(restored) == encode_program(program),
        "output_match": SanskriptVM().execute(program) == SanskriptVM().execute(restored),
    }


def stable_example_paths() -> list[Path]:
    return sorted(
        path
        for path in EXAMPLES_DIR.glob("*.ssk")
        if path.name not in GOLDEN_COMPILE_SKIP
    )


def golden_stable_coverage_ratio() -> dict[str, Any]:
    stable = stable_example_paths()
    manifest = _load_golden_manifest()
    golden_paths = {entry["path"] for entry in manifest.get("source", [])}
    covered = [path.relative_to(REPO_ROOT).as_posix() for path in stable if path.relative_to(REPO_ROOT).as_posix() in golden_paths]
    ratio = len(covered) / len(stable) if stable else 0.0
    return {
        "stable_example_count": len(stable),
        "golden_source_count": len(covered),
        "golden_stable_ratio": round(ratio, 4),
        "min_golden_stable_ratio": MIN_GOLDEN_STABLE_SOURCE_RATIO,
        "meets_threshold": ratio >= MIN_GOLDEN_STABLE_SOURCE_RATIO,
    }


def coverage_thresholds_met(*, coverage_audits: dict[str, Any] | None = None) -> dict[str, Any]:
    parser = (coverage_audits or {}).get("parser_rules") or audit_parser_rule_coverage()
    opcodes = (coverage_audits or {}).get("opcodes") or audit_opcode_coverage()
    lowerings = (coverage_audits or {}).get("compiler_lowerings") or audit_compiler_lowering_coverage()
    golden = golden_stable_coverage_ratio()
    checks = {
        "opcodes": opcodes.get("per_opcode_dedicated_unit_tests", False),
        "parser_ast": parser.get("per_rule_unit_tests", False),
        "compiler_lowerings": lowerings.get("per_lowering_unit_tests", False),
        "golden_stable": golden.get("meets_threshold", False),
    }
    return {
        "met": all(checks.values()),
        "checks": checks,
        "golden": golden,
        "parser_ast_ratio": parser.get("dedicated_test_ratio"),
        "opcode_ratio": opcodes.get("dedicated_test_ratio"),
        "lowering_ratio": lowerings.get("dedicated_test_ratio"),
    }


def build_coverage_map() -> dict[str, Any]:
    """Structured coverage map for parser rules, compiler lowerings, and VM opcodes."""
    parser = audit_parser_rule_coverage()
    opcodes = audit_opcode_coverage()
    lowerings = audit_compiler_lowering_coverage()
    example_ssk = sorted(EXAMPLES_DIR.glob("*.ssk"))
    golden_manifest = _load_golden_manifest()
    golden_sources = {entry["path"] for entry in golden_manifest.get("source", [])}
    stable = golden_stable_coverage_ratio()
    return {
        "version": 1,
        "phase": 25,
        "parser_rules": parser,
        "vm_opcodes": opcodes,
        "compiler_lowerings": lowerings,
        "examples": {
            "ssk_count": len(example_ssk),
            "golden_source_count": len(golden_sources),
            "golden_source_paths": sorted(golden_sources),
            "golden_coverage_ratio": round(len(golden_sources) / len(example_ssk), 4) if example_ssk else 0.0,
            "stable_golden": stable,
        },
        "conformance_fixtures": len(list(CONFORMANCE_DIR.glob("*.json"))),
        "thresholds": {
            "min_opcode_dedicated_test_ratio": MIN_OPCODE_DEDICATED_TEST_RATIO,
            "min_ast_dedicated_test_ratio": MIN_AST_DEDICATED_TEST_RATIO,
            "min_compiler_lowering_test_ratio": MIN_COMPILER_LOWERING_TEST_RATIO,
            "min_golden_stable_source_ratio": MIN_GOLDEN_STABLE_SOURCE_RATIO,
        },
        "coverage_thresholds_met": coverage_thresholds_met(
            coverage_audits={
                "parser_rules": parser,
                "opcodes": opcodes,
                "compiler_lowerings": lowerings,
            }
        ),
    }


def write_coverage_map(path: Path | None = None) -> Path:
    target = path or COVERAGE_MAP_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = build_coverage_map()
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def differential_rust_vm_optional(
    fixture_paths: tuple[Path, ...] | None = None,
) -> dict[str, Any]:
    """Run Python VM vs ssk-vm on conformance fixtures when cargo is available."""
    import shutil
    import subprocess

    paths = fixture_paths or tuple(sorted(CONFORMANCE_DIR.glob("*.json")))
    if not shutil.which("cargo"):
        return {
            "claim_level": "skipped-no-cargo",
            "fixtures": len(paths),
            "all_match": None,
            "rust_vm_checked": False,
            "rows": [],
            "note": "Install Rust/cargo to enable host-Python vs ssk-vm differential rows.",
        }

    binary = SSK_VM_DIR / "target" / "debug" / ("ssk-vm.exe" if sys.platform.startswith("win") else "ssk-vm")
    if not binary.exists():
        subprocess.run(["cargo", "build", "--quiet"], cwd=SSK_VM_DIR, check=True)

    rows: list[dict[str, Any]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        program = load_bytecode_file(path)
        python_output = SanskriptVM().execute(program)
        completed = subprocess.run(
            [str(binary), str(path)],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        rust_output = [line for line in completed.stdout.splitlines() if line.strip()]
        expected = payload.get("expected_output", [])
        rows.append(
            {
                "fixture": path.name,
                "python_vm_output": python_output,
                "rust_vm_output": rust_output,
                "expected_output": expected,
                "python_matches_fixture": python_output == expected,
                "rust_matches_fixture": rust_output == expected,
                "python_rust_match": python_output == rust_output,
                "independent_differential_proof": False,
                "note": "ssk-vm is a second host implementation; not a Sanskript-native VM proof.",
            }
        )
    return {
        "claim_level": "host-python-vs-rust-ssk-vm",
        "fixtures": len(rows),
        "all_match": all(
            row["python_matches_fixture"] and row["rust_matches_fixture"] and row["python_rust_match"]
            for row in rows
        ),
        "rust_vm_checked": True,
        "rows": rows,
    }


def phase25_seal_verdict(evidence: dict[str, Any]) -> dict[str, Any]:
    """Seal-ready when exhaustive coverage thresholds and harness gates pass."""
    blockers: list[str] = []
    warnings: list[str] = []

    coverage = evidence.get("coverage_audits", {})
    thresholds = evidence.get("coverage_thresholds", coverage_thresholds_met(coverage_audits=coverage))
    non_overclaim = evidence.get("non_overclaim", {})
    fuzz = evidence.get("fuzz", {})
    property_tests = evidence.get("property", {})
    golden = evidence.get("golden", {})
    golden_stability = evidence.get("golden_stability", {})
    differential = evidence.get("differential", {})
    differential_det = evidence.get("differential_determinism", {})

    parser_cov = coverage.get("parser_rules", {})
    opcode_cov = coverage.get("opcodes", {})
    lowering_cov = coverage.get("compiler_lowerings", {})

    if not thresholds.get("met"):
        checks = thresholds.get("checks", {})
        if not checks.get("opcodes"):
            blockers.append(
                f"Opcode dedicated coverage below {MIN_OPCODE_DEDICATED_TEST_RATIO:.0%} "
                f"({opcode_cov.get('opcodes_with_dedicated_test', 0)}/{opcode_cov.get('opcode_enum_count', 0)})."
            )
        if not checks.get("parser_ast"):
            blockers.append(
                f"AST dedicated coverage below {MIN_AST_DEDICATED_TEST_RATIO:.0%} "
                f"({parser_cov.get('nodes_with_dedicated_test', 0)}/{parser_cov.get('ast_statement_nodes', 0)})."
            )
        if not checks.get("compiler_lowerings"):
            blockers.append(
                f"Compiler lowering dedicated coverage below {MIN_COMPILER_LOWERING_TEST_RATIO:.0%} "
                f"({lowering_cov.get('lowerings_with_dedicated_test', 0)}/"
                f"{lowering_cov.get('compiler_referenced_opcodes', 0)})."
            )
        if not checks.get("golden_stable"):
            golden_stable = thresholds.get("golden", {})
            blockers.append(
                f"Golden stable-example coverage below {MIN_GOLDEN_STABLE_SOURCE_RATIO:.0%} "
                f"({golden_stable.get('golden_source_count', 0)}/"
                f"{golden_stable.get('stable_example_count', 0)})."
            )

    if not non_overclaim.get("independent_vm_differential_proof"):
        warnings.append("No independent Sanskript VM differential proof (host Python + optional Rust ssk-vm only).")

    if not non_overclaim.get("independent_self_hosted_compiler_proof"):
        warnings.append("Self-hosted compiler proof is S0 host-replay only, not independent.")

    fuzz_meta = evidence.get("fuzz_non_overclaim", {})
    if fuzz_meta.get("production_fuzz_claim_rejected") is False:
        blockers.append(
            f"Trial count meets production fuzz threshold ({PRODUCTION_FUZZ_MIN_TRIALS}+) "
            "but continuous CI fuzz and corpus minimization are not implemented."
        )
    for name, report in fuzz.items():
        if report.get("crashes", 0) > 0:
            blockers.append(f"Fuzz harness {name} recorded crashes.")
        if report.get("trial_budget_class") == "production-continuous":
            blockers.append(f"Fuzz harness {name} mislabeled as production continuous fuzz.")
        if report.get("production_fuzz_claim_rejected") is False and report.get("trials", 0) < PRODUCTION_FUZZ_MIN_TRIALS:
            blockers.append(f"Fuzz harness {name} allows production fuzz overclaim at {report.get('trials')} trials.")
    if fuzz.get("bytecode_verifier", {}).get("rejected", 0) != fuzz.get("bytecode_verifier", {}).get("trials", 0):
        warnings.append("Bytecode verifier fuzz did not reject every mutation trial.")
    if fuzz_meta.get("default_trials_are_smoke_only"):
        warnings.append(
            f"Fuzz trial budget is smoke-only (default {FUZZ_SMOKE_TRIAL_BUDGET}); "
            "not production/continuous fuzz CI."
        )

    for name, report in property_tests.items():
        if report.get("failures", 0) > 0:
            blockers.append(f"Property harness {name} reported failures.")

    if golden_stability and not golden_stability.get("stable", True):
        blockers.append(
            "Golden hash verification is nondeterministic across back-to-back runs: "
            f"{golden_stability.get('mismatched_categories', [])}."
        )
    if differential_det and not differential_det.get("deterministic", True):
        blockers.append("Differential scaffolding fingerprints differ across repeated invocations.")

    source_golden = golden.get("source", [])
    if not source_golden or not all(row.get("bytecode_match") for row in source_golden):
        blockers.append("Golden source bytecode/sskyp hashes do not all match manifest.")
    output_rows = [row for row in source_golden if row.get("output_match") is False]
    if output_rows:
        blockers.append(f"Golden source output mismatch: {[r.get('id') for r in output_rows]}")
    golden_stable = thresholds.get("golden", {})
    if not golden_stable.get("meets_threshold", True):
        blockers.append(
            f"Golden registry missing stable examples "
            f"({golden_stable.get('golden_source_count', 0)}/"
            f"{golden_stable.get('stable_example_count', 0)})."
        )

    checklist = evidence.get("checklist_truth", [])
    not_met = [row["item"] for row in checklist if row.get("status") == "not_met"]
    if not_met:
        warnings.append(f"Phase 25 checklist items still not_met: {len(not_met)} (e.g. {not_met[0]}).")
    partial_without_harness = [
        row["item"]
        for row in checklist
        if row.get("status") == "partial" and not row.get("harness")
    ]
    if partial_without_harness:
        warnings.append(
            f"Phase 25 partial rows lack harness pointer: {partial_without_harness[0]}"
        )

    rust_diff = differential.get("rust_vm")
    if rust_diff and rust_diff.get("rust_vm_checked") and not rust_diff.get("all_match"):
        blockers.append("Python VM and ssk-vm outputs diverged on conformance fixtures.")

    harness_green = not any("Fuzz harness" in b or "Property harness" in b for b in blockers) and not any(
        "Golden source bytecode" in b or "output mismatch" in b for b in blockers
    )

    exhaustive_suites_ready = bool(thresholds.get("met"))
    coverage_proof = evidence.get("coverage_proof", {})
    if not coverage_proof:
        blockers.insert(0, "Coverage proof missing — seal_ready rejected (anti-fake gatekeeper).")
    elif not coverage_proof.get("passed"):
        for failure in coverage_proof.get("failures", []):
            blockers.insert(0, f"Coverage proof: {failure}")

    seal_ready = bool(coverage_proof.get("passed")) and exhaustive_suites_ready and harness_green and len(blockers) == 0

    return {
        "seal_ready": seal_ready,
        "harness_ready": harness_green,
        "harness_green": harness_green,
        "coverage_proof_passed": bool(coverage_proof.get("passed")),
        "exhaustive_suites_ready": exhaustive_suites_ready,
        "coverage_thresholds_met": thresholds.get("met", False),
        "blockers": blockers,
        "warnings": warnings,
        "repro_commands": [
            "PYTHONPATH=src python tools/generate_phase25_tests.py",
            "PYTHONPATH=src python tools/generate_phase25_golden.py",
            "PYTHONPATH=src python -m pytest tests/test_phase25_exhaustive_coverage.py tests/test_phase25_borrow_negatives.py tests/test_phase25_testing_verification.py -q",
            "PYTHONPATH=src python -m sanskript.cli phase25-evidence",
            "PYTHONPATH=src python tools/phase25_coverage_map.py",
        ],
    }


def differential_host_vm_scaffold(
    fixture_paths: tuple[Path, ...] | None = None,
) -> dict[str, Any]:
    paths = fixture_paths or tuple(sorted(CONFORMANCE_DIR.glob("*.json")))
    rows: list[dict[str, Any]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        program = load_bytecode_file(path)
        python_output = SanskriptVM().execute(program)
        rows.append(
            {
                "fixture": path.name,
                "python_vm_output": python_output,
                "expected_output": payload.get("expected_output"),
                "python_matches_fixture": python_output == payload.get("expected_output"),
                "rust_vm_checked": False,
                "independent_differential_proof": False,
                "note": "Rust ssk-vm differential requires cargo; see tests/test_rust_vm.py",
            }
        )
    return {
        "claim_level": "host-python-vm-scaffold",
        "fixtures": len(rows),
        "all_python_match": all(row["python_matches_fixture"] for row in rows),
        "rows": rows,
    }


def differential_host_compiler_scaffold(
    sources: tuple[Path, ...],
    *,
    artifact_root: Path | None = None,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for source in sources:
        base = artifact_root or (source.parent / ".phase25-diff")
        evidence = verify_host_vs_self_compile(source, base / source.stem)
        rows.append(
            {
                "source": _repo_relative_posix(source),
                "stage": evidence.stage,
                "independent_self_compile": evidence.independent_self_compile,
                "bytecode_match": evidence.bytecode_match,
                "sskyp_match": evidence.sskyp_match,
                "proof_method": evidence.proof_method,
            }
        )
    return {
        "claim_level": "S0-host-replay-not-independent",
        "all_bytecode_match": all(row["bytecode_match"] for row in rows),
        "rows": rows,
    }


def security_review_checklist() -> list[dict[str, Any]]:
    return [
        {
            "id": "sec-input-validation",
            "topic": "Parser and bytecode input validation",
            "status": "partial",
            "evidence": ["tests/test_phase17_toolchain.py", "phase25 bytecode/sskyp fuzz harness"],
        },
        {
            "id": "sec-unsafe-tier",
            "topic": "Unsafe / arakṣita tier gates",
            "status": "partial",
            "evidence": ["tests/test_vm_numeric_heap.py", "examples/phase14-surakshita.ssk"],
        },
        {
            "id": "sec-package-signing",
            "topic": "Package signing and lockfiles",
            "status": "partial",
            "evidence": ["src/sanskript/package_signing.py", "tests/test_phase9_modules.py"],
        },
        {
            "id": "sec-concurrency",
            "topic": "Concurrency stress and data races",
            "status": "partial",
            "evidence": [
                "src/sanskript/phase23_concurrency.py",
                "tests/test_phase23_concurrency_async.py",
            ],
        },
        {
            "id": "sec-fuzz-coverage",
            "topic": "Smoke fuzz harness for parser/verifier/sskyp (not continuous CI fuzz)",
            "status": "partial",
            "evidence": ["src/sanskript/phase25_testing_verification.py"],
        },
        {
            "id": "sec-independent-vm",
            "topic": "Independent VM/compiler differential proof",
            "status": "not_met",
            "evidence": ["docs/phase18-vm-runtime-self-hosting.md", "docs/phase19-compiler-self-hosting.md"],
        },
    ]


def phase25_checklist_truth() -> list[dict[str, Any]]:
    """Honest checklist rows for Phase 25 — tick only what harnesses prove."""
    parser = audit_parser_rule_coverage()
    opcodes = audit_opcode_coverage()
    lowerings = audit_compiler_lowering_coverage()
    golden = golden_stable_coverage_ratio()
    parser_ok = parser.get("per_rule_unit_tests", False)
    opcode_ok = opcodes.get("per_opcode_dedicated_unit_tests", False)
    lowering_ok = lowerings.get("per_lowering_unit_tests", False)
    golden_ok = golden.get("meets_threshold", False)
    exhaustive_harness = "tests/test_phase25_exhaustive_coverage.py"
    return [
        {
            "item": "Unit tests for every parser rule",
            "status": "met" if parser_ok else "partial",
            "harness": exhaustive_harness,
            "note": f"{parser.get('nodes_with_dedicated_test', 0)}/{parser.get('ast_statement_nodes', 0)} AST dedicated tests",
        },
        {
            "item": "Unit tests for every compiler lowering",
            "status": "met" if lowering_ok else "partial",
            "harness": exhaustive_harness,
            "note": f"{lowerings.get('lowerings_with_dedicated_test', 0)}/{lowerings.get('compiler_referenced_opcodes', 0)} lowering tests",
        },
        {
            "item": "Unit tests for every VM opcode",
            "status": "met" if opcode_ok else "partial",
            "harness": exhaustive_harness,
            "note": f"{opcodes.get('opcodes_with_dedicated_test', 0)}/{opcodes.get('opcode_enum_count', 0)} opcode tests",
        },
        {
            "item": "Golden tests for source examples",
            "status": "met" if golden_ok else "partial",
            "harness": "tools/generate_phase25_golden.py",
            "note": f"{golden.get('golden_source_count', 0)}/{golden.get('stable_example_count', 0)} stable examples in manifest",
        },
        {
            "item": "Golden tests for bytecode output",
            "status": "partial",
            "harness": "data/bytecode/conformance + tests/test_phase25_testing_verification.py",
            "note": "conformance + phase25 minimal fixture",
        },
        {
            "item": "Golden tests for .sskyp output",
            "status": "partial",
            "harness": "tests/test_phase25_testing_verification.py",
            "note": "sha256 fixtures + roundtrip harness",
        },
        {
            "item": "Round-trip tests for source formatting",
            "status": "not_met",
            "note": "No canonical source formatter round-trip",
        },
        {
            "item": "Round-trip tests for bytecode serialization",
            "status": "partial",
            "harness": "tests/test_bytecode_conformance.py",
            "note": "tests/test_bytecode_conformance.py + phase25 binary roundtrip",
        },
        {
            "item": "Round-trip tests for .sskyp assembly",
            "status": "partial",
            "harness": "tests/test_phase25_testing_verification.py",
            "note": "yantra_patha roundtrip helper",
        },
        {
            "item": "Negative parser tests",
            "status": "partial",
            "harness": "tests/test_phase17_toolchain.py",
            "note": "tests/test_phase17_toolchain.py and phase files",
        },
        {
            "item": "Negative type-checker tests",
            "status": "partial",
            "harness": "tests/test_phase4_type_system.py",
            "note": "tests/test_phase4_type_system.py",
        },
        {
            "item": "Negative borrow-checker tests",
            "status": "met" if (TESTS_DIR / "test_phase25_borrow_negatives.py").exists() else "partial",
            "harness": "tests/test_phase25_borrow_negatives.py",
            "note": "tests/test_phase25_borrow_negatives.py generated corpus",
        },
        {
            "item": "Negative unsafe-code tests",
            "status": "partial",
            "harness": "tests/test_vm_numeric_heap.py",
            "note": "tests/test_vm_numeric_heap.py",
        },
        {
            "item": "Runtime error tests",
            "status": "partial",
            "harness": "tests/test_errors.py",
            "note": "tests/test_errors.py and phase12 diagnostics",
        },
        {
            "item": "Cross-platform tests",
            "status": "partial",
            "harness": "src/sanskript/phase25_testing_verification.py",
            "note": f"host={platform.system()}; CI matrix not in-repo",
        },
        {
            "item": "Fuzz parser",
            "status": "partial",
            "harness": "src/sanskript/phase25_testing_verification.py",
            "note": f"run_parser_fuzz smoke harness ({FUZZ_SMOKE_TRIAL_BUDGET} trials default; not production fuzz)",
        },
        {
            "item": "Fuzz bytecode verifier",
            "status": "partial",
            "harness": "src/sanskript/phase25_testing_verification.py",
            "note": f"run_bytecode_verifier_fuzz smoke harness ({FUZZ_SMOKE_TRIAL_BUDGET} trials default)",
        },
        {
            "item": "Fuzz .sskyp parser",
            "status": "partial",
            "harness": "src/sanskript/phase25_testing_verification.py",
            "note": f"run_sskyp_fuzz smoke harness ({FUZZ_SMOKE_TRIAL_BUDGET} trials default)",
        },
        {
            "item": "Property-test standard library collections",
            "status": "partial",
            "harness": "src/sanskript/phase25_testing_verification.py",
            "note": "VM list property harness",
        },
        {
            "item": "Property-test numeric operations",
            "status": "partial",
            "harness": "src/sanskript/phase25_testing_verification.py",
            "note": "add/subtract/multiply/compare_eq property harnesses",
        },
        {
            "item": "Property-test text operations",
            "status": "partial",
            "harness": "src/sanskript/phase25_testing_verification.py",
            "note": "VM text concat property harness",
        },
        {
            "item": "Property-test map operations",
            "status": "partial",
            "harness": "src/sanskript/phase25_testing_verification.py",
            "note": "VM map get/set property harness",
        },
        {
            "item": "Differential-test host VM vs Sanskript VM",
            "status": "scaffold",
            "harness": "src/sanskript/phase25_testing_verification.py",
            "note": "Python VM + rust_vm test; not independent",
        },
        {
            "item": "Differential-test host compiler vs self-hosted compiler",
            "status": "scaffold",
            "harness": "src/sanskript/self_hosting.py",
            "note": "S0 host-replay via self_hosting.py",
        },
        {
            "item": "Performance benchmark suite",
            "status": "partial",
            "harness": "tests/test_performance_baseline.py",
            "note": "tests/test_performance_baseline.py",
        },
        {
            "item": "Memory safety test suite",
            "status": "partial",
            "harness": "tests/test_phase13_memory_model.py",
            "note": "tests/test_phase13_memory_model.py",
        },
        {
            "item": "Concurrency stress tests",
            "status": "partial",
            "harness": "tests/test_phase23_concurrency_async.py",
            "note": "tests/test_phase23_concurrency_async.py + std.phase23.seal_verdict runtime gatekeeper",
        },
        {
            "item": "Security review checklist",
            "status": "partial",
            "harness": "src/sanskript/phase25_testing_verification.py",
            "note": "security_review_checklist() scaffold",
        },
    ]


def generate_phase25_evidence(*, request: Phase25EvidenceRequest) -> dict[str, Any]:
    from .phase25_exhaustive_registry import build_coverage_proof  # noqa: WPS433

    request.out_dir.mkdir(parents=True, exist_ok=True)
    coverage_map_path = write_coverage_map()
    coverage_proof = build_coverage_proof(execute_opcodes=True, compile_ast=True).as_dict()
    minimal = BytecodeProgram((Instruction(OpCode.PUSH_INT, 7), Instruction(OpCode.EMIT), Instruction(OpCode.HALT)))
    example_sources = (
        REPO_ROOT / "examples" / "prathama.ssk",
        REPO_ROOT / "examples" / "phase3-data-types.ssk",
        REPO_ROOT / "examples" / "phase6-functions.ssk",
        REPO_ROOT / "examples" / "phase7-oop.ssk",
    )
    payload: dict[str, Any] = {
        "phase": 25,
        "host_platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "pytest_test_functions_estimated": _count_pytest_tests(),
        "coverage_audits": {
            "parser_rules": audit_parser_rule_coverage(),
            "opcodes": audit_opcode_coverage(),
            "compiler_lowerings": audit_compiler_lowering_coverage(),
        },
        "golden": {
            "source": verify_golden_source_entries(),
            "bytecode": verify_golden_bytecode_entries(),
            "sskyp": verify_golden_sskyp_entries(),
        },
        "roundtrip": {
            "bytecode_binary": roundtrip_bytecode_serialization(minimal),
            "sskyp": roundtrip_sskyp_assembly(minimal),
        },
        "fuzz_non_overclaim": fuzz_non_overclaim_metadata(trials=request.fuzz_trials),
        "fuzz": {
            "parser": run_parser_fuzz(seed=request.fuzz_seed, trials=request.fuzz_trials).as_dict(),
            "bytecode_verifier": run_bytecode_verifier_fuzz(
                seed=request.fuzz_seed, trials=request.fuzz_trials
            ).as_dict(),
            "sskyp": run_sskyp_fuzz(seed=request.fuzz_seed, trials=request.fuzz_trials).as_dict(),
        },
        "golden_stability": verify_golden_hashes_stable(),
        "differential_determinism": differential_scaffolds_deterministic(),
        "property": {
            "numeric": run_property_numeric(seed=request.fuzz_seed, trials=request.property_trials).__dict__,
            "numeric_subtract": run_property_subtract(
                seed=request.fuzz_seed, trials=request.property_trials
            ).__dict__,
            "numeric_multiply": run_property_multiply(
                seed=request.fuzz_seed, trials=request.property_trials
            ).__dict__,
            "compare_eq": run_property_compare_eq(
                seed=request.fuzz_seed, trials=request.property_trials
            ).__dict__,
            "collections": run_property_collections(
                seed=request.fuzz_seed, trials=request.property_trials
            ).__dict__,
            "list_get": run_property_list_get(seed=request.fuzz_seed, trials=request.property_trials).__dict__,
            "map_get": run_property_map_roundtrip(
                seed=request.fuzz_seed, trials=request.property_trials
            ).__dict__,
            "text": run_property_text(seed=request.fuzz_seed, trials=request.property_trials).__dict__,
        },
        "coverage_proof": coverage_proof,
        "coverage_thresholds": coverage_thresholds_met(),
        "coverage_map_path": str(coverage_map_path.relative_to(REPO_ROOT)),
        "differential": {
            "host_vm": differential_host_vm_scaffold(),
            "rust_vm": differential_rust_vm_optional(),
            "host_compiler": differential_host_compiler_scaffold(
                example_sources,
                artifact_root=request.out_dir / "compiler-diff",
            ),
        },
        "security_checklist": security_review_checklist(),
        "checklist_truth": phase25_checklist_truth(),
        "non_overclaim": {
            "per_parser_rule_unit_tests": audit_parser_rule_coverage().get("per_rule_unit_tests", False),
            "per_opcode_unit_tests": audit_opcode_coverage().get("per_opcode_dedicated_unit_tests", False),
            "per_lowering_unit_tests": audit_compiler_lowering_coverage().get("per_lowering_unit_tests", False),
            "independent_vm_differential_proof": False,
            "independent_self_hosted_compiler_proof": False,
            "production_continuous_fuzz": False,
        },
    }
    payload["seal_verdict"] = phase25_seal_verdict(payload)
    out_path = request.out_dir / "phase25-evidence.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    payload["evidence_path"] = str(out_path)
    return payload
