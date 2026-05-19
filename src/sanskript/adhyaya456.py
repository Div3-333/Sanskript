from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .sutra_logic import atomic_evidence_for, has_discrete_sutra_logic

class RuleKind(str, Enum):
    TADDHITA = "taddhita"
    FEMININE_SUFFIX = "feminine_suffix"
    POSSESSION = "possession"
    COMPARISON = "comparison"
    NUMERAL = "numeral"
    VOWEL_SANDHI = "vowel_sandhi"
    ACCENT = "accent"
    UTTARAPADA = "uttarapada"
    ANGA = "anga"


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
    "4.1": 178,
    "4.2": 145,
    "4.3": 168,
    "4.4": 143,
    "5.1": 136,
    "5.2": 140,
    "5.3": 119,
    "5.4": 160,
    "6.1": 223,
    "6.2": 199,
    "6.3": 139,
    "6.4": 175,
}


PADA_INDICES = {
    pada: tuple(range(1, count + 1))
    for pada, count in PADA_COUNTS.items()
}
PADA_INDICES["4.4"] = tuple(range(1, 129)) + tuple(range(130, 145))


SPECIAL_RULES: dict[str, tuple[RuleKind, str, str, tuple[str, ...], str, ImplementationMode]] = {
    "4.1.1": (RuleKind.FEMININE_SUFFIX, "ṅyāp prātipadikāt", "opens the feminine suffix domain after nominal bases", ("sanskript.subanta.iter_nominal_analyses", "sanskript.grammar.Gender"), "feminine suffix", ImplementationMode.EXECUTABLE),
    "4.1.2": (RuleKind.FEMININE_SUFFIX, "ajādy ataṣṭāp", "records ṭāp-like feminine derivation for a-stem bases", ("sanskript.subanta.decline_aa_feminine",), "latā", ImplementationMode.EXECUTABLE),
    "4.1.3": (RuleKind.FEMININE_SUFFIX, "striyām", "marks the feminine-domain reading for following suffixes", ("sanskript.grammar.Gender",), "feminine domain", ImplementationMode.EXECUTABLE),
    "4.1.83": (RuleKind.TADDHITA, "prāg dīvyato'ṇ", "opens a major taddhita suffix domain", ("sanskript.derivation.derive", "sanskript.derivation.TaddhitaSuffix"), "taddhita domain", ImplementationMode.EXECUTABLE),
    "4.1.92": (RuleKind.TADDHITA, "tasyāpatyam", "derives patronymic/descendant taddhita forms", ("sanskript.derivation.derive", "sanskript.derivation.TaddhitaSuffix.APATYA"), "aupagava", ImplementationMode.EXECUTABLE),
    "5.2.94": (RuleKind.POSSESSION, "tad asyāsty asminn iti matup", "derives possession adjectives with matup", ("sanskript.derivation.derive", "sanskript.derivation.TaddhitaSuffix.MATUP"), "balavān", ImplementationMode.EXECUTABLE),
    "5.3.55": (RuleKind.COMPARISON, "atiśāyane tamab iṣṭhanau", "derives superlative/comparison forms", ("sanskript.derivation.derive", "sanskript.derivation.TaddhitaSuffix.ATISHAYANA"), "laghiṣṭha", ImplementationMode.EXECUTABLE),
    "5.4.1": (RuleKind.TADDHITA, "pādānte taddhita continuation", "keeps late taddhita suffixes in the derivational registry", ("sanskript.derivation.forms_by_family",), "late taddhita", ImplementationMode.SEMANTIC),
    "6.1.77": (RuleKind.VOWEL_SANDHI, "iko yaṇ aci", "records vowel-to-semivowel transition before vowels", ("sanskript.sandhi.join_words", "sanskript.phonology.pratyahara"), "vowel transition", ImplementationMode.SEMANTIC),
    "6.1.78": (RuleKind.VOWEL_SANDHI, "eco'yavāyāvaḥ", "applies ay/av/āy/āv-style replacement for ec vowels", ("sanskript.sandhi.join_words",), "harayatra", ImplementationMode.EXECUTABLE),
    "6.1.87": (RuleKind.VOWEL_SANDHI, "ād guṇaḥ", "applies guṇa sandhi after a/ā", ("sanskript.sandhi.join_words",), "deveti", ImplementationMode.EXECUTABLE),
    "6.1.88": (RuleKind.VOWEL_SANDHI, "vṛddhir eci", "applies vṛddhi sandhi before ec vowels", ("sanskript.sandhi.join_words",), "devaiva", ImplementationMode.EXECUTABLE),
    "6.1.101": (RuleKind.VOWEL_SANDHI, "akaḥ savarṇe dīrghaḥ", "applies savarṇa-dīrgha vowel sandhi", ("sanskript.sandhi.join_words",), "devātra", ImplementationMode.EXECUTABLE),
    "6.2.1": (RuleKind.ACCENT, "bahuvrīhau prakṛtyā pūrvapadam", "opens compound accent handling", ("sanskript.accent.profile_accent",), "compound accent", ImplementationMode.EXECUTABLE),
    "6.3.1": (RuleKind.UTTARAPADA, "alug uttarapade", "opens uttarapada/internal compound operation handling", ("sanskript.anga.operations_for_range", "sanskript.samasa.create_compound"), "uttarapada domain", ImplementationMode.EXECUTABLE),
    "6.4.1": (RuleKind.ANGA, "aṅgasya", "opens the aṅga operation domain", ("sanskript.anga.operations_for_range",), "aṅga domain", ImplementationMode.EXECUTABLE),
    "6.4.2": (RuleKind.ANGA, "hal", "records consonant-sensitive aṅga operation conditions", ("sanskript.phonology.is_consonant", "sanskript.anga.apply_anga_operation"), "hal condition", ImplementationMode.EXECUTABLE),
    "6.4.146": (RuleKind.ANGA, "oḥ supi", "records late stem-final operation before sup suffixes", ("sanskript.anga.apply_anga_operation",), "stem-final operation", ImplementationMode.SEMANTIC),
}


PADA_PROFILES: dict[str, tuple[RuleKind, str, str, tuple[str, ...]]] = {
    "4.1": (RuleKind.FEMININE_SUFFIX, "feminine and early taddhita suffix rule", "records feminine suffixes, prātipadika-conditioned taddhita domains, and descendant semantics", ("sanskript.subanta.iter_nominal_analyses", "sanskript.derivation.derive", "sanskript.derivation.TaddhitaSuffix")),
    "4.2": (RuleKind.TADDHITA, "taddhita semantic relation rule", "records taddhita suffixes for place, descent, possession, relation, and conventional naming", ("sanskript.derivation.derive", "sanskript.derivation.forms_by_family")),
    "4.3": (RuleKind.TADDHITA, "taddhita source and regional rule", "records taddhita derivation for source, region, study, affiliation, and lineage domains", ("sanskript.derivation.derive", "sanskript.derivation.TaddhitaSuffix")),
    "4.4": (RuleKind.TADDHITA, "late taddhita occupation and relation rule", "records late taddhita derivation for occupation, product, possession, and contextual relation domains", ("sanskript.derivation.derive", "sanskript.derivation.forms_by_family")),
    "5.1": (RuleKind.TADDHITA, "quantified taddhita rule", "records taddhita suffixes for measure, value, number, time, and semantic relation", ("sanskript.derivation.derive", "sanskript.derivation.TaddhitaSuffix")),
    "5.2": (RuleKind.POSSESSION, "possession and quality taddhita rule", "records matup-like possession, quality, and state suffix behavior", ("sanskript.derivation.derive", "sanskript.derivation.TaddhitaSuffix.MATUP")),
    "5.3": (RuleKind.COMPARISON, "degree and comparison taddhita rule", "records comparative, superlative, deictic, and degree semantics", ("sanskript.derivation.derive", "sanskript.derivation.TaddhitaSuffix.ATISHAYANA")),
    "5.4": (RuleKind.NUMERAL, "late taddhita and compound-final rule", "records late taddhita, numeral, possession, and compound-final suffix behavior", ("sanskript.derivation.derive", "sanskript.samasa.create_compound")),
    "6.1": (RuleKind.VOWEL_SANDHI, "vowel sandhi and sound substitution rule", "records vowel coalescence, guṇa, vṛddhi, ayavāyāva, reduplication, and sound replacement", ("sanskript.sandhi.join_words", "sanskript.phonology.best_substitute", "sanskript.anga.guna", "sanskript.anga.vrddhi")),
    "6.2": (RuleKind.ACCENT, "compound and pada accent rule", "records udātta, anudātta, svarita, and compound accent domains", ("sanskript.accent.profile_accent", "sanskript.accent.assign_svarita")),
    "6.3": (RuleKind.UTTARAPADA, "uttarapada and internal compound rule", "records second-member, internal compound, and stem-domain operations", ("sanskript.anga.operations_for_range", "sanskript.samasa.create_compound")),
    "6.4": (RuleKind.ANGA, "late aṅga operation rule", "records late stem-final, suffix-sensitive, accent-sensitive, and substitution operations on aṅgas", ("sanskript.anga.operations_for_range", "sanskript.anga.apply_anga_operation")),
}


def rule_for(sutra_id: str) -> SutraRule:
    try:
        return ADHYAYA456_RULES[sutra_id]
    except KeyError as exc:
        raise ValueError(f"No Adhyaya 4/5/6 rule for {sutra_id!r}") from exc


def rules_for_pada(pada: str) -> tuple[SutraRule, ...]:
    return tuple(rule for rule in ADHYAYA456_RULES.values() if rule.pada == pada)


def expected_adhyaya456_ids() -> tuple[str, ...]:
    return tuple(
        f"{pada}.{index}"
        for pada in PADA_COUNTS
        for index in PADA_INDICES[pada]
    )


def missing_rule_ids() -> tuple[str, ...]:
    return tuple(sutra_id for sutra_id in expected_adhyaya456_ids() if sutra_id not in ADHYAYA456_RULES)


def implemented_sutra_ids() -> frozenset[str]:
    return frozenset(sutra_id for sutra_id, rule in ADHYAYA456_RULES.items() if rule.implemented)


def partial_sutra_ids() -> frozenset[str]:
    return frozenset(sutra_id for sutra_id, rule in ADHYAYA456_RULES.items() if not rule.implemented)


def implementation_note_for(sutra_id: str) -> str:
    rule = rule_for(sutra_id)
    mode = "Discrete executable" if rule.mode == ImplementationMode.DISCRETE else "Partial"
    hooks = ", ".join(rule.hooks)
    return f"{mode} Adhyaya 4/5/6 implementation: {rule.sutra_text_iast}. {rule.compiler_effect} Hooks: {hooks}."


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
    for sutra_id in expected_adhyaya456_ids():
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


ADHYAYA456_RULES = _build_rules()
