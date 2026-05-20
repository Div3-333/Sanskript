from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Union


class OpCode(str, Enum):
    PUSH_INT = "push_int"
    LOAD_NAME = "load_name"
    STORE_NAME = "store_name"
    ADD = "add"
    SUBTRACT = "subtract"
    EMIT = "emit"
    HALT = "halt"


Operand = Union[int, str, None]


@dataclass(frozen=True)
class Instruction:
    opcode: OpCode
    operand: Operand = None


@dataclass(frozen=True)
class BytecodeProgram:
    instructions: tuple[Instruction, ...]

