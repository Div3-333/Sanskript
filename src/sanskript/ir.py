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


IRValue = Union[IRLiteral, IRFloatLiteral, IRBoolLiteral, IRTextLiteral, IRReference, IRCallValue]


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
class IRCompareEq:
    left: IRValue
    right: IRValue


@dataclass(frozen=True)
class IRIf:
    condition: IRCompareEq
    then_body: tuple["IRInstruction", ...]
    else_body: tuple["IRInstruction", ...] = ()


@dataclass(frozen=True)
class IRWhile:
    condition: IRCompareEq
    body: tuple["IRInstruction", ...]


@dataclass(frozen=True)
class IRCall:
    target: str
    args: tuple[IRValue, ...] = ()


@dataclass(frozen=True)
class IRReturn:
    value: IRValue | None = None


IRInstruction = Union[
    IRStore,
    IRIncrease,
    IRDecrease,
    IRMultiply,
    IREmit,
    IRListInit,
    IRMapInit,
    IRListAppend,
    IRMapPut,
    IRMapGet,
    IRMapContains,
    IRIf,
    IRWhile,
    IRCall,
    IRReturn,
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
