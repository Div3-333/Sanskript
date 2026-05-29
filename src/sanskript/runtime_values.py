"""Runtime value model for the surakṣita tier (managed, checked collections)."""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass, field
from enum import IntEnum
from typing import TYPE_CHECKING, TypeAlias

from .fixed_width import FixedIntValue, I32_SPEC, U32_SPEC
from .phase3_values import (
    ComplexValue,
    CounterValue,
    DecimalValue,
    DefaultMapValue,
    EnumValue,
    FrozenSetValue,
    GraphValue,
    MinHeapValue,
    NamedTupleValue,
    OrderedMapValue,
    PriorityQueueValue,
    QueueValue,
    RationalValue,
    ResourceHandle,
    ScalarValue,
    StackValue,
    TaggedUnionValue,
    TreeValue,
    TypedErrorValue,
    text_grapheme_len as phase3_text_grapheme_len,
)


class RuntimeTypeId(IntEnum):
    """Stable runtime tags for Phase 3 values (VM substrate)."""

    INT = 1
    BIGINT = 2
    BOOL = 3
    FLOAT = 4
    TEXT = 5
    I32 = 6
    U32 = 7
    BYTES = 8
    BYTEARRAY = 9
    TUPLE = 10
    SET = 11
    DEQUE = 12
    OPTION = 13
    RESULT = 14
    LIST = 15
    MAP = 16
    RECORD = 17
    OPAQUE = 18
    RATIONAL = 19
    DECIMAL = 20
    COMPLEX = 21
    NIL = 22
    FIXED_INT = 23
    SCALAR = 24
    FROZEN_SET = 25
    ORDERED_MAP = 26
    DEFAULT_MAP = 27
    COUNTER = 28
    QUEUE = 29
    STACK = 30
    MIN_HEAP = 31
    PRIORITY_QUEUE = 32
    TREE = 33
    GRAPH = 34
    ENUM = 35
    TAGGED_UNION = 36
    TYPED_ERROR = 37
    NAMED_TUPLE = 38
    RESOURCE_HANDLE = 39


I32_MIN = -(2**31)
I32_MAX = 2**31 - 1
U32_MAX = 2**32 - 1


@dataclass(frozen=True)
class BigIntValue:
    """Arbitrary-precision integer (host: Python ``int``)."""

    value: int


@dataclass(frozen=True)
class I32Value:
    value: int


@dataclass(frozen=True)
class U32Value:
    value: int


@dataclass(frozen=True)
class OptionValue:
    present: bool
    value: "SanskriptValue | None" = None


@dataclass(frozen=True)
class ResultValue:
    ok: bool
    value: "SanskriptValue"


@dataclass(frozen=True)
class TupleValue:
    items: tuple["SanskriptValue", ...]


@dataclass
class SetValue:
    """Insertion-ordered unique set (equality via ``values_equal``)."""

    items: list["SanskriptValue"] = field(default_factory=list)


@dataclass
class DequeValue:
    items: deque["SanskriptValue"] = field(default_factory=deque)


@dataclass(frozen=True)
class BytesValue:
    data: bytes


@dataclass
class ByteArrayValue:
    data: bytearray


@dataclass(frozen=True)
class OpaqueHandle:
    kind: str
    handle_id: int


@dataclass
class MutableCell:
    """Shared mutable capture cell for closure variables."""

    value: "SanskriptValue"


@dataclass
class FunctionValue:
    """First-class callable, optionally carrying lexical capture."""

    target: str
    defaults: tuple["SanskriptValue", ...] = ()
    variadic_param: str | None = None
    closure: dict[str, "SanskriptValue"] = field(default_factory=dict)
    bound_args: tuple["SanskriptValue", ...] = ()
    bound_kwargs: dict[str, "SanskriptValue"] = field(default_factory=dict)


@dataclass
class RecordValue:
    """Managed named-field value; the object substrate before full classes."""

    fields: dict[str, "SanskriptValue"] = field(default_factory=dict)


class NilValue:
    """Distinct nil/absence (śūnyam), not integer zero."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "śūnyam"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NilValue)

    def __hash__(self) -> int:
        return hash("śūnyam")


NIL = NilValue()


# Host representation until values gain a dedicated heap / tag word in the VM.
SanskriptValue: TypeAlias = (
    int
    | float
    | str
    | bool
    | list["SanskriptValue"]
    | dict[str, "SanskriptValue"]
    | BigIntValue
    | I32Value
    | U32Value
    | OptionValue
    | ResultValue
    | TupleValue
    | SetValue
    | DequeValue
    | BytesValue
    | ByteArrayValue
    | OpaqueHandle
    | FunctionValue
    | FixedIntValue
    | RationalValue
    | DecimalValue
    | ComplexValue
    | ScalarValue
    | FrozenSetValue
    | OrderedMapValue
    | DefaultMapValue
    | CounterValue
    | QueueValue
    | StackValue
    | MinHeapValue
    | PriorityQueueValue
    | TreeValue
    | GraphValue
    | EnumValue
    | TaggedUnionValue
    | TypedErrorValue
    | NamedTupleValue
    | ResourceHandle
    | RecordValue
    | NilValue
)

MapKey: TypeAlias = str | int


def runtime_type_id(value: SanskriptValue) -> RuntimeTypeId:
    if isinstance(value, NilValue):
        return RuntimeTypeId.NIL
    if isinstance(value, bool):
        return RuntimeTypeId.BOOL
    if isinstance(value, BigIntValue):
        return RuntimeTypeId.BIGINT
    if isinstance(value, I32Value):
        return RuntimeTypeId.I32
    if isinstance(value, U32Value):
        return RuntimeTypeId.U32
    if isinstance(value, int):
        return RuntimeTypeId.INT
    if isinstance(value, float):
        return RuntimeTypeId.FLOAT
    if isinstance(value, str):
        return RuntimeTypeId.TEXT
    if isinstance(value, BytesValue):
        return RuntimeTypeId.BYTES
    if isinstance(value, ByteArrayValue):
        return RuntimeTypeId.BYTEARRAY
    if isinstance(value, TupleValue):
        return RuntimeTypeId.TUPLE
    if isinstance(value, SetValue):
        return RuntimeTypeId.SET
    if isinstance(value, DequeValue):
        return RuntimeTypeId.DEQUE
    if isinstance(value, OptionValue):
        return RuntimeTypeId.OPTION
    if isinstance(value, ResultValue):
        return RuntimeTypeId.RESULT
    if isinstance(value, list):
        return RuntimeTypeId.LIST
    if isinstance(value, dict):
        return RuntimeTypeId.MAP
    if isinstance(value, RecordValue):
        return RuntimeTypeId.RECORD
    if isinstance(value, OpaqueHandle):
        return RuntimeTypeId.OPAQUE
    if isinstance(value, FunctionValue):
        return RuntimeTypeId.RESOURCE_HANDLE
    if isinstance(value, FixedIntValue):
        return RuntimeTypeId.FIXED_INT
    if isinstance(value, RationalValue):
        return RuntimeTypeId.RATIONAL
    if isinstance(value, DecimalValue):
        return RuntimeTypeId.DECIMAL
    if isinstance(value, ComplexValue):
        return RuntimeTypeId.COMPLEX
    if isinstance(value, ScalarValue):
        return RuntimeTypeId.SCALAR
    if isinstance(value, FrozenSetValue):
        return RuntimeTypeId.FROZEN_SET
    if isinstance(value, OrderedMapValue):
        return RuntimeTypeId.ORDERED_MAP
    if isinstance(value, DefaultMapValue):
        return RuntimeTypeId.DEFAULT_MAP
    if isinstance(value, CounterValue):
        return RuntimeTypeId.COUNTER
    if isinstance(value, QueueValue):
        return RuntimeTypeId.QUEUE
    if isinstance(value, StackValue):
        return RuntimeTypeId.STACK
    if isinstance(value, MinHeapValue):
        return RuntimeTypeId.MIN_HEAP
    if isinstance(value, PriorityQueueValue):
        return RuntimeTypeId.PRIORITY_QUEUE
    if isinstance(value, TreeValue):
        return RuntimeTypeId.TREE
    if isinstance(value, GraphValue):
        return RuntimeTypeId.GRAPH
    if isinstance(value, EnumValue):
        return RuntimeTypeId.ENUM
    if isinstance(value, TaggedUnionValue):
        return RuntimeTypeId.TAGGED_UNION
    if isinstance(value, TypedErrorValue):
        return RuntimeTypeId.TYPED_ERROR
    if isinstance(value, NamedTupleValue):
        return RuntimeTypeId.NAMED_TUPLE
    if isinstance(value, ResourceHandle):
        return RuntimeTypeId.RESOURCE_HANDLE
    raise TypeError(f"unknown runtime value: {type(value).__name__}")


def clamp_i32(value: int) -> int:
    if value < I32_MIN:
        return I32_MIN
    if value > I32_MAX:
        return I32_MAX
    return value


def wrap_i32(value: int) -> int:
    masked = (value + 2**32) % 2**32
    return masked - 2**32 if masked >= 2**31 else masked


def wrap_u32(value: int) -> int:
    return (value + 2**32) % 2**32


def checked_i32_add(left: int, right: int) -> int:
    result = left + right
    if result < I32_MIN or result > I32_MAX:
        raise OverflowError(f"i32 overflow: {left} + {right}")
    return result


def checked_u32_add(left: int, right: int) -> int:
    result = left + right
    if result < 0 or result > U32_MAX:
        raise OverflowError(f"u32 overflow: {left} + {right}")
    return result


def is_map_key(value: SanskriptValue) -> bool:
    return isinstance(value, (str, int)) and not isinstance(value, bool)


def is_truthy(value: SanskriptValue) -> bool:
    if isinstance(value, NilValue):
        return False
    if value is False or value == 0 or value == "":
        return False
    if isinstance(value, OptionValue):
        return value.present and is_truthy(value.value) if value.value is not None else False
    if isinstance(value, ResultValue):
        return is_truthy(value.value)
    if isinstance(value, (list, dict)) and len(value) == 0:
        return False
    if isinstance(value, (BytesValue, ByteArrayValue)) and len(value.data) == 0:
        return False
    if isinstance(value, TupleValue) and len(value.items) == 0:
        return False
    if isinstance(value, SetValue) and len(value.items) == 0:
        return False
    if isinstance(value, DequeValue) and len(value.items) == 0:
        return False
    if isinstance(value, RecordValue) and len(value.fields) == 0:
        return False
    if isinstance(value, float) and (math.isnan(value) or value == 0.0):
        return False
    return True


def values_equal(left: SanskriptValue, right: SanskriptValue) -> bool:
    if isinstance(left, NilValue) or isinstance(right, NilValue):
        return isinstance(left, NilValue) and isinstance(right, NilValue)
    if type(left) is not type(right):
        if isinstance(left, int) and not isinstance(left, bool) and isinstance(right, BigIntValue):
            return left == right.value
        if isinstance(right, int) and not isinstance(right, bool) and isinstance(left, BigIntValue):
            return right == left.value
        return False
    if isinstance(left, OptionValue):
        assert isinstance(right, OptionValue)
        return left.present == right.present and (
            left.value is None and right.value is None
            or left.value is not None
            and right.value is not None
            and values_equal(left.value, right.value)
        )
    if isinstance(left, ResultValue):
        assert isinstance(right, ResultValue)
        return left.ok == right.ok and values_equal(left.value, right.value)
    if isinstance(left, TupleValue):
        assert isinstance(right, TupleValue)
        return len(left.items) == len(right.items) and all(
            values_equal(a, b) for a, b in zip(left.items, right.items)
        )
    if isinstance(left, SetValue):
        assert isinstance(right, SetValue)
        if len(left.items) != len(right.items):
            return False
        return all(any(values_equal(item, other) for other in right.items) for item in left.items)
    if isinstance(left, DequeValue):
        assert isinstance(right, DequeValue)
        return len(left.items) == len(right.items) and all(
            values_equal(a, b) for a, b in zip(left.items, right.items)
        )
    if isinstance(left, BytesValue):
        assert isinstance(right, BytesValue)
        return left.data == right.data
    if isinstance(left, ByteArrayValue):
        assert isinstance(right, ByteArrayValue)
        return left.data == right.data
    if isinstance(left, RecordValue):
        assert isinstance(right, RecordValue)
        return left.fields == right.fields
    return left == right


def values_identical(left: SanskriptValue, right: SanskriptValue) -> bool:
    """Identity comparison (sadr̥śam) — text compared as strings; otherwise ``values_equal``."""
    if isinstance(left, str) and isinstance(right, str):
        return left == right
    return values_equal(left, right)


def to_display_string(value: SanskriptValue) -> str:
    if isinstance(value, NilValue):
        return "śūnyam"
    if isinstance(value, BigIntValue):
        return f"bigint({value.value})"
    if isinstance(value, I32Value):
        return f"i32({value.value})"
    if isinstance(value, U32Value):
        return f"u32({value.value})"
    if isinstance(value, OptionValue):
        if not value.present:
            return "none"
        return f"some({to_display_string(value.value)})"
    if isinstance(value, ResultValue):
        tag = "ok" if value.ok else "err"
        return f"{tag}({to_display_string(value.value)})"
    if isinstance(value, TupleValue):
        inner = ", ".join(to_display_string(item) for item in value.items)
        return f"({inner})"
    if isinstance(value, SetValue):
        inner = ", ".join(to_display_string(item) for item in value.items)
        return "{" + inner + "}"
    if isinstance(value, DequeValue):
        inner = ", ".join(to_display_string(item) for item in value.items)
        return f"deque[{inner}]"
    if isinstance(value, BytesValue):
        return f"bytes({value.data!r})"
    if isinstance(value, ByteArrayValue):
        return f"bytearray({bytes(value.data)!r})"
    if isinstance(value, OpaqueHandle):
        return f"opaque({value.kind}:{value.handle_id})"
    if isinstance(value, FunctionValue):
        return f"callable({value.target})"
    if isinstance(value, FixedIntValue):
        return f"{value.spec.name}({value.value})"
    if isinstance(value, RationalValue):
        return f"rational({value.numerator}/{value.denominator})"
    if isinstance(value, DecimalValue):
        return f"decimal({value.value})"
    if isinstance(value, ComplexValue):
        return f"complex({value.real}, {value.imag})"
    if isinstance(value, ScalarValue):
        return f"scalar(U+{value.code_point:04X})"
    if isinstance(value, FrozenSetValue):
        inner = ", ".join(to_display_string(item) for item in value.items)
        return "frozenset{" + inner + "}"
    if isinstance(value, OrderedMapValue):
        parts = [f"{k}:{to_display_string(v)}" for k, v in value.entries.items()]
        return "ordered{" + ", ".join(parts) + "}"
    if isinstance(value, DefaultMapValue):
        parts = [f"{k}:{to_display_string(v)}" for k, v in value.entries.items()]
        return f"defaultmap({to_display_string(value.default)}, {{{', '.join(parts)}}})"
    if isinstance(value, CounterValue):
        parts = [f"{to_display_string(k)}:{v}" for k, v in value.counts.items()]
        return "counter{" + ", ".join(parts) + "}"
    if isinstance(value, QueueValue):
        inner = ", ".join(to_display_string(item) for item in value.items)
        return f"queue[{inner}]"
    if isinstance(value, StackValue):
        inner = ", ".join(to_display_string(item) for item in value.items)
        return f"stack[{inner}]"
    if isinstance(value, MinHeapValue):
        inner = ", ".join(to_display_string(item) for item in value._heap)
        return f"heap[{inner}]"
    if isinstance(value, PriorityQueueValue):
        inner = ", ".join(to_display_string(item) for _, _, item in value._heap)
        return f"pq[{inner}]"
    if isinstance(value, TreeValue):
        return "tree(...)"
    if isinstance(value, GraphValue):
        return f"graph(nodes={len(value.nodes)}, edges={len(value.edges)})"
    if isinstance(value, EnumValue):
        return f"enum({value.type_name}.{value.variant})"
    if isinstance(value, TaggedUnionValue):
        return f"union({value.tag}, {to_display_string(value.payload)})"
    if isinstance(value, TypedErrorValue):
        return f"error({value.code}: {value.message})"
    if isinstance(value, NamedTupleValue):
        parts = [
            f"{name}={to_display_string(val)}"
            for name, val in zip(value.field_names, value.items)
        ]
        return f"named({', '.join(parts)})"
    if isinstance(value, ResourceHandle):
        return f"handle({value.kind}:{value.handle_id})"
    if isinstance(value, float):
        if math.isnan(value):
            return "nan"
        if math.isinf(value):
            return "inf" if value > 0 else "-inf"
        text = format(value, "g")
        return text if "." in text else f"{text}.0"
    if isinstance(value, bool):
        return "satyam" if value else "asatyam"
    if isinstance(value, list):
        inner = ", ".join(to_display_string(item) for item in value)
        return f"[{inner}]"
    if isinstance(value, dict):
        parts = [f"{to_display_string(key)}:{to_display_string(val)}" for key, val in value.items()]
        return "{" + ", ".join(parts) + "}"
    if isinstance(value, RecordValue):
        parts = [
            f"{to_display_string(key)}:{to_display_string(val)}"
            for key, val in value.fields.items()
        ]
        return "vastu{" + ", ".join(parts) + "}"
    return str(value)


def expect_list(value: SanskriptValue) -> list[SanskriptValue]:
    if not isinstance(value, list):
        raise TypeError(f"expected list, got {type(value).__name__}")
    return value


def expect_map(value: SanskriptValue) -> dict[str, SanskriptValue]:
    if not isinstance(value, dict):
        raise TypeError(f"expected map, got {type(value).__name__}")
    return value


def expect_text(value: SanskriptValue) -> str:
    if not isinstance(value, str):
        raise TypeError(f"expected text, got {type(value).__name__}")
    return value


def expect_record(value: SanskriptValue) -> RecordValue:
    if not isinstance(value, RecordValue):
        raise TypeError(f"expected record, got {type(value).__name__}")
    return value


def expect_i32(value: SanskriptValue) -> I32Value:
    if not isinstance(value, I32Value):
        raise TypeError(f"expected i32, got {type(value).__name__}")
    return value


def expect_u32(value: SanskriptValue) -> U32Value:
    if not isinstance(value, U32Value):
        raise TypeError(f"expected u32, got {type(value).__name__}")
    return value


def expect_option(value: SanskriptValue) -> OptionValue:
    if not isinstance(value, OptionValue):
        raise TypeError(f"expected option, got {type(value).__name__}")
    return value


def expect_result(value: SanskriptValue) -> ResultValue:
    if not isinstance(value, ResultValue):
        raise TypeError(f"expected result, got {type(value).__name__}")
    return value


def expect_tuple(value: SanskriptValue) -> TupleValue:
    if not isinstance(value, TupleValue):
        raise TypeError(f"expected tuple, got {type(value).__name__}")
    return value


def expect_set(value: SanskriptValue) -> SetValue:
    if not isinstance(value, SetValue):
        raise TypeError(f"expected set, got {type(value).__name__}")
    return value


def expect_deque(value: SanskriptValue) -> DequeValue:
    if not isinstance(value, DequeValue):
        raise TypeError(f"expected deque, got {type(value).__name__}")
    return value


def expect_bytes(value: SanskriptValue) -> BytesValue:
    if not isinstance(value, BytesValue):
        raise TypeError(f"expected bytes, got {type(value).__name__}")
    return value


def expect_bytearray(value: SanskriptValue) -> ByteArrayValue:
    if not isinstance(value, ByteArrayValue):
        raise TypeError(f"expected bytearray, got {type(value).__name__}")
    return value


def set_add_unique(target: SetValue, item: SanskriptValue) -> None:
    if not any(values_equal(existing, item) for existing in target.items):
        target.items.append(item)


def map_key_from_value(value: SanskriptValue) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    raise TypeError(f"map key must be text or integer, got {value!r}")


def record_field_from_value(value: SanskriptValue) -> str:
    if isinstance(value, str) and value:
        return value
    raise TypeError(f"record field must be non-empty text, got {value!r}")


def text_grapheme_len(text: str) -> int:
    """Grapheme cluster count (Phase 3)."""
    return phase3_text_grapheme_len(text)


__all__ = [
    "NIL",
    "NilValue",
    "BigIntValue",
    "ByteArrayValue",
    "BytesValue",
    "ComplexValue",
    "CounterValue",
    "DecimalValue",
    "DefaultMapValue",
    "EnumValue",
    "FixedIntValue",
    "FrozenSetValue",
    "GraphValue",
    "MinHeapValue",
    "NamedTupleValue",
    "OrderedMapValue",
    "PriorityQueueValue",
    "QueueValue",
    "RationalValue",
    "ResourceHandle",
    "ScalarValue",
    "StackValue",
    "TaggedUnionValue",
    "TreeValue",
    "TypedErrorValue",
    "DequeValue",
    "I32_MAX",
    "I32_MIN",
    "I32Value",
    "MapKey",
    "OpaqueHandle",
    "FunctionValue",
    "OptionValue",
    "RecordValue",
    "ResultValue",
    "RuntimeTypeId",
    "SanskriptValue",
    "SetValue",
    "TupleValue",
    "U32_MAX",
    "U32Value",
    "checked_i32_add",
    "checked_u32_add",
    "clamp_i32",
    "expect_bytearray",
    "expect_bytes",
    "expect_deque",
    "expect_i32",
    "expect_list",
    "expect_map",
    "expect_option",
    "expect_record",
    "expect_result",
    "expect_set",
    "expect_text",
    "expect_tuple",
    "expect_u32",
    "is_map_key",
    "is_truthy",
    "map_key_from_value",
    "record_field_from_value",
    "runtime_type_id",
    "set_add_unique",
    "text_grapheme_len",
    "to_display_string",
    "values_equal",
    "values_identical",
    "wrap_i32",
    "wrap_u32",
]
