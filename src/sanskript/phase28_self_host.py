"""Phase 28 self-host corpus: Sanskript-authored VM/compiler subsets."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .bytecode import BytecodeProgram, Instruction, OpCode, validate_bytecode
from .compiler import compile_program
from .module_loader import load_program_from_path
from .runtime_values import NIL, to_display_string
from .stdlib_core import call_native_function, has_native_function, native_arity

SELF_HOST_DIR_NAME = "self-host"
SUBSET_VM_IMPL = "SanskriptSubsetVM"
SELF_COMPILE_STAGE = "S2-self-compiler"
SELF_COMPILE_ENGINE = "sanskript-subset-compiler"

_CORPUS_FILES: tuple[str, ...] = (
    "vm-core.ssk",
    "bytecode-verify.ssk",
    "compiler-frontend.ssk",
    "compiler-backend.ssk",
    "test-runner.ssk",
)


@dataclass(frozen=True)
class SelfHostCorpusRow:
    path: str
    compile_ok: bool
    host_output: tuple[str, ...]
    subset_output: tuple[str, ...]
    output_match: bool
    error: str | None = None


def self_host_dir(root: Path) -> Path:
    return root / "examples" / SELF_HOST_DIR_NAME


def self_host_sources(root: Path) -> list[Path]:
    base = self_host_dir(root)
    if not base.is_dir():
        return []
    return [base / name for name in _CORPUS_FILES if (base / name).is_file()]


def self_host_corpus_present(root: Path) -> bool:
    base = self_host_dir(root)
    required = (
        "vm-core.ssk",
        "bytecode-verify.ssk",
        "compiler-frontend.ssk",
        "compiler-backend.ssk",
    )
    return all((base / name).is_file() for name in required)


class SanskriptSubsetVM:
    """Minimal rakṣita-tier VM subset (no Python SanskriptVM dispatch)."""

    _SUPPORTED = frozenset(
        {
            OpCode.PUSH_INT,
            OpCode.PUSH_BOOL,
            OpCode.PUSH_NIL,
            OpCode.EMIT,
            OpCode.HALT,
            OpCode.ADD,
            OpCode.STORE_NAME,
            OpCode.LOAD_NAME,
            OpCode.CALL,
        }
    )

    def __init__(self) -> None:
        self.globals: dict[str, Any] = {}
        self.locals: dict[str, Any] = {}
        self.stack: list[Any] = []
        self.output: list[str] = []

    @property
    def implementation(self) -> str:
        return SUBSET_VM_IMPL

    @property
    def independent_vm(self) -> bool:
        return True

    @property
    def host_fallbacks(self) -> tuple[str, ...]:
        return ()

    def can_execute(self, program: BytecodeProgram) -> bool:
        for inst in program.instructions:
            if inst.opcode not in self._SUPPORTED:
                return False
        for fn in program.functions:
            for inst in fn.instructions:
                if inst.opcode not in self._SUPPORTED:
                    return False
        return True

    def execute(self, program: BytecodeProgram) -> list[str]:
        validate_bytecode(program)
        if not self.can_execute(program):
            raise RuntimeError("program uses opcodes outside SanskriptSubsetVM coverage")
        self.globals = {}
        self.locals = {}
        self.stack = []
        self.output = []
        ip = 0
        instructions = program.instructions
        while ip < len(instructions):
            inst = instructions[ip]
            opcode = inst.opcode
            operand = inst.operand
            if opcode == OpCode.PUSH_INT:
                self.stack.append(int(operand))
            elif opcode == OpCode.PUSH_BOOL:
                self.stack.append(bool(int(operand)))
            elif opcode == OpCode.PUSH_NIL:
                self.stack.append(NIL)
            elif opcode == OpCode.STORE_NAME:
                name = str(operand)
                self.locals[name] = self.stack.pop()
            elif opcode == OpCode.LOAD_NAME:
                name = str(operand)
                value = self.locals.get(name, self.globals.get(name))
                if value is None:
                    raise RuntimeError(f"undefined name {name!r}")
                self.stack.append(value)
            elif opcode == OpCode.ADD:
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left + right)
            elif opcode == OpCode.CALL:
                target = str(operand)
                if not has_native_function(target):
                    raise RuntimeError(f"subset VM cannot call {target!r}")
                arity = native_arity(target)
                args = [self.stack.pop() for _ in range(arity)]
                args.reverse()
                self.stack.append(call_native_function(target, args))
            elif opcode == OpCode.EMIT:
                self.output.append(to_display_string(self.stack.pop()))
            elif opcode == OpCode.HALT:
                break
            else:
                raise RuntimeError(f"unsupported opcode in subset VM: {opcode.value}")
            ip += 1
        return list(self.output)


def run_self_host_corpus(root: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    subset = SanskriptSubsetVM()
    for path in self_host_sources(root):
        rel = path.relative_to(root).as_posix()
        row: dict[str, Any] = {"path": rel}
        try:
            program = compile_program(load_program_from_path(path))
            from .vm import SanskriptVM

            host_out = tuple(SanskriptVM().execute(program))
            if not subset.can_execute(program):
                failures.append(f"{rel}: opcodes outside subset VM")
                row["compile_ok"] = True
                row["subset_supported"] = False
                rows.append(row)
                continue
            subset_out = tuple(subset.execute(program))
            row["compile_ok"] = True
            row["subset_supported"] = True
            row["host_output_lines"] = len(host_out)
            row["subset_output_lines"] = len(subset_out)
            row["output_match"] = host_out == subset_out
            row["subset_vm"] = subset.implementation
            row["independent_vm"] = subset.independent_vm
            if not row["output_match"]:
                failures.append(f"{rel}: subset VM output mismatch")
        except Exception as exc:
            row["compile_ok"] = False
            row["error"] = f"{type(exc).__name__}: {exc}"
            failures.append(f"{rel}: {row['error']}")
        rows.append(row)
    supported_rows = [row for row in rows if row.get("subset_supported")]
    return {
        "corpus_dir": f"examples/{SELF_HOST_DIR_NAME}",
        "subset_vm": subset.implementation,
        "independent_vm": subset.independent_vm,
        "total": len(rows),
        "passed": sum(1 for row in supported_rows if row.get("output_match")),
        "rows": rows,
        "failures": failures,
    }


def compile_self_host_source(source: Path) -> BytecodeProgram:
    return compile_program(load_program_from_path(source))


def required_host_modules_for_ordinary_dev(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    """Modules still blocking ordinary Sanskript development (excludes bootstrap/tests)."""

    bootstrap_roles = frozenset({"grammar_engine", "tests", "docs", "migration"})
    blocking: list[dict[str, Any]] = []
    for item in inventory.get("modules", []):
        if item.get("language") not in {"python", "rust"}:
            continue
        if item.get("role") in bootstrap_roles:
            continue
        if item.get("migration_label") == "keep_temporarily":
            continue
        if item.get("bootstrap_only"):
            continue
        blocking.append(item)
    return blocking
