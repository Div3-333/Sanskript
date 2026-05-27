"""Native stdlib registry for VM `CALL std.*` dispatch."""

from __future__ import annotations

from .errors import RuntimeSanskriptError
from .runtime_values import SanskriptValue
from .stdlib_common import NativeSpec
from .stdlib_impl import NATIVE_REGISTRY

_NATIVE_STD: dict[str, NativeSpec] = dict(NATIVE_REGISTRY)


def has_native_function(name: str) -> bool:
    return name in _NATIVE_STD


def native_arity(name: str) -> int:
    return _NATIVE_STD[name].arity


def call_native_function(name: str, args: list[SanskriptValue]) -> SanskriptValue:
    try:
        spec = _NATIVE_STD[name]
    except KeyError as exc:
        raise RuntimeSanskriptError(f"Unknown native stdlib function {name!r}") from exc
    if len(args) != spec.arity:
        raise RuntimeSanskriptError(
            f"{name} expects {spec.arity} argument(s), got {len(args)}"
        )
    return spec.fn(args)


def list_native_functions() -> list[str]:
    return sorted(_NATIVE_STD.keys())


__all__ = [
    "call_native_function",
    "has_native_function",
    "list_native_functions",
    "native_arity",
]
