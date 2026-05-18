from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SamasaType(str, Enum):
    AVYAYIBHAVA = "avyayībhāva"
    TATPURUSHA = "tatpuruṣa"
    BAHUVRIHI = "bahuvrīhi"
    DVANDVA = "dvandva"


@dataclass(frozen=True)
class CompoundExample:
    samasa_type: SamasaType
    members: tuple[str, ...]
    surface: str
    gloss: str


COMPOUND_EXAMPLES: tuple[CompoundExample, ...] = (
    CompoundExample(SamasaType.AVYAYIBHAVA, ("upa", "grāmam"), "upagrāmam", "near the village"),
    CompoundExample(SamasaType.TATPURUSHA, ("rājasya", "puruṣaḥ"), "rājapuruṣaḥ", "king's man"),
    CompoundExample(SamasaType.BAHUVRIHI, ("pītam", "ambaram"), "pītāmbaraḥ", "one whose garment is yellow"),
    CompoundExample(SamasaType.DVANDVA, ("rāmaḥ", "lakṣmaṇaḥ"), "rāmalakṣmaṇau", "Rāma and Lakṣmaṇa"),
)


def classify_compound(surface: str) -> SamasaType:
    for example in COMPOUND_EXAMPLES:
        if example.surface == surface:
            return example.samasa_type
    raise ValueError(f"Unknown controlled compound example: {surface!r}")


def examples_for(samasa_type: SamasaType) -> tuple[CompoundExample, ...]:
    return tuple(example for example in COMPOUND_EXAMPLES if example.samasa_type == samasa_type)
