"""Phase 8 functional/declarative bytecode opcodes and metadata."""

from __future__ import annotations

PHASE8_OPCODE_NAMES: tuple[str, ...] = (
    "immutable_list_new",
    "immutable_list_append",
    "immutable_list_len",
    "immutable_list_get",
    "list_scan",
    "list_zip",
    "list_enumerate",
    "list_any",
    "list_comprehension",
    "lazy_iter_new",
    "lazy_iter_next",
    "generator_new",
    "generator_next",
    "generator_yield",
    "pipeline_chain",
    "match_expr",
    "result_bind",
    "data_query",
    "rule_register",
    "rule_invoke",
    "memo_call",
)

_OPERAND_KIND_PHASE8: dict[str, str | None] = {
    "immutable_list_new": None,
    "immutable_list_append": None,
    "immutable_list_len": None,
    "immutable_list_get": None,
    "list_scan": "name",
    "list_zip": None,
    "list_enumerate": None,
    "list_any": "name",
    "list_comprehension": "name",
    "lazy_iter_new": None,
    "lazy_iter_next": None,
    "generator_new": "name",
    "generator_next": None,
    "generator_yield": None,
    "pipeline_chain": "name",
    "match_expr": None,
    "result_bind": "name",
    "data_query": "name",
    "rule_register": "name",
    "rule_invoke": "name",
    "memo_call": "name",
}

_STACK_EFFECT_PHASE8: dict[str, tuple[int, int]] = {
    "immutable_list_new": (0, 1),
    "immutable_list_append": (2, 1),
    "immutable_list_len": (1, 1),
    "immutable_list_get": (2, 1),
    "list_scan": (3, 1),
    "list_zip": (2, 1),
    "list_enumerate": (1, 1),
    "list_any": (2, 1),
    "list_comprehension": (2, 1),
    "lazy_iter_new": (1, 1),
    "lazy_iter_next": (1, 1),
    "generator_new": (0, 1),
    "generator_next": (1, 1),
    "generator_yield": (1, 0),
    "pipeline_chain": (2, 1),
    "match_expr": (0, 0),
    "result_bind": (2, 1),
    "data_query": (2, 1),
    "rule_register": (2, 0),
    "rule_invoke": (1, 1),
    "memo_call": (1, 1),
}


def extend_opcode_enum(opcode_enum: type) -> None:
    for name in PHASE8_OPCODE_NAMES:
        if name in opcode_enum.__members__:
            continue
        member = str.__new__(opcode_enum, name)
        member._name_ = name
        member._value_ = name
        opcode_enum._member_map_[name] = member
        opcode_enum._value2member_map_[name] = member


def register_phase8_bytecode_metadata(
    operand_kind: dict[str, str | None],
    stack_effect: dict[str, tuple[int, int]],
) -> None:
    operand_kind.update(_OPERAND_KIND_PHASE8)
    stack_effect.update(_STACK_EFFECT_PHASE8)


def all_phase8_opcode_names() -> tuple[str, ...]:
    return PHASE8_OPCODE_NAMES
