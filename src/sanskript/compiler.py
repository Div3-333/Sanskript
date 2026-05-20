from __future__ import annotations

from .ast import Assign, Decrease, Display, Increase, Literal, Reference, Statement, Value
from .bytecode import BytecodeProgram, Instruction, OpCode
from .errors import RuntimeSanskriptError
from .ir import (
    IRDecrease,
    IREmit,
    IRIncrease,
    IRInstruction,
    IRLiteral,
    IRProgram,
    IRReference,
    IRStore,
    IRValue,
)
from .parser import parse_program


def compile_source(source: str) -> BytecodeProgram:
    return lower_ir_to_bytecode(compile_statements_to_ir(parse_program(source)))


def compile_statements(statements: list[Statement]) -> BytecodeProgram:
    return lower_ir_to_bytecode(compile_statements_to_ir(statements))


def compile_statements_to_ir(statements: list[Statement]) -> IRProgram:
    return IRProgram(tuple(_compile_statement_to_ir(statement) for statement in statements))


def lower_ir_to_bytecode(program: IRProgram) -> BytecodeProgram:
    instructions: list[Instruction] = []
    for instruction in program.instructions:
        instructions.extend(_lower_instruction(instruction))
    instructions.append(Instruction(OpCode.HALT))
    return BytecodeProgram(tuple(instructions))


def _compile_statement_to_ir(statement: Statement) -> IRInstruction:
    if isinstance(statement, Assign):
        return IRStore(statement.target, _compile_value_to_ir(statement.value))
    if isinstance(statement, Increase):
        return IRIncrease(statement.target, _compile_value_to_ir(statement.amount))
    if isinstance(statement, Decrease):
        return IRDecrease(statement.target, _compile_value_to_ir(statement.amount))
    if isinstance(statement, Display):
        return IREmit(_compile_value_to_ir(statement.value))
    raise RuntimeSanskriptError(f"Cannot compile unknown statement: {statement!r}")


def _compile_value_to_ir(value: Value) -> IRValue:
    if isinstance(value, Literal):
        return IRLiteral(value.value)
    if isinstance(value, Reference):
        return IRReference(value.name)
    raise RuntimeSanskriptError(f"Cannot compile unknown value: {value!r}")


def _lower_instruction(instruction: IRInstruction) -> tuple[Instruction, ...]:
    if isinstance(instruction, IRStore):
        return (*_lower_value(instruction.value), Instruction(OpCode.STORE_NAME, instruction.target))
    if isinstance(instruction, IRIncrease):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.target),
            *_lower_value(instruction.amount),
            Instruction(OpCode.ADD),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRDecrease):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.target),
            *_lower_value(instruction.amount),
            Instruction(OpCode.SUBTRACT),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IREmit):
        return (*_lower_value(instruction.value), Instruction(OpCode.EMIT))
    raise RuntimeSanskriptError(f"Cannot lower unknown IR instruction: {instruction!r}")


def _lower_value(value: IRValue) -> tuple[Instruction, ...]:
    if isinstance(value, IRLiteral):
        return (Instruction(OpCode.PUSH_INT, value.value),)
    if isinstance(value, IRReference):
        return (Instruction(OpCode.LOAD_NAME, value.name),)
    raise RuntimeSanskriptError(f"Cannot lower unknown IR value: {value!r}")

