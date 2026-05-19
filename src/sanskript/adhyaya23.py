from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .adhyaya2_atomic import ADHYAYA2_ATOMIC_SUTRAS, AtomicSutraSpec


class RuleKind(str, Enum):
    SAMASA_DOMAIN = "samasa_domain"
    COMPOUND_FORM = "compound_form"
    VIBHAKTI = "vibhakti"
    SUBANTA = "subanta"
    LOPA = "lopa"
    DHATU_DERIVATION = "dhatu_derivation"
    VIKARANA = "vikarana"
    KRT = "krt"
    LAKARA = "lakara"
    TIN = "tin"
    PARTICIPLE = "participle"


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
        return self.mode == ImplementationMode.DISCRETE and self.atomic

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
    "2.1": 72,
    "2.2": 38,
    "2.3": 73,
    "2.4": 84,
    "3.1": 150,
    "3.2": 188,
    "3.3": 176,
    "3.4": 117,
}


PADA_INDICES = {
    pada: tuple(range(1, count + 1))
    for pada, count in PADA_COUNTS.items()
}
PADA_INDICES["2.4"] = tuple(range(1, 27)) + tuple(range(28, 86))


DISCRETE_ADHYAYA2_IDS = frozenset(
    {
        "2.1.1",
        "2.1.5",
        "2.1.22",
        "2.1.30",
        "2.1.36",
        "2.1.57",
        "2.2.23",
        "2.2.29",
        "2.2.30",
        "2.3.1",
        "2.3.2",
        "2.3.5",
        "2.3.13",
        "2.3.16",
        "2.3.18",
        "2.3.19",
        "2.3.20",
        "2.3.23",
        "2.3.28",
        "2.3.36",
        "2.3.50",
        "2.4.1",
        "2.4.17",
        "2.4.26",
        "2.4.36",
        "2.4.37",
        "2.4.42",
        "2.4.45",
        "2.4.47",
        "2.4.48",
        "2.4.52",
        "2.4.71",
        "2.4.72",
        "2.4.75",
    }
)


def rule_for(sutra_id: str) -> SutraRule:
    try:
        return ADHYAYA23_RULES[sutra_id]
    except KeyError as exc:
        raise ValueError(f"No Adhyaya 2/3 rule for {sutra_id!r}") from exc


def rules_for_pada(pada: str) -> tuple[SutraRule, ...]:
    return tuple(rule for rule in ADHYAYA23_RULES.values() if rule.pada == pada)


def expected_adhyaya23_ids() -> tuple[str, ...]:
    return tuple(
        f"{pada}.{index}"
        for pada in PADA_COUNTS
        for index in PADA_INDICES[pada]
    )


def missing_rule_ids() -> tuple[str, ...]:
    return tuple(sutra_id for sutra_id in expected_adhyaya23_ids() if sutra_id not in ADHYAYA23_RULES)


def implemented_sutra_ids() -> frozenset[str]:
    return frozenset(sutra_id for sutra_id, rule in ADHYAYA23_RULES.items() if rule.implemented)


def partial_sutra_ids() -> frozenset[str]:
    return frozenset(sutra_id for sutra_id, rule in ADHYAYA23_RULES.items() if not rule.implemented)


def implementation_note_for(sutra_id: str) -> str:
    rule = rule_for(sutra_id)
    mode = "Discrete executable" if rule.mode == ImplementationMode.DISCRETE else "Partial"
    hooks = ", ".join(rule.hooks)
    return f"{mode} Adhyaya 2/3 implementation: {rule.sutra_text_iast}. {rule.compiler_effect} Hooks: {hooks}."


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
    )


def _atomic_rule(base: SutraRule, spec: AtomicSutraSpec) -> SutraRule:
    if spec.id in DISCRETE_ADHYAYA2_IDS:
        mode = ImplementationMode.DISCRETE
    else:
        mode = ImplementationMode.ATOMIC_EXECUTABLE if base.mode == ImplementationMode.EXECUTABLE else ImplementationMode.ATOMIC_FORMAL
    return _rule(
        spec.id,
        base.kind,
        mode,
        f"{spec.id} {spec.iast}",
        spec.operation,
        base.hooks,
        (RuleExample(spec.id, spec.positive_example, spec.operation),),
        sutra_text_devanagari=spec.devanagari,
        sutra_text_iast=spec.iast,
        source=spec.source,
        anuvritti=spec.anuvritti,
        conditions=spec.conditions,
        exceptions=spec.exceptions,
        counterexamples=(RuleExample(spec.id, spec.negative_example, "rejected counterexample for the atomic sutra condition"),),
    )


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
        rules[sutra_id] = _rule(sutra_id, kind, mode, title, compiler_effect, hooks, examples)

    executable_2_1 = {
        1: ("samarthaḥ padavidhiḥ", "requires compound members to have a meaningful syntactic-semantic relation"),
        5: ("avyayaṃ vibhakti-samīpa-samṛddhi...", "builds avyayībhāva compounds from indeclinable first members"),
        22: ("tatpuruṣaḥ", "classifies case-governed compounds as tatpuruṣa"),
        30: ("tṛtīyā tatkṛtārthena", "records instrumental tatpuruṣa sense"),
        36: ("saptamī śauṇḍaiḥ", "records locative tatpuruṣa sense"),
        49: ("pūrvakālaika...", "keeps temporal relation visible in compound semantics"),
        57: ("viśeṣaṇaṃ viśeṣyeṇa bahulam", "allows adjective-noun karmadhāraya analysis"),
        72: ("mayūravyamsakādayaś ca", "records listed compound exceptions as semantic examples"),
    }
    for index in range(1, 73):
        if index in executable_2_1:
            title, effect = executable_2_1[index]
            mode = ImplementationMode.EXECUTABLE
        elif index < 22:
            title = f"avyayībhāva domain rule {index}"
            effect = "records an indeclinable-first compound relation and its governed meaning"
            mode = ImplementationMode.SEMANTIC
        elif index < 50:
            title = f"tatpuruṣa case relation rule {index}"
            effect = "records the case-relation semantics that license a tatpuruṣa compound"
            mode = ImplementationMode.SEMANTIC
        else:
            title = f"karmadhāraya and compound subtype rule {index}"
            effect = "records qualifier, comparison, or listed compound semantics"
            mode = ImplementationMode.SEMANTIC
        add(
            f"2.1.{index}",
            RuleKind.SAMASA_DOMAIN,
            title,
            effect,
            ("sanskript.samasa.is_samartha", "sanskript.samasa.create_compound", "sanskript.samasa.SamasaSense"),
            _example(title, "compound relation", effect),
            mode,
        )

    executable_2_2 = {
        1: ("pūrvāparādhara-uttaram ekadeśinā", "records positional tatpuruṣa/karmadhāraya relations"),
        18: ("kugati-prādayaḥ", "keeps ku/gati/pra-style first members in compound analysis"),
        23: ("śeṣo bahuvrīhiḥ", "classifies residual exocentric compounds as bahuvrīhi"),
        29: ("cārthe dvandvaḥ", "classifies coordinated members as dvandva"),
        30: ("upasarjanaṃ pūrvam", "keeps upasarjana order visible in compound construction"),
        38: ("kaḍārāḥ karmadhāraye", "records the closing karmadhāraya exception domain"),
    }
    for index in range(1, 39):
        if index in executable_2_2:
            title, effect = executable_2_2[index]
            mode = ImplementationMode.EXECUTABLE
        elif index < 23:
            title = f"tatpuruṣa/bahuvrīhi boundary rule {index}"
            effect = "records member ordering and semantic conditions around tatpuruṣa formation"
            mode = ImplementationMode.SEMANTIC
        elif index < 30:
            title = f"bahuvrīhi rule {index}"
            effect = "records exocentric compound semantics and agreement behavior"
            mode = ImplementationMode.SEMANTIC
        else:
            title = f"dvandva/order rule {index}"
            effect = "records coordination, upasarjana order, or residual compound ordering"
            mode = ImplementationMode.SEMANTIC
        add(
            f"2.2.{index}",
            RuleKind.COMPOUND_FORM,
            title,
            effect,
            ("sanskript.samasa.classify_compound", "sanskript.samasa.create_compound", "sanskript.samasa.SamasaType"),
            _example(title, "compound form", effect),
            mode,
        )

    executable_2_3 = {
        1: ("anabhihite", "only assigns a kāraka case when the role is not already expressed"),
        2: ("karmaṇi dvitīyā", "maps unexpressed karman to accusative"),
        13: ("caturthī sampradāne", "maps sampradāna to dative"),
        18: ("kartṛ-karaṇayos tṛtīyā", "maps agent/instrument to instrumental where appropriate"),
        28: ("apādāne pañcamī", "maps apādāna to ablative"),
        36: ("saptamy adhikaraṇe ca", "maps adhikaraṇa to locative"),
        46: ("prātipadikārtha-liṅga-parimāṇa-vacana-mātre prathamā", "keeps nominative as default expressed nominal case"),
        50: ("ṣaṣṭhī śeṣe", "uses genitive for residual relations"),
        73: ("caturthī ca āśiṣi", "records the closing blessing/beneficiary case domain"),
    }
    for index in range(1, 74):
        if index in executable_2_3:
            title, effect = executable_2_3[index]
            mode = ImplementationMode.EXECUTABLE
        elif index < 13:
            title = f"accusative/upapada vibhakti rule {index}"
            effect = "records accusative or governed-object case selection"
            mode = ImplementationMode.SEMANTIC
        elif index < 28:
            title = f"instrumental/dative vibhakti rule {index}"
            effect = "records instrumental or dative case selection and upapada overrides"
            mode = ImplementationMode.SEMANTIC
        elif index < 46:
            title = f"ablative/locative vibhakti rule {index}"
            effect = "records separation, source, locus, or governed locative case selection"
            mode = ImplementationMode.SEMANTIC
        else:
            title = f"genitive/nominative residual vibhakti rule {index}"
            effect = "records default, genitive, blessing, or residual case behavior"
            mode = ImplementationMode.SEMANTIC
        add(
            f"2.3.{index}",
            RuleKind.VIBHAKTI,
            title,
            effect,
            ("sanskript.karaka.get_vibhakti", "sanskript.karaka.role_for_case", "sanskript.grammar.Case"),
            _example(title, "case selection", effect),
            mode,
        )

    executable_2_4 = {
        1: ("dvigur ekavacanam", "makes dvigu compounds singular"),
        17: ("avyayībhāvaś ca", "keeps avyayībhāva compound results neuter/indeclinable-like"),
        26: ("paraval-liṅgaṃ dvandva-tatpuruṣayoḥ", "uses the final member for dvandva/tatpuruṣa gender behavior"),
        35: ("ārdhadhātuke", "opens the ārdhadhātuka root-substitution domain"),
        36: ("ado jagdhiḥ", "substitutes jagdh for ad in selected ārdhadhātuka domains"),
        37: ("hano vadha liṅi", "substitutes vadh for han in āśīrliṅ"),
        42: ("hano vadha luṅi", "substitutes vadh for han in luṅ"),
        45: ("iṇo gā luṅi", "substitutes gā for i in luṅ"),
        47: ("khyāñ-cakṣiṅaḥ", "substitutes khyā for cakṣ"),
        52: ("aster bhūḥ", "substitutes bhū for as in ārdhadhātuka domains"),
        71: ("supo dhātu-prātipadikayoḥ", "elides internal sup endings before dhātu/prātipadika compounding"),
        72: ("adiprabhṛtibhyaḥ śapaḥ", "applies luk elision of śap for class-2 roots"),
        75: ("juhotyādibhyaḥ śluḥ", "records ślu behavior for class-3 roots"),
    }
    for index in PADA_INDICES["2.4"]:
        if index in executable_2_4:
            title, effect = executable_2_4[index]
            mode = ImplementationMode.EXECUTABLE
        elif index < 35:
            title = f"compound number/gender rule {index}"
            effect = "records number, gender, or retained-member behavior after compounding"
            mode = ImplementationMode.SEMANTIC
        elif index < 58:
            title = f"dhātu substitution rule {index}"
            effect = "records root substitution under finite or ārdhadhātuka conditions"
            mode = ImplementationMode.SEMANTIC
        else:
            title = f"sup/tiṅ/luk elision rule {index}"
            effect = "records suffix deletion, luk, ślu, or lup behavior while preserving grammatical effects"
            mode = ImplementationMode.SEMANTIC
        add(
            f"2.4.{index}",
            RuleKind.SUBANTA if index < 35 else RuleKind.LOPA,
            title,
            effect,
            ("sanskript.samasa.create_compound", "sanskript.tinanta.get_substituted_dhatu", "sanskript.tinanta.apply_luk_elision"),
            _example(title, "post-compound/inflection rule", effect),
            mode,
        )

    executable_3_1 = {
        1: ("pratyayaḥ", "opens the suffix-introduction domain"),
        2: ("paraś ca", "keeps suffix placement after the base"),
        5: ("gupti-jkdbhyaḥ san", "creates desiderative roots with san"),
        8: ("sup ātmanaḥ kyac", "creates denominative roots with kyac"),
        22: ("dhātoḥ ekāco halādeḥ kriyāsamabhihāre yaṅ", "creates intensive roots with yaṅ"),
        25: ("satyāpāśarūpavīṇātūlaślokasenālomātvaṅvarma-varṇa-cūrṇa-curādibhyo ṇic", "creates causative/curādi stems with ṇic"),
        33: ("syatāsi lṛ-luṭoḥ", "adds future/conditional stem material for lṛ/lṛṅ/luṭ"),
        68: ("kartari śap", "uses śap/a as the class-1 present stem-former"),
        69: ("divādibhyaḥ śyan", "uses śyan/ya for class-4 roots"),
        73: ("svādibhyaḥ śnu", "uses śnu/nu for class-5 roots"),
        77: ("tudādibhyaḥ śaḥ", "uses śa/a for class-6 roots"),
        78: ("rudhādibhyaḥ śnam", "uses śnam/na for class-7 roots"),
        79: ("tanādikṛñbhya uḥ", "uses u for class-8 roots"),
        81: ("kryādibhyaḥ śnā", "uses śnā/nā for class-9 roots"),
        91: ("dhātoḥ", "applies kṛt suffixes to verbal roots"),
        93: ("kṛd atiriṅ", "classifies non-tiṅ suffixes after roots as kṛt"),
    }
    for index in range(1, 151):
        if index in executable_3_1:
            title, effect = executable_3_1[index]
            mode = ImplementationMode.EXECUTABLE
        elif index < 33:
            title = f"sanādi-dhātu rule {index}"
            effect = "records a derived-root suffix and the semantic class it creates"
            mode = ImplementationMode.SEMANTIC
        elif index < 91:
            title = f"vikaraṇa and finite-base rule {index}"
            effect = "records present-stem formation and suffix conditions before tiṅ"
            mode = ImplementationMode.SEMANTIC
        else:
            title = f"kṛt-pratyaya domain rule {index}"
            effect = "records root-based nominal/participial suffix introduction"
            mode = ImplementationMode.SEMANTIC
        add(
            f"3.1.{index}",
            RuleKind.DHATU_DERIVATION if index < 33 else (RuleKind.VIKARANA if index < 91 else RuleKind.KRT),
            title,
            effect,
            ("sanskript.tinanta.create_derived_dhatu", "sanskript.tinanta.get_vikarana", "sanskript.derivation.derive"),
            _example(title, "derived root/stem", effect),
            mode,
        )

    executable_3_2 = {
        1: ("karmaṇy aṇ", "derives controlled aṇ forms in object relation"),
        3: ("āto'nupasarge kaḥ", "derives ka after ā-final roots without upasarga"),
        16: ("careṣ ṭaḥ", "derives ṭa/ta-class forms in motion/action domains"),
        102: ("niṣṭhā", "introduces kta/ktavatū participial forms"),
        110: ("luṅ", "selects luṅ for past event reference"),
        111: ("anadyatane laṅ", "selects laṅ for non-today past"),
        123: ("vartamāne laṭ", "selects laṭ for present time"),
        124: ("laṭaḥ śatṛ-śānacau", "introduces present participles from laṭ domains"),
        135: ("ṇvul-tṛcau", "derives agent/instrument nouns with ṇvul and tṛc"),
        188: ("matibuddhipūjārthebhyaś ca", "records the closing kṛt semantic condition of the pāda"),
    }
    for index in range(1, 189):
        if index in executable_3_2:
            title, effect = executable_3_2[index]
            mode = ImplementationMode.EXECUTABLE
        elif index < 102:
            title = f"kṛt semantic environment rule {index}"
            effect = "records the semantic environment that licenses a kṛt suffix"
            mode = ImplementationMode.SEMANTIC
        elif index < 124:
            title = f"lakāra time-selection rule {index}"
            effect = "records tense/time semantics that select a lakāra"
            mode = ImplementationMode.SEMANTIC
        else:
            title = f"participial/agentive kṛt rule {index}"
            effect = "records participial, agentive, or instrumental nominal derivation"
            mode = ImplementationMode.SEMANTIC
        add(
            f"3.2.{index}",
            RuleKind.KRT if index < 102 else (RuleKind.LAKARA if index < 124 else RuleKind.PARTICIPLE),
            title,
            effect,
            ("sanskript.derivation.derive", "sanskript.tinanta.get_lakara_for_time", "sanskript.derivation.KrtSuffix"),
            _example(title, "kṛt/lakāra output", effect),
            mode,
        )

    executable_3_3 = {
        1: ("uṇādayo bahulam", "records productive-but-controlled uṇādi-style derivation"),
        15: ("lṛṭ śeṣe ca", "selects lṛṭ for future reference"),
        18: ("bhāve ghañ", "derives bhāva/abstract nouns with ghañ"),
        33: ("anadyatane luṭ", "selects luṭ for non-today future"),
        94: ("striyāṃ ktin", "derives feminine abstract/action nouns with ktin"),
        115: ("lyuṭ ca", "derives action nouns with lyuṭ"),
        121: ("halś ca", "derives gha-class forms after consonant-final roots"),
        139: ("liṅ-nimitte lṛṅ kriyātipattau", "selects lṛṅ for counterfactual/conditional semantics"),
        161: ("vidhi-nimantraṇa-āmantraṇa-adhīṣṭa-sampraśna-prārthaneṣu liṅ", "selects potential liṅ for injunction/request domains"),
        162: ("loṭ ca", "selects loṭ for command semantics"),
        163: ("praiṣātisargaprāptakāleṣu kṛtyāś ca", "allows kṛtya forms in command/permission contexts"),
        176: ("smottare laṅ ca", "records closing laṅ-domain condition"),
    }
    for index in range(1, 177):
        if index in executable_3_3:
            title, effect = executable_3_3[index]
            mode = ImplementationMode.EXECUTABLE
        elif index < 94:
            title = f"kṛt/bhāva suffix rule {index}"
            effect = "records abstract, action, or semantic-condition suffix behavior"
            mode = ImplementationMode.SEMANTIC
        elif index < 139:
            title = f"nominal action suffix rule {index}"
            effect = "records ktin, lyuṭ, gha, or related nominal derivation"
            mode = ImplementationMode.SEMANTIC
        else:
            title = f"mood and modal lakāra rule {index}"
            effect = "records potential, imperative, conditional, or permission semantics"
            mode = ImplementationMode.SEMANTIC
        add(
            f"3.3.{index}",
            RuleKind.KRT if index < 139 else RuleKind.LAKARA,
            title,
            effect,
            ("sanskript.derivation.derive", "sanskript.tinanta.get_lakara_for_time", "sanskript.tinanta.TimeContext"),
            _example(title, "derived form or lakāra", effect),
            mode,
        )

    executable_3_4 = {
        69: ("laḥ karmaṇi ca bhāve cākarmakebhyaḥ", "keeps voice/prayoga domains attached to tiṅ morphology"),
        79: ("ṭita ātmanepadānāṃ ṭere", "maps ātmanepada endings through e-like replacements"),
        80: ("thāsas se", "maps ātmanepada thās to se"),
        86: ("er uḥ", "maps loṭ third-person i endings to u"),
        87: ("ser hiḥ", "maps loṭ second singular si to hi"),
        88: ("ato heḥ", "elides hi after a-final stems"),
        92: ("āḍ uttamasya pic ca", "adds ā to first-person loṭ forms"),
        94: ("letó'ḍāṭau", "records luṭ/let-style person ending behavior"),
        100: ("itaś ca", "elides final i in ṅit lakāra endings"),
        101: ("tas-tas-tha-mipāṃ tām-taṃ-ta-amaḥ", "maps selected tiṅ endings in ṅit/loṭ domains"),
        108: ("jher jus", "maps jhi/nti to jus in vidhiliṅ"),
        113: ("tiṅ-śit sārvadhātukam", "classifies tiṅ/śit suffixes as sārvadhātuka"),
        114: ("ārdhadhātukaṃ śeṣaḥ", "classifies the remaining suffixes as ārdhadhātuka"),
        115: ("liṭ ca", "classifies liṭ as ārdhadhātuka"),
        117: ("chandasy ubhayathā", "records the closing Vedic optionality domain"),
    }
    for index in range(1, 118):
        if index in executable_3_4:
            title, effect = executable_3_4[index]
            mode = ImplementationMode.EXECUTABLE
        elif index < 69:
            title = f"indeclinable/kṛt completion rule {index}"
            effect = "records completion behavior for non-finite suffixes and indeclinable derivations"
            mode = ImplementationMode.SEMANTIC
        elif index < 94:
            title = f"tiṅ replacement rule {index}"
            effect = "records person-number ending replacement and voice-sensitive tiṅ behavior"
            mode = ImplementationMode.SEMANTIC
        else:
            title = f"sārvadhātuka/ārdhadhātuka rule {index}"
            effect = "records suffix-class behavior that controls downstream strengthening and endings"
            mode = ImplementationMode.SEMANTIC
        add(
            f"3.4.{index}",
            RuleKind.TIN if index >= 69 else RuleKind.KRT,
            title,
            effect,
            ("sanskript.tinanta.tin_ending", "sanskript.tinanta.join_stem_ending", "sanskript.tinanta.is_sarvadhatuka", "sanskript.tinanta.is_ardhadhatuka"),
            _example(title, "tiṅ/kṛt behavior", effect),
            mode,
        )

    for sutra_id, spec in ADHYAYA2_ATOMIC_SUTRAS.items():
        rules[sutra_id] = _atomic_rule(rules[sutra_id], spec)
    return rules


ADHYAYA23_RULES = _build_rules()
