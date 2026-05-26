from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class IRLiteral:
    value: int


@dataclass(frozen=True)
class IRFloatLiteral:
    value: float


@dataclass(frozen=True)
class IRBoolLiteral:
    value: bool


@dataclass(frozen=True)
class IRTextLiteral:
    value: str


@dataclass(frozen=True)
class IRReference:
    name: str


@dataclass(frozen=True)
class IRCallValue:
    target: str
    args: tuple["IRValue", ...] = ()


@dataclass(frozen=True)
class IRBinaryValue:
    operator: str
    left: "IRValue"
    right: "IRValue"


IRValue = Union[
    IRLiteral,
    IRFloatLiteral,
    IRBoolLiteral,
    IRTextLiteral,
    IRReference,
    IRCallValue,
    IRBinaryValue,
]


@dataclass(frozen=True)
class IRStore:
    target: str
    value: IRValue


@dataclass(frozen=True)
class IRIncrease:
    target: str
    amount: IRValue


@dataclass(frozen=True)
class IRDecrease:
    target: str
    amount: IRValue


@dataclass(frozen=True)
class IRMultiply:
    target: str
    factor: IRValue


@dataclass(frozen=True)
class IREmit:
    value: IRValue


@dataclass(frozen=True)
class IRTextConcat:
    target: str
    left: IRValue
    right: IRValue


@dataclass(frozen=True)
class IRTextLength:
    target: str
    text: IRValue


@dataclass(frozen=True)
class IRTextGet:
    target: str
    text: IRValue
    index: IRValue


@dataclass(frozen=True)
class IRTextSlice:
    target: str
    text: IRValue
    start: IRValue
    end: IRValue


@dataclass(frozen=True)
class IRTextContains:
    target: str
    text: IRValue
    needle: IRValue


@dataclass(frozen=True)
class IRListInit:
    container: str


@dataclass(frozen=True)
class IRMapInit:
    container: str


@dataclass(frozen=True)
class IRListAppend:
    container: str
    item: IRValue


@dataclass(frozen=True)
class IRListGet:
    target: str
    container: str
    index: IRValue


@dataclass(frozen=True)
class IRListLength:
    target: str
    container: str


@dataclass(frozen=True)
class IRMapPut:
    container: str
    key: IRValue
    value: IRValue


@dataclass(frozen=True)
class IRMapGet:
    target: str
    container: str
    key: IRValue


@dataclass(frozen=True)
class IRMapContains:
    target: str
    container: str
    key: IRValue


@dataclass(frozen=True)
class IRRecordInit:
    record: str


@dataclass(frozen=True)
class IRFieldSet:
    record: str
    field: IRValue
    value: IRValue


@dataclass(frozen=True)
class IRFieldGet:
    target: str
    record: str
    field: IRValue


@dataclass(frozen=True)
class IRFieldContains:
    target: str
    record: str
    field: IRValue


@dataclass(frozen=True)
class IRCompareEq:
    left: IRValue
    right: IRValue


@dataclass(frozen=True)
class IRCompareLt:
    left: IRValue
    right: IRValue


@dataclass(frozen=True)
class IRIf:
    condition: IRCompareEq | IRCompareLt
    then_body: tuple["IRInstruction", ...]
    else_body: tuple["IRInstruction", ...] = ()


@dataclass(frozen=True)
class IRWhile:
    condition: IRCompareEq | IRCompareLt
    body: tuple["IRInstruction", ...]


@dataclass(frozen=True)
class IRCall:
    target: str
    args: tuple[IRValue, ...] = ()


@dataclass(frozen=True)
class IRReturn:
    value: IRValue | None = None


@dataclass(frozen=True)
class IRUnsafeEnter:
    pass


@dataclass(frozen=True)
class IRUnsafeExit:
    pass


@dataclass(frozen=True)
class IRHeapAlloc:
    target: str
    size: IRValue


@dataclass(frozen=True)
class IRHeapStore:
    address: IRValue
    value: IRValue


@dataclass(frozen=True)
class IRHeapLoad:
    target: str
    address: IRValue


@dataclass(frozen=True)
class IRHeapFree:
    address: IRValue


IRInstruction = Union[
    IRStore,
    IRIncrease,
    IRDecrease,
    IRMultiply,
    IREmit,
    IRTextConcat,
    IRTextLength,
    IRTextGet,
    IRTextSlice,
    IRTextContains,
    IRListInit,
    IRMapInit,
    IRListAppend,
    IRListGet,
    IRListLength,
    IRMapPut,
    IRMapGet,
    IRMapContains,
    IRRecordInit,
    IRFieldSet,
    IRFieldGet,
    IRFieldContains,
    IRIf,
    IRWhile,
    IRCall,
    IRReturn,
    IRUnsafeEnter,
    IRUnsafeExit,
    IRHeapAlloc,
    IRHeapStore,
    IRHeapLoad,
    IRHeapFree,
]


@dataclass(frozen=True)
class IRFunction:
    name: str
    instructions: tuple[IRInstruction, ...]
    module: str | None = None
    params: tuple[str, ...] = ()


@dataclass(frozen=True)
class IRModule:
    name: str
    functions: tuple[IRFunction, ...]


@dataclass(frozen=True)
class IRProgram:
    instructions: tuple[IRInstruction, ...]
    functions: tuple[IRFunction, ...] = ()
    modules: tuple[IRModule, ...] = ()
