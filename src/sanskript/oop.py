"""Phase 7 object model: classes, dispatch, protocols, visibility."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from .ast import ClassDecl, Program
    from .bytecode import BytecodeProgram

# Standard protocol trait names (nominal; methods listed in trait declarations).
PROTOCOL_EQUALITY = "Samānatā"
PROTOCOL_ORDERING = "Kramanirṇaya"
PROTOCOL_HASHING = "Saṅkhyābandha"
PROTOCOL_DISPLAY = "Darśana"
PROTOCOL_ITERATION = "Anukrama"
PROTOCOL_CONTEXT = "Sandarbha"
PROTOCOL_SERIALIZATION = "Saṃkīrtana"

STANDARD_PROTOCOLS: tuple[str, ...] = (
    PROTOCOL_EQUALITY,
    PROTOCOL_ORDERING,
    PROTOCOL_HASHING,
    PROTOCOL_DISPLAY,
    PROTOCOL_ITERATION,
    PROTOCOL_CONTEXT,
    PROTOCOL_SERIALIZATION,
)

# Expected method names on classes implementing each protocol (operator-like, named only).
PROTOCOL_METHODS: dict[str, tuple[str, ...]] = {
    PROTOCOL_EQUALITY: ("samāna",),
    PROTOCOL_ORDERING: ("pūrva", "anantara"),
    PROTOCOL_HASHING: ("saṅkhyābandha",),
    PROTOCOL_DISPLAY: ("darśaya",),
    PROTOCOL_ITERATION: ("agream", "antaram"),
    PROTOCOL_CONTEXT: ("praveśa", "niḥsaraṇa"),
    PROTOCOL_SERIALIZATION: ("saṃkīrtana", "visarjana"),
}

_VISIBILITY_ORDER = {"private": 0, "protected": 1, "public": 2}


@dataclass(frozen=True)
class ClassMetadata:
    """Resolved class declaration used by checker, compiler, and VM."""

    name: str
    fields: tuple[tuple[str, str], ...]
    methods: tuple[str, ...]
    static_methods: tuple[str, ...]
    class_methods: tuple[str, ...]
    field_visibility: dict[str, str]
    base_class: str | None
    mixins: tuple[str, ...]
    trait_impls: tuple[str, ...]
    trait_bounds: tuple[tuple[str, str], ...]
    abstract: bool
    sealed: bool
    computed_properties: tuple[str, ...]
    metaclass: str | None
    declared_methods: tuple[str, ...]
    declared_static_methods: tuple[str, ...]
    declared_class_methods: tuple[str, ...]
    mro: tuple[str, ...]


def class_metadata_from_decl(decl: ClassDecl, registry: dict[str, ClassDecl]) -> ClassMetadata:
    """Flatten fields/methods along inheritance and mixin chain."""

    mro: list[str] = []
    seen: set[str] = set()

    def walk(name: str) -> None:
        if name in seen or name not in registry:
            return
        seen.add(name)
        current = registry[name]
        if current.base_class:
            walk(current.base_class)
        for mixin in current.mixins:
            walk(mixin)
        mro.append(name)

    walk(decl.name)

    fields: dict[str, str] = {}
    visibility: dict[str, str] = {}
    methods: list[str] = []
    static_methods: list[str] = []
    class_methods: list[str] = []
    computed: list[str] = []
    trait_impls: list[str] = []
    trait_bounds: list[tuple[str, str]] = []
    abstract = False
    sealed = False
    base_class: str | None = None
    metaclass: str | None = None

    for name in mro:
        current = registry[name]
        if name == decl.name:
            base_class = current.base_class
            abstract = current.abstract
            sealed = current.sealed
            metaclass = current.metaclass
        for field_name, field_type in current.fields:
            fields[field_name] = field_type
            vis = dict(current.field_visibility).get(field_name, "public")
            visibility[field_name] = vis
        for method in current.methods:
            if method not in methods:
                methods.append(method)
        for method in current.static_methods:
            if method not in static_methods:
                static_methods.append(method)
        for method in current.class_methods:
            if method not in class_methods:
                class_methods.append(method)
        for prop in current.computed_properties:
            if prop not in computed:
                computed.append(prop)
        trait_impls.extend(t for t in current.trait_impls if t not in trait_impls)
        trait_bounds.extend(b for b in current.trait_bounds if b not in trait_bounds)

    return ClassMetadata(
        name=decl.name,
        fields=tuple(fields.items()),
        methods=tuple(methods),
        static_methods=tuple(static_methods),
        class_methods=tuple(class_methods),
        field_visibility=visibility,
        base_class=base_class,
        mixins=decl.mixins,
        trait_impls=tuple(trait_impls),
        trait_bounds=tuple(trait_bounds),
        abstract=abstract,
        sealed=sealed,
        computed_properties=tuple(computed),
        metaclass=metaclass,
        declared_methods=tuple(decl.methods),
        declared_static_methods=tuple(decl.static_methods),
        declared_class_methods=tuple(decl.class_methods),
        mro=tuple(reversed(mro)),
    )


def build_class_registry(program: Program) -> dict[str, ClassDecl]:
    return {decl.name: decl for decl in program.classes}


def build_class_metadata(program: Program) -> dict[str, ClassMetadata]:
    registry = build_class_registry(program)
    return {name: class_metadata_from_decl(decl, registry) for name, decl in registry.items()}


def method_symbol(class_name: str, method: str, *, static: bool = False) -> str:
    prefix = f"{class_name}__"
    if static:
        return f"{prefix}static__{method}"
    return f"{prefix}{method}" if not method.startswith("__") else f"{prefix}{method.lstrip('_')}"


def resolve_instance_method(
    class_name: str,
    method: str,
    metadata: dict[str, ClassMetadata],
    *,
    functions: Iterable[str] | None = None,
) -> str | None:
    """Dynamic dispatch: walk MRO (most-derived first) and return the first method symbol."""

    meta = metadata.get(class_name)
    order = meta.mro if meta is not None else (class_name,)
    for candidate in order:
        sub = metadata.get(candidate)
        if sub is None or method not in sub.methods or method not in sub.declared_methods:
            continue
        symbol = method_symbol(candidate, method)
        if functions is None or symbol in functions:
            return symbol
    return None


def resolve_static_method(
    class_name: str,
    method: str,
    metadata: dict[str, ClassMetadata],
    *,
    functions: Iterable[str] | None = None,
) -> str | None:
    meta = metadata.get(class_name)
    order = meta.mro if meta is not None else (class_name,)
    for candidate in order:
        sub = metadata.get(candidate)
        if sub is None or method not in sub.static_methods:
            continue
        if method not in sub.declared_static_methods:
            continue
        symbol = method_symbol(candidate, method, static=True)
        if functions is None or symbol in functions:
            return symbol
    metaclass = _resolve_metaclass(class_name, metadata)
    if metaclass is not None:
        return resolve_static_method(metaclass, method, metadata, functions=functions)
    return None


def resolve_class_method(
    class_name: str,
    method: str,
    metadata: dict[str, ClassMetadata],
    *,
    functions: Iterable[str] | None = None,
) -> str | None:
    meta = metadata.get(class_name)
    order = meta.mro if meta is not None else (class_name,)
    for candidate in order:
        sub = metadata.get(candidate)
        if sub is None or method not in sub.class_methods:
            continue
        if method not in sub.declared_class_methods:
            continue
        symbol = method_symbol(candidate, method, static=False)
        if functions is None or symbol in functions:
            return symbol
    metaclass = _resolve_metaclass(class_name, metadata)
    if metaclass is not None:
        return resolve_class_method(metaclass, method, metadata, functions=functions)
    return None


def _resolve_metaclass(class_name: str, metadata: dict[str, ClassMetadata]) -> str | None:
    seen: set[str] = set()
    current = class_name
    while current and current not in seen:
        seen.add(current)
        meta = metadata.get(current)
        if meta is None:
            return None
        if meta.metaclass:
            return meta.metaclass
        current = meta.base_class
    return None


def check_field_access(
    *,
    class_name: str,
    field: str,
    from_class: str | None,
    metadata: dict[str, ClassMetadata],
) -> None:
    from .errors import TypeCheckError

    meta = metadata.get(class_name)
    if meta is None:
        raise TypeCheckError(f"Unknown class {class_name!r}")
    vis = meta.field_visibility.get(field, "public")
    if vis == "public":
        return
    if from_class is None:
        raise TypeCheckError(f"Field {field!r} on {class_name!r} is {vis} and not accessible here")
    if vis == "protected" and from_class not in meta.mro:
        raise TypeCheckError(f"Protected field {field!r} is not visible from {from_class!r}")
    if vis == "private" and from_class != class_name:
        raise TypeCheckError(f"Private field {field!r} is not visible outside {class_name!r}")


def validate_class_decl(decl: ClassDecl, registry: dict[str, ClassDecl]) -> None:
    from .errors import TypeCheckError

    if decl.base_class and decl.base_class not in registry:
        raise TypeCheckError(f"Unknown base class {decl.base_class!r} for {decl.name!r}")
    if decl.base_class:
        base = registry[decl.base_class]
        if base.sealed:
            raise TypeCheckError(f"Cannot extend sealed class {decl.base_class!r}")
    for mixin in decl.mixins:
        if mixin not in registry:
            raise TypeCheckError(f"Unknown mixin {mixin!r} on class {decl.name!r}")
    if decl.metaclass is not None and decl.metaclass not in registry:
        raise TypeCheckError(f"Unknown metaclass {decl.metaclass!r} on class {decl.name!r}")
    if decl.metaclass == decl.name:
        raise TypeCheckError(f"Class {decl.name!r} cannot be its own metaclass")
    if decl.abstract and not decl.methods and not decl.static_methods:
        raise TypeCheckError(f"Abstract class {decl.name!r} must declare at least one method")


def validate_trait_impl_on_class(
    class_name: str,
    trait_name: str,
    metadata: dict[str, ClassMetadata],
    trait_method_names: dict[str, tuple[str, ...]],
) -> None:
    from .errors import TypeCheckError

    meta = metadata.get(class_name)
    if meta is None:
        raise TypeCheckError(f"Unknown class {class_name!r}")
    required = trait_method_names.get(trait_name, PROTOCOL_METHODS.get(trait_name, ()))
    available = set(meta.methods) | set(meta.static_methods) | set(meta.class_methods)
    for method in required:
        if method not in available:
            raise TypeCheckError(
                f"Class {class_name!r} does not implement trait {trait_name!r}: missing method {method!r}",
            )


def function_names(program: BytecodeProgram) -> frozenset[str]:
    names = {function.name for function in program.functions}
    for module in program.modules:
        for function in module.functions:
            names.add(function.name)
    return frozenset(names)
