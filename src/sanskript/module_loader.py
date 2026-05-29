from __future__ import annotations

from pathlib import Path

from .ast import Program
from .errors import CompileError
from .package_manifest import validate_manifest_features
from .package_resolver import (
    PackageContext,
    build_package_context,
    package_init_paths,
    register_import_binding,
    resolve_import_path,
)
from .parser import parse_program


def load_program_from_path(entry_path: Path, *, profile: str | None = None) -> Program:
    entry = entry_path.resolve()
    if not entry.exists():
        raise CompileError(f"Source file not found: {entry}")
    ctx = build_package_context(entry, profile=profile)
    loaded = _load_recursive(entry, ctx=ctx, visiting=[], entry=entry)
    return loaded


def _load_recursive(path: Path, *, ctx: PackageContext, visiting: list[Path], entry: Path) -> Program:
    resolved = path.resolve()
    if resolved in visiting:
        cycle = " -> ".join(str(item.name) for item in [*visiting, resolved])
        raise CompileError(f"Cyclic imports detected: {cycle}")
    visiting.append(resolved)
    programs: list[Program] = []
    for init_path in package_init_paths(resolved):
        if init_path not in visiting:
            programs.append(_load_recursive(init_path, ctx=ctx, visiting=visiting, entry=entry))
    source = resolved.read_text(encoding="utf-8")
    current = parse_program(source)
    merged = _merge_programs([*programs, current])
    for directive in current.imports:
        if directive.required_features:
            validate_manifest_features(ctx.manifest, directive.required_features)
        target_path = resolve_import_path(ctx, resolved.parent, directive.module_path)
        register_import_binding(
            ctx,
            directive.alias or _default_binding_name(directive.module_path),
            target_path,
        )
        dep = _load_recursive(target_path, ctx=ctx, visiting=visiting, entry=entry)
        merged = _merge_programs([merged, dep])
    visiting.pop()
    keep_imports = current.imports if resolved == entry.resolve() else ()
    return Program(
        tuple(merged.statements),
        tuple(merged.functions),
        tuple(merged.modules),
        imports=tuple(keep_imports),
        safety_tier=merged.safety_tier,
        type_aliases=tuple(merged.type_aliases),
        newtypes=tuple(merged.newtypes),
        record_types=tuple(merged.record_types),
        constants=tuple(merged.constants),
        generic_records=tuple(merged.generic_records),
        traits=tuple(merged.traits),
        trait_impls=tuple(merged.trait_impls),
        classes=tuple(merged.classes),
        lifetimes=tuple(merged.lifetimes),
        algebraic_types=tuple(merged.algebraic_types),
        rules=tuple(merged.rules),
    )


def _default_binding_name(module_path: str) -> str:
    cleaned = module_path.replace("\\", "/").rstrip("/")
    if "/" in cleaned:
        cleaned = cleaned.rsplit("/", 1)[-1]
    if cleaned.startswith("@"):
        cleaned = cleaned.split("/")[-1]
    if "." in cleaned and not cleaned.endswith(".ssk"):
        cleaned = cleaned.rsplit(".", 1)[-1]
    if cleaned.endswith(".ssk"):
        cleaned = cleaned[:-4]
    return cleaned


def _merge_programs(programs: list[Program]) -> Program:
    merged_modules: list = []
    merged_functions: list = []
    merged_statements: list = []
    merged_aliases: list = []
    merged_newtypes: list = []
    merged_record_types: list = []
    merged_constants: list = []
    merged_generics: list = []
    merged_traits: list = []
    merged_trait_impls: list = []
    merged_classes: list = []
    merged_lifetimes: list = []
    merged_algebraic: list = []
    merged_rules: list = []
    safety_tier = "surakshita"
    for current in programs:
        safety_tier = current.safety_tier
        for module in current.modules:
            if all(existing.name != module.name for existing in merged_modules):
                merged_modules.append(module)
        # Preserve function overload sets (same logical name, different arity/signature).
        # Deduplicating by name drops valid overloads and changes call resolution.
        merged_functions.extend(current.functions)
        merged_statements.extend(current.statements)
        merged_aliases.extend(current.type_aliases)
        merged_newtypes.extend(current.newtypes)
        merged_record_types.extend(current.record_types)
        merged_constants.extend(current.constants)
        merged_generics.extend(current.generic_records)
        merged_traits.extend(current.traits)
        merged_trait_impls.extend(current.trait_impls)
        merged_classes.extend(current.classes)
        merged_lifetimes.extend(current.lifetimes)
        merged_algebraic.extend(current.algebraic_types)
        merged_rules.extend(current.rules)
    return Program(
        tuple(merged_statements),
        tuple(merged_functions),
        tuple(merged_modules),
        safety_tier=safety_tier,
        type_aliases=tuple(merged_aliases),
        newtypes=tuple(merged_newtypes),
        record_types=tuple(merged_record_types),
        constants=tuple(merged_constants),
        generic_records=tuple(merged_generics),
        traits=tuple(merged_traits),
        trait_impls=tuple(merged_trait_impls),
        classes=tuple(merged_classes),
        lifetimes=tuple(merged_lifetimes),
        algebraic_types=tuple(merged_algebraic),
        rules=tuple(merged_rules),
    )


__all__ = ["load_program_from_path"]
