from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Accent(str, Enum):
    UDATTA = "udātta"
    ANUDATTA = "anudātta"
    SVARITA = "svarita"
    PRACAYA = "pracaya"


@dataclass(frozen=True)
class AccentAssignment:
    token: str
    accent: Accent
    position: int


@dataclass(frozen=True)
class AccentProfile:
    domain: str
    assignments: tuple[AccentAssignment, ...]
    sutra_range: str

    @property
    def primary(self) -> AccentAssignment | None:
        return next((item for item in self.assignments if item.accent == Accent.UDATTA), None)


ACCENT_DOMAINS = {
    "6.2": "compound and pada accent domains",
    "6.3": "uttarapada and internal accent-sensitive domains",
    "6.4": "late stem-final operations that interact with accent",
}


def profile_accent(tokens: tuple[str, ...], udatta_index: int = 0, sutra_range: str = "6.2") -> AccentProfile:
    if not tokens:
        raise ValueError("Accent profiles need at least one token")
    if udatta_index < 0 or udatta_index >= len(tokens):
        raise ValueError(f"udātta index out of range: {udatta_index}")

    assignments = []
    for index, token in enumerate(tokens):
        accent = Accent.UDATTA if index == udatta_index else Accent.ANUDATTA
        assignments.append(AccentAssignment(token=token, accent=accent, position=index))
    return AccentProfile(
        domain=ACCENT_DOMAINS.get(sutra_range, "controlled accent domain"),
        assignments=tuple(assignments),
        sutra_range=sutra_range,
    )


def assign_svarita(profile: AccentProfile, token: str) -> AccentProfile:
    assignments = tuple(
        AccentAssignment(item.token, Accent.SVARITA if item.token == token else item.accent, item.position)
        for item in profile.assignments
    )
    return AccentProfile(domain=profile.domain, assignments=assignments, sutra_range=profile.sutra_range)
