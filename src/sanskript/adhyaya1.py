from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RuleKind(str, Enum):
    SOUND_DEFINITION = "sound_definition"
    BLOCKING_RULE = "blocking_rule"
    TECHNICAL_TERM = "technical_term"
    SUBSTITUTION_META = "substitution_meta"
    PRATYAHARA_META = "pratyahara_meta"
    ACCENT_RULE = "accent_rule"
    COMPOUND_META = "compound_meta"
    PRATIPADIKA_META = "pratipadika_meta"
    LOPA_SEMANTICS = "lopa_semantics"
    EKASESHA = "ekashesha"
    DHATU_META = "dhatu_meta"
    IT_MARKER = "it_marker"
    PADA_DOMAIN = "pada_domain"
    VOICE_RULE = "voice_rule"
    SAMJNA = "samjna"
    KARAKA = "karaka"
    GATI = "gati"
    UPASARGA = "upasarga"
    KARMAPRAVACANIYA = "karmapravacaniya"
    SAMHITA = "samhita"


class ImplementationMode(str, Enum):
    EXECUTABLE = "executable_anchor"
    SEMANTIC = "semantic_scaffold"
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
    reviewer_notes: tuple[str, ...] = ()

    @property
    def implemented(self) -> bool:
        return self.mode == ImplementationMode.DISCRETE and self.discrete

    @property
    def discrete(self) -> bool:
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
                self.reviewer_notes,
            )
        )

def rule_for(sutra_id: str) -> SutraRule:
    try:
        return ADHYAYA1_RULES[sutra_id]
    except KeyError as exc:
        raise ValueError(f"No Adhyaya 1 rule for {sutra_id!r}") from exc


def rules_for_pada(pada: str) -> tuple[SutraRule, ...]:
    return tuple(rule for rule in ADHYAYA1_RULES.values() if rule.pada == pada)


def implemented_sutra_ids() -> frozenset[str]:
    return frozenset(sutra_id for sutra_id, rule in ADHYAYA1_RULES.items() if rule.implemented)


def partial_sutra_ids() -> frozenset[str]:
    return frozenset(sutra_id for sutra_id, rule in ADHYAYA1_RULES.items() if not rule.implemented)


def implementation_note_for(sutra_id: str) -> str:
    rule = rule_for(sutra_id)
    mode = "Discrete executable" if rule.mode == ImplementationMode.DISCRETE else "Partial"
    hooks = ", ".join(rule.hooks)
    return f"{mode} Adhyaya 1 implementation: {rule.compiler_effect} Hooks: {hooks}."


def partial_implementation_note_for(sutra_id: str) -> str:
    rule = rule_for(sutra_id)
    hooks = ", ".join(rule.hooks)
    prefix = "Executable anchor only" if rule.mode == ImplementationMode.EXECUTABLE else "Semantic scaffold only"
    return (
        f"{prefix}, not a complete discrete Paninian sutra implementation: "
        f"{rule.compiler_effect} Required before completion: exact sutra text, inherited domain, "
        f"conditions, exceptions, rule-specific executable logic, positive behavioral tests, "
        f"negative behavioral tests, and reviewer notes. Hooks: {hooks}."
    )


def expected_half_adhyaya_ids() -> tuple[str, ...]:
    return tuple(f"1.1.{index}" for index in range(1, 76)) + tuple(f"1.2.{index}" for index in range(1, 74))


def expected_adhyaya1_ids() -> tuple[str, ...]:
    return (
        expected_half_adhyaya_ids()
        + tuple(f"1.3.{index}" for index in range(1, 94))
        + tuple(f"1.4.{index}" for index in range(1, 111))
    )


def missing_rule_ids() -> tuple[str, ...]:
    return tuple(sutra_id for sutra_id in expected_adhyaya1_ids() if sutra_id not in ADHYAYA1_RULES)


def _example(tag: str, output: str, note: str) -> tuple[RuleExample, ...]:
    return (RuleExample(tag, output, note),)


def _rule(
    sutra_id: str,
    kind: RuleKind,
    mode: ImplementationMode,
    title: str,
    compiler_effect: str,
    hooks: tuple[str, ...],
    examples: tuple[RuleExample, ...],
    sutra_text_devanagari: str = "",
    sutra_text_iast: str = "",
    source: str = "",
    anuvritti: tuple[str, ...] = (),
    conditions: tuple[str, ...] = (),
    exceptions: tuple[str, ...] = (),
    counterexamples: tuple[RuleExample, ...] = (),
    reviewer_notes: tuple[str, ...] = (),
) -> SutraRule:
    return SutraRule(
        id=sutra_id,
        pada=sutra_id.rsplit(".", 1)[0],
        kind=kind,
        mode=mode,
        title=title,
        compiler_effect=compiler_effect,
        hooks=hooks,
        examples=examples,
        sutra_text_devanagari=sutra_text_devanagari,
        sutra_text_iast=sutra_text_iast,
        source=source,
        anuvritti=anuvritti,
        conditions=conditions,
        exceptions=exceptions,
        counterexamples=counterexamples,
        reviewer_notes=reviewer_notes,
    )


PANINI_SOURCE = "https://sanskritlibrary.org/grammatical/data/panini.html"


DISCRETE_SUTRA_EVIDENCE: dict[str, dict[str, object]] = {
    "1.1.1": {
        "sutra_text_devanagari": "वृद्धिरादैच्",
        "sutra_text_iast": "vṛddhir ādaiC",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("The term vṛddhi denotes exactly ā, ai, and au.",),
        "exceptions": ("No sound outside ā/ai/au receives vṛddhi-saṃjñā by this rule.",),
        "counterexamples": _example("e", "not vṛddhi", "e is rejected because it belongs to guṇa, not vṛddhi."),
        "reviewer_notes": ("Behavior is executable through VRDDHI_SOUNDS and is_vrddhi with positive and negative tests.",),
    },
    "1.1.2": {
        "sutra_text_devanagari": "अदेङ् गुणः",
        "sutra_text_iast": "adeṅ guṇaḥ",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("The term guṇa denotes exactly a, e, and o.",),
        "exceptions": ("No sound outside a/e/o receives guṇa-saṃjñā by this rule.",),
        "counterexamples": _example("ai", "not guṇa", "ai is rejected because it belongs to vṛddhi, not guṇa."),
        "reviewer_notes": ("Behavior is executable through GUNA_SOUNDS and is_guna with positive and negative tests.",),
    },
    "1.1.3": {
        "sutra_text_devanagari": "इको गुणवृद्धी",
        "sutra_text_iast": "iko guṇavṛddhī",
        "source": PANINI_SOURCE,
        "anuvritti": ("guṇa and vṛddhi from 1.1.1-1.1.2",),
        "conditions": ("Guṇa and vṛddhi replacement targets are limited to ik sounds.",),
        "exceptions": ("Non-ik sounds cannot enter the guṇa/vṛddhi replacement table.",),
        "counterexamples": _example("a", "not an ik replacement target", "a raises a rule-specific replacement error."),
        "reviewer_notes": ("Behavior is executable through is_ik, guna_replacement_for_ik, and vrddhi_replacement_for_ik.",),
    },
    "1.1.4": {
        "sutra_text_devanagari": "न धातुलोप आर्धधातुके",
        "sutra_text_iast": "na dhātulopa ārdhadhātuke",
        "source": PANINI_SOURCE,
        "anuvritti": ("guṇa-vṛddhi replacement domain from 1.1.3",),
        "conditions": ("A dhātu-lopa context before an ārdhadhātuka suffix blocks guṇa/vṛddhi.",),
        "exceptions": ("Without dhātu-lopa, the ordinary ik replacement path remains available.",),
        "counterexamples": _example("i + ārdhadhātuka without dhātu-lopa", "e", "guṇa is allowed when the blocking condition is absent."),
        "reviewer_notes": ("Behavior is executable in anga.guna and anga.vrddhi via DerivationContext.has_dhatu_lopa.",),
    },
    "1.1.5": {
        "sutra_text_devanagari": "क्ङिति च",
        "sutra_text_iast": "kṅiti ca",
        "source": PANINI_SOURCE,
        "anuvritti": ("guṇa-vṛddhi replacement domain from 1.1.3",),
        "conditions": ("A kit or ṅit suffix blocks guṇa/vṛddhi.",),
        "exceptions": ("Suffixes not treated as kit or ṅit do not trigger this block.",),
        "counterexamples": _example("i + non-kit/non-ṅit suffix", "e", "guṇa is allowed when the k/ṅ marker condition is absent."),
        "reviewer_notes": ("Behavior is executable in DerivationContext.get_is_kit/get_is_ngit and anga.guna/vrddhi.",),
    },
    "1.1.6": {
        "sutra_text_devanagari": "दीधीवेवीटाम्",
        "sutra_text_iast": "dīdhīvevīṭām",
        "source": PANINI_SOURCE,
        "anuvritti": ("guṇa-vṛddhi replacement domain from 1.1.3",),
        "conditions": ("The listed dīdhī/vevī roots and controlled iṭ-augment contexts block guṇa/vṛddhi.",),
        "exceptions": ("The ktvā iṭ context is handled separately and does not use this broad iṭ block.",),
        "counterexamples": _example("bhū + ordinary suffix", "guṇa allowed", "ordinary roots do not trigger the listed-root block."),
        "reviewer_notes": ("Behavior is executable in anga.guna and anga.vrddhi through root_lemma and is_it_augment.",),
    },
    "1.1.7": {
        "sutra_text_devanagari": "हलोनन्तराः संयोगः",
        "sutra_text_iast": "halo'nantarāḥ saṃyogaḥ",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("Two or more adjacent hal sounds with no intervening vowel receive saṃyoga-saṃjñā.",),
        "exceptions": ("Any intervening ac sound prevents saṃyoga.",),
        "counterexamples": _example("k+a", "not saṃyoga", "A vowel between or among sounds breaks the hal-only adjacency."),
        "reviewer_notes": ("Behavior is executable through phonology.is_samyoga with accepted and rejected sound lists.",),
    },
    "1.1.8": {
        "sutra_text_devanagari": "मुखनासिकावचनोऽनुनासिकः",
        "sutra_text_iast": "mukhanāsikāvacano'nunāsikaḥ",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("A sound marked with nasal articulation receives anunāsika-saṃjñā.",),
        "exceptions": ("Non-nasal sounds do not receive anunāsika-saṃjñā.",),
        "counterexamples": _example("k", "not anunāsika", "k is oral and not nasal in the sound inventory."),
        "reviewer_notes": ("Behavior is executable through Sound.nasal and phonology.is_anunasika.",),
    },
    "1.1.9": {
        "sutra_text_devanagari": "तुल्यास्यप्रयत्नं सवर्णम्",
        "sutra_text_iast": "tulyāsyaprayatnaṃ savarṇam",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("Sounds with matching articulation place and effort inside the same ac/hal class are savarṇa.",),
        "exceptions": ("A later prohibition keeps ac and hal from becoming savarṇa with each other.",),
        "counterexamples": _example("i/u", "not savarṇa", "Different articulation places reject savarṇa-saṃjñā."),
        "reviewer_notes": ("Behavior is executable through phonology.is_savarna and savarna_class.",),
    },
    "1.1.10": {
        "sutra_text_devanagari": "नाज्झलौ",
        "sutra_text_iast": "nājjhalau",
        "source": PANINI_SOURCE,
        "anuvritti": ("savarṇa from 1.1.9",),
        "conditions": ("An ac sound and a hal sound are not mutually savarṇa.",),
        "exceptions": ("Same-class savarṇa relations, such as a/ā, remain governed by 1.1.9.",),
        "counterexamples": _example("a/ā", "savarṇa", "The prohibition is not applied to two ac sounds."),
        "reviewer_notes": ("Behavior is executable through the vowel/consonant class check inside phonology.is_savarna.",),
    },
    "1.1.11": {
        "sutra_text_devanagari": "ईदूदेद्द्विवचनं प्रगृह्यम्",
        "sutra_text_iast": "īdūded-dvivacanaṃ pragṛhyam",
        "source": PANINI_SOURCE,
        "anuvritti": ("pragṛhya-saṃjñā domain",),
        "conditions": ("Dual forms ending in ī, ū, or e receive pragṛhya-saṃjñā.",),
        "exceptions": ("Non-dual forms with the same endings do not receive this saṃjñā from 1.1.11.",),
        "counterexamples": _example("nadī singular", "not pragṛhya by 1.1.11", "A singular ī-final form lacks the dual condition."),
        "reviewer_notes": ("Behavior is executable through phonology.is_pragrhya on Analysis.number == dual.",),
    },
    "1.1.12": {
        "sutra_text_devanagari": "अदसो मात्",
        "sutra_text_iast": "adaso māt",
        "source": PANINI_SOURCE,
        "anuvritti": ("pragṛhya-saṃjñā from 1.1.11",),
        "conditions": ("adas forms ending in mī or mū receive pragṛhya-saṃjñā.",),
        "exceptions": ("A non-adas form with the same ending is not licensed by this rule.",),
        "counterexamples": _example("amī with lemma anya", "not pragṛhya by 1.1.12", "The lemma condition must be adas."),
        "reviewer_notes": ("Behavior is executable through phonology.is_pragrhya on lemma adas and surface mī/mū.",),
    },
    "1.1.15": {
        "sutra_text_devanagari": "ओत्",
        "sutra_text_iast": "ot",
        "source": PANINI_SOURCE,
        "anuvritti": ("pragṛhya-saṃjñā from 1.1.11",),
        "conditions": ("The particle o receives pragṛhya-saṃjñā.",),
        "exceptions": ("Ordinary non-particle o-like material is not licensed by this string shortcut.",),
        "counterexamples": _example("a", "not pragṛhya", "A different particle surface does not satisfy ot."),
        "reviewer_notes": ("Behavior is executable through phonology.is_pragrhya on the controlled particle string o.",),
    },
    "1.1.19": {
        "sutra_text_devanagari": "ईदूतौ च सप्तम्यर्थे",
        "sutra_text_iast": "īdūtau ca saptamyarthe",
        "source": PANINI_SOURCE,
        "anuvritti": ("pragṛhya-saṃjñā from 1.1.11",),
        "conditions": ("Locative-sense forms ending in ī or ū receive pragṛhya-saṃjñā.",),
        "exceptions": ("The same ending outside the locative condition is not licensed by 1.1.19.",),
        "counterexamples": _example("nadī nominative", "not pragṛhya by 1.1.19", "The locative condition must be present."),
        "reviewer_notes": ("Behavior is executable through phonology.is_pragrhya on Analysis.case == locative.",),
    },
    "1.1.20": {
        "sutra_text_devanagari": "दाधा घ्वदाप्",
        "sutra_text_iast": "dādhā ghvadāp",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("dā and dhā roots receive ghu-saṃjñā.",),
        "exceptions": ("dāp and daip are excluded from the ghu class.",),
        "counterexamples": _example("dāp", "not ghu", "The explicit exclusion prevents ghu-saṃjñā."),
        "reviewer_notes": ("Behavior is executable through categories.is_ghu_root.",),
    },
    "1.1.21": {
        "sutra_text_devanagari": "आद्यन्तवदेकस्मिन्",
        "sutra_text_iast": "ādyantavad ekasmin",
        "source": PANINI_SOURCE,
        "anuvritti": ("metarule domain",),
        "conditions": ("A single sound is treated as both beginning-like and end-like.",),
        "exceptions": ("A multi-sound term does not satisfy this single-sound metarule.",),
        "counterexamples": _example("ai", "not single simple boundary", "The tokenizer treats ai as one diphthong, while two-token words fail."),
        "reviewer_notes": ("Behavior is executable through categories.has_single_sound_boundary.",),
    },
    "1.1.22": {
        "sutra_text_devanagari": "तरप्तमपौ घः",
        "sutra_text_iast": "taraptamapau ghaḥ",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("The tarap and tamap suffixes receive gha-saṃjñā.",),
        "exceptions": ("Other suffixes do not receive gha-saṃjñā by this rule.",),
        "counterexamples": _example("kta", "not gha", "kta is not tarap or tamap."),
        "reviewer_notes": ("Behavior is executable through categories.is_gha_suffix.",),
    },
    "1.1.23": {
        "sutra_text_devanagari": "बहुगणवतुडति संख्या",
        "sutra_text_iast": "bahugaṇavatuḍati saṃkhyā",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("bahu, gaṇa, vatu, and ḍati enter the controlled saṃkhyā class.",),
        "exceptions": ("Non-listed terms do not receive saṃkhyā-saṃjñā by this rule.",),
        "counterexamples": _example("deva", "not saṃkhyā", "A regular nominal stem is outside the listed class."),
        "reviewer_notes": ("Behavior is executable through categories.is_sankhya_term.",),
    },
    "1.1.24": {
        "sutra_text_devanagari": "ष्णान्ता षट्",
        "sutra_text_iast": "ṣṇāntā ṣaṭ",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃkhyā from 1.1.23",),
        "conditions": ("Controlled numerals ending in ṣ or n receive ṣaṭ-saṃjñā.",),
        "exceptions": ("Non-numeral words with similar endings are not admitted by the controlled list.",),
        "counterexamples": _example("rājan", "not ṣaṭ", "The form ends in n but is not a controlled numeral here."),
        "reviewer_notes": ("Behavior is executable through categories.is_shat_numeral.",),
    },
    "1.1.25": {
        "sutra_text_devanagari": "डति च",
        "sutra_text_iast": "ḍati ca",
        "source": PANINI_SOURCE,
        "anuvritti": ("ṣaṭ from 1.1.24",),
        "conditions": ("ḍati is also treated as ṣaṭ.",),
        "exceptions": ("Unlisted terms are not extended by this ca rule.",),
        "counterexamples": _example("vatu", "not ṣaṭ", "vatu is saṃkhyā in 1.1.23 but not this ṣaṭ extension."),
        "reviewer_notes": ("Behavior is executable through categories.is_shat_numeral.",),
    },
    "1.1.26": {
        "sutra_text_devanagari": "क्तक्तवतू निष्ठा",
        "sutra_text_iast": "ktaktavatū niṣṭhā",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("kta and ktavatū suffixes receive niṣṭhā-saṃjñā.",),
        "exceptions": ("Other kṛt suffixes do not receive niṣṭhā-saṃjñā by this rule.",),
        "counterexamples": _example("lyuṭ", "not niṣṭhā", "lyuṭ is not kta or ktavatū."),
        "reviewer_notes": ("Behavior is executable through categories.is_nistha_suffix.",),
    },
    "1.1.27": {
        "sutra_text_devanagari": "सर्वादीनि सर्वनामानि",
        "sutra_text_iast": "sarvādīni sarvanāmāni",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("The controlled sarva-class stems receive sarvanāma-saṃjñā.",),
        "exceptions": ("Ordinary nominal stems outside the sarvādi list are not sarvanāma.",),
        "counterexamples": _example("deva", "not sarvanāma", "deva is not part of the sarvādi list."),
        "reviewer_notes": ("Behavior is executable through categories.is_sarvanama_stem.",),
    },
    "1.1.37": {
        "sutra_text_devanagari": "स्वरादिनिपातमव्ययम्",
        "sutra_text_iast": "svarādinipātam avyayam",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("Controlled svarādi and nipāta forms receive avyaya-saṃjñā.",),
        "exceptions": ("Ordinary nominal stems are not avyaya by this rule.",),
        "counterexamples": _example("deva", "not avyaya", "A regular nominal stem is outside the controlled avyaya registry."),
        "reviewer_notes": ("Behavior is executable through avyaya.is_controlled_avyaya and iter_avyaya_analyses.",),
    },
    "1.1.40": {
        "sutra_text_devanagari": "क्त्वातोसुन्कसुनः",
        "sutra_text_iast": "ktvātosunkasunaḥ",
        "source": PANINI_SOURCE,
        "anuvritti": ("avyaya-saṃjñā from 1.1.37",),
        "conditions": ("The ktvā, tosun, and kasun suffixes produce avyaya behavior.",),
        "exceptions": ("Other suffixes do not receive avyaya-saṃjñā by this rule.",),
        "counterexamples": _example("kta", "not avyaya by 1.1.40", "kta is handled elsewhere and is not one of ktvā/tosun/kasun."),
        "reviewer_notes": ("Behavior is executable through avyaya.is_avyaya_suffix.",),
    },
    "1.1.41": {
        "sutra_text_devanagari": "अव्ययीभावश्च",
        "sutra_text_iast": "avyayībhāvaś ca",
        "source": PANINI_SOURCE,
        "anuvritti": ("avyaya-saṃjñā from 1.1.37",),
        "conditions": ("Avyayībhāva compounds receive avyaya behavior.",),
        "exceptions": ("Other compound types are not licensed by this rule.",),
        "counterexamples": _example("tatpuruṣa", "not avyayībhāva", "A tatpuruṣa compound is outside this avyaya extension."),
        "reviewer_notes": ("Behavior is executable through samasa.create_compound result samjñā for avyayībhāva.",),
    },
    "1.1.42": {
        "sutra_text_devanagari": "शि सर्वनामस्थानम्",
        "sutra_text_iast": "śi sarvanāmasthānam",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("The śi suffix receives sarvanāmasthāna-saṃjñā.",),
        "exceptions": ("Unlisted suffixes do not receive sarvanāmasthāna-saṃjñā by this rule.",),
        "counterexamples": _example("kta", "not sarvanāmasthāna", "kta is not śi."),
        "reviewer_notes": ("Behavior is executable through categories.is_sarvanamasthana_suffix.",),
    },
    "1.1.43": {
        "sutra_text_devanagari": "सुडनपुंसकस्य",
        "sutra_text_iast": "suḍ anapuṃsakasya",
        "source": PANINI_SOURCE,
        "anuvritti": ("sarvanāmasthāna from 1.1.42",),
        "conditions": ("The controlled suṭ endings receive sarvanāmasthāna-saṃjñā outside neuter contexts.",),
        "exceptions": ("Neuter context blocks this suṭ extension.",),
        "counterexamples": _example("su + neuter", "not sarvanāmasthāna by 1.1.43", "The anapuṃsaka condition excludes neuter."),
        "reviewer_notes": ("Behavior is executable through categories.is_sarvanamasthana_suffix with gender.",),
    },
    "1.1.44": {
        "sutra_text_devanagari": "न वेति विभाषा",
        "sutra_text_iast": "na veti vibhāṣā",
        "source": PANINI_SOURCE,
        "anuvritti": ("metarule domain",),
        "conditions": ("na/vā-style wording marks a grammatically optional operation.",),
        "exceptions": ("Non-optional directive wording is not vibhāṣā.",),
        "counterexamples": _example("nityam", "not vibhāṣā", "A mandatory expression is not optional by this rule."),
        "reviewer_notes": ("Behavior is executable through metarules.is_vibhasha_expression and optional directives.",),
    },
    "1.1.46": {
        "sutra_text_devanagari": "आद्यन्तौ टकितौ",
        "sutra_text_iast": "ādyantau ṭakitau",
        "source": PANINI_SOURCE,
        "anuvritti": ("substitution metarule domain",),
        "conditions": ("ṭit augments are initial and kit augments are final.",),
        "exceptions": ("Other markers do not choose an ādi/anta boundary by this rule.",),
        "counterexamples": _example("mit", "not ādi/anta by 1.1.46", "m uses the last-vowel rule of 1.1.47."),
        "reviewer_notes": ("Behavior is executable through metarules.augment_boundary.",),
    },
    "1.1.47": {
        "sutra_text_devanagari": "मिदचोऽन्त्यात्परः",
        "sutra_text_iast": "mid aco'ntyāt paraḥ",
        "source": PANINI_SOURCE,
        "anuvritti": ("substitution metarule domain",),
        "conditions": ("A mit augment is placed after the final vowel of the base.",),
        "exceptions": ("A base without a vowel has no target for this rule.",),
        "counterexamples": _example("krt", "no final-vowel position", "No ac sound is available."),
        "reviewer_notes": ("Behavior is executable through metarules.mid_augment_index.",),
    },
    "1.1.48": {
        "sutra_text_devanagari": "एच इग्घ्रस्वादेशे",
        "sutra_text_iast": "eca ig hrasvādeśe",
        "source": PANINI_SOURCE,
        "anuvritti": ("substitution metarule domain",),
        "conditions": ("Short substitutes for ec vowels route through i/u.",),
        "exceptions": ("Non-ec vowels are rejected.",),
        "counterexamples": _example("a", "not ec", "a cannot receive an ec hrasva substitute."),
        "reviewer_notes": ("Behavior is executable through phonology.hrasva_substitute_for_ec.",),
    },
    "1.1.49": {
        "sutra_text_devanagari": "षष्ठी स्थानेयोगा",
        "sutra_text_iast": "ṣaṣṭhī sthāneyogā",
        "source": PANINI_SOURCE,
        "anuvritti": ("substitution metarule domain",),
        "conditions": ("A genitive expression marks the substitution site.",),
        "exceptions": ("Other cases do not mark sthāna by this rule.",),
        "counterexamples": _example("saptamī", "not substitution site", "Locative does not trigger this genitive rule."),
        "reviewer_notes": ("Behavior is executable through metarules.genitive_marks_substitution_site.",),
    },
    "1.1.50": {
        "sutra_text_devanagari": "स्थानेऽन्तरतमः",
        "sutra_text_iast": "sthāne'ntaratamaḥ",
        "source": PANINI_SOURCE,
        "anuvritti": ("substitution metarule domain",),
        "conditions": ("Among possible substitutes, the closest by place and effort is chosen.",),
        "exceptions": ("Unknown sounds fall back conservatively to the first candidate.",),
        "counterexamples": _example("i among a/e/o", "e", "The palatal candidate is nearer than a or o."),
        "reviewer_notes": ("Behavior is executable through phonology.best_substitute.",),
    },
    "1.1.51": {
        "sutra_text_devanagari": "उरण् रपरः",
        "sutra_text_iast": "ur aṇ raparaḥ",
        "source": PANINI_SOURCE,
        "anuvritti": ("substitution metarule domain",),
        "conditions": ("ṛ/ṝ/ḷ substitutions place r/l after the a/ā substitute.",),
        "exceptions": ("Non-ur sounds keep the candidate substitute unchanged.",),
        "counterexamples": _example("i -> a", "a", "i is not ur and therefore receives no rapara addition."),
        "reviewer_notes": ("Behavior is executable through phonology.rapara_substitute_for_ur.",),
    },
    "1.1.52": {
        "sutra_text_devanagari": "अलोऽन्त्यस्य",
        "sutra_text_iast": "alo'ntyasya",
        "source": PANINI_SOURCE,
        "anuvritti": ("substitution metarule domain",),
        "conditions": ("Default substitution targets the final sound of the term.",),
        "exceptions": ("An empty term has no final sound target.",),
        "counterexamples": _example("", "no target", "No al is present."),
        "reviewer_notes": ("Behavior is executable through metarules.default_final_substitution_index.",),
    },
    "1.1.53": {
        "sutra_text_devanagari": "ङिच्च",
        "sutra_text_iast": "ṅic ca",
        "source": PANINI_SOURCE,
        "anuvritti": ("sarvasya replacement domain",),
        "conditions": ("A ṅit substitute can replace the whole term.",),
        "exceptions": ("A single unmarked substitute does not trigger whole-term replacement.",),
        "counterexamples": _example("a without marker", "not whole term", "No ṅ/ś marker or multi-sound substitute is present."),
        "reviewer_notes": ("Behavior is executable through metarules.whole_term_replacement_applies.",),
    },
    "1.1.54": {
        "sutra_text_devanagari": "आदेः परस्य",
        "sutra_text_iast": "ādeḥ parasya",
        "source": PANINI_SOURCE,
        "anuvritti": ("substitution metarule domain",),
        "conditions": ("When the following term is targeted, substitution starts at its first sound.",),
        "exceptions": ("An empty following term has no first-sound target.",),
        "counterexamples": _example("", "no following target", "No para term is available."),
        "reviewer_notes": ("Behavior is executable through metarules.following_initial_substitution_index.",),
    },
    "1.1.55": {
        "sutra_text_devanagari": "अनेकाल्शित्सर्वस्य",
        "sutra_text_iast": "anekāl śit sarvasya",
        "source": PANINI_SOURCE,
        "anuvritti": ("sarvasya replacement domain",),
        "conditions": ("A multi-sound or śit substitute replaces the whole term.",),
        "exceptions": ("A single unmarked substitute does not trigger this whole-term behavior.",),
        "counterexamples": _example("a without marker", "not whole term", "Single unmarked replacement uses the default target."),
        "reviewer_notes": ("Behavior is executable through metarules.whole_term_replacement_applies.",),
    },
    "1.1.64": {
        "sutra_text_devanagari": "अचोऽन्त्यादि टि",
        "sutra_text_iast": "aco'ntyādi ṭi",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("ṭi is the final vowel and any following sounds of a term.",),
        "exceptions": ("A term without a vowel returns the whole controlled remainder rather than a vowel-starting ṭi.",),
        "counterexamples": _example("krt", "no vowel-starting ṭi", "No ac sound is present."),
        "reviewer_notes": ("Behavior is executable through phonology.is_ti.",),
    },
    "1.1.65": {
        "sutra_text_devanagari": "अलोऽन्त्यात्पूर्व उपधा",
        "sutra_text_iast": "alo'ntyāt pūrva upadhā",
        "source": PANINI_SOURCE,
        "anuvritti": ("saṃjñā domain",),
        "conditions": ("upadhā is the sound immediately before the final sound.",),
        "exceptions": ("A one-sound term has no upadhā.",),
        "counterexamples": _example("a", "no upadhā", "There is no sound before the final sound."),
        "reviewer_notes": ("Behavior is executable through phonology.is_upadha.",),
    },
    "1.1.69": {
        "sutra_text_devanagari": "अणुदित्सवर्णस्य चाप्रत्ययः",
        "sutra_text_iast": "aṇudit savarṇasya cāpratyayaḥ",
        "source": PANINI_SOURCE,
        "anuvritti": ("savarṇa from 1.1.9",),
        "conditions": ("A sound reference can include its savarṇa class outside pratyaya formation.",),
        "exceptions": ("The pratyaya condition blocks this savarṇa expansion.",),
        "counterexamples": _example("a as pratyaya", "no savarṇa expansion", "The apratyaya condition is violated."),
        "reviewer_notes": ("Behavior is executable through phonology.savarna_reference.",),
    },
    "1.1.70": {
        "sutra_text_devanagari": "तपरस्तत्कालस्य",
        "sutra_text_iast": "taparas tatkālasya",
        "source": PANINI_SOURCE,
        "anuvritti": ("sound-reference metarule domain",),
        "conditions": ("A t-marked sound refers only to candidates of the same duration.",),
        "exceptions": ("Different vowel duration fails this match.",),
        "counterexamples": _example("a/ā", "different duration", "Short a and long ā do not share duration."),
        "reviewer_notes": ("Behavior is executable through phonology.tapara_matches_duration.",),
    },
    "1.1.71": {
        "sutra_text_devanagari": "आदिरन्त्येन सहेता",
        "sutra_text_iast": "ādir antyena sahetā",
        "source": PANINI_SOURCE,
        "anuvritti": ("pratyāhāra metarule domain",),
        "conditions": ("A pratyāhāra is formed from an initial sound and a final it-marker.",),
        "exceptions": ("Unknown start sounds or impossible marker spans are rejected.",),
        "counterexamples": _example("zz", "invalid pratyāhāra", "The start sound is not in the Śiva-sūtra inventory."),
        "reviewer_notes": ("Behavior is executable through phonology.pratyahara.",),
    },
    "1.1.73": {
        "sutra_text_devanagari": "वृद्धिर्यस्याचामादिस्तद् वृद्धम्",
        "sutra_text_iast": "vṛddhir yasyācām ādis tad vṛddham",
        "source": PANINI_SOURCE,
        "anuvritti": ("vṛddha-saṃjñā domain",),
        "conditions": ("A word whose first vowel is vṛddhi receives vṛddha-saṃjñā.",),
        "exceptions": ("A word whose first vowel is not vṛddhi is not vṛddha by this rule.",),
        "counterexamples": _example("agni", "not vṛddha", "The first vowel is a, not vṛddhi."),
        "reviewer_notes": ("Behavior is executable through phonology.is_vrddha_word.",),
    },
    "1.1.74": {
        "sutra_text_devanagari": "त्यदादीनि च",
        "sutra_text_iast": "tyadādīni ca",
        "source": PANINI_SOURCE,
        "anuvritti": ("vṛddha-saṃjñā from 1.1.73",),
        "conditions": ("tyadādi items can receive vṛddha-saṃjñā.",),
        "exceptions": ("Non-tyadādi words still require the 1.1.73 first-vowel condition.",),
        "counterexamples": _example("agni without tyadādi", "not vṛddha", "No vṛddhi first vowel or tyadādi flag is present."),
        "reviewer_notes": ("Behavior is executable through phonology.is_vrddha_word with tyadadi=True.",),
    },
    "1.1.75": {
        "sutra_text_devanagari": "एङ् प्राचां देशे",
        "sutra_text_iast": "eṅ prācāṃ deśe",
        "source": PANINI_SOURCE,
        "anuvritti": ("vṛddha-saṃjñā from 1.1.73",),
        "conditions": ("Eastern place names beginning with e/o receive vṛddha-saṃjñā.",),
        "exceptions": ("Without the eastern-name condition, e/o initial words do not use this extension.",),
        "counterexamples": _example("ekadeśa without eastern flag", "not vṛddha", "The regional condition is absent."),
        "reviewer_notes": ("Behavior is executable through phonology.is_vrddha_word with eastern_name=True.",),
    },
    "1.3.2": {
        "sutra_text_devanagari": "उपदेशेऽजनुनासिक इत्",
        "sutra_text_iast": "upadeśe'janunāsika it",
        "source": PANINI_SOURCE,
        "anuvritti": ("it-marker domain",),
        "conditions": ("A nasalized vowel in upadeśa is marked as it.",),
        "exceptions": ("A non-nasalized vowel is not removed by this rule.",),
        "counterexamples": _example("bhū", "no nasal-vowel marker", "No nasalization marker is present."),
        "reviewer_notes": ("Behavior is executable through markers.analyze_it_markers using the controlled nasalization sign.",),
    },
    "1.3.3": {
        "sutra_text_devanagari": "हलन्त्यम्",
        "sutra_text_iast": "halantyam",
        "source": PANINI_SOURCE,
        "anuvritti": ("it-marker domain",),
        "conditions": ("A final consonant in upadeśa is marked as it.",),
        "exceptions": ("A final vowel is not marked by this rule.",),
        "counterexamples": _example("bhū", "no final-consonant marker", "The final sound is a vowel."),
        "reviewer_notes": ("Behavior is executable through markers.analyze_it_markers final-consonant handling.",),
    },
    "1.3.4": {
        "sutra_text_devanagari": "न विभक्तौ तुस्माः",
        "sutra_text_iast": "na vibhaktau tusmāḥ",
        "source": PANINI_SOURCE,
        "anuvritti": ("halantyam from 1.3.3",),
        "conditions": ("Final tusmāḥ sounds in vibhakti endings are not it by 1.3.3.",),
        "exceptions": ("The same final consonants outside vibhakti upadeśa can still be marked by halantyam.",),
        "counterexamples": _example("tas as suffix", "s marked", "Outside vibhakti, halantyam applies."),
        "reviewer_notes": ("Behavior is executable through markers.analyze_it_markers kind='vibhakti'.",),
    },
    "1.3.5": {
        "sutra_text_devanagari": "आदिर्ञिटुडवः",
        "sutra_text_iast": "ādir ñiṭuḍavaḥ",
        "source": PANINI_SOURCE,
        "anuvritti": ("it-marker domain",),
        "conditions": ("Initial ñi, ṭu, and ḍu in root upadeśa are marked as it.",),
        "exceptions": ("The same initial sounds outside root upadeśa are not handled by this root rule.",),
        "counterexamples": _example("ñibhū as suffix", "not root-initial ñi marker", "The root condition is absent."),
        "reviewer_notes": ("Behavior is executable through markers.analyze_it_markers kind='root'.",),
    },
    "1.3.6": {
        "sutra_text_devanagari": "षः प्रत्ययस्य",
        "sutra_text_iast": "ṣaḥ pratyayasya",
        "source": PANINI_SOURCE,
        "anuvritti": ("it-marker domain",),
        "conditions": ("Initial ṣ of a suffix is marked as it.",),
        "exceptions": ("Initial ṣ outside suffix/vibhakti upadeśa is not licensed by this suffix rule.",),
        "counterexamples": _example("ṣa as root", "not suffix ṣ marker", "The pratyaya condition is absent."),
        "reviewer_notes": ("Behavior is executable through markers.analyze_it_markers suffix initial handling.",),
    },
    "1.3.7": {
        "sutra_text_devanagari": "चुटू",
        "sutra_text_iast": "cuṭū",
        "source": PANINI_SOURCE,
        "anuvritti": ("it-marker domain",),
        "conditions": ("Initial palatal and retroflex sounds of suffixes are marked as it.",),
        "exceptions": ("Non-palatal/non-retroflex initials are not marked by this rule.",),
        "counterexamples": _example("pa", "not cuṭū", "p is outside the palatal/retroflex classes."),
        "reviewer_notes": ("Behavior is executable through markers.analyze_it_markers palatal/retroflex handling.",),
    },
    "1.3.8": {
        "sutra_text_devanagari": "लशक्वतद्धिते",
        "sutra_text_iast": "laśakv ataddhite",
        "source": PANINI_SOURCE,
        "anuvritti": ("it-marker domain",),
        "conditions": ("Initial l, ś, and k-varga sounds of non-taddhita suffixes are marked as it.",),
        "exceptions": ("The taddhita condition blocks this initial-marker rule.",),
        "counterexamples": _example("ka as taddhita", "not laśakv", "The ataddhita condition is absent."),
        "reviewer_notes": ("Behavior is executable through markers.analyze_it_markers is_taddhita handling.",),
    },
    "1.3.9": {
        "sutra_text_devanagari": "तस्य लोपः",
        "sutra_text_iast": "tasya lopaḥ",
        "source": PANINI_SOURCE,
        "anuvritti": ("it-marker domain",),
        "conditions": ("Marked it sounds are removed from the usable lemma while retained as marker metadata.",),
        "exceptions": ("Unmarked sounds remain in the lemma.",),
        "counterexamples": _example("a", "a", "An unmarked vowel is not elided."),
        "reviewer_notes": ("Behavior is executable through markers.analyze_it_markers lemma reconstruction.",),
    },
}


def _build_rules() -> dict[str, SutraRule]:
    rules: dict[str, SutraRule] = {}

    def add(
        sutra_id: str,
        kind: RuleKind,
        title: str,
        compiler_effect: str,
        hooks: tuple[str, ...],
        examples: tuple[RuleExample, ...],
        mode: ImplementationMode = ImplementationMode.SEMANTIC,
    ) -> None:
        evidence = DISCRETE_SUTRA_EVIDENCE.get(sutra_id, {})
        if evidence:
            mode = ImplementationMode.DISCRETE
        rules[sutra_id] = _rule(
            sutra_id,
            kind,
            mode,
            title,
            compiler_effect,
            hooks,
            examples,
            sutra_text_devanagari=str(evidence.get("sutra_text_devanagari", "")),
            sutra_text_iast=str(evidence.get("sutra_text_iast", "")),
            source=str(evidence.get("source", "")),
            anuvritti=tuple(evidence.get("anuvritti", ())),
            conditions=tuple(evidence.get("conditions", ())),
            exceptions=tuple(evidence.get("exceptions", ())),
            counterexamples=tuple(evidence.get("counterexamples", ())),
            reviewer_notes=tuple(evidence.get("reviewer_notes", ())),
        )

    add(
        "1.1.1",
        RuleKind.SOUND_DEFINITION,
        "vṛddhi-saṃjñā",
        "defines the vṛddhi set as exactly ā, ai, and au for later replacements",
        ("sanskript.phonology.is_vrddhi", "sanskript.anga.vrddhi"),
        _example("ai", "vṛddhi", "ai is accepted, e is rejected by the sound tests"),
        ImplementationMode.EXECUTABLE,
    )
    add(
        "1.1.2",
        RuleKind.SOUND_DEFINITION,
        "guṇa-saṃjñā",
        "defines the guṇa set as exactly a, e, and o for later replacements",
        ("sanskript.phonology.is_guna", "sanskript.anga.guna"),
        _example("e", "guṇa", "e is accepted, ai is rejected by the sound tests"),
        ImplementationMode.EXECUTABLE,
    )
    add(
        "1.1.3",
        RuleKind.SOUND_DEFINITION,
        "iko guṇavṛddhī",
        "restricts guṇa and vṛddhi replacement targets to ik sounds",
        ("sanskript.phonology.guna_replacement_for_ik", "sanskript.phonology.vrddhi_replacement_for_ik"),
        _example("i", "e/ai", "i maps to e under guṇa and ai under vṛddhi"),
        ImplementationMode.EXECUTABLE,
    )

    for sutra_id, title, effect, example in (
        ("1.1.4", "na dhātulopa ārdhadhātuke", "blocks guṇa/vṛddhi after dhātu-lopa before an ārdhadhātuka suffix", "dhātu-lopa + ārdhadhātuka"),
        ("1.1.5", "kniti ca", "blocks guṇa/vṛddhi before kit or ṅit suffixes", "kit suffix"),
        ("1.1.6", "dīdīvevīṭām", "blocks guṇa/vṛddhi for dīdī/vevī and selected iṭ-augment contexts", "iṭ augment"),
    ):
        add(
            sutra_id,
            RuleKind.BLOCKING_RULE,
            title,
            effect,
            ("sanskript.anga.DerivationContext", "sanskript.anga.guna", "sanskript.anga.vrddhi"),
            _example(example, "unchanged vowel", effect),
            ImplementationMode.EXECUTABLE,
        )

    for sutra_id, title, hook, example in (
        ("1.1.7", "saṃyoga", "sanskript.phonology.is_samyoga", "k+t"),
        ("1.1.8", "anunāsika", "sanskript.phonology.is_anunasika", "ṅ"),
        ("1.1.9", "savarṇa", "sanskript.phonology.is_savarna", "a/ā"),
        ("1.1.10", "ac and hal savarṇa boundary", "sanskript.phonology.is_savarna", "a/k"),
    ):
        add(
            sutra_id,
            RuleKind.SOUND_DEFINITION,
            title,
            f"records the {title} relation in the sound inventory",
            (hook,),
            _example(example, title, f"{title} is available as a phonology predicate"),
            ImplementationMode.EXECUTABLE,
        )

    for index in range(11, 20):
        add(
            f"1.1.{index}",
            RuleKind.TECHNICAL_TERM,
            "pragṛhya domain",
            "marks forms that resist ordinary sandhi in the pragṛhya environment",
            ("sanskript.phonology.is_pragrhya",),
            _example("dual ī/ū/e or listed nipāta", "pragṛhya", "the predicate exposes a sandhi-blocking flag"),
            ImplementationMode.EXECUTABLE,
        )

    technical_1_1 = {
        20: ("ghu", "classifies dā/dhā-style roots as ghu where later rules need that handle"),
        21: ("single-term boundary", "treats a single sound as beginning-like and end-like in metarules"),
        22: ("gha", "classifies tarap/tamap-style suffixes as gha"),
        23: ("saṃkhyā", "records numerical technical names for count-sensitive grammar"),
        24: ("ṣaṭ", "recognizes ṣaṭ numerals ending in ṣ or n"),
        25: ("ḍati as ṣaṭ", "extends the ṣaṭ class to ḍati"),
        26: ("niṣṭhā", "marks kta/ktavatū-style suffixes as niṣṭhā"),
        27: ("sarvanāma", "records the sarvādī pronoun class as a compiler category"),
        28: ("directional bahuvrīhi option", "keeps the optional sarvanāma reading for direction compounds"),
        29: ("bahuvrīhi restriction", "blocks the general sarvanāma reading in ordinary bahuvrīhi"),
        30: ("tṛtīyā-samāsa option", "keeps the optional pronoun-class reading in instrumental compounds"),
        31: ("dvandva restriction", "blocks the sarvanāma reading in dvandva compounds"),
        32: ("jasi option", "records optional pronoun behavior in nominative plural contexts"),
        33: ("prathama/carama option", "records optional pronoun behavior for prathama, carama, and related terms"),
        34: ("pūrva/para option", "records optional pronoun behavior for pūrva/para and related terms"),
        35: ("sva option", "records the restricted optional pronoun reading of sva"),
        36: ("antara option", "records the restricted optional pronoun reading of antara"),
        37: ("avyaya", "classifies svarādi/nipāta forms as indeclinables"),
        38: ("taddhita avyaya", "keeps non-inflecting taddhita forms in the avyaya channel"),
        39: ("kṛt avyaya", "keeps mejanta kṛt forms in the avyaya channel"),
        40: ("ktvā/tosun/kasun avyaya", "keeps absolutive-like suffixes in the avyaya channel"),
        41: ("avyayībhāva", "marks avyayībhāva compounds as indeclinable compounds"),
        42: ("śi sarvanāmasthānam", "marks śi as a sarvanāmasthāna suffix"),
        43: ("suḍ anapuṃsakasya", "marks the suṭ endings as sarvanāmasthāna outside neuter contexts"),
        44: ("na veti vibhāṣā", "models vibhāṣā as a first-class optionality directive"),
        45: ("ik replacement target", "keeps guṇa/vṛddhi tied to ik-bearing targets"),
    }
    for index, (title, effect) in technical_1_1.items():
        hooks = ("sanskript.avyaya", "sanskript.categories", "sanskript.metarules.rules_for_range")
        if index in {37, 38, 39, 40, 41}:
            hooks = ("sanskript.avyaya.iter_avyaya_analyses", "sanskript.avyaya.is_avyaya_suffix", "sanskript.samasa.create_compound")
        if index in {42, 43}:
            hooks = ("sanskript.categories.is_sarvanamasthana_suffix",)
        if index == 44:
            hooks = ("sanskript.metarules.directive", "sanskript.metarules.is_vibhasha_expression")
        if index == 45:
            hooks = ("sanskript.phonology.is_ik", "sanskript.anga.guna", "sanskript.anga.vrddhi")
        add(
            f"1.1.{index}",
            RuleKind.TECHNICAL_TERM,
            title,
            effect,
            hooks,
            _example(title, "technical category", effect),
            ImplementationMode.EXECUTABLE if index in {37, 41, 42, 45} else ImplementationMode.SEMANTIC,
        )

    substitution_1_1 = {
        46: ("ādyantau ṭakitau", "ṭ/k markers place augments at beginning or end"),
        47: ("midaco'ntyāt paraḥ", "m markers place augments after the last vowel"),
        48: ("eca iṅ hrasvādeśe", "short replacements for ec are routed to i/u"),
        49: ("ṣaṣṭhī sthāneyogā", "genitive syntax identifies the substitution site"),
        50: ("sthāne'ntaratamaḥ", "chooses the nearest substitute by place and effort"),
        51: ("uraṇ raparaḥ", "adds r/l behavior around ṛ/ḷ replacement"),
        52: ("alo'ntyasya", "defaults substitution to the final sound"),
        53: ("ṅic ca", "allows whole-term replacement under a ṅit substitute"),
        54: ("ādeḥ parasya", "targets the first sound of the following term"),
        55: ("anekāl śit sarvasya", "whole-term replacement for multisound/śit substitutes"),
        56: ("sthānivadbhāva", "keeps substitute identity unless a sound-specific rule says otherwise"),
        57: ("acyasmin pūrvavidhau", "extends sthānivad behavior into earlier-vowel environments"),
        58: ("sthānivad limitation", "records contexts where sthānivad behavior is blocked"),
        59: ("reduplication limitation", "records sthānivad limits in vowel reduplication"),
        60: ("lopa", "models deletion as non-appearance rather than string absence only"),
        61: ("luk/ślu/lup", "distinguishes deletion flavors for suffix-memory rules"),
        62: ("pratyaya-lakṣaṇa", "preserves suffix effects after deletion"),
        63: ("lumat blocking", "blocks suffix-memory effects for lumat deletion"),
    }
    substitution_hooks = {
        46: ("sanskript.metarules.augment_boundary",),
        47: ("sanskript.metarules.mid_augment_index",),
        48: ("sanskript.phonology.hrasva_substitute_for_ec",),
        49: ("sanskript.metarules.genitive_marks_substitution_site",),
        50: ("sanskript.phonology.best_substitute",),
        51: ("sanskript.phonology.rapara_substitute_for_ur",),
        52: ("sanskript.metarules.default_final_substitution_index",),
        53: ("sanskript.metarules.whole_term_replacement_applies",),
        54: ("sanskript.metarules.following_initial_substitution_index",),
        55: ("sanskript.metarules.whole_term_replacement_applies",),
    }
    for index, (title, effect) in substitution_1_1.items():
        add(
            f"1.1.{index}",
            RuleKind.SUBSTITUTION_META if index < 60 else RuleKind.LOPA_SEMANTICS,
            title,
            effect,
            substitution_hooks.get(index, ("sanskript.phonology.best_substitute", "sanskript.metarules.directive", "sanskript.markers.analyze_it_markers")),
            _example(title, "substitution directive", effect),
            ImplementationMode.EXECUTABLE if index in {48, 50, 51, 60, 61, 62} else ImplementationMode.SEMANTIC,
        )

    tail_1_1 = {
        64: ("ṭi", "returns the final vowel and following sounds"),
        65: ("upadhā", "returns the penultimate sound"),
        66: ("locative meta-scope", "locative reference targets the preceding term"),
        67: ("ablative meta-scope", "ablative reference targets the following term"),
        68: ("self-form reference", "keeps a word's own surface unless it is a technical term"),
        69: ("savarṇa reference", "lets a sound reference its savarṇa class outside suffix formation"),
        70: ("same-duration tapara", "constrains t-marked references to the same duration"),
        71: ("pratyāhāra", "forms a sound class from start sound plus final it-marker"),
        72: ("tadanta extension", "extends a rule to forms ending in the named term"),
        73: ("vṛddha", "recognizes words whose first vowel is vṛddhi"),
        74: ("tyadādi vṛddha", "adds tyadādi items to the vṛddha class"),
        75: ("eṅ eastern vṛddha", "recognizes eastern-name e/o vṛddha behavior"),
    }
    for index, (title, effect) in tail_1_1.items():
        hooks = ("sanskript.phonology", "sanskript.metarules.rules_for_range")
        mode = ImplementationMode.SEMANTIC
        if index == 64:
            hooks = ("sanskript.phonology.is_ti",)
            mode = ImplementationMode.EXECUTABLE
        elif index == 65:
            hooks = ("sanskript.phonology.is_upadha",)
            mode = ImplementationMode.EXECUTABLE
        elif index == 71:
            hooks = ("sanskript.phonology.pratyahara",)
            mode = ImplementationMode.EXECUTABLE
        elif index == 69:
            hooks = ("sanskript.phonology.savarna_reference",)
        elif index == 70:
            hooks = ("sanskript.phonology.tapara_matches_duration",)
        elif index in {73, 74, 75}:
            hooks = ("sanskript.phonology.savarna_class", "sanskript.phonology.is_vrddha_word")
        add(
            f"1.1.{index}",
            RuleKind.PRATYAHARA_META if index == 71 else RuleKind.TECHNICAL_TERM,
            title,
            effect,
            hooks,
            _example(title, "metarule applied", effect),
            mode,
        )

    kit_ngit = {
        1: ("ṅit after gāṅ/kuṭādi", "suffixes without ñ/ṇ after gāṅ/kuṭādi are treated as ṅit"),
        2: ("vij iṭ", "iṭ after vij is treated as ṅit"),
        3: ("optional ūrṇu behavior", "records vibhāṣā for the ūrṇu domain"),
        4: ("sārvadhātukam apit", "sārvadhātuka suffixes without p are treated as ṅit"),
        5: ("asaṃyogāl liṭ kit", "liṭ after a non-cluster-final root is treated as kit"),
        6: ("indh/bhū liṭ kit", "liṭ after indh/bhū is treated as kit"),
        7: ("ktvā kit list", "ktvā after the listed roots is treated as kit"),
        8: ("rud/vid/etc. ktvā-san", "ktvā/san with iṭ after the listed roots is treated as kit"),
        9: ("iko jhal", "san after ik before jhal is treated as kit"),
        10: ("halanta extension", "extends kit behavior to hal-final roots in the local domain"),
        11: ("liṅ/sic ātmanepada", "liṅ and sic in ātmanepada are treated as kit"),
        12: ("uś ca", "short-ṛ/u-like subcase for the sic kit domain"),
        13: ("vā gamaḥ", "records optional kit behavior for gam + sic"),
        14: ("han sic", "records kit behavior for han + sic"),
        15: ("yam gandhane", "records kit behavior for yam in the smell/perception domain"),
        16: ("optional upayamana", "records optional kit behavior in the upayamana domain"),
        17: ("sthāghvor ic ca", "records kit behavior for sthā/ghu in the ic domain"),
        18: ("na ktvā seṭ", "blocks kit behavior for seṭ ktvā"),
        19: ("niṣṭhā prohibition list", "blocks kit behavior for the listed niṣṭhā contexts"),
        20: ("mṛṣ titīkṣāyām", "blocks kit behavior for mṛṣ in the endurance sense"),
        21: ("ud-upadhā option", "records optional kit behavior in the bhāva/ādikarma domain"),
        22: ("pūṅ ktvā", "records pūṅ + ktvā behavior"),
        23: ("n-upadhā option", "records optional behavior after n-upadhā roots"),
        24: ("vañc/lup/kṛt option", "records optional behavior for the listed roots"),
        25: ("tṛṣ/mṛṣ/kṛśeḥ", "records Kāśyapa's optional domain"),
        26: ("ral vyupadhā", "records optional kit behavior for ral roots with i/u upadhā"),
    }
    for index, (title, effect) in kit_ngit.items():
        add(
            f"1.2.{index}",
            RuleKind.BLOCKING_RULE,
            title,
            effect,
            ("sanskript.anga.DerivationContext.get_is_kit", "sanskript.anga.DerivationContext.get_is_ngit"),
            _example(title, "kit/ṅit decision", effect),
            ImplementationMode.EXECUTABLE if index in {1, 2, 4, 5, 6, 7, 8, 9, 11, 18, 19, 20, 26} else ImplementationMode.SEMANTIC,
        )

    accent_1_2 = {
        27: ("ūkāla", "models vowel duration as hrasva/dīrgha/pluta"),
        28: ("ac duration", "extends duration typing to all vowels"),
        29: ("udātta", "maps high pitch to udātta"),
        30: ("anudātta", "maps low pitch to anudātta"),
        31: ("svarita", "maps combined pitch to svarita"),
        32: ("svarita half-measure", "records the initial udātta half of svarita"),
        33: ("ekaśruti address", "records monotone distant address"),
        34: ("yajña accents", "records ritual accent restrictions"),
        35: ("vaṣaṭ option", "records stronger optional vaṣaṭ accent"),
        36: ("chandas option", "keeps metrical optionality separate"),
        37: ("subrahmaṇyā restriction", "records the subrahmaṇyā accent exception"),
        38: ("deva/brahman accent", "records anudātta behavior for deva/brahman"),
        39: ("svarita-saṃhitā", "propagates anudātta after svarita in saṃhitā"),
        40: ("sannatara", "marks the lower-than-anudātta contour after udātta/svarita"),
        41: ("apṛkta", "marks a single-sound suffix as apṛkta"),
    }
    for index, (title, effect) in accent_1_2.items():
        hooks = ("sanskript.accent.profile_accent", "sanskript.phonology.SOUNDS")
        mode = ImplementationMode.SEMANTIC
        if index in {27, 28}:
            hooks = ("sanskript.phonology.SOUNDS", "sanskript.phonology.VowelLength")
            mode = ImplementationMode.EXECUTABLE
        elif index in {29, 30, 31, 32, 39, 40}:
            hooks = ("sanskript.accent.profile_accent", "sanskript.accent.assign_svarita")
            mode = ImplementationMode.EXECUTABLE
        elif index == 41:
            hooks = ("sanskript.phonology.is_aprkta",)
            mode = ImplementationMode.EXECUTABLE
        add(
            f"1.2.{index}",
            RuleKind.ACCENT_RULE if index < 41 else RuleKind.TECHNICAL_TERM,
            title,
            effect,
            hooks,
            _example(title, "accent/apṛkta metadata", effect),
            mode,
        )

    compound_pratipadika = {
        42: ("karmadhāraya", "classifies samānādhikaraṇa tatpuruṣa as karmadhāraya"),
        43: ("upasarjana", "marks the first-named member in samāsa as upasarjana"),
        44: ("single-case upasarjana", "extends upasarjana behavior to shared-case members before compounding"),
        45: ("prātipadika", "recognizes meaningful non-dhātu/non-pratyaya bases as prātipadika"),
        46: ("kṛt/taddhita/samāsa prātipadika", "extends prātipadika status to kṛt, taddhita, and compound bases"),
        47: ("neuter hrasva", "records short-final behavior for neuter prātipadika"),
        48: ("go/strī upasarjana", "records upasarjana behavior for go/strī"),
        49: ("taddhita-luk", "preserves taddhita behavior through luk deletion"),
        50: ("id goṇyāḥ", "records the local id substitution domain"),
        51: ("lup agreement", "keeps gender/number/case agreement after lup deletion"),
        52: ("adjective agreement", "extends agreement behavior to non-jāti adjectives"),
        53: ("saṃjñā authority", "keeps conventional names authoritative"),
        54: ("luk non-expression", "records non-expression caused by luk"),
        55: ("yoga-pramāṇa", "records inferential absence under yoga evidence"),
        56: ("principal suffix meaning", "keeps suffix meaning as the primary semantic source"),
        57: ("kāla-upasarjana", "extends the same logic to temporal subordination"),
        58: ("jāti singular/plural option", "records optional plural usage for a class name in one member"),
        59: ("asmad dual option", "records special dual behavior for asmad"),
        60: ("nakṣatra plural", "records plural behavior for Phalgunī/Proṣṭhapadā nakṣatras"),
        61: ("chandas punarvasu", "records singular behavior in Vedic Punarvasu"),
        62: ("viśākhā", "records the Viśākhā parallel"),
        63: ("nakṣatra dvandva", "maps plural to dual in tiṣya/punarvasu nakṣatra dvandva"),
    }
    for index, (title, effect) in compound_pratipadika.items():
        kind = RuleKind.COMPOUND_META if index in {42, 43, 44} else RuleKind.PRATIPADIKA_META
        if index in {49, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63}:
            kind = RuleKind.LOPA_SEMANTICS
        hooks = ("sanskript.samasa.create_compound", "sanskript.categories.assign_technical_names", "sanskript.subanta.iter_nominal_analyses")
        if index in {51, 52, 58, 59, 60, 61, 62, 63}:
            hooks = ("sanskript.samasa.apply_ekashesha", "sanskript.subanta.iter_pronoun_analyses")
        add(
            f"1.2.{index}",
            kind,
            title,
            effect,
            hooks,
            _example(title, "nominal semantic directive", effect),
            ImplementationMode.EXECUTABLE if index in {42, 43, 45, 46, 51, 58, 59, 63} else ImplementationMode.SEMANTIC,
        )

    ekashesha = {
        64: ("sarūpa ekaśeṣa", "reduces same-form members to one remainder with the right number"),
        65: ("elder over younger", "keeps the elder/member marked vṛddha when that is the only distinction"),
        66: ("feminine as masculine-like", "records feminine treatment in the ekaśeṣa hierarchy"),
        67: ("masculine over feminine", "keeps the masculine member when paired with feminine"),
        68: ("brother/son remainder", "keeps bhrātṛ over svasṛ and putra over duhitṛ"),
        69: ("neuter option", "keeps neuter with optional behavior against non-neuter"),
        70: ("father over mother", "keeps pitṛ over mātṛ"),
        71: ("father-in-law pair", "keeps śvaśura over śvaśrū"),
        72: ("tyadādi always", "keeps tyadādi pronouns as the remainder"),
        73: ("village animal female", "keeps the feminine term in the listed village-animal collectives"),
    }
    for index, (title, effect) in ekashesha.items():
        add(
            f"1.2.{index}",
            RuleKind.EKASESHA,
            title,
            effect,
            ("sanskript.samasa.apply_ekashesha",),
            _example(title, "single remainder", effect),
            ImplementationMode.EXECUTABLE if index in {64, 65, 67, 68, 69, 70, 71, 72} else ImplementationMode.SEMANTIC,
        )

    add(
        "1.3.1",
        RuleKind.DHATU_META,
        "bhūvādayo dhātavaḥ",
        "declares controlled verbal roots as dhātu entries for tinanta and derivational morphology",
        ("sanskript.tinanta.DHATUS", "sanskript.tinanta.Dhatu"),
        _example("bhū", "dhātu", "registered roots become verbal bases instead of ordinary nouns"),
        ImplementationMode.EXECUTABLE,
    )

    marker_titles = {
        2: ("upadeśe'janunāsika it", "marks nasalized vowels in upadeśa as it"),
        3: ("halantyam", "marks a final consonant in upadeśa as it"),
        4: ("na vibhaktau tusmāḥ", "blocks tusmāḥ-final it marking in vibhakti endings"),
        5: ("ādir ñiṭuḍavaḥ", "marks initial ñi, ṭu, and ḍu in root upadeśa"),
        6: ("ṣaḥ pratyayasya", "marks initial ṣ of suffixes as it"),
        7: ("cuṭū", "marks initial palatal and retroflex sounds of suffixes as it"),
        8: ("laśakv ataddhite", "marks initial l, ś, and k-varga sounds except in taddhita contexts"),
        9: ("tasya lopaḥ", "removes it markers from the usable lemma while preserving marker metadata"),
        10: ("yathāsaṃkhyam marker carry", "keeps marker effects aligned with their source positions"),
        11: ("svarita/anudātta marker domain", "records accent-sensitive marker domains for pada selection"),
    }
    for index, (title, effect) in marker_titles.items():
        add(
            f"1.3.{index}",
            RuleKind.IT_MARKER,
            title,
            effect,
            ("sanskript.markers.analyze_it_markers", "sanskript.markers.MarkerAnalysis"),
            _example(title, "it-marker analysis", effect),
            ImplementationMode.EXECUTABLE if index in range(2, 10) else ImplementationMode.SEMANTIC,
        )

    voice_titles = {
        12: ("anudātta-ṅita ātmanepadam", "ṅit or anudātta roots select ātmanepada"),
        13: ("bhāva-karmaṇoḥ", "passive/reflexive-result domains select ātmanepada"),
        14: ("kartari karma-vyatihāre", "reciprocal action keeps a distinct ātmanepada domain"),
        15: ("na gati-hiṃsārthebhyaḥ", "blocks that ātmanepada reading for motion/injury senses"),
        16: ("itaretarānyonyopapadāc ca", "keeps reciprocal upapada conditions in pada selection"),
        17: ("ner viśaḥ", "ni + viś selects ātmanepada"),
        18: ("parivyawebhyaḥ kriyaḥ", "pari/vi/ava + krī selects ātmanepada"),
        19: ("vipa-paribhyāṃ jñaḥ", "vi/parā + jñā selects ātmanepada"),
        20: ("āṅo do'nāsye viharaṇe", "records a prefix-and-sense ātmanepada subdomain"),
        21: ("krīḍo'nusamparibhyaś ca", "anu/sam/pari + krīḍ selects ātmanepada"),
        22: ("samavapravibhyaḥ sthaḥ", "records prefix-conditioned ātmanepada for sthā"),
        23: ("na śasaḥ", "records a prohibition in the preceding prefix domain"),
        24: ("ud-vido jñāne", "ud + vid in the knowing sense selects ātmanepada"),
        25: ("upān mantra-karaṇe", "upa + verbal utterance in mantra-instrument sense selects ātmanepada"),
        29: ("samo gamyṛcchibhyām", "sam + gam/ṛcch selects ātmanepada"),
        32: ("gandhana-avakṣepaṇa-sevana-kṣiyaḥ", "records sense-specific ātmanepada for kṣi"),
        40: ("upakrama speech/motion class", "records a prefix-and-sense ātmanepada cluster"),
        72: ("svarita-ñitaḥ kartrabhiprāye kriyāphale", "svarita/ñit roots select ātmanepada when the result returns to the agent"),
        78: ("śeṣāt kartari parasmaipadam", "defaults the remaining active-agent domain to parasmaipada"),
    }
    for index in range(12, 94):
        if index in voice_titles:
            title, effect = voice_titles[index]
        elif index < 72:
            title = f"ātmanepada domain rule {index}"
            effect = "records a root, prefix, or sense condition that can select ātmanepada"
        elif index < 78:
            title = f"ubhayapada/reflexive result rule {index}"
            effect = "records optional or reflexive-result pada behavior for roots that can take both padas"
        else:
            title = f"parasmaipada domain rule {index}"
            effect = "records an active-agent or residual condition that selects parasmaipada"
        add(
            f"1.3.{index}",
            RuleKind.VOICE_RULE if index != 78 else RuleKind.PADA_DOMAIN,
            title,
            effect,
            ("sanskript.voice.determine_available_padas", "sanskript.grammar.Pada", "sanskript.tinanta.iter_tinanta_analyses"),
            _example(title, "pada decision", effect),
            ImplementationMode.EXECUTABLE if index in {12, 13, 17, 18, 19, 21, 24, 25, 29, 32, 40, 72, 78} else ImplementationMode.SEMANTIC,
        )

    samjna_titles = {
        1: ("ā kaḍārād ekā saṃjñā", "keeps mutually exclusive technical names under an explicit priority policy"),
        2: ("vipratiṣedhe paraṃ kāryam", "resolves conflicting rule applicability by later-rule priority"),
        3: ("yū stryākhyau nadī", "marks feminine ī/ū words as nadī"),
        4: ("neyaṅuvaṅsthānāv astrī", "records the exception domain for nadī behavior"),
        5: ("vāmi", "records an optional nadī-related domain"),
        6: ("ṅiti hrasvaś ca", "records a short-vowel exception before ṅit"),
        7: ("śeṣo ghyasakhi", "marks final i/u words except sakhi as ghi"),
        8: ("patyur no yajña-saṃyoge", "records a pati exception outside yajña compounds"),
        9: ("ṣaṣṭhī-yuktaś chandasi vā", "records a Vedic optional technical-name domain"),
        10: ("hrasvaṃ laghu", "marks short vowels as laghu"),
        11: ("saṃyoge guru", "marks a vowel before a consonant cluster as guru"),
        12: ("dīrghaṃ ca", "marks long vowels and diphthongs as guru"),
        13: ("yasmāt pratyayavidhis tadādi pratyaye'ṅgam", "marks the base before a suffix as aṅga"),
        14: ("suptiṅantaṃ padam", "marks sup- and tiṅ-ending forms as pada"),
        15: ("naḥ kye", "records a pada restriction before kya-like suffixes"),
        16: ("siti ca", "records a pada restriction before sit suffixes"),
        17: ("svādiṣv asarvanāmasthāne", "keeps pada before selected svādi suffixes"),
        18: ("yaci bham", "marks bha before y or vowel-initial suffixes"),
        19: ("tasau matvarthe", "records a bha-domain extension for matup-like meaning"),
        20: ("ayas-mayādīni chandasi", "records Vedic bha-domain exceptions"),
        21: ("bahuṣu bahuvacanam", "records plural reference for many members"),
        22: ("dvyekayor dvivacanaikavacane", "records dual/singular reference for two/one members"),
    }
    for index in range(1, 23):
        title, effect = samjna_titles[index]
        hooks = ("sanskript.categories.assign_technical_names", "sanskript.grammar.Samjna")
        if index in {10, 11, 12}:
            hooks = ("sanskript.categories.get_vowel_weight", "sanskript.grammar.Samjna")
        add(
            f"1.4.{index}",
            RuleKind.SAMJNA,
            title,
            effect,
            hooks,
            _example(title, "technical name", effect),
            ImplementationMode.EXECUTABLE if index in {1, 2, 3, 7, 10, 11, 12, 13, 14, 17, 18} else ImplementationMode.SEMANTIC,
        )

    karaka_titles = {
        23: ("kārake", "opens the kāraka technical domain"),
        24: ("dhruvam apāye'pādānam", "assigns apādāna to the fixed point in separation"),
        25: ("bhītrārthānāṃ bhayahetuḥ", "assigns apādāna to the cause of fear/protection"),
        26: ("parājer asoḍhaḥ", "assigns apādāna in the unbearable object domain"),
        27: ("vāraṇārthānām īpsitaḥ", "assigns apādāna to what is warded off"),
        28: ("antardhau yenādarśanam icchati", "assigns apādāna to what one hides from"),
        29: ("ākhyātopayoge", "assigns apādāna to the source/teacher of learning"),
        30: ("janikartuḥ prakṛtiḥ", "records source-material apādāna behavior"),
        31: ("bhuvaḥ prabhavaḥ", "records origin apādāna behavior"),
        32: ("karmaṇā yam abhipraiti sa sampradānam", "assigns sampradāna to the intended recipient"),
        33: ("rucyarthānāṃ prīyamāṇaḥ", "assigns sampradāna to the one pleased"),
        34: ("ślāghahnuṅsthāśapāṃ jñīpsyamānaḥ", "records sampradāna in praise/concealment/standing/oath domains"),
        35: ("dhārer uttamarṇaḥ", "records sampradāna in owing/holding domains"),
        36: ("spṛher īpsitaḥ", "records sampradāna for the desired object of spṛh"),
        37: ("krudhadruherṣyāsūyārthānāṃ yaṃ prati kopaḥ", "records sampradāna for anger/envy targets"),
        38: ("krudhadruhor upasṛṣṭayoḥ karma", "records exception behavior for prefixed anger/envy roots"),
        39: ("rādhyīkṣyor yasya vipraśnaḥ", "records sampradāna for inquiry domains"),
        40: ("pratyāṅbhyāṃ śruvaḥ", "records a prefix-conditioned sampradāna domain"),
        41: ("anupadiśṛṇvateḥ", "records a prohibition in the previous domain"),
        42: ("sādhakatamaṃ karaṇam", "assigns karaṇa to the most effective means"),
        43: ("divaḥ karma ca", "records karaṇa/karman alternation for div"),
        44: ("parikrayane sampradānam anyatarasyām", "records optional sampradāna in hiring/exchange"),
        45: ("ādhāro'dhikaraṇam", "assigns adhikaraṇa to the substratum/location"),
        46: ("adhiśīṅsthāsāṃ karma", "records karman behavior for adhi + rest/stand/sit roots"),
        47: ("abhiniviśaś ca", "records karman behavior for abhi-ni-viś"),
        48: ("upānvadhyāṅvasaḥ", "records an upa/anu/adhi/āṅ + vas domain"),
        49: ("kartur īpsitatamaṃ karma", "assigns karman to what the agent most wants to affect"),
        50: ("tathāyuktaṃ cānīpsitam", "assigns karman to connected but undesired objects"),
        51: ("akathitaṃ ca", "records unexpressed-object karman behavior"),
        52: ("gatibuddhipratyavasānārtha...", "records karman in motion/knowing/eating/causative domains"),
        53: ("hṛkror anyatarasyām", "records optional karman behavior for hṛ/kṛ domains"),
        54: ("svatantraḥ kartā", "assigns kartṛ to the independent agent"),
        55: ("tatprayojako hetuś ca", "assigns causative hetu/agent behavior"),
    }
    for index in range(23, 56):
        title, effect = karaka_titles[index]
        add(
            f"1.4.{index}",
            RuleKind.KARAKA,
            title,
            effect,
            ("sanskript.karaka.get_karaka_role", "sanskript.karaka.explain_case", "sanskript.grammar.Role"),
            _example(title, "kāraka role", effect),
            ImplementationMode.EXECUTABLE if index in {23, 24, 25, 26, 27, 28, 29, 32, 33, 42, 45, 49, 54, 55} else ImplementationMode.SEMANTIC,
        )

    gati_titles = {
        56: ("prāg rājīyāt gati-saṃjñā", "opens the gati technical-name domain"),
        57: ("cādāyo'sattve", "records particle-like gati behavior outside substantive use"),
        58: ("prādayaḥ", "marks pra and related prefixes as gati/upasarga material"),
        59: ("upasargāḥ kriyāyoge", "marks verbal prefixes as upasarga when joined to a verb"),
        60: ("gatiś ca", "preserves gati behavior as a compiler-visible relation"),
    }
    for index in range(56, 61):
        title, effect = gati_titles[index]
        kind = RuleKind.UPASARGA if index in {58, 59} else RuleKind.GATI
        add(
            f"1.4.{index}",
            kind,
            title,
            effect,
            ("sanskript.avyaya.upasarga_surfaces", "sanskript.avyaya.iter_avyaya_analyses", "sanskript.grammar.Samjna"),
            _example(title, "gati/upasarga", effect),
            ImplementationMode.EXECUTABLE if index in {58, 59, 60} else ImplementationMode.SEMANTIC,
        )

    for index in range(61, 98):
        add(
            f"1.4.{index}",
            RuleKind.GATI if index < 83 else RuleKind.KARMAPRAVACANIYA,
            f"gati/karmapravacanīya domain rule {index}",
            "records a particle, prefix, or governed-object relation that changes grammatical role without pretending to be word order",
            ("sanskript.avyaya.iter_avyaya_analyses", "sanskript.syntax.profile_sentence", "sanskript.karaka.get_vibhakti"),
            _example(f"1.4.{index}", "relation particle metadata", "the relation remains visible to syntax and vibhakti selection"),
            ImplementationMode.SEMANTIC,
        )

    for index in range(98, 109):
        add(
            f"1.4.{index}",
            RuleKind.KARMAPRAVACANIYA,
            f"nipāta/karmapravacanīya rule {index}",
            "records a late Adhyāya 1 particle relation as syntax-visible metadata",
            ("sanskript.avyaya.iter_avyaya_analyses", "sanskript.syntax.profile_sentence"),
            _example(f"1.4.{index}", "particle relation", "particle force is represented by analysis metadata"),
            ImplementationMode.SEMANTIC,
        )

    for index, title, effect, hook in (
        (109, "paraḥ sannikarṣaḥ saṃhitā", "recognizes close phonological proximity as saṃhitā", "sanskript.categories.is_samhita"),
        (110, "virāmo'vasānam", "recognizes cessation of sound as avasāna", "sanskript.categories.is_avasana"),
    ):
        add(
            f"1.4.{index}",
            RuleKind.SAMHITA,
            title,
            effect,
            (hook,),
            _example(title, "sound boundary", effect),
            ImplementationMode.EXECUTABLE,
        )

    return rules


ADHYAYA1_RULES = _build_rules()
