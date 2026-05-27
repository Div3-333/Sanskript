"""Phase 2 value and condition parsing helpers (used by parser.py)."""

from __future__ import annotations

import re
from typing import Callable

from .ast import (
    BoolAnd,
    BoolAndCond,
    BoolLiteral,
    BoolNot,
    BoolNotCond,
    BoolOr,
    BoolOrCond,
    BytesLiteral,
    CallValue,
    CompareEq,
    CompareGt,
    CompareIdentity,
    CompareLe,
    CompareLt,
    CompareMembership,
    CompareNe,
    Condition,
    FloatLiteral,
    GroupValue,
    ListLiteral,
    Literal,
    MapLiteral,
    NilLiteral,
    PartialApply,
    Reference,
    TextLiteral,
    Value,
)
from .grammar import PartOfSpeech
from .identifiers import IdentifierError, canonical_identifier
from .morphology_facade import get_default_facade

_SOURCE_INT_WORDS = {
    "śūnya": 0,
    "shunya": 0,
    "eka": 1,
    "dvi": 2,
    "tri": 3,
    "catur": 4,
    "pañca": 5,
    "panca": 5,
    "ṣaṭ": 6,
    "sat": 6,
    "sapta": 7,
    "aṣṭa": 8,
    "asta": 8,
    "nava": 9,
    "daśa": 10,
    "dasha": 10,
}

_BINARY_VALUE_OPERATORS = {
    "yoga": "add",
    "yogena": "add",
    "vyavakalanam": "subtract",
    "hīna": "subtract",
    "hina": "subtract",
    "guṇanam": "multiply",
    "gunanam": "multiply",
    "guṇena": "multiply",
    "gunena": "multiply",
    "bhāga": "divide",
    "bhaga": "divide",
    "bhāgena": "divide",
    "bhagena": "divide",
}

_COMPARE_MARKERS: dict[str, str] = {
    "samam": "eq",
    "asamam": "ne",
    "nyūnam": "lt",
    "nyunam": "lt",
    "laghutaram": "lt",
    "mahattaram": "gt",
    "tulyam": "le",
    "sadr̥śam": "identity",
    "sadrisham": "identity",
    "sadṛśam": "identity",
}

_TEXT_MARKERS = frozenset({"vākyam", "vakyam", "śabdam", "shabdam"})


def _parse_atomic_condition(
    tokens: list[str],
    *,
    value_parser: Callable[[list[str]], Value | None],
) -> Condition | None:
    if not tokens:
        return None
    for marker, kind in _COMPARE_MARKERS.items():
        if marker in tokens:
            split_at = tokens.index(marker)
            left = value_parser(tokens[:split_at])
            right = value_parser(tokens[split_at + 1 :])
            if left is None or right is None:
                return None
            if kind == "eq":
                return CompareEq(left, right)
            if kind == "ne":
                return CompareNe(left, right)
            if kind == "lt":
                return CompareLt(left, right)
            if kind == "gt":
                return CompareGt(left, right)
            if kind == "le":
                return CompareLe(left, right)
    for marker in ("sadr̥śam", "sadrisham", "sadṛśam"):
        if marker in tokens:
            split_at = tokens.index(marker)
            left = value_parser(tokens[:split_at])
            right = value_parser(tokens[split_at + 1 :])
            if left is None or right is None:
                return None
            return CompareIdentity(left, right)
    if "asti" in tokens and len(tokens) >= 3:
        split_at = tokens.index("asti")
        container = value_parser(tokens[:split_at])
        key = value_parser(tokens[split_at + 1 :])
        if container is not None and key is not None:
            return CompareMembership(container, key)
    return None


def parse_condition_tokens(
    tokens: list[str],
    *,
    value_parser: Callable[[list[str]], Value | None] | None = None,
) -> Condition | None:
    if value_parser is None:
        value_parser = lambda part: parse_value_tokens(part)
    if not tokens:
        return None
    if tokens[0] == "na":
        inner = parse_condition_tokens(tokens[1:], value_parser=value_parser)
        if inner is None:
            return None
        return BoolNotCond(inner)
    parts = _split_bool_tokens(tokens, "vā", value_parser=value_parser)
    if len(parts) > 1:
        result: Condition | None = parts[0]
        for part in parts[1:]:
            if result is None:
                return None
            result = BoolOrCond(result, part)
        return result
    parts = _split_bool_tokens(tokens, "ca", value_parser=value_parser)
    if len(parts) > 1:
        result = parts[0]
        for part in parts[1:]:
            if result is None:
                return None
            result = BoolAndCond(result, part)
        return result
    return _parse_atomic_condition(tokens, value_parser=value_parser)


def _split_bool_tokens(
    tokens: list[str],
    marker: str,
    *,
    value_parser: Callable[[list[str]], Value | None],
) -> list[Condition]:
    segments: list[list[str]] = []
    current: list[str] = []
    index = 0
    while index < len(tokens):
        if tokens[index] == marker and _outside_text_literal(tokens, index):
            if current:
                segments.append(current)
            current = []
            index += 1
            continue
        current.append(tokens[index])
        index += 1
    if current:
        segments.append(current)
    conditions: list[Condition] = []
    for segment in segments:
        cond = _parse_atomic_condition(segment, value_parser=value_parser)
        if cond is not None:
            conditions.append(cond)
    return conditions


def _outside_text_literal(tokens: list[str], index: int) -> bool:
    in_text = False
    for position, token in enumerate(tokens):
        if token in _TEXT_MARKERS:
            in_text = True
        if token == "iti":
            in_text = False
        if position == index:
            return not in_text
    return True


def parse_value_tokens(
    tokens: list[str],
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> Value | None:
    if not tokens:
        return None

    if tokens[0] == "na":
        operand = _parse_value_tokens_core(tokens[1:], known_modules=known_modules)
        if operand is None:
            return None
        return BoolNot(operand)

    parts = _split_value_bool_tokens(tokens, "vā", known_modules=known_modules)
    if len(parts) > 1:
        result = parts[0]
        for part in parts[1:]:
            if result is None:
                return None
            result = BoolOr(result, part)
        return result

    parts = _split_value_bool_tokens(tokens, "ca", known_modules=known_modules)
    if len(parts) > 1:
        result = parts[0]
        for part in parts[1:]:
            if result is None:
                return None
            result = BoolAnd(result, part)
        return result

    return _parse_value_tokens_core(tokens, known_modules=known_modules)


def _lemma_from_token(token: str) -> str:
    try:
        return canonical_identifier(token, facade=get_default_facade())
    except IdentifierError:
        return token


def parse_call_arg_tokens(
    tokens: list[str],
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> tuple[tuple[Value, ...], tuple[tuple[str, Value], ...]]:
    """Positional args plus keyword args written as VALUE iti paramName."""
    positional: list[Value] = []
    kwargs: list[tuple[str, Value]] = []
    index = 0
    while index < len(tokens):
        # Support natural text literals written with a "source" marker,
        # e.g. "likha vākyam <words> iti" where the marker itself becomes a
        # dynamic text value.
        if tokens[index] in _TEXT_MARKERS and "iti" in tokens[index + 1 :]:
            end = tokens.index("iti", index + 1)
            text = _text_literal_from_tokens(tokens[index : end + 1])
            if text is not None:
                positional.append(text)
                index = end + 1
                continue
        if index + 2 < len(tokens) and tokens[index + 1] == "iti":
            value = parse_value_tokens([tokens[index]], known_modules=known_modules)
            if value is not None:
                kwargs.append((_lemma_from_token(tokens[index + 2]), value))
                index += 3
                continue
        chunk_end = index + 1
        while chunk_end <= len(tokens):
            if chunk_end < len(tokens) and tokens[chunk_end] == "iti":
                break
            trial = parse_value_tokens(tokens[index:chunk_end], known_modules=known_modules)
            if trial is None:
                break
            chunk_end += 1
        if chunk_end > index + 1:
            chunk_end -= 1
        value = parse_value_tokens(tokens[index:chunk_end], known_modules=known_modules)
        if value is not None:
            positional.append(value)
            index = chunk_end
        else:
            index += 1
    return tuple(positional), tuple(kwargs)


def _parse_value_tokens_core(
    tokens: list[str],
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> Value | None:
    if not tokens:
        return None

    curry = False
    start = 0
    if tokens[0] in {"anukrameṇa", "anukramena"}:
        curry = True
        start = 1
    if start < len(tokens) and tokens[start] in {"āṃśikam", "amshikam", "aṃśikam", "ansikam"}:
        inner = _parse_value_tokens_core(tokens[start + 1 :], known_modules=known_modules)
        if inner is None:
            return None
        if isinstance(inner, CallValue):
            return PartialApply(
                Reference(inner.name),
                args=inner.args,
                kwargs=inner.kwargs,
                curry=curry,
            )
        return PartialApply(inner, curry=curry)

    if tokens[0] in {"pariveṣṭanam", "parivestanam"} and "antam" in tokens:
        end = tokens.index("antam")
        inner = _parse_value_tokens_core(tokens[1:end], known_modules=known_modules)
        if inner is None:
            return None
        return GroupValue(inner)

    if len(tokens) == 1 and tokens[0] in {"śūnyam", "shunyam"}:
        return NilLiteral()

    call_value = _call_value_from_tokens(tokens, known_modules=known_modules)
    if call_value is not None:
        return call_value
    binary_value = _binary_value_from_tokens(tokens, known_modules=known_modules)
    if binary_value is not None:
        return binary_value
    text = _text_literal_from_tokens(tokens)
    if text is not None:
        return text
    if len(tokens) == 1:
        token = tokens[0]
        if token in _SOURCE_INT_WORDS:
            return Literal(_SOURCE_INT_WORDS[token])
        if re.fullmatch(r"\d+", token):
            return Literal(int(token))
        if token in {"satyam", "asatyam"}:
            return BoolLiteral(token == "satyam")
        if re.fullmatch(r"\d+\.\d+", token):
            return FloatLiteral(float(token))
    facade = get_default_facade()
    for token in tokens:
        try:
            analysis = facade.analyze_token(token)
        except Exception:
            continue
        if analysis.value is not None:
            return Literal(analysis.value)
        if analysis.pos == PartOfSpeech.NOUN:
            return Reference(analysis.lemma)
    if len(tokens) == 1:
        try:
            return Reference(canonical_identifier(tokens[0], facade=facade))
        except IdentifierError:
            return None
    return None


def _split_value_bool_tokens(
    tokens: list[str],
    marker: str,
    *,
    known_modules: set[str] | frozenset[str],
) -> list[Value]:
    segments: list[list[str]] = []
    current: list[str] = []
    index = 0
    while index < len(tokens):
        if tokens[index] == marker and _outside_text_literal(tokens, index):
            if current:
                segments.append(current)
            current = []
            index += 1
            continue
        current.append(tokens[index])
        index += 1
    if current:
        segments.append(current)
    values: list[Value] = []
    for segment in segments:
        value = _parse_value_tokens_core(segment, known_modules=known_modules)
        if value is not None:
            values.append(value)
    return values


def _binary_value_from_tokens(
    tokens: list[str],
    *,
    known_modules: set[str] | frozenset[str],
) -> Value | None:
    from .ast import BinaryValue

    for index, token in enumerate(tokens):
        operator = _BINARY_VALUE_OPERATORS.get(token)
        if operator is None or index == 0 or index == len(tokens) - 1:
            continue
        left = _parse_value_tokens_core(tokens[:index], known_modules=known_modules)
        right = _parse_value_tokens_core(tokens[index + 1 :], known_modules=known_modules)
        if left is not None and right is not None:
            return BinaryValue(operator, left, right)
    return None


def _call_value_from_tokens(
    tokens: list[str],
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> CallValue | None:
    if len(tokens) < 2 or tokens[0] not in {"āhvānam", "ahvanam"}:
        return None
    if len(tokens) >= 3 and tokens[1] in known_modules:
        args, kwargs = parse_call_arg_tokens(tokens[3:], known_modules=known_modules)
        return CallValue(tokens[2], module=tokens[1], args=args, kwargs=kwargs)
    args, kwargs = parse_call_arg_tokens(tokens[2:], known_modules=known_modules)
    return CallValue(tokens[1], args=args, kwargs=kwargs)


def _text_literal_from_tokens(tokens: list[str]) -> TextLiteral | None:
    if len(tokens) >= 3 and tokens[0] in _TEXT_MARKERS and tokens[-1] == "iti":
        words = tokens[1:-1]
        if words:
            return TextLiteral(" ".join(words))
    return None


def _values_from_tokens(
    tokens: list[str],
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> tuple[Value, ...]:
    values: list[Value] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token in _TEXT_MARKERS and "iti" in tokens[index + 1 :]:
            end = tokens.index("iti", index + 1)
            text = _text_literal_from_tokens(tokens[index : end + 1])
            if text is not None:
                values.append(text)
                index = end + 1
                continue
        value = parse_value_tokens([token], known_modules=known_modules)
        if value is not None:
            values.append(value)
        index += 1
    return tuple(values)


def parse_bytes_payload(tokens: list[str]) -> bytes | None:
    if len(tokens) >= 3 and tokens[0] in _TEXT_MARKERS and tokens[-1] == "iti":
        return " ".join(tokens[1:-1]).encode("utf-8")
    try:
        return bytes.fromhex("".join(tokens))
    except ValueError:
        return None
