"""Adhyāya 7 registry (agama, vikara, ādeśa, ṇati/lopa).

Discrete implementations live in ``sutra_impl_7_1`` … ``sutra_impl_7_4``.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .sutra_logic import atomic_evidence_for, has_discrete_sutra_logic


class RuleKind(str, Enum):
    AGAMA = "agama"
    VIKARA = "vikara"
    ADESHA = "adesha"
    NT_LOPA = "nt_lopa"


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
    "7.1": 103,
    "7.2": 118,
    "7.3": 120,
    "7.4": 97,
}

PADA_INDICES = {pada: tuple(range(1, count + 1)) for pada, count in PADA_COUNTS.items()}

SPECIAL_RULES: dict[str, tuple[RuleKind, str, str, tuple[str, ...], str, ImplementationMode]] = {
    "7.2.1": (
        RuleKind.VIKARA,
        "sici vṛddhiḥ parasmai-padeṣu",
        "vṛddhi in sic before parasmaipada endings",
        ("sanskript.anga.vrddhi", "sanskript.anga.operations_for_range"),
        "sic vṛddhi",
        ImplementationMode.EXECUTABLE,
    ),
    "7.3.1": (
        RuleKind.ADESHA,
        "devikāśiṃśapādityavāṭ dīrgha-satra-śreyasām āt",
        "long āt after listed stems",
        ("sanskript.anga.operations_for_range",),
        "āt lengthening",
        ImplementationMode.EXECUTABLE,
    ),
    "7.4.1": (
        RuleKind.NT_LOPA,
        "ṇau caṅi upadhāyāḥ hrasvaḥ",
        "short vowel in ṇau caṅ with light penultimate",
        ("sanskript.phonology.is_consonant",),
        "ṇati hrasva",
        ImplementationMode.EXECUTABLE,
    ),
}

PADA_PROFILES: dict[str, tuple[RuleKind, str, str, tuple[str, ...]]] = {
    "7.1": (
        RuleKind.AGAMA,
        "agama and ending-insertion rule",
        "records augments and segment insertions before tiṅ/ārdhadhātuka endings",
        ("sanskript.anga.operations_for_range", "sanskript.anga.apply_anga_operation"),
    ),
    "7.2": (
        RuleKind.VIKARA,
        "vikara and guṇa-vṛddhi substitution rule",
        "records stem/suffix vowel strengthening before parasmaipada and related endings",
        ("sanskript.anga.guna", "sanskript.anga.vrddhi", "sanskript.anga.operations_for_range"),
    ),
    "7.3": (
        RuleKind.ADESHA,
        "ādeśa and pratyāhāra insertion rule",
        "records substitute segments (āt, num, nasal) and insertion domains",
        ("sanskript.anga.operations_for_range", "sanskript.anga.apply_anga_operation"),
    ),
    "7.4": (
        RuleKind.NT_LOPA,
        "ṇati retroflexion and lopa rule",
        "records ṇ insertion, retroflexion, and controlled lopa in pada-final domains",
        ("sanskript.anga.operations_for_range", "sanskript.phonology.is_consonant"),
    ),
}


def rule_for(sutra_id: str) -> SutraRule:
    try:
        return ADHYAYA7_RULES[sutra_id]
    except KeyError as exc:
        raise ValueError(f"No Adhyāya 7 rule for {sutra_id!r}") from exc


def rules_for_pada(pada: str) -> tuple[SutraRule, ...]:
    return tuple(rule for rule in ADHYAYA7_RULES.values() if rule.pada == pada)


def expected_adhyaya7_ids() -> tuple[str, ...]:
    return tuple(f"{pada}.{index}" for pada in PADA_COUNTS for index in PADA_INDICES[pada])


def missing_rule_ids() -> tuple[str, ...]:
    return tuple(sutra_id for sutra_id in expected_adhyaya7_ids() if sutra_id not in ADHYAYA7_RULES)


def implemented_sutra_ids() -> frozenset[str]:
    return frozenset(sutra_id for sutra_id, rule in ADHYAYA7_RULES.items() if rule.implemented)


def partial_sutra_ids() -> frozenset[str]:
    return frozenset(sutra_id for sutra_id, rule in ADHYAYA7_RULES.items() if not rule.implemented)


def implementation_note_for(sutra_id: str) -> str:
    rule = rule_for(sutra_id)
    mode = "Discrete executable" if rule.mode == ImplementationMode.DISCRETE else "Partial"
    hooks = ", ".join(rule.hooks)
    return f"{mode} Adhyāya 7 implementation: {rule.sutra_text_iast}. {rule.compiler_effect} Hooks: {hooks}."


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
    for sutra_id in expected_adhyaya7_ids():
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


ADHYAYA7_RULES = _build_rules()
