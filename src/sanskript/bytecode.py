from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Union

from .errors import SanskriptError

BYTECODE_VERSION_1 = 1
BYTECODE_VERSION_2 = 2
BYTECODE_LATEST = BYTECODE_VERSION_2

# Operand kinds: None, "int", "name", "label"
_OPERAND_KIND: dict[str, str | None] = {
    "push_int": "int",
    "load_name": "name",
    "store_name": "name",
    "add": None,
    "subtract": None,
    "multiply": None,
    "divide": None,
    "compare_eq": None,
    "compare_lt": None,
    "emit": None,
    "jump": "label",
    "jump_if_zero": "label",
    "call": "name",
    "return": None,
    "pop": None,
    "halt": None,
}

_STACK_EFFECT: dict[str, tuple[int, int]] = {
    "push_int": (0, 1),
    "load_name": (0, 1),
    "store_name": (1, 0),
    "add": (2, 1),
    "subtract": (2, 1),
    "multiply": (2, 1),
    "divide": (2, 1),
    "compare_eq": (2, 1),
    "compare_lt": (2, 1),
    "emit": (1, 0),
    "jump": (0, 0),
    "jump_if_zero": (1, 0),
    "call": (0, 0),
    "return": (1, 0),
    "pop": (1, 0),
    "halt": (0, 0),
}

_V1_OPCODES = frozenset(
    {"push_int", "load_name", "store_name", "add", "subtract", "emit", "halt"}
)


class OpCode(str, Enum):
    PUSH_INT = "push_int"
    LOAD_NAME = "load_name"
    STORE_NAME = "store_name"
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    COMPARE_EQ = "compare_eq"
    COMPARE_LT = "compare_lt"
    EMIT = "emit"
    JUMP = "jump"
    JUMP_IF_ZERO = "jump_if_zero"
    CALL = "call"
    RETURN = "return"
    POP = "pop"
    HALT = "halt"


# Backward-compatible alias
BYTECODE_VERSION = BYTECODE_LATEST

_OPERAND_BY_OPCODE = dict(_OPERAND_KIND)


class BytecodeValidationError(SanskriptError):
    code = "SANSKRIPT_BYTECODE"


Operand = Union[int, str, None]


@dataclass(frozen=True)
class Instruction:
    opcode: OpCode
    operand: Operand = None


@dataclass(frozen=True)
class FunctionBytecode:
    name: str
    instructions: tuple[Instruction, ...]


@dataclass(frozen=True)
class ModuleBytecode:
    name: str
    functions: tuple[FunctionBytecode, ...]


@dataclass(frozen=True)
class BytecodeProgram:
    instructions: tuple[Instruction, ...]
    functions: tuple[FunctionBytecode, ...] = ()
    modules: tuple[ModuleBytecode, ...] = ()


def instruction_to_dict(instruction: Instruction) -> dict[str, Any]:
    payload: dict[str, Any] = {"op": instruction.opcode.value}
    if instruction.operand is not None:
        payload["operand"] = instruction.operand
    return payload


def instruction_from_dict(raw: dict[str, Any], *, allowed: frozenset[str] | None = None) -> Instruction:
    op_value = str(raw.get("op", ""))
    if allowed is not None and op_value not in allowed:
        raise BytecodeValidationError(f"Opcode not allowed in this bytecode version: {op_value!r}")
    try:
        opcode = OpCode(op_value)
    except ValueError as exc:
        raise BytecodeValidationError(f"Unknown opcode: {op_value!r}") from exc

    kind = _OPERAND_BY_OPCODE[opcode.value]
    operand = raw.get("operand")
    if kind is None:
        if "operand" in raw:
            raise BytecodeValidationError(f"{opcode.value} must not have an operand")
        return Instruction(opcode)

    if operand is None:
        raise BytecodeValidationError(f"{opcode.value} requires an operand")

    if kind in {"int", "label"}:
        if not isinstance(operand, int) or isinstance(operand, bool):
            raise BytecodeValidationError(
                f"{opcode.value} operand must be an integer, got {operand!r}"
            )
        return Instruction(opcode, operand)

    if kind == "name":
        if not isinstance(operand, str) or not operand:
            raise BytecodeValidationError(
                f"{opcode.value} operand must be a non-empty string name"
            )
        return Instruction(opcode, operand)

    raise BytecodeValidationError(f"Internal operand kind {kind!r}")


def _function_to_dict(function: FunctionBytecode) -> dict[str, Any]:
    return {
        "name": function.name,
        "instructions": [instruction_to_dict(item) for item in function.instructions],
    }


def _function_from_dict(raw: dict[str, Any], *, version: int) -> FunctionBytecode:
    allowed = _V1_OPCODES if version == BYTECODE_VERSION_1 else None
    name = str(raw.get("name", ""))
    if not name:
        raise BytecodeValidationError("function name is required")
    body = raw.get("instructions", [])
    if not isinstance(body, list) or not body:
        raise BytecodeValidationError(f"function {name!r} must have instructions")
    instructions = tuple(instruction_from_dict(item, allowed=allowed) for item in body)
    _validate_instruction_stream(
        instructions,
        version=version,
        strict_stack=False,
        require_halt=False,
    )
    return FunctionBytecode(name, instructions)


def encode_program(
    program: BytecodeProgram,
    *,
    version: int = BYTECODE_LATEST,
) -> dict[str, Any]:
    if version not in {BYTECODE_VERSION_1, BYTECODE_VERSION_2}:
        raise BytecodeValidationError(f"Unsupported bytecode version: {version}")
    payload: dict[str, Any] = {
        "version": version,
        "instructions": [instruction_to_dict(item) for item in program.instructions],
    }
    if version >= BYTECODE_VERSION_2 and program.functions:
        payload["functions"] = [_function_to_dict(item) for item in program.functions]
    if version >= BYTECODE_VERSION_2 and program.modules:
        payload["modules"] = [
            {
                "name": module.name,
                "functions": [_function_to_dict(fn) for fn in module.functions],
            }
            for module in program.modules
        ]
    return payload


def decode_program(payload: dict[str, Any]) -> BytecodeProgram:
    version = payload.get("version")
    if version not in {BYTECODE_VERSION_1, BYTECODE_VERSION_2}:
        raise BytecodeValidationError(
            f"Unsupported bytecode version: {version!r} "
            f"(expected {BYTECODE_VERSION_1} or {BYTECODE_VERSION_2})"
        )
    allowed = _V1_OPCODES if version == BYTECODE_VERSION_1 else None
    raw_instructions = payload.get("instructions")
    if not isinstance(raw_instructions, list) or not raw_instructions:
        raise BytecodeValidationError("instructions must be a non-empty list")
    instructions = tuple(instruction_from_dict(item, allowed=allowed) for item in raw_instructions)

    functions: list[FunctionBytecode] = []
    for raw_fn in payload.get("functions", []):
        functions.append(_function_from_dict(raw_fn, version=version))

    modules: list[ModuleBytecode] = []
    for raw_mod in payload.get("modules", []):
        mod_name = str(raw_mod.get("name", ""))
        if not mod_name:
            raise BytecodeValidationError("module name is required")
        mod_fns = tuple(
            _function_from_dict(item, version=version) for item in raw_mod.get("functions", [])
        )
        modules.append(ModuleBytecode(mod_name, mod_fns))

    program = BytecodeProgram(tuple(instructions), tuple(functions), tuple(modules))
    validate_bytecode(program, version=version)
    return program


def load_bytecode_file(path: Path | str) -> BytecodeProgram:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise BytecodeValidationError("Bytecode file must contain a JSON object")
    return decode_program(data)


def dump_bytecode_file(program: BytecodeProgram, path: Path | str, *, version: int = BYTECODE_LATEST) -> None:
    Path(path).write_text(
        json.dumps(encode_program(program, version=version), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _has_control_flow(program: BytecodeProgram) -> bool:
    control = {
        OpCode.JUMP,
        OpCode.JUMP_IF_ZERO,
        OpCode.CALL,
        OpCode.RETURN,
    }
    for stream in (program.instructions, *(f.instructions for f in program.functions)):
        if any(inst.opcode in control for inst in stream):
            return True
    return False


def validate_bytecode(program: BytecodeProgram, *, version: int = BYTECODE_LATEST) -> None:
    if not program.instructions:
        raise BytecodeValidationError("Program must contain at least one instruction")

    _validate_instruction_stream(
        program.instructions,
        version=version,
        strict_stack=not _has_control_flow(program),
        require_halt=True,
    )

    for function in program.functions:
        _validate_instruction_stream(
            function.instructions,
            version=version,
            strict_stack=False,
            require_halt=False,
        )

    for module in program.modules:
        seen: set[str] = set()
        for function in module.functions:
            if function.name in seen:
                raise BytecodeValidationError(
                    f"Duplicate function {function.name!r} in module {module.name!r}"
                )
            seen.add(function.name)
            _validate_instruction_stream(
                function.instructions,
                version=version,
                strict_stack=False,
                require_halt=False,
            )


def _validate_instruction_stream(
    instructions: tuple[Instruction, ...],
    *,
    version: int,
    strict_stack: bool,
    require_halt: bool = True,
) -> None:
    allowed = _V1_OPCODES if version == BYTECODE_VERSION_1 else None
    depth = 0
    length = len(instructions)
    for index, instruction in enumerate(instructions):
        opcode = instruction.opcode.value
        if allowed is not None and opcode not in allowed:
            raise BytecodeValidationError(f"Opcode {opcode!r} is not valid in bytecode v1")

        kind = _OPERAND_BY_OPCODE.get(opcode)
        if kind is None and opcode not in _OPERAND_BY_OPCODE:
            raise BytecodeValidationError(f"Unknown opcode at index {index}: {opcode!r}")

        if kind is None and instruction.operand is not None:
            raise BytecodeValidationError(
                f"Instruction {index} ({opcode}) must not have an operand"
            )
        if kind in {"int", "label"} and (
            not isinstance(instruction.operand, int) or isinstance(instruction.operand, bool)
        ):
            raise BytecodeValidationError(
                f"Instruction {index} ({opcode}) requires an integer operand"
            )
        if kind == "name" and (not isinstance(instruction.operand, str) or not instruction.operand):
            raise BytecodeValidationError(
                f"Instruction {index} ({opcode}) requires a non-empty name operand"
            )

        if kind == "label":
            target = instruction.operand
            if not isinstance(target, int) or target < 0 or target >= length:
                raise BytecodeValidationError(
                    f"Jump target {target!r} at instruction {index} is out of range (0..{length - 1})"
                )

        pop_count, push_count = _STACK_EFFECT[opcode]
        if strict_stack and depth < pop_count:
            raise BytecodeValidationError(
                f"Stack underflow at instruction {index} ({opcode}): depth {depth}, need {pop_count}"
            )
        if strict_stack:
            depth = depth - pop_count + push_count

    last_opcode = instructions[-1].opcode
    if require_halt:
        if last_opcode != OpCode.HALT:
            raise BytecodeValidationError("Final instruction must be halt")
    elif last_opcode not in {OpCode.HALT, OpCode.RETURN}:
        raise BytecodeValidationError("Function body must end with return or halt")

    if strict_stack and depth != 0:
        raise BytecodeValidationError(
            f"Program leaves {depth} value(s) on the stack; expected empty stack at halt"
        )


def qualified_function_name(module: str | None, name: str) -> str:
    if module:
        return f"{module}.{name}"
    return name


def resolve_call_target(program: BytecodeProgram, target: str) -> tuple[Instruction, ...]:
    if "." in target:
        module_name, fn_name = target.split(".", 1)
        for module in program.modules:
            if module.name == module_name:
                for function in module.functions:
                    if function.name in {fn_name, target}:
                        return function.instructions
        raise BytecodeValidationError(f"Unknown module function {target!r}")

    for function in program.functions:
        if function.name == target:
            return function.instructions
    raise BytecodeValidationError(f"Unknown function {target!r}")


__all__ = [
    "BYTECODE_LATEST",
    "BYTECODE_VERSION",
    "BYTECODE_VERSION_1",
    "BYTECODE_VERSION_2",
    "BytecodeProgram",
    "BytecodeValidationError",
    "FunctionBytecode",
    "Instruction",
    "ModuleBytecode",
    "OpCode",
    "Operand",
    "decode_program",
    "dump_bytecode_file",
    "encode_program",
    "instruction_from_dict",
    "instruction_to_dict",
    "load_bytecode_file",
    "qualified_function_name",
    "resolve_call_target",
    "validate_bytecode",
]
