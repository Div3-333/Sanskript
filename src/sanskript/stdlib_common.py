"""Shared helpers for native stdlib implementations."""

from __future__ import annotations

import json
from dataclasses import dataclass

from .errors import RuntimeSanskriptError
from .runtime_values import BytesValue, NIL, NilValue, SanskriptValue


@dataclass(frozen=True)
class NativeSpec:
    arity: int
    fn: callable


def expect_text(value: SanskriptValue, *, fn_name: str) -> str:
    if not isinstance(value, str):
        raise RuntimeSanskriptError(f"{fn_name} expected text, got {value!r}")
    return value


def expect_number(value: SanskriptValue, *, fn_name: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise RuntimeSanskriptError(f"{fn_name} expected number, got {value!r}")
    return value


def expect_int(value: SanskriptValue, *, fn_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise RuntimeSanskriptError(f"{fn_name} expected integer, got {value!r}")
    return value


def expect_bool(value: SanskriptValue, *, fn_name: str) -> bool:
    if not isinstance(value, bool):
        raise RuntimeSanskriptError(f"{fn_name} expected boolean, got {value!r}")
    return value


def expect_list(value: SanskriptValue, *, fn_name: str) -> list[SanskriptValue]:
    if not isinstance(value, list):
        raise RuntimeSanskriptError(f"{fn_name} expected list, got {value!r}")
    return value


def expect_map(value: SanskriptValue, *, fn_name: str) -> dict[str, SanskriptValue]:
    if not isinstance(value, dict):
        raise RuntimeSanskriptError(f"{fn_name} expected map, got {value!r}")
    return value


def expect_bytes(value: SanskriptValue, *, fn_name: str) -> BytesValue:
    if not isinstance(value, BytesValue):
        raise RuntimeSanskriptError(f"{fn_name} expected bytes, got {value!r}")
    return value


def from_json(value: object) -> SanskriptValue:
    if value is None:
        return NIL
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return [from_json(item) for item in value]
    if isinstance(value, dict):
        out: dict[str, SanskriptValue] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise RuntimeSanskriptError("JSON object keys must be text")
            out[key] = from_json(item)
        return out
    raise RuntimeSanskriptError(f"cannot map JSON type {type(value).__name__}")


def to_json(value: SanskriptValue) -> object:
    if isinstance(value, NilValue):
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float, str)):
        return value
    if isinstance(value, list):
        return [to_json(item) for item in value]
    if isinstance(value, dict):
        out: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise RuntimeSanskriptError("JSON map keys must be text")
            out[key] = to_json(item)
        return out
    if isinstance(value, BytesValue):
        raise RuntimeSanskriptError("bytes values cannot be JSON-stringified directly")
    raise RuntimeSanskriptError(f"unsupported JSON value {type(value).__name__}")


def parse_json_text(text: str, *, fn_name: str) -> SanskriptValue:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeSanskriptError(f"{fn_name} invalid JSON: {exc.msg}") from exc
    return from_json(payload)


def stringify_json(value: SanskriptValue) -> str:
    return json.dumps(to_json(value), ensure_ascii=False, separators=(",", ":"), sort_keys=True)


__all__ = [
    "NativeSpec",
    "expect_bool",
    "expect_bytes",
    "expect_int",
    "expect_list",
    "expect_map",
    "expect_number",
    "expect_text",
    "from_json",
    "parse_json_text",
    "stringify_json",
    "to_json",
]
