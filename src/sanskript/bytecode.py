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

# Operand kinds: None, "int", "text", "name", "label"
_OPERAND_KIND: dict[str, str | None] = {
    "push_int": "int",
    "push_text": "text",
    "push_bool": "int",
    "text_concat": None,
    "text_len": None,
    "text_get": None,
    "text_slice": None,
    "text_contains": None,
    "list_new": None,
    "list_append": None,
    "list_len": None,
    "list_get": None,
    "list_map": "name",
    "list_filter": "name",
    "list_reduce": "name",
    "list_all": "name",
    "list_scan": "name",
    "list_zip": None,
    "list_enumerate": None,
    "list_any": "name",
    "list_comprehension": "name",
    "immutable_list_new": None,
    "immutable_list_append": None,
    "immutable_list_len": None,
    "immutable_list_get": None,
    "lazy_iter_new": None,
    "lazy_iter_next": None,
    "generator_new": "name",
    "generator_next": None,
    "generator_yield": None,
    "pipeline_chain": "name",
    "result_bind": "name",
    "data_query": "name",
    "rule_register": "name",
    "rule_invoke": "name",
    "memo_call": "name",
    "map_new": None,
    "map_set": None,
    "map_get": None,
    "map_contains": None,
    "record_new": None,
    "record_set": None,
    "record_get": None,
    "record_contains": None,
    "class_new": "name",
    "method_call": "name",
    "push_bigint": "int",
    "push_i32": "int",
    "push_u32": "int",
    "i32_add_checked": None,
    "u32_add_checked": None,
    "i32_add_wrapping": None,
    "u32_add_wrapping": None,
    "i32_add_saturating": None,
    "u32_add_saturating": None,
    "push_bytes": "text",
    "byte_new": None,
    "byte_len": None,
    "byte_get": None,
    "bytearray_new": None,
    "bytearray_set": None,
    "bytearray_get": None,
    "tuple_new": "int",
    "tuple_get": "int",
    "set_new": None,
    "set_add": None,
    "set_contains": None,
    "set_len": None,
    "deque_new": None,
    "deque_push_back": None,
    "deque_push_front": None,
    "deque_pop_back": None,
    "deque_pop_front": None,
    "deque_len": None,
    "option_none": None,
    "option_some": None,
    "option_is_some": None,
    "option_unwrap": None,
    "result_ok": None,
    "result_err": None,
    "result_is_ok": None,
    "result_unwrap_ok": None,
    "result_unwrap_err": None,
    "text_grapheme_len": None,
    "float_is_nan": None,
    "float_is_inf": None,
    "opaque_new": "name",
    "array_new": "int",
    "slice_view": None,
    "push_float": "float",
    "heap_alloc": None,
    "heap_store": None,
    "heap_load": None,
    "heap_free": None,
    "unsafe_enter": "optional_text",
    "unsafe_exit": None,
    "ptr_from_int": None,
    "ptr_to_int": None,
    "ptr_add": None,
    "ptr_sub": None,
    "load_u8": None,
    "load_u16_le": None,
    "load_u16_be": None,
    "load_u32_le": None,
    "load_u32_be": None,
    "store_u8": None,
    "store_u16_le": None,
    "store_u16_be": None,
    "store_u32_le": None,
    "store_u32_be": None,
    "volatile_load_u32_le": None,
    "volatile_store_u32_le": None,
    "bit_and": None,
    "bit_or": None,
    "bit_xor": None,
    "bit_not": None,
    "shift_left": None,
    "shift_right": None,
    "rotate_left32": None,
    "rotate_right32": None,
    "reg_set": "name",
    "reg_get": "name",
    "sp_set": None,
    "sp_get": None,
    "fp_set": None,
    "fp_get": None,
    "call_conv": "name",
    "prologue": None,
    "epilogue": None,
    "inline_asm": "text",
    "label": "name",
    "jump_label": "name",
    "jump_if_zero_label": "name",
    "jump_indirect": None,
    "call_indirect": None,
    "syscall": "name",
    "trap": "int",
    "mmio_read": None,
    "mmio_write": None,
    "atomic_cas_u32_le": None,
    "fence": "name",
    "load_name": "name",
    "store_name": "name",
    "add": None,
    "subtract": None,
    "multiply": None,
    "divide": None,
    "compare_eq": None,
    "compare_ne": None,
    "compare_lt": None,
    "compare_gt": None,
    "compare_le": None,
    "compare_identity": None,
    "push_nil": None,
    "scope_enter": None,
    "scope_exit": None,
    "break_loop": "name",
    "continue_loop": "name",
    "defer_push": "label",
    "defer_run": None,
    "match_eq": None,
    "match_tuple_len": "int",
    "match_record_has": "text",
    "emit": None,
    "jump": "label",
    "jump_if_zero": "label",
    "call": "name",
    "tail_call": "name",
    "push_func": "name",
    "return": None,
    "pop": None,
    "halt": None,
    "throw": None,
    "panic": None,
    "try_begin": "label",
    "try_end": None,
}

_STACK_EFFECT: dict[str, tuple[int, int]] = {
    "push_int": (0, 1),
    "push_text": (0, 1),
    "push_bool": (0, 1),
    "text_concat": (2, 1),
    "text_len": (1, 1),
    "text_get": (2, 1),
    "text_slice": (3, 1),
    "text_contains": (2, 1),
    "list_new": (0, 1),
    "list_append": (2, 1),
    "list_len": (1, 1),
    "list_get": (2, 1),
    "list_map": (1, 1),
    "list_filter": (1, 1),
    "list_reduce": (2, 1),
    "list_all": (1, 1),
    "list_scan": (3, 1),
    "list_zip": (2, 1),
    "list_enumerate": (1, 1),
    "list_any": (2, 1),
    "list_comprehension": (2, 1),
    "immutable_list_new": (0, 1),
    "immutable_list_append": (2, 1),
    "immutable_list_len": (1, 1),
    "immutable_list_get": (2, 1),
    "lazy_iter_new": (1, 1),
    "lazy_iter_next": (1, 2),
    "generator_new": (0, 1),
    "generator_next": (1, 2),
    "generator_yield": (1, 0),
    "pipeline_chain": (2, 1),
    "result_bind": (2, 1),
    "data_query": (2, 1),
    "rule_register": (0, 0),
    "rule_invoke": (1, 1),
    "memo_call": (1, 1),
    "map_new": (0, 1),
    "map_set": (3, 1),
    "map_get": (2, 1),
    "map_contains": (2, 1),
    "record_new": (0, 1),
    "record_set": (3, 1),
    "record_get": (2, 1),
    "record_contains": (2, 1),
    "class_new": (0, 1),
    "method_call": (0, 0),  # pops argc, args, receiver; pushes return dynamically
    "push_bigint": (0, 1),
    "push_i32": (0, 1),
    "push_u32": (0, 1),
    "i32_add_checked": (2, 1),
    "u32_add_checked": (2, 1),
    "i32_add_wrapping": (2, 1),
    "u32_add_wrapping": (2, 1),
    "i32_add_saturating": (2, 1),
    "u32_add_saturating": (2, 1),
    "push_bytes": (0, 1),
    "byte_new": (0, 1),
    "byte_len": (1, 1),
    "byte_get": (2, 1),
    "bytearray_new": (0, 1),
    "bytearray_set": (3, 1),
    "bytearray_get": (2, 1),
    "tuple_new": (0, 0),  # pops operand-many values in VM (dynamic)
    "tuple_get": (1, 1),
    "set_new": (0, 1),
    "set_add": (2, 1),
    "set_contains": (2, 1),
    "set_len": (1, 1),
    "deque_new": (0, 1),
    "deque_push_back": (2, 1),
    "deque_push_front": (2, 1),
    "deque_pop_back": (1, 1),
    "deque_pop_front": (1, 1),
    "deque_len": (1, 1),
    "option_none": (0, 1),
    "option_some": (1, 1),
    "option_is_some": (1, 1),
    "option_unwrap": (1, 1),
    "result_ok": (1, 1),
    "result_err": (1, 1),
    "result_is_ok": (1, 1),
    "result_unwrap_ok": (1, 1),
    "result_unwrap_err": (1, 1),
    "text_grapheme_len": (1, 1),
    "float_is_nan": (1, 1),
    "float_is_inf": (1, 1),
    "opaque_new": (1, 1),
    "array_new": (0, 1),
    "slice_view": (3, 1),
    "push_float": (0, 1),
    "heap_alloc": (1, 1),
    "heap_store": (2, 0),
    "heap_load": (1, 1),
    "heap_free": (1, 0),
    "unsafe_enter": (0, 0),
    "unsafe_exit": (0, 0),
    "ptr_from_int": (1, 1),
    "ptr_to_int": (1, 1),
    "ptr_add": (2, 1),
    "ptr_sub": (2, 1),
    "load_u8": (1, 1),
    "load_u16_le": (1, 1),
    "load_u16_be": (1, 1),
    "load_u32_le": (1, 1),
    "load_u32_be": (1, 1),
    "store_u8": (2, 0),
    "store_u16_le": (2, 0),
    "store_u16_be": (2, 0),
    "store_u32_le": (2, 0),
    "store_u32_be": (2, 0),
    "volatile_load_u32_le": (1, 1),
    "volatile_store_u32_le": (2, 0),
    "bit_and": (2, 1),
    "bit_or": (2, 1),
    "bit_xor": (2, 1),
    "bit_not": (1, 1),
    "shift_left": (2, 1),
    "shift_right": (2, 1),
    "rotate_left32": (2, 1),
    "rotate_right32": (2, 1),
    "reg_set": (1, 0),
    "reg_get": (0, 1),
    "sp_set": (1, 0),
    "sp_get": (0, 1),
    "fp_set": (1, 0),
    "fp_get": (0, 1),
    "call_conv": (0, 0),
    "prologue": (0, 0),
    "epilogue": (0, 0),
    "inline_asm": (0, 0),
    "label": (0, 0),
    "jump_label": (0, 0),
    "jump_if_zero_label": (1, 0),
    "jump_indirect": (1, 0),
    "call_indirect": (1, 0),
    "syscall": (0, 1),
    "trap": (0, 0),
    "mmio_read": (1, 1),
    "mmio_write": (2, 0),
    "atomic_cas_u32_le": (3, 1),
    "fence": (0, 0),
    "load_name": (0, 1),
    "store_name": (1, 0),
    "add": (2, 1),
    "subtract": (2, 1),
    "multiply": (2, 1),
    "divide": (2, 1),
    "compare_eq": (2, 1),
    "compare_ne": (2, 1),
    "compare_lt": (2, 1),
    "compare_gt": (2, 1),
    "compare_le": (2, 1),
    "compare_identity": (2, 1),
    "push_nil": (0, 1),
    "scope_enter": (0, 0),
    "scope_exit": (0, 0),
    "break_loop": (0, 0),
    "continue_loop": (0, 0),
    "defer_push": (0, 0),
    "defer_run": (0, 0),
    "match_eq": (2, 1),
    "match_tuple_len": (2, 1),
    "match_record_has": (2, 1),
    "emit": (1, 0),
    "jump": (0, 0),
    "jump_if_zero": (1, 0),
    "call": (0, 0),
    "tail_call": (0, 0),
    "push_func": (0, 1),
    "return": (1, 0),
    "pop": (1, 0),
    "halt": (0, 0),
    "throw": (1, 0),
    "panic": (1, 0),
    "try_begin": (0, 0),
    "try_end": (0, 0),
}

_V1_OPCODES = frozenset(
    {"push_int", "load_name", "store_name", "add", "subtract", "emit", "halt"}
)


class OpCode(str, Enum):
    PUSH_INT = "push_int"
    PUSH_TEXT = "push_text"
    PUSH_BOOL = "push_bool"
    TEXT_CONCAT = "text_concat"
    TEXT_LEN = "text_len"
    TEXT_GET = "text_get"
    TEXT_SLICE = "text_slice"
    TEXT_CONTAINS = "text_contains"
    LIST_NEW = "list_new"
    LIST_APPEND = "list_append"
    LIST_LEN = "list_len"
    LIST_GET = "list_get"
    LIST_MAP = "list_map"
    LIST_FILTER = "list_filter"
    LIST_REDUCE = "list_reduce"
    LIST_ALL = "list_all"
    LIST_SCAN = "list_scan"
    LIST_ZIP = "list_zip"
    LIST_ENUMERATE = "list_enumerate"
    LIST_ANY = "list_any"
    LIST_COMPREHENSION = "list_comprehension"
    IMMUTABLE_LIST_NEW = "immutable_list_new"
    IMMUTABLE_LIST_APPEND = "immutable_list_append"
    IMMUTABLE_LIST_LEN = "immutable_list_len"
    IMMUTABLE_LIST_GET = "immutable_list_get"
    LAZY_ITER_NEW = "lazy_iter_new"
    LAZY_ITER_NEXT = "lazy_iter_next"
    GENERATOR_NEW = "generator_new"
    GENERATOR_NEXT = "generator_next"
    GENERATOR_YIELD = "generator_yield"
    PIPELINE_CHAIN = "pipeline_chain"
    RESULT_BIND = "result_bind"
    DATA_QUERY = "data_query"
    RULE_REGISTER = "rule_register"
    RULE_INVOKE = "rule_invoke"
    MEMO_CALL = "memo_call"
    MAP_NEW = "map_new"
    MAP_SET = "map_set"
    MAP_GET = "map_get"
    MAP_CONTAINS = "map_contains"
    RECORD_NEW = "record_new"
    RECORD_SET = "record_set"
    RECORD_GET = "record_get"
    RECORD_CONTAINS = "record_contains"
    CLASS_NEW = "class_new"
    METHOD_CALL = "method_call"
    PUSH_BIGINT = "push_bigint"
    PUSH_I32 = "push_i32"
    PUSH_U32 = "push_u32"
    I32_ADD_CHECKED = "i32_add_checked"
    U32_ADD_CHECKED = "u32_add_checked"
    I32_ADD_WRAPPING = "i32_add_wrapping"
    U32_ADD_WRAPPING = "u32_add_wrapping"
    I32_ADD_SATURATING = "i32_add_saturating"
    U32_ADD_SATURATING = "u32_add_saturating"
    PUSH_BYTES = "push_bytes"
    BYTE_NEW = "byte_new"
    BYTE_LEN = "byte_len"
    BYTE_GET = "byte_get"
    BYTEARRAY_NEW = "bytearray_new"
    BYTEARRAY_SET = "bytearray_set"
    BYTEARRAY_GET = "bytearray_get"
    TUPLE_NEW = "tuple_new"
    TUPLE_GET = "tuple_get"
    SET_NEW = "set_new"
    SET_ADD = "set_add"
    SET_CONTAINS = "set_contains"
    SET_LEN = "set_len"
    DEQUE_NEW = "deque_new"
    DEQUE_PUSH_BACK = "deque_push_back"
    DEQUE_PUSH_FRONT = "deque_push_front"
    DEQUE_POP_BACK = "deque_pop_back"
    DEQUE_POP_FRONT = "deque_pop_front"
    DEQUE_LEN = "deque_len"
    OPTION_NONE = "option_none"
    OPTION_SOME = "option_some"
    OPTION_IS_SOME = "option_is_some"
    OPTION_UNWRAP = "option_unwrap"
    RESULT_OK = "result_ok"
    RESULT_ERR = "result_err"
    RESULT_IS_OK = "result_is_ok"
    RESULT_UNWRAP_OK = "result_unwrap_ok"
    RESULT_UNWRAP_ERR = "result_unwrap_err"
    TEXT_GRAPHEME_LEN = "text_grapheme_len"
    FLOAT_IS_NAN = "float_is_nan"
    FLOAT_IS_INF = "float_is_inf"
    OPAQUE_NEW = "opaque_new"
    ARRAY_NEW = "array_new"
    SLICE_VIEW = "slice_view"
    PUSH_FLOAT = "push_float"
    HEAP_ALLOC = "heap_alloc"
    HEAP_STORE = "heap_store"
    HEAP_LOAD = "heap_load"
    HEAP_FREE = "heap_free"
    UNSAFE_ENTER = "unsafe_enter"
    UNSAFE_EXIT = "unsafe_exit"
    PTR_FROM_INT = "ptr_from_int"
    PTR_TO_INT = "ptr_to_int"
    PTR_ADD = "ptr_add"
    PTR_SUB = "ptr_sub"
    LOAD_U8 = "load_u8"
    LOAD_U16_LE = "load_u16_le"
    LOAD_U16_BE = "load_u16_be"
    LOAD_U32_LE = "load_u32_le"
    LOAD_U32_BE = "load_u32_be"
    STORE_U8 = "store_u8"
    STORE_U16_LE = "store_u16_le"
    STORE_U16_BE = "store_u16_be"
    STORE_U32_LE = "store_u32_le"
    STORE_U32_BE = "store_u32_be"
    VOLATILE_LOAD_U32_LE = "volatile_load_u32_le"
    VOLATILE_STORE_U32_LE = "volatile_store_u32_le"
    BIT_AND = "bit_and"
    BIT_OR = "bit_or"
    BIT_XOR = "bit_xor"
    BIT_NOT = "bit_not"
    SHIFT_LEFT = "shift_left"
    SHIFT_RIGHT = "shift_right"
    ROTATE_LEFT32 = "rotate_left32"
    ROTATE_RIGHT32 = "rotate_right32"
    REG_SET = "reg_set"
    REG_GET = "reg_get"
    SP_SET = "sp_set"
    SP_GET = "sp_get"
    FP_SET = "fp_set"
    FP_GET = "fp_get"
    CALL_CONV = "call_conv"
    PROLOGUE = "prologue"
    EPILOGUE = "epilogue"
    INLINE_ASM = "inline_asm"
    LABEL = "label"
    JUMP_LABEL = "jump_label"
    JUMP_IF_ZERO_LABEL = "jump_if_zero_label"
    JUMP_INDIRECT = "jump_indirect"
    CALL_INDIRECT = "call_indirect"
    SYSCALL = "syscall"
    TRAP = "trap"
    MMIO_READ = "mmio_read"
    MMIO_WRITE = "mmio_write"
    ATOMIC_CAS_U32_LE = "atomic_cas_u32_le"
    FENCE = "fence"
    LOAD_NAME = "load_name"
    STORE_NAME = "store_name"
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    COMPARE_EQ = "compare_eq"
    COMPARE_NE = "compare_ne"
    COMPARE_LT = "compare_lt"
    COMPARE_GT = "compare_gt"
    COMPARE_LE = "compare_le"
    COMPARE_IDENTITY = "compare_identity"
    PUSH_NIL = "push_nil"
    SCOPE_ENTER = "scope_enter"
    SCOPE_EXIT = "scope_exit"
    BREAK_LOOP = "break_loop"
    CONTINUE_LOOP = "continue_loop"
    DEFER_PUSH = "defer_push"
    DEFER_RUN = "defer_run"
    MATCH_EQ = "match_eq"
    MATCH_TUPLE_LEN = "match_tuple_len"
    MATCH_RECORD_HAS = "match_record_has"
    EMIT = "emit"
    JUMP = "jump"
    JUMP_IF_ZERO = "jump_if_zero"
    CALL = "call"
    TAIL_CALL = "tail_call"
    PUSH_FUNC = "push_func"
    RETURN = "return"
    POP = "pop"
    HALT = "halt"
    THROW = "throw"
    PANIC = "panic"
    TRY_BEGIN = "try_begin"
    TRY_END = "try_end"


from .phase3_opcodes import extend_opcode_enum, register_phase3_bytecode_metadata
from .phase8_opcodes import extend_opcode_enum as extend_phase8_opcode_enum
from .phase8_opcodes import register_phase8_bytecode_metadata

extend_opcode_enum(OpCode)
register_phase3_bytecode_metadata(_OPERAND_KIND, _STACK_EFFECT)
extend_phase8_opcode_enum(OpCode)
register_phase8_bytecode_metadata(_OPERAND_KIND, _STACK_EFFECT)

# Backward-compatible alias
BYTECODE_VERSION = BYTECODE_LATEST

_OPERAND_BY_OPCODE = dict(_OPERAND_KIND)


class BytecodeValidationError(SanskriptError):
    code = "SANSKRIPT_BYTECODE"


Operand = Union[int, float, str, None]


@dataclass(frozen=True)
class Instruction:
    opcode: OpCode
    operand: Operand = None


@dataclass(frozen=True)
class FunctionBytecode:
    name: str
    instructions: tuple[Instruction, ...]
    params: tuple[str, ...] = ()
    defaults: tuple[Operand, ...] = ()
    variadic_param: str | None = None
    capture_mut: frozenset[str] = frozenset()
    effect: str | None = None
    is_generator: bool = False
    is_memoized: bool = False
    is_inline: bool = False
    is_naked: bool = False
    abi_name: str | None = None
    named_returns: tuple[str, ...] = ()


@dataclass(frozen=True)
class ModuleBytecode:
    name: str
    functions: tuple[FunctionBytecode, ...]


@dataclass(frozen=True)
class BytecodeProgram:
    instructions: tuple[Instruction, ...]
    functions: tuple[FunctionBytecode, ...] = ()
    modules: tuple[ModuleBytecode, ...] = ()
    safety_tier: str = "surakshita"
    defer_blocks: tuple[tuple[Instruction, ...], ...] = ()


def instruction_to_dict(instruction: Instruction) -> dict[str, Any]:
    payload: dict[str, Any] = {"op": instruction.opcode.value}
    if instruction.operand is not None:
        payload["operand"] = instruction.operand
    return payload


def instruction_from_dict(raw: dict[str, Any], *, allowed: frozenset[str] | None = None) -> Instruction:
    if not isinstance(raw, dict):
        raise BytecodeValidationError("instruction entry must be an object")
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

    if kind == "optional_text":
        if "operand" not in raw:
            return Instruction(opcode)
        if operand is not None and not isinstance(operand, str):
            raise BytecodeValidationError(f"{opcode.value} optional operand must be a string")
        return Instruction(opcode, operand)

    if operand is None:
        raise BytecodeValidationError(f"{opcode.value} requires an operand")

    if kind in {"int", "label"}:
        if not isinstance(operand, int) or isinstance(operand, bool):
            raise BytecodeValidationError(
                f"{opcode.value} operand must be an integer, got {operand!r}"
            )
        return Instruction(opcode, operand)

    if kind == "float":
        if not isinstance(operand, (int, float)) or isinstance(operand, bool):
            raise BytecodeValidationError(f"{opcode.value} operand must be a number, got {operand!r}")
        return Instruction(opcode, float(operand))

    if kind == "text":
        if not isinstance(operand, str):
            raise BytecodeValidationError(f"{opcode.value} operand must be a string")
        return Instruction(opcode, operand)

    if kind == "name":
        if not isinstance(operand, str) or not operand:
            raise BytecodeValidationError(
                f"{opcode.value} operand must be a non-empty string name"
            )
        return Instruction(opcode, operand)

    raise BytecodeValidationError(f"Internal operand kind {kind!r}")


def _function_to_dict(function: FunctionBytecode) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "name": function.name,
        "instructions": [instruction_to_dict(item) for item in function.instructions],
    }
    if function.params:
        payload["params"] = list(function.params)
    if function.defaults:
        payload["defaults"] = list(function.defaults)
    if function.variadic_param:
        payload["variadic_param"] = function.variadic_param
    if function.capture_mut:
        payload["capture_mut"] = sorted(function.capture_mut)
    if function.effect:
        payload["effect"] = function.effect
    if function.is_memoized:
        payload["memoized"] = True
    if function.is_generator:
        payload["generator"] = True
    if function.is_inline:
        payload["inline"] = True
    if function.is_naked:
        payload["naked"] = True
    if function.abi_name:
        payload["abi_name"] = function.abi_name
    if function.named_returns:
        payload["named_returns"] = list(function.named_returns)
    return payload


def _function_from_dict(raw: dict[str, Any], *, version: int) -> FunctionBytecode:
    allowed = _V1_OPCODES if version == BYTECODE_VERSION_1 else None
    name = str(raw.get("name", ""))
    if not name:
        raise BytecodeValidationError("function name is required")
    params = _params_from_raw(raw.get("params", []), owner=f"function {name!r}")
    defaults_raw = raw.get("defaults", [])
    if not isinstance(defaults_raw, list):
        raise BytecodeValidationError(f"function {name!r} defaults must be a list")
    defaults = tuple(defaults_raw)
    variadic_param = raw.get("variadic_param")
    if variadic_param is not None and (not isinstance(variadic_param, str) or not variadic_param):
        raise BytecodeValidationError(f"function {name!r} variadic_param must be non-empty string")
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
    capture_mut_raw = raw.get("capture_mut", [])
    if not isinstance(capture_mut_raw, list):
        raise BytecodeValidationError(f"function {name!r} capture_mut must be a list")
    capture_mut: frozenset[str] = frozenset()
    if capture_mut_raw:
        if any(not isinstance(item, str) or not item for item in capture_mut_raw):
            raise BytecodeValidationError(
                f"function {name!r} capture_mut entries must be non-empty strings"
            )
        capture_mut = frozenset(capture_mut_raw)
    effect = raw.get("effect")
    is_inline = bool(raw.get("inline", False))
    is_naked = bool(raw.get("naked", False))
    is_memoized = bool(raw.get("memoized", False))
    is_generator = bool(raw.get("generator", False))
    abi_name = raw.get("abi_name")
    named_returns_raw = raw.get("named_returns", [])
    if not isinstance(named_returns_raw, list):
        raise BytecodeValidationError(f"function {name!r} named_returns must be a list")
    if any(not isinstance(item, str) or not item for item in named_returns_raw):
        raise BytecodeValidationError(
            f"function {name!r} named_returns entries must be non-empty strings"
        )
    named_returns = tuple(named_returns_raw)
    return FunctionBytecode(
        name,
        instructions,
        params=params,
        defaults=defaults,
        variadic_param=variadic_param,
        capture_mut=capture_mut,
        effect=str(effect) if effect else None,
        is_generator=is_generator,
        is_memoized=is_memoized,
        is_inline=is_inline,
        is_naked=is_naked,
        abi_name=str(abi_name) if abi_name else None,
        named_returns=named_returns,
    )


def _params_from_raw(raw: object, *, owner: str) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise BytecodeValidationError(f"{owner} params must be a list")
    params: list[str] = []
    seen: set[str] = set()
    for item in raw:
        if not isinstance(item, str) or not item:
            raise BytecodeValidationError(f"{owner} params must be non-empty string names")
        if item in seen:
            raise BytecodeValidationError(f"{owner} has duplicate param {item!r}")
        params.append(item)
        seen.add(item)
    return tuple(params)


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
    if version >= BYTECODE_VERSION_2 and program.safety_tier != "surakshita":
        payload["safety_tier"] = program.safety_tier
    return payload


def decode_program(payload: dict[str, Any]) -> BytecodeProgram:
    if not isinstance(payload, dict):
        raise BytecodeValidationError("program payload must be an object")
    version = payload.get("version")
    if version not in {BYTECODE_VERSION_1, BYTECODE_VERSION_2}:
        raise BytecodeValidationError(
            f"Unsupported bytecode version: {version!r} "
            f"(expected {BYTECODE_VERSION_1} or {BYTECODE_VERSION_2})"
        )
    if version == BYTECODE_VERSION_1:
        for field in ("functions", "modules", "safety_tier"):
            if field in payload:
                raise BytecodeValidationError(f"bytecode v1 does not permit field {field!r}")
    allowed = _V1_OPCODES if version == BYTECODE_VERSION_1 else None
    raw_instructions = payload.get("instructions")
    if not isinstance(raw_instructions, list) or not raw_instructions:
        raise BytecodeValidationError("instructions must be a non-empty list")
    instructions = tuple(instruction_from_dict(item, allowed=allowed) for item in raw_instructions)

    functions: list[FunctionBytecode] = []
    raw_functions = payload.get("functions", [])
    if not isinstance(raw_functions, list):
        raise BytecodeValidationError("functions must be a list")
    for raw_fn in raw_functions:
        if not isinstance(raw_fn, dict):
            raise BytecodeValidationError("function entries must be objects")
        functions.append(_function_from_dict(raw_fn, version=version))

    modules: list[ModuleBytecode] = []
    raw_modules = payload.get("modules", [])
    if not isinstance(raw_modules, list):
        raise BytecodeValidationError("modules must be a list")
    for raw_mod in raw_modules:
        if not isinstance(raw_mod, dict):
            raise BytecodeValidationError("module entries must be objects")
        mod_name = str(raw_mod.get("name", ""))
        if not mod_name:
            raise BytecodeValidationError("module name is required")
        mod_fns_raw = raw_mod.get("functions", [])
        if not isinstance(mod_fns_raw, list):
            raise BytecodeValidationError(f"module {mod_name!r} functions must be a list")
        for item in mod_fns_raw:
            if not isinstance(item, dict):
                raise BytecodeValidationError(
                    f"module {mod_name!r} function entries must be objects"
                )
        mod_fns = tuple(_function_from_dict(item, version=version) for item in mod_fns_raw)
        modules.append(ModuleBytecode(mod_name, mod_fns))

    tier = str(payload.get("safety_tier", "surakshita"))
    if tier not in {"surakshita", "rakshita", "arakshita"}:
        raise BytecodeValidationError(f"Unknown safety_tier: {tier!r}")
    program = BytecodeProgram(tuple(instructions), tuple(functions), tuple(modules), safety_tier=tier)
    validate_bytecode(program, version=version)
    return program


def load_bytecode_file(path: Path | str) -> BytecodeProgram:
    raw = Path(path).read_text(encoding="utf-8").strip()
    if not raw:
        raise BytecodeValidationError(f"Bytecode file is empty: {path}")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise BytecodeValidationError("Bytecode file must contain a JSON object")
    return decode_program(data)


def dump_bytecode_file(program: BytecodeProgram, path: Path | str, *, version: int = BYTECODE_LATEST) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(encode_program(program, version=version), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _has_control_flow(program: BytecodeProgram) -> bool:
    control = {
        OpCode.JUMP,
        OpCode.JUMP_IF_ZERO,
        OpCode.CALL,
        OpCode.TAIL_CALL,
        OpCode.METHOD_CALL,
        OpCode.RETURN,
    }
    streams = (
        program.instructions,
        *(function.instructions for function in program.functions),
        *(function.instructions for module in program.modules for function in module.functions),
    )
    for stream in streams:
        if any(inst.opcode in control for inst in stream):
            return True
    return False


def validate_bytecode(program: BytecodeProgram, *, version: int = BYTECODE_LATEST) -> None:
    if not program.instructions:
        raise BytecodeValidationError("Program must contain at least one instruction")
    if program.safety_tier not in {"surakshita", "rakshita", "arakshita"}:
        raise BytecodeValidationError(f"Unknown safety_tier: {program.safety_tier!r}")

    _validate_instruction_stream(
        program.instructions,
        version=version,
        strict_stack=not _has_control_flow(program),
        require_halt=True,
    )

    for function in program.functions:
        _validate_function_signature(function)
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
            _validate_function_signature(function)
            _validate_instruction_stream(
                function.instructions,
                version=version,
                strict_stack=False,
                require_halt=False,
            )


def _validate_function_signature(function: FunctionBytecode) -> None:
    seen: set[str] = set()
    for param in function.params:
        if not isinstance(param, str) or not param:
            raise BytecodeValidationError(f"function {function.name!r} has invalid param {param!r}")
        if param in seen:
            raise BytecodeValidationError(f"function {function.name!r} has duplicate param {param!r}")
        seen.add(param)
    if function.defaults and len(function.defaults) != len(function.params):
        raise BytecodeValidationError(
            f"function {function.name!r} defaults length must match params length"
        )
    if function.variadic_param and function.variadic_param in seen:
        raise BytecodeValidationError(
            f"function {function.name!r} variadic param duplicates regular param"
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
        if kind == "float" and (
            not isinstance(instruction.operand, (int, float)) or isinstance(instruction.operand, bool)
        ):
            raise BytecodeValidationError(
                f"Instruction {index} ({opcode}) requires a numeric operand"
            )
        if kind == "text" and not isinstance(instruction.operand, str):
            raise BytecodeValidationError(
                f"Instruction {index} ({opcode}) requires a string operand"
            )
        if kind == "optional_text" and instruction.operand is not None and not isinstance(
            instruction.operand, str
        ):
            raise BytecodeValidationError(
                f"Instruction {index} ({opcode}) optional operand must be a string"
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
        if opcode == OpCode.TUPLE_NEW.value:
            arity = instruction.operand
            if not isinstance(arity, int) or arity < 0:
                raise BytecodeValidationError(
                    f"Instruction {index} ({opcode}) requires a non-negative arity operand"
                )
            pop_count, push_count = arity, 1
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


def resolve_call_target(program: BytecodeProgram, target: str) -> FunctionBytecode:
    if "." in target:
        module_name, fn_name = target.split(".", 1)
        for module in program.modules:
            if module.name == module_name:
                for function in module.functions:
                    if function.name in {fn_name, target}:
                        return function
        raise BytecodeValidationError(f"Unknown module function {target!r}")

    for function in program.functions:
        if function.name == target:
            return function
    raise BytecodeValidationError(f"Unknown function {target!r}")


def resolve_method_target(
    program: BytecodeProgram,
    class_name: str,
    method_name: str,
    *,
    argc: int,
    mro: tuple[str, ...] | None = None,
) -> FunctionBytecode:
    """Resolve instance method to a function symbol (supports overload suffixes)."""

    order = mro if mro else (class_name,)
    tried_symbols: list[str] = []

    def _symbol(cls: str) -> str:
        return f"{cls}{method_name}" if method_name.startswith("__") else f"{cls}__{method_name}"

    expected_arity = 1 + argc
    for cls in order:
        base = _symbol(cls)
        tried_symbols.append(base)
        exact = [fn for fn in program.functions if fn.name == base]
        if len(exact) == 1:
            if len(exact[0].params) == expected_arity:
                return exact[0]
        elif exact:
            for fn in exact:
                if len(fn.params) == expected_arity:
                    return fn
            return exact[0]
        prefixed = sorted(
            fn for fn in program.functions if fn.name.startswith(f"{base}_")
        )
        tried_symbols.extend(fn.name for fn in prefixed)
        for fn in prefixed:
            if len(fn.params) == expected_arity:
                return fn
        if len(prefixed) == 1:
            return prefixed[0]
    raise BytecodeValidationError(
        f"Unknown method {method_name!r} on class {class_name!r} "
        f"(mro={order}, argc={argc}, expected_arity={expected_arity}, tried={tried_symbols})",
    )


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
