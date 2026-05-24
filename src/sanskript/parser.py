from __future__ import annotations

from collections.abc import Callable
from typing import Iterable

from .ast import Assign, Decrease, Display, Increase, Literal, Reference, Statement, Value
from .errors import ParseError
from .grammar import VERB_FRAMES, Analysis, FrameOperation, PartOfSpeech, Role, VerbFrame
from .morphology_facade import get_default_facade
from .morphology import split_sentences


def parse_program(source: str) -> list[Statement]:
    return [parse_sentence(sentence) for sentence in split_sentences(source)]


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


def _build_display(frame: VerbFrame, roles: dict[Role, list[Analysis]]) -> Display:
    return Display(value=_value_from(_single(roles, _frame_role(frame, "value_role"))))


FRAME_DISPATCH: dict[FrameOperation, FrameBuilder] = {
    FrameOperation.ASSIGN: _build_assign,
    FrameOperation.INCREASE: _build_increase,
    FrameOperation.DECREASE: _build_decrease,
    FrameOperation.DISPLAY: _build_display,
}


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
