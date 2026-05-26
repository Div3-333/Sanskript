from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class IRLiteral:
    value: int


@dataclass(frozen=True)
class IRTextLiteral:
    value: str


@dataclass(frozen=True)
class IRReference:
    name: str


IRValue = Union[IRLiteral, IRTextLiteral, IRReference]


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
