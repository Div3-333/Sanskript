"""Discrete Pāṇinian predicates for Adhyāya 1.1 sūtras that were absent
from the main ``sutra_logic`` registry (29 sūtras).

Each function tests the specific condition the sūtra names — sambuddhi
pragṛhya, sarvanāma restrictions in compounds, krt-avyaya endings,
sthānivat-bhāva and lopa paribhāṣās, etc. Every predicate is exercised
against a hand-curated positive context (Pāṇini's canonical example)
and a near-miss negative context.

The module is wired into the main truth-gate registry via
:func:`sutra_impl_base.register_module_in_registry`, so each sūtra gets
a real :class:`DiscreteSutraLogic` record (not a slug roundtrip).
"""
from __future__ import annotations

from .sutra_impl_base import SutraMeta, make_module_api


# ---------------------------------------------------------------------------
# Pragṛhya extensions (1.1.13-19): which surface forms are NOT subject to sandhi
# ---------------------------------------------------------------------------

def sutra_1_1_13(c) -> bool:
    """śe: the locative singular ending 'śe' (after dual/plural pronouns) is pragṛhya."""
    return str(c.get("ending")) == "śe" and bool(c.get("is_locative_singular"))


def sutra_1_1_14(c) -> bool:
    """nipāta ekāj anāṅ: single-vowel nipātas (particles), excluding 'āṅ', are pragṛhya."""
    surface = str(c.get("surface", ""))
    return (bool(c.get("is_nipata"))
            and len(surface) == 1
            and surface != "ā")


def sutra_1_1_16(c) -> bool:
    """sambuddhau śākalyasyetāvanārṣe: per Śākalya, the vocative singular -o/-e
    final is pragṛhya in non-Vedic (laukika) usage."""
    return (bool(c.get("is_sambuddhi"))
            and str(c.get("final", "")) in {"o", "e"}
            and not bool(c.get("is_vedic")))


def sutra_1_1_17(c) -> bool:
    """uñaḥ: the particle 'uñ' is pragṛhya."""
    return str(c.get("surface")) == "u" and bool(c.get("is_nipata"))


def sutra_1_1_18(c) -> bool:
    """ūm̐: the particle 'ūm̐' is pragṛhya."""
    return str(c.get("surface")) in {"ūm̐", "ūm"} and bool(c.get("is_nipata"))


# ---------------------------------------------------------------------------
# Sarvanāma restrictions inside compounds (1.1.28-36)
# ---------------------------------------------------------------------------

def sutra_1_1_28(c) -> bool:
    """vibhāṣā diksamāse bahuvrīhau: sarvanāma status is OPTIONAL for a
    direction-word inside a bahuvrīhi compound."""
    return (bool(c.get("is_sarvanama_stem"))
            and str(c.get("compound_type")) == "bahuvrihi"
            and bool(c.get("is_dik_compound")))


def sutra_1_1_29(c) -> bool:
    """na bahuvrīhau: sarvanāma status is BLOCKED inside a bahuvrīhi
    compound (general rule, overridden by 1.1.28)."""
    return (bool(c.get("is_sarvanama_stem"))
            and str(c.get("compound_type")) == "bahuvrihi"
            and not bool(c.get("is_dik_compound")))


def sutra_1_1_30(c) -> bool:
    """tṛtīyāsamāse: sarvanāma status is blocked in instrumental-tatpuruṣa."""
    return (bool(c.get("is_sarvanama_stem"))
            and str(c.get("compound_type")) == "tatpurusha"
            and str(c.get("compound_case")) == "instrumental")


def sutra_1_1_31(c) -> bool:
    """dvandve ca: sarvanāma status is blocked in dvandva compounds."""
    return (bool(c.get("is_sarvanama_stem"))
            and str(c.get("compound_type")) == "dvandva")


def sutra_1_1_32(c) -> bool:
    """vibhāṣā jasi: sarvanāma status is OPTIONAL before the nominative
    plural ending 'jas'."""
    return (bool(c.get("is_sarvanama_stem"))
            and str(c.get("following_suffix")) == "jas")


SARVANAMA_LIST_1_1_33 = frozenset({
    "prathama", "carama", "taya", "alpa", "ardha", "katipaya", "nema",
})


def sutra_1_1_33(c) -> bool:
    """prathamacaramatayālpārdhakatipayanemāśca: the listed terms are sarvanāma
    (in their non-jas usage)."""
    return str(c.get("stem")) in SARVANAMA_LIST_1_1_33


SARVANAMA_LIST_1_1_34 = frozenset({
    "pūrva", "para", "avara", "dakṣiṇa", "uttara", "apara", "adhara",
})


def sutra_1_1_34(c) -> bool:
    """pūrvaparāvaradakṣiṇottarāparādharāṇi vyavasthāyāmasaṁjñāyām:
    the seven directional terms are sarvanāma when used positionally
    and not as proper names."""
    return (str(c.get("stem")) in SARVANAMA_LIST_1_1_34
            and bool(c.get("is_vyavastha"))
            and not bool(c.get("is_proper_name")))


def sutra_1_1_35(c) -> bool:
    """svamajñātidhanākhyāyām: 'sva' is sarvanāma EXCEPT when it means
    'kinsman' (jñāti) or 'property' (dhana)."""
    if str(c.get("stem")) != "sva":
        return False
    sense = str(c.get("semantic", ""))
    return sense not in {"jnati", "dhana"}


def sutra_1_1_36(c) -> bool:
    """antaraṁ bahir-yogopasaṁvyānayoḥ: 'antara' is sarvanāma when paired
    with bahis (outside) or upasaṁvyāna (clothing)."""
    return (str(c.get("stem")) == "antara"
            and str(c.get("semantic", "")) in {"bahir_yoga", "upasamvyana"})


# ---------------------------------------------------------------------------
# Avyaya (indeclinables) 1.1.38-39
# ---------------------------------------------------------------------------

def sutra_1_1_38(c) -> bool:
    """taddhitaścāsarvavibhaktiḥ: a taddhita-formed word that does not
    inflect in all cases (lacks full case-paradigm) is avyaya."""
    return (bool(c.get("is_taddhita"))
            and not bool(c.get("has_full_case_paradigm")))


def sutra_1_1_39(c) -> bool:
    """kṛnmejantaḥ: krt-suffix-formed words ending in m / e / o / au
    (the 'mejantaḥ' set) are avyaya."""
    surface = str(c.get("surface", ""))
    return (bool(c.get("is_krt"))
            and len(surface) >= 1
            and (surface.endswith("m") or surface[-1] in {"e", "o"}
                 or surface.endswith("au")))


# ---------------------------------------------------------------------------
# Saṁprasāraṇa (1.1.45)
# ---------------------------------------------------------------------------

IK_VOWELS = frozenset({"i", "ī", "u", "ū", "ṛ", "ṝ", "ḷ", "ḹ"})
YAN_CONSONANTS = frozenset({"y", "v", "r", "l"})


def sutra_1_1_45(c) -> bool:
    """ig yaṇaḥ samprasāraṇam: a yaṇ (y/v/r/l) being replaced by its
    corresponding ik vowel (i/u/ṛ/ḷ) is called saṁprasāraṇa."""
    return (str(c.get("original")) in YAN_CONSONANTS
            and str(c.get("substitute")) in IK_VOWELS)


# ---------------------------------------------------------------------------
# Sthānivat-bhāva and lopa paribhāṣās (1.1.56-63)
# ---------------------------------------------------------------------------

def sutra_1_1_56(c) -> bool:
    """sthānivad ādeśo'nalvidhau: an ādeśa (substitute) behaves like its
    sthānin (substituendum) for all rules EXCEPT al-vidhi (rules referring
    to specific sounds)."""
    return bool(c.get("has_adesha")) and not bool(c.get("is_al_vidhi"))


def sutra_1_1_57(c) -> bool:
    """acaḥ parasmin pūrvavidhau: a vowel-ādeśa, in respect of the rule
    of the FOLLOWING term, behaves like the previous (sthānivat)."""
    return (bool(c.get("has_adesha"))
            and bool(c.get("is_vowel_adesha"))
            and str(c.get("vidhi_target")) == "para")


_1_1_58_EXCLUDED_RULES = frozenset({
    "padanta", "dvirvacana", "vareyalopa", "svara", "savarna",
    "anusvara", "dirgha", "jashcar",
})


def sutra_1_1_58(c) -> bool:
    """na padāntadvirvacanavareyalopasvarasavarṇānusvāradīrghajaścarvidhiṣu:
    sthānivat-bhāva is blocked for the listed eight rule-classes."""
    return str(c.get("vidhi_class")) in _1_1_58_EXCLUDED_RULES


def sutra_1_1_59(c) -> bool:
    """dvirvacane'ci: in reduplication before a vowel, the substitute is
    treated as the original (sthānivat reinstated for this case)."""
    return (str(c.get("vidhi_class")) == "dvirvacana"
            and bool(c.get("following_is_vowel")))


def sutra_1_1_60(c) -> bool:
    """adarśanaṁ lopaḥ: the non-appearance (disappearance) of a unit is
    called lopa."""
    return str(c.get("operation")) == "lopa" and not bool(c.get("is_visible"))


_LOPA_NAMES_1_1_61 = frozenset({"luk", "ślu", "lup"})


def sutra_1_1_61(c) -> bool:
    """pratyayasya lukślulupaḥ: the three named varieties (luk / ślu / lup)
    of lopa apply specifically to pratyaya (suffix) deletion."""
    return (str(c.get("operation")) in _LOPA_NAMES_1_1_61
            and bool(c.get("is_pratyaya")))


def sutra_1_1_62(c) -> bool:
    """pratyayalope pratyayalakṣaṇam: even after the suffix is deleted by
    lopa, the operations conditioned by the (now-deleted) suffix still
    apply (pratyaya-lakṣaṇa)."""
    return (str(c.get("operation")) == "pratyaya-lopa"
            and bool(c.get("post_lopa_pratyaya_property")))


def sutra_1_1_63(c) -> bool:
    """na lumatāṅgasya: but the pratyaya-property does NOT condition
    operations on the aṅga (stem) before luk / ślu / lup."""
    return (str(c.get("operation")) in _LOPA_NAMES_1_1_61
            and str(c.get("target")) == "anga")


# ---------------------------------------------------------------------------
# Case-reference paribhāṣās and śabdarūpa (1.1.66-72)
# ---------------------------------------------------------------------------

def sutra_1_1_66(c) -> bool:
    """tasminniti nirdiṣṭe pūrvasya: when a rule names a context in the
    locative ('in/under that'), the operation targets the PREVIOUS unit."""
    return str(c.get("ref_case")) == "locative" and str(c.get("operation_target")) == "purva"


def sutra_1_1_67(c) -> bool:
    """tasmādityuttarasya: when a rule names a context in the ablative
    ('from that'), the operation targets the FOLLOWING unit."""
    return str(c.get("ref_case")) == "ablative" and str(c.get("operation_target")) == "uttara"


def sutra_1_1_68(c) -> bool:
    """svaṁ rūpaṁ śabdasyāśabdasaṁjñā: a word, when not used as a saṁjñā
    (technical name), refers to its own form (and not to its sense)."""
    return not bool(c.get("is_samjna_use")) and bool(c.get("refers_to_own_form"))


def sutra_1_1_72(c) -> bool:
    """yena vidhistadantasya: an operation prescribed for X applies to
    whatever ENDS in X (the 'tad-anta' principle)."""
    return (str(c.get("operation_specifier")) == str(c.get("target_final"))
            and bool(c.get("apply_tadanta")))


# ---------------------------------------------------------------------------
# Linguistic fixtures (positive, negative) for every sūtra above
# ---------------------------------------------------------------------------

FIXTURES: dict[str, tuple[dict, dict]] = {
    "1.1.13": (
        {"ending": "śe", "is_locative_singular": True},
        {"ending": "su", "is_locative_singular": True},
    ),
    "1.1.14": (
        {"surface": "a", "is_nipata": True},
        {"surface": "ā", "is_nipata": True},
    ),
    "1.1.16": (
        {"is_sambuddhi": True, "final": "o", "is_vedic": False},
        {"is_sambuddhi": True, "final": "o", "is_vedic": True},
    ),
    "1.1.17": (
        {"surface": "u", "is_nipata": True},
        {"surface": "u", "is_nipata": False},
    ),
    "1.1.18": (
        {"surface": "ūm̐", "is_nipata": True},
        {"surface": "ūm̐", "is_nipata": False},
    ),
    "1.1.28": (
        {"is_sarvanama_stem": True, "compound_type": "bahuvrihi", "is_dik_compound": True},
        {"is_sarvanama_stem": True, "compound_type": "bahuvrihi", "is_dik_compound": False},
    ),
    "1.1.29": (
        {"is_sarvanama_stem": True, "compound_type": "bahuvrihi", "is_dik_compound": False},
        {"is_sarvanama_stem": True, "compound_type": "tatpurusha", "is_dik_compound": False},
    ),
    "1.1.30": (
        {"is_sarvanama_stem": True, "compound_type": "tatpurusha", "compound_case": "instrumental"},
        {"is_sarvanama_stem": True, "compound_type": "tatpurusha", "compound_case": "genitive"},
    ),
    "1.1.31": (
        {"is_sarvanama_stem": True, "compound_type": "dvandva"},
        {"is_sarvanama_stem": True, "compound_type": "tatpurusha"},
    ),
    "1.1.32": (
        {"is_sarvanama_stem": True, "following_suffix": "jas"},
        {"is_sarvanama_stem": True, "following_suffix": "su"},
    ),
    "1.1.33": (
        {"stem": "prathama"},
        {"stem": "deva"},
    ),
    "1.1.34": (
        {"stem": "pūrva", "is_vyavastha": True, "is_proper_name": False},
        {"stem": "pūrva", "is_vyavastha": True, "is_proper_name": True},
    ),
    "1.1.35": (
        {"stem": "sva", "semantic": "atman"},
        {"stem": "sva", "semantic": "jnati"},
    ),
    "1.1.36": (
        {"stem": "antara", "semantic": "bahir_yoga"},
        {"stem": "antara", "semantic": "ordinary"},
    ),
    "1.1.38": (
        {"is_taddhita": True, "has_full_case_paradigm": False},
        {"is_taddhita": True, "has_full_case_paradigm": True},
    ),
    "1.1.39": (
        {"is_krt": True, "surface": "kartum"},
        {"is_krt": True, "surface": "kartā"},
    ),
    "1.1.45": (
        {"original": "y", "substitute": "i"},
        {"original": "y", "substitute": "a"},
    ),
    "1.1.56": (
        {"has_adesha": True, "is_al_vidhi": False},
        {"has_adesha": True, "is_al_vidhi": True},
    ),
    "1.1.57": (
        {"has_adesha": True, "is_vowel_adesha": True, "vidhi_target": "para"},
        {"has_adesha": True, "is_vowel_adesha": False, "vidhi_target": "para"},
    ),
    "1.1.58": (
        {"vidhi_class": "dvirvacana"},
        {"vidhi_class": "samasa"},
    ),
    "1.1.59": (
        {"vidhi_class": "dvirvacana", "following_is_vowel": True},
        {"vidhi_class": "dvirvacana", "following_is_vowel": False},
    ),
    "1.1.60": (
        {"operation": "lopa", "is_visible": False},
        {"operation": "lopa", "is_visible": True},
    ),
    "1.1.61": (
        {"operation": "luk", "is_pratyaya": True},
        {"operation": "luk", "is_pratyaya": False},
    ),
    "1.1.62": (
        {"operation": "pratyaya-lopa", "post_lopa_pratyaya_property": True},
        {"operation": "pratyaya-lopa", "post_lopa_pratyaya_property": False},
    ),
    "1.1.63": (
        {"operation": "luk", "target": "anga"},
        {"operation": "luk", "target": "pratyaya"},
    ),
    "1.1.66": (
        {"ref_case": "locative", "operation_target": "purva"},
        {"ref_case": "locative", "operation_target": "uttara"},
    ),
    "1.1.67": (
        {"ref_case": "ablative", "operation_target": "uttara"},
        {"ref_case": "ablative", "operation_target": "purva"},
    ),
    "1.1.68": (
        {"is_samjna_use": False, "refers_to_own_form": True},
        {"is_samjna_use": True, "refers_to_own_form": True},
    ),
    "1.1.72": (
        {"operation_specifier": "a", "target_final": "a", "apply_tadanta": True},
        {"operation_specifier": "a", "target_final": "i", "apply_tadanta": True},
    ),
}


# ---------------------------------------------------------------------------
# Registry metadata (operator class, summary, assigned tags) for each sūtra
# ---------------------------------------------------------------------------

_SAMJNA = "samjna"
_PARIBHASHA = "paribhasha"
_VIDHI = "vidhi"
_PRATISEDHA = "pratisedha"
_VIBHASHA = "vibhasha"

META: dict[str, SutraMeta] = {
    "1.1.13": SutraMeta(_SAMJNA, "śe: locative-singular śe is pragṛhya", ("samjna:pragrhya",)),
    "1.1.14": SutraMeta(_SAMJNA, "nipāta ekāj anāṅ: single-vowel particles (except āṅ) are pragṛhya", ("samjna:pragrhya",)),
    "1.1.16": SutraMeta(_SAMJNA, "sambuddhau śākalyasyetāvanārṣe: laukika vocative-singular -o/-e is pragṛhya per Śākalya", ("samjna:pragrhya",)),
    "1.1.17": SutraMeta(_SAMJNA, "uñaḥ: particle uñ is pragṛhya", ("samjna:pragrhya",)),
    "1.1.18": SutraMeta(_SAMJNA, "ūm̐: particle ūm̐ is pragṛhya", ("samjna:pragrhya",)),
    "1.1.28": SutraMeta(_VIBHASHA, "vibhāṣā diksamāse bahuvrīhau: sarvanāma optional in dik-bahuvrīhi", ("samjna:sarvanama-optional",)),
    "1.1.29": SutraMeta(_PRATISEDHA, "na bahuvrīhau: sarvanāma blocked in bahuvrīhi", ("block:sarvanama",)),
    "1.1.30": SutraMeta(_PRATISEDHA, "tṛtīyāsamāse: sarvanāma blocked in instrumental-tatpuruṣa", ("block:sarvanama",)),
    "1.1.31": SutraMeta(_PRATISEDHA, "dvandve ca: sarvanāma blocked in dvandva", ("block:sarvanama",)),
    "1.1.32": SutraMeta(_VIBHASHA, "vibhāṣā jasi: sarvanāma optional before jas", ("samjna:sarvanama-optional",)),
    "1.1.33": SutraMeta(_SAMJNA, "prathamacaramatayālpārdhakatipayanemāśca: listed terms are sarvanāma", ("samjna:sarvanama",)),
    "1.1.34": SutraMeta(_SAMJNA, "directional terms are sarvanāma when used positionally and not as names", ("samjna:sarvanama",)),
    "1.1.35": SutraMeta(_PRATISEDHA, "svamajñātidhanākhyāyām: sva is NOT sarvanāma in kin/wealth senses", ("block:sarvanama",)),
    "1.1.36": SutraMeta(_SAMJNA, "antaram bahiryogopasaṁvyānayoḥ: antara is sarvanāma in bahis/clothing senses", ("samjna:sarvanama",)),
    "1.1.38": SutraMeta(_SAMJNA, "taddhitaścāsarvavibhaktiḥ: case-defective taddhita derivation is avyaya", ("samjna:avyaya",)),
    "1.1.39": SutraMeta(_SAMJNA, "kṛnmejantaḥ: m-/e-/o-/au-final krt forms are avyaya", ("samjna:avyaya",)),
    "1.1.45": SutraMeta(_SAMJNA, "ig yaṇaḥ samprasāraṇam: yaṇ → ik substitution is saṁprasāraṇa", ("samjna:samprasarana",)),
    "1.1.56": SutraMeta(_PARIBHASHA, "sthānivadādeśo'nalvidhau: ādeśa is sthānivat except in al-vidhi", ("meta:sthanivat",)),
    "1.1.57": SutraMeta(_PARIBHASHA, "acaḥ parasmin pūrvavidhau: vowel-ādeśa sthānivat for following rules", ("meta:sthanivat",)),
    "1.1.58": SutraMeta(_PRATISEDHA, "blocks sthānivat for 8 listed rule-classes (padānta, dvirvacana, ...)", ("block:sthanivat",)),
    "1.1.59": SutraMeta(_PARIBHASHA, "dvirvacane'ci: in reduplication before vowel, treat substitute as sthānin", ("meta:sthanivat",)),
    "1.1.60": SutraMeta(_SAMJNA, "adarśanaṁ lopaḥ: disappearance is called lopa", ("samjna:lopa",)),
    "1.1.61": SutraMeta(_SAMJNA, "pratyayasya luk-ślu-lupaḥ: three suffix-lopa varieties", ("samjna:suffix-lopa",)),
    "1.1.62": SutraMeta(_PARIBHASHA, "pratyayalope pratyayalakṣaṇam: suffix-properties survive lopa", ("meta:pratyaya-laksana",)),
    "1.1.63": SutraMeta(_PRATISEDHA, "na lumatā'ṅgasya: but not for aṅga before luk/ślu/lup", ("block:pratyaya-laksana",)),
    "1.1.66": SutraMeta(_PARIBHASHA, "tasmin iti nirdiṣṭe pūrvasya: locative reference targets previous", ("meta:case-reference",)),
    "1.1.67": SutraMeta(_PARIBHASHA, "tasmādityuttarasya: ablative reference targets following", ("meta:case-reference",)),
    "1.1.68": SutraMeta(_PARIBHASHA, "svaṁ rūpaṁ śabdasya: a word denotes itself unless used as saṁjñā", ("meta:sva-rupa",)),
    "1.1.72": SutraMeta(_PARIBHASHA, "yena vidhistadantasya: an X-rule applies to whatever ends in X", ("meta:tadanta",)),
}


(
    IMPLEMENTED_IDS,
    has_real_implementation,
    handler_for,
    positive_features,
    negative_features,
) = make_module_api(FIXTURES, globals())
