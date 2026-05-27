"""Compile-time lexical scope and binding rules (Phase 2)."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import CompileError


@dataclass
class _Binding:
    immutable: bool = False
    forward_only: bool = False


class ScopeStack:
    """Nested scopes: duplicate bind in the same frame is an error."""

    def __init__(self) -> None:
        self._frames: list[dict[str, _Binding]] = [{}]

    def push(self) -> None:
        self._frames.append({})

    def pop(self) -> None:
        if len(self._frames) <= 1:
            raise CompileError("Internal scope stack underflow")
        self._frames.pop()

    def declare(self, name: str, *, immutable: bool = False, forward: bool = False) -> None:
        frame = self._frames[-1]
        if name in frame:
            raise CompileError(
                f"Duplicate binding {name!r} in the same scope",
                hint="Choose another name or use an outer binding without redeclaring.",
            )
        frame[name] = _Binding(immutable=immutable, forward_only=forward)

    def is_bound(self, name: str) -> bool:
        return self._lookup(name) is not None

    def assign(self, name: str) -> None:
        binding = self._lookup(name)
        if binding is None:
            self._frames[-1][name] = _Binding()
            return
        if binding.immutable:
            raise CompileError(
                f"Cannot assign to immutable binding {name!r}",
                hint="Declare a new mutable name or use acalachihnam only for constants.",
            )
        if binding.forward_only:
            binding.forward_only = False

    def _lookup(self, name: str) -> _Binding | None:
        for frame in reversed(self._frames):
            if name in frame:
                return frame[name]
        return None
