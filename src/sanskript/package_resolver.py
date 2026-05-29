from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

from .errors import CompileError
from .package_lock import PackageLock, load_lock, resolve_locked_path
from .package_manifest import (
    DependencySpec,
    PackageManifest,
    find_manifest_path,
    load_manifest,
    load_manifest_for_path,
    validate_manifest_features,
)
from .package_signing import verify_package_signature

PACKAGE_INIT_NAMES = ("samārambha.ssk", "samarambha.ssk", "__init__.ssk")
REGISTRY_CACHE_DIR = ".ssk/registry"


@dataclass
class PackageContext:
    root: Path
    manifest: PackageManifest
    manifest_path: Path | None
    lock: PackageLock | None
    stdlib_root: Path
    active_profile: str = "debug"
    import_bindings: dict[str, Path] = field(default_factory=dict)

    @property
    def enabled_features(self) -> frozenset[str]:
        return self.manifest.enabled_features()

    @property
    def platform(self) -> str:
        if sys.platform.startswith("win"):
            return "windows"
        if sys.platform == "darwin":
            return "macos"
        if sys.platform.startswith("linux"):
            return "linux"
        return sys.platform


def build_package_context(entry: Path, *, profile: str | None = None) -> PackageContext:
    entry = entry.resolve()
    manifest_path = find_manifest_path(entry)
    if manifest_path is None:
        root = entry.parent if entry.is_file() else entry
        manifest = load_manifest_for_path(entry)[0]
    else:
        root = manifest_path.parent
        manifest = load_manifest(manifest_path)
    lock = load_lock(root)
    _validate_security_requirements(manifest, lock)
    verify_package_signature(root, manifest.signature)
    stdlib_root = _stdlib_root()
    ctx = PackageContext(
        root=root,
        manifest=manifest,
        manifest_path=manifest_path,
        lock=lock,
        stdlib_root=stdlib_root,
        active_profile=profile or os.environ.get("SANSKRIPT_PROFILE", "debug"),
    )
    _apply_profile(ctx)
    _preload_manifest_dependencies(ctx)
    _apply_platform_modules(ctx)
    return ctx


def resolve_import_path(ctx: PackageContext, base_dir: Path, module_path: str) -> Path:
    cleaned = module_path.replace("\\", "/").strip()
    if cleaned.startswith("@"):
        return _resolve_absolute(ctx, cleaned[1:])
    if cleaned.startswith("./") or cleaned.startswith("../"):
        return _resolve_relative(base_dir, cleaned)
    if cleaned.startswith("/"):
        return _resolve_project_absolute(ctx, cleaned.lstrip("/"))
    if "." in cleaned and "/" not in cleaned and not cleaned.endswith(".ssk"):
        return _resolve_dotted(ctx, base_dir, cleaned)
    return _resolve_file_candidate(base_dir, cleaned)


def package_init_paths(target: Path) -> list[Path]:
    directory = target.parent if target.suffix == ".ssk" else target
    if not directory.is_dir():
        directory = directory.parent
    inits: list[Path] = []
    for name in PACKAGE_INIT_NAMES:
        candidate = directory / name
        if candidate.is_file() and candidate.resolve() != target.resolve():
            inits.append(candidate.resolve())
    return inits


def register_import_binding(ctx: PackageContext, local_name: str, resolved: Path) -> None:
    key = local_name.strip()
    previous = ctx.import_bindings.get(key)
    if previous is not None and previous.resolve() != resolved.resolve():
        raise CompileError(
            f"Import name conflict: {key!r} resolves to both {previous} and {resolved}",
            hint="Use distinct aliases (nāmnā) or rename modules.",
            code="SANSKRIPT_IMPORT_CONFLICT",
        )
    ctx.import_bindings[key] = resolved.resolve()


def resolve_registry_dependency(ctx: PackageContext, spec: DependencySpec) -> Path:
    lock_entry = _lock_entry_for(ctx.lock, spec.name)
    if lock_entry is not None:
        if lock_entry.kind != "registry":
            raise CompileError(
                f"Lock kind mismatch for registry dependency {spec.name!r}: {lock_entry.kind}",
                hint="Regenerate ssk.lock so dependency kinds match ssk.toml.",
            )
        return resolve_locked_path(
            ctx.root,
            ctx.manifest,
            ctx.lock,
            spec.name,
            fallback_path=ctx.root / ctx.manifest.vendor_dir / spec.name,
            expected_kind="registry",
        )
    cache = ctx.root / REGISTRY_CACHE_DIR / spec.registry / spec.name
    version = spec.version or "0.0.0"
    marker = cache / version / ".resolved"
    if marker.is_file():
        marker_value = marker.read_text(encoding="utf-8").strip()
        target = Path(marker_value)
        if not target.is_absolute():
            target = (cache / version / marker_value).resolve()
        else:
            target = target.resolve()
        if cache.resolve() in {target, *target.parents} and target.exists():
            return target
    vendored = ctx.root / ctx.manifest.vendor_dir / spec.name
    if vendored.exists():
        return vendored.resolve()
    raise CompileError(
        f"Registry dependency {spec.name!r}@{version} is not installed",
        hint=f"Vendor it under {ctx.manifest.vendor_dir}/{spec.name} or add a lock entry.",
    )


def _stdlib_root() -> Path:
    env = os.environ.get("SANSKRIPT_STDLIB")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parents[2] / "data" / "stdlib"


def _apply_profile(ctx: PackageContext) -> None:
    profile = next((item for item in ctx.manifest.profiles if item.name == ctx.active_profile), None)
    if profile is None:
        return
    required = profile.options.get("requires")
    if required:
        flags = frozenset(part.strip() for part in required.split(",") if part.strip())
        validate_manifest_features(ctx.manifest, flags)


def _preload_manifest_dependencies(ctx: PackageContext) -> None:
    for dep in ctx.manifest.dependencies:
        lock_entry = _lock_entry_for(ctx.lock, dep.name)
        if lock_entry is not None and lock_entry.kind != dep.kind:
            raise CompileError(
                f"Lock kind mismatch for dependency {dep.name!r}: manifest={dep.kind}, lock={lock_entry.kind}",
                hint="Regenerate ssk.lock so dependency kinds match ssk.toml.",
            )
        if dep.kind == "local":
            if dep.path is None:
                continue
            resolved = resolve_locked_path(
                ctx.root,
                ctx.manifest,
                ctx.lock,
                dep.name,
                fallback_path=ctx.root / dep.path,
                expected_kind="local",
            )
            register_import_binding(ctx, dep.name, resolved)
        elif dep.kind == "vendored":
            if dep.path is None:
                path = ctx.root / ctx.manifest.vendor_dir / dep.name
            else:
                path = ctx.root / dep.path
            resolved = resolve_locked_path(
                ctx.root,
                ctx.manifest,
                ctx.lock,
                dep.name,
                fallback_path=path,
                expected_kind="vendored",
            )
            register_import_binding(ctx, dep.name, resolved)
        elif dep.kind == "registry":
            resolved = resolve_registry_dependency(ctx, dep)
            register_import_binding(ctx, dep.name, resolved)


def _validate_security_requirements(manifest: PackageManifest, lock: PackageLock | None) -> None:
    needs_lock = manifest.lock_required or any(dep.kind in {"registry", "vendored"} or dep.locked for dep in manifest.dependencies)
    if needs_lock and lock is None:
        raise CompileError(
            "Dependency lock is required but ssk.lock is missing",
            hint="Generate and commit ssk.lock for reproducible dependency resolution.",
            code="SANSKRIPT_LOCK_REQUIRED",
        )
    if manifest.signature_required and not manifest.signature:
        raise CompileError(
            "Package signature is required but missing from manifest",
            hint="Set [package].signature after signing the package with sign_package().",
            code="SANSKRIPT_SIGNATURE_REQUIRED",
        )
    if needs_lock and lock is not None:
        manifest_names = {dep.name for dep in manifest.dependencies}
        lock_names = {item.name for item in lock.dependencies}
        missing = sorted(manifest_names - lock_names)
        extra = sorted(lock_names - manifest_names)
        if missing:
            raise CompileError(
                f"Lockfile is missing dependency entries: {', '.join(missing)}",
                hint="Regenerate ssk.lock from current manifest dependencies.",
                code="SANSKRIPT_LOCK_INCOMPLETE",
            )
        if extra:
            raise CompileError(
                f"Lockfile has unexpected dependency entries: {', '.join(extra)}",
                hint="Regenerate ssk.lock from current manifest dependencies.",
                code="SANSKRIPT_LOCK_INCOMPLETE",
            )
        hash_required = {dep.name for dep in manifest.dependencies if dep.locked or dep.kind in {"vendored", "registry"}}
        hash_missing = sorted(item.name for item in lock.dependencies if item.name in hash_required and not item.sha256)
        if hash_missing:
            raise CompileError(
                f"Lockfile entries missing sha256: {', '.join(hash_missing)}",
                hint="Regenerate ssk.lock with deterministic hashes for vendored/registry/locked dependencies.",
                code="SANSKRIPT_LOCK_INCOMPLETE",
            )
        if lock.package_name != manifest.name or lock.package_version != manifest.version:
            raise CompileError(
                "Lockfile package identity does not match manifest",
                hint="Regenerate ssk.lock after changing [package] name or version.",
                code="SANSKRIPT_LOCK_IDENTITY",
            )
        if manifest.signature_required:
            if not lock.signature:
                raise CompileError(
                    "Lockfile signature missing while signature_required is enabled",
                    hint="Regenerate ssk.lock with the active manifest signature.",
                    code="SANSKRIPT_LOCK_SIGNATURE",
                )
            if lock.signature != manifest.signature:
                raise CompileError(
                    "Lockfile signature does not match manifest signature",
                    hint="Regenerate ssk.lock after updating [package].signature.",
                    code="SANSKRIPT_LOCK_SIGNATURE",
                )


def _lock_entry_for(lock: PackageLock | None, name: str):
    if lock is None:
        return None
    return next((item for item in lock.dependencies if item.name == name), None)


def _apply_platform_modules(ctx: PackageContext) -> None:
    active_platforms = {ctx.platform, sys.platform}
    for spec in ctx.manifest.platform_modules:
        if spec.platform not in active_platforms:
            continue
        resolved = _resolve_file_candidate(ctx.root, spec.module_path)
        alias = _default_binding_name(spec.module_path)
        register_import_binding(ctx, alias, resolved)


def _resolve_absolute(ctx: PackageContext, path: str) -> Path:
    cleaned = path.replace("\\", "/").lstrip("/")
    if cleaned.startswith("stdlib/") or cleaned.split("/", 1)[0] == ctx.manifest.stdlib_namespace:
        remainder = cleaned.split("/", 1)[-1] if "/" in cleaned else cleaned
        if cleaned.startswith("stdlib/"):
            remainder = cleaned[len("stdlib/") :]
        return _resolve_file_candidate(ctx.stdlib_root, remainder)
    if cleaned.startswith(f"{ctx.manifest.user_namespace}/") or cleaned.split("/", 1)[0] == ctx.manifest.user_namespace:
        remainder = cleaned.split("/", 1)[-1]
        return _resolve_file_candidate(ctx.root / ctx.manifest.user_namespace, remainder)
    return _resolve_project_absolute(ctx, cleaned)


def _resolve_project_absolute(ctx: PackageContext, path: str) -> Path:
    return _resolve_file_candidate(ctx.root, path)


def _resolve_relative(base_dir: Path, path: str) -> Path:
    relative = Path(path)
    if path.endswith(".ssk"):
        candidate = (base_dir / relative).resolve()
        if candidate.exists():
            return candidate
        raise CompileError(
            f"Cannot resolve relative import {path!r} from {base_dir}",
            hint="Check ./ and ../ segments point at an existing .ssk file.",
        )
    candidate = (base_dir / Path(path + ".ssk")).resolve()
    if candidate.exists():
        return candidate
    package = (base_dir / path / "samārambha.ssk").resolve()
    if package.exists():
        return package
    package = (base_dir / path / "__init__.ssk").resolve()
    if package.exists():
        return package
    raise CompileError(
        f"Cannot resolve relative import {path!r} from {base_dir}",
        hint="Use ./file.ssk, ../pkg/module, or a package directory with samārambha.ssk.",
    )


def _resolve_dotted(ctx: PackageContext, base_dir: Path, path: str) -> Path:
    parts = path.split(".")
    if parts[0] in ctx.import_bindings:
        base = ctx.import_bindings[parts[0]]
        if base.is_file():
            base = base.parent
        remainder = "/".join(parts[1:])
        if remainder:
            return _resolve_file_candidate(base, remainder)
        return base
    relative = Path(*parts).with_suffix(".ssk")
    candidate = (base_dir / relative).resolve()
    if candidate.exists():
        return candidate
    candidate = (ctx.root / relative).resolve()
    if candidate.exists():
        return candidate
    raise CompileError(
        f"Cannot resolve dotted import {path!r}",
        hint="Use package.module paths relative to the importer or project root.",
    )


def _resolve_file_candidate(base_dir: Path, module_path: str) -> Path:
    if module_path.endswith(".ssk"):
        relative = Path(module_path)
    elif "/" in module_path or "\\" in module_path:
        relative = Path(module_path + ".ssk")
    else:
        relative = Path(*module_path.split(".")).with_suffix(".ssk")
    candidate = (base_dir / relative).resolve()
    if candidate.exists():
        return candidate
    platform_candidate = _platform_specific_candidate(base_dir, module_path)
    if platform_candidate is not None:
        return platform_candidate
    raise CompileError(
        f"Cannot resolve import {module_path!r} from {base_dir}",
        hint="Use @stdlib/…, @lib/…, @root/…, relative, or dotted package paths.",
    )


def _platform_specific_candidate(base_dir: Path, module_path: str) -> Path | None:
    stem = module_path.replace("\\", "/").rstrip("/")
    if stem.endswith(".ssk"):
        stem = stem[:-4]
    for suffix in (f"{sys.platform}.ssk", f"{_platform_tag()}.ssk"):
        candidate = (base_dir / f"{stem}.{suffix}").resolve()
        if candidate.exists():
            return candidate
    return None


def _platform_tag() -> str:
    if sys.platform.startswith("win"):
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    if sys.platform.startswith("linux"):
        return "linux"
    return sys.platform


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


__all__ = [
    "PACKAGE_INIT_NAMES",
    "PackageContext",
    "build_package_context",
    "package_init_paths",
    "register_import_binding",
    "resolve_import_path",
    "resolve_registry_dependency",
]
