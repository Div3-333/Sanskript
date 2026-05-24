from __future__ import annotations

from typing import Iterable

from .ast import Assign, Decrease, Display, Increase, Literal, Reference, Statement, Value
from .errors import ParseError
from .grammar import VERB_FRAMES, Analysis, PartOfSpeech, Role
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
        raise ParseError(f"No verb frame has been declared for {verb.surface!r}") from exc

    facade.validate_karaka(analyses, verb)

    roles = _roles_by_type(item for item in analyses if item.pos != PartOfSpeech.VERB)

    if verb.surface == "nidadhāti":
        return Assign(
            target=_single(roles, Role.ADHIKARANA).lemma,
            value=_value_from(_single(roles, Role.KARMAN)),
        )

    if verb.surface == "vardhayati":
        return Increase(
            target=_single(roles, Role.KARMAN).lemma,
            amount=_value_from(_single(roles, Role.KARANA)),
        )

    if verb.surface == "nyūnayati":
        return Decrease(
            target=_single(roles, Role.KARMAN).lemma,
            amount=_value_from(_single(roles, Role.KARANA)),
        )

    if verb.surface == "darśayati":
        return Display(value=_value_from(_single(roles, Role.KARMAN)))

    raise ParseError(f"Unhandled verb frame: {verb.surface}")


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
        raise ParseError(f"Expected exactly one {role.value} participant, found {len(matches)}")
    return matches[0]


def _value_from(item: Analysis) -> Value:
    if item.value is not None:
        return Literal(item.value)
    return Reference(item.lemma)
