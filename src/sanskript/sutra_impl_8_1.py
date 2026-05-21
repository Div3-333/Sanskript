"""
Discrete Pāṇinian predicates for Adhyāya 8.1 (74 sūtras).

Hand-written per sūtra from data/ashtadhyayi_sutras.json. Domain:
samāsānta, dvigu/dvandva accent, āmreḍita, pada-level accent,
and yuṣmad/asmad pratyaya behavior (pada 8.1).
"""
from __future__ import annotations

from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api, _predicate_name


_SAMJNA = 'samjna'
_PARIBHASHA = 'paribhasha'
_VIDHI = 'vidhi'
_PRATISEDHA = 'pratisedha'
_VIBHASHA = 'vibhasha'
_ATIDESA = 'atidesa'

GANA_8_1_8 = frozenset({'asūyā', 'bhartṣana', 'kopa', 'kutsana', 'sammati'})
GANA_8_1_15 = frozenset({'abhivyakti', 'maryādā', 'prayoga', 'rahasya', 'vacana', 'vyutkramaṇa', 'yajñapātra'})
GANA_8_1_57 = frozenset({'ca', 'dhita', 'gotrādi', 'id', 'iva', 'na', 'tad', 'āmreḍita'})

def sutra_8_1_1(c) -> bool:
    """In dvigu compounds, dual inflection applies to the whole compound (both members).

    Padaccheda terms:
    - सर्वस्य
    - ६/१
    - द्वे
    - १/२
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'compound_type', 'dvigu')
        and _eq(c, 'inflection', 'dvivacana')
        and _eq(c, 'member_role', 'sarvam')
    )


def sutra_8_1_2(c) -> bool:
    """The final member of an āmreḍita is named paramāmreḍita.

    Padaccheda terms:
    - तस्य
    - ६/१
    - परम्
    - १/१
    - आम्रेडितम्
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'assigns_samjna', 'paramāmreḍita')
        and _eq(c, 'compound_type', 'āmreḍita')
        and _eq(c, 'member_role', 'para')
    )


def sutra_8_1_3(c) -> bool:
    """Also applies to anudātta (continues from prior accent rule).

    Padaccheda terms:
    - अनुदात्तम्
    - १/१
    - ०/०
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'accent', 'anudātta')
        and _eq(c, 'also', True)
        and _eq(c, 'compound_type', 'āmreḍita')
    )


def sutra_8_1_4(c) -> bool:
    """Dual in contexts of nitya and vīpsā (repetition).

    Padaccheda terms:
    - नित्यवीप्सयोः
    - ७/२
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'inflection', 'dvivacana')
        and _in(c, 'semantic', {'nitya', 'vīpsā'})
    )


def sutra_8_1_5(c) -> bool:
    """Excludes the final (para) member from the dual rule.

    Padaccheda terms:
    - परेः
    - ६/१
    - वर्जने
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'member_role', 'para')
        and _eq(c, 'rule_blocked', True)
        and _eq(c, 'inflection', 'dvivacana')
    )


def sutra_8_1_6(c) -> bool:
    """pr/sam/up/ud take dual when completing a pāda (pādapūraṇa).

    Padaccheda terms:
    - प्रसमुपोदः
    - ६/१
    - पादपूरणे
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _in(c, 'prefix', {'pra', 'sam', 'ud', 'upa'})
        and _eq(c, 'semantic', 'pādapūraṇa')
        and _eq(c, 'inflection', 'dvivacana')
    )


def sutra_8_1_7(c) -> bool:
    """upari/adhi/adhas take dual in proximity (sāmīpya) sense.

    Padaccheda terms:
    - उपर्यध्यधसः
    - ६/१
    - सामीप्ये
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _in(c, 'stem', {'adhas', 'adhi', 'upari'})
        and _eq(c, 'semantic', 'sāmīpya')
        and _eq(c, 'inflection', 'dvivacana')
    )


def sutra_8_1_8(c) -> bool:
    """Sentence etc. with āmreḍita in asūyā/sammati/kopa/kutsana/bhartṣana.

    Padaccheda terms:
    - वाक्यादेः
    - ६/१
    - आमन्त्रितस्य
    - ६/१
    - असूयासम्मतिकोपकुत्सनभर्त्सनेषु
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'syntactic_unit', 'vākyādi')
        and _eq(c, 'compound_type', 'āmreḍita')
        and _in(c, 'semantic', GANA_8_1_8)
    )


def sutra_8_1_9(c) -> bool:
    """Single (eka) is treated like bahuvrīhi (atideśa).

    Padaccheda terms:
    - एकम्
    - १/१
    - बहुव्रीहिवत्
    - ०/०
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'atidesha', 'bahuvrīhi')
        and _eq(c, 'semantic', 'eka')
        and _eq(c, 'compound_type', 'dvandva')
    )


def sutra_8_1_10(c) -> bool:
    """Also in ābādha (obstruction) sense.

    Padaccheda terms:
    - आबाधे
    - ७/१
    - ०/०
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'semantic', 'ābādha')
        and _eq(c, 'also', True)
        and _eq(c, 'inflection', 'dvivacana')
    )


def sutra_8_1_11(c) -> bool:
    """In following (uttara) rules, treat like karmadhāraya (atideśa).

    Padaccheda terms:
    - कर्मधारयवत्
    - ०/०
    - उत्तरेषु
    - ७/३
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'atidesha', 'karmadhāraya')
        and _eq(c, 'scope', 'uttareṣu')
        and _eq(c, 'compound_type', 'dvandva')
    )


def sutra_8_1_12(c) -> bool:
    """In prakāra (manner), guṇavācana takes dual.

    Padaccheda terms:
    - प्रकारे
    - ७/१
    - गुणवचनस्य
    - ६/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'semantic', 'prakāra')
        and _eq(c, 'stem_class', 'guṇavācana')
        and _eq(c, 'inflection', 'dvivacana')
    )


def sutra_8_1_13(c) -> bool:
    """In non-difficulty (akṛcchra), optionally with priya or sukha.

    Padaccheda terms:
    - अकृच्छ्रे
    - ७/१
    - प्रियसुखयोः
    - ६/२
    - अन्यतरस्याम्
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'semantic', 'akṛcchra')
        and _in(c, 'stem', {'priya', 'sukha'})
        and _eq(c, 'optional', True)
    )


def sutra_8_1_14(c) -> bool:
    """yathāsva takes yathāyatham; yathāyatham in yathāsva context.

    Padaccheda terms:
    - यथास्वे
    - ७/१
    - यथायथम्
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'semantic', 'yathāsva')
        and _eq(c, 'form', 'yathāyatham')
        and _eq(c, 'inflection', 'dvivacana')
    )


def sutra_8_1_15(c) -> bool:
    """Dvandva is dual in secret, limit, order, ritual vessel, and expression senses.

    Padaccheda terms:
    - द्वन्द्वम्
    - १/१
    - रहस्यमर्यादावचनव्युत्क्रमणयज्ञपात्रप्रयोगाभिव्यक्तिषु
    - ७/३
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'compound_type', 'dvandva')
        and _eq(c, 'inflection', 'dvivacana')
        and _in(c, 'semantic', GANA_8_1_15)
    )


def sutra_8_1_16(c) -> bool:
    """Adhikāra over pada (word) for accent rules following.

    Padaccheda terms:
    - पदस्य
    - ६/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'adhikara', 'pada')
        and _eq(c, 'range', '8.1')
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_17(c) -> bool:
    """Adhikāra: rules operate from pada (onward).

    Padaccheda terms:
    - पदात्
    - ५/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'adhikara', 'padāt')
        and _eq(c, 'range', '8.1')
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_18(c) -> bool:
    """All is anudātta before non-pāda-initial position (apādādau).

    Padaccheda terms:
    - अनुदात्तम्
    - १/१
    - सर्वम्
    - १/१
    - अपादादौ
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'accent', 'anudātta')
        and _eq(c, 'position', 'apādādau')
        and _eq(c, 'scope', 'sarva')
    )


def sutra_8_1_19(c) -> bool:
    """Also for āmreḍita (continues anudātta rule).

    Padaccheda terms:
    - आमन्त्रितस्य
    - ६/१
    - ०/०
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'compound_type', 'āmreḍita')
        and _eq(c, 'accent', 'anudātta')
        and _eq(c, 'also', True)
    )


def sutra_8_1_20(c) -> bool:
    """yuṣmad/asmad: ṣaṣṭhī/caturthī/dvitīyā/sthā take vā/nau in dual.

    Padaccheda terms:
    - युष्मदस्मदोः
    - ६/२
    - षष्ठीचतुर्थीद्वितीयास्थयोः
    - ६/२
    - वान्नावौ
    """
    return (
        _eq(c, 'range', '8.1')
        and _in(c, 'stem', {'asmad', 'yuṣmad'})
        and _in(c, 'case', {'caturthī', 'dvitīyā', 'sthāna', 'ṣaṣṭhī'})
        and _eq(c, 'inflection', 'dvivacana')
        and _in(c, 'ending', {'nau', 'vā'})
    )


def sutra_8_1_21(c) -> bool:
    """In plural (bahuvacana), vas/nas endings apply.

    Padaccheda terms:
    - बहुवचनस्य
    - ६/१
    - वस्नसौ
    - १/२
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'inflection', 'bahuvacana')
        and _in(c, 'ending', {'nas', 'vas'})
        and _in(c, 'stem', {'asmad', 'yuṣmad'})
    )


def sutra_8_1_22(c) -> bool:
    """In singular, te/mayo endings for yuṣmad/asmad.

    Padaccheda terms:
    - तेमयौ
    - १/२
    - एकवचनस्य
    - ६/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'inflection', 'ekavacana')
        and _in(c, 'ending', {'mayo', 'te'})
        and _in(c, 'stem', {'asmad', 'yuṣmad'})
    )


def sutra_8_1_23(c) -> bool:
    """tvāmau are dvitīyā (accusative) endings.

    Padaccheda terms:
    - त्वामौ
    - १/२
    - द्वितीयायाः
    - ६/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _in(c, 'ending', {'au', 'tvām'})
        and _eq(c, 'case', 'dvitīyā')
        and _in(c, 'stem', {'asmad', 'yuṣmad'})
    )


def sutra_8_1_24(c) -> bool:
    """Not when ca/vā/hā/ha/eva are connected (ca-vādi).

    Padaccheda terms:
    - ०/०
    - चवाहाहैवयुक्ते
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'rule_blocked', True)
        and _in(c, 'connected', {'ca', 'eva', 'ha', 'hā', 'vā'})
        and _in(c, 'stem', {'asmad', 'yuṣmad'})
    )


def sutra_8_1_25(c) -> bool:
    """With paśya-meaning roots and non-reflection (anālocana).

    Padaccheda terms:
    - पश्यार्थैः
    - ३/१
    - ०/०
    - अनालोचने
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'semantic', 'anālocana')
        and _eq(c, 'root_class', 'paśyārtha')
        and _eq(c, 'inflection', 'dvivacana')
    )


def sutra_8_1_26(c) -> bool:
    """Optional first (prathamā) when preceded by sa- (sapūrvā).

    Padaccheda terms:
    - सपूर्वायाः
    - ५/१
    - प्रथमायाः
    - ५/१
    - विभाषा
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'case', 'prathamā')
        and _eq(c, 'prefix', 'sa')
        and _eq(c, 'optional', True)
    )


def sutra_8_1_27(c) -> bool:
    """tiṅ before gotra-etc. in contempt/frequency (kutsana/abhīkṣṇya).

    Padaccheda terms:
    - तिङः
    - ५/१
    - गोत्रादीनि
    - १/३
    - कुत्सनाभीक्ष्ण्ययोः
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'suffix_class', 'tiṅ')
        and _eq(c, 'stem_class', 'gotrādi')
        and _in(c, 'semantic', {'abhīkṣṇya', 'kutsana'})
    )


def sutra_8_1_28(c) -> bool:
    """tiṅ after atiṅ (secondary tiṅ derivation).

    Padaccheda terms:
    - तिङ्
    - १/१
    - अतिङः
    - ५/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'suffix_class', 'tiṅ')
        and _eq(c, 'following', 'atiṅ')
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_29(c) -> bool:
    """Not for luṭ (periphrastic future).

    Padaccheda terms:
    - ०/०
    - लुट्
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'lakara', 'luṭ')
        and _eq(c, 'rule_blocked', True)
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_30(c) -> bool:
    """Nipāta yad/yad/ih/ant/ku/vin/na/ce/ccaṇ/ka/ccid/ya/tra combinations.

    Padaccheda terms:
    - निपातैः
    - ३/३
    - यद्यदिहन्तकुविन्नेच्चेच्चण्कच्चिद्यत्रयुक्तम्
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'nipata_set', 'yadyadihantakuvinnecceccankaccidyatra')
        and _eq(c, 'domain', 'accent')
        and _eq(c, 'connected', True)
    )


def sutra_8_1_31(c) -> bool:
    """naḥ is not used at the start of an utterance (pratyārambha).

    Padaccheda terms:
    - नह
    - ०/०
    - प्रत्यारम्भे
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'nipata', 'nah')
        and _eq(c, 'position', 'pratyārambha')
        and _eq(c, 'rule_blocked', True)
    )


def sutra_8_1_32(c) -> bool:
    """satyam in question (praśna) context.

    Padaccheda terms:
    - सत्यम्
    - १/१
    - प्रश्ने
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'form', 'satyam')
        and _eq(c, 'semantic', 'praśna')
        and _eq(c, 'accent', 'anudātta')
    )


def sutra_8_1_33(c) -> bool:
    """aṅga in non-prātilomya (not reverse order) sense.

    Padaccheda terms:
    - अङ्ग
    - ०/०
    - अप्रातिलोम्ये
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'nipata', 'aṅga')
        and _eq(c, 'semantic', 'aprātilomya')
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_34(c) -> bool:
    """Also hi (continues prior nipāta rule).

    Padaccheda terms:
    - हि
    - ०/०
    - ०/०
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'nipata', 'hi')
        and _eq(c, 'also', True)
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_35(c) -> bool:
    """In chandas, even non-single (aneka) may be sākāṅkṣa.

    Padaccheda terms:
    - छन्दसि
    - ७/१
    - अनेकम्
    - १/१
    - अपि
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'domain', 'chandas')
        and _eq(c, 'semantic', 'sākāṅkṣa')
        and _eq(c, 'scope', 'aneka')
    )


def sutra_8_1_36(c) -> bool:
    """yāvat and yathā (instrumental/ablative pair) accent rule.

    Padaccheda terms:
    - यावद्यथाभ्याम्
    - ३/२
    """
    return (
        _eq(c, 'range', '8.1')
        and _in(c, 'stem', {'yathā', 'yāvat'})
        and _eq(c, 'case', 'instrumental_ablative')
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_37(c) -> bool:
    """In praise (pūjā), not immediately after (anantaram).

    Padaccheda terms:
    - पूजायाम्
    - ७/१
    - ०/०
    - अनन्तरम्
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'semantic', 'pūjā')
        and _eq(c, 'relation', 'anantaram')
        and _eq(c, 'rule_blocked', True)
    )


def sutra_8_1_38(c) -> bool:
    """Also when upasarga is separated (vyapeta).

    Padaccheda terms:
    - उपसर्गव्यपेतम्
    - १/१
    - ०/०
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'upasarga', 'vyapeta')
        and _eq(c, 'also', True)
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_39(c) -> bool:
    """tu/paśya/paśyata/āhā in praise (pūjā).

    Padaccheda terms:
    - तुपश्यपश्यताहैः
    - ३/३
    - पूजायाम्
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _in(c, 'nipata', {'paśya', 'paśyata', 'tu', 'āhā'})
        and _eq(c, 'semantic', 'pūjā')
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_40(c) -> bool:
    """Also aho (continues nipāta accent rules).

    Padaccheda terms:
    - अहो
    - ०/०
    - ०/०
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'nipata', 'aho')
        and _eq(c, 'also', True)
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_41(c) -> bool:
    """Optional (vibhāṣā) in remaining (śeṣa) contexts.

    Padaccheda terms:
    - शेषे
    - ७/१
    - विभाषा
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'scope', 'śeṣa')
        and _eq(c, 'optional', True)
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_42(c) -> bool:
    """Also purā in desire to surpass (parīpsā).

    Padaccheda terms:
    - पुरा
    - ०/०
    - ०/०
    - परीप्सायाम्
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'nipata', 'purā')
        and _eq(c, 'semantic', 'parīpsā')
        and _eq(c, 'also', True)
    )


def sutra_8_1_43(c) -> bool:
    """nanu/iti in permission/inquiry (anujñā/eṣaṇā).

    Padaccheda terms:
    - ननु
    - ०/०
    - ०/०
    - अनुज्ञैषणायाम्
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _in(c, 'nipata', {'iti', 'nanu'})
        and _in(c, 'semantic', {'anujñā', 'eṣaṇā'})
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_44(c) -> bool:
    """kim in verbal question, without upasarga, not forbidden.

    Padaccheda terms:
    - किम्
    - १/१
    - क्रियाप्रश्ने
    - ७/१
    - अनुपसर्गम्
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'nipata', 'kim')
        and _eq(c, 'semantic', 'kriyāpraśna')
        and _eq(c, 'has_upasarga', False)
        and _eq(c, 'rule_blocked', False)
    )


def sutra_8_1_45(c) -> bool:
    """Optional when lopa (deletion) is involved.

    Padaccheda terms:
    - लोपे
    - ७/१
    - विभाषा
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'operation', 'lopa')
        and _eq(c, 'optional', True)
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_46(c) -> bool:
    """ehi/manye in jest (prahāsa) take lṛṭ.

    Padaccheda terms:
    - एहिमन्ये
    - प्रहासे
    - ७/१
    - लृट्
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _in(c, 'stem', {'ehi', 'manye'})
        and _eq(c, 'semantic', 'prahāsa')
        and _eq(c, 'lakara', 'lṛṭ')
    )


def sutra_8_1_47(c) -> bool:
    """jātu is not initial (apūrva) in the utterance.

    Padaccheda terms:
    - जातु
    - ०/०
    - अपूर्वम्
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'nipata', 'jātu')
        and _eq(c, 'position', 'apūrva')
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_48(c) -> bool:
    """kimvṛttam and cid follow uttara (posterior).

    Padaccheda terms:
    - किम्वृत्तम्
    - १/१
    - ०/०
    - चिदुत्तरम्
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _in(c, 'form', {'cid', 'kimvṛttam'})
        and _eq(c, 'relation', 'uttara')
        and _eq(c, 'also', True)
    )


def sutra_8_1_49(c) -> bool:
    """āho/utāho are not immediately consecutive (anantaram).

    Padaccheda terms:
    - आहो
    - ०/०
    - उताहो
    - ०/०
    - ०/०
    """
    return (
        _eq(c, 'range', '8.1')
        and _in(c, 'nipata', {'utāho', 'āho'})
        and _eq(c, 'relation', 'anantaram')
        and _eq(c, 'rule_blocked', True)
    )


def sutra_8_1_50(c) -> bool:
    """Optional in remaining (śeṣa) nipāta contexts.

    Padaccheda terms:
    - शेषे
    - ७/१
    - विभाषा
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'scope', 'śeṣa')
        and _eq(c, 'optional', True)
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_51(c) -> bool:
    """Motion-meaning lot: lṛṭ not when all kārakas are present.

    Padaccheda terms:
    - गत्यर्थलोटा
    - ३/१
    - लृट्
    - १/१
    - ०/०
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'semantic', 'gati')
        and _eq(c, 'lakara', 'lot')
        and _eq(c, 'karaka_complete', False)
    )


def sutra_8_1_52(c) -> bool:
    """Also lot (continues gati rule).

    Padaccheda terms:
    - लोट्
    - १/१
    - ०/०
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'lakara', 'lot')
        and _eq(c, 'also', True)
        and _eq(c, 'semantic', 'gati')
    )


def sutra_8_1_53(c) -> bool:
    """Vibhāṣita form with upasarga, not uttama (superlative).

    Padaccheda terms:
    - विभाषितम्
    - १/१
    - सोपसर्गम्
    - १/१
    - अनुत्तमम्
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'marked', 'vibhāṣita')
        and _eq(c, 'has_upasarga', True)
        and _eq(c, 'degree', 'anuttama')
    )


def sutra_8_1_54(c) -> bool:
    """Also hant (continues prior nipāta/lakāra rule).

    Padaccheda terms:
    - हन्त
    - ०/०
    - ०/०
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'nipata', 'hant')
        and _eq(c, 'also', True)
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_55(c) -> bool:
    """ām after single interval is āmreḍita in immediacy (anantike).

    Padaccheda terms:
    - आम
    - ५/१
    - एकान्तरम्
    - १/१
    - आमन्त्रितम्
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'form', 'ām')
        and _eq(c, 'compound_type', 'āmreḍita')
        and _eq(c, 'semantic', 'anantike')
    )


def sutra_8_1_56(c) -> bool:
    """What follows a dhitu (verbal derivative) in chandas.

    Padaccheda terms:
    - यद्धितुपरम्
    - १/१
    - छन्दसि
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'domain', 'chandas')
        and _eq(c, 'following', 'dhitu')
        and _eq(c, 'position', 'para')
    )


def sutra_8_1_57(c) -> bool:
    """ca/na/ca/id/iva/gotra/ādi/tad/dhita/āmreḍita: āgat (came) sense.

    Padaccheda terms:
    - चनचिदिवगोत्रादितद्धिताम्रेडितेषु
    - ७/३
    - आगतेः
    - ५/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _in(c, 'stem_class', GANA_8_1_57)
        and _eq(c, 'semantic', 'āgati')
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_58(c) -> bool:
    """Also in cādi (ca and following nipātas).

    Padaccheda terms:
    - चादिषु
    - ७/३
    - ०/०
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'nipata_class', 'cādi')
        and _eq(c, 'also', True)
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_59(c) -> bool:
    """When ca and vā are together, prathamā (nominative).

    Padaccheda terms:
    - चवायोगे
    - ७/१
    - प्रथमा
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _in(c, 'connected', {'ca', 'vā'})
        and _eq(c, 'case', 'prathamā')
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_60(c) -> bool:
    """he/itī in injury (kṣiyā).

    Padaccheda terms:
    - ह
    - ०/०
    - ०/०
    - क्षियायाम्
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'nipata', 'he')
        and _eq(c, 'particle', 'iti')
        and _eq(c, 'semantic', 'kṣiyā')
    )


def sutra_8_1_61(c) -> bool:
    """Also aho/itī in assignment (viniyoga).

    Padaccheda terms:
    - अह
    - ०/०
    - ०/०
    - विनियोगे
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'nipata', 'aho')
        and _eq(c, 'particle', 'iti')
        and _eq(c, 'semantic', 'viniyoga')
        and _eq(c, 'also', True)
    )


def sutra_8_1_62(c) -> bool:
    """Restriction (avadhāraṇa): cāhalo lopa only with eva.

    Padaccheda terms:
    - चाहलोप
    - ७/१
    - एव
    - ०/०
    - ०/०
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'operation', 'lopa')
        and _eq(c, 'nipata_class', 'cāhalo')
        and _eq(c, 'restrictor', 'eva')
    )


def sutra_8_1_63(c) -> bool:
    """Optional lopa in cādi (ca-initial group).

    Padaccheda terms:
    - चादिलोपे
    - ७/१
    - विभाषा
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'nipata_class', 'cādi')
        and _eq(c, 'operation', 'lopa')
        and _eq(c, 'optional', True)
    )


def sutra_8_1_64(c) -> bool:
    """Also vaivāva/itī in chandas.

    Padaccheda terms:
    - वैवाव
    - ०/०
    - ०/०
    - छन्दसि
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'form', 'vaivāva')
        and _eq(c, 'particle', 'iti')
        and _eq(c, 'domain', 'chandas')
        and _eq(c, 'also', True)
    )


def sutra_8_1_65(c) -> bool:
    """With one other and with capable (samartha) pair.

    Padaccheda terms:
    - एकान्याभ्याम्
    - ३/२
    - समर्थाभ्याम्
    - ३/२
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'relation', 'ekānya')
        and _eq(c, 'semantic', 'samartha')
        and _eq(c, 'compound_type', 'dvandva')
    )


def sutra_8_1_66(c) -> bool:
    """From yadvṛt (relative participle), nitya (always).

    Padaccheda terms:
    - यद्वृतात्
    - ५/१
    - नित्यम्
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'source', 'yadvṛt')
        and _eq(c, 'rule_strength', 'nitya')
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_67(c) -> bool:
    """Honored (pūjita) from worship (pūjana) is anudātta (kāṣṭhādi).

    Padaccheda terms:
    - पूजनात्
    - ५/१
    - पूजितम्
    - १/१
    - अनुदात्तम्
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'source', 'pūjana')
        and _eq(c, 'form', 'pūjita')
        and _eq(c, 'accent', 'anudātta')
    )


def sutra_8_1_68(c) -> bool:
    """Even gati (motion) roots may be treated as tiṅ.

    Padaccheda terms:
    - सगतिः
    - १/१
    - अपि
    - ०/०
    - तिङ्
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'stem_class', 'gati')
        and _eq(c, 'suffix_class', 'tiṅ')
        and _eq(c, 'also', True)
    )


def sutra_8_1_69(c) -> bool:
    """Also in contempt (kutsana) with sup and non-gotra.

    Padaccheda terms:
    - कुत्सने
    - ७/१
    - ०/०
    - सुपि
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'semantic', 'kutsana')
        and _eq(c, 'suffix_class', 'sup')
        and _eq(c, 'stem_class', 'agotrādi')
        and _eq(c, 'also', True)
    )


def sutra_8_1_70(c) -> bool:
    """gati in gati sense (denominal motion).

    Padaccheda terms:
    - गतिः
    - १/१
    - गतौ
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'stem_class', 'gati')
        and _eq(c, 'semantic', 'gati')
        and _eq(c, 'domain', 'accent')
    )


def sutra_8_1_71(c) -> bool:
    """Also tiṅ in udāttavat (udātta-like) context.

    Padaccheda terms:
    - तिङि
    - ७/१
    - ०/०
    - उदात्तवति
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'suffix_class', 'tiṅ')
        and _eq(c, 'accent', 'udāttavat')
        and _eq(c, 'also', True)
    )


def sutra_8_1_72(c) -> bool:
    """Prior āmreḍita treated as non-existent (avidyamānavat atideśa).

    Padaccheda terms:
    - आमन्त्रितम्
    - १/१
    - पूर्वम्
    - १/१
    - अविद्यमानवत्
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'atidesha', 'avidyamānavat')
        and _eq(c, 'compound_type', 'āmreḍita')
        and _eq(c, 'member_role', 'pūrva')
    )


def sutra_8_1_73(c) -> bool:
    """Not āmreḍita in co-referential (samānādhikaraṇa) context.

    Padaccheda terms:
    - ०/०
    - आमन्त्रिते
    - ७/१
    - समानाधिकरणे
    - ७/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'compound_type', 'āmreḍita')
        and _eq(c, 'semantic', 'samānādhikaraṇa')
        and _eq(c, 'rule_blocked', True)
    )


def sutra_8_1_74(c) -> bool:
    """Optional plural (bahuvacana) in viśeṣavacana (specific number).

    Padaccheda terms:
    - (सामान्यवचनम्
    - १/१
    - )
    - विभाषितम्
    - १/१
    """
    return (
        _eq(c, 'range', '8.1')
        and _eq(c, 'optional', True)
        and _eq(c, 'semantic', 'viśeṣavacana')
        and _eq(c, 'inflection', 'bahuvacana')
    )


def _fx(pos: dict, neg: dict) -> tuple[dict, dict]:
    return (pos, neg)


FIXTURES: dict[str, tuple[dict, dict]] = {

    "8.1.1": _fx(

        {'compound_type': 'dvigu', 'inflection': 'dvivacana', 'member_role': 'sarvam', 'range': '8.1'},

        # neg: wrong vacana for dvigu sarvasya dve

        {'compound_type': 'dvigu', 'inflection': 'ekavacana', 'member_role': 'sarvam', 'range': '8.1'},

    ),

    "8.1.2": _fx(

        {'assigns_samjna': 'paramāmreḍita', 'compound_type': 'āmreḍita', 'member_role': 'para', 'range': '8.1'},

        # neg: samjna targets non-final member

        {'assigns_samjna': 'paramāmreḍita', 'compound_type': 'āmreḍita', 'member_role': 'pūrva', 'range': '8.1'},

    ),

    "8.1.3": _fx(

        {'accent': 'anudātta', 'also': True, 'compound_type': 'āmreḍita', 'range': '8.1'},

        # neg: not anudātta accent

        {'accent': 'udātta', 'also': True, 'compound_type': 'āmreḍita', 'range': '8.1'},

    ),

    "8.1.4": _fx(

        {'inflection': 'dvivacana', 'range': '8.1', 'semantic': 'nitya'},

        # neg: outside nityavīpsā semantic scope

        {'inflection': 'dvivacana', 'range': '8.1', 'semantic': 'ekakāla'},

    ),

    "8.1.5": _fx(

        {'inflection': 'dvivacana', 'member_role': 'para', 'range': '8.1', 'rule_blocked': True},

        # neg: para not blocked from dual

        {'inflection': 'dvivacana', 'member_role': 'para', 'range': '8.1', 'rule_blocked': False},

    ),

    "8.1.6": _fx(

        {'inflection': 'dvivacana', 'prefix': 'pra', 'range': '8.1', 'semantic': 'pādapūraṇa'},

        # neg: not pādapūraṇa context

        {'inflection': 'dvivacana', 'prefix': 'pra', 'range': '8.1', 'semantic': 'arthavāda'},

    ),

    "8.1.7": _fx(

        {'inflection': 'dvivacana', 'range': '8.1', 'semantic': 'sāmīpya', 'stem': 'adhas'},

        # neg: not sāmīpya sense

        {'inflection': 'dvivacana', 'range': '8.1', 'semantic': 'kālānvaya', 'stem': 'adhas'},

    ),

    "8.1.8": _fx(

        {'compound_type': 'āmreḍita', 'range': '8.1', 'semantic': 'asūyā', 'syntactic_unit': 'vākyādi'},

        # neg: wrong emotion semantic for vākyādi rule

        {'compound_type': 'āmreḍita', 'range': '8.1', 'semantic': 'praśaṃsā', 'syntactic_unit': 'vākyādi'},

    ),

    "8.1.9": _fx(

        {'atidesha': 'bahuvrīhi', 'compound_type': 'dvandva', 'range': '8.1', 'semantic': 'eka'},

        # neg: wrong atideśa compound model

        {'atidesha': 'tatpuruṣa', 'compound_type': 'dvandva', 'range': '8.1', 'semantic': 'eka'},

    ),

    "8.1.10": _fx(

        {'also': True, 'inflection': 'dvivacana', 'range': '8.1', 'semantic': 'ābādha'},

        # neg: not ābādha semantic

        {'also': True, 'inflection': 'dvivacana', 'range': '8.1', 'semantic': 'sāmīpya'},

    ),

    "8.1.11": _fx(

        {'atidesha': 'karmadhāraya', 'compound_type': 'dvandva', 'range': '8.1', 'scope': 'uttareṣu'},

        # neg: wrong atideśa for uttareṣu

        {'atidesha': 'bahuvrīhi', 'compound_type': 'dvandva', 'range': '8.1', 'scope': 'uttareṣu'},

    ),

    "8.1.12": _fx(

        {'inflection': 'dvivacana', 'range': '8.1', 'semantic': 'prakāra', 'stem_class': 'guṇavācana'},

        # neg: not guṇavācana stem

        {'inflection': 'dvivacana', 'range': '8.1', 'semantic': 'prakāra', 'stem_class': 'saṃkhyā'},

    ),

    "8.1.13": _fx(

        {'optional': True, 'range': '8.1', 'semantic': 'akṛcchra', 'stem': 'priya'},

        # neg: vibhāṣā not taken for priya/sukha

        {'optional': False, 'range': '8.1', 'semantic': 'akṛcchra', 'stem': 'priya'},

    ),

    "8.1.14": _fx(

        {'form': 'yathāyatham', 'inflection': 'dvivacana', 'range': '8.1', 'semantic': 'yathāsva'},

        # neg: wrong yathā-correlative form

        {'form': 'yathātatham', 'inflection': 'dvivacana', 'range': '8.1', 'semantic': 'yathāsva'},

    ),

    "8.1.15": _fx(

        {'compound_type': 'dvandva', 'inflection': 'dvivacana', 'range': '8.1', 'semantic': 'abhivyakti'},

        # neg: not dvandva compound

        {'compound_type': 'tatpuruṣa', 'inflection': 'dvivacana', 'range': '8.1', 'semantic': 'abhivyakti'},

    ),

    "8.1.16": _fx(

        {'adhikara': 'pada', 'domain': 'accent', 'range': '8.1'},

        # neg: wrong adhikāra domain

        {'adhikara': 'samāsa', 'domain': 'accent', 'range': '8.1'},

    ),

    "8.1.17": _fx(

        {'adhikara': 'padāt', 'domain': 'accent', 'range': '8.1'},

        # neg: scope not padāt

        {'adhikara': 'vākya', 'domain': 'accent', 'range': '8.1'},

    ),

    "8.1.18": _fx(

        {'accent': 'anudātta', 'position': 'apādādau', 'range': '8.1', 'scope': 'sarva'},

        # neg: not apādādau position

        {'accent': 'anudātta', 'position': 'pādādi', 'range': '8.1', 'scope': 'sarva'},

    ),

    "8.1.19": _fx(

        {'accent': 'anudātta', 'also': True, 'compound_type': 'āmreḍita', 'range': '8.1'},

        # neg: not āmreḍita continuation

        {'accent': 'anudātta', 'also': True, 'compound_type': 'dvandva', 'range': '8.1'},

    ),

    "8.1.20": _fx(

        {'case': 'caturthī', 'ending': 'nau', 'inflection': 'dvivacana', 'range': '8.1', 'stem': 'asmad'},

        # neg: wrong dual ending for yuṣmad/asmad

        {'case': 'caturthī', 'ending': 'bhām', 'inflection': 'dvivacana', 'range': '8.1', 'stem': 'asmad'},

    ),

    "8.1.21": _fx(

        {'ending': 'nas', 'inflection': 'bahuvacana', 'range': '8.1', 'stem': 'asmad'},

        # neg: wrong vacana for vas/nas

        {'ending': 'nas', 'inflection': 'dvivacana', 'range': '8.1', 'stem': 'asmad'},

    ),

    "8.1.22": _fx(

        {'ending': 'mayo', 'inflection': 'ekavacana', 'range': '8.1', 'stem': 'asmad'},

        # neg: wrong singular ending set

        {'ending': 'tvam', 'inflection': 'ekavacana', 'range': '8.1', 'stem': 'asmad'},

    ),

    "8.1.23": _fx(

        {'case': 'dvitīyā', 'ending': 'au', 'range': '8.1', 'stem': 'asmad'},

        # neg: tvāmau not in dvitīyā

        {'case': 'prathama', 'ending': 'au', 'range': '8.1', 'stem': 'asmad'},

    ),

    "8.1.24": _fx(

        {'connected': 'ca', 'range': '8.1', 'rule_blocked': True, 'stem': 'asmad'},

        # neg: ca-vādi block not applied

        {'connected': 'ca', 'range': '8.1', 'rule_blocked': False, 'stem': 'asmad'},

    ),

    "8.1.25": _fx(

        {'inflection': 'dvivacana', 'range': '8.1', 'root_class': 'paśyārtha', 'semantic': 'anālocana'},

        # neg: reflection context blocks rule

        {'inflection': 'dvivacana', 'range': '8.1', 'root_class': 'paśyārtha', 'semantic': 'ālocana'},

    ),

    "8.1.26": _fx(

        {'case': 'prathamā', 'optional': True, 'prefix': 'sa', 'range': '8.1'},

        # neg: vibhāṣā for sapūrvā prathamā not used

        {'case': 'prathamā', 'optional': False, 'prefix': 'sa', 'range': '8.1'},

    ),

    "8.1.27": _fx(

        {'range': '8.1', 'semantic': 'abhīkṣṇya', 'stem_class': 'gotrādi', 'suffix_class': 'tiṅ'},

        # neg: not tiṅ context

        {'range': '8.1', 'semantic': 'abhīkṣṇya', 'stem_class': 'gotrādi', 'suffix_class': 'sup'},

    ),

    "8.1.28": _fx(

        {'domain': 'accent', 'following': 'atiṅ', 'range': '8.1', 'suffix_class': 'tiṅ'},

        # neg: not after atiṅ

        {'domain': 'accent', 'following': 'sup', 'range': '8.1', 'suffix_class': 'tiṅ'},

    ),

    "8.1.29": _fx(

        {'domain': 'accent', 'lakara': 'luṭ', 'range': '8.1', 'rule_blocked': True},

        # neg: block applies to wrong lakāra

        {'domain': 'accent', 'lakara': 'laṭ', 'range': '8.1', 'rule_blocked': True},

    ),

    "8.1.30": _fx(

        {'connected': True, 'domain': 'accent', 'nipata_set': 'yadyadihantakuvinnecceccankaccidyatra', 'range': '8.1'},

        # neg: not listed nipāta cluster

        {'connected': True, 'domain': 'accent', 'nipata_set': 'other', 'range': '8.1'},

    ),

    "8.1.31": _fx(

        {'nipata': 'nah', 'position': 'pratyārambha', 'range': '8.1', 'rule_blocked': True},

        # neg: nah blocked only at pratyārambha

        {'nipata': 'nah', 'position': 'madhya', 'range': '8.1', 'rule_blocked': True},

    ),

    "8.1.32": _fx(

        {'accent': 'anudātta', 'form': 'satyam', 'range': '8.1', 'semantic': 'praśna'},

        # neg: not praśna semantic

        {'accent': 'anudātta', 'form': 'satyam', 'range': '8.1', 'semantic': 'nidāna'},

    ),

    "8.1.33": _fx(

        {'domain': 'accent', 'nipata': 'aṅga', 'range': '8.1', 'semantic': 'aprātilomya'},

        # neg: prātilomya blocks aṅga rule

        {'domain': 'accent', 'nipata': 'aṅga', 'range': '8.1', 'semantic': 'prātilomya'},

    ),

    "8.1.34": _fx(

        {'also': True, 'domain': 'accent', 'nipata': 'hi', 'range': '8.1'},

        # neg: hi continuation not active

        {'also': True, 'domain': 'accent', 'nipata': 'ca', 'range': '8.1'},

    ),

    "8.1.35": _fx(

        {'domain': 'chandas', 'range': '8.1', 'scope': 'aneka', 'semantic': 'sākāṅkṣa'},

        # neg: chandas-only sākāṅkṣa for aneka

        {'domain': 'loka', 'range': '8.1', 'scope': 'aneka', 'semantic': 'sākāṅkṣa'},

    ),

    "8.1.36": _fx(

        {'case': 'instrumental_ablative', 'domain': 'accent', 'range': '8.1', 'stem': 'yathā'},

        # neg: wrong case for yāvad-yathā

        {'case': 'prathama', 'domain': 'accent', 'range': '8.1', 'stem': 'yathā'},

    ),

    "8.1.37": _fx(

        {'range': '8.1', 'relation': 'anantaram', 'rule_blocked': True, 'semantic': 'pūjā'},

        # neg: anantaram not blocked in pūjā

        {'range': '8.1', 'relation': 'anantaram', 'rule_blocked': False, 'semantic': 'pūjā'},

    ),

    "8.1.38": _fx(

        {'also': True, 'domain': 'accent', 'range': '8.1', 'upasarga': 'vyapeta'},

        # neg: upasarga not vyapeta

        {'also': True, 'domain': 'accent', 'range': '8.1', 'upasarga': 'saha'},

    ),

    "8.1.39": _fx(

        {'domain': 'accent', 'nipata': 'paśya', 'range': '8.1', 'semantic': 'pūjā'},

        # neg: not pūjā semantic

        {'domain': 'accent', 'nipata': 'paśya', 'range': '8.1', 'semantic': 'kopa'},

    ),

    "8.1.40": _fx(

        {'also': True, 'domain': 'accent', 'nipata': 'aho', 'range': '8.1'},

        # neg: aho continuation

        {'also': True, 'domain': 'accent', 'nipata': 'ahoḥ', 'range': '8.1'},

    ),

    "8.1.41": _fx(

        {'domain': 'accent', 'optional': True, 'range': '8.1', 'scope': 'śeṣa'},

        # neg: śeṣa vibhāṣā not optional

        {'domain': 'accent', 'optional': False, 'range': '8.1', 'scope': 'śeṣa'},

    ),

    "8.1.42": _fx(

        {'also': True, 'nipata': 'purā', 'range': '8.1', 'semantic': 'parīpsā'},

        # neg: purā not in parīpsā

        {'also': True, 'nipata': 'purā', 'range': '8.1', 'semantic': 'pūrvakāla'},

    ),

    "8.1.43": _fx(

        {'domain': 'accent', 'nipata': 'iti', 'range': '8.1', 'semantic': 'anujñā'},

        # neg: wrong semantic for nanviti

        {'domain': 'accent', 'nipata': 'iti', 'range': '8.1', 'semantic': 'niṣedha'},

    ),

    "8.1.44": _fx(

        {'has_upasarga': False, 'nipata': 'kim', 'range': '8.1', 'rule_blocked': False, 'semantic': 'kriyāpraśna'},

        # neg: not kriyāpraśna for kim

        {'has_upasarga': False, 'nipata': 'kim', 'range': '8.1', 'rule_blocked': False, 'semantic': 'padapraśna'},

    ),

    "8.1.45": _fx(

        {'domain': 'accent', 'operation': 'lopa', 'optional': True, 'range': '8.1'},

        # neg: lopa vibhāṣā not in play

        {'domain': 'accent', 'operation': 'āgama', 'optional': True, 'range': '8.1'},

    ),

    "8.1.46": _fx(

        {'lakara': 'lṛṭ', 'range': '8.1', 'semantic': 'prahāsa', 'stem': 'ehi'},

        # neg: wrong lakāra for prahāsa

        {'lakara': 'lot', 'range': '8.1', 'semantic': 'prahāsa', 'stem': 'ehi'},

    ),

    "8.1.47": _fx(

        {'domain': 'accent', 'nipata': 'jātu', 'position': 'apūrva', 'range': '8.1'},

        # neg: jātu wrongly initial

        {'domain': 'accent', 'nipata': 'jātu', 'position': 'pūrva', 'range': '8.1'},

    ),

    "8.1.48": _fx(

        {'also': True, 'form': 'cid', 'range': '8.1', 'relation': 'uttara'},

        # neg: not uttara position

        {'also': True, 'form': 'cid', 'range': '8.1', 'relation': 'pūrva'},

    ),

    "8.1.49": _fx(

        {'nipata': 'utāho', 'range': '8.1', 'relation': 'anantaram', 'rule_blocked': True},

        # neg: anantaram block missing

        {'nipata': 'utāho', 'range': '8.1', 'relation': 'anantaram', 'rule_blocked': False},

    ),

    "8.1.50": _fx(

        {'domain': 'accent', 'optional': True, 'range': '8.1', 'scope': 'śeṣa'},

        # neg: not śeṣa scope

        {'domain': 'accent', 'optional': True, 'range': '8.1', 'scope': 'prāpta'},

    ),

    "8.1.51": _fx(

        {'karaka_complete': False, 'lakara': 'lot', 'range': '8.1', 'semantic': 'gati'},

        # neg: sarva-kāraka blocks gatyarthalot rule

        {'karaka_complete': True, 'lakara': 'lot', 'range': '8.1', 'semantic': 'gati'},

    ),

    "8.1.52": _fx(

        {'also': True, 'lakara': 'lot', 'range': '8.1', 'semantic': 'gati'},

        # neg: lot continuation

        {'also': True, 'lakara': 'laṭ', 'range': '8.1', 'semantic': 'gati'},

    ),

    "8.1.53": _fx(

        {'degree': 'anuttama', 'has_upasarga': True, 'marked': 'vibhāṣita', 'range': '8.1'},

        # neg: uttama degree blocks rule

        {'degree': 'uttama', 'has_upasarga': True, 'marked': 'vibhāṣita', 'range': '8.1'},

    ),

    "8.1.54": _fx(

        {'also': True, 'domain': 'accent', 'nipata': 'hant', 'range': '8.1'},

        # neg: hant continuation

        {'also': True, 'domain': 'accent', 'nipata': 'hanta', 'range': '8.1'},

    ),

    "8.1.55": _fx(

        {'compound_type': 'āmreḍita', 'form': 'ām', 'range': '8.1', 'semantic': 'anantike'},

        # neg: not anantike āmreḍita

        {'compound_type': 'āmreḍita', 'form': 'ām', 'range': '8.1', 'semantic': 'viprakṛṣṭa'},

    ),

    "8.1.56": _fx(

        {'domain': 'chandas', 'following': 'dhitu', 'position': 'para', 'range': '8.1'},

        # neg: chandas-only yad-dhitu-para

        {'domain': 'loka', 'following': 'dhitu', 'position': 'para', 'range': '8.1'},

    ),

    "8.1.57": _fx(

        {'domain': 'accent', 'range': '8.1', 'semantic': 'āgati', 'stem_class': 'ca'},

        # neg: āgati not gati semantic

        {'domain': 'accent', 'range': '8.1', 'semantic': 'gatyartha', 'stem_class': 'ca'},

    ),

    "8.1.58": _fx(

        {'also': True, 'domain': 'accent', 'nipata_class': 'cādi', 'range': '8.1'},

        # neg: not cādi set

        {'also': True, 'domain': 'accent', 'nipata_class': 'other', 'range': '8.1'},

    ),

    "8.1.59": _fx(

        {'case': 'prathamā', 'connected': 'ca', 'domain': 'accent', 'range': '8.1'},

        # neg: cavāyoge not prathamā

        {'case': 'dvitīyā', 'connected': 'ca', 'domain': 'accent', 'range': '8.1'},

    ),

    "8.1.60": _fx(

        {'nipata': 'he', 'particle': 'iti', 'range': '8.1', 'semantic': 'kṣiyā'},

        # neg: not kṣiyā for he-iti

        {'nipata': 'he', 'particle': 'iti', 'range': '8.1', 'semantic': 'praśaṃsā'},

    ),

    "8.1.61": _fx(

        {'also': True, 'nipata': 'aho', 'particle': 'iti', 'range': '8.1', 'semantic': 'viniyoga'},

        # neg: viniyoga not kṣiyā

        {'also': True, 'nipata': 'aho', 'particle': 'iti', 'range': '8.1', 'semantic': 'kṣiyā'},

    ),

    "8.1.62": _fx(

        {'nipata_class': 'cāhalo', 'operation': 'lopa', 'range': '8.1', 'restrictor': 'eva'},

        # neg: cāhalo lopa without eva avadhāraṇa

        {'nipata_class': 'cāhalo', 'operation': 'lopa', 'range': '8.1', 'restrictor': 'evaṃ'},

    ),

    "8.1.63": _fx(

        {'nipata_class': 'cādi', 'operation': 'lopa', 'optional': True, 'range': '8.1'},

        # neg: cādilopa vibhāṣā not taken

        {'nipata_class': 'cādi', 'operation': 'lopa', 'optional': False, 'range': '8.1'},

    ),

    "8.1.64": _fx(

        {'also': True, 'domain': 'chandas', 'form': 'vaivāva', 'particle': 'iti', 'range': '8.1'},

        # neg: vaivāva chandas-only

        {'also': True, 'domain': 'loka', 'form': 'vaivāva', 'particle': 'iti', 'range': '8.1'},

    ),

    "8.1.65": _fx(

        {'compound_type': 'dvandva', 'range': '8.1', 'relation': 'ekānya', 'semantic': 'samartha'},

        # neg: not samartha pair

        {'compound_type': 'dvandva', 'range': '8.1', 'relation': 'ekānya', 'semantic': 'asamartha'},

    ),

    "8.1.66": _fx(

        {'domain': 'accent', 'range': '8.1', 'rule_strength': 'nitya', 'source': 'yadvṛt'},

        # neg: not nitya from yadvṛt

        {'domain': 'accent', 'range': '8.1', 'rule_strength': 'vibhāṣā', 'source': 'yadvṛt'},

    ),

    "8.1.67": _fx(

        {'accent': 'anudātta', 'form': 'pūjita', 'range': '8.1', 'source': 'pūjana'},

        # neg: pūjita not anudātta

        {'accent': 'udātta', 'form': 'pūjita', 'range': '8.1', 'source': 'pūjana'},

    ),

    "8.1.68": _fx(

        {'also': True, 'range': '8.1', 'stem_class': 'gati', 'suffix_class': 'tiṅ'},

        # neg: not gati-as-tiṅ

        {'also': True, 'range': '8.1', 'stem_class': 'dhātu', 'suffix_class': 'tiṅ'},

    ),

    "8.1.69": _fx(

        {'also': True, 'range': '8.1', 'semantic': 'kutsana', 'stem_class': 'agotrādi', 'suffix_class': 'sup'},

        # neg: gotra blocks kutsana sup rule

        {'also': True, 'range': '8.1', 'semantic': 'kutsana', 'stem_class': 'gotra', 'suffix_class': 'sup'},

    ),

    "8.1.70": _fx(

        {'domain': 'accent', 'range': '8.1', 'semantic': 'gati', 'stem_class': 'gati'},

        # neg: not gati semantic

        {'domain': 'accent', 'range': '8.1', 'semantic': 'bhāva', 'stem_class': 'gati'},

    ),

    "8.1.71": _fx(

        {'accent': 'udāttavat', 'also': True, 'range': '8.1', 'suffix_class': 'tiṅ'},

        # neg: not udāttavat for tiṅ

        {'accent': 'anudātta', 'also': True, 'range': '8.1', 'suffix_class': 'tiṅ'},

    ),

    "8.1.72": _fx(

        {'atidesha': 'avidyamānavat', 'compound_type': 'āmreḍita', 'member_role': 'pūrva', 'range': '8.1'},

        # neg: atideśa on wrong āmreḍita member

        {'atidesha': 'avidyamānavat', 'compound_type': 'āmreḍita', 'member_role': 'para', 'range': '8.1'},

    ),

    "8.1.73": _fx(

        {'compound_type': 'āmreḍita', 'range': '8.1', 'rule_blocked': True, 'semantic': 'samānādhikaraṇa'},

        # neg: āmreḍita should be blocked in samānādhikaraṇa

        {'compound_type': 'āmreḍita', 'range': '8.1', 'rule_blocked': False, 'semantic': 'samānādhikaraṇa'},

    ),

    "8.1.74": _fx(

        {'inflection': 'bahuvacana', 'optional': True, 'range': '8.1', 'semantic': 'viśeṣavacana'},

        # neg: wrong vacana for viśeṣavacana vibhāṣā

        {'inflection': 'ekavacana', 'optional': True, 'range': '8.1', 'semantic': 'viśeṣavacana'},

    ),

}


META: dict[str, SutraMeta] = {

    "8.1.1": SutraMeta('adhikara', "सर्वस्य द्वे ।", ("domain:samasanta", "pada:8.1")),

    "8.1.2": SutraMeta('samjna', "तस्य परमाम्रेडितम्‌ ।", ("domain:samasanta", "pada:8.1")),

    "8.1.3": SutraMeta('vidhi', "अनुदात्तं च ।", ("domain:samasanta", "pada:8.1")),

    "8.1.4": SutraMeta('vidhi', "नित्यवीप्सयोः ।", ("domain:samasanta", "pada:8.1")),

    "8.1.5": SutraMeta('vidhi', "परेर्वर्जने ।", ("domain:samasanta", "pada:8.1")),

    "8.1.6": SutraMeta('vidhi', "प्रसमुपोदः पादपूरणे ।", ("domain:samasanta", "pada:8.1")),

    "8.1.7": SutraMeta('vidhi', "उपर्यध्यधसः सामीप्ये ।", ("domain:samasanta", "pada:8.1")),

    "8.1.8": SutraMeta('vidhi', "वाक्यादेरामन्त्रितस्यासूयासम्मतिकोपकुत्सनभर्त्सनेषु ।", ("domain:samasanta", "pada:8.1")),

    "8.1.9": SutraMeta('atidesa', "एकं बहुव्रीहिवत्‌ ।", ("domain:samasanta", "pada:8.1")),

    "8.1.10": SutraMeta('vidhi', "आबाधे च ।", ("domain:samasanta", "pada:8.1")),

    "8.1.11": SutraMeta('atidesa', "कर्मधारयवत्‌ उत्तरेषु ।", ("domain:samasanta", "pada:8.1")),

    "8.1.12": SutraMeta('vidhi', "प्रकारे गुणवचनस्य ।", ("domain:samasanta", "pada:8.1")),

    "8.1.13": SutraMeta('vibhasha', "अकृच्छ्रे प्रियसुखयोरन्यतरस्याम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.14": SutraMeta('vidhi', "यथास्वे यथायथम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.15": SutraMeta('vidhi', "द्वन्द्वं रहस्यमर्यादावचनव्युत्क्रमणयज्ञपात्रप्रयोगाभिव्यक्तिषु ।", ("domain:samasanta", "pada:8.1")),

    "8.1.16": SutraMeta('adhikara', "पदस्य ।", ("domain:samasanta", "pada:8.1")),

    "8.1.17": SutraMeta('adhikara', "पदात्‌ ।", ("domain:samasanta", "pada:8.1")),

    "8.1.18": SutraMeta('adhikara', "अनुदात्तं सर्वमपादादौ ।", ("domain:samasanta", "pada:8.1")),

    "8.1.19": SutraMeta('vidhi', "आमन्त्रितस्य च ।", ("domain:samasanta", "pada:8.1")),

    "8.1.20": SutraMeta('vidhi', "युष्मदस्मदोः षष्ठीचतुर्थीद्वितीयास्थयोर्वान्नावौ ।", ("domain:samasanta", "pada:8.1")),

    "8.1.21": SutraMeta('vidhi', "बहुवचने वस्नसौ ।", ("domain:samasanta", "pada:8.1")),

    "8.1.22": SutraMeta('vidhi', "तेमयावेकवचनस्य ।", ("domain:samasanta", "pada:8.1")),

    "8.1.23": SutraMeta('vidhi', "त्वामौ द्वितीयायाः ।", ("domain:samasanta", "pada:8.1")),

    "8.1.24": SutraMeta('vidhi', "न चवाहाहैवयुक्ते ।", ("domain:samasanta", "pada:8.1")),

    "8.1.25": SutraMeta('vidhi', "पश्यार्थैश्चानालोचने ।", ("domain:samasanta", "pada:8.1")),

    "8.1.26": SutraMeta('vibhasha', "सपूर्वायाः प्रथमाया विभाषा ।", ("domain:samasanta", "pada:8.1")),

    "8.1.27": SutraMeta('vidhi', "तिङो गोत्रादीनि कुत्सनाभीक्ष्ण्ययोः ।", ("domain:samasanta", "pada:8.1")),

    "8.1.28": SutraMeta('vidhi', "तिङ्ङतिङः ।", ("domain:samasanta", "pada:8.1")),

    "8.1.29": SutraMeta('vidhi', "न लुट् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.30": SutraMeta('vidhi', "निपातैर्यद्यदिहन्तकुविन्नेच्चेच्चण्कच्चिद्यत्रयुक्तम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.31": SutraMeta('vidhi', "नह प्रत्यारम्भे ।", ("domain:samasanta", "pada:8.1")),

    "8.1.32": SutraMeta('vidhi', "सत्यं प्रश्ने ।", ("domain:samasanta", "pada:8.1")),

    "8.1.33": SutraMeta('vidhi', "अङ्गाप्रातिलोम्ये ।", ("domain:samasanta", "pada:8.1")),

    "8.1.34": SutraMeta('vidhi', "हि च ।", ("domain:samasanta", "pada:8.1")),

    "8.1.35": SutraMeta('vidhi', "छन्दस्यनेकमपि साकाङ्क्षम्‌ ।", ("domain:samasanta", "pada:8.1")),

    "8.1.36": SutraMeta('vidhi', "यावद्यथाभ्याम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.37": SutraMeta('vidhi', "पूजायां नानन्तरम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.38": SutraMeta('vidhi', "उपसर्गव्यपेतं च ।", ("domain:samasanta", "pada:8.1")),

    "8.1.39": SutraMeta('vidhi', "तुपश्यपश्यताहैः पूजायाम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.40": SutraMeta('vidhi', "अहो च ।", ("domain:samasanta", "pada:8.1")),

    "8.1.41": SutraMeta('vibhasha', "शेषे विभाषा ।", ("domain:samasanta", "pada:8.1")),

    "8.1.42": SutraMeta('vidhi', "पुरा च परीप्सायाम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.43": SutraMeta('vidhi', "नन्वित्यनुज्ञैषणायाम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.44": SutraMeta('vidhi', "किं क्रियाप्रश्नेऽनुपसर्गमप्रतिषिद्धम्‌ ।", ("domain:samasanta", "pada:8.1")),

    "8.1.45": SutraMeta('vibhasha', "लोपे विभाषा ।", ("domain:samasanta", "pada:8.1")),

    "8.1.46": SutraMeta('vidhi', "एहिमन्ये प्रहासे लृट् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.47": SutraMeta('vidhi', "जात्वपूर्वम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.48": SutraMeta('vidhi', "किम्वृत्तं च चिदुत्तरम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.49": SutraMeta('vidhi', "आहो उताहो चानन्तरम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.50": SutraMeta('vibhasha', "शेषे विभाषा ।", ("domain:samasanta", "pada:8.1")),

    "8.1.51": SutraMeta('vidhi', "गत्यर्थलोटा लृण्न चेत्‌ कारकं सर्वान्यत्‌ ।", ("domain:samasanta", "pada:8.1")),

    "8.1.52": SutraMeta('vidhi', "लोट् च ।", ("domain:samasanta", "pada:8.1")),

    "8.1.53": SutraMeta('vidhi', "विभाषितं सोपसर्गमनुत्तमम्‌ ।", ("domain:samasanta", "pada:8.1")),

    "8.1.54": SutraMeta('vidhi', "हन्त च ।", ("domain:samasanta", "pada:8.1")),

    "8.1.55": SutraMeta('vidhi', "आम एकान्तरमामन्त्रितमनन्तिके ।", ("domain:samasanta", "pada:8.1")),

    "8.1.56": SutraMeta('vidhi', "यद्धितुपरं छन्दसि ।", ("domain:samasanta", "pada:8.1")),

    "8.1.57": SutraMeta('vidhi', "चनचिदिवगोत्रादितद्धिताम्रेडितेष्वगतेः ।", ("domain:samasanta", "pada:8.1")),

    "8.1.58": SutraMeta('vidhi', "चादिषु च ।", ("domain:samasanta", "pada:8.1")),

    "8.1.59": SutraMeta('vidhi', "चवायोगे प्रथमा ।", ("domain:samasanta", "pada:8.1")),

    "8.1.60": SutraMeta('vidhi', "हेति क्षियायाम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.61": SutraMeta('vidhi', "अहेति विनियोगे च ।", ("domain:samasanta", "pada:8.1")),

    "8.1.62": SutraMeta('vidhi', "चाहलोप एवेत्यवधारणम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.63": SutraMeta('vibhasha', "चादिलोपे विभाषा ।", ("domain:samasanta", "pada:8.1")),

    "8.1.64": SutraMeta('vidhi', "वैवावेति च च्छन्दसि ।", ("domain:samasanta", "pada:8.1")),

    "8.1.65": SutraMeta('vidhi', "एकान्याभ्यां समर्थाभ्याम् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.66": SutraMeta('vidhi', "यद्वृत्तान्नित्यं ।", ("domain:samasanta", "pada:8.1")),

    "8.1.67": SutraMeta('vidhi', "पूजनात्‌ पूजितमनुदात्तम् (काष्ठादिभ्यः) ।", ("domain:samasanta", "pada:8.1")),

    "8.1.68": SutraMeta('vidhi', "सगतिरपि तिङ् ।", ("domain:samasanta", "pada:8.1")),

    "8.1.69": SutraMeta('vidhi', "कुत्सने च सुप्यगोत्रादौ ।", ("domain:samasanta", "pada:8.1")),

    "8.1.70": SutraMeta('vidhi', "गतिर्गतौ ।", ("domain:samasanta", "pada:8.1")),

    "8.1.71": SutraMeta('vidhi', "तिङि चोदात्तवति ।", ("domain:samasanta", "pada:8.1")),

    "8.1.72": SutraMeta('atidesa', "आमन्त्रितं पूर्वम् अविद्यमानवत्‌ ।", ("domain:samasanta", "pada:8.1")),

    "8.1.73": SutraMeta('vidhi', "नामन्त्रिते समानाधिकरणे (सामान्यवचनम्) ।", ("domain:samasanta", "pada:8.1")),

    "8.1.74": SutraMeta('vibhasha', "विभाषितं विशेषवचने बहुवचनम् ।", ("domain:samasanta", "pada:8.1")),

}


def _self_check() -> dict[str, int]:
    """Verify every predicate against its positive/negative fixtures."""
    failures: list[str] = []
    for sid in sorted(FIXTURES):
        fn = globals()[_predicate_name(sid)]
        pos, neg = FIXTURES[sid]
        if not fn(pos):
            failures.append(f"{sid}: positive")
        if fn(neg):
            failures.append(f"{sid}: negative")
    if failures:
        raise AssertionError("sutra_impl_8_1 self-check failed: " + ", ".join(failures))
    return {
        "sutras": len(FIXTURES),
        "meta": len(META),
        "predicates": len([n for n in globals() if n.startswith("sutra_8_1_")]),
    }


(
    IMPLEMENTED_IDS,
    has_real_implementation,
    handler_for,
    positive_features,
    negative_features,
) = make_module_api(FIXTURES, globals())

_COUNTS = _self_check()
