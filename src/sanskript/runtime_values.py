"""Runtime value model for the surakṣita tier (managed, checked collections)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeAlias


@dataclass
class RecordValue:
    """Managed named-field value; the object substrate before full classes."""

    fields: dict[str, "SanskriptValue"] = field(default_factory=dict)


# Host representation until values gain a dedicated heap / tag word in the VM.
SanskriptValue: TypeAlias = (
    int
    | float
    | str
    | bool
    | list["SanskriptValue"]
    | dict[str, "SanskriptValue"]
    | RecordValue
)

MapKey: TypeAlias = str | int


def is_map_key(value: SanskriptValue) -> bool:
    return isinstance(value, (str, int)) and not isinstance(value, bool)


def is_truthy(value: SanskriptValue) -> bool:
    if value is False or value == 0 or value == "":
        return False
    if isinstance(value, (list, dict)) and len(value) == 0:
        return False
    if isinstance(value, RecordValue) and len(value.fields) == 0:
        return False
    return True


def values_equal(left: SanskriptValue, right: SanskriptValue) -> bool:
    return left == right


def to_display_string(value: SanskriptValue) -> str:
    if isinstance(value, float):
        text = format(value, "g")
        return text if "." in text else f"{text}.0"
    if isinstance(value, bool):
        return "satyam" if value else "asatyam"
    if isinstance(value, list):
        inner = ", ".join(to_display_string(item) for item in value)
        return f"[{inner}]"
    if isinstance(value, dict):
        parts = [f"{to_display_string(key)}:{to_display_string(val)}" for key, val in value.items()]
        return "{" + ", ".join(parts) + "}"
    if isinstance(value, RecordValue):
        parts = [
            f"{to_display_string(key)}:{to_display_string(val)}"
            for key, val in value.fields.items()
        ]
        return "vastu{" + ", ".join(parts) + "}"
    return str(value)


def expect_list(value: SanskriptValue) -> list[SanskriptValue]:
    if not isinstance(value, list):
        raise TypeError(f"expected list, got {type(value).__name__}")
    return value


def expect_map(value: SanskriptValue) -> dict[str, SanskriptValue]:
    if not isinstance(value, dict):
        raise TypeError(f"expected map, got {type(value).__name__}")
    return value


def expect_record(value: SanskriptValue) -> RecordValue:
    if not isinstance(value, RecordValue):
        raise TypeError(f"expected record, got {type(value).__name__}")
    return value


def map_key_from_value(value: SanskriptValue) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    raise TypeError(f"map key must be text or integer, got {value!r}")


def record_field_from_value(value: SanskriptValue) -> str:
    if isinstance(value, str) and value:
        return value
    raise TypeError(f"record field must be non-empty text, got {value!r}")


__all__ = [
    "MapKey",
    "RecordValue",
    "SanskriptValue",
    "expect_list",
    "expect_map",
    "expect_record",
    "is_map_key",
    "is_truthy",
    "map_key_from_value",
    "record_field_from_value",
    "to_display_string",
    "values_equal",
]
