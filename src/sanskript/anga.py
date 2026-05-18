from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AngaOperationKind(str, Enum):
    GUNA = "guṇa"
    VRDDHI = "vṛddhi"
    FINAL_LENGTHENING = "final_lengthening"
    AUGMENT = "augment"
    LOPA = "lopa"
    NASALIZATION = "nasalization"
    RETROFLEXION = "retroflexion"


@dataclass(frozen=True)
class AngaOperation:
    name: str
    sutra_range: str
    kind: AngaOperationKind
    source: str
    target: str
    description: str


GUNA_REPLACEMENTS = {
    "i": "e",
    "ī": "e",
    "u": "o",
    "ū": "o",
    "ṛ": "ar",
    "ṝ": "ar",
    "ḷ": "al",
}


VRDDHI_REPLACEMENTS = {
    "a": "ā",
    "i": "ai",
    "ī": "ai",
    "u": "au",
    "ū": "au",
    "ṛ": "ār",
    "ṝ": "ār",
}


ANGA_OPERATIONS: tuple[AngaOperation, ...] = (
    AngaOperation("compound-accent-domain", "6.2", AngaOperationKind.AUGMENT, "", "", "records compound-level accent scope"),
    AngaOperation("uttarapada-domain", "6.3", AngaOperationKind.AUGMENT, "", "", "records second-member form scope"),
    AngaOperation("final-a-lengthening", "6.4", AngaOperationKind.FINAL_LENGTHENING, "a", "ā", "lengthens a final stem vowel"),
    AngaOperation("final-lopa", "6.4", AngaOperationKind.LOPA, "a", "", "drops a final stem sound under controlled conditions"),
    AngaOperation("num-augment", "7.1", AngaOperationKind.AUGMENT, "", "n", "adds a controlled nasal augment"),
    AngaOperation("i-guṇa", "7.2", AngaOperationKind.GUNA, "i", "e", "applies guṇa to i/ī"),
    AngaOperation("u-vṛddhi", "7.2", AngaOperationKind.VRDDHI, "u", "au", "applies vṛddhi to u/ū"),
    AngaOperation("ṛ-guṇa", "7.3", AngaOperationKind.GUNA, "ṛ", "ar", "applies guṇa to vocalic ṛ"),
    AngaOperation("n-nasalization", "7.3", AngaOperationKind.NASALIZATION, "n", "ṃ", "records nasalization as an aṅga operation"),
    AngaOperation("ṇati-retroflexion", "7.4", AngaOperationKind.RETROFLEXION, "n", "ṇ", "retroflexes dental n in controlled ṇati domains"),
)


def guna(sound: str) -> str:
    try:
        return GUNA_REPLACEMENTS[sound]
    except KeyError as exc:
        raise ValueError(f"No controlled guṇa replacement for {sound!r}") from exc


def vrddhi(sound: str) -> str:
    try:
        return VRDDHI_REPLACEMENTS[sound]
    except KeyError as exc:
        raise ValueError(f"No controlled vṛddhi replacement for {sound!r}") from exc


def operations_for_range(sutra_range: str) -> tuple[AngaOperation, ...]:
    return tuple(operation for operation in ANGA_OPERATIONS if operation.sutra_range == sutra_range)


def operation_named(name: str) -> AngaOperation:
    for operation in ANGA_OPERATIONS:
        if operation.name == name:
            return operation
    raise ValueError(f"Unknown controlled aṅga operation: {name!r}")


def apply_anga_operation(form: str, operation: AngaOperation) -> str:
    if operation.kind == AngaOperationKind.AUGMENT:
        return operation.target + form
    if operation.kind == AngaOperationKind.FINAL_LENGTHENING and form.endswith(operation.source):
        return form[: -len(operation.source)] + operation.target
    if operation.kind == AngaOperationKind.LOPA and form.endswith(operation.source):
        return form[: -len(operation.source)]
    if operation.kind in {AngaOperationKind.GUNA, AngaOperationKind.VRDDHI, AngaOperationKind.NASALIZATION, AngaOperationKind.RETROFLEXION}:
        return form.replace(operation.source, operation.target, 1)
    return form
