from __future__ import annotations

from collections.abc import Callable
from typing import Iterable

from .ast import (
    Assign,
    Call,
    CompareEq,
    Decrease,
    Display,
    FunctionDef,
    If,
    Increase,
    Literal,
    Multiply,
    Program,
    Reference,
    Return,
    Statement,
    Value,
    While,
)
from .errors import ParseError
from .grammar import VERB_FRAMES, Analysis, FrameOperation, PartOfSpeech, Role, VerbFrame
from .morphology import split_sentences
from .morphology_facade import get_default_facade
import re

_BLOCK_END_MARKERS = frozenset({"antam", "anta", "yadi", "punaḥ", "punah", "vidhānam", "vidhanam", "samāpanam", "samapanam"})


def parse_program(source: str) -> Program:
    sentences = split_sentences(source)
    statements: list[Statement] = []
    functions: list[FunctionDef] = []
    modules: list[tuple[str, tuple[FunctionDef, ...]]] = []

    index = 0
    current_module: str | None = None
    module_functions: list[FunctionDef] = []
    known_modules: set[str] = set()

    while index < len(sentences):
        sentence = sentences[index].strip()
        if not sentence:
            index += 1
            continue

        header = _parse_directive_header(sentence, known_modules=known_modules)
        if header is not None:
            kind, payload = header
            if kind == "module":
                if current_module and module_functions:
                    modules.append((current_module, tuple(module_functions)))
                current_module = payload
                known_modules.add(current_module)
                module_functions = []
                index += 1
                continue
            if kind == "function":
                name, params = payload
                index += 1
                body, index = _collect_until(
                    sentences,
                    index,
                    end_markers={"samāpanam", "samapanam"},
                    known_modules=known_modules,
                )
                fn = FunctionDef(name, body, module=current_module, params=params)
                if current_module:
                    module_functions.append(fn)
                else:
                    functions.append(fn)
                continue
            if kind == "if":
                condition = payload
                index += 1
                then_body, index = _collect_until(
                    sentences,
                    index,
                    end_markers={"anyathā", "anyatha", "antam", "anta"},
                    stop_before_markers=True,
                    known_modules=known_modules,
                )
                else_body: tuple[Statement, ...] = ()
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"anyathā", "anyatha"}):
                    index += 1
                    else_body, index = _collect_until(
                        sentences,
                        index,
                        end_markers=_BLOCK_END_MARKERS,
                        stop_before_markers=True,
                        known_modules=known_modules,
                    )
                if index < len(sentences) and _is_marker_sentence(
                    sentences[index], {"antam", "anta"}
                ):
                    index += 1
                statements.append(If(condition, then_body, else_body))
                continue
            if kind == "while":
                condition = payload
                index += 1
                body, index = _collect_until(
                    sentences,
                    index,
                    end_markers=_BLOCK_END_MARKERS,
                    stop_before_markers=True,
                    known_modules=known_modules,
                )
                if index < len(sentences) and _is_marker_sentence(
                    sentences[index], {"antam", "anta"}
                ):
                    index += 1
                statements.append(While(condition, body))
                continue
            if kind == "call":
                module_name, fn_name, args = payload
                statements.append(Call(fn_name, module=module_name, args=args))
                index += 1
                continue
            if kind == "return":
                statements.append(Return(payload))
                index += 1
                continue

        if _is_marker_sentence(sentence, {"samāpanam", "samapanam"}):
            if current_module and module_functions:
                modules.append((current_module, tuple(module_functions)))
                current_module = None
                module_functions = []
            index += 1
            continue

        statements.append(parse_sentence(sentence))
        index += 1

    if current_module and module_functions:
        modules.append((current_module, tuple(module_functions)))

    return Program(tuple(statements), tuple(functions), tuple(modules))


def parse_sentence(sentence: str) -> Statement:
    facade = get_default_facade()
    analyses = facade.analyze_sentence(sentence)
    verbs = [item for item in analyses if item.pos == PartOfSpeech.VERB]
    if len(verbs) != 1:
        raise ParseError(f"Expected exactly one finite verb, found {len(verbs)} in {sentence!r}")

    verb = verbs[0]
    try:
        frame = VERB_FRAMES[verb.surface]
    except KeyError as exc:
        raise ParseError(
            f"No verb frame has been declared for {verb.surface!r}",
            hint="Declare the surface in data/verb_frames.json and rebuild the lexicon.",
        ) from exc

    _validate_verb_analysis(verb, frame)
    facade.validate_karaka(analyses, verb)

    roles = _roles_by_type(item for item in analyses if item.pos != PartOfSpeech.VERB)
    try:
        return FRAME_DISPATCH[frame.operation](frame, roles)
    except KeyError as exc:
        raise ParseError(
            f"No parser operation has been declared for {frame.operation.value!r}",
            hint="Add the operation to parser.FRAME_DISPATCH.",
        ) from exc


FrameBuilder = Callable[[VerbFrame, dict[Role, list[Analysis]]], Statement]


def _build_assign(frame: VerbFrame, roles: dict[Role, list[Analysis]]) -> Assign:
    return Assign(
        target=_single(roles, _frame_role(frame, "target_role")).lemma,
        value=_value_from(_single(roles, _frame_role(frame, "value_role"))),
    )


def _build_increase(frame: VerbFrame, roles: dict[Role, list[Analysis]]) -> Increase:
    return Increase(
        target=_single(roles, _frame_role(frame, "target_role")).lemma,
        amount=_value_from(_single(roles, _frame_role(frame, "amount_role"))),
    )


def _build_decrease(frame: VerbFrame, roles: dict[Role, list[Analysis]]) -> Decrease:
    return Decrease(
        target=_single(roles, _frame_role(frame, "target_role")).lemma,
        amount=_value_from(_single(roles, _frame_role(frame, "amount_role"))),
    )


def _build_multiply(frame: VerbFrame, roles: dict[Role, list[Analysis]]) -> Multiply:
    return Multiply(
        target=_single(roles, _frame_role(frame, "target_role")).lemma,
        factor=_value_from(_single(roles, _frame_role(frame, "amount_role"))),
    )


def _build_display(frame: VerbFrame, roles: dict[Role, list[Analysis]]) -> Display:
    return Display(value=_value_from(_single(roles, _frame_role(frame, "value_role"))))


FRAME_DISPATCH: dict[FrameOperation, FrameBuilder] = {
    FrameOperation.ASSIGN: _build_assign,
    FrameOperation.INCREASE: _build_increase,
    FrameOperation.DECREASE: _build_decrease,
    FrameOperation.MULTIPLY: _build_multiply,
    FrameOperation.DISPLAY: _build_display,
}


def _parse_directive_header(
    sentence: str,
    *,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> tuple[str, object] | None:
    tokens = _directive_tokens(sentence)
    if not tokens:
        return None

    first = tokens[0]
    if first in {"kṣetram", "ksetram"} and len(tokens) >= 2:
        return ("module", tokens[1])

    if first in {"vidhānam", "vidhanam"} and len(tokens) >= 2:
        return ("function", (tokens[1], tuple(_identifier_from_token(token) for token in tokens[2:])))

    if first in {"āhvānam", "ahvanam"}:
        if len(tokens) >= 2:
            if len(tokens) >= 3 and tokens[1] in known_modules:
                return ("call", (tokens[1], tokens[2], _values_from_tokens(tokens[3:])))
            return ("call", (None, tokens[1], _values_from_tokens(tokens[2:])))
        return None

    if first in {"pratyāvartanam", "pratyavartanam"}:
        if len(tokens) == 1:
            return ("return", None)
        value = _value_from_tokens(tokens[1:])
        if value is None:
            return None
        return ("return", value)

    if first == "punaḥ" or first == "punah":
        condition = _parse_compare_tokens(tokens[1:])
        if condition is not None:
            return ("while", condition)
        return None

    if first == "yadi":
        condition = _parse_compare_tokens(tokens[1:])
        if condition is not None:
            return ("if", condition)
        return None

    return None


def _parse_compare_tokens(tokens: list[str]) -> CompareEq | None:
    if "samam" not in tokens:
        return None
    split_at = tokens.index("samam")
    left_tokens = tokens[:split_at]
    right_tokens = tokens[split_at + 1 :]
    if not left_tokens or not right_tokens:
        return None
    left = _value_from_tokens(left_tokens)
    right = _value_from_tokens(right_tokens)
    if left is None or right is None:
        return None
    return CompareEq(left, right)


def _value_from_tokens(tokens: list[str]) -> Value | None:
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
        return Reference(tokens[0])
    return None


def _values_from_tokens(tokens: list[str]) -> tuple[Value, ...]:
    values: list[Value] = []
    for token in tokens:
        value = _value_from_tokens([token])
        if value is not None:
            values.append(value)
    return tuple(values)


def _identifier_from_token(token: str) -> str:
    facade = get_default_facade()
    try:
        analysis = facade.analyze_token(token)
    except Exception:
        return token
    if analysis.value is None and analysis.pos == PartOfSpeech.NOUN:
        return analysis.lemma
    return token


def _collect_until(
    sentences: list[str],
    index: int,
    *,
    end_markers: set[str],
    stop_before_markers: bool = False,
    known_modules: set[str] | frozenset[str] = frozenset(),
) -> tuple[tuple[Statement, ...], int]:
    body: list[Statement] = []
    while index < len(sentences):
        sentence = sentences[index].strip()
        if not sentence:
            index += 1
            continue
        if _is_marker_sentence(sentence, end_markers):
            if stop_before_markers:
                return tuple(body), index
            index += 1
            if not stop_before_markers:
                return tuple(body), index
            continue
        header = _parse_directive_header(sentence, known_modules=known_modules)
        if header is not None:
            if stop_before_markers:
                return tuple(body), index
            kind, payload = header
            if kind == "call":
                module_name, fn_name, args = payload
                body.append(Call(fn_name, module=module_name, args=args))
                index += 1
                continue
            if kind == "return":
                body.append(Return(payload))
                index += 1
                continue
            if kind == "if":
                condition = payload
                index += 1
                then_body, index = _collect_until(
                    sentences,
                    index,
                    end_markers={"anyathā", "anyatha", "antam", "anta"},
                    stop_before_markers=True,
                    known_modules=known_modules,
                )
                else_body: tuple[Statement, ...] = ()
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"anyathā", "anyatha"}):
                    index += 1
                    else_body, index = _collect_until(
                        sentences,
                        index,
                        end_markers=_BLOCK_END_MARKERS,
                        stop_before_markers=True,
                        known_modules=known_modules,
                    )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                body.append(If(condition, then_body, else_body))
                continue
            if kind == "while":
                condition = payload
                index += 1
                loop_body, index = _collect_until(
                    sentences,
                    index,
                    end_markers=_BLOCK_END_MARKERS,
                    stop_before_markers=True,
                    known_modules=known_modules,
                )
                if index < len(sentences) and _is_marker_sentence(sentences[index], {"antam", "anta"}):
                    index += 1
                body.append(While(condition, loop_body))
                continue
            return tuple(body), index
        body.append(parse_sentence(sentence))
        index += 1
    return tuple(body), index


def _is_marker_sentence(sentence: str, markers: set[str]) -> bool:
    tokens = _directive_tokens(sentence)
    return bool(tokens) and tokens[0] in markers


def _directive_tokens(sentence: str) -> list[str]:
    return [
        token.strip(".,;:!?।")
        for token in re.split(r"[\s,;]+", sentence)
        if token.strip(".,;:!?।")
    ]


def _roles_by_type(items: Iterable[Analysis]) -> dict[Role, list[Analysis]]:
    roles: dict[Role, list[Analysis]] = {}
    for item in items:
        if item.role is None:
            continue
        roles.setdefault(item.role, []).append(item)
    return roles


def _single(roles: dict[Role, list[Analysis]], role: Role) -> Analysis:
    matches = roles.get(role, [])
    if len(matches) != 1:
        raise ParseError(
            f"Expected exactly one {role.value} participant, found {len(matches)}",
            hint="Check that the participant has the vibhakti required by the verb frame.",
        )
    return matches[0]


def _frame_role(frame: VerbFrame, attribute: str) -> Role:
    role = getattr(frame, attribute)
    if role is None:
        raise ParseError(f"Verb frame {frame.surface!r} is missing {attribute}")
    return role


def _validate_verb_analysis(verb: Analysis, frame: VerbFrame) -> None:
    mismatches: list[str] = []
    for field in ("lemma", "person", "number", "lakara", "pada"):
        expected = getattr(frame, field)
        actual = getattr(verb, field)
        if actual != expected:
            expected_text = expected.value if hasattr(expected, "value") else expected
            actual_text = actual.value if hasattr(actual, "value") else actual
            mismatches.append(f"{field}={actual_text!r}, expected {expected_text!r}")
    if mismatches:
        raise ParseError(f"{verb.surface!r} does not match its verb frame: {', '.join(mismatches)}")


def _value_from(item: Analysis) -> Value:
    if item.value is not None:
        return Literal(item.value)
    return Reference(item.lemma)
