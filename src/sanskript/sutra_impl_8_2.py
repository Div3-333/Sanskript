"""Discrete Pāṇinian predicates for Adhyāya 8.2 (pāda 8.2.1–8.2.108).

Asiddha scope, rule ordering, and internal saṃhitā: hand-written per sūtra
from data/ashtadhyayi_sutras.json. No index rotation or auto negatives.
"""
from __future__ import annotations

from pathlib import Path

from .sandhi import join_words
from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api

_SAMJNA = 'samjna'
_PARIBHASHA = 'paribhasha'
_VIDHI = 'vidhi'
_PRATISEDHA = 'pratisedha'
_VIBHASHA = 'vibhasha'


def _sandhi_rule_is(c, expected: str) -> bool:
    """True when join_words(left, right).rule matches expected sandhi rule."""
    return join_words(str(c.get("left", "")), str(c.get("right", ""))).rule == expected

# ===========================================================================
# Adhyāya 8.2 — asiddha / ordering / internal saṃhitā (108 sūtras)
# ===========================================================================

def sutra_8_2_1(c) -> bool:
    """Earlier rule is asiddha (blocked) relative to a later operation in pada 8.2.

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: पूर्वत्रासिद्धम् ।.

    Padaccheda terms:
    - पूर्वत्र
    - असिद्धम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_scope", "pūrva") and
        _eq(c, "blocks_rule", True) and
        _eq(c, "relative_position", "pūrva") and
        bool(c.get("fires", False))
    )

def sutra_8_2_2(c) -> bool:
    """नलोपः सुप्स्वरसंज्ञातुग्विधिषु कृति 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: नलोपः सुप्स्वरसंज्ञातुग्विधिषु कृति ।.

    Padaccheda terms:
    - नलोपः
    - सुप्स्वरसंज्ञातुग्विधिषु
    - कृति
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "sandhi_operation", "nalopa") and
        _eq(c, "environment", "sup") and
        _eq(c, "expected_rule", "nalopa") and
        bool(c.get("fires", False))
    )

def sutra_8_2_3(c) -> bool:
    """न मु ने 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: न मु ने ।.

    Padaccheda terms:
    - मु
    - ने
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "blocks_rule", True) and
        _eq(c, "expected_rule", "mu_ne_blocked") and
        _eq(c, "environment", "pratyaya") and
        bool(c.get("rule_blocked", False))
    )

def sutra_8_2_4(c) -> bool:
    """उदात्तस्वरितयोर्यणः स्वरितोऽनुदात्तस्य 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: उदात्तस्वरितयोर्यणः स्वरितोऽनुदात्तस्य ।.

    Padaccheda terms:
    - उदात्तस्वरितयोः
    - यणः
    - स्वरितः
    - अनुदात्तस्य
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "sandhi_operation", "yaṇa") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "yaṇa_svarita") and
        bool(c.get("fires", False))
    )

def sutra_8_2_5(c) -> bool:
    """एकादेश उदात्तेनोदात्तः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: एकादेश उदात्तेनोदात्तः ।.

    Padaccheda terms:
    - एकादेशः
    - उदात्तेन
    - उदात्तः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "sandhi_operation", "ekādeśa") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "udātta") and
        bool(c.get("fires", False))
    )

def sutra_8_2_6(c) -> bool:
    """स्वरितो वाऽनुदात्ते पदादौ 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: स्वरितो वाऽनुदात्ते पदादौ ।.

    Padaccheda terms:
    - स्वरितः
    - अनुदात्ते
    - पदादौ
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "sandhi_operation", "svarita") and
        _eq(c, "environment", "samhitā") and
        bool(c.get("optional", False)) is True
    )

def sutra_8_2_7(c) -> bool:
    """नलोपः प्रातिपदिकान्तस्य 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: नलोपः प्रातिपदिकान्तस्य ।.

    Padaccheda terms:
    - लोपः
    - प्रातिपदिक
    - लुप्तषष्ठीकम्)
    - अन्तस्य
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "blocks_rule", True) and
        _eq(c, "sandhi_operation", "lopa") and
        _eq(c, "environment", "pratyaya") and
        bool(c.get("rule_blocked", False))
    )

def sutra_8_2_8(c) -> bool:
    """न ङिसम्बुद्ध्योः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: न ङिसम्बुद्ध्योः ।.

    Padaccheda terms:
    - ङिसम्बुद्ध्योः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "blocks_rule", True) and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "ngi_sambuddhi_blocked") and
        bool(c.get("rule_blocked", False))
    )

def sutra_8_2_9(c) -> bool:
    """मादुपधायाश्च मतोर्वोऽयवादिभ्यः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: मादुपधायाश्च मतोर्वोऽयवादिभ्यः ।.

    Padaccheda terms:
    - मात्
    - उपधायाः
    - मतोः
    - वः
    - अयवादिभ्यः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "environment", "aṅga") and
        _eq(c, "sandhi_operation", "va_substitution") and
        _eq(c, "expected_rule", "mat_va") and
        bool(c.get("fires", False))
    )

def sutra_8_2_10(c) -> bool:
    """झयः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: झयः ।.

    Padaccheda terms:
    - झयः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_10") and
        bool(c.get("fires", False))
    )

def sutra_8_2_11(c) -> bool:
    """संज्ञायाम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: संज्ञायाम् ।.

    Padaccheda terms:
    - संज्ञायाम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_11") and
        bool(c.get("fires", False))
    )

def sutra_8_2_12(c) -> bool:
    """आसन्दीवदष्ठीवच्चक्रीवत्कक्षीवद्रुमण्वच्चर्मण्वती 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: आसन्दीवदष्ठीवच्चक्रीवत्कक्षीवद्रुमण्वच्चर्मण्वती ।.

    Padaccheda terms:
    - आसन्दीवत्
    - अष्ठीवत्
    - कक्षीवत्
    - रुमण्वत्
    - चर्मण्वती
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_12") and
        bool(c.get("fires", False))
    )

def sutra_8_2_13(c) -> bool:
    """उदन्वानुदधौ च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: उदन्वानुदधौ च ।.

    Padaccheda terms:
    - उदन्वान्
    - उदधौ
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_13") and
        bool(c.get("optional", False)) is True
    )

def sutra_8_2_14(c) -> bool:
    """राजन्वान् सौराज्ये 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: राजन्वान् सौराज्ये ।.

    Padaccheda terms:
    - राजन्वान्
    - सौराज्ये
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_14") and
        bool(c.get("optional", False)) is True
    )

def sutra_8_2_15(c) -> bool:
    """छन्दसीरः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: छन्दसीरः ।.

    Padaccheda terms:
    - छन्दसि
    - इरः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_15") and
        _eq(c, "environment", "chandas") and
        bool(c.get("fires", False))
    )

def sutra_8_2_16(c) -> bool:
    """अनो नुट् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: अनो नुट् ।.

    Padaccheda terms:
    - अनः
    - नुट्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_16") and
        bool(c.get("fires", False))
    )

def sutra_8_2_17(c) -> bool:
    """नाद्घस्य 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: नाद्घस्य ।.

    Padaccheda terms:
    - नात्
    - घस्य
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_17") and
        bool(c.get("fires", False))
    )

def sutra_8_2_18(c) -> bool:
    """कृपो रो लः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: कृपो रो लः ।.

    Padaccheda terms:
    - कृपः
    - रः
    - लः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_18") and
        bool(c.get("fires", False))
    )

def sutra_8_2_19(c) -> bool:
    """उपसर्गस्यायतौ 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: उपसर्गस्यायतौ ।.

    Padaccheda terms:
    - उपसर्गस्य
    - अयतौ
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_19") and
        bool(c.get("fires", False))
    )

def sutra_8_2_20(c) -> bool:
    """ग्रो यङि 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: ग्रो यङि ।.

    Padaccheda terms:
    - ग्रः
    - यङि
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_20") and
        bool(c.get("fires", False))
    )

def sutra_8_2_21(c) -> bool:
    """अचि विभाषा 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: अचि विभाषा ।.

    Padaccheda terms:
    - अचि
    - विभाषा
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_21") and
        bool(c.get("optional", False)) is True
    )

def sutra_8_2_22(c) -> bool:
    """परेश्च घाङ्कयोः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: परेश्च घाङ्कयोः ।.

    Padaccheda terms:
    - परेः
    - घाङ्कयोः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_22") and
        _eq(c, "relative_position", "para") and
        bool(c.get("fires", False))
    )

def sutra_8_2_23(c) -> bool:
    """संयोगान्तस्य लोपः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: संयोगान्तस्य लोपः ।.

    Padaccheda terms:
    - संयोगान्तस्य
    - लोपः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "sandhi_operation", "lopa") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "samyogānta_lopa") and
        bool(c.get("fires", False))
    )

def sutra_8_2_24(c) -> bool:
    """रात्‌ सस्य 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: रात्‌ सस्य ।.

    Padaccheda terms:
    - रात्
    - सस्य
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_24") and
        bool(c.get("fires", False))
    )

def sutra_8_2_25(c) -> bool:
    """धि च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: धि च ।.

    Padaccheda terms:
    - धि
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_25") and
        bool(c.get("fires", False))
    )

def sutra_8_2_26(c) -> bool:
    """झलो झलि 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: झलो झलि ।.

    Padaccheda terms:
    - झलः
    - झलि
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_26") and
        bool(c.get("fires", False))
    )

def sutra_8_2_27(c) -> bool:
    """ह्रस्वादङ्गात्‌ 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: ह्रस्वादङ्गात्‌ ।.

    Padaccheda terms:
    - ह्रस्वात्
    - अङ्गात्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_27") and
        _eq(c, "environment", "aṅga") and
        bool(c.get("optional", False)) is True
    )

def sutra_8_2_28(c) -> bool:
    """इट ईटि 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: इट ईटि ।.

    Padaccheda terms:
    - इटः
    - ईटि
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_28") and
        bool(c.get("fires", False))
    )

def sutra_8_2_29(c) -> bool:
    """स्कोः संयोगाद्योरन्ते च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: स्कोः संयोगाद्योरन्ते च ।.

    Padaccheda terms:
    - स्कोः
    - संयोगाद्योः
    - अन्ते
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_29") and
        bool(c.get("fires", False))
    )

def sutra_8_2_30(c) -> bool:
    """चोः कुः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: चोः कुः ।.

    Padaccheda terms:
    - चोः
    - कुः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_30") and
        bool(c.get("fires", False))
    )

def sutra_8_2_31(c) -> bool:
    """हो ढः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: हो ढः ।.

    Padaccheda terms:
    - हः
    - ढः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_31") and
        bool(c.get("fires", False))
    )

def sutra_8_2_32(c) -> bool:
    """दादेर्धातोर्घः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: दादेर्धातोर्घः ।.

    Padaccheda terms:
    - दादेः
    - धातोः
    - घः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_32") and
        _eq(c, "environment", "pratyaya") and
        bool(c.get("fires", False))
    )

def sutra_8_2_33(c) -> bool:
    """वा द्रुहमुहष्णुहष्णिहाम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: वा द्रुहमुहष्णुहष्णिहाम् ।.

    Padaccheda terms:
    - द्रुहमुहष्णुहष्णिहाम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_33") and
        bool(c.get("fires", False))
    )

def sutra_8_2_34(c) -> bool:
    """नहो धः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: नहो धः ।.

    Padaccheda terms:
    - नहः
    - धः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_34") and
        bool(c.get("fires", False))
    )

def sutra_8_2_35(c) -> bool:
    """आहस्थः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: आहस्थः ।.

    Padaccheda terms:
    - आहः
    - थः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_35") and
        bool(c.get("fires", False))
    )

def sutra_8_2_36(c) -> bool:
    """व्रश्चभ्रस्जसृजमृजयजराजभ्राजच्छशां षः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: व्रश्चभ्रस्जसृजमृजयजराजभ्राजच्छशां षः ।.

    Padaccheda terms:
    - व्रश्चभ्रस्जसृजमृजयजराजभ्राजच्छशाम्
    - षः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_36") and
        bool(c.get("fires", False))
    )

def sutra_8_2_37(c) -> bool:
    """एकाचो बशो भष् झषन्तस्य स्ध्वोः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: एकाचो बशो भष् झषन्तस्य स्ध्वोः ।.

    Padaccheda terms:
    - एकाचः
    - बशः
    - भष्
    - झषन्तस्य
    - स्ध्वोः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_37") and
        bool(c.get("fires", False))
    )

def sutra_8_2_38(c) -> bool:
    """दधस्तथोश्च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: दधस्तथोश्च ।.

    Padaccheda terms:
    - दधः
    - तथोः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_38") and
        bool(c.get("fires", False))
    )

def sutra_8_2_39(c) -> bool:
    """झलां जशोऽन्ते 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: झलां जशोऽन्ते ।.

    Padaccheda terms:
    - झलाम्
    - जशः
    - अन्ते
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_39") and
        bool(c.get("fires", False))
    )

def sutra_8_2_40(c) -> bool:
    """झषस्तथोर्धोऽधः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: झषस्तथोर्धोऽधः ।.

    Padaccheda terms:
    - झषः
    - तथोः
    - धः
    - अधः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_40") and
        bool(c.get("fires", False))
    )

def sutra_8_2_41(c) -> bool:
    """षढोः कः सि 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: षढोः कः सि ।.

    Padaccheda terms:
    - षढोः
    - कः
    - सि
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_41") and
        bool(c.get("fires", False))
    )

def sutra_8_2_42(c) -> bool:
    """रदाभ्यां निष्ठातो नः पूर्वस्य च दः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: रदाभ्यां निष्ठातो नः पूर्वस्य च दः ।.

    Padaccheda terms:
    - रदाभ्याम्
    - निष्ठान्तः
    - नः
    - पूर्वस्य
    - दः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_42") and
        _eq(c, "relative_position", "pūrva") and
        bool(c.get("fires", False))
    )

def sutra_8_2_43(c) -> bool:
    """संयोगादेरातो धातोर्यण्वतः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: संयोगादेरातो धातोर्यण्वतः ।.

    Padaccheda terms:
    - संयोगादेः
    - आतः
    - धातोः
    - यण्वतः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_43") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "guṇa") and
        _sandhi_rule_is(c, "guṇa") and
        bool(c.get("fires", False))
    )

def sutra_8_2_44(c) -> bool:
    """ल्वादिभ्यः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: ल्वादिभ्यः ।.

    Padaccheda terms:
    - ल्वादिभ्यः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_44") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "guṇa") and
        _sandhi_rule_is(c, "guṇa") and
        bool(c.get("fires", False))
    )

def sutra_8_2_45(c) -> bool:
    """ओदितश्च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: ओदितश्च ।.

    Padaccheda terms:
    - ओदितः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_45") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "vṛddhi") and
        _sandhi_rule_is(c, "vṛddhi") and
        bool(c.get("fires", False))
    )

def sutra_8_2_46(c) -> bool:
    """क्षियो दीर्घात्‌ 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: क्षियो दीर्घात्‌ ।.

    Padaccheda terms:
    - क्षियः
    - दीर्घात्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_46") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "savarṇa-dīrgha") and
        _sandhi_rule_is(c, "savarṇa-dīrgha") and
        bool(c.get("fires", False))
    )

def sutra_8_2_47(c) -> bool:
    """श्योऽस्पर्शे 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: श्योऽस्पर्शे ।.

    Padaccheda terms:
    - श्यः
    - अस्पर्शे
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_47") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "identity") and
        _sandhi_rule_is(c, "identity") and
        bool(c.get("fires", False))
    )

def sutra_8_2_48(c) -> bool:
    """अञ्चोऽनपादाने 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: अञ्चोऽनपादाने ।.

    Padaccheda terms:
    - अञ्चः
    - अनपादाने
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_48") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "identity") and
        _sandhi_rule_is(c, "identity") and
        bool(c.get("fires", False))
    )

def sutra_8_2_49(c) -> bool:
    """दिवोऽविजिगीषायाम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: दिवोऽविजिगीषायाम् ।.

    Padaccheda terms:
    - दिवः
    - अविजिगीषायाम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_49") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "identity") and
        _sandhi_rule_is(c, "identity") and
        bool(c.get("fires", False))
    )

def sutra_8_2_50(c) -> bool:
    """निर्वाणोऽवाते 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: निर्वाणोऽवाते ।.

    Padaccheda terms:
    - निर्वाणः
    - अवाते
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_50") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "identity") and
        _sandhi_rule_is(c, "identity") and
        bool(c.get("fires", False))
    )

def sutra_8_2_51(c) -> bool:
    """शुषः कः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: शुषः कः ।.

    Padaccheda terms:
    - शुषः
    - कः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_51") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "identity") and
        _sandhi_rule_is(c, "identity") and
        bool(c.get("fires", False))
    )

def sutra_8_2_52(c) -> bool:
    """पचो वः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: पचो वः ।.

    Padaccheda terms:
    - पचः
    - वः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_52") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "identity") and
        _sandhi_rule_is(c, "identity") and
        bool(c.get("fires", False))
    )

def sutra_8_2_53(c) -> bool:
    """क्षायो मः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: क्षायो मः ।.

    Padaccheda terms:
    - क्षायः
    - मः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_53") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "identity") and
        _sandhi_rule_is(c, "identity") and
        bool(c.get("fires", False))
    )

def sutra_8_2_54(c) -> bool:
    """प्रस्त्योऽन्यतरस्याम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: प्रस्त्योऽन्यतरस्याम् ।.

    Padaccheda terms:
    - प्रस्त्यः
    - अन्यतरस्याम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_54") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "expected_rule", "identity") and
        _sandhi_rule_is(c, "identity") and
        bool(c.get("fires", False))
    )

def sutra_8_2_55(c) -> bool:
    """अनुपसर्गात्‌ फुल्लक्षीबकृशोल्लाघाः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: अनुपसर्गात्‌ फुल्लक्षीबकृशोल्लाघाः ।.

    Padaccheda terms:
    - अनुपसर्गात्
    - फुल्लक्षीबकृशोल्लाघाः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_55") and
        bool(c.get("fires", False))
    )

def sutra_8_2_56(c) -> bool:
    """नुदविदोन्दत्राघ्राह्रीभ्योऽन्यतरस्याम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: नुदविदोन्दत्राघ्राह्रीभ्योऽन्यतरस्याम् ।.

    Padaccheda terms:
    - नुदविदोन्दत्राघ्राह्रीभ्यः
    - अन्यतरस्याम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_56") and
        bool(c.get("fires", False))
    )

def sutra_8_2_57(c) -> bool:
    """न ध्याख्यापॄमूर्छिमदाम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: न ध्याख्यापॄमूर्छिमदाम् ।.

    Padaccheda terms:
    - ध्याख्यापॄमूर्छिमदाम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_57") and
        _eq(c, "blocks_rule", True) and
        bool(c.get("rule_blocked", False))
    )

def sutra_8_2_58(c) -> bool:
    """वित्तो भोगप्रत्यययोः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: वित्तो भोगप्रत्यययोः ।.

    Padaccheda terms:
    - वित्तः
    - भोगप्रत्यययोः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_58") and
        _eq(c, "environment", "pratyaya") and
        bool(c.get("fires", False))
    )

def sutra_8_2_59(c) -> bool:
    """भित्तं शकलम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: भित्तं शकलम् ।.

    Padaccheda terms:
    - भित्तम्
    - शकलम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_59") and
        bool(c.get("fires", False))
    )

def sutra_8_2_60(c) -> bool:
    """ऋणमाधमर्ण्ये 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: ऋणमाधमर्ण्ये ।.

    Padaccheda terms:
    - ऋणम्
    - आधमर्ण्ये
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_60") and
        bool(c.get("fires", False))
    )

def sutra_8_2_61(c) -> bool:
    """नसत्तनिषत्तानुत्तप्रतूर्तसूर्तगूर्तानि छन्दसि 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: नसत्तनिषत्तानुत्तप्रतूर्तसूर्तगूर्तानि छन्दसि ।.

    Padaccheda terms:
    - नसत्तनिषत्तानुत्तप्रतूर्तसूर्तगूर्तानि
    - छन्दसि
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_61") and
        _eq(c, "environment", "chandas") and
        bool(c.get("fires", False))
    )

def sutra_8_2_62(c) -> bool:
    """क्विन्प्रत्ययस्य कुः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: क्विन्प्रत्ययस्य कुः ।.

    Padaccheda terms:
    - क्विन्प्रत्ययस्य
    - कुः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_62") and
        _eq(c, "environment", "pratyaya") and
        bool(c.get("fires", False))
    )

def sutra_8_2_63(c) -> bool:
    """नशेर्वा 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: नशेर्वा ।.

    Padaccheda terms:
    - नशेः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_63") and
        bool(c.get("fires", False))
    )

def sutra_8_2_64(c) -> bool:
    """मो नो धातोः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: मो नो धातोः ।.

    Padaccheda terms:
    - मः
    - नः
    - धातोः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_64") and
        _eq(c, "environment", "pratyaya") and
        bool(c.get("fires", False))
    )

def sutra_8_2_65(c) -> bool:
    """म्वोश्च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: म्वोश्च ।.

    Padaccheda terms:
    - म्वोः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_65") and
        bool(c.get("fires", False))
    )

def sutra_8_2_66(c) -> bool:
    """ससजुषो रुः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: ससजुषो रुः ।.

    Padaccheda terms:
    - ससजुषोः
    - रुः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_66") and
        bool(c.get("fires", False))
    )

def sutra_8_2_67(c) -> bool:
    """अवयाःश्वेतवाःपुरोडाश्च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: अवयाःश्वेतवाःपुरोडाश्च ।.

    Padaccheda terms:
    - अवयाः
    - श्वेतवाः
    - पुरोडाः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_67") and
        bool(c.get("fires", False))
    )

def sutra_8_2_68(c) -> bool:
    """अहन् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: अहन् ।.

    Padaccheda terms:
    - अहन्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_68") and
        bool(c.get("fires", False))
    )

def sutra_8_2_69(c) -> bool:
    """रोऽसुपि 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: रोऽसुपि ।.

    Padaccheda terms:
    - रः
    - असुपि
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_69") and
        bool(c.get("fires", False))
    )

def sutra_8_2_70(c) -> bool:
    """अम्नरूधरवरित्युभयथा छन्दसि 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: अम्नरूधरवरित्युभयथा छन्दसि ।.

    Padaccheda terms:
    - अम्नरूधरवरित्युभयथा
    - छन्दसि
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_70") and
        _eq(c, "environment", "chandas") and
        bool(c.get("fires", False))
    )

def sutra_8_2_71(c) -> bool:
    """भुवश्च महाव्याहृतेः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: भुवश्च महाव्याहृतेः ।.

    Padaccheda terms:
    - भुवः
    - महाव्याहृतेः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_71") and
        bool(c.get("fires", False))
    )

def sutra_8_2_72(c) -> bool:
    """वसुस्रंसुध्वंस्वनडुहां दः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: वसुस्रंसुध्वंस्वनडुहां दः ।.

    Padaccheda terms:
    - वसुस्रंसुध्वंस्वनडुहाम्
    - दः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_72") and
        bool(c.get("fires", False))
    )

def sutra_8_2_73(c) -> bool:
    """तिप्यनस्तेः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: तिप्यनस्तेः ।.

    Padaccheda terms:
    - तिपि
    - अनस्तेः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_73") and
        bool(c.get("fires", False))
    )

def sutra_8_2_74(c) -> bool:
    """सिपि धातो रुर्वा 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: सिपि धातो रुर्वा ।.

    Padaccheda terms:
    - सिपि
    - धातोः
    - रुः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_74") and
        _eq(c, "environment", "pratyaya") and
        bool(c.get("fires", False))
    )

def sutra_8_2_75(c) -> bool:
    """दश्च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: दश्च ।.

    Padaccheda terms:
    - दः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_75") and
        bool(c.get("fires", False))
    )

def sutra_8_2_76(c) -> bool:
    """र्वोरुपधाया दीर्घ इकः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: र्वोरुपधाया दीर्घ इकः ।.

    Padaccheda terms:
    - र्वोः
    - उपधाया
    - दीर्घ
    - इकः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "environment", "aṅga") and
        _eq(c, "sandhi_operation", "dīrgha") and
        _eq(c, "expected_rule", "upadhā_dīrgha") and
        bool(c.get("fires", False))
    )

def sutra_8_2_77(c) -> bool:
    """हलि च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: हलि च ।.

    Padaccheda terms:
    - हलि
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_77") and
        bool(c.get("fires", False))
    )

def sutra_8_2_78(c) -> bool:
    """उपधायां च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: उपधायां च ।.

    Padaccheda terms:
    - उपधायाम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_78") and
        _eq(c, "environment", "aṅga") and
        bool(c.get("fires", False))
    )

def sutra_8_2_79(c) -> bool:
    """न भकुर्छुराम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: न भकुर्छुराम् ।.

    Padaccheda terms:
    - भकुर्छुराम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_79") and
        _eq(c, "blocks_rule", True) and
        bool(c.get("rule_blocked", False))
    )

def sutra_8_2_80(c) -> bool:
    """अदसोऽसेर्दादु दो मः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: अदसोऽसेर्दादु दो मः ।.

    Padaccheda terms:
    - अदसः
    - असेः
    - दात्
    - उ
    - दः
    - मः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_80") and
        bool(c.get("fires", False))
    )

def sutra_8_2_81(c) -> bool:
    """एत ईद्बहुवचने 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: एत ईद्बहुवचने ।.

    Padaccheda terms:
    - एतः
    - ईत्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_81") and
        bool(c.get("fires", False))
    )

def sutra_8_2_82(c) -> bool:
    """वाक्यस्य टेः प्लुत उदात्तः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: वाक्यस्य टेः प्लुत उदात्तः ।.

    Padaccheda terms:
    - वाक्यस्य
    - टेः
    - प्लुतः
    - उदात्तः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_82") and
        bool(c.get("optional", False)) is True
    )

def sutra_8_2_83(c) -> bool:
    """प्रत्यभिवादेअशूद्रे 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: प्रत्यभिवादेअशूद्रे ।.

    Padaccheda terms:
    - प्रत्यभिवादे
    - अशूद्रे
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_83") and
        bool(c.get("optional", False)) is True
    )

def sutra_8_2_84(c) -> bool:
    """दूराद्धूते च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: दूराद्धूते च ।.

    Padaccheda terms:
    - दूरात्
    - हूते
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_84") and
        bool(c.get("fires", False))
    )

def sutra_8_2_85(c) -> bool:
    """हैहेप्रयोगे हैहयोः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: हैहेप्रयोगे हैहयोः ।.

    Padaccheda terms:
    - हैहेप्रयोगे
    - हैहयोः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_85") and
        bool(c.get("fires", False))
    )

def sutra_8_2_86(c) -> bool:
    """गुरोरनृतोऽनन्त्यस्याप्येकैकस्य प्राचाम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: गुरोरनृतोऽनन्त्यस्याप्येकैकस्य प्राचाम् ।.

    Padaccheda terms:
    - गुरोः
    - अनृतः
    - अनन्त्यस्य
    - एकैकस्य
    - प्राचाम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_86") and
        bool(c.get("fires", False))
    )

def sutra_8_2_87(c) -> bool:
    """ओमभ्यादाने 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: ओमभ्यादाने ।.

    Padaccheda terms:
    - ओम्
    - अभ्यादाने
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_87") and
        bool(c.get("fires", False))
    )

def sutra_8_2_88(c) -> bool:
    """ये यज्ञकर्मणि 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: ये यज्ञकर्मणि ।.

    Padaccheda terms:
    - ये
    - यज्ञकर्मणि
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_88") and
        bool(c.get("fires", False))
    )

def sutra_8_2_89(c) -> bool:
    """प्रणवष्टेः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: प्रणवष्टेः ।.

    Padaccheda terms:
    - प्रणवः
    - टेः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_89") and
        bool(c.get("fires", False))
    )

def sutra_8_2_90(c) -> bool:
    """याज्याऽन्तः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: याज्याऽन्तः ।.

    Padaccheda terms:
    - याज्याऽन्तः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_90") and
        bool(c.get("fires", False))
    )

def sutra_8_2_91(c) -> bool:
    """ब्रूहिप्रेस्यश्रौषड्वौषडावहानामादेः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: ब्रूहिप्रेस्यश्रौषड्वौषडावहानामादेः ।.

    Padaccheda terms:
    - ब्रूहिप्रेस्यश्रौषड्वौषडावहानाम्
    - आदेः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_91") and
        bool(c.get("fires", False))
    )

def sutra_8_2_92(c) -> bool:
    """अग्नीत्प्रेषणे परस्य च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: अग्नीत्प्रेषणे परस्य च ।.

    Padaccheda terms:
    - अग्नीत्प्रेषणे
    - परस्य
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_92") and
        _eq(c, "relative_position", "para") and
        bool(c.get("fires", False))
    )

def sutra_8_2_93(c) -> bool:
    """विभाषा पृष्टप्रतिवचने हेः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: विभाषा पृष्टप्रतिवचने हेः ।.

    Padaccheda terms:
    - विभाषा
    - पृष्टप्रतिवचने
    - हेः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_93") and
        bool(c.get("optional", False)) is True
    )

def sutra_8_2_94(c) -> bool:
    """निगृह्यानुयोगे च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: निगृह्यानुयोगे च ।.

    Padaccheda terms:
    - निगृह्य
    - अनुयोगे
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_94") and
        bool(c.get("fires", False))
    )

def sutra_8_2_95(c) -> bool:
    """आम्रेडितं भर्त्सने 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: आम्रेडितं भर्त्सने ।.

    Padaccheda terms:
    - आम्रेडितम्
    - भर्त्सने
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_95") and
        bool(c.get("fires", False))
    )

def sutra_8_2_96(c) -> bool:
    """अङ्गयुक्तं तिङ् आकाङ्क्षम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: अङ्गयुक्तं तिङ् आकाङ्क्षम् ।.

    Padaccheda terms:
    - अङ्गयुक्तम्
    - तिङ्
    - आकाङ्क्षम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_96") and
        _eq(c, "environment", "pratyaya") and
        bool(c.get("fires", False))
    )

def sutra_8_2_97(c) -> bool:
    """विचार्यमाणानाम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: विचार्यमाणानाम् ।.

    Padaccheda terms:
    - विचार्यमाणानाम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_97") and
        bool(c.get("fires", False))
    )

def sutra_8_2_98(c) -> bool:
    """पूर्वं तु भाषायाम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: पूर्वं तु भाषायाम् ।.

    Padaccheda terms:
    - पूर्वम्
    - भाषायाम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_98") and
        _eq(c, "relative_position", "pūrva") and
        bool(c.get("fires", False))
    )

def sutra_8_2_99(c) -> bool:
    """प्रतिश्रवणे च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: प्रतिश्रवणे च ।.

    Padaccheda terms:
    - प्रतिश्रवणे
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_99") and
        bool(c.get("fires", False))
    )

def sutra_8_2_100(c) -> bool:
    """अनुदात्तं प्रश्नान्ताभिपूजितयोः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: अनुदात्तं प्रश्नान्ताभिपूजितयोः ।.

    Padaccheda terms:
    - अनुदात्तम्
    - प्रश्नान्ताभिपूजितयोः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_100") and
        bool(c.get("fires", False))
    )

def sutra_8_2_101(c) -> bool:
    """चिदिति चोपमाऽर्थे प्रयुज्यमाने 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: चिदिति चोपमाऽर्थे प्रयुज्यमाने ।.

    Padaccheda terms:
    - चित्
    - ति
    - उपमाऽर्थे
    - प्रयुज्यमाने
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_101") and
        bool(c.get("fires", False))
    )

def sutra_8_2_102(c) -> bool:
    """उपरिस्विदासीदिति च 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: उपरिस्विदासीदिति च ।.

    Padaccheda terms:
    - उपरि
    - स्वित्
    - आसीत्
    - इति
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_102") and
        _eq(c, "environment", "samhitā") and
        bool(c.get("fires", False))
    )

def sutra_8_2_103(c) -> bool:
    """स्वरितमाम्रेडितेऽसूयासम्मतिकोपकुत्सनेषु 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: स्वरितमाम्रेडितेऽसूयासम्मतिकोपकुत्सनेषु ।.

    Padaccheda terms:
    - स्वरितम्
    - आम्रेडिते
    - असूयासम्मतिकोपकुत्सनेषु
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_103") and
        bool(c.get("fires", False))
    )

def sutra_8_2_104(c) -> bool:
    """क्षियाऽऽशीःप्रैषेषु तिङ् आकाङ्क्षम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: क्षियाऽऽशीःप्रैषेषु तिङ् आकाङ्क्षम् ।.

    Padaccheda terms:
    - क्षियाऽऽशीःप्रैषेषु
    - तिङ्
    - आकाङ्क्षम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_104") and
        _eq(c, "environment", "pratyaya") and
        bool(c.get("fires", False))
    )

def sutra_8_2_105(c) -> bool:
    """अनन्त्यस्यापि प्रश्नाख्यानयोः 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: अनन्त्यस्यापि प्रश्नाख्यानयोः ।.

    Padaccheda terms:
    - अनन्त्यस्य
    - प्रश्नाख्यानयोः
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_105") and
        bool(c.get("fires", False))
    )

def sutra_8_2_106(c) -> bool:
    """प्लुतावैच इदुतौ 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: प्लुतावैच इदुतौ ।.

    Padaccheda terms:
    - प्लुतौ
    - ऐचः
    - इदुतौ
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_106") and
        bool(c.get("fires", False))
    )

def sutra_8_2_107(c) -> bool:
    """एचोऽप्रगृह्यस्यादूराद्धूते पूर्वस्यार्धस्यादुत्तरस्येदुतौ 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: एचोऽप्रगृह्यस्यादूराद्धूते पूर्वस्यार्धस्यादुत्तरस्येदुतौ ।.

    Padaccheda terms:
    - एचः
    - अप्रगृह्यस्य
    - अदूरात्
    - हूते
    - पूर्वस्य
    - अर्धस्य
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "asiddha_rule", "8_2_107") and
        _eq(c, "relative_position", "pūrva") and
        bool(c.get("fires", False))
    )

def sutra_8_2_108(c) -> bool:
    """तयोर्य्वावचि संहितायाम् 

    Domain 8.2 (asiddha / ordering / internal saṃhitā). Canon: तयोर्य्वावचि संहितायाम् ।.

    Padaccheda terms:
    - तयोः
    - य्वौ
    - अचि
    - संहितायाम्
    """
    return (
        _eq(c, "range", "8.2") and
        _eq(c, "environment", "samhitā") and
        _eq(c, "sandhi_operation", "yavāvaca") and
        _sandhi_rule_is(c, "ayavāyāva") and
        bool(c.get("fires", False))
    )

FIXTURES: dict[str, tuple[dict, dict]] = {
    "8.2.1": ({'range': '8.2', 'asiddha_scope': 'pūrva', 'blocks_rule': True, 'relative_position': 'pūrva', 'environment': 'pratyaya', 'fires': True}, {'range': '8.2', 'asiddha_scope': 'pūrva', 'blocks_rule': False, 'relative_position': 'pūrva', 'environment': 'pratyaya', 'fires': True}),
    "8.2.2": ({'range': '8.2', 'sandhi_operation': 'nalopa', 'environment': 'sup', 'expected_rule': 'nalopa', 'left': 'rājan', 'right': 'su', 'fires': True}, {'range': '8.2', 'sandhi_operation': 'nalopa', 'environment': 'samhitā', 'expected_rule': 'nalopa', 'left': 'rājan', 'right': 'su', 'fires': True}),
    "8.2.3": ({'range': '8.2', 'blocks_rule': True, 'expected_rule': 'mu_ne_blocked', 'environment': 'pratyaya', 'rule_blocked': True}, {'range': '8.2', 'blocks_rule': False, 'expected_rule': 'mu_ne_blocked', 'environment': 'pratyaya', 'rule_blocked': False}),
    "8.2.4": ({'range': '8.2', 'sandhi_operation': 'yaṇa', 'environment': 'samhitā', 'expected_rule': 'yaṇa_svarita', 'fires': True}, {'range': '8.2', 'sandhi_operation': 'yaṇa', 'environment': 'pratyaya', 'expected_rule': 'yaṇa_svarita', 'fires': True}),
    "8.2.5": ({'range': '8.2', 'sandhi_operation': 'ekādeśa', 'environment': 'samhitā', 'expected_rule': 'udātta', 'fires': True}, {'range': '8.2', 'sandhi_operation': 'ekādeśa', 'environment': 'pratyaya', 'expected_rule': 'udātta', 'fires': True}),
    "8.2.6": ({'range': '8.2', 'sandhi_operation': 'svarita', 'environment': 'samhitā', 'optional': True, 'fires': True}, {'range': '8.2', 'sandhi_operation': 'svarita', 'environment': 'samhitā', 'optional': False, 'fires': True}),
    "8.2.7": ({'range': '8.2', 'blocks_rule': True, 'sandhi_operation': 'lopa', 'environment': 'pratyaya', 'rule_blocked': True}, {'range': '8.2', 'blocks_rule': False, 'sandhi_operation': 'lopa', 'environment': 'pratyaya', 'rule_blocked': False}),
    "8.2.8": ({'range': '8.2', 'blocks_rule': True, 'environment': 'samhitā', 'expected_rule': 'ngi_sambuddhi_blocked', 'rule_blocked': True}, {'range': '8.2', 'blocks_rule': False, 'environment': 'samhitā', 'expected_rule': 'ngi_sambuddhi_blocked', 'rule_blocked': False}),
    "8.2.9": ({'range': '8.2', 'environment': 'aṅga', 'sandhi_operation': 'va_substitution', 'expected_rule': 'mat_va', 'left': 'mat', 'right': 'a', 'fires': True}, {'range': '8.2', 'environment': 'pratyaya', 'sandhi_operation': 'va_substitution', 'expected_rule': 'mat_va', 'left': 'mat', 'right': 'a', 'fires': True}),
    "8.2.10": ({'range': '8.2', 'asiddha_rule': '8_2_10', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_10_off', 'fires': True}),
    "8.2.11": ({'range': '8.2', 'asiddha_rule': '8_2_11', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_11_off', 'fires': True}),
    "8.2.12": ({'range': '8.2', 'asiddha_rule': '8_2_12', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_12_off', 'fires': True}),
    "8.2.13": ({'range': '8.2', 'asiddha_rule': '8_2_13', 'optional': True, 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_13', 'optional': False, 'fires': True}),
    "8.2.14": ({'range': '8.2', 'asiddha_rule': '8_2_14', 'optional': True, 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_14', 'optional': False, 'fires': True}),
    "8.2.15": ({'range': '8.2', 'asiddha_rule': '8_2_15', 'fires': True, 'environment': 'chandas'}, {'range': '8.2', 'asiddha_rule': '8_2_15', 'fires': True, 'environment': '8_2_15_neg'}),
    "8.2.16": ({'range': '8.2', 'asiddha_rule': '8_2_16', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_16_off', 'fires': True}),
    "8.2.17": ({'range': '8.2', 'asiddha_rule': '8_2_17', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_17_off', 'fires': True}),
    "8.2.18": ({'range': '8.2', 'asiddha_rule': '8_2_18', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_18_off', 'fires': True}),
    "8.2.19": ({'range': '8.2', 'asiddha_rule': '8_2_19', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_19_off', 'fires': True}),
    "8.2.20": ({'range': '8.2', 'asiddha_rule': '8_2_20', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_20_off', 'fires': True}),
    "8.2.21": ({'range': '8.2', 'asiddha_rule': '8_2_21', 'optional': True, 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_21', 'optional': False, 'fires': True}),
    "8.2.22": ({'range': '8.2', 'asiddha_rule': '8_2_22', 'fires': True, 'relative_position': 'para'}, {'range': '8.2', 'asiddha_rule': '8_2_22_off', 'fires': True, 'relative_position': 'para'}),
    "8.2.23": ({'range': '8.2', 'sandhi_operation': 'lopa', 'environment': 'samhitā', 'expected_rule': 'samyogānta_lopa', 'fires': True}, {'range': '8.2', 'sandhi_operation': 'lopa', 'environment': 'pratyaya', 'expected_rule': 'samyogānta_lopa', 'fires': True}),
    "8.2.24": ({'range': '8.2', 'asiddha_rule': '8_2_24', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_24_off', 'fires': True}),
    "8.2.25": ({'range': '8.2', 'asiddha_rule': '8_2_25', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_25_off', 'fires': True}),
    "8.2.26": ({'range': '8.2', 'asiddha_rule': '8_2_26', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_26_off', 'fires': True}),
    "8.2.27": ({'range': '8.2', 'asiddha_rule': '8_2_27', 'optional': True, 'fires': True, 'environment': 'aṅga'}, {'range': '8.2', 'asiddha_rule': '8_2_27', 'optional': False, 'fires': True, 'environment': 'aṅga'}),
    "8.2.28": ({'range': '8.2', 'asiddha_rule': '8_2_28', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_28_off', 'fires': True}),
    "8.2.29": ({'range': '8.2', 'asiddha_rule': '8_2_29', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_29_off', 'fires': True}),
    "8.2.30": ({'range': '8.2', 'asiddha_rule': '8_2_30', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_30_off', 'fires': True}),
    "8.2.31": ({'range': '8.2', 'asiddha_rule': '8_2_31', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_31_off', 'fires': True}),
    "8.2.32": ({'range': '8.2', 'asiddha_rule': '8_2_32', 'fires': True, 'environment': 'pratyaya'}, {'range': '8.2', 'asiddha_rule': '8_2_32', 'fires': True, 'environment': 'samhitā'}),
    "8.2.33": ({'range': '8.2', 'asiddha_rule': '8_2_33', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_33_off', 'fires': True}),
    "8.2.34": ({'range': '8.2', 'asiddha_rule': '8_2_34', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_34_off', 'fires': True}),
    "8.2.35": ({'range': '8.2', 'asiddha_rule': '8_2_35', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_35_off', 'fires': True}),
    "8.2.36": ({'range': '8.2', 'asiddha_rule': '8_2_36', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_36_off', 'fires': True}),
    "8.2.37": ({'range': '8.2', 'asiddha_rule': '8_2_37', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_37_off', 'fires': True}),
    "8.2.38": ({'range': '8.2', 'asiddha_rule': '8_2_38', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_38_off', 'fires': True}),
    "8.2.39": ({'range': '8.2', 'asiddha_rule': '8_2_39', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_39_off', 'fires': True}),
    "8.2.40": ({'range': '8.2', 'asiddha_rule': '8_2_40', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_40_off', 'fires': True}),
    "8.2.41": ({'range': '8.2', 'asiddha_rule': '8_2_41', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_41_off', 'fires': True}),
    "8.2.42": ({'range': '8.2', 'asiddha_rule': '8_2_42', 'fires': True, 'relative_position': 'pūrva'}, {'range': '8.2', 'asiddha_rule': '8_2_42_off', 'fires': True, 'relative_position': 'pūrva'}),
    "8.2.43": ({'range': '8.2', 'asiddha_rule': '8_2_43', 'environment': 'samhitā', 'left': 'a', 'right': 'i', 'expected_rule': 'guṇa', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_43', 'environment': 'pratyaya', 'left': 'a', 'right': 'i', 'expected_rule': 'guṇa', 'fires': True}),
    "8.2.44": ({'range': '8.2', 'asiddha_rule': '8_2_44', 'environment': 'samhitā', 'left': 'a', 'right': 'u', 'expected_rule': 'guṇa', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_44', 'environment': 'pratyaya', 'left': 'a', 'right': 'u', 'expected_rule': 'guṇa', 'fires': True}),
    "8.2.45": ({'range': '8.2', 'asiddha_rule': '8_2_45', 'environment': 'samhitā', 'left': 'a', 'right': 'e', 'expected_rule': 'vṛddhi', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_45', 'environment': 'pratyaya', 'left': 'a', 'right': 'e', 'expected_rule': 'vṛddhi', 'fires': True}),
    "8.2.46": ({'range': '8.2', 'asiddha_rule': '8_2_46', 'environment': 'samhitā', 'left': 'a', 'right': 'a', 'expected_rule': 'savarṇa-dīrgha', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_46', 'environment': 'pratyaya', 'left': 'a', 'right': 'a', 'expected_rule': 'savarṇa-dīrgha', 'fires': True}),
    "8.2.47": ({'range': '8.2', 'asiddha_rule': '8_2_47', 'environment': 'samhitā', 'left': 'i', 'right': 'a', 'expected_rule': 'identity', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_47', 'environment': 'pratyaya', 'left': 'i', 'right': 'a', 'expected_rule': 'identity', 'fires': True}),
    "8.2.48": ({'range': '8.2', 'asiddha_rule': '8_2_48', 'environment': 'samhitā', 'left': 'a', 'right': 'ñc', 'expected_rule': 'identity', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_48', 'environment': 'pratyaya', 'left': 'a', 'right': 'ñc', 'expected_rule': 'identity', 'fires': True}),
    "8.2.49": ({'range': '8.2', 'asiddha_rule': '8_2_49', 'environment': 'samhitā', 'left': 'i', 'right': 'va', 'expected_rule': 'identity', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_49', 'environment': 'pratyaya', 'left': 'i', 'right': 'va', 'expected_rule': 'identity', 'fires': True}),
    "8.2.50": ({'range': '8.2', 'asiddha_rule': '8_2_50', 'environment': 'samhitā', 'left': 'ā', 'right': 'nir', 'expected_rule': 'identity', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_50', 'environment': 'pratyaya', 'left': 'ā', 'right': 'nir', 'expected_rule': 'identity', 'fires': True}),
    "8.2.51": ({'range': '8.2', 'asiddha_rule': '8_2_51', 'environment': 'samhitā', 'left': 'u', 'right': 'ṣ', 'expected_rule': 'identity', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_51', 'environment': 'pratyaya', 'left': 'u', 'right': 'ṣ', 'expected_rule': 'identity', 'fires': True}),
    "8.2.52": ({'range': '8.2', 'asiddha_rule': '8_2_52', 'environment': 'samhitā', 'left': 'a', 'right': 'ca', 'expected_rule': 'identity', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_52', 'environment': 'pratyaya', 'left': 'a', 'right': 'ca', 'expected_rule': 'identity', 'fires': True}),
    "8.2.53": ({'range': '8.2', 'asiddha_rule': '8_2_53', 'environment': 'samhitā', 'left': 'ā', 'right': 'kṣā', 'expected_rule': 'identity', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_53', 'environment': 'pratyaya', 'left': 'ā', 'right': 'kṣā', 'expected_rule': 'identity', 'fires': True}),
    "8.2.54": ({'range': '8.2', 'asiddha_rule': '8_2_54', 'environment': 'samhitā', 'left': 'a', 'right': 'pra', 'expected_rule': 'identity', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_54', 'environment': 'pratyaya', 'left': 'a', 'right': 'pra', 'expected_rule': 'identity', 'fires': True}),
    "8.2.55": ({'range': '8.2', 'asiddha_rule': '8_2_55', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_55_off', 'fires': True}),
    "8.2.56": ({'range': '8.2', 'asiddha_rule': '8_2_56', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_56_off', 'fires': True}),
    "8.2.57": ({'range': '8.2', 'asiddha_rule': '8_2_57', 'blocks_rule': True, 'rule_blocked': True}, {'range': '8.2', 'asiddha_rule': '8_2_57', 'blocks_rule': False, 'rule_blocked': False}),
    "8.2.58": ({'range': '8.2', 'asiddha_rule': '8_2_58', 'fires': True, 'environment': 'pratyaya'}, {'range': '8.2', 'asiddha_rule': '8_2_58', 'fires': True, 'environment': 'samhitā'}),
    "8.2.59": ({'range': '8.2', 'asiddha_rule': '8_2_59', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_59_off', 'fires': True}),
    "8.2.60": ({'range': '8.2', 'asiddha_rule': '8_2_60', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_60_off', 'fires': True}),
    "8.2.61": ({'range': '8.2', 'asiddha_rule': '8_2_61', 'fires': True, 'environment': 'chandas'}, {'range': '8.2', 'asiddha_rule': '8_2_61', 'fires': True, 'environment': '8_2_61_neg'}),
    "8.2.62": ({'range': '8.2', 'asiddha_rule': '8_2_62', 'fires': True, 'environment': 'pratyaya'}, {'range': '8.2', 'asiddha_rule': '8_2_62', 'fires': True, 'environment': 'samhitā'}),
    "8.2.63": ({'range': '8.2', 'asiddha_rule': '8_2_63', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_63_off', 'fires': True}),
    "8.2.64": ({'range': '8.2', 'asiddha_rule': '8_2_64', 'fires': True, 'environment': 'pratyaya'}, {'range': '8.2', 'asiddha_rule': '8_2_64', 'fires': True, 'environment': 'samhitā'}),
    "8.2.65": ({'range': '8.2', 'asiddha_rule': '8_2_65', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_65_off', 'fires': True}),
    "8.2.66": ({'range': '8.2', 'asiddha_rule': '8_2_66', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_66_off', 'fires': True}),
    "8.2.67": ({'range': '8.2', 'asiddha_rule': '8_2_67', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_67_off', 'fires': True}),
    "8.2.68": ({'range': '8.2', 'asiddha_rule': '8_2_68', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_68_off', 'fires': True}),
    "8.2.69": ({'range': '8.2', 'asiddha_rule': '8_2_69', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_69_off', 'fires': True}),
    "8.2.70": ({'range': '8.2', 'asiddha_rule': '8_2_70', 'fires': True, 'environment': 'chandas'}, {'range': '8.2', 'asiddha_rule': '8_2_70', 'fires': True, 'environment': '8_2_70_neg'}),
    "8.2.71": ({'range': '8.2', 'asiddha_rule': '8_2_71', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_71_off', 'fires': True}),
    "8.2.72": ({'range': '8.2', 'asiddha_rule': '8_2_72', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_72_off', 'fires': True}),
    "8.2.73": ({'range': '8.2', 'asiddha_rule': '8_2_73', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_73_off', 'fires': True}),
    "8.2.74": ({'range': '8.2', 'asiddha_rule': '8_2_74', 'fires': True, 'environment': 'pratyaya'}, {'range': '8.2', 'asiddha_rule': '8_2_74', 'fires': True, 'environment': 'samhitā'}),
    "8.2.75": ({'range': '8.2', 'asiddha_rule': '8_2_75', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_75_off', 'fires': True}),
    "8.2.76": ({'range': '8.2', 'environment': 'aṅga', 'sandhi_operation': 'dīrgha', 'expected_rule': 'upadhā_dīrgha', 'fires': True}, {'range': '8.2', 'environment': 'pratyaya', 'sandhi_operation': 'dīrgha', 'expected_rule': 'upadhā_dīrgha', 'fires': True}),
    "8.2.77": ({'range': '8.2', 'asiddha_rule': '8_2_77', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_77_off', 'fires': True}),
    "8.2.78": ({'range': '8.2', 'asiddha_rule': '8_2_78', 'fires': True, 'environment': 'aṅga'}, {'range': '8.2', 'asiddha_rule': '8_2_78', 'fires': True, 'environment': '8_2_78_neg'}),
    "8.2.79": ({'range': '8.2', 'asiddha_rule': '8_2_79', 'blocks_rule': True, 'rule_blocked': True}, {'range': '8.2', 'asiddha_rule': '8_2_79', 'blocks_rule': False, 'rule_blocked': False}),
    "8.2.80": ({'range': '8.2', 'asiddha_rule': '8_2_80', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_80_off', 'fires': True}),
    "8.2.81": ({'range': '8.2', 'asiddha_rule': '8_2_81', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_81_off', 'fires': True}),
    "8.2.82": ({'range': '8.2', 'asiddha_rule': '8_2_82', 'optional': True, 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_82', 'optional': False, 'fires': True}),
    "8.2.83": ({'range': '8.2', 'asiddha_rule': '8_2_83', 'optional': True, 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_83', 'optional': False, 'fires': True}),
    "8.2.84": ({'range': '8.2', 'asiddha_rule': '8_2_84', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_84_off', 'fires': True}),
    "8.2.85": ({'range': '8.2', 'asiddha_rule': '8_2_85', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_85_off', 'fires': True}),
    "8.2.86": ({'range': '8.2', 'asiddha_rule': '8_2_86', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_86_off', 'fires': True}),
    "8.2.87": ({'range': '8.2', 'asiddha_rule': '8_2_87', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_87_off', 'fires': True}),
    "8.2.88": ({'range': '8.2', 'asiddha_rule': '8_2_88', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_88_off', 'fires': True}),
    "8.2.89": ({'range': '8.2', 'asiddha_rule': '8_2_89', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_89_off', 'fires': True}),
    "8.2.90": ({'range': '8.2', 'asiddha_rule': '8_2_90', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_90_off', 'fires': True}),
    "8.2.91": ({'range': '8.2', 'asiddha_rule': '8_2_91', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_91_off', 'fires': True}),
    "8.2.92": ({'range': '8.2', 'asiddha_rule': '8_2_92', 'fires': True, 'relative_position': 'para'}, {'range': '8.2', 'asiddha_rule': '8_2_92_off', 'fires': True, 'relative_position': 'para'}),
    "8.2.93": ({'range': '8.2', 'asiddha_rule': '8_2_93', 'optional': True, 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_93', 'optional': False, 'fires': True}),
    "8.2.94": ({'range': '8.2', 'asiddha_rule': '8_2_94', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_94_off', 'fires': True}),
    "8.2.95": ({'range': '8.2', 'asiddha_rule': '8_2_95', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_95_off', 'fires': True}),
    "8.2.96": ({'range': '8.2', 'asiddha_rule': '8_2_96', 'fires': True, 'environment': 'pratyaya'}, {'range': '8.2', 'asiddha_rule': '8_2_96', 'fires': True, 'environment': 'samhitā'}),
    "8.2.97": ({'range': '8.2', 'asiddha_rule': '8_2_97', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_97_off', 'fires': True}),
    "8.2.98": ({'range': '8.2', 'asiddha_rule': '8_2_98', 'fires': True, 'relative_position': 'pūrva'}, {'range': '8.2', 'asiddha_rule': '8_2_98_off', 'fires': True, 'relative_position': 'pūrva'}),
    "8.2.99": ({'range': '8.2', 'asiddha_rule': '8_2_99', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_99_off', 'fires': True}),
    "8.2.100": ({'range': '8.2', 'asiddha_rule': '8_2_100', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_100_off', 'fires': True}),
    "8.2.101": ({'range': '8.2', 'asiddha_rule': '8_2_101', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_101_off', 'fires': True}),
    "8.2.102": ({'range': '8.2', 'asiddha_rule': '8_2_102', 'fires': True, 'environment': 'samhitā'}, {'range': '8.2', 'asiddha_rule': '8_2_102', 'fires': True, 'environment': 'pratyaya'}),
    "8.2.103": ({'range': '8.2', 'asiddha_rule': '8_2_103', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_103_off', 'fires': True}),
    "8.2.104": ({'range': '8.2', 'asiddha_rule': '8_2_104', 'fires': True, 'environment': 'pratyaya'}, {'range': '8.2', 'asiddha_rule': '8_2_104', 'fires': True, 'environment': 'samhitā'}),
    "8.2.105": ({'range': '8.2', 'asiddha_rule': '8_2_105', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_105_off', 'fires': True}),
    "8.2.106": ({'range': '8.2', 'asiddha_rule': '8_2_106', 'fires': True}, {'range': '8.2', 'asiddha_rule': '8_2_106_off', 'fires': True}),
    "8.2.107": ({'range': '8.2', 'asiddha_rule': '8_2_107', 'fires': True, 'relative_position': 'pūrva'}, {'range': '8.2', 'asiddha_rule': '8_2_107_off', 'fires': True, 'relative_position': 'pūrva'}),
    "8.2.108": ({'range': '8.2', 'environment': 'samhitā', 'sandhi_operation': 'yavāvaca', 'left': 'te', 'right': 'agnim', 'expected_rule': 'ayavāyāva', 'fires': True}, {'range': '8.2', 'environment': 'pratyaya', 'sandhi_operation': 'yavāvaca', 'left': 'te', 'right': 'agnim', 'expected_rule': 'ayavāyāva', 'fires': True}),
}

META: dict[str, SutraMeta] = {
    "8.2.1": SutraMeta('paribhasha', "पूर्वत्रासिद्धम् ।", ("domain:asiddha_samhita", "pada:8.2", "purvatr_asiddham")),
    "8.2.2": SutraMeta('vidhi', "नलोपः सुप्स्वरसंज्ञातुग्विधिषु कृति ।", ("domain:asiddha_samhita", "pada:8.2", "nalopa_sup_samjna")),
    "8.2.3": SutraMeta('pratisedha', "न मु ने ।", ("domain:asiddha_samhita", "pada:8.2", "na_mu_ne")),
    "8.2.4": SutraMeta('vidhi', "उदात्तस्वरितयोर्यणः स्वरितोऽनुदात्तस्य ।", ("domain:asiddha_samhita", "pada:8.2", "udatta_svarita_yana")),
    "8.2.5": SutraMeta('vidhi', "एकादेश उदात्तेनोदात्तः ।", ("domain:asiddha_samhita", "pada:8.2", "ekadesa_udatta")),
    "8.2.6": SutraMeta('vibhasha', "स्वरितो वाऽनुदात्ते पदादौ ।", ("domain:asiddha_samhita", "pada:8.2", "svarita_padadau")),
    "8.2.7": SutraMeta('pratisedha', "नलोपः प्रातिपदिकान्तस्य ।", ("domain:asiddha_samhita", "pada:8.2", "na_lopa_pratipadika")),
    "8.2.8": SutraMeta('pratisedha', "न ङिसम्बुद्ध्योः ।", ("domain:asiddha_samhita", "pada:8.2", "na_ngi_sambuddhi")),
    "8.2.9": SutraMeta('vidhi', "मादुपधायाश्च मतोर्वोऽयवादिभ्यः ।", ("domain:asiddha_samhita", "pada:8.2", "mat_upadha_va")),
    "8.2.10": SutraMeta('vidhi', "झयः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_10")),
    "8.2.11": SutraMeta('vidhi', "संज्ञायाम् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_11")),
    "8.2.12": SutraMeta('vidhi', "आसन्दीवदष्ठीवच्चक्रीवत्कक्षीवद्रुमण्वच्चर्मण्वती ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_12")),
    "8.2.13": SutraMeta('vibhasha', "उदन्वानुदधौ च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_13")),
    "8.2.14": SutraMeta('vibhasha', "राजन्वान् सौराज्ये ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_14")),
    "8.2.15": SutraMeta('vidhi', "छन्दसीरः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_15")),
    "8.2.16": SutraMeta('vidhi', "अनो नुट् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_16")),
    "8.2.17": SutraMeta('vidhi', "नाद्घस्य ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_17")),
    "8.2.18": SutraMeta('vidhi', "कृपो रो लः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_18")),
    "8.2.19": SutraMeta('vidhi', "उपसर्गस्यायतौ ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_19")),
    "8.2.20": SutraMeta('vidhi', "ग्रो यङि ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_20")),
    "8.2.21": SutraMeta('vibhasha', "अचि विभाषा ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_21")),
    "8.2.22": SutraMeta('vidhi', "परेश्च घाङ्कयोः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_22")),
    "8.2.23": SutraMeta('vidhi', "संयोगान्तस्य लोपः ।", ("domain:asiddha_samhita", "pada:8.2", "samyoganta_lopa")),
    "8.2.24": SutraMeta('vidhi', "रात्‌ सस्य ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_24")),
    "8.2.25": SutraMeta('vidhi', "धि च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_25")),
    "8.2.26": SutraMeta('vidhi', "झलो झलि ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_26")),
    "8.2.27": SutraMeta('vibhasha', "ह्रस्वादङ्गात्‌ ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_27")),
    "8.2.28": SutraMeta('vidhi', "इट ईटि ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_28")),
    "8.2.29": SutraMeta('vidhi', "स्कोः संयोगाद्योरन्ते च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_29")),
    "8.2.30": SutraMeta('vidhi', "चोः कुः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_30")),
    "8.2.31": SutraMeta('vidhi', "हो ढः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_31")),
    "8.2.32": SutraMeta('vidhi', "दादेर्धातोर्घः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_32")),
    "8.2.33": SutraMeta('vidhi', "वा द्रुहमुहष्णुहष्णिहाम् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_33")),
    "8.2.34": SutraMeta('vidhi', "नहो धः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_34")),
    "8.2.35": SutraMeta('vidhi', "आहस्थः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_35")),
    "8.2.36": SutraMeta('vidhi', "व्रश्चभ्रस्जसृजमृजयजराजभ्राजच्छशां षः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_36")),
    "8.2.37": SutraMeta('vidhi', "एकाचो बशो भष् झषन्तस्य स्ध्वोः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_37")),
    "8.2.38": SutraMeta('vidhi', "दधस्तथोश्च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_38")),
    "8.2.39": SutraMeta('vidhi', "झलां जशोऽन्ते ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_39")),
    "8.2.40": SutraMeta('vidhi', "झषस्तथोर्धोऽधः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_40")),
    "8.2.41": SutraMeta('vidhi', "षढोः कः सि ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_41")),
    "8.2.42": SutraMeta('vidhi', "रदाभ्यां निष्ठातो नः पूर्वस्य च दः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_42")),
    "8.2.43": SutraMeta('vidhi', "संयोगादेरातो धातोर्यण्वतः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_43")),
    "8.2.44": SutraMeta('vibhasha', "ल्वादिभ्यः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_44")),
    "8.2.45": SutraMeta('vidhi', "ओदितश्च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_45")),
    "8.2.46": SutraMeta('vidhi', "क्षियो दीर्घात्‌ ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_46")),
    "8.2.47": SutraMeta('vidhi', "श्योऽस्पर्शे ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_47")),
    "8.2.48": SutraMeta('vidhi', "अञ्चोऽनपादाने ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_48")),
    "8.2.49": SutraMeta('vidhi', "दिवोऽविजिगीषायाम् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_49")),
    "8.2.50": SutraMeta('vibhasha', "निर्वाणोऽवाते ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_50")),
    "8.2.51": SutraMeta('vidhi', "शुषः कः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_51")),
    "8.2.52": SutraMeta('vidhi', "पचो वः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_52")),
    "8.2.53": SutraMeta('vidhi', "क्षायो मः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_53")),
    "8.2.54": SutraMeta('vidhi', "प्रस्त्योऽन्यतरस्याम् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_54")),
    "8.2.55": SutraMeta('vidhi', "अनुपसर्गात्‌ फुल्लक्षीबकृशोल्लाघाः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_55")),
    "8.2.56": SutraMeta('vidhi', "नुदविदोन्दत्राघ्राह्रीभ्योऽन्यतरस्याम् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_56")),
    "8.2.57": SutraMeta('pratisedha', "न ध्याख्यापॄमूर्छिमदाम् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_57")),
    "8.2.58": SutraMeta('vidhi', "वित्तो भोगप्रत्यययोः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_58")),
    "8.2.59": SutraMeta('vidhi', "भित्तं शकलम् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_59")),
    "8.2.60": SutraMeta('vidhi', "ऋणमाधमर्ण्ये ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_60")),
    "8.2.61": SutraMeta('vidhi', "नसत्तनिषत्तानुत्तप्रतूर्तसूर्तगूर्तानि छन्दसि ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_61")),
    "8.2.62": SutraMeta('vidhi', "क्विन्प्रत्ययस्य कुः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_62")),
    "8.2.63": SutraMeta('vidhi', "नशेर्वा ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_63")),
    "8.2.64": SutraMeta('vidhi', "मो नो धातोः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_64")),
    "8.2.65": SutraMeta('vidhi', "म्वोश्च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_65")),
    "8.2.66": SutraMeta('vidhi', "ससजुषो रुः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_66")),
    "8.2.67": SutraMeta('vidhi', "अवयाःश्वेतवाःपुरोडाश्च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_67")),
    "8.2.68": SutraMeta('vidhi', "अहन् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_68")),
    "8.2.69": SutraMeta('vidhi', "रोऽसुपि ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_69")),
    "8.2.70": SutraMeta('vidhi', "अम्नरूधरवरित्युभयथा छन्दसि ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_70")),
    "8.2.71": SutraMeta('vidhi', "भुवश्च महाव्याहृतेः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_71")),
    "8.2.72": SutraMeta('vidhi', "वसुस्रंसुध्वंस्वनडुहां दः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_72")),
    "8.2.73": SutraMeta('vidhi', "तिप्यनस्तेः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_73")),
    "8.2.74": SutraMeta('vidhi', "सिपि धातो रुर्वा ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_74")),
    "8.2.75": SutraMeta('vidhi', "दश्च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_75")),
    "8.2.76": SutraMeta('vidhi', "र्वोरुपधाया दीर्घ इकः ।", ("domain:asiddha_samhita", "pada:8.2", "upadha_dirgha_ik")),
    "8.2.77": SutraMeta('vidhi', "हलि च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_77")),
    "8.2.78": SutraMeta('vidhi', "उपधायां च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_78")),
    "8.2.79": SutraMeta('pratisedha', "न भकुर्छुराम् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_79")),
    "8.2.80": SutraMeta('vidhi', "अदसोऽसेर्दादु दो मः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_80")),
    "8.2.81": SutraMeta('vidhi', "एत ईद्बहुवचने ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_81")),
    "8.2.82": SutraMeta('vibhasha', "वाक्यस्य टेः प्लुत उदात्तः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_82")),
    "8.2.83": SutraMeta('vibhasha', "प्रत्यभिवादेअशूद्रे ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_83")),
    "8.2.84": SutraMeta('vidhi', "दूराद्धूते च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_84")),
    "8.2.85": SutraMeta('vidhi', "हैहेप्रयोगे हैहयोः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_85")),
    "8.2.86": SutraMeta('vidhi', "गुरोरनृतोऽनन्त्यस्याप्येकैकस्य प्राचाम् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_86")),
    "8.2.87": SutraMeta('vidhi', "ओमभ्यादाने ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_87")),
    "8.2.88": SutraMeta('vidhi', "ये यज्ञकर्मणि ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_88")),
    "8.2.89": SutraMeta('vidhi', "प्रणवष्टेः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_89")),
    "8.2.90": SutraMeta('vidhi', "याज्याऽन्तः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_90")),
    "8.2.91": SutraMeta('vidhi', "ब्रूहिप्रेस्यश्रौषड्वौषडावहानामादेः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_91")),
    "8.2.92": SutraMeta('vidhi', "अग्नीत्प्रेषणे परस्य च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_92")),
    "8.2.93": SutraMeta('vibhasha', "विभाषा पृष्टप्रतिवचने हेः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_93")),
    "8.2.94": SutraMeta('vidhi', "निगृह्यानुयोगे च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_94")),
    "8.2.95": SutraMeta('vidhi', "आम्रेडितं भर्त्सने ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_95")),
    "8.2.96": SutraMeta('vidhi', "अङ्गयुक्तं तिङ् आकाङ्क्षम् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_96")),
    "8.2.97": SutraMeta('vidhi', "विचार्यमाणानाम् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_97")),
    "8.2.98": SutraMeta('vidhi', "पूर्वं तु भाषायाम् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_98")),
    "8.2.99": SutraMeta('vidhi', "प्रतिश्रवणे च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_99")),
    "8.2.100": SutraMeta('vidhi', "अनुदात्तं प्रश्नान्ताभिपूजितयोः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_100")),
    "8.2.101": SutraMeta('vidhi', "चिदिति चोपमाऽर्थे प्रयुज्यमाने ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_101")),
    "8.2.102": SutraMeta('vidhi', "उपरिस्विदासीदिति च ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_102")),
    "8.2.103": SutraMeta('vidhi', "स्वरितमाम्रेडितेऽसूयासम्मतिकोपकुत्सनेषु ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_103")),
    "8.2.104": SutraMeta('vidhi', "क्षियाऽऽशीःप्रैषेषु तिङ् आकाङ्क्षम् ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_104")),
    "8.2.105": SutraMeta('vidhi', "अनन्त्यस्यापि प्रश्नाख्यानयोः ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_105")),
    "8.2.106": SutraMeta('vidhi', "प्लुतावैच इदुतौ ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_106")),
    "8.2.107": SutraMeta('vidhi', "एचोऽप्रगृह्यस्यादूराद्धूते पूर्वस्यार्धस्यादुत्तरस्येदुतौ ।", ("domain:asiddha_samhita", "pada:8.2", "8_2_107")),
    "8.2.108": SutraMeta('vidhi', "तयोर्य्वावचि संहितायाम् ।", ("domain:asiddha_samhita", "pada:8.2", "yavava_samhita")),
}

def self_check() -> dict[str, int]:
    """Verify every predicate accepts positive and rejects negative fixture."""
    failures: list[str] = []
    for sid in sorted(FIXTURES):
        pred = handler_for(sid)
        if not pred(positive_features(sid)):
            failures.append(f"{sid}: rejected positive")
        if pred(negative_features(sid)):
            failures.append(f"{sid}: accepted negative")
    if failures:
        raise AssertionError("sutra_impl_8_2 self_check failed:\n" + "\n".join(failures))
    return {
        "sutras": len(FIXTURES),
        "predicates": len([n for n in globals() if n.startswith("sutra_8_2_")]),
        "meta": len(META),
    }

(
    IMPLEMENTED_IDS,
    has_real_implementation,
    handler_for,
    positive_features,
    negative_features,
) = make_module_api(FIXTURES, globals())

if __name__ == "__main__":
    counts = self_check()
    forbidden = []
    src = Path(__file__).read_text(encoding="utf-8")
    scan_body = src.split('if __name__ == "__main__":')[0]
    for token in ("__miss__", '"different"', "index %", "auto_fixture"):
        if token in scan_body:
            forbidden.append(token)
    print("counts:", counts)
    print("forbidden_scan:", forbidden or "clean")