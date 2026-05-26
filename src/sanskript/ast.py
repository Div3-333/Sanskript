from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Literal:
    value: int


@dataclass(frozen=True)
class FloatLiteral:
    value: float


@dataclass(frozen=True)
class BoolLiteral:
    value: bool


@dataclass(frozen=True)
class TextLiteral:
    value: str


@dataclass(frozen=True)
class Reference:
    name: str


@dataclass(frozen=True)
class CallValue:
    name: str
    module: str | None = None
    args: tuple["Value", ...] = ()


@dataclass(frozen=True)
class BinaryValue:
    operator: str
    left: "Value"
    right: "Value"


Value = Union[Literal, FloatLiteral, BoolLiteral, TextLiteral, Reference, CallValue, BinaryValue]


@dataclass(frozen=True)
class Assign:
    target: str
    value: Value


@dataclass(frozen=True)
class Increase:
    target: str
    amount: Value


@dataclass(frozen=True)
class Decrease:
    target: str
    amount: Value


@dataclass(frozen=True)
class Multiply:
    target: str
    factor: Value


@dataclass(frozen=True)
class Display:
    value: Value


@dataclass(frozen=True)
class ListInit:
    container: str


@dataclass(frozen=True)
class MapInit:
    container: str


@dataclass(frozen=True)
class ListAppend:
    container: str
    item: Value


@dataclass(frozen=True)
class ListGet:
    target: str
    container: str
    index: Value


@dataclass(frozen=True)
class ListLength:
    target: str
    container: str


@dataclass(frozen=True)
class MapPut:
    container: str
    key: Value
    value: Value


@dataclass(frozen=True)
class MapGet:
    target: str
    container: str
    key: Value


@dataclass(frozen=True)
class MapContains:
    target: str
    container: str
    key: Value


@dataclass(frozen=True)
class RecordInit:
    record: str


@dataclass(frozen=True)
class FieldSet:
    record: str
    field: Value
    value: Value


@dataclass(frozen=True)
class FieldGet:
    target: str
    record: str
    field: Value


@dataclass(frozen=True)
class FieldContains:
    target: str
    record: str
    field: Value


@dataclass(frozen=True)
class CompareEq:
    left: Value
    right: Value


@dataclass(frozen=True)
class CompareLt:
    left: Value
    right: Value


Condition = Union[CompareEq, CompareLt]


@dataclass(frozen=True)
class If:
    condition: Condition
    then_body: tuple["Statement", ...]
    else_body: tuple["Statement", ...] = ()


@dataclass(frozen=True)
class While:
    condition: Condition
    body: tuple["Statement", ...]


@dataclass(frozen=True)
class FunctionDef:
    name: str
    body: tuple["Statement", ...]
    module: str | None = None
    params: tuple[str, ...] = ()


@dataclass(frozen=True)
class Call:
    name: str
    module: str | None = None
    args: tuple[Value, ...] = ()


@dataclass(frozen=True)
class Return:
    value: Value | None = None


@dataclass(frozen=True)
class UnsafeEnter:
    pass


@dataclass(frozen=True)
class UnsafeExit:
    pass


@dataclass(frozen=True)
class HeapAlloc:
    target: str
    size: Value


@dataclass(frozen=True)
class HeapStore:
    address: Value
    value: Value


@dataclass(frozen=True)
class HeapLoad:
    target: str
    address: Value


@dataclass(frozen=True)
class HeapFree:
    address: Value


Statement = Union[
    Assign,
    Increase,
    Decrease,
    Multiply,
    Display,
    ListInit,
    MapInit,
    ListAppend,
    ListGet,
    ListLength,
    MapPut,
    MapGet,
    MapContains,
    RecordInit,
    FieldSet,
    FieldGet,
    FieldContains,
    If,
    While,
    FunctionDef,
    Call,
    Return,
    UnsafeEnter,
    UnsafeExit,
    HeapAlloc,
    HeapStore,
    HeapLoad,
    HeapFree,
]


@dataclass(frozen=True)
class Program:
    """Top-level compilation unit."""

    statements: tuple[Statement, ...]
    functions: tuple[FunctionDef, ...] = ()
    modules: tuple[tuple[str, tuple[FunctionDef, ...]], ...] = ()
    safety_tier: str = "surakshita"
