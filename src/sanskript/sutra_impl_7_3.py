"""
Discrete Pāṇinian predicates for Adhyāya 7.3 (ādeśa / insertions).

Hand-written per sūtra from padaccheda in data/ashtadhyayi_sutras.json.
Domain: substitute segments (āt, num, nasal) and pratyāhāra insertions
on aṅgas and related bases (range 7.3).
"""
from __future__ import annotations

from .anga import apply_anga_operation, operations_for_range
from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api

_SAMJNA = 'samjna'
_PARIBHASHA = 'paribhasha'
_VIDHI = 'vidhi'
_PRATISEDHA = 'pratisedha'
_VIBHASHA = 'vibhasha'


def _in_adesha_range(c) -> bool:
    """True when context is in the 7.3 ādeśa operation domain."""
    return any(op.sutra_range == "7.3" for op in operations_for_range(str(c.get("range"))))


DEVIKA_ASHIMSHAPADITYAVAT = frozenset({
    "devikā",
    "śiṃśapa",
    "pāditya",
    "vāṭ",
    "dīrgha",
    "satra",
    "śreya"
})

def sutra_7_3_1(c) -> bool:
    """देविकाशिंशपादित्यवाड्दीर्घसत्रश्रेयसामात्‌"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _in(c, "stem_class", DEVIKA_ASHIMSHAPADITYAVAT) and _eq(c, 'stem_group', 'dīrghasatraśreyas')

def sutra_7_3_2(c) -> bool:
    """केकयमित्त्रयुप्रलयानां यादेरियः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'iya') and _eq(c, 'source', 'yādeḥ') and _eq(c, 'stem_class', 'kekayamittrayupralaya')

def sutra_7_3_3(c) -> bool:
    """न य्वाभ्यां पदान्ताभ्याम् पूर्वौ तु ताभ्यामैच्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'aic') and _eq(c, 'source', 'padāntābhyām') and _eq(c, 'scope', 'pūrvau') and _eq(c, 'pratisedha', 'yvābhyām')

def sutra_7_3_4(c) -> bool:
    """द्वारादीनां च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem_class', 'dvārādi') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_5(c) -> bool:
    """न्यग्रोधस्य च केवलस्य"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem', 'nyagrodha') and _eq(c, 'semantic', 'kevala') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_6(c) -> bool:
    """न कर्मव्यतिहारे"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'pratisedha') and _eq(c, 'semantic', 'karmavyatihāra') and _eq(c, 'pratisedha', 'na')

def sutra_7_3_7(c) -> bool:
    """स्वागतादीनां च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem_class', 'svāgatādi') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_8(c) -> bool:
    """श्वादेरिञि"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem_class', 'śvādi') and _eq(c, 'suffix', 'iñ')

def sutra_7_3_9(c) -> bool:
    """पदान्तस्यान्यतरस्याम्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'source', 'padānta') and bool(c.get('optional')) is True

def sutra_7_3_10(c) -> bool:
    """उत्तरपदस्य"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'adhikāra') and _eq(c, 'insertion', 'uttarapada') and _in_adesha_range(c)

def sutra_7_3_11(c) -> bool:
    """अवयवादृतोः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'source', 'avayavāt') and _eq(c, 'stem_class', 'ṛtoḥ')

def sutra_7_3_12(c) -> bool:
    """सुसर्वार्धाज्जनपदस्य"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'source', 'susarvārdhāt') and _eq(c, 'stem_class', 'janapadasya')

def sutra_7_3_13(c) -> bool:
    """दिशोऽमद्राणाम्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'source', 'diśaḥ') and _eq(c, 'stem_class', 'amadrāṇām')

def sutra_7_3_14(c) -> bool:
    """प्राचां ग्रामनगराणाम्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'prācām') and _eq(c, 'semantic', 'grāmanagarāṇām')

def sutra_7_3_15(c) -> bool:
    """संख्यायाः संवत्सरसंख्यस्य च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'source', 'saṃkhyāyāḥ') and _eq(c, 'stem_class', 'saṃvatsarasaṃkhyasya') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_16(c) -> bool:
    """वर्षस्याभविष्यति"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'varṣasya') and _eq(c, 'suffix_context', 'abhaviṣyati')

def sutra_7_3_17(c) -> bool:
    """परिमाणान्तस्यासंज्ञाशाणयोः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'parimāṇāntasya') and _eq(c, 'suffix_context', 'asaṃjñāśāṇayoḥ')

def sutra_7_3_18(c) -> bool:
    """जे प्रोष्ठपदानाम्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'proṣṭhapadānām') and _eq(c, 'suffix_context', 'je')

def sutra_7_3_19(c) -> bool:
    """हृद्भगसिन्ध्वन्ते पूर्वपदस्य च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem_class', 'pūrvapadasya') and _eq(c, 'suffix_context', 'hṛdbhagasindhvante') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_20(c) -> bool:
    """अनुशतिकादीनां च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem_class', 'anuśatikādi') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_21(c) -> bool:
    """देवताद्वंद्वे च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'suffix_context', 'devatādvandve') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_22(c) -> bool:
    """नेन्द्रस्य परस्य"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'pratisedha') and _eq(c, 'stem_class', 'indrasya') and _eq(c, 'semantic', 'parasya') and _eq(c, 'pratisedha', 'na')

def sutra_7_3_23(c) -> bool:
    """दीर्घाच्च वरुणस्य"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'source', 'dīrghāt') and _eq(c, 'stem_class', 'varuṇasya') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_24(c) -> bool:
    """प्राचां नगरान्ते"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'prācām') and _eq(c, 'suffix_context', 'nagarānte')

def sutra_7_3_25(c) -> bool:
    """जङ्गलधेनुवलजान्तस्य विभाषितमुत्तरम्‌"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'uttaram') and _eq(c, 'stem_class', 'jaṅgaladhenuvalajāntasya') and _eq(c, 'semantic', 'vibhāṣitam')

def sutra_7_3_26(c) -> bool:
    """अर्धात्‌ परिमाणस्य पूर्वस्य तु वा"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'source', 'ardhāt') and _eq(c, 'stem_class', 'parimāṇasya') and _eq(c, 'semantic', 'pūrvasya') and _eq(c, 'anuvritti', 'tu') and bool(c.get('optional')) is True

def sutra_7_3_27(c) -> bool:
    """नातः परस्य"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'pratisedha') and _eq(c, 'stem_class', 'ataḥ') and _eq(c, 'semantic', 'parasya') and _eq(c, 'pratisedha', 'na')

def sutra_7_3_28(c) -> bool:
    """प्रवाहणस्य ढे"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'pravāhaṇasya') and _eq(c, 'suffix_context', 'ḍhe')

def sutra_7_3_29(c) -> bool:
    """तत्प्रत्ययस्य च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem_class', 'tatpratyayasya') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_30(c) -> bool:
    """नञः शुचीश्वरक्षेत्रज्ञकुशलनिपुणानाम्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'source', 'nañaḥ') and _eq(c, 'stem_class', 'śucīśvarakṣetrajñakuśalanipuṇānām')

def sutra_7_3_31(c) -> bool:
    """यथातथयथापुरयोः पर्यायेण"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'yathātathayathāpurayoḥ')

def sutra_7_3_32(c) -> bool:
    """हनस्तोऽचिण्णलोः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'taḥ') and _eq(c, 'stem_class', 'hanaḥ') and _eq(c, 'suffix_context', 'aciṇṇaloḥ')

def sutra_7_3_33(c) -> bool:
    """आतो युक् चिण्कृतोः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'yuk') and _eq(c, 'stem_class', 'ātaḥ') and _eq(c, 'suffix_context', 'ciṇkṛtoḥ')

def sutra_7_3_34(c) -> bool:
    """नोदात्तोपदेशस्य मान्तस्यानाचमेः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'pratisedha') and _eq(c, 'stem_class', 'udāttopadeśasya') and _eq(c, 'semantic', 'māntasya') and _eq(c, 'pratisedha', 'na')

def sutra_7_3_35(c) -> bool:
    """जनिवध्योश्च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem_class', 'janivadhyoḥ') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_36(c) -> bool:
    """अर्त्तिह्रीब्लीरीक्नूयीक्ष्माय्यातां पुङ्णौ"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'puk') and _eq(c, 'stem_class', 'arttihrīvlīrīknūyīkṣmāyyātām') and _eq(c, 'suffix_context', 'ṇau')

def sutra_7_3_37(c) -> bool:
    """शाच्छासाह्वाव्यावेपां युक्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'yuk') and _eq(c, 'stem_class', 'śācchāsāhvāvyāvepām')

def sutra_7_3_38(c) -> bool:
    """वो विधूनने जुक्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'juk') and _eq(c, 'stem_class', 'vaḥ') and _eq(c, 'suffix_context', 'vidhūnane')

def sutra_7_3_39(c) -> bool:
    """लीलोर्नुग्लुकावन्यतरस्यां स्नेहविपातने"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'nuglukau') and _eq(c, 'stem_class', 'līloḥ') and _eq(c, 'suffix_context', 'anyatarasyām') and _eq(c, 'semantic', 'snehavipātane')

def sutra_7_3_40(c) -> bool:
    """भियो हेतुभये षुक्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'ṣuk') and _eq(c, 'stem_class', 'bhiyaḥ') and _eq(c, 'suffix_context', 'hetubhaye')

def sutra_7_3_41(c) -> bool:
    """स्फायो वः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'vaḥ') and _eq(c, 'stem_class', 'sphāyaḥ')

def sutra_7_3_42(c) -> bool:
    """शदेरगतौ तः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'taḥ') and _eq(c, 'stem_class', 'śadeḥ') and _eq(c, 'suffix_context', 'agatau')

def sutra_7_3_43(c) -> bool:
    """रुहः पोऽन्यतरस्याम्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'paḥ') and _eq(c, 'stem_class', 'ruhaḥ') and _eq(c, 'suffix_context', 'anyatarasyām')

def sutra_7_3_44(c) -> bool:
    """प्रत्ययस्थात्‌ कात्‌ पूर्वस्यात इदाप्यसुपः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'it') and _eq(c, 'source', 'pratyayasthāt') and _eq(c, 'stem_class', 'pūrvasya') and _eq(c, 'suffix_context', 'āpi') and _eq(c, 'semantic', 'ataḥ')

def sutra_7_3_45(c) -> bool:
    """न यासयोः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'pratisedha') and _eq(c, 'stem_class', 'yāsayoḥ') and _eq(c, 'pratisedha', 'na')

def sutra_7_3_46(c) -> bool:
    """उदीचामातः स्थाने यकपूर्वायाः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'udīcām') and _eq(c, 'suffix_context', 'sthāne') and _eq(c, 'semantic', 'ātaḥ')

def sutra_7_3_47(c) -> bool:
    """भस्त्रैषाऽजाज्ञाद्वास्वानञ्पूर्वाणामपि"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'pratisedha') and _eq(c, 'substitute', 'bhastraiṣāऽjājñādvāsvāḥ') and _eq(c, 'stem_class', 'nañpūrvāṇām') and _eq(c, 'pratisedha', 'na')

def sutra_7_3_48(c) -> bool:
    """अभाषितपुंस्काच्च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'source', 'abhāṣitapuṃskā') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_49(c) -> bool:
    """आदाचार्याणाम्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem_class', 'ācāryāṇām')

def sutra_7_3_50(c) -> bool:
    """ठस्येकः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'ika') and _eq(c, 'source', 'ṭha')

def sutra_7_3_51(c) -> bool:
    """इसुसुक्तान्तात्‌ कः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'kaḥ') and _eq(c, 'source', 'isusuktāntāt')

def sutra_7_3_52(c) -> bool:
    """चजोः कु घिन्ण्यतोः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'ku') and _eq(c, 'stem_class', 'cajoḥ') and _eq(c, 'suffix_context', 'ghinṇyatoḥ')

def sutra_7_3_53(c) -> bool:
    """न्यङ्क्वादीनां च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem_class', 'nyaṅkvādi') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_54(c) -> bool:
    """हो हन्तेर्ञ्णिन्नेषु"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'haḥ') and _eq(c, 'suffix_context', 'ñṇinneṣu') and _eq(c, 'semantic', 'hanteḥ')

def sutra_7_3_55(c) -> bool:
    """अभ्यासाच्च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'source', 'abhyāsāt') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_56(c) -> bool:
    """हेरचङि"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'heḥ') and _eq(c, 'suffix_context', 'acaṅi')

def sutra_7_3_57(c) -> bool:
    """सन्लिटोर्जेः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'jeḥ') and _eq(c, 'suffix_context', 'sanliṭoḥ')

def sutra_7_3_58(c) -> bool:
    """विभाषा चेः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'vibhāṣā') and _eq(c, 'stem_class', 'ceḥ')

def sutra_7_3_59(c) -> bool:
    """न क्वादेः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'pratisedha') and _eq(c, 'stem_class', 'kvādeḥ') and _eq(c, 'pratisedha', 'na')

def sutra_7_3_60(c) -> bool:
    """अजिवृज्योश्च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem_class', 'ajivṛjyoḥ') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_61(c) -> bool:
    """भुजन्युब्जौ पाण्युपतापयोः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'bhujanyubjau') and _eq(c, 'suffix_context', 'pāṇyupatāpayoḥ')

def sutra_7_3_62(c) -> bool:
    """प्रयाजानुयाजौ यज्ञाङ्गे"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'prayājānuyājau') and _eq(c, 'suffix_context', 'yajñāṅge')

def sutra_7_3_63(c) -> bool:
    """वञ्चेर्गतौ"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'vañceḥ') and _eq(c, 'suffix_context', 'gatau')

def sutra_7_3_64(c) -> bool:
    """ओक उचः के"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'okaḥ') and _eq(c, 'stem_class', 'ucaḥ') and _eq(c, 'suffix_context', 'ke')

def sutra_7_3_65(c) -> bool:
    """ण्य आवश्यके"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'suffix_context', 'ṇye') and _eq(c, 'semantic', 'āvaśyake')

def sutra_7_3_66(c) -> bool:
    """यजयाचरुचप्रवचर्चश्च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem_class', 'yajayācarucapravacarcaḥ') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_67(c) -> bool:
    """वचोऽशब्दसंज्ञायाम्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'vacaḥ') and _eq(c, 'suffix_context', 'aśabdasaṃjñāyām')

def sutra_7_3_68(c) -> bool:
    """प्रयोज्यनियोज्यौ शक्यार्थे"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'prayojyaniyojyau') and _eq(c, 'suffix_context', 'śakyārthe')

def sutra_7_3_69(c) -> bool:
    """भोज्यं भक्ष्ये"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'bhojyam') and _eq(c, 'suffix_context', 'bhakṣye')

def sutra_7_3_70(c) -> bool:
    """घोर्लोपो लेटि वा"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'lopaḥ') and _eq(c, 'stem_class', 'ghoḥ') and _eq(c, 'suffix_context', 'leṭi') and bool(c.get('optional')) is True

def sutra_7_3_71(c) -> bool:
    """ओतः श्यनि"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'otaḥ') and _eq(c, 'suffix_context', 'śyani')

def sutra_7_3_72(c) -> bool:
    """क्सस्याचि"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'ksasya') and _eq(c, 'suffix_context', 'aci')

def sutra_7_3_73(c) -> bool:
    """लुग्वा दुहदिहलिहगुहामात्मनेपदे दन्त्ये"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'luk') and _eq(c, 'stem_class', 'duhadihalihaguhām') and _eq(c, 'suffix_context', 'ātmanepade') and _eq(c, 'semantic', 'dantye') and bool(c.get('optional')) is True

def sutra_7_3_74(c) -> bool:
    """शमामष्टानां दीर्घः श्यनि"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'dīrghaḥ') and _eq(c, 'stem_class', 'śamām') and _eq(c, 'suffix_context', 'śyani') and _eq(c, 'semantic', 'aṣṭānām')

def sutra_7_3_75(c) -> bool:
    """ष्ठिवुक्लम्याचमां शिति"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'ṣṭhivuklamucamām') and _eq(c, 'suffix_context', 'śiti')

def sutra_7_3_76(c) -> bool:
    """क्रमः परस्मैपदेषु"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'kramaḥ') and _eq(c, 'suffix_context', 'parasmaipadeṣu')

def sutra_7_3_77(c) -> bool:
    """इषुगमियमां छः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'chaḥ') and _eq(c, 'stem_class', 'iṣugamiyamām')

def sutra_7_3_78(c) -> bool:
    """पाघ्राध्मास्थाम्नादाण्दृश्यर्त्तिसर्त्तिशदसदां पिबजिघ्रधमतिष्ठमनयच्छपश्यर्च्छधौशीयसीदाः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'pibajighradhamatiṣṭhamanayacchapaśyarcchadhauśīyasīdāḥ') and _eq(c, 'stem_class', 'pāghrādhmāsthāmnādāṇdṛśyarttisarttiśadasadām')

def sutra_7_3_79(c) -> bool:
    """ज्ञाजनोर्जा"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'jñājanoḥ')

def sutra_7_3_80(c) -> bool:
    """प्वादीनां ह्रस्वः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'hrasvaḥ') and _eq(c, 'stem_class', 'pvādi')

def sutra_7_3_81(c) -> bool:
    """मीनातेर्निगमे"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'mīnāteḥ') and _eq(c, 'suffix_context', 'nigame')

def sutra_7_3_82(c) -> bool:
    """मिदेर्गुणः"""
    return _eq(c, "range", "7.3") and _eq(c, "operation", "ṛ-guṇa") and any(op.name == "ṛ-guṇa" for op in operations_for_range("7.3")) and _eq(c, 'substitute', 'ar') and _eq(c, 'source', 'mid') and _eq(c, 'stem', 'mṛd') and apply_anga_operation(str(c.get("stem", "mid")), next(op for op in operations_for_range("7.3") if op.name == "ṛ-guṇa")) != str(c.get("stem", ""))

def sutra_7_3_83(c) -> bool:
    """जुसि च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'suffix_context', 'jusi') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_84(c) -> bool:
    """सार्वधातुकार्धधातुकयोः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'suffix_context', 'sārvadhātukārdhadhātukayoḥ')

def sutra_7_3_85(c) -> bool:
    """जाग्रोऽविचिण्णल्ङित्सु"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'jāgraḥ') and _eq(c, 'suffix_context', 'aviciṇṇalṅitsu')

def sutra_7_3_86(c) -> bool:
    """पुगन्तलघूपधस्य च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem_class', 'pugantalaghūpadhasya') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_87(c) -> bool:
    """नाभ्यस्तस्याचि पिति सार्वधातुके"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'pratisedha') and _eq(c, 'stem_class', 'abhyastasya') and _eq(c, 'suffix_context', 'aci') and _eq(c, 'semantic', 'sārvadhātuke') and _eq(c, 'pratisedha', 'na')

def sutra_7_3_88(c) -> bool:
    """भूसुवोस्तिङि"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'bhūsuvoḥ') and _eq(c, 'suffix_context', 'tiṅi')

def sutra_7_3_89(c) -> bool:
    """उतो वृद्धिर्लुकि हलि"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'vṛddhiḥ') and _eq(c, 'stem_class', 'utaḥ') and _eq(c, 'suffix_context', 'luki') and _eq(c, 'semantic', 'hali')

def sutra_7_3_90(c) -> bool:
    """ऊर्णोतेर्विभाषा"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'vibhāṣā') and _eq(c, 'stem_class', 'ūrṇoteḥ')

def sutra_7_3_91(c) -> bool:
    """गुणोऽपृक्ते"""
    return _eq(c, "range", "7.3") and _eq(c, "operation", "guṇa") and any(op.kind.value == "guṇa" for op in operations_for_range("7.3")) and _eq(c, 'semantic', 'apṛkta')

def sutra_7_3_92(c) -> bool:
    """तृणह इम्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'im') and _eq(c, 'stem_class', 'tṛṇahaḥ')

def sutra_7_3_93(c) -> bool:
    """ब्रुव ईट्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'īṭ') and _eq(c, 'source', 'bruvaḥ')

def sutra_7_3_94(c) -> bool:
    """यङो वा"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'source', 'yaṅaḥ') and bool(c.get('optional')) is True

def sutra_7_3_95(c) -> bool:
    """तुरुस्तुशम्यमः सार्वधातुके"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'source', 'turustuśamyamaḥ') and _eq(c, 'suffix_context', 'sārvadhātuke')

def sutra_7_3_96(c) -> bool:
    """अस्तिसिचोऽपृक्ते"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'source', 'astisicaḥ') and _eq(c, 'suffix_context', 'apṛkte')

def sutra_7_3_97(c) -> bool:
    """बहुलं छन्दसि"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'bahulam') and _eq(c, 'domain', 'chandas')

def sutra_7_3_98(c) -> bool:
    """रुदश्च पञ्चभ्यः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'source', 'rudaḥ') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_99(c) -> bool:
    """अड्गार्ग्यगालवयोः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'aṭ') and _eq(c, 'stem_class', 'gārgyagālavayoḥ')

def sutra_7_3_100(c) -> bool:
    """अदः सर्वेषाम्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'source', 'ad') and _eq(c, 'scope', 'sarva')

def sutra_7_3_101(c) -> bool:
    """अतो दीर्घो यञि"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'dīrghaḥ') and _eq(c, 'stem_class', 'ataḥ') and _eq(c, 'suffix_context', 'yañi')

def sutra_7_3_102(c) -> bool:
    """सुपि च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'suffix_context', 'supi') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_103(c) -> bool:
    """बहुवचने झल्येत्‌"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'et') and _eq(c, 'suffix_context', 'bahuvacane') and _eq(c, 'semantic', 'jhali')

def sutra_7_3_104(c) -> bool:
    """ओसि च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'suffix_context', 'osi') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_105(c) -> bool:
    """आङि चापः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'stem_class', 'āpaḥ') and _eq(c, 'suffix_context', 'āṅi') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_106(c) -> bool:
    """सम्बुद्धौ च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'suffix_context', 'sambuddhau') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_107(c) -> bool:
    """अम्बाऽर्थनद्योर्ह्रस्वः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'hrasvaḥ') and _eq(c, 'stem_class', 'ambāऽrthanadyoḥ')

def sutra_7_3_108(c) -> bool:
    """ह्रस्वस्य गुणः"""
    return _eq(c, "range", "7.3") and _eq(c, "operation", "guṇa") and any(op.kind.value == "guṇa" for op in operations_for_range("7.3")) and _eq(c, 'source', 'hrasva')

def sutra_7_3_109(c) -> bool:
    """जसि च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āt') and _eq(c, 'suffix_context', 'jasi') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_110(c) -> bool:
    """ऋतो ङिसर्वनामस्थानयोः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'ṅi') and _eq(c, 'source', 'ṛt') and _eq(c, 'suffix_context', 'sarvanāmasthāna')

def sutra_7_3_111(c) -> bool:
    """घेर्ङिति"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'stem_class', 'gheḥ') and _eq(c, 'suffix_context', 'ṅiti')

def sutra_7_3_112(c) -> bool:
    """आण्नद्याः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'āṭ') and _eq(c, 'source', 'nadyāḥ')

def sutra_7_3_113(c) -> bool:
    """याडापः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'yāṭ') and _eq(c, 'source', 'āpaḥ')

def sutra_7_3_114(c) -> bool:
    """सर्वनाम्नः स्याड्ढ्रस्वश्च"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'syāṭ') and _eq(c, 'source', 'sarvanāmnaḥ') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_115(c) -> bool:
    """विभाषा द्वितीयातृतीयाभ्याम्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'vibhāṣā') and _eq(c, 'source', 'dvitīyātṛtīyābhyām')

def sutra_7_3_116(c) -> bool:
    """ङेराम्नद्याम्नीभ्यः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'ām') and _eq(c, 'source', 'nadyāmnībhyaḥ') and _eq(c, 'stem_class', 'ṅeḥ')

def sutra_7_3_117(c) -> bool:
    """इदुद्भ्याम्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'source', 'idudbhyām')

def sutra_7_3_118(c) -> bool:
    """औत्‌"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'aut')

def sutra_7_3_119(c) -> bool:
    """अच्च घेः"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'at') and _eq(c, 'stem_class', 'gheḥ') and _eq(c, 'anuvritti', 'ca')

def sutra_7_3_120(c) -> bool:
    """आङो नाऽस्त्रियाम्"""
    return _eq(c, "range", "7.3") and _eq(c, 'operation', 'insertion') and _eq(c, 'substitute', 'na') and _eq(c, 'source', 'āṅ') and _eq(c, 'semantic', 'astrī')


def _fx_pair(pos: dict, neg: dict | None = None):
    if neg is None:
        neg = dict(pos)
        for key, bad in (
            ("range", "7.2"), ("stem_class", "other_stem"),
            ("substitute", "other_sub"), ("operation", "other_op"),
            ("optional", False), ("pratisedha", "none"), ("stem", "other_stem"),
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
    "7.3.1": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'devikā', 'stem_group': 'dīrghasatraśreyas', 'substitute': 'āt'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'stem_group': 'dīrghasatraśreyas', 'substitute': 'āt'}),
    "7.3.2": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'yādeḥ', 'stem_class': 'kekayamittrayupralaya', 'substitute': 'iya'}, {'operation': 'insertion', 'range': '7.3', 'source': 'yādeḥ', 'stem_class': 'other_stem', 'substitute': 'iya'}),
    "7.3.3": _fx_pair({'operation': 'insertion', 'pratisedha': 'yvābhyām', 'range': '7.3', 'scope': 'pūrvau', 'source': 'padāntābhyām', 'substitute': 'aic'}, {'operation': 'insertion', 'pratisedha': 'yvābhyām', 'range': '7.3', 'scope': 'pūrvau', 'source': 'padāntābhyām', 'substitute': 'other_sub'}),
    "7.3.4": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'dvārādi', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'āt'}),
    "7.3.5": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'semantic': 'kevala', 'stem': 'nyagrodha', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'semantic': 'kevala', 'stem': 'nyagrodha', 'substitute': 'other_sub'}),
    "7.3.6": _fx_pair({'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'semantic': 'karmavyatihāra'}, {'operation': 'other_op', 'pratisedha': 'na', 'range': '7.3', 'semantic': 'karmavyatihāra'}),
    "7.3.7": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'svāgatādi', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'āt'}),
    "7.3.8": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'śvādi', 'substitute': 'āt', 'suffix': 'iñ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'āt', 'suffix': 'iñ'}),
    "7.3.9": _fx_pair({'operation': 'insertion', 'optional': True, 'range': '7.3', 'source': 'padānta', 'substitute': 'āt'}, {'operation': 'insertion', 'optional': True, 'range': '7.3', 'source': 'padānta', 'substitute': 'other_sub'}),
    "7.3.10": _fx_pair({'insertion': 'uttarapada', 'operation': 'adhikāra', 'range': '7.3'}, {'insertion': 'uttarapada', 'operation': 'other_op', 'range': '7.3'}),
    "7.3.11": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'avayavāt', 'stem_class': 'ṛtoḥ'}, {'operation': 'insertion', 'range': '7.3', 'source': 'avayavāt', 'stem_class': 'other_stem'}),
    "7.3.12": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'susarvārdhāt', 'stem_class': 'janapadasya'}, {'operation': 'insertion', 'range': '7.3', 'source': 'susarvārdhāt', 'stem_class': 'other_stem'}),
    "7.3.13": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'diśaḥ', 'stem_class': 'amadrāṇām'}, {'operation': 'insertion', 'range': '7.3', 'source': 'diśaḥ', 'stem_class': 'other_stem'}),
    "7.3.14": _fx_pair({'operation': 'insertion', 'range': '7.3', 'semantic': 'grāmanagarāṇām', 'stem_class': 'prācām'}, {'operation': 'insertion', 'range': '7.3', 'semantic': 'grāmanagarāṇām', 'stem_class': 'other_stem'}),
    "7.3.15": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'source': 'saṃkhyāyāḥ', 'stem_class': 'saṃvatsarasaṃkhyasya', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'source': 'saṃkhyāyāḥ', 'stem_class': 'other_stem', 'substitute': 'āt'}),
    "7.3.16": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'varṣasya', 'suffix_context': 'abhaviṣyati'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'abhaviṣyati'}),
    "7.3.17": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'parimāṇāntasya', 'suffix_context': 'asaṃjñāśāṇayoḥ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'asaṃjñāśāṇayoḥ'}),
    "7.3.18": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'proṣṭhapadānām', 'suffix_context': 'je'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'je'}),
    "7.3.19": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'pūrvapadasya', 'substitute': 'āt', 'suffix_context': 'hṛdbhagasindhvante'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'āt', 'suffix_context': 'hṛdbhagasindhvante'}),
    "7.3.20": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'anuśatikādi', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'āt'}),
    "7.3.21": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'substitute': 'āt', 'suffix_context': 'devatādvandve'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'substitute': 'other_sub', 'suffix_context': 'devatādvandve'}),
    "7.3.22": _fx_pair({'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'semantic': 'parasya', 'stem_class': 'indrasya'}, {'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'semantic': 'parasya', 'stem_class': 'other_stem'}),
    "7.3.23": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'source': 'dīrghāt', 'stem_class': 'varuṇasya', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'source': 'dīrghāt', 'stem_class': 'other_stem', 'substitute': 'āt'}),
    "7.3.24": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'prācām', 'suffix_context': 'nagarānte'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'nagarānte'}),
    "7.3.25": _fx_pair({'operation': 'insertion', 'range': '7.3', 'semantic': 'vibhāṣitam', 'stem_class': 'jaṅgaladhenuvalajāntasya', 'substitute': 'uttaram'}, {'operation': 'insertion', 'range': '7.3', 'semantic': 'vibhāṣitam', 'stem_class': 'other_stem', 'substitute': 'uttaram'}),
    "7.3.26": _fx_pair({'anuvritti': 'tu', 'operation': 'insertion', 'optional': True, 'range': '7.3', 'semantic': 'pūrvasya', 'source': 'ardhāt', 'stem_class': 'parimāṇasya'}, {'anuvritti': 'tu', 'operation': 'insertion', 'optional': True, 'range': '7.3', 'semantic': 'pūrvasya', 'source': 'ardhāt', 'stem_class': 'other_stem'}),
    "7.3.27": _fx_pair({'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'semantic': 'parasya', 'stem_class': 'ataḥ'}, {'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'semantic': 'parasya', 'stem_class': 'other_stem'}),
    "7.3.28": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'pravāhaṇasya', 'suffix_context': 'ḍhe'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'ḍhe'}),
    "7.3.29": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'tatpratyayasya', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'āt'}),
    "7.3.30": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'nañaḥ', 'stem_class': 'śucīśvarakṣetrajñakuśalanipuṇānām'}, {'operation': 'insertion', 'range': '7.3', 'source': 'nañaḥ', 'stem_class': 'other_stem'}),
    "7.3.31": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'yathātathayathāpurayoḥ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem'}),
    "7.3.32": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'hanaḥ', 'substitute': 'taḥ', 'suffix_context': 'aciṇṇaloḥ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'taḥ', 'suffix_context': 'aciṇṇaloḥ'}),
    "7.3.33": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'ātaḥ', 'substitute': 'yuk', 'suffix_context': 'ciṇkṛtoḥ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'yuk', 'suffix_context': 'ciṇkṛtoḥ'}),
    "7.3.34": _fx_pair({'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'semantic': 'māntasya', 'stem_class': 'udāttopadeśasya'}, {'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'semantic': 'māntasya', 'stem_class': 'other_stem'}),
    "7.3.35": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'janivadhyoḥ', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'āt'}),
    "7.3.36": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'arttihrīvlīrīknūyīkṣmāyyātām', 'substitute': 'puk', 'suffix_context': 'ṇau'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'puk', 'suffix_context': 'ṇau'}),
    "7.3.37": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'śācchāsāhvāvyāvepām', 'substitute': 'yuk'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'yuk'}),
    "7.3.38": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'vaḥ', 'substitute': 'juk', 'suffix_context': 'vidhūnane'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'juk', 'suffix_context': 'vidhūnane'}),
    "7.3.39": _fx_pair({'operation': 'insertion', 'range': '7.3', 'semantic': 'snehavipātane', 'stem_class': 'līloḥ', 'substitute': 'nuglukau', 'suffix_context': 'anyatarasyām'}, {'operation': 'insertion', 'range': '7.3', 'semantic': 'snehavipātane', 'stem_class': 'other_stem', 'substitute': 'nuglukau', 'suffix_context': 'anyatarasyām'}),
    "7.3.40": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'bhiyaḥ', 'substitute': 'ṣuk', 'suffix_context': 'hetubhaye'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'ṣuk', 'suffix_context': 'hetubhaye'}),
    "7.3.41": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'sphāyaḥ', 'substitute': 'vaḥ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'vaḥ'}),
    "7.3.42": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'śadeḥ', 'substitute': 'taḥ', 'suffix_context': 'agatau'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'taḥ', 'suffix_context': 'agatau'}),
    "7.3.43": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'ruhaḥ', 'substitute': 'paḥ', 'suffix_context': 'anyatarasyām'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'paḥ', 'suffix_context': 'anyatarasyām'}),
    "7.3.44": _fx_pair({'operation': 'insertion', 'range': '7.3', 'semantic': 'ataḥ', 'source': 'pratyayasthāt', 'stem_class': 'pūrvasya', 'substitute': 'it', 'suffix_context': 'āpi'}, {'operation': 'insertion', 'range': '7.3', 'semantic': 'ataḥ', 'source': 'pratyayasthāt', 'stem_class': 'other_stem', 'substitute': 'it', 'suffix_context': 'āpi'}),
    "7.3.45": _fx_pair({'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'stem_class': 'yāsayoḥ'}, {'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'stem_class': 'other_stem'}),
    "7.3.46": _fx_pair({'operation': 'insertion', 'range': '7.3', 'semantic': 'ātaḥ', 'stem_class': 'udīcām', 'suffix_context': 'sthāne'}, {'operation': 'insertion', 'range': '7.3', 'semantic': 'ātaḥ', 'stem_class': 'other_stem', 'suffix_context': 'sthāne'}),
    "7.3.47": _fx_pair({'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'stem_class': 'nañpūrvāṇām', 'substitute': 'bhastraiṣāऽjājñādvāsvāḥ'}, {'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'bhastraiṣāऽjājñādvāsvāḥ'}),
    "7.3.48": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'source': 'abhāṣitapuṃskā', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'source': 'abhāṣitapuṃskā', 'substitute': 'other_sub'}),
    "7.3.49": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'ācāryāṇām', 'substitute': 'āt'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'āt'}),
    "7.3.50": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'ṭha', 'substitute': 'ika'}, {'operation': 'insertion', 'range': '7.3', 'source': 'ṭha', 'substitute': 'other_sub'}),
    "7.3.51": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'isusuktāntāt', 'substitute': 'kaḥ'}, {'operation': 'insertion', 'range': '7.3', 'source': 'isusuktāntāt', 'substitute': 'other_sub'}),
    "7.3.52": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'cajoḥ', 'substitute': 'ku', 'suffix_context': 'ghinṇyatoḥ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'ku', 'suffix_context': 'ghinṇyatoḥ'}),
    "7.3.53": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'nyaṅkvādi', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'āt'}),
    "7.3.54": _fx_pair({'operation': 'insertion', 'range': '7.3', 'semantic': 'hanteḥ', 'stem_class': 'haḥ', 'suffix_context': 'ñṇinneṣu'}, {'operation': 'insertion', 'range': '7.3', 'semantic': 'hanteḥ', 'stem_class': 'other_stem', 'suffix_context': 'ñṇinneṣu'}),
    "7.3.55": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'source': 'abhyāsāt', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'source': 'abhyāsāt', 'substitute': 'other_sub'}),
    "7.3.56": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'heḥ', 'suffix_context': 'acaṅi'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'acaṅi'}),
    "7.3.57": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'jeḥ', 'suffix_context': 'sanliṭoḥ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'sanliṭoḥ'}),
    "7.3.58": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'ceḥ', 'substitute': 'vibhāṣā'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'vibhāṣā'}),
    "7.3.59": _fx_pair({'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'stem_class': 'kvādeḥ'}, {'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'stem_class': 'other_stem'}),
    "7.3.60": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'ajivṛjyoḥ', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'āt'}),
    "7.3.61": _fx_pair({'operation': 'insertion', 'range': '7.3', 'substitute': 'bhujanyubjau', 'suffix_context': 'pāṇyupatāpayoḥ'}, {'operation': 'insertion', 'range': '7.3', 'substitute': 'other_sub', 'suffix_context': 'pāṇyupatāpayoḥ'}),
    "7.3.62": _fx_pair({'operation': 'insertion', 'range': '7.3', 'substitute': 'prayājānuyājau', 'suffix_context': 'yajñāṅge'}, {'operation': 'insertion', 'range': '7.3', 'substitute': 'other_sub', 'suffix_context': 'yajñāṅge'}),
    "7.3.63": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'vañceḥ', 'suffix_context': 'gatau'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'gatau'}),
    "7.3.64": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'ucaḥ', 'substitute': 'okaḥ', 'suffix_context': 'ke'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'okaḥ', 'suffix_context': 'ke'}),
    "7.3.65": _fx_pair({'operation': 'insertion', 'range': '7.3', 'semantic': 'āvaśyake', 'suffix_context': 'ṇye'}, {'operation': 'other_op', 'range': '7.3', 'semantic': 'āvaśyake', 'suffix_context': 'ṇye'}),
    "7.3.66": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'yajayācarucapravacarcaḥ', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'āt'}),
    "7.3.67": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'vacaḥ', 'suffix_context': 'aśabdasaṃjñāyām'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'aśabdasaṃjñāyām'}),
    "7.3.68": _fx_pair({'operation': 'insertion', 'range': '7.3', 'substitute': 'prayojyaniyojyau', 'suffix_context': 'śakyārthe'}, {'operation': 'insertion', 'range': '7.3', 'substitute': 'other_sub', 'suffix_context': 'śakyārthe'}),
    "7.3.69": _fx_pair({'operation': 'insertion', 'range': '7.3', 'substitute': 'bhojyam', 'suffix_context': 'bhakṣye'}, {'operation': 'insertion', 'range': '7.3', 'substitute': 'other_sub', 'suffix_context': 'bhakṣye'}),
    "7.3.70": _fx_pair({'operation': 'insertion', 'optional': True, 'range': '7.3', 'stem_class': 'ghoḥ', 'substitute': 'lopaḥ', 'suffix_context': 'leṭi'}, {'operation': 'insertion', 'optional': True, 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'lopaḥ', 'suffix_context': 'leṭi'}),
    "7.3.71": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'otaḥ', 'suffix_context': 'śyani'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'śyani'}),
    "7.3.72": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'ksasya', 'suffix_context': 'aci'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'aci'}),
    "7.3.73": _fx_pair({'operation': 'insertion', 'optional': True, 'range': '7.3', 'semantic': 'dantye', 'stem_class': 'duhadihalihaguhām', 'substitute': 'luk', 'suffix_context': 'ātmanepade'}, {'operation': 'insertion', 'optional': True, 'range': '7.3', 'semantic': 'dantye', 'stem_class': 'other_stem', 'substitute': 'luk', 'suffix_context': 'ātmanepade'}),
    "7.3.74": _fx_pair({'operation': 'insertion', 'range': '7.3', 'semantic': 'aṣṭānām', 'stem_class': 'śamām', 'substitute': 'dīrghaḥ', 'suffix_context': 'śyani'}, {'operation': 'insertion', 'range': '7.3', 'semantic': 'aṣṭānām', 'stem_class': 'other_stem', 'substitute': 'dīrghaḥ', 'suffix_context': 'śyani'}),
    "7.3.75": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'ṣṭhivuklamucamām', 'suffix_context': 'śiti'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'śiti'}),
    "7.3.76": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'kramaḥ', 'suffix_context': 'parasmaipadeṣu'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'parasmaipadeṣu'}),
    "7.3.77": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'iṣugamiyamām', 'substitute': 'chaḥ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'chaḥ'}),
    "7.3.78": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'pāghrādhmāsthāmnādāṇdṛśyarttisarttiśadasadām', 'substitute': 'pibajighradhamatiṣṭhamanayacchapaśyarcchadhauśīyasīdāḥ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'pibajighradhamatiṣṭhamanayacchapaśyarcchadhauśīyasīdāḥ'}),
    "7.3.79": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'jñājanoḥ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem'}),
    "7.3.80": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'pvādi', 'substitute': 'hrasvaḥ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'hrasvaḥ'}),
    "7.3.81": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'mīnāteḥ', 'suffix_context': 'nigame'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'nigame'}),
    "7.3.82": _fx_pair({'operation': 'ṛ-guṇa', 'range': '7.3', 'source': 'mid', 'stem': 'mṛd', 'substitute': 'ar'}, {'operation': 'ṛ-guṇa', 'range': '7.3', 'source': 'mid', 'stem': 'mṛd', 'substitute': 'other_sub'}),
    "7.3.83": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'substitute': 'āt', 'suffix_context': 'jusi'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'substitute': 'other_sub', 'suffix_context': 'jusi'}),
    "7.3.84": _fx_pair({'operation': 'insertion', 'range': '7.3', 'suffix_context': 'sārvadhātukārdhadhātukayoḥ'}, {'operation': 'other_op', 'range': '7.3', 'suffix_context': 'sārvadhātukārdhadhātukayoḥ'}),
    "7.3.85": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'jāgraḥ', 'suffix_context': 'aviciṇṇalṅitsu'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'aviciṇṇalṅitsu'}),
    "7.3.86": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'pugantalaghūpadhasya', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'āt'}),
    "7.3.87": _fx_pair({'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'semantic': 'sārvadhātuke', 'stem_class': 'abhyastasya', 'suffix_context': 'aci'}, {'operation': 'pratisedha', 'pratisedha': 'na', 'range': '7.3', 'semantic': 'sārvadhātuke', 'stem_class': 'other_stem', 'suffix_context': 'aci'}),
    "7.3.88": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'bhūsuvoḥ', 'suffix_context': 'tiṅi'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'tiṅi'}),
    "7.3.89": _fx_pair({'operation': 'insertion', 'range': '7.3', 'semantic': 'hali', 'stem_class': 'utaḥ', 'substitute': 'vṛddhiḥ', 'suffix_context': 'luki'}, {'operation': 'insertion', 'range': '7.3', 'semantic': 'hali', 'stem_class': 'other_stem', 'substitute': 'vṛddhiḥ', 'suffix_context': 'luki'}),
    "7.3.90": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'ūrṇoteḥ', 'substitute': 'vibhāṣā'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'vibhāṣā'}),
    "7.3.91": _fx_pair({'operation': 'guṇa', 'range': '7.3', 'semantic': 'apṛkta'}, {'operation': 'other_op', 'range': '7.3', 'semantic': 'apṛkta'}),
    "7.3.92": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'tṛṇahaḥ', 'substitute': 'im'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'im'}),
    "7.3.93": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'bruvaḥ', 'substitute': 'īṭ'}, {'operation': 'insertion', 'range': '7.3', 'source': 'bruvaḥ', 'substitute': 'other_sub'}),
    "7.3.94": _fx_pair({'operation': 'insertion', 'optional': True, 'range': '7.3', 'source': 'yaṅaḥ'}, {'operation': 'insertion', 'optional': True, 'range': '7.3', 'source': 'other_src'}),
    "7.3.95": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'turustuśamyamaḥ', 'suffix_context': 'sārvadhātuke'}, {'operation': 'insertion', 'range': '7.3', 'source': 'other_src', 'suffix_context': 'sārvadhātuke'}),
    "7.3.96": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'astisicaḥ', 'suffix_context': 'apṛkte'}, {'operation': 'insertion', 'range': '7.3', 'source': 'other_src', 'suffix_context': 'apṛkte'}),
    "7.3.97": _fx_pair({'domain': 'chandas', 'operation': 'bahulam', 'range': '7.3'}, {'domain': 'chandas', 'operation': 'other_op', 'range': '7.3'}),
    "7.3.98": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'source': 'rudaḥ', 'substitute': 'āt'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'source': 'rudaḥ', 'substitute': 'other_sub'}),
    "7.3.99": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'gārgyagālavayoḥ', 'substitute': 'aṭ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'aṭ'}),
    "7.3.100": _fx_pair({'operation': 'insertion', 'range': '7.3', 'scope': 'sarva', 'source': 'ad'}, {'operation': 'insertion', 'range': '7.3', 'scope': 'sarva', 'source': 'other_src'}),
    "7.3.101": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'ataḥ', 'substitute': 'dīrghaḥ', 'suffix_context': 'yañi'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'dīrghaḥ', 'suffix_context': 'yañi'}),
    "7.3.102": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'substitute': 'āt', 'suffix_context': 'supi'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'substitute': 'other_sub', 'suffix_context': 'supi'}),
    "7.3.103": _fx_pair({'operation': 'insertion', 'range': '7.3', 'semantic': 'jhali', 'substitute': 'et', 'suffix_context': 'bahuvacane'}, {'operation': 'insertion', 'range': '7.3', 'semantic': 'jhali', 'substitute': 'other_sub', 'suffix_context': 'bahuvacane'}),
    "7.3.104": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'substitute': 'āt', 'suffix_context': 'osi'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'substitute': 'other_sub', 'suffix_context': 'osi'}),
    "7.3.105": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'āpaḥ', 'substitute': 'āt', 'suffix_context': 'āṅi'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'āt', 'suffix_context': 'āṅi'}),
    "7.3.106": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'substitute': 'āt', 'suffix_context': 'sambuddhau'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'substitute': 'other_sub', 'suffix_context': 'sambuddhau'}),
    "7.3.107": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'ambāऽrthanadyoḥ', 'substitute': 'hrasvaḥ'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'hrasvaḥ'}),
    "7.3.108": _fx_pair({'operation': 'guṇa', 'range': '7.3', 'source': 'hrasva'}, {'operation': 'guṇa', 'range': '7.3', 'source': 'other_src'}),
    "7.3.109": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'substitute': 'āt', 'suffix_context': 'jasi'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'substitute': 'other_sub', 'suffix_context': 'jasi'}),
    "7.3.110": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'ṛt', 'substitute': 'ṅi', 'suffix_context': 'sarvanāmasthāna'}, {'operation': 'insertion', 'range': '7.3', 'source': 'ṛt', 'substitute': 'other_sub', 'suffix_context': 'sarvanāmasthāna'}),
    "7.3.111": _fx_pair({'operation': 'insertion', 'range': '7.3', 'stem_class': 'gheḥ', 'suffix_context': 'ṅiti'}, {'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'suffix_context': 'ṅiti'}),
    "7.3.112": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'nadyāḥ', 'substitute': 'āṭ'}, {'operation': 'insertion', 'range': '7.3', 'source': 'nadyāḥ', 'substitute': 'other_sub'}),
    "7.3.113": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'āpaḥ', 'substitute': 'yāṭ'}, {'operation': 'insertion', 'range': '7.3', 'source': 'āpaḥ', 'substitute': 'other_sub'}),
    "7.3.114": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'source': 'sarvanāmnaḥ', 'substitute': 'syāṭ'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'source': 'sarvanāmnaḥ', 'substitute': 'other_sub'}),
    "7.3.115": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'dvitīyātṛtīyābhyām', 'substitute': 'vibhāṣā'}, {'operation': 'insertion', 'range': '7.3', 'source': 'dvitīyātṛtīyābhyām', 'substitute': 'other_sub'}),
    "7.3.116": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'nadyāmnībhyaḥ', 'stem_class': 'ṅeḥ', 'substitute': 'ām'}, {'operation': 'insertion', 'range': '7.3', 'source': 'nadyāmnībhyaḥ', 'stem_class': 'other_stem', 'substitute': 'ām'}),
    "7.3.117": _fx_pair({'operation': 'insertion', 'range': '7.3', 'source': 'idudbhyām'}, {'operation': 'insertion', 'range': '7.3', 'source': 'other_src'}),
    "7.3.118": _fx_pair({'operation': 'insertion', 'range': '7.3', 'substitute': 'aut'}, {'operation': 'insertion', 'range': '7.3', 'substitute': 'other_sub'}),
    "7.3.119": _fx_pair({'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'gheḥ', 'substitute': 'at'}, {'anuvritti': 'ca', 'operation': 'insertion', 'range': '7.3', 'stem_class': 'other_stem', 'substitute': 'at'}),
    "7.3.120": _fx_pair({'operation': 'insertion', 'range': '7.3', 'semantic': 'astrī', 'source': 'āṅ', 'substitute': 'na'}, {'operation': 'insertion', 'range': '7.3', 'semantic': 'astrī', 'source': 'āṅ', 'substitute': 'other_sub'}),
}

META: dict[str, SutraMeta] = {
    "7.3.1": SutraMeta('vidhi', 'देविकाशिंशपादित्यवाड्दीर्घसत्रश्रेयसामात्\u200c ।', ("domain:adesha", "pada:7.3")),
    "7.3.2": SutraMeta('vidhi', 'केकयमित्त्रयुप्रलयानां यादेरियः ।', ("domain:adesha", "pada:7.3")),
    "7.3.3": SutraMeta('pratisedha', 'न य्वाभ्यां पदान्ताभ्याम् पूर्वौ तु ताभ्यामैच् ।', ("domain:adesha", "pada:7.3")),
    "7.3.4": SutraMeta('vidhi', 'द्वारादीनां च ।', ("domain:adesha", "pada:7.3")),
    "7.3.5": SutraMeta('vidhi', 'न्यग्रोधस्य च केवलस्य ।', ("domain:adesha", "pada:7.3")),
    "7.3.6": SutraMeta('pratisedha', 'न कर्मव्यतिहारे ।', ("domain:adesha", "pada:7.3")),
    "7.3.7": SutraMeta('vidhi', 'स्वागतादीनां च ।', ("domain:adesha", "pada:7.3")),
    "7.3.8": SutraMeta('vidhi', 'श्वादेरिञि ।', ("domain:adesha", "pada:7.3")),
    "7.3.9": SutraMeta('vidhi', 'पदान्तस्यान्यतरस्याम् ।', ("domain:adesha", "pada:7.3")),
    "7.3.10": SutraMeta('samjna', 'उत्तरपदस्य ।', ("domain:adesha", "pada:7.3")),
    "7.3.11": SutraMeta('vidhi', 'अवयवादृतोः ।', ("domain:adesha", "pada:7.3")),
    "7.3.12": SutraMeta('vidhi', 'सुसर्वार्धाज्जनपदस्य ।', ("domain:adesha", "pada:7.3")),
    "7.3.13": SutraMeta('vidhi', 'दिशोऽमद्राणाम् ।', ("domain:adesha", "pada:7.3")),
    "7.3.14": SutraMeta('vidhi', 'प्राचां ग्रामनगराणाम् ।', ("domain:adesha", "pada:7.3")),
    "7.3.15": SutraMeta('vidhi', 'संख्यायाः संवत्सरसंख्यस्य च ।', ("domain:adesha", "pada:7.3")),
    "7.3.16": SutraMeta('vidhi', 'वर्षस्याभविष्यति ।', ("domain:adesha", "pada:7.3")),
    "7.3.17": SutraMeta('vidhi', 'परिमाणान्तस्यासंज्ञाशाणयोः ।', ("domain:adesha", "pada:7.3")),
    "7.3.18": SutraMeta('vidhi', 'जे प्रोष्ठपदानाम् ।', ("domain:adesha", "pada:7.3")),
    "7.3.19": SutraMeta('vidhi', 'हृद्भगसिन्ध्वन्ते पूर्वपदस्य च ।', ("domain:adesha", "pada:7.3")),
    "7.3.20": SutraMeta('vidhi', 'अनुशतिकादीनां च ।', ("domain:adesha", "pada:7.3")),
    "7.3.21": SutraMeta('vidhi', 'देवताद्वंद्वे च ।', ("domain:adesha", "pada:7.3")),
    "7.3.22": SutraMeta('pratisedha', 'नेन्द्रस्य परस्य ।', ("domain:adesha", "pada:7.3")),
    "7.3.23": SutraMeta('vidhi', 'दीर्घाच्च वरुणस्य ।', ("domain:adesha", "pada:7.3")),
    "7.3.24": SutraMeta('vidhi', 'प्राचां नगरान्ते ।', ("domain:adesha", "pada:7.3")),
    "7.3.25": SutraMeta('vidhi', 'जङ्गलधेनुवलजान्तस्य विभाषितमुत्तरम्\u200c ।', ("domain:adesha", "pada:7.3")),
    "7.3.26": SutraMeta('vidhi', 'अर्धात्\u200c परिमाणस्य पूर्वस्य तु वा ।', ("domain:adesha", "pada:7.3")),
    "7.3.27": SutraMeta('pratisedha', 'नातः परस्य ।', ("domain:adesha", "pada:7.3")),
    "7.3.28": SutraMeta('vidhi', 'प्रवाहणस्य ढे ।', ("domain:adesha", "pada:7.3")),
    "7.3.29": SutraMeta('vidhi', 'तत्प्रत्ययस्य च ।', ("domain:adesha", "pada:7.3")),
    "7.3.30": SutraMeta('vidhi', 'नञः शुचीश्वरक्षेत्रज्ञकुशलनिपुणानाम् ।', ("domain:adesha", "pada:7.3")),
    "7.3.31": SutraMeta('vidhi', 'यथातथयथापुरयोः पर्यायेण ।', ("domain:adesha", "pada:7.3")),
    "7.3.32": SutraMeta('vidhi', 'हनस्तोऽचिण्णलोः ।', ("domain:adesha", "pada:7.3")),
    "7.3.33": SutraMeta('vidhi', 'आतो युक् चिण्कृतोः ।', ("domain:adesha", "pada:7.3")),
    "7.3.34": SutraMeta('pratisedha', 'नोदात्तोपदेशस्य मान्तस्यानाचमेः ।', ("domain:adesha", "pada:7.3")),
    "7.3.35": SutraMeta('vidhi', 'जनिवध्योश्च ।', ("domain:adesha", "pada:7.3")),
    "7.3.36": SutraMeta('vidhi', 'अर्त्तिह्रीब्लीरीक्नूयीक्ष्माय्यातां पुङ्णौ ।', ("domain:adesha", "pada:7.3")),
    "7.3.37": SutraMeta('vidhi', 'शाच्छासाह्वाव्यावेपां युक् ।', ("domain:adesha", "pada:7.3")),
    "7.3.38": SutraMeta('vidhi', 'वो विधूनने जुक् ।', ("domain:adesha", "pada:7.3")),
    "7.3.39": SutraMeta('vidhi', 'लीलोर्नुग्लुकावन्यतरस्यां स्नेहविपातने ।', ("domain:adesha", "pada:7.3")),
    "7.3.40": SutraMeta('vidhi', 'भियो हेतुभये षुक् ।', ("domain:adesha", "pada:7.3")),
    "7.3.41": SutraMeta('vidhi', 'स्फायो वः ।', ("domain:adesha", "pada:7.3")),
    "7.3.42": SutraMeta('vidhi', 'शदेरगतौ तः ।', ("domain:adesha", "pada:7.3")),
    "7.3.43": SutraMeta('vidhi', 'रुहः पोऽन्यतरस्याम् ।', ("domain:adesha", "pada:7.3")),
    "7.3.44": SutraMeta('vidhi', 'प्रत्ययस्थात्\u200c कात्\u200c पूर्वस्यात इदाप्यसुपः ।', ("domain:adesha", "pada:7.3")),
    "7.3.45": SutraMeta('pratisedha', 'न यासयोः ।', ("domain:adesha", "pada:7.3")),
    "7.3.46": SutraMeta('vidhi', 'उदीचामातः स्थाने यकपूर्वायाः ।', ("domain:adesha", "pada:7.3")),
    "7.3.47": SutraMeta('vidhi', 'भस्त्रैषाऽजाज्ञाद्वास्वानञ्पूर्वाणामपि ।', ("domain:adesha", "pada:7.3")),
    "7.3.48": SutraMeta('vidhi', 'अभाषितपुंस्काच्च ।', ("domain:adesha", "pada:7.3")),
    "7.3.49": SutraMeta('vidhi', 'आदाचार्याणाम् ।', ("domain:adesha", "pada:7.3")),
    "7.3.50": SutraMeta('vidhi', 'ठस्येकः ।', ("domain:adesha", "pada:7.3")),
    "7.3.51": SutraMeta('vidhi', 'इसुसुक्तान्तात्\u200c कः ।', ("domain:adesha", "pada:7.3")),
    "7.3.52": SutraMeta('vidhi', 'चजोः कु घिन्ण्यतोः ।', ("domain:adesha", "pada:7.3")),
    "7.3.53": SutraMeta('vidhi', 'न्यङ्क्वादीनां च ।', ("domain:adesha", "pada:7.3")),
    "7.3.54": SutraMeta('vidhi', 'हो हन्तेर्ञ्णिन्नेषु ।', ("domain:adesha", "pada:7.3")),
    "7.3.55": SutraMeta('vidhi', 'अभ्यासाच्च ।', ("domain:adesha", "pada:7.3")),
    "7.3.56": SutraMeta('vidhi', 'हेरचङि ।', ("domain:adesha", "pada:7.3")),
    "7.3.57": SutraMeta('vidhi', 'सन्लिटोर्जेः ।', ("domain:adesha", "pada:7.3")),
    "7.3.58": SutraMeta('vibhasha', 'विभाषा चेः ।', ("domain:adesha", "pada:7.3")),
    "7.3.59": SutraMeta('pratisedha', 'न क्वादेः ।', ("domain:adesha", "pada:7.3")),
    "7.3.60": SutraMeta('vidhi', 'अजिवृज्योश्च ।', ("domain:adesha", "pada:7.3")),
    "7.3.61": SutraMeta('vidhi', 'भुजन्युब्जौ पाण्युपतापयोः ।', ("domain:adesha", "pada:7.3")),
    "7.3.62": SutraMeta('vidhi', 'प्रयाजानुयाजौ यज्ञाङ्गे ।', ("domain:adesha", "pada:7.3")),
    "7.3.63": SutraMeta('vidhi', 'वञ्चेर्गतौ ।', ("domain:adesha", "pada:7.3")),
    "7.3.64": SutraMeta('vidhi', 'ओक उचः के ।', ("domain:adesha", "pada:7.3")),
    "7.3.65": SutraMeta('vidhi', 'ण्य आवश्यके ।', ("domain:adesha", "pada:7.3")),
    "7.3.66": SutraMeta('vidhi', 'यजयाचरुचप्रवचर्चश्च ।', ("domain:adesha", "pada:7.3")),
    "7.3.67": SutraMeta('vidhi', 'वचोऽशब्दसंज्ञायाम् ।', ("domain:adesha", "pada:7.3")),
    "7.3.68": SutraMeta('vidhi', 'प्रयोज्यनियोज्यौ शक्यार्थे ।', ("domain:adesha", "pada:7.3")),
    "7.3.69": SutraMeta('vidhi', 'भोज्यं भक्ष्ये ।', ("domain:adesha", "pada:7.3")),
    "7.3.70": SutraMeta('vidhi', 'घोर्लोपो लेटि वा ।', ("domain:adesha", "pada:7.3")),
    "7.3.71": SutraMeta('vidhi', 'ओतः श्यनि ।', ("domain:adesha", "pada:7.3")),
    "7.3.72": SutraMeta('vidhi', 'क्सस्याचि ।', ("domain:adesha", "pada:7.3")),
    "7.3.73": SutraMeta('vidhi', 'लुग्वा दुहदिहलिहगुहामात्मनेपदे दन्त्ये ।', ("domain:adesha", "pada:7.3")),
    "7.3.74": SutraMeta('vidhi', 'शमामष्टानां दीर्घः श्यनि ।', ("domain:adesha", "pada:7.3")),
    "7.3.75": SutraMeta('vidhi', 'ष्ठिवुक्लम्याचमां शिति ।', ("domain:adesha", "pada:7.3")),
    "7.3.76": SutraMeta('vidhi', 'क्रमः परस्मैपदेषु ।', ("domain:adesha", "pada:7.3")),
    "7.3.77": SutraMeta('vidhi', 'इषुगमियमां छः ।', ("domain:adesha", "pada:7.3")),
    "7.3.78": SutraMeta('vidhi', 'पाघ्राध्मास्थाम्नादाण्दृश्यर्त्तिसर्त्तिशदसदां पिबजिघ्रधमतिष्ठमनयच्छपश्यर्च्छधौशीयसीदाः ।', ("domain:adesha", "pada:7.3")),
    "7.3.79": SutraMeta('vidhi', 'ज्ञाजनोर्जा ।', ("domain:adesha", "pada:7.3")),
    "7.3.80": SutraMeta('vidhi', 'प्वादीनां ह्रस्वः ।', ("domain:adesha", "pada:7.3")),
    "7.3.81": SutraMeta('vidhi', 'मीनातेर्निगमे ।', ("domain:adesha", "pada:7.3")),
    "7.3.82": SutraMeta('vidhi', 'मिदेर्गुणः ।', ("domain:adesha", "pada:7.3")),
    "7.3.83": SutraMeta('vidhi', 'जुसि च ।', ("domain:adesha", "pada:7.3")),
    "7.3.84": SutraMeta('vidhi', 'सार्वधातुकार्धधातुकयोः ।', ("domain:adesha", "pada:7.3")),
    "7.3.85": SutraMeta('vidhi', 'जाग्रोऽविचिण्णल्ङित्सु ।', ("domain:adesha", "pada:7.3")),
    "7.3.86": SutraMeta('vidhi', 'पुगन्तलघूपधस्य च ।', ("domain:adesha", "pada:7.3")),
    "7.3.87": SutraMeta('pratisedha', 'नाभ्यस्तस्याचि पिति सार्वधातुके ।', ("domain:adesha", "pada:7.3")),
    "7.3.88": SutraMeta('vidhi', 'भूसुवोस्तिङि ।', ("domain:adesha", "pada:7.3")),
    "7.3.89": SutraMeta('vidhi', 'उतो वृद्धिर्लुकि हलि ।', ("domain:adesha", "pada:7.3")),
    "7.3.90": SutraMeta('vibhasha', 'ऊर्णोतेर्विभाषा ।', ("domain:adesha", "pada:7.3")),
    "7.3.91": SutraMeta('vidhi', 'गुणोऽपृक्ते ।', ("domain:adesha", "pada:7.3")),
    "7.3.92": SutraMeta('vidhi', 'तृणह इम् ।', ("domain:adesha", "pada:7.3")),
    "7.3.93": SutraMeta('vidhi', 'ब्रुव ईट् ।', ("domain:adesha", "pada:7.3")),
    "7.3.94": SutraMeta('vidhi', 'यङो वा ।', ("domain:adesha", "pada:7.3")),
    "7.3.95": SutraMeta('vidhi', 'तुरुस्तुशम्यमः सार्वधातुके ।', ("domain:adesha", "pada:7.3")),
    "7.3.96": SutraMeta('vidhi', 'अस्तिसिचोऽपृक्ते ।', ("domain:adesha", "pada:7.3")),
    "7.3.97": SutraMeta('vidhi', 'बहुलं छन्दसि ।', ("domain:adesha", "pada:7.3")),
    "7.3.98": SutraMeta('vidhi', 'रुदश्च पञ्चभ्यः ।', ("domain:adesha", "pada:7.3")),
    "7.3.99": SutraMeta('vidhi', 'अड्गार्ग्यगालवयोः ।', ("domain:adesha", "pada:7.3")),
    "7.3.100": SutraMeta('vidhi', 'अदः सर्वेषाम् ।', ("domain:adesha", "pada:7.3")),
    "7.3.101": SutraMeta('vidhi', 'अतो दीर्घो यञि ।', ("domain:adesha", "pada:7.3")),
    "7.3.102": SutraMeta('vidhi', 'सुपि च ।', ("domain:adesha", "pada:7.3")),
    "7.3.103": SutraMeta('vidhi', 'बहुवचने झल्येत्\u200c ।', ("domain:adesha", "pada:7.3")),
    "7.3.104": SutraMeta('vidhi', 'ओसि च ।', ("domain:adesha", "pada:7.3")),
    "7.3.105": SutraMeta('vidhi', 'आङि चापः ।', ("domain:adesha", "pada:7.3")),
    "7.3.106": SutraMeta('vidhi', 'सम्बुद्धौ च ।', ("domain:adesha", "pada:7.3")),
    "7.3.107": SutraMeta('vidhi', 'अम्बाऽर्थनद्योर्ह्रस्वः ।', ("domain:adesha", "pada:7.3")),
    "7.3.108": SutraMeta('vidhi', 'ह्रस्वस्य गुणः ।', ("domain:adesha", "pada:7.3")),
    "7.3.109": SutraMeta('vidhi', 'जसि च ।', ("domain:adesha", "pada:7.3")),
    "7.3.110": SutraMeta('vidhi', 'ऋतो ङिसर्वनामस्थानयोः ।', ("domain:adesha", "pada:7.3")),
    "7.3.111": SutraMeta('vidhi', 'घेर्ङिति ।', ("domain:adesha", "pada:7.3")),
    "7.3.112": SutraMeta('vidhi', 'आण्नद्याः ।', ("domain:adesha", "pada:7.3")),
    "7.3.113": SutraMeta('vidhi', 'याडापः ।', ("domain:adesha", "pada:7.3")),
    "7.3.114": SutraMeta('vidhi', 'सर्वनाम्नः स्याड्ढ्रस्वश्च ।', ("domain:adesha", "pada:7.3")),
    "7.3.115": SutraMeta('vibhasha', 'विभाषा द्वितीयातृतीयाभ्याम् ।', ("domain:adesha", "pada:7.3")),
    "7.3.116": SutraMeta('vidhi', 'ङेराम्नद्याम्नीभ्यः ।', ("domain:adesha", "pada:7.3")),
    "7.3.117": SutraMeta('vidhi', 'इदुद्भ्याम् ।', ("domain:adesha", "pada:7.3")),
    "7.3.118": SutraMeta('vidhi', 'औत्\u200c ।', ("domain:adesha", "pada:7.3")),
    "7.3.119": SutraMeta('vidhi', 'अच्च घेः ।', ("domain:adesha", "pada:7.3")),
    "7.3.120": SutraMeta('vidhi', 'आङो नाऽस्त्रियाम् ।', ("domain:adesha", "pada:7.3")),
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
        raise AssertionError("sutra_impl_7_3 self_check failed:\n" + "\n".join(failures))
    return {
        "sutras": len(FIXTURES),
        "predicates": len([n for n in globals() if n.startswith("sutra_7_3_")]),
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
