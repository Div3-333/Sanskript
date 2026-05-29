"""Phase 25 exhaustive coverage registry and coverage-proof gate."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .bytecode import OpCode
from .compiler import compile_program
from .phase25_opcode_smoke import build_opcode_smoke_spec, run_opcode_smoke

REPO_ROOT = Path(__file__).resolve().parents[2]
TESTS_DIR = REPO_ROOT / "tests"
EXHAUSTIVE_TEST_PATH = TESTS_DIR / "test_phase25_exhaustive_coverage.py"
COMPILER_SOURCE = (REPO_ROOT / "src" / "sanskript" / "compiler.py").read_text(encoding="utf-8", errors="replace")
COMPILER_EMITTED_OPCODES = sorted(set(re.findall(r"OpCode\.([A-Z0-9_]+)", COMPILER_SOURCE)))
# AST nodes with dedicated tests but no compile lowering yet (honest partial).
AST_COMPILE_SKIP: frozenset[str] = frozenset(
    {"DestructureAssign", "Guard", "Propagate", "ResultBind", "TypeConvert"}
)


@dataclass(frozen=True)
class CoverageProof:
    passed: bool
    parser_ast: dict[str, Any]
    vm_opcodes: dict[str, Any]
    compiler_lowerings: dict[str, Any]
    exhaustive_test_module: str
    failures: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "parser_ast": self.parser_ast,
            "vm_opcodes": self.vm_opcodes,
            "compiler_lowerings": self.compiler_lowerings,
            "exhaustive_test_module": self.exhaustive_test_module,
            "failures": list(self.failures),
        }


def _exhaustive_test_source() -> str:
    if not EXHAUSTIVE_TEST_PATH.exists():
        return ""
    return EXHAUSTIVE_TEST_PATH.read_text(encoding="utf-8", errors="replace")


def _ast_statement_nodes() -> list[str]:
    sys_path = str(REPO_ROOT)
    if sys_path not in __import__("sys").path:
        __import__("sys").path.insert(0, sys_path)
    from tools.phase0_common import ast_statement_nodes  # noqa: WPS433

    return ast_statement_nodes()


def verify_opcode_exhaustive_suite(*, execute: bool = True) -> dict[str, Any]:
    """Per-opcode dedicated smoke via phase25_opcode_smoke."""
    missing_spec: list[str] = []
    execution_failures: list[str] = []
    for opcode in OpCode:
        try:
            build_opcode_smoke_spec(opcode)
        except KeyError:
            missing_spec.append(opcode.value)
            continue
        if execute:
            try:
                run_opcode_smoke(opcode)
            except Exception as exc:  # noqa: BLE001
                execution_failures.append(f"{opcode.value}: {exc}")
    total = len(OpCode)
    covered = total - len(missing_spec)
    return {
        "opcode_enum_count": total,
        "opcodes_with_dedicated_smoke": covered,
        "opcodes_missing_smoke_spec": missing_spec,
        "execution_failures": execution_failures,
        "per_opcode_dedicated_unit_tests": len(missing_spec) == 0 and len(execution_failures) == 0,
        "claim_level": "dedicated-opcode-smoke-suite",
    }


def verify_parser_ast_exhaustive_suite(*, compile_smoke: bool = True) -> dict[str, Any]:
    """Per AST statement node: dedicated test_ast_* in exhaustive module."""
    from .phase25_ast_smoke import build_ast_program  # noqa: WPS433

    source = _exhaustive_test_source()
    nodes = _ast_statement_nodes()
    missing_tests: list[str] = []
    compile_failures: list[str] = []
    for node in nodes:
        test_name = f"test_ast_{_snake_case(node)}"
        if test_name not in source:
            missing_tests.append(node)
            continue
        if compile_smoke and node not in AST_COMPILE_SKIP:
            try:
                compile_program(build_ast_program(node))
            except Exception as exc:  # noqa: BLE001
                compile_failures.append(f"{node}: {exc}")
    return {
        "ast_statement_nodes": len(nodes),
        "nodes_with_dedicated_test": len(nodes) - len(missing_tests),
        "nodes_missing_dedicated_test": missing_tests,
        "compile_failures": compile_failures,
        "compile_skipped_nodes": sorted(AST_COMPILE_SKIP),
        "per_rule_unit_tests": len(missing_tests) == 0 and len(compile_failures) == 0,
        "claim_level": "dedicated-ast-smoke-suite",
    }


def verify_compiler_lowering_exhaustive_suite() -> dict[str, Any]:
    """Per compiler-emitted opcode: dedicated test_lowering_* in exhaustive module."""
    source = _exhaustive_test_source()
    missing: list[str] = []
    for member in COMPILER_EMITTED_OPCODES:
        test_name = f"test_lowering_{member.lower()}"
        if test_name not in source:
            missing.append(member)
    total = len(COMPILER_EMITTED_OPCODES)
    covered = total - len(missing)
    return {
        "compiler_referenced_opcodes": total,
        "lowerings_with_dedicated_test": covered,
        "lowerings_missing_dedicated_test": missing,
        "per_lowering_unit_tests": len(missing) == 0,
        "claim_level": "dedicated-lowering-test-suite",
    }


def build_coverage_proof(*, execute_opcodes: bool = True, compile_ast: bool = True) -> CoverageProof:
    """Coverage proof required before seal_ready may be considered."""
    parser = verify_parser_ast_exhaustive_suite(compile_smoke=compile_ast)
    opcodes = verify_opcode_exhaustive_suite(execute=execute_opcodes)
    lowerings = verify_compiler_lowering_exhaustive_suite()
    failures: list[str] = []
    if not EXHAUSTIVE_TEST_PATH.exists():
        failures.append(f"Missing exhaustive test module: {EXHAUSTIVE_TEST_PATH.as_posix()}")
    if not parser["per_rule_unit_tests"]:
        failures.append(
            f"Parser AST suite incomplete ({parser['nodes_with_dedicated_test']}/{parser['ast_statement_nodes']})."
        )
    if not opcodes["per_opcode_dedicated_unit_tests"]:
        failures.append(
            f"Opcode suite incomplete ({opcodes['opcodes_with_dedicated_smoke']}/{opcodes['opcode_enum_count']})."
        )
    if not lowerings["per_lowering_unit_tests"]:
        failures.append(
            f"Lowering suite incomplete ({lowerings['lowerings_with_dedicated_test']}/"
            f"{lowerings['compiler_referenced_opcodes']})."
        )
    passed = len(failures) == 0
    return CoverageProof(
        passed=passed,
        parser_ast=parser,
        vm_opcodes=opcodes,
        compiler_lowerings=lowerings,
        exhaustive_test_module=EXHAUSTIVE_TEST_PATH.as_posix(),
        failures=tuple(failures),
    )


def _snake_case(name: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()
