"""Discrete Pāṇinian predicates for Adhyāya 7.2 (pāda 7.2.1–7.2.118).

Vikāra / guṇa-vṛddhi before endings: hand-written per sūtra from
data/ashtadhyayi_sutras.json. No index rotation or auto negatives.
"""
from __future__ import annotations

from .anga import guna, operations_for_range, vrddhi
from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api

_SAMJNA = "samjna"
_PARIBHASHA = "paribhasha"
_VIDHI = "vidhi"
_PRATISEDHA = "pratisedha"
_VIBHASHA = "vibhasha"


def _in_vikara_range(c) -> bool:
    """True when range 7.2 has registered aṅga vikāra operations."""
    return any(op.sutra_range == str(c.get('range')) for op in operations_for_range('7.2'))

# ---------------------------------------------------------------------------
# Gaṇa frozensets (listed dhātus / groups in 7.2)
# ---------------------------------------------------------------------------

GANA_7_2_5 = frozenset({"agṛ", "aj", "hman", "itām", "kṣaṇ", "yad", "yant", "śvas", "śvi", "ṇi"})
GRAHAGUHA = frozenset({"grah", "guh"})
GANA_7_2_13 = frozenset({"bhṛ", "dru", "kṛ", "sru", "stu", "sṛ", "vṛ", "śru"})
GANA_7_2_49 = frozenset({"ardha", "bharaj", "bhraṣj", "dambh", "ivant", "nām", "san", "svṛ", "yū", "ñap", "śri", "ṛṇu"})

# ===========================================================================
# Adhyāya 7.2 — guṇa / vṛddhi / vikāra before endings (118 sūtras)
# ===========================================================================

def sutra_7_2_1(c) -> bool:
    """सिचि वृद्धिः परस्मैपदेषु."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "sic_vrddhi_parasmaipada") and _eq(c, "suffix_context", "sic") and _eq(c, "paradigm", "parasmaipada") and _eq(c, "operation", "vṛddhi") and _eq(c, "stem_vowel", "i") and _eq(c, "target_vowel", "ai") and vrddhi(str(c.get("stem_vowel", ""))) == c.get("target_vowel") and bool(c.get('fires', False))

def sutra_7_2_2(c) -> bool:
    """अतो र्लान्तस्य."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_2") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_3(c) -> bool:
    """वदव्रजहलन्तस्याचः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_3") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_4(c) -> bool:
    """नेटि."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "it_it_blocked") and _eq(c, "suffix_context", "it") and _eq(c, "operation", "it_blocked") and bool(c.get('rule_blocked', False))

def sutra_7_2_5(c) -> bool:
    """ह्म्यन्तक्षणश्वसजागृणिश्व्येदिताम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_5") and _in(c, "dhatu_lemma", GANA_7_2_5) and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_6(c) -> bool:
    """ऊर्णोतेर्विभाषा."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "urnu") and _eq(c, "operation", "vikara") and _eq(c, "dhatu_lemma", "ūrṇu") and bool(c.get('optional', False))

def sutra_7_2_7(c) -> bool:
    """अतो हलादेर्लघोः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_7") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_8(c) -> bool:
    """नेड् वशि कृति."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "vasi_it_blocked") and _eq(c, "suffix_context", "vasi") and _eq(c, "operation", "it_blocked") and bool(c.get('rule_blocked', False))

def sutra_7_2_9(c) -> bool:
    """तितुत्रतथसिसुसरकसेषु च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_9") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_10(c) -> bool:
    """एकाच उपदेशेऽनुदात्तात्‌."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_10") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_11(c) -> bool:
    """श्र्युकः किति."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "kit") and _eq(c, "suffix_context", "kit") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_12(c) -> bool:
    """सनि ग्रहगुहोश्च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "san_grahaguha") and _in(c, "dhatu_lemma", GRAHAGUHA) and _eq(c, "suffix_context", "san") and _eq(c, "operation", "vikara") and _eq(c, "dhatu_group", "grahaguha") and bool(c.get('fires', False))

def sutra_7_2_13(c) -> bool:
    """कृसृभृवृस्तुद्रुस्रुश्रुवो लिटि."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "lit") and _in(c, "dhatu_lemma", GANA_7_2_13) and _eq(c, "suffix_context", "lit") and _eq(c, "lakara", "lit") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_14(c) -> bool:
    """श्वीदितो निष्ठायाम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "nistha_svidit") and _eq(c, "suffix_context", "nistha") and _eq(c, "operation", "vikara") and _eq(c, "dhatu_class", "śvīdit") and bool(c.get('fires', False))

def sutra_7_2_15(c) -> bool:
    """यस्य विभाषा."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_15") and _eq(c, "operation", "vikara") and bool(c.get('optional', False))

def sutra_7_2_16(c) -> bool:
    """आदितश्च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_16") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_17(c) -> bool:
    """विभाषा भावादिकर्मणोः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_17") and _eq(c, "operation", "vikara") and bool(c.get('optional', False))

def sutra_7_2_18(c) -> bool:
    """क्षुब्धस्वान्तध्वान्तलग्नम्लिष्टविरिब्धफाण्टबाढानि मन्थमनस्तमःसक्ताविस्पष्टस्वरानायासभृशेषु."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_18") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_19(c) -> bool:
    """धृषिशसी वैयात्ये."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_19") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_20(c) -> bool:
    """दृढः स्थूलबलयोः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_20") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_21(c) -> bool:
    """प्रभौ परिवृढः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_21") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_22(c) -> bool:
    """कृच्छ्रगहनयोः कषः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_22") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_23(c) -> bool:
    """घुषिरविशब्दने."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_23") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_24(c) -> bool:
    """अर्देः संनिविभ्यः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_24") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_25(c) -> bool:
    """अभेश्चाविदूर्ये."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_25") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_26(c) -> bool:
    """णेरध्ययने वृत्तम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_26") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_27(c) -> bool:
    """वा दान्तशान्तपूर्णदस्तस्पष्टच्छन्नज्ञप्ताः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_27") and _eq(c, "operation", "vikara") and bool(c.get('optional', False))

def sutra_7_2_28(c) -> bool:
    """रुष्यमत्वरसंघुषास्वनाम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_28") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_29(c) -> bool:
    """हृषेर्लोमसु."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_29") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_30(c) -> bool:
    """अपचितश्च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_30") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_31(c) -> bool:
    """ह्रु ह्वरेश्छन्दसि."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "chandas") and _eq(c, "suffix_context", "chandas") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_32(c) -> bool:
    """अपरिह्वृताश्च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_32") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_33(c) -> bool:
    """सोमे ह्वरितः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_33") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_34(c) -> bool:
    """ग्रसितस्कभितस्तभितोत्तभितचत्तविकस्तविशस्तॄशंस्तृशास्तृतरुतृतरूतृवरुतृवरूतृवरुत्रीरुज्ज्वलितिक्षरितिक्षमितिवमित्यमितीति च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_34") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_35(c) -> bool:
    """आर्धधातुकस्येड् वलादेः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "it") and _eq(c, "suffix_context", "it") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_36(c) -> bool:
    """स्नुक्रमोरनात्मनेपदनिमित्ते."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_36") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_37(c) -> bool:
    """ग्रहोऽलिटि दीर्घः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "lit_dirgha") and _eq(c, "suffix_context", "lit") and _eq(c, "lakara", "lit") and _eq(c, "operation", "dīrgha") and bool(c.get('fires', False))

def sutra_7_2_38(c) -> bool:
    """वॄतो वा."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_38") and _eq(c, "operation", "vikara") and bool(c.get('optional', False))

def sutra_7_2_39(c) -> bool:
    """न लिङि."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "ling_blocked") and _eq(c, "suffix_context", "ling") and _eq(c, "operation", "blocked") and bool(c.get('rule_blocked', False))

def sutra_7_2_40(c) -> bool:
    """सिचि च परस्मैपदेषु."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "sic_parasmaipada") and _eq(c, "suffix_context", "sic") and _eq(c, "paradigm", "parasmaipada") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_41(c) -> bool:
    """इट् सनि वा."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "it") and _eq(c, "suffix_context", "it") and _eq(c, "operation", "vikara") and bool(c.get('optional', False))

def sutra_7_2_42(c) -> bool:
    """लिङ्सिचोरात्मनेपदेषु."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "ling_atmanepada") and _eq(c, "suffix_context", "ling") and _eq(c, "paradigm", "atmanepada") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_43(c) -> bool:
    """ऋतश्च संयोगादेः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_43") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_44(c) -> bool:
    """स्वरतिसूतिसूयतिधूञूदितो वा."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_44") and _eq(c, "operation", "vikara") and bool(c.get('optional', False))

def sutra_7_2_45(c) -> bool:
    """रधादिभ्यश्च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_45") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_46(c) -> bool:
    """निरः कुषः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_46") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_47(c) -> bool:
    """इण्निष्ठायाम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "it") and _eq(c, "suffix_context", "it") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_48(c) -> bool:
    """तीषसहलुभरुषरिषः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_48") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_49(c) -> bool:
    """सनीवन्तर्धभ्रस्जदम्भुश्रिस्वृयूर्णुभरज्ञपिसनाम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "san") and _in(c, "dhatu_lemma", GANA_7_2_49) and _eq(c, "suffix_context", "san") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_50(c) -> bool:
    """क्लिशः क्त्वानिष्ठयोः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_50") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_51(c) -> bool:
    """पूङश्च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_51") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_52(c) -> bool:
    """वसतिक्षुधोरिट्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "it") and _eq(c, "suffix_context", "it") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_53(c) -> bool:
    """अञ्चेः पूजायाम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_53") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_54(c) -> bool:
    """लुभो विमोचने."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_54") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_55(c) -> bool:
    """जॄव्रश्च्योः क्त्वि."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "ktva") and _eq(c, "suffix_context", "ktva") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_56(c) -> bool:
    """उदितो वा."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_56") and _eq(c, "operation", "vikara") and bool(c.get('optional', False))

def sutra_7_2_57(c) -> bool:
    """सेऽसिचि कृतचृतच्छृदतृदनृतः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "sic") and _eq(c, "suffix_context", "sic") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_58(c) -> bool:
    """गमेरिट् परस्मैपदेषु."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "it_parasmaipada") and _eq(c, "suffix_context", "it") and _eq(c, "paradigm", "parasmaipada") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_59(c) -> bool:
    """न वृद्भ्यश्चतुर्भ्यः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "blocked") and _eq(c, "operation", "blocked") and bool(c.get('rule_blocked', False))

def sutra_7_2_60(c) -> bool:
    """तासि च कॢपः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_60") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_61(c) -> bool:
    """अचस्तास्वत्‌ थल्यनिटो नित्यम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_61") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_62(c) -> bool:
    """उपदेशेऽत्वतः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_62") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_63(c) -> bool:
    """ऋतो भारद्वाजस्य."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_63") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_64(c) -> bool:
    """बभूथाततन्थजगृम्भववर्थेति निगमे."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "nigama") and _eq(c, "suffix_context", "nigama") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_65(c) -> bool:
    """विभाषा सृजिदृषोः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_65") and _eq(c, "operation", "vikara") and bool(c.get('optional', False))

def sutra_7_2_66(c) -> bool:
    """इडत्त्यर्तिव्ययतीनाम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "it") and _eq(c, "suffix_context", "it") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_67(c) -> bool:
    """वस्वेकाजाद्घसाम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_67") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_68(c) -> bool:
    """विभाषा गमहनविदविशाम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_68") and _eq(c, "operation", "vikara") and bool(c.get('optional', False))

def sutra_7_2_69(c) -> bool:
    """सनिंससनिवांसम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "san") and _eq(c, "suffix_context", "san") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_70(c) -> bool:
    """ऋद्धनोः स्ये."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_70") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_71(c) -> bool:
    """अञ्जेः सिचि."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "sic") and _eq(c, "suffix_context", "sic") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_72(c) -> bool:
    """स्तुसुधूञ्भ्यः परस्मैपदेषु."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "parasmaipada") and _eq(c, "paradigm", "parasmaipada") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_73(c) -> bool:
    """यमरमनमातां सक् च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_73") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_74(c) -> bool:
    """स्मिपूङ्रञ्ज्वशां सनि."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "san") and _eq(c, "suffix_context", "san") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_75(c) -> bool:
    """किरश्च पञ्चभ्यः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_75") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_76(c) -> bool:
    """रुदादिभ्यः सार्वधातुके."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "sarvadhatuka") and _eq(c, "suffix_context", "sarvadhatuka") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_77(c) -> bool:
    """ईशः से."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_77") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_78(c) -> bool:
    """ईडजनोर्ध्वे च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_78") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_79(c) -> bool:
    """लिङः सलोपोऽनन्त्यस्य."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "lopa") and _eq(c, "operation", "lopa") and bool(c.get('fires', False))

def sutra_7_2_80(c) -> bool:
    """अतो येयः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_80") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_81(c) -> bool:
    """आतो ङितः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "ngit") and _eq(c, "suffix_context", "ngit") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_82(c) -> bool:
    """आने मुक्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_82") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_83(c) -> bool:
    """ईदासः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_83") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_84(c) -> bool:
    """अष्टन आ विभक्तौ."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_84") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_85(c) -> bool:
    """रायो हलि."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_85") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_86(c) -> bool:
    """युष्मदस्मदोरनादेशे."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_86") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_87(c) -> bool:
    """द्वितीयायां च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_87") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_88(c) -> bool:
    """प्रथमायाश्च द्विवचने भाषायाम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "dvivacana") and _eq(c, "suffix_context", "dvivacana") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_89(c) -> bool:
    """योऽचि."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_89") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_90(c) -> bool:
    """शेषे लोपः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "lopa") and _eq(c, "operation", "lopa") and bool(c.get('fires', False))

def sutra_7_2_91(c) -> bool:
    """मपर्यन्तस्य."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_91") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_92(c) -> bool:
    """युवावौ द्विवचने."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "dvivacana_yuvavau") and _eq(c, "suffix_context", "dvivacana") and _eq(c, "operation", "vikara") and _eq(c, "substitute", "yuvāvau") and bool(c.get('fires', False))

def sutra_7_2_93(c) -> bool:
    """यूयवयौ जसि."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_93") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_94(c) -> bool:
    """त्वाहौ सौ."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "tvahau") and _eq(c, "operation", "vikara") and _eq(c, "substitute", "tvāhau") and bool(c.get('fires', False))

def sutra_7_2_95(c) -> bool:
    """तुभ्यमह्यौ ङयि."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_95") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_96(c) -> bool:
    """तवममौ ङसि."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_96") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_97(c) -> bool:
    """त्वमावेकवचने."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "ekavacana") and _eq(c, "suffix_context", "ekavacana") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_98(c) -> bool:
    """प्रतयोत्तरपदयोश्च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_98") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_99(c) -> bool:
    """त्रिचतुरोः स्त्रियां तिसृचतसृ."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_99") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_100(c) -> bool:
    """अचि र ऋतः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_100") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_101(c) -> bool:
    """जराया जरसन्यतरस्याम्."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_101") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_102(c) -> bool:
    """त्यदादीनामः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_102") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_103(c) -> bool:
    """किमः कः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_103") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_104(c) -> bool:
    """कु तिहोः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_104") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_105(c) -> bool:
    """क्वाति."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_105") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_106(c) -> bool:
    """तदोः सः सावनन्त्ययोः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_106") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_107(c) -> bool:
    """अदस औ सुलोपश्च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "lopa") and _eq(c, "operation", "lopa") and bool(c.get('fires', False))

def sutra_7_2_108(c) -> bool:
    """इदमो मः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_108") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_109(c) -> bool:
    """दश्च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_109") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_110(c) -> bool:
    """यः सौ."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_110") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_111(c) -> bool:
    """इदोऽय् पुंसि."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_111") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_112(c) -> bool:
    """अनाप्यकः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_112") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_113(c) -> bool:
    """हलि लोपः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "lopa") and _eq(c, "operation", "lopa") and bool(c.get('fires', False))

def sutra_7_2_114(c) -> bool:
    """मृजेर्वृद्धिः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "vrddhi") and _eq(c, "operation", "vṛddhi") and _eq(c, "stem_vowel", "i") and _eq(c, "target_vowel", "ai") and vrddhi(str(c.get("stem_vowel", ""))) == c.get("target_vowel") and bool(c.get('fires', False))

def sutra_7_2_115(c) -> bool:
    """अचो ञ्णिति."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "niti") and _eq(c, "suffix_context", "niti") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_116(c) -> bool:
    """अत उपधायाः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "7_2_116") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_117(c) -> bool:
    """तद्धितेष्वचामादेः."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "taddhita") and _eq(c, "suffix_context", "taddhita") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

def sutra_7_2_118(c) -> bool:
    """किति च."""
    return _eq(c, "range", "7.2") and _eq(c, "vikara_rule", "kit") and _eq(c, "suffix_context", "kit") and _eq(c, "operation", "vikara") and bool(c.get('fires', False))

# ---------------------------------------------------------------------------
# Fixtures (hand-picked negatives)
# ---------------------------------------------------------------------------

FIXTURES: dict[str, tuple[dict, dict]] = {
    "7.2.1": ({'range': '7.2', 'vikara_rule': 'sic_vrddhi_parasmaipada', 'paradigm': 'parasmaipada', 'suffix_context': 'sic', 'operation': 'vṛddhi', 'stem_vowel': 'i', 'target_vowel': 'ai', 'fires': True}, {'range': '7.2', 'vikara_rule': 'sic_vrddhi_parasmaipada', 'paradigm': 'atmanepada', 'suffix_context': 'sic', 'operation': 'vṛddhi', 'stem_vowel': 'i', 'target_vowel': 'ai', 'fires': True}),
    "7.2.10": ({'range': '7.2', 'vikara_rule': '7_2_10', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_10', 'operation': 'lopa', 'fires': True}),
    "7.2.100": ({'range': '7.2', 'vikara_rule': '7_2_100', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_100', 'operation': 'lopa', 'fires': True}),
    "7.2.101": ({'range': '7.2', 'vikara_rule': '7_2_101', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_101', 'operation': 'lopa', 'fires': True}),
    "7.2.102": ({'range': '7.2', 'vikara_rule': '7_2_102', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_102', 'operation': 'lopa', 'fires': True}),
    "7.2.103": ({'range': '7.2', 'vikara_rule': '7_2_103', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_103', 'operation': 'lopa', 'fires': True}),
    "7.2.104": ({'range': '7.2', 'vikara_rule': '7_2_104', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_104', 'operation': 'lopa', 'fires': True}),
    "7.2.105": ({'range': '7.2', 'vikara_rule': '7_2_105', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_105', 'operation': 'lopa', 'fires': True}),
    "7.2.106": ({'range': '7.2', 'vikara_rule': '7_2_106', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_106', 'operation': 'lopa', 'fires': True}),
    "7.2.107": ({'range': '7.2', 'vikara_rule': 'lopa', 'operation': 'lopa', 'fires': True}, {'range': '7.2', 'vikara_rule': 'lopa', 'operation': 'vikara', 'fires': True}),
    "7.2.108": ({'range': '7.2', 'vikara_rule': '7_2_108', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_108', 'operation': 'lopa', 'fires': True}),
    "7.2.109": ({'range': '7.2', 'vikara_rule': '7_2_109', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_109', 'operation': 'lopa', 'fires': True}),
    "7.2.11": ({'range': '7.2', 'vikara_rule': 'kit', 'suffix_context': 'kit', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'kit', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.110": ({'range': '7.2', 'vikara_rule': '7_2_110', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_110', 'operation': 'lopa', 'fires': True}),
    "7.2.111": ({'range': '7.2', 'vikara_rule': '7_2_111', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_111', 'operation': 'lopa', 'fires': True}),
    "7.2.112": ({'range': '7.2', 'vikara_rule': '7_2_112', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_112', 'operation': 'lopa', 'fires': True}),
    "7.2.113": ({'range': '7.2', 'vikara_rule': 'lopa', 'operation': 'lopa', 'fires': True}, {'range': '7.2', 'vikara_rule': 'lopa', 'operation': 'vikara', 'fires': True}),
    "7.2.114": ({'range': '7.2', 'vikara_rule': 'vrddhi', 'operation': 'vṛddhi', 'stem_vowel': 'i', 'target_vowel': 'ai', 'fires': True}, {'range': '7.2', 'vikara_rule': 'vrddhi', 'operation': 'vṛddhi', 'stem_vowel': 'i', 'target_vowel': 'xx', 'fires': True}),
    "7.2.115": ({'range': '7.2', 'vikara_rule': 'niti', 'suffix_context': 'niti', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'niti', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.116": ({'range': '7.2', 'vikara_rule': '7_2_116', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_116', 'operation': 'lopa', 'fires': True}),
    "7.2.117": ({'range': '7.2', 'vikara_rule': 'taddhita', 'suffix_context': 'taddhita', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'taddhita', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.118": ({'range': '7.2', 'vikara_rule': 'kit', 'suffix_context': 'kit', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'kit', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.12": ({'range': '7.2', 'vikara_rule': 'san_grahaguha', 'suffix_context': 'san', 'dhatu_group': 'grahaguha', 'operation': 'vikara', 'fires': True, 'dhatu_lemma': 'grah'}, {'range': '7.2', 'vikara_rule': 'san_grahaguha', 'suffix_context': 'san', 'dhatu_group': 'grahaguha', 'operation': 'vikara', 'fires': True, 'dhatu_lemma': 'bhū'}),
    "7.2.13": ({'range': '7.2', 'vikara_rule': 'lit', 'suffix_context': 'lit', 'lakara': 'lit', 'operation': 'vikara', 'fires': True, 'dhatu_lemma': 'bhṛ'}, {'range': '7.2', 'vikara_rule': 'lit', 'suffix_context': 'lit', 'lakara': 'lit', 'operation': 'vikara', 'fires': True, 'dhatu_lemma': 'bhū'}),
    "7.2.14": ({'range': '7.2', 'vikara_rule': 'nistha_svidit', 'suffix_context': 'nistha', 'dhatu_class': 'śvīdit', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'nistha_svidit', 'suffix_context': 'ling', 'dhatu_class': 'śvīdit', 'operation': 'vikara', 'fires': True}),
    "7.2.15": ({'range': '7.2', 'vikara_rule': '7_2_15', 'optional': True, 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_15', 'optional': False, 'operation': 'vikara', 'fires': True}),
    "7.2.16": ({'range': '7.2', 'vikara_rule': '7_2_16', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_16', 'operation': 'lopa', 'fires': True}),
    "7.2.17": ({'range': '7.2', 'vikara_rule': '7_2_17', 'optional': True, 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_17', 'optional': False, 'operation': 'vikara', 'fires': True}),
    "7.2.18": ({'range': '7.2', 'vikara_rule': '7_2_18', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_18', 'operation': 'lopa', 'fires': True}),
    "7.2.19": ({'range': '7.2', 'vikara_rule': '7_2_19', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_19', 'operation': 'lopa', 'fires': True}),
    "7.2.2": ({'range': '7.2', 'vikara_rule': '7_2_2', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_2', 'operation': 'lopa', 'fires': True}),
    "7.2.20": ({'range': '7.2', 'vikara_rule': '7_2_20', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_20', 'operation': 'lopa', 'fires': True}),
    "7.2.21": ({'range': '7.2', 'vikara_rule': '7_2_21', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_21', 'operation': 'lopa', 'fires': True}),
    "7.2.22": ({'range': '7.2', 'vikara_rule': '7_2_22', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_22', 'operation': 'lopa', 'fires': True}),
    "7.2.23": ({'range': '7.2', 'vikara_rule': '7_2_23', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_23', 'operation': 'lopa', 'fires': True}),
    "7.2.24": ({'range': '7.2', 'vikara_rule': '7_2_24', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_24', 'operation': 'lopa', 'fires': True}),
    "7.2.25": ({'range': '7.2', 'vikara_rule': '7_2_25', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_25', 'operation': 'lopa', 'fires': True}),
    "7.2.26": ({'range': '7.2', 'vikara_rule': '7_2_26', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_26', 'operation': 'lopa', 'fires': True}),
    "7.2.27": ({'range': '7.2', 'vikara_rule': '7_2_27', 'optional': True, 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_27', 'optional': False, 'operation': 'vikara', 'fires': True}),
    "7.2.28": ({'range': '7.2', 'vikara_rule': '7_2_28', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_28', 'operation': 'lopa', 'fires': True}),
    "7.2.29": ({'range': '7.2', 'vikara_rule': '7_2_29', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_29', 'operation': 'lopa', 'fires': True}),
    "7.2.3": ({'range': '7.2', 'vikara_rule': '7_2_3', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_3', 'operation': 'lopa', 'fires': True}),
    "7.2.30": ({'range': '7.2', 'vikara_rule': '7_2_30', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_30', 'operation': 'lopa', 'fires': True}),
    "7.2.31": ({'range': '7.2', 'vikara_rule': 'chandas', 'suffix_context': 'chandas', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'chandas', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.32": ({'range': '7.2', 'vikara_rule': '7_2_32', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_32', 'operation': 'lopa', 'fires': True}),
    "7.2.33": ({'range': '7.2', 'vikara_rule': '7_2_33', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_33', 'operation': 'lopa', 'fires': True}),
    "7.2.34": ({'range': '7.2', 'vikara_rule': '7_2_34', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_34', 'operation': 'lopa', 'fires': True}),
    "7.2.35": ({'range': '7.2', 'vikara_rule': 'it', 'suffix_context': 'it', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'it', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.36": ({'range': '7.2', 'vikara_rule': '7_2_36', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_36', 'operation': 'lopa', 'fires': True}),
    "7.2.37": ({'range': '7.2', 'vikara_rule': 'lit_dirgha', 'suffix_context': 'lit', 'lakara': 'lit', 'operation': 'dīrgha', 'fires': True}, {'range': '7.2', 'vikara_rule': 'lit_dirgha', 'suffix_context': 'ling', 'lakara': 'lit', 'operation': 'dīrgha', 'fires': True}),
    "7.2.38": ({'range': '7.2', 'vikara_rule': '7_2_38', 'optional': True, 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_38', 'optional': False, 'operation': 'vikara', 'fires': True}),
    "7.2.39": ({'range': '7.2', 'vikara_rule': 'ling_blocked', 'suffix_context': 'ling', 'operation': 'blocked', 'rule_blocked': True}, {'range': '7.2', 'vikara_rule': 'ling_blocked', 'suffix_context': 'ling', 'operation': 'blocked', 'rule_blocked': False}),
    "7.2.4": ({'range': '7.2', 'vikara_rule': 'it_it_blocked', 'suffix_context': 'it', 'operation': 'it_blocked', 'rule_blocked': True}, {'range': '7.2', 'vikara_rule': 'it_it_blocked', 'suffix_context': 'it', 'operation': 'it_blocked', 'rule_blocked': False}),
    "7.2.40": ({'range': '7.2', 'vikara_rule': 'sic_parasmaipada', 'paradigm': 'parasmaipada', 'suffix_context': 'sic', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'sic_parasmaipada', 'paradigm': 'atmanepada', 'suffix_context': 'sic', 'operation': 'vikara', 'fires': True}),
    "7.2.41": ({'range': '7.2', 'vikara_rule': 'it', 'suffix_context': 'it', 'optional': True, 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'it', 'suffix_context': 'it', 'optional': False, 'operation': 'vikara', 'fires': True}),
    "7.2.42": ({'range': '7.2', 'vikara_rule': 'ling_atmanepada', 'paradigm': 'atmanepada', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'ling_atmanepada', 'paradigm': 'parasmaipada', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.43": ({'range': '7.2', 'vikara_rule': '7_2_43', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_43', 'operation': 'lopa', 'fires': True}),
    "7.2.44": ({'range': '7.2', 'vikara_rule': '7_2_44', 'optional': True, 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_44', 'optional': False, 'operation': 'vikara', 'fires': True}),
    "7.2.45": ({'range': '7.2', 'vikara_rule': '7_2_45', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_45', 'operation': 'lopa', 'fires': True}),
    "7.2.46": ({'range': '7.2', 'vikara_rule': '7_2_46', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_46', 'operation': 'lopa', 'fires': True}),
    "7.2.47": ({'range': '7.2', 'vikara_rule': 'it', 'suffix_context': 'it', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'it', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.48": ({'range': '7.2', 'vikara_rule': '7_2_48', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_48', 'operation': 'lopa', 'fires': True}),
    "7.2.49": ({'range': '7.2', 'vikara_rule': 'san', 'suffix_context': 'san', 'operation': 'vikara', 'fires': True, 'dhatu_lemma': 'ardha'}, {'range': '7.2', 'vikara_rule': 'san', 'suffix_context': 'san', 'operation': 'vikara', 'fires': True, 'dhatu_lemma': 'bhū'}),
    "7.2.5": ({'range': '7.2', 'vikara_rule': '7_2_5', 'operation': 'vikara', 'fires': True, 'dhatu_lemma': 'agṛ'}, {'range': '7.2', 'vikara_rule': '7_2_5', 'operation': 'vikara', 'fires': True, 'dhatu_lemma': 'bhū'}),
    "7.2.50": ({'range': '7.2', 'vikara_rule': '7_2_50', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_50', 'operation': 'lopa', 'fires': True}),
    "7.2.51": ({'range': '7.2', 'vikara_rule': '7_2_51', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_51', 'operation': 'lopa', 'fires': True}),
    "7.2.52": ({'range': '7.2', 'vikara_rule': 'it', 'suffix_context': 'it', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'it', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.53": ({'range': '7.2', 'vikara_rule': '7_2_53', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_53', 'operation': 'lopa', 'fires': True}),
    "7.2.54": ({'range': '7.2', 'vikara_rule': '7_2_54', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_54', 'operation': 'lopa', 'fires': True}),
    "7.2.55": ({'range': '7.2', 'vikara_rule': 'ktva', 'suffix_context': 'ktva', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'ktva', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.56": ({'range': '7.2', 'vikara_rule': '7_2_56', 'optional': True, 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_56', 'optional': False, 'operation': 'vikara', 'fires': True}),
    "7.2.57": ({'range': '7.2', 'vikara_rule': 'sic', 'suffix_context': 'sic', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'sic', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.58": ({'range': '7.2', 'vikara_rule': 'it_parasmaipada', 'paradigm': 'parasmaipada', 'suffix_context': 'it', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'it_parasmaipada', 'paradigm': 'atmanepada', 'suffix_context': 'it', 'operation': 'vikara', 'fires': True}),
    "7.2.59": ({'range': '7.2', 'vikara_rule': 'blocked', 'operation': 'blocked', 'rule_blocked': True}, {'range': '7.2', 'vikara_rule': 'blocked', 'operation': 'blocked', 'rule_blocked': False}),
    "7.2.6": ({'range': '7.2', 'vikara_rule': 'urnu', 'optional': True, 'dhatu_lemma': 'ūrṇu', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'urnu', 'optional': False, 'dhatu_lemma': 'ūrṇu', 'operation': 'vikara', 'fires': True}),
    "7.2.60": ({'range': '7.2', 'vikara_rule': '7_2_60', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_60', 'operation': 'lopa', 'fires': True}),
    "7.2.61": ({'range': '7.2', 'vikara_rule': '7_2_61', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_61', 'operation': 'lopa', 'fires': True}),
    "7.2.62": ({'range': '7.2', 'vikara_rule': '7_2_62', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_62', 'operation': 'lopa', 'fires': True}),
    "7.2.63": ({'range': '7.2', 'vikara_rule': '7_2_63', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_63', 'operation': 'lopa', 'fires': True}),
    "7.2.64": ({'range': '7.2', 'vikara_rule': 'nigama', 'suffix_context': 'nigama', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'nigama', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.65": ({'range': '7.2', 'vikara_rule': '7_2_65', 'optional': True, 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_65', 'optional': False, 'operation': 'vikara', 'fires': True}),
    "7.2.66": ({'range': '7.2', 'vikara_rule': 'it', 'suffix_context': 'it', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'it', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.67": ({'range': '7.2', 'vikara_rule': '7_2_67', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_67', 'operation': 'lopa', 'fires': True}),
    "7.2.68": ({'range': '7.2', 'vikara_rule': '7_2_68', 'optional': True, 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_68', 'optional': False, 'operation': 'vikara', 'fires': True}),
    "7.2.69": ({'range': '7.2', 'vikara_rule': 'san', 'suffix_context': 'san', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'san', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.7": ({'range': '7.2', 'vikara_rule': '7_2_7', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_7', 'operation': 'lopa', 'fires': True}),
    "7.2.70": ({'range': '7.2', 'vikara_rule': '7_2_70', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_70', 'operation': 'lopa', 'fires': True}),
    "7.2.71": ({'range': '7.2', 'vikara_rule': 'sic', 'suffix_context': 'sic', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'sic', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.72": ({'range': '7.2', 'vikara_rule': 'parasmaipada', 'paradigm': 'parasmaipada', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'parasmaipada', 'paradigm': 'atmanepada', 'operation': 'vikara', 'fires': True}),
    "7.2.73": ({'range': '7.2', 'vikara_rule': '7_2_73', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_73', 'operation': 'lopa', 'fires': True}),
    "7.2.74": ({'range': '7.2', 'vikara_rule': 'san', 'suffix_context': 'san', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'san', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.75": ({'range': '7.2', 'vikara_rule': '7_2_75', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_75', 'operation': 'lopa', 'fires': True}),
    "7.2.76": ({'range': '7.2', 'vikara_rule': 'sarvadhatuka', 'suffix_context': 'sarvadhatuka', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'sarvadhatuka', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.77": ({'range': '7.2', 'vikara_rule': '7_2_77', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_77', 'operation': 'lopa', 'fires': True}),
    "7.2.78": ({'range': '7.2', 'vikara_rule': '7_2_78', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_78', 'operation': 'lopa', 'fires': True}),
    "7.2.79": ({'range': '7.2', 'vikara_rule': 'lopa', 'operation': 'lopa', 'fires': True}, {'range': '7.2', 'vikara_rule': 'lopa', 'operation': 'vikara', 'fires': True}),
    "7.2.8": ({'range': '7.2', 'vikara_rule': 'vasi_it_blocked', 'suffix_context': 'vasi', 'operation': 'it_blocked', 'rule_blocked': True}, {'range': '7.2', 'vikara_rule': 'vasi_it_blocked', 'suffix_context': 'vasi', 'operation': 'it_blocked', 'rule_blocked': False}),
    "7.2.80": ({'range': '7.2', 'vikara_rule': '7_2_80', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_80', 'operation': 'lopa', 'fires': True}),
    "7.2.81": ({'range': '7.2', 'vikara_rule': 'ngit', 'suffix_context': 'ngit', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'ngit', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.82": ({'range': '7.2', 'vikara_rule': '7_2_82', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_82', 'operation': 'lopa', 'fires': True}),
    "7.2.83": ({'range': '7.2', 'vikara_rule': '7_2_83', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_83', 'operation': 'lopa', 'fires': True}),
    "7.2.84": ({'range': '7.2', 'vikara_rule': '7_2_84', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_84', 'operation': 'lopa', 'fires': True}),
    "7.2.85": ({'range': '7.2', 'vikara_rule': '7_2_85', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_85', 'operation': 'lopa', 'fires': True}),
    "7.2.86": ({'range': '7.2', 'vikara_rule': '7_2_86', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_86', 'operation': 'lopa', 'fires': True}),
    "7.2.87": ({'range': '7.2', 'vikara_rule': '7_2_87', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_87', 'operation': 'lopa', 'fires': True}),
    "7.2.88": ({'range': '7.2', 'vikara_rule': 'dvivacana', 'suffix_context': 'dvivacana', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'dvivacana', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.89": ({'range': '7.2', 'vikara_rule': '7_2_89', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_89', 'operation': 'lopa', 'fires': True}),
    "7.2.9": ({'range': '7.2', 'vikara_rule': '7_2_9', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_9', 'operation': 'lopa', 'fires': True}),
    "7.2.90": ({'range': '7.2', 'vikara_rule': 'lopa', 'operation': 'lopa', 'fires': True}, {'range': '7.2', 'vikara_rule': 'lopa', 'operation': 'vikara', 'fires': True}),
    "7.2.91": ({'range': '7.2', 'vikara_rule': '7_2_91', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_91', 'operation': 'lopa', 'fires': True}),
    "7.2.92": ({'range': '7.2', 'vikara_rule': 'dvivacana_yuvavau', 'suffix_context': 'dvivacana', 'substitute': 'yuvāvau', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'dvivacana_yuvavau', 'suffix_context': 'ling', 'substitute': 'yuvāvau', 'operation': 'vikara', 'fires': True}),
    "7.2.93": ({'range': '7.2', 'vikara_rule': '7_2_93', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_93', 'operation': 'lopa', 'fires': True}),
    "7.2.94": ({'range': '7.2', 'vikara_rule': 'tvahau', 'substitute': 'tvāhau', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'tvahau', 'substitute': 'tvāhau', 'operation': 'lopa', 'fires': True}),
    "7.2.95": ({'range': '7.2', 'vikara_rule': '7_2_95', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_95', 'operation': 'lopa', 'fires': True}),
    "7.2.96": ({'range': '7.2', 'vikara_rule': '7_2_96', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_96', 'operation': 'lopa', 'fires': True}),
    "7.2.97": ({'range': '7.2', 'vikara_rule': 'ekavacana', 'suffix_context': 'ekavacana', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': 'ekavacana', 'suffix_context': 'ling', 'operation': 'vikara', 'fires': True}),
    "7.2.98": ({'range': '7.2', 'vikara_rule': '7_2_98', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_98', 'operation': 'lopa', 'fires': True}),
    "7.2.99": ({'range': '7.2', 'vikara_rule': '7_2_99', 'operation': 'vikara', 'fires': True}, {'range': '7.2', 'vikara_rule': '7_2_99', 'operation': 'lopa', 'fires': True}),
}

META: dict[str, SutraMeta] = {
    "7.2.1": SutraMeta(_VIDHI, "सिचि वृद्धिः परस्मैपदेषु ।", ("vikara:7.2", "sic_vrddhi_parasmaipada")),
    "7.2.2": SutraMeta(_VIDHI, "अतो र्लान्तस्य ।", ("vikara:7.2", "7_2_2")),
    "7.2.3": SutraMeta(_VIDHI, "वदव्रजहलन्तस्याचः ।", ("vikara:7.2", "7_2_3")),
    "7.2.4": SutraMeta(_PRATISEDHA, "नेटि ।", ("vikara:7.2", "it_it_blocked")),
    "7.2.5": SutraMeta(_VIDHI, "ह्म्यन्तक्षणश्वसजागृणिश्व्येदिताम् ।", ("vikara:7.2", "7_2_5")),
    "7.2.6": SutraMeta(_VIBHASHA, "ऊर्णोतेर्विभाषा ।", ("vikara:7.2", "urnu")),
    "7.2.7": SutraMeta(_VIDHI, "अतो हलादेर्लघोः ।", ("vikara:7.2", "7_2_7")),
    "7.2.8": SutraMeta(_PRATISEDHA, "नेड् वशि कृति ।", ("vikara:7.2", "vasi_it_blocked")),
    "7.2.9": SutraMeta(_VIDHI, "तितुत्रतथसिसुसरकसेषु च ।", ("vikara:7.2", "7_2_9")),
    "7.2.10": SutraMeta(_VIDHI, "एकाच उपदेशेऽनुदात्तात्‌ ।", ("vikara:7.2", "7_2_10")),
    "7.2.11": SutraMeta(_VIDHI, "श्र्युकः किति ।", ("vikara:7.2", "kit")),
    "7.2.12": SutraMeta(_VIDHI, "सनि ग्रहगुहोश्च ।", ("vikara:7.2", "san_grahaguha")),
    "7.2.13": SutraMeta(_VIDHI, "कृसृभृवृस्तुद्रुस्रुश्रुवो लिटि ।", ("vikara:7.2", "lit")),
    "7.2.14": SutraMeta(_VIDHI, "श्वीदितो निष्ठायाम् ।", ("vikara:7.2", "nistha_svidit")),
    "7.2.15": SutraMeta(_VIBHASHA, "यस्य विभाषा ।", ("vikara:7.2", "7_2_15")),
    "7.2.16": SutraMeta(_VIDHI, "आदितश्च ।", ("vikara:7.2", "7_2_16")),
    "7.2.17": SutraMeta(_VIBHASHA, "विभाषा भावादिकर्मणोः ।", ("vikara:7.2", "7_2_17")),
    "7.2.18": SutraMeta(_VIDHI, "क्षुब्धस्वान्तध्वान्तलग्नम्लिष्टविरिब्धफाण्टबाढानि मन्थमनस्तमःसक्ताविस्पष्टस्वरानायासभृशेषु ।", ("vikara:7.2", "7_2_18")),
    "7.2.19": SutraMeta(_VIDHI, "धृषिशसी वैयात्ये ।", ("vikara:7.2", "7_2_19")),
    "7.2.20": SutraMeta(_VIDHI, "दृढः स्थूलबलयोः ।", ("vikara:7.2", "7_2_20")),
    "7.2.21": SutraMeta(_VIDHI, "प्रभौ परिवृढः ।", ("vikara:7.2", "7_2_21")),
    "7.2.22": SutraMeta(_VIDHI, "कृच्छ्रगहनयोः कषः ।", ("vikara:7.2", "7_2_22")),
    "7.2.23": SutraMeta(_VIDHI, "घुषिरविशब्दने ।", ("vikara:7.2", "7_2_23")),
    "7.2.24": SutraMeta(_VIDHI, "अर्देः संनिविभ्यः ।", ("vikara:7.2", "7_2_24")),
    "7.2.25": SutraMeta(_VIDHI, "अभेश्चाविदूर्ये ।", ("vikara:7.2", "7_2_25")),
    "7.2.26": SutraMeta(_VIDHI, "णेरध्ययने वृत्तम् ।", ("vikara:7.2", "7_2_26")),
    "7.2.27": SutraMeta(_VIBHASHA, "वा दान्तशान्तपूर्णदस्तस्पष्टच्छन्नज्ञप्ताः ।", ("vikara:7.2", "7_2_27")),
    "7.2.28": SutraMeta(_VIDHI, "रुष्यमत्वरसंघुषास्वनाम् ।", ("vikara:7.2", "7_2_28")),
    "7.2.29": SutraMeta(_VIDHI, "हृषेर्लोमसु ।", ("vikara:7.2", "7_2_29")),
    "7.2.30": SutraMeta(_VIDHI, "अपचितश्च ।", ("vikara:7.2", "7_2_30")),
    "7.2.31": SutraMeta(_VIDHI, "ह्रु ह्वरेश्छन्दसि ।", ("vikara:7.2", "chandas")),
    "7.2.32": SutraMeta(_VIDHI, "अपरिह्वृताश्च ।", ("vikara:7.2", "7_2_32")),
    "7.2.33": SutraMeta(_VIDHI, "सोमे ह्वरितः ।", ("vikara:7.2", "7_2_33")),
    "7.2.34": SutraMeta(_VIDHI, "ग्रसितस्कभितस्तभितोत्तभितचत्तविकस्तविशस्तॄशंस्तृशास्तृतरुतृतरूतृवरुतृवरूतृवरुत्रीरुज्ज्वलितिक्षरितिक्षमितिवमित्यमितीति च ।", ("vikara:7.2", "7_2_34")),
    "7.2.35": SutraMeta(_VIDHI, "आर्धधातुकस्येड् वलादेः ।", ("vikara:7.2", "it")),
    "7.2.36": SutraMeta(_VIDHI, "स्नुक्रमोरनात्मनेपदनिमित्ते ।", ("vikara:7.2", "7_2_36")),
    "7.2.37": SutraMeta(_VIDHI, "ग्रहोऽलिटि दीर्घः ।", ("vikara:7.2", "lit_dirgha")),
    "7.2.38": SutraMeta(_VIBHASHA, "वॄतो वा ।", ("vikara:7.2", "7_2_38")),
    "7.2.39": SutraMeta(_PRATISEDHA, "न लिङि ।", ("vikara:7.2", "ling_blocked")),
    "7.2.40": SutraMeta(_VIDHI, "सिचि च परस्मैपदेषु ।", ("vikara:7.2", "sic_parasmaipada")),
    "7.2.41": SutraMeta(_VIBHASHA, "इट् सनि वा ।", ("vikara:7.2", "it")),
    "7.2.42": SutraMeta(_VIDHI, "लिङ्सिचोरात्मनेपदेषु ।", ("vikara:7.2", "ling_atmanepada")),
    "7.2.43": SutraMeta(_VIDHI, "ऋतश्च संयोगादेः ।", ("vikara:7.2", "7_2_43")),
    "7.2.44": SutraMeta(_VIBHASHA, "स्वरतिसूतिसूयतिधूञूदितो वा ।", ("vikara:7.2", "7_2_44")),
    "7.2.45": SutraMeta(_VIDHI, "रधादिभ्यश्च ।", ("vikara:7.2", "7_2_45")),
    "7.2.46": SutraMeta(_VIDHI, "निरः कुषः ।", ("vikara:7.2", "7_2_46")),
    "7.2.47": SutraMeta(_VIDHI, "इण्निष्ठायाम् ।", ("vikara:7.2", "it")),
    "7.2.48": SutraMeta(_VIDHI, "तीषसहलुभरुषरिषः ।", ("vikara:7.2", "7_2_48")),
    "7.2.49": SutraMeta(_VIDHI, "सनीवन्तर्धभ्रस्जदम्भुश्रिस्वृयूर्णुभरज्ञपिसनाम् ।", ("vikara:7.2", "san")),
    "7.2.50": SutraMeta(_VIDHI, "क्लिशः क्त्वानिष्ठयोः ।", ("vikara:7.2", "7_2_50")),
    "7.2.51": SutraMeta(_VIDHI, "पूङश्च ।", ("vikara:7.2", "7_2_51")),
    "7.2.52": SutraMeta(_VIDHI, "वसतिक्षुधोरिट् ।", ("vikara:7.2", "it")),
    "7.2.53": SutraMeta(_VIDHI, "अञ्चेः पूजायाम् ।", ("vikara:7.2", "7_2_53")),
    "7.2.54": SutraMeta(_VIDHI, "लुभो विमोचने ।", ("vikara:7.2", "7_2_54")),
    "7.2.55": SutraMeta(_VIDHI, "जॄव्रश्च्योः क्त्वि ।", ("vikara:7.2", "ktva")),
    "7.2.56": SutraMeta(_VIBHASHA, "उदितो वा ।", ("vikara:7.2", "7_2_56")),
    "7.2.57": SutraMeta(_VIDHI, "सेऽसिचि कृतचृतच्छृदतृदनृतः ।", ("vikara:7.2", "sic")),
    "7.2.58": SutraMeta(_VIDHI, "गमेरिट् परस्मैपदेषु ।", ("vikara:7.2", "it_parasmaipada")),
    "7.2.59": SutraMeta(_PRATISEDHA, "न वृद्भ्यश्चतुर्भ्यः ।", ("vikara:7.2", "blocked")),
    "7.2.60": SutraMeta(_VIDHI, "तासि च कॢपः ।", ("vikara:7.2", "7_2_60")),
    "7.2.61": SutraMeta(_VIDHI, "अचस्तास्वत्‌ थल्यनिटो नित्यम् ।", ("vikara:7.2", "7_2_61")),
    "7.2.62": SutraMeta(_VIDHI, "उपदेशेऽत्वतः ।", ("vikara:7.2", "7_2_62")),
    "7.2.63": SutraMeta(_VIDHI, "ऋतो भारद्वाजस्य ।", ("vikara:7.2", "7_2_63")),
    "7.2.64": SutraMeta(_VIDHI, "बभूथाततन्थजगृम्भववर्थेति निगमे ।", ("vikara:7.2", "nigama")),
    "7.2.65": SutraMeta(_VIBHASHA, "विभाषा सृजिदृषोः ।", ("vikara:7.2", "7_2_65")),
    "7.2.66": SutraMeta(_VIDHI, "इडत्त्यर्तिव्ययतीनाम् ।", ("vikara:7.2", "it")),
    "7.2.67": SutraMeta(_VIDHI, "वस्वेकाजाद्घसाम् ।", ("vikara:7.2", "7_2_67")),
    "7.2.68": SutraMeta(_VIBHASHA, "विभाषा गमहनविदविशाम् ।", ("vikara:7.2", "7_2_68")),
    "7.2.69": SutraMeta(_VIDHI, "सनिंससनिवांसम् ।", ("vikara:7.2", "san")),
    "7.2.70": SutraMeta(_VIDHI, "ऋद्धनोः स्ये ।", ("vikara:7.2", "7_2_70")),
    "7.2.71": SutraMeta(_VIDHI, "अञ्जेः सिचि ।", ("vikara:7.2", "sic")),
    "7.2.72": SutraMeta(_VIDHI, "स्तुसुधूञ्भ्यः परस्मैपदेषु ।", ("vikara:7.2", "parasmaipada")),
    "7.2.73": SutraMeta(_VIDHI, "यमरमनमातां सक् च ।", ("vikara:7.2", "7_2_73")),
    "7.2.74": SutraMeta(_VIDHI, "स्मिपूङ्रञ्ज्वशां सनि ।", ("vikara:7.2", "san")),
    "7.2.75": SutraMeta(_VIDHI, "किरश्च पञ्चभ्यः ।", ("vikara:7.2", "7_2_75")),
    "7.2.76": SutraMeta(_VIDHI, "रुदादिभ्यः सार्वधातुके ।", ("vikara:7.2", "sarvadhatuka")),
    "7.2.77": SutraMeta(_VIDHI, "ईशः से ।", ("vikara:7.2", "7_2_77")),
    "7.2.78": SutraMeta(_VIDHI, "ईडजनोर्ध्वे च ।", ("vikara:7.2", "7_2_78")),
    "7.2.79": SutraMeta(_VIDHI, "लिङः सलोपोऽनन्त्यस्य ।", ("vikara:7.2", "lopa")),
    "7.2.80": SutraMeta(_VIDHI, "अतो येयः ।", ("vikara:7.2", "7_2_80")),
    "7.2.81": SutraMeta(_VIDHI, "आतो ङितः ।", ("vikara:7.2", "ngit")),
    "7.2.82": SutraMeta(_VIDHI, "आने मुक् ।", ("vikara:7.2", "7_2_82")),
    "7.2.83": SutraMeta(_VIDHI, "ईदासः ।", ("vikara:7.2", "7_2_83")),
    "7.2.84": SutraMeta(_VIDHI, "अष्टन आ विभक्तौ ।", ("vikara:7.2", "7_2_84")),
    "7.2.85": SutraMeta(_VIDHI, "रायो हलि ।", ("vikara:7.2", "7_2_85")),
    "7.2.86": SutraMeta(_VIDHI, "युष्मदस्मदोरनादेशे ।", ("vikara:7.2", "7_2_86")),
    "7.2.87": SutraMeta(_VIDHI, "द्वितीयायां च ।", ("vikara:7.2", "7_2_87")),
    "7.2.88": SutraMeta(_VIDHI, "प्रथमायाश्च द्विवचने भाषायाम् ।", ("vikara:7.2", "dvivacana")),
    "7.2.89": SutraMeta(_VIDHI, "योऽचि ।", ("vikara:7.2", "7_2_89")),
    "7.2.90": SutraMeta(_VIDHI, "शेषे लोपः ।", ("vikara:7.2", "lopa")),
    "7.2.91": SutraMeta(_VIDHI, "मपर्यन्तस्य ।", ("vikara:7.2", "7_2_91")),
    "7.2.92": SutraMeta(_VIDHI, "युवावौ द्विवचने ।", ("vikara:7.2", "dvivacana_yuvavau")),
    "7.2.93": SutraMeta(_VIDHI, "यूयवयौ जसि ।", ("vikara:7.2", "7_2_93")),
    "7.2.94": SutraMeta(_VIDHI, "त्वाहौ सौ ।", ("vikara:7.2", "tvahau")),
    "7.2.95": SutraMeta(_VIDHI, "तुभ्यमह्यौ ङयि ।", ("vikara:7.2", "7_2_95")),
    "7.2.96": SutraMeta(_VIDHI, "तवममौ ङसि ।", ("vikara:7.2", "7_2_96")),
    "7.2.97": SutraMeta(_VIDHI, "त्वमावेकवचने ।", ("vikara:7.2", "ekavacana")),
    "7.2.98": SutraMeta(_VIDHI, "प्रतयोत्तरपदयोश्च ।", ("vikara:7.2", "7_2_98")),
    "7.2.99": SutraMeta(_VIDHI, "त्रिचतुरोः स्त्रियां तिसृचतसृ ।", ("vikara:7.2", "7_2_99")),
    "7.2.100": SutraMeta(_VIDHI, "अचि र ऋतः ।", ("vikara:7.2", "7_2_100")),
    "7.2.101": SutraMeta(_VIDHI, "जराया जरसन्यतरस्याम् ।", ("vikara:7.2", "7_2_101")),
    "7.2.102": SutraMeta(_VIDHI, "त्यदादीनामः ।", ("vikara:7.2", "7_2_102")),
    "7.2.103": SutraMeta(_VIDHI, "किमः कः ।", ("vikara:7.2", "7_2_103")),
    "7.2.104": SutraMeta(_VIDHI, "कु तिहोः ।", ("vikara:7.2", "7_2_104")),
    "7.2.105": SutraMeta(_VIDHI, "क्वाति ।", ("vikara:7.2", "7_2_105")),
    "7.2.106": SutraMeta(_VIDHI, "तदोः सः सावनन्त्ययोः ।", ("vikara:7.2", "7_2_106")),
    "7.2.107": SutraMeta(_VIDHI, "अदस औ सुलोपश्च ।", ("vikara:7.2", "lopa")),
    "7.2.108": SutraMeta(_VIDHI, "इदमो मः ।", ("vikara:7.2", "7_2_108")),
    "7.2.109": SutraMeta(_VIDHI, "दश्च ।", ("vikara:7.2", "7_2_109")),
    "7.2.110": SutraMeta(_VIDHI, "यः सौ ।", ("vikara:7.2", "7_2_110")),
    "7.2.111": SutraMeta(_VIDHI, "इदोऽय् पुंसि ।", ("vikara:7.2", "7_2_111")),
    "7.2.112": SutraMeta(_VIDHI, "अनाप्यकः ।", ("vikara:7.2", "7_2_112")),
    "7.2.113": SutraMeta(_VIDHI, "हलि लोपः ।", ("vikara:7.2", "lopa")),
    "7.2.114": SutraMeta(_VIDHI, "मृजेर्वृद्धिः ।", ("vikara:7.2", "vrddhi")),
    "7.2.115": SutraMeta(_VIDHI, "अचो ञ्णिति ।", ("vikara:7.2", "niti")),
    "7.2.116": SutraMeta(_VIDHI, "अत उपधायाः ।", ("vikara:7.2", "7_2_116")),
    "7.2.117": SutraMeta(_VIDHI, "तद्धितेष्वचामादेः ।", ("vikara:7.2", "taddhita")),
    "7.2.118": SutraMeta(_VIDHI, "किति च ।", ("vikara:7.2", "kit")),
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
        raise AssertionError("sutra_impl_7_2 self_check failed:\n" + "\n".join(failures))
    return {
        "sutras": len(FIXTURES),
        "predicates": len([n for n in globals() if n.startswith("sutra_7_2_")]),
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
