from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from . import bytecode as bytecode_mod
from .bytecode import (
    BYTECODE_VERSION_2,
    BytecodeProgram,
    BytecodeValidationError,
    Instruction,
    OpCode,
    decode_program,
    dump_bytecode_file,
    encode_program,
    instruction_from_dict,
    load_bytecode_file,
    validate_bytecode,
)
from .yantra_patha import _parse_instruction, program_from_yantra_patha, program_to_yantra_patha

PHASE17_SPEC_VERSION = "17.0.0"
SSKYP_BINARY_MAGIC = b"SSKYP17\x00"


@dataclass(frozen=True)
class StackLayout:
    value_stack: str = "LIFO value stack"
    ownership_stack: str = "Parallel ownership tags per value"
    effect_stack: str = "Effect capability stack for call boundaries"


@dataclass(frozen=True)
class CallFrameLayout:
    function_name: str = "Symbol of active function"
    return_ip: str = "Instruction pointer to resume in caller"
    locals_slot_base: str = "Base offset for locals frame"
    stack_base: str = "Stack depth at call entry"
    exception_base: str = "Try-stack depth at call entry"


@dataclass(frozen=True)
class PoolTableLayout:
    constant_pool: str = "Deduplicated scalar constants"
    symbol_table: str = "Function/module symbols"
    debug_table: str = "Offset -> source/debug spans"
    exception_table: str = "Try ranges and handler offsets"
    ownership_table: str = "Borrow/move/alias policy metadata"


@dataclass(frozen=True)
class RuntimeMetadataLayout:
    function_table: str = "Function symbol -> entrypoint and signature metadata"
    module_table: str = "Module symbol -> exported function set and imports"
    type_table: str = "Runtime type-id -> nominal/structural descriptors"
    object_layout: str = "Object field offsets, vtable slots, and visibility bits"
    debug_table: str = "Instruction offset -> source span and inlining info"
    exception_table: str = "Try region -> handler and unwind metadata"
    ownership_table: str = "Ownership/borrow region metadata for runtime checks"


@dataclass(frozen=True)
class VerifyReport:
    ok: bool
    warnings: tuple[str, ...]
    errors: tuple[str, ...]


@dataclass(frozen=True)
class OpcodeProseEvidence:
    mapped: MappingProxyType[str, str]
    unsupported: MappingProxyType[str, str]


def _iter_instruction_streams(program: BytecodeProgram) -> list[tuple[str, tuple[Instruction, ...]]]:
    streams: list[tuple[str, tuple[Instruction, ...]]] = [("main", program.instructions)]
    streams.extend((f"function:{fn.name}", fn.instructions) for fn in program.functions)
    for mod in program.modules:
        streams.extend((f"module:{mod.name}.{fn.name}", fn.instructions) for fn in mod.functions)
    return streams


def freeze_phase17_spec() -> MappingProxyType[str, Any]:
    opcode_table = {name: index for index, name in enumerate(sorted(op.value for op in OpCode))}
    parity = opcode_machine_prose_evidence()
    spec = {
        "phase": 17,
        "version": PHASE17_SPEC_VERSION,
        "bytecode_version": BYTECODE_VERSION_2,
        "file_formats": {
            "json": ".sskbc",
            "machine_prose": ".sskyp",
            "binary": ".sskypb",
        },
        "layouts": {
            "stack": StackLayout().__dict__,
            "call_frame": CallFrameLayout().__dict__,
            "tables": PoolTableLayout().__dict__,
            "runtime_metadata": RuntimeMetadataLayout().__dict__,
        },
        "encoding": {
            "opcode_index": opcode_table,
            "operand_kind": dict(getattr(bytecode_mod, "_OPERAND_BY_OPCODE")),
            "binary_magic_hex": SSKYP_BINARY_MAGIC.hex(),
            "binary_layout": {
                "magic": "8 bytes",
                "length_prefix": "u64 big-endian payload length",
                "sha256": "32 bytes digest of canonical JSON body",
                "payload": "utf-8 canonical JSON bytecode object",
            },
        },
        "machine_prose_parity": {
            "mapped_count": len(parity.mapped),
            "unsupported_count": len(parity.unsupported),
            "unsupported_opcodes": sorted(parity.unsupported),
        },
    }
    return MappingProxyType(spec)


def verify_program_phase17(program: BytecodeProgram) -> VerifyReport:
    warnings: list[str] = []
    errors: list[str] = []
    try:
        validate_bytecode(program, version=BYTECODE_VERSION_2)
    except BytecodeValidationError as exc:
        errors.append(str(exc))
        return VerifyReport(ok=False, warnings=tuple(warnings), errors=tuple(errors))

    known_functions = {fn.name for fn in program.functions}
    for module in program.modules:
        for fn in module.functions:
            known_functions.add(fn.name)

    def _check_stream(stream: tuple[Instruction, ...], owner: str) -> None:
        for index, inst in enumerate(stream):
            if inst.opcode in {OpCode.CALL, OpCode.TAIL_CALL}:
                target = str(inst.operand)
                if "." in target:
                    mod_name, _, fn_name = target.partition(".")
                    if not any(mod.name == mod_name for mod in program.modules):
                        errors.append(f"{owner}[{index}] unknown module target {target!r}")
                    if target not in known_functions and fn_name not in known_functions:
                        errors.append(f"{owner}[{index}] unknown function target {target!r}")
                elif target not in known_functions:
                    warnings.append(f"{owner}[{index}] call target {target!r} unresolved in static image")
            if inst.opcode == OpCode.RETURN and owner == "main":
                errors.append("main stream contains return; only functions/modules may return")

    for owner, stream in _iter_instruction_streams(program):
        _check_stream(stream, owner)
    evidence = opcode_machine_prose_evidence()
    if evidence.unsupported:
        warnings.append(
            "machine-prose parity is partial: "
            f"{len(evidence.mapped)}/{len(evidence.mapped) + len(evidence.unsupported)} opcodes "
            f"have bijective opcode<->prose evidence"
        )
    return VerifyReport(ok=not errors, warnings=tuple(warnings), errors=tuple(errors))


def optimize_program_phase17(program: BytecodeProgram) -> BytecodeProgram:
    def _optimize_stream(stream: tuple[Instruction, ...]) -> tuple[Instruction, ...]:
        optimized: list[Instruction] = []
        for idx, inst in enumerate(stream):
            # Peephole: remove jumps to next instruction.
            if (
                inst.opcode == OpCode.JUMP
                and isinstance(inst.operand, int)
                and inst.operand == idx + 1
            ):
                continue
            # Peephole: remove push/pop pair.
            if optimized and inst.opcode == OpCode.POP:
                prev = optimized[-1]
                if prev.opcode in {
                    OpCode.PUSH_INT,
                    OpCode.PUSH_TEXT,
                    OpCode.PUSH_BOOL,
                    OpCode.PUSH_FLOAT,
                    OpCode.PUSH_NIL,
                }:
                    optimized.pop()
                    continue
            optimized.append(inst)
        return tuple(optimized)

    optimized = BytecodeProgram(
        instructions=_optimize_stream(program.instructions),
        functions=tuple(
            fn.__class__(
                name=fn.name,
                instructions=_optimize_stream(fn.instructions),
                params=fn.params,
                defaults=fn.defaults,
                variadic_param=fn.variadic_param,
                capture_mut=fn.capture_mut,
                effect=fn.effect,
                is_generator=fn.is_generator,
                is_memoized=fn.is_memoized,
                is_inline=fn.is_inline,
                is_naked=fn.is_naked,
                abi_name=fn.abi_name,
                named_returns=fn.named_returns,
            )
            for fn in program.functions
        ),
        modules=tuple(
            mod.__class__(
                name=mod.name,
                functions=tuple(
                    fn.__class__(
                        name=fn.name,
                        instructions=_optimize_stream(fn.instructions),
                        params=fn.params,
                        defaults=fn.defaults,
                        variadic_param=fn.variadic_param,
                        capture_mut=fn.capture_mut,
                        effect=fn.effect,
                        is_generator=fn.is_generator,
                        is_memoized=fn.is_memoized,
                        is_inline=fn.is_inline,
                        is_naked=fn.is_naked,
                        abi_name=fn.abi_name,
                        named_returns=fn.named_returns,
                    )
                    for fn in mod.functions
                ),
            )
            for mod in program.modules
        ),
        safety_tier=program.safety_tier,
        defer_blocks=program.defer_blocks,
    )
    validate_bytecode(optimized, version=BYTECODE_VERSION_2)
    return optimized


def link_programs_phase17(programs: list[BytecodeProgram]) -> BytecodeProgram:
    if not programs:
        raise BytecodeValidationError("link requires at least one program")
    main = programs[0]
    instructions: list[Instruction] = []
    for index, program in enumerate(programs):
        stream = list(program.instructions)
        if index < len(programs) - 1 and stream and stream[-1].opcode == OpCode.HALT:
            stream.pop()
        instructions.extend(stream)
    functions = list(main.functions)
    modules = list(main.modules)
    seen = {fn.name for fn in functions}
    seen_modules = {mod.name for mod in modules}
    for mod in modules:
        for fn in mod.functions:
            seen.add(fn.name)
    for program in programs[1:]:
        for fn in program.functions:
            if fn.name in seen:
                raise BytecodeValidationError(f"duplicate function during link: {fn.name!r}")
            functions.append(fn)
            seen.add(fn.name)
        for mod in program.modules:
            if mod.name in seen_modules:
                raise BytecodeValidationError(f"duplicate module during link: {mod.name!r}")
            modules.append(mod)
            seen_modules.add(mod.name)
    linked = BytecodeProgram(
        instructions=tuple(instructions),
        functions=tuple(functions),
        modules=tuple(modules),
        safety_tier=main.safety_tier,
        defer_blocks=main.defer_blocks,
    )
    validate_bytecode(linked, version=BYTECODE_VERSION_2)
    return linked


def serialize_canonical_json(program: BytecodeProgram) -> str:
    payload = encode_program(program, version=BYTECODE_VERSION_2)
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def deserialize_canonical_json(source: str) -> BytecodeProgram:
    parsed = json.loads(source)
    if not isinstance(parsed, dict):
        raise BytecodeValidationError("canonical payload must be an object")
    return decode_program(parsed)


def serialize_binary(program: BytecodeProgram) -> bytes:
    body = serialize_canonical_json(program).encode("utf-8")
    length = len(body).to_bytes(8, byteorder="big", signed=False)
    digest = hashlib.sha256(body).digest()
    return SSKYP_BINARY_MAGIC + length + digest + body


def deserialize_binary(blob: bytes) -> BytecodeProgram:
    if len(blob) < len(SSKYP_BINARY_MAGIC) + 8 + 32:
        raise BytecodeValidationError("binary blob too short")
    if not blob.startswith(SSKYP_BINARY_MAGIC):
        raise BytecodeValidationError("invalid binary magic")
    offset = len(SSKYP_BINARY_MAGIC)
    declared = int.from_bytes(blob[offset : offset + 8], byteorder="big", signed=False)
    offset += 8
    digest = blob[offset : offset + 32]
    offset += 32
    body = blob[offset:]
    if declared != len(body):
        raise BytecodeValidationError("binary length prefix mismatch")
    if hashlib.sha256(body).digest() != digest:
        raise BytecodeValidationError("binary sha256 mismatch")
    return deserialize_canonical_json(body.decode("utf-8"))


def render_machine_prose(program: BytecodeProgram) -> str:
    return program_to_yantra_patha(program)


def parse_machine_prose(source: str) -> BytecodeProgram:
    return program_from_yantra_patha(source)


def _sample_instruction_for_opcode(opcode: OpCode, kind: str | None) -> Instruction:
    if kind == "int" or kind == "label":
        return Instruction(opcode, 1)
    if kind == "float":
        return Instruction(opcode, 1.0)
    if kind == "text":
        return Instruction(opcode, "x")
    if kind == "name":
        return Instruction(opcode, "fn")
    return Instruction(opcode)


def opcode_machine_prose_evidence() -> OpcodeProseEvidence:
    operand_kinds = dict(getattr(bytecode_mod, "_OPERAND_BY_OPCODE"))
    mapping: dict[str, str] = {}
    prose_to_opcode: dict[str, str] = {}
    unsupported: dict[str, str] = {}
    for opcode in sorted(OpCode, key=lambda item: item.value):
        kind = operand_kinds.get(opcode.value)
        inst = _sample_instruction_for_opcode(opcode, kind)
        try:
            rendered = program_to_yantra_patha(
                BytecodeProgram((Instruction(OpCode.HALT), inst, Instruction(OpCode.HALT)))
            )
            sentence = rendered.splitlines()[4]
            roundtrip_inst = _parse_instruction(sentence.rstrip("."))
        except BytecodeValidationError as exc:
            unsupported[opcode.value] = str(exc)
            continue
        if roundtrip_inst != inst:
            raise BytecodeValidationError(f"opcode prose mapping is not one-to-one for {opcode.value}")
        if sentence in prose_to_opcode:
            raise BytecodeValidationError(
                f"opcode prose sentence collision: {opcode.value} and {prose_to_opcode[sentence]}"
            )
        prose_to_opcode[sentence] = opcode.value
        mapping[opcode.value] = sentence
    return OpcodeProseEvidence(
        mapped=MappingProxyType(mapping),
        unsupported=MappingProxyType(unsupported),
    )


def opcode_machine_prose_map() -> dict[str, str]:
    return dict(opcode_machine_prose_evidence().mapped)


def load_program_any(path: str | Path) -> BytecodeProgram:
    file_path = Path(path)
    if file_path.suffix == ".sskyp":
        return parse_machine_prose(file_path.read_text(encoding="utf-8"))
    if file_path.suffix == ".sskypb":
        return deserialize_binary(file_path.read_bytes())
    return load_bytecode_file(file_path)


def save_program_any(program: BytecodeProgram, path: str | Path) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if file_path.suffix == ".sskyp":
        file_path.write_text(render_machine_prose(program), encoding="utf-8")
        return
    if file_path.suffix == ".sskypb":
        file_path.write_bytes(serialize_binary(program))
        return
    dump_bytecode_file(program, file_path, version=BYTECODE_VERSION_2)


def roundtrip_conformance(program: BytecodeProgram) -> None:
    canonical = serialize_canonical_json(program)
    restored = deserialize_canonical_json(canonical)
    validate_bytecode(restored, version=BYTECODE_VERSION_2)
    if restored != program:
        raise BytecodeValidationError("canonical json round-trip changed bytecode payload")
    prose = render_machine_prose(restored)
    reparsed = parse_machine_prose(prose)
    validate_bytecode(reparsed, version=BYTECODE_VERSION_2)
    if reparsed != restored:
        raise BytecodeValidationError(".sskyp round-trip changed bytecode payload")
    blob = serialize_binary(reparsed)
    rebinary = deserialize_binary(blob)
    validate_bytecode(rebinary, version=BYTECODE_VERSION_2)
    if rebinary != reparsed:
        raise BytecodeValidationError("binary .sskypb round-trip changed bytecode payload")


def assemble(source: str) -> BytecodeProgram:
    return parse_machine_prose(source)


def disassemble(program: BytecodeProgram) -> str:
    return render_machine_prose(program)


__all__ = [
    "PHASE17_SPEC_VERSION",
    "SSKYP_BINARY_MAGIC",
    "VerifyReport",
    "assemble",
    "deserialize_binary",
    "deserialize_canonical_json",
    "disassemble",
    "freeze_phase17_spec",
    "link_programs_phase17",
    "load_program_any",
    "OpcodeProseEvidence",
    "opcode_machine_prose_evidence",
    "opcode_machine_prose_map",
    "optimize_program_phase17",
    "parse_machine_prose",
    "render_machine_prose",
    "roundtrip_conformance",
    "save_program_any",
    "serialize_binary",
    "serialize_canonical_json",
    "verify_program_phase17",
]
