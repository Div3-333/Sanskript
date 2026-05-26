from __future__ import annotations

from .ast import (
    Assign,
    BoolLiteral,
    Call,
    CallValue,
    CompareEq,
    Decrease,
    Display,
    FieldContains,
    FieldGet,
    FieldSet,
    FloatLiteral,
    FunctionDef,
    If,
    Increase,
    ListAppend,
    ListInit,
    Literal,
    MapContains,
    MapGet,
    MapInit,
    MapPut,
    Multiply,
    Program,
    Reference,
    RecordInit,
    Return,
    Statement,
    TextLiteral,
    Value,
    While,
)
from .bytecode import (
    BytecodeProgram,
    FunctionBytecode,
    Instruction,
    ModuleBytecode,
    OpCode,
    qualified_function_name,
)
from .errors import RuntimeSanskriptError
from .ir import (
    IRBoolLiteral,
    IRCall,
    IRCallValue,
    IRCompareEq,
    IRDecrease,
    IREmit,
    IRFieldContains,
    IRFieldGet,
    IRFieldSet,
    IRFloatLiteral,
    IRFunction,
    IRIf,
    IRIncrease,
    IRInstruction,
    IRListAppend,
    IRListInit,
    IRMapContains,
    IRMapGet,
    IRMapInit,
    IRMapPut,
    IRModule,
    IRMultiply,
    IRProgram,
    IRReference,
    IRRecordInit,
    IRReturn,
    IRStore,
    IRTextLiteral,
    IRValue,
    IRWhile,
    IRLiteral,
)
from .parser import parse_program


class _Lowerer:
    def __init__(self) -> None:
        self.instructions: list[Instruction] = []

    def emit(self, opcode: OpCode, operand: int | float | str | None = None) -> int:
        index = len(self.instructions)
        self.instructions.append(Instruction(opcode, operand))
        return index

    def patch(self, index: int, operand: int) -> None:
        old = self.instructions[index]
        self.instructions[index] = Instruction(old.opcode, operand)

    def extend(self, items: tuple[Instruction, ...], *, offset: int = 0) -> None:
        if offset:
            items = _relocate_jump_targets(items, offset)
        self.instructions.extend(items)

    def finish(self) -> tuple[Instruction, ...]:
        self.emit(OpCode.HALT)
        return tuple(self.instructions)


def _relocate_jump_targets(
    items: tuple[Instruction, ...],
    offset: int,
) -> tuple[Instruction, ...]:
    jump_ops = {OpCode.JUMP, OpCode.JUMP_IF_ZERO}
    relocated: list[Instruction] = []
    for item in items:
        if item.opcode in jump_ops and isinstance(item.operand, int):
            relocated.append(Instruction(item.opcode, item.operand + offset))
        else:
            relocated.append(item)
    return tuple(relocated)


def compile_source(source: str) -> BytecodeProgram:
    return compile_program(parse_program(source))


def compile_program(program: Program) -> BytecodeProgram:
    ir = compile_program_to_ir(program)
    bytecode = lower_ir_to_bytecode(ir)
    if program.safety_tier == bytecode.safety_tier:
        return bytecode
    return BytecodeProgram(
        bytecode.instructions,
        bytecode.functions,
        bytecode.modules,
        safety_tier=program.safety_tier,
    )


def compile_statements(statements: list[Statement]) -> BytecodeProgram:
    return compile_program(Program(tuple(statements)))


def compile_program_to_ir(program: Program) -> IRProgram:
    top_functions = tuple(
        IRFunction(
            function.name,
            _compile_statement_block(function.body),
            module=None,
            params=function.params,
        )
        for function in program.functions
    )

    modules = tuple(
        IRModule(
            module_name,
            tuple(
                IRFunction(
                    function.name,
                    _compile_statement_block(function.body),
                    module=module_name,
                    params=function.params,
                )
                for function in functions
            ),
        )
        for module_name, functions in program.modules
    )

    return IRProgram(
        _compile_statement_block(program.statements),
        functions=top_functions,
        modules=modules,
    )


def compile_statements_to_ir(statements: list[Statement]) -> IRProgram:
    return compile_program_to_ir(Program(tuple(statements)))


def lower_ir_to_bytecode(program: IRProgram) -> BytecodeProgram:
    main = _lower_instruction_block(program.instructions)

    functions: list[FunctionBytecode] = []
    for function in program.functions:
        key = qualified_function_name(function.module, function.name)
        functions.append(
            FunctionBytecode(
                key,
                _lower_function_body(function.instructions),
                params=function.params,
            )
        )

    modules: list[ModuleBytecode] = []
    for module in program.modules:
        mod_fns = tuple(
            FunctionBytecode(
                qualified_function_name(module.name, function.name),
                _lower_function_body(function.instructions),
                params=function.params,
            )
            for function in module.functions
        )
        modules.append(ModuleBytecode(module.name, mod_fns))

    return BytecodeProgram(main, tuple(functions), tuple(modules))


def _lower_function_body(instructions: tuple[IRInstruction, ...]) -> tuple[Instruction, ...]:
    lowerer = _Lowerer()
    _lower_block(lowerer, instructions)
    lowerer.emit(OpCode.PUSH_INT, 0)
    lowerer.emit(OpCode.RETURN)
    return tuple(lowerer.instructions)


def _lower_instruction_block(instructions: tuple[IRInstruction, ...]) -> tuple[Instruction, ...]:
    lowerer = _Lowerer()
    _lower_block(lowerer, instructions)
    return lowerer.finish()


def _lower_block(lowerer: _Lowerer, instructions: tuple[IRInstruction, ...]) -> None:
    for instruction in instructions:
        chunk = _lower_instruction(instruction)
        if isinstance(instruction, (IRIf, IRWhile)):
            lowerer.extend(chunk, offset=len(lowerer.instructions))
        else:
            lowerer.extend(chunk)


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
    if isinstance(instruction, IRMultiply):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.target),
            *_lower_value(instruction.factor),
            Instruction(OpCode.MULTIPLY),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IREmit):
        return (*_lower_value(instruction.value), Instruction(OpCode.EMIT))
    if isinstance(instruction, IRListInit):
        return (
            Instruction(OpCode.LIST_NEW),
            Instruction(OpCode.STORE_NAME, instruction.container),
        )
    if isinstance(instruction, IRMapInit):
        return (
            Instruction(OpCode.MAP_NEW),
            Instruction(OpCode.STORE_NAME, instruction.container),
        )
    if isinstance(instruction, IRListAppend):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            *_lower_value(instruction.item),
            Instruction(OpCode.LIST_APPEND),
            Instruction(OpCode.STORE_NAME, instruction.container),
        )
    if isinstance(instruction, IRMapPut):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            *_lower_value(instruction.key),
            *_lower_value(instruction.value),
            Instruction(OpCode.MAP_SET),
            Instruction(OpCode.STORE_NAME, instruction.container),
        )
    if isinstance(instruction, IRMapGet):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            *_lower_value(instruction.key),
            Instruction(OpCode.MAP_GET),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRMapContains):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            *_lower_value(instruction.key),
            Instruction(OpCode.MAP_CONTAINS),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRRecordInit):
        return (
            Instruction(OpCode.RECORD_NEW),
            Instruction(OpCode.STORE_NAME, instruction.record),
        )
    if isinstance(instruction, IRFieldSet):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.record),
            *_lower_value(instruction.field),
            *_lower_value(instruction.value),
            Instruction(OpCode.RECORD_SET),
            Instruction(OpCode.STORE_NAME, instruction.record),
        )
    if isinstance(instruction, IRFieldGet):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.record),
            *_lower_value(instruction.field),
            Instruction(OpCode.RECORD_GET),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRFieldContains):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.record),
            *_lower_value(instruction.field),
            Instruction(OpCode.RECORD_CONTAINS),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRCall):
        return (
            *tuple(item for arg in instruction.args for item in _lower_value(arg)),
            Instruction(OpCode.CALL, instruction.target),
            Instruction(OpCode.POP),
        )
    if isinstance(instruction, IRReturn):
        if instruction.value is None:
            return (Instruction(OpCode.PUSH_INT, 0), Instruction(OpCode.RETURN))
        return (*_lower_value(instruction.value), Instruction(OpCode.RETURN))
    if isinstance(instruction, IRIf):
        return _lower_if(instruction)
    if isinstance(instruction, IRWhile):
        return _lower_while(instruction)
    raise RuntimeSanskriptError(f"Cannot lower unknown IR instruction: {instruction!r}")


def _emit_branch_pad(lowerer: _Lowerer) -> int:
    """Landing pad so forward jumps target real instructions in the returned stream."""
    index = len(lowerer.instructions)
    lowerer.emit(OpCode.PUSH_INT, 0)
    lowerer.emit(OpCode.POP)
    return index


def _lower_if(instruction: IRIf) -> tuple[Instruction, ...]:
    lowerer = _Lowerer()
    lowerer.extend(_lower_compare(instruction.condition))
    jump_false = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
    _lower_block(lowerer, instruction.then_body)
    jump_end = lowerer.emit(OpCode.JUMP, 0)
    else_start = len(lowerer.instructions)
    _lower_block(lowerer, instruction.else_body)
    end_label = _emit_branch_pad(lowerer)
    lowerer.patch(jump_false, else_start)
    lowerer.patch(jump_end, end_label)
    return tuple(lowerer.instructions)


def _lower_while(instruction: IRWhile) -> tuple[Instruction, ...]:
    lowerer = _Lowerer()
    loop_start = len(lowerer.instructions)
    lowerer.extend(_lower_compare(instruction.condition))
    jump_exit = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
    _lower_block(lowerer, instruction.body)
    lowerer.emit(OpCode.JUMP, loop_start)
    exit_label = _emit_branch_pad(lowerer)
    lowerer.patch(jump_exit, exit_label)
    return tuple(lowerer.instructions)


def _lower_compare(condition: IRCompareEq) -> tuple[Instruction, ...]:
    return (*_lower_value(condition.left), *_lower_value(condition.right), Instruction(OpCode.COMPARE_EQ))


def _lower_value(value: IRValue) -> tuple[Instruction, ...]:
    if isinstance(value, IRLiteral):
        return (Instruction(OpCode.PUSH_INT, value.value),)
    if isinstance(value, IRFloatLiteral):
        return (Instruction(OpCode.PUSH_FLOAT, value.value),)
    if isinstance(value, IRBoolLiteral):
        return (Instruction(OpCode.PUSH_BOOL, 1 if value.value else 0),)
    if isinstance(value, IRTextLiteral):
        return (Instruction(OpCode.PUSH_TEXT, value.value),)
    if isinstance(value, IRReference):
        return (Instruction(OpCode.LOAD_NAME, value.name),)
    if isinstance(value, IRCallValue):
        return (
            *tuple(item for arg in value.args for item in _lower_value(arg)),
            Instruction(OpCode.CALL, value.target),
        )
    raise RuntimeSanskriptError(f"Cannot lower unknown IR value: {value!r}")


def _compile_statement_block(statements: tuple[Statement, ...]) -> tuple[IRInstruction, ...]:
    items: list[IRInstruction] = []
    for statement in statements:
        if isinstance(statement, FunctionDef):
            continue
        items.append(_compile_statement_to_ir(statement))
    return tuple(items)


def _compile_statement_to_ir(statement: Statement) -> IRInstruction:
    if isinstance(statement, Assign):
        return IRStore(statement.target, _compile_value_to_ir(statement.value))
    if isinstance(statement, Increase):
        return IRIncrease(statement.target, _compile_value_to_ir(statement.amount))
    if isinstance(statement, Decrease):
        return IRDecrease(statement.target, _compile_value_to_ir(statement.amount))
    if isinstance(statement, Multiply):
        return IRMultiply(statement.target, _compile_value_to_ir(statement.factor))
    if isinstance(statement, Display):
        return IREmit(_compile_value_to_ir(statement.value))
    if isinstance(statement, ListInit):
        return IRListInit(statement.container)
    if isinstance(statement, MapInit):
        return IRMapInit(statement.container)
    if isinstance(statement, ListAppend):
        return IRListAppend(statement.container, _compile_value_to_ir(statement.item))
    if isinstance(statement, MapPut):
        return IRMapPut(
            statement.container,
            _compile_value_to_ir(statement.key),
            _compile_value_to_ir(statement.value),
        )
    if isinstance(statement, MapGet):
        return IRMapGet(
            statement.target,
            statement.container,
            _compile_value_to_ir(statement.key),
        )
    if isinstance(statement, MapContains):
        return IRMapContains(
            statement.target,
            statement.container,
            _compile_value_to_ir(statement.key),
        )
    if isinstance(statement, RecordInit):
        return IRRecordInit(statement.record)
    if isinstance(statement, FieldSet):
        return IRFieldSet(
            statement.record,
            _compile_value_to_ir(statement.field),
            _compile_value_to_ir(statement.value),
        )
    if isinstance(statement, FieldGet):
        return IRFieldGet(
            statement.target,
            statement.record,
            _compile_value_to_ir(statement.field),
        )
    if isinstance(statement, FieldContains):
        return IRFieldContains(
            statement.target,
            statement.record,
            _compile_value_to_ir(statement.field),
        )
    if isinstance(statement, If):
        return IRIf(
            IRCompareEq(
                _compile_value_to_ir(statement.condition.left),
                _compile_value_to_ir(statement.condition.right),
            ),
            _compile_statement_block(statement.then_body),
            _compile_statement_block(statement.else_body),
        )
    if isinstance(statement, While):
        return IRWhile(
            IRCompareEq(
                _compile_value_to_ir(statement.condition.left),
                _compile_value_to_ir(statement.condition.right),
            ),
            _compile_statement_block(statement.body),
        )
    if isinstance(statement, Call):
        target = qualified_function_name(statement.module, statement.name)
        return IRCall(target, tuple(_compile_value_to_ir(arg) for arg in statement.args))
    if isinstance(statement, Return):
        value = None if statement.value is None else _compile_value_to_ir(statement.value)
        return IRReturn(value)
    raise RuntimeSanskriptError(f"Cannot compile unknown statement: {statement!r}")


def _compile_value_to_ir(value: Value) -> IRValue:
    if isinstance(value, Literal):
        return IRLiteral(value.value)
    if isinstance(value, FloatLiteral):
        return IRFloatLiteral(value.value)
    if isinstance(value, BoolLiteral):
        return IRBoolLiteral(value.value)
    if isinstance(value, TextLiteral):
        return IRTextLiteral(value.value)
    if isinstance(value, Reference):
        return IRReference(value.name)
    if isinstance(value, CallValue):
        target = qualified_function_name(value.module, value.name)
        return IRCallValue(target, tuple(_compile_value_to_ir(arg) for arg in value.args))
    raise RuntimeSanskriptError(f"Cannot compile unknown value: {value!r}")
