"""Load and query the canonical Sanskript type / data-structure catalog."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any

from .errors import SanskriptError

CATALOG_PATH = Path(__file__).resolve().parents[2] / "data" / "types" / "catalog.json"


class TypeCatalogError(SanskriptError):
    code = "SANSKRIPT_TYPE_CATALOG"


class SafetyTier(str, Enum):
    SURAKSHITA = "surakshita"
    RAKSHITA = "rakshita"
    ARAKSHITA = "arakshita"


class TierAvailability(str, Enum):
    FULL = "full"
    RESTRICTED = "restricted"
    FORBIDDEN = "forbidden"


class ImplementationStatus(str, Enum):
    IMPLEMENTED = "implemented"
    PARTIAL = "partial"
    PLANNED = "planned"


class TypeCategory(str, Enum):
    SCALAR = "scalar"
    COMPOSITE = "composite"
    COLLECTION = "collection"
    FUNCTIONAL = "functional"
    MEMORY = "memory"
    OBJECT = "object"
    CONCURRENCY = "concurrency"
    IO = "io"
    META = "meta"
    SPECIAL = "special"


@dataclass(frozen=True)
class SafetyTierInfo:
    key: SafetyTier
    iast: str
    gloss: str
    analogy: str


@dataclass(frozen=True)
class TypeEntry:
    id: str
    name: str
    category: TypeCategory
    c_types: tuple[str, ...]
    python_types: tuple[str, ...]
    implementation: ImplementationStatus
    tiers: dict[SafetyTier, TierAvailability]
    sanskrit_hint: str | None = None
    type_form: str | None = None
    bytecode_tag: str | None = None
    notes: str | None = None


@dataclass(frozen=True)
class TypeCatalog:
    version: int
    safety_tiers: dict[SafetyTier, SafetyTierInfo]
    karaka_roles_for_types: dict[str, str]
    types: tuple[TypeEntry, ...]
    tier_availability_legend: dict[str, str]
    implementation_legend: dict[str, str]

    def by_id(self, type_id: str) -> TypeEntry:
        for entry in self.types:
            if entry.id == type_id:
                return entry
        raise TypeCatalogError(f"Unknown type id: {type_id!r}")

    def by_name(self, name: str) -> TypeEntry:
        for entry in self.types:
            if entry.name == name:
                return entry
        raise TypeCatalogError(f"Unknown type name: {name!r}")

    def types_in_category(self, category: TypeCategory) -> tuple[TypeEntry, ...]:
        return tuple(entry for entry in self.types if entry.category == category)

    def types_for_tier(
        self,
        tier: SafetyTier,
        *,
        availability: TierAvailability | None = None,
    ) -> tuple[TypeEntry, ...]:
        items: list[TypeEntry] = []
        for entry in self.types:
            level = entry.tiers.get(tier, TierAvailability.FORBIDDEN)
            if availability is None:
                if level != TierAvailability.FORBIDDEN:
                    items.append(entry)
            elif level == availability:
                items.append(entry)
        return tuple(items)

    def implemented_types(self) -> tuple[TypeEntry, ...]:
        return tuple(
            entry
            for entry in self.types
            if entry.implementation in {ImplementationStatus.IMPLEMENTED, ImplementationStatus.PARTIAL}
        )


def _parse_tier_map(raw: dict[str, str]) -> dict[SafetyTier, TierAvailability]:
    parsed: dict[SafetyTier, TierAvailability] = {}
    for key, value in raw.items():
        parsed[SafetyTier(key)] = TierAvailability(value)
    return parsed


def load_type_catalog(path: Path | None = None) -> TypeCatalog:
    catalog_path = path or CATALOG_PATH
    payload: dict[str, Any] = json.loads(catalog_path.read_text(encoding="utf-8"))

    safety_tiers: dict[SafetyTier, SafetyTierInfo] = {}
    for key, info in payload.get("safety_tiers", {}).items():
        tier = SafetyTier(key)
        safety_tiers[tier] = SafetyTierInfo(
            key=tier,
            iast=str(info.get("iast", key)),
            gloss=str(info.get("gloss", "")),
            analogy=str(info.get("analogy", "")),
        )

    types: list[TypeEntry] = []
    seen_ids: set[str] = set()
    for raw in payload.get("types", []):
        type_id = str(raw["id"])
        if type_id in seen_ids:
            raise TypeCatalogError(f"Duplicate type id: {type_id!r}")
        seen_ids.add(type_id)
        types.append(
            TypeEntry(
                id=type_id,
                name=str(raw["name"]),
                category=TypeCategory(str(raw["category"])),
                c_types=tuple(str(item) for item in raw.get("c_types", [])),
                python_types=tuple(str(item) for item in raw.get("python_types", [])),
                implementation=ImplementationStatus(str(raw.get("implementation", "planned"))),
                tiers=_parse_tier_map(raw.get("tiers", {})),
                sanskrit_hint=raw.get("sanskrit_hint"),
                type_form=raw.get("type_form"),
                bytecode_tag=raw.get("bytecode_tag"),
                notes=raw.get("notes"),
            )
        )

    return TypeCatalog(
        version=int(payload.get("version", 0)),
        safety_tiers=safety_tiers,
        karaka_roles_for_types={
            str(key): str(value) for key, value in payload.get("karaka_roles_for_types", {}).items()
        },
        types=tuple(types),
        tier_availability_legend={
            str(key): str(value) for key, value in payload.get("tier_availability_legend", {}).items()
        },
        implementation_legend={
            str(key): str(value) for key, value in payload.get("implementation_legend", {}).items()
        },
    )


@lru_cache(maxsize=1)
def get_type_catalog() -> TypeCatalog:
    return load_type_catalog()


__all__ = [
    "CATALOG_PATH",
    "ImplementationStatus",
    "SafetyTier",
    "SafetyTierInfo",
    "TierAvailability",
    "TypeCatalog",
    "TypeCatalogError",
    "TypeCategory",
    "TypeEntry",
    "get_type_catalog",
    "load_type_catalog",
]
