from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Literal:
    value: int


@dataclass(frozen=True)
class FloatLiteral:
    value: float


@dataclass(frozen=True)
class BoolLiteral:
    value: bool


@dataclass(frozen=True)
class TextLiteral:
    value: str


@dataclass(frozen=True)
class NilLiteral:
    """Distinct absence value (śūnyam), not integer zero."""

    pass


@dataclass(frozen=True)
class BytesLiteral:
    value: bytes


@dataclass(frozen=True)
class ListLiteral:
    elements: tuple["Value", ...]


@dataclass(frozen=True)
class MapLiteral:
    entries: tuple[tuple["Value", "Value"], ...]


@dataclass(frozen=True)
class GroupValue:
    """Explicit grouping (pariveṣṭanam … antam)."""

    inner: "Value"


@dataclass(frozen=True)
class Reference:
    name: str


@dataclass(frozen=True)
class PartialApply:
    """Partial application: āṃśikam callable args… (currying via anukrameṇa prefix)."""

    callable: "Value"
    args: tuple["Value", ...] = ()
    kwargs: tuple[tuple[str, "Value"], ...] = ()
    curry: bool = False


@dataclass(frozen=True)
class CallValue:
    name: str
    module: str | None = None
    args: tuple["Value", ...] = ()
    kwargs: tuple[tuple[str, "Value"], ...] = ()


@dataclass(frozen=True)
class BinaryValue:
    operator: str
    left: "Value"
    right: "Value"


@dataclass(frozen=True)
class BoolNot:
    operand: "Value"


@dataclass(frozen=True)
class BoolAnd:
    left: "Value"
    right: "Value"


@dataclass(frozen=True)
class BoolOr:
    left: "Value"
    right: "Value"


@dataclass(frozen=True)
class TupleLiteral:
    items: tuple["Value", ...]


@dataclass(frozen=True)
class SomeValue:
    inner: "Value"


@dataclass(frozen=True)
class NoneValue:
    pass


@dataclass(frozen=True)
class PatternLiteral:
    value: "Value"


@dataclass(frozen=True)
class PatternWildcard:
    pass


@dataclass(frozen=True)
class PatternTuple:
    items: tuple["Pattern", ...]


@dataclass(frozen=True)
class PatternRecord:
    fields: tuple[tuple[str, "Pattern"], ...]


@dataclass(frozen=True)
class PatternEnum:
    variant: str


Pattern = Union[PatternLiteral, PatternWildcard, PatternTuple, PatternRecord, PatternEnum]


@dataclass(frozen=True)
class MatchArm:
    pattern: Pattern
    body: tuple["Statement", ...]


Value = Union[
    Literal,
    FloatLiteral,
    BoolLiteral,
    TextLiteral,
    NilLiteral,
    BytesLiteral,
    ListLiteral,
    MapLiteral,
    GroupValue,
    Reference,
    CallValue,
    PartialApply,
    BinaryValue,
    BoolNot,
    BoolAnd,
    BoolOr,
    TupleLiteral,
    SomeValue,
    NoneValue,
]

# Alias for Value union (including BytesLiteral explicitly above)


@dataclass(frozen=True)
class DestructureAssign:
    pattern: Pattern
    value: Value


@dataclass(frozen=True)
class Assign:
    target: str
    value: Value


@dataclass(frozen=True)
class Bind:
    """Explicit binding with optional immutability (gaṇitam / acalachihnam)."""

    target: str
    value: Value
    immutable: bool = False
    ownership: str | None = None  # "owned" | "borrow" | "borrow_mut"
    lifetime: str | None = None


@dataclass(frozen=True)
class ForwardDecl:
    """Forward declaration (ghoṣaṇam) — name reserved in scope."""

    target: str


@dataclass(frozen=True)
class Increase:
    target: str
    amount: Value


@dataclass(frozen=True)
class Decrease:
    target: str
    amount: Value


@dataclass(frozen=True)
class Multiply:
    target: str
    factor: Value


@dataclass(frozen=True)
class Display:
    value: Value


@dataclass(frozen=True)
class Pop:
    """Discard an expression value (tyāgaḥ)."""

    value: Value


@dataclass(frozen=True)
class TextConcat:
    target: str
    left: Value
    right: Value


@dataclass(frozen=True)
class TextLength:
    target: str
    text: Value


@dataclass(frozen=True)
class TextGet:
    target: str
    text: Value
    index: Value


@dataclass(frozen=True)
class TextSlice:
    target: str
    text: Value
    start: Value
    end: Value


@dataclass(frozen=True)
class TextContains:
    target: str
    text: Value
    needle: Value


@dataclass(frozen=True)
class ListInit:
    container: str


@dataclass(frozen=True)
class MapInit:
    container: str


@dataclass(frozen=True)
class ListAppend:
    container: str
    item: Value


@dataclass(frozen=True)
class ListGet:
    target: str
    container: str
    index: Value


@dataclass(frozen=True)
class ListLength:
    target: str
    container: str


@dataclass(frozen=True)
class ListMap:
    target: str
    container: str
    function_name: str


@dataclass(frozen=True)
class ListFilter:
    target: str
    container: str
    function_name: str


@dataclass(frozen=True)
class ListReduce:
    target: str
    container: str
    function_name: str
    initial: Value


@dataclass(frozen=True)
class ListAll:
    target: str
    container: str
    function_name: str


@dataclass(frozen=True)
class ListScan:
    target: str
    container: str
    function_name: str
    initial: Value


@dataclass(frozen=True)
class ListZip:
    target: str
    left: str
    right: str


@dataclass(frozen=True)
class ListEnumerate:
    target: str
    container: str


@dataclass(frozen=True)
class ListAny:
    target: str
    container: str
    function_name: str


@dataclass(frozen=True)
class ImmutableListInit:
    container: str


@dataclass(frozen=True)
class ImmutableListAppend:
    target: str
    container: str
    item: Value


@dataclass(frozen=True)
class ListComprehension:
    target: str
    container: str
    where_function: str
    with_function: str


@dataclass(frozen=True)
class LazyIterNew:
    target: str
    container: str


@dataclass(frozen=True)
class LazyIterNext:
    has_more: str
    value: str
    iterator: str


@dataclass(frozen=True)
class GeneratorNew:
    target: str
    function_name: str


@dataclass(frozen=True)
class GeneratorNext:
    has_more: str
    value: str
    generator: str


@dataclass(frozen=True)
class Yield:
    value: Value


@dataclass(frozen=True)
class PipelineChain:
    target: str
    container: str
    steps: tuple[str, ...]


@dataclass(frozen=True)
class MatchExpr:
    target: str
    subject: Value
    arms: tuple[MatchArm, ...]


@dataclass(frozen=True)
class ResultBind:
    target: str
    result: str
    function_name: str


@dataclass(frozen=True)
class DataQuery:
    target: str
    container: str
    field: str
    predicate_function: str


@dataclass(frozen=True)
class RuleDecl:
    rule_id: str
    when_function: str
    then_function: str


@dataclass(frozen=True)
class RuleInvoke:
    target: str
    rule_id: str
    context: Value


@dataclass(frozen=True)
class MemoFunction:
    """Wraps the following FunctionDef with memoization."""

    function: "FunctionDef"


@dataclass(frozen=True)
class AlgebraicTypeDecl:
    """prakāra-vikalpaḥ — algebraic type with named variants."""

    name: str
    variants: tuple[str, ...]


@dataclass(frozen=True)
class MapPut:
    container: str
    key: Value
    value: Value


@dataclass(frozen=True)
class MapGet:
    target: str
    container: str
    key: Value


@dataclass(frozen=True)
class MapContains:
    target: str
    container: str
    key: Value


@dataclass(frozen=True)
class RecordInit:
    record: str


@dataclass(frozen=True)
class FieldSet:
    record: str
    field: Value
    value: Value


@dataclass(frozen=True)
class FieldGet:
    target: str
    record: str
    field: Value


@dataclass(frozen=True)
class FieldContains:
    target: str
    record: str
    field: Value


@dataclass(frozen=True)
class CompareEq:
    left: Value
    right: Value


@dataclass(frozen=True)
class CompareNe:
    left: Value
    right: Value


@dataclass(frozen=True)
class CompareLt:
    left: Value
    right: Value


@dataclass(frozen=True)
class CompareGt:
    left: Value
    right: Value


@dataclass(frozen=True)
class CompareLe:
    left: Value
    right: Value


@dataclass(frozen=True)
class CompareIdentity:
    """Identity comparison (sadr̥śam) — text equality for now."""

    left: Value
    right: Value


@dataclass(frozen=True)
class CompareMembership:
    """Membership in list or map (asti / kośe asti)."""

    container: Value
    key: Value


@dataclass(frozen=True)
class BoolNotCond:
    operand: "Condition"


@dataclass(frozen=True)
class BoolAndCond:
    left: "Condition"
    right: "Condition"


@dataclass(frozen=True)
class BoolOrCond:
    left: "Condition"
    right: "Condition"


Condition = Union[
    CompareEq,
    CompareNe,
    CompareLt,
    CompareGt,
    CompareLe,
    CompareIdentity,
    CompareMembership,
    BoolNotCond,
    BoolAndCond,
    BoolOrCond,
]


@dataclass(frozen=True)
class Block:
    body: tuple["Statement", ...]


@dataclass(frozen=True)
class If:
    condition: Condition
    then_body: tuple["Statement", ...]
    else_body: tuple["Statement", ...] = ()
    elif_branches: tuple[tuple[Condition, tuple["Statement", ...]], ...] = ()


@dataclass(frozen=True)
class Guard:
    condition: Condition
    body: tuple["Statement", ...]


@dataclass(frozen=True)
class Match:
    subject: Value
    arms: tuple[MatchArm, ...]


@dataclass(frozen=True)
class While:
    condition: Condition
    body: tuple["Statement", ...]
    label: str | None = None


@dataclass(frozen=True)
class Until:
    condition: Condition
    body: tuple["Statement", ...]
    label: str | None = None


@dataclass(frozen=True)
class CountedFor:
    counter: str
    start: Value
    end: Value
    body: tuple["Statement", ...]
    label: str | None = None


@dataclass(frozen=True)
class ForEach:
    item: str
    container: str
    body: tuple["Statement", ...]
    label: str | None = None


@dataclass(frozen=True)
class InfiniteLoop:
    body: tuple["Statement", ...]
    label: str | None = None


@dataclass(frozen=True)
class Break:
    label: str | None = None


@dataclass(frozen=True)
class Continue:
    label: str | None = None


@dataclass(frozen=True)
class Defer:
    body: tuple["Statement", ...]


@dataclass(frozen=True)
class Assert:
    condition: Condition
    message: Value | None = None


@dataclass(frozen=True)
class Propagate:
    value: Value


@dataclass(frozen=True)
class Throw:
    """vikṣepaḥ — catchable throw."""

    message: Value


@dataclass(frozen=True)
class Panic:
    """vipattim — unrecoverable abort."""

    message: Value


@dataclass(frozen=True)
class TryCatch:
    """āgrahītvā name ... antam — try/catch block."""

    body: tuple["Statement", ...]
    error_name: str
    handler: tuple["Statement", ...]


@dataclass(frozen=True)
class PreCondition:
    """pūrvaśartam condition — precondition (checked at function entry)."""

    condition: "Condition"


@dataclass(frozen=True)
class PostCondition:
    """uttaraśartam condition — postcondition (checked before return)."""

    condition: "Condition"


@dataclass(frozen=True)
class Invariant:
    """nityaśartam condition — invariant (checked at point of declaration)."""

    condition: "Condition"


@dataclass(frozen=True)
class ForEachDestructure:
    """pratyekam (a, b) : container — foreach with tuple destructuring."""

    names: tuple[str, ...]
    container: str
    body: tuple["Statement", ...]
    label: str | None = None


@dataclass(frozen=True)
class TypeAliasDecl:
    alias: str
    target: str


@dataclass(frozen=True)
class NewtypeDecl:
    name: str
    base: str


@dataclass(frozen=True)
class TypeConvert:
    target: str
    to_type: str
    value: Value


@dataclass(frozen=True)
class ConstDecl:
    name: str
    value: Value
    type_name: str | None = None


@dataclass(frozen=True)
class RecordTypeDecl:
    name: str
    fields: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class GenericRecordDecl:
    """Generic record with one type parameter: vastuḥ Name T { fields }."""

    name: str
    type_param: str
    fields: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class TraitDecl:
    """Interface/trait declaration: abhilakṣaṇaṃ Name T { method signatures }."""

    name: str
    type_param: str | None
    methods: tuple[tuple[str, tuple[str, ...], str | None], ...]


@dataclass(frozen=True)
class TraitImpl:
    """Assert that a record implements a trait."""

    record_name: str
    trait_name: str


@dataclass(frozen=True)
class TypeReflect:
    """Type reflection directive: prakāra-āharaṇam target type_name."""

    target: str
    type_name: str


@dataclass(frozen=True)
class ClassDecl:
    """Class declaration: fields, methods, visibility, inheritance, traits."""

    name: str
    type_param: str | None
    fields: tuple[tuple[str, str], ...]
    methods: tuple[str, ...] = ()
    field_visibility: tuple[tuple[str, str], ...] = ()
    static_methods: tuple[str, ...] = ()
    class_methods: tuple[str, ...] = ()
    base_class: str | None = None
    mixins: tuple[str, ...] = ()
    trait_impls: tuple[str, ...] = ()
    trait_bounds: tuple[tuple[str, str], ...] = ()
    abstract: bool = False
    sealed: bool = False
    computed_properties: tuple[str, ...] = ()
    metaclass: str | None = None
    composition_fields: tuple[str, ...] = ()


@dataclass(frozen=True)
class ClassNew:
    """Instance construction from class metadata (record-backed object)."""

    target: str
    class_name: str
    args: tuple[Value, ...] = ()


@dataclass(frozen=True)
class MethodCall:
    """Instance method dispatch with explicit receiver."""

    target: str
    receiver: str
    method: str
    args: tuple[Value, ...] = ()
    static_dispatch_class: str | None = None


@dataclass(frozen=True)
class StaticMethodCall:
    """Static method call on a class (sthira-paddhati-āhvānam)."""

    target: str
    class_name: str
    method: str
    args: tuple[Value, ...] = ()


@dataclass(frozen=True)
class ClassMethodCall:
    """Class method call with explicit class receiver (varga-paddhati-āhvānam)."""

    target: str
    class_name: str
    method: str
    args: tuple[Value, ...] = ()


@dataclass(frozen=True)
class PropertyGet:
    """Computed property read (guṇa-āharaṇam)."""

    target: str
    receiver: str
    property_name: str


@dataclass(frozen=True)
class InstanceFinalize:
    """Destructor/finalizer call (antima-saṃskāraṃ)."""

    receiver: str


@dataclass(frozen=True)
class ClassReflect:
    """Reflection: class name as text (varga-prakāra-āharaṇam)."""

    target: str
    receiver: str


@dataclass(frozen=True)
class MethodReflect:
    """Reflection: method name as text (paddhati-prakāra-āharaṇam)."""

    target: str
    receiver: str
    method: str


@dataclass(frozen=True)
class LifetimeDecl:
    """Lifetime/region name for rakṣita (āyuḥ / kṣetra)."""

    name: str
    region: str | None = None


@dataclass(frozen=True)
class OwnershipAnnotation:
    """Ownership/borrow annotation on a binding: svāmitvaṃ / uddhāram / parivartanīya-uddhāram."""

    kind: str  # "owned" | "borrow" | "borrow_mut"


@dataclass(frozen=True)
class EffectAnnotation:
    """Effect annotation on a function: śuddhaḥ (pure) | sādhanaṃ (effectful)."""

    kind: str  # "pure" | "effectful"


@dataclass(frozen=True)
class FunctionDef:
    name: str
    body: tuple["Statement", ...]
    module: str | None = None
    params: tuple[str, ...] = ()
    param_defaults: tuple["Value | None", ...] = ()
    variadic_param: str | None = None
    type_params: tuple[str, ...] = ()
    param_types: tuple[str | None, ...] = ()
    return_type: str | None = None
    type_param_bounds: tuple[tuple[str, str], ...] = ()
    effect: str | None = None
    decorators: tuple[str, ...] = ()
    capture_mut: frozenset[str] = frozenset()
    is_inline: bool = False
    is_naked: bool = False
    is_compile_time: bool = False
    named_returns: tuple[str, ...] = ()
    abi_name: str | None = None


@dataclass(frozen=True)
class ReexportDef:
    """Re-export a symbol from another loaded module under this module's export surface."""

    name: str
    source_module: str
    source_symbol: str


@dataclass(frozen=True)
class ModuleDef:
    name: str
    functions: tuple[FunctionDef, ...]
    exports: frozenset[str] = frozenset()
    reexports: tuple[ReexportDef, ...] = ()


@dataclass(frozen=True)
class ImportSymbol:
    name: str
    alias: str | None = None


@dataclass(frozen=True)
class ImportDirective:
    module_path: str
    alias: str | None = None
    symbols: tuple[ImportSymbol, ...] = ()
    required_features: frozenset[str] = frozenset()


@dataclass(frozen=True)
class Call:
    name: str
    module: str | None = None
    args: tuple[Value, ...] = ()
    kwargs: tuple[tuple[str, Value], ...] = ()


@dataclass(frozen=True)
class Return:
    value: Value | None = None
    name: str | None = None
    tail: bool = False


@dataclass(frozen=True)
class UnsafeEnter:
    proof: str | None = None


@dataclass(frozen=True)
class UnsafeExit:
    pass


@dataclass(frozen=True)
class HeapAlloc:
    target: str
    size: Value


@dataclass(frozen=True)
class HeapStore:
    address: Value
    value: Value


@dataclass(frozen=True)
class HeapLoad:
    target: str
    address: Value


@dataclass(frozen=True)
class HeapFree:
    address: Value


@dataclass(frozen=True)
class Phase3RuntimeTypeMarker:
    """Phase 3 runtime type name for future prose literals (bytecode substrate today)."""

    type_name: str


@dataclass(frozen=True)
class Phase3Bind:
    """Bind a name via a Phase 3 bytecode opcode (source directive lowering)."""

    target: str
    opcode: str
    operand: int | str | None = None
    value: "Value | None" = None
    items: tuple["Value", ...] = ()


Statement = Union[
    Assign,
    DestructureAssign,
    Bind,
    ForwardDecl,
    Increase,
    Decrease,
    Multiply,
    Display,
    Pop,
    TextConcat,
    TextLength,
    TextGet,
    TextSlice,
    TextContains,
    ListInit,
    MapInit,
    ListAppend,
    ListGet,
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
    MemoFunction,
    AlgebraicTypeDecl,
    MapPut,
    MapGet,
    MapContains,
    RecordInit,
    FieldSet,
    FieldGet,
    FieldContains,
    ClassNew,
    MethodCall,
    StaticMethodCall,
    ClassMethodCall,
    PropertyGet,
    InstanceFinalize,
    ClassReflect,
    MethodReflect,
    Block,
    If,
    Guard,
    Match,
    While,
    Until,
    CountedFor,
    ForEach,
    InfiniteLoop,
    Break,
    Continue,
    Defer,
    Assert,
    Propagate,
    FunctionDef,
    Call,
    Return,
    UnsafeEnter,
    UnsafeExit,
    HeapAlloc,
    HeapStore,
    HeapLoad,
    HeapFree,
    Phase3Bind,
    TypeAliasDecl,
    NewtypeDecl,
    TypeConvert,
    ConstDecl,
    RecordTypeDecl,
    GenericRecordDecl,
    TraitDecl,
    TraitImpl,
    TypeReflect,
    Throw,
    Panic,
    TryCatch,
    PreCondition,
    PostCondition,
    Invariant,
    ForEachDestructure,
]


@dataclass(frozen=True)
class Program:
    """Top-level compilation unit."""

    statements: tuple[Statement, ...]
    functions: tuple[FunctionDef, ...] = ()
    modules: tuple[ModuleDef, ...] = ()
    imports: tuple[ImportDirective, ...] = ()
    safety_tier: str = "surakshita"
    type_aliases: tuple[TypeAliasDecl, ...] = ()
    newtypes: tuple[NewtypeDecl, ...] = ()
    record_types: tuple[RecordTypeDecl, ...] = ()
    constants: tuple[ConstDecl, ...] = ()
    generic_records: tuple[GenericRecordDecl, ...] = ()
    traits: tuple[TraitDecl, ...] = ()
    trait_impls: tuple[TraitImpl, ...] = ()
    classes: tuple[ClassDecl, ...] = ()
    lifetimes: tuple[LifetimeDecl, ...] = ()
    algebraic_types: tuple[AlgebraicTypeDecl, ...] = ()
    rules: tuple[RuleDecl, ...] = ()
