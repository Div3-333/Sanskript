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


class ImplementationMode(str, Enum):
    EXECUTABLE = "executable"
    SEMANTIC = "semantic"


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

    @property
    def implemented(self) -> bool:
        return bool(self.hooks) and bool(self.examples)


def rule_for(sutra_id: str) -> SutraRule:
    try:
        return ADHYAYA1_RULES[sutra_id]
    except KeyError as exc:
        raise ValueError(f"No Adhyaya 1 half-workpack rule for {sutra_id!r}") from exc


def rules_for_pada(pada: str) -> tuple[SutraRule, ...]:
    return tuple(rule for rule in ADHYAYA1_RULES.values() if rule.pada == pada)


def implemented_sutra_ids() -> frozenset[str]:
    return frozenset(sutra_id for sutra_id, rule in ADHYAYA1_RULES.items() if rule.implemented)


def implementation_note_for(sutra_id: str) -> str:
    rule = rule_for(sutra_id)
    mode = "Executable" if rule.mode == ImplementationMode.EXECUTABLE else "Formal semantic"
    hooks = ", ".join(rule.hooks)
    return f"{mode} Adhyaya 1 implementation: {rule.compiler_effect} Hooks: {hooks}."


def expected_half_adhyaya_ids() -> tuple[str, ...]:
    return tuple(f"1.1.{index}" for index in range(1, 76)) + tuple(f"1.2.{index}" for index in range(1, 74))


def missing_rule_ids() -> tuple[str, ...]:
    return tuple(sutra_id for sutra_id in expected_half_adhyaya_ids() if sutra_id not in ADHYAYA1_RULES)


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

    sound_hooks = ("sanskript.phonology", "sanskript.anga")
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
        42: ("vibhāṣā", "models vibhāṣā as a first-class optionality directive"),
        43: ("suṭ", "records suṭ as the first five sup endings"),
        44: ("vibhāṣā repetition", "keeps optionality available through the local anuvṛtti domain"),
        45: ("ik replacement target", "keeps guṇa/vṛddhi tied to ik-bearing targets"),
    }
    for index, (title, effect) in technical_1_1.items():
        hooks = ("sanskript.avyaya", "sanskript.categories", "sanskript.metarules.rules_for_range")
        if index in {37, 38, 39, 40, 41}:
            hooks = ("sanskript.avyaya.iter_avyaya_analyses", "sanskript.samasa.create_compound")
        if index in {42, 44}:
            hooks = ("sanskript.metarules.directive",)
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
        53: ("ṅid/śit/sarvasya", "allows whole-term replacement under ṅit, multisound, or śit triggers"),
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
    for index, (title, effect) in substitution_1_1.items():
        add(
            f"1.1.{index}",
            RuleKind.SUBSTITUTION_META if index < 60 else RuleKind.LOPA_SEMANTICS,
            title,
            effect,
            ("sanskript.phonology.best_substitute", "sanskript.metarules.directive", "sanskript.markers.analyze_it_markers"),
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
        elif index in {69, 70, 73, 74, 75}:
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

    return rules


ADHYAYA1_RULES = _build_rules()
