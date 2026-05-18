from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Literal:
    value: int


@dataclass(frozen=True)
class Reference:
    name: str


Value = Union[Literal, Reference]


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
class Display:
    value: Value


Statement = Union[Assign, Increase, Decrease, Display]
