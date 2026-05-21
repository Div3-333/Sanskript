"""Adhyāya 8 registry (samāsānta, asiddha, saṃhitā sandhi, avasāna).

Discrete implementations live in ``sutra_impl_8_1`` … ``sutra_impl_8_4``.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .sutra_logic import atomic_evidence_for, has_discrete_sutra_logic


class RuleKind(str, Enum):
    SAMASANTA = "samasanta"
    ASIDDHA = "asiddha"
    SAMHITA_SANDHI = "samhita_sandhi"
    AVASANA = "avasana"


class ImplementationMode(str, Enum):
    EXECUTABLE = "executable_anchor"
    SEMANTIC = "semantic_scaffold"
    ATOMIC_EXECUTABLE = "atomic_executable"
    ATOMIC_FORMAL = "atomic_formal"
    DISCRETE = "discrete_executable"


@dataclass(frozen=True)
class RuleExample:
    input: str
    output: str
    note: str


@dataclass(frozen=True)
class SutraRule:
    id: str
    pada: str
    kind: RuleKind
    mode: ImplementationMode
    title: str
    compiler_effect: str
    hooks: tuple[str, ...]
    examples: tuple[RuleExample, ...]
    sutra_text_devanagari: str = ""
    sutra_text_iast: str = ""
    source: str = ""
    anuvritti: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    exceptions: tuple[str, ...] = ()
    counterexamples: tuple[RuleExample, ...] = ()

    @property
    def implemented(self) -> bool:
        return self.mode == ImplementationMode.DISCRETE and self.atomic and has_discrete_sutra_logic(self.id)

    @property
    def atomic(self) -> bool:
        return all(
            (
                self.sutra_text_devanagari,
                self.sutra_text_iast,
                self.source,
                self.anuvritti,
                self.conditions,
                self.examples,
                self.counterexamples,
                self.hooks,
            )
        )


PADA_COUNTS = {
    "8.1": 74,
    "8.2": 108,
    "8.3": 119,
    "8.4": 68,
}

PADA_INDICES = {pada: tuple(range(1, count + 1)) for pada, count in PADA_COUNTS.items()}

SPECIAL_RULES: dict[str, tuple[RuleKind, str, str, tuple[str, ...], str, ImplementationMode]] = {
    "8.1.1": (
        RuleKind.SAMASANTA,
        "sarvāsya dve",
        "dvigu compounds take dual inflection on both members",
        ("sanskript.samasa.create_compound",),
        "dvigu dual",
        ImplementationMode.EXECUTABLE,
    ),
    "8.2.1": (
        RuleKind.ASIDDHA,
        "pūrvatrāsiddham",
        "earlier rule is asiddha relative to later operation",
        ("sanskript.metarules",),
        "asiddha scope",
        ImplementationMode.EXECUTABLE,
    ),
    "8.3.1": (
        RuleKind.SAMHITA_SANDHI,
        "matuvaso ru sambuddhau chandasi",
        "ru substitute after matup/vasu in vocative chandas",
        ("sanskript.sandhi.join_words",),
        "ru sambuddhi",
        ImplementationMode.EXECUTABLE,
    ),
    "8.4.1": (
        RuleKind.SAMHITA_SANDHI,
        "raṣābhyāṃ no ṇaḥ samānapade",
        "blocks ṇ between r/ṣ in same pada",
        ("sanskript.phonology.is_consonant",),
        "ṇ block",
        ImplementationMode.EXECUTABLE,
    ),
    "8.4.68": (
        RuleKind.AVASANA,
        "a a iti",
        "period (avasāna) after final a",
        ("sanskript.categories.is_avasana",),
        "period",
        ImplementationMode.EXECUTABLE,
    ),
}

PADA_PROFILES: dict[str, tuple[RuleKind, str, str, tuple[str, ...]]] = {
    "8.1": (
        RuleKind.SAMASANTA,
        "samāsānta and compound-final rule",
        "records dvigu, copulative, and other compound-final inflection and suffix behavior",
        ("sanskript.samasa.create_compound", "sanskript.subanta.iter_nominal_analyses"),
    ),
    "8.2": (
        RuleKind.ASIDDHA,
        "asiddha and internal sandhi ordering rule",
        "records blocking (asiddha), ordering, and internal saṃhitā constraints",
        ("sanskript.metarules", "sanskript.sandhi.join_words"),
    ),
    "8.3": (
        RuleKind.SAMHITA_SANDHI,
        "external saṃhitā sandhi rule",
        "records visarga, ru/lu substitution, lopa, and chandas-specific saṃhitā operations",
        ("sanskript.sandhi.join_words", "sanskript.sandhi.apply_visarga_sandhi"),
    ),
    "8.4": (
        RuleKind.AVASANA,
        "avasāna and sentence-edge rule",
        "records final pause, period, and pada-boundary phonology",
        ("sanskript.categories.is_avasana", "sanskript.categories.is_samhita"),
    ),
}


def rule_for(sutra_id: str) -> SutraRule:
    try:
        return ADHYAYA8_RULES[sutra_id]
    except KeyError as exc:
        raise ValueError(f"No Adhyāya 8 rule for {sutra_id!r}") from exc


def rules_for_pada(pada: str) -> tuple[SutraRule, ...]:
    return tuple(rule for rule in ADHYAYA8_RULES.values() if rule.pada == pada)


def expected_adhyaya8_ids() -> tuple[str, ...]:
    return tuple(f"{pada}.{index}" for pada in PADA_COUNTS for index in PADA_INDICES[pada])


def missing_rule_ids() -> tuple[str, ...]:
    return tuple(sutra_id for sutra_id in expected_adhyaya8_ids() if sutra_id not in ADHYAYA8_RULES)


def implemented_sutra_ids() -> frozenset[str]:
    return frozenset(sutra_id for sutra_id, rule in ADHYAYA8_RULES.items() if rule.implemented)


def partial_sutra_ids() -> frozenset[str]:
    return frozenset(sutra_id for sutra_id, rule in ADHYAYA8_RULES.items() if not rule.implemented)


def implementation_note_for(sutra_id: str) -> str:
    rule = rule_for(sutra_id)
    mode = "Discrete executable" if rule.mode == ImplementationMode.DISCRETE else "Partial"
    hooks = ", ".join(rule.hooks)
    return f"{mode} Adhyāya 8 implementation: {rule.sutra_text_iast}. {rule.compiler_effect} Hooks: {hooks}."


def partial_implementation_note_for(sutra_id: str) -> str:
    rule = rule_for(sutra_id)
    hooks = ", ".join(rule.hooks)
    if rule.mode in {ImplementationMode.ATOMIC_EXECUTABLE, ImplementationMode.ATOMIC_FORMAL}:
        prefix = "Atomic metadata only"
    elif rule.mode == ImplementationMode.EXECUTABLE:
        prefix = "Executable anchor only"
    else:
        prefix = "Semantic scaffold only"
    return (
        f"{prefix}, not a complete discrete Paninian sutra implementation: "
        f"{rule.compiler_effect} Required before completion: exact sutra text, inherited domain, "
        f"conditions, exceptions, rule-specific executable logic, positive behavioral tests, "
        f"negative behavioral tests, and reviewer notes. Hooks: {hooks}."
    )


def _example(tag: str, output: str, note: str) -> tuple[RuleExample, ...]:
    return (RuleExample(tag, output, note),)


def _build_rules() -> dict[str, SutraRule]:
    rules: dict[str, SutraRule] = {}
    for sutra_id in expected_adhyaya8_ids():
        pada, index_text = sutra_id.rsplit(".", 1)
        index = int(index_text)
        if sutra_id in SPECIAL_RULES:
            kind, title, effect, hooks, output, mode = SPECIAL_RULES[sutra_id]
        else:
            kind, base_title, effect, hooks = PADA_PROFILES[pada]
            title = f"{base_title} {index}"
            output = kind.value
            mode = ImplementationMode.SEMANTIC
        sutra_text_devanagari = ""
        sutra_text_iast = ""
        source = ""
        anuvritti: tuple[str, ...] = ()
        conditions: tuple[str, ...] = ()
        exceptions: tuple[str, ...] = ()
        counterexamples: tuple[RuleExample, ...] = ()
        if has_discrete_sutra_logic(sutra_id):
            evidence = atomic_evidence_for(sutra_id)
            mode = ImplementationMode.DISCRETE
            sutra_text_devanagari = str(evidence["sutra_text_devanagari"])
            sutra_text_iast = str(evidence["sutra_text_iast"])
            source = str(evidence["source"])
            anuvritti = tuple(evidence["anuvritti"])
            conditions = tuple(evidence["conditions"])
            exceptions = tuple(evidence["exceptions"])
            counterexamples = (
                RuleExample(sutra_id, str(evidence["negative_example"]), "rejected by the sutra-specific predicate"),
            )
        rules[sutra_id] = SutraRule(
            id=sutra_id,
            pada=pada,
            kind=kind,
            mode=mode,
            title=title,
            compiler_effect=effect,
            hooks=hooks,
            examples=_example(title, output, effect),
            sutra_text_devanagari=sutra_text_devanagari,
            sutra_text_iast=sutra_text_iast,
            source=source,
            anuvritti=anuvritti,
            conditions=conditions,
            exceptions=exceptions,
            counterexamples=counterexamples,
        )
    return rules


ADHYAYA8_RULES = _build_rules()
