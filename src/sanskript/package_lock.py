from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from .errors import CompileError
from .package_manifest import MANIFEST_TOML, PackageManifest

LOCK_FILE = "ssk.lock"


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
    deps = tuple(
        LockedDependency(
            name=name,
            kind=entry.get("kind", "local"),
            resolved_path=entry["resolved"],
            version=entry.get("version"),
            sha256=entry.get("sha256"),
        )
        for name, entry in data.get("dependencies", {}).items()
    )
    package = data.get("package", {})
    return PackageLock(
        lock_version=int(data.get("lock_version", 1)),
        package_name=package.get("name", "anonymous"),
        package_version=package.get("version", "0.0.0"),
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


def resolve_locked_path(
    root: Path,
    manifest: PackageManifest,
    lock: PackageLock | None,
    dep_name: str,
    *,
    fallback_path: Path,
) -> Path:
    if lock is None:
        return fallback_path.resolve()
    entry = next((item for item in lock.dependencies if item.name == dep_name), None)
    if entry is None:
        return fallback_path.resolve()
    resolved = (root / entry.resolved_path).resolve()
    if not resolved.exists():
        raise CompileError(
            f"Locked dependency {dep_name!r} points to missing path {resolved}",
            hint=f"Regenerate {LOCK_FILE} from {MANIFEST_TOML}.",
        )
    if entry.sha256 is not None:
        actual = sha256_file(resolved)
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
        locked.append(
            LockedDependency(
                name=dep.name,
                kind=dep.kind,
                resolved_path=str(resolved.relative_to(root)).replace("\\", "/"),
                version=dep.version,
                sha256=sha256_file(resolved) if resolved.is_file() else None,
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
    "write_lock",
]
