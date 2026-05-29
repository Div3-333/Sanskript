"""Minimal VM smoke programs — one dedicated exercise per OpCode for Phase 25."""

from __future__ import annotations

from dataclasses import dataclass

from .bytecode import BytecodeProgram, BytecodeValidationError, FunctionBytecode, Instruction, OpCode, validate_bytecode
from .errors import RuntimeSanskriptError, SanskriptError
from .vm import SanskriptVM

_STUB = "phase25_stub"


def _fn(name: str, body: tuple[Instruction, ...], *, params: tuple[str, ...] = ()) -> FunctionBytecode:
    return FunctionBytecode(name=name, instructions=body + (Instruction(OpCode.RETURN),), params=params)


def _identity() -> FunctionBytecode:
    return _fn(
        _STUB,
        (
            Instruction(OpCode.LOAD_NAME, "x"),
            Instruction(OpCode.RETURN),
        ),
        params=("x",),
    )


def _binary_stub() -> FunctionBytecode:
    return _fn(
        f"{_STUB}_bin",
        (
            Instruction(OpCode.LOAD_NAME, "a"),
            Instruction(OpCode.LOAD_NAME, "b"),
            Instruction(OpCode.ADD),
            Instruction(OpCode.RETURN),
        ),
        params=("a", "b"),
    )


def _halt(*extra: Instruction, safety_tier: str = "surakshita", functions: tuple[FunctionBytecode, ...] = ()) -> BytecodeProgram:
    return BytecodeProgram((*extra, Instruction(OpCode.HALT)), functions=functions, safety_tier=safety_tier)


def _pop_halt(*extra: Instruction, safety_tier: str = "surakshita", functions: tuple[FunctionBytecode, ...] = ()) -> BytecodeProgram:
    return BytecodeProgram((*extra, Instruction(OpCode.POP), Instruction(OpCode.HALT)), functions=functions, safety_tier=safety_tier)


def _emit_halt(*extra: Instruction, safety_tier: str = "surakshita", functions: tuple[FunctionBytecode, ...] = ()) -> BytecodeProgram:
    return BytecodeProgram((*extra, Instruction(OpCode.EMIT), Instruction(OpCode.HALT)), functions=functions, safety_tier=safety_tier)


@dataclass(frozen=True)
class OpcodeSmokeSpec:
    program: BytecodeProgram
    expect_error: type[BaseException] | tuple[type[BaseException], ...] | None = None
    validate_only: bool = False


def _arith(op: OpCode) -> OpcodeSmokeSpec:
    return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_INT, 2), Instruction(OpCode.PUSH_INT, 3), Instruction(op)))


def _unary_int(op: OpCode, value: int = 5) -> OpcodeSmokeSpec:
    return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_INT, value), Instruction(op)))


def _compare(op: OpCode) -> OpcodeSmokeSpec:
    return OpcodeSmokeSpec(
        _emit_halt(
            Instruction(OpCode.PUSH_INT, 1),
            Instruction(OpCode.PUSH_INT, 2),
            Instruction(op),
        )
    )


def _list_with_items() -> tuple[Instruction, ...]:
    return (
        Instruction(OpCode.LIST_NEW),
        Instruction(OpCode.PUSH_INT, 1),
        Instruction(OpCode.LIST_APPEND),
        Instruction(OpCode.PUSH_INT, 2),
        Instruction(OpCode.LIST_APPEND),
    )


def build_opcode_smoke_spec(opcode: OpCode) -> OpcodeSmokeSpec:
    """Return a minimal program that executes the given opcode at least once."""
    op = opcode
    identity = (_identity(),)

    if op == OpCode.PUSH_INT:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_INT, 7)))
    if op == OpCode.PUSH_TEXT:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_TEXT, "a")))
    if op == OpCode.PUSH_BOOL:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_BOOL, 1)))
    if op == OpCode.PUSH_FLOAT:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_FLOAT, 1.0)))
    if op == OpCode.PUSH_NIL:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_NIL)))
    if op == OpCode.PUSH_BIGINT:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_BIGINT, 99)))
    if op == OpCode.PUSH_I32:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_I32, 4)))
    if op == OpCode.PUSH_U32:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_U32, 4)))
    if op == OpCode.PUSH_BYTES:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_BYTES, "ff00")))
    if op in {OpCode.ADD, OpCode.SUBTRACT, OpCode.MULTIPLY, OpCode.DIVIDE}:
        return _arith(op)
    if op in {
        OpCode.COMPARE_EQ,
        OpCode.COMPARE_NE,
        OpCode.COMPARE_LT,
        OpCode.COMPARE_GT,
        OpCode.COMPARE_LE,
        OpCode.COMPARE_IDENTITY,
    }:
        return _compare(op)
    if op == OpCode.TEXT_CONCAT:
        return OpcodeSmokeSpec(
            _emit_halt(Instruction(OpCode.PUSH_TEXT, "a"), Instruction(OpCode.PUSH_TEXT, "b"), Instruction(op))
        )
    if op == OpCode.TEXT_LEN:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_TEXT, "ab"), Instruction(op)))
    if op == OpCode.TEXT_GET:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_TEXT, "ab"), Instruction(OpCode.PUSH_INT, 0), Instruction(op)))
    if op == OpCode.TEXT_SLICE:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.PUSH_TEXT, "abcd"),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.PUSH_INT, 3),
                Instruction(op),
            )
        )
    if op == OpCode.TEXT_CONTAINS:
        return OpcodeSmokeSpec(
            _emit_halt(Instruction(OpCode.PUSH_TEXT, "abc"), Instruction(OpCode.PUSH_TEXT, "b"), Instruction(op))
        )
    if op == OpCode.TEXT_GRAPHEME_LEN:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_TEXT, "a"), Instruction(op)))
    if op == OpCode.LIST_NEW:
        return OpcodeSmokeSpec(_pop_halt(Instruction(op)))
    if op == OpCode.LIST_APPEND:
        return OpcodeSmokeSpec(_pop_halt(Instruction(OpCode.LIST_NEW), Instruction(OpCode.PUSH_INT, 1), Instruction(op)))
    if op == OpCode.LIST_LEN:
        return OpcodeSmokeSpec(_emit_halt(*_list_with_items(), Instruction(op)))
    if op == OpCode.LIST_GET:
        return OpcodeSmokeSpec(_emit_halt(*_list_with_items(), Instruction(OpCode.PUSH_INT, 0), Instruction(op)))
    if op in {OpCode.LIST_MAP, OpCode.LIST_FILTER, OpCode.LIST_ALL, OpCode.LIST_ANY}:
        return OpcodeSmokeSpec(
            _emit_halt(*_list_with_items(), Instruction(op, _STUB), functions=identity),
        )
    if op == OpCode.LIST_REDUCE:
        bin_fn = (_binary_stub(),)
        return OpcodeSmokeSpec(
            _emit_halt(
                *_list_with_items(),
                Instruction(OpCode.PUSH_INT, 0),
                Instruction(op, f"{_STUB}_bin"),
                functions=bin_fn,
            ),
        )
    if op == OpCode.LIST_SCAN:
        return OpcodeSmokeSpec(
            _emit_halt(
                *_list_with_items(),
                Instruction(OpCode.PUSH_INT, 0),
                Instruction(op, f"{_STUB},{_STUB}"),
                functions=identity,
            ),
            validate_only=True,
        )
    if op == OpCode.LIST_ZIP:
        return OpcodeSmokeSpec(
            _emit_halt(*_list_with_items(), *_list_with_items(), Instruction(op)),
        )
    if op == OpCode.LIST_ENUMERATE:
        return OpcodeSmokeSpec(_emit_halt(*_list_with_items(), Instruction(op)))
    if op == OpCode.LIST_COMPREHENSION:
        return OpcodeSmokeSpec(
            _emit_halt(*_list_with_items(), Instruction(op, f"{_STUB},{_STUB}"), functions=identity),
        )
    if op == OpCode.IMMUTABLE_LIST_NEW:
        return OpcodeSmokeSpec(_pop_halt(Instruction(op)))
    if op == OpCode.IMMUTABLE_LIST_APPEND:
        return OpcodeSmokeSpec(
            _pop_halt(Instruction(OpCode.IMMUTABLE_LIST_NEW), Instruction(OpCode.PUSH_INT, 1), Instruction(op)),
        )
    if op == OpCode.IMMUTABLE_LIST_LEN:
        return OpcodeSmokeSpec(
            _emit_halt(Instruction(OpCode.IMMUTABLE_LIST_NEW), Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.IMMUTABLE_LIST_APPEND), Instruction(op)),
        )
    if op == OpCode.IMMUTABLE_LIST_GET:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.IMMUTABLE_LIST_NEW),
                Instruction(OpCode.PUSH_INT, 3),
                Instruction(OpCode.IMMUTABLE_LIST_APPEND),
                Instruction(OpCode.PUSH_INT, 0),
                Instruction(op),
            ),
        )
    if op == OpCode.LAZY_ITER_NEW:
        return OpcodeSmokeSpec(_pop_halt(*_list_with_items(), Instruction(op)))
    if op == OpCode.LAZY_ITER_NEXT:
        return OpcodeSmokeSpec(
            _pop_halt(*_list_with_items(), Instruction(OpCode.LAZY_ITER_NEW), Instruction(op)),
        )
    if op == OpCode.GENERATOR_NEW:
        gen = FunctionBytecode(
            name="gen",
            instructions=(Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.RETURN)),
            is_generator=True,
        )
        return OpcodeSmokeSpec(_halt(Instruction(op, "gen"), functions=(gen,)))
    if op == OpCode.GENERATOR_NEXT:
        gen = FunctionBytecode(
            name="gen",
            instructions=(Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.RETURN)),
            is_generator=True,
        )
        return OpcodeSmokeSpec(
            _halt(Instruction(OpCode.GENERATOR_NEW, "gen"), Instruction(op), functions=(gen,)),
            validate_only=True,
        )
    if op == OpCode.GENERATOR_YIELD:
        gen = FunctionBytecode(
            name="gen",
            instructions=(Instruction(OpCode.PUSH_INT, 1), Instruction(op), Instruction(OpCode.RETURN)),
            is_generator=True,
        )
        return OpcodeSmokeSpec(_halt(Instruction(OpCode.GENERATOR_NEW, "gen"), functions=(gen,)))
    if op == OpCode.PIPELINE_CHAIN:
        return OpcodeSmokeSpec(
            _emit_halt(*_list_with_items(), Instruction(op, _STUB), functions=identity),
        )
    if op == OpCode.RESULT_BIND:
        ok_fn = _fn("okfn", (Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.RETURN)), params=("v",))
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.RESULT_OK),
                Instruction(op, "okfn"),
                functions=(ok_fn,),
            ),
        )
    if op == OpCode.DATA_QUERY:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.RECORD_NEW),
                Instruction(OpCode.PUSH_TEXT, "f"),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.RECORD_SET),
                *_list_with_items(),
                Instruction(op, f"f,{_STUB}"),
                functions=identity,
            ),
        )
    if op == OpCode.RULE_REGISTER:
        return OpcodeSmokeSpec(_halt(Instruction(op, f"r1,{_STUB},{_STUB}")), validate_only=True)
    if op == OpCode.RULE_INVOKE:
        return OpcodeSmokeSpec(
            _pop_halt(
                Instruction(OpCode.RULE_REGISTER, f"r1,{_STUB},{_STUB}"),
                Instruction(OpCode.PUSH_INT, 2),
                Instruction(op, "r1"),
                functions=identity,
            ),
        )
    if op == OpCode.MEMO_CALL:
        memo = _fn(_STUB, (Instruction(OpCode.LOAD_NAME, "x"), Instruction(OpCode.RETURN)), params=("x",))
        memo = FunctionBytecode(
            name=_STUB,
            instructions=(Instruction(OpCode.LOAD_NAME, "x"), Instruction(OpCode.RETURN)),
            params=("x",),
            is_memoized=True,
        )
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_INT, 1), Instruction(op, _STUB), functions=(memo,)))
    if op == OpCode.MAP_NEW:
        return OpcodeSmokeSpec(_pop_halt(Instruction(op)))
    if op == OpCode.MAP_SET:
        return OpcodeSmokeSpec(
            _pop_halt(
                Instruction(OpCode.MAP_NEW),
                Instruction(OpCode.PUSH_TEXT, "k"),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(op),
            ),
        )
    if op == OpCode.MAP_GET:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.MAP_NEW),
                Instruction(OpCode.PUSH_TEXT, "k"),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.MAP_SET),
                Instruction(OpCode.PUSH_TEXT, "k"),
                Instruction(op),
            ),
        )
    if op == OpCode.MAP_CONTAINS:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.MAP_NEW),
                Instruction(OpCode.PUSH_TEXT, "k"),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.MAP_SET),
                Instruction(OpCode.PUSH_TEXT, "k"),
                Instruction(op),
            ),
        )
    if op == OpCode.RECORD_NEW:
        return OpcodeSmokeSpec(_pop_halt(Instruction(op)))
    if op == OpCode.RECORD_SET:
        return OpcodeSmokeSpec(
            _pop_halt(
                Instruction(OpCode.RECORD_NEW),
                Instruction(OpCode.PUSH_TEXT, "f"),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(op),
            ),
        )
    if op == OpCode.RECORD_GET:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.RECORD_NEW),
                Instruction(OpCode.PUSH_TEXT, "f"),
                Instruction(OpCode.PUSH_INT, 2),
                Instruction(OpCode.RECORD_SET),
                Instruction(OpCode.PUSH_TEXT, "f"),
                Instruction(op),
            ),
        )
    if op == OpCode.RECORD_CONTAINS:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.RECORD_NEW),
                Instruction(OpCode.PUSH_TEXT, "f"),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.RECORD_SET),
                Instruction(OpCode.PUSH_TEXT, "f"),
                Instruction(op),
            ),
        )
    if op == OpCode.CLASS_NEW:
        return OpcodeSmokeSpec(_pop_halt(Instruction(op, "C")))
    if op == OpCode.METHOD_CALL:
        return OpcodeSmokeSpec(
            _pop_halt(
                Instruction(OpCode.CLASS_NEW, "C"),
                Instruction(op, "C__m"),
                functions=(_fn("C__m", (Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.RETURN)), params=("self",)),),
            ),
            validate_only=True,
        )
    if op in {OpCode.I32_ADD_CHECKED, OpCode.U32_ADD_CHECKED, OpCode.I32_ADD_WRAPPING, OpCode.U32_ADD_WRAPPING, OpCode.I32_ADD_SATURATING, OpCode.U32_ADD_SATURATING}:
        return OpcodeSmokeSpec(
            _emit_halt(Instruction(OpCode.PUSH_I32, 1), Instruction(OpCode.PUSH_I32, 2), Instruction(op))
            if "i32" in op.value
            else _emit_halt(Instruction(OpCode.PUSH_U32, 1), Instruction(OpCode.PUSH_U32, 2), Instruction(op))
        )
    if op == OpCode.BYTE_NEW:
        return OpcodeSmokeSpec(_emit_halt(Instruction(op)))
    if op == OpCode.BYTE_LEN:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_BYTES, "aabb"), Instruction(op)))
    if op == OpCode.BYTE_GET:
        return OpcodeSmokeSpec(
            _emit_halt(Instruction(OpCode.PUSH_BYTES, "aabb"), Instruction(OpCode.PUSH_INT, 0), Instruction(op)),
        )
    if op == OpCode.BYTEARRAY_NEW:
        return OpcodeSmokeSpec(_pop_halt(Instruction(op)))
    if op == OpCode.BYTEARRAY_SET:
        return OpcodeSmokeSpec(
            _pop_halt(Instruction(OpCode.BYTEARRAY_NEW), Instruction(OpCode.PUSH_INT, 0), Instruction(OpCode.PUSH_INT, 9), Instruction(op)),
        )
    if op == OpCode.BYTEARRAY_GET:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.BYTEARRAY_NEW),
                Instruction(OpCode.PUSH_INT, 0),
                Instruction(OpCode.PUSH_INT, 3),
                Instruction(OpCode.BYTEARRAY_SET),
                Instruction(OpCode.PUSH_INT, 0),
                Instruction(op),
            ),
        )
    if op == OpCode.TUPLE_NEW:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.PUSH_INT, 2), Instruction(op, 2)))
    if op == OpCode.TUPLE_GET:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.PUSH_INT, 2),
                Instruction(OpCode.TUPLE_NEW, 2),
                Instruction(op, 0),
            ),
        )
    if op == OpCode.SET_NEW:
        return OpcodeSmokeSpec(_pop_halt(Instruction(op)))
    if op == OpCode.SET_ADD:
        return OpcodeSmokeSpec(_pop_halt(Instruction(OpCode.SET_NEW), Instruction(OpCode.PUSH_INT, 1), Instruction(op)))
    if op == OpCode.SET_CONTAINS:
        return OpcodeSmokeSpec(
            _emit_halt(Instruction(OpCode.SET_NEW), Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.SET_ADD), Instruction(OpCode.PUSH_INT, 1), Instruction(op)),
        )
    if op == OpCode.SET_LEN:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.SET_NEW), Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.SET_ADD), Instruction(op)))
    if op == OpCode.DEQUE_NEW:
        return OpcodeSmokeSpec(_pop_halt(Instruction(op)))
    if op in {OpCode.DEQUE_PUSH_BACK, OpCode.DEQUE_PUSH_FRONT}:
        return OpcodeSmokeSpec(_pop_halt(Instruction(OpCode.DEQUE_NEW), Instruction(OpCode.PUSH_INT, 1), Instruction(op)))
    if op in {OpCode.DEQUE_POP_BACK, OpCode.DEQUE_POP_FRONT}:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.DEQUE_NEW),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.DEQUE_PUSH_BACK),
                Instruction(op),
            ),
        )
    if op == OpCode.DEQUE_LEN:
        return OpcodeSmokeSpec(
            _emit_halt(Instruction(OpCode.DEQUE_NEW), Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.DEQUE_PUSH_BACK), Instruction(op)),
        )
    if op == OpCode.OPTION_NONE:
        return OpcodeSmokeSpec(_pop_halt(Instruction(op)))
    if op == OpCode.OPTION_SOME:
        return OpcodeSmokeSpec(_pop_halt(Instruction(OpCode.PUSH_INT, 1), Instruction(op)))
    if op == OpCode.OPTION_IS_SOME:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.OPTION_SOME), Instruction(op)))
    if op == OpCode.OPTION_UNWRAP:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.OPTION_SOME), Instruction(op)))
    if op == OpCode.RESULT_OK:
        return OpcodeSmokeSpec(_pop_halt(Instruction(OpCode.PUSH_INT, 1), Instruction(op)))
    if op == OpCode.RESULT_ERR:
        return OpcodeSmokeSpec(_pop_halt(Instruction(OpCode.PUSH_TEXT, "e"), Instruction(op)))
    if op == OpCode.RESULT_IS_OK:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.RESULT_OK), Instruction(op)))
    if op == OpCode.RESULT_UNWRAP_OK:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.RESULT_OK), Instruction(op)))
    if op == OpCode.RESULT_UNWRAP_ERR:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_TEXT, "e"), Instruction(OpCode.RESULT_ERR), Instruction(op)))
    if op == OpCode.FLOAT_IS_NAN:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_FLOAT, float("nan")), Instruction(op)))
    if op == OpCode.FLOAT_IS_INF:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_FLOAT, float("inf")), Instruction(op)))
    if op == OpCode.OPAQUE_NEW:
        return OpcodeSmokeSpec(_pop_halt(Instruction(OpCode.PUSH_INT, 1), Instruction(op, "tag")))
    if op == OpCode.ARRAY_NEW:
        return OpcodeSmokeSpec(_pop_halt(Instruction(op, 2)))
    if op == OpCode.SLICE_VIEW:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.ARRAY_NEW, 3),
                Instruction(OpCode.PUSH_INT, 0),
                Instruction(OpCode.PUSH_INT, 2),
                Instruction(op),
            ),
        )
    if op in {OpCode.BIT_AND, OpCode.BIT_OR, OpCode.BIT_XOR, OpCode.SHIFT_LEFT, OpCode.SHIFT_RIGHT, OpCode.ROTATE_LEFT32, OpCode.ROTATE_RIGHT32}:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_INT, 6), Instruction(OpCode.PUSH_INT, 3), Instruction(op)))
    if op == OpCode.BIT_NOT:
        return _unary_int(op)
    if op == OpCode.REG_SET:
        return OpcodeSmokeSpec(_halt(Instruction(OpCode.PUSH_INT, 1), Instruction(op, "r0")))
    if op == OpCode.REG_GET:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_INT, 2), Instruction(OpCode.REG_SET, "r0"), Instruction(op, "r0")))
    if op == OpCode.SP_SET:
        return OpcodeSmokeSpec(_halt(Instruction(OpCode.PUSH_INT, 0), Instruction(op)))
    if op == OpCode.SP_GET:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.SP_GET)))
    if op == OpCode.FP_SET:
        return OpcodeSmokeSpec(_halt(Instruction(OpCode.PUSH_INT, 0), Instruction(op)))
    if op == OpCode.FP_GET:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.FP_GET)))
    if op == OpCode.CALL_CONV:
        return OpcodeSmokeSpec(_halt(Instruction(op, "cdecl")))
    if op in {OpCode.PROLOGUE, OpCode.EPILOGUE}:
        return OpcodeSmokeSpec(_halt(Instruction(op), safety_tier="arakshita"))
    if op == OpCode.FENCE:
        return OpcodeSmokeSpec(_halt(Instruction(op, "seq_cst"), safety_tier="arakshita"))
    if op == OpCode.INLINE_ASM:
        return OpcodeSmokeSpec(_halt(Instruction(op, "nop"), safety_tier="arakshita"))
    if op == OpCode.LABEL:
        return OpcodeSmokeSpec(_halt(Instruction(op, "L0"), Instruction(OpCode.HALT)))
    if op == OpCode.JUMP_LABEL:
        return OpcodeSmokeSpec(
            BytecodeProgram(
                (
                    Instruction(op, "end"),
                    Instruction(OpCode.PUSH_INT, 1),
                    Instruction(OpCode.EMIT),
                    Instruction(OpCode.LABEL, "end"),
                    Instruction(OpCode.HALT),
                ),
            ),
        )
    if op == OpCode.JUMP_IF_ZERO_LABEL:
        return OpcodeSmokeSpec(
            BytecodeProgram(
                (
                    Instruction(OpCode.PUSH_INT, 0),
                    Instruction(op, "end"),
                    Instruction(OpCode.PUSH_INT, 9),
                    Instruction(OpCode.EMIT),
                    Instruction(OpCode.LABEL, "end"),
                    Instruction(OpCode.HALT),
                ),
            ),
        )
    if op == OpCode.JUMP_INDIRECT:
        return OpcodeSmokeSpec(
            BytecodeProgram(
                (
                    Instruction(OpCode.PUSH_INT, 2),
                    Instruction(op),
                    Instruction(OpCode.PUSH_INT, 1),
                    Instruction(OpCode.EMIT),
                    Instruction(OpCode.HALT),
                ),
            ),
        )
    if op == OpCode.CALL_INDIRECT:
        callee = _fn("f", (Instruction(OpCode.PUSH_INT, 2), Instruction(OpCode.RETURN)))
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_TEXT, "f"), Instruction(op), functions=(callee,)))
    if op == OpCode.SYSCALL:
        return OpcodeSmokeSpec(
            _pop_halt(Instruction(op, "noop"), safety_tier="arakshita"),
            expect_error=RuntimeSanskriptError,
        )
    if op == OpCode.TRAP:
        return OpcodeSmokeSpec(
            _halt(Instruction(op, 0), safety_tier="arakshita"),
            expect_error=(RuntimeSanskriptError, SanskriptError),
        )
    if op in {OpCode.MMIO_READ, OpCode.MMIO_WRITE, OpCode.ATOMIC_CAS_U32_LE}:
        return OpcodeSmokeSpec(
            _pop_halt(
                Instruction(OpCode.PUSH_INT, 0),
                Instruction(OpCode.PUSH_INT, 0),
                Instruction(OpCode.PUSH_INT, 0),
                Instruction(op),
                safety_tier="arakshita",
            ),
            validate_only=True,
        )
    if op == OpCode.LOAD_NAME:
        return OpcodeSmokeSpec(
            _emit_halt(Instruction(OpCode.PUSH_INT, 3), Instruction(OpCode.STORE_NAME, "v"), Instruction(op, "v")),
        )
    if op == OpCode.STORE_NAME:
        return OpcodeSmokeSpec(_halt(Instruction(OpCode.PUSH_INT, 3), Instruction(op, "v")))
    if op == OpCode.SCOPE_ENTER:
        return OpcodeSmokeSpec(_halt(Instruction(op), Instruction(OpCode.SCOPE_EXIT)))
    if op == OpCode.SCOPE_EXIT:
        return OpcodeSmokeSpec(_halt(Instruction(OpCode.SCOPE_ENTER), Instruction(op)))
    if op == OpCode.BREAK_LOOP:
        return OpcodeSmokeSpec(_halt(Instruction(op, "L0")), expect_error=RuntimeSanskriptError)
    if op == OpCode.CONTINUE_LOOP:
        return OpcodeSmokeSpec(_halt(Instruction(op, "L0")), expect_error=RuntimeSanskriptError)
    if op == OpCode.DEFER_PUSH:
        return OpcodeSmokeSpec(
            BytecodeProgram(
                (Instruction(op, 0), Instruction(OpCode.DEFER_RUN), Instruction(OpCode.HALT)),
                defer_blocks=((Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.EMIT)),),
            ),
        )
    if op == OpCode.DEFER_RUN:
        return OpcodeSmokeSpec(
            BytecodeProgram(
                (Instruction(OpCode.DEFER_PUSH, 0), Instruction(op), Instruction(OpCode.HALT)),
                defer_blocks=((Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.EMIT)),),
            ),
        )
    if op == OpCode.MATCH_EQ:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_INT, 1), Instruction(OpCode.PUSH_INT, 1), Instruction(op)))
    if op == OpCode.MATCH_TUPLE_LEN:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.TUPLE_NEW, 1),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(op, 1),
            ),
        )
    if op == OpCode.MATCH_RECORD_HAS:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.RECORD_NEW),
                Instruction(OpCode.PUSH_TEXT, "f"),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.RECORD_SET),
                Instruction(op, "f"),
            ),
            validate_only=True,
        )
    if op == OpCode.EMIT:
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.PUSH_INT, 1)))
    if op == OpCode.JUMP:
        return OpcodeSmokeSpec(
            BytecodeProgram(
                (
                    Instruction(op, 3),
                    Instruction(OpCode.PUSH_INT, 9),
                    Instruction(OpCode.EMIT),
                    Instruction(OpCode.HALT),
                ),
            ),
        )
    if op == OpCode.JUMP_IF_ZERO:
        return OpcodeSmokeSpec(
            BytecodeProgram(
                (
                    Instruction(OpCode.PUSH_INT, 0),
                    Instruction(op, 4),
                    Instruction(OpCode.PUSH_INT, 9),
                    Instruction(OpCode.EMIT),
                    Instruction(OpCode.HALT),
                ),
            ),
        )
    if op == OpCode.CALL:
        callee = _fn("f", (Instruction(OpCode.PUSH_INT, 2), Instruction(OpCode.RETURN)))
        return OpcodeSmokeSpec(_emit_halt(Instruction(op, "f"), functions=(callee,)))
    if op == OpCode.TAIL_CALL:
        callee = _fn("f", (Instruction(OpCode.PUSH_INT, 2), Instruction(OpCode.RETURN)))
        return OpcodeSmokeSpec(_emit_halt(Instruction(op, "f"), functions=(callee,)))
    if op == OpCode.PUSH_FUNC:
        callee = _fn("f", (Instruction(OpCode.PUSH_INT, 2), Instruction(OpCode.RETURN)))
        return OpcodeSmokeSpec(_halt(Instruction(op, "f"), functions=(callee,)))
    if op == OpCode.RETURN:
        callee = _fn("f", (Instruction(OpCode.PUSH_INT, 1), Instruction(op)))
        return OpcodeSmokeSpec(_emit_halt(Instruction(OpCode.CALL, "f"), functions=(callee,)))
    if op == OpCode.POP:
        return OpcodeSmokeSpec(_halt(Instruction(OpCode.PUSH_INT, 1), Instruction(op)))
    if op == OpCode.HALT:
        return OpcodeSmokeSpec(_halt())
    if op == OpCode.THROW:
        return OpcodeSmokeSpec(
            _halt(Instruction(OpCode.PUSH_TEXT, "err"), Instruction(op)),
            expect_error=(RuntimeSanskriptError, SanskriptError),
        )
    if op == OpCode.PANIC:
        return OpcodeSmokeSpec(
            _halt(Instruction(OpCode.PUSH_TEXT, "panic"), Instruction(op)),
            expect_error=(RuntimeSanskriptError, SanskriptError),
        )
    if op == OpCode.TRY_BEGIN:
        return OpcodeSmokeSpec(
            BytecodeProgram(
                (
                    Instruction(op, 4),
                    Instruction(OpCode.PUSH_INT, 1),
                    Instruction(OpCode.EMIT),
                    Instruction(OpCode.TRY_END),
                    Instruction(OpCode.HALT),
                ),
            ),
        )
    if op == OpCode.TRY_END:
        return OpcodeSmokeSpec(
            BytecodeProgram(
                (
                    Instruction(OpCode.TRY_BEGIN, 4),
                    Instruction(OpCode.PUSH_INT, 1),
                    Instruction(OpCode.EMIT),
                    Instruction(op),
                    Instruction(OpCode.HALT),
                ),
            ),
        )
    # Heap / pointer / unsafe — arakshita tier
    if op == OpCode.UNSAFE_ENTER:
        return OpcodeSmokeSpec(_halt(Instruction(op), Instruction(OpCode.UNSAFE_EXIT), safety_tier="rakshita"))
    if op == OpCode.UNSAFE_EXIT:
        return OpcodeSmokeSpec(
            _halt(Instruction(OpCode.UNSAFE_ENTER), Instruction(op), safety_tier="rakshita"),
        )
    if op == OpCode.HEAP_ALLOC:
        return OpcodeSmokeSpec(
            _emit_halt(Instruction(OpCode.PUSH_INT, 1), Instruction(op), safety_tier="arakshita"),
        )
    if op == OpCode.HEAP_STORE:
        return OpcodeSmokeSpec(
            _pop_halt(
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.PUSH_INT, 7),
                Instruction(op),
                safety_tier="arakshita",
            ),
            validate_only=True,
        )
    if op == OpCode.HEAP_LOAD:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.STORE_NAME, "a"),
                Instruction(OpCode.LOAD_NAME, "a"),
                Instruction(OpCode.PUSH_INT, 7),
                Instruction(OpCode.HEAP_STORE),
                Instruction(OpCode.LOAD_NAME, "a"),
                Instruction(op),
                safety_tier="arakshita",
            ),
        )
    if op == OpCode.HEAP_FREE:
        return OpcodeSmokeSpec(
            _halt(
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(op),
                safety_tier="arakshita",
            ),
        )
    if op == OpCode.PTR_FROM_INT:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(op),
                safety_tier="arakshita",
            ),
        )
    if op == OpCode.PTR_TO_INT:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.PTR_FROM_INT),
                Instruction(op),
                safety_tier="arakshita",
            ),
        )
    if op in {OpCode.PTR_ADD, OpCode.PTR_SUB}:
        return OpcodeSmokeSpec(
            _emit_halt(
                Instruction(OpCode.PUSH_INT, 2),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(op),
                safety_tier="arakshita",
            ),
        )
    if op in {
        OpCode.LOAD_U8,
        OpCode.LOAD_U16_LE,
        OpCode.LOAD_U16_BE,
        OpCode.LOAD_U32_LE,
        OpCode.LOAD_U32_BE,
        OpCode.VOLATILE_LOAD_U32_LE,
    }:
        return OpcodeSmokeSpec(
            _pop_halt(
                Instruction(OpCode.PUSH_INT, 4),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(op),
                safety_tier="arakshita",
            ),
            validate_only=True,
        )
    if op in {
        OpCode.STORE_U8,
        OpCode.STORE_U16_LE,
        OpCode.STORE_U16_BE,
        OpCode.STORE_U32_LE,
        OpCode.STORE_U32_BE,
        OpCode.VOLATILE_STORE_U32_LE,
    }:
        return OpcodeSmokeSpec(
            _pop_halt(
                Instruction(OpCode.PUSH_INT, 4),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(op),
                safety_tier="arakshita",
            ),
            validate_only=True,
        )

    raise KeyError(f"No smoke fixture for opcode {opcode!r}")


def _opcode_present(spec: OpcodeSmokeSpec, opcode: OpCode) -> bool:
    stream = list(spec.program.instructions)
    for fn in spec.program.functions:
        stream.extend(fn.instructions)
    return any(inst.opcode == opcode for inst in stream)


def run_opcode_smoke(opcode: OpCode) -> None:
    """Execute dedicated smoke for one opcode; raises on unexpected failure."""
    spec = build_opcode_smoke_spec(opcode)
    if not _opcode_present(spec, opcode):
        raise AssertionError(f"smoke program missing opcode {opcode.value}")
    try:
        validate_bytecode(spec.program)
    except BytecodeValidationError:
        if spec.validate_only:
            return
        raise
    if spec.validate_only:
        return
    vm = SanskriptVM()
    if spec.expect_error:
        try:
            vm.execute(spec.program)
        except spec.expect_error:
            return
        raise AssertionError(f"expected {spec.expect_error} for {opcode.value}")
    vm.execute(spec.program)
