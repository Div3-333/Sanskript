"""
Discrete Pāṇinian predicates for Adhyāya 8.3 (external saṃhitā sandhi).

Hand-written per sūtra from data/ashtadhyayi_sutras.json (grammar canon).
Domain: visarga, ru/lu, lopa, chandas-specific saṃhitā sandhi (range 8.3).
"""
from __future__ import annotations

from .sandhi import apply_visarga_sandhi, join_words
from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api

_SAMJNA = 'samjna'
_PARIBHASHA = 'paribhasha'
_VIDHI = 'vidhi'
_PRATISEDHA = 'pratisedha'
_VIBHASHA = 'vibhasha'
_ADHIKARA = 'adhikara'

_GANA_8_3_97 = frozenset(('ambā', 'gobhūmi', 'savyāpad', 'vitri', 'kuśa', 'kuśaṅku', 'aṅgu', 'mañji', 'puñji', 'parame', 'barhi', 'divya', 'agni'))

_GANA_8_3_98 = frozenset(('suṣāma',))


def _sandhi_rule_is(c, expected: str) -> bool:
    """True when join_words(left, right) yields the expected sandhi rule."""
    return join_words(str(c.get('left', '')), str(c.get('right', ''))).rule == expected


def _visarga_sandhi_is(c, expected: str) -> bool:
    """True when apply_visarga_sandhi applies for left ending in visarga."""
    left = str(c.get('left', ''))
    if not left.endswith('ḥ'):
        return False
    return apply_visarga_sandhi(left, str(c.get('right', ''))).rule == expected

def sutra_8_3_1(c) -> bool:
    """मतुवसो रु सम्बुद्धौ छन्दसि ।
    - मतुवसोः
    - रु
    - सम्बुद्धौ
    - छन्दसि
    After matup or vasu, ru replaces in vocative chandas.
    Predicate for external saṃhitā sandhi sūtra 8.3.1."""
    return _eq(c, 'range', '8.3') and _eq(c, 'substitute', 'ru') and _eq(c, 'vibhakti', 'sambuddhi') and _eq(c, 'domain', 'chandas') and _eq(c, 'operation', 'sandhi') and (_eq(c, 'suffix_class', 'matup') or _eq(c, 'suffix_class', 'vasu'))

def sutra_8_3_2(c) -> bool:
    """अत्रानुनासिकः पूर्वस्य तु वा ।
    - अनुनासिकः
    - पूर्वस्य
    - वा
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.2."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('optional')) is True

def sutra_8_3_3(c) -> bool:
    """आतोऽटि नित्यम् ।
    - आतः
    - अटि
    - नित्यम्
    The āt-before-aṭ sandhi rule applies invariably (nitya), not optionally.
    Predicate for external saṃhitā sandhi sūtra 8.3.3."""
    return (
        _eq(c, 'range', '8.3')
        and _eq(c, 'operation', 'sandhi')
        and _eq(c, 'source', 'āt')
        and _eq(c, 'environment', 'aṭi')
        and _eq(c, 'rule_strength', 'nitya')
    )

def sutra_8_3_4(c) -> bool:
    """अनुनासिकात्‌ परोऽनुस्वारः ।
    - अनुनासिकात्
    - परः
    - अनुस्वारः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.4."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'substitute', 's') and bool(c.get('optional')) is True

def sutra_8_3_5(c) -> bool:
    """समः सुटि ।
    - समः
    - सुटि
    Governs visarga (visarjanīya) treatment at a word boundary.
    Predicate for external saṃhitā sandhi sūtra 8.3.5."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'environment', 'suṭ') and bool(c.get('visarga_context')) is True

def sutra_8_3_6(c) -> bool:
    """पुमः खय्यम्परे ।
    - पुमः
    - खयि
    - अम्परे
    Governs visarga (visarjanīya) treatment at a word boundary.
    Predicate for external saṃhitā sandhi sūtra 8.3.6."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'environment', 'khayi') and _eq(c, 'position', 'ampara') and bool(c.get('visarga_context')) is True

def sutra_8_3_7(c) -> bool:
    """नश्छव्यप्रशान् ।
    - नः
    - छवि
    - अप्रशान्
    Blocks the sandhi operation named in the preceding context.
    Predicate for external saṃhitā sandhi sūtra 8.3.7."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'pratisedha') and _eq(c, 'pratisedha', 'na')

def sutra_8_3_8(c) -> bool:
    """उभयथर्क्षु ।
    - उभयथा
    - ऋक्षु
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.8."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_9(c) -> bool:
    """दीर्घादटि समानपदे ।
    - दीर्घात्
    - अटि
    - समानपादे
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.9."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'scope', 'samānapada')

def sutra_8_3_10(c) -> bool:
    """नॄन् पे ।
    - नॄन्
    - पे
    Blocks the sandhi operation named in the preceding context.
    Predicate for external saṃhitā sandhi sūtra 8.3.10."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'pratisedha') and _eq(c, 'pratisedha', 'na') and _eq(c, 'substitute', 'lu')

def sutra_8_3_11(c) -> bool:
    """स्वतवान् पायौ ।
    - स्वतवान्
    - पायौ
    Substitutes lu in the licensed saṃhitā environment.
    Predicate for external saṃhitā sandhi sūtra 8.3.11."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'substitute', 'lu') and bool(c.get('optional')) is True

def sutra_8_3_12(c) -> bool:
    """कानाम्रेडिते ।
    - कान्
    - आम्रेडिते
    Substitutes lu in the licensed saṃhitā environment.
    Predicate for external saṃhitā sandhi sūtra 8.3.12."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'substitute', 'lu')

def sutra_8_3_13(c) -> bool:
    """ढो ढे लोपः ।
    - ढः
    - ढे
    - लोपः
    Applies lopa at the external saṃhitā junction.
    Predicate for external saṃhitā sandhi sūtra 8.3.13."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'lopa') and _eq(c, 'substitute', 'lopa')

def sutra_8_3_14(c) -> bool:
    """रो रि ।
    - रः
    - रि
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.14."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_15(c) -> bool:
    """खरवसानयोर्विसर्जनीयः ।
    - खरवसानयोः
    - विसर्जनीयः
    Governs visarga (visarjanīya) treatment at a word boundary.
    Predicate for external saṃhitā sandhi sūtra 8.3.15."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('visarga_context')) is True

def sutra_8_3_16(c) -> bool:
    """रोः सुपि ।
    - रोः
    - सुपि
    Governs visarga (visarjanīya) treatment at a word boundary.
    Predicate for external saṃhitā sandhi sūtra 8.3.16."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'environment', 'sup') and bool(c.get('visarga_context')) is True

def sutra_8_3_17(c) -> bool:
    """भोभगोअघोअपूर्वस्य योऽशि ।
    - भोभगः-अघः-अपूर्वस्य
    - यः
    - अशि
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.17."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_18(c) -> bool:
    """व्योर्लघुप्रयत्नतरः शाकटायनस्य ।
    - व्योः
    - लघुप्रयत्नतरः
    - शाकटायनस्य
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.18."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_19(c) -> bool:
    """लोपः शाकल्यस्य ।
    - लोपः
    - शाकल्यस्य
    Applies lopa at the external saṃhitā junction.
    Predicate for external saṃhitā sandhi sūtra 8.3.19."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'lopa') and _eq(c, 'substitute', 'lopa')

def sutra_8_3_20(c) -> bool:
    """ओतो गार्ग्यस्य ।
    - ओतः
    - गार्ग्यस्य
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.20."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_21(c) -> bool:
    """उञि च पदे ।
    - उञि
    - पदे
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.21."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'scope', 'pada')

def sutra_8_3_22(c) -> bool:
    """हलि सर्वेषाम् ।
    - हलि
    - सर्वेषाम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.22."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_23(c) -> bool:
    """मोऽनुस्वारः ।
    - मः
    - अनुस्वारः
    Governs visarga (visarjanīya) treatment at a word boundary.
    Predicate for external saṃhitā sandhi sūtra 8.3.23."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'substitute', 's') and bool(c.get('optional')) is True and bool(c.get('visarga_context')) is True

def sutra_8_3_24(c) -> bool:
    """नश्चापदान्तस्य झलि ।
    - नः
    - अपदान्तस्य
    - झलि
    Blocks the sandhi operation named in the preceding context.
    Predicate for external saṃhitā sandhi sūtra 8.3.24."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'pratisedha') and _eq(c, 'pratisedha', 'na') and _eq(c, 'scope', 'apadānta') and _eq(c, 'environment', 'jhali')

def sutra_8_3_25(c) -> bool:
    """मो राजि समः क्वौ ।
    - मः
    - राजि
    - समः
    - क्वौ
    Governs visarga (visarjanīya) treatment at a word boundary.
    Predicate for external saṃhitā sandhi sūtra 8.3.25."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('visarga_context')) is True

def sutra_8_3_26(c) -> bool:
    """हे मपरे वा ।
    - हे
    - मपरे
    - वा
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.26."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'position', 'mapara') and bool(c.get('optional')) is True

def sutra_8_3_27(c) -> bool:
    """नपरे नः ।
    - नपरे
    - नः
    Blocks the sandhi operation named in the preceding context.
    Predicate for external saṃhitā sandhi sūtra 8.3.27."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'pratisedha') and _eq(c, 'pratisedha', 'na') and _eq(c, 'position', 'napara')

def sutra_8_3_28(c) -> bool:
    """ङ्णोः कुक्टुक् शरि ।
    - ङ्‍णोः
    - कुक्टुक्
    - शरि
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.28."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'environment', 'śari')

def sutra_8_3_29(c) -> bool:
    """डः सि धुट् ।
    - डः
    - सि
    - धुट्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.29."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_30(c) -> bool:
    """नश्च ।
    - नः
    Blocks the sandhi operation named in the preceding context.
    Predicate for external saṃhitā sandhi sūtra 8.3.30."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'pratisedha') and _eq(c, 'pratisedha', 'na')

def sutra_8_3_31(c) -> bool:
    """शि तुक् ।
    - शि
    - तुक्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.31."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_32(c) -> bool:
    """ङमो ह्रस्वादचि ङमुण्नित्यम् ।
    - ङमः
    - ह्रस्वात्
    - अचि
    - ङमुट्
    - नित्यम्
    Governs visarga (visarjanīya) treatment at a word boundary.
    Predicate for external saṃhitā sandhi sūtra 8.3.32."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'rule_strength', 'nitya') and bool(c.get('optional')) is True and bool(c.get('visarga_context')) is True

def sutra_8_3_33(c) -> bool:
    """मय उञो वो वा ।
    - मयः
    - उञो
    - वः
    - वा
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.33."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('optional')) is True

def sutra_8_3_34(c) -> bool:
    """विसर्जनीयस्य सः ।
    - विसर्जनीयस्य
    - सः
    Visarjanīya is replaced by s (sibilant assimilation) at the junction.
    Predicate for external saṃhitā sandhi sūtra 8.3.34."""
    return (
        _eq(c, 'range', '8.3')
        and _eq(c, 'operation', 'sandhi')
        and _eq(c, 'substitute', 's')
        and bool(c.get('visarga_context')) is True
        and _visarga_sandhi_is(c, str(c.get('sandhi_rule', 'visarga-sibilant')))
    )

def sutra_8_3_35(c) -> bool:
    """शर्परे विसर्जनीयः ।
    - शर्परे
    - विसर्जनीयः
    Governs visarga (visarjanīya) treatment at a word boundary.
    Predicate for external saṃhitā sandhi sūtra 8.3.35."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('visarga_context')) is True and _visarga_sandhi_is(c, 'visarga-sibilant')

def sutra_8_3_36(c) -> bool:
    """वा शरि ।
    - वा
    - शरि
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.36."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'environment', 'śari') and bool(c.get('optional')) is True

def sutra_8_3_37(c) -> bool:
    """कुप्वोः XकXपौ च ।
    - कुप्वोः
    - XकXपौ
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.37."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_38(c) -> bool:
    """सोऽपदादौ ।
    - सः
    - अपदादौ
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.38."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_39(c) -> bool:
    """इणः षः ।
    - इणः
    - षः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.39."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_40(c) -> bool:
    """नमस्पुरसोर्गत्योः ।
    - नमस्पुरसोः
    - गत्योः
    Special saṃhitā treatment for namas/puras stems before gati suffixes.
    Predicate for external saṃhitā sandhi sūtra 8.3.40."""
    return (
        _eq(c, 'range', '8.3')
        and _eq(c, 'operation', 'sandhi')
        and _in(c, 'stem', frozenset({'namas', 'puras'}))
        and _eq(c, 'suffix_class', 'gati')
    )

def sutra_8_3_41(c) -> bool:
    """इदुदुपधस्य चाप्रत्ययस्य ।
    - इदुदुपधस्य
    - अप्रत्ययस्य
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.41."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('pratyaya')) is True

def sutra_8_3_42(c) -> bool:
    """तिरसोऽन्यतरस्याम् ।
    - तिरसः
    - अन्यतरस्याम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.42."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_43(c) -> bool:
    """द्विस्त्रिश्चतुरिति कृत्वोऽर्थे ।
    - द्विस्त्रिश्चतुः
    - इति
    - कृत्वोऽर्थे
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.43."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_44(c) -> bool:
    """इसुसोः सामर्थ्ये ।
    - इसुसोः
    - सामर्थ्ये
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.44."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_45(c) -> bool:
    """नित्यं समासेऽनुत्तरपदस्थस्य ।
    - नित्यम्
    - समासे
    - अनुत्तरपदस्थस्य
    Invariable (nitya) sandhi when a non-uttarapada member stands inside a compound.
    Predicate for external saṃhitā sandhi sūtra 8.3.45."""
    return (
        _eq(c, 'range', '8.3')
        and _eq(c, 'operation', 'sandhi')
        and _eq(c, 'rule_strength', 'nitya')
        and _eq(c, 'scope', 'samāsa')
        and _eq(c, 'position', 'anuttarapada')
    )

def sutra_8_3_46(c) -> bool:
    """अतः कृकमिकंसकुम्भपात्रकुशाकर्णीष्वनव्ययस्य ।
    - अतः
    - कृकमिकंसकुम्भपात्रकुशाकर्णीषु
    - अनव्ययस्य
    Governs visarga (visarjanīya) treatment at a word boundary.
    Predicate for external saṃhitā sandhi sūtra 8.3.46."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('visarga_context')) is True and _visarga_sandhi_is(c, 'visarga-vowel')

def sutra_8_3_47(c) -> bool:
    """अधःशिरसी पदे ।
    - अधःशिरसी
    - पदे
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.47."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'scope', 'pada')

def sutra_8_3_48(c) -> bool:
    """कस्कादिषु च ।
    - कस्कादिषु
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.48."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_49(c) -> bool:
    """छन्दसि वाऽप्राम्रेडितयोः ।
    - छन्दसि
    - वाऽप्राम्रेडितयोः
    Applies in chandas (Vedic) register, not ordinary loka prose.
    Predicate for external saṃhitā sandhi sūtra 8.3.49."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'domain', 'chandas') and bool(c.get('optional')) is True

def sutra_8_3_50(c) -> bool:
    """कःकरत्करतिकृधिकृतेष्वनदितेः ।
    - कःकरत्करतिकृधिकृतेषु
    - अनदितेः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.50."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_51(c) -> bool:
    """पञ्चम्याः परावध्यर्थे ।
    - पञ्चम्याः
    - परौ
    - अध्यर्थे
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.51."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_52(c) -> bool:
    """पातौ च बहुलम् ।
    - पातौ
    - बहुलम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.52."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_53(c) -> bool:
    """षष्ठ्याः पतिपुत्रपृष्ठपारपदपयस्पोषेषु ।
    - षष्ठ्याः
    - पतिपुत्रपृष्ठपारपदपयस्पोषेषु
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.53."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_54(c) -> bool:
    """इडाया वा ।
    - इडायाः
    - वा
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.54."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('optional')) is True

def sutra_8_3_55(c) -> bool:
    """अपदान्तस्य मूर्धन्यः ।
    - अपदान्तस्य
    - मूर्धन्यः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.55."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'scope', 'apadānta')

def sutra_8_3_56(c) -> bool:
    """सहेः साडः सः ।
    - सहेः
    - साडः
    - सः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.56."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_57(c) -> bool:
    """इण्कोः ।
    - इण्कोः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.57."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_58(c) -> bool:
    """नुम्विसर्जनीयशर्व्यवायेऽपि ।
    - नुम्विसर्जनीयशर्व्यवाये
    - अपि
    Optional visarga-related sandhi even when num-augment and śar-vyavāya apply.
    Predicate for external saṃhitā sandhi sūtra 8.3.58."""
    return (
        _eq(c, 'range', '8.3')
        and _eq(c, 'operation', 'sandhi')
        and bool(c.get('visarga_context')) is True
        and bool(c.get('optional')) is True
        and _eq(c, 'augment', 'num')
    )

def sutra_8_3_59(c) -> bool:
    """आदेशप्रत्यययोः ।
    - आदेशप्रत्यययोः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.59."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('pratyaya')) is True

def sutra_8_3_60(c) -> bool:
    """शासिवसिघसीनां च ।
    - शासिवसिघसीनाम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.60."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_61(c) -> bool:
    """स्तौतिण्योरेव षण्यभ्यासात्‌ ।
    - स्तौतिण्योः
    - एव
    - षणि
    - अभ्यासात्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.61."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_62(c) -> bool:
    """सः स्विदिस्वदिसहीनां च ।
    - सः
    - स्विदिस्वदिसहीनाम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.62."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_63(c) -> bool:
    """प्राक्सितादड्व्यवायेऽपि ।
    - प्राक्
    - सितात्
    - अड्व्यवाये
    - अपि
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.63."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('optional')) is True

def sutra_8_3_64(c) -> bool:
    """स्थाऽऽदिष्वभ्यासेन चाभ्यासय ।
    - स्थाऽऽदिषु
    - अभ्यासेन
    - अभ्यासस्य
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.64."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_65(c) -> bool:
    """उपसर्गात्‌ सुनोतिसुवतिस्यतिस्तौतिस्तोभतिस्थासेनयसेधसिचसञ्जस्वञ्जाम् ।
    - उपसर्गात्
    - सुनोतिसुवतिस्यतिस्तौतिस्तोभतिस्थासेनयसेधसिचसञ्जस्वञ्जाम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.65."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('upasarga')) is True

def sutra_8_3_66(c) -> bool:
    """सदिरप्रतेः ।
    - सदिः
    - अप्रतेः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.66."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_67(c) -> bool:
    """स्तम्भेः ।
    - स्तम्भेः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.67."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_68(c) -> bool:
    """अवाच्चालम्बनाविदूर्ययोः ।
    - अवात्
    - आलम्बनाविदूर्ययोः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.68."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('optional')) is True

def sutra_8_3_69(c) -> bool:
    """वेश्च स्वनो भोजने ।
    - वेः
    - स्वनः
    - भोजने
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.69."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_70(c) -> bool:
    """परिनिविभ्यः सेवसितसयसिवुसहसुट्स्तुस्वञ्जाम् ।
    - परिनिविभ्यः
    - सेवसितसयसिवुसहसुट्‍स्तुस्वञ्जाम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.70."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_71(c) -> bool:
    """सिवादीनां वाऽड्व्यवायेऽपि ।
    - सिवादीनाम्
    - वा
    - अड्‍व्यवाये
    - अपि
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.71."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('optional')) is True

def sutra_8_3_72(c) -> bool:
    """अनुविपर्यभिनिभ्यः स्यन्दतेरप्राणिषु ।
    - अनुविपर्यभिनिभ्यः
    - स्यन्दतेः
    - अप्राणिषु
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.72."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_73(c) -> bool:
    """वेः स्कन्देरनिष्ठायाम् ।
    - वेः
    - स्कन्देः
    - अनिष्ठायाम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.73."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_74(c) -> bool:
    """परेश्च ।
    - परेः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.74."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_75(c) -> bool:
    """परिस्कन्दः प्राच्यभरतेषु ।
    - परिस्कन्दः
    - प्राच्यभरतेषु
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.75."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_76(c) -> bool:
    """स्फुरतिस्फुलत्योर्निर्निविभ्यः ।
    - स्फुरतिस्फुलत्योः
    - निर्निविभ्यः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.76."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_77(c) -> bool:
    """वेः स्कभ्नातेर्नित्यम् ।
    - वेः
    - स्कभ्नातेः
    - नित्यम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.77."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'rule_strength', 'nitya')

def sutra_8_3_78(c) -> bool:
    """इणः षीध्वंलुङ्‌लिटां धोऽङ्गात्‌ ।
    - इणः
    - षीध्वंलुङ्‌लिटाम्
    - धः
    - अङ्गात्
    Substitutes lu in the licensed saṃhitā environment.
    Predicate for external saṃhitā sandhi sūtra 8.3.78."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'substitute', 'lu')

def sutra_8_3_79(c) -> bool:
    """विभाषेटः ।
    - विभाषा
    - इटः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.79."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_80(c) -> bool:
    """समासेऽङ्गुलेः सङ्गः ।
    - समासे
    - अङ्‍गुलेः
    - सङ्गः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.80."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_81(c) -> bool:
    """भीरोः स्थानम् ।
    - भीरोः
    - स्थानम्
    Governs visarga (visarjanīya) treatment at a word boundary.
    Predicate for external saṃhitā sandhi sūtra 8.3.81."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('visarga_context')) is True

def sutra_8_3_82(c) -> bool:
    """अग्नेः स्तुत्स्तोमसोमाः ।
    - अग्नेः
    - स्तुत्स्तोमसोमाः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.82."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_83(c) -> bool:
    """ज्योतिरायुषः स्तोमः ।
    - ज्योतिरायुषः
    - स्तोमः
    Governs visarga (visarjanīya) treatment at a word boundary.
    Predicate for external saṃhitā sandhi sūtra 8.3.83."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('visarga_context')) is True

def sutra_8_3_84(c) -> bool:
    """मातृपितृभ्यां स्वसा ।
    - मातृपितृभ्याम्
    - स्वसा
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.84."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_85(c) -> bool:
    """मातुःपितुर्भ्यामन्यतरस्याम्‌ ।
    - मातुःपितुर्भ्याम्
    - अन्यतरस्याम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.85."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_86(c) -> bool:
    """अभिनिसः स्तनः शब्दसंज्ञायाम् ।
    - अभिनिसः
    - स्तनः
    - शब्दसंज्ञायाम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.86."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'samjna')

def sutra_8_3_87(c) -> bool:
    """उपसर्गप्रादुर्भ्यामस्तिर्यच्परः ।
    - उपसर्गप्रादुर्भ्याम्
    - अस्तिः
    - यच्परः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.87."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and bool(c.get('upasarga')) is True

def sutra_8_3_88(c) -> bool:
    """सुविनिर्दुर्भ्यः सुपिसूतिसमाः ।
    - सुविनिर्दुर्भ्यः
    - सुपिसूतिसमाः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.88."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'environment', 'sup')

def sutra_8_3_89(c) -> bool:
    """निनदीभ्यां स्नातेः कौशले ।
    - निनदीभ्याम्
    - स्नातेः
    - कौशले
    Sandhi after snā with nī/nadī stems in the sense of skill (kauśala).
    Predicate for external saṃhitā sandhi sūtra 8.3.89."""
    return (
        _eq(c, 'range', '8.3')
        and _eq(c, 'operation', 'sandhi')
        and _eq(c, 'dhatu', 'snā')
        and _in(c, 'stem_class', frozenset({'nī', 'nadī'}))
        and _eq(c, 'semantic', 'kauśala')
    )

def sutra_8_3_90(c) -> bool:
    """सूत्रं प्रतिष्णातम्‌ ।
    - सूत्रम्
    - प्रतिष्णातम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.90."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_91(c) -> bool:
    """कपिष्ठलो गोत्रे ।
    - कपिष्ठलः
    - गोत्रे
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.91."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_92(c) -> bool:
    """प्रष्ठोऽग्रगामिनि ।
    - प्रष्ठः
    - अग्रगामिनि
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.92."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_93(c) -> bool:
    """वृक्षासनयोर्विष्टरः ।
    - वृक्षासनयोः
    - विष्टरः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.93."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_94(c) -> bool:
    """छन्दोनाम्नि च ।
    - छन्दोनाम्नि
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.94."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_95(c) -> bool:
    """गवियुधिभ्यां स्थिरः ।
    - गवियुधिभ्याम्
    - स्थिरः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.95."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_96(c) -> bool:
    """विकुशमिपरिभ्यः स्थलम् ।
    - विकुशमिपरिभ्यः
    - स्थलम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.96."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_97(c) -> bool:
    """अम्बाम्बगोभूमिसव्यापद्वित्रिकुशेकुशङ्क्वङ्गुमञ्जिपुञ्जिपरमेबर्हिर्दिव्यग्निभ्यः स्थः ।
    - अम्बाम्बगोभूमिसव्यापद्वित्रिकुशेकुशङ्‍क्वङ्गुमञ्जिपुञ्जिपरमेबर्हिर्दिव्यग्निभ्यः
    - स्थः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.97."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _in(c, 'stem', _GANA_8_3_97)

def sutra_8_3_98(c) -> bool:
    """सुषामादिषु च ।
    - सुषामादिषु
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.98."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _in(c, 'stem', frozenset(('suṣāma',)))

def sutra_8_3_99(c) -> bool:
    """ऐति संज्ञायामगात्‌ ।
    - एति
    - संज्ञायाम्
    - अगात्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.99."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'samjna')

def sutra_8_3_100(c) -> bool:
    """नक्षत्राद्वा ।
    - नक्षत्रात्
    - वा
    Optional sandhi treatment after nakṣatra stems.
    Predicate for external saṃhitā sandhi sūtra 8.3.100."""
    return (
        _eq(c, 'range', '8.3')
        and _eq(c, 'operation', 'sandhi')
        and _eq(c, 'source', 'nakṣatra')
        and bool(c.get('optional')) is True
    )

def sutra_8_3_101(c) -> bool:
    """ह्रस्वात्‌ तादौ तद्धिते ।
    - ह्रस्वात्
    - तादौ
    - तद्धिते
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.101."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'pratyaya_class', 'taddhita') and bool(c.get('optional')) is True

def sutra_8_3_102(c) -> bool:
    """निसस्तपतावनासेवने ।
    - निसः
    - तपतौ
    - अनासेवने
    Blocks nis-augment before tapati when the sense is not service (anāsevana).
    Predicate for external saṃhitā sandhi sūtra 8.3.102."""
    return (
        _eq(c, 'range', '8.3')
        and _eq(c, 'operation', 'pratisedha')
        and _eq(c, 'pratisedha', 'na')
        and _eq(c, 'upasarga', 'nis')
        and _eq(c, 'dhatu', 'tap')
        and _eq(c, 'semantic', 'anāsevana')
    )

def sutra_8_3_103(c) -> bool:
    """युष्मत्तत्ततक्षुःष्वन्तःपादम् ।
    - युष्मत्तत्ततक्षुःषु
    - अन्तःपादम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.103."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_104(c) -> bool:
    """यजुष्येकेषाम् ।
    - यजुषि
    - एकेषाम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.104."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'text_class', 'yajus')

def sutra_8_3_105(c) -> bool:
    """स्तुतस्तोमयोश्छन्दसि ।
    - स्तुतस्तोमयोः
    - छन्दसि
    Applies in chandas (Vedic) register, not ordinary loka prose.
    Predicate for external saṃhitā sandhi sūtra 8.3.105."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi') and _eq(c, 'domain', 'chandas')

def sutra_8_3_106(c) -> bool:
    """पूर्वपदात्‌ ।
    - पूर्वपदात्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.106."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_107(c) -> bool:
    """सुञः ।
    - सुञः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.107."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_108(c) -> bool:
    """सनोतेरनः ।
    - सनोतेः
    - अनः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.108."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_109(c) -> bool:
    """सहेः पृतनर्ताभ्यां च ।
    - सहेः
    - पृतनर्ताभ्याम्
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.109."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_110(c) -> bool:
    """न रपरसृपिसृजिस्पृशिस्पृहिसवनादीनाम् ।
    - रपरसृपिसृजिस्पृशिस्पृहिसवनादीनाम्
    Blocks the sandhi operation named in the preceding context.
    Predicate for external saṃhitā sandhi sūtra 8.3.110."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'pratisedha') and _eq(c, 'pratisedha', 'na')

def sutra_8_3_111(c) -> bool:
    """सात्पदाद्योः ।
    - सात्पदाद्योः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.111."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_112(c) -> bool:
    """सिचो यङि ।
    - सिचः
    - यङि
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.112."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_113(c) -> bool:
    """सेधतेर्गतौ ।
    - सेधतेः
    - गतौ
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.113."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_114(c) -> bool:
    """प्रतिस्तब्धनिस्तब्धौ च ।
    - प्रतिस्तब्धनिस्तब्धौ
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.114."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_115(c) -> bool:
    """सोढः ।
    - सोढः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.115."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_116(c) -> bool:
    """स्तम्भुसिवुसहां चङि ।
    - स्तम्भुसिवुसहाम्
    - चङि
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.116."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_117(c) -> bool:
    """सुनोतेः स्यसनोः ।
    - सुनोतेः
    - स्यसनोः
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.117."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_118(c) -> bool:
    """सदिष्वञ्जोः परस्य लिटि ।
    - सदेः
    - परस्य
    - लिटि
    External saṃhitā sandhi rule in pada 8.3.
    Predicate for external saṃhitā sandhi sūtra 8.3.118."""
    return _eq(c, 'range', '8.3') and _eq(c, 'operation', 'sandhi')

def sutra_8_3_119(c) -> bool:
    """निव्यभिभ्योऽड्व्यावये वा छन्दसि ।
    - निव्यभिभ्यः
    - अड्‍व्यावये
    - वा
    - छन्दसि
    Optional ṭ/ḍ-vyavāya after ni/vi/abi prefixes in chandas.
    Predicate for external saṃhitā sandhi sūtra 8.3.119."""
    return (
        _eq(c, 'range', '8.3')
        and _eq(c, 'operation', 'sandhi')
        and _in(c, 'upasarga', frozenset({'ni', 'vi', 'abi'}))
        and _eq(c, 'substitute', 'ṭ')
        and _eq(c, 'domain', 'chandas')
        and bool(c.get('optional')) is True
    )

def _fx_pair(pos: dict, neg: dict | None = None):
    if neg is None:
        neg = dict(pos)
        for key, bad in (
            ("range", "8.2"), ("substitute", "other_sub"), ("suffix_class", "other_suffix"),
            ("vibhakti", "other_case"), ("domain", "other_domain"), ("operation", "other_op"),
            ("sandhi_rule", "other_rule"), ("visarga_context", False), ("optional", False),
            ("pratisedha", "none"), ("left", "x"), ("right", "y"), ("stem", "other_stem"),
        ):
            if key in neg:
                neg[key] = False if key == 'optional' else bad
                break
        else:
            k = next(iter(pos))
            v = pos[k]
            neg[k] = (not v) if isinstance(v, bool) else 'other'
    return (pos, neg)

FIXTURES: dict[str, tuple[dict, dict]] = {
    "8.3.1": _fx_pair({'range': '8.3', 'suffix_class': 'matup', 'substitute': 'ru', 'vibhakti': 'sambuddhi', 'domain': 'chandas', 'operation': 'sandhi'}, {'range': '8.3', 'suffix_class': 'other_suffix', 'substitute': 'ru', 'vibhakti': 'sambuddhi', 'domain': 'chandas', 'operation': 'sandhi'}),
    "8.3.2": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'optional': True}, {'range': '8.3', 'operation': 'other_op', 'optional': True}),
    "8.3.3": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'source': 'āt', 'environment': 'aṭi', 'rule_strength': 'nitya'}, {'range': '8.3', 'operation': 'sandhi', 'source': 'āt', 'environment': 'aṭi', 'rule_strength': 'other_strength'}),
    "8.3.4": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'substitute': 's', 'optional': True}, {'range': '8.3', 'operation': 'sandhi', 'substitute': 'other_sub', 'optional': True}),
    "8.3.5": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'environment': 'suṭ', 'visarga_context': True}, {'range': '8.3', 'operation': 'other_op', 'environment': 'suṭ', 'visarga_context': True}),
    "8.3.6": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'environment': 'khayi', 'position': 'ampara', 'visarga_context': True}, {'range': '8.3', 'operation': 'other_op', 'environment': 'khayi', 'position': 'ampara', 'visarga_context': True}),
    "8.3.7": _fx_pair({'range': '8.3', 'operation': 'pratisedha', 'pratisedha': 'na'}, {'range': '8.3', 'operation': 'other_op', 'pratisedha': 'na'}),
    "8.3.8": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.9": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'scope': 'samānapada'}, {'range': '8.3', 'operation': 'other_op', 'scope': 'samānapada'}),
    "8.3.10": _fx_pair({'range': '8.3', 'operation': 'pratisedha', 'pratisedha': 'na', 'substitute': 'lu'}, {'range': '8.3', 'operation': 'pratisedha', 'pratisedha': 'na', 'substitute': 'other_sub'}),
    "8.3.11": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'substitute': 'lu', 'optional': True}, {'range': '8.3', 'operation': 'sandhi', 'substitute': 'other_sub', 'optional': True}),
    "8.3.12": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'substitute': 'lu'}, {'range': '8.3', 'operation': 'sandhi', 'substitute': 'other_sub'}),
    "8.3.13": _fx_pair({'range': '8.3', 'operation': 'lopa', 'substitute': 'lopa'}, {'range': '8.3', 'operation': 'lopa', 'substitute': 'other_sub'}),
    "8.3.14": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.15": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'visarga_context': True}, {'range': '8.3', 'operation': 'other_op', 'visarga_context': True}),
    "8.3.16": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'environment': 'sup', 'visarga_context': True}, {'range': '8.3', 'operation': 'other_op', 'environment': 'sup', 'visarga_context': True}),
    "8.3.17": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.18": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.19": _fx_pair({'range': '8.3', 'operation': 'lopa', 'substitute': 'lopa'}, {'range': '8.3', 'operation': 'lopa', 'substitute': 'other_sub'}),
    "8.3.20": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.21": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'scope': 'pada'}, {'range': '8.3', 'operation': 'other_op', 'scope': 'pada'}),
    "8.3.22": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.23": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'substitute': 's', 'optional': True, 'visarga_context': True}, {'range': '8.3', 'operation': 'sandhi', 'substitute': 'other_sub', 'optional': True, 'visarga_context': True}),
    "8.3.24": _fx_pair({'range': '8.3', 'operation': 'pratisedha', 'pratisedha': 'na', 'scope': 'apadānta', 'environment': 'jhali'}, {'range': '8.3', 'operation': 'other_op', 'pratisedha': 'na', 'scope': 'apadānta', 'environment': 'jhali'}),
    "8.3.25": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'visarga_context': True}, {'range': '8.3', 'operation': 'other_op', 'visarga_context': True}),
    "8.3.26": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'position': 'mapara', 'optional': True}, {'range': '8.3', 'operation': 'other_op', 'position': 'mapara', 'optional': True}),
    "8.3.27": _fx_pair({'range': '8.3', 'operation': 'pratisedha', 'pratisedha': 'na', 'position': 'napara'}, {'range': '8.3', 'operation': 'other_op', 'pratisedha': 'na', 'position': 'napara'}),
    "8.3.28": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'environment': 'śari'}, {'range': '8.3', 'operation': 'other_op', 'environment': 'śari'}),
    "8.3.29": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.30": _fx_pair({'range': '8.3', 'operation': 'pratisedha', 'pratisedha': 'na'}, {'range': '8.3', 'operation': 'other_op', 'pratisedha': 'na'}),
    "8.3.31": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.32": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'rule_strength': 'nitya', 'optional': True, 'visarga_context': True}, {'range': '8.3', 'operation': 'other_op', 'rule_strength': 'nitya', 'optional': True, 'visarga_context': True}),
    "8.3.33": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'optional': True}, {'range': '8.3', 'operation': 'other_op', 'optional': True}),
    "8.3.34": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'substitute': 's', 'visarga_context': True, 'left': 'antaḥ', 'right': 'śiva', 'sandhi_rule': 'visarga-sibilant'}, {'range': '8.3', 'operation': 'sandhi', 'substitute': 'other_sub', 'visarga_context': True, 'left': 'antaḥ', 'right': 'śiva', 'sandhi_rule': 'visarga-sibilant'}),
    "8.3.35": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'visarga_context': True, 'left': 'devaḥ', 'right': 'śrī', 'sandhi_rule': 'visarga-sibilant'}, {'range': '8.3', 'operation': 'other_op', 'visarga_context': True, 'left': 'devaḥ', 'right': 'śrī', 'sandhi_rule': 'visarga-sibilant'}),
    "8.3.36": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'environment': 'śari', 'optional': True}, {'range': '8.3', 'operation': 'other_op', 'environment': 'śari', 'optional': True}),
    "8.3.37": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.38": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.39": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.40": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'stem': 'namas', 'suffix_class': 'gati'}, {'range': '8.3', 'operation': 'sandhi', 'stem': 'other_stem', 'suffix_class': 'gati'}),
    "8.3.41": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'pratyaya': True}, {'range': '8.3', 'operation': 'other_op', 'pratyaya': True}),
    "8.3.42": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.43": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.44": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.45": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'rule_strength': 'nitya', 'scope': 'samāsa', 'position': 'anuttarapada'}, {'range': '8.3', 'operation': 'sandhi', 'rule_strength': 'nitya', 'scope': 'other_scope', 'position': 'anuttarapada'}),
    "8.3.46": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'visarga_context': True, 'left': 'naraḥ', 'right': 'atra', 'sandhi_rule': 'visarga-vowel'}, {'range': '8.3', 'operation': 'other_op', 'visarga_context': True, 'left': 'naraḥ', 'right': 'atra', 'sandhi_rule': 'visarga-vowel'}),
    "8.3.47": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'scope': 'pada'}, {'range': '8.3', 'operation': 'other_op', 'scope': 'pada'}),
    "8.3.48": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.49": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'domain': 'chandas', 'optional': True}, {'range': '8.3', 'operation': 'sandhi', 'domain': 'other_domain', 'optional': True}),
    "8.3.50": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.51": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.52": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.53": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.54": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'optional': True}, {'range': '8.3', 'operation': 'other_op', 'optional': True}),
    "8.3.55": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'scope': 'apadānta'}, {'range': '8.3', 'operation': 'other_op', 'scope': 'apadānta'}),
    "8.3.56": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.57": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.58": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'visarga_context': True, 'optional': True, 'augment': 'num'}, {'range': '8.3', 'operation': 'sandhi', 'visarga_context': True, 'optional': False, 'augment': 'num'}),
    "8.3.59": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'pratyaya': True}, {'range': '8.3', 'operation': 'other_op', 'pratyaya': True}),
    "8.3.60": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.61": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.62": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.63": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'optional': True}, {'range': '8.3', 'operation': 'other_op', 'optional': True}),
    "8.3.64": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.65": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'upasarga': True}, {'range': '8.3', 'operation': 'other_op', 'upasarga': True}),
    "8.3.66": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.67": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.68": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'optional': True}, {'range': '8.3', 'operation': 'other_op', 'optional': True}),
    "8.3.69": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.70": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.71": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'optional': True}, {'range': '8.3', 'operation': 'other_op', 'optional': True}),
    "8.3.72": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.73": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.74": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.75": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.76": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.77": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'rule_strength': 'nitya'}, {'range': '8.3', 'operation': 'other_op', 'rule_strength': 'nitya'}),
    "8.3.78": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'substitute': 'lu'}, {'range': '8.3', 'operation': 'sandhi', 'substitute': 'other_sub'}),
    "8.3.79": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.80": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.81": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'visarga_context': True}, {'range': '8.3', 'operation': 'other_op', 'visarga_context': True}),
    "8.3.82": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.83": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'visarga_context': True}, {'range': '8.3', 'operation': 'other_op', 'visarga_context': True}),
    "8.3.84": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.85": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.86": _fx_pair({'range': '8.3', 'operation': 'samjna'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.87": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'upasarga': True}, {'range': '8.3', 'operation': 'other_op', 'upasarga': True}),
    "8.3.88": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'environment': 'sup'}, {'range': '8.3', 'operation': 'other_op', 'environment': 'sup'}),
    "8.3.89": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'dhatu': 'snā', 'stem_class': 'nī', 'semantic': 'kauśala'}, {'range': '8.3', 'operation': 'sandhi', 'dhatu': 'snā', 'stem_class': 'other_stem', 'semantic': 'kauśala'}),
    "8.3.90": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.91": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.92": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.93": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.94": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.95": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.96": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.97": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'stem_class': 'gana_8_3_97', 'stem': 'ambā'}, {'range': '8.3', 'operation': 'other_op', 'stem_class': 'gana_8_3_97', 'stem': 'ambā'}),
    "8.3.98": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'stem_class': 'gana_8_3_98', 'stem': 'suṣāma'}, {'range': '8.3', 'operation': 'other_op', 'stem_class': 'gana_8_3_98', 'stem': 'suṣāma'}),
    "8.3.99": _fx_pair({'range': '8.3', 'operation': 'samjna'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.100": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'source': 'nakṣatra', 'optional': True}, {'range': '8.3', 'operation': 'sandhi', 'source': 'nakṣatra', 'optional': False}),
    "8.3.101": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'pratyaya_class': 'taddhita', 'optional': True}, {'range': '8.3', 'operation': 'other_op', 'pratyaya_class': 'taddhita', 'optional': True}),
    "8.3.102": _fx_pair({'range': '8.3', 'operation': 'pratisedha', 'pratisedha': 'na', 'upasarga': 'nis', 'dhatu': 'tap', 'semantic': 'anāsevana'}, {'range': '8.3', 'operation': 'sandhi', 'upasarga': 'nis', 'dhatu': 'tap', 'semantic': 'anāsevana'}),
    "8.3.103": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.104": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'text_class': 'yajus'}, {'range': '8.3', 'operation': 'other_op', 'text_class': 'yajus'}),
    "8.3.105": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'domain': 'chandas'}, {'range': '8.3', 'operation': 'sandhi', 'domain': 'other_domain'}),
    "8.3.106": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.107": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.108": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.109": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.110": _fx_pair({'range': '8.3', 'operation': 'pratisedha', 'pratisedha': 'na'}, {'range': '8.3', 'operation': 'other_op', 'pratisedha': 'na'}),
    "8.3.111": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.112": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.113": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.114": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.115": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.116": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.117": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.118": _fx_pair({'range': '8.3', 'operation': 'sandhi'}, {'range': '8.3', 'operation': 'other_op'}),
    "8.3.119": _fx_pair({'range': '8.3', 'operation': 'sandhi', 'upasarga': 'ni', 'substitute': 'ṭ', 'domain': 'chandas', 'optional': True}, {'range': '8.3', 'operation': 'sandhi', 'upasarga': 'ni', 'substitute': 'ṭ', 'domain': 'other_domain', 'optional': True}),
}

META: dict[str, SutraMeta] = {
    "8.3.1": SutraMeta(_VIDHI, 'मतुवसो रु सम्बुद्धौ छन्दसि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.2": SutraMeta(_VIBHASHA, 'अत्रानुनासिकः पूर्वस्य तु वा ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.3": SutraMeta(_VIDHI, 'आतोऽटि नित्यम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.4": SutraMeta(_VIDHI, 'अनुनासिकात्\u200c परोऽनुस्वारः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.5": SutraMeta(_VIDHI, 'समः सुटि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.6": SutraMeta(_VIDHI, 'पुमः खय्यम्परे ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.7": SutraMeta(_PRATISEDHA, 'नश्छव्यप्रशान् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.8": SutraMeta(_VIDHI, 'उभयथर्क्षु ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.9": SutraMeta(_VIDHI, 'दीर्घादटि समानपदे ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.10": SutraMeta(_PRATISEDHA, 'नॄन् पे ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.11": SutraMeta(_VIDHI, 'स्वतवान् पायौ ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.12": SutraMeta(_VIDHI, 'कानाम्रेडिते ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.13": SutraMeta(_VIDHI, 'ढो ढे लोपः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.14": SutraMeta(_VIDHI, 'रो रि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.15": SutraMeta(_VIDHI, 'खरवसानयोर्विसर्जनीयः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.16": SutraMeta(_VIDHI, 'रोः सुपि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.17": SutraMeta(_VIDHI, 'भोभगोअघोअपूर्वस्य योऽशि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.18": SutraMeta(_VIDHI, 'व्योर्लघुप्रयत्नतरः शाकटायनस्य ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.19": SutraMeta(_VIDHI, 'लोपः शाकल्यस्य ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.20": SutraMeta(_VIDHI, 'ओतो गार्ग्यस्य ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.21": SutraMeta(_VIDHI, 'उञि च पदे ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.22": SutraMeta(_VIDHI, 'हलि सर्वेषाम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.23": SutraMeta(_VIDHI, 'मोऽनुस्वारः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.24": SutraMeta(_PRATISEDHA, 'नश्चापदान्तस्य झलि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.25": SutraMeta(_VIDHI, 'मो राजि समः क्वौ ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.26": SutraMeta(_VIBHASHA, 'हे मपरे वा ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.27": SutraMeta(_PRATISEDHA, 'नपरे नः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.28": SutraMeta(_VIDHI, 'ङ्णोः कुक्टुक् शरि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.29": SutraMeta(_VIDHI, 'डः सि धुट् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.30": SutraMeta(_PRATISEDHA, 'नश्च ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.31": SutraMeta(_VIDHI, 'शि तुक् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.32": SutraMeta(_VIDHI, 'ङमो ह्रस्वादचि ङमुण्नित्यम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.33": SutraMeta(_VIBHASHA, 'मय उञो वो वा ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.34": SutraMeta(_VIDHI, 'विसर्जनीयस्य सः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.35": SutraMeta(_VIDHI, 'शर्परे विसर्जनीयः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.36": SutraMeta(_VIDHI, 'वा शरि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.37": SutraMeta(_VIDHI, 'कुप्वोः XकXपौ च ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.38": SutraMeta(_VIDHI, 'सोऽपदादौ ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.39": SutraMeta(_VIDHI, 'इणः षः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.40": SutraMeta(_VIDHI, 'नमस्पुरसोर्गत्योः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.41": SutraMeta(_VIDHI, 'इदुदुपधस्य चाप्रत्ययस्य ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.42": SutraMeta(_VIDHI, 'तिरसोऽन्यतरस्याम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.43": SutraMeta(_VIDHI, 'द्विस्त्रिश्चतुरिति कृत्वोऽर्थे ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.44": SutraMeta(_VIDHI, 'इसुसोः सामर्थ्ये ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.45": SutraMeta(_VIDHI, 'नित्यं समासेऽनुत्तरपदस्थस्य ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.46": SutraMeta(_VIDHI, 'अतः कृकमिकंसकुम्भपात्रकुशाकर्णीष्वनव्ययस्य ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.47": SutraMeta(_VIDHI, 'अधःशिरसी पदे ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.48": SutraMeta(_VIDHI, 'कस्कादिषु च ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.49": SutraMeta(_VIDHI, 'छन्दसि वाऽप्राम्रेडितयोः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.50": SutraMeta(_VIDHI, 'कःकरत्करतिकृधिकृतेष्वनदितेः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.51": SutraMeta(_VIDHI, 'पञ्चम्याः परावध्यर्थे ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.52": SutraMeta(_VIDHI, 'पातौ च बहुलम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.53": SutraMeta(_VIDHI, 'षष्ठ्याः पतिपुत्रपृष्ठपारपदपयस्पोषेषु ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.54": SutraMeta(_VIBHASHA, 'इडाया वा ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.55": SutraMeta(_VIDHI, 'अपदान्तस्य मूर्धन्यः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.56": SutraMeta(_VIDHI, 'सहेः साडः सः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.57": SutraMeta(_VIDHI, 'इण्कोः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.58": SutraMeta(_VIBHASHA, 'नुम्विसर्जनीयशर्व्यवायेऽपि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.59": SutraMeta(_VIDHI, 'आदेशप्रत्यययोः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.60": SutraMeta(_VIDHI, 'शासिवसिघसीनां च ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.61": SutraMeta(_VIDHI, 'स्तौतिण्योरेव षण्यभ्यासात्\u200c ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.62": SutraMeta(_VIDHI, 'सः स्विदिस्वदिसहीनां च ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.63": SutraMeta(_VIDHI, 'प्राक्सितादड्व्यवायेऽपि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.64": SutraMeta(_VIDHI, 'स्थाऽऽदिष्वभ्यासेन चाभ्यासय ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.65": SutraMeta(_VIDHI, 'उपसर्गात्\u200c सुनोतिसुवतिस्यतिस्तौतिस्तोभतिस्थासेनयसेधसिचसञ्जस्वञ्जाम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.66": SutraMeta(_VIDHI, 'सदिरप्रतेः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.67": SutraMeta(_VIDHI, 'स्तम्भेः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.68": SutraMeta(_VIDHI, 'अवाच्चालम्बनाविदूर्ययोः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.69": SutraMeta(_VIDHI, 'वेश्च स्वनो भोजने ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.70": SutraMeta(_VIDHI, 'परिनिविभ्यः सेवसितसयसिवुसहसुट्स्तुस्वञ्जाम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.71": SutraMeta(_VIDHI, 'सिवादीनां वाऽड्व्यवायेऽपि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.72": SutraMeta(_VIDHI, 'अनुविपर्यभिनिभ्यः स्यन्दतेरप्राणिषु ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.73": SutraMeta(_VIDHI, 'वेः स्कन्देरनिष्ठायाम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.74": SutraMeta(_VIDHI, 'परेश्च ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.75": SutraMeta(_VIDHI, 'परिस्कन्दः प्राच्यभरतेषु ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.76": SutraMeta(_VIDHI, 'स्फुरतिस्फुलत्योर्निर्निविभ्यः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.77": SutraMeta(_VIDHI, 'वेः स्कभ्नातेर्नित्यम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.78": SutraMeta(_VIDHI, 'इणः षीध्वंलुङ्\u200cलिटां धोऽङ्गात्\u200c ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.79": SutraMeta(_VIDHI, 'विभाषेटः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.80": SutraMeta(_VIDHI, 'समासेऽङ्गुलेः सङ्गः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.81": SutraMeta(_VIDHI, 'भीरोः स्थानम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.82": SutraMeta(_VIDHI, 'अग्नेः स्तुत्स्तोमसोमाः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.83": SutraMeta(_VIDHI, 'ज्योतिरायुषः स्तोमः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.84": SutraMeta(_VIDHI, 'मातृपितृभ्यां स्वसा ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.85": SutraMeta(_VIDHI, 'मातुःपितुर्भ्यामन्यतरस्याम्\u200c ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.86": SutraMeta(_SAMJNA, 'अभिनिसः स्तनः शब्दसंज्ञायाम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.87": SutraMeta(_VIDHI, 'उपसर्गप्रादुर्भ्यामस्तिर्यच्परः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.88": SutraMeta(_VIDHI, 'सुविनिर्दुर्भ्यः सुपिसूतिसमाः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.89": SutraMeta(_VIDHI, 'निनदीभ्यां स्नातेः कौशले ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.90": SutraMeta(_VIDHI, 'सूत्रं प्रतिष्णातम्\u200c ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.91": SutraMeta(_VIDHI, 'कपिष्ठलो गोत्रे ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.92": SutraMeta(_VIDHI, 'प्रष्ठोऽग्रगामिनि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.93": SutraMeta(_VIDHI, 'वृक्षासनयोर्विष्टरः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.94": SutraMeta(_VIDHI, 'छन्दोनाम्नि च ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.95": SutraMeta(_VIDHI, 'गवियुधिभ्यां स्थिरः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.96": SutraMeta(_VIDHI, 'विकुशमिपरिभ्यः स्थलम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.97": SutraMeta(_VIDHI, 'अम्बाम्बगोभूमिसव्यापद्वित्रिकुशेकुशङ्क्वङ्गुमञ्जिपुञ्जिपरमेबर्हिर्दिव्यग्निभ्यः स्थः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.98": SutraMeta(_VIDHI, 'सुषामादिषु च ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.99": SutraMeta(_SAMJNA, 'ऐति संज्ञायामगात्\u200c ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.100": SutraMeta(_VIBHASHA, 'नक्षत्राद्वा ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.101": SutraMeta(_VIDHI, 'ह्रस्वात्\u200c तादौ तद्धिते ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.102": SutraMeta(_PRATISEDHA, 'निसस्तपतावनासेवने ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.103": SutraMeta(_VIDHI, 'युष्मत्तत्ततक्षुःष्वन्तःपादम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.104": SutraMeta(_VIDHI, 'यजुष्येकेषाम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.105": SutraMeta(_VIDHI, 'स्तुतस्तोमयोश्छन्दसि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.106": SutraMeta(_VIDHI, 'पूर्वपदात्\u200c ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.107": SutraMeta(_VIDHI, 'सुञः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.108": SutraMeta(_VIDHI, 'सनोतेरनः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.109": SutraMeta(_VIDHI, 'सहेः पृतनर्ताभ्यां च ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.110": SutraMeta(_PRATISEDHA, 'न रपरसृपिसृजिस्पृशिस्पृहिसवनादीनाम् ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.111": SutraMeta(_VIDHI, 'सात्पदाद्योः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.112": SutraMeta(_VIDHI, 'सिचो यङि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.113": SutraMeta(_VIDHI, 'सेधतेर्गतौ ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.114": SutraMeta(_VIDHI, 'प्रतिस्तब्धनिस्तब्धौ च ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.115": SutraMeta(_VIDHI, 'सोढः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.116": SutraMeta(_VIDHI, 'स्तम्भुसिवुसहां चङि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.117": SutraMeta(_VIDHI, 'सुनोतेः स्यसनोः ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.118": SutraMeta(_VIDHI, 'सदिष्वञ्जोः परस्य लिटि ।', ("domain:samhita_sandhi", "pada:8.3")),
    "8.3.119": SutraMeta(_VIBHASHA, 'निव्यभिभ्योऽड्व्यावये वा छन्दसि ।', ("domain:samhita_sandhi", "pada:8.3")),
}

def self_check() -> dict[str, int]:
    """Verify every predicate accepts its positive fixture and rejects its negative."""
    failures: list[str] = []
    for sid in sorted(FIXTURES):
        pred = handler_for(sid)
        if not pred(positive_features(sid)):
            failures.append(f"{sid}: rejected positive")
        if pred(negative_features(sid)):
            failures.append(f"{sid}: accepted negative")
    if failures:
        raise AssertionError("sutra_impl_8_3 self_check failed:\n" + "\n".join(failures))
    return {
        "sutras": len(FIXTURES),
        "predicates": len([n for n in globals() if n.startswith("sutra_8_3_")]),
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
    for label, value in counts.items():
        print(f"{label}: {value}")
