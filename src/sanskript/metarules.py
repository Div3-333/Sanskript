from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RuleBehavior(str, Enum):
    TECHNICAL_MARKER = "technical_marker"
    OPTIONALITY = "optionality"
    SUBSTITUTION = "substitution"
    PROHIBITION = "prohibition"
    RECURSION = "recursion"
    OVERRIDE = "override"
    DOMAIN = "domain"


@dataclass(frozen=True)
class MetaRule:
    sutra_range: str
    behavior: RuleBehavior
    name: str
    compiler_use: str


@dataclass(frozen=True)
class CanonDirective:
    input_form: str
    output_form: str
    rule: MetaRule
    optional: bool = False


META_RULES: tuple[MetaRule, ...] = (
    MetaRule("1.2", RuleBehavior.TECHNICAL_MARKER, "it-marker discipline", "tracks markers that guide derivation and then disappear"),
    MetaRule("1.2", RuleBehavior.OPTIONALITY, "vā-option", "marks grammatically licensed alternatives without treating them as parser hacks"),
    MetaRule("1.2", RuleBehavior.PROHIBITION, "blocking conditions", "records when a later operation is grammatically unavailable"),
    MetaRule("1.3", RuleBehavior.DOMAIN, "pada and voice domains", "keeps parasmaipada and ātmanepada choices attached to verbal morphology"),
    MetaRule("1.3", RuleBehavior.RECURSION, "anuvṛtti carry", "carries a governing condition into later rules until its domain closes"),
    MetaRule("8.1", RuleBehavior.OVERRIDE, "sentence-edge operations", "models clause-bound late operations separately from word formation"),
)


def rules_for_range(sutra_range: str) -> tuple[MetaRule, ...]:
    return tuple(rule for rule in META_RULES if rule.sutra_range == sutra_range)


def directive(input_form: str, output_form: str, behavior: RuleBehavior, optional: bool = False) -> CanonDirective:
    for rule in META_RULES:
        if rule.behavior == behavior:
            return CanonDirective(input_form=input_form, output_form=output_form, rule=rule, optional=optional)
    raise ValueError(f"No metarule registered for {behavior.value!r}")
