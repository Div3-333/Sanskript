"""Static type checking pass over AST before bytecode compilation (Phase 4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union

from .ast import (
    Assign,
    BinaryValue,
    Bind,
    BoolAnd,
    BoolLiteral,
    BoolNot,
    BoolOr,
    BytesLiteral,
    Call,
    CallValue,
    ClassNew,
    ClassDecl,
    ConstDecl,
    DestructureAssign,
    Display,
    FloatLiteral,
    FunctionDef,
    GenericRecordDecl,
    LifetimeDecl,
    Literal,
    ListAll,
    ListAny,
    ListScan,
    ListZip,
    ListEnumerate,
    ListFilter,
    ListLiteral,
    ListMap,
    ListReduce,
    ImmutableListInit,
    ImmutableListAppend,
    ListComprehension,
    LazyIterNew,
    GeneratorNew,
    ResultBind,
    DataQuery,
    Yield,
    PipelineChain,
    MatchExpr,
    RuleInvoke,
    MapLiteral,
    ModuleDef,
    NewtypeDecl,
    NoneValue,
    Program,
    RecordTypeDecl,
    Reference,
    MethodCall,
    StaticMethodCall,
    ClassMethodCall,
    PropertyGet,
    InstanceFinalize,
    ClassReflect,
    MethodReflect,
    SomeValue,
    TextLiteral,
    TraitDecl,
    TraitImpl,
    TupleLiteral,
    TypeAliasDecl,
    TypeConvert,
    TypeReflect,
    Value,
)
from .errors import TypeCheckError
from .type_catalog import (
    SafetyTier,
    TierAvailability,
    get_type_catalog,
)

# Canonical surakṣita type names used in source directives and inference.
_BUILTIN_TYPES = frozenset(
    {
        "i32",
        "u32",
        "i64",
        "f64",
        "f32",
        "text",
        "bool",
        "list",
        "hash_map",
        "bytes",
        "tuple",
        "option",
        "result",
        "callable",
        "iterator",
        "void",
        "record",
        "safe_ref",
        "owned",
        "borrow",
        "borrow_mut",
        "async_future",
        "generator",
        "coroutine",
        "linear",
        "affine",
        "metaclass",
        "class_instance",
        "raw_ptr_mut",
        "addr",
    }
)

_NUMERIC_TYPES = frozenset({"i32", "u32", "i64", "f64", "f32", "int"})
_ITERABLE_TYPES = frozenset({"list", "immutable_list", "iterator", "hash_map", "lazy_iterator", "generator"})
_SEQUENCE_TYPES = frozenset({"list", "immutable_list"})

# Implicit widening conversions (source -> permitted targets).
_IMPLICIT_CONVERSIONS: dict[str, frozenset[str]] = {
    "bool": frozenset({"i32", "i64", "f64"}),
    "i32": frozenset({"i64", "f64"}),
    "i64": frozenset({"f64"}),
    "f32": frozenset({"f64"}),
}

# Pointer types available per tier.
_SAFE_REF_TIERS = frozenset({SafetyTier.RAKSHITA, SafetyTier.ARAKSHITA})
_RAW_PTR_TIERS = frozenset({SafetyTier.RAKSHITA, SafetyTier.ARAKSHITA})


@dataclass
class TypeEnv:
    locals: dict[str, "TypeExpr"] = field(default_factory=dict)
    constants: dict[str, "TypeExpr"] = field(default_factory=dict)
    immutable: set[str] = field(default_factory=set)
    ownership: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class PrimitiveType:
    name: str


@dataclass(frozen=True)
class AliasType:
    alias: str
    target: "TypeExpr"


@dataclass(frozen=True)
class NewtypeType:
    name: str
    base: "TypeExpr"


@dataclass(frozen=True)
class OptionType:
    inner: "TypeExpr"


@dataclass(frozen=True)
class CallableType:
    param_types: tuple["TypeExpr", ...]
    return_type: "TypeExpr"


@dataclass(frozen=True)
class GenericType:
    param: str
    inner: "TypeExpr"
    bound: str | None = None


@dataclass(frozen=True)
class ConstType:
    name: str
    inner: "TypeExpr"


@dataclass(frozen=True)
class RecordNominalType:
    name: str
    fields: tuple[tuple[str, "TypeExpr"], ...]


@dataclass(frozen=True)
class GenericRecordType:
    name: str
    type_param: str
    fields: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class TraitType:
    name: str
    type_param: str | None
    methods: tuple[tuple[str, tuple[str, ...], str | None], ...]


@dataclass(frozen=True)
class ClassInstanceType:
    name: str
    fields: tuple[tuple[str, "TypeExpr"], ...]
    methods: tuple[str, ...]


TypeExpr = Union[
    PrimitiveType,
    AliasType,
    NewtypeType,
    OptionType,
    CallableType,
    GenericType,
    ConstType,
    RecordNominalType,
    GenericRecordType,
    TraitType,
    ClassInstanceType,
]


class TypeChecker:
    def __init__(self, program: Program) -> None:
        self.program = program
        self.catalog = get_type_catalog()
        if program.safety_tier == "surakshita":
            self.tier = SafetyTier.SURAKSHITA
        elif program.safety_tier == "rakshita":
            self.tier = SafetyTier.RAKSHITA
        else:
            self.tier = SafetyTier.ARAKSHITA
        self.aliases: dict[str, TypeExpr] = {}
        self.newtypes: dict[str, NewtypeType] = {}
        self.records: dict[str, RecordNominalType] = {}
        self.generic_records: dict[str, GenericRecordType] = {}
        self.traits: dict[str, TraitType] = {}
        self.classes: dict[str, ClassInstanceType] = {}
        self.lifetimes: dict[str, LifetimeDecl] = {}
        self.env = TypeEnv()
        self._inferred_returns: dict[str, list[TypeExpr]] = {}
        self._functions: dict[str, list[FunctionDef]] = {}
        self._init_declarations()
        self._index_functions()

    def _init_declarations(self) -> None:
        for decl in self.program.type_aliases:
            target = self._resolve_type_name(decl.target)
            self.aliases[decl.alias] = AliasType(decl.alias, target)

        for decl in self.program.newtypes:
            base = self._resolve_type_name(decl.base)
            self.newtypes[decl.name] = NewtypeType(decl.name, base)

        for decl in self.program.record_types:
            fields = tuple((name, self._resolve_type_name(ty)) for name, ty in decl.fields)
            self.records[decl.name] = RecordNominalType(decl.name, fields)

        for decl in self.program.generic_records:
            self.generic_records[decl.name] = GenericRecordType(
                decl.name, decl.type_param, decl.fields
            )

        for decl in self.program.traits:
            self.traits[decl.name] = TraitType(decl.name, decl.type_param, decl.methods)

        from .oop import build_class_metadata, validate_class_decl, validate_trait_impl_on_class

        registry = {decl.name: decl for decl in self.program.classes}
        class_meta = build_class_metadata(self.program)
        trait_method_names = {
            t.name: tuple(method for method, _, _ in t.methods) for t in self.program.traits
        }
        for decl in self.program.classes:
            validate_class_decl(decl, registry)
            meta = class_meta[decl.name]
            fields = tuple((name, self._resolve_type_name(ty)) for name, ty in meta.fields)
            all_methods = meta.methods + meta.static_methods + meta.class_methods
            self.classes[decl.name] = ClassInstanceType(decl.name, fields, all_methods)
            if decl.name not in self.records:
                self.records[decl.name] = RecordNominalType(decl.name, fields)
            for trait_name in meta.trait_impls:
                validate_trait_impl_on_class(
                    decl.name,
                    trait_name,
                    class_meta,
                    trait_method_names,
                )

        for decl in self.program.lifetimes:
            self.lifetimes[decl.name] = decl

        for decl in self.program.constants:
            ty = (
                self._resolve_type_name(decl.type_name)
                if decl.type_name
                else self._infer_value(decl.value)
            )
            self.env.constants[decl.name] = ConstType(decl.name, ty)
            self.env.immutable.add(decl.name)

    def _index_functions(self) -> None:
        for function in self.program.functions:
            self._functions.setdefault(function.name, []).append(function)
        for module in self.program.modules:
            functions = module.functions if hasattr(module, "functions") else module[1]
            for function in functions:
                self._functions.setdefault(function.name, []).append(function)

    def instantiate_generic_record(self, name: str, type_arg: str) -> RecordNominalType:
        if name not in self.generic_records:
            raise TypeCheckError(f"Unknown generic record {name!r}")
        generic = self.generic_records[name]
        inner = self._resolve_type_name(type_arg)
        fields: list[tuple[str, TypeExpr]] = []
        for field_name, field_type in generic.fields:
            if field_type == generic.type_param:
                fields.append((field_name, inner))
            else:
                fields.append((field_name, self._resolve_type_name(field_type)))
        inst_name = f"{name}<{type_arg}>"
        return RecordNominalType(inst_name, tuple(fields))

    def resolve_overload(self, name: str, arg_types: list[TypeExpr]) -> FunctionDef | None:
        candidates = list(self._functions.get(name, []))
        for fn_name, overloads in self._functions.items():
            if fn_name == name:
                continue
            if fn_name.startswith(f"{name}_"):
                for fn in overloads:
                    if fn not in candidates:
                        candidates.append(fn)
        if not candidates:
            return None
        arity_matches = [fn for fn in candidates if len(fn.params) == len(arg_types)]
        if not arity_matches:
            return None
        if len(arity_matches) == 1:
            return arity_matches[0]
        suffix = "_".join(self._type_name(t) for t in arg_types)
        for fn in arity_matches:
            if fn.name.endswith(f"_{suffix}") or fn.name.endswith(suffix):
                return fn
        dispatch_name = f"{name}_{suffix}"
        for fn in arity_matches:
            if fn.name == dispatch_name:
                return fn
        typed_matches = [
            fn
            for fn in arity_matches
            if len(fn.param_types) == len(arg_types)
            and all(
                fn.param_types[i]
                and self._param_accepts(
                    self._resolve_type_name(fn.param_types[i]),
                    arg_types[i],
                )
                for i in range(len(arg_types))
            )
        ]
        if len(typed_matches) == 1:
            return typed_matches[0]
        return arity_matches[0]

    def check(self) -> None:
        self._check_tier_forbidden_types()
        self._check_trait_impls()
        for statement in self.program.statements:
            self._check_statement(statement)
        for function in self.program.functions:
            self._check_function(function)
        for module in self.program.modules:
            functions = module.functions if hasattr(module, "functions") else module[1]
            for function in functions:
                self._check_function(function)

    def _check_tier_forbidden_types(self) -> None:
        forbidden: set[str] = set()
        for entry in self.catalog.types:
            level = entry.tiers.get(self.tier, TierAvailability.FORBIDDEN)
            if level == TierAvailability.FORBIDDEN:
                forbidden.add(entry.name)
        # safe_ref is forbidden in surakshita (not in catalog path since it's a builtin)
        if self.tier == SafetyTier.SURAKSHITA:
            forbidden.add("safe_ref")
        # Check alias targets as well as alias names
        for name in forbidden:
            if name in self.newtypes:
                raise TypeCheckError(
                    f"Type {name!r} is forbidden in {self.tier.value} tier",
                    hint="Choose a surakṣita-safe type or raise the safety tier.",
                )
        for alias_name, alias_expr in self.aliases.items():
            # Check the alias name itself
            if alias_name in forbidden:
                raise TypeCheckError(
                    f"Type {alias_name!r} is forbidden in {self.tier.value} tier",
                    hint="Choose a surakṣita-safe type or raise the safety tier.",
                )
            # Check the target of the alias
            from .ast import TypeAliasDecl
            for decl in self.program.type_aliases:
                if decl.alias == alias_name and decl.target in forbidden:
                    raise TypeCheckError(
                        f"Type {decl.target!r} is forbidden in {self.tier.value} tier",
                        hint="Choose a surakṣita-safe type or raise the safety tier.",
                    )

    def _check_trait_impls(self) -> None:
        """Verify that each trait_impl record satisfies all trait method signatures."""
        for impl in self.program.trait_impls:
            if impl.trait_name not in self.traits:
                raise TypeCheckError(
                    f"Unknown trait {impl.trait_name!r} in trait implementation for {impl.record_name!r}"
                )
            if impl.record_name not in self.records and impl.record_name not in self.classes:
                raise TypeCheckError(
                    f"Unknown type {impl.record_name!r} in trait implementation"
                )
            trait = self.traits[impl.trait_name]
            if impl.record_name in self.classes:
                from .oop import build_class_metadata, validate_trait_impl_on_class

                trait_method_names = {
                    t.name: tuple(method for method, _, _ in t.methods)
                    for t in self.program.traits
                }
                validate_trait_impl_on_class(
                    impl.record_name,
                    impl.trait_name,
                    build_class_metadata(self.program),
                    trait_method_names,
                )
                continue
            record = self.records[impl.record_name]
            record_field_names = {name for name, _ in record.fields}
            for method_name, _param_types, _return_type in trait.methods:
                if method_name not in record_field_names:
                    raise TypeCheckError(
                        f"Record {impl.record_name!r} does not satisfy trait {impl.trait_name!r}: "
                        f"missing method/field {method_name!r}",
                        hint="Add the required method or field to the record declaration.",
                    )

    def _check_effect_statement(self, function: FunctionDef, statement: object) -> None:
        if function.effect != "pure":
            return
        from .ast import Display, HeapAlloc, HeapStore

        if isinstance(statement, Display):
            raise TypeCheckError(
                f"Pure function {function.name!r} cannot use darśanam",
                hint="Mark the function sādhanaṃ or remove the effect.",
            )
        if isinstance(statement, (HeapAlloc, HeapStore)):
            raise TypeCheckError(
                f"Pure function {function.name!r} cannot perform heap effects",
            )

    def _check_function(self, function: FunctionDef) -> None:
        saved = TypeEnv(
            dict(self.env.locals),
            dict(self.env.constants),
            set(self.env.immutable),
            dict(self.env.ownership),
        )
        type_map: dict[str, TypeExpr] = {}
        bounds: dict[str, str] = {}
        if function.type_params:
            for param in function.type_params:
                bound = next(
                    (b for tp, b in function.type_param_bounds if tp == param), None
                )
                type_map[param] = GenericType(param, PrimitiveType("unknown"), bound)
                if bound:
                    bounds[param] = bound
        for index, param in enumerate(function.params):
            if index < len(function.param_types) and function.param_types[index]:
                type_map[param] = self._resolve_type_name(function.param_types[index])
            else:
                type_map[param] = PrimitiveType("unknown")
        self.env.locals.update(type_map)
        return_types: list[TypeExpr] = []
        self._inferred_returns[function.name] = return_types
        for statement in function.body:
            self._check_statement(statement, return_collector=return_types)
            self._check_effect_statement(function, statement)
        if function.effect == "pure" and function.capture_mut:
            raise TypeCheckError(
                f"Pure function {function.name!r} cannot use mutable capture",
                hint="Remove parivartanīya-gṛhī or drop śuddhaḥ.",
            )
        if return_types:
            function_inferred = self._unify_types(return_types)
            self._inferred_returns[function.name] = [function_inferred]
            if function.return_type:
                declared = self._resolve_type_name(function.return_type)
                if not self._types_compatible(function_inferred, declared, for_equality=False):
                    raise TypeCheckError(
                        f"Return type mismatch in {function.name!r}: "
                        f"inferred {self._type_name(function_inferred)!r}, "
                        f"declared {function.return_type!r}",
                    )
        elif function.return_type:
            self._inferred_returns[function.name] = [
                self._resolve_type_name(function.return_type)
            ]
        if function.type_param_bounds:
            for param, bound in function.type_param_bounds:
                if bound not in self.traits:
                    raise TypeCheckError(
                        f"Unknown trait bound {bound!r} for type parameter {param!r}",
                    )
        self.env = saved

    def _check_statement(self, statement: object, *, return_collector: list[TypeExpr] | None = None) -> None:
        from .ast import (
            Assert,
            Break,
            Continue,
            CountedFor,
            Defer,
            ForEach,
            Guard,
            If,
            InfiniteLoop,
            Match,
            Propagate,
            Return,
            Until,
            While,
        )

        if isinstance(statement, (TypeAliasDecl, NewtypeDecl, RecordTypeDecl, ConstDecl,
                                  GenericRecordDecl, TraitDecl)):
            return
        if isinstance(statement, TraitImpl):
            if statement.trait_name not in self.traits:
                raise TypeCheckError(f"Unknown trait {statement.trait_name!r}")
            if statement.record_name not in self.records:
                raise TypeCheckError(f"Unknown record {statement.record_name!r}")
            return
        if isinstance(statement, TypeReflect):
            self.env.locals[statement.target] = PrimitiveType("text")
            return
        if isinstance(statement, Assign):
            ty = self._infer_value(statement.value)
            if statement.target in self.env.immutable:
                raise TypeCheckError(f"Cannot assign to immutable binding {statement.target!r}")
            self.env.locals[statement.target] = ty
            return
        if isinstance(statement, Bind):
            ty = self._infer_value(statement.value)
            if statement.immutable:
                self.env.immutable.add(statement.target)
            if statement.ownership:
                self.env.ownership[statement.target] = statement.ownership
            if statement.lifetime:
                if self.tier == SafetyTier.SURAKSHITA:
                    raise TypeCheckError(
                        f"Lifetime annotation on {statement.target!r} requires rakṣita or arakṣita tier",
                    )
                if statement.lifetime not in self.lifetimes:
                    self.lifetimes[statement.lifetime] = LifetimeDecl(statement.lifetime)
            self.env.locals[statement.target] = ty
            return
        if isinstance(statement, DestructureAssign):
            self._infer_value(statement.value)
            return
        if isinstance(statement, TypeConvert):
            source_ty = self._infer_value(statement.value)
            target_ty = self._resolve_type_name(statement.to_type)
            if not self._convertible(source_ty, target_ty):
                raise TypeCheckError(
                    f"Cannot convert {self._type_name(source_ty)!r} to {statement.to_type!r}",
                    hint="Use parivartana only between compatible types or add an explicit newtype.",
                )
            self.env.locals[statement.target] = target_ty
            return
        if isinstance(statement, Display):
            self._infer_value(statement.value)
            return
        from .ast import ListInit, ListLength

        if isinstance(statement, ListInit):
            self.env.locals[statement.container] = PrimitiveType("list")
            return
        if isinstance(statement, ListLength):
            container_ty = self._lookup(statement.container)
            if self._type_name(container_ty) != "list":
                raise TypeCheckError(
                    f"parimāṇam requires list type, got {self._type_name(container_ty)!r}",
                )
            self.env.locals[statement.target] = PrimitiveType("i32")
            return
        if isinstance(statement, ImmutableListInit):
            self.env.locals[statement.container] = PrimitiveType("immutable_list")
            return
        if isinstance(statement, ImmutableListAppend):
            container_ty = self._lookup(statement.container)
            if self._type_name(container_ty) not in _SEQUENCE_TYPES:
                raise TypeCheckError(
                    f"nitye yojanam requires list or immutable_list, got {self._type_name(container_ty)!r}",
                )
            self._infer_value(statement.item)
            self.env.locals[statement.target] = PrimitiveType("immutable_list")
            return
        if isinstance(statement, (ListMap, ListFilter, ListReduce, ListAll, ListScan, ListAny, ListComprehension)):
            container_ty = self._lookup(statement.container)
            if self._type_name(container_ty) not in _SEQUENCE_TYPES:
                raise TypeCheckError(
                    f"Functional list operation requires list type, got {self._type_name(container_ty)!r}",
                )
            if isinstance(statement, ListAll) or isinstance(statement, ListAny):
                self.env.locals[statement.target] = PrimitiveType("bool")
            elif isinstance(statement, ListReduce) or isinstance(statement, ListScan):
                self.env.locals[statement.target] = self._infer_value(statement.initial)
            else:
                self.env.locals[statement.target] = PrimitiveType("list")
            return
        if isinstance(statement, (ListZip, ListEnumerate)):
            for name in (
                (statement.target, statement.left, statement.right)
                if isinstance(statement, ListZip)
                else (statement.target, statement.container)
            ):
                ty = self._lookup(name)
                if self._type_name(ty) not in _SEQUENCE_TYPES and name != statement.target:
                    raise TypeCheckError(
                        f"Sequence operation requires list type for {name!r}, got {self._type_name(ty)!r}",
                    )
            self.env.locals[statement.target] = PrimitiveType("list")
            return
        if isinstance(statement, LazyIterNew):
            container_ty = self._lookup(statement.container)
            if self._type_name(container_ty) not in _SEQUENCE_TYPES:
                raise TypeCheckError(
                    f"alasaḥ requires list type, got {self._type_name(container_ty)!r}",
                )
            self.env.locals[statement.target] = PrimitiveType("lazy_iterator")
            return
        if isinstance(statement, GeneratorNew):
            self.env.locals[statement.target] = PrimitiveType("generator")
            return
        if isinstance(statement, PipelineChain):
            container_ty = self._lookup(statement.container)
            if self._type_name(container_ty) not in _SEQUENCE_TYPES:
                raise TypeCheckError(
                    f"pravāhaḥ requires list type, got {self._type_name(container_ty)!r}",
                )
            self.env.locals[statement.target] = PrimitiveType("list")
            return
        if isinstance(statement, ResultBind):
            result_ty = self._lookup(statement.result)
            if self._type_name(result_ty) != "result":
                raise TypeCheckError("bandhanam requires result-typed value")
            self.env.locals[statement.target] = PrimitiveType("result")
            return
        if isinstance(statement, DataQuery):
            container_ty = self._lookup(statement.container)
            if self._type_name(container_ty) not in _SEQUENCE_TYPES:
                raise TypeCheckError(
                    f"anveṣaṇam requires list type, got {self._type_name(container_ty)!r}",
                )
            self.env.locals[statement.target] = PrimitiveType("list")
            return
        if isinstance(statement, (MatchExpr, RuleInvoke)):
            if isinstance(statement, MatchExpr):
                self._infer_value(statement.subject)
            else:
                self._infer_value(statement.context)
            return
        if isinstance(statement, Yield):
            self._infer_value(statement.value)
            return
        if isinstance(statement, Return):
            if statement.value is not None:
                ty = self._infer_value(statement.value)
                if return_collector is not None:
                    return_collector.append(ty)
            return
        if isinstance(statement, If):
            self._check_condition(statement.condition)
            for body_stmt in statement.then_body:
                self._check_statement(body_stmt, return_collector=return_collector)
            for body_stmt in statement.else_body:
                self._check_statement(body_stmt, return_collector=return_collector)
            for condition, body in statement.elif_branches:
                self._check_condition(condition)
                for body_stmt in body:
                    self._check_statement(body_stmt, return_collector=return_collector)
            return
        if isinstance(statement, (While, Until)):
            self._check_condition(statement.condition)
            for body_stmt in statement.body:
                self._check_statement(body_stmt, return_collector=return_collector)
            return
        if isinstance(statement, CountedFor):
            self._infer_value(statement.start)
            self._infer_value(statement.end)
            self.env.locals[statement.counter] = PrimitiveType("i32")
            for body_stmt in statement.body:
                self._check_statement(body_stmt, return_collector=return_collector)
            return
        if isinstance(statement, ForEach):
            container_ty = self._lookup(statement.container)
            if self._type_name(container_ty) not in _ITERABLE_TYPES:
                raise TypeCheckError(
                    f"foreach requires iterable type, got {self._type_name(container_ty)!r}",
                )
            self.env.locals[statement.item] = PrimitiveType("unknown")
            for body_stmt in statement.body:
                self._check_statement(body_stmt, return_collector=return_collector)
            return
        if isinstance(statement, InfiniteLoop):
            for body_stmt in statement.body:
                self._check_statement(body_stmt, return_collector=return_collector)
            return
        if isinstance(statement, (Break, Continue, Defer)):
            return
        if isinstance(statement, Guard):
            self._check_condition(statement.condition)
            for body_stmt in statement.body:
                self._check_statement(body_stmt, return_collector=return_collector)
            return
        if isinstance(statement, Match):
            self._infer_value(statement.subject)
            for arm in statement.arms:
                for body_stmt in arm.body:
                    self._check_statement(body_stmt, return_collector=return_collector)
            return
        if isinstance(statement, Assert):
            self._check_condition(statement.condition)
            return
        if isinstance(statement, Propagate):
            value_ty = self._infer_value(statement.value)
            if self._type_name(value_ty) != "result":
                raise TypeCheckError(
                    "prasāra requires a result-typed value",
                    hint="Wrap errors in result(err) before propagation.",
                )
            return
        if isinstance(statement, FunctionDef):
            self._check_function(statement)
            return
        if isinstance(statement, Call):
            arg_types = [self._infer_value(arg) for arg in statement.args]
            resolved = self.resolve_overload(statement.name, arg_types)
            if resolved is not None and resolved.param_types:
                for index, param_ty_name in enumerate(resolved.param_types):
                    if index >= len(arg_types) or not param_ty_name:
                        continue
                    expected = self._resolve_type_name(param_ty_name)
                    if not self._param_accepts(expected, arg_types[index]):
                        raise TypeCheckError(
                            f"Argument {index + 1} to {statement.name!r}: "
                            f"expected {param_ty_name!r}, got {self._type_name(arg_types[index])!r}",
                        )
            return
        if isinstance(statement, ClassNew):
            if statement.class_name not in self.classes:
                raise TypeCheckError(f"Unknown class {statement.class_name!r}")
            decl = next((c for c in self.program.classes if c.name == statement.class_name), None)
            if decl is not None and decl.abstract:
                raise TypeCheckError(f"Cannot construct abstract class {statement.class_name!r}")
            self.env.locals[statement.target] = self.classes[statement.class_name]
            return
        if isinstance(statement, MethodCall):
            receiver_ty = self._lookup(statement.receiver)
            receiver_name = self._type_name(receiver_ty)
            class_decl = self.classes.get(receiver_name)
            if class_decl is None:
                raise TypeCheckError(f"Method receiver {statement.receiver!r} is not a class instance")
            if (
                statement.method not in class_decl.methods
                and statement.method != "__init__"
                and not statement.method.startswith("get_")
            ):
                raise TypeCheckError(
                    f"Class {receiver_name!r} has no declared method {statement.method!r}",
                )
            for arg in statement.args:
                self._infer_value(arg)
            self.env.locals[statement.target] = PrimitiveType("unknown")
            return
        if isinstance(statement, StaticMethodCall):
            if statement.class_name not in self.classes:
                raise TypeCheckError(f"Unknown class {statement.class_name!r}")
            decl = self.program.classes
            meta_methods = next(
                (c.static_methods for c in decl if c.name == statement.class_name),
                (),
            )
            if statement.method not in meta_methods:
                raise TypeCheckError(
                    f"Class {statement.class_name!r} has no static method {statement.method!r}",
                )
            for arg in statement.args:
                self._infer_value(arg)
            self.env.locals[statement.target] = PrimitiveType("unknown")
            return
        if isinstance(statement, ClassMethodCall):
            if statement.class_name not in self.classes:
                raise TypeCheckError(f"Unknown class {statement.class_name!r}")
            meta_methods = next(
                (c.class_methods for c in self.program.classes if c.name == statement.class_name),
                (),
            )
            if statement.method not in meta_methods:
                raise TypeCheckError(
                    f"Class {statement.class_name!r} has no class method {statement.method!r}",
                )
            for arg in statement.args:
                self._infer_value(arg)
            self.env.locals[statement.target] = PrimitiveType("unknown")
            return
        if isinstance(statement, PropertyGet):
            receiver_ty = self._lookup(statement.receiver)
            receiver_name = self._type_name(receiver_ty)
            decl = next((c for c in self.program.classes if c.name == receiver_name), None)
            if decl is None:
                raise TypeCheckError(f"Property receiver {statement.receiver!r} is not a class instance")
            if statement.property_name not in decl.computed_properties:
                raise TypeCheckError(
                    f"Class {receiver_name!r} has no computed property {statement.property_name!r}",
                )
            self.env.locals[statement.target] = PrimitiveType("unknown")
            return
        if isinstance(statement, InstanceFinalize):
            receiver_ty = self._lookup(statement.receiver)
            if self._type_name(receiver_ty) not in self.classes:
                raise TypeCheckError(f"Finalize receiver {statement.receiver!r} is not a class instance")
            return
        if isinstance(statement, ClassReflect):
            receiver_ty = self._lookup(statement.receiver)
            if self._type_name(receiver_ty) not in self.classes:
                raise TypeCheckError(f"Reflect receiver {statement.receiver!r} is not a class instance")
            self.env.locals[statement.target] = PrimitiveType("text")
            return
        if isinstance(statement, MethodReflect):
            self.env.locals[statement.target] = PrimitiveType("text")
            return

    def _check_condition(self, condition: object) -> None:
        from .ast import (
            BoolAndCond,
            BoolNotCond,
            BoolOrCond,
            CompareEq,
            CompareGt,
            CompareIdentity,
            CompareLe,
            CompareLt,
            CompareMembership,
            CompareNe,
        )

        if isinstance(condition, (CompareEq, CompareNe, CompareIdentity)):
            self._check_comparable(self._infer_value(condition.left), self._infer_value(condition.right))
        elif isinstance(condition, (CompareLt, CompareGt, CompareLe)):
            left_ty = self._infer_value(condition.left)
            right_ty = self._infer_value(condition.right)
            if not self._is_numeric(left_ty) or not self._is_numeric(right_ty):
                raise TypeCheckError("Ordering comparison requires numeric operands")
        elif isinstance(condition, CompareMembership):
            self._infer_value(condition.container)
            self._infer_value(condition.key)
        elif isinstance(condition, BoolNotCond):
            self._check_condition(condition.operand)
        elif isinstance(condition, (BoolAndCond, BoolOrCond)):
            self._check_condition(condition.left)
            self._check_condition(condition.right)

    def _check_comparable(self, left: TypeExpr, right: TypeExpr) -> None:
        if self._type_name(left) == "unknown" or self._type_name(right) == "unknown":
            return
        if not self._types_compatible(left, right, for_equality=True):
            raise TypeCheckError(
                f"Cannot compare {self._type_name(left)!r} with {self._type_name(right)!r}",
            )

    def _infer_value(self, value: Value) -> TypeExpr:
        if isinstance(value, Literal):
            return PrimitiveType("i32")
        if isinstance(value, FloatLiteral):
            return PrimitiveType("f64")
        if isinstance(value, BoolLiteral):
            return PrimitiveType("bool")
        if isinstance(value, TextLiteral):
            return PrimitiveType("text")
        if isinstance(value, BytesLiteral):
            return PrimitiveType("bytes")
        if isinstance(value, ListLiteral):
            return PrimitiveType("list")
        if isinstance(value, MapLiteral):
            return PrimitiveType("hash_map")
        if isinstance(value, TupleLiteral):
            return PrimitiveType("tuple")
        if isinstance(value, SomeValue):
            return OptionType(self._infer_value(value.inner))
        if isinstance(value, NoneValue):
            return OptionType(PrimitiveType("unknown"))
        if isinstance(value, Reference):
            return self._lookup(value.name)
        if isinstance(value, CallValue):
            arg_types = [self._infer_value(arg) for arg in value.args]
            resolved = self.resolve_overload(value.name, arg_types)
            if resolved is not None:
                if resolved.return_type:
                    return self._resolve_type_name(resolved.return_type)
                inferred = self.get_inferred_return_type(resolved.name)
                if self._type_name(inferred) != "void":
                    return inferred
            return PrimitiveType("unknown")
        if isinstance(value, BinaryValue):
            left_ty = self._infer_value(value.left)
            right_ty = self._infer_value(value.right)
            return self._promote_numeric(left_ty, right_ty)
        if isinstance(value, (BoolNot, BoolAnd, BoolOr)):
            return PrimitiveType("bool")
        return PrimitiveType("unknown")

    def _lookup(self, name: str) -> TypeExpr:
        if name in self.env.locals:
            return self.env.locals[name]
        if name in self.env.constants:
            return self.env.constants[name]
        if name in self.newtypes:
            return self.newtypes[name]
        if name in self.records:
            return self.records[name]
        return PrimitiveType("unknown")

    def _resolve_type_name(self, name: str | None) -> TypeExpr:
        if not name:
            return PrimitiveType("unknown")
        if name in self.aliases:
            resolved = self.aliases[name]
            return resolved if not isinstance(resolved, AliasType) else resolved.target
        if name in self.newtypes:
            return self.newtypes[name]
        if name in self.records:
            return self.records[name]
        if name in self.generic_records:
            return self.generic_records[name]
        if "<" in name and name.endswith(">"):
            base, _, arg = name.partition("<")
            arg = arg[:-1].strip()
            if base in self.generic_records and arg:
                return self.instantiate_generic_record(base, arg)
        if name in self.classes:
            return self.classes[name]
        if name.startswith("Option<") and name.endswith(">"):
            inner_name = name[7:-1].strip()
            return OptionType(self._resolve_type_name(inner_name))
        if name in _BUILTIN_TYPES:
            return PrimitiveType(name)
        try:
            entry = self.catalog.by_name(name)
            forbidden = entry.tiers.get(self.tier, TierAvailability.FORBIDDEN)
            if forbidden == TierAvailability.FORBIDDEN:
                raise TypeCheckError(
                    f"Type {name!r} is forbidden in {self.tier.value} tier",
                )
        except TypeCheckError:
            raise
        except Exception:
            pass
        return PrimitiveType(name)

    def _structural_match(self, record_a: RecordNominalType, record_b: RecordNominalType) -> bool:
        """Return True if record_a has at least all fields that record_b declares (duck typing)."""
        b_fields = {name: ty for name, ty in record_b.fields}
        a_fields = {name: ty for name, ty in record_a.fields}
        for field_name, field_ty in b_fields.items():
            if field_name not in a_fields:
                return False
            if not self._types_compatible(a_fields[field_name], field_ty, for_equality=True):
                return False
        return True

    def _promote_numeric(self, left: TypeExpr, right: TypeExpr) -> TypeExpr:
        left_name = self._type_name(left)
        right_name = self._type_name(right)
        if left_name == "f64" or right_name == "f64":
            return PrimitiveType("f64")
        if left_name == "f32" or right_name == "f32":
            return PrimitiveType("f32")
        if left_name == "i64" or right_name == "i64":
            return PrimitiveType("i64")
        if left_name in _NUMERIC_TYPES and right_name in _NUMERIC_TYPES:
            return PrimitiveType("i32")
        return PrimitiveType("unknown")

    def _convertible(self, source: TypeExpr, target: TypeExpr) -> bool:
        if self._types_compatible(source, target, for_equality=False):
            return True
        source_name = self._type_name(source)
        target_name = self._type_name(target)
        # Implicit widening conversions
        if target_name in _IMPLICIT_CONVERSIONS.get(source_name, frozenset()):
            return True
        # text → bytes conversion (parivartana vakya āhāra)
        if source_name == "text" and target_name == "bytes":
            return True
        # bytes → text conversion
        if source_name == "bytes" and target_name == "text":
            return True
        if isinstance(source, NewtypeType) and isinstance(target, NewtypeType):
            return source.name == target.name
        if isinstance(target, NewtypeType):
            return self._types_compatible(source, target.base, for_equality=False)
        return False

    def _types_compatible(
        self, left: TypeExpr, right: TypeExpr, *, for_equality: bool
    ) -> bool:
        left_name = self._type_name(left)
        right_name = self._type_name(right)
        if left_name == right_name:
            return True
        if for_equality and left_name in _NUMERIC_TYPES and right_name in _NUMERIC_TYPES:
            return True
        if isinstance(left, OptionType) and isinstance(right, OptionType):
            return self._types_compatible(left.inner, right.inner, for_equality=for_equality)
        if isinstance(left, RecordNominalType) and isinstance(right, RecordNominalType):
            if left.name == right.name:
                return True
            if for_equality:
                return self._structural_match(left, right)
            return False
        if isinstance(left, ClassInstanceType) and isinstance(right, ClassInstanceType):
            return left.name == right.name
        return False

    def _param_accepts(self, expected: TypeExpr, actual: TypeExpr) -> bool:
        if self._types_compatible(actual, expected, for_equality=False):
            return True
        if isinstance(expected, RecordNominalType) and isinstance(actual, RecordNominalType):
            return self._structural_match(actual, expected)
        return False

    def _is_numeric(self, ty: TypeExpr) -> bool:
        return self._type_name(ty) in _NUMERIC_TYPES

    def _unify_types(self, types: list[TypeExpr]) -> TypeExpr:
        """Unify a list of inferred return types to a single type."""
        if not types:
            return PrimitiveType("void")
        names = {self._type_name(t) for t in types}
        if len(names) == 1:
            return types[0]
        # Numeric promotion chain
        if names <= _NUMERIC_TYPES:
            if "f64" in names:
                return PrimitiveType("f64")
            if "f32" in names:
                return PrimitiveType("f32")
            if "i64" in names:
                return PrimitiveType("i64")
            return PrimitiveType("i32")
        return PrimitiveType("unknown")

    def get_inferred_return_type(self, function_name: str) -> TypeExpr:
        returns = self._inferred_returns.get(function_name, [])
        if not returns:
            return PrimitiveType("void")
        return returns[0] if len(returns) == 1 else self._unify_types(returns)

    @staticmethod
    def _type_name(ty: TypeExpr) -> str:
        if isinstance(ty, PrimitiveType):
            return ty.name
        if isinstance(ty, AliasType):
            return ty.alias
        if isinstance(ty, NewtypeType):
            return ty.name
        if isinstance(ty, OptionType):
            return f"Option<{TypeChecker._type_name(ty.inner)}>"
        if isinstance(ty, CallableType):
            return "callable"
        if isinstance(ty, GenericType):
            return ty.param
        if isinstance(ty, ConstType):
            return TypeChecker._type_name(ty.inner)
        if isinstance(ty, RecordNominalType):
            return ty.name
        if isinstance(ty, GenericRecordType):
            return ty.name
        if isinstance(ty, TraitType):
            return ty.name
        if isinstance(ty, ClassInstanceType):
            return ty.name
        return "unknown"


def check_program(program: Program) -> None:
    """Run static type validation; raises TypeCheckError on failure."""
    TypeChecker(program).check()
