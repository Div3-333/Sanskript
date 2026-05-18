from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .grammar import Analysis, IndeclinableKind, PartOfSpeech, Person, Role


class SentenceKind(str, Enum):
    STATEMENT = "statement"
    QUESTION = "question"
    RELATIVE = "relative"
    VERBLESS = "verbless"
    COORDINATED = "coordinated"


@dataclass(frozen=True)
class SentenceProfile:
    kind: SentenceKind
    finite_verbs: tuple[str, ...]
    participants: tuple[str, ...]
    particles: tuple[str, ...]


@dataclass(frozen=True)
class AgreementCheck:
    agrees: bool
    subject: str | None
    verb: str | None
    reason: str


def profile_sentence(analyses: Iterable[Analysis]) -> SentenceProfile:
    items = tuple(analyses)
    verbs = tuple(item.surface for item in items if item.pos == PartOfSpeech.VERB)
    participants = tuple(item.surface for item in items if item.role is not None)
    particles = tuple(item.surface for item in items if item.pos == PartOfSpeech.INDECLINABLE)
    return SentenceProfile(
        kind=classify_sentence(items),
        finite_verbs=verbs,
        participants=participants,
        particles=particles,
    )


def classify_sentence(analyses: Iterable[Analysis]) -> SentenceKind:
    items = tuple(analyses)
    kinds = {item.indeclinable_kind for item in items if item.indeclinable_kind is not None}
    has_verb = any(item.pos == PartOfSpeech.VERB for item in items)

    if IndeclinableKind.QUESTION in kinds:
        return SentenceKind.QUESTION
    if IndeclinableKind.RELATIVE in kinds:
        return SentenceKind.RELATIVE
    if not has_verb:
        return SentenceKind.VERBLESS
    if kinds.intersection({IndeclinableKind.CONJUNCTION, IndeclinableKind.ALTERNATIVE}):
        return SentenceKind.COORDINATED
    return SentenceKind.STATEMENT


def check_subject_verb_agreement(analyses: Iterable[Analysis]) -> AgreementCheck:
    items = tuple(analyses)
    subjects = [item for item in items if item.role == Role.KARTR]
    verbs = [item for item in items if item.pos == PartOfSpeech.VERB]

    if not subjects or not verbs:
        return AgreementCheck(True, None, verbs[0].surface if verbs else None, "no explicit subject-verb pair")
    if len(subjects) != 1 or len(verbs) != 1:
        return AgreementCheck(False, None, None, "agreement requires exactly one subject and one finite verb")

    subject = subjects[0]
    verb = verbs[0]
    expected_person = subject.person or Person.THIRD
    agrees = subject.number == verb.number and expected_person == verb.person
    reason = "subject and finite verb agree" if agrees else "subject and finite verb differ in person or number"
    return AgreementCheck(agrees, subject.surface, verb.surface, reason)
