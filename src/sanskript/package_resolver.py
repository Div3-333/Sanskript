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
    cache = ctx.root / REGISTRY_CACHE_DIR / spec.registry / spec.name
    version = spec.version or "0.0.0"
    marker = cache / version / ".resolved"
    if marker.is_file():
        target = Path(marker.read_text(encoding="utf-8").strip())
        if target.exists():
            return target.resolve()
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
        if dep.kind == "local":
            if dep.path is None:
                continue
            resolved = resolve_locked_path(
                ctx.root,
                ctx.manifest,
                ctx.lock,
                dep.name,
                fallback_path=ctx.root / dep.path,
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
            )
            register_import_binding(ctx, dep.name, resolved)
        elif dep.kind == "registry":
            resolved = resolve_registry_dependency(ctx, dep)
            register_import_binding(ctx, dep.name, resolved)


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


__all__ = [
    "PACKAGE_INIT_NAMES",
    "PackageContext",
    "build_package_context",
    "package_init_paths",
    "register_import_binding",
    "resolve_import_path",
    "resolve_registry_dependency",
]
