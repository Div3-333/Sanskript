from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from .errors import CompileError
from .package_manifest import MANIFEST_TOML, PackageManifest

LOCK_FILE = "ssk.lock"
_ALLOWED_LOCK_KINDS = {"local", "registry", "vendored"}


@dataclass(frozen=True)
class LockedDependency:
    name: str
    kind: str
    resolved_path: str
    version: str | None = None
    sha256: str | None = None


@dataclass(frozen=True)
class PackageLock:
    lock_version: int
    package_name: str
    package_version: str
    dependencies: tuple[LockedDependency, ...]
    signature: str | None = None

    def to_dict(self) -> dict:
        return {
            "lock_version": self.lock_version,
            "package": {"name": self.package_name, "version": self.package_version},
            "dependencies": {
                item.name: {
                    "kind": item.kind,
                    "resolved": item.resolved_path,
                    "version": item.version,
                    "sha256": item.sha256,
                }
                for item in self.dependencies
            },
            "signature": self.signature,
        }


def lock_path_for_root(root: Path) -> Path:
    return root / LOCK_FILE


def load_lock(root: Path) -> PackageLock | None:
    path = lock_path_for_root(root)
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CompileError(f"Invalid {LOCK_FILE}: top-level JSON object required")
    dependencies = data.get("dependencies", {})
    if not isinstance(dependencies, dict):
        raise CompileError(f"Invalid {LOCK_FILE}: dependencies must be an object")
    lock_version = int(data.get("lock_version", 1))
    if lock_version != 1:
        raise CompileError(f"Invalid {LOCK_FILE}: unsupported lock_version {lock_version}")
    deps_list: list[LockedDependency] = []
    for name, entry in dependencies.items():
        if not isinstance(name, str) or not name.strip():
            raise CompileError(f"Invalid {LOCK_FILE}: dependency names must be non-empty strings")
        if not isinstance(entry, dict):
            raise CompileError(f"Invalid {LOCK_FILE}: dependency entry for {name!r} must be an object")
        kind = str(entry.get("kind", "local"))
        if kind not in _ALLOWED_LOCK_KINDS:
            raise CompileError(f"Invalid {LOCK_FILE}: dependency {name!r} has unsupported kind {kind!r}")
        resolved = entry.get("resolved")
        if not isinstance(resolved, str) or not resolved.strip():
            raise CompileError(f"Invalid {LOCK_FILE}: dependency {name!r} must provide a non-empty resolved path")
        sha256 = entry.get("sha256")
        if sha256 is not None:
            if not isinstance(sha256, str) or len(sha256) != 64 or any(ch not in "0123456789abcdef" for ch in sha256):
                raise CompileError(f"Invalid {LOCK_FILE}: dependency {name!r} has malformed sha256")
        deps_list.append(
            LockedDependency(
                name=name,
                kind=kind,
                resolved_path=resolved,
                version=entry.get("version"),
                sha256=sha256,
            )
        )
    deps = tuple(deps_list)
    package = data.get("package", {})
    if not isinstance(package, dict):
        raise CompileError(f"Invalid {LOCK_FILE}: package must be an object")
    package_name = package.get("name", "anonymous")
    package_version = package.get("version", "0.0.0")
    if not isinstance(package_name, str) or not package_name.strip():
        raise CompileError(f"Invalid {LOCK_FILE}: package.name must be a non-empty string")
    if not isinstance(package_version, str) or not package_version.strip():
        raise CompileError(f"Invalid {LOCK_FILE}: package.version must be a non-empty string")
    return PackageLock(
        lock_version=lock_version,
        package_name=package_name,
        package_version=package_version,
        dependencies=deps,
        signature=data.get("signature"),
    )


def write_lock(root: Path, lock: PackageLock) -> Path:
    path = lock_path_for_root(root)
    path.write_text(json.dumps(lock.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def sha256_path(path: Path) -> str:
    if path.is_file():
        return sha256_file(path)
    if not path.is_dir():
        raise CompileError(f"Cannot hash missing dependency path: {path}")
    digest = hashlib.sha256()
    for entry in sorted(path.rglob("*")):
        if not entry.is_file():
            continue
        rel = str(entry.relative_to(path)).replace("\\", "/")
        digest.update(rel.encode("utf-8"))
        digest.update(entry.read_bytes())
    return digest.hexdigest()


def resolve_locked_path(
    root: Path,
    manifest: PackageManifest,
    lock: PackageLock | None,
    dep_name: str,
    *,
    fallback_path: Path,
    expected_kind: str | None = None,
) -> Path:
    def _ensure_inside_root(candidate: Path, dep: str) -> Path:
        resolved_candidate = candidate.resolve()
        resolved_root = root.resolve()
        if resolved_root not in {resolved_candidate, *resolved_candidate.parents}:
            raise CompileError(
                f"Locked dependency {dep!r} escapes package root via {candidate}",
                hint=f"Fix {LOCK_FILE} so dependency paths stay inside the package root.",
            )
        return resolved_candidate

    if lock is None:
        return _ensure_inside_root(fallback_path, dep_name)
    entry = next((item for item in lock.dependencies if item.name == dep_name), None)
    if entry is None:
        return _ensure_inside_root(fallback_path, dep_name)
    if expected_kind and entry.kind != expected_kind:
        raise CompileError(
            f"Lock kind mismatch for dependency {dep_name!r}: manifest={expected_kind}, lock={entry.kind}",
            hint=f"Regenerate {LOCK_FILE} so dependency kinds match ssk.toml.",
        )
    resolved = _ensure_inside_root(root / entry.resolved_path, dep_name)
    if manifest.lock_required and entry.sha256 is None:
        raise CompileError(
            f"Lock hash missing for dependency {dep_name!r}",
            hint=f"Regenerate {LOCK_FILE} with sha256 hashes for reproducible verification.",
        )
    if not resolved.exists():
        raise CompileError(
            f"Locked dependency {dep_name!r} points to missing path {resolved}",
            hint=f"Regenerate {LOCK_FILE} from {MANIFEST_TOML}.",
        )
    if entry.sha256 is not None:
        actual = sha256_path(resolved)
        if actual != entry.sha256:
            raise CompileError(
                f"Lock hash mismatch for dependency {dep_name!r}",
                hint=f"Expected sha256 {entry.sha256}, found {actual}.",
            )
    return resolved


def build_lock_from_manifest(root: Path, manifest: PackageManifest) -> PackageLock:
    locked: list[LockedDependency] = []
    for dep in manifest.dependencies:
        if dep.path is None:
            continue
        resolved = (root / dep.path).resolve()
        try:
            resolved_rel = resolved.relative_to(root.resolve())
        except ValueError as exc:
            raise CompileError(
                f"Dependency {dep.name!r} path escapes package root: {dep.path}",
                hint="Keep manifest dependency paths inside the package root.",
            ) from exc
        locked.append(
            LockedDependency(
                name=dep.name,
                kind=dep.kind,
                resolved_path=str(resolved_rel).replace("\\", "/"),
                version=dep.version,
                sha256=sha256_path(resolved),
            )
        )
    return PackageLock(
        lock_version=1,
        package_name=manifest.name,
        package_version=manifest.version,
        dependencies=tuple(locked),
        signature=manifest.signature,
    )


__all__ = [
    "LOCK_FILE",
    "LockedDependency",
    "PackageLock",
    "build_lock_from_manifest",
    "load_lock",
    "lock_path_for_root",
    "resolve_locked_path",
    "sha256_file",
    "sha256_path",
    "write_lock",
]
