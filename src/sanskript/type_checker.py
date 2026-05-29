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
    FieldGet,
    FieldSet,
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
    LazyIterNext,
    GeneratorNew,
    GeneratorNext,
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
    Phase3Bind,
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
    UnsafeEnter,
    UnsafeExit,
    Value,
    RuleDecl,
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
    lifetimes: dict[str, str] = field(default_factory=dict)
    borrow_source: dict[str, str] = field(default_factory=dict)
    moved: set[str] = field(default_factory=set)
    generator_item_types: dict[str, "TypeExpr"] = field(default_factory=dict)


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
        self._inferred_yields: dict[str, list[TypeExpr]] = {}
        self._generator_functions: set[str] = set()
        self._functions: dict[str, list[FunctionDef]] = {}
        self._current_function_name: str | None = None
        self._current_function_effect: str | None = None
        self._class_meta: dict[str, object] = {}
        self._algebraic_variants: dict[str, frozenset[str]] = {
            decl.name: frozenset(decl.variants) for decl in program.algebraic_types
        }
        self._rules: dict[str, RuleDecl] = {}
        self._scope_depth = 0
        self._borrow_scope_depth: dict[str, int] = {}
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
        self._class_meta = class_meta
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
        # Overload participation is declaration-driven: only functions declared
        # with the same logical base name belong to an overload set.
        candidates = list(self._functions.get(name, []))
        if not candidates:
            prefix = f"{name}_"
            for fn_name, defs in self._functions.items():
                if fn_name.startswith(prefix) and self._has_type_suffix(fn_name[len(prefix):]):
                    candidates.extend(defs)
        if not candidates:
            return None
        arity_matches = [fn for fn in candidates if len(fn.params) == len(arg_types)]
        if not arity_matches:
            return None
        if len(arity_matches) == 1:
            return arity_matches[0]
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
        self._check_phase23_concurrency_rules()
        self._check_trait_impls()
        self._check_rule_declarations()
        for statement in self.program.statements:
            self._check_statement(statement)
        for function in self.program.functions:
            self._check_function(function)
        for module in self.program.modules:
            functions = module.functions if hasattr(module, "functions") else module[1]
            for function in functions:
                self._check_function(function)

    def _check_phase23_concurrency_rules(self) -> None:
        """Compile-time guards for async/future and tiered concurrent surfaces."""
        if self.tier == SafetyTier.ARAKSHITA:
            for alias_name, _alias_expr in self.aliases.items():
                if alias_name == "channel" or alias_name.endswith("_channel"):
                    raise TypeCheckError(
                        f"Type alias {alias_name!r} is not permitted in arakṣita concurrent code",
                        hint="Use raw memory + explicit unsafe proofs instead of channel abstractions.",
                    )
        for function in self.program.functions:
            if function.return_type != "async_future":
                continue
            if any(param.type_name in {"raw_ptr_mut", "borrow_mut"} for param in function.params if param.type_name):
                raise TypeCheckError(
                    f"Function {function.name!r} cannot combine async_future with mutable low-level parameters",
                    hint="Split async work from arakṣita mutable pointer parameters.",
                )

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

    def _check_rule_declarations(self) -> None:
        for rule in self.program.rules:
            if rule.rule_id in self._rules:
                raise TypeCheckError(f"Duplicate rule id {rule.rule_id!r}")
            self._rules[rule.rule_id] = rule
            self._require_function_arity(rule.when_function, 1, context=f"rule {rule.rule_id} when")
            self._require_function_arity(rule.then_function, 1, context=f"rule {rule.rule_id} then")

    def _require_function_arity(self, name: str, arity: int, *, context: str) -> None:
        candidates = self._functions.get(name, [])
        if not candidates:
            raise TypeCheckError(f"Unknown function {name!r} referenced by {context}")
        if not any(len(fn.params) == arity for fn in candidates):
            got = ", ".join(str(len(fn.params)) for fn in candidates)
            raise TypeCheckError(
                f"{context} requires arity {arity} for {name!r}, got [{got}]",
            )

    def _check_enum_new(self, statement: Phase3Bind) -> None:
        type_name = str(statement.operand) if statement.operand is not None else ""
        if type_name not in self._algebraic_variants:
            raise TypeCheckError(
                f"Unknown algebraic type {type_name!r} in gaṇavikalpaḥ construction",
                hint="Declare it with prakāra-vikalpaḥ before constructing variants.",
            )
        if not statement.items:
            raise TypeCheckError("enum_new requires variant and payload items")
        variant_value = statement.items[0]
        if not isinstance(variant_value, TextLiteral):
            raise TypeCheckError("enum_new variant must be text literal")
        if variant_value.value not in self._algebraic_variants[type_name]:
            raise TypeCheckError(
                f"Unknown variant {variant_value.value!r} for algebraic type {type_name!r}",
            )

    def _check_effect_statement(self, function: FunctionDef, statement: object) -> None:
        if function.effect != "pure":
            return
        from .ast import Display, HeapAlloc, HeapStore, HeapLoad, HeapFree

        if isinstance(statement, Display):
            raise TypeCheckError(
                f"Pure function {function.name!r} cannot use darśanam",
                hint="Mark the function sādhanaṃ or remove the effect.",
            )
        if isinstance(statement, (HeapAlloc, HeapStore, HeapLoad, HeapFree)):
            raise TypeCheckError(
                f"Pure function {function.name!r} cannot perform heap effects",
            )

    def _check_function(self, function: FunctionDef) -> None:
        saved = TypeEnv(
            dict(self.env.locals),
            dict(self.env.constants),
            set(self.env.immutable),
            dict(self.env.ownership),
            dict(self.env.lifetimes),
            dict(self.env.borrow_source),
            set(self.env.moved),
            dict(self.env.generator_item_types),
        )
        saved_fn_name = self._current_function_name
        saved_fn_effect = self._current_function_effect
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
        self._current_function_name = function.name
        self._current_function_effect = function.effect
        return_types: list[TypeExpr] = []
        yield_types: list[TypeExpr] = []
        self._inferred_returns[function.name] = return_types
        self._inferred_yields[function.name] = yield_types
        self._check_block(
            function.body,
            return_collector=return_types,
            yield_collector=yield_types,
            function_for_effect=function,
        )
        if function.is_inline and self.tier != SafetyTier.RAKSHITA:
            raise TypeCheckError(
                f"Inline function {function.name!r} requires rakṣita tier",
                hint="Use antarbhūtam only in rakṣita programs.",
            )
        if function.is_naked and self.tier != SafetyTier.ARAKSHITA:
            raise TypeCheckError(
                f"Naked function {function.name!r} requires arakṣita tier",
                hint="Use nagnā only in arakṣita programs.",
            )
        if function.abi_name and self.tier != SafetyTier.ARAKSHITA:
            raise TypeCheckError(
                f"ABI export {function.name!r} requires arakṣita tier",
                hint="Use `abi` only in arakṣita programs.",
            )
        if function.abi_name and not function.is_naked:
            raise TypeCheckError(
                f"Function {function.name!r} uses abi without nagnā",
                hint="Pair abi declarations with nagnā in arakṣita.",
            )
        if function.effect == "pure" and function.capture_mut:
            raise TypeCheckError(
                f"Pure function {function.name!r} cannot use mutable capture",
                hint="Remove parivartanīya-gṛhī or drop śuddhaḥ.",
            )
        if any(deco in {"smaraṇa", "smarana"} for deco in function.decorators):
            if function.effect == "effectful":
                raise TypeCheckError(
                    f"Memoized function {function.name!r} cannot be marked sādhanaṃ (effectful)",
                    hint="Use śuddhaḥ for memoization or remove saṃskāraṃ smaraṇa.",
                )
            if function.capture_mut:
                raise TypeCheckError(
                    f"Memoized function {function.name!r} cannot capture mutable state",
                    hint="Memoization keys must depend only on call arguments.",
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
        declared_return = function.return_type or ""
        has_yield = bool(yield_types)
        if has_yield:
            self._generator_functions.add(function.name)
            if declared_return and declared_return not in {"generator", "coroutine"}:
                raise TypeCheckError(
                    f"Function {function.name!r} yields values but declares return type {declared_return!r}",
                    hint="Use return type 'generator' or 'coroutine' for yielding functions.",
                )
        elif declared_return in {"generator", "coroutine"}:
            raise TypeCheckError(
                f"Function {function.name!r} declares {declared_return!r} but has no pradānam (yield)",
                hint="Add yield statements or change the return type.",
            )
        if declared_return == "async_future" and has_yield:
            raise TypeCheckError(
                f"Function {function.name!r} cannot combine async_future return with generator yields",
                hint="Use coroutine/generator return type for yielding functions.",
            )
        if declared_return == "async_future" and function.effect == "pure":
            raise TypeCheckError(
                f"Function {function.name!r} cannot be pure with async_future return type",
                hint="Mark async functions as effectful (sādhanaṃ).",
            )
        self.env = saved
        self._current_function_name = saved_fn_name
        self._current_function_effect = saved_fn_effect

    def _check_statement(
        self,
        statement: object,
        *,
        return_collector: list[TypeExpr] | None = None,
        yield_collector: list[TypeExpr] | None = None,
    ) -> None:
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
            if statement.target in self.env.borrow_source:
                raise TypeCheckError(
                    f"Cannot assign to borrowed binding {statement.target!r}",
                    hint="Rebind from owner instead of mutating a borrow alias.",
                )
            if self._has_active_borrows(statement.target):
                raise TypeCheckError(
                    f"Cannot mutate {statement.target!r} while borrows are active",
                )
            self.env.locals[statement.target] = ty
            self.env.generator_item_types.pop(statement.target, None)
            self.env.moved.discard(statement.target)
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
                    raise TypeCheckError(
                        f"Unknown lifetime {statement.lifetime!r} on binding {statement.target!r}",
                        hint="Declare the lifetime with āyuḥ before using it on bindings.",
                    )
                self.env.lifetimes[statement.target] = statement.lifetime
            source_ref = statement.value.name if isinstance(statement.value, Reference) else None
            if statement.ownership in {"borrow", "borrow_mut"}:
                if source_ref is None:
                    raise TypeCheckError(
                        f"{statement.ownership} binding {statement.target!r} must borrow from a named reference",
                    )
                self._check_borrow_rules(
                    source_ref,
                    statement.target,
                    mutable=statement.ownership == "borrow_mut",
                    lifetime=statement.lifetime,
                )
                self.env.borrow_source[statement.target] = source_ref
                self._borrow_scope_depth[statement.target] = self._scope_depth
                self.env.moved.discard(statement.target)
            elif statement.ownership == "owned" and source_ref is not None:
                self._check_can_move(source_ref)
                self.env.moved.add(source_ref)
                self.env.borrow_source.pop(statement.target, None)
                self._borrow_scope_depth.pop(statement.target, None)
                self.env.moved.discard(statement.target)
            else:
                self.env.borrow_source.pop(statement.target, None)
                self._borrow_scope_depth.pop(statement.target, None)
                self.env.moved.discard(statement.target)
            self.env.locals[statement.target] = ty
            self.env.generator_item_types.pop(statement.target, None)
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
        if isinstance(statement, UnsafeEnter):
            if self.tier == SafetyTier.RAKSHITA and not (statement.proof and statement.proof.strip()):
                raise TypeCheckError(
                    "rakṣita unsafe block requires an explicit proof annotation",
                    hint="Use `arakṣitaḥ adhikāraḥ ārabhyate pramāṇam vākyam ... iti.`",
                )
            return
        if isinstance(statement, UnsafeExit):
            return
        if isinstance(statement, Phase3Bind):
            if statement.opcode == "enum_new":
                self._check_enum_new(statement)
            self.env.locals[statement.target] = PrimitiveType("unknown")
            return
        if isinstance(statement, FieldSet):
            receiver_ty = self._lookup(statement.record)
            receiver_name = self._type_name(receiver_ty)
            if receiver_name in self.classes:
                if self._class_meta.get(receiver_name) is None:
                    raise TypeCheckError(f"Unknown class metadata for {receiver_name!r}")
                field_name = self._literal_text(statement.field)
                if field_name is None:
                    raise TypeCheckError("Class field access requires literal field name")
                class_fields = {name for name, _ in self.classes[receiver_name].fields}
                if field_name not in class_fields:
                    raise TypeCheckError(
                        f"Class {receiver_name!r} has no field {field_name!r}",
                    )
                from .oop import check_field_access
                check_field_access(
                    class_name=receiver_name,
                    field=field_name,
                    from_class=self._current_class_name(),
                    metadata=self._class_meta,
                )
            self._infer_value(statement.value)
            return
        if isinstance(statement, FieldGet):
            receiver_ty = self._lookup(statement.record)
            receiver_name = self._type_name(receiver_ty)
            if receiver_name in self.classes:
                if self._class_meta.get(receiver_name) is None:
                    raise TypeCheckError(f"Unknown class metadata for {receiver_name!r}")
                field_name = self._literal_text(statement.field)
                if field_name is None:
                    raise TypeCheckError("Class field access requires literal field name")
                class_fields = {name for name, _ in self.classes[receiver_name].fields}
                if field_name not in class_fields:
                    raise TypeCheckError(
                        f"Class {receiver_name!r} has no field {field_name!r}",
                    )
                from .oop import check_field_access
                check_field_access(
                    class_name=receiver_name,
                    field=field_name,
                    from_class=self._current_class_name(),
                    metadata=self._class_meta,
                )
                field_type = dict(self.classes[receiver_name].fields).get(field_name)
                self.env.locals[statement.target] = field_type or PrimitiveType("unknown")
                return
            self.env.locals[statement.target] = PrimitiveType("unknown")
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
            if isinstance(statement, ListComprehension):
                self._require_function_arity(statement.where_function, 1, context="samīkaraṇam where")
                self._require_function_arity(statement.with_function, 1, context="samīkaraṇam with")
            else:
                expected_arity = 2 if isinstance(statement, (ListReduce, ListScan)) else 1
                self._require_function_arity(
                    statement.function_name,  # type: ignore[attr-defined]
                    expected_arity,
                    context=type(statement).__name__,
                )
            if isinstance(statement, ListAll) or isinstance(statement, ListAny):
                self.env.locals[statement.target] = PrimitiveType("bool")
            elif isinstance(statement, ListReduce) or isinstance(statement, ListScan):
                self.env.locals[statement.target] = self._infer_value(statement.initial)
            else:
                self.env.locals[statement.target] = PrimitiveType("list")
            if self._current_function_effect == "pure":
                fn_name = (
                    statement.function_name
                    if hasattr(statement, "function_name")
                    else statement.where_function
                )
                resolved = self.resolve_overload(fn_name, [PrimitiveType("unknown")])
                if resolved is None or resolved.effect == "effectful":
                    raise TypeCheckError(
                        f"Pure function {self._current_function_name!r} cannot call effectful or unknown function {fn_name!r}",
                    )
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
        if isinstance(statement, LazyIterNext):
            iterator_ty = self._lookup(statement.iterator)
            if self._type_name(iterator_ty) != "lazy_iterator":
                raise TypeCheckError(
                    f"alasa-agrima requires lazy_iterator, got {self._type_name(iterator_ty)!r}",
                )
            self.env.locals[statement.has_more] = PrimitiveType("bool")
            self.env.locals[statement.value] = PrimitiveType("unknown")
            return
        if isinstance(statement, GeneratorNew):
            fn = self.resolve_overload(statement.function_name, [])
            if fn is None:
                raise TypeCheckError(f"Unknown generator function {statement.function_name!r}")
            if fn.name not in self._generator_functions and not self._function_contains_yield(fn):
                raise TypeCheckError(
                    f"Function {statement.function_name!r} is not a generator",
                    hint="Add pradānam (yield) statements to the function body.",
                )
            self.env.locals[statement.target] = PrimitiveType("generator")
            self.env.generator_item_types[statement.target] = self.get_inferred_yield_type(fn.name)
            return
        if isinstance(statement, GeneratorNext):
            generator_ty = self._lookup(statement.generator)
            if self._type_name(generator_ty) != "generator":
                raise TypeCheckError(
                    f"utpādaka-agrima requires generator, got {self._type_name(generator_ty)!r}",
                )
            self.env.locals[statement.has_more] = PrimitiveType("bool")
            self.env.locals[statement.value] = self.env.generator_item_types.get(
                statement.generator, PrimitiveType("unknown")
            )
            return
        if isinstance(statement, PipelineChain):
            container_ty = self._lookup(statement.container)
            if self._type_name(container_ty) not in _SEQUENCE_TYPES:
                raise TypeCheckError(
                    f"pravāhaḥ requires list type, got {self._type_name(container_ty)!r}",
                )
            for fn_name in statement.steps:
                self._require_function_arity(fn_name, 1, context="pravāhaḥ step")
            self.env.locals[statement.target] = PrimitiveType("list")
            if self._current_function_effect == "pure":
                for fn_name in statement.steps:
                    resolved = self.resolve_overload(fn_name, [PrimitiveType("unknown")])
                    if resolved is None or resolved.effect == "effectful":
                        raise TypeCheckError(
                            f"Pure function {self._current_function_name!r} cannot call effectful or unknown function {fn_name!r}",
                        )
            return
        if isinstance(statement, ResultBind):
            result_ty = self._lookup(statement.result)
            if self._type_name(result_ty) != "result":
                raise TypeCheckError("bandhanam requires result-typed value")
            self.env.locals[statement.target] = PrimitiveType("result")
            if self._current_function_effect == "pure":
                resolved = self.resolve_overload(statement.function_name, [PrimitiveType("unknown")])
                if resolved is None or resolved.effect == "effectful":
                    raise TypeCheckError(
                        f"Pure function {self._current_function_name!r} cannot call effectful or unknown function {statement.function_name!r}",
                    )
            return
        if isinstance(statement, DataQuery):
            container_ty = self._lookup(statement.container)
            if self._type_name(container_ty) not in _SEQUENCE_TYPES:
                raise TypeCheckError(
                    f"anveṣaṇam requires list type, got {self._type_name(container_ty)!r}",
                )
            self._require_function_arity(
                statement.predicate_function, 1, context="anveṣaṇam predicate"
            )
            self.env.locals[statement.target] = PrimitiveType("list")
            if self._current_function_effect == "pure":
                resolved = self.resolve_overload(statement.predicate_function, [PrimitiveType("unknown")])
                if resolved is None or resolved.effect == "effectful":
                    raise TypeCheckError(
                        f"Pure function {self._current_function_name!r} cannot call effectful or unknown function {statement.predicate_function!r}",
                    )
            return
        if isinstance(statement, (MatchExpr, RuleInvoke)):
            if isinstance(statement, MatchExpr):
                self._infer_value(statement.subject)
            else:
                if statement.rule_id not in self._rules:
                    raise TypeCheckError(f"Unknown rule {statement.rule_id!r} in niyama-āhvānam")
                self._infer_value(statement.context)
            return
        if isinstance(statement, Yield):
            if self._current_function_name is None:
                raise TypeCheckError("pradānam (yield) is only valid inside a function")
            ty = self._infer_value(statement.value)
            if yield_collector is not None:
                yield_collector.append(ty)
            return
        if isinstance(statement, Return):
            if statement.value is not None:
                ty = self._infer_value(statement.value)
                if return_collector is not None:
                    return_collector.append(ty)
            return
        if isinstance(statement, If):
            self._check_condition(statement.condition)
            self._check_block(
                statement.then_body,
                return_collector=return_collector,
                yield_collector=yield_collector,
            )
            self._check_block(
                statement.else_body,
                return_collector=return_collector,
                yield_collector=yield_collector,
            )
            for condition, body in statement.elif_branches:
                self._check_condition(condition)
                self._check_block(
                    body,
                    return_collector=return_collector,
                    yield_collector=yield_collector,
                )
            return
        if isinstance(statement, (While, Until)):
            self._check_condition(statement.condition)
            self._check_block(
                statement.body,
                return_collector=return_collector,
                yield_collector=yield_collector,
            )
            return
        if isinstance(statement, CountedFor):
            self._infer_value(statement.start)
            self._infer_value(statement.end)
            self.env.locals[statement.counter] = PrimitiveType("i32")
            self._check_block(
                statement.body,
                return_collector=return_collector,
                yield_collector=yield_collector,
            )
            return
        if isinstance(statement, ForEach):
            container_ty = self._lookup(statement.container)
            if self._type_name(container_ty) not in _ITERABLE_TYPES:
                raise TypeCheckError(
                    f"foreach requires iterable type, got {self._type_name(container_ty)!r}",
                )
            self.env.locals[statement.item] = PrimitiveType("unknown")
            self._check_block(
                statement.body,
                return_collector=return_collector,
                yield_collector=yield_collector,
            )
            return
        if isinstance(statement, InfiniteLoop):
            self._check_block(
                statement.body,
                return_collector=return_collector,
                yield_collector=yield_collector,
            )
            return
        if isinstance(statement, (Break, Continue, Defer)):
            return
        if isinstance(statement, Guard):
            self._check_condition(statement.condition)
            self._check_block(
                statement.body,
                return_collector=return_collector,
                yield_collector=yield_collector,
            )
            return
        if isinstance(statement, Match):
            self._infer_value(statement.subject)
            for arm in statement.arms:
                self._check_block(
                    arm.body,
                    return_collector=return_collector,
                    yield_collector=yield_collector,
                )
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
            if self._current_function_effect == "pure" and (
                resolved is None or resolved.effect == "effectful"
            ):
                raise TypeCheckError(
                    f"Pure function {self._current_function_name!r} cannot call effectful or unknown function {statement.name!r}",
                )
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
            if self._current_function_effect == "pure":
                raise TypeCheckError(
                    f"Pure function {self._current_function_name!r} cannot construct class instances",
                )
            if statement.class_name not in self.classes:
                raise TypeCheckError(f"Unknown class {statement.class_name!r}")
            decl = next((c for c in self.program.classes if c.name == statement.class_name), None)
            if decl is not None and decl.abstract:
                raise TypeCheckError(f"Cannot construct abstract class {statement.class_name!r}")
            init_fn = self._resolve_class_function(statement.class_name, "__init__", statement.args, include_receiver=True)
            if init_fn is not None:
                self._validate_function_args(init_fn, [PrimitiveType(statement.class_name)] + [self._infer_value(arg) for arg in statement.args], "__init__")
            self.env.locals[statement.target] = self.classes[statement.class_name]
            return
        if isinstance(statement, MethodCall):
            if self._current_function_effect == "pure":
                raise TypeCheckError(
                    f"Pure function {self._current_function_name!r} cannot call instance methods",
                )
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
            fn = self._resolve_class_function(receiver_name, statement.method, statement.args, include_receiver=True)
            arg_types = [PrimitiveType(receiver_name)] + [self._infer_value(arg) for arg in statement.args]
            if fn is not None:
                self._validate_function_args(fn, arg_types, f"{receiver_name}.{statement.method}")
                self.env.locals[statement.target] = self._function_return_type(fn)
            else:
                self.env.locals[statement.target] = PrimitiveType("unknown")
            return
        if isinstance(statement, StaticMethodCall):
            if self._current_function_effect == "pure":
                raise TypeCheckError(
                    f"Pure function {self._current_function_name!r} cannot call static methods",
                )
            if statement.class_name not in self.classes:
                raise TypeCheckError(f"Unknown class {statement.class_name!r}")
            from .oop import resolve_static_method
            if resolve_static_method(statement.class_name, statement.method, self._class_meta) is None:
                raise TypeCheckError(
                    f"Class {statement.class_name!r} has no static method {statement.method!r}",
                )
            fn = self._resolve_class_function(
                statement.class_name,
                statement.method,
                statement.args,
                include_receiver=False,
                call_kind="static",
            )
            if fn is not None:
                arg_types = [self._infer_value(arg) for arg in statement.args]
                self._validate_function_args(fn, arg_types, f"{statement.class_name}.{statement.method}")
                self.env.locals[statement.target] = self._function_return_type(fn)
            else:
                self.env.locals[statement.target] = PrimitiveType("unknown")
            return
        if isinstance(statement, ClassMethodCall):
            if self._current_function_effect == "pure":
                raise TypeCheckError(
                    f"Pure function {self._current_function_name!r} cannot call class methods",
                )
            if statement.class_name not in self.classes:
                raise TypeCheckError(f"Unknown class {statement.class_name!r}")
            from .oop import resolve_class_method
            if resolve_class_method(statement.class_name, statement.method, self._class_meta) is None:
                raise TypeCheckError(
                    f"Class {statement.class_name!r} has no class method {statement.method!r}",
                )
            fn = self._resolve_class_function(
                statement.class_name,
                statement.method,
                statement.args,
                include_receiver=True,
                call_kind="class",
            )
            if fn is not None:
                arg_types = [PrimitiveType("text")] + [self._infer_value(arg) for arg in statement.args]
                self._validate_function_args(fn, arg_types, f"{statement.class_name}.{statement.method}")
                self.env.locals[statement.target] = self._function_return_type(fn)
            else:
                self.env.locals[statement.target] = PrimitiveType("unknown")
            return
        if isinstance(statement, PropertyGet):
            receiver_ty = self._lookup(statement.receiver)
            receiver_name = self._type_name(receiver_ty)
            class_meta = self._class_meta.get(receiver_name)
            if class_meta is None:
                raise TypeCheckError(f"Property receiver {statement.receiver!r} is not a class instance")
            computed_props = getattr(class_meta, "computed_properties", ())
            if statement.property_name not in computed_props:
                raise TypeCheckError(
                    f"Class {receiver_name!r} has no computed property {statement.property_name!r}",
                )
            getter = self._resolve_class_function(
                receiver_name,
                f"get_{statement.property_name}",
                (),
                include_receiver=True,
                call_kind="instance",
            )
            self.env.locals[statement.target] = self._function_return_type(getter) if getter is not None else PrimitiveType("unknown")
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
            if self._type_name(left_ty) == "unknown" or self._type_name(right_ty) == "unknown":
                return
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
            if value.name in self.env.moved:
                raise TypeCheckError(
                    f"Use of moved value {value.name!r}",
                    hint="Move creates exclusive transfer; use the new owner binding.",
                )
            return self._lookup(value.name)
        if isinstance(value, CallValue):
            args = value.args
            # Backward compatibility for older positional construction:
            # CallValue(name, (arg1, arg2)) where tuple was passed into module slot.
            if not args and isinstance(value.module, tuple):
                args = value.module
            arg_types = [self._infer_value(arg) for arg in args]
            resolved = self.resolve_overload(value.name, arg_types)
            if self._current_function_effect == "pure" and (
                resolved is None or resolved.effect == "effectful"
            ):
                raise TypeCheckError(
                    f"Pure function {self._current_function_name!r} cannot call effectful or unknown function {value.name!r}",
                )
            if resolved is not None:
                if resolved.param_types:
                    for index, param_ty_name in enumerate(resolved.param_types):
                        if index >= len(arg_types) or not param_ty_name:
                            continue
                        expected = self._resolve_type_name(param_ty_name)
                        if not self._param_accepts(expected, arg_types[index]):
                            raise TypeCheckError(
                                f"Argument {index + 1} to {value.name!r}: "
                                f"expected {param_ty_name!r}, got {self._type_name(arg_types[index])!r}",
                            )
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

    def _check_can_move(self, source_name: str) -> None:
        if source_name not in self.env.locals and source_name not in self.env.constants:
            raise TypeCheckError(f"Cannot move unknown value {source_name!r}")
        if source_name in self.env.borrow_source:
            raise TypeCheckError(
                f"Cannot move borrow alias {source_name!r}",
                hint="Move the owner binding instead of a borrowed alias.",
            )
        if self._has_active_borrows(source_name):
            raise TypeCheckError(
                f"Cannot move {source_name!r} while it is borrowed",
            )
        if source_name in self.env.moved:
            raise TypeCheckError(f"Value {source_name!r} was already moved")

    def _has_active_borrows(self, owner: str) -> bool:
        return any(
            src == owner and self._is_borrow_binding_active(borrow_name)
            for borrow_name, src in self.env.borrow_source.items()
        )

    def _is_borrow_binding_active(self, borrow_name: str) -> bool:
        if borrow_name not in self.env.borrow_source:
            return False
        depth = self._borrow_scope_depth.get(borrow_name, 0)
        return depth <= self._scope_depth

    def _check_borrow_rules(
        self,
        source_name: str,
        target_name: str,
        *,
        mutable: bool,
        lifetime: str | None,
    ) -> None:
        if source_name not in self.env.locals and source_name not in self.env.constants:
            raise TypeCheckError(f"Cannot borrow unknown value {source_name!r}")
        if source_name in self.env.moved:
            raise TypeCheckError(f"Cannot borrow moved value {source_name!r}")
        if source_name == target_name:
            raise TypeCheckError("Borrow target must differ from source")
        if mutable and source_name in self.env.immutable:
            raise TypeCheckError(
                f"Cannot create mutable borrow of immutable binding {source_name!r}",
            )
        if source_name in self.env.borrow_source and mutable:
            raise TypeCheckError(
                f"Cannot create mutable reborrow from borrow alias {source_name!r}",
            )
        if mutable and self._has_active_borrows(source_name):
            raise TypeCheckError(
                f"Cannot create mutable borrow of {source_name!r} while borrows are active",
            )
        if not mutable:
            for borrow_name, src in self.env.borrow_source.items():
                if (
                    src == source_name
                    and self._is_borrow_binding_active(borrow_name)
                    and self.env.ownership.get(borrow_name) == "borrow_mut"
                ):
                    raise TypeCheckError(
                        f"Cannot create shared borrow of {source_name!r} while mutable borrow {borrow_name!r} is active",
                    )
        owner_lifetime = self.env.lifetimes.get(source_name)
        if lifetime and owner_lifetime and lifetime != owner_lifetime:
            raise TypeCheckError(
                f"Borrow lifetime {lifetime!r} does not match owner lifetime {owner_lifetime!r} for {source_name!r}",
            )
        if lifetime:
            borrow_decl = self.lifetimes.get(lifetime)
            owner_decl = self.lifetimes.get(owner_lifetime) if owner_lifetime else None
            if borrow_decl is not None and owner_decl is not None:
                borrow_region = borrow_decl.region or "global"
                owner_region = owner_decl.region or "global"
                if borrow_region != owner_region:
                    raise TypeCheckError(
                        f"Borrow lifetime region {borrow_region!r} does not match owner region {owner_region!r} for {source_name!r}",
                    )

    def _function_return_type(self, function: FunctionDef | None) -> TypeExpr:
        if function is None:
            return PrimitiveType("unknown")
        if function.return_type:
            return self._resolve_type_name(function.return_type)
        return self.get_inferred_return_type(function.name)

    def _validate_function_args(self, function: FunctionDef, arg_types: list[TypeExpr], call_name: str) -> None:
        if not function.param_types:
            return
        for index, param_ty_name in enumerate(function.param_types):
            if index >= len(arg_types) or not param_ty_name:
                continue
            expected = self._resolve_type_name(param_ty_name)
            if not self._param_accepts(expected, arg_types[index]):
                raise TypeCheckError(
                    f"Argument {index + 1} to {call_name!r}: expected {param_ty_name!r}, got {self._type_name(arg_types[index])!r}",
                )

    def _resolve_class_function(
        self,
        class_name: str,
        method_name: str,
        args: tuple[Value, ...],
        *,
        include_receiver: bool,
        call_kind: str = "instance",
    ) -> FunctionDef | None:
        from .oop import method_symbol, resolve_class_method, resolve_instance_method, resolve_static_method

        available = frozenset(self._functions.keys())
        candidates: list[str] = []
        if call_kind == "instance":
            resolved = resolve_instance_method(
                class_name,
                method_name,
                self._class_meta,
                functions=available,
            )
            if resolved is not None:
                candidates.append(resolved)
            candidates.append(method_symbol(class_name, method_name))
        elif call_kind == "static":
            resolved = resolve_static_method(
                class_name,
                method_name,
                self._class_meta,
                functions=available,
            )
            if resolved is not None:
                candidates.append(resolved)
            candidates.append(method_symbol(class_name, method_name, static=True))
        elif call_kind == "class":
            resolved = resolve_class_method(
                class_name,
                method_name,
                self._class_meta,
                functions=available,
            )
            if resolved is not None:
                candidates.append(resolved)
            candidates.append(method_symbol(class_name, method_name))
        else:
            raise TypeCheckError(f"Unknown class call kind {call_kind!r}")
        if method_name.startswith("__"):
            candidates.append(f"{class_name}{method_name}")
        deduped_candidates = list(dict.fromkeys(candidates))
        arg_types = [self._infer_value(arg) for arg in args]
        if include_receiver:
            arg_types = [PrimitiveType(class_name)] + arg_types
        for candidate in deduped_candidates:
            resolved = self.resolve_overload(candidate, arg_types)
            if resolved is not None:
                return resolved
        return None

    def _current_class_name(self) -> str | None:
        if self._current_function_name is None:
            return None
        name = self._current_function_name
        if "__static__" in name:
            return name.split("__static__", 1)[0]
        if "__" in name:
            return name.split("__", 1)[0]
        return None

    @staticmethod
    def _literal_text(value: Value) -> str | None:
        if isinstance(value, TextLiteral):
            return value.value
        return None

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
        if self._type_name(actual) == "unknown":
            return True
        if self._types_compatible(actual, expected, for_equality=False):
            return True
        if isinstance(expected, ClassInstanceType) and isinstance(actual, ClassInstanceType):
            actual_meta = self._class_meta.get(actual.name)
            if actual_meta is not None and expected.name in getattr(actual_meta, "mro", ()):
                return True
        if isinstance(expected, RecordNominalType) and isinstance(actual, RecordNominalType):
            return self._structural_match(actual, expected)
        return False

    def _function_contains_yield(self, function: FunctionDef) -> bool:
        from .ast import (
            CountedFor,
            ForEach,
            Guard,
            If,
            InfiniteLoop,
            Match,
            Until,
            While,
            Yield,
        )

        def block_has_yield(statements: tuple[object, ...]) -> bool:
            for statement in statements:
                if isinstance(statement, Yield):
                    return True
                if isinstance(statement, If):
                    if block_has_yield(statement.then_body) or block_has_yield(statement.else_body):
                        return True
                    for _cond, body in statement.elif_branches:
                        if block_has_yield(body):
                            return True
                elif isinstance(statement, (While, Until, CountedFor, ForEach, InfiniteLoop, Guard)):
                    if block_has_yield(statement.body):
                        return True
                elif isinstance(statement, Match):
                    for arm in statement.arms:
                        if block_has_yield(arm.body):
                            return True
            return False

        return block_has_yield(function.body)

    def _check_block(
        self,
        statements: tuple[object, ...],
        *,
        return_collector: list[TypeExpr] | None = None,
        yield_collector: list[TypeExpr] | None = None,
        function_for_effect: FunctionDef | None = None,
    ) -> None:
        self._scope_depth += 1
        try:
            for statement in statements:
                self._check_statement(
                    statement,
                    return_collector=return_collector,
                    yield_collector=yield_collector,
                )
                if function_for_effect is not None:
                    self._check_effect_statement(function_for_effect, statement)
        finally:
            self._scope_depth -= 1
            expired = [
                name
                for name, depth in self._borrow_scope_depth.items()
                if depth > self._scope_depth
            ]
            for name in expired:
                self.env.borrow_source.pop(name, None)
                self._borrow_scope_depth.pop(name, None)

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

    def get_inferred_yield_type(self, function_name: str) -> TypeExpr:
        yields = self._inferred_yields.get(function_name, [])
        if not yields:
            function = next((fn for fn in self.program.functions if fn.name == function_name), None)
            if function is not None:
                collected: list[TypeExpr] = []
                self._collect_function_yields(function.body, collected)
                yields = collected
        if not yields:
            return PrimitiveType("unknown")
        return yields[0] if len(yields) == 1 else self._unify_types(yields)

    def _has_type_suffix(self, suffix: str) -> bool:
        parts = [part for part in suffix.split("_") if part]
        if not parts:
            return False
        for part in parts:
            if part in _BUILTIN_TYPES:
                continue
            if part in self.aliases or part in self.newtypes or part in self.records or part in self.classes:
                continue
            try:
                self.catalog.by_name(part)
                continue
            except Exception:
                return False
        return True

    def _collect_function_yields(
        self,
        statements: tuple[object, ...],
        collector: list[TypeExpr],
    ) -> None:
        from .ast import CountedFor, ForEach, Guard, If, InfiniteLoop, Match, Until, While, Yield

        for statement in statements:
            if isinstance(statement, Yield):
                collector.append(self._infer_value(statement.value))
            elif isinstance(statement, If):
                self._collect_function_yields(statement.then_body, collector)
                self._collect_function_yields(statement.else_body, collector)
                for _cond, body in statement.elif_branches:
                    self._collect_function_yields(body, collector)
            elif isinstance(statement, (While, Until, CountedFor, ForEach, InfiniteLoop, Guard)):
                self._collect_function_yields(statement.body, collector)
            elif isinstance(statement, Match):
                for arm in statement.arms:
                    self._collect_function_yields(arm.body, collector)

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
