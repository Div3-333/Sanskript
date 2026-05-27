from __future__ import annotations

from dataclasses import dataclass

from .ast import (
    Assert,
    Assign,
    Bind,
    Break,
    ConstDecl,
    Continue,
    CountedFor,
    Defer,
    ForEach,
    ForEachDestructure,
    Guard,
    InfiniteLoop,
    Invariant,
    Match,
    ModuleDef,
    NewtypeDecl,
    Panic,
    PostCondition,
    PreCondition,
    Propagate,
    RecordTypeDecl,
    Throw,
    TryCatch,
    TupleLiteral,
    TypeAliasDecl,
    TypeConvert,
    TypeReflect,
    Until,
    BinaryValue,
    Block,
    BoolAnd,
    BoolAndCond,
    BoolLiteral,
    BoolNot,
    BoolNotCond,
    BoolOr,
    BoolOrCond,
    BytesLiteral,
    Call,
    CallValue,
    PartialApply,
    CompareEq,
    CompareGt,
    CompareIdentity,
    CompareLe,
    CompareLt,
    CompareMembership,
    CompareNe,
    Condition,
    Decrease,
    Display,
    ClassNew,
    ClassMethodCall,
    ClassReflect,
    FieldContains,
    FieldGet,
    FieldSet,
    InstanceFinalize,
    MethodCall,
    MethodReflect,
    PropertyGet,
    StaticMethodCall,
    FloatLiteral,
    ForwardDecl,
    FunctionDef,
    GroupValue,
    HeapAlloc,
    HeapFree,
    HeapLoad,
    HeapStore,
    If,
    Increase,
    ListAppend,
    ListGet,
    ListInit,
    ListLength,
    ListMap,
    ListFilter,
    ListReduce,
    ListAll,
    ListScan,
    ListZip,
    ListEnumerate,
    ListAny,
    ImmutableListInit,
    ImmutableListAppend,
    ListComprehension,
    LazyIterNew,
    LazyIterNext,
    GeneratorNew,
    GeneratorNext,
    Yield,
    PipelineChain,
    MatchExpr,
    ResultBind,
    DataQuery,
    RuleDecl,
    RuleInvoke,
    ListLiteral,
    Literal,
    MapContains,
    MapGet,
    MapInit,
    MapLiteral,
    MapPut,
    Multiply,
    NilLiteral,
    NoneValue,
    Phase3Bind,
    Pop,
    Program,
    ImportDirective,
    ImportSymbol,
    SomeValue,
    Reference,
    RecordInit,
    Return,
    Statement,
    TextConcat,
    TextContains,
    TextGet,
    TextLength,
    TextLiteral,
    TextSlice,
    UnsafeEnter,
    UnsafeExit,
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
from .errors import CompileError, RuntimeSanskriptError
from .ir import (
    IRBoolAnd,
    IRBoolAndCond,
    IRBoolLiteral,
    IRBoolNot,
    IRBoolNotCond,
    IRBoolOr,
    IRBoolOrCond,
    IRBinaryValue,
    IRBytesLiteral,
    IRCall,
    IRCallValue,
    IRCompareEq,
    IRCompareGt,
    IRCompareIdentity,
    IRCompareLe,
    IRCompareLt,
    IRCompareMembership,
    IRCompareNe,
    IRCondition,
    IRDecrease,
    IREmit,
    IRFieldContains,
    IRFieldGet,
    IRFieldSet,
    IRClassNew,
    IRMethodCall,
    IRStaticMethodCall,
    IRClassMethodCall,
    IRPropertyGet,
    IRInstanceFinalize,
    IRClassReflect,
    IRMethodReflect,
    IRFloatLiteral,
    IRFunction,
    IRGroupValue,
    IRHeapAlloc,
    IRHeapFree,
    IRHeapLoad,
    IRPhase3Bind,
    IRPhase3Bind,
    IRPhase3Opcode,
    IRPhase3Value,
    IRPhase3Value,
    IRHeapStore,
    IRIf,
    IRIncrease,
    IRInstruction,
    IRListAppend,
    IRListGet,
    IRListInit,
    IRListLength,
    IRListMap,
    IRListFilter,
    IRListReduce,
    IRListAll,
    IRListScan,
    IRListZip,
    IRListEnumerate,
    IRListAny,
    IRImmutableListInit,
    IRImmutableListAppend,
    IRListComprehension,
    IRLazyIterNew,
    IRLazyIterNext,
    IRGeneratorNew,
    IRGeneratorNext,
    IRYield,
    IRPipelineChain,
    IRMatchExpr,
    IRResultBind,
    IRDataQuery,
    IRRuleDecl,
    IRRuleInvoke,
    IRListLiteral,
    IRMapContains,
    IRMapGet,
    IRMapInit,
    IRMapLiteral,
    IRMapPut,
    IRModule,
    IRMultiply,
    IRNilLiteral,
    IRPop,
    IRProgram,
    IRReference,
    IRRecordInit,
    IRReturn,
    IRScopeEnter,
    IRScopeExit,
    IRStore,
    IRTextLiteral,
    IRTextConcat,
    IRTextContains,
    IRTextGet,
    IRTextLength,
    IRTextSlice,
    IRUnsafeEnter,
    IRUnsafeExit,
    IRValue,
    IRAssert,
    IRBreak,
    IRContinue,
    IRCountedFor,
    IRDefer,
    IRForEach,
    IRInfiniteLoop,
    IRMatch,
    IRPropagate,
    IRUntil,
    IRWhile,
    IRLiteral,
    IRThrow,
    IRPanic,
    IRTryCatch,
    IRForEachDestructure,
    IRCondAssert,
    IRTupleLiteral,
)
from .parser import parse_program
from .scope import ScopeStack

_BINARY_OPCODES: dict[str, OpCode] = {
    "add": OpCode.ADD,
    "subtract": OpCode.SUBTRACT,
    "multiply": OpCode.MULTIPLY,
    "divide": OpCode.DIVIDE,
}


@dataclass
class _LoopContext:
    start_ip: int
    break_patches: list[int]
    label: str | None = None


class _Lowerer:
    def __init__(self) -> None:
        self.instructions: list[Instruction] = []
        self._loop_stack: list[_LoopContext] = []

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
    from .type_checker import check_program

    program = _resolve_imports(program)
    check_program(program)
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
    global _CLASS_METADATA, _COMPILE_PROGRAM
    program = _resolve_imports(program)
    _validate_module_exports(program)
    _NESTED_IR_FUNCTIONS.clear()
    _index_functions(program)
    _PROGRAM_SAFETY_TIER = program.safety_tier
    from .oop import build_class_metadata

    _COMPILE_PROGRAM = program
    _CLASS_METADATA = build_class_metadata(program)

    top_functions = tuple(
        _compile_function_with_nested(function, module=None) for function in program.functions
    )

    modules = tuple(
        IRModule(
            module.name if hasattr(module, "name") else module[0],
            tuple(
                _compile_function_with_nested(
                    function, module=module.name if hasattr(module, "name") else module[0]
                )
                for function in (module.functions if hasattr(module, "functions") else module[1])
            ),
        )
        for module in program.modules
    )

    scope = ScopeStack()
    rule_stmts: list[IRInstruction] = [
        IRRuleDecl(rule.rule_id, rule.when_function, rule.then_function) for rule in program.rules
    ]
    return IRProgram(
        tuple(rule_stmts) + _compile_statement_block(program.statements, scope=scope),
        functions=top_functions + tuple(_NESTED_IR_FUNCTIONS),
        modules=modules,
    )


_NESTED_IR_FUNCTIONS: list[IRFunction] = []
_COMPILE_FUNCTIONS: dict[str, list[FunctionDef]] = {}
_CURRENT_FN_KEY: str | None = None
_PROGRAM_SAFETY_TIER: str = "surakshita"

_CLASS_METADATA: dict | None = None
_COMPILE_PROGRAM: Program | None = None


def _resolve_function_symbol(base: str, *, arity: int) -> str:
    """Map logical name (e.g. Point__sum) to emitted function symbol (overload suffix)."""
    if _COMPILE_PROGRAM is None:
        return base
    exact: list[str] = []
    prefixed: list[str] = []
    for function in _COMPILE_PROGRAM.functions:
        if function.name == base:
            exact.append(function.name)
        elif function.name.startswith(f"{base}_"):
            prefixed.append(function.name)
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        for name in exact:
            fn = next(f for f in _COMPILE_PROGRAM.functions if f.name == name)
            if len(fn.params) == arity:
                return name
        return exact[0]
    for name in sorted(prefixed):
        fn = next(f for f in _COMPILE_PROGRAM.functions if f.name == name)
        if len(fn.params) == arity:
            return name
    return prefixed[0] if len(prefixed) == 1 else base


def _index_functions(program: Program) -> None:
    _COMPILE_FUNCTIONS.clear()
    all_modules = []
    for module in program.modules:
        functions = module.functions if hasattr(module, "functions") else module[1]
        all_modules.append(tuple(functions))
    all_fns = tuple(program.functions) + tuple(function for functions in all_modules for function in functions)
    for function in all_fns:
        _COMPILE_FUNCTIONS.setdefault(function.name, []).append(function)


def _overload_key_for(function: FunctionDef, all_functions: tuple[FunctionDef, ...]) -> str:
    same = [fn for fn in all_functions if fn.name == function.name]
    if len(same) <= 1:
        return function.name
    return f"{function.name}_{len(function.params)}"


def _overload_key(function: FunctionDef) -> str:
    all_fns = tuple(
        fn
        for fns in _COMPILE_FUNCTIONS.values()
        for fn in fns
    )
    return _overload_key_for(function, all_fns) if all_fns else function.name


def _resolve_compile_target(name: str, *, arity: int) -> str:
    candidates = _COMPILE_FUNCTIONS.get(name, [])
    if not candidates:
        return name
    arity_matches = [fn for fn in candidates if len(fn.params) == arity]
    all_fns = _all_indexed_functions()
    if len(arity_matches) == 1:
        return _overload_key_for(arity_matches[0], all_fns)
    if len(candidates) == 1:
        return _overload_key_for(candidates[0], all_fns)
    chosen = arity_matches[0] if arity_matches else candidates[0]
    return _overload_key_for(chosen, all_fns)


def _all_indexed_functions() -> tuple[FunctionDef, ...]:
    seen: dict[int, FunctionDef] = {}
    for functions in _COMPILE_FUNCTIONS.values():
        for function in functions:
            seen[id(function)] = function
    return tuple(seen.values())


def _find_function_def(name: str) -> FunctionDef | None:
    matches = _COMPILE_FUNCTIONS.get(name, [])
    return matches[0] if matches else None


def _find_inline_function(name: str, module: str | None) -> FunctionDef | None:
    fn = _find_function_def(name)
    if fn is not None and fn.is_inline:
        return fn
    return None


def _find_compile_time_function(name: str) -> FunctionDef | None:
    fn = _find_function_def(name)
    if fn is not None and fn.is_compile_time:
        return fn
    return None


def _inline_call_instructions(function: FunctionDef, call: Call) -> tuple[IRInstruction, ...]:
    scope = ScopeStack()
    for index, param in enumerate(function.params):
        if index < len(call.args):
            scope.declare(param)
    body = _compile_function_body(function.body, params=function.params)
    items: list[IRInstruction] = []
    for index, param in enumerate(function.params):
        if index < len(call.args):
            items.append(IRStore(param, _compile_value_to_ir(call.args[index])))
    items.extend(body)
    return tuple(items)


def _expand_macro_call(function: FunctionDef, call: Call) -> tuple[IRInstruction, ...]:
    """Expand compile-time macro body with literal argument substitution."""
    if len(call.args) != len(function.params):
        raise CompileError(
            f"Macro {function.name!r} expects {len(function.params)} arguments, got {len(call.args)}",
        )
    subst: dict[str, Value] = {}
    for param, arg in zip(function.params, call.args):
        if not isinstance(arg, Literal):
            raise CompileError(
                f"Macro argument {param!r} must be a compile-time literal",
                hint="Pass numeric or text literals to compile-time functions.",
            )
        subst[param] = arg
    expanded: list[Statement] = []
    for statement in function.body:
        if isinstance(statement, Return) and statement.value is not None:
            expanded.append(Return(_substitute_value(statement.value, subst)))
        elif isinstance(statement, Assign):
            expanded.append(Assign(statement.target, _substitute_value(statement.value, subst)))
        else:
            expanded.append(statement)
    scope = ScopeStack()
    return _compile_statement_block(tuple(expanded), scope=scope)


def _order_call_arguments(
    name: str,
    positional: tuple[Value, ...],
    kwargs: tuple[tuple[str, Value], ...],
) -> tuple[Value, ...]:
    candidates = _COMPILE_FUNCTIONS.get(name, [])
    fn = next((f for f in candidates if len(f.params) == len(positional) + len(kwargs)), None)
    if fn is None:
        fn = candidates[0] if candidates else None
    if fn is None or not kwargs:
        return positional
    kw_map = dict(kwargs)
    ordered: list[Value] = []
    pos_index = 0
    for param in fn.params:
        if param in kw_map:
            ordered.append(kw_map[param])
        elif pos_index < len(positional):
            ordered.append(positional[pos_index])
            pos_index += 1
    return tuple(ordered)


def _substitute_value(value: Value, subst: dict[str, Value]) -> Value:
    if isinstance(value, Reference) and value.name in subst:
        return subst[value.name]
    if isinstance(value, BinaryValue):
        return BinaryValue(
            value.operator,
            _substitute_value(value.left, subst),
            _substitute_value(value.right, subst),
        )
    return value


def _apply_decorators(function: FunctionDef, body: tuple[IRInstruction, ...]) -> tuple[IRInstruction, ...]:
    items: list[IRInstruction] = []
    for decorator in function.decorators:
        if decorator in {"trace", "anuvīkṣaṇam", "anuvikshanam"}:
            items.append(IREmit(IRTextLiteral(f"[trace] enter {function.name}")))
    items.extend(body)
    for decorator in function.decorators:
        if decorator in {"trace", "anuvīkṣaṇam", "anuvikshanam"}:
            items.append(IREmit(IRTextLiteral(f"[trace] leave {function.name}")))
    return tuple(items)


def _compile_function_with_nested(function: FunctionDef, *, module: str | None) -> IRFunction:
    global _CURRENT_FN_KEY
    ir_name = qualified_function_name(module, function.name)
    previous_key = _CURRENT_FN_KEY
    _CURRENT_FN_KEY = ir_name
    raw_body = _compile_function_body(function.body, params=function.params, function_key=ir_name)
    body = _apply_decorators(function, raw_body)
    _CURRENT_FN_KEY = previous_key
    deco = set(function.decorators)
    mangled = _overload_key_for(function, _all_indexed_functions())
    return IRFunction(
        mangled,
        body,
        module=module,
        params=function.params,
        defaults=tuple(_compile_value_to_ir(v) if v is not None else None for v in function.param_defaults),
        variadic_param=function.variadic_param,
        capture_mut=function.capture_mut,
        effect=function.effect,
        is_generator=any(d in {"utpādaka", "utpadaka"} for d in deco),
        is_memoized=any(d in {"smaraṇa", "smarana"} for d in deco),
        is_inline=function.is_inline,
        is_naked=function.is_naked,
        abi_name=function.abi_name,
        named_returns=function.named_returns,
    )


def _validate_module_exports(program: Program) -> None:
    module_index: dict[str, ModuleDef] = {}
    for module in program.modules:
        if hasattr(module, "name"):
            module_index[module.name] = module
        else:
            # Backward compatibility for tuple-based module fixtures in legacy tests.
            name, functions = module
            module_index[name] = ModuleDef(name=name, functions=functions, exports=frozenset(), reexports=())
    for module in program.modules:
        functions = module.functions if hasattr(module, "functions") else module[1]
        exports = module.exports if hasattr(module, "exports") else frozenset()
        reexports = module.reexports if hasattr(module, "reexports") else ()
        defined = {function.name for function in functions}
        for name in exports:
            if name in defined:
                continue
            reexport = next((item for item in reexports if item.name == name), None)
            if reexport is None:
                mod_name = module.name if hasattr(module, "name") else module[0]
                raise CompileError(
                    f"Export {name!r} is not defined in module {mod_name!r}",
                    hint="Add a vidhānam, punaranayanam re-export, or fix niḥsāram.",
                )
            source = module_index.get(reexport.source_module)
            if source is None:
                raise CompileError(
                    f"Re-export source module {reexport.source_module!r} is not loaded",
                    hint="Import the source module before punaranayanam.",
                )
            source_defined = {fn.name for fn in source.functions}
            if reexport.source_symbol not in source_defined:
                raise CompileError(
                    f"Re-export {name!r} refers to missing symbol {reexport.source_symbol!r}",
                    hint="Export the symbol from the source module with niḥsāram.",
                )


def _resolve_imports(program: Program) -> Program:
    if not program.imports:
        _validate_module_visibility(program)
        return program
    module_index = {module.name: module for module in program.modules}
    alias_map: dict[str, str] = {}
    selective_map: dict[str, tuple[str, str]] = {}
    reexport_map: dict[tuple[str, str], tuple[str, str]] = {}
    for module in program.modules:
        for item in module.reexports:
            reexport_map[(module.name, item.name)] = (item.source_module, item.source_symbol)
    for directive in program.imports:
        module_name = _resolve_imported_module_name(directive, module_index)
        local_name = directive.alias or _default_import_local_name(directive.module_path, module_name)
        alias_map[local_name] = module_name
        if directive.symbols:
            for symbol in directive.symbols:
                target_name = symbol.alias or symbol.name
                selective_map[target_name] = (module_name, symbol.name)
    resolved_statements = tuple(
        _resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in program.statements
    )
    resolved_functions = tuple(
        FunctionDef(
            function.name,
            tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in function.body),
            module=function.module,
            params=function.params,
            param_defaults=function.param_defaults,
            variadic_param=function.variadic_param,
            type_params=function.type_params,
            param_types=function.param_types,
            return_type=function.return_type,
            type_param_bounds=function.type_param_bounds,
            effect=function.effect,
            decorators=function.decorators,
            capture_mut=function.capture_mut,
            is_inline=function.is_inline,
            is_naked=function.is_naked,
            is_compile_time=function.is_compile_time,
            named_returns=function.named_returns,
            abi_name=function.abi_name,
        )
        for function in program.functions
    )
    resolved_modules = tuple(
        ModuleDef(
            module.name,
            tuple(
                FunctionDef(
                    function.name,
                    tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in function.body),
                    module=function.module,
                    params=function.params,
                    param_defaults=function.param_defaults,
                    variadic_param=function.variadic_param,
                    type_params=function.type_params,
                    param_types=function.param_types,
                    return_type=function.return_type,
                    type_param_bounds=function.type_param_bounds,
                    effect=function.effect,
                    decorators=function.decorators,
                    capture_mut=function.capture_mut,
                    is_inline=function.is_inline,
                    is_naked=function.is_naked,
                    is_compile_time=function.is_compile_time,
                    named_returns=function.named_returns,
                    abi_name=function.abi_name,
                )
                for function in module.functions
            ),
            module.exports,
            module.reexports,
        )
        for module in program.modules
    )
    resolved = Program(
        resolved_statements,
        resolved_functions,
        resolved_modules,
        imports=(),
        safety_tier=program.safety_tier,
        type_aliases=program.type_aliases,
        newtypes=program.newtypes,
        record_types=program.record_types,
        constants=program.constants,
        generic_records=program.generic_records,
        traits=program.traits,
        trait_impls=program.trait_impls,
        classes=program.classes,
        lifetimes=program.lifetimes,
    )
    _validate_module_visibility(resolved)
    return resolved


def _resolve_imported_module_name(directive: ImportDirective, module_index: dict[str, ModuleDef]) -> str:
    candidate = _default_import_local_name(directive.module_path, "")
    if candidate in module_index:
        return candidate
    if len(module_index) == 1:
        only = next(iter(module_index))
        return only
    raise CompileError(
        f"Cannot resolve import path {directive.module_path!r} to a loaded module",
        hint="Match the module name with kṣetram name or import a file with one module.",
    )


def _default_import_local_name(module_path: str, fallback: str) -> str:
    cleaned = module_path.replace("\\", "/").rstrip("/")
    if "/" in cleaned:
        cleaned = cleaned.rsplit("/", 1)[-1]
    if "." in cleaned:
        cleaned = cleaned.rsplit(".", 1)[-1]
    return cleaned or fallback


def _resolve_statement_calls(
    statement: Statement,
    alias_map: dict[str, str],
    selective_map: dict[str, tuple[str, str]],
    reexport_map: dict[tuple[str, str], tuple[str, str]],
) -> Statement:
    if isinstance(statement, Call):
        if statement.module is not None:
            module_name = alias_map.get(statement.module, statement.module)
            fn_name = statement.name
            redirected = reexport_map.get((module_name, fn_name))
            if redirected is not None:
                module_name, fn_name = redirected
            return Call(
                fn_name,
                module=module_name,
                args=tuple(_resolve_value_calls(arg, alias_map, selective_map, reexport_map) for arg in statement.args),
            )
        if statement.name in selective_map:
            module_name, fn_name = selective_map[statement.name]
            return Call(
                fn_name,
                module=module_name,
                args=tuple(_resolve_value_calls(arg, alias_map, selective_map, reexport_map) for arg in statement.args),
            )
        return Call(
            statement.name,
            module=None,
            args=tuple(_resolve_value_calls(arg, alias_map, selective_map, reexport_map) for arg in statement.args),
        )
    if isinstance(statement, Bind):
        return Bind(
            statement.target,
            _resolve_value_calls(statement.value, alias_map, selective_map, reexport_map),
            immutable=statement.immutable,
            ownership=statement.ownership,
            lifetime=statement.lifetime,
        )
    if isinstance(statement, Assign):
        return Assign(statement.target, _resolve_value_calls(statement.value, alias_map, selective_map, reexport_map))
    if isinstance(statement, Display):
        return Display(_resolve_value_calls(statement.value, alias_map, selective_map, reexport_map))
    if isinstance(statement, Return) and statement.value is not None:
        return Return(_resolve_value_calls(statement.value, alias_map, selective_map, reexport_map))
    if isinstance(statement, Block):
        return Block(tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in statement.body))
    if isinstance(statement, If):
        return If(
            _resolve_condition_calls(statement.condition, alias_map, selective_map, reexport_map),
            tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in statement.then_body),
            tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in statement.else_body),
            tuple(
                (
                    _resolve_condition_calls(cond, alias_map, selective_map, reexport_map),
                    tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in body),
                )
                for cond, body in statement.elif_branches
            ),
        )
    if isinstance(statement, While):
        return While(
            _resolve_condition_calls(statement.condition, alias_map, selective_map, reexport_map),
            tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in statement.body),
            label=statement.label,
        )
    if isinstance(statement, Until):
        return Until(
            _resolve_condition_calls(statement.condition, alias_map, selective_map, reexport_map),
            tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in statement.body),
            label=statement.label,
        )
    if isinstance(statement, CountedFor):
        return CountedFor(
            statement.counter,
            _resolve_value_calls(statement.start, alias_map, selective_map, reexport_map),
            _resolve_value_calls(statement.end, alias_map, selective_map, reexport_map),
            tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in statement.body),
            label=statement.label,
        )
    if isinstance(statement, ForEach):
        return ForEach(
            statement.item,
            statement.container,
            tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in statement.body),
            label=statement.label,
        )
    if isinstance(statement, InfiniteLoop):
        return InfiniteLoop(
            tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in statement.body),
            label=statement.label,
        )
    if isinstance(statement, TryCatch):
        return TryCatch(
            tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in statement.body),
            statement.error_name,
            tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in statement.handler),
        )
    if isinstance(statement, ForEachDestructure):
        return ForEachDestructure(
            statement.names,
            statement.container,
            tuple(_resolve_statement_calls(item, alias_map, selective_map, reexport_map) for item in statement.body),
            label=statement.label,
        )
    return statement


def _resolve_value_calls(
    value: Value,
    alias_map: dict[str, str],
    selective_map: dict[str, tuple[str, str]],
    reexport_map: dict[tuple[str, str], tuple[str, str]],
) -> Value:
    if isinstance(value, CallValue):
        if value.module is not None:
            module_name = alias_map.get(value.module, value.module)
            fn_name = value.name
            redirected = reexport_map.get((module_name, fn_name))
            if redirected is not None:
                module_name, fn_name = redirected
            return CallValue(
                fn_name,
                module=module_name,
                args=tuple(_resolve_value_calls(arg, alias_map, selective_map, reexport_map) for arg in value.args),
            )
        if value.name in selective_map:
            module_name, fn_name = selective_map[value.name]
            return CallValue(
                fn_name,
                module=module_name,
                args=tuple(_resolve_value_calls(arg, alias_map, selective_map, reexport_map) for arg in value.args),
            )
        return CallValue(
            value.name,
            args=tuple(_resolve_value_calls(arg, alias_map, selective_map, reexport_map) for arg in value.args),
        )
    if isinstance(value, BinaryValue):
        return BinaryValue(
            value.operator,
            _resolve_value_calls(value.left, alias_map, selective_map, reexport_map),
            _resolve_value_calls(value.right, alias_map, selective_map, reexport_map),
        )
    if isinstance(value, BoolNot):
        return BoolNot(_resolve_value_calls(value.operand, alias_map, selective_map, reexport_map))
    if isinstance(value, BoolAnd):
        return BoolAnd(
            _resolve_value_calls(value.left, alias_map, selective_map, reexport_map),
            _resolve_value_calls(value.right, alias_map, selective_map, reexport_map),
        )
    if isinstance(value, BoolOr):
        return BoolOr(
            _resolve_value_calls(value.left, alias_map, selective_map, reexport_map),
            _resolve_value_calls(value.right, alias_map, selective_map, reexport_map),
        )
    return value


def _resolve_condition_calls(
    condition: Condition,
    alias_map: dict[str, str],
    selective_map: dict[str, tuple[str, str]],
    reexport_map: dict[tuple[str, str], tuple[str, str]],
) -> Condition:
    if isinstance(condition, (CompareEq, CompareNe, CompareLt, CompareGt, CompareLe, CompareIdentity)):
        return type(condition)(
            _resolve_value_calls(condition.left, alias_map, selective_map, reexport_map),
            _resolve_value_calls(condition.right, alias_map, selective_map, reexport_map),
        )
    if isinstance(condition, CompareMembership):
        return CompareMembership(
            _resolve_value_calls(condition.container, alias_map, selective_map, reexport_map),
            _resolve_value_calls(condition.key, alias_map, selective_map, reexport_map),
        )
    if isinstance(condition, BoolNotCond):
        return BoolNotCond(_resolve_condition_calls(condition.operand, alias_map, selective_map, reexport_map))
    if isinstance(condition, BoolAndCond):
        return BoolAndCond(
            _resolve_condition_calls(condition.left, alias_map, selective_map, reexport_map),
            _resolve_condition_calls(condition.right, alias_map, selective_map, reexport_map),
        )
    if isinstance(condition, BoolOrCond):
        return BoolOrCond(
            _resolve_condition_calls(condition.left, alias_map, selective_map, reexport_map),
            _resolve_condition_calls(condition.right, alias_map, selective_map, reexport_map),
        )
    return condition


def _validate_module_visibility(program: Program) -> None:
    modules: dict[str, ModuleDef] = {}
    for module in program.modules:
        if hasattr(module, "name"):
            modules[module.name] = module
        else:
            # Backward compatibility for tuple-based module fixtures in legacy tests.
            name, functions = module
            modules[name] = ModuleDef(name=name, functions=functions, exports=frozenset())
    for statement in program.statements:
        _validate_statement_visibility(statement, modules)
    for function in program.functions:
        for statement in function.body:
            _validate_statement_visibility(statement, modules)
    for module in program.modules:
        functions = module.functions if hasattr(module, "functions") else module[1]
        for function in functions:
            for statement in function.body:
                _validate_statement_visibility(statement, modules)


def _validate_statement_visibility(statement: Statement, modules: dict[str, ModuleDef]) -> None:
    if isinstance(statement, Call):
        _validate_call_visibility(statement.module, statement.name, modules)
        for arg in statement.args:
            _validate_value_visibility(arg, modules)
        return
    if isinstance(statement, (Assign, Bind)):
        _validate_value_visibility(statement.value, modules)
    if isinstance(statement, Display):
        _validate_value_visibility(statement.value, modules)
    if isinstance(statement, Return) and statement.value is not None:
        _validate_value_visibility(statement.value, modules)
    if isinstance(statement, Block):
        for item in statement.body:
            _validate_statement_visibility(item, modules)
    if isinstance(statement, If):
        _validate_condition_visibility(statement.condition, modules)
        for item in statement.then_body:
            _validate_statement_visibility(item, modules)
        for item in statement.else_body:
            _validate_statement_visibility(item, modules)
        for cond, body in statement.elif_branches:
            _validate_condition_visibility(cond, modules)
            for item in body:
                _validate_statement_visibility(item, modules)
    if isinstance(statement, (While, Until)):
        _validate_condition_visibility(statement.condition, modules)
        for item in statement.body:
            _validate_statement_visibility(item, modules)
    if isinstance(statement, (CountedFor,)):
        _validate_value_visibility(statement.start, modules)
        _validate_value_visibility(statement.end, modules)
        for item in statement.body:
            _validate_statement_visibility(item, modules)
    if isinstance(statement, (ForEach, InfiniteLoop, ForEachDestructure)):
        for item in statement.body:
            _validate_statement_visibility(item, modules)
    if isinstance(statement, TryCatch):
        for item in statement.body:
            _validate_statement_visibility(item, modules)
        for item in statement.handler:
            _validate_statement_visibility(item, modules)


def _validate_value_visibility(value: Value, modules: dict[str, ModuleDef]) -> None:
    if isinstance(value, CallValue):
        _validate_call_visibility(value.module, value.name, modules)
        for arg in value.args:
            _validate_value_visibility(arg, modules)
    if isinstance(value, BinaryValue):
        _validate_value_visibility(value.left, modules)
        _validate_value_visibility(value.right, modules)
    if isinstance(value, BoolNot):
        _validate_value_visibility(value.operand, modules)
    if isinstance(value, (BoolAnd, BoolOr)):
        _validate_value_visibility(value.left, modules)
        _validate_value_visibility(value.right, modules)


def _validate_condition_visibility(condition: Condition, modules: dict[str, ModuleDef]) -> None:
    if isinstance(condition, (CompareEq, CompareNe, CompareLt, CompareGt, CompareLe, CompareIdentity)):
        _validate_value_visibility(condition.left, modules)
        _validate_value_visibility(condition.right, modules)
    if isinstance(condition, CompareMembership):
        _validate_value_visibility(condition.container, modules)
        _validate_value_visibility(condition.key, modules)
    if isinstance(condition, BoolNotCond):
        _validate_condition_visibility(condition.operand, modules)
    if isinstance(condition, (BoolAndCond, BoolOrCond)):
        _validate_condition_visibility(condition.left, modules)
        _validate_condition_visibility(condition.right, modules)


def _validate_call_visibility(module_name: str | None, function_name: str, modules: dict[str, ModuleDef]) -> None:
    if module_name is None:
        return
    module = modules.get(module_name)
    if module is None:
        raise CompileError(f"Unknown module {module_name!r} in call to {function_name!r}")
    reexport = next((item for item in module.reexports if item.name == function_name), None)
    if reexport is not None:
        _validate_call_visibility(reexport.source_module, reexport.source_symbol, modules)
        return
    defined = {fn.name for fn in module.functions}
    if function_name not in defined:
        raise CompileError(f"Unknown function {function_name!r} in module {module_name!r}")
    if module.exports and function_name not in module.exports:
        raise CompileError(
            f"Function {function_name!r} in module {module_name!r} is private",
            hint="Export it with niḥsāram or call a public symbol.",
        )


def _compile_function_body(
    statements: tuple[Statement, ...],
    *,
    params: tuple[str, ...],
    function_key: str | None = None,
) -> tuple[IRInstruction, ...]:
    scope = ScopeStack()
    prologue: list[IRInstruction] = []
    for param in params:
        if param.startswith("__destruct__"):
            names = param[len("__destruct__"):].split("__")
            scope.declare(param)
            for i, name in enumerate(names):
                scope.declare(name)
                prologue.append(IRPhase3Opcode("load_name", param))
                prologue.append(IRPhase3Opcode("tuple_get", i))  # operand=index
                prologue.append(IRPhase3Opcode("store_name", name))
        else:
            scope.declare(param)
    body_statements: list[Statement] = []
    for statement in statements:
        if isinstance(statement, FunctionDef):
            nested_base = (function_key or "fn").replace(".", "__")
            nested_name = f"{nested_base}::{statement.name}"
            _NESTED_IR_FUNCTIONS.append(
                IRFunction(
                    nested_name,
                    _compile_function_body(
                        statement.body,
                        params=statement.params,
                        function_key=nested_name,
                    ),
                    module=None,
                    params=statement.params,
                    defaults=tuple(
                        _compile_value_to_ir(v) if v is not None else None
                        for v in statement.param_defaults
                    ),
                    variadic_param=statement.variadic_param,
                )
            )
            prologue.append(IRPhase3Opcode("push_func", nested_name))
            prologue.append(IRPhase3Opcode("store_name", statement.name))
            continue
        body_statements.append(statement)
    return (*prologue, *_compile_statement_block(tuple(body_statements), scope=scope))


def compile_statements_to_ir(statements: list[Statement]) -> IRProgram:
    scope = ScopeStack()
    return IRProgram(_compile_statement_block(tuple(statements), scope=scope))


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
                defaults=tuple(
                    _ir_default_to_operand(item) for item in function.defaults
                ) if function.defaults else (),
                variadic_param=function.variadic_param,
                capture_mut=function.capture_mut,
                effect=function.effect,
                is_generator=getattr(function, "is_generator", False),
                is_memoized=getattr(function, "is_memoized", False),
                is_inline=function.is_inline,
                is_naked=function.is_naked,
                abi_name=function.abi_name,
                named_returns=function.named_returns,
            )
        )

    modules: list[ModuleBytecode] = []
    for module in program.modules:
        mod_fns = tuple(
            FunctionBytecode(
                qualified_function_name(module.name, function.name),
                _lower_function_body(function.instructions),
                params=function.params,
                defaults=tuple(
                    _ir_default_to_operand(item) for item in function.defaults
                ) if function.defaults else (),
                variadic_param=function.variadic_param,
                capture_mut=function.capture_mut,
                effect=function.effect,
                is_inline=function.is_inline,
                is_naked=function.is_naked,
                abi_name=function.abi_name,
                named_returns=function.named_returns,
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
        if isinstance(instruction, IRBreak):
            ctx = _resolve_loop(lowerer, instruction.label)
            ctx.break_patches.append(lowerer.emit(OpCode.JUMP, 0))
            continue
        if isinstance(instruction, IRContinue):
            ctx = _resolve_loop(lowerer, instruction.label)
            lowerer.emit(OpCode.JUMP, ctx.start_ip)
            continue
        chunk = _lower_instruction(instruction, lowerer)
        control_flow = (
            IRIf,
            IRWhile,
            IRUntil,
            IRCountedFor,
            IRForEach,
            IRInfiniteLoop,
            IRMatch,
            IRTryCatch,
            IRForEachDestructure,
            IRCondAssert,
            IRAssert,
        )
        if isinstance(instruction, control_flow) and lowerer is not None:
            continue
        if isinstance(instruction, control_flow):
            lowerer.extend(chunk, offset=len(lowerer.instructions))
        else:
            lowerer.extend(chunk)


def _lower_instruction(
    instruction: IRInstruction,
    lowerer: _Lowerer | None = None,
) -> tuple[Instruction, ...]:
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
    if isinstance(instruction, IRPop):
        return (*_lower_value(instruction.value), Instruction(OpCode.POP))
    if isinstance(instruction, IRScopeEnter):
        return (Instruction(OpCode.SCOPE_ENTER),)
    if isinstance(instruction, IRScopeExit):
        return (Instruction(OpCode.SCOPE_EXIT),)
    if isinstance(instruction, IRTextConcat):
        return (
            *_lower_value(instruction.left),
            *_lower_value(instruction.right),
            Instruction(OpCode.TEXT_CONCAT),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRTextLength):
        return (
            *_lower_value(instruction.text),
            Instruction(OpCode.TEXT_LEN),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRTextGet):
        return (
            *_lower_value(instruction.text),
            *_lower_value(instruction.index),
            Instruction(OpCode.TEXT_GET),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRTextSlice):
        return (
            *_lower_value(instruction.text),
            *_lower_value(instruction.start),
            *_lower_value(instruction.end),
            Instruction(OpCode.TEXT_SLICE),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRTextContains):
        return (
            *_lower_value(instruction.text),
            *_lower_value(instruction.needle),
            Instruction(OpCode.TEXT_CONTAINS),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
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
    if isinstance(instruction, IRListGet):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            *_lower_value(instruction.index),
            Instruction(OpCode.LIST_GET),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRListLength):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            Instruction(OpCode.LIST_LEN),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRListMap):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            Instruction(OpCode.LIST_MAP, instruction.function_name),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRListFilter):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            Instruction(OpCode.LIST_FILTER, instruction.function_name),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRListReduce):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            *_lower_value(instruction.initial),
            Instruction(OpCode.LIST_REDUCE, instruction.function_name),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRListAll):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            Instruction(OpCode.LIST_ALL, instruction.function_name),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRListScan):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            *_lower_value(instruction.initial),
            Instruction(OpCode.LIST_SCAN, instruction.function_name),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRListZip):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.left),
            Instruction(OpCode.LOAD_NAME, instruction.right),
            Instruction(OpCode.LIST_ZIP),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRListEnumerate):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            Instruction(OpCode.LIST_ENUMERATE),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRListAny):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            Instruction(OpCode.LIST_ANY, instruction.function_name),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRImmutableListInit):
        return (
            Instruction(OpCode.IMMUTABLE_LIST_NEW),
            Instruction(OpCode.STORE_NAME, instruction.container),
        )
    if isinstance(instruction, IRImmutableListAppend):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            *_lower_value(instruction.item),
            Instruction(OpCode.IMMUTABLE_LIST_APPEND),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRListComprehension):
        operand = f"{instruction.where_function},{instruction.with_function}"
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            Instruction(OpCode.LIST_COMPREHENSION, operand),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRLazyIterNew):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            Instruction(OpCode.LAZY_ITER_NEW),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRLazyIterNext):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.iterator),
            Instruction(OpCode.LAZY_ITER_NEXT),
            Instruction(OpCode.STORE_NAME, instruction.value),
            Instruction(OpCode.STORE_NAME, instruction.has_more),
        )
    if isinstance(instruction, IRGeneratorNew):
        return (
            Instruction(OpCode.GENERATOR_NEW, instruction.function_name),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRGeneratorNext):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.generator),
            Instruction(OpCode.GENERATOR_NEXT),
            Instruction(OpCode.STORE_NAME, instruction.value),
            Instruction(OpCode.STORE_NAME, instruction.has_more),
        )
    if isinstance(instruction, IRYield):
        return (*_lower_value(instruction.value), Instruction(OpCode.GENERATOR_YIELD))
    if isinstance(instruction, IRPipelineChain):
        operand = ",".join(instruction.steps)
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            Instruction(OpCode.PIPELINE_CHAIN, operand),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRResultBind):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.result),
            Instruction(OpCode.RESULT_BIND, instruction.function_name),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRDataQuery):
        operand = f"{instruction.field},{instruction.predicate_function}"
        return (
            Instruction(OpCode.LOAD_NAME, instruction.container),
            Instruction(OpCode.DATA_QUERY, operand),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRRuleDecl):
        operand = f"{instruction.rule_id},{instruction.when_function},{instruction.then_function}"
        return (Instruction(OpCode.RULE_REGISTER, operand),)
    if isinstance(instruction, IRRuleInvoke):
        return (
            *_lower_value(instruction.context),
            Instruction(OpCode.RULE_INVOKE, instruction.rule_id),
            Instruction(OpCode.STORE_NAME, instruction.target),
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
    if isinstance(instruction, IRClassNew):
        items: list[Instruction] = [
            Instruction(OpCode.CLASS_NEW, instruction.class_name),
            Instruction(OpCode.STORE_NAME, instruction.target),
        ]
        meta = (_CLASS_METADATA or {}).get(instruction.class_name)
        if meta is not None and meta.mro:
            items.extend(
                (
                    Instruction(OpCode.LOAD_NAME, instruction.target),
                    Instruction(OpCode.PUSH_TEXT, ",".join(meta.mro)),
                    Instruction(OpCode.PUSH_TEXT, "__mro__"),
                    Instruction(OpCode.RECORD_SET),
                    Instruction(OpCode.STORE_NAME, instruction.target),
                )
            )
        items.append(Instruction(OpCode.LOAD_NAME, instruction.target))
        for arg in instruction.args:
            items.extend(_lower_value(arg))
        items.append(Instruction(OpCode.PUSH_INT, len(instruction.args)))
        items.append(Instruction(OpCode.METHOD_CALL, "__init__"))
        items.append(Instruction(OpCode.POP))
        return tuple(items)
    if isinstance(instruction, IRMethodCall):
        if instruction.static_dispatch:
            from .oop import method_symbol

            symbol = _resolve_function_symbol(
                method_symbol(instruction.static_dispatch, instruction.method),
                arity=1 + len(instruction.args),
            )
            return (
                Instruction(OpCode.LOAD_NAME, instruction.receiver),
                *tuple(item for arg in instruction.args for item in _lower_value(arg)),
                Instruction(OpCode.CALL, symbol),
                Instruction(OpCode.STORE_NAME, instruction.target),
            )
        return (
            Instruction(OpCode.LOAD_NAME, instruction.receiver),
            *tuple(item for arg in instruction.args for item in _lower_value(arg)),
            Instruction(OpCode.PUSH_INT, len(instruction.args)),
            Instruction(OpCode.METHOD_CALL, instruction.method),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRStaticMethodCall):
        from .oop import method_symbol

        symbol = _resolve_function_symbol(
            method_symbol(instruction.class_name, instruction.method, static=True),
            arity=len(instruction.args),
        )
        return (
            *tuple(item for arg in instruction.args for item in _lower_value(arg)),
            Instruction(OpCode.CALL, symbol),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRClassMethodCall):
        from .oop import method_symbol

        symbol = _resolve_function_symbol(
            method_symbol(instruction.class_name, instruction.method),
            arity=1 + len(instruction.args),
        )
        return (
            Instruction(OpCode.PUSH_TEXT, instruction.class_name),
            *tuple(item for arg in instruction.args for item in _lower_value(arg)),
            Instruction(OpCode.CALL, symbol),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRPropertyGet):
        from .oop import method_symbol

        getter_method = f"get_{instruction.property_name}"
        receiver_class = None
        if _COMPILE_PROGRAM is not None:
            for decl in _COMPILE_PROGRAM.classes:
                if instruction.property_name in decl.computed_properties:
                    receiver_class = decl.name
                    break
        symbol_base = (
            method_symbol(receiver_class, getter_method) if receiver_class else getter_method
        )
        symbol = _resolve_function_symbol(symbol_base, arity=1)
        return (
            Instruction(OpCode.LOAD_NAME, instruction.receiver),
            Instruction(OpCode.CALL, symbol),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRInstanceFinalize):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.receiver),
            Instruction(OpCode.PUSH_INT, 0),
            Instruction(OpCode.METHOD_CALL, "__finalize__"),
        )
    if isinstance(instruction, IRClassReflect):
        return (
            Instruction(OpCode.LOAD_NAME, instruction.receiver),
            Instruction(OpCode.PUSH_TEXT, "__class__"),
            Instruction(OpCode.RECORD_GET),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRMethodReflect):
        return (
            Instruction(OpCode.PUSH_TEXT, instruction.method),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRCall):
        items = [item for arg in instruction.args for item in _lower_value(arg)]
        opcode = OpCode.TAIL_CALL if instruction.tail else OpCode.CALL
        items.append(Instruction(opcode, instruction.target))
        if not instruction.tail:
            items.append(Instruction(OpCode.POP))
        return tuple(items)
    if isinstance(instruction, IRReturn):
        if instruction.tail:
            return ()
        if instruction.value is None:
            return (Instruction(OpCode.PUSH_INT, 0), Instruction(OpCode.RETURN))
        return (*_lower_value(instruction.value), Instruction(OpCode.RETURN))
    if isinstance(instruction, IRUnsafeEnter):
        return (Instruction(OpCode.UNSAFE_ENTER),)
    if isinstance(instruction, IRUnsafeExit):
        return (Instruction(OpCode.UNSAFE_EXIT),)
    if isinstance(instruction, IRHeapAlloc):
        return (
            *_lower_value(instruction.size),
            Instruction(OpCode.HEAP_ALLOC),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRHeapStore):
        return (
            *_lower_value(instruction.address),
            *_lower_value(instruction.value),
            Instruction(OpCode.HEAP_STORE),
        )
    if isinstance(instruction, IRHeapLoad):
        return (
            *_lower_value(instruction.address),
            Instruction(OpCode.HEAP_LOAD),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRHeapFree):
        return (*_lower_value(instruction.address), Instruction(OpCode.HEAP_FREE))
    if isinstance(instruction, IRIf):
        return _lower_if(instruction, lowerer)
    if isinstance(instruction, IRWhile):
        return _lower_while(instruction, lowerer)
    if isinstance(instruction, IRUntil):
        return _lower_until(instruction, lowerer)
    if isinstance(instruction, IRCountedFor):
        return _lower_counted_for(instruction, lowerer)
    if isinstance(instruction, IRForEach):
        return _lower_foreach(instruction, lowerer)
    if isinstance(instruction, IRInfiniteLoop):
        return _lower_infinite(instruction, lowerer)
    if isinstance(instruction, (IRBreak, IRContinue)):
        return ()
    if isinstance(instruction, IRAssert):
        return _lower_assert(instruction, lowerer)
    if isinstance(instruction, IRMatch):
        return _lower_match(instruction, lowerer)
    if isinstance(instruction, IRDefer):
        return ()
    if isinstance(instruction, IRPropagate):
        return _lower_propagate(instruction)
    if isinstance(instruction, IRPhase3Opcode):
        try:
            opcode = OpCode(instruction.opcode)
        except ValueError as exc:
            raise RuntimeSanskriptError(f"Unknown Phase 3 opcode: {instruction.opcode!r}") from exc
        if instruction.operand is None:
            return (Instruction(opcode),)
        return (Instruction(opcode, instruction.operand),)
    if isinstance(instruction, IRPhase3Bind):
        return (
            *_lower_phase3_value_ops(
                IRPhase3Value(
                    instruction.opcode,
                    instruction.operand,
                    instruction.value,
                    instruction.items,
                )
            ),
            Instruction(OpCode.STORE_NAME, instruction.target),
        )
    if isinstance(instruction, IRThrow):
        return (*_lower_value(instruction.message), Instruction(OpCode.THROW))
    if isinstance(instruction, IRPanic):
        return (*_lower_value(instruction.message), Instruction(OpCode.PANIC))
    if isinstance(instruction, IRCondAssert):
        target = lowerer if lowerer is not None else _Lowerer()
        lowerer_start = len(target.instructions)
        target.extend(_lower_condition(instruction.condition))
        jump_true = target.emit(OpCode.JUMP_IF_ZERO, 0)  # if FALSE (0), jump to panic
        skip_panic = target.emit(OpCode.JUMP, 0)          # if TRUE, skip to end
        panic_ip = len(target.instructions)
        target.patch(jump_true, panic_ip)
        target.emit(OpCode.PUSH_TEXT, instruction.message)
        target.emit(OpCode.PANIC)
        end_ip = len(target.instructions)
        target.patch(skip_panic, end_ip)
        return tuple(target.instructions[lowerer_start:])
    if isinstance(instruction, IRTryCatch):
        return _lower_try_catch(instruction, lowerer)
    if isinstance(instruction, IRForEachDestructure):
        return _lower_foreach_destructure(instruction, lowerer)
    raise RuntimeSanskriptError(f"Cannot lower unknown IR instruction: {instruction!r}")


def _emit_branch_pad(lowerer: _Lowerer) -> int:
    """Landing pad so forward jumps target real instructions in the returned stream."""
    index = len(lowerer.instructions)
    lowerer.emit(OpCode.PUSH_INT, 0)
    lowerer.emit(OpCode.POP)
    return index


def _lower_if(instruction: IRIf, parent: _Lowerer | None = None) -> tuple[Instruction, ...]:
    lowerer = parent if parent is not None else _Lowerer()
    start_index = len(lowerer.instructions)
    branches = [(instruction.condition, instruction.then_body)]
    branches.extend(instruction.elif_branches)
    else_body = instruction.else_body
    end_patches: list[int] = []
    for index, (condition, body) in enumerate(branches):
        lowerer.extend(_lower_condition(condition))
        jump_false = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
        _lower_block(lowerer, body)
        end_patches.append(lowerer.emit(OpCode.JUMP, 0))
        next_start = len(lowerer.instructions)
        lowerer.patch(jump_false, next_start)
        if index == len(branches) - 1 and not else_body:
            break
    if else_body:
        _lower_block(lowerer, else_body)
    end_label = _emit_branch_pad(lowerer)
    for patch_index in end_patches:
        lowerer.patch(patch_index, end_label)
    return tuple(lowerer.instructions[start_index:])


def _enter_loop(lowerer: _Lowerer, *, label: str | None = None) -> _LoopContext:
    ctx = _LoopContext(start_ip=len(lowerer.instructions), break_patches=[], label=label)
    lowerer._loop_stack.append(ctx)
    return ctx


def _exit_loop(lowerer: _Lowerer, ctx: _LoopContext) -> int:
    exit_label = _emit_branch_pad(lowerer)
    for patch_index in ctx.break_patches:
        lowerer.patch(patch_index, exit_label)
    lowerer._loop_stack.pop()
    return exit_label


def _lower_while(instruction: IRWhile, parent: _Lowerer | None = None) -> tuple[Instruction, ...]:
    lowerer = parent if parent is not None else _Lowerer()
    start_index = len(lowerer.instructions)
    ctx = _enter_loop(lowerer, label=instruction.label)
    loop_start = len(lowerer.instructions)
    ctx.start_ip = loop_start
    lowerer.extend(_lower_condition(instruction.condition))
    jump_exit = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
    _lower_block(lowerer, instruction.body)
    lowerer.emit(OpCode.JUMP, loop_start)
    exit_label = _exit_loop(lowerer, ctx)
    lowerer.patch(jump_exit, exit_label)
    return tuple(lowerer.instructions[start_index:])


def _resolve_loop(lowerer: _Lowerer, label: str | None) -> _LoopContext:
    if not lowerer._loop_stack:
        raise RuntimeSanskriptError("break/continue outside loop")
    if label is None:
        return lowerer._loop_stack[-1]
    for ctx in reversed(lowerer._loop_stack):
        if ctx.label == label:
            return ctx
    raise RuntimeSanskriptError(f"No loop with label {label!r}")


def _lower_until(instruction: IRUntil, parent: _Lowerer | None = None) -> tuple[Instruction, ...]:
    lowerer = parent if parent is not None else _Lowerer()
    start = len(lowerer.instructions)
    ctx = _enter_loop(lowerer, label=instruction.label)
    loop_start = len(lowerer.instructions)
    ctx.start_ip = loop_start
    lowerer.extend(_lower_condition(instruction.condition))
    skip_exit = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
    ctx.break_patches.append(lowerer.emit(OpCode.JUMP, 0))
    lowerer.patch(skip_exit, len(lowerer.instructions))
    _lower_block(lowerer, instruction.body)
    lowerer.emit(OpCode.JUMP, loop_start)
    exit_label = _exit_loop(lowerer, ctx)
    return tuple(lowerer.instructions[start:])


def _lower_counted_for(instruction: IRCountedFor, parent: _Lowerer | None = None) -> tuple[Instruction, ...]:
    lowerer = parent if parent is not None else _Lowerer()
    start = len(lowerer.instructions)
    lowerer.extend(_lower_value(instruction.start))
    lowerer.instructions.append(Instruction(OpCode.STORE_NAME, instruction.counter))
    ctx = _enter_loop(lowerer, label=instruction.label)
    loop_start = len(lowerer.instructions)
    ctx.start_ip = loop_start
    lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, instruction.counter))
    lowerer.extend(_lower_value(instruction.end))
    lowerer.instructions.append(Instruction(OpCode.COMPARE_LT))
    jump_exit = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
    _lower_block(lowerer, instruction.body)
    lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, instruction.counter))
    lowerer.instructions.append(Instruction(OpCode.PUSH_INT, 1))
    lowerer.instructions.append(Instruction(OpCode.ADD))
    lowerer.instructions.append(Instruction(OpCode.STORE_NAME, instruction.counter))
    lowerer.emit(OpCode.JUMP, loop_start)
    exit_label = _exit_loop(lowerer, ctx)
    lowerer.patch(jump_exit, exit_label)
    return tuple(lowerer.instructions[start:])


def _lower_foreach(instruction: IRForEach, parent: _Lowerer | None = None) -> tuple[Instruction, ...]:
    index_name = f"__idx_{instruction.item}"
    lowerer = parent if parent is not None else _Lowerer()
    start = len(lowerer.instructions)
    lowerer.instructions.append(Instruction(OpCode.PUSH_INT, 0))
    lowerer.instructions.append(Instruction(OpCode.STORE_NAME, index_name))
    ctx = _enter_loop(lowerer, label=instruction.label)
    loop_start = len(lowerer.instructions)
    ctx.start_ip = loop_start
    lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, index_name))
    lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, instruction.container))
    lowerer.instructions.append(Instruction(OpCode.LIST_LEN))
    lowerer.instructions.append(Instruction(OpCode.COMPARE_LT))
    jump_exit = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
    lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, instruction.container))
    lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, index_name))
    lowerer.instructions.append(Instruction(OpCode.LIST_GET))
    lowerer.instructions.append(Instruction(OpCode.STORE_NAME, instruction.item))
    _lower_block(lowerer, instruction.body)
    lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, index_name))
    lowerer.instructions.append(Instruction(OpCode.PUSH_INT, 1))
    lowerer.instructions.append(Instruction(OpCode.ADD))
    lowerer.instructions.append(Instruction(OpCode.STORE_NAME, index_name))
    lowerer.emit(OpCode.JUMP, loop_start)
    exit_label = _exit_loop(lowerer, ctx)
    lowerer.patch(jump_exit, exit_label)
    return tuple(lowerer.instructions[start:])


def _lower_infinite(instruction: IRInfiniteLoop, parent: _Lowerer | None = None) -> tuple[Instruction, ...]:
    lowerer = parent if parent is not None else _Lowerer()
    start = len(lowerer.instructions)
    ctx = _enter_loop(lowerer, label=instruction.label)
    loop_start = len(lowerer.instructions)
    ctx.start_ip = loop_start
    _lower_block(lowerer, instruction.body)
    lowerer.emit(OpCode.JUMP, loop_start)
    _exit_loop(lowerer, ctx)
    return tuple(lowerer.instructions[start:])


def _lower_assert(instruction: IRAssert, parent: _Lowerer | None = None) -> tuple[Instruction, ...]:
    target = parent if parent is not None else _Lowerer()
    start = len(target.instructions)
    target.extend(_lower_condition(instruction.condition))
    # JUMP_IF_ZERO pops the condition value; jump to panic block on failure.
    jump_panic = target.emit(OpCode.JUMP_IF_ZERO, 0)
    # Condition passed: skip panic block.
    skip_panic = target.emit(OpCode.JUMP, 0)
    panic_ip = len(target.instructions)
    target.patch(jump_panic, panic_ip)
    if instruction.message is None:
        target.emit(OpCode.PUSH_TEXT, "assertion failed")
    else:
        target.extend(_lower_value(instruction.message))
    target.emit(OpCode.PANIC)
    end_ip = len(target.instructions)
    target.patch(skip_panic, end_ip)
    return tuple(target.instructions[start:])


def _lower_match(instruction: IRMatch, parent: _Lowerer | None = None) -> tuple[Instruction, ...]:
    lowerer = parent if parent is not None else _Lowerer()
    start = len(lowerer.instructions)
    lowerer.extend(_lower_value(instruction.subject))
    subject_temp = "__match_subject"
    lowerer.instructions.append(Instruction(OpCode.STORE_NAME, subject_temp))
    end_patches: list[int] = []
    for pattern, body in instruction.arms:
        lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, subject_temp))
        from .ast import PatternLiteral, PatternWildcard

        if isinstance(pattern, PatternWildcard):
            lowerer.instructions.append(Instruction(OpCode.PUSH_INT, 1))
        elif isinstance(pattern, PatternLiteral):
            lowerer.extend(_lower_value(_compile_value_to_ir(pattern.value)))
            lowerer.instructions.append(Instruction(OpCode.MATCH_EQ))
        else:
            lowerer.instructions.append(Instruction(OpCode.PUSH_INT, 1))
        jump_next = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
        _lower_block(lowerer, body)
        end_patches.append(lowerer.emit(OpCode.JUMP, 0))
        lowerer.patch(jump_next, len(lowerer.instructions))
    end_label = _emit_branch_pad(lowerer)
    for patch_index in end_patches:
        lowerer.patch(patch_index, end_label)
    return tuple(lowerer.instructions[start:])


def _lower_propagate(instruction: IRPropagate) -> tuple[Instruction, ...]:
    lowerer = _Lowerer()
    lowerer.extend(_lower_value(instruction.value))
    lowerer.instructions.append(Instruction(OpCode.RESULT_IS_OK))
    jump_ok = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
    lowerer.instructions.append(Instruction(OpCode.RESULT_UNWRAP_ERR))
    lowerer.instructions.append(Instruction(OpCode.RETURN))
    lowerer.patch(jump_ok, len(lowerer.instructions))
    lowerer.instructions.append(Instruction(OpCode.RESULT_UNWRAP_OK))
    return tuple(lowerer.instructions)


def _lower_try_catch(instruction: IRTryCatch, parent: _Lowerer | None = None) -> tuple[Instruction, ...]:
    """Lower try-catch to a sentinel-based pattern using a special try_begin/try_end pseudo-protocol.

    Since the VM is Python, we use a dedicated TRY_BEGIN/TRY_END approach stored as labels.
    We encode: push sentinel, body, try_end jump, handler_start, store error_name, handler_body, end.
    The VM catches ThrownError between try_begin and try_end positions stored in a try-stack.
    """
    lowerer = parent if parent is not None else _Lowerer()
    start = len(lowerer.instructions)
    # emit try_begin with operand = (will be patched to handler_ip)
    try_begin_idx = lowerer.emit(OpCode.TRY_BEGIN, 0)
    _lower_block(lowerer, instruction.body)
    skip_handler = lowerer.emit(OpCode.JUMP, 0)
    handler_start = len(lowerer.instructions)
    lowerer.patch(try_begin_idx, handler_start)
    lowerer.emit(OpCode.STORE_NAME, instruction.error_name)
    _lower_block(lowerer, instruction.handler)
    end_label = _emit_branch_pad(lowerer)
    lowerer.patch(skip_handler, end_label)
    lowerer.emit(OpCode.TRY_END)
    return tuple(lowerer.instructions[start:])


def _lower_foreach_destructure(instruction: IRForEachDestructure, parent: _Lowerer | None = None) -> tuple[Instruction, ...]:
    index_name = f"__idx_dst_{'_'.join(instruction.names)}"
    lowerer = parent if parent is not None else _Lowerer()
    start = len(lowerer.instructions)
    lowerer.instructions.append(Instruction(OpCode.PUSH_INT, 0))
    lowerer.instructions.append(Instruction(OpCode.STORE_NAME, index_name))
    ctx = _enter_loop(lowerer, label=instruction.label)
    loop_start = len(lowerer.instructions)
    ctx.start_ip = loop_start
    lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, index_name))
    lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, instruction.container))
    lowerer.instructions.append(Instruction(OpCode.LIST_LEN))
    lowerer.instructions.append(Instruction(OpCode.COMPARE_LT))
    jump_exit = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
    # Load the tuple item
    tuple_temp = f"__tup_dst_{'_'.join(instruction.names)}"
    lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, instruction.container))
    lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, index_name))
    lowerer.instructions.append(Instruction(OpCode.LIST_GET))
    lowerer.instructions.append(Instruction(OpCode.STORE_NAME, tuple_temp))
    # Destructure: bind each name to tuple element
    for i, name in enumerate(instruction.names):
        lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, tuple_temp))
        lowerer.instructions.append(Instruction(OpCode.TUPLE_GET, i))
        lowerer.instructions.append(Instruction(OpCode.STORE_NAME, name))
    _lower_block(lowerer, instruction.body)
    lowerer.instructions.append(Instruction(OpCode.LOAD_NAME, index_name))
    lowerer.instructions.append(Instruction(OpCode.PUSH_INT, 1))
    lowerer.instructions.append(Instruction(OpCode.ADD))
    lowerer.instructions.append(Instruction(OpCode.STORE_NAME, index_name))
    lowerer.emit(OpCode.JUMP, loop_start)
    exit_label = _exit_loop(lowerer, ctx)
    lowerer.patch(jump_exit, exit_label)
    return tuple(lowerer.instructions[start:])


def _lower_compare(condition: IRCompareEq | IRCompareLt | IRCompareNe | IRCompareGt | IRCompareLe | IRCompareIdentity | IRCompareMembership) -> tuple[Instruction, ...]:
    if isinstance(condition, IRCompareEq):
        opcode = OpCode.COMPARE_EQ
        return (*_lower_value(condition.left), *_lower_value(condition.right), Instruction(opcode))
    if isinstance(condition, IRCompareNe):
        return (*_lower_value(condition.left), *_lower_value(condition.right), Instruction(OpCode.COMPARE_NE))
    if isinstance(condition, IRCompareLt):
        return (*_lower_value(condition.left), *_lower_value(condition.right), Instruction(OpCode.COMPARE_LT))
    if isinstance(condition, IRCompareGt):
        return (*_lower_value(condition.left), *_lower_value(condition.right), Instruction(OpCode.COMPARE_GT))
    if isinstance(condition, IRCompareLe):
        return (*_lower_value(condition.left), *_lower_value(condition.right), Instruction(OpCode.COMPARE_LE))
    if isinstance(condition, IRCompareIdentity):
        return (*_lower_value(condition.left), *_lower_value(condition.right), Instruction(OpCode.COMPARE_IDENTITY))
    if isinstance(condition, IRCompareMembership):
        return (
            *_lower_value(condition.container),
            *_lower_value(condition.key),
            Instruction(OpCode.MAP_CONTAINS),
        )
    raise RuntimeSanskriptError(f"Cannot lower unknown comparison: {condition!r}")


def _lower_condition(condition: IRCondition) -> tuple[Instruction, ...]:
    if isinstance(condition, (IRCompareEq, IRCompareNe, IRCompareLt, IRCompareGt, IRCompareLe, IRCompareIdentity, IRCompareMembership)):
        return _lower_compare(condition)
    if isinstance(condition, IRBoolNotCond):
        lowerer = _Lowerer()
        lowerer.extend(_lower_condition(condition.operand))
        jump_was_truthy = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
        lowerer.emit(OpCode.PUSH_INT, 1)
        jump_end = lowerer.emit(OpCode.JUMP, 0)
        false_label = len(lowerer.instructions)
        lowerer.emit(OpCode.PUSH_INT, 0)
        end_label = len(lowerer.instructions)
        lowerer.patch(jump_was_truthy, false_label)
        lowerer.patch(jump_end, end_label)
        return tuple(lowerer.instructions)
    if isinstance(condition, IRBoolAndCond):
        return _lower_short_circuit_and(
            lambda: _lower_condition(condition.left),
            lambda: _lower_condition(condition.right),
        )
    if isinstance(condition, IRBoolOrCond):
        return _lower_short_circuit_or(
            lambda: _lower_condition(condition.left),
            lambda: _lower_condition(condition.right),
        )
    raise RuntimeSanskriptError(f"Cannot lower unknown condition: {condition!r}")


def _lower_short_circuit_and(left_fn, right_fn) -> tuple[Instruction, ...]:
    lowerer = _Lowerer()
    lowerer.extend(left_fn())
    jump_fail = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
    lowerer.extend(right_fn())
    jump_end = lowerer.emit(OpCode.JUMP, 0)
    fail_label = len(lowerer.instructions)
    lowerer.emit(OpCode.PUSH_INT, 0)
    end_label = len(lowerer.instructions)
    lowerer.patch(jump_fail, fail_label)
    lowerer.patch(jump_end, end_label)
    return tuple(lowerer.instructions)


def _lower_short_circuit_or(left_fn, right_fn) -> tuple[Instruction, ...]:
    lowerer = _Lowerer()
    lowerer.extend(left_fn())
    jump_true = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
    lowerer.emit(OpCode.PUSH_INT, 1)
    jump_end = lowerer.emit(OpCode.JUMP, 0)
    false_label = len(lowerer.instructions)
    lowerer.patch(jump_true, false_label)
    lowerer.extend(right_fn())
    end_label = len(lowerer.instructions)
    lowerer.patch(jump_end, end_label)
    return tuple(lowerer.instructions)


def _lower_value(value: IRValue) -> tuple[Instruction, ...]:
    if isinstance(value, IRLiteral):
        return (Instruction(OpCode.PUSH_INT, value.value),)
    if isinstance(value, IRFloatLiteral):
        return (Instruction(OpCode.PUSH_FLOAT, value.value),)
    if isinstance(value, IRBoolLiteral):
        return (Instruction(OpCode.PUSH_BOOL, 1 if value.value else 0),)
    if isinstance(value, IRTextLiteral):
        return (Instruction(OpCode.PUSH_TEXT, value.value),)
    if isinstance(value, IRNilLiteral):
        return (Instruction(OpCode.PUSH_NIL),)
    if isinstance(value, IRBytesLiteral):
        return (Instruction(OpCode.PUSH_BYTES, value.value.hex()),)
    if isinstance(value, IRGroupValue):
        return _lower_value(value.inner)
    if isinstance(value, IRBoolNot):
        lowerer = _Lowerer()
        lowerer.extend(_lower_value(value.operand))
        jump_truthy = lowerer.emit(OpCode.JUMP_IF_ZERO, 0)
        lowerer.emit(OpCode.PUSH_INT, 1)
        jump_end = lowerer.emit(OpCode.JUMP, 0)
        false_label = len(lowerer.instructions)
        lowerer.emit(OpCode.PUSH_INT, 0)
        end_label = len(lowerer.instructions)
        lowerer.patch(jump_truthy, false_label)
        lowerer.patch(jump_end, end_label)
        return tuple(lowerer.instructions)
    if isinstance(value, IRBoolAnd):
        return _lower_short_circuit_and(
            lambda: _lower_value(value.left),
            lambda: _lower_value(value.right),
        )
    if isinstance(value, IRBoolOr):
        return _lower_short_circuit_or(
            lambda: _lower_value(value.left),
            lambda: _lower_value(value.right),
        )
    if isinstance(value, IRListLiteral):
        items: list[Instruction] = [Instruction(OpCode.LIST_NEW)]
        for element in value.elements:
            items.extend(_lower_value(element))
            items.append(Instruction(OpCode.LIST_APPEND))
        return tuple(items)
    if isinstance(value, IRMapLiteral):
        items = [Instruction(OpCode.MAP_NEW)]
        for key, val in value.entries:
            items.extend(_lower_value(key))
            items.extend(_lower_value(val))
            items.append(Instruction(OpCode.MAP_SET))
        return tuple(items)
    if isinstance(value, IRReference):
        return (Instruction(OpCode.LOAD_NAME, value.name),)
    if isinstance(value, IRCallValue):
        return (
            *tuple(item for arg in value.args for item in _lower_value(arg)),
            Instruction(OpCode.CALL, value.target),
        )
    if isinstance(value, IRBinaryValue):
        try:
            opcode = _BINARY_OPCODES[value.operator]
        except KeyError as exc:
            raise RuntimeSanskriptError(f"Unknown binary value operator: {value.operator!r}") from exc
        return (*_lower_value(value.left), *_lower_value(value.right), Instruction(opcode))
    if isinstance(value, IRTupleLiteral):
        items: list[Instruction] = []
        for item in value.items:
            items.extend(_lower_value(item))
        items.append(Instruction(OpCode.TUPLE_NEW, len(value.items)))
        return tuple(items)
    if isinstance(value, IRPhase3Value):
        return _lower_phase3_value_ops(value)
    raise RuntimeSanskriptError(f"Cannot lower unknown IR value: {value!r}")


def _lower_phase3_value_ops(value: IRPhase3Value) -> tuple[Instruction, ...]:
    items: list[Instruction] = []
    if value.opcode == "option_none":
        items.append(Instruction(OpCode.OPTION_NONE))
        return tuple(items)
    if value.opcode == "option_some" and value.value is not None:
        items.extend(_lower_value(value.value))
        items.append(Instruction(OpCode.OPTION_SOME))
        return tuple(items)
    if value.opcode in {"result_ok", "result_err"} and value.value is not None:
        items.extend(_lower_value(value.value))
        items.append(Instruction(OpCode(value.opcode)))
        return tuple(items)
    if value.opcode == "tuple_new":
        for item in value.items:
            items.extend(_lower_value(item))
        items.append(Instruction(OpCode.TUPLE_NEW, value.operand))
        return tuple(items)
    if value.opcode == "set_new":
        items.append(Instruction(OpCode.SET_NEW))
        for item in value.items:
            items.extend(_lower_value(item))
            items.append(Instruction(OpCode.SET_ADD))
        return tuple(items)
    if value.opcode == "deque_new":
        items.append(Instruction(OpCode.DEQUE_NEW))
        return tuple(items)
    try:
        opcode = OpCode(value.opcode)
    except ValueError as exc:
        raise RuntimeSanskriptError(f"Unknown Phase 3 opcode: {value.opcode!r}") from exc
    if value.value is not None:
        items.extend(_lower_value(value.value))
    if value.operand is None:
        items.append(Instruction(opcode))
    else:
        items.append(Instruction(opcode, value.operand))
    return tuple(items)


def _ir_default_to_operand(value: IRValue | None):
    if value is None:
        return None
    if isinstance(value, IRLiteral):
        return value.value
    if isinstance(value, IRFloatLiteral):
        return value.value
    if isinstance(value, IRTextLiteral):
        return value.value
    if isinstance(value, IRBoolLiteral):
        return bool(value.value)
    if isinstance(value, IRNilLiteral):
        return None
    raise RuntimeSanskriptError("Default parameters currently support only literal defaults")


def _compile_statement_block(
    statements: tuple[Statement, ...],
    *,
    scope: ScopeStack,
    allow_rebind: bool = False,
) -> tuple[IRInstruction, ...]:
    items: list[IRInstruction] = []
    for statement in statements:
        if isinstance(statement, FunctionDef):
            continue
        items.extend(
            _compile_statement_to_ir(statement, scope=scope, allow_rebind=allow_rebind),
        )
    return tuple(items)


def _compile_statement_to_ir(
    statement: Statement,
    *,
    scope: ScopeStack,
    allow_rebind: bool = False,
) -> tuple[IRInstruction, ...]:
    if isinstance(statement, Phase3Bind):
        scope.declare(statement.target, immutable=True)
        return (
            IRPhase3Bind(
                statement.target,
                statement.opcode,
                statement.operand,
                _compile_value_to_ir(statement.value) if statement.value is not None else None,
                tuple(_compile_value_to_ir(item) for item in statement.items),
            ),
        )
    if isinstance(statement, Bind):
        if allow_rebind and scope.is_bound(statement.target):
            scope.assign(statement.target)
        else:
            scope.declare(statement.target, immutable=statement.immutable)
        return (IRStore(statement.target, _compile_value_to_ir(statement.value)),)
    if isinstance(statement, ForwardDecl):
        scope.declare(statement.target, forward=True)
        return ()
    if isinstance(statement, Block):
        scope.push()
        body = _compile_statement_block(statement.body, scope=scope)
        scope.pop()
        return (IRScopeEnter(), *body, IRScopeExit())
    if isinstance(statement, Assign):
        scope.assign(statement.target)
        if isinstance(statement.value, PartialApply):
            wrapper = _register_partial_wrapper(statement.value)
            return (
                IRPhase3Opcode("push_func", wrapper),
                IRPhase3Opcode("store_name", statement.target),
            )
        return (IRStore(statement.target, _compile_value_to_ir(statement.value)),)
    if isinstance(statement, Increase):
        scope.assign(statement.target)
        return (IRIncrease(statement.target, _compile_value_to_ir(statement.amount)),)
    if isinstance(statement, Decrease):
        scope.assign(statement.target)
        return (IRDecrease(statement.target, _compile_value_to_ir(statement.amount)),)
    if isinstance(statement, Multiply):
        scope.assign(statement.target)
        return (IRMultiply(statement.target, _compile_value_to_ir(statement.factor)),)
    if isinstance(statement, Display):
        return (IREmit(_compile_value_to_ir(statement.value)),)
    if isinstance(statement, Pop):
        return (IRPop(_compile_value_to_ir(statement.value)),)
    if isinstance(statement, TextConcat):
        return (
            IRTextConcat(
            statement.target,
            _compile_value_to_ir(statement.left),
            _compile_value_to_ir(statement.right),
            ),
        )
    if isinstance(statement, TextLength):
        return (IRTextLength(statement.target, _compile_value_to_ir(statement.text)),)
    if isinstance(statement, TextGet):
        return (
            IRTextGet(
            statement.target,
            _compile_value_to_ir(statement.text),
            _compile_value_to_ir(statement.index),
            ),
        )
    if isinstance(statement, TextSlice):
        return (
            IRTextSlice(
            statement.target,
            _compile_value_to_ir(statement.text),
            _compile_value_to_ir(statement.start),
            _compile_value_to_ir(statement.end),
            ),
        )
    if isinstance(statement, TextContains):
        return (
            IRTextContains(
            statement.target,
            _compile_value_to_ir(statement.text),
            _compile_value_to_ir(statement.needle),
            ),
        )
    if isinstance(statement, ListInit):
        scope.declare(statement.container)
        return (IRListInit(statement.container),)
    if isinstance(statement, MapInit):
        scope.declare(statement.container)
        return (IRMapInit(statement.container),)
    if isinstance(statement, ListAppend):
        return (IRListAppend(statement.container, _compile_value_to_ir(statement.item)),)
    if isinstance(statement, ListGet):
        return (
            IRListGet(
            statement.target,
            statement.container,
            _compile_value_to_ir(statement.index),
            ),
        )
    if isinstance(statement, ListLength):
        return (IRListLength(statement.target, statement.container),)
    if isinstance(statement, ListMap):
        return (IRListMap(statement.target, statement.container, statement.function_name),)
    if isinstance(statement, ListFilter):
        return (IRListFilter(statement.target, statement.container, statement.function_name),)
    if isinstance(statement, ListReduce):
        return (
            IRListReduce(
                statement.target,
                statement.container,
                statement.function_name,
                _compile_value_to_ir(statement.initial),
            ),
        )
    if isinstance(statement, ListAll):
        return (IRListAll(statement.target, statement.container, statement.function_name),)
    if isinstance(statement, ListScan):
        return (
            IRListScan(
                statement.target,
                statement.container,
                statement.function_name,
                _compile_value_to_ir(statement.initial),
            ),
        )
    if isinstance(statement, ListZip):
        scope.declare(statement.target)
        return (IRListZip(statement.target, statement.left, statement.right),)
    if isinstance(statement, ListEnumerate):
        scope.declare(statement.target)
        return (IRListEnumerate(statement.target, statement.container),)
    if isinstance(statement, ListAny):
        scope.declare(statement.target)
        return (IRListAny(statement.target, statement.container, statement.function_name),)
    if isinstance(statement, ImmutableListInit):
        scope.declare(statement.container)
        return (IRImmutableListInit(statement.container),)
    if isinstance(statement, ImmutableListAppend):
        scope.declare(statement.target)
        return (
            IRImmutableListAppend(
                statement.target,
                statement.container,
                _compile_value_to_ir(statement.item),
            ),
        )
    if isinstance(statement, ListComprehension):
        scope.declare(statement.target)
        return (
            IRListComprehension(
                statement.target,
                statement.container,
                statement.where_function,
                statement.with_function,
            ),
        )
    if isinstance(statement, LazyIterNew):
        scope.declare(statement.target)
        return (IRLazyIterNew(statement.target, statement.container),)
    if isinstance(statement, LazyIterNext):
        scope.declare(statement.has_more)
        scope.declare(statement.value)
        return (IRLazyIterNext(statement.has_more, statement.value, statement.iterator),)
    if isinstance(statement, GeneratorNew):
        scope.declare(statement.target)
        return (IRGeneratorNew(statement.target, statement.function_name),)
    if isinstance(statement, GeneratorNext):
        scope.declare(statement.has_more)
        scope.declare(statement.value)
        return (IRGeneratorNext(statement.has_more, statement.value, statement.generator),)
    if isinstance(statement, Yield):
        return (IRYield(_compile_value_to_ir(statement.value)),)
    if isinstance(statement, PipelineChain):
        scope.declare(statement.target)
        return (IRPipelineChain(statement.target, statement.container, statement.steps),)
    if isinstance(statement, MatchExpr):
        scope.declare(statement.target)
        return (
            IRMatch(
                _compile_value_to_ir(statement.subject),
                tuple((arm.pattern, _compile_statement_block(arm.body, scope=scope)) for arm in statement.arms),
            ),
        )
    if isinstance(statement, ResultBind):
        scope.declare(statement.target)
        return (IRResultBind(statement.target, statement.result, statement.function_name),)
    if isinstance(statement, DataQuery):
        scope.declare(statement.target)
        return (
            IRDataQuery(
                statement.target,
                statement.container,
                statement.field,
                statement.predicate_function,
            ),
        )
    if isinstance(statement, RuleInvoke):
        scope.declare(statement.target)
        return (
            IRRuleInvoke(
                statement.target,
                statement.rule_id,
                _compile_value_to_ir(statement.context),
            ),
        )
    if isinstance(statement, MapPut):
        return (
            IRMapPut(
            statement.container,
            _compile_value_to_ir(statement.key),
            _compile_value_to_ir(statement.value),
            ),
        )
    if isinstance(statement, MapGet):
        return (
            IRMapGet(
            statement.target,
            statement.container,
            _compile_value_to_ir(statement.key),
            ),
        )
    if isinstance(statement, MapContains):
        return (
            IRMapContains(
            statement.target,
            statement.container,
            _compile_value_to_ir(statement.key),
            ),
        )
    if isinstance(statement, RecordInit):
        scope.declare(statement.record)
        return (IRRecordInit(statement.record),)
    if isinstance(statement, FieldSet):
        return (
            IRFieldSet(
            statement.record,
            _compile_value_to_ir(statement.field),
            _compile_value_to_ir(statement.value),
            ),
        )
    if isinstance(statement, FieldGet):
        return (
            IRFieldGet(
            statement.target,
            statement.record,
            _compile_value_to_ir(statement.field),
            ),
        )
    if isinstance(statement, FieldContains):
        return (
            IRFieldContains(
            statement.target,
            statement.record,
            _compile_value_to_ir(statement.field),
            ),
        )
    if isinstance(statement, ClassNew):
        scope.declare(statement.target)
        return (
            IRClassNew(
                statement.target,
                statement.class_name,
                tuple(_compile_value_to_ir(arg) for arg in statement.args),
            ),
        )
    if isinstance(statement, MethodCall):
        scope.declare(statement.target)
        return (
            IRMethodCall(
                statement.target,
                statement.receiver,
                statement.method,
                tuple(_compile_value_to_ir(arg) for arg in statement.args),
                static_dispatch=statement.static_dispatch_class,
            ),
        )
    if isinstance(statement, StaticMethodCall):
        scope.declare(statement.target)
        return (
            IRStaticMethodCall(
                statement.target,
                statement.class_name,
                statement.method,
                tuple(_compile_value_to_ir(arg) for arg in statement.args),
            ),
        )
    if isinstance(statement, ClassMethodCall):
        scope.declare(statement.target)
        return (
            IRClassMethodCall(
                statement.target,
                statement.class_name,
                statement.method,
                tuple(_compile_value_to_ir(arg) for arg in statement.args),
            ),
        )
    if isinstance(statement, PropertyGet):
        scope.declare(statement.target)
        return (IRPropertyGet(statement.target, statement.receiver, statement.property_name),)
    if isinstance(statement, InstanceFinalize):
        return (IRInstanceFinalize(statement.receiver),)
    if isinstance(statement, ClassReflect):
        scope.declare(statement.target)
        return (IRClassReflect(statement.target, statement.receiver),)
    if isinstance(statement, MethodReflect):
        scope.declare(statement.target)
        return (IRMethodReflect(statement.target, statement.method),)
    if isinstance(statement, If):
        return (
            IRIf(
                _compile_condition_to_ir(statement.condition),
                _compile_statement_block(statement.then_body, scope=scope),
                _compile_statement_block(statement.else_body, scope=scope),
                tuple(
                    (
                        _compile_condition_to_ir(condition),
                        _compile_statement_block(body, scope=scope),
                    )
                    for condition, body in statement.elif_branches
                ),
            ),
        )
    if isinstance(statement, While):
        return (
            IRWhile(
                _compile_condition_to_ir(statement.condition),
                _compile_statement_block(statement.body, scope=scope, allow_rebind=True),
                label=statement.label,
            ),
        )
    if isinstance(statement, Until):
        return (
            IRUntil(
                _compile_condition_to_ir(statement.condition),
                _compile_statement_block(statement.body, scope=scope, allow_rebind=True),
                label=statement.label,
            ),
        )
    if isinstance(statement, CountedFor):
        return (
            IRCountedFor(
                statement.counter,
                _compile_value_to_ir(statement.start),
                _compile_value_to_ir(statement.end),
                _compile_statement_block(statement.body, scope=scope, allow_rebind=True),
                label=statement.label,
            ),
        )
    if isinstance(statement, ForEach):
        scope.declare(statement.item)
        return (
            IRForEach(
                statement.item,
                statement.container,
                _compile_statement_block(statement.body, scope=scope, allow_rebind=True),
                label=statement.label,
            ),
        )
    if isinstance(statement, InfiniteLoop):
        return (
            IRInfiniteLoop(
                _compile_statement_block(statement.body, scope=scope, allow_rebind=True),
                label=statement.label,
            ),
        )
    if isinstance(statement, Break):
        return (IRBreak(statement.label),)
    if isinstance(statement, Continue):
        return (IRContinue(statement.label),)
    if isinstance(statement, Assert):
        return (
            IRAssert(
                _compile_condition_to_ir(statement.condition),
                None if statement.message is None else _compile_value_to_ir(statement.message),
            ),
        )
    if isinstance(statement, Match):
        return (
            IRMatch(
                _compile_value_to_ir(statement.subject),
                tuple((arm.pattern, _compile_statement_block(arm.body, scope=scope)) for arm in statement.arms),
            ),
        )
    if isinstance(statement, Defer):
        return _compile_statement_block(statement.body, scope=scope)
    if isinstance(statement, Propagate):
        return (IRPropagate(_compile_value_to_ir(statement.value)),)
    if isinstance(statement, TypeConvert):
        scope.declare(statement.target)
        value_ir = _compile_value_to_ir(statement.value)
        if statement.to_type == "bytes" and isinstance(statement.value, TextLiteral):
            encoded = statement.value.value.encode("utf-8")
            return (
                IRStore(statement.target, IRBytesLiteral(encoded)),
            )
        if statement.to_type == "text" and isinstance(statement.value, BytesLiteral):
            decoded = statement.value.value.decode("utf-8", errors="replace")
            return (
                IRStore(statement.target, IRTextLiteral(decoded)),
            )
        return (IRStore(statement.target, value_ir),)
    if isinstance(statement, TypeReflect):
        scope.declare(statement.target)
        return (IRStore(statement.target, IRTextLiteral(statement.type_name)),)
    if isinstance(
        statement,
        (
            TypeAliasDecl,
            NewtypeDecl,
            RecordTypeDecl,
            ConstDecl,
        ),
    ):
        return ()
    if isinstance(statement, Call):
        resolved = _resolve_compile_target(statement.name, arity=len(statement.args) + len(statement.kwargs))
        target = qualified_function_name(statement.module, resolved)
        inline_fn = _find_inline_function(resolved, statement.module)
        if inline_fn is not None and _PROGRAM_SAFETY_TIER == "rakshita":
            return _inline_call_instructions(inline_fn, statement)
        macro_fn = _find_compile_time_function(resolved)
        if macro_fn is not None:
            return _expand_macro_call(macro_fn, statement)
        ordered = _order_call_arguments(resolved, statement.args, statement.kwargs)
        return (IRCall(target, tuple(_compile_value_to_ir(arg) for arg in ordered)),)
    if isinstance(statement, Return):
        if isinstance(statement.value, CallValue):
            resolved = _resolve_compile_target(
                statement.value.name,
                arity=len(statement.value.args) + len(statement.value.kwargs),
            )
            target = qualified_function_name(statement.value.module, resolved)
            tail = _CURRENT_FN_KEY is not None and (
                target == _CURRENT_FN_KEY
                or (
                    target.endswith(f".{resolved}")
                    and _CURRENT_FN_KEY.endswith(f".{resolved}")
                )
            )
            if tail:
                ordered = _order_call_arguments(
                    resolved,
                    statement.value.args,
                    statement.value.kwargs,
                )
                ir_args = tuple(_compile_value_to_ir(arg) for arg in ordered)
                return (IRCall(target, ir_args, tail=True),)
        value = None if statement.value is None else _compile_value_to_ir(statement.value)
        return (IRReturn(value, name=statement.name),)
    if isinstance(statement, UnsafeEnter):
        return (IRUnsafeEnter(),)
    if isinstance(statement, UnsafeExit):
        return (IRUnsafeExit(),)
    if isinstance(statement, HeapAlloc):
        scope.declare(statement.target)
        return (IRHeapAlloc(statement.target, _compile_value_to_ir(statement.size)),)
    if isinstance(statement, HeapStore):
        return (
            IRHeapStore(
                _compile_value_to_ir(statement.address),
                _compile_value_to_ir(statement.value),
            ),
        )
    if isinstance(statement, HeapLoad):
        return (IRHeapLoad(statement.target, _compile_value_to_ir(statement.address)),)
    if isinstance(statement, HeapFree):
        return (IRHeapFree(_compile_value_to_ir(statement.address)),)
    if isinstance(statement, Throw):
        return (IRThrow(_compile_value_to_ir(statement.message)),)
    if isinstance(statement, Panic):
        return (IRPanic(_compile_value_to_ir(statement.message)),)
    if isinstance(statement, TryCatch):
        return (
            IRTryCatch(
                _compile_statement_block(statement.body, scope=scope),
                statement.error_name,
                _compile_statement_block(statement.handler, scope=scope),
            ),
        )
    if isinstance(statement, PreCondition):
        return (IRCondAssert(_compile_condition_to_ir(statement.condition), "precondition failed"),)
    if isinstance(statement, PostCondition):
        return (IRCondAssert(_compile_condition_to_ir(statement.condition), "postcondition failed"),)
    if isinstance(statement, Invariant):
        return (IRCondAssert(_compile_condition_to_ir(statement.condition), "invariant failed"),)
    if isinstance(statement, ForEachDestructure):
        for name in statement.names:
            scope.declare(name)
        return (
            IRForEachDestructure(
                statement.names,
                statement.container,
                _compile_statement_block(statement.body, scope=scope, allow_rebind=True),
                label=statement.label,
            ),
        )
    raise RuntimeSanskriptError(f"Cannot compile unknown statement: {statement!r}")


def _compile_condition_to_ir(condition: Condition) -> IRCondition:
    if isinstance(condition, CompareEq):
        return IRCompareEq(
            _compile_value_to_ir(condition.left),
            _compile_value_to_ir(condition.right),
        )
    if isinstance(condition, CompareNe):
        return IRCompareNe(
            _compile_value_to_ir(condition.left),
            _compile_value_to_ir(condition.right),
        )
    if isinstance(condition, CompareLt):
        return IRCompareLt(
            _compile_value_to_ir(condition.left),
            _compile_value_to_ir(condition.right),
        )
    if isinstance(condition, CompareGt):
        return IRCompareGt(
            _compile_value_to_ir(condition.left),
            _compile_value_to_ir(condition.right),
        )
    if isinstance(condition, CompareLe):
        return IRCompareLe(
            _compile_value_to_ir(condition.left),
            _compile_value_to_ir(condition.right),
        )
    if isinstance(condition, CompareIdentity):
        return IRCompareIdentity(
            _compile_value_to_ir(condition.left),
            _compile_value_to_ir(condition.right),
        )
    if isinstance(condition, CompareMembership):
        return IRCompareMembership(
            _compile_value_to_ir(condition.container),
            _compile_value_to_ir(condition.key),
        )
    if isinstance(condition, BoolNotCond):
        return IRBoolNotCond(_compile_condition_to_ir(condition.operand))
    if isinstance(condition, BoolAndCond):
        return IRBoolAndCond(
            _compile_condition_to_ir(condition.left),
            _compile_condition_to_ir(condition.right),
        )
    if isinstance(condition, BoolOrCond):
        return IRBoolOrCond(
            _compile_condition_to_ir(condition.left),
            _compile_condition_to_ir(condition.right),
        )
    raise RuntimeSanskriptError(f"Cannot compile unknown condition: {condition!r}")


def _compile_value_to_ir(value: Value) -> IRValue:
    if isinstance(value, Literal):
        return IRLiteral(value.value)
    if isinstance(value, FloatLiteral):
        return IRFloatLiteral(value.value)
    if isinstance(value, BoolLiteral):
        return IRBoolLiteral(value.value)
    if isinstance(value, TextLiteral):
        return IRTextLiteral(value.value)
    if isinstance(value, NilLiteral):
        return IRNilLiteral()
    if isinstance(value, BytesLiteral):
        return IRBytesLiteral(value.value)
    if isinstance(value, GroupValue):
        return IRGroupValue(_compile_value_to_ir(value.inner))
    if isinstance(value, BoolNot):
        return IRBoolNot(_compile_value_to_ir(value.operand))
    if isinstance(value, BoolAnd):
        return IRBoolAnd(
            _compile_value_to_ir(value.left),
            _compile_value_to_ir(value.right),
        )
    if isinstance(value, BoolOr):
        return IRBoolOr(
            _compile_value_to_ir(value.left),
            _compile_value_to_ir(value.right),
        )
    if isinstance(value, ListLiteral):
        return IRListLiteral(tuple(_compile_value_to_ir(item) for item in value.elements))
    if isinstance(value, MapLiteral):
        return IRMapLiteral(
            tuple(
                (_compile_value_to_ir(key), _compile_value_to_ir(val))
                for key, val in value.entries
            )
        )
    if isinstance(value, Reference):
        return IRReference(value.name)
    if isinstance(value, PartialApply):
        return _compile_partial_apply_value(value)
    if isinstance(value, CallValue):
        resolved = _resolve_compile_target(
            value.name,
            arity=len(value.args) + len(value.kwargs),
        )
        target = qualified_function_name(value.module, resolved)
        ordered = _order_call_arguments(value.name, value.args, value.kwargs)
        return IRCallValue(target, tuple(_compile_value_to_ir(arg) for arg in ordered))
    if isinstance(value, BinaryValue):
        return IRBinaryValue(
            value.operator,
            _compile_value_to_ir(value.left),
            _compile_value_to_ir(value.right),
        )
    if isinstance(value, TupleLiteral):
        return IRTupleLiteral(tuple(_compile_value_to_ir(item) for item in value.items))
    if isinstance(value, NoneValue):
        return IRPhase3Value("option_none")
    if isinstance(value, SomeValue):
        return IRPhase3Value("option_some", value=_compile_value_to_ir(value.inner))
    raise RuntimeSanskriptError(f"Cannot compile unknown value: {value!r}")


def _register_partial_wrapper(value: PartialApply) -> str:
    if isinstance(value.callable, Reference):
        target_name = value.callable.name
        target_module = None
    elif isinstance(value.callable, CallValue):
        target_name = value.callable.name
        target_module = value.callable.module
    else:
        raise CompileError("Partial application requires a named function reference")
    base_fn = _find_function_def(target_name)
    if base_fn is None:
        raise CompileError(f"Unknown function for partial application: {target_name!r}")
    bind_count = 1 if value.curry else len(value.args)
    bind_count = min(bind_count, len(base_fn.params))
    remaining_params = base_fn.params[bind_count:]
    wrapper_name = f"__partial__{target_name}__{len(_NESTED_IR_FUNCTIONS)}"
    call_args = list(value.args[:bind_count]) + [Reference(p) for p in remaining_params]
    inner_call = CallValue(
        target_name,
        module=target_module,
        args=tuple(call_args),
        kwargs=value.kwargs,
    )
    wrapper_body = (Return(inner_call),)
    _NESTED_IR_FUNCTIONS.append(
        IRFunction(
            wrapper_name,
            _compile_function_body(wrapper_body, params=remaining_params, function_key=wrapper_name),
            params=remaining_params,
        )
    )
    return wrapper_name


def _compile_partial_apply_value(value: PartialApply) -> IRReference:
    return IRReference(_register_partial_wrapper(value))
