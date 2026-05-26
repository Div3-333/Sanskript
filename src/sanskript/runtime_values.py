"""Runtime value model for the surakṣita tier (managed, checked collections)."""

from __future__ import annotations

from typing import TypeAlias

# Host representation until values gain a dedicated heap / tag word in the VM.
SanskriptValue: TypeAlias = (
    int | float | str | bool | list["SanskriptValue"] | dict[str, "SanskriptValue"]
)

MapKey: TypeAlias = str | int


def is_map_key(value: SanskriptValue) -> bool:
    return isinstance(value, (str, int)) and not isinstance(value, bool)


def is_truthy(value: SanskriptValue) -> bool:
    if value is False or value == 0 or value == "":
        return False
    if isinstance(value, (list, dict)) and len(value) == 0:
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
    return str(value)


def expect_list(value: SanskriptValue) -> list[SanskriptValue]:
    if not isinstance(value, list):
        raise TypeError(f"expected list, got {type(value).__name__}")
    return value


def expect_map(value: SanskriptValue) -> dict[str, SanskriptValue]:
    if not isinstance(value, dict):
        raise TypeError(f"expected map, got {type(value).__name__}")
    return value


def map_key_from_value(value: SanskriptValue) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    raise TypeError(f"map key must be text or integer, got {value!r}")


__all__ = [
    "MapKey",
    "SanskriptValue",
    "expect_list",
    "expect_map",
    "is_map_key",
    "is_truthy",
    "map_key_from_value",
    "to_display_string",
    "values_equal",
]
