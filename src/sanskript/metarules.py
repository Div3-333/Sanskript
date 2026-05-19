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
    MetaRule("1.1.4", RuleBehavior.PROHIBITION, "na dhātulopa ārdhadhātuke", "prohibits guṇa/vṛddhi when dhātu-lopa occurs before an ārdhadhātuka suffix"),
    MetaRule("1.1.5", RuleBehavior.PROHIBITION, "kniti ca", "prohibits guṇa/vṛddhi when followed by a kit or ṅit suffix"),
    MetaRule("1.1.6", RuleBehavior.PROHIBITION, "dīdīvevīṭām", "prohibits guṇa/vṛddhi for roots dīdī, vevī, and before the augment iṭ"),
    MetaRule("1.1.7", RuleBehavior.TECHNICAL_MARKER, "halo'nantarāḥ saṃyogaḥ", "defines saṃyoga as a sequence of consonants without intervening vowels"),
    MetaRule("1.1.20", RuleBehavior.TECHNICAL_MARKER, "dādhāghvadāp", "defines ghu for dā and dhā roots (except dāp and daip)"),
    MetaRule("1.1.21", RuleBehavior.TECHNICAL_MARKER, "ādyantavad-ekasmin", "meta-logical rule: single sound treated as both beginning and end"),
    MetaRule("1.1.22", RuleBehavior.TECHNICAL_MARKER, "taraptamapau ghaḥ", "defines gha for tarap and tamap suffixes"),
    MetaRule("1.1.23", RuleBehavior.TECHNICAL_MARKER, "bahu-gaṇa-vatu-ḍati saṃkhyā", "defines saṃkhyā for bahu, gaṇa, vatu, and ḍati"),
    MetaRule("1.1.24", RuleBehavior.TECHNICAL_MARKER, "ṣṇāntā ṣaṭ", "defines ṣaṭ for numerals ending in ṣ or n"),
    MetaRule("1.1.25", RuleBehavior.TECHNICAL_MARKER, "ḍati ca", "ḍati is also ṣaṭ"),
    MetaRule("1.1.26", RuleBehavior.TECHNICAL_MARKER, "ktaktavatū niṣṭhā", "defines niṣṭhā for kta and ktavatu suffixes"),
    MetaRule("1.1.27", RuleBehavior.TECHNICAL_MARKER, "sarvādīni sarvanāmāni", "defines sarvanāma for sarva etc."),
    MetaRule("1.1.28", RuleBehavior.OPTIONALITY, "vibhāṣā dik-samāse bahuvrīhau", "optional sarvanāma in direction compounds"),
    MetaRule("1.1.29", RuleBehavior.PROHIBITION, "na bahuvrīhau", "prohibits sarvanāma in general bahuvrīhi"),
    MetaRule("1.1.30", RuleBehavior.OPTIONALITY, "tṛtīyā-samāse", "optional sarvanāma in tṛtīyā-tatpuruṣa"),
    MetaRule("1.1.31", RuleBehavior.PROHIBITION, "dvandve ca", "prohibits sarvanāma in dvandva"),
    MetaRule("1.1.32", RuleBehavior.OPTIONALITY, "vibhāṣā jasi", "optional sarvanāma for certain words in nominative plural"),
    MetaRule("1.1.33", RuleBehavior.OPTIONALITY, "prathama-carama...", "optional sarvanāma for prathama, carama, etc."),
    MetaRule("1.1.34", RuleBehavior.OPTIONALITY, "pūrva-parāvara...", "optional sarvanāma for pūrva, para, etc. in certain contexts"),
    MetaRule("1.1.35", RuleBehavior.OPTIONALITY, "svam-ajñāti-dhanākhyāyām", "optional sarvanāma for sva"),
    MetaRule("1.1.36", RuleBehavior.OPTIONALITY, "antaraṃ bahiryoga-upasaṃvyānayoḥ", "optional sarvanāma for antara"),
    MetaRule("1.1.37", RuleBehavior.TECHNICAL_MARKER, "svarādi-nipātam-avyayam", "defines avyaya for svar etc. and nipātas"),
    MetaRule("1.1.38", RuleBehavior.TECHNICAL_MARKER, "taddhitaś-ca-asarvavibhaktiḥ", "defines avyaya for non-inflecting taddhitas"),
    MetaRule("1.1.39", RuleBehavior.TECHNICAL_MARKER, "kṛn-mejantaḥ", "defines avyaya for kṛt suffixes ending in m, e, ai, o, au"),
    MetaRule("1.1.40", RuleBehavior.TECHNICAL_MARKER, "ktvā-tosun-kasunaḥ", "defines avyaya for ktvā, tosun, kasun"),
    MetaRule("1.1.41", RuleBehavior.TECHNICAL_MARKER, "avyayībhāvaś-ca", "defines avyaya for avyayībhāva compounds"),
    MetaRule("1.1.42", RuleBehavior.TECHNICAL_MARKER, "na-veti vibhāṣā", "defines vibhāṣā as 'not' or 'optionally'"),
    MetaRule("1.1.43", RuleBehavior.TECHNICAL_MARKER, "suḍ-anapuṃsakasya", "technical term suṭ for the first five case endings"),
    MetaRule("1.1.44", RuleBehavior.TECHNICAL_MARKER, "na veti vibhāṣā", "repeated vibhāṣā definition context"),
    MetaRule("1.1.45", RuleBehavior.TECHNICAL_MARKER, "iggata-asya guṇa-vṛddhī", "guṇa and vṛddhi replacements apply to ik sounds"),
    MetaRule("1.1.46", RuleBehavior.SUBSTITUTION, "ādyantau ṭakitau", "markers ṭ/k make the pratyaya/augment an initial/final part"),
    MetaRule("1.1.47", RuleBehavior.SUBSTITUTION, "midaco'ntyāt paraḥ", "marker m makes the augment follow the last vowel"),
    MetaRule("1.1.48", RuleBehavior.SUBSTITUTION, "eca iṅ hrasvādeśe", "hrasva of ec is i/u"),
    MetaRule("1.1.49", RuleBehavior.SUBSTITUTION, "ṣaṣṭhī sthāneyogā", "genitive marks the place of substitution"),
    MetaRule("1.1.50", RuleBehavior.SUBSTITUTION, "sthāne'ntaratamaḥ", "closest substitute among candidates"),
    MetaRule("1.1.51", RuleBehavior.SUBSTITUTION, "uraṇ raparaḥ", "ṛ substitute followed by r/l"),
    MetaRule("1.1.52", RuleBehavior.SUBSTITUTION, "alo'ntyasya", "substitution happens to the last sound (unless otherwise stated)"),
    MetaRule("1.1.53", RuleBehavior.SUBSTITUTION, "ṅid-anekāl-śit-sarvasya", "substitute with multiple sounds or ś replaces all"),
    MetaRule("1.1.54", RuleBehavior.SUBSTITUTION, "ādeḥ parasya", "substitute happens to the first sound of the following"),
    MetaRule("1.1.55", RuleBehavior.SUBSTITUTION, "anekāl-śit-sarvasya", "multisound/ś substitute replaces the entire term"),
    MetaRule("1.1.56", RuleBehavior.TECHNICAL_MARKER, "sthānivadādeśo'nalvidhau", "substitute behaves like the original (unless sound-specific)"),
    MetaRule("1.1.57", RuleBehavior.TECHNICAL_MARKER, "acyasmin pūrva-vidhau", "sthānivadbhāva in context of preceding vowel operations"),
    MetaRule("1.1.58", RuleBehavior.PROHIBITION, "na padānta-dvircana...", "limitations on sthānivadbhāva"),
    MetaRule("1.1.59", RuleBehavior.PROHIBITION, "dvirvacane'ci", "limitations on sthānivadbhāva in reduplication"),
    MetaRule("1.1.60", RuleBehavior.TECHNICAL_MARKER, "adadarśanaṃ lopaḥ", "lopa is the non-appearance of a sound/morpheme"),
    MetaRule("1.1.61", RuleBehavior.TECHNICAL_MARKER, "pratyayasya luk-ślu-lupaḥ", "types of deletion: luk, ślu, lup"),
    MetaRule("1.1.62", RuleBehavior.TECHNICAL_MARKER, "pratyaya-lope pratyaya-lakṣaṇam", "the effects of a suffix persist after its deletion"),
    MetaRule("1.1.63", RuleBehavior.PROHIBITION, "na lumatā-aṅgasya", "prohibition of pratyaya-lakṣaṇa for lumat deletion"),
    MetaRule("1.1.64", RuleBehavior.TECHNICAL_MARKER, "acyantyādi ṭi", "defines ṭi as the last vowel and any following consonants"),
    MetaRule("1.1.65", RuleBehavior.TECHNICAL_MARKER, "alo'ntyāt pūrva upadhā", "defines upadhā as the second to last sound"),
    MetaRule("1.1.66", RuleBehavior.TECHNICAL_MARKER, "tasminniti nirdiṣṭe pūrvasya", "locative marks the preceding term for operation"),
    MetaRule("1.1.67", RuleBehavior.TECHNICAL_MARKER, "tasmādityuttarasya", "ablative marks the following term for operation"),
    MetaRule("1.1.68", RuleBehavior.TECHNICAL_MARKER, "svam rūpaṃ śabdasyāśabdasaṃjñā", "a word represents its own form unless it is a technical term"),
    MetaRule("1.1.69", RuleBehavior.TECHNICAL_MARKER, "aṇ-udit savarṇasya cāpratyayaḥ", "a sound/udit represents its savarṇas (if not a suffix)"),
    MetaRule("1.1.70", RuleBehavior.TECHNICAL_MARKER, "taparas-tatkālasya", "a sound with marker t represents only that length"),
    MetaRule("1.1.71", RuleBehavior.TECHNICAL_MARKER, "ādirantyena sahetā", "defines pratyāhāra as start + end marker"),
    MetaRule("1.1.72", RuleBehavior.TECHNICAL_MARKER, "yena vidhis-tadantasya", "a rule applying to a term applies to its ending too"),
    MetaRule("1.1.73", RuleBehavior.TECHNICAL_MARKER, "vṛddhiryasyā-acām ādis-tad-vṛddham", "defines vṛddha as having vṛddhi as the first vowel"),
    MetaRule("1.1.74", RuleBehavior.TECHNICAL_MARKER, "tyādīni ca", "tyad etc. are also vṛddha"),
    MetaRule("1.1.75", RuleBehavior.TECHNICAL_MARKER, "eṅ prācāṃ deśe", "e/o as first vowel makes it vṛddha in eastern names"),
    MetaRule("1.2.1", RuleBehavior.TECHNICAL_MARKER, "gāṅkuṭādibhyo'ñṇit ṅit", "suffixes without ñ/ṇ after gāṅ/kuṭādi are ṅit"),
    MetaRule("1.2.4", RuleBehavior.TECHNICAL_MARKER, "sārvadhātukam-apit", "sārvadhātuka suffixes without p are ṅit"),
    MetaRule("1.2.5", RuleBehavior.TECHNICAL_MARKER, "asaṃyogāl-liṭ kit", "liṭ after a root not ending in a cluster is kit"),
    MetaRule("1.2.7", RuleBehavior.TECHNICAL_MARKER, "mṛḍa-mṛda-guḍa-kuṣa-kliśa-vada-vasaḥ ktvā", "ktvā after these roots is kit"),
    MetaRule("1.2.18", RuleBehavior.PROHIBITION, "na ktvā seṭ", "seṭ ktvā blocks kit behavior in the controlled derivation context"),
    MetaRule("1.2", RuleBehavior.TECHNICAL_MARKER, "it-marker discipline", "tracks markers that guide derivation and then disappear"),
    MetaRule("1.2", RuleBehavior.OPTIONALITY, "vā-option", "marks grammatically licensed alternatives without treating them as parser hacks"),
    MetaRule("1.2", RuleBehavior.PROHIBITION, "blocking conditions", "records when a later operation is grammatically unavailable"),
    MetaRule("1.2.41", RuleBehavior.TECHNICAL_MARKER, "apṛkta ekāl pratyayaḥ", "a single-sound suffix is apṛkta"),
    MetaRule("1.3", RuleBehavior.DOMAIN, "pada and voice domains", "keeps parasmaipada and ātmanepada choices attached to verbal morphology"),
    MetaRule("1.3", RuleBehavior.RECURSION, "anuvṛtti carry", "carries a governing condition into later rules until its domain closes"),
    MetaRule("8.1", RuleBehavior.OVERRIDE, "sentence-edge operations", "models clause-bound late operations separately from word formation"),
)


def rules_for_range(sutra_range: str) -> tuple[MetaRule, ...]:
    return tuple(rule for rule in META_RULES if rule.sutra_range == sutra_range)


def directive(input_form: str, output_form: str, behavior: RuleBehavior, optional: bool = False) -> CanonDirective:
    # Prefer general/named rules over specific sutra citations for standard behaviors
    for rule in META_RULES:
        if rule.behavior == behavior and not rule.sutra_range.startswith("1.1."):
            return CanonDirective(input_form=input_form, output_form=output_form, rule=rule, optional=optional)

    # Fallback to any matching rule
    for rule in META_RULES:
        if rule.behavior == behavior:
            return CanonDirective(input_form=input_form, output_form=output_form, rule=rule, optional=optional)
    raise ValueError(f"No metarule registered for {behavior.value!r}")


def is_vibhasha_expression(text: str) -> bool:
    """1.1.44 na veti vibhāṣā: na/vā-style wording marks grammatical optionality."""
    normalized = " ".join(text.strip().split())
    return normalized in {"na vā", "vā", "vibhāṣā", "na veti vibhāṣā"}
