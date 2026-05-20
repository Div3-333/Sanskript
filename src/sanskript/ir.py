from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class IRLiteral:
    value: int


@dataclass(frozen=True)
class IRReference:
    name: str


IRValue = Union[IRLiteral, IRReference]


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
class IREmit:
    value: IRValue


IRInstruction = Union[IRStore, IRIncrease, IRDecrease, IREmit]


@dataclass(frozen=True)
class IRProgram:
    instructions: tuple[IRInstruction, ...]
