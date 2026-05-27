"""Data-driven fixed-width integer specs and arithmetic for Phase 3."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterator


def _word_bits() -> int:
    return 64 if sys.maxsize > 2**32 else 32


@dataclass(frozen=True)
class FixedWidthSpec:
    """One signed or unsigned fixed-width integer kind."""

    name: str  # e.g. i8, u64, isize
    signed: bool
    bits: int
    push_opcode: str
    add_checked_opcode: str
    add_wrapping_opcode: str
    add_saturating_opcode: str
    yantra_push_suffix: str  # Sanskrit prose tail after literal
    yantra_add_checked: str

    @property
    def min_value(self) -> int:
        if not self.signed:
            return 0
        return -(2 ** (self.bits - 1))

    @property
    def max_value(self) -> int:
        if not self.signed:
            return 2**self.bits - 1
        return 2 ** (self.bits - 1) - 1

    @property
    def modulus(self) -> int:
        return 2**self.bits

    def validate_literal(self, value: int) -> None:
        if value < self.min_value or value > self.max_value:
            raise ValueError(
                f"{self.name} literal out of range [{self.min_value}, {self.max_value}]: {value}"
            )

    def wrap(self, value: int) -> int:
        masked = (value + self.modulus) % self.modulus
        if self.signed and masked >= 2 ** (self.bits - 1):
            return masked - self.modulus
        return masked

    def clamp(self, value: int) -> int:
        if value < self.min_value:
            return self.min_value
        if value > self.max_value:
            return self.max_value
        return value

    def checked_add(self, left: int, right: int) -> int:
        result = left + right
        if result < self.min_value or result > self.max_value:
            raise OverflowError(f"{self.name} overflow: {left} + {right}")
        return result

    def saturating_add(self, left: int, right: int) -> int:
        return self.clamp(left + right)


@dataclass(frozen=True)
class FixedIntValue:
    """Runtime tagged fixed-width integer."""

    spec: FixedWidthSpec
    value: int

    def __post_init__(self) -> None:
        self.spec.validate_literal(self.value)


_WIDTHS = (8, 16, 32, 64, 128)


def _signed_specs() -> list[FixedWidthSpec]:
    specs: list[FixedWidthSpec] = []
    for bits in _WIDTHS:
        name = f"i{bits}"
        specs.append(
            FixedWidthSpec(
                name=name,
                signed=True,
                bits=bits,
                push_opcode=f"push_{name}",
                add_checked_opcode=f"{name}_add_checked",
                add_wrapping_opcode=f"{name}_add_wrapping",
                add_saturating_opcode=f"{name}_add_saturating",
                yantra_push_suffix=f"saṅkhyā-{bits//8 if bits >= 8 else bits}",
                yantra_add_checked=f"saṅkhyā-{bits//8 if bits >= 8 else bits}ayoḥ yogaḥ parīkṣitaḥ kriyate.",
            )
        )
    return specs


def _unsigned_specs() -> list[FixedWidthSpec]:
    specs: list[FixedWidthSpec] = []
    for bits in _WIDTHS:
        name = f"u{bits}"
        specs.append(
            FixedWidthSpec(
                name=name,
                signed=False,
                bits=bits,
                push_opcode=f"push_{name}",
                add_checked_opcode=f"{name}_add_checked",
                add_wrapping_opcode=f"{name}_add_wrapping",
                add_saturating_opcode=f"{name}_add_saturating",
                yantra_push_suffix=f"saṅkhyā-nirṇāśa-{bits//8 if bits >= 8 else bits}",
                yantra_add_checked=f"saṅkhyā-nirṇāśa-{bits//8 if bits >= 8 else bits}ayoḥ yogaḥ parīkṣitaḥ kriyate.",
            )
        )
    return specs


def _word_specs() -> list[FixedWidthSpec]:
    bits = _word_bits()
    return [
        FixedWidthSpec(
            name="isize",
            signed=True,
            bits=bits,
            push_opcode="push_isize",
            add_checked_opcode="isize_add_checked",
            add_wrapping_opcode="isize_add_wrapping",
            add_saturating_opcode="isize_add_saturating",
            yantra_push_suffix="yantra-saṅkhyā",
            yantra_add_checked="yantra-saṅkhyāyoḥ yogaḥ parīkṣitaḥ kriyate.",
        ),
        FixedWidthSpec(
            name="usize",
            signed=False,
            bits=bits,
            push_opcode="push_usize",
            add_checked_opcode="usize_add_checked",
            add_wrapping_opcode="usize_add_wrapping",
            add_saturating_opcode="usize_add_saturating",
            yantra_push_suffix="yantra-saṅkhyā-nirṇāśa",
            yantra_add_checked="yantra-saṅkhyā-nirṇāśayoḥ yogaḥ parīkṣitaḥ kriyate.",
        ),
    ]


FIXED_WIDTH_SPECS: tuple[FixedWidthSpec, ...] = tuple(
    _signed_specs() + _unsigned_specs() + _word_specs()
)

SPEC_BY_NAME: dict[str, FixedWidthSpec] = {s.name: s for s in FIXED_WIDTH_SPECS}
SPEC_BY_PUSH_OPCODE: dict[str, FixedWidthSpec] = {s.push_opcode: s for s in FIXED_WIDTH_SPECS}
SPEC_BY_ADD_CHECKED: dict[str, FixedWidthSpec] = {
    s.add_checked_opcode: s for s in FIXED_WIDTH_SPECS
}
SPEC_BY_ADD_WRAPPING: dict[str, FixedWidthSpec] = {
    s.add_wrapping_opcode: s for s in FIXED_WIDTH_SPECS
}
SPEC_BY_ADD_SATURATING: dict[str, FixedWidthSpec] = {
    s.add_saturating_opcode: s for s in FIXED_WIDTH_SPECS
}

# i32/u32 legacy aliases share specs with width-32 entries
I32_SPEC = SPEC_BY_NAME["i32"]
U32_SPEC = SPEC_BY_NAME["u32"]


def fixed_int(spec_name: str, value: int) -> FixedIntValue:
    return FixedIntValue(SPEC_BY_NAME[spec_name], value)


def iter_fixed_opcode_names() -> Iterator[str]:
    """All push and add opcodes for schema / enum registration."""
    for spec in FIXED_WIDTH_SPECS:
        yield spec.push_opcode
        yield spec.add_checked_opcode
        yield spec.add_wrapping_opcode
        yield spec.add_saturating_opcode
    # Legacy names kept for backward compatibility (same semantics as i32/u32)
    yield "push_i32"
    yield "push_u32"
    yield "i32_add_checked"
    yield "u32_add_checked"
    yield "i32_add_wrapping"
    yield "u32_add_wrapping"
    yield "i32_add_saturating"
    yield "u32_add_saturating"


class ArithmeticMode(str, Enum):
    CHECKED = "checked"
    WRAPPING = "wrapping"
    SATURATING = "saturating"


def apply_add(spec: FixedWidthSpec, left: int, right: int, mode: ArithmeticMode) -> int:
    if mode == ArithmeticMode.CHECKED:
        return spec.checked_add(left, right)
    if mode == ArithmeticMode.WRAPPING:
        return spec.wrap(left + right)
    return spec.saturating_add(left, right)


def register_fixed_width_opcodes(
    *,
    operand_kind: dict[str, str | None],
    stack_effect: dict[str, tuple[int, int]],
) -> None:
    """Register operand kinds and stack effects for all fixed-width opcodes."""
    for spec in FIXED_WIDTH_SPECS:
        operand_kind[spec.push_opcode] = "int"
        stack_effect[spec.push_opcode] = (0, 1)
        for op in (
            spec.add_checked_opcode,
            spec.add_wrapping_opcode,
            spec.add_saturating_opcode,
        ):
            operand_kind[op] = None
            stack_effect[op] = (2, 1)


__all__ = [
    "ArithmeticMode",
    "FIXED_WIDTH_SPECS",
    "FixedIntValue",
    "FixedWidthSpec",
    "I32_SPEC",
    "U32_SPEC",
    "SPEC_BY_ADD_CHECKED",
    "SPEC_BY_ADD_SATURATING",
    "SPEC_BY_ADD_WRAPPING",
    "SPEC_BY_NAME",
    "SPEC_BY_PUSH_OPCODE",
    "apply_add",
    "fixed_int",
    "iter_fixed_opcode_names",
    "register_fixed_width_opcodes",
]
