from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from .errors import CompileError

MANIFEST_TOML = "ssk.toml"
MANIFEST_PROSE = "saṃskaraṇa.sskm"
MANIFEST_PROSE_ASCII = "samskarana.sskm"

DependencyKind = Literal["local", "registry", "vendored"]


@dataclass(frozen=True)
class DependencySpec:
    name: str
    kind: DependencyKind
    path: str | None = None
    version: str | None = None
    registry: str = "ssk"
    locked: bool = False


@dataclass(frozen=True)
class PlatformModuleSpec:
    platform: str
    module_path: str


@dataclass(frozen=True)
class BuildProfile:
    name: str
    options: dict[str, str]


@dataclass(frozen=True)
class PackageManifest:
    name: str
    version: str
    dependencies: tuple[DependencySpec, ...] = ()
    features: dict[str, bool] = field(default_factory=dict)
    profiles: tuple[BuildProfile, ...] = ()
    platform_modules: tuple[PlatformModuleSpec, ...] = ()
    stdlib_namespace: str = "stdlib"
    user_namespace: str = "lib"
    vendor_dir: str = "vendor"
    signature: str | None = None

    def enabled_features(self) -> frozenset[str]:
        return frozenset(name for name, on in self.features.items() if on)


def find_manifest_path(start: Path) -> Path | None:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for directory in (current, *current.parents):
        for name in (MANIFEST_TOML, MANIFEST_PROSE, MANIFEST_PROSE_ASCII):
            candidate = directory / name
            if candidate.is_file():
                return candidate
    return None


def load_manifest(path: Path) -> PackageManifest:
    text = path.read_text(encoding="utf-8")
    if path.name.endswith(".toml"):
        return _parse_toml_manifest(text)
    return _parse_prose_manifest(text)


def default_manifest(package_name: str = "anonymous") -> PackageManifest:
    return PackageManifest(name=package_name, version="0.0.0")


def load_manifest_for_path(entry: Path) -> tuple[PackageManifest, Path | None]:
    manifest_path = find_manifest_path(entry)
    if manifest_path is None:
        return default_manifest(entry.stem), None
    return load_manifest(manifest_path), manifest_path


def _parse_toml_manifest(text: str) -> PackageManifest:
    sections: dict[str, dict[str, str]] = {}
    current = "package"
    sections[current] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        section_match = re.match(r"^\[([^\]]+)\]$", line)
        if section_match:
            current = section_match.group(1).strip()
            sections.setdefault(current, {})
            continue
        if "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        sections.setdefault(current, {})[key] = _unquote(value)

    package = sections.get("package", {})
    name = package.get("name", "anonymous")
    version = package.get("version", "0.0.0")
    signature = package.get("signature") or sections.get("signing", {}).get("signature")

    dependencies: list[DependencySpec] = []
    for key, value in sections.get("dependencies.local", {}).items():
        path = _table_path(value) or value
        dependencies.append(DependencySpec(name=key, kind="local", path=path))
    for key, value in sections.get("dependencies.registry", {}).items():
        version_req, registry = _registry_fields(value)
        dependencies.append(
            DependencySpec(name=key, kind="registry", version=version_req, registry=registry)
        )
    for key, value in sections.get("dependencies.vendored", {}).items():
        path = _table_path(value) or value
        locked = "locked" in value.lower() and "true" in value.lower()
        dependencies.append(DependencySpec(name=key, kind="vendored", path=path, locked=locked))

    features: dict[str, bool] = {}
    for key, value in sections.get("features", {}).items():
        features[key] = value.lower() in {"1", "true", "yes", "on"}

    profiles: list[BuildProfile] = []
    profile_sections = [name for name in sections if name.startswith("profile.")]
    for section in profile_sections:
        profile_name = section.split(".", 1)[1]
        profiles.append(BuildProfile(profile_name, dict(sections[section])))

    platform_modules: list[PlatformModuleSpec] = []
    for key, value in sections.get("platform", {}).items():
        platform_modules.append(PlatformModuleSpec(platform=key, module_path=value))

    namespace = sections.get("namespace", {})
    return PackageManifest(
        name=name,
        version=version,
        dependencies=tuple(dependencies),
        features=features,
        profiles=tuple(profiles),
        platform_modules=tuple(platform_modules),
        stdlib_namespace=namespace.get("stdlib", "stdlib"),
        user_namespace=namespace.get("user", "lib"),
        vendor_dir=sections.get("package", {}).get("vendor_dir", "vendor"),
        signature=signature,
    )


def _parse_prose_manifest(text: str) -> PackageManifest:
    name = "anonymous"
    version = "0.0.0"
    dependencies: list[DependencySpec] = []
    features: dict[str, bool] = {}
    profiles: list[BuildProfile] = []
    platform_modules: list[PlatformModuleSpec] = []
    stdlib_namespace = "stdlib"
    user_namespace = "lib"
    vendor_dir = "vendor"
    signature: str | None = None
    active_profile: dict[str, str] | None = None

    for sentence in re.split(r"(?:\n|।)|\.\s+", text):
        tokens = sentence.strip().split()
        if not tokens:
            continue
        first = tokens[0]
        if first in {"pūtikā", "putika"} and len(tokens) >= 3:
            name = tokens[2]
        elif first in {"saṃskaraṇam", "samskaranam"} and len(tokens) >= 2:
            name = tokens[1]
        elif first in {"saṃskaraṇa-avāntara", "samskarana-avantara", "avāntara", "avantara"} and len(tokens) >= 2:
            version = tokens[1]
        elif first in {"āśraya", "ashraya"} and len(tokens) >= 3:
            dep_name = tokens[-1]
            if tokens[1] in {"panthanāt", "panthat", "local"}:
                path = " ".join(tokens[2:-1])
                dependencies.append(DependencySpec(dep_name, "local", path=path))
            elif tokens[1] in {"sañcikāyāḥ", "sancikayah", "registry"}:
                version_req = tokens[2] if len(tokens) >= 4 else None
                dependencies.append(DependencySpec(dep_name, "registry", version=version_req))
            elif tokens[1] in {"nikṣipta", "nikshipta", "vendored"}:
                path = " ".join(tokens[2:-1])
                dependencies.append(DependencySpec(dep_name, "vendored", path=path, locked=True))
        elif first in {"viśeṣa", "vishesha", "feature"} and len(tokens) >= 3:
            features[tokens[1]] = tokens[2].lower() in {"sat", "true", "1", "yes"}
        elif first in {"rūpa", "rupa", "profile"} and len(tokens) >= 2:
            active_profile = {}
            profiles.append(BuildProfile(tokens[1], active_profile))
        elif first in {"taru", "option"} and len(tokens) >= 3 and active_profile is not None:
            active_profile[tokens[1]] = " ".join(tokens[2:])
        elif first in {"mañca", "manca", "platform"} and len(tokens) >= 3:
            platform_modules.append(PlatformModuleSpec(tokens[1], " ".join(tokens[2:])))
        elif first in {"nāma-kṣetra", "nama-kshetra", "namespace"} and len(tokens) >= 3:
            if tokens[1] in {"mūla-āśraya", "mula-ashraya", "stdlib"}:
                stdlib_namespace = tokens[2]
            elif tokens[1] in {"sva-āśraya", "sva-ashraya", "user", "lib"}:
                user_namespace = tokens[2]
        elif first in {"nikṣepa", "nikshepa", "vendor"} and len(tokens) >= 2:
            vendor_dir = tokens[1]
        elif first in {"mudrā", "mudra", "signature"} and len(tokens) >= 2:
            signature = tokens[1]

    return PackageManifest(
        name=name,
        version=version,
        dependencies=tuple(dependencies),
        features=features,
        profiles=tuple(profiles),
        platform_modules=tuple(platform_modules),
        stdlib_namespace=stdlib_namespace,
        user_namespace=user_namespace,
        vendor_dir=vendor_dir,
        signature=signature,
    )


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _table_path(value: str) -> str | None:
    match = re.search(r"path\s*=\s*[\"']([^\"']+)[\"']", value)
    if match:
        return match.group(1)
    match = re.search(r"path\s*=\s*([^\s,}]+)", value)
    return match.group(1) if match else None


def _registry_fields(value: str) -> tuple[str | None, str]:
    version_match = re.search(r"version\s*=\s*[\"']([^\"']+)[\"']", value)
    registry_match = re.search(r"registry\s*=\s*[\"']([^\"']+)[\"']", value)
    version = version_match.group(1) if version_match else (value if not value.startswith("{") else None)
    registry = registry_match.group(1) if registry_match else "ssk"
    return version, registry


def validate_manifest_features(manifest: PackageManifest, required: frozenset[str]) -> None:
    missing = sorted(flag for flag in required if flag not in manifest.enabled_features())
    if missing:
        raise CompileError(
            f"Required feature flags not enabled: {', '.join(missing)}",
            hint="Enable them under [features] in ssk.toml or viśeṣa lines in saṃskaraṇa.sskm.",
        )


__all__ = [
    "BuildProfile",
    "DependencyKind",
    "DependencySpec",
    "MANIFEST_PROSE",
    "MANIFEST_TOML",
    "PackageManifest",
    "PlatformModuleSpec",
    "find_manifest_path",
    "load_manifest",
    "load_manifest_for_path",
    "default_manifest",
    "validate_manifest_features",
]
