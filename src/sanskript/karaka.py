from __future__ import annotations

from dataclasses import dataclass

from .grammar import CASE_TO_ROLE, Case, Role


@dataclass(frozen=True)
class KarakaExplanation:
    case: Case
    role: Role | None
    gloss: str
    compiler_use: str


KARAKA_EXPLANATIONS = {
    Case.NOMINATIVE: KarakaExplanation(Case.NOMINATIVE, Role.KARTR, "agent or subject", "actor or named agent"),
    Case.ACCUSATIVE: KarakaExplanation(Case.ACCUSATIVE, Role.KARMAN, "object acted on", "value or mutable target"),
    Case.INSTRUMENTAL: KarakaExplanation(Case.INSTRUMENTAL, Role.KARANA, "means or instrument", "tool, amount, or operand"),
    Case.DATIVE: KarakaExplanation(Case.DATIVE, Role.SAMPRADANA, "recipient", "destination or continuation target"),
    Case.ABLATIVE: KarakaExplanation(Case.ABLATIVE, Role.APADANA, "source or separation", "source, lower bound, or comparison base"),
    Case.GENITIVE: KarakaExplanation(Case.GENITIVE, None, "relation or possession", "ownership, module, or field relation"),
    Case.LOCATIVE: KarakaExplanation(Case.LOCATIVE, Role.ADHIKARANA, "location or context", "storage location or scope"),
    Case.VOCATIVE: KarakaExplanation(Case.VOCATIVE, None, "address", "interactive address or diagnostic target"),
}


def role_for_case(case: Case) -> Role | None:
    return CASE_TO_ROLE.get(case)


def explain_case(case: Case) -> KarakaExplanation:
    return KARAKA_EXPLANATIONS[case]
