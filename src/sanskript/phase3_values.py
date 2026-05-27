"""Phase 3 extended runtime value types (collections, numerics, handles)."""

from __future__ import annotations

import heapq
import math
from collections import Counter, OrderedDict, deque
from dataclasses import dataclass, field
from decimal import Decimal
from fractions import Fraction
from typing import Any


@dataclass(frozen=True)
class RationalValue:
    numerator: int
    denominator: int

    def __post_init__(self) -> None:
        if self.denominator == 0:
            raise ValueError("rational denominator must not be zero")

    def as_fraction(self) -> Fraction:
        return Fraction(self.numerator, self.denominator)


@dataclass(frozen=True)
class DecimalValue:
    value: Decimal

    @staticmethod
    def from_string(text: str) -> DecimalValue:
        return DecimalValue(Decimal(text))


@dataclass(frozen=True)
class ComplexValue:
    real: float
    imag: float

    def as_complex(self) -> complex:
        return complex(self.real, self.imag)


@dataclass(frozen=True)
class ScalarValue:
    """Unicode scalar (code point)."""

    code_point: int

    def __post_init__(self) -> None:
        if self.code_point < 0 or self.code_point > 0x10FFFF:
            raise ValueError(f"invalid Unicode scalar: {self.code_point}")
        if 0xD800 <= self.code_point <= 0xDFFF:
            raise ValueError("surrogate code points are not scalars")


@dataclass(frozen=True)
class FrozenSetValue:
    items: tuple[Any, ...]


@dataclass
class OrderedMapValue:
    entries: OrderedDict[str, Any] = field(default_factory=OrderedDict)


@dataclass
class DefaultMapValue:
    entries: dict[str, Any] = field(default_factory=dict)
    default: Any = None


@dataclass
class CounterValue:
    counts: Counter[Any] = field(default_factory=Counter)


@dataclass
class QueueValue:
    items: deque[Any] = field(default_factory=deque)


@dataclass
class StackValue:
    items: list[Any] = field(default_factory=list)


@dataclass
class MinHeapValue:
    _heap: list[Any] = field(default_factory=list)

    def push(self, item: Any) -> None:
        heapq.heappush(self._heap, item)

    def pop(self) -> Any:
        return heapq.heappop(self._heap)


@dataclass
class PriorityQueueValue:
    """Max-heap via inverted comparison on (priority, item) tuples."""

    _heap: list[tuple[int, int, Any]] = field(default_factory=list)
    _seq: int = 0

    def push(self, priority: int, item: Any) -> None:
        heapq.heappush(self._heap, (-priority, self._seq, item))
        self._seq += 1

    def pop(self) -> Any:
        return heapq.heappop(self._heap)[2]


@dataclass
class TreeNode:
    key: Any
    left: TreeNode | None = None
    right: TreeNode | None = None


@dataclass
class TreeValue:
    root: TreeNode | None = None


@dataclass
class GraphValue:
    nodes: set[Any] = field(default_factory=set)
    edges: set[tuple[Any, Any]] = field(default_factory=set)


@dataclass(frozen=True)
class EnumValue:
    type_name: str
    variant: str
    payload: Any = None


@dataclass(frozen=True)
class TaggedUnionValue:
    tag: str
    payload: Any = None


@dataclass(frozen=True)
class TypedErrorValue:
    code: str
    message: str
    details: Any = None


@dataclass(frozen=True)
class ResourceHandle:
    kind: str  # file | socket | thread | process | opaque
    handle_id: int


@dataclass(frozen=True)
class NamedTupleValue:
    field_names: tuple[str, ...]
    items: tuple[Any, ...]

    def __post_init__(self) -> None:
        if len(self.field_names) != len(self.items):
            raise ValueError("named tuple field count mismatch")


def text_grapheme_len(text: str) -> int:
    """Grapheme cluster count using Unicode extended grapheme clusters (simplified)."""
    if not text:
        return 0
    count = 0
    index = 0
    length = len(text)
    while index < length:
        code = ord(text[index])
        index += 1
        if 0xD800 <= code <= 0xDBFF and index < length:
            next_code = ord(text[index])
            if 0xDC00 <= next_code <= 0xDFFF:
                index += 1
        count += 1
        while index < length:
            ch = text[index]
            cat = _grapheme_extend_category(ch)
            if cat:
                index += 1
                continue
            break
    return count


def _grapheme_extend_category(ch: str) -> bool:
    o = ord(ch)
    if 0x0300 <= o <= 0x036F:
        return True
    if 0x1AB0 <= o <= 0x1AFF:
        return True
    if 0x1DC0 <= o <= 0x1DFF:
        return True
    if 0x20D0 <= o <= 0x20FF:
        return True
    if 0xFE00 <= o <= 0xFE0F:
        return True
    if o == 0x200D:
        return True
    return False


def ieee_float_add(left: float, right: float) -> float:
    return left + right


def ieee_is_nan(value: float) -> bool:
    return math.isnan(value)


def ieee_is_inf(value: float) -> bool:
    return math.isinf(value)


__all__ = [
    "ComplexValue",
    "CounterValue",
    "DecimalValue",
    "DefaultMapValue",
    "EnumValue",
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
    "TreeNode",
    "TreeValue",
    "TypedErrorValue",
    "ieee_float_add",
    "ieee_is_inf",
    "ieee_is_nan",
    "text_grapheme_len",
]
