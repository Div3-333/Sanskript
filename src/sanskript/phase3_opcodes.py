"""Phase 3 opcode names and bytecode metadata registration."""

from __future__ import annotations

from .fixed_width import FIXED_WIDTH_SPECS, iter_fixed_opcode_names, register_fixed_width_opcodes

# Collection / numeric opcodes beyond fixed-width table
PHASE3_COLLECTION_OPCODES: tuple[str, ...] = (
    "push_rational",
    "rational_add",
    "push_decimal",
    "decimal_add",
    "push_complex",
    "complex_add",
    "push_scalar",
    "text_scalar_at",
    "frozen_set_new",
    "frozen_set_add",
    "frozen_set_len",
    "ordered_map_new",
    "ordered_map_set",
    "ordered_map_get",
    "default_map_new",
    "default_map_set",
    "default_map_get",
    "counter_new",
    "counter_add",
    "counter_get",
    "queue_new",
    "queue_enqueue",
    "queue_dequeue",
    "stack_new",
    "stack_push",
    "stack_pop",
    "heap_new",
    "heap_push",
    "heap_pop",
    "pq_new",
    "pq_push",
    "pq_pop",
    "tree_new",
    "tree_insert",
    "tree_contains",
    "graph_new",
    "graph_add_edge",
    "graph_has_edge",
    "enum_new",
    "tagged_union_new",
    "tagged_union_tag",
    "tagged_union_payload",
    "typed_error_new",
    "named_tuple_new",
    "named_tuple_get",
    "handle_new",
)

_OPERAND_KIND_PHASE3: dict[str, str | None] = {
    "push_rational": None,
    "rational_add": None,
    "push_decimal": "text",
    "decimal_add": None,
    "push_complex": None,
    "complex_add": None,
    "push_scalar": "int",
    "text_scalar_at": None,
    "frozen_set_new": None,
    "frozen_set_add": None,
    "frozen_set_len": None,
    "ordered_map_new": None,
    "ordered_map_set": None,
    "ordered_map_get": None,
    "default_map_new": None,
    "default_map_set": None,
    "default_map_get": None,
    "counter_new": None,
    "counter_add": None,
    "counter_get": None,
    "queue_new": None,
    "queue_enqueue": None,
    "queue_dequeue": None,
    "stack_new": None,
    "stack_push": None,
    "stack_pop": None,
    "heap_new": None,
    "heap_push": None,
    "heap_pop": None,
    "pq_new": None,
    "pq_push": None,
    "pq_pop": None,
    "tree_new": None,
    "tree_insert": None,
    "tree_contains": None,
    "graph_new": None,
    "graph_add_edge": None,
    "graph_has_edge": None,
    "enum_new": "name",
    "tagged_union_new": "name",
    "tagged_union_tag": None,
    "tagged_union_payload": None,
    "typed_error_new": "name",
    "named_tuple_new": "int",
    "named_tuple_get": "name",
    "handle_new": "name",
}

_STACK_EFFECT_PHASE3: dict[str, tuple[int, int]] = {
    "push_rational": (2, 1),
    "rational_add": (2, 1),
    "push_decimal": (0, 1),
    "decimal_add": (2, 1),
    "push_complex": (2, 1),
    "complex_add": (2, 1),
    "push_scalar": (0, 1),
    "text_scalar_at": (2, 1),
    "frozen_set_new": (0, 1),
    "frozen_set_add": (2, 1),
    "frozen_set_len": (1, 1),
    "ordered_map_new": (0, 1),
    "ordered_map_set": (3, 1),
    "ordered_map_get": (2, 1),
    "default_map_new": (1, 1),
    "default_map_set": (3, 1),
    "default_map_get": (2, 1),
    "counter_new": (0, 1),
    "counter_add": (2, 1),
    "counter_get": (2, 1),
    "queue_new": (0, 1),
    "queue_enqueue": (2, 1),
    "queue_dequeue": (1, 1),
    "stack_new": (0, 1),
    "stack_push": (2, 1),
    "stack_pop": (1, 1),
    "heap_new": (0, 1),
    "heap_push": (2, 1),
    "heap_pop": (1, 1),
    "pq_new": (0, 1),
    "pq_push": (3, 1),
    "pq_pop": (1, 1),
    "tree_new": (0, 1),
    "tree_insert": (2, 1),
    "tree_contains": (2, 1),
    "graph_new": (0, 1),
    "graph_add_edge": (3, 1),
    "graph_has_edge": (3, 1),
    "enum_new": (2, 1),
    "tagged_union_new": (1, 1),
    "tagged_union_tag": (1, 1),
    "tagged_union_payload": (1, 1),
    "typed_error_new": (1, 1),
    "named_tuple_new": (0, 0),
    "named_tuple_get": (2, 1),
    "handle_new": (1, 1),
}


def all_phase3_opcode_names() -> list[str]:
    names = list(iter_fixed_opcode_names())
    names.extend(PHASE3_COLLECTION_OPCODES)
    return sorted(set(names))


def extend_opcode_enum(opcode_enum: type) -> None:
    """Add Phase 3 members to ``OpCode`` without duplicating existing names."""
    for name in all_phase3_opcode_names():
        if name in opcode_enum.__members__:
            continue
        member = str.__new__(opcode_enum, name)
        member._name_ = name
        member._value_ = name
        opcode_enum._member_map_[name] = member
        opcode_enum._value2member_map_[name] = member


def register_phase3_bytecode_metadata(
    operand_kind: dict[str, str | None],
    stack_effect: dict[str, tuple[int, int]],
) -> None:
    register_fixed_width_opcodes(operand_kind=operand_kind, stack_effect=stack_effect)
    operand_kind.update(_OPERAND_KIND_PHASE3)
    stack_effect.update(_STACK_EFFECT_PHASE3)
