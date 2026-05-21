"""Discrete Pāṇinian predicates for Adhyāya 8.4 (avasāna / pada-final / period).

Hand-written per sūtra from ``data/ashtadhyayi_sutras.json``.
Domain: avasāna, pada-boundary phonology, pluti, and sentence-edge sandhi (8.4).
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .categories import is_avasana, is_samhita
from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api

_SAMJNA = "samjna"
_PARIBHASHA = "paribhasha"
_VIDHI = "vidhi"
_PRATISEDHA = "pratisedha"
_VIBHASHA = "vibhasha"

_GANA_8_4_4 = frozenset({
    "agre",
    "asidhra",
    "kasharika",
    "kotara",
    "puragami",
    "shraka",
})

_GANA_8_4_5 = frozenset({
    "amra",
    "api",
    "ikshu",
    "karshya",
    "khadira",
    "plaksha",
    "pranta",
    "shara",
    "yuksha",
})

_GANA_8_4_17 = frozenset({
    "apat",
    "cinoti",
    "degdhi",
    "drati",
    "gad",
    "ghu",
    "hanti",
    "mas",
    "nad",
    "pad",
    "psati",
    "shamyati",
    "vahati",
    "vapati",
    "vati",
    "yati",
})

_GANA_8_4_34 = frozenset({
    "amip",
    "bha",
    "bhu",
    "mig",
    "puka",
    "vepa",
    "yayi",
})

_GANA_8_4_39 = frozenset({
    "ad",
    "adi",
    "kshubhna",
})

_GANA_8_4_67 = frozenset({
    "agargya",
    "galava",
    "kashyapa",
})


def _samhita_word(c: Mapping[str, Any]) -> bool:
    """True when ``word`` is non-empty saṃhitā (1.4.109)."""
    return is_samhita(str(c.get("word", "")))


def _avasana_index(c: Mapping[str, Any]) -> bool:
    """True when ``index`` marks avasāna at end of ``word`` (1.4.110)."""
    return is_avasana(str(c.get("word", "")), int(c.get("index", -1)))


def _fx_pair(pos: dict, neg: dict) -> tuple[dict, dict]:
    return (pos, neg)

def sutra_8_4_1(c) -> bool:
    """raṣābhyāṃ no ṇaḥ samānapade: रषाभ्यां नो णः समानपदे ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'retroflex_block', True) and
        _in(c, 'left', frozenset({'r', 'ṣ'})) and
        _eq(c, 'final_sound', 'ṇ') and
        bool(c.get('samānapada'))
    )

def sutra_8_4_2(c) -> bool:
    """aṭkupvāṅnumvyavāye'pi: अट्कुप्वाङ्नुम्व्यवायेऽपि ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'aṭkupvāṅnumvyavāya') and
        bool(c.get('pada_boundary')) and
        bool(c.get('retroflex_block')) and
        _eq(c, 'final_sound', 'ṇ')
    )

def sutra_8_4_3(c) -> bool:
    """pūrvapadāt saṃjñāyām agaḥ: पूर्वपदात्‌ संज्ञायामगः ।"""
    return (
        _eq(c, 'range', '8.4') and
        bool(c.get('pūrvapada')) and
        _eq(c, 'environment', 'saṃjñā') and
        _eq(c, 'operation', 'agaḥ') and
        _eq(c, 'left', 'pūrvapada')
    )

def sutra_8_4_4(c) -> bool:
    """vanaṃ puragāmi-gaṇa: वनं पुरगामिश्रकासिध्रकाशारिकाकोटराऽग्रेभ्यः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'stem', 'vana') and
        _in(c, 'right', _GANA_8_4_4) and
        _eq(c, 'case_relation', 'prathamā') and
        _eq(c, 'environment', 'ṣaṣṭhīvyatyaya')
    )

def sutra_8_4_5(c) -> bool:
    """pra-nir-antaḥ-gaṇa: प्रनिरन्तःशरेक्षुप्लक्षाम्रकार्ष्यखदिरपियूक्षाभ्योऽसंज्ञायामपि ।"""
    return (
        _eq(c, 'range', '8.4') and
        _in(c, 'left', _GANA_8_4_5) and
        _eq(c, 'environment', 'asaṃjñā') and
        bool(c.get('optional')) and
        _eq(c, 'stem', 'vana')
    )

def sutra_8_4_6(c) -> bool:
    """vibhāṣā oṣadhi-vanaspati: विभाषौषधिवनस्पतिभ्यः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _in(c, 'left', frozenset({'oṣadhi', 'vanaspati'})) and
        bool(c.get('optional')) and
        _eq(c, 'rule', 'vibhāṣā') and
        _eq(c, 'environment', 'compound')
    )

def sutra_8_4_7(c) -> bool:
    """ahno 'dantāt: अह्नोऽदन्तात्‌ ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'stem', 'ahan') and
        _eq(c, 'condition', 'adanta') and
        _eq(c, 'case_relation', 'prathamā') and
        _eq(c, 'environment', 'ṣaṣṭhī')
    )

def sutra_8_4_8(c) -> bool:
    """vāhanaṃ āhitāt: वाहनमाहितात्‌ ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'stem', 'vāhana') and
        _eq(c, 'environment', 'āhita') and
        _eq(c, 'right', 'āhita') and
        _eq(c, 'operation', 'substitution')
    )

def sutra_8_4_9(c) -> bool:
    """pānaṃ deśe: पानं देशे ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'stem', 'pāna') and
        _eq(c, 'environment', 'deśa') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'pada_boundary', False)
    )

def sutra_8_4_10(c) -> bool:
    """vā bhāva-karaṇa: वा भावकरणयोः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _in(c, 'environment', frozenset({'bhāva', 'karaṇa'})) and
        bool(c.get('optional')) and
        _eq(c, 'rule', 'vā') and
        _eq(c, 'operation', 'substitution')
    )

def sutra_8_4_11(c) -> bool:
    """prātipadikānta-num-vibhakti: प्रातिपदिकान्तनुम्विभक्तिषु च ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'prātipadikānta') and
        bool(c.get('num')) and
        _eq(c, 'suffix_class', 'vibhakti') and
        _eq(c, 'rule', 'ca')
    )

def sutra_8_4_12(c) -> bool:
    """ekāj-uttara-pade ṇaḥ: एकाजुत्तरपदे णः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'ekājuttara') and
        _eq(c, 'final_sound', 'ṇ') and
        bool(c.get('samānapada')) and
        _eq(c, 'operation', 'ṇati')
    )

def sutra_8_4_13(c) -> bool:
    """kumati ca: कुमति च ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'kumati') and
        _eq(c, 'rule', 'ca') and
        _eq(c, 'final_sound', 'ṇ') and
        bool(c.get('samānapada'))
    )

def sutra_8_4_14(c) -> bool:
    """upasargād asamāse ṇopadeśa: उपसर्गादसमासेऽपि णोपदेशस्य ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'upasarga') and
        _eq(c, 'compound', 'asamāsa') and
        _eq(c, 'final_sound', 'ṇ') and
        _eq(c, 'condition', 'ṇopadeśa')
    )

def sutra_8_4_15(c) -> bool:
    """hinu mīna: हिनुमीना ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'dhatu', 'hinu') and
        _eq(c, 'right', 'mīna') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'environment', 'samāsa')
    )

def sutra_8_4_16(c) -> bool:
    """āni loṭ: आनि लोट् ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'stem', 'āni') and
        _eq(c, 'lakara', 'loṭ') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'environment', 'tiṅ')
    )

def sutra_8_4_17(c) -> bool:
    """ner-gaṇa: नेर्गदनदपतपदघुमास्यतिहन्तियातिवातिद्रातिप्सातिवपतिवहतिशाम्यतिचिनोतिदेग्धिषु च ।"""
    return (
        _eq(c, 'range', '8.4') and
        _in(c, 'dhatu', _GANA_8_4_17) and
        _eq(c, 'suffix', 'ṇer') and
        _eq(c, 'rule', 'ca') and
        _eq(c, 'environment', 'tiṅ')
    )

def sutra_8_4_18(c) -> bool:
    """śeṣe vibhāṣā akakhādi: शेषे विभाषाऽकखादावषान्त उपदेशे ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'śeṣa') and
        bool(c.get('optional')) and
        _eq(c, 'environment_2', 'akakhādi') and
        _eq(c, 'condition', 'aṣānta') and
        _eq(c, 'site', 'upadeśa')
    )

def sutra_8_4_19(c) -> bool:
    """aniteḥ: अनितेः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'suffix', 'aniti') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'environment', 'tiṅ') and
        _eq(c, 'final_sound', 'ṇ')
    )

def sutra_8_4_20(c) -> bool:
    """antaḥ: अन्तः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'anta') and
        _eq(c, 'operation', 'substitution') and
        bool(c.get('pada_boundary')) and
        _eq(c, 'final_sound', 'ṇ')
    )

def sutra_8_4_21(c) -> bool:
    """ubhau sābhyāsasya: उभौ साभ्यासस्य ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'substitute', 'ubhau') and
        _eq(c, 'environment', 'sābhyāsa') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'count', 2)
    )

def sutra_8_4_22(c) -> bool:
    """hanteḥ atpūrvasya: हन्तेरत्पूर्वस्य ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'dhatu', 'han') and
        _eq(c, 'condition', 'atpūrva') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'environment', 'tiṅ')
    )

def sutra_8_4_23(c) -> bool:
    """vamor vā: वमोर्वा ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'stem_final', 'vam') and
        bool(c.get('optional')) and
        _eq(c, 'rule', 'vā') and
        _eq(c, 'environment', 'sandhi')
    )

def sutra_8_4_24(c) -> bool:
    """antaradeśe: अन्तरदेशे ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'antaradeśa') and
        _eq(c, 'environment_2', 'anta') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'pada_boundary', False)
    )

def sutra_8_4_25(c) -> bool:
    """ayanaṃ ca: अयनं च ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'stem', 'ayana') and
        _eq(c, 'rule', 'ca') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'environment', 'samāsa')
    )

def sutra_8_4_26(c) -> bool:
    """chandasi ṛd avagrahāt: छन्दस्यृदवग्रहात्‌ ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'chandas') and
        _eq(c, 'stem_final', 'ṛ') and
        _eq(c, 'left', 'avagraha') and
        _eq(c, 'operation', 'substitution')
    )

def sutra_8_4_27(c) -> bool:
    """naś ca dhātu-stha-uruṣu: नश्च धातुस्थोरुषुभ्यः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'final_sound', 'n') and
        _in(c, 'environment', frozenset({'dhātu', 'stha', 'uru'})) and
        _eq(c, 'rule', 'ca') and
        _eq(c, 'operation', 'substitution')
    )

def sutra_8_4_28(c) -> bool:
    """upasargād bahulam: उपसर्गाद् बहुलम् ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'upasarga') and
        _eq(c, 'rule', 'bahula') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'pada_boundary', False)
    )

def sutra_8_4_29(c) -> bool:
    """kṛtyacaḥ: कृत्यचः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'suffix_class', 'kṛti') and
        _eq(c, 'right', 'ac') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'environment', 'pratyaya')
    )

def sutra_8_4_30(c) -> bool:
    """ṇer vibhāṣā: णेर्विभाषा ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'suffix', 'ṇer') and
        bool(c.get('optional')) and
        _eq(c, 'rule', 'vibhāṣā') and
        _eq(c, 'environment', 'tiṅ')
    )

def sutra_8_4_31(c) -> bool:
    """hal śca ijupadhāt: हलश्च इजुपधात्‌ ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'phoneme_class', 'hal') and
        _eq(c, 'rule', 'ca') and
        _eq(c, 'condition', 'ijupadhā') and
        _eq(c, 'site', 'upadeśa')
    )

def sutra_8_4_32(c) -> bool:
    """ijādeḥ sanumaḥ: इजादेः सनुमः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'condition', 'ijādi') and
        _eq(c, 'environment', 'sanuma') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'site', 'upadeśa')
    )

def sutra_8_4_33(c) -> bool:
    """vā niṃsa-nikṣa-ninda: वा निंसनिक्षनिन्दाम् ।"""
    return (
        _eq(c, 'range', '8.4') and
        _in(c, 'dhatu', frozenset({'niṃs', 'nikṣ', 'nind'})) and
        bool(c.get('optional')) and
        _eq(c, 'rule', 'vā') and
        _eq(c, 'environment', 'tiṅ')
    )

def sutra_8_4_34(c) -> bool:
    """na bhābhū-gaṇa: न भाभूपूकमिगमिप्यायीवेपाम् ।"""
    return (
        _eq(c, 'range', '8.4') and
        _in(c, 'dhatu', _GANA_8_4_34) and
        bool(c.get('rule_blocked')) and
        _eq(c, 'suffix', 'ṇer') and
        _eq(c, 'environment', 'tiṅ')
    )

def sutra_8_4_35(c) -> bool:
    """ṣāt padāntāt: षात्‌ पदान्तात्‌ ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'left', 'ṣ') and
        bool(c.get('pada_boundary')) and
        _eq(c, 'environment', 'padānta') and
        _eq(c, 'operation', 'visarga')
    )

def sutra_8_4_36(c) -> bool:
    """naśeḥ ṣāntasya: नशेः षान्तस्य ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'dhatu', 'naś') and
        _eq(c, 'condition', 'ṣānta') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'environment', 'tiṅ')
    )

def sutra_8_4_37(c) -> bool:
    """padāntasya: पदान्तस्य ।"""
    return (
        _eq(c, 'range', '8.4') and
        bool(c.get('pada_boundary')) and
        _eq(c, 'environment', 'padānta') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'final_sound', 's')
    )

def sutra_8_4_38(c) -> bool:
    """padavyavāye'pi: पदव्यवायेऽपि ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'padavyavāya') and
        bool(c.get('pada_boundary')) and
        _eq(c, 'rule', 'api') and
        _eq(c, 'operation', 'substitution')
    )

def sutra_8_4_39(c) -> bool:
    """kṣubhnādiṣu ca: क्षुभ्नाऽऽदिषु च ।"""
    return (
        _eq(c, 'range', '8.4') and
        _in(c, 'dhatu', _GANA_8_4_39) and
        _eq(c, 'rule', 'ca') and
        _eq(c, 'environment', 'padānta') and
        _eq(c, 'operation', 'substitution')
    )

def sutra_8_4_40(c) -> bool:
    """stoḥ ścuna ścuḥ pluti: स्तोः श्चुना श्चुः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'stem', 'stu') and
        _eq(c, 'operation', 'pluti') and
        _eq(c, 'substitute', 'ścu') and
        _eq(c, 'augment', 'ścuna')
    )

def sutra_8_4_41(c) -> bool:
    """ṣṭuna ṣṭuḥ pluti: ष्टुना ष्टुः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'operation', 'pluti') and
        _eq(c, 'substitute', 'ṣṭu') and
        _eq(c, 'augment', 'ṣṭuna') and
        _eq(c, 'environment', 'padānta')
    )

def sutra_8_4_42(c) -> bool:
    """na padāntāṭṭor anām: न पदान्ताट्टोरनाम् ।"""
    return (
        _eq(c, 'range', '8.4') and
        bool(c.get('pada_boundary')) and
        _eq(c, 'left', 'ṭ') and
        bool(c.get('rule_blocked')) and
        _eq(c, 'condition', 'anām')
    )

def sutra_8_4_43(c) -> bool:
    """toḥ ṣi: तोः षि ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'left', 't') and
        _eq(c, 'environment', 'ṣi') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'final_sound', 's')
    )

def sutra_8_4_44(c) -> bool:
    """śāt: शात्‌ ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'left', 'ś') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'environment', 'sandhi') and
        _samhita_word(c)
    )

def sutra_8_4_45(c) -> bool:
    """yaro'nunāsike: यरोऽनुनासिकेऽनुनासिको वा ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'phoneme_class', 'yara') and
        _eq(c, 'environment', 'anunāsika') and
        _eq(c, 'substitute', 'anunāsika') and
        bool(c.get('optional'))
    )

def sutra_8_4_46(c) -> bool:
    """aco rahābhyāṃ dve: अचो रहाभ्यां द्वे ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'phoneme_class', 'ac') and
        _in(c, 'left', frozenset({'r', 'h'})) and
        _eq(c, 'operation', 'duplication') and
        _eq(c, 'count', 2)
    )

def sutra_8_4_47(c) -> bool:
    """anaci ca: अनचि च ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'anac') and
        _eq(c, 'rule', 'ca') and
        _eq(c, 'operation', 'substitution') and
        _samhita_word(c)
    )

def sutra_8_4_48(c) -> bool:
    """nādiny ākrośe putrasya: नादिन्याक्रोशे पुत्रस्य ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'ādini') and
        _eq(c, 'environment_2', 'ākrośa') and
        bool(c.get('rule_blocked')) and
        _eq(c, 'semantic', 'putra')
    )

def sutra_8_4_49(c) -> bool:
    """śaro'ci: शरोऽचि ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'left', 'śar') and
        _eq(c, 'environment', 'ac') and
        _eq(c, 'operation', 'substitution') and
        _samhita_word(c)
    )

def sutra_8_4_50(c) -> bool:
    """tri-prabhṛti śākaṭāyana: त्रिप्रभृतिषु शाकटायनस्य ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'triprabhṛti') and
        _eq(c, 'authority', 'śākaṭāyana') and
        _eq(c, 'operation', 'substitution') and
        _samhita_word(c)
    )

def sutra_8_4_51(c) -> bool:
    """sarvatra śākalya: सर्वत्र शाकल्यस्य ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'scope', 'sarvatra') and
        _eq(c, 'authority', 'śākalya') and
        _eq(c, 'operation', 'substitution') and
        _samhita_word(c)
    )

def sutra_8_4_52(c) -> bool:
    """dīrghād ācārya: दीर्घादाचार्याणाम् ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'vowel_weight', 'dīrgha') and
        _eq(c, 'authority', 'ācārya') and
        _eq(c, 'operation', 'substitution') and
        _samhita_word(c)
    )

def sutra_8_4_53(c) -> bool:
    """jhalāṃ jaś jhaśi: झलां जश् झशि ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'phoneme_class', 'jhal') and
        _eq(c, 'substitute', 'jaś') and
        _eq(c, 'environment', 'jhaśi') and
        _samhita_word(c)
    )

def sutra_8_4_54(c) -> bool:
    """abhyāse car ca: अभ्यासे चर्च्च ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'abhyāsa') and
        _eq(c, 'dhatu', 'car') and
        _eq(c, 'rule', 'ca') and
        _eq(c, 'operation', 'substitution')
    )

def sutra_8_4_55(c) -> bool:
    """khari ca: खरि च ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'environment', 'khari') and
        _eq(c, 'rule', 'ca') and
        _eq(c, 'operation', 'substitution') and
        _samhita_word(c)
    )

def sutra_8_4_56(c) -> bool:
    """vā avasāne: वाऽवसाने ।"""
    return (
        _eq(c, 'range', '8.4') and
        bool(c.get('optional')) and
        _eq(c, 'environment', 'avasāna') and
        _avasana_index(c) and
        _eq(c, 'rule', 'vā')
    )

def sutra_8_4_57(c) -> bool:
    """aṇo'pragṛhyasyānunāsikaḥ: अणोऽप्रगृह्यस्यानुनासिकः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'suffix', 'aṇ') and
        _eq(c, 'condition', 'aprāgṛhya') and
        _eq(c, 'substitute', 'anunāsika') and
        _eq(c, 'environment', 'padānta')
    )

def sutra_8_4_58(c) -> bool:
    """anusvārasya yayi parasavarnaḥ: अनुस्वारस्य ययि परसवर्णः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'left', 'anusvāra') and
        _eq(c, 'environment', 'yayi') and
        _eq(c, 'substitute', 'parasavarna') and
        _samhita_word(c)
    )

def sutra_8_4_59(c) -> bool:
    """vā padāntasya: वा पदान्तस्य ।"""
    return (
        _eq(c, 'range', '8.4') and
        bool(c.get('pada_boundary')) and
        bool(c.get('optional')) and
        _eq(c, 'environment', 'padānta') and
        _eq(c, 'rule', 'vā')
    )

def sutra_8_4_60(c) -> bool:
    """tor li: तोर्लि ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'left', 't') and
        _eq(c, 'environment', 'li') and
        _eq(c, 'operation', 'substitution') and
        _eq(c, 'final_sound', 's')
    )

def sutra_8_4_61(c) -> bool:
    """udaḥ sthā-stambhoḥ pūrvasya: उदः स्थास्तम्भोः पूर्वस्य ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'left', 'ud') and
        _in(c, 'right', frozenset({'sthā', 'stambhu'})) and
        _eq(c, 'relation', 'pūrva') and
        _eq(c, 'operation', 'substitution')
    )

def sutra_8_4_62(c) -> bool:
    """jhayo ho'nyatarasyām: झयो होऽन्यतरस्याम् ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'phoneme_class', 'jhay') and
        _eq(c, 'substitute', 'ho') and
        bool(c.get('optional')) and
        _eq(c, 'environment', 'sandhi')
    )

def sutra_8_4_63(c) -> bool:
    """śaś cho'ṭi: शश्छोऽटि ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'left', 'ś') and
        _eq(c, 'substitute', 'ch') and
        _eq(c, 'environment', 'ṭi') and
        _eq(c, 'operation', 'substitution')
    )

def sutra_8_4_64(c) -> bool:
    """halo yamāṃ yami lopaḥ: हलो यमां यमि लोपः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'phoneme_class', 'hal') and
        _eq(c, 'environment', 'yami') and
        _eq(c, 'operation', 'lopa') and
        _in(c, 'right', frozenset({'yam', 'ra', 'la', 'va'}))
    )

def sutra_8_4_65(c) -> bool:
    """jharo jhari savarṇe: झरो झरि सवर्णे ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'phoneme_class', 'jhar') and
        _eq(c, 'environment', 'jhari') and
        _eq(c, 'condition', 'savarṇa') and
        _samhita_word(c)
    )

def sutra_8_4_66(c) -> bool:
    """udāttād anudāttasya svaritaḥ: उदात्तादनुदात्तस्य स्वरितः ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'accent_left', 'udātta') and
        _eq(c, 'accent', 'anudātta') and
        _eq(c, 'substitute', 'svarita') and
        _eq(c, 'environment', 'sandhi')
    )

def sutra_8_4_67(c) -> bool:
    """no udātta-svaritodaya: नोदात्तस्वरितोदयमगार्ग्यकाश्यपगालवानाम्‌ ।"""
    return (
        _eq(c, 'range', '8.4') and
        _in(c, 'authority', _GANA_8_4_67) and
        bool(c.get('rule_blocked')) and
        _eq(c, 'accent', 'udātta-svaritodaya') and
        _eq(c, 'environment', 'accent')
    )

def sutra_8_4_68(c) -> bool:
    """a a iti avasāna: अ अ इति ।"""
    return (
        _eq(c, 'range', '8.4') and
        _eq(c, 'final_sound', 'a') and
        _eq(c, 'pause_marker', 'iti') and
        _eq(c, 'operation', 'avasāna') and
        _avasana_index(c)
    )

FIXTURES: dict[str, tuple[dict, dict]] = {
    # neg: samānapada false — ṇ not blocked across pada
    "8.4.1": _fx_pair({'range': '8.4', 'retroflex_block': True, 'left': 'r', 'final_sound': 'ṇ', 'samānapada': True}, {'range': '8.4', 'retroflex_block': True, 'left': 'r', 'final_sound': 'ṇ', 'samānapada': False}),
    # neg: pada_boundary false — vyavāya scope missing
    "8.4.2": _fx_pair({'range': '8.4', 'environment': 'aṭkupvāṅnumvyavāya', 'pada_boundary': True, 'retroflex_block': True, 'final_sound': 'ṇ'}, {'range': '8.4', 'environment': 'aṭkupvāṅnumvyavāya', 'pada_boundary': False, 'retroflex_block': True, 'final_sound': 'ṇ'}),
    # neg: breaks predicate for 8.4.3
    "8.4.3": _fx_pair({'range': '8.4', 'pūrvapada': True, 'environment': 'saṃjñā', 'operation': 'agaḥ', 'left': 'pūrvapada'}, {'range': '8.4', 'pūrvapada': False, 'environment': 'saṃjñā', 'operation': 'agaḥ', 'left': 'pūrvapada'}),
    # neg: breaks predicate for 8.4.4
    "8.4.4": _fx_pair({'range': '8.4', 'stem': 'vana', 'right': 'puragami', 'case_relation': 'prathamā', 'environment': 'ṣaṣṭhīvyatyaya'}, {'range': '8.4', 'stem': 'vana', 'right': 'pac', 'case_relation': 'prathamā', 'environment': 'ṣaṣṭhīvyatyaya'}),
    # neg: breaks predicate for 8.4.5
    "8.4.5": _fx_pair({'range': '8.4', 'left': 'pranta', 'environment': 'asaṃjñā', 'optional': True, 'stem': 'vana'}, {'range': '8.4', 'left': 'pranta', 'environment': 'saṃjñā', 'optional': True, 'stem': 'vana'}),
    # neg: breaks predicate for 8.4.6
    "8.4.6": _fx_pair({'range': '8.4', 'left': 'oṣadhi', 'optional': True, 'rule': 'vibhāṣā', 'environment': 'compound'}, {'range': '8.4', 'left': 'oṣadhi', 'optional': False, 'rule': 'vibhāṣā', 'environment': 'compound'}),
    # neg: breaks predicate for 8.4.7
    "8.4.7": _fx_pair({'range': '8.4', 'stem': 'ahan', 'condition': 'adanta', 'case_relation': 'prathamā', 'environment': 'ṣaṣṭhī'}, {'range': '8.4', 'stem': 'ahan', 'condition': 'adanta', 'case_relation': 'prathamā', 'environment': 'loka'}),
    # neg: breaks predicate for 8.4.8
    "8.4.8": _fx_pair({'range': '8.4', 'stem': 'vāhana', 'environment': 'āhita', 'right': 'āhita', 'operation': 'substitution'}, {'range': '8.4', 'stem': 'vāhana', 'environment': 'loka', 'right': 'āhita', 'operation': 'substitution'}),
    # neg: breaks predicate for 8.4.9
    "8.4.9": _fx_pair({'range': '8.4', 'stem': 'pāna', 'environment': 'deśa', 'operation': 'substitution', 'pada_boundary': False}, {'range': '8.4', 'stem': 'pāna', 'environment': 'loka', 'operation': 'substitution', 'pada_boundary': False}),
    # neg: breaks predicate for 8.4.10
    "8.4.10": _fx_pair({'range': '8.4', 'environment': 'bhāva', 'optional': True, 'rule': 'vā', 'operation': 'substitution'}, {'range': '8.4', 'environment': 'bhāva', 'optional': True, 'rule': 'vā', 'operation': 'lopa'}),
    # neg: breaks predicate for 8.4.11
    "8.4.11": _fx_pair({'range': '8.4', 'environment': 'prātipadikānta', 'num': True, 'suffix_class': 'vibhakti', 'rule': 'ca'}, {'range': '8.4', 'environment': 'prātipadikānta', 'num': False, 'suffix_class': 'vibhakti', 'rule': 'ca'}),
    # neg: breaks predicate for 8.4.12
    "8.4.12": _fx_pair({'range': '8.4', 'environment': 'ekājuttara', 'final_sound': 'ṇ', 'samānapada': True, 'operation': 'ṇati'}, {'range': '8.4', 'environment': 'ekājuttara', 'final_sound': 'ṇ', 'samānapada': False, 'operation': 'ṇati'}),
    # neg: breaks predicate for 8.4.13
    "8.4.13": _fx_pair({'range': '8.4', 'environment': 'kumati', 'rule': 'ca', 'final_sound': 'ṇ', 'samānapada': True}, {'range': '8.4', 'environment': 'kumati', 'rule': 'na', 'final_sound': 'ṇ', 'samānapada': True}),
    # neg: breaks predicate for 8.4.14
    "8.4.14": _fx_pair({'range': '8.4', 'environment': 'upasarga', 'compound': 'asamāsa', 'final_sound': 'ṇ', 'condition': 'ṇopadeśa'}, {'range': '8.4', 'environment': 'upasarga', 'compound': 'samāsa', 'final_sound': 'ṇ', 'condition': 'ṇopadeśa'}),
    # neg: breaks predicate for 8.4.15
    "8.4.15": _fx_pair({'range': '8.4', 'dhatu': 'hinu', 'right': 'mīna', 'operation': 'substitution', 'environment': 'samāsa'}, {'range': '8.4', 'dhatu': 'hinu', 'right': 'pac', 'operation': 'substitution', 'environment': 'samāsa'}),
    # neg: breaks predicate for 8.4.16
    "8.4.16": _fx_pair({'range': '8.4', 'stem': 'āni', 'lakara': 'loṭ', 'operation': 'substitution', 'environment': 'tiṅ'}, {'range': '8.4', 'stem': 'āni', 'lakara': 'laṭ', 'operation': 'substitution', 'environment': 'tiṅ'}),
    # neg: breaks predicate for 8.4.17
    "8.4.17": _fx_pair({'range': '8.4', 'dhatu': 'gad', 'suffix': 'ṇer', 'rule': 'ca', 'environment': 'tiṅ'}, {'range': '8.4', 'dhatu': 'pac', 'suffix': 'ṇer', 'rule': 'ca', 'environment': 'tiṅ'}),
    # neg: breaks predicate for 8.4.18
    "8.4.18": _fx_pair({'range': '8.4', 'environment': 'śeṣa', 'optional': True, 'environment_2': 'akakhādi', 'condition': 'aṣānta', 'site': 'upadeśa'}, {'range': '8.4', 'environment': 'śeṣa', 'optional': True, 'environment_2': 'akakhādi', 'condition': 'ṣānta', 'site': 'upadeśa'}),
    # neg: breaks predicate for 8.4.19
    "8.4.19": _fx_pair({'range': '8.4', 'suffix': 'aniti', 'operation': 'substitution', 'environment': 'tiṅ', 'final_sound': 'ṇ'}, {'range': '8.4', 'suffix': 'aniti', 'operation': 'substitution', 'environment': 'tiṅ', 'final_sound': 't'}),
    # neg: breaks predicate for 8.4.20
    "8.4.20": _fx_pair({'range': '8.4', 'environment': 'anta', 'operation': 'substitution', 'pada_boundary': True, 'final_sound': 'ṇ'}, {'range': '8.4', 'environment': 'anta', 'operation': 'substitution', 'pada_boundary': False, 'final_sound': 'ṇ'}),
    # neg: breaks predicate for 8.4.21
    "8.4.21": _fx_pair({'range': '8.4', 'substitute': 'ubhau', 'environment': 'sābhyāsa', 'operation': 'substitution', 'count': 2}, {'range': '8.4', 'substitute': 'ubhau', 'environment': 'sābhyāsa', 'operation': 'substitution', 'count': 1}),
    # neg: breaks predicate for 8.4.22
    "8.4.22": _fx_pair({'range': '8.4', 'dhatu': 'han', 'condition': 'atpūrva', 'operation': 'substitution', 'environment': 'tiṅ'}, {'range': '8.4', 'dhatu': 'han', 'condition': 'atpūrva', 'operation': 'substitution', 'environment': 'loka'}),
    # neg: breaks predicate for 8.4.23
    "8.4.23": _fx_pair({'range': '8.4', 'stem_final': 'vam', 'optional': True, 'rule': 'vā', 'environment': 'sandhi'}, {'range': '8.4', 'stem_final': 'vam', 'optional': False, 'rule': 'vā', 'environment': 'sandhi'}),
    # neg: breaks predicate for 8.4.24
    "8.4.24": _fx_pair({'range': '8.4', 'environment': 'antaradeśa', 'environment_2': 'anta', 'operation': 'substitution', 'pada_boundary': False}, {'range': '8.4', 'environment': 'antaradeśa', 'environment_2': 'anta', 'operation': 'substitution', 'pada_boundary': True}),
    # neg: breaks predicate for 8.4.25
    "8.4.25": _fx_pair({'range': '8.4', 'stem': 'ayana', 'rule': 'ca', 'operation': 'substitution', 'environment': 'samāsa'}, {'range': '8.4', 'stem': 'ayana', 'rule': 'na', 'operation': 'substitution', 'environment': 'samāsa'}),
    # neg: breaks predicate for 8.4.26
    "8.4.26": _fx_pair({'range': '8.4', 'environment': 'chandas', 'stem_final': 'ṛ', 'left': 'avagraha', 'operation': 'substitution'}, {'range': '8.4', 'environment': 'loka', 'stem_final': 'ṛ', 'left': 'avagraha', 'operation': 'substitution'}),
    # neg: breaks predicate for 8.4.27
    "8.4.27": _fx_pair({'range': '8.4', 'final_sound': 'n', 'environment': 'dhātu', 'rule': 'ca', 'operation': 'substitution'}, {'range': '8.4', 'final_sound': 'n', 'environment': 'loka', 'rule': 'ca', 'operation': 'substitution'}),
    # neg: breaks predicate for 8.4.28
    "8.4.28": _fx_pair({'range': '8.4', 'environment': 'upasarga', 'rule': 'bahula', 'operation': 'substitution', 'pada_boundary': False}, {'range': '8.4', 'environment': 'upasarga', 'rule': 'nitya', 'operation': 'substitution', 'pada_boundary': False}),
    # neg: breaks predicate for 8.4.29
    "8.4.29": _fx_pair({'range': '8.4', 'suffix_class': 'kṛti', 'right': 'ac', 'operation': 'substitution', 'environment': 'pratyaya'}, {'range': '8.4', 'suffix_class': 'kṛti', 'right': 'ac', 'operation': 'substitution', 'environment': 'loka'}),
    # neg: breaks predicate for 8.4.30
    "8.4.30": _fx_pair({'range': '8.4', 'suffix': 'ṇer', 'optional': True, 'rule': 'vibhāṣā', 'environment': 'tiṅ'}, {'range': '8.4', 'suffix': 'ṇer', 'optional': False, 'rule': 'vibhāṣā', 'environment': 'tiṅ'}),
    # neg: breaks predicate for 8.4.31
    "8.4.31": _fx_pair({'range': '8.4', 'phoneme_class': 'hal', 'rule': 'ca', 'condition': 'ijupadhā', 'site': 'upadeśa'}, {'range': '8.4', 'phoneme_class': 'hal', 'rule': 'ca', 'condition': 'ikopadhā', 'site': 'upadeśa'}),
    # neg: breaks predicate for 8.4.32
    "8.4.32": _fx_pair({'range': '8.4', 'condition': 'ijādi', 'environment': 'sanuma', 'operation': 'substitution', 'site': 'upadeśa'}, {'range': '8.4', 'condition': 'ijādi', 'environment': 'sanuma', 'operation': 'substitution', 'site': 'loka'}),
    # neg: breaks predicate for 8.4.33
    "8.4.33": _fx_pair({'range': '8.4', 'dhatu': 'niṃs', 'optional': True, 'rule': 'vā', 'environment': 'tiṅ'}, {'range': '8.4', 'dhatu': 'niṃs', 'optional': True, 'rule': 'vā', 'environment': 'loka'}),
    # neg: breaks predicate for 8.4.34
    "8.4.34": _fx_pair({'range': '8.4', 'dhatu': 'bha', 'rule_blocked': True, 'suffix': 'ṇer', 'environment': 'tiṅ'}, {'range': '8.4', 'dhatu': 'bha', 'rule_blocked': False, 'suffix': 'ṇer', 'environment': 'tiṅ'}),
    # neg: breaks predicate for 8.4.35
    "8.4.35": _fx_pair({'range': '8.4', 'left': 'ṣ', 'pada_boundary': True, 'environment': 'padānta', 'operation': 'visarga'}, {'range': '8.4', 'left': 'ṣ', 'pada_boundary': False, 'environment': 'padānta', 'operation': 'visarga'}),
    # neg: breaks predicate for 8.4.36
    "8.4.36": _fx_pair({'range': '8.4', 'dhatu': 'naś', 'condition': 'ṣānta', 'operation': 'substitution', 'environment': 'tiṅ'}, {'range': '8.4', 'dhatu': 'naś', 'condition': 'ṣānta', 'operation': 'substitution', 'environment': 'loka'}),
    # neg: breaks predicate for 8.4.37
    "8.4.37": _fx_pair({'range': '8.4', 'pada_boundary': True, 'environment': 'padānta', 'operation': 'substitution', 'final_sound': 's'}, {'range': '8.4', 'pada_boundary': False, 'environment': 'padānta', 'operation': 'substitution', 'final_sound': 's'}),
    # neg: breaks predicate for 8.4.38
    "8.4.38": _fx_pair({'range': '8.4', 'environment': 'padavyavāya', 'pada_boundary': True, 'rule': 'api', 'operation': 'substitution'}, {'range': '8.4', 'environment': 'padavyavāya', 'pada_boundary': False, 'rule': 'api', 'operation': 'substitution'}),
    # neg: breaks predicate for 8.4.39
    "8.4.39": _fx_pair({'range': '8.4', 'dhatu': 'kshubhna', 'rule': 'ca', 'environment': 'padānta', 'operation': 'substitution'}, {'range': '8.4', 'dhatu': 'pac', 'rule': 'ca', 'environment': 'padānta', 'operation': 'substitution'}),
    # neg: breaks predicate for 8.4.40
    "8.4.40": _fx_pair({'range': '8.4', 'stem': 'stu', 'operation': 'pluti', 'substitute': 'ścu', 'augment': 'ścuna'}, {'range': '8.4', 'stem': 'stu', 'operation': 'lopa', 'substitute': 'ścu', 'augment': 'ścuna'}),
    # neg: breaks predicate for 8.4.41
    "8.4.41": _fx_pair({'range': '8.4', 'operation': 'pluti', 'substitute': 'ṣṭu', 'augment': 'ṣṭuna', 'environment': 'padānta'}, {'range': '8.4', 'operation': 'lopa', 'substitute': 'ṣṭu', 'augment': 'ṣṭuna', 'environment': 'padānta'}),
    # neg: breaks predicate for 8.4.42
    "8.4.42": _fx_pair({'range': '8.4', 'pada_boundary': True, 'left': 'ṭ', 'rule_blocked': True, 'condition': 'anām'}, {'range': '8.4', 'pada_boundary': True, 'left': 'ṭ', 'rule_blocked': False, 'condition': 'anām'}),
    # neg: breaks predicate for 8.4.43
    "8.4.43": _fx_pair({'range': '8.4', 'left': 't', 'environment': 'ṣi', 'operation': 'substitution', 'final_sound': 's'}, {'range': '8.4', 'left': 't', 'environment': 'li', 'operation': 'substitution', 'final_sound': 's'}),
    # neg: empty word — not saṃhitā
    "8.4.44": _fx_pair({'range': '8.4', 'left': 'ś', 'operation': 'substitution', 'environment': 'sandhi', 'word': 'devaḥ'}, {'range': '8.4', 'left': 'ś', 'operation': 'substitution', 'environment': 'sandhi', 'word': ''}),
    # neg: breaks predicate for 8.4.45
    "8.4.45": _fx_pair({'range': '8.4', 'phoneme_class': 'yara', 'environment': 'anunāsika', 'substitute': 'anunāsika', 'optional': True}, {'range': '8.4', 'phoneme_class': 'yara', 'environment': 'anunāsika', 'substitute': 'anunāsika', 'optional': False}),
    # neg: breaks predicate for 8.4.46
    "8.4.46": _fx_pair({'range': '8.4', 'phoneme_class': 'ac', 'left': 'r', 'operation': 'duplication', 'count': 2}, {'range': '8.4', 'phoneme_class': 'ac', 'left': 'r', 'operation': 'duplication', 'count': 1}),
    # neg: breaks predicate for 8.4.47
    "8.4.47": _fx_pair({'range': '8.4', 'environment': 'anac', 'rule': 'ca', 'operation': 'substitution', 'word': 'agni'}, {'range': '8.4', 'environment': 'anac', 'rule': 'ca', 'operation': 'substitution', 'word': ''}),
    # neg: breaks predicate for 8.4.48
    "8.4.48": _fx_pair({'range': '8.4', 'environment': 'ādini', 'environment_2': 'ākrośa', 'rule_blocked': True, 'semantic': 'putra'}, {'range': '8.4', 'environment': 'ādini', 'environment_2': 'ākrośa', 'rule_blocked': False, 'semantic': 'putra'}),
    # neg: breaks predicate for 8.4.49
    "8.4.49": _fx_pair({'range': '8.4', 'left': 'śar', 'environment': 'ac', 'operation': 'substitution', 'word': 'śaraḥ'}, {'range': '8.4', 'left': 'śar', 'environment': 'ac', 'operation': 'substitution', 'word': ''}),
    # neg: breaks predicate for 8.4.50
    "8.4.50": _fx_pair({'range': '8.4', 'environment': 'triprabhṛti', 'authority': 'śākaṭāyana', 'operation': 'substitution', 'word': 'tri'}, {'range': '8.4', 'environment': 'triprabhṛti', 'authority': 'śākaṭāyana', 'operation': 'substitution', 'word': ''}),
    # neg: breaks predicate for 8.4.51
    "8.4.51": _fx_pair({'range': '8.4', 'scope': 'sarvatra', 'authority': 'śākalya', 'operation': 'substitution', 'word': 'agni'}, {'range': '8.4', 'scope': 'sarvatra', 'authority': 'śākalya', 'operation': 'substitution', 'word': ''}),
    # neg: breaks predicate for 8.4.52
    "8.4.52": _fx_pair({'range': '8.4', 'vowel_weight': 'dīrgha', 'authority': 'ācārya', 'operation': 'substitution', 'word': 'agni'}, {'range': '8.4', 'vowel_weight': 'hrasva', 'authority': 'ācārya', 'operation': 'substitution', 'word': 'agni'}),
    # neg: breaks predicate for 8.4.53
    "8.4.53": _fx_pair({'range': '8.4', 'phoneme_class': 'jhal', 'substitute': 'jaś', 'environment': 'jhaśi', 'word': 'agni'}, {'range': '8.4', 'phoneme_class': 'jhal', 'substitute': 'jaś', 'environment': 'jhaśi', 'word': ''}),
    # neg: breaks predicate for 8.4.54
    "8.4.54": _fx_pair({'range': '8.4', 'environment': 'abhyāsa', 'dhatu': 'car', 'rule': 'ca', 'operation': 'substitution'}, {'range': '8.4', 'environment': 'abhyāsa', 'dhatu': 'car', 'rule': 'na', 'operation': 'substitution'}),
    # neg: breaks predicate for 8.4.55
    "8.4.55": _fx_pair({'range': '8.4', 'environment': 'khari', 'rule': 'ca', 'operation': 'substitution', 'word': 'agni'}, {'range': '8.4', 'environment': 'khari', 'rule': 'na', 'operation': 'substitution', 'word': 'agni'}),
    # neg: mid-word index — optional avasāna rule fails
    "8.4.56": _fx_pair({'range': '8.4', 'optional': True, 'environment': 'avasāna', 'word': 'deva', 'index': 4, 'rule': 'vā'}, {'range': '8.4', 'optional': True, 'environment': 'avasāna', 'word': 'deva', 'index': 1, 'rule': 'vā'}),
    # neg: breaks predicate for 8.4.57
    "8.4.57": _fx_pair({'range': '8.4', 'suffix': 'aṇ', 'condition': 'aprāgṛhya', 'substitute': 'anunāsika', 'environment': 'padānta'}, {'range': '8.4', 'suffix': 'aṇ', 'condition': 'pragṛhya', 'substitute': 'anunāsika', 'environment': 'padānta'}),
    # neg: breaks predicate for 8.4.58
    "8.4.58": _fx_pair({'range': '8.4', 'left': 'anusvāra', 'environment': 'yayi', 'substitute': 'parasavarna', 'word': 'saṃ'}, {'range': '8.4', 'left': 'anusvāra', 'environment': 'yayi', 'substitute': 'parasavarna', 'word': ''}),
    # neg: breaks predicate for 8.4.59
    "8.4.59": _fx_pair({'range': '8.4', 'pada_boundary': True, 'optional': True, 'environment': 'padānta', 'rule': 'vā'}, {'range': '8.4', 'pada_boundary': True, 'optional': False, 'environment': 'padānta', 'rule': 'vā'}),
    # neg: breaks predicate for 8.4.60
    "8.4.60": _fx_pair({'range': '8.4', 'left': 't', 'environment': 'li', 'operation': 'substitution', 'final_sound': 's'}, {'range': '8.4', 'left': 't', 'environment': 'ṣi', 'operation': 'substitution', 'final_sound': 's'}),
    # neg: breaks predicate for 8.4.61
    "8.4.61": _fx_pair({'range': '8.4', 'left': 'ud', 'right': 'sthā', 'relation': 'pūrva', 'operation': 'substitution'}, {'range': '8.4', 'left': 'ud', 'right': 'pac', 'relation': 'pūrva', 'operation': 'substitution'}),
    # neg: breaks predicate for 8.4.62
    "8.4.62": _fx_pair({'range': '8.4', 'phoneme_class': 'jhay', 'substitute': 'ho', 'optional': True, 'environment': 'sandhi'}, {'range': '8.4', 'phoneme_class': 'jhay', 'substitute': 'ho', 'optional': False, 'environment': 'sandhi'}),
    # neg: breaks predicate for 8.4.63
    "8.4.63": _fx_pair({'range': '8.4', 'left': 'ś', 'substitute': 'ch', 'environment': 'ṭi', 'operation': 'substitution'}, {'range': '8.4', 'left': 'ś', 'substitute': 'ch', 'environment': 'li', 'operation': 'substitution'}),
    # neg: breaks predicate for 8.4.64
    "8.4.64": _fx_pair({'range': '8.4', 'phoneme_class': 'hal', 'environment': 'yami', 'operation': 'lopa', 'right': 'yam'}, {'range': '8.4', 'phoneme_class': 'hal', 'environment': 'yami', 'operation': 'ṇati', 'right': 'yam'}),
    # neg: breaks predicate for 8.4.65
    "8.4.65": _fx_pair({'range': '8.4', 'phoneme_class': 'jhar', 'environment': 'jhari', 'condition': 'savarṇa', 'word': 'agni'}, {'range': '8.4', 'phoneme_class': 'jhar', 'environment': 'jhari', 'condition': 'savarṇa', 'word': ''}),
    # neg: breaks predicate for 8.4.66
    "8.4.66": _fx_pair({'range': '8.4', 'accent_left': 'udātta', 'accent': 'anudātta', 'substitute': 'svarita', 'environment': 'sandhi'}, {'range': '8.4', 'accent_left': 'anudātta', 'accent': 'anudātta', 'substitute': 'svarita', 'environment': 'sandhi'}),
    # neg: breaks predicate for 8.4.67
    "8.4.67": _fx_pair({'range': '8.4', 'authority': 'agargya', 'rule_blocked': True, 'accent': 'udātta-svaritodaya', 'environment': 'accent'}, {'range': '8.4', 'authority': 'agargya', 'rule_blocked': False, 'accent': 'udātta-svaritodaya', 'environment': 'accent'}),
    # neg: index before word end — not avasāna (8.4.68)
    "8.4.68": _fx_pair({'range': '8.4', 'final_sound': 'a', 'pause_marker': 'iti', 'operation': 'avasāna', 'word': 'deva', 'index': 4}, {'range': '8.4', 'final_sound': 'a', 'pause_marker': 'iti', 'operation': 'avasāna', 'word': 'deva', 'index': 1}),
}

META: dict[str, SutraMeta] = {
    "8.4.1": SutraMeta(_VIDHI, "रषाभ्यां नो णः समानपदे ।", ("domain:avasana", "pada:8.4", "8_4_1")),
    "8.4.2": SutraMeta(_VIDHI, "अट्कुप्वाङ्नुम्व्यवायेऽपि ।", ("domain:avasana", "pada:8.4", "8_4_2")),
    "8.4.3": SutraMeta(_VIDHI, "पूर्वपदात्‌ संज्ञायामगः ।", ("domain:avasana", "pada:8.4", "8_4_3")),
    "8.4.4": SutraMeta(_VIDHI, "वनं पुरगामिश्रकासिध्रकाशारिकाकोटराऽग्रेभ्यः ।", ("domain:avasana", "pada:8.4", "8_4_4")),
    "8.4.5": SutraMeta(_VIDHI, "प्रनिरन्तःशरेक्षुप्लक्षाम्रकार्ष्यखदिरपियूक्षाभ्योऽसंज्ञायामपि ।", ("domain:avasana", "pada:8.4", "8_4_5")),
    "8.4.6": SutraMeta(_VIDHI, "विभाषौषधिवनस्पतिभ्यः ।", ("domain:avasana", "pada:8.4", "8_4_6")),
    "8.4.7": SutraMeta(_VIDHI, "अह्नोऽदन्तात्‌ ।", ("domain:avasana", "pada:8.4", "8_4_7")),
    "8.4.8": SutraMeta(_VIDHI, "वाहनमाहितात्‌ ।", ("domain:avasana", "pada:8.4", "8_4_8")),
    "8.4.9": SutraMeta(_VIDHI, "पानं देशे ।", ("domain:avasana", "pada:8.4", "8_4_9")),
    "8.4.10": SutraMeta(_VIDHI, "वा भावकरणयोः ।", ("domain:avasana", "pada:8.4", "8_4_10")),
    "8.4.11": SutraMeta(_VIDHI, "प्रातिपदिकान्तनुम्विभक्तिषु च ।", ("domain:avasana", "pada:8.4", "8_4_11")),
    "8.4.12": SutraMeta(_VIDHI, "एकाजुत्तरपदे णः ।", ("domain:avasana", "pada:8.4", "8_4_12")),
    "8.4.13": SutraMeta(_VIDHI, "कुमति च ।", ("domain:avasana", "pada:8.4", "8_4_13")),
    "8.4.14": SutraMeta(_VIDHI, "उपसर्गादसमासेऽपि णोपदेशस्य ।", ("domain:avasana", "pada:8.4", "8_4_14")),
    "8.4.15": SutraMeta(_VIDHI, "हिनुमीना ।", ("domain:avasana", "pada:8.4", "8_4_15")),
    "8.4.16": SutraMeta(_VIDHI, "आनि लोट् ।", ("domain:avasana", "pada:8.4", "8_4_16")),
    "8.4.17": SutraMeta(_VIDHI, "नेर्गदनदपतपदघुमास्यतिहन्तियातिवातिद्रातिप्सातिवपतिवहतिशाम्यतिचिनोतिदेग्धिषु च ।", ("domain:avasana", "pada:8.4", "8_4_17")),
    "8.4.18": SutraMeta(_VIDHI, "शेषे विभाषाऽकखादावषान्त उपदेशे ।", ("domain:avasana", "pada:8.4", "8_4_18")),
    "8.4.19": SutraMeta(_VIDHI, "अनितेः ।", ("domain:avasana", "pada:8.4", "8_4_19")),
    "8.4.20": SutraMeta(_VIDHI, "अन्तः ।", ("domain:avasana", "pada:8.4", "8_4_20")),
    "8.4.21": SutraMeta(_VIDHI, "उभौ साभ्यासस्य ।", ("domain:avasana", "pada:8.4", "8_4_21")),
    "8.4.22": SutraMeta(_VIDHI, "हन्तेरत्पूर्वस्य ।", ("domain:avasana", "pada:8.4", "8_4_22")),
    "8.4.23": SutraMeta(_VIDHI, "वमोर्वा ।", ("domain:avasana", "pada:8.4", "8_4_23")),
    "8.4.24": SutraMeta(_VIDHI, "अन्तरदेशे ।", ("domain:avasana", "pada:8.4", "8_4_24")),
    "8.4.25": SutraMeta(_VIDHI, "अयनं च ।", ("domain:avasana", "pada:8.4", "8_4_25")),
    "8.4.26": SutraMeta(_VIDHI, "छन्दस्यृदवग्रहात्‌ ।", ("domain:avasana", "pada:8.4", "8_4_26")),
    "8.4.27": SutraMeta(_VIDHI, "नश्च धातुस्थोरुषुभ्यः ।", ("domain:avasana", "pada:8.4", "8_4_27")),
    "8.4.28": SutraMeta(_VIDHI, "उपसर्गाद् बहुलम् ।", ("domain:avasana", "pada:8.4", "8_4_28")),
    "8.4.29": SutraMeta(_VIDHI, "कृत्यचः ।", ("domain:avasana", "pada:8.4", "8_4_29")),
    "8.4.30": SutraMeta(_VIDHI, "णेर्विभाषा ।", ("domain:avasana", "pada:8.4", "8_4_30")),
    "8.4.31": SutraMeta(_VIDHI, "हलश्च इजुपधात्‌ ।", ("domain:avasana", "pada:8.4", "8_4_31")),
    "8.4.32": SutraMeta(_VIDHI, "इजादेः सनुमः ।", ("domain:avasana", "pada:8.4", "8_4_32")),
    "8.4.33": SutraMeta(_VIDHI, "वा निंसनिक्षनिन्दाम् ।", ("domain:avasana", "pada:8.4", "8_4_33")),
    "8.4.34": SutraMeta(_VIDHI, "न भाभूपूकमिगमिप्यायीवेपाम् ।", ("domain:avasana", "pada:8.4", "8_4_34")),
    "8.4.35": SutraMeta(_VIDHI, "षात्‌ पदान्तात्‌ ।", ("domain:avasana", "pada:8.4", "8_4_35")),
    "8.4.36": SutraMeta(_VIDHI, "नशेः षान्तस्य ।", ("domain:avasana", "pada:8.4", "8_4_36")),
    "8.4.37": SutraMeta(_VIDHI, "पदान्तस्य ।", ("domain:avasana", "pada:8.4", "8_4_37")),
    "8.4.38": SutraMeta(_VIDHI, "पदव्यवायेऽपि ।", ("domain:avasana", "pada:8.4", "8_4_38")),
    "8.4.39": SutraMeta(_VIDHI, "क्षुभ्नाऽऽदिषु च ।", ("domain:avasana", "pada:8.4", "8_4_39")),
    "8.4.40": SutraMeta(_VIDHI, "स्तोः श्चुना श्चुः ।", ("domain:avasana", "pada:8.4", "8_4_40")),
    "8.4.41": SutraMeta(_VIDHI, "ष्टुना ष्टुः ।", ("domain:avasana", "pada:8.4", "8_4_41")),
    "8.4.42": SutraMeta(_VIDHI, "न पदान्ताट्टोरनाम् ।", ("domain:avasana", "pada:8.4", "8_4_42")),
    "8.4.43": SutraMeta(_VIDHI, "तोः षि ।", ("domain:avasana", "pada:8.4", "8_4_43")),
    "8.4.44": SutraMeta(_VIDHI, "शात्‌ ।", ("domain:avasana", "pada:8.4", "8_4_44")),
    "8.4.45": SutraMeta(_VIDHI, "यरोऽनुनासिकेऽनुनासिको वा ।", ("domain:avasana", "pada:8.4", "8_4_45")),
    "8.4.46": SutraMeta(_VIDHI, "अचो रहाभ्यां द्वे ।", ("domain:avasana", "pada:8.4", "8_4_46")),
    "8.4.47": SutraMeta(_VIDHI, "अनचि च ।", ("domain:avasana", "pada:8.4", "8_4_47")),
    "8.4.48": SutraMeta(_VIDHI, "नादिन्याक्रोशे पुत्रस्य ।", ("domain:avasana", "pada:8.4", "8_4_48")),
    "8.4.49": SutraMeta(_VIDHI, "शरोऽचि ।", ("domain:avasana", "pada:8.4", "8_4_49")),
    "8.4.50": SutraMeta(_VIDHI, "त्रिप्रभृतिषु शाकटायनस्य ।", ("domain:avasana", "pada:8.4", "8_4_50")),
    "8.4.51": SutraMeta(_VIDHI, "सर्वत्र शाकल्यस्य ।", ("domain:avasana", "pada:8.4", "8_4_51")),
    "8.4.52": SutraMeta(_VIDHI, "दीर्घादाचार्याणाम् ।", ("domain:avasana", "pada:8.4", "8_4_52")),
    "8.4.53": SutraMeta(_VIDHI, "झलां जश् झशि ।", ("domain:avasana", "pada:8.4", "8_4_53")),
    "8.4.54": SutraMeta(_VIDHI, "अभ्यासे चर्च्च ।", ("domain:avasana", "pada:8.4", "8_4_54")),
    "8.4.55": SutraMeta(_VIDHI, "खरि च ।", ("domain:avasana", "pada:8.4", "8_4_55")),
    "8.4.56": SutraMeta(_VIDHI, "वाऽवसाने ।", ("domain:avasana", "pada:8.4", "8_4_56")),
    "8.4.57": SutraMeta(_VIDHI, "अणोऽप्रगृह्यस्यानुनासिकः ।", ("domain:avasana", "pada:8.4", "8_4_57")),
    "8.4.58": SutraMeta(_VIDHI, "अनुस्वारस्य ययि परसवर्णः ।", ("domain:avasana", "pada:8.4", "8_4_58")),
    "8.4.59": SutraMeta(_VIDHI, "वा पदान्तस्य ।", ("domain:avasana", "pada:8.4", "8_4_59")),
    "8.4.60": SutraMeta(_VIDHI, "तोर्लि ।", ("domain:avasana", "pada:8.4", "8_4_60")),
    "8.4.61": SutraMeta(_VIDHI, "उदः स्थास्तम्भोः पूर्वस्य ।", ("domain:avasana", "pada:8.4", "8_4_61")),
    "8.4.62": SutraMeta(_VIDHI, "झयो होऽन्यतरस्याम् ।", ("domain:avasana", "pada:8.4", "8_4_62")),
    "8.4.63": SutraMeta(_VIDHI, "शश्छोऽटि ।", ("domain:avasana", "pada:8.4", "8_4_63")),
    "8.4.64": SutraMeta(_VIDHI, "हलो यमां यमि लोपः ।", ("domain:avasana", "pada:8.4", "8_4_64")),
    "8.4.65": SutraMeta(_VIDHI, "झरो झरि सवर्णे ।", ("domain:avasana", "pada:8.4", "8_4_65")),
    "8.4.66": SutraMeta(_VIDHI, "उदात्तादनुदात्तस्य स्वरितः ।", ("domain:avasana", "pada:8.4", "8_4_66")),
    "8.4.67": SutraMeta(_VIDHI, "नोदात्तस्वरितोदयमगार्ग्यकाश्यपगालवानाम्‌ ।", ("domain:avasana", "pada:8.4", "8_4_67")),
    "8.4.68": SutraMeta(_VIDHI, "अ अ इति ।", ("domain:avasana", "pada:8.4", "8_4_68")),
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
        raise AssertionError("sutra_impl_8_4 self_check failed:\n" + "\n".join(failures))
    handlers = [n for n in globals() if n.startswith("sutra_8_4_") and callable(globals()[n])]
    return {
        "sutras": len(FIXTURES),
        "predicates": len(handlers),
        "meta": len(META),
    }

(
    IMPLEMENTED_IDS,
    has_real_implementation,
    handler_for,
    positive_features,
    negative_features,
) = make_module_api(FIXTURES, globals())

_COUNTS = self_check()

if __name__ == "__main__":
    for label, value in _COUNTS.items():
        print(f"{label}: {value}")
