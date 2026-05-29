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
class IRNilLiteral:
    pass


@dataclass(frozen=True)
class IRBytesLiteral:
    value: bytes


@dataclass(frozen=True)
class IRListLiteral:
    elements: tuple["IRValue", ...]


@dataclass(frozen=True)
class IRMapLiteral:
    entries: tuple[tuple["IRValue", "IRValue"], ...]


@dataclass(frozen=True)
class IRGroupValue:
    inner: "IRValue"


@dataclass(frozen=True)
class IRBoolNot:
    operand: "IRValue"


@dataclass(frozen=True)
class IRBoolAnd:
    left: "IRValue"
    right: "IRValue"


@dataclass(frozen=True)
class IRBoolOr:
    left: "IRValue"
    right: "IRValue"


@dataclass(frozen=True)
class IRReference:
    name: str


@dataclass(frozen=True)
class IRCallValue:
    target: str
    args: tuple["IRValue", ...] = ()
    kwargs: tuple[tuple[str, "IRValue"], ...] = ()


@dataclass(frozen=True)
class IRBinaryValue:
    operator: str
    left: "IRValue"
    right: "IRValue"


@dataclass(frozen=True)
class IRTupleLiteral:
    items: tuple["IRValue", ...]


IRValue = Union[
    IRLiteral,
    IRFloatLiteral,
    IRBoolLiteral,
    IRTextLiteral,
    IRNilLiteral,
    IRBytesLiteral,
    IRListLiteral,
    IRMapLiteral,
    IRGroupValue,
    IRBoolNot,
    IRBoolAnd,
    IRBoolOr,
    IRReference,
    IRCallValue,
    IRBinaryValue,
    IRTupleLiteral,
    "IRPhase3Value",
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
class IRPop:
    value: IRValue


@dataclass(frozen=True)
class IRScopeEnter:
    pass


@dataclass(frozen=True)
class IRScopeExit:
    pass


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
class IRListMap:
    target: str
    container: str
    function_name: str


@dataclass(frozen=True)
class IRListFilter:
    target: str
    container: str
    function_name: str


@dataclass(frozen=True)
class IRListReduce:
    target: str
    container: str
    function_name: str
    initial: IRValue


@dataclass(frozen=True)
class IRListAll:
    target: str
    container: str
    function_name: str


@dataclass(frozen=True)
class IRListScan:
    target: str
    container: str
    function_name: str
    initial: IRValue


@dataclass(frozen=True)
class IRListZip:
    target: str
    left: str
    right: str


@dataclass(frozen=True)
class IRListEnumerate:
    target: str
    container: str


@dataclass(frozen=True)
class IRListAny:
    target: str
    container: str
    function_name: str


@dataclass(frozen=True)
class IRImmutableListInit:
    container: str


@dataclass(frozen=True)
class IRImmutableListAppend:
    target: str
    container: str
    item: IRValue


@dataclass(frozen=True)
class IRListComprehension:
    target: str
    container: str
    where_function: str
    with_function: str


@dataclass(frozen=True)
class IRLazyIterNew:
    target: str
    container: str


@dataclass(frozen=True)
class IRLazyIterNext:
    has_more: str
    value: str
    iterator: str


@dataclass(frozen=True)
class IRGeneratorNew:
    target: str
    function_name: str


@dataclass(frozen=True)
class IRGeneratorNext:
    has_more: str
    value: str
    generator: str


@dataclass(frozen=True)
class IRYield:
    value: IRValue


@dataclass(frozen=True)
class IRPipelineChain:
    target: str
    container: str
    steps: tuple[str, ...]


@dataclass(frozen=True)
class IRMatchExpr:
    target: str
    subject: IRValue
    arms: tuple[tuple[object, tuple[IRInstruction, ...]], ...]


@dataclass(frozen=True)
class IRResultBind:
    target: str
    result: str
    function_name: str


@dataclass(frozen=True)
class IRDataQuery:
    target: str
    container: str
    field: str
    predicate_function: str


@dataclass(frozen=True)
class IRRuleDecl:
    rule_id: str
    when_function: str
    then_function: str


@dataclass(frozen=True)
class IRRuleInvoke:
    target: str
    rule_id: str
    context: IRValue


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
class IRClassNew:
    target: str
    class_name: str
    args: tuple[IRValue, ...] = ()


@dataclass(frozen=True)
class IRMethodCall:
    target: str
    receiver: str
    method: str
    args: tuple[IRValue, ...] = ()
    static_dispatch: str | None = None


@dataclass(frozen=True)
class IRStaticMethodCall:
    target: str
    class_name: str
    method: str
    args: tuple[IRValue, ...] = ()


@dataclass(frozen=True)
class IRClassMethodCall:
    target: str
    class_name: str
    method: str
    args: tuple[IRValue, ...] = ()


@dataclass(frozen=True)
class IRPropertyGet:
    target: str
    receiver: str
    property_name: str


@dataclass(frozen=True)
class IRInstanceFinalize:
    receiver: str


@dataclass(frozen=True)
class IRClassReflect:
    target: str
    receiver: str


@dataclass(frozen=True)
class IRMethodReflect:
    target: str
    method: str


@dataclass(frozen=True)
class IRCompareEq:
    left: IRValue
    right: IRValue


@dataclass(frozen=True)
class IRCompareLt:
    left: IRValue
    right: IRValue


@dataclass(frozen=True)
class IRCompareNe:
    left: IRValue
    right: IRValue


@dataclass(frozen=True)
class IRCompareGt:
    left: IRValue
    right: IRValue


@dataclass(frozen=True)
class IRCompareLe:
    left: IRValue
    right: IRValue


@dataclass(frozen=True)
class IRCompareIdentity:
    left: IRValue
    right: IRValue


@dataclass(frozen=True)
class IRCompareMembership:
    container: IRValue
    key: IRValue


@dataclass(frozen=True)
class IRBoolNotCond:
    operand: "IRCondition"


@dataclass(frozen=True)
class IRBoolAndCond:
    left: "IRCondition"
    right: "IRCondition"


@dataclass(frozen=True)
class IRBoolOrCond:
    left: "IRCondition"
    right: "IRCondition"


IRCondition = Union[
    IRCompareEq,
    IRCompareNe,
    IRCompareLt,
    IRCompareGt,
    IRCompareLe,
    IRCompareIdentity,
    IRCompareMembership,
    IRBoolNotCond,
    IRBoolAndCond,
    IRBoolOrCond,
]


@dataclass(frozen=True)
class IRIf:
    condition: IRCondition
    then_body: tuple["IRInstruction", ...]
    else_body: tuple["IRInstruction", ...] = ()
    elif_branches: tuple[tuple[IRCondition, tuple["IRInstruction", ...]], ...] = ()


@dataclass(frozen=True)
class IRWhile:
    condition: IRCondition
    body: tuple["IRInstruction", ...]
    label: str | None = None


@dataclass(frozen=True)
class IRCall:
    target: str
    args: tuple[IRValue, ...] = ()
    kwargs: tuple[tuple[str, IRValue], ...] = ()
    tail: bool = False


@dataclass(frozen=True)
class IRReturn:
    value: IRValue | None = None
    name: str | None = None
    tail: bool = False


@dataclass(frozen=True)
class IRUnsafeEnter:
    proof: str | None = None


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


@dataclass(frozen=True)
class IRPhase3Opcode:
    """Direct Phase 3 bytecode emission hook (used when lowering typed runtime ops)."""

    opcode: str
    operand: object | None = None


@dataclass(frozen=True)
class IRPhase3Value:
    """Phase 3 value built entirely from bytecode (option, fixed int push, etc.)."""

    opcode: str
    operand: object | None = None
    value: "IRValue | None" = None
    items: tuple["IRValue", ...] = ()


@dataclass(frozen=True)
class IRPhase3Bind:
    target: str
    opcode: str
    operand: object | None = None
    value: "IRValue | None" = None
    items: tuple["IRValue", ...] = ()


@dataclass(frozen=True)
class IRBreak:
    label: str | None = None


@dataclass(frozen=True)
class IRContinue:
    label: str | None = None


@dataclass(frozen=True)
class IRDefer:
    body: tuple["IRInstruction", ...]


@dataclass(frozen=True)
class IRAssert:
    condition: "IRCondition"
    message: IRValue | None = None


@dataclass(frozen=True)
class IRPropagate:
    value: IRValue


@dataclass(frozen=True)
class IRUntil:
    condition: "IRCondition"
    body: tuple["IRInstruction", ...]
    label: str | None = None


@dataclass(frozen=True)
class IRCountedFor:
    counter: str
    start: IRValue
    end: IRValue
    body: tuple["IRInstruction", ...]
    label: str | None = None


@dataclass(frozen=True)
class IRForEach:
    item: str
    container: str
    body: tuple["IRInstruction", ...]
    label: str | None = None


@dataclass(frozen=True)
class IRInfiniteLoop:
    body: tuple["IRInstruction", ...]
    label: str | None = None


@dataclass(frozen=True)
class IRMatch:
    subject: IRValue
    arms: tuple[tuple[object, tuple["IRInstruction", ...]], ...]


@dataclass(frozen=True)
class IRCondAssert:
    """Assert condition holds; panic with message if it fails."""

    condition: "IRCondition"
    message: str


@dataclass(frozen=True)
class IRThrow:
    message: IRValue


@dataclass(frozen=True)
class IRPanic:
    message: IRValue


@dataclass(frozen=True)
class IRTryCatch:
    body: tuple["IRInstruction", ...]
    error_name: str
    handler: tuple["IRInstruction", ...]


@dataclass(frozen=True)
class IRForEachDestructure:
    names: tuple[str, ...]
    container: str
    body: tuple["IRInstruction", ...]
    label: str | None = None


IRInstruction = Union[
    IRStore,
    IRIncrease,
    IRDecrease,
    IRMultiply,
    IREmit,
    IRPop,
    IRScopeEnter,
    IRScopeExit,
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
    IRMapPut,
    IRMapGet,
    IRMapContains,
    IRRecordInit,
    IRFieldSet,
    IRFieldGet,
    IRFieldContains,
    IRClassNew,
    IRMethodCall,
    IRStaticMethodCall,
    IRClassMethodCall,
    IRPropertyGet,
    IRInstanceFinalize,
    IRClassReflect,
    IRMethodReflect,
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
    IRPhase3Opcode,
    IRPhase3Bind,
    IRBreak,
    IRContinue,
    IRDefer,
    IRAssert,
    IRPropagate,
    IRUntil,
    IRCountedFor,
    IRForEach,
    IRInfiniteLoop,
    IRMatch,
    IRThrow,
    IRPanic,
    IRTryCatch,
    IRForEachDestructure,
    IRCondAssert,
]


@dataclass(frozen=True)
class IRFunction:
    name: str
    instructions: tuple[IRInstruction, ...]
    module: str | None = None
    params: tuple[str, ...] = ()
    defaults: tuple[IRValue | None, ...] = ()
    variadic_param: str | None = None
    capture_mut: frozenset[str] = frozenset()
    effect: str | None = None
    is_generator: bool = False
    is_memoized: bool = False
    is_inline: bool = False
    is_naked: bool = False
    abi_name: str | None = None
    named_returns: tuple[str, ...] = ()


@dataclass(frozen=True)
class IRModule:
    name: str
    functions: tuple[IRFunction, ...]


@dataclass(frozen=True)
class IRProgram:
    instructions: tuple[IRInstruction, ...]
    functions: tuple[IRFunction, ...] = ()
    modules: tuple[IRModule, ...] = ()
