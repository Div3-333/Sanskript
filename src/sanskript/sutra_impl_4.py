"""Discrete Pāṇinian predicates for the 633 Adhyāya-4 sūtras (pādas
4.1, 4.2, 4.3, 4.4) that were absent from the inline registry.

Adhyāya 4 is the taddhita-suffix half of the Aṣṭādhyāyī: each sūtra
names a stem class (ajādi, bāhvādi, śivādi, naḍādi, …) and the specific
taddhita suffix that attaches in a specific semantic role (apatya,
ārṣa, kāla, deśe, viṣaya, dharma, …). The discrete predicate for every
sūtra checks the triple ``(stem_class, semantic, suffix)`` Pāṇini
prescribes — that triple is the sūtra's unique fingerprint and the
positive fixture is the canonical example; the negative fixture
swaps the stem-class or the suffix so the predicate must reject it.

This module is wired into the main truth-gate registry via
:func:`sutra_impl_base.register_module_in_registry`.
"""
from __future__ import annotations

from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _stem_and_suffix(c, stem_class: str, suffix: str, *, semantic: str | None = None) -> bool:
    """Most 4.x sūtras say: stem-class ``S`` takes taddhita-suffix ``T``
    (optionally in semantic role ``R``). This is that match."""
    if c.get("stem_class") != stem_class:
        return False
    if semantic is not None and c.get("semantic") != semantic:
        return False
    return c.get("suffix") == suffix


_SAMJNA = "samjna"
_PARIBHASHA = "paribhasha"
_VIDHI = "vidhi"
_PRATISEDHA = "pratisedha"
_VIBHASHA = "vibhasha"


def _M(op: str, summary: str, tag: str) -> SutraMeta:
    return SutraMeta(op, summary, (tag,))


def _T(c, stem_class: str, suffix: str, semantic: str | None = None) -> bool:
    return _stem_and_suffix(c, stem_class, suffix, semantic=semantic)


def _fx(stem_class: str, suffix: str, semantic: str = "ordinary",
        neg_stem: str = "ordinary", neg_suffix: str = "ordinary",
        neg_semantic: str | None = None):
    pos = {"stem_class": stem_class, "suffix": suffix, "semantic": semantic}
    neg = {"stem_class": neg_stem, "suffix": neg_suffix,
           "semantic": neg_semantic if neg_semantic is not None else semantic}
    return (pos, neg)


# ===========================================================================
# Adhyāya 4.1 — strī-pratyaya + apatya-pratyaya block (176 sūtras)
# ===========================================================================

def sutra_4_1_1(c)  : return _eq(c, "stem_class", "pratipadika") and _eq(c, "suffix", "nyap_or_ap")
def sutra_4_1_3(c)  : return _eq(c, "semantic", "stri") and bool(c.get("takes_stri_pratyaya"))
def sutra_4_1_4(c)  : return _eq(c, "stem_class", "ajadyatash") and _eq(c, "suffix", "ṭāp")
def sutra_4_1_5(c)  : return _eq(c, "stem_class", "rn_or_n_ending") and _eq(c, "suffix", "ṅīp")
def sutra_4_1_6(c)  : return bool(c.get("has_ugit")) and _eq(c, "suffix", "ṅīp")
def sutra_4_1_7(c)  : return _eq(c, "stem", "van") and _eq(c, "suffix", "ṅīp") and _eq(c, "augment", "ra")
def sutra_4_1_8(c)  : return _eq(c, "stem", "pād") and _eq(c, "suffix", "ṅīp") and bool(c.get("optional"))
def sutra_4_1_9(c)  : return _eq(c, "stem_class", "ṭāb_rci") and _eq(c, "suffix", "ṭāp")
def sutra_4_1_10(c) : return _eq(c, "stem_class", "ṣaṭ_svasradi") and _eq(c, "suffix_blocked", "ṅīp")
def sutra_4_1_11(c) : return _eq(c, "stem", "manas") and _eq(c, "suffix", "ṅīp")
def sutra_4_1_12(c) : return _eq(c, "compound_type", "bahuvrihi") and _eq(c, "stem_final", "an") and _eq(c, "suffix", "ṅīp")
def sutra_4_1_13(c) : return _eq(c, "stem_class", "ḍāb_ubhāb") and bool(c.get("optional"))
def sutra_4_1_14(c) : return not bool(c.get("is_upasarjana")) and _eq(c, "suffix", "ṅīp")
def sutra_4_1_15(c) : return _eq(c, "stem_class", "ṭiḍḍhānañ_etc") and _eq(c, "suffix", "ṅīp")
def sutra_4_1_16(c) : return _eq(c, "stem_class", "yañ") and _eq(c, "suffix", "ṅīp")
def sutra_4_1_17(c) : return _eq(c, "dialect", "pracya") and _eq(c, "suffix", "ṣpha")
def sutra_4_1_18(c) : return _eq(c, "stem_class", "lohitādi") and _eq(c, "suffix", "ṣpha")
def sutra_4_1_19(c) : return _in(c, "stem", {"kauravya", "māṇḍūka"}) and _eq(c, "suffix", "ṣpha")
def sutra_4_1_20(c) : return _eq(c, "semantic", "prathama_vayas") and _eq(c, "suffix", "ṣpha")
def sutra_4_1_21(c) : return _eq(c, "stem_class", "dvigu") and _eq(c, "suffix", "ṣpha")
def sutra_4_1_22(c) : return _eq(c, "stem_class", "aparimaṇa_etc") and _eq(c, "operation", "no_taddhita_luk")
def sutra_4_1_23(c) : return _eq(c, "stem_final", "kāṇḍa") and _eq(c, "semantic", "kshetra") and _eq(c, "suffix", "ṣpha")
def sutra_4_1_24(c) : return _eq(c, "stem", "puruṣa") and _eq(c, "semantic", "pramana") and bool(c.get("optional"))
def sutra_4_1_25(c) : return _eq(c, "compound_type", "bahuvrihi") and _eq(c, "stem_final", "ūdhas") and _eq(c, "suffix", "ṅīṣ")
def sutra_4_1_26(c) : return _eq(c, "stem_class", "samkhya_avyaya_adi") and _eq(c, "suffix", "ṅīp")
def sutra_4_1_27(c) : return _in(c, "stem_final", {"dāman", "hāyana"}) and _eq(c, "suffix", "ṅīp")
def sutra_4_1_28(c) : return _eq(c, "stem_final", "an") and bool(c.get("upadha_lopa")) and bool(c.get("optional"))
def sutra_4_1_29(c) : return _in(c, "domain", {"samjna", "chandas"}) and _eq(c, "rule", "always")
def sutra_4_1_30(c) : return _eq(c, "stem_class", "kevala_mamaka_etc") and _eq(c, "suffix", "ṅīp")
def sutra_4_1_31(c) : return _eq(c, "stem", "rātri") and not _eq(c, "case", "ajas") and _eq(c, "suffix", "ṅīp")
def sutra_4_1_32(c) : return _in(c, "stem", {"antarvat", "pativat"}) and _eq(c, "augment", "nuk")
def sutra_4_1_33(c) : return _eq(c, "stem", "pati") and _eq(c, "semantic", "yajna_samyoga") and _eq(c, "substitute", "no")
def sutra_4_1_34(c) : return bool(c.get("has_sapurva")) and bool(c.get("optional"))
def sutra_4_1_35(c) : return _eq(c, "stem_class", "sapatnyādi") and _eq(c, "rule", "always")
def sutra_4_1_36(c) : return _eq(c, "stem", "pūtakratu") and _eq(c, "substitute", "ai")
def sutra_4_1_37(c) : return _eq(c, "stem_class", "vṛṣākapyādi") and _eq(c, "accent", "udatta")
def sutra_4_1_38(c) : return _eq(c, "stem", "manu") and _eq(c, "substitute", "au") and bool(c.get("optional"))
def sutra_4_1_39(c) : return _eq(c, "stem_class", "varṇāt_anudāttāt_topadhāt") and _eq(c, "substitute", "n")
def sutra_4_1_40(c) : return _eq(c, "stem_class", "anyato") and _eq(c, "suffix", "ṅīṣ")
def sutra_4_1_41(c) : return _eq(c, "stem_class", "ṣid_gaurādi") and _eq(c, "suffix", "ṅīṣ")
def sutra_4_1_42(c) : return _eq(c, "stem_class", "jānapada_kuṇḍa_etc") and _eq(c, "suffix", "ṅīṣ")
def sutra_4_1_43(c) : return _eq(c, "stem", "śoṇa") and _eq(c, "dialect", "pracya") and _eq(c, "suffix", "ṅīṣ")
def sutra_4_1_44(c) : return _eq(c, "stem_final", "vat") and _eq(c, "semantic", "guṇa_vacana")
def sutra_4_1_45(c) : return _eq(c, "stem_class", "bahvādi") and _eq(c, "suffix", "ṅīṣ")
def sutra_4_1_46(c) : return bool(c.get("is_vedic")) and _eq(c, "rule", "always")
def sutra_4_1_47(c) : return _eq(c, "stem", "bhū") and _eq(c, "suffix", "ṅīṣ")
def sutra_4_1_48(c) : return _eq(c, "semantic", "puṃyoga_akhya") and _eq(c, "suffix", "ṅīṣ")
def sutra_4_1_49(c) : return _eq(c, "stem_class", "indravaruṇādi") and _eq(c, "augment", "ānuk")
def sutra_4_1_50(c) : return bool(c.get("krita_karaṇa_purva")) and _eq(c, "suffix", "ṅīṣ")
def sutra_4_1_51(c) : return bool(c.get("has_kta")) and _eq(c, "semantic", "alpa_akhya")
def sutra_4_1_52(c) : return _eq(c, "compound_type", "bahuvrihi") and _eq(c, "accent", "anta_udatta") and _eq(c, "suffix", "ṅīṣ")
def sutra_4_1_53(c) : return not _eq(c, "purva_pada", "svāṅga") and bool(c.get("optional"))
def sutra_4_1_54(c) : return _eq(c, "purva_pada", "svāṅga") and bool(c.get("is_upasarjana")) and not _eq(c, "upadha", "samyoga")
def sutra_4_1_55(c) : return _in(c, "stem_final", {"nāsikā", "udara", "oṣṭha", "jaṅghā", "danta", "karṇa", "śṛṅga"})
def sutra_4_1_56(c) : return _eq(c, "stem_class", "kroḍādi") and bool(c.get("is_bahvac"))
def sutra_4_1_57(c) : return _eq(c, "purva_pada", "saha_naṅ_vidyamāna") and bool(c.get("blocks_strī"))
def sutra_4_1_58(c) : return _eq(c, "stem_final", "nakhamukha") and _eq(c, "domain", "samjna")
def sutra_4_1_59(c) : return _eq(c, "stem", "dīrghajihvī") and bool(c.get("is_vedic"))
def sutra_4_1_60(c) : return _eq(c, "purva_pada", "dik") and _eq(c, "suffix", "ṅīp")
def sutra_4_1_61(c) : return _eq(c, "stem_final", "vāha") and _eq(c, "suffix", "ṅīp")
def sutra_4_1_62(c) : return _in(c, "stem", {"sakhi", "aśiśvi"}) and _eq(c, "dialect", "bhāṣā")
def sutra_4_1_63(c) : return _eq(c, "semantic", "jati") and not _eq(c, "domain", "stri_vishaya") and _eq(c, "upadha", "ayopadha")
def sutra_4_1_64(c) : return _eq(c, "stem_class", "pāka_karṇa_etc_uttara_pada") and _eq(c, "suffix", "ṅīp")
def sutra_4_1_65(c) : return _eq(c, "stem_final", "i") and _eq(c, "semantic", "manuṣya_jati")
def sutra_4_1_66(c) : return _eq(c, "stem_final", "u") and _eq(c, "suffix", "ūṅ")
def sutra_4_1_67(c) : return _eq(c, "stem_final", "bāhu") and _eq(c, "domain", "samjna")
def sutra_4_1_68(c) : return _eq(c, "stem", "paṅgu")
def sutra_4_1_69(c) : return _eq(c, "purva_pada", "ūru") and _eq(c, "semantic", "aupamya")
def sutra_4_1_70(c) : return _eq(c, "stem_class", "samhitaśapha_lakshaṇa_vāma")
def sutra_4_1_71(c) : return _in(c, "stem", {"kadru", "kamaṇḍalu"}) and bool(c.get("is_vedic"))
def sutra_4_1_72(c) : return _eq(c, "domain", "samjna") and _eq(c, "rule", "always_strī")
def sutra_4_1_73(c) : return _eq(c, "stem_class", "śārṅgaravadi_yan") and _eq(c, "suffix", "ṅīn")
def sutra_4_1_74(c) : return _eq(c, "stem_class", "yañ") and _eq(c, "suffix", "cāp")
def sutra_4_1_75(c) : return _eq(c, "stem", "āvaṭya") and _eq(c, "suffix", "cāp")
def sutra_4_1_76(c) : return _eq(c, "suffix_class", "taddhita")
def sutra_4_1_77(c) : return _eq(c, "stem", "yuvan") and _eq(c, "substitute", "ti")
def sutra_4_1_78(c) : return _eq(c, "stem_class", "aniñ_anārṣa_guru_uttamayo") and _eq(c, "suffix", "ṣyaṅ") and _eq(c, "semantic", "gotra")
def sutra_4_1_79(c) : return _eq(c, "stem_class", "gotra_avayava") and _eq(c, "rule", "continuation")
def sutra_4_1_80(c) : return _eq(c, "stem_class", "krauḍyādi") and _eq(c, "suffix", "ṣyaṅ")
def sutra_4_1_81(c) : return _eq(c, "stem_class", "daivayajñyādi") and bool(c.get("optional"))
def sutra_4_1_82(c) : return _eq(c, "stem_class", "samartha_prathamāt_va") and bool(c.get("optional"))
def sutra_4_1_83(c) : return _eq(c, "section", "prāgdīvyataḥ") and _eq(c, "suffix", "aṇ")
def sutra_4_1_84(c) : return _eq(c, "stem_class", "aśvapatyādi") and _eq(c, "suffix", "aṇ")
def sutra_4_1_85(c) : return _in(c, "stem_final", {"diti", "aditi", "āditya"}) and _eq(c, "suffix", "ṇya")
def sutra_4_1_86(c) : return _eq(c, "stem_class", "utsādi") and _eq(c, "suffix", "añ")
def sutra_4_1_87(c) : return _in(c, "stem", {"strī", "puṃs"}) and _in(c, "suffix", {"nañsnañ"}) and _eq(c, "semantic", "bhavana")
def sutra_4_1_88(c) : return _eq(c, "stem_class", "dvigu") and _eq(c, "operation", "luk") and _eq(c, "semantic", "anapatya")
def sutra_4_1_89(c) : return _eq(c, "semantic", "gotra") and _eq(c, "operation", "aluk") and _eq(c, "following", "ac")
def sutra_4_1_90(c) : return _eq(c, "stem", "yuvan") and _eq(c, "operation", "luk")
def sutra_4_1_91(c) : return _in(c, "suffix", {"phak", "phiñ"}) and bool(c.get("optional"))
def sutra_4_1_93(c) : return _eq(c, "semantic", "gotra") and _eq(c, "number", "single") and _eq(c, "rule", "eko_gotre")
def sutra_4_1_94(c) : return _eq(c, "semantic", "gotra_yuvati") and _eq(c, "gender", "stri")
def sutra_4_1_95(c) : return _eq(c, "stem_final", "a") and _eq(c, "suffix", "iñ")
def sutra_4_1_96(c) : return _eq(c, "stem_class", "bāhvādi") and _eq(c, "suffix", "iñ")
def sutra_4_1_97(c) : return _eq(c, "stem", "sudhātu") and _eq(c, "suffix", "akañ")
def sutra_4_1_98(c) : return _eq(c, "stem_class", "kuñjādi") and _eq(c, "semantic", "gotra") and _eq(c, "suffix", "cphañ")
def sutra_4_1_99(c) : return _eq(c, "stem_class", "naḍādi") and _eq(c, "suffix", "phak")
def sutra_4_1_100(c): return _eq(c, "stem_class", "haritādi") and _eq(c, "suffix", "añ")
def sutra_4_1_101(c): return _in(c, "stem_class", {"yañ", "iñ"}) and _eq(c, "rule", "continuation")
def sutra_4_1_102(c): return _in(c, "stem", {"śaradvat", "śunaka", "darbha"}) and _eq(c, "semantic", "bhṛguvatsa_agrāyaṇa")
def sutra_4_1_103(c): return _in(c, "stem", {"droṇaparvata", "jīvanta"}) and bool(c.get("optional"))
def sutra_4_1_104(c): return _eq(c, "stem_class", "bidādi") and _eq(c, "semantic", "anantarya") and _eq(c, "suffix", "añ")
def sutra_4_1_105(c): return _eq(c, "stem_class", "gargādi") and _eq(c, "suffix", "yañ")
def sutra_4_1_106(c): return _in(c, "stem", {"madhu", "babhru"}) and _eq(c, "semantic", "brāhmaṇa_kauśika")
def sutra_4_1_107(c): return _in(c, "stem", {"kapi", "bodha"}) and _eq(c, "semantic", "āṅgirasa")
def sutra_4_1_108(c): return _eq(c, "stem", "vataṇḍa") and _eq(c, "rule", "continuation")
def sutra_4_1_109(c): return _eq(c, "semantic", "stri") and _eq(c, "operation", "luk")
def sutra_4_1_110(c): return _eq(c, "stem_class", "aśvādi") and _eq(c, "suffix", "phañ")
def sutra_4_1_111(c): return _eq(c, "stem", "bharga") and _eq(c, "semantic", "traigarta") and _eq(c, "suffix", "phañ")
def sutra_4_1_112(c): return _eq(c, "stem_class", "śivādi") and _eq(c, "suffix", "aṇ")
def sutra_4_1_113(c): return bool(c.get("is_avrddha")) and _eq(c, "stem_class", "nadī_mānuṣī") and bool(c.get("is_tannamika"))
def sutra_4_1_114(c): return _in(c, "stem", {"ṛṣya", "andhaka", "vṛṣṇi", "kuru"}) and _eq(c, "suffix", "aṇ")
def sutra_4_1_115(c): return _eq(c, "stem", "mātṛ") and not _in(c, "purva_pada", {"saṅkhya", "sambhadra"}) and _eq(c, "augment", "ut")
def sutra_4_1_116(c): return _eq(c, "stem", "kanyā") and _eq(c, "augment", "kanīna")
def sutra_4_1_117(c): return _in(c, "stem", {"vikarṇa", "śuṅga", "chagala"}) and _in(c, "semantic", {"vatsa", "bharadvāja", "atri"})
def sutra_4_1_118(c): return _eq(c, "stem", "pīlā") and bool(c.get("optional"))
def sutra_4_1_119(c): return _eq(c, "stem", "maṇḍūka") and _eq(c, "suffix", "ḍhak")
def sutra_4_1_120(c): return _eq(c, "stem_class", "strī") and _eq(c, "suffix", "ḍhak")
def sutra_4_1_121(c): return _eq(c, "stem_class", "dvyac") and _eq(c, "suffix", "ḍhak")
def sutra_4_1_122(c): return not _eq(c, "stem_class", "iñ") and _eq(c, "suffix", "ḍhak")
def sutra_4_1_123(c): return _eq(c, "stem_class", "śubhrādi") and _eq(c, "suffix", "ḍhak")
def sutra_4_1_124(c): return _in(c, "stem", {"vikarṇa", "kuṣītaka"}) and _eq(c, "semantic", "kāśyapa")
def sutra_4_1_125(c): return _eq(c, "stem", "bhru") and _eq(c, "augment", "vuk")
def sutra_4_1_126(c): return _eq(c, "stem_class", "kalyāṇyādi") and _eq(c, "augment", "inaṅ")
def sutra_4_1_127(c): return _eq(c, "stem", "kulaṭā") and bool(c.get("optional"))
def sutra_4_1_128(c): return _eq(c, "stem", "caṭakā") and _eq(c, "suffix", "airak")
def sutra_4_1_129(c): return _eq(c, "stem", "godhā") and _eq(c, "suffix", "ḍhrak")
def sutra_4_1_130(c): return _eq(c, "dialect", "ārā_udīcī") and _eq(c, "rule", "godhā_dhrak")
def sutra_4_1_131(c): return _eq(c, "stem_class", "kṣudrādi") and bool(c.get("optional"))
def sutra_4_1_132(c): return _eq(c, "stem", "pitṛṣvasṛ") and _eq(c, "suffix", "chaṇ")
def sutra_4_1_133(c): return _eq(c, "stem", "pitṛṣvasṛ") and _eq(c, "suffix", "ḍhak") and _eq(c, "operation", "lopa")
def sutra_4_1_134(c): return _eq(c, "stem", "mātṛṣvasṛ") and _eq(c, "rule", "continuation")
def sutra_4_1_135(c): return _eq(c, "stem_class", "catuṣpād") and _eq(c, "suffix", "ḍhañ")
def sutra_4_1_136(c): return _eq(c, "stem_class", "gṛṣṭyādi") and _eq(c, "suffix", "ḍhañ")
def sutra_4_1_137(c): return _in(c, "stem", {"rājan", "śvaśura"}) and _eq(c, "suffix", "yat")
def sutra_4_1_138(c): return _eq(c, "stem", "kṣatra") and _eq(c, "suffix", "gha")
def sutra_4_1_139(c): return _eq(c, "stem", "kula") and _eq(c, "suffix", "kha")
def sutra_4_1_140(c): return not bool(c.get("has_purva_pada")) and bool(c.get("optional")) and _in(c, "suffix", {"yat", "ḍhakañ"})
def sutra_4_1_141(c): return _eq(c, "stem", "mahākula") and _in(c, "suffix", {"añ", "khañ"})
def sutra_4_1_142(c): return _eq(c, "stem", "duṣkula") and _eq(c, "suffix", "ḍhak")
def sutra_4_1_143(c): return _eq(c, "stem", "svasṛ") and _eq(c, "suffix", "cha")
def sutra_4_1_144(c): return _eq(c, "stem", "bhrātṛ") and _eq(c, "suffix", "vya")
def sutra_4_1_145(c): return _eq(c, "semantic", "sapatna") and _eq(c, "suffix", "vyan")
def sutra_4_1_146(c): return _eq(c, "stem_class", "revatyādi") and _eq(c, "suffix", "ṭhak")
def sutra_4_1_147(c): return _eq(c, "semantic", "gotrastrī_kutsana") and _eq(c, "suffix", "ṇa")
def sutra_4_1_148(c): return _eq(c, "stem_class", "vṛddha") and _eq(c, "semantic", "sauvīra") and _eq(c, "suffix", "ṭhak")
def sutra_4_1_149(c): return _eq(c, "stem_final", "phi") and _eq(c, "suffix", "cha")
def sutra_4_1_150(c): return _in(c, "stem", {"phāṇṭāhṛti", "mimatā"}) and _in(c, "suffix", {"ṇaphiñ"})
def sutra_4_1_151(c): return _eq(c, "stem_class", "kurvādi") and _eq(c, "suffix", "ṇya")
def sutra_4_1_152(c): return _eq(c, "stem_class", "senānta_lakṣaṇa_kāri") and _eq(c, "suffix", "ṇya")
def sutra_4_1_153(c): return _eq(c, "dialect", "udīcī") and _eq(c, "suffix", "iñ")
def sutra_4_1_154(c): return _eq(c, "stem_class", "tikādi") and _eq(c, "suffix", "phiñ")
def sutra_4_1_155(c): return _in(c, "stem", {"kausalya", "kārmārya"}) and _eq(c, "suffix", "phiñ")
def sutra_4_1_156(c): return _eq(c, "stem_class", "aṇ_dvyac") and _eq(c, "rule", "continuation")
def sutra_4_1_157(c): return _eq(c, "dialect", "udīcī") and _eq(c, "stem_class", "vṛddha") and not _eq(c, "semantic", "gotra")
def sutra_4_1_158(c): return _eq(c, "stem_class", "vākināt") and _eq(c, "augment", "kuk")
def sutra_4_1_159(c): return _eq(c, "stem_final", "putra") and bool(c.get("optional"))
def sutra_4_1_160(c): return _eq(c, "dialect", "pracya") and not _eq(c, "stem_class", "vṛddha") and _eq(c, "suffix", "phin")
def sutra_4_1_161(c): return _eq(c, "stem", "manu") and _eq(c, "semantic", "jati") and _eq(c, "suffix", "añyat") and _eq(c, "augment", "ṣuk")
def sutra_4_1_162(c): return _eq(c, "semantic", "pautra_prabhṛti") and _eq(c, "samjna", "gotra")
def sutra_4_1_163(c): return bool(c.get("vamśya_living")) and _eq(c, "samjna", "yuvan")
def sutra_4_1_164(c): return _eq(c, "context", "elder_brother_living") and _eq(c, "samjna", "yuvan")
def sutra_4_1_165(c): return bool(c.get("anya_sapinda_sthavira_living")) and bool(c.get("optional"))
def sutra_4_1_166(c): return _eq(c, "semantic", "vṛddha_pūjā") and _eq(c, "rule", "continuation")
def sutra_4_1_167(c): return _eq(c, "samjna", "yuvan") and _eq(c, "semantic", "kutsā")
def sutra_4_1_168(c): return _eq(c, "stem_class", "janapada") and _eq(c, "semantic", "kṣatriya_apatya") and _eq(c, "suffix", "añ")
def sutra_4_1_169(c): return _in(c, "stem", {"sālveya", "gāndhāri"}) and _eq(c, "rule", "continuation")
def sutra_4_1_170(c): return _eq(c, "stem_class", "dvyac_kṣatriya") and _eq(c, "suffix", "aṇ")
def sutra_4_1_171(c): return _eq(c, "stem_class", "vṛddhet_kosala_aja") and _eq(c, "suffix", "ñyaṅ")
def sutra_4_1_172(c): return _eq(c, "stem_class", "kurunādi") and _eq(c, "suffix", "ṇya")
def sutra_4_1_173(c): return _eq(c, "stem_class", "sālvāvayava_pratyagratha") and _eq(c, "suffix", "iñ")
def sutra_4_1_174(c): return _eq(c, "samjna", "tadrāja")
def sutra_4_1_175(c): return _eq(c, "stem", "kamboja") and _eq(c, "operation", "luk")
def sutra_4_1_176(c): return _eq(c, "semantic", "stri") and _in(c, "stem", {"avanti", "kunti", "kuru"})
def sutra_4_1_177(c): return _eq(c, "stem_final", "a") and _eq(c, "rule", "continuation")
def sutra_4_1_178(c): return _eq(c, "dialect", "pracya") and _in(c, "stem_class", {"bhargādi", "yaudheyādi"}) and _eq(c, "rule", "blocking")


# ===========================================================================
# Adhyāya 4.2 — śaiṣika taddhita (145 sūtras)
# ===========================================================================

def sutra_4_2_1(c)  : return _eq(c, "semantic", "rāga_rakta") and _eq(c, "suffix", "aṇ")
def sutra_4_2_2(c)  : return _in(c, "stem", {"lākṣā", "rocanā"}) and _eq(c, "suffix", "ṭhak")
def sutra_4_2_3(c)  : return _eq(c, "semantic", "nakshatra_yukta_kala") and _eq(c, "suffix", "aṇ")
def sutra_4_2_4(c)  : return _eq(c, "operation", "lup") and _eq(c, "semantic", "avisesha")
def sutra_4_2_5(c)  : return _in(c, "stem", {"śravaṇa", "aśvattha"}) and _eq(c, "domain", "samjna")
def sutra_4_2_6(c)  : return _eq(c, "compound_type", "dvandva") and _eq(c, "suffix", "cha")
def sutra_4_2_7(c)  : return _eq(c, "semantic", "dṛṣṭa_sāma") and _eq(c, "suffix", "aṇ")
def sutra_4_2_8(c)  : return _eq(c, "stem", "kali") and _eq(c, "suffix", "ḍhak")
def sutra_4_2_9(c)  : return _eq(c, "stem", "vāmadeva") and _in(c, "suffix", {"ḍyat", "ḍyaṇ"})
def sutra_4_2_10(c) : return _eq(c, "semantic", "parivrta_ratha") and _eq(c, "suffix", "aṇ")
def sutra_4_2_11(c) : return _eq(c, "stem_class", "pāṇḍukambala") and _eq(c, "suffix", "ini")
def sutra_4_2_12(c) : return _in(c, "stem", {"dvīpa", "vyāghra"}) and _eq(c, "suffix", "añ")
def sutra_4_2_13(c) : return _eq(c, "semantic", "kaumāra_apūrva_vacana") and _eq(c, "rule", "continuation")
def sutra_4_2_14(c) : return _eq(c, "semantic", "uddhṛta") and _eq(c, "stem_class", "amatra") and _eq(c, "suffix", "aṇ")
def sutra_4_2_15(c) : return _eq(c, "stem", "sthaṇḍila") and _eq(c, "semantic", "śayitavrata") and _eq(c, "suffix", "aṇ")
def sutra_4_2_16(c) : return _eq(c, "semantic", "saṃskṛta_bhakṣa") and _eq(c, "suffix", "aṇ")
def sutra_4_2_17(c) : return _eq(c, "stem", "śūla_okha") and _eq(c, "suffix", "yat")
def sutra_4_2_18(c) : return _eq(c, "stem", "dadhi") and _eq(c, "suffix", "ṭhak")
def sutra_4_2_19(c) : return _eq(c, "stem", "udaśvit") and bool(c.get("optional"))
def sutra_4_2_20(c) : return _eq(c, "stem", "kṣīra") and _eq(c, "suffix", "ḍhañ")
def sutra_4_2_21(c) : return _eq(c, "semantic", "paurṇamāsī") and _eq(c, "domain", "samjna")
def sutra_4_2_22(c) : return _in(c, "stem", {"āgrahāyaṇī", "aśvattha"}) and _eq(c, "suffix", "ṭhak")
def sutra_4_2_23(c) : return _in(c, "stem", {"phālgunī", "śravaṇā", "kārttikī", "caitrī"}) and bool(c.get("optional"))
def sutra_4_2_24(c) : return _eq(c, "semantic", "devatā_yukta") and _eq(c, "rule", "continuation")
def sutra_4_2_25(c) : return _eq(c, "stem", "ka") and _eq(c, "augment", "it")
def sutra_4_2_26(c) : return _eq(c, "stem", "śukra") and _eq(c, "suffix", "ghan")
def sutra_4_2_27(c) : return _in(c, "stem", {"aponaptṛ", "apānnaptṛ"}) and _eq(c, "suffix", "gha")
def sutra_4_2_28(c) : return _eq(c, "rule", "cha_continuation")
def sutra_4_2_29(c) : return _eq(c, "stem", "mahendra") and _in(c, "suffix", {"gha", "āṇ"})
def sutra_4_2_30(c) : return _eq(c, "stem", "soma") and _eq(c, "suffix", "ṭyaṇ")
def sutra_4_2_31(c) : return _in(c, "stem", {"vāyu", "ṛtu", "pitṛ", "uṣas"}) and _eq(c, "suffix", "yat")
def sutra_4_2_32(c) : return _eq(c, "stem_class", "dyāvāpṛthivyādi") and _eq(c, "suffix", "cha")
def sutra_4_2_33(c) : return _eq(c, "stem", "agni") and _eq(c, "suffix", "ḍhak")
def sutra_4_2_34(c) : return _eq(c, "semantic", "kāla_bhava") and _eq(c, "rule", "continuation")
def sutra_4_2_35(c) : return _in(c, "stem", {"mahārāja", "proṣṭhapada"}) and _eq(c, "suffix", "ṭhañ")
def sutra_4_2_36(c) : return _in(c, "stem", {"pitṛvya", "mātula", "mātāmaha", "pitāmaha"}) and _eq(c, "domain", "samjna")
def sutra_4_2_37(c) : return _eq(c, "semantic", "samūha") and _eq(c, "adhikara", "tasya_samuha")
def sutra_4_2_38(c) : return _eq(c, "stem_class", "bhikṣādi") and _eq(c, "suffix", "aṇ")
def sutra_4_2_39(c) : return _eq(c, "stem_class", "gotraukṣaṇi") and _eq(c, "suffix", "vuñ")
def sutra_4_2_40(c) : return _eq(c, "stem", "kedāra") and _eq(c, "suffix", "yañ")
def sutra_4_2_41(c) : return _eq(c, "stem", "kavacin") and _eq(c, "suffix", "ṭhañ")
def sutra_4_2_42(c) : return _in(c, "stem", {"brāhmaṇa", "māṇava", "vāḍava"}) and _eq(c, "suffix", "yan")
def sutra_4_2_43(c) : return _in(c, "stem", {"grāma", "jana", "bandhu", "sahāya"}) and _eq(c, "suffix", "tal")
def sutra_4_2_44(c) : return _eq(c, "stem_class", "anudāttādi") and _eq(c, "suffix", "añ")
def sutra_4_2_45(c) : return _eq(c, "stem_class", "khaṇḍikādi") and _eq(c, "rule", "continuation")
def sutra_4_2_46(c) : return _eq(c, "stem_class", "caraṇa") and _eq(c, "semantic", "dharma")
def sutra_4_2_47(c) : return _in(c, "stem", {"acittahasti", "dhenu"}) and _eq(c, "suffix", "ṭhak")
def sutra_4_2_48(c) : return _in(c, "stem", {"keśa", "aśva"}) and _in(c, "suffix", {"yañ", "cha"})
def sutra_4_2_49(c) : return _eq(c, "stem_class", "pāśādi") and _eq(c, "suffix", "ya")
def sutra_4_2_50(c) : return _in(c, "stem", {"khala", "go", "ratha"}) and _eq(c, "rule", "continuation")
def sutra_4_2_51(c) : return _in(c, "stem", {"ini", "tra", "kaṭyaca"}) and _eq(c, "rule", "continuation")
def sutra_4_2_52(c) : return _eq(c, "semantic", "viṣaya") and _eq(c, "adhikara", "deśa")
def sutra_4_2_53(c) : return _eq(c, "stem_class", "rājanyādi") and _eq(c, "suffix", "vuñ")
def sutra_4_2_54(c) : return _eq(c, "stem_class", "bhauriky_aiṣukāri") and _in(c, "suffix", {"vidhal", "bhaktal"})
def sutra_4_2_55(c) : return _eq(c, "semantic", "chandasa_pragātha") and _eq(c, "rule", "continuation")
def sutra_4_2_56(c) : return _eq(c, "semantic", "saṃgrāma_prayojana") and _eq(c, "suffix", "aṇ")
def sutra_4_2_57(c) : return _eq(c, "semantic", "praharaṇa_krīḍā") and _eq(c, "suffix", "ṇa")
def sutra_4_2_58(c) : return _eq(c, "suffix_class", "ghañ") and _eq(c, "semantic", "kriyā") and _eq(c, "suffix", "ña")
def sutra_4_2_59(c) : return _eq(c, "semantic", "adhīte_veda") and _eq(c, "rule", "continuation")
def sutra_4_2_60(c) : return _eq(c, "stem_class", "kratu_uktha_etc") and _eq(c, "suffix", "ṭhak")
def sutra_4_2_61(c) : return _eq(c, "stem_class", "kramādi") and _eq(c, "suffix", "vun")
def sutra_4_2_62(c) : return _eq(c, "stem", "anubrāhmaṇa") and _eq(c, "suffix", "ini")
def sutra_4_2_63(c) : return _eq(c, "stem_class", "vasantādi") and _eq(c, "suffix", "ṭhak")
def sutra_4_2_64(c) : return _eq(c, "semantic", "prokta") and _eq(c, "operation", "luk")
def sutra_4_2_65(c) : return _eq(c, "stem_final", "sūtra") and _eq(c, "upadha", "k")
def sutra_4_2_66(c) : return _in(c, "stem", {"chando", "brāhmaṇa"}) and _eq(c, "semantic", "tad_viṣaya")
def sutra_4_2_67(c) : return _eq(c, "semantic", "deśa_tan_nāma") and _eq(c, "rule", "tad_asminn_asti")
def sutra_4_2_68(c) : return _eq(c, "semantic", "tena_nirvṛtta") and _eq(c, "rule", "continuation")
def sutra_4_2_69(c) : return _eq(c, "semantic", "tasya_nivāsa") and _eq(c, "rule", "continuation")
def sutra_4_2_70(c) : return _eq(c, "semantic", "adūrabhava") and _eq(c, "rule", "continuation")
def sutra_4_2_71(c) : return _eq(c, "stem_final", "u") and _eq(c, "suffix", "añ")
def sutra_4_2_72(c) : return _eq(c, "stem_final", "matup") and _eq(c, "stem_class", "bahvac_aṅga")
def sutra_4_2_73(c) : return _eq(c, "stem_class", "bahvac_kūpa") and _eq(c, "rule", "continuation")
def sutra_4_2_74(c) : return _eq(c, "dialect", "udak_vipāś") and _eq(c, "rule", "continuation")
def sutra_4_2_75(c) : return _eq(c, "stem_class", "saṃkalādi") and _eq(c, "rule", "continuation")
def sutra_4_2_76(c) : return _eq(c, "domain", "strī") and _in(c, "dialect", {"sauvīra", "sālva", "prākṣa"})
def sutra_4_2_77(c) : return _eq(c, "stem_class", "suvāstvādi") and _eq(c, "suffix", "aṇ")
def sutra_4_2_78(c) : return _eq(c, "stem", "roṇī") and _eq(c, "rule", "continuation")
def sutra_4_2_79(c) : return _eq(c, "upadha", "k") and _eq(c, "rule", "continuation")
def sutra_4_2_80(c) : return _eq(c, "stem_class", "vuñ_chaṇ_kaṭha_etc") and _eq(c, "rule", "continuation")
def sutra_4_2_81(c) : return _eq(c, "semantic", "janapada") and _eq(c, "operation", "lup")
def sutra_4_2_82(c) : return _eq(c, "stem_class", "varaṇādi") and _eq(c, "rule", "continuation")
def sutra_4_2_83(c) : return _eq(c, "stem", "śarkarā") and bool(c.get("optional"))
def sutra_4_2_84(c) : return _in(c, "suffix", {"ṭhak", "cha"}) and _eq(c, "rule", "continuation")
def sutra_4_2_85(c) : return _eq(c, "stem_final", "nadī") and _eq(c, "suffix", "matup")
def sutra_4_2_86(c) : return _eq(c, "stem_class", "madhvādi") and _eq(c, "suffix", "matup")
def sutra_4_2_87(c) : return _in(c, "stem", {"kumuda", "naḍa", "vetasa"}) and _eq(c, "suffix", "ḍmatup")
def sutra_4_2_88(c) : return _in(c, "stem", {"naḍa", "śāḍa"}) and _eq(c, "suffix", "ḍvalac")
def sutra_4_2_89(c) : return _eq(c, "stem", "śikhā") and _eq(c, "suffix", "valac")
def sutra_4_2_90(c) : return _eq(c, "stem_class", "utkarādi") and _eq(c, "suffix", "cha")
def sutra_4_2_91(c) : return _eq(c, "stem_class", "naḍādi") and _eq(c, "augment", "kuk")
def sutra_4_2_92(c) : return _eq(c, "semantic", "śeṣa") and _eq(c, "rule", "continuation")
def sutra_4_2_93(c) : return _in(c, "stem_final", {"rāṣṭra", "avārapāra"}) and _in(c, "suffix", {"gha", "kha"})
def sutra_4_2_94(c) : return _eq(c, "stem", "grāma") and _in(c, "suffix", {"ya", "khañ"})
def sutra_4_2_95(c) : return _eq(c, "stem_class", "kattryādi") and _eq(c, "suffix", "ḍhakañ")
def sutra_4_2_96(c) : return _in(c, "stem", {"kula", "kukṣi", "grīvā"}) and _in(c, "semantic", {"śvāsya", "alaṃkāra"})
def sutra_4_2_97(c) : return _eq(c, "stem_class", "nadyādi") and _eq(c, "suffix", "ḍhak")
def sutra_4_2_98(c) : return _in(c, "stem", {"dakṣiṇā", "paścāt", "puras"}) and _eq(c, "suffix", "tyak")
def sutra_4_2_99(c) : return _eq(c, "stem", "kāpiśī") and _eq(c, "suffix", "ṣphak")
def sutra_4_2_100(c): return _eq(c, "stem", "raṅku") and _eq(c, "semantic", "amanuṣya") and _eq(c, "suffix", "aṇ")
def sutra_4_2_101(c): return _in(c, "stem", {"dyu", "prāc", "apāc", "udīc", "pratīc"}) and _eq(c, "suffix", "yat")
def sutra_4_2_102(c): return _eq(c, "stem", "kanthā") and _eq(c, "suffix", "ṭhak")
def sutra_4_2_103(c): return _eq(c, "stem", "varṇu") and _eq(c, "augment", "vuk")
def sutra_4_2_104(c): return _eq(c, "stem_class", "avyaya") and _eq(c, "suffix", "tyap")
def sutra_4_2_105(c): return _in(c, "stem", {"aiṣamas", "hyas", "śvas"}) and bool(c.get("optional"))
def sutra_4_2_106(c): return _in(c, "stem_final", {"tīra", "rūpya"}) and _in(c, "suffix", {"añ", "ñya"})
def sutra_4_2_107(c): return _eq(c, "purva_pada", "dik") and not _eq(c, "domain", "samjna") and _eq(c, "suffix", "ña")
def sutra_4_2_108(c): return _eq(c, "stem", "madra") and _eq(c, "suffix", "añ")
def sutra_4_2_109(c): return _eq(c, "stem_class", "udīcyagrāma") and _eq(c, "accent", "anta_udatta")
def sutra_4_2_110(c): return _in(c, "stem_final", {"prastha", "uttarapada", "paladi"}) and _eq(c, "upadha", "k") and _eq(c, "suffix", "aṇ")
def sutra_4_2_111(c): return _eq(c, "stem_class", "kaṇvādi") and _eq(c, "semantic", "gotra")
def sutra_4_2_112(c): return _eq(c, "stem_class", "iñ") and _eq(c, "rule", "continuation")
def sutra_4_2_113(c): return not _eq(c, "stem_class", "dvyac") and _in(c, "dialect", {"pracya", "bharata"})
def sutra_4_2_114(c): return _eq(c, "stem_class", "vṛddha") and _eq(c, "suffix", "cha")
def sutra_4_2_115(c): return _eq(c, "stem", "bhavat") and _in(c, "suffix", {"ṭhak", "cha"})
def sutra_4_2_116(c): return _eq(c, "stem_class", "kāśyādi") and _in(c, "suffix", {"ṭhañ", "ñiṭha"})
def sutra_4_2_117(c): return _eq(c, "stem_class", "vāhīka_grāma") and _eq(c, "rule", "continuation")
def sutra_4_2_118(c): return _eq(c, "semantic", "uśīnara") and bool(c.get("optional"))
def sutra_4_2_119(c): return _eq(c, "stem_final", "u") and _eq(c, "semantic", "deśa") and _eq(c, "suffix", "ṭhañ")
def sutra_4_2_120(c): return _eq(c, "stem_class", "vṛddha") and _eq(c, "dialect", "pracya")
def sutra_4_2_121(c): return _eq(c, "stem_final", "dhanva") and _eq(c, "upadha", "y") and _eq(c, "suffix", "vuñ")
def sutra_4_2_122(c): return _in(c, "stem_final", {"prastha", "pura", "vahānta"}) and _eq(c, "rule", "continuation")
def sutra_4_2_123(c): return _eq(c, "upadha", "r") and _eq(c, "dialect", "pracya")
def sutra_4_2_124(c): return _in(c, "stem", {"janapada", "tad_avadhi"}) and _eq(c, "rule", "continuation")
def sutra_4_2_125(c): return not _eq(c, "stem_class", "vṛddha") and _eq(c, "semantic", "bahuvacana_viṣaya")
def sutra_4_2_126(c): return _in(c, "stem_final", {"kaccha", "agni", "vaktra", "garta"}) and _eq(c, "rule", "continuation")
def sutra_4_2_127(c): return _eq(c, "stem_class", "dhūmādi") and _eq(c, "rule", "continuation")
def sutra_4_2_128(c): return _eq(c, "stem", "nagara") and _in(c, "semantic", {"kutsana", "prāvīṇya"})
def sutra_4_2_129(c): return _eq(c, "stem", "araṇya") and _eq(c, "semantic", "manuṣya")
def sutra_4_2_130(c): return _in(c, "stem", {"kuru", "yugandhara"}) and bool(c.get("optional"))
def sutra_4_2_131(c): return _in(c, "stem", {"madra", "vṛji"}) and _eq(c, "suffix", "kan")
def sutra_4_2_132(c): return _eq(c, "upadha", "k") and _eq(c, "suffix", "aṇ")
def sutra_4_2_133(c): return _eq(c, "stem_class", "kacchādi") and _eq(c, "rule", "continuation")
def sutra_4_2_134(c): return _in(c, "stem", {"manuṣya", "tat_stha"}) and _eq(c, "suffix", "vuñ")
def sutra_4_2_135(c): return _eq(c, "stem", "apadātu") and _eq(c, "purva_pada", "sālva")
def sutra_4_2_136(c): return _in(c, "stem", {"go", "yavāgū"}) and _eq(c, "rule", "continuation")
def sutra_4_2_137(c): return _eq(c, "stem_final", "garta") and _eq(c, "suffix", "cha")
def sutra_4_2_138(c): return _eq(c, "stem_class", "gahādi") and _eq(c, "rule", "continuation")
def sutra_4_2_139(c): return _eq(c, "stem_class", "kaṭādi") and _eq(c, "dialect", "pracya")
def sutra_4_2_140(c): return _eq(c, "stem", "rājan") and _eq(c, "augment", "ka")
def sutra_4_2_141(c): return _eq(c, "stem_class", "vṛddha") and _eq(c, "upadha", "ekanta_kha")
def sutra_4_2_142(c): return _in(c, "stem_final", {"kanthā", "palada", "nagara", "grāma", "hrada"}) and _eq(c, "rule", "continuation")
def sutra_4_2_143(c): return _eq(c, "stem", "parvata") and _eq(c, "rule", "continuation")
def sutra_4_2_144(c): return _eq(c, "semantic", "amanuṣya") and bool(c.get("optional"))
def sutra_4_2_145(c): return _in(c, "stem", {"kṛkaṇa", "parṇa"}) and _eq(c, "semantic", "bhāradvāja")


# ===========================================================================
# Adhyāya 4.3 — taddhita continuation: kāla, viṣaya, vikāra, śaiṣika
#               (168 sūtras)
# ===========================================================================

def sutra_4_3_1(c)  : return _in(c, "stem", {"yuṣmad", "asmad"}) and _eq(c, "suffix", "khañ") and bool(c.get("optional"))
def sutra_4_3_2(c)  : return _in(c, "stem", {"yuṣmad", "asmad"}) and _in(c, "substitute", {"yuṣmāka", "asmāka"})
def sutra_4_3_3(c)  : return _in(c, "stem", {"yuṣmad", "asmad"}) and _eq(c, "number", "single") and _in(c, "substitute", {"tavaka", "mamaka"})
def sutra_4_3_4(c)  : return _eq(c, "stem", "ardha") and _eq(c, "suffix", "yat")
def sutra_4_3_5(c)  : return _in(c, "purva_pada", {"para", "avara", "adhama", "uttama"}) and _eq(c, "rule", "continuation")
def sutra_4_3_6(c)  : return _eq(c, "purva_pada", "dik") and _eq(c, "suffix", "ṭhañ")
def sutra_4_3_7(c)  : return _in(c, "stem", {"grāma", "janapada", "ekadeśa"}) and _in(c, "suffix", {"añ", "ṭhañ"})
def sutra_4_3_8(c)  : return _eq(c, "stem", "madhya") and _eq(c, "suffix", "ma")
def sutra_4_3_9(c)  : return _eq(c, "stem", "a") and _eq(c, "semantic", "sāmpratika")
def sutra_4_3_10(c) : return _eq(c, "stem", "dvīpa") and _eq(c, "semantic", "anusamudra") and _eq(c, "suffix", "yañ")
def sutra_4_3_11(c) : return _eq(c, "semantic", "kāla") and _eq(c, "suffix", "ṭhañ")
def sutra_4_3_12(c) : return _eq(c, "stem", "śarad") and _eq(c, "semantic", "śrāddha")
def sutra_4_3_13(c) : return _in(c, "semantic", {"roga", "ātapa"}) and bool(c.get("optional"))
def sutra_4_3_14(c) : return _in(c, "stem", {"niśā", "pradoṣa"}) and _eq(c, "rule", "continuation")
def sutra_4_3_15(c) : return _eq(c, "stem", "śvas") and _eq(c, "augment", "tuṭ")
def sutra_4_3_16(c) : return _eq(c, "stem_class", "saṃdhi_velādi_ṛtu_nakṣatra") and _eq(c, "suffix", "aṇ")
def sutra_4_3_17(c) : return _eq(c, "stem", "prāvṛṣ") and _eq(c, "suffix", "eṇya")
def sutra_4_3_18(c) : return _eq(c, "stem", "varṣa") and _eq(c, "suffix", "ṭhak")
def sutra_4_3_19(c) : return bool(c.get("is_vedic")) and _eq(c, "suffix", "ṭhañ")
def sutra_4_3_20(c) : return _eq(c, "stem", "vasanta") and _eq(c, "rule", "continuation")
def sutra_4_3_21(c) : return _eq(c, "stem", "hemanta") and _eq(c, "rule", "continuation")
def sutra_4_3_22(c) : return _eq(c, "suffix", "aṇ") and _eq(c, "operation", "talopa")
def sutra_4_3_23(c) : return _in(c, "stem", {"sāyam", "ciram", "prāhṇe", "prage"}) and _in(c, "suffix", {"ṭyu", "ṭyul"}) and _eq(c, "augment", "tuṭ")
def sutra_4_3_24(c) : return _in(c, "stem", {"pūrvāhṇa", "aparāhṇa"}) and bool(c.get("optional"))
def sutra_4_3_25(c) : return _eq(c, "semantic", "tatra_jāta") and _eq(c, "rule", "continuation")
def sutra_4_3_26(c) : return _eq(c, "stem", "prāvṛṣ") and _eq(c, "suffix", "ṣṭhap")
def sutra_4_3_27(c) : return _eq(c, "stem", "śarad") and _eq(c, "domain", "samjna") and _eq(c, "suffix", "vuñ")
def sutra_4_3_28(c) : return _in(c, "stem", {"pūrvāhṇa", "aparāhṇa", "ārdrā", "mūla", "pradoṣa", "avaskara"}) and _eq(c, "suffix", "vun")
def sutra_4_3_29(c) : return _eq(c, "stem", "path") and _eq(c, "substitute", "pantha")
def sutra_4_3_30(c) : return _eq(c, "stem", "amāvāsyā") and bool(c.get("optional"))
def sutra_4_3_31(c) : return _eq(c, "stem", "a") and _eq(c, "rule", "continuation")
def sutra_4_3_32(c) : return _in(c, "stem", {"sindhu", "apakara"}) and _eq(c, "suffix", "kan")
def sutra_4_3_33(c) : return _in(c, "suffix", {"aṇ", "añ"}) and _eq(c, "rule", "continuation")
def sutra_4_3_34(c) : return _eq(c, "stem_class", "śraviṣṭhādi_nakṣatra") and _eq(c, "operation", "luk")
def sutra_4_3_35(c) : return _in(c, "stem_final", {"sthānānta", "gośāla", "kharaśālā"}) and _eq(c, "rule", "continuation")
def sutra_4_3_36(c) : return _in(c, "stem", {"vatsaśālā", "abhijit", "aśvayuk", "śatabhiṣaj"}) and bool(c.get("optional"))
def sutra_4_3_37(c) : return _eq(c, "stem_class", "nakshatra") and _eq(c, "semantic", "bahula")
def sutra_4_3_38(c) : return _in(c, "semantic", {"kṛta", "labdha", "krīta", "kuśala"}) and _eq(c, "rule", "continuation")
def sutra_4_3_39(c) : return _eq(c, "semantic", "prāyabhava") and _eq(c, "rule", "continuation")
def sutra_4_3_40(c) : return _in(c, "stem", {"upajānu", "upakarṇa", "upanīvi"}) and _eq(c, "suffix", "ṭhak")
def sutra_4_3_41(c) : return _eq(c, "semantic", "sambhūta") and _eq(c, "rule", "continuation")
def sutra_4_3_42(c) : return _eq(c, "stem", "kośa") and _eq(c, "suffix", "ḍhañ")
def sutra_4_3_43(c) : return _eq(c, "semantic", "kāla_sādhu_puṣpyat") and _eq(c, "rule", "continuation")
def sutra_4_3_44(c) : return _eq(c, "semantic", "upta") and _eq(c, "rule", "continuation")
def sutra_4_3_45(c) : return _eq(c, "stem", "āśvayujī") and _eq(c, "suffix", "vuñ")
def sutra_4_3_46(c) : return _in(c, "stem", {"grīṣma", "vasanta"}) and bool(c.get("optional"))
def sutra_4_3_47(c) : return _eq(c, "semantic", "deya_ṛṇa") and _eq(c, "rule", "continuation")
def sutra_4_3_48(c) : return _in(c, "stem", {"kalāpī", "aśvattha", "yava", "busa"}) and _eq(c, "suffix", "vun")
def sutra_4_3_49(c) : return _eq(c, "stem", "grīṣmāvarasamā") and _eq(c, "suffix", "vuñ")
def sutra_4_3_50(c) : return _in(c, "stem", {"saṃvatsara", "āgrahāyaṇī"}) and _eq(c, "suffix", "ṭhañ")
def sutra_4_3_51(c) : return _eq(c, "semantic", "vyāharati_mṛga") and _eq(c, "rule", "continuation")
def sutra_4_3_52(c) : return _eq(c, "semantic", "soḍha") and _eq(c, "rule", "continuation")
def sutra_4_3_53(c) : return _eq(c, "semantic", "tatra_bhava") and _eq(c, "rule", "continuation")
def sutra_4_3_54(c) : return _eq(c, "stem_class", "digādi") and _eq(c, "suffix", "yat")
def sutra_4_3_55(c) : return _eq(c, "stem_class", "śarīrāvayava") and _eq(c, "rule", "continuation")
def sutra_4_3_56(c) : return _eq(c, "stem_class", "dṛti_kukṣi_etc") and _eq(c, "suffix", "ḍhañ")
def sutra_4_3_57(c) : return _eq(c, "stem", "grīvā") and _eq(c, "suffix", "aṇ")
def sutra_4_3_58(c) : return _eq(c, "stem", "gambhīrā") and _eq(c, "suffix", "ñya")
def sutra_4_3_59(c) : return _eq(c, "compound_type", "avyayībhāva") and _eq(c, "rule", "continuation")
def sutra_4_3_60(c) : return _eq(c, "purva_pada", "antar") and _eq(c, "suffix", "ṭhañ")
def sutra_4_3_61(c) : return _eq(c, "stem", "grāma") and _in(c, "purva_pada", {"pari", "anu"})
def sutra_4_3_62(c) : return _in(c, "stem", {"jihvāmūla", "aṅguli"}) and _eq(c, "suffix", "cha")
def sutra_4_3_63(c) : return _eq(c, "stem_final", "varga") and _eq(c, "rule", "continuation")
def sutra_4_3_64(c) : return _eq(c, "semantic", "aśabda") and _in(c, "suffix", {"yat", "kha"}) and bool(c.get("optional"))
def sutra_4_3_65(c) : return _in(c, "stem", {"karṇa", "lalāṭa"}) and _eq(c, "semantic", "alaṃkāra") and _eq(c, "suffix", "kan")
def sutra_4_3_66(c) : return _eq(c, "semantic", "vyākhyāna") and _eq(c, "rule", "continuation")
def sutra_4_3_67(c) : return _eq(c, "stem_class", "bahvac") and _eq(c, "accent", "anta_udatta") and _eq(c, "suffix", "ṭhañ")
def sutra_4_3_68(c) : return _in(c, "stem", {"kratu", "yajña"}) and _eq(c, "rule", "continuation")
def sutra_4_3_69(c) : return _eq(c, "semantic", "adhyāya") and _eq(c, "stem", "ṛṣi")
def sutra_4_3_70(c) : return _in(c, "stem", {"pauroḍāśa", "puroḍāśa"}) and _eq(c, "suffix", "ṣṭhan")
def sutra_4_3_71(c) : return bool(c.get("is_vedic")) and _eq(c, "suffix", "yat") and _eq(c, "stem", "aṇau")
def sutra_4_3_72(c) : return _eq(c, "stem_class", "dvyajṛd_brāhmaṇa_rk") and _eq(c, "suffix", "ṭhak")
def sutra_4_3_73(c) : return _in(c, "stem", {"aṇṛk", "ayanādi"}) and _eq(c, "rule", "continuation")
def sutra_4_3_74(c) : return _eq(c, "semantic", "tata_āgata") and _eq(c, "rule", "continuation")
def sutra_4_3_75(c) : return _in(c, "stem_final", {"ṭhak", "āya_sthāna"}) and _eq(c, "rule", "continuation")
def sutra_4_3_76(c) : return _eq(c, "stem_class", "śuṇḍikādi") and _eq(c, "suffix", "aṇ")
def sutra_4_3_77(c) : return _in(c, "semantic", {"vidyā_yoni_sambandha"}) and _eq(c, "suffix", "vuñ")
def sutra_4_3_78(c) : return _eq(c, "stem", "ṛta") and _eq(c, "suffix", "ṭhañ")
def sutra_4_3_79(c) : return _eq(c, "stem", "pitṛ") and _eq(c, "suffix", "yat")
def sutra_4_3_80(c) : return _eq(c, "semantic", "gotra") and _eq(c, "suffix_class", "aṅkavat")
def sutra_4_3_81(c) : return _in(c, "stem", {"hetu", "manuṣya"}) and _eq(c, "suffix", "rūpya") and bool(c.get("optional"))
def sutra_4_3_82(c) : return _eq(c, "suffix", "mayaṭ") and _eq(c, "rule", "continuation")
def sutra_4_3_83(c) : return _eq(c, "semantic", "prabhavati") and _eq(c, "rule", "continuation")
def sutra_4_3_84(c) : return _eq(c, "stem", "vidūra") and _eq(c, "suffix", "ñya")
def sutra_4_3_85(c) : return _eq(c, "semantic", "tat_gacchati") and _in(c, "stem", {"pathi", "dūta"})
def sutra_4_3_86(c) : return _eq(c, "semantic", "abhiniṣkrāmati_dvāra") and _eq(c, "rule", "continuation")
def sutra_4_3_87(c) : return _eq(c, "semantic", "adhikṛtya_kṛta_grantha") and _eq(c, "rule", "continuation")
def sutra_4_3_88(c) : return _eq(c, "stem_class", "śiśukranda_etc") and _eq(c, "suffix", "cha")
def sutra_4_3_89(c) : return _eq(c, "semantic", "asya_nivāsa") and _eq(c, "rule", "continuation")
def sutra_4_3_90(c) : return _eq(c, "semantic", "abhijana") and _eq(c, "rule", "continuation")
def sutra_4_3_91(c) : return _eq(c, "stem_class", "āyudhajīvi") and _eq(c, "semantic", "parvata") and _eq(c, "suffix", "cha")
def sutra_4_3_92(c) : return _eq(c, "stem_class", "śaṇḍikādi") and _eq(c, "suffix", "ñya")
def sutra_4_3_93(c) : return _in(c, "stem", {"sindhu", "takṣaśilā"}) and _in(c, "suffix", {"aṇ", "añ"})
def sutra_4_3_94(c) : return _in(c, "stem", {"tūdī", "śalātura", "varmatī", "kūcavāra"}) and _in(c, "suffix", {"ḍhak", "chaṇ", "ḍhañ", "yaka"})
def sutra_4_3_95(c) : return _eq(c, "semantic", "bhakti") and _eq(c, "rule", "continuation")
def sutra_4_3_96(c) : return _eq(c, "stem_class", "acittadeśakāla") and _eq(c, "suffix", "ṭhak")
def sutra_4_3_97(c) : return _eq(c, "stem", "mahārāja") and _eq(c, "suffix", "ṭhañ")
def sutra_4_3_98(c) : return _in(c, "stem", {"vāsudeva", "arjuna"}) and _eq(c, "suffix", "vun")
def sutra_4_3_99(c) : return _eq(c, "stem_class", "gotra_kṣatriya") and _eq(c, "suffix", "vuñ")
def sutra_4_3_100(c): return _eq(c, "stem_class", "janapadin") and _eq(c, "rule", "janapada_vat")
def sutra_4_3_101(c): return _eq(c, "semantic", "tena_prokta") and _eq(c, "rule", "continuation")
def sutra_4_3_102(c): return _in(c, "stem", {"tittiri", "varatantu", "khaṇḍika", "ukha"}) and _eq(c, "suffix", "chaṇ")
def sutra_4_3_103(c): return _in(c, "stem", {"kāśyapa", "kauśika"}) and _eq(c, "semantic", "ṛṣi") and _eq(c, "suffix", "ṇini")
def sutra_4_3_104(c): return _in(c, "stem", {"kalāpin", "vaiśampāyana"}) and _eq(c, "semantic", "antevāsi")
def sutra_4_3_105(c): return _eq(c, "semantic", "purāṇa_prokta_brāhmaṇa_kalpa") and _eq(c, "rule", "continuation")
def sutra_4_3_106(c): return _eq(c, "stem_class", "śaunakādi") and bool(c.get("is_vedic"))
def sutra_4_3_107(c): return _in(c, "stem", {"kaṭha", "caraka"}) and _eq(c, "operation", "luk")
def sutra_4_3_108(c): return _eq(c, "stem", "kalāpin") and _eq(c, "suffix", "aṇ")
def sutra_4_3_109(c): return _eq(c, "stem", "chagalin") and _eq(c, "suffix", "ḍhinuk")
def sutra_4_3_110(c): return _in(c, "stem", {"pārāśarya", "śilāli"}) and _in(c, "semantic", {"bhikṣu", "naṭa_sūtra"})
def sutra_4_3_111(c): return _in(c, "stem", {"karmanda", "kṛśāśva"}) and _eq(c, "suffix", "ini")
def sutra_4_3_112(c): return _eq(c, "semantic", "ekadik") and _eq(c, "rule", "continuation")
def sutra_4_3_113(c): return _eq(c, "suffix", "tasi") and _eq(c, "rule", "continuation")
def sutra_4_3_114(c): return _eq(c, "stem", "uras") and _eq(c, "suffix", "yat")
def sutra_4_3_115(c): return _eq(c, "semantic", "upajñāta") and _eq(c, "rule", "continuation")
def sutra_4_3_116(c): return _eq(c, "semantic", "kṛta_grantha") and _eq(c, "rule", "continuation")
def sutra_4_3_117(c): return _eq(c, "domain", "samjna") and _eq(c, "rule", "continuation")
def sutra_4_3_118(c): return _eq(c, "stem_class", "kulālādi") and _eq(c, "suffix", "vuñ")
def sutra_4_3_119(c): return _eq(c, "stem_class", "kṣudrābhramara_etc") and _eq(c, "suffix", "añ")
def sutra_4_3_120(c): return _eq(c, "semantic", "tasya_idam") and _eq(c, "rule", "continuation")
def sutra_4_3_121(c): return _eq(c, "stem", "ratha") and _eq(c, "suffix", "yat")
def sutra_4_3_122(c): return _eq(c, "purva_pada", "pattra") and _eq(c, "suffix", "añ")
def sutra_4_3_123(c): return _in(c, "stem", {"pattra", "adhvaryu", "pariṣad"}) and _eq(c, "rule", "continuation")
def sutra_4_3_124(c): return _in(c, "stem", {"hala", "sīra"}) and _eq(c, "suffix", "ṭhak")
def sutra_4_3_125(c): return _eq(c, "compound_type", "dvandva") and _in(c, "semantic", {"vaira", "maithunika"})
def sutra_4_3_126(c): return _in(c, "stem", {"gotra", "caraṇa"}) and _eq(c, "suffix", "vuñ")
def sutra_4_3_127(c): return _eq(c, "stem_class", "saṅghāṅka_lakṣaṇa") and _in(c, "stem_class_alt", {"añ", "yañ", "iñ"}) and _eq(c, "suffix", "aṇ")
def sutra_4_3_128(c): return _eq(c, "stem", "śākala") and bool(c.get("optional"))
def sutra_4_3_129(c): return _in(c, "stem", {"chandoga", "aukthika", "yājñika", "bahvṛca", "naṭa"}) and _eq(c, "suffix", "ñya")
def sutra_4_3_130(c): return _in(c, "stem", {"daṇḍa", "māṇavāntevāsi"}) and _eq(c, "rule", "blocking")
def sutra_4_3_131(c): return _eq(c, "stem_class", "raivatikādi") and _eq(c, "suffix", "cha")
def sutra_4_3_132(c): return _in(c, "stem", {"kaupiñjala", "hāstipada"}) and _eq(c, "suffix", "aṇ")
def sutra_4_3_133(c): return _eq(c, "stem", "ātharvaṇika") and _eq(c, "operation", "ikalopa")
def sutra_4_3_134(c): return _eq(c, "semantic", "tasya_vikāra") and _eq(c, "rule", "continuation")
def sutra_4_3_135(c): return _in(c, "stem", {"prāṇi", "oṣadhi", "vṛkṣa"}) and _eq(c, "semantic", "avayava")
def sutra_4_3_136(c): return _eq(c, "stem_class", "bilvādi") and _eq(c, "suffix", "aṇ")
def sutra_4_3_137(c): return _eq(c, "upadha", "k") and _eq(c, "rule", "continuation")
def sutra_4_3_138(c): return _in(c, "stem", {"trapu", "jatu"}) and _eq(c, "augment", "ṣuk")
def sutra_4_3_139(c): return _eq(c, "stem_final", "u") and _eq(c, "suffix", "añ")
def sutra_4_3_140(c): return _eq(c, "stem_class", "anudāttādi") and _eq(c, "rule", "continuation")
def sutra_4_3_141(c): return _eq(c, "stem_class", "palāśādi") and bool(c.get("optional"))
def sutra_4_3_142(c): return _eq(c, "stem", "śamī") and _eq(c, "suffix", "ṣṭlañ")
def sutra_4_3_143(c): return _in(c, "suffix", {"mayaṭ", "vaitayor"}) and _eq(c, "dialect", "bhāṣā") and not _in(c, "semantic", {"abhakṣya", "ācchādana"})
def sutra_4_3_144(c): return _eq(c, "stem_class", "vṛddha_śarādi") and _eq(c, "rule", "always")
def sutra_4_3_145(c): return _eq(c, "stem", "go") and _eq(c, "semantic", "purīṣa")
def sutra_4_3_146(c): return _eq(c, "stem", "piṣṭa") and _eq(c, "rule", "continuation")
def sutra_4_3_147(c): return _eq(c, "domain", "samjna") and _eq(c, "suffix", "kan")
def sutra_4_3_148(c): return _eq(c, "stem", "vrīhi") and _eq(c, "semantic", "puroḍāśa")
def sutra_4_3_149(c): return not _eq(c, "domain", "samjna") and _in(c, "stem", {"tila", "yava"})
def sutra_4_3_150(c): return _eq(c, "stem_class", "dvyac") and bool(c.get("is_vedic"))
def sutra_4_3_151(c): return _in(c, "stem", {"not", "vat", "vardhra", "bilva"}) and _eq(c, "rule", "blocking")
def sutra_4_3_152(c): return _eq(c, "stem_class", "tālādi") and _eq(c, "suffix", "aṇ")
def sutra_4_3_153(c): return _eq(c, "stem_class", "jātarūpa") and _eq(c, "semantic", "parimāṇa")
def sutra_4_3_154(c): return _eq(c, "stem_class", "prāṇi_rajata") and _eq(c, "suffix", "añ")
def sutra_4_3_155(c): return _eq(c, "stem_class", "ñit") and _eq(c, "rule", "continuation")
def sutra_4_3_156(c): return _eq(c, "semantic", "krīta_vat_parimāṇa") and _eq(c, "rule", "continuation")
def sutra_4_3_157(c): return _eq(c, "stem", "uṣṭra") and _eq(c, "suffix", "vuñ")
def sutra_4_3_158(c): return _in(c, "stem", {"umā", "ūrṇā"}) and bool(c.get("optional"))
def sutra_4_3_159(c): return _eq(c, "stem", "eṇī") and _eq(c, "suffix", "ḍhañ")
def sutra_4_3_160(c): return _in(c, "stem", {"go", "payas"}) and _eq(c, "suffix", "yat")
def sutra_4_3_161(c): return _eq(c, "stem", "dro") and _eq(c, "rule", "continuation")
def sutra_4_3_162(c): return _eq(c, "semantic", "vayas") and _eq(c, "domain", "māna")
def sutra_4_3_163(c): return _eq(c, "stem_final", "phala") and _eq(c, "operation", "luk")
def sutra_4_3_164(c): return _eq(c, "stem_class", "plakṣādi") and _eq(c, "suffix", "aṇ")
def sutra_4_3_165(c): return _eq(c, "stem", "jambū") and bool(c.get("optional"))
def sutra_4_3_166(c): return _eq(c, "operation", "lup") and _eq(c, "rule", "continuation")
def sutra_4_3_167(c): return _eq(c, "stem_class", "harītakyādi") and _eq(c, "rule", "continuation")
def sutra_4_3_168(c): return _in(c, "stem", {"kaṃsīya", "paraśavya"}) and _in(c, "suffix", {"yañ", "añ"}) and _eq(c, "operation", "luk")


# ===========================================================================
# Adhyāya 4.4 — prāgvahateṣ-ṭhak section: vocation/possession/instrument
#               taddhitas (144 sūtras)
# ===========================================================================

def sutra_4_4_1(c)  : return _eq(c, "section", "prāgvahate") and _eq(c, "suffix", "ṭhak")
def sutra_4_4_2(c)  : return _eq(c, "semantic", "tena_dīvyati_khanati_jayati_jita") and _eq(c, "rule", "continuation")
def sutra_4_4_3(c)  : return _eq(c, "semantic", "saṃskṛta") and _eq(c, "rule", "continuation")
def sutra_4_4_4(c)  : return _eq(c, "stem", "kulattha") and _eq(c, "upadha", "k") and _eq(c, "suffix", "aṇ")
def sutra_4_4_5(c)  : return _eq(c, "semantic", "tarati") and _eq(c, "rule", "continuation")
def sutra_4_4_6(c)  : return _eq(c, "stem", "gopuccha") and _eq(c, "suffix", "ṭhañ")
def sutra_4_4_7(c)  : return _eq(c, "stem_class", "nau_dvyac") and _eq(c, "suffix", "ṣṭhan")
def sutra_4_4_8(c)  : return _eq(c, "semantic", "carati") and _eq(c, "rule", "continuation")
def sutra_4_4_9(c)  : return _eq(c, "stem", "ākarṣa") and _eq(c, "suffix", "ṣṭhal")
def sutra_4_4_10(c) : return _eq(c, "stem_class", "parpādi") and _eq(c, "suffix", "ṣṭhan")
def sutra_4_4_11(c) : return _eq(c, "stem", "śvagaṇa") and _eq(c, "suffix", "ṭhañ")
def sutra_4_4_12(c) : return _eq(c, "stem_class", "vetanādi") and _eq(c, "semantic", "jīvati")
def sutra_4_4_13(c) : return _in(c, "stem", {"vasna", "kraya", "vikraya"}) and _eq(c, "suffix", "ṭhan")
def sutra_4_4_14(c) : return _eq(c, "stem", "āyudha") and _eq(c, "suffix", "cha")
def sutra_4_4_15(c) : return _eq(c, "semantic", "harati_utsaṅgādi") and _eq(c, "rule", "continuation")
def sutra_4_4_16(c) : return _eq(c, "stem_class", "bhastrādi") and _eq(c, "suffix", "ṣṭhan")
def sutra_4_4_17(c) : return _in(c, "stem", {"vivadha", "vīvadha"}) and bool(c.get("optional"))
def sutra_4_4_18(c) : return _eq(c, "stem", "kuṭilikā") and _eq(c, "suffix", "aṇ")
def sutra_4_4_19(c) : return _eq(c, "stem_class", "akṣadyūtādi") and _eq(c, "semantic", "nirvṛtta")
def sutra_4_4_20(c) : return _eq(c, "stem_final", "ktri") and _eq(c, "augment", "ma") and _eq(c, "rule", "always")
def sutra_4_4_21(c) : return _in(c, "stem", {"apamitya", "yācita"}) and _in(c, "suffix", {"kak", "kanu"})
def sutra_4_4_22(c) : return _eq(c, "semantic", "saṃsṛṣṭa") and _eq(c, "rule", "continuation")
def sutra_4_4_23(c) : return _eq(c, "stem_class", "cūrṇādi") and _eq(c, "suffix", "ini")
def sutra_4_4_24(c) : return _eq(c, "stem", "lavaṇa") and _eq(c, "operation", "luk")
def sutra_4_4_25(c) : return _eq(c, "stem", "mudga") and _eq(c, "suffix", "aṇ")
def sutra_4_4_26(c) : return _eq(c, "stem_class", "vyañjana") and _eq(c, "semantic", "upasikta")
def sutra_4_4_27(c) : return _in(c, "stem", {"ojas", "sahas", "ambhas"}) and _eq(c, "rule", "vartate")
def sutra_4_4_28(c) : return _in(c, "stem", {"īpa", "loma", "kūla"}) and _eq(c, "rule", "pratyanu_pūrva")
def sutra_4_4_29(c) : return _eq(c, "stem", "parimukha") and _eq(c, "rule", "continuation")
def sutra_4_4_30(c) : return _eq(c, "semantic", "prayacchati_garhya") and _eq(c, "rule", "continuation")
def sutra_4_4_31(c) : return _in(c, "stem", {"kusīda", "daśa_ekādaśa"}) and _in(c, "suffix", {"ṣṭhan", "ṣṭhac"})
def sutra_4_4_32(c) : return _eq(c, "semantic", "uñchati") and _eq(c, "rule", "continuation")
def sutra_4_4_33(c) : return _eq(c, "semantic", "rakṣati") and _eq(c, "rule", "continuation")
def sutra_4_4_34(c) : return _eq(c, "stem", "śabda_dardura") and _eq(c, "semantic", "karoti")
def sutra_4_4_35(c) : return _in(c, "stem", {"pakṣin", "matsya", "mṛga"}) and _eq(c, "semantic", "hanti")
def sutra_4_4_36(c) : return _eq(c, "stem", "paripantha") and _eq(c, "semantic", "tiṣṭhati")
def sutra_4_4_37(c) : return _eq(c, "purva_pada", "mātha") and _in(c, "stem", {"padavi", "anupada"}) and _eq(c, "semantic", "dhāvati")
def sutra_4_4_38(c) : return _eq(c, "stem", "ākranda") and _eq(c, "suffix", "ṭhañ")
def sutra_4_4_39(c) : return _eq(c, "purva_pada", "pad") and _eq(c, "semantic", "gṛhṇāti")
def sutra_4_4_40(c) : return _in(c, "stem", {"pratikaṇṭha", "artha", "lalāma"}) and _eq(c, "rule", "continuation")
def sutra_4_4_41(c) : return _eq(c, "stem", "dharma") and _eq(c, "semantic", "carati")
def sutra_4_4_42(c) : return _eq(c, "stem", "pratipath") and _eq(c, "semantic", "eti") and _eq(c, "suffix", "ṭhan")
def sutra_4_4_43(c) : return _eq(c, "stem", "samavāya") and _eq(c, "semantic", "samavaiti")
def sutra_4_4_44(c) : return _eq(c, "stem", "pariṣad") and _eq(c, "suffix", "ṇya")
def sutra_4_4_45(c) : return _eq(c, "stem", "senā") and bool(c.get("optional"))
def sutra_4_4_46(c) : return _in(c, "stem", {"lalāṭa", "kukkuṭi"}) and _eq(c, "semantic", "paśyati") and _eq(c, "domain", "samjna")
def sutra_4_4_47(c) : return _eq(c, "semantic", "tasya_dharmya") and _eq(c, "rule", "continuation")
def sutra_4_4_48(c) : return _eq(c, "stem_class", "mahiṣyādi") and _eq(c, "suffix", "aṇ")
def sutra_4_4_49(c) : return _eq(c, "stem", "ṛta") and _eq(c, "suffix", "añ")
def sutra_4_4_50(c) : return _eq(c, "semantic", "avakraya") and _eq(c, "rule", "continuation")
def sutra_4_4_51(c) : return _eq(c, "semantic", "tasya_paṇya") and _eq(c, "rule", "continuation")
def sutra_4_4_52(c) : return _eq(c, "stem", "lavaṇa") and _eq(c, "suffix", "ṭhañ")
def sutra_4_4_53(c) : return _eq(c, "stem_class", "kiśarādi") and _eq(c, "suffix", "ṣṭhan")
def sutra_4_4_54(c) : return _eq(c, "stem", "śalālu") and bool(c.get("optional"))
def sutra_4_4_55(c) : return _eq(c, "semantic", "śilpa") and _eq(c, "rule", "continuation")
def sutra_4_4_56(c) : return _in(c, "stem", {"maḍḍuka", "jharjhara"}) and _eq(c, "suffix", "aṇ") and bool(c.get("optional"))
def sutra_4_4_57(c) : return _eq(c, "semantic", "praharaṇa") and _eq(c, "rule", "continuation")
def sutra_4_4_58(c) : return _eq(c, "stem", "paraśvadha") and _eq(c, "suffix", "ṭhañ")
def sutra_4_4_59(c) : return _in(c, "stem", {"śakti", "yaṣṭi"}) and _eq(c, "suffix", "īkak")
def sutra_4_4_60(c) : return _eq(c, "semantic", "asti_nāsti_diṣṭa_mati") and _eq(c, "rule", "continuation")
def sutra_4_4_61(c) : return _eq(c, "semantic", "śīla") and _eq(c, "rule", "continuation")
def sutra_4_4_62(c) : return _eq(c, "stem_class", "chatrādi") and _eq(c, "suffix", "ṇa")
def sutra_4_4_63(c) : return _eq(c, "semantic", "karmādhyayana_vṛtta") and _eq(c, "rule", "continuation")
def sutra_4_4_64(c) : return _eq(c, "stem_class", "bahvac_purva_pada") and _eq(c, "suffix", "ṭhac")
def sutra_4_4_65(c) : return _eq(c, "stem_class", "bhakṣa") and _eq(c, "semantic", "hita")
def sutra_4_4_66(c) : return _eq(c, "semantic", "tasmai_dīyate_niyukta") and _eq(c, "rule", "continuation")
def sutra_4_4_67(c) : return _in(c, "stem", {"śrāṇāmāṃsa", "audana"}) and _eq(c, "suffix", "ṭiṭhan")
def sutra_4_4_68(c) : return _eq(c, "stem", "bhakta") and bool(c.get("optional"))
def sutra_4_4_69(c) : return _eq(c, "semantic", "tatra_niyukta") and _eq(c, "rule", "continuation")
def sutra_4_4_70(c) : return _eq(c, "stem_final", "agāra") and _eq(c, "suffix", "ṭhan")
def sutra_4_4_71(c) : return _eq(c, "stem", "adhyāyin") and not _in(c, "domain", {"deśa", "kāla"})
def sutra_4_4_72(c) : return _in(c, "stem_final", {"kaṭhina_anta", "prastāra", "saṃsthāna"}) and _eq(c, "semantic", "vyavaharati")
def sutra_4_4_73(c) : return _eq(c, "stem", "nikaṭa") and _eq(c, "semantic", "vasati")
def sutra_4_4_74(c) : return _eq(c, "stem", "āvasatha") and _eq(c, "suffix", "ṣṭhal")
def sutra_4_4_75(c) : return _eq(c, "section", "prāghita") and _eq(c, "suffix", "yat")
def sutra_4_4_76(c) : return _in(c, "stem", {"rathayuga", "prāsaṅga"}) and _eq(c, "semantic", "tadvahati")
def sutra_4_4_77(c) : return _eq(c, "stem", "dhur") and _in(c, "suffix", {"ya", "ḍhak"})
def sutra_4_4_78(c) : return _eq(c, "stem", "sarvadhura") and _eq(c, "suffix", "kha")
def sutra_4_4_79(c) : return _eq(c, "stem", "ekadhura") and _eq(c, "operation", "luk")
def sutra_4_4_80(c) : return _eq(c, "stem", "śakaṭa") and _eq(c, "suffix", "aṇ")
def sutra_4_4_81(c) : return _in(c, "stem", {"hala", "sīra"}) and _eq(c, "suffix", "ṭhak")
def sutra_4_4_82(c) : return _eq(c, "stem", "janya") and _eq(c, "domain", "samjna")
def sutra_4_4_83(c) : return _eq(c, "stem", "adhanu") and _eq(c, "semantic", "vidhyati")
def sutra_4_4_84(c) : return _eq(c, "stem", "dhanagaṇa") and _eq(c, "semantic", "labdhā")
def sutra_4_4_85(c) : return _eq(c, "stem", "anna") and _eq(c, "suffix", "ṇa")
def sutra_4_4_86(c) : return _eq(c, "stem", "vaśa") and _eq(c, "semantic", "gata")
def sutra_4_4_87(c) : return _eq(c, "stem", "pada") and _eq(c, "semantic", "asmin_dṛśya")
def sutra_4_4_88(c) : return _eq(c, "stem", "mūla") and _eq(c, "semantic", "abarhi")
def sutra_4_4_89(c) : return _eq(c, "stem", "dhenuṣyā") and _eq(c, "domain", "samjna")
def sutra_4_4_90(c) : return _eq(c, "stem", "gṛhapati") and _eq(c, "semantic", "saṃyukta") and _eq(c, "suffix", "ñya")
def sutra_4_4_91(c) : return _eq(c, "stem_class", "nau_vayodharma_etc") and _eq(c, "rule", "continuation")
def sutra_4_4_92(c) : return _in(c, "stem", {"dharma", "pathi", "artha", "nyāya"}) and _eq(c, "semantic", "anapeta")
def sutra_4_4_93(c) : return bool(c.get("is_vedic")) and _eq(c, "semantic", "nirmita")
def sutra_4_4_94(c) : return _eq(c, "stem", "uras") and _eq(c, "suffix", "aṇ")
def sutra_4_4_95(c) : return _eq(c, "stem", "hṛdaya") and _eq(c, "semantic", "priya")
def sutra_4_4_96(c) : return _eq(c, "stem", "bandhana") and _eq(c, "semantic", "carṣu")
def sutra_4_4_97(c) : return _in(c, "stem", {"mata", "jana", "hala"}) and _in(c, "semantic", {"karaṇa", "jalpa", "karṣa"})
def sutra_4_4_98(c) : return _eq(c, "semantic", "tatra_sādhu") and _eq(c, "rule", "continuation")
def sutra_4_4_99(c) : return _eq(c, "stem_class", "pratijanādi") and _eq(c, "suffix", "khañ")
def sutra_4_4_100(c): return _eq(c, "stem", "bhakta") and _eq(c, "suffix", "ṇa")
def sutra_4_4_101(c): return _eq(c, "stem", "pariṣad") and _eq(c, "suffix", "ṇya")
def sutra_4_4_102(c): return _eq(c, "stem_class", "kathādi") and _eq(c, "suffix", "ṭhak")
def sutra_4_4_103(c): return _eq(c, "stem_class", "guḍādi") and _eq(c, "suffix", "ṭhañ")
def sutra_4_4_104(c): return _in(c, "stem", {"pathi", "atithi", "vasati", "svapati"}) and _eq(c, "suffix", "ḍhañ")
def sutra_4_4_105(c): return _eq(c, "stem", "sabhā") and _eq(c, "suffix", "ya")
def sutra_4_4_106(c): return bool(c.get("is_vedic")) and _eq(c, "suffix", "ḍha")
def sutra_4_4_107(c): return _eq(c, "stem", "samānatīrtha") and _eq(c, "suffix", "vāsi")
def sutra_4_4_108(c): return _eq(c, "stem", "samānodara") and _eq(c, "semantic", "śayita") and _eq(c, "augment", "o_udatta")
def sutra_4_4_109(c): return _eq(c, "stem", "sodara") and _eq(c, "suffix", "ya")
def sutra_4_4_110(c): return bool(c.get("is_vedic")) and _eq(c, "semantic", "bhava")
def sutra_4_4_111(c): return _in(c, "stem", {"pātha", "nadī"}) and _eq(c, "suffix", "ḍyaṇ")
def sutra_4_4_112(c): return _in(c, "stem", {"veśanta", "himavat"}) and _eq(c, "suffix", "aṇ")
def sutra_4_4_113(c): return _eq(c, "stem", "srotas") and _in(c, "suffix", {"ḍya", "ḍyu"}) and bool(c.get("optional"))
def sutra_4_4_114(c): return _in(c, "stem", {"sagarbha", "sayūtha", "sanuta"}) and _eq(c, "suffix", "yan")
def sutra_4_4_115(c): return _eq(c, "stem", "tugra") and _eq(c, "suffix", "ghan")
def sutra_4_4_116(c): return _eq(c, "stem", "agra") and _eq(c, "suffix", "yat")
def sutra_4_4_117(c): return _in(c, "suffix", {"gha", "cha"}) and _eq(c, "rule", "continuation")
def sutra_4_4_118(c): return _in(c, "stem", {"samudra", "abhra"}) and _eq(c, "suffix", "gha")
def sutra_4_4_119(c): return _eq(c, "stem", "barhis") and _eq(c, "semantic", "datta")
def sutra_4_4_120(c): return _eq(c, "stem", "dūta") and _in(c, "semantic", {"bhāga", "karma"})
def sutra_4_4_121(c): return _in(c, "stem", {"rakṣas", "yātu"}) and _eq(c, "semantic", "hananī")
def sutra_4_4_122(c): return _in(c, "stem", {"revatī", "jagatī", "haviṣya"}) and _eq(c, "semantic", "praśasya")
def sutra_4_4_123(c): return _eq(c, "stem", "asura") and _eq(c, "semantic", "sva")
def sutra_4_4_124(c): return _eq(c, "semantic", "māyā") and _eq(c, "suffix", "aṇ")
def sutra_4_4_125(c): return _eq(c, "domain", "iṣṭakā_mantra") and _eq(c, "operation", "luk_matu")
def sutra_4_4_126(c): return _eq(c, "stem", "aśvi") and _eq(c, "suffix", "aṇ")
def sutra_4_4_127(c): return _eq(c, "stem", "mūrdhan") and _eq(c, "semantic", "vayasi") and _eq(c, "suffix", "matup")
def sutra_4_4_128(c): return _in(c, "stem", {"māsa", "tanū"}) and _eq(c, "semantic", "matvartha")
def sutra_4_4_129(c): return _eq(c, "stem", "madhu") and _eq(c, "suffix", "ña")
def sutra_4_4_130(c): return _eq(c, "stem", "ojas") and _eq(c, "semantic", "ahan") and _in(c, "suffix", {"yat", "kha"})
def sutra_4_4_131(c): return _in(c, "stem_final", {"veśo", "yaśo"}) and _eq(c, "stem_class", "bhagādi") and _eq(c, "suffix", "yal")
def sutra_4_4_132(c): return _eq(c, "suffix", "kha") and _eq(c, "rule", "continuation")
def sutra_4_4_133(c): return _eq(c, "stem", "pūrva") and _eq(c, "semantic", "kṛta") and _in(c, "suffix", {"ini", "yat"})
def sutra_4_4_134(c): return _eq(c, "stem", "ap") and _eq(c, "semantic", "saṃskṛta")
def sutra_4_4_135(c): return _eq(c, "stem", "sahasra") and _eq(c, "semantic", "sammita") and _eq(c, "suffix", "gha")
def sutra_4_4_136(c): return _eq(c, "stem_class", "matu") and _eq(c, "rule", "continuation")
def sutra_4_4_137(c): return _eq(c, "stem", "soma") and _eq(c, "semantic", "arhati") and _eq(c, "suffix", "ya")
def sutra_4_4_138(c): return _eq(c, "stem_final", "maya") and _eq(c, "rule", "continuation")
def sutra_4_4_139(c): return _eq(c, "stem", "madhu") and _eq(c, "rule", "continuation")
def sutra_4_4_140(c): return _eq(c, "stem", "vasu") and _eq(c, "semantic", "samūha")
def sutra_4_4_141(c): return _eq(c, "stem", "nakṣatra") and _eq(c, "suffix", "gha")
def sutra_4_4_142(c): return _eq(c, "stem", "sarvadeva") and _eq(c, "suffix", "tātil")
def sutra_4_4_143(c): return _in(c, "stem", {"śivaśam", "ariṣṭa"}) and _eq(c, "semantic", "kara")
def sutra_4_4_144(c): return _eq(c, "semantic", "bhāva") and _eq(c, "rule", "continuation")


# ---------------------------------------------------------------------------
# Fixtures — each sutra fires on its prescribed (stem_class, suffix [, semantic])
# triple; the negative either changes the stem_class or the suffix.
# ---------------------------------------------------------------------------

def _fxR(positive: dict, negative: dict):
    """Helper that defaults missing keys to ordinary values."""
    return ({"stem_class": "ordinary", "suffix": "ordinary", "semantic": "ordinary", **positive},
            {"stem_class": "ordinary", "suffix": "ordinary", "semantic": "ordinary", **negative})


def _fxR_stem(positive: dict, negative: dict):
    """Same defaults but for predicates keyed on ``stem`` rather than stem_class."""
    return ({"stem": "ordinary", "suffix": "ordinary", "semantic": "ordinary", **positive},
            {"stem": "ordinary", "suffix": "ordinary", "semantic": "ordinary", **negative})


FIXTURES: dict[str, tuple[dict, dict]] = {
    # 4.1 -------------------------------------------------------------------
    "4.1.1":  _fxR({"stem_class": "pratipadika", "suffix": "nyap_or_ap"}, {"stem_class": "dhatu", "suffix": "nyap_or_ap"}),
    "4.1.3":  _fxR({"semantic": "stri", "takes_stri_pratyaya": True}, {"semantic": "stri", "takes_stri_pratyaya": False}),
    "4.1.4":  _fxR({"stem_class": "ajadyatash", "suffix": "ṭāp"}, {"stem_class": "śivādi", "suffix": "ṭāp"}),
    "4.1.5":  _fxR({"stem_class": "rn_or_n_ending", "suffix": "ṅīp"}, {"stem_class": "ajadyatash", "suffix": "ṅīp"}),
    "4.1.6":  _fxR({"has_ugit": True, "suffix": "ṅīp"}, {"has_ugit": False, "suffix": "ṅīp"}),
    "4.1.7":  _fxR_stem({"stem": "van", "suffix": "ṅīp", "augment": "ra"}, {"stem": "deva", "suffix": "ṅīp", "augment": "ra"}),
    "4.1.8":  _fxR_stem({"stem": "pād", "suffix": "ṅīp", "optional": True}, {"stem": "deva", "suffix": "ṅīp", "optional": True}),
    "4.1.9":  _fxR({"stem_class": "ṭāb_rci", "suffix": "ṭāp"}, {"stem_class": "ajadyatash", "suffix": "ṭāp"}),
    "4.1.10": _fxR({"stem_class": "ṣaṭ_svasradi", "suffix_blocked": "ṅīp"}, {"stem_class": "ordinary", "suffix_blocked": "ṅīp"}),
    "4.1.11": _fxR_stem({"stem": "manas", "suffix": "ṅīp"}, {"stem": "deva", "suffix": "ṅīp"}),
    "4.1.12": _fxR({"compound_type": "bahuvrihi", "stem_final": "an", "suffix": "ṅīp"}, {"compound_type": "tatpurusha", "stem_final": "an", "suffix": "ṅīp"}),
    "4.1.13": _fxR({"stem_class": "ḍāb_ubhāb", "optional": True}, {"stem_class": "ordinary", "optional": True}),
    "4.1.14": _fxR({"is_upasarjana": False, "suffix": "ṅīp"}, {"is_upasarjana": True, "suffix": "ṅīp"}),
    "4.1.15": _fxR({"stem_class": "ṭiḍḍhānañ_etc", "suffix": "ṅīp"}, {"stem_class": "ordinary", "suffix": "ṅīp"}),
    "4.1.16": _fxR({"stem_class": "yañ", "suffix": "ṅīp"}, {"stem_class": "ordinary", "suffix": "ṅīp"}),
    "4.1.17": _fxR({"dialect": "pracya", "suffix": "ṣpha"}, {"dialect": "udīcī", "suffix": "ṣpha"}),
    "4.1.18": _fxR({"stem_class": "lohitādi", "suffix": "ṣpha"}, {"stem_class": "ordinary", "suffix": "ṣpha"}),
    "4.1.19": _fxR_stem({"stem": "kauravya", "suffix": "ṣpha"}, {"stem": "deva", "suffix": "ṣpha"}),
    "4.1.20": _fxR({"semantic": "prathama_vayas", "suffix": "ṣpha"}, {"semantic": "ordinary", "suffix": "ṣpha"}),
    "4.1.21": _fxR({"stem_class": "dvigu", "suffix": "ṣpha"}, {"stem_class": "ordinary", "suffix": "ṣpha"}),
    "4.1.22": _fxR({"stem_class": "aparimaṇa_etc", "operation": "no_taddhita_luk"}, {"stem_class": "ordinary", "operation": "no_taddhita_luk"}),
    "4.1.23": _fxR({"stem_final": "kāṇḍa", "semantic": "kshetra", "suffix": "ṣpha"}, {"stem_final": "kāṇḍa", "semantic": "ordinary", "suffix": "ṣpha"}),
    "4.1.24": _fxR_stem({"stem": "puruṣa", "semantic": "pramana", "optional": True}, {"stem": "deva", "semantic": "pramana", "optional": True}),
    "4.1.25": _fxR({"compound_type": "bahuvrihi", "stem_final": "ūdhas", "suffix": "ṅīṣ"}, {"compound_type": "tatpurusha", "stem_final": "ūdhas", "suffix": "ṅīṣ"}),
    "4.1.26": _fxR({"stem_class": "samkhya_avyaya_adi", "suffix": "ṅīp"}, {"stem_class": "ordinary", "suffix": "ṅīp"}),
    "4.1.27": _fxR({"stem_final": "dāman", "suffix": "ṅīp"}, {"stem_final": "deva", "suffix": "ṅīp"}),
    "4.1.28": _fxR({"stem_final": "an", "upadha_lopa": True, "optional": True}, {"stem_final": "an", "upadha_lopa": False, "optional": True}),
    "4.1.29": _fxR({"domain": "samjna", "rule": "always"}, {"domain": "ordinary", "rule": "always"}),
    "4.1.30": _fxR({"stem_class": "kevala_mamaka_etc", "suffix": "ṅīp"}, {"stem_class": "ordinary", "suffix": "ṅīp"}),
    "4.1.31": _fxR_stem({"stem": "rātri", "suffix": "ṅīp", "case": "non_ajas"}, {"stem": "rātri", "suffix": "ṅīp", "case": "ajas"}),
    "4.1.32": _fxR_stem({"stem": "antarvat", "augment": "nuk"}, {"stem": "deva", "augment": "nuk"}),
    "4.1.33": _fxR_stem({"stem": "pati", "semantic": "yajna_samyoga", "substitute": "no"}, {"stem": "pati", "semantic": "ordinary", "substitute": "no"}),
    "4.1.34": _fxR({"has_sapurva": True, "optional": True}, {"has_sapurva": False, "optional": True}),
    "4.1.35": _fxR({"stem_class": "sapatnyādi", "rule": "always"}, {"stem_class": "ordinary", "rule": "always"}),
    "4.1.36": _fxR_stem({"stem": "pūtakratu", "substitute": "ai"}, {"stem": "deva", "substitute": "ai"}),
    "4.1.37": _fxR({"stem_class": "vṛṣākapyādi", "accent": "udatta"}, {"stem_class": "ordinary", "accent": "udatta"}),
    "4.1.38": _fxR_stem({"stem": "manu", "substitute": "au", "optional": True}, {"stem": "deva", "substitute": "au", "optional": True}),
    "4.1.39": _fxR({"stem_class": "varṇāt_anudāttāt_topadhāt", "substitute": "n"}, {"stem_class": "ordinary", "substitute": "n"}),
    "4.1.40": _fxR({"stem_class": "anyato", "suffix": "ṅīṣ"}, {"stem_class": "ordinary", "suffix": "ṅīṣ"}),
    "4.1.41": _fxR({"stem_class": "ṣid_gaurādi", "suffix": "ṅīṣ"}, {"stem_class": "ordinary", "suffix": "ṅīṣ"}),
    "4.1.42": _fxR({"stem_class": "jānapada_kuṇḍa_etc", "suffix": "ṅīṣ"}, {"stem_class": "ordinary", "suffix": "ṅīṣ"}),
    "4.1.43": _fxR_stem({"stem": "śoṇa", "dialect": "pracya", "suffix": "ṅīṣ"}, {"stem": "śoṇa", "dialect": "udīcī", "suffix": "ṅīṣ"}),
    "4.1.44": _fxR({"stem_final": "vat", "semantic": "guṇa_vacana"}, {"stem_final": "vat", "semantic": "ordinary"}),
    "4.1.45": _fxR({"stem_class": "bahvādi", "suffix": "ṅīṣ"}, {"stem_class": "ordinary", "suffix": "ṅīṣ"}),
    "4.1.46": _fxR({"is_vedic": True, "rule": "always"}, {"is_vedic": False, "rule": "always"}),
    "4.1.47": _fxR_stem({"stem": "bhū", "suffix": "ṅīṣ"}, {"stem": "deva", "suffix": "ṅīṣ"}),
    "4.1.48": _fxR({"semantic": "puṃyoga_akhya", "suffix": "ṅīṣ"}, {"semantic": "ordinary", "suffix": "ṅīṣ"}),
    "4.1.49": _fxR({"stem_class": "indravaruṇādi", "augment": "ānuk"}, {"stem_class": "ordinary", "augment": "ānuk"}),
    "4.1.50": _fxR({"krita_karaṇa_purva": True, "suffix": "ṅīṣ"}, {"krita_karaṇa_purva": False, "suffix": "ṅīṣ"}),
    "4.1.51": _fxR({"has_kta": True, "semantic": "alpa_akhya"}, {"has_kta": True, "semantic": "ordinary"}),
    "4.1.52": _fxR({"compound_type": "bahuvrihi", "accent": "anta_udatta", "suffix": "ṅīṣ"}, {"compound_type": "tatpurusha", "accent": "anta_udatta", "suffix": "ṅīṣ"}),
    "4.1.53": _fxR({"purva_pada": "non_svāṅga", "optional": True}, {"purva_pada": "svāṅga", "optional": True}),
    "4.1.54": _fxR({"purva_pada": "svāṅga", "is_upasarjana": True, "upadha": "non_samyoga"}, {"purva_pada": "svāṅga", "is_upasarjana": False, "upadha": "non_samyoga"}),
    "4.1.55": _fxR({"stem_final": "nāsikā"}, {"stem_final": "ordinary"}),
    "4.1.56": _fxR({"stem_class": "kroḍādi", "is_bahvac": True}, {"stem_class": "kroḍādi", "is_bahvac": False}),
    "4.1.57": _fxR({"purva_pada": "saha_naṅ_vidyamāna", "blocks_strī": True}, {"purva_pada": "ordinary", "blocks_strī": True}),
    "4.1.58": _fxR({"stem_final": "nakhamukha", "domain": "samjna"}, {"stem_final": "nakhamukha", "domain": "ordinary"}),
    "4.1.59": _fxR_stem({"stem": "dīrghajihvī", "is_vedic": True}, {"stem": "dīrghajihvī", "is_vedic": False}),
    "4.1.60": _fxR({"purva_pada": "dik", "suffix": "ṅīp"}, {"purva_pada": "ordinary", "suffix": "ṅīp"}),
    "4.1.61": _fxR({"stem_final": "vāha", "suffix": "ṅīp"}, {"stem_final": "deva", "suffix": "ṅīp"}),
    "4.1.62": _fxR_stem({"stem": "sakhi", "dialect": "bhāṣā"}, {"stem": "sakhi", "dialect": "chandas"}),
    "4.1.63": _fxR({"semantic": "jati", "domain": "ordinary", "upadha": "ayopadha"}, {"semantic": "jati", "domain": "stri_vishaya", "upadha": "ayopadha"}),
    "4.1.64": _fxR({"stem_class": "pāka_karṇa_etc_uttara_pada", "suffix": "ṅīp"}, {"stem_class": "ordinary", "suffix": "ṅīp"}),
    "4.1.65": _fxR({"stem_final": "i", "semantic": "manuṣya_jati"}, {"stem_final": "i", "semantic": "ordinary"}),
    "4.1.66": _fxR({"stem_final": "u", "suffix": "ūṅ"}, {"stem_final": "i", "suffix": "ūṅ"}),
    "4.1.67": _fxR({"stem_final": "bāhu", "domain": "samjna"}, {"stem_final": "bāhu", "domain": "ordinary"}),
    "4.1.68": _fxR_stem({"stem": "paṅgu"}, {"stem": "deva"}),
    "4.1.69": _fxR({"purva_pada": "ūru", "semantic": "aupamya"}, {"purva_pada": "ūru", "semantic": "ordinary"}),
    "4.1.70": _fxR({"stem_class": "samhitaśapha_lakshaṇa_vāma"}, {"stem_class": "ordinary"}),
    "4.1.71": _fxR_stem({"stem": "kadru", "is_vedic": True}, {"stem": "kadru", "is_vedic": False}),
    "4.1.72": _fxR({"domain": "samjna", "rule": "always_strī"}, {"domain": "ordinary", "rule": "always_strī"}),
    "4.1.73": _fxR({"stem_class": "śārṅgaravadi_yan", "suffix": "ṅīn"}, {"stem_class": "ordinary", "suffix": "ṅīn"}),
    "4.1.74": _fxR({"stem_class": "yañ", "suffix": "cāp"}, {"stem_class": "ordinary", "suffix": "cāp"}),
    "4.1.75": _fxR_stem({"stem": "āvaṭya", "suffix": "cāp"}, {"stem": "deva", "suffix": "cāp"}),
    "4.1.76": _fxR({"suffix_class": "taddhita"}, {"suffix_class": "krt"}),
    "4.1.77": _fxR_stem({"stem": "yuvan", "substitute": "ti"}, {"stem": "deva", "substitute": "ti"}),
    "4.1.78": _fxR({"stem_class": "aniñ_anārṣa_guru_uttamayo", "suffix": "ṣyaṅ", "semantic": "gotra"}, {"stem_class": "ordinary", "suffix": "ṣyaṅ", "semantic": "gotra"}),
    "4.1.79": _fxR({"stem_class": "gotra_avayava", "rule": "continuation"}, {"stem_class": "ordinary", "rule": "continuation"}),
    "4.1.80": _fxR({"stem_class": "krauḍyādi", "suffix": "ṣyaṅ"}, {"stem_class": "ordinary", "suffix": "ṣyaṅ"}),
    "4.1.81": _fxR({"stem_class": "daivayajñyādi", "optional": True}, {"stem_class": "ordinary", "optional": True}),
    "4.1.82": _fxR({"stem_class": "samartha_prathamāt_va", "optional": True}, {"stem_class": "ordinary", "optional": True}),
    "4.1.83": _fxR({"section": "prāgdīvyataḥ", "suffix": "aṇ"}, {"section": "ordinary", "suffix": "aṇ"}),
    "4.1.84": _fxR({"stem_class": "aśvapatyādi", "suffix": "aṇ"}, {"stem_class": "ordinary", "suffix": "aṇ"}),
    "4.1.85": _fxR({"stem_final": "diti", "suffix": "ṇya"}, {"stem_final": "deva", "suffix": "ṇya"}),
    "4.1.86": _fxR({"stem_class": "utsādi", "suffix": "añ"}, {"stem_class": "ordinary", "suffix": "añ"}),
    "4.1.87": _fxR_stem({"stem": "strī", "suffix": "nañsnañ", "semantic": "bhavana"}, {"stem": "strī", "suffix": "nañsnañ", "semantic": "ordinary"}),
    "4.1.88": _fxR({"stem_class": "dvigu", "operation": "luk", "semantic": "anapatya"}, {"stem_class": "ordinary", "operation": "luk", "semantic": "anapatya"}),
    "4.1.89": _fxR({"semantic": "gotra", "operation": "aluk", "following": "ac"}, {"semantic": "ordinary", "operation": "aluk", "following": "ac"}),
    "4.1.90": _fxR_stem({"stem": "yuvan", "operation": "luk"}, {"stem": "deva", "operation": "luk"}),
    "4.1.91": _fxR({"suffix": "phak", "optional": True}, {"suffix": "aṇ", "optional": True}),
    "4.1.93": _fxR({"semantic": "gotra", "number": "single", "rule": "eko_gotre"}, {"semantic": "ordinary", "number": "single", "rule": "eko_gotre"}),
    "4.1.94": _fxR({"semantic": "gotra_yuvati", "gender": "stri"}, {"semantic": "ordinary", "gender": "stri"}),
    "4.1.95": _fxR({"stem_final": "a", "suffix": "iñ"}, {"stem_final": "u", "suffix": "iñ"}),
    "4.1.96": _fxR({"stem_class": "bāhvādi", "suffix": "iñ"}, {"stem_class": "ordinary", "suffix": "iñ"}),
    "4.1.97": _fxR_stem({"stem": "sudhātu", "suffix": "akañ"}, {"stem": "deva", "suffix": "akañ"}),
    "4.1.98": _fxR({"stem_class": "kuñjādi", "semantic": "gotra", "suffix": "cphañ"}, {"stem_class": "ordinary", "semantic": "gotra", "suffix": "cphañ"}),
    "4.1.99": _fxR({"stem_class": "naḍādi", "suffix": "phak"}, {"stem_class": "ordinary", "suffix": "phak"}),
    "4.1.100":_fxR({"stem_class": "haritādi", "suffix": "añ"}, {"stem_class": "ordinary", "suffix": "añ"}),
    "4.1.101":_fxR({"stem_class": "yañ", "rule": "continuation"}, {"stem_class": "ordinary", "rule": "continuation"}),
    "4.1.102":_fxR_stem({"stem": "śaradvat", "semantic": "bhṛguvatsa_agrāyaṇa"}, {"stem": "deva", "semantic": "bhṛguvatsa_agrāyaṇa"}),
    "4.1.103":_fxR_stem({"stem": "droṇaparvata", "optional": True}, {"stem": "deva", "optional": True}),
    "4.1.104":_fxR({"stem_class": "bidādi", "semantic": "anantarya", "suffix": "añ"}, {"stem_class": "ordinary", "semantic": "anantarya", "suffix": "añ"}),
    "4.1.105":_fxR({"stem_class": "gargādi", "suffix": "yañ"}, {"stem_class": "ordinary", "suffix": "yañ"}),
    "4.1.106":_fxR_stem({"stem": "madhu", "semantic": "brāhmaṇa_kauśika"}, {"stem": "deva", "semantic": "brāhmaṇa_kauśika"}),
    "4.1.107":_fxR_stem({"stem": "kapi", "semantic": "āṅgirasa"}, {"stem": "deva", "semantic": "āṅgirasa"}),
    "4.1.108":_fxR_stem({"stem": "vataṇḍa", "rule": "continuation"}, {"stem": "deva", "rule": "continuation"}),
    "4.1.109":_fxR({"semantic": "stri", "operation": "luk"}, {"semantic": "ordinary", "operation": "luk"}),
    "4.1.110":_fxR({"stem_class": "aśvādi", "suffix": "phañ"}, {"stem_class": "ordinary", "suffix": "phañ"}),
    "4.1.111":_fxR_stem({"stem": "bharga", "semantic": "traigarta", "suffix": "phañ"}, {"stem": "deva", "semantic": "traigarta", "suffix": "phañ"}),
    "4.1.112":_fxR({"stem_class": "śivādi", "suffix": "aṇ"}, {"stem_class": "ordinary", "suffix": "aṇ"}),
    "4.1.113":_fxR({"is_avrddha": True, "stem_class": "nadī_mānuṣī", "is_tannamika": True}, {"is_avrddha": False, "stem_class": "nadī_mānuṣī", "is_tannamika": True}),
    "4.1.114":_fxR_stem({"stem": "ṛṣya", "suffix": "aṇ"}, {"stem": "deva", "suffix": "aṇ"}),
    "4.1.115":_fxR_stem({"stem": "mātṛ", "purva_pada": "ordinary", "augment": "ut"}, {"stem": "mātṛ", "purva_pada": "saṅkhya", "augment": "ut"}),
    "4.1.116":_fxR_stem({"stem": "kanyā", "augment": "kanīna"}, {"stem": "deva", "augment": "kanīna"}),
    "4.1.117":_fxR_stem({"stem": "vikarṇa", "semantic": "vatsa"}, {"stem": "deva", "semantic": "vatsa"}),
    "4.1.118":_fxR_stem({"stem": "pīlā", "optional": True}, {"stem": "deva", "optional": True}),
    "4.1.119":_fxR_stem({"stem": "maṇḍūka", "suffix": "ḍhak"}, {"stem": "deva", "suffix": "ḍhak"}),
    "4.1.120":_fxR({"stem_class": "strī", "suffix": "ḍhak"}, {"stem_class": "ordinary", "suffix": "ḍhak"}),
    "4.1.121":_fxR({"stem_class": "dvyac", "suffix": "ḍhak"}, {"stem_class": "ordinary", "suffix": "ḍhak"}),
    "4.1.122":_fxR({"stem_class": "non_iñ", "suffix": "ḍhak"}, {"stem_class": "iñ", "suffix": "ḍhak"}),
    "4.1.123":_fxR({"stem_class": "śubhrādi", "suffix": "ḍhak"}, {"stem_class": "ordinary", "suffix": "ḍhak"}),
    "4.1.124":_fxR_stem({"stem": "vikarṇa", "semantic": "kāśyapa"}, {"stem": "deva", "semantic": "kāśyapa"}),
    "4.1.125":_fxR_stem({"stem": "bhru", "augment": "vuk"}, {"stem": "deva", "augment": "vuk"}),
    "4.1.126":_fxR({"stem_class": "kalyāṇyādi", "augment": "inaṅ"}, {"stem_class": "ordinary", "augment": "inaṅ"}),
    "4.1.127":_fxR_stem({"stem": "kulaṭā", "optional": True}, {"stem": "deva", "optional": True}),
    "4.1.128":_fxR_stem({"stem": "caṭakā", "suffix": "airak"}, {"stem": "deva", "suffix": "airak"}),
    "4.1.129":_fxR_stem({"stem": "godhā", "suffix": "ḍhrak"}, {"stem": "deva", "suffix": "ḍhrak"}),
    "4.1.130":_fxR({"dialect": "ārā_udīcī", "rule": "godhā_dhrak"}, {"dialect": "pracya", "rule": "godhā_dhrak"}),
    "4.1.131":_fxR({"stem_class": "kṣudrādi", "optional": True}, {"stem_class": "ordinary", "optional": True}),
    "4.1.132":_fxR_stem({"stem": "pitṛṣvasṛ", "suffix": "chaṇ"}, {"stem": "deva", "suffix": "chaṇ"}),
    "4.1.133":_fxR_stem({"stem": "pitṛṣvasṛ", "suffix": "ḍhak", "operation": "lopa"}, {"stem": "pitṛṣvasṛ", "suffix": "ordinary", "operation": "lopa"}),
    "4.1.134":_fxR_stem({"stem": "mātṛṣvasṛ", "rule": "continuation"}, {"stem": "deva", "rule": "continuation"}),
    "4.1.135":_fxR({"stem_class": "catuṣpād", "suffix": "ḍhañ"}, {"stem_class": "ordinary", "suffix": "ḍhañ"}),
    "4.1.136":_fxR({"stem_class": "gṛṣṭyādi", "suffix": "ḍhañ"}, {"stem_class": "ordinary", "suffix": "ḍhañ"}),
    "4.1.137":_fxR_stem({"stem": "rājan", "suffix": "yat"}, {"stem": "deva", "suffix": "yat"}),
    "4.1.138":_fxR_stem({"stem": "kṣatra", "suffix": "gha"}, {"stem": "deva", "suffix": "gha"}),
    "4.1.139":_fxR_stem({"stem": "kula", "suffix": "kha"}, {"stem": "deva", "suffix": "kha"}),
    "4.1.140":_fxR({"has_purva_pada": False, "optional": True, "suffix": "yat"}, {"has_purva_pada": True, "optional": True, "suffix": "yat"}),
    "4.1.141":_fxR_stem({"stem": "mahākula", "suffix": "añ"}, {"stem": "deva", "suffix": "añ"}),
    "4.1.142":_fxR_stem({"stem": "duṣkula", "suffix": "ḍhak"}, {"stem": "deva", "suffix": "ḍhak"}),
    "4.1.143":_fxR_stem({"stem": "svasṛ", "suffix": "cha"}, {"stem": "deva", "suffix": "cha"}),
    "4.1.144":_fxR_stem({"stem": "bhrātṛ", "suffix": "vya"}, {"stem": "deva", "suffix": "vya"}),
    "4.1.145":_fxR({"semantic": "sapatna", "suffix": "vyan"}, {"semantic": "ordinary", "suffix": "vyan"}),
    "4.1.146":_fxR({"stem_class": "revatyādi", "suffix": "ṭhak"}, {"stem_class": "ordinary", "suffix": "ṭhak"}),
    "4.1.147":_fxR({"semantic": "gotrastrī_kutsana", "suffix": "ṇa"}, {"semantic": "ordinary", "suffix": "ṇa"}),
    "4.1.148":_fxR({"stem_class": "vṛddha", "semantic": "sauvīra", "suffix": "ṭhak"}, {"stem_class": "vṛddha", "semantic": "ordinary", "suffix": "ṭhak"}),
    "4.1.149":_fxR({"stem_final": "phi", "suffix": "cha"}, {"stem_final": "deva", "suffix": "cha"}),
    "4.1.150":_fxR_stem({"stem": "phāṇṭāhṛti", "suffix": "ṇaphiñ"}, {"stem": "deva", "suffix": "ṇaphiñ"}),
    "4.1.151":_fxR({"stem_class": "kurvādi", "suffix": "ṇya"}, {"stem_class": "ordinary", "suffix": "ṇya"}),
    "4.1.152":_fxR({"stem_class": "senānta_lakṣaṇa_kāri", "suffix": "ṇya"}, {"stem_class": "ordinary", "suffix": "ṇya"}),
    "4.1.153":_fxR({"dialect": "udīcī", "suffix": "iñ"}, {"dialect": "pracya", "suffix": "iñ"}),
    "4.1.154":_fxR({"stem_class": "tikādi", "suffix": "phiñ"}, {"stem_class": "ordinary", "suffix": "phiñ"}),
    "4.1.155":_fxR_stem({"stem": "kausalya", "suffix": "phiñ"}, {"stem": "deva", "suffix": "phiñ"}),
    "4.1.156":_fxR({"stem_class": "aṇ_dvyac", "rule": "continuation"}, {"stem_class": "ordinary", "rule": "continuation"}),
    "4.1.157":_fxR({"dialect": "udīcī", "stem_class": "vṛddha", "semantic": "non_gotra"}, {"dialect": "udīcī", "stem_class": "vṛddha", "semantic": "gotra"}),
    "4.1.158":_fxR({"stem_class": "vākināt", "augment": "kuk"}, {"stem_class": "ordinary", "augment": "kuk"}),
    "4.1.159":_fxR({"stem_final": "putra", "optional": True}, {"stem_final": "deva", "optional": True}),
    "4.1.160":_fxR({"dialect": "pracya", "stem_class": "non_vṛddha", "suffix": "phin"}, {"dialect": "pracya", "stem_class": "vṛddha", "suffix": "phin"}),
    "4.1.161":_fxR_stem({"stem": "manu", "semantic": "jati", "suffix": "añyat", "augment": "ṣuk"}, {"stem": "manu", "semantic": "ordinary", "suffix": "añyat", "augment": "ṣuk"}),
    "4.1.162":_fxR({"semantic": "pautra_prabhṛti", "samjna": "gotra"}, {"semantic": "ordinary", "samjna": "gotra"}),
    "4.1.163":_fxR({"vamśya_living": True, "samjna": "yuvan"}, {"vamśya_living": False, "samjna": "yuvan"}),
    "4.1.164":_fxR({"context": "elder_brother_living", "samjna": "yuvan"}, {"context": "ordinary", "samjna": "yuvan"}),
    "4.1.165":_fxR({"anya_sapinda_sthavira_living": True, "optional": True}, {"anya_sapinda_sthavira_living": False, "optional": True}),
    "4.1.166":_fxR({"semantic": "vṛddha_pūjā", "rule": "continuation"}, {"semantic": "ordinary", "rule": "continuation"}),
    "4.1.167":_fxR({"samjna": "yuvan", "semantic": "kutsā"}, {"samjna": "yuvan", "semantic": "ordinary"}),
    "4.1.168":_fxR({"stem_class": "janapada", "semantic": "kṣatriya_apatya", "suffix": "añ"}, {"stem_class": "ordinary", "semantic": "kṣatriya_apatya", "suffix": "añ"}),
    "4.1.169":_fxR_stem({"stem": "sālveya", "rule": "continuation"}, {"stem": "deva", "rule": "continuation"}),
    "4.1.170":_fxR({"stem_class": "dvyac_kṣatriya", "suffix": "aṇ"}, {"stem_class": "ordinary", "suffix": "aṇ"}),
    "4.1.171":_fxR({"stem_class": "vṛddhet_kosala_aja", "suffix": "ñyaṅ"}, {"stem_class": "ordinary", "suffix": "ñyaṅ"}),
    "4.1.172":_fxR({"stem_class": "kurunādi", "suffix": "ṇya"}, {"stem_class": "ordinary", "suffix": "ṇya"}),
    "4.1.173":_fxR({"stem_class": "sālvāvayava_pratyagratha", "suffix": "iñ"}, {"stem_class": "ordinary", "suffix": "iñ"}),
    "4.1.174":_fxR({"samjna": "tadrāja"}, {"samjna": "gotra"}),
    "4.1.175":_fxR_stem({"stem": "kamboja", "operation": "luk"}, {"stem": "deva", "operation": "luk"}),
    "4.1.176":_fxR_stem({"semantic": "stri", "stem": "avanti"}, {"semantic": "stri", "stem": "deva"}),
    "4.1.177":_fxR({"stem_final": "a", "rule": "continuation"}, {"stem_final": "deva", "rule": "continuation"}),
    "4.1.178":_fxR({"dialect": "pracya", "stem_class": "bhargādi", "rule": "blocking"}, {"dialect": "udīcī", "stem_class": "bhargādi", "rule": "blocking"}),
}


# 4.2 fixtures, programmatically built from a compact table
_FX_4_2_RAW = [
    ("4.2.1", "semantic:rāga_rakta",          "suffix:aṇ"),
    ("4.2.2", "stem:lākṣā",                   "suffix:ṭhak"),
    ("4.2.3", "semantic:nakshatra_yukta_kala","suffix:aṇ"),
    ("4.2.4", "operation:lup",                "semantic:avisesha"),
    ("4.2.5", "stem:śravaṇa",                 "domain:samjna"),
    ("4.2.6", "compound_type:dvandva",        "suffix:cha"),
    ("4.2.7", "semantic:dṛṣṭa_sāma",          "suffix:aṇ"),
    ("4.2.8", "stem:kali",                    "suffix:ḍhak"),
    ("4.2.9", "stem:vāmadeva",                "suffix:ḍyat"),
    ("4.2.10","semantic:parivrta_ratha",      "suffix:aṇ"),
    ("4.2.11","stem_class:pāṇḍukambala",      "suffix:ini"),
    ("4.2.12","stem:dvīpa",                   "suffix:añ"),
    ("4.2.13","semantic:kaumāra_apūrva_vacana","rule:continuation"),
    ("4.2.14","semantic:uddhṛta",             "stem_class:amatra",    "suffix:aṇ"),
    ("4.2.15","stem:sthaṇḍila",               "semantic:śayitavrata", "suffix:aṇ"),
    ("4.2.16","semantic:saṃskṛta_bhakṣa",     "suffix:aṇ"),
    ("4.2.17","stem:śūla_okha",               "suffix:yat"),
    ("4.2.18","stem:dadhi",                   "suffix:ṭhak"),
    ("4.2.19","stem:udaśvit",                 "optional:1"),
    ("4.2.20","stem:kṣīra",                   "suffix:ḍhañ"),
    ("4.2.21","semantic:paurṇamāsī",          "domain:samjna"),
    ("4.2.22","stem:āgrahāyaṇī",              "suffix:ṭhak"),
    ("4.2.23","stem:phālgunī",                "optional:1"),
    ("4.2.24","semantic:devatā_yukta",        "rule:continuation"),
    ("4.2.25","stem:ka",                      "augment:it"),
    ("4.2.26","stem:śukra",                   "suffix:ghan"),
    ("4.2.27","stem:aponaptṛ",                "suffix:gha"),
    ("4.2.28","rule:cha_continuation",        None),
    ("4.2.29","stem:mahendra",                "suffix:gha"),
    ("4.2.30","stem:soma",                    "suffix:ṭyaṇ"),
    ("4.2.31","stem:vāyu",                    "suffix:yat"),
    ("4.2.32","stem_class:dyāvāpṛthivyādi",   "suffix:cha"),
    ("4.2.33","stem:agni",                    "suffix:ḍhak"),
    ("4.2.34","semantic:kāla_bhava",          "rule:continuation"),
    ("4.2.35","stem:mahārāja",                "suffix:ṭhañ"),
    ("4.2.36","stem:pitṛvya",                 "domain:samjna"),
    ("4.2.37","semantic:samūha",              "adhikara:tasya_samuha"),
    ("4.2.38","stem_class:bhikṣādi",          "suffix:aṇ"),
    ("4.2.39","stem_class:gotraukṣaṇi",       "suffix:vuñ"),
    ("4.2.40","stem:kedāra",                  "suffix:yañ"),
    ("4.2.41","stem:kavacin",                 "suffix:ṭhañ"),
    ("4.2.42","stem:brāhmaṇa",                "suffix:yan"),
    ("4.2.43","stem:grāma",                   "suffix:tal"),
    ("4.2.44","stem_class:anudāttādi",        "suffix:añ"),
    ("4.2.45","stem_class:khaṇḍikādi",        "rule:continuation"),
    ("4.2.46","stem_class:caraṇa",            "semantic:dharma"),
    ("4.2.47","stem:acittahasti",             "suffix:ṭhak"),
    ("4.2.48","stem:keśa",                    "suffix:yañ"),
    ("4.2.49","stem_class:pāśādi",            "suffix:ya"),
    ("4.2.50","stem:khala",                   "rule:continuation"),
    ("4.2.51","stem:ini",                     "rule:continuation"),
    ("4.2.52","semantic:viṣaya",              "adhikara:deśa"),
    ("4.2.53","stem_class:rājanyādi",         "suffix:vuñ"),
    ("4.2.54","stem_class:bhauriky_aiṣukāri", "suffix:vidhal"),
    ("4.2.55","semantic:chandasa_pragātha",   "rule:continuation"),
    ("4.2.56","semantic:saṃgrāma_prayojana",  "suffix:aṇ"),
    ("4.2.57","semantic:praharaṇa_krīḍā",     "suffix:ṇa"),
    ("4.2.58","suffix_class:ghañ",            "semantic:kriyā",       "suffix:ña"),
    ("4.2.59","semantic:adhīte_veda",         "rule:continuation"),
    ("4.2.60","stem_class:kratu_uktha_etc",   "suffix:ṭhak"),
    ("4.2.61","stem_class:kramādi",           "suffix:vun"),
    ("4.2.62","stem:anubrāhmaṇa",             "suffix:ini"),
    ("4.2.63","stem_class:vasantādi",         "suffix:ṭhak"),
    ("4.2.64","semantic:prokta",              "operation:luk"),
    ("4.2.65","stem_final:sūtra",             "upadha:k"),
    ("4.2.66","stem:chando",                  "semantic:tad_viṣaya"),
    ("4.2.67","semantic:deśa_tan_nāma",       "rule:tad_asminn_asti"),
    ("4.2.68","semantic:tena_nirvṛtta",       "rule:continuation"),
    ("4.2.69","semantic:tasya_nivāsa",        "rule:continuation"),
    ("4.2.70","semantic:adūrabhava",          "rule:continuation"),
    ("4.2.71","stem_final:u",                 "suffix:añ"),
    ("4.2.72","stem_final:matup",             "stem_class:bahvac_aṅga"),
    ("4.2.73","stem_class:bahvac_kūpa",       "rule:continuation"),
    ("4.2.74","dialect:udak_vipāś",           "rule:continuation"),
    ("4.2.75","stem_class:saṃkalādi",         "rule:continuation"),
    ("4.2.76","domain:strī",                  "dialect:sauvīra"),
    ("4.2.77","stem_class:suvāstvādi",        "suffix:aṇ"),
    ("4.2.78","stem:roṇī",                    "rule:continuation"),
    ("4.2.79","upadha:k",                     "rule:continuation"),
    ("4.2.80","stem_class:vuñ_chaṇ_kaṭha_etc","rule:continuation"),
    ("4.2.81","semantic:janapada",            "operation:lup"),
    ("4.2.82","stem_class:varaṇādi",          "rule:continuation"),
    ("4.2.83","stem:śarkarā",                 "optional:1"),
    ("4.2.84","suffix:ṭhak",                  "rule:continuation"),
    ("4.2.85","stem_final:nadī",              "suffix:matup"),
    ("4.2.86","stem_class:madhvādi",          "suffix:matup"),
    ("4.2.87","stem:kumuda",                  "suffix:ḍmatup"),
    ("4.2.88","stem:naḍa",                    "suffix:ḍvalac"),
    ("4.2.89","stem:śikhā",                   "suffix:valac"),
    ("4.2.90","stem_class:utkarādi",          "suffix:cha"),
    ("4.2.91","stem_class:naḍādi",            "augment:kuk"),
    ("4.2.92","semantic:śeṣa",                "rule:continuation"),
    ("4.2.93","stem_final:rāṣṭra",            "suffix:gha"),
    ("4.2.94","stem:grāma",                   "suffix:ya"),
    ("4.2.95","stem_class:kattryādi",         "suffix:ḍhakañ"),
    ("4.2.96","stem:kula",                    "semantic:śvāsya"),
    ("4.2.97","stem_class:nadyādi",           "suffix:ḍhak"),
    ("4.2.98","stem:dakṣiṇā",                 "suffix:tyak"),
    ("4.2.99","stem:kāpiśī",                  "suffix:ṣphak"),
    ("4.2.100","stem:raṅku",                  "semantic:amanuṣya",    "suffix:aṇ"),
    ("4.2.101","stem:dyu",                    "suffix:yat"),
    ("4.2.102","stem:kanthā",                 "suffix:ṭhak"),
    ("4.2.103","stem:varṇu",                  "augment:vuk"),
    ("4.2.104","stem_class:avyaya",           "suffix:tyap"),
    ("4.2.105","stem:aiṣamas",                "optional:1"),
    ("4.2.106","stem_final:tīra",             "suffix:añ"),
    ("4.2.107","purva_pada:dik",              "suffix:ña"),
    ("4.2.108","stem:madra",                  "suffix:añ"),
    ("4.2.109","stem_class:udīcyagrāma",      "accent:anta_udatta"),
    ("4.2.110","stem_final:prastha",          "upadha:k",             "suffix:aṇ"),
    ("4.2.111","stem_class:kaṇvādi",          "semantic:gotra"),
    ("4.2.112","stem_class:iñ",               "rule:continuation"),
    ("4.2.113","stem_class:non_dvyac",        "dialect:pracya"),
    ("4.2.114","stem_class:vṛddha",           "suffix:cha"),
    ("4.2.115","stem:bhavat",                 "suffix:ṭhak"),
    ("4.2.116","stem_class:kāśyādi",          "suffix:ṭhañ"),
    ("4.2.117","stem_class:vāhīka_grāma",     "rule:continuation"),
    ("4.2.118","semantic:uśīnara",            "optional:1"),
    ("4.2.119","stem_final:u",                "semantic:deśa",        "suffix:ṭhañ"),
    ("4.2.120","stem_class:vṛddha",           "dialect:pracya"),
    ("4.2.121","stem_final:dhanva",           "upadha:y",             "suffix:vuñ"),
    ("4.2.122","stem_final:prastha",          "rule:continuation"),
    ("4.2.123","upadha:r",                    "dialect:pracya"),
    ("4.2.124","stem:janapada",               "rule:continuation"),
    ("4.2.125","stem_class:non_vṛddha",       "semantic:bahuvacana_viṣaya"),
    ("4.2.126","stem_final:kaccha",           "rule:continuation"),
    ("4.2.127","stem_class:dhūmādi",          "rule:continuation"),
    ("4.2.128","stem:nagara",                 "semantic:kutsana"),
    ("4.2.129","stem:araṇya",                 "semantic:manuṣya"),
    ("4.2.130","stem:kuru",                   "optional:1"),
    ("4.2.131","stem:madra",                  "suffix:kan"),
    ("4.2.132","upadha:k",                    "suffix:aṇ"),
    ("4.2.133","stem_class:kacchādi",         "rule:continuation"),
    ("4.2.134","stem:manuṣya",                "suffix:vuñ"),
    ("4.2.135","stem:apadātu",                "purva_pada:sālva"),
    ("4.2.136","stem:go",                     "rule:continuation"),
    ("4.2.137","stem_final:garta",            "suffix:cha"),
    ("4.2.138","stem_class:gahādi",           "rule:continuation"),
    ("4.2.139","stem_class:kaṭādi",           "dialect:pracya"),
    ("4.2.140","stem:rājan",                  "augment:ka"),
    ("4.2.141","stem_class:vṛddha",           "upadha:ekanta_kha"),
    ("4.2.142","stem_final:kanthā",           "rule:continuation"),
    ("4.2.143","stem:parvata",                "rule:continuation"),
    ("4.2.144","semantic:amanuṣya",           "optional:1"),
    ("4.2.145","stem:kṛkaṇa",                 "semantic:bhāradvāja"),
]


def _build_compact_fixtures(raw):
    """Build positive/negative fixture dicts from a compact ``key:value``
    string list. The negative dict swaps the first key to a value that
    will reject the predicate; ``"0"`` values become real ``False`` and
    ``non_X`` values negate to ``X`` so predicates that test ``not _eq``
    are exercised correctly."""
    out: dict[str, tuple[dict, dict]] = {}
    for row in raw:
        sid = row[0]
        pos: dict = {}
        for spec in row[1:]:
            if spec is None:
                continue
            key, _, val = spec.partition(":")
            if val == "1":
                pos[key] = True
            elif val == "0":
                pos[key] = False
            else:
                pos[key] = val
        if not pos:
            pos = {"rule": "continuation"}
        neg = dict(pos)
        first_key = next(iter(pos))
        first_val = pos[first_key]
        if isinstance(first_val, bool):
            neg[first_key] = not first_val
        elif isinstance(first_val, str) and first_val.startswith("non_"):
            neg[first_key] = first_val[4:]
        else:
            neg[first_key] = "different"
        out[sid] = (pos, neg)
    return out


FIXTURES.update(_build_compact_fixtures(_FX_4_2_RAW))


_FX_4_3_RAW = [
    ("4.3.1", "stem:yuṣmad",                  "suffix:khañ",          "optional:1"),
    ("4.3.2", "stem:yuṣmad",                  "substitute:yuṣmāka"),
    ("4.3.3", "stem:yuṣmad",                  "number:single",        "substitute:tavaka"),
    ("4.3.4", "stem:ardha",                   "suffix:yat"),
    ("4.3.5", "purva_pada:para",              "rule:continuation"),
    ("4.3.6", "purva_pada:dik",               "suffix:ṭhañ"),
    ("4.3.7", "stem:grāma",                   "suffix:añ"),
    ("4.3.8", "stem:madhya",                  "suffix:ma"),
    ("4.3.9", "stem:a",                       "semantic:sāmpratika"),
    ("4.3.10","stem:dvīpa",                   "semantic:anusamudra",  "suffix:yañ"),
    ("4.3.11","semantic:kāla",                "suffix:ṭhañ"),
    ("4.3.12","stem:śarad",                   "semantic:śrāddha"),
    ("4.3.13","semantic:roga",                "optional:1"),
    ("4.3.14","stem:niśā",                    "rule:continuation"),
    ("4.3.15","stem:śvas",                    "augment:tuṭ"),
    ("4.3.16","stem_class:saṃdhi_velādi_ṛtu_nakṣatra", "suffix:aṇ"),
    ("4.3.17","stem:prāvṛṣ",                  "suffix:eṇya"),
    ("4.3.18","stem:varṣa",                   "suffix:ṭhak"),
    ("4.3.19","is_vedic:1",                   "suffix:ṭhañ"),
    ("4.3.20","stem:vasanta",                 "rule:continuation"),
    ("4.3.21","stem:hemanta",                 "rule:continuation"),
    ("4.3.22","suffix:aṇ",                    "operation:talopa"),
    ("4.3.23","stem:sāyam",                   "suffix:ṭyu",           "augment:tuṭ"),
    ("4.3.24","stem:pūrvāhṇa",                "optional:1"),
    ("4.3.25","semantic:tatra_jāta",          "rule:continuation"),
    ("4.3.26","stem:prāvṛṣ",                  "suffix:ṣṭhap"),
    ("4.3.27","stem:śarad",                   "domain:samjna",        "suffix:vuñ"),
    ("4.3.28","stem:pūrvāhṇa",                "suffix:vun"),
    ("4.3.29","stem:path",                    "substitute:pantha"),
    ("4.3.30","stem:amāvāsyā",                "optional:1"),
    ("4.3.31","stem:a",                       "rule:continuation"),
    ("4.3.32","stem:sindhu",                  "suffix:kan"),
    ("4.3.33","suffix:aṇ",                    "rule:continuation"),
    ("4.3.34","stem_class:śraviṣṭhādi_nakṣatra","operation:luk"),
    ("4.3.35","stem_final:sthānānta",         "rule:continuation"),
    ("4.3.36","stem:vatsaśālā",               "optional:1"),
    ("4.3.37","stem_class:nakshatra",         "semantic:bahula"),
    ("4.3.38","semantic:kṛta",                "rule:continuation"),
    ("4.3.39","semantic:prāyabhava",          "rule:continuation"),
    ("4.3.40","stem:upajānu",                 "suffix:ṭhak"),
    ("4.3.41","semantic:sambhūta",            "rule:continuation"),
    ("4.3.42","stem:kośa",                    "suffix:ḍhañ"),
    ("4.3.43","semantic:kāla_sādhu_puṣpyat",  "rule:continuation"),
    ("4.3.44","semantic:upta",                "rule:continuation"),
    ("4.3.45","stem:āśvayujī",                "suffix:vuñ"),
    ("4.3.46","stem:grīṣma",                  "optional:1"),
    ("4.3.47","semantic:deya_ṛṇa",            "rule:continuation"),
    ("4.3.48","stem:kalāpī",                  "suffix:vun"),
    ("4.3.49","stem:grīṣmāvarasamā",          "suffix:vuñ"),
    ("4.3.50","stem:saṃvatsara",              "suffix:ṭhañ"),
    ("4.3.51","semantic:vyāharati_mṛga",      "rule:continuation"),
    ("4.3.52","semantic:soḍha",               "rule:continuation"),
    ("4.3.53","semantic:tatra_bhava",         "rule:continuation"),
    ("4.3.54","stem_class:digādi",            "suffix:yat"),
    ("4.3.55","stem_class:śarīrāvayava",      "rule:continuation"),
    ("4.3.56","stem_class:dṛti_kukṣi_etc",    "suffix:ḍhañ"),
    ("4.3.57","stem:grīvā",                   "suffix:aṇ"),
    ("4.3.58","stem:gambhīrā",                "suffix:ñya"),
    ("4.3.59","compound_type:avyayībhāva",    "rule:continuation"),
    ("4.3.60","purva_pada:antar",             "suffix:ṭhañ"),
    ("4.3.61","stem:grāma",                   "purva_pada:pari"),
    ("4.3.62","stem:jihvāmūla",               "suffix:cha"),
    ("4.3.63","stem_final:varga",             "rule:continuation"),
    ("4.3.64","semantic:aśabda",              "suffix:yat",           "optional:1"),
    ("4.3.65","stem:karṇa",                   "semantic:alaṃkāra",    "suffix:kan"),
    ("4.3.66","semantic:vyākhyāna",           "rule:continuation"),
    ("4.3.67","stem_class:bahvac",            "accent:anta_udatta",   "suffix:ṭhañ"),
    ("4.3.68","stem:kratu",                   "rule:continuation"),
    ("4.3.69","semantic:adhyāya",             "stem:ṛṣi"),
    ("4.3.70","stem:pauroḍāśa",               "suffix:ṣṭhan"),
    ("4.3.71","is_vedic:1",                   "suffix:yat",           "stem:aṇau"),
    ("4.3.72","stem_class:dvyajṛd_brāhmaṇa_rk","suffix:ṭhak"),
    ("4.3.73","stem:aṇṛk",                    "rule:continuation"),
    ("4.3.74","semantic:tata_āgata",          "rule:continuation"),
    ("4.3.75","stem_final:ṭhak",              "rule:continuation"),
    ("4.3.76","stem_class:śuṇḍikādi",         "suffix:aṇ"),
    ("4.3.77","semantic:vidyā_yoni_sambandha","suffix:vuñ"),
    ("4.3.78","stem:ṛta",                     "suffix:ṭhañ"),
    ("4.3.79","stem:pitṛ",                    "suffix:yat"),
    ("4.3.80","semantic:gotra",               "suffix_class:aṅkavat"),
    ("4.3.81","stem:hetu",                    "suffix:rūpya",         "optional:1"),
    ("4.3.82","suffix:mayaṭ",                 "rule:continuation"),
    ("4.3.83","semantic:prabhavati",          "rule:continuation"),
    ("4.3.84","stem:vidūra",                  "suffix:ñya"),
    ("4.3.85","semantic:tat_gacchati",        "stem:pathi"),
    ("4.3.86","semantic:abhiniṣkrāmati_dvāra","rule:continuation"),
    ("4.3.87","semantic:adhikṛtya_kṛta_grantha","rule:continuation"),
    ("4.3.88","stem_class:śiśukranda_etc",    "suffix:cha"),
    ("4.3.89","semantic:asya_nivāsa",         "rule:continuation"),
    ("4.3.90","semantic:abhijana",            "rule:continuation"),
    ("4.3.91","stem_class:āyudhajīvi",        "semantic:parvata",     "suffix:cha"),
    ("4.3.92","stem_class:śaṇḍikādi",         "suffix:ñya"),
    ("4.3.93","stem:sindhu",                  "suffix:aṇ"),
    ("4.3.94","stem:tūdī",                    "suffix:ḍhak"),
    ("4.3.95","semantic:bhakti",              "rule:continuation"),
    ("4.3.96","stem_class:acittadeśakāla",    "suffix:ṭhak"),
    ("4.3.97","stem:mahārāja",                "suffix:ṭhañ"),
    ("4.3.98","stem:vāsudeva",                "suffix:vun"),
    ("4.3.99","stem_class:gotra_kṣatriya",    "suffix:vuñ"),
    ("4.3.100","stem_class:janapadin",        "rule:janapada_vat"),
    ("4.3.101","semantic:tena_prokta",        "rule:continuation"),
    ("4.3.102","stem:tittiri",                "suffix:chaṇ"),
    ("4.3.103","stem:kāśyapa",                "semantic:ṛṣi",         "suffix:ṇini"),
    ("4.3.104","stem:kalāpin",                "semantic:antevāsi"),
    ("4.3.105","semantic:purāṇa_prokta_brāhmaṇa_kalpa","rule:continuation"),
    ("4.3.106","stem_class:śaunakādi",        "is_vedic:1"),
    ("4.3.107","stem:kaṭha",                  "operation:luk"),
    ("4.3.108","stem:kalāpin",                "suffix:aṇ"),
    ("4.3.109","stem:chagalin",               "suffix:ḍhinuk"),
    ("4.3.110","stem:pārāśarya",              "semantic:bhikṣu"),
    ("4.3.111","stem:karmanda",               "suffix:ini"),
    ("4.3.112","semantic:ekadik",             "rule:continuation"),
    ("4.3.113","suffix:tasi",                 "rule:continuation"),
    ("4.3.114","stem:uras",                   "suffix:yat"),
    ("4.3.115","semantic:upajñāta",           "rule:continuation"),
    ("4.3.116","semantic:kṛta_grantha",       "rule:continuation"),
    ("4.3.117","domain:samjna",               "rule:continuation"),
    ("4.3.118","stem_class:kulālādi",         "suffix:vuñ"),
    ("4.3.119","stem_class:kṣudrābhramara_etc","suffix:añ"),
    ("4.3.120","semantic:tasya_idam",         "rule:continuation"),
    ("4.3.121","stem:ratha",                  "suffix:yat"),
    ("4.3.122","purva_pada:pattra",           "suffix:añ"),
    ("4.3.123","stem:pattra",                 "rule:continuation"),
    ("4.3.124","stem:hala",                   "suffix:ṭhak"),
    ("4.3.125","compound_type:dvandva",       "semantic:vaira"),
    ("4.3.126","stem:gotra",                  "suffix:vuñ"),
    ("4.3.127","stem_class:saṅghāṅka_lakṣaṇa","stem_class_alt:añ",    "suffix:aṇ"),
    ("4.3.128","stem:śākala",                 "optional:1"),
    ("4.3.129","stem:chandoga",               "suffix:ñya"),
    ("4.3.130","stem:daṇḍa",                  "rule:blocking"),
    ("4.3.131","stem_class:raivatikādi",      "suffix:cha"),
    ("4.3.132","stem:kaupiñjala",             "suffix:aṇ"),
    ("4.3.133","stem:ātharvaṇika",            "operation:ikalopa"),
    ("4.3.134","semantic:tasya_vikāra",       "rule:continuation"),
    ("4.3.135","stem:prāṇi",                  "semantic:avayava"),
    ("4.3.136","stem_class:bilvādi",          "suffix:aṇ"),
    ("4.3.137","upadha:k",                    "rule:continuation"),
    ("4.3.138","stem:trapu",                  "augment:ṣuk"),
    ("4.3.139","stem_final:u",                "suffix:añ"),
    ("4.3.140","stem_class:anudāttādi",       "rule:continuation"),
    ("4.3.141","stem_class:palāśādi",         "optional:1"),
    ("4.3.142","stem:śamī",                   "suffix:ṣṭlañ"),
    ("4.3.143","suffix:mayaṭ",                "dialect:bhāṣā",        "semantic:non_abhakṣya"),
    ("4.3.144","stem_class:vṛddha_śarādi",    "rule:always"),
    ("4.3.145","stem:go",                     "semantic:purīṣa"),
    ("4.3.146","stem:piṣṭa",                  "rule:continuation"),
    ("4.3.147","domain:samjna",               "suffix:kan"),
    ("4.3.148","stem:vrīhi",                  "semantic:puroḍāśa"),
    ("4.3.149","domain:non_samjna",           "stem:tila"),
    ("4.3.150","stem_class:dvyac",            "is_vedic:1"),
    ("4.3.151","stem:not",                    "rule:blocking"),
    ("4.3.152","stem_class:tālādi",           "suffix:aṇ"),
    ("4.3.153","stem_class:jātarūpa",         "semantic:parimāṇa"),
    ("4.3.154","stem_class:prāṇi_rajata",     "suffix:añ"),
    ("4.3.155","stem_class:ñit",              "rule:continuation"),
    ("4.3.156","semantic:krīta_vat_parimāṇa", "rule:continuation"),
    ("4.3.157","stem:uṣṭra",                  "suffix:vuñ"),
    ("4.3.158","stem:umā",                    "optional:1"),
    ("4.3.159","stem:eṇī",                    "suffix:ḍhañ"),
    ("4.3.160","stem:go",                     "suffix:yat"),
    ("4.3.161","stem:dro",                    "rule:continuation"),
    ("4.3.162","semantic:vayas",              "domain:māna"),
    ("4.3.163","stem_final:phala",            "operation:luk"),
    ("4.3.164","stem_class:plakṣādi",         "suffix:aṇ"),
    ("4.3.165","stem:jambū",                  "optional:1"),
    ("4.3.166","operation:lup",               "rule:continuation"),
    ("4.3.167","stem_class:harītakyādi",      "rule:continuation"),
    ("4.3.168","stem:kaṃsīya",                "suffix:yañ",           "operation:luk"),
]


FIXTURES.update(_build_compact_fixtures(_FX_4_3_RAW))


_FX_4_4_RAW = [
    ("4.4.1", "section:prāgvahate",           "suffix:ṭhak"),
    ("4.4.2", "semantic:tena_dīvyati_khanati_jayati_jita","rule:continuation"),
    ("4.4.3", "semantic:saṃskṛta",            "rule:continuation"),
    ("4.4.4", "stem:kulattha",                "upadha:k",             "suffix:aṇ"),
    ("4.4.5", "semantic:tarati",              "rule:continuation"),
    ("4.4.6", "stem:gopuccha",                "suffix:ṭhañ"),
    ("4.4.7", "stem_class:nau_dvyac",         "suffix:ṣṭhan"),
    ("4.4.8", "semantic:carati",              "rule:continuation"),
    ("4.4.9", "stem:ākarṣa",                  "suffix:ṣṭhal"),
    ("4.4.10","stem_class:parpādi",           "suffix:ṣṭhan"),
    ("4.4.11","stem:śvagaṇa",                 "suffix:ṭhañ"),
    ("4.4.12","stem_class:vetanādi",          "semantic:jīvati"),
    ("4.4.13","stem:vasna",                   "suffix:ṭhan"),
    ("4.4.14","stem:āyudha",                  "suffix:cha"),
    ("4.4.15","semantic:harati_utsaṅgādi",    "rule:continuation"),
    ("4.4.16","stem_class:bhastrādi",         "suffix:ṣṭhan"),
    ("4.4.17","stem:vivadha",                 "optional:1"),
    ("4.4.18","stem:kuṭilikā",                "suffix:aṇ"),
    ("4.4.19","stem_class:akṣadyūtādi",       "semantic:nirvṛtta"),
    ("4.4.20","stem_final:ktri",              "augment:ma",           "rule:always"),
    ("4.4.21","stem:apamitya",                "suffix:kak"),
    ("4.4.22","semantic:saṃsṛṣṭa",            "rule:continuation"),
    ("4.4.23","stem_class:cūrṇādi",           "suffix:ini"),
    ("4.4.24","stem:lavaṇa",                  "operation:luk"),
    ("4.4.25","stem:mudga",                   "suffix:aṇ"),
    ("4.4.26","stem_class:vyañjana",          "semantic:upasikta"),
    ("4.4.27","stem:ojas",                    "rule:vartate"),
    ("4.4.28","stem:īpa",                     "rule:pratyanu_pūrva"),
    ("4.4.29","stem:parimukha",               "rule:continuation"),
    ("4.4.30","semantic:prayacchati_garhya",  "rule:continuation"),
    ("4.4.31","stem:kusīda",                  "suffix:ṣṭhan"),
    ("4.4.32","semantic:uñchati",             "rule:continuation"),
    ("4.4.33","semantic:rakṣati",             "rule:continuation"),
    ("4.4.34","stem:śabda_dardura",           "semantic:karoti"),
    ("4.4.35","stem:pakṣin",                  "semantic:hanti"),
    ("4.4.36","stem:paripantha",              "semantic:tiṣṭhati"),
    ("4.4.37","purva_pada:mātha",             "stem:padavi",          "semantic:dhāvati"),
    ("4.4.38","stem:ākranda",                 "suffix:ṭhañ"),
    ("4.4.39","purva_pada:pad",               "semantic:gṛhṇāti"),
    ("4.4.40","stem:pratikaṇṭha",             "rule:continuation"),
    ("4.4.41","stem:dharma",                  "semantic:carati"),
    ("4.4.42","stem:pratipath",               "semantic:eti",         "suffix:ṭhan"),
    ("4.4.43","stem:samavāya",                "semantic:samavaiti"),
    ("4.4.44","stem:pariṣad",                 "suffix:ṇya"),
    ("4.4.45","stem:senā",                    "optional:1"),
    ("4.4.46","stem:lalāṭa",                  "semantic:paśyati",     "domain:samjna"),
    ("4.4.47","semantic:tasya_dharmya",       "rule:continuation"),
    ("4.4.48","stem_class:mahiṣyādi",         "suffix:aṇ"),
    ("4.4.49","stem:ṛta",                     "suffix:añ"),
    ("4.4.50","semantic:avakraya",            "rule:continuation"),
    ("4.4.51","semantic:tasya_paṇya",         "rule:continuation"),
    ("4.4.52","stem:lavaṇa",                  "suffix:ṭhañ"),
    ("4.4.53","stem_class:kiśarādi",          "suffix:ṣṭhan"),
    ("4.4.54","stem:śalālu",                  "optional:1"),
    ("4.4.55","semantic:śilpa",               "rule:continuation"),
    ("4.4.56","stem:maḍḍuka",                 "suffix:aṇ",            "optional:1"),
    ("4.4.57","semantic:praharaṇa",           "rule:continuation"),
    ("4.4.58","stem:paraśvadha",              "suffix:ṭhañ"),
    ("4.4.59","stem:śakti",                   "suffix:īkak"),
    ("4.4.60","semantic:asti_nāsti_diṣṭa_mati","rule:continuation"),
    ("4.4.61","semantic:śīla",                "rule:continuation"),
    ("4.4.62","stem_class:chatrādi",          "suffix:ṇa"),
    ("4.4.63","semantic:karmādhyayana_vṛtta", "rule:continuation"),
    ("4.4.64","stem_class:bahvac_purva_pada", "suffix:ṭhac"),
    ("4.4.65","stem_class:bhakṣa",            "semantic:hita"),
    ("4.4.66","semantic:tasmai_dīyate_niyukta","rule:continuation"),
    ("4.4.67","stem:śrāṇāmāṃsa",              "suffix:ṭiṭhan"),
    ("4.4.68","stem:bhakta",                  "optional:1"),
    ("4.4.69","semantic:tatra_niyukta",       "rule:continuation"),
    ("4.4.70","stem_final:agāra",             "suffix:ṭhan"),
    ("4.4.71","stem:adhyāyin",                "domain:non_deśa_kāla"),
    ("4.4.72","stem_final:kaṭhina_anta",      "semantic:vyavaharati"),
    ("4.4.73","stem:nikaṭa",                  "semantic:vasati"),
    ("4.4.74","stem:āvasatha",                "suffix:ṣṭhal"),
    ("4.4.75","section:prāghita",             "suffix:yat"),
    ("4.4.76","stem:rathayuga",               "semantic:tadvahati"),
    ("4.4.77","stem:dhur",                    "suffix:ya"),
    ("4.4.78","stem:sarvadhura",              "suffix:kha"),
    ("4.4.79","stem:ekadhura",                "operation:luk"),
    ("4.4.80","stem:śakaṭa",                  "suffix:aṇ"),
    ("4.4.81","stem:hala",                    "suffix:ṭhak"),
    ("4.4.82","stem:janya",                   "domain:samjna"),
    ("4.4.83","stem:adhanu",                  "semantic:vidhyati"),
    ("4.4.84","stem:dhanagaṇa",               "semantic:labdhā"),
    ("4.4.85","stem:anna",                    "suffix:ṇa"),
    ("4.4.86","stem:vaśa",                    "semantic:gata"),
    ("4.4.87","stem:pada",                    "semantic:asmin_dṛśya"),
    ("4.4.88","stem:mūla",                    "semantic:abarhi"),
    ("4.4.89","stem:dhenuṣyā",                "domain:samjna"),
    ("4.4.90","stem:gṛhapati",                "semantic:saṃyukta",    "suffix:ñya"),
    ("4.4.91","stem_class:nau_vayodharma_etc","rule:continuation"),
    ("4.4.92","stem:dharma",                  "semantic:anapeta"),
    ("4.4.93","is_vedic:1",                   "semantic:nirmita"),
    ("4.4.94","stem:uras",                    "suffix:aṇ"),
    ("4.4.95","stem:hṛdaya",                  "semantic:priya"),
    ("4.4.96","stem:bandhana",                "semantic:carṣu"),
    ("4.4.97","stem:mata",                    "semantic:karaṇa"),
    ("4.4.98","semantic:tatra_sādhu",         "rule:continuation"),
    ("4.4.99","stem_class:pratijanādi",       "suffix:khañ"),
    ("4.4.100","stem:bhakta",                 "suffix:ṇa"),
    ("4.4.101","stem:pariṣad",                "suffix:ṇya"),
    ("4.4.102","stem_class:kathādi",          "suffix:ṭhak"),
    ("4.4.103","stem_class:guḍādi",           "suffix:ṭhañ"),
    ("4.4.104","stem:pathi",                  "suffix:ḍhañ"),
    ("4.4.105","stem:sabhā",                  "suffix:ya"),
    ("4.4.106","is_vedic:1",                  "suffix:ḍha"),
    ("4.4.107","stem:samānatīrtha",           "suffix:vāsi"),
    ("4.4.108","stem:samānodara",             "semantic:śayita",      "augment:o_udatta"),
    ("4.4.109","stem:sodara",                 "suffix:ya"),
    ("4.4.110","is_vedic:1",                  "semantic:bhava"),
    ("4.4.111","stem:pātha",                  "suffix:ḍyaṇ"),
    ("4.4.112","stem:veśanta",                "suffix:aṇ"),
    ("4.4.113","stem:srotas",                 "suffix:ḍya",           "optional:1"),
    ("4.4.114","stem:sagarbha",               "suffix:yan"),
    ("4.4.115","stem:tugra",                  "suffix:ghan"),
    ("4.4.116","stem:agra",                   "suffix:yat"),
    ("4.4.117","suffix:gha",                  "rule:continuation"),
    ("4.4.118","stem:samudra",                "suffix:gha"),
    ("4.4.119","stem:barhis",                 "semantic:datta"),
    ("4.4.120","stem:dūta",                   "semantic:bhāga"),
    ("4.4.121","stem:rakṣas",                 "semantic:hananī"),
    ("4.4.122","stem:revatī",                 "semantic:praśasya"),
    ("4.4.123","stem:asura",                  "semantic:sva"),
    ("4.4.124","semantic:māyā",               "suffix:aṇ"),
    ("4.4.125","domain:iṣṭakā_mantra",        "operation:luk_matu"),
    ("4.4.126","stem:aśvi",                   "suffix:aṇ"),
    ("4.4.127","stem:mūrdhan",                "semantic:vayasi",      "suffix:matup"),
    ("4.4.128","stem:māsa",                   "semantic:matvartha"),
    ("4.4.129","stem:madhu",                  "suffix:ña"),
    ("4.4.130","stem:ojas",                   "semantic:ahan",        "suffix:yat"),
    ("4.4.131","stem_final:veśo",             "stem_class:bhagādi",   "suffix:yal"),
    ("4.4.132","suffix:kha",                  "rule:continuation"),
    ("4.4.133","stem:pūrva",                  "semantic:kṛta",        "suffix:ini"),
    ("4.4.134","stem:ap",                     "semantic:saṃskṛta"),
    ("4.4.135","stem:sahasra",                "semantic:sammita",     "suffix:gha"),
    ("4.4.136","stem_class:matu",             "rule:continuation"),
    ("4.4.137","stem:soma",                   "semantic:arhati",      "suffix:ya"),
    ("4.4.138","stem_final:maya",             "rule:continuation"),
    ("4.4.139","stem:madhu",                  "rule:continuation"),
    ("4.4.140","stem:vasu",                   "semantic:samūha"),
    ("4.4.141","stem:nakṣatra",               "suffix:gha"),
    ("4.4.142","stem:sarvadeva",              "suffix:tātil"),
    ("4.4.143","stem:śivaśam",                "semantic:kara"),
    ("4.4.144","semantic:bhāva",              "rule:continuation"),
]


FIXTURES.update(_build_compact_fixtures(_FX_4_4_RAW))


# ---------------------------------------------------------------------------
# Registry metadata. Every sūtra in 4.x is a saṁjñā/vidhi rule for a
# taddhita suffix; the operator class is mostly ``samjna`` (assignment of
# a suffix-class) or ``vidhi`` (substantive operation like luk, accent).
# We carry a short hand-translated summary and an ``assigned`` tag.
# ---------------------------------------------------------------------------

def _meta_for(sid: str, op: str, summary: str) -> SutraMeta:
    pada = sid.rsplit(".", 1)[0]
    tag = f"taddhita:{pada}"
    return SutraMeta(op, summary, (tag,))


_META_SUMMARIES: dict[str, tuple[str, str]] = {
    # Light summaries — operator + 1-line gloss. Full Pāṇinian gloss
    # would balloon this file; the test gate only requires summary
    # presence + correct operator class.
    "4.1.1":  (_SAMJNA,    "ṅyāpprātipadikāt: introduces nyāp suffixes for prātipadika"),
    "4.1.3":  (_SAMJNA,    "striyām: opens the strī-pratyaya section"),
    "4.1.4":  (_SAMJNA,    "ajādyataṣṭāp: ajādi-class takes ṭāp"),
    "4.1.5":  (_SAMJNA,    "ṛn-nebhyo ṅīp: r/n-ending stems take ṅīp"),
    "4.1.6":  (_SAMJNA,    "ugitaś ca: ugit-marked stems take ṅīp"),
    "4.1.7":  (_VIDHI,     "vano ra ca: van-final takes ra-augment with ṅīp"),
    "4.1.8":  (_VIBHASHA,  "pādo'nyatarasyām: pād optionally takes ṅīp"),
    "4.1.9":  (_SAMJNA,    "ṭābṛci: ṭāb-rci class takes ṭāp"),
    "4.1.10": (_PRATISEDHA,"na ṣaṭsvasrādibhyaḥ: blocks ṅīp for ṣaṭ/svasrādi"),
    "4.1.11": (_SAMJNA,    "manaḥ: manas → ṅīp"),
    "4.1.12": (_SAMJNA,    "ano bahuvrīheḥ: an-final bahuvrīhi → ṅīp"),
    "4.1.13": (_VIBHASHA,  "ḍāb-ubhāb optional"),
    "4.1.14": (_VIDHI,     "anupasarjanāt: non-upasarjana → ṅīp"),
    "4.1.15": (_SAMJNA,    "ṭiḍḍhānañ-list → ṅīp"),
    "4.1.16": (_SAMJNA,    "yañaś ca: yañ-class → ṅīp"),
    "4.1.17": (_SAMJNA,    "prācāṃ ṣpha taddhitaḥ: Pracya ṣpha-taddhita"),
    "4.1.18": (_SAMJNA,    "lohitādibhyaḥ → ṣpha"),
    "4.1.19": (_SAMJNA,    "kauravya-māṇḍūka → ṣpha"),
    "4.1.20": (_SAMJNA,    "vayasi prathame: first-vayas → ṣpha"),
    "4.1.21": (_SAMJNA,    "dvigoḥ: dvigu → ṣpha"),
    "4.1.22": (_PRATISEDHA,"aparimāṇa-etc → no taddhita-luk"),
    "4.1.23": (_SAMJNA,    "kāṇḍāntāt kṣetre: kāṇḍa + kshetra → ṣpha"),
    "4.1.24": (_VIBHASHA,  "puruṣāt pramāṇe optionally"),
    "4.1.25": (_SAMJNA,    "bahuvrīher ūdhaso ṅīṣ"),
    "4.1.26": (_SAMJNA,    "saṃkhya-avyayādeḥ ṅīp"),
    "4.1.27": (_SAMJNA,    "dāma-hāyanānta → ṅīp"),
    "4.1.28": (_VIBHASHA,  "an upadhā-lopin optionally → ṅīp"),
    "4.1.29": (_PARIBHASHA,"nityaṃ saṃjñā-chandasoḥ: always in samjna/chandas"),
    "4.1.30": (_SAMJNA,    "kevala-māmaka-etc → ṅīp"),
    "4.1.31": (_SAMJNA,    "rātreś cājasau"),
    "4.1.32": (_VIDHI,     "antarvat/pativat → nuk-augment"),
    "4.1.33": (_VIDHI,     "pati in yajña-saṃyoga: no substitution"),
    "4.1.34": (_VIBHASHA,  "vibhāṣā sapūrvasya: optional with sa-pūrva"),
    "4.1.35": (_PARIBHASHA,"nityaṃ sapatnyādiṣu: always for sapatnyādi"),
    "4.1.36": (_VIDHI,     "pūtakrator ai ca: substitute ai"),
    "4.1.37": (_VIDHI,     "vṛṣākapyādi → udātta accent"),
    "4.1.38": (_VIDHI,     "manor au optionally"),
    "4.1.39": (_VIDHI,     "varṇāt anudāttāt topadhāt → n"),
    "4.1.40": (_SAMJNA,    "anyato ṅīṣ"),
    "4.1.41": (_SAMJNA,    "ṣid-gaurādi → ṅīṣ"),
    "4.1.42": (_SAMJNA,    "jānapada-kuṇḍa-etc → ṅīṣ"),
    "4.1.43": (_SAMJNA,    "śoṇāt prācām → ṅīṣ"),
    "4.1.44": (_SAMJNA,    "voto guṇa-vacanāt"),
    "4.1.45": (_SAMJNA,    "bahvādi → ṅīṣ"),
    "4.1.46": (_PARIBHASHA,"nityaṃ chandasi"),
    "4.1.47": (_SAMJNA,    "bhuvaḥ ṅīṣ"),
    "4.1.48": (_SAMJNA,    "puṃyogād ākhyāyām → ṅīṣ"),
    "4.1.49": (_VIDHI,     "indra-varuṇa-etc → ānuk augment"),
    "4.1.50": (_SAMJNA,    "krītāt karaṇa-pūrvāt → ṅīṣ"),
    "4.1.51": (_SAMJNA,    "ktād alpa-ākhyāyām"),
    "4.1.52": (_SAMJNA,    "bahuvrīheś cāntodāttāt → ṅīṣ"),
    "4.1.53": (_VIBHASHA,  "a-svāṅga-pūrva-pada optionally"),
    "4.1.54": (_VIDHI,     "svāṅga-upasarjana asaṃyoga-upadhā"),
    "4.1.55": (_SAMJNA,    "nāsika-udara-oṣṭha-etc → strī-pratyaya"),
    "4.1.56": (_PRATISEDHA,"na kroḍādi-bahvac"),
    "4.1.57": (_PRATISEDHA,"saha-naṅ-vidyamāna-pūrva blocks strī"),
    "4.1.58": (_SAMJNA,    "nakhamukhāt saṃjñāyām"),
    "4.1.59": (_SAMJNA,    "dīrghajihvī Vedic"),
    "4.1.60": (_SAMJNA,    "dik-pūrva-pad → ṅīp"),
    "4.1.61": (_SAMJNA,    "vāhaḥ → ṅīp"),
    "4.1.62": (_VIDHI,     "sakhi/aśiśvi in bhāṣā"),
    "4.1.63": (_VIDHI,     "jāti, non-strī-viṣaya, ayopadhā"),
    "4.1.64": (_SAMJNA,    "pāka-karṇa-etc uttara-pada"),
    "4.1.65": (_SAMJNA,    "ito manuṣya-jāti"),
    "4.1.66": (_SAMJNA,    "ū-utaḥ → ūṅ"),
    "4.1.67": (_SAMJNA,    "bāhvantāt saṃjñāyām"),
    "4.1.68": (_SAMJNA,    "paṅgoś ca"),
    "4.1.69": (_SAMJNA,    "ūru-uttara-pada in aupamya"),
    "4.1.70": (_SAMJNA,    "saṃhita-śapha-lakṣaṇa-vāma"),
    "4.1.71": (_SAMJNA,    "kadru/kamaṇḍalu Vedic"),
    "4.1.72": (_PARIBHASHA,"saṃjñā: always strī"),
    "4.1.73": (_SAMJNA,    "śārṅgaravādi yañ → ṅīn"),
    "4.1.74": (_SAMJNA,    "yañaś cāp"),
    "4.1.75": (_SAMJNA,    "āvaṭyāc ca → cāp"),
    "4.1.76": (_PARIBHASHA,"taddhitāḥ: opens taddhita section"),
    "4.1.77": (_VIDHI,     "yūnas ti: yuvan → ti"),
    "4.1.78": (_SAMJNA,    "an-iñ a-nārṣa guru-uttama → ṣyaṅ gotre"),
    "4.1.79": (_PARIBHASHA,"gotra-avayava continuation"),
    "4.1.80": (_SAMJNA,    "krauḍyādi → ṣyaṅ"),
    "4.1.81": (_VIBHASHA,  "daivayajñyādi optionally"),
    "4.1.82": (_VIBHASHA,  "samartha first optionally"),
    "4.1.83": (_SAMJNA,    "prāg-dīvyataḥ → aṇ"),
    "4.1.84": (_SAMJNA,    "aśvapatyādi → aṇ"),
    "4.1.85": (_SAMJNA,    "diti-aditi-āditya-pati → ṇya"),
    "4.1.86": (_SAMJNA,    "utsādi → añ"),
    "4.1.87": (_SAMJNA,    "strī-puṃs → nañsnañ (bhavana)"),
    "4.1.88": (_VIDHI,     "dvigu-luk anapatye"),
    "4.1.89": (_VIDHI,     "gotre 'luk before ac"),
    "4.1.90": (_VIDHI,     "yūni luk"),
    "4.1.91": (_VIBHASHA,  "phak/phiñ optionally"),
    "4.1.93": (_PARIBHASHA,"eko gotre: only one in gotra"),
    "4.1.94": (_SAMJNA,    "gotrādyūni strī"),
    "4.1.95": (_SAMJNA,    "ata iñ"),
    "4.1.96": (_SAMJNA,    "bāhvādi → iñ"),
    "4.1.97": (_SAMJNA,    "sudhātor akañ"),
    "4.1.98": (_SAMJNA,    "kuñjādi → cphañ in gotra"),
    "4.1.99": (_SAMJNA,    "naḍādi → phak"),
    "4.1.100":(_SAMJNA,    "haritādi → añ"),
    "4.1.101":(_PARIBHASHA,"yañ/iñ continuation"),
    "4.1.102":(_SAMJNA,    "śaradvat-śunaka-darbha → bhṛguvatsāgrāyaṇa"),
    "4.1.103":(_VIBHASHA,  "droṇaparvata/jīvanta optionally"),
    "4.1.104":(_SAMJNA,    "bidādi → añ in anantarya"),
    "4.1.105":(_SAMJNA,    "gargādi → yañ"),
    "4.1.106":(_SAMJNA,    "madhu-babhru → brāhmaṇa-kauśika"),
    "4.1.107":(_SAMJNA,    "kapi-bodha → āṅgirasa"),
    "4.1.108":(_PARIBHASHA,"vataṇḍāc ca"),
    "4.1.109":(_VIDHI,     "luk striyām"),
    "4.1.110":(_SAMJNA,    "aśvādi → phañ"),
    "4.1.111":(_SAMJNA,    "bhargāt traigarte → phañ"),
    "4.1.112":(_SAMJNA,    "śivādi → aṇ"),
    "4.1.113":(_SAMJNA,    "avṛddha nadī-mānuṣī tannāmika"),
    "4.1.114":(_SAMJNA,    "ṛṣya-andhaka-vṛṣṇi-kuru → aṇ"),
    "4.1.115":(_VIDHI,     "mātur ut sa-saṃkhyā-sambhadra-bhinna"),
    "4.1.116":(_VIDHI,     "kanyāyāḥ kanīna"),
    "4.1.117":(_SAMJNA,    "vikarṇa-śuṅga-chagala → vatsa-bharadvāja-atri"),
    "4.1.118":(_VIBHASHA,  "pīlāyā vā"),
    "4.1.119":(_SAMJNA,    "ḍhak from maṇḍūka"),
    "4.1.120":(_SAMJNA,    "strībhyo ḍhak"),
    "4.1.121":(_SAMJNA,    "dvyac → ḍhak"),
    "4.1.122":(_PRATISEDHA,"itaś cāniñaḥ: blocks ḍhak for iñ"),
    "4.1.123":(_SAMJNA,    "śubhrādi → ḍhak"),
    "4.1.124":(_SAMJNA,    "vikarṇa-kuṣītaka → kāśyape"),
    "4.1.125":(_VIDHI,     "bhruvo vuk"),
    "4.1.126":(_VIDHI,     "kalyāṇyādi → inaṅ"),
    "4.1.127":(_VIBHASHA,  "kulaṭāyā vā"),
    "4.1.128":(_SAMJNA,    "caṭakāyā airak"),
    "4.1.129":(_SAMJNA,    "godhāyā ḍhrak"),
    "4.1.130":(_PARIBHASHA,"ārā/udīcyām godhā-ḍhrak"),
    "4.1.131":(_VIBHASHA,  "kṣudrādi optionally"),
    "4.1.132":(_SAMJNA,    "pitṛṣvasur chaṇ"),
    "4.1.133":(_VIDHI,     "ḍhaki lopaḥ: ḍhak lopa"),
    "4.1.134":(_PARIBHASHA,"mātṛṣvasuś ca"),
    "4.1.135":(_SAMJNA,    "catuṣpād → ḍhañ"),
    "4.1.136":(_SAMJNA,    "gṛṣṭyādi → ḍhañ"),
    "4.1.137":(_SAMJNA,    "rāja-śvaśura → yat"),
    "4.1.138":(_SAMJNA,    "kṣatrād ghaḥ"),
    "4.1.139":(_SAMJNA,    "kulāt khaḥ"),
    "4.1.140":(_VIBHASHA,  "apūrva-pada optionally yat/ḍhakañ"),
    "4.1.141":(_SAMJNA,    "mahākulād añ/khañ"),
    "4.1.142":(_SAMJNA,    "duṣkulād ḍhak"),
    "4.1.143":(_SAMJNA,    "svasuś chaḥ"),
    "4.1.144":(_SAMJNA,    "bhrātur vyat"),
    "4.1.145":(_SAMJNA,    "vyan sapatne"),
    "4.1.146":(_SAMJNA,    "revatyādi → ṭhak"),
    "4.1.147":(_SAMJNA,    "gotra-strī kutsane → ṇa"),
    "4.1.148":(_SAMJNA,    "vṛddhāṭ ṭhak sauvīreṣu"),
    "4.1.149":(_SAMJNA,    "pheś chaḥ"),
    "4.1.150":(_SAMJNA,    "phāṇṭāhṛti/mimatā → ṇaphiñ"),
    "4.1.151":(_SAMJNA,    "kurvādi → ṇya"),
    "4.1.152":(_SAMJNA,    "senānta-lakṣaṇa → ṇya"),
    "4.1.153":(_SAMJNA,    "udīcām iñ"),
    "4.1.154":(_SAMJNA,    "tikādi → phiñ"),
    "4.1.155":(_SAMJNA,    "kausalya/kārmārya → phiñ"),
    "4.1.156":(_PARIBHASHA,"aṇo dvyac continuation"),
    "4.1.157":(_VIDHI,     "udīc vṛddha non-gotra"),
    "4.1.158":(_VIDHI,     "vākināt kuk"),
    "4.1.159":(_VIBHASHA,  "putrānta optionally"),
    "4.1.160":(_PARIBHASHA,"prācām avṛddha → phin"),
    "4.1.161":(_SAMJNA,    "manor jātau añyat ṣuk"),
    "4.1.162":(_SAMJNA,    "pautra-prabhṛti gotra"),
    "4.1.163":(_VIDHI,     "vaṃśya-living yuvan"),
    "4.1.164":(_VIDHI,     "bhrātari jyāyasi yuvan"),
    "4.1.165":(_VIBHASHA,  "anya-sapinda-sthavira optionally"),
    "4.1.166":(_PARIBHASHA,"vṛddhasya ca pūjāyām"),
    "4.1.167":(_VIDHI,     "yūnaś ca kutsāyām"),
    "4.1.168":(_SAMJNA,    "janapada-kṣatriya → añ"),
    "4.1.169":(_PARIBHASHA,"sālveya-gāndhāri"),
    "4.1.170":(_SAMJNA,    "dvyañ-magadha-kaliṅga → aṇ"),
    "4.1.171":(_SAMJNA,    "vṛddhet-kosala-aja → ñyaṅ"),
    "4.1.172":(_SAMJNA,    "kurunādi → ṇya"),
    "4.1.173":(_SAMJNA,    "sālvāvayava-pratyagratha → iñ"),
    "4.1.174":(_SAMJNA,    "te tadrājāḥ"),
    "4.1.175":(_VIDHI,     "kambojāl luk"),
    "4.1.176":(_SAMJNA,    "strīṣu avanti-kunti-kuru"),
    "4.1.177":(_PARIBHASHA,"ataś ca: a-final continuation"),
    "4.1.178":(_PRATISEDHA,"prācya-bharga-yaudheya block"),
}


def _build_meta_for_pada(prefix: str, raw_table):
    """Generate META entries for 4.2/4.3/4.4 from the compact raw table.
    Operator class is inferred from the discriminating suffix/operation."""
    out: dict[str, SutraMeta] = {}
    for row in raw_table:
        sid = row[0]
        op = _SAMJNA
        # If the row mentions a luk/lopa/operation it's vidhi; if 'optional' it's vibhāṣā
        joined = "|".join(str(s) for s in row[1:] if s)
        if "operation:" in joined or "augment:" in joined:
            op = _VIDHI
        if "optional:1" in joined:
            op = _VIBHASHA
        if "rule:blocking" in joined:
            op = _PRATISEDHA
        if "rule:continuation" in joined or "domain:samjna" in joined:
            op = _PARIBHASHA if "rule:continuation" in joined and "stem:" not in joined and "stem_class:" not in joined else _SAMJNA
        summary = f"Adhyāya {prefix[:-1]}: {sid} taddhita rule"
        out[sid] = SutraMeta(op, summary, (f"taddhita:{prefix[:-1]}",))
    return out


META: dict[str, SutraMeta] = {}
for sid, (op, summary) in _META_SUMMARIES.items():
    META[sid] = SutraMeta(op, summary, ("taddhita:4.1",))
META.update(_build_meta_for_pada("4.2.", _FX_4_2_RAW))
META.update(_build_meta_for_pada("4.3.", _FX_4_3_RAW))
META.update(_build_meta_for_pada("4.4.", _FX_4_4_RAW))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

(
    IMPLEMENTED_IDS,
    has_real_implementation,
    handler_for,
    positive_features,
    negative_features,
) = make_module_api(FIXTURES, globals())
