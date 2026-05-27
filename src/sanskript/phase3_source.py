"""Phase 3 Sanskrit source directive parsing helpers."""

from __future__ import annotations

from .fixed_width import SPEC_BY_NAME

_WIDTH_DIRECTIVES: dict[str, str] = {
    "saṅkhyā8": "i8",
    "sankhya8": "i8",
    "saṅkhyā16": "i16",
    "sankhya16": "i16",
    "saṅkhyā32": "i32",
    "sankhya32": "i32",
    "saṅkhyā64": "i64",
    "sankhya64": "i64",
    "saṅkhyā128": "i128",
    "sankhya128": "i128",
    "saṅkhyā-nirṇāśa8": "u8",
    "sankhya-nirnasha8": "u8",
    "saṅkhyā-nirṇāśa16": "u16",
    "saṅkhyā-nirṇāśa32": "u32",
    "saṅkhyā-nirṇāśa64": "u64",
    "saṅkhyā-nirṇāśa128": "u128",
    "yantra-saṅkhyā": "isize",
    "yantra-sankhya": "isize",
    "yantra-saṅkhyā-nirṇāśa": "usize",
}


def parse_fixed_width_directive(first: str, tokens: list[str]) -> tuple[str, tuple] | None:
    """``saṅkhyā8 x asti 42`` → (phase3_bind, (target, push_opcode, value))."""
    width = _WIDTH_DIRECTIVES.get(first)
    if width is None or len(tokens) < 4:
        return None
    if tokens[2] not in {"asti", "aste"}:
        return None
    target = tokens[1]
    try:
        value = int(tokens[3])
    except ValueError:
        return None
    spec = SPEC_BY_NAME[width]
    return ("phase3_bind", (target, spec.push_opcode, value))


def parse_vikalpam(tokens: list[str]) -> tuple[str, tuple] | None:
    if len(tokens) < 3:
        return None
    target = tokens[1]
    if tokens[2] in {"śūnyam", "shunyam", "śūnya", "shunya"}:
        return ("phase3_bind", (target, "option_none", None))
    if tokens[2] == "asti" and len(tokens) >= 4:
        # value parsed by caller — return marker
        return ("phase3_some", (target, tokens[3:]))
    return None


def parse_phalam(tokens: list[str]) -> tuple[str, tuple] | None:
    if len(tokens) < 4:
        return None
    target = tokens[1]
    if tokens[2] in {"siddha", "saphala"}:
        return ("phase3_result", (target, True, tokens[3:]))
    if tokens[2] in {"doṣa", "dosa", "doṣaḥ"}:
        return ("phase3_result", (target, False, tokens[3:]))
    return None


__all__ = ["parse_fixed_width_directive", "parse_phalam", "parse_vikalpam"]
