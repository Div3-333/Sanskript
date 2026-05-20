"""Discrete Pāṇinian predicates for the 553 Adhyāya-5 sūtras (pādas
5.1, 5.2, 5.3, 5.4) that were absent from the inline registry.

Adhyāya 5 continues the taddhita suite begun in Adhyāya 4 and adds the
matvarthīya/saṁjñā derivative block (5.2), the case-adverb / praśaṁsā
/ kutsana / krīḍā suffix block (5.3), and the samāsānta and bahuvrīhi
ending block (5.4). Each sūtra is encoded as a discrete one-line
predicate that checks the stem/semantic/suffix triple it prescribes;
fixtures fire on Pāṇini's canonical example and reject the near-miss.

This module is wired into the main truth-gate registry via
:func:`sutra_impl_base.register_module_in_registry`.
"""
from __future__ import annotations

from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api


_SAMJNA = "samjna"
_PARIBHASHA = "paribhasha"
_VIDHI = "vidhi"
_PRATISEDHA = "pratisedha"
_VIBHASHA = "vibhasha"


# ===========================================================================
# Adhyāya 5.1 — āhīya / krīta / arhati / bhāva taddhita (136 sūtras)
# ===========================================================================

def sutra_5_1_1(c)  : return _eq(c, "section", "prāk_krīta") and _eq(c, "suffix", "cha")
def sutra_5_1_2(c)  : return _eq(c, "stem_class", "ugavādi") and _eq(c, "suffix", "at")
def sutra_5_1_3(c)  : return _eq(c, "stem", "kambala") and _eq(c, "domain", "samjna")
def sutra_5_1_4(c)  : return _eq(c, "stem_class", "haviṣ_apūpādi") and bool(c.get("optional"))
def sutra_5_1_5(c)  : return _eq(c, "semantic", "tasmai_hita") and _eq(c, "rule", "continuation")
def sutra_5_1_6(c)  : return _eq(c, "stem_class", "śarīrāvayava") and _eq(c, "suffix", "yat")
def sutra_5_1_7(c)  : return _in(c, "stem", {"khala", "yava", "māṣa", "tila", "vṛṣa", "brahman"}) and _eq(c, "rule", "continuation")
def sutra_5_1_8(c)  : return _in(c, "stem", {"aja", "avi"}) and _eq(c, "suffix", "thyan")
def sutra_5_1_9(c)  : return _in(c, "stem_final", {"ātman", "viśvajana", "bhoga"}) and _eq(c, "suffix", "kha")
def sutra_5_1_10(c) : return _in(c, "stem", {"sarva", "puruṣa"}) and _in(c, "suffix", {"ṇa", "ḍhañ"})
def sutra_5_1_11(c) : return _in(c, "stem", {"māṇava", "caraka"}) and _eq(c, "suffix", "khañ")
def sutra_5_1_12(c) : return _eq(c, "semantic", "tadartha_vikṛti") and _eq(c, "rule", "continuation")
def sutra_5_1_13(c) : return _in(c, "stem", {"chadis", "upadhi", "bali"}) and _eq(c, "suffix", "ḍhañ")
def sutra_5_1_14(c) : return _in(c, "stem", {"ṛṣabha", "upānaha"}) and _eq(c, "suffix", "ñya")
def sutra_5_1_15(c) : return _eq(c, "stem", "carmaṇa") and _eq(c, "suffix", "añ")
def sutra_5_1_16(c) : return _eq(c, "semantic", "tad_asya_tad_asmin_syat") and _eq(c, "rule", "continuation")
def sutra_5_1_17(c) : return _eq(c, "stem", "parikhā") and _eq(c, "suffix", "ḍhañ")
def sutra_5_1_18(c) : return _eq(c, "section", "prāgvateḥ") and _eq(c, "suffix", "ṭhañ")
def sutra_5_1_19(c) : return _eq(c, "semantic", "ārha") and not _eq(c, "stem_class", "gopuccha_etc") and _eq(c, "suffix", "ṭhak")
def sutra_5_1_20(c) : return not bool(c.get("in_compound")) and _eq(c, "stem_class", "niṣkādi")
def sutra_5_1_21(c) : return _eq(c, "stem_final", "śata") and not _eq(c, "stem_final", "śata_ant") and _in(c, "suffix", {"ṭhan", "yat"})
def sutra_5_1_22(c) : return _eq(c, "stem_class", "saṅkhya_atiśadanta") and _eq(c, "suffix", "kan")
def sutra_5_1_23(c) : return _eq(c, "stem_class", "vatu") and _eq(c, "augment", "iḍ") and bool(c.get("optional"))
def sutra_5_1_24(c) : return _in(c, "stem", {"viṃśati", "triṃśat"}) and _eq(c, "suffix", "ḍvun")
def sutra_5_1_25(c) : return _eq(c, "stem", "kaṃsa") and _eq(c, "suffix", "ṭiṭhan")
def sutra_5_1_26(c) : return _eq(c, "stem", "śūrpa") and _eq(c, "suffix", "añ") and bool(c.get("optional"))
def sutra_5_1_27(c) : return _in(c, "stem", {"śatamāna", "viṃśatika", "sahasra", "vasana"}) and _eq(c, "suffix", "aṇ")
def sutra_5_1_28(c) : return _eq(c, "stem_class", "adhyardha_pūrva_dvigu") and _eq(c, "operation", "luk")
def sutra_5_1_29(c) : return _in(c, "stem", {"kārṣāpaṇa", "sahasra"}) and bool(c.get("optional"))
def sutra_5_1_30(c) : return _eq(c, "stem", "dvi_tri_pūrva_niṣka") and _eq(c, "rule", "continuation")
def sutra_5_1_31(c) : return _eq(c, "stem", "bista") and _eq(c, "rule", "continuation")
def sutra_5_1_32(c) : return _eq(c, "stem", "viṃśatika") and _eq(c, "suffix", "kha")
def sutra_5_1_33(c) : return _eq(c, "stem", "khārī") and _eq(c, "suffix", "īkan")
def sutra_5_1_34(c) : return _in(c, "stem", {"paṇa", "pāda", "māṣa", "śata"}) and _eq(c, "suffix", "at")
def sutra_5_1_35(c) : return _eq(c, "stem", "śāṇa") and bool(c.get("optional"))
def sutra_5_1_36(c) : return _eq(c, "stem_class", "dvi_tri_pūrva") and _eq(c, "suffix", "aṇ")
def sutra_5_1_37(c) : return _eq(c, "semantic", "tena_krīta") and _eq(c, "rule", "continuation")
def sutra_5_1_38(c) : return _eq(c, "semantic", "saṃyoga_utpāta") and _eq(c, "rule", "continuation")
def sutra_5_1_39(c) : return _eq(c, "stem_class", "go_dvyac_aśva") and _eq(c, "suffix", "yat")
def sutra_5_1_40(c) : return _eq(c, "stem", "putra") and _eq(c, "suffix", "cha")
def sutra_5_1_41(c) : return _in(c, "stem", {"sarvabhūmi", "pṛthivī"}) and _in(c, "suffix", {"aṇ", "añ"})
def sutra_5_1_42(c) : return _eq(c, "semantic", "tasya_īśvara") and _eq(c, "rule", "continuation")
def sutra_5_1_43(c) : return _eq(c, "semantic", "tatra_vidita") and _eq(c, "rule", "continuation")
def sutra_5_1_44(c) : return _in(c, "stem", {"loka", "sarvaloka"}) and _eq(c, "suffix", "ṭhañ")
def sutra_5_1_45(c) : return _eq(c, "semantic", "tasya_vāpa") and _eq(c, "rule", "continuation")
def sutra_5_1_46(c) : return _eq(c, "stem", "pātra") and _eq(c, "suffix", "ṣṭhan")
def sutra_5_1_47(c) : return _eq(c, "semantic", "vṛddhi_āya_lābha_śulka_upadā") and _eq(c, "rule", "continuation")
def sutra_5_1_48(c) : return _in(c, "stem", {"pūraṇa", "ardha"}) and _eq(c, "suffix", "ṭhan")
def sutra_5_1_49(c) : return _eq(c, "stem", "bhāga") and _eq(c, "suffix", "yat")
def sutra_5_1_50(c) : return _eq(c, "stem_class", "bhārādi_vaṃśādi") and _eq(c, "semantic", "harati")
def sutra_5_1_51(c) : return _in(c, "stem", {"vasna", "dravya"}) and _in(c, "suffix", {"ṭhan", "kan"})
def sutra_5_1_52(c) : return _eq(c, "semantic", "sambhavati_avaharati_pacati") and _eq(c, "rule", "continuation")
def sutra_5_1_53(c) : return _in(c, "stem", {"āḍhaka", "ācita", "pātra"}) and _eq(c, "suffix", "kha") and bool(c.get("optional"))
def sutra_5_1_54(c) : return _eq(c, "stem_class", "dvigu") and _eq(c, "suffix", "ṭhaṃś")
def sutra_5_1_55(c) : return _eq(c, "stem", "kulija") and _in(c, "operation", {"luk", "kha"})
def sutra_5_1_56(c) : return _eq(c, "semantic", "aṃśa_vasna_bhṛti") and _eq(c, "rule", "continuation")
def sutra_5_1_57(c) : return _eq(c, "semantic", "tad_asya_parimāṇa") and _eq(c, "rule", "continuation")
def sutra_5_1_58(c) : return _eq(c, "stem_class", "saṅkhya") and _in(c, "domain", {"samjna", "saṅgha", "sūtra", "adhyayana"})
def sutra_5_1_59(c) : return _eq(c, "stem_class", "saṅkhya_paṅkti") and _eq(c, "rule", "continuation")
def sutra_5_1_60(c) : return _in(c, "stem", {"pañcat", "daśat"}) and _eq(c, "semantic", "varga") and bool(c.get("optional"))
def sutra_5_1_61(c) : return _eq(c, "stem", "saptan") and _eq(c, "suffix", "añ") and bool(c.get("is_vedic"))
def sutra_5_1_62(c) : return _in(c, "stem", {"triṃśat", "catvāriṃśat"}) and _eq(c, "semantic", "brāhmaṇa") and _eq(c, "suffix", "ḍaṇ")
def sutra_5_1_63(c) : return _eq(c, "semantic", "tad_arhati") and _eq(c, "rule", "continuation")
def sutra_5_1_64(c) : return _eq(c, "stem_class", "chedādi") and _eq(c, "rule", "always")
def sutra_5_1_65(c) : return _eq(c, "stem_class", "śīrṣaccheda") and _eq(c, "suffix", "yat")
def sutra_5_1_66(c) : return _eq(c, "stem_class", "daṇḍādi") and _eq(c, "rule", "continuation")
def sutra_5_1_67(c) : return bool(c.get("is_vedic")) and _eq(c, "rule", "continuation")
def sutra_5_1_68(c) : return _eq(c, "stem", "pātra") and _eq(c, "suffix", "ghaṃś")
def sutra_5_1_69(c) : return _in(c, "stem", {"kaḍaṅgara", "dakṣiṇā"}) and _eq(c, "rule", "continuation")
def sutra_5_1_70(c) : return _eq(c, "stem", "sthālībila") and _eq(c, "rule", "continuation")
def sutra_5_1_71(c) : return _in(c, "stem", {"yajña", "ṛtvik"}) and _in(c, "suffix", {"gha", "khañ"})
def sutra_5_1_72(c) : return _in(c, "stem", {"pārāyaṇa", "turāyaṇa", "cāndrāyaṇa"}) and _eq(c, "semantic", "vartayati")
def sutra_5_1_73(c) : return _eq(c, "semantic", "saṃśaya_āpanna") and _eq(c, "rule", "continuation")
def sutra_5_1_74(c) : return _eq(c, "stem", "yojana") and _eq(c, "semantic", "gacchati")
def sutra_5_1_75(c) : return _eq(c, "stem", "path") and _eq(c, "suffix", "ṣkan")
def sutra_5_1_76(c) : return _eq(c, "stem", "pantha") and _eq(c, "suffix", "ṇa") and _eq(c, "rule", "always")
def sutra_5_1_77(c) : return _eq(c, "stem", "uttarapatha") and _eq(c, "semantic", "āhṛta")
def sutra_5_1_78(c) : return _eq(c, "semantic", "kāla") and _eq(c, "rule", "continuation")
def sutra_5_1_79(c) : return _eq(c, "semantic", "tena_nirvṛtta") and _eq(c, "rule", "continuation")
def sutra_5_1_80(c) : return _eq(c, "semantic", "tam_adhīṣṭa") and _eq(c, "rule", "continuation")
def sutra_5_1_81(c) : return _eq(c, "stem", "māsa") and _eq(c, "semantic", "vayas") and _in(c, "suffix", {"yat", "khañ"})
def sutra_5_1_82(c) : return _eq(c, "stem_class", "dvigu") and _eq(c, "suffix", "yap")
def sutra_5_1_83(c) : return _eq(c, "stem", "ṣaṇmāsa") and _eq(c, "suffix", "ṇyat")
def sutra_5_1_84(c) : return _eq(c, "semantic", "avayas") and _eq(c, "suffix", "ṭhaṃś")
def sutra_5_1_85(c) : return _eq(c, "stem", "samā") and _eq(c, "suffix", "kha")
def sutra_5_1_86(c) : return _eq(c, "stem_class", "dvigu") and bool(c.get("optional"))
def sutra_5_1_87(c) : return _in(c, "stem", {"rātri", "ahar", "saṃvatsara"}) and _eq(c, "rule", "continuation")
def sutra_5_1_88(c) : return _eq(c, "stem", "varṣa") and _eq(c, "operation", "luk")
def sutra_5_1_89(c) : return _eq(c, "semantic", "cittavat") and _eq(c, "rule", "always")
def sutra_5_1_90(c) : return _eq(c, "stem", "ṣaṣṭika") and _eq(c, "semantic", "ṣaṣṭi_rātreṇa_pacyate")
def sutra_5_1_91(c) : return _eq(c, "stem_final", "vatsarānta") and _eq(c, "suffix", "cha") and bool(c.get("is_vedic"))
def sutra_5_1_92(c) : return _in(c, "purva_pada", {"sam", "pari"}) and _eq(c, "suffix", "kha")
def sutra_5_1_93(c) : return _eq(c, "semantic", "tena_parijayya_labhya_kārya_sukara") and _eq(c, "rule", "continuation")
def sutra_5_1_94(c) : return _eq(c, "semantic", "tad_asya_brahmacarya") and _eq(c, "rule", "continuation")
def sutra_5_1_95(c) : return _eq(c, "semantic", "yajñākhya_dakṣiṇā") and _eq(c, "rule", "continuation")
def sutra_5_1_96(c) : return _eq(c, "semantic", "tatra_dīyate_kārya") and _eq(c, "rule", "bhava_vat")
def sutra_5_1_97(c) : return _eq(c, "stem_class", "vyuṣṭādi") and _eq(c, "suffix", "aṇ")
def sutra_5_1_98(c) : return _in(c, "stem", {"yathākatha", "hasta"}) and _in(c, "suffix", {"ṇa", "yat"})
def sutra_5_1_99(c) : return _eq(c, "semantic", "sampādini") and _eq(c, "rule", "continuation")
def sutra_5_1_100(c): return _eq(c, "stem", "karmaveṣa") and _eq(c, "suffix", "yat")
def sutra_5_1_101(c): return _eq(c, "stem_class", "saṃtāpādi") and _eq(c, "semantic", "tasmai_prabhavati")
def sutra_5_1_102(c): return _eq(c, "stem", "yoga") and _eq(c, "suffix", "yat")
def sutra_5_1_103(c): return _eq(c, "stem", "karman") and _eq(c, "suffix", "ukañ")
def sutra_5_1_104(c): return _eq(c, "stem", "samaya") and _eq(c, "semantic", "tasya_prāpta")
def sutra_5_1_105(c): return _eq(c, "stem", "ṛtu") and _eq(c, "suffix", "aṇ")
def sutra_5_1_106(c): return bool(c.get("is_vedic")) and _eq(c, "suffix", "ghas")
def sutra_5_1_107(c): return _eq(c, "stem", "kāla") and _eq(c, "suffix", "yat")
def sutra_5_1_108(c): return _eq(c, "semantic", "prakṛṣṭa") and _eq(c, "suffix", "ṭhañ")
def sutra_5_1_109(c): return _eq(c, "semantic", "prayojana") and _eq(c, "rule", "continuation")
def sutra_5_1_110(c): return _in(c, "stem", {"viśākhā", "āṣāḍhā"}) and _in(c, "semantic", {"mantha", "daṇḍa"})
def sutra_5_1_111(c): return _eq(c, "stem_class", "anupravacanādi") and _eq(c, "suffix", "cha")
def sutra_5_1_112(c): return _eq(c, "stem", "samāpana") and bool(c.get("has_sapurva"))
def sutra_5_1_113(c): return _eq(c, "stem", "aikāgārika") and _eq(c, "semantic", "caura")
def sutra_5_1_114(c): return _eq(c, "stem", "ākālika") and _in(c, "suffix", {"ḍa", "ādyantavacana"})
def sutra_5_1_115(c): return _eq(c, "semantic", "tena_tulya_kriyā") and _eq(c, "suffix", "vati")
def sutra_5_1_116(c): return _eq(c, "semantic", "tatra_tasya_iva") and _eq(c, "rule", "continuation")
def sutra_5_1_117(c): return _eq(c, "semantic", "tad_arha") and _eq(c, "rule", "continuation")
def sutra_5_1_118(c): return _eq(c, "stem_class", "upasarga") and bool(c.get("is_vedic")) and _eq(c, "semantic", "dhātvartha")
def sutra_5_1_119(c): return _eq(c, "semantic", "tasya_bhāva") and _in(c, "suffix", {"tva", "tal"})
def sutra_5_1_120(c): return _eq(c, "rule", "ā_ca_tvāt") and _eq(c, "section", "bhāva")
def sutra_5_1_121(c): return _eq(c, "compound_type", "naṅ_tatpurusha") and _in(c, "stem", {"acatura", "asaṃgata", "lavaṇa", "vaṭa", "yudha", "katara", "sala"}) and _eq(c, "rule", "blocking")
def sutra_5_1_122(c): return _eq(c, "stem_class", "pṛthvādi") and _in(c, "suffix", {"imanic", "vā"})
def sutra_5_1_123(c): return _eq(c, "stem_class", "varṇa_dṛḍhādi") and _eq(c, "suffix", "ṣyañ")
def sutra_5_1_124(c): return _eq(c, "stem_class", "guṇavacana_brāhmaṇādi") and _eq(c, "semantic", "karman")
def sutra_5_1_125(c): return _eq(c, "stem_class", "stenādi") and _eq(c, "operation", "yat_n_lopa")
def sutra_5_1_126(c): return _eq(c, "stem", "sakhi") and _eq(c, "suffix", "ya")
def sutra_5_1_127(c): return _in(c, "stem", {"kapi", "jñāti"}) and _eq(c, "suffix", "ḍhak")
def sutra_5_1_128(c): return _in(c, "stem_final", {"pati", "purohita"}) and _eq(c, "suffix", "yak")
def sutra_5_1_129(c): return _eq(c, "stem_class", "prāṇabhṛj_jāti_vayo_vacana") and _eq(c, "suffix", "añ")
def sutra_5_1_130(c): return _in(c, "stem_final", {"hāyana", "yuvādi"}) and _eq(c, "suffix", "aṇ")
def sutra_5_1_131(c): return _eq(c, "stem_final", "igantā") and _eq(c, "upadha", "laghu")
def sutra_5_1_132(c): return _eq(c, "upadha", "y") and _eq(c, "stem_class", "guru_uttama") and _eq(c, "suffix", "vuñ")
def sutra_5_1_133(c): return _eq(c, "compound_type", "dvandva") and _eq(c, "stem_class", "manojñādi")
def sutra_5_1_134(c): return _in(c, "stem", {"gotra", "caraṇa"}) and _eq(c, "semantic", "ślāghā_tyākāra")
def sutra_5_1_135(c): return _eq(c, "stem_class", "hotrā") and _eq(c, "suffix", "cha")
def sutra_5_1_136(c): return _eq(c, "stem", "brahman") and _eq(c, "suffix", "tva")


# ===========================================================================
# Adhyāya 5.2 — matvarthīya: -in, -mat, -vat, -ka possessive taddhita
#               (139 sūtras)
# ===========================================================================

def sutra_5_2_1(c)  : return _eq(c, "stem_class", "dhānya") and _eq(c, "semantic", "bhavana_kshetra") and _eq(c, "suffix", "khañ")
def sutra_5_2_2(c)  : return _in(c, "stem", {"vrīhi", "śāli"}) and _eq(c, "suffix", "ḍhak")
def sutra_5_2_3(c)  : return _in(c, "stem", {"yava", "yavaka", "ṣaṣṭika"}) and _eq(c, "suffix", "at")
def sutra_5_2_4(c)  : return _in(c, "stem", {"tila", "māṣa", "umā", "bhaṅga", "aṇu"}) and bool(c.get("optional"))
def sutra_5_2_5(c)  : return _eq(c, "stem", "sarvacarman") and _eq(c, "semantic", "kṛta") and _in(c, "suffix", {"kha", "khañ"})
def sutra_5_2_6(c)  : return _in(c, "stem", {"yathāmukha", "saṃmukha"}) and _eq(c, "semantic", "darśana")
def sutra_5_2_7(c)  : return _eq(c, "stem", "tat_sarvādi") and _in(c, "stem_final", {"path", "aṅga_karma", "patra", "pātra"})
def sutra_5_2_8(c)  : return _eq(c, "stem", "āprapada") and _eq(c, "semantic", "prāpnoti")
def sutra_5_2_9(c)  : return _in(c, "stem", {"anupada", "sarvānna", "ayāna"}) and _eq(c, "rule", "continuation")
def sutra_5_2_10(c) : return _in(c, "stem", {"paravara", "paramparā", "putrapautra"}) and _eq(c, "semantic", "anubhavati")
def sutra_5_2_11(c) : return _in(c, "stem", {"avārapāra", "atyanta", "anukāma"}) and _eq(c, "semantic", "gāmī")
def sutra_5_2_12(c) : return _eq(c, "stem", "samāṃsamā") and _eq(c, "semantic", "vijāyate")
def sutra_5_2_13(c) : return _eq(c, "stem", "adyaśvīnā") and _eq(c, "semantic", "avaṣṭabdha")
def sutra_5_2_14(c) : return _eq(c, "stem", "āgavīna")
def sutra_5_2_15(c) : return _eq(c, "stem", "anugu") and _eq(c, "semantic", "alaṃgāmī")
def sutra_5_2_16(c) : return _eq(c, "stem", "adhvan") and _in(c, "suffix", {"yat", "kha"})
def sutra_5_2_17(c) : return _eq(c, "stem", "abhyamitra") and _eq(c, "suffix", "cha")
def sutra_5_2_18(c) : return _eq(c, "stem", "goṣṭha") and _eq(c, "suffix", "khañ") and _eq(c, "semantic", "bhūtapūrva")
def sutra_5_2_19(c) : return _eq(c, "stem", "aśva") and _eq(c, "semantic", "ekāhagama")
def sutra_5_2_20(c) : return _in(c, "stem", {"śālīna", "kaupīna"}) and _in(c, "semantic", {"adhṛṣṭa", "akārya"})
def sutra_5_2_21(c) : return _eq(c, "stem", "vrāta") and _eq(c, "semantic", "jīvati")
def sutra_5_2_22(c) : return _eq(c, "stem", "sāptapadīna") and _eq(c, "semantic", "sakhya")
def sutra_5_2_23(c) : return _eq(c, "stem", "haiyaṃgavīna") and _eq(c, "domain", "samjna")
def sutra_5_2_24(c) : return _eq(c, "semantic", "tasya_pāka_mūla") and _in(c, "stem_class", {"pīlvādi", "karṇādi"})
def sutra_5_2_25(c) : return _eq(c, "stem", "pakṣa") and _eq(c, "suffix", "ti")
def sutra_5_2_26(c) : return _eq(c, "semantic", "tena_vitta") and _in(c, "suffix", {"cuñcup", "caṇap"})
def sutra_5_2_27(c) : return _in(c, "stem", {"vi", "naṅ"}) and _in(c, "suffix", {"nāñ"})
def sutra_5_2_28(c) : return _eq(c, "stem", "vi") and _in(c, "suffix", {"śāla", "śaṅkaṭa"})
def sutra_5_2_29(c) : return _in(c, "stem", {"sam", "pra", "ud"}) and _eq(c, "suffix", "kaṭac")
def sutra_5_2_30(c) : return _eq(c, "stem", "ava") and _eq(c, "suffix", "kuṭāra")
def sutra_5_2_31(c) : return _eq(c, "stem", "nata") and _eq(c, "semantic", "nāsikā") and _eq(c, "domain", "samjna")
def sutra_5_2_32(c) : return _eq(c, "stem", "ni") and _in(c, "suffix", {"biḍac", "birīsac"})
def sutra_5_2_33(c) : return _in(c, "suffix", {"inac", "piṭac", "cikac"}) and _eq(c, "rule", "continuation")
def sutra_5_2_34(c) : return _in(c, "stem", {"upadhi", "upadhī"}) and _in(c, "suffix", {"tyak", "annāsanna_ārūḍha"})
def sutra_5_2_35(c) : return _eq(c, "stem", "ghaṭa") and _eq(c, "semantic", "karman") and _eq(c, "suffix", "ṭhac")
def sutra_5_2_36(c) : return _eq(c, "stem_class", "tārakādi") and _eq(c, "semantic", "tad_asya_saṃjāta") and _eq(c, "suffix", "itac")
def sutra_5_2_37(c) : return _eq(c, "semantic", "pramāṇa") and _in(c, "suffix", {"dvayasac", "daghnac", "mātrac"})
def sutra_5_2_38(c) : return _in(c, "stem", {"puruṣa", "hastin"}) and _eq(c, "suffix", "aṇ")
def sutra_5_2_39(c) : return _in(c, "stem", {"yad", "tad", "etad"}) and _eq(c, "semantic", "parimāṇa") and _eq(c, "suffix", "vatup")
def sutra_5_2_40(c) : return _in(c, "stem", {"kim", "idam"}) and _eq(c, "substitute", "va") and _eq(c, "augment", "gha")
def sutra_5_2_41(c) : return _eq(c, "stem", "kim") and _eq(c, "semantic", "saṅkhya_parimāṇa") and _eq(c, "suffix", "ḍati")
def sutra_5_2_42(c) : return _eq(c, "stem_class", "saṅkhya") and _eq(c, "semantic", "avayava") and _eq(c, "suffix", "tayap")
def sutra_5_2_43(c) : return _in(c, "stem", {"dvi", "tri"}) and _eq(c, "substitute", "ayaj")
def sutra_5_2_44(c) : return _eq(c, "stem", "ubha") and _eq(c, "accent", "udatta") and _eq(c, "rule", "always")
def sutra_5_2_45(c) : return _eq(c, "semantic", "tad_asminn_adhikam") and _eq(c, "stem_final", "daśānta") and _eq(c, "suffix", "ḍa")
def sutra_5_2_46(c) : return _eq(c, "stem_final", "śadanta_viṃśateḥ") and _eq(c, "rule", "continuation")
def sutra_5_2_47(c) : return _eq(c, "stem_class", "saṅkhya") and _eq(c, "semantic", "guṇa_nimāne") and _eq(c, "suffix", "mayaṭ")
def sutra_5_2_48(c) : return _eq(c, "stem_class", "saṅkhya") and _eq(c, "semantic", "tasya_pūraṇa") and _eq(c, "suffix", "ḍaṭ")
def sutra_5_2_49(c) : return _eq(c, "stem_final", "nānta") and not _eq(c, "stem_class", "saṅkhyādi") and _eq(c, "augment", "maṭ")
def sutra_5_2_50(c) : return bool(c.get("is_vedic")) and _eq(c, "suffix", "thaṭ")
def sutra_5_2_51(c) : return _in(c, "stem", {"ṣaṭ", "kati", "katipaya", "catur"}) and _eq(c, "augment", "thuk")
def sutra_5_2_52(c) : return _in(c, "stem", {"bahu", "pūga", "gaṇa", "saṃgha"}) and _eq(c, "augment", "tithuk")
def sutra_5_2_53(c) : return _eq(c, "stem", "vatu") and _eq(c, "augment", "ithuk")
def sutra_5_2_54(c) : return _eq(c, "stem", "dvi") and _eq(c, "suffix", "tīya")
def sutra_5_2_55(c) : return _eq(c, "stem", "tri") and _eq(c, "operation", "samprasāraṇa")
def sutra_5_2_56(c) : return _eq(c, "stem_class", "viṃśatyādi") and _eq(c, "suffix", "tamaṭ") and bool(c.get("optional"))
def sutra_5_2_57(c) : return _in(c, "stem", {"śata", "māsa", "ardhamāsa", "saṃvatsara"}) and _eq(c, "rule", "always")
def sutra_5_2_58(c) : return _eq(c, "stem_class", "ṣaṣṭyādi_non_saṅkhyādi") and _eq(c, "rule", "continuation")
def sutra_5_2_59(c) : return _eq(c, "stem_class", "matu") and _in(c, "stem", {"sūkta", "sāma"}) and _eq(c, "suffix", "cha")
def sutra_5_2_60(c) : return _in(c, "stem", {"adhyāya", "anuvāka"}) and _eq(c, "operation", "luk")
def sutra_5_2_61(c) : return _eq(c, "stem_class", "vimuktādi") and _eq(c, "suffix", "aṇ")
def sutra_5_2_62(c) : return _eq(c, "stem_class", "goṣadādi") and _eq(c, "suffix", "vun")
def sutra_5_2_63(c) : return _eq(c, "stem", "patha") and _eq(c, "semantic", "kuśala")
def sutra_5_2_64(c) : return _eq(c, "stem_class", "ākarṣādi") and _eq(c, "suffix", "kan")
def sutra_5_2_65(c) : return _in(c, "stem", {"dhana", "hiraṇya"}) and _eq(c, "semantic", "kāma")
def sutra_5_2_66(c) : return _eq(c, "stem_class", "svāṅga") and _eq(c, "semantic", "prasita")
def sutra_5_2_67(c) : return _eq(c, "stem", "udara") and _eq(c, "suffix", "ṭhag") and _eq(c, "semantic", "ādyūna")
def sutra_5_2_68(c) : return _eq(c, "stem", "sasya") and _eq(c, "semantic", "parijāta")
def sutra_5_2_69(c) : return _eq(c, "stem", "aṃśa") and _eq(c, "semantic", "hārī")
def sutra_5_2_70(c) : return _eq(c, "stem", "tantra") and _eq(c, "semantic", "acirāpahṛta")
def sutra_5_2_71(c) : return _in(c, "stem", {"brāhmaṇa", "koṣṇika"}) and _eq(c, "domain", "samjna")
def sutra_5_2_72(c) : return _in(c, "stem", {"śīta", "uṣṇa"}) and _eq(c, "semantic", "kāri")
def sutra_5_2_73(c) : return _eq(c, "semantic", "adhika") and _eq(c, "rule", "continuation")
def sutra_5_2_74(c) : return _in(c, "stem", {"anukā", "abhikā", "abhīka"}) and _eq(c, "semantic", "kamitā")
def sutra_5_2_75(c) : return _eq(c, "stem", "pārśva") and _eq(c, "semantic", "anvicchati")
def sutra_5_2_76(c) : return _in(c, "stem", {"ayaḥśūla", "daṇḍa", "ajina"}) and _in(c, "suffix", {"ṭhak", "ṭhañ"})
def sutra_5_2_77(c) : return _eq(c, "stem", "tāvatittha") and _eq(c, "semantic", "grahaṇa") and bool(c.get("optional"))
def sutra_5_2_78(c) : return _eq(c, "semantic", "grāmaṇī") and _eq(c, "rule", "continuation")
def sutra_5_2_79(c) : return _eq(c, "stem", "śṛṅkhala") and _eq(c, "semantic", "bandhana") and _eq(c, "stem_final", "karabha")
def sutra_5_2_80(c) : return _eq(c, "stem", "utka") and _eq(c, "semantic", "unmanas")
def sutra_5_2_81(c) : return _eq(c, "stem_class", "kāla_prayojana") and _eq(c, "semantic", "roga")
def sutra_5_2_82(c) : return _eq(c, "semantic", "tad_asminn_anna_prāya") and _eq(c, "domain", "samjna")
def sutra_5_2_83(c) : return _eq(c, "stem", "kulmāṣa") and _eq(c, "suffix", "añ")
def sutra_5_2_84(c) : return _eq(c, "stem", "śrotriya") and _eq(c, "semantic", "chando_adhīte")
def sutra_5_2_85(c) : return _eq(c, "stem", "śrāddha") and _eq(c, "semantic", "bhukta") and _in(c, "suffix", {"ini", "ṭhan"})
def sutra_5_2_86(c) : return _eq(c, "stem", "pūrva") and _eq(c, "suffix", "ini")
def sutra_5_2_87(c) : return bool(c.get("has_sapurva")) and _eq(c, "rule", "continuation")
def sutra_5_2_88(c) : return _eq(c, "stem_class", "iṣṭādi") and _eq(c, "rule", "continuation")
def sutra_5_2_89(c) : return bool(c.get("is_vedic")) and _in(c, "stem", {"paripanthi", "pari_pariṇa"}) and _eq(c, "semantic", "paryavasthātṛ")
def sutra_5_2_90(c) : return _eq(c, "stem", "anupadi") and _eq(c, "semantic", "anveṣṭṛ")
def sutra_5_2_91(c) : return _eq(c, "stem", "sākṣād") and _eq(c, "semantic", "draṣṭṛ") and _eq(c, "domain", "samjna")
def sutra_5_2_92(c) : return _eq(c, "stem", "kṣetriya") and _eq(c, "semantic", "para_kṣetra_cikitsya")
def sutra_5_2_93(c) : return _eq(c, "stem", "indriya") and _eq(c, "semantic", "indra_liṅga")
def sutra_5_2_95(c) : return _eq(c, "stem_class", "rasādi") and _eq(c, "rule", "continuation")
def sutra_5_2_96(c) : return _eq(c, "stem_class", "prāṇistha") and _eq(c, "stem_final", "ā") and _eq(c, "suffix", "lajan") and bool(c.get("optional"))
def sutra_5_2_97(c) : return _eq(c, "stem_class", "sidhmādi") and _eq(c, "rule", "continuation")
def sutra_5_2_98(c) : return _in(c, "stem", {"vatsa", "aṃsa"}) and _in(c, "semantic", {"kāma", "bala"})
def sutra_5_2_99(c) : return _eq(c, "stem_class", "phenādi") and _eq(c, "suffix", "lac")
def sutra_5_2_100(c): return _eq(c, "stem_class", "lomādi_pāmādi_picchādi") and _eq(c, "suffix", "śanelac")
def sutra_5_2_101(c): return _in(c, "stem", {"prajñā", "śraddhā", "arcā", "vṛtti"}) and _eq(c, "suffix", "ṇa")
def sutra_5_2_102(c): return _in(c, "stem", {"tapas", "sahasra"}) and _in(c, "suffix", {"vini", "ṇini"})
def sutra_5_2_103(c): return _eq(c, "rule", "continuation") and _eq(c, "suffix", "aṇ")
def sutra_5_2_104(c): return _in(c, "stem", {"sikatā", "śarkarā"}) and _eq(c, "rule", "continuation")
def sutra_5_2_105(c): return _eq(c, "semantic", "deśa") and _in(c, "suffix", {"lup", "lac"})
def sutra_5_2_106(c): return _eq(c, "stem", "danta") and _eq(c, "semantic", "unnata") and _eq(c, "suffix", "urac")
def sutra_5_2_107(c): return _in(c, "stem", {"ūṣa", "suṣi", "muṣka", "madhu"}) and _eq(c, "suffix", "ra")
def sutra_5_2_108(c): return _in(c, "stem", {"dyu", "dru"}) and _eq(c, "suffix", "ma")
def sutra_5_2_109(c): return _eq(c, "stem", "keśa") and _eq(c, "suffix", "va") and bool(c.get("optional"))
def sutra_5_2_110(c): return _eq(c, "stem", "gāṇḍī") and _eq(c, "semantic", "ajagā") and _eq(c, "domain", "samjna")
def sutra_5_2_111(c): return _in(c, "stem", {"kāṇḍa", "aṇḍa"}) and _eq(c, "augment", "īra_īrac")
def sutra_5_2_112(c): return _in(c, "stem", {"rajas", "kṛṣyā", "āsuti", "pariṣad"}) and _eq(c, "suffix", "valac")
def sutra_5_2_113(c): return _eq(c, "stem", "dantaśikha") and _eq(c, "domain", "samjna")
def sutra_5_2_114(c): return _in(c, "stem", {"jyotsnā", "tamisrā", "śṛṅgin"}) and _eq(c, "suffix", "matup")
def sutra_5_2_115(c): return _eq(c, "stem_final", "ata") and _in(c, "suffix", {"ini", "ṭhan"})
def sutra_5_2_116(c): return _eq(c, "stem_class", "vrīhyādi") and _eq(c, "rule", "continuation")
def sutra_5_2_117(c): return _eq(c, "stem_class", "tundādi") and _eq(c, "suffix", "ilac")
def sutra_5_2_118(c): return _eq(c, "purva_pada", "eka_go") and _eq(c, "suffix", "ṭhañ") and _eq(c, "rule", "always")
def sutra_5_2_119(c): return _eq(c, "stem", "niṣka") and _eq(c, "stem_final", "śata_sahasra_anta")
def sutra_5_2_120(c): return _eq(c, "stem", "rūpa") and _in(c, "semantic", {"āhata", "praśaṃsā"})
def sutra_5_2_121(c): return _in(c, "stem", {"asu", "māyā", "medhā", "sraj"}) and _eq(c, "suffix", "vini")
def sutra_5_2_122(c): return bool(c.get("is_vedic")) and _eq(c, "rule", "bahulam")
def sutra_5_2_123(c): return _eq(c, "stem", "ūrṇā") and _eq(c, "suffix", "yus")
def sutra_5_2_124(c): return _eq(c, "stem", "vāc") and _eq(c, "suffix", "gmini")
def sutra_5_2_125(c): return _in(c, "suffix", {"ālaj", "āṭac"}) and _eq(c, "semantic", "bahu_bhāṣin")
def sutra_5_2_126(c): return _eq(c, "stem", "svāmin") and _eq(c, "semantic", "aiśvarya")
def sutra_5_2_127(c): return _eq(c, "stem_class", "arśa_ādi") and _eq(c, "suffix", "ac")
def sutra_5_2_128(c): return _eq(c, "stem_class", "dvandva_upatāpa_garhya_prāṇistha") and _eq(c, "suffix", "ini")
def sutra_5_2_129(c): return _in(c, "stem", {"vāta", "atisāra"}) and _eq(c, "augment", "kuk")
def sutra_5_2_130(c): return _eq(c, "semantic", "vayas") and _eq(c, "stem_class", "pūraṇa")
def sutra_5_2_131(c): return _eq(c, "stem_class", "sukhādi") and _eq(c, "rule", "continuation")
def sutra_5_2_132(c): return _in(c, "stem_final", {"dharma", "śīla", "varṇa"}) and _eq(c, "rule", "continuation")
def sutra_5_2_133(c): return _eq(c, "stem", "hasta") and _eq(c, "semantic", "jati")
def sutra_5_2_134(c): return _eq(c, "stem", "varṇa") and _eq(c, "semantic", "brahmacārin")
def sutra_5_2_135(c): return _eq(c, "stem_class", "puṣkarādi") and _eq(c, "semantic", "deśa")
def sutra_5_2_136(c): return _eq(c, "stem_class", "balādi") and _in(c, "suffix", {"matup", "anyatarasyām"})
def sutra_5_2_137(c): return _eq(c, "domain", "samjna") and _in(c, "suffix", {"manma", "abhya"})
def sutra_5_2_138(c): return _in(c, "stem", {"kaṃ", "śaṃ"}) and _in(c, "suffix", {"babhayu", "stitutayasa"})
def sutra_5_2_139(c): return _in(c, "stem", {"tundi", "vali", "vaṭi"}) and _eq(c, "suffix", "bha")
def sutra_5_2_140(c): return _in(c, "stem", {"ahaṃ", "śubha"}) and _eq(c, "suffix", "yus")


# ===========================================================================
# Adhyāya 5.3 — case-adverb taddhitas + praśaṁsā/kutsana/krīḍā/saṁjñā kan
#               (118 sūtras)
# ===========================================================================

def sutra_5_3_1(c)  : return _eq(c, "section", "prāgdiśo_vibhakti") and _eq(c, "samjna", "vibhakti")
def sutra_5_3_2(c)  : return _eq(c, "stem_class", "kim_sarvanāma_bahu_non_dvyādi") and _eq(c, "rule", "continuation")
def sutra_5_3_3(c)  : return _eq(c, "stem", "idam") and _eq(c, "substitute", "i")
def sutra_5_3_4(c)  : return _in(c, "stem", {"eta", "ta"}) and _eq(c, "substitute", "ra")
def sutra_5_3_5(c)  : return _eq(c, "stem", "etad") and _eq(c, "substitute", "aś")
def sutra_5_3_6(c)  : return _eq(c, "stem", "sarva") and _eq(c, "substitute", "sa") and bool(c.get("optional"))
def sutra_5_3_7(c)  : return _eq(c, "case", "pancami") and _eq(c, "suffix", "tasil")
def sutra_5_3_8(c)  : return _eq(c, "suffix", "tasi") and _eq(c, "rule", "continuation")
def sutra_5_3_9(c)  : return _in(c, "stem", {"pari", "abhi"}) and _eq(c, "rule", "continuation")
def sutra_5_3_10(c) : return _eq(c, "case", "saptami") and _eq(c, "suffix", "tral")
def sutra_5_3_11(c) : return _eq(c, "stem", "idam") and _eq(c, "augment", "ha")
def sutra_5_3_12(c) : return _eq(c, "stem", "kim") and _eq(c, "augment", "at")
def sutra_5_3_13(c) : return bool(c.get("is_vedic")) and _eq(c, "augment", "ha") and bool(c.get("optional"))
def sutra_5_3_14(c) : return _eq(c, "stem_class", "itarād") and _eq(c, "rule", "continuation")
def sutra_5_3_15(c) : return _in(c, "stem", {"sarva", "eka", "anya", "kim", "yad", "tad"}) and _eq(c, "semantic", "kāla") and _eq(c, "suffix", "dā")
def sutra_5_3_16(c) : return _eq(c, "stem", "idam") and _eq(c, "suffix", "rhil")
def sutra_5_3_17(c) : return _eq(c, "stem", "adhunā")
def sutra_5_3_18(c) : return _eq(c, "stem", "dānīm") and _eq(c, "rule", "continuation")
def sutra_5_3_19(c) : return _eq(c, "stem", "tad") and _eq(c, "suffix", "dā")
def sutra_5_3_20(c) : return _eq(c, "stem", "tayor") and bool(c.get("is_vedic"))
def sutra_5_3_21(c) : return _eq(c, "semantic", "anadyatana") and _eq(c, "suffix", "rhil") and bool(c.get("optional"))
def sutra_5_3_22(c) : return _in(c, "stem", {"sadya", "parut", "parāri", "aiṣamas", "paredyavi"}) and _eq(c, "rule", "continuation")
def sutra_5_3_23(c) : return _eq(c, "semantic", "prakāra_vacana") and _eq(c, "suffix", "thāl")
def sutra_5_3_24(c) : return _eq(c, "stem", "idam") and _eq(c, "suffix", "tham_uh")
def sutra_5_3_25(c) : return _eq(c, "stem", "kim") and _eq(c, "rule", "continuation")
def sutra_5_3_26(c) : return _eq(c, "suffix", "thā") and _eq(c, "semantic", "hetu") and bool(c.get("is_vedic"))
def sutra_5_3_27(c) : return _eq(c, "stem_class", "dik_shabda") and _in(c, "case", {"saptami", "pancami", "prathama"}) and _eq(c, "suffix", "astāti")
def sutra_5_3_28(c) : return _in(c, "stem", {"dakṣiṇā", "uttarā"}) and _eq(c, "suffix", "atasuc")
def sutra_5_3_29(c) : return _in(c, "stem", {"para", "avara"}) and bool(c.get("optional"))
def sutra_5_3_30(c) : return _eq(c, "stem", "añcer") and _eq(c, "operation", "luk")
def sutra_5_3_31(c) : return _eq(c, "stem", "upari") and _eq(c, "substitute", "upariṣṭāt")
def sutra_5_3_32(c) : return _eq(c, "stem", "paścāt")
def sutra_5_3_33(c) : return _in(c, "stem", {"paśca", "paścā"}) and bool(c.get("is_vedic"))
def sutra_5_3_34(c) : return _in(c, "stem", {"uttara", "adhara", "dakṣiṇa"}) and _eq(c, "suffix", "āti")
def sutra_5_3_35(c) : return _eq(c, "suffix", "enab") and not _eq(c, "case", "pancami") and bool(c.get("optional"))
def sutra_5_3_36(c) : return _eq(c, "stem", "dakṣiṇa") and _eq(c, "suffix", "āc")
def sutra_5_3_37(c) : return _eq(c, "suffix", "āhi") and _eq(c, "semantic", "dūra")
def sutra_5_3_38(c) : return _eq(c, "stem", "uttara") and _eq(c, "rule", "continuation")
def sutra_5_3_39(c) : return _in(c, "stem", {"pūrva", "adhara", "avara"}) and _eq(c, "stem_final", "asi_pur_adha_vas")
def sutra_5_3_40(c) : return _eq(c, "suffix", "astāti") and _eq(c, "rule", "continuation")
def sutra_5_3_41(c) : return _eq(c, "stem", "avara") and bool(c.get("optional"))
def sutra_5_3_42(c) : return _eq(c, "stem_class", "saṅkhya") and _eq(c, "semantic", "vidha_artha") and _eq(c, "suffix", "dhā")
def sutra_5_3_43(c) : return _eq(c, "semantic", "adhikaraṇa_vicāla") and _eq(c, "rule", "continuation")
def sutra_5_3_44(c) : return _eq(c, "stem", "eka") and _in(c, "suffix", {"dhyamuñ", "anyāra"})
def sutra_5_3_45(c) : return _in(c, "stem", {"dvi", "tri"}) and _eq(c, "suffix", "dhamuñ")
def sutra_5_3_46(c) : return _eq(c, "stem", "edhā") and _eq(c, "rule", "continuation")
def sutra_5_3_47(c) : return _eq(c, "semantic", "yāpya") and _eq(c, "suffix", "pāśap")
def sutra_5_3_48(c) : return _eq(c, "stem_class", "pūraṇa") and _eq(c, "semantic", "bhāga") and _eq(c, "suffix", "tīyādan")
def sutra_5_3_49(c) : return _eq(c, "stem_class", "prāg_ekādaśa") and not bool(c.get("is_vedic"))
def sutra_5_3_50(c) : return _in(c, "stem", {"ṣaṣṭha", "aṣṭama"}) and _eq(c, "suffix", "ña")
def sutra_5_3_51(c) : return _eq(c, "semantic", "māna_paśu_aṅga") and _in(c, "suffix", {"kan", "luk"})
def sutra_5_3_52(c) : return _eq(c, "stem", "eka") and _eq(c, "suffix", "ākinic") and _eq(c, "semantic", "asahāya")
def sutra_5_3_53(c) : return _eq(c, "semantic", "bhūtapūrva") and _eq(c, "suffix", "caraṭ")
def sutra_5_3_54(c) : return _eq(c, "case", "ṣaṣṭhi") and _eq(c, "suffix", "rūpya")
def sutra_5_3_56(c) : return _eq(c, "stem_class", "tin") and _eq(c, "rule", "continuation")
def sutra_5_3_57(c) : return bool(c.get("dvivacana_vibhajya_upapade")) and _in(c, "suffix", {"tarap", "īyasun"})
def sutra_5_3_58(c) : return _eq(c, "stem_class", "ajādi") and _eq(c, "stem_class_alt", "guṇa_vacana") and _eq(c, "rule", "continuation")
def sutra_5_3_59(c) : return _eq(c, "augment", "tu") and bool(c.get("is_vedic"))
def sutra_5_3_60(c) : return _eq(c, "stem", "praśasya") and _eq(c, "substitute", "śra")
def sutra_5_3_61(c) : return _eq(c, "substitute", "jya") and _eq(c, "rule", "continuation")
def sutra_5_3_62(c) : return _eq(c, "stem", "vṛddha") and _eq(c, "rule", "continuation")
def sutra_5_3_63(c) : return _in(c, "stem", {"antika", "bāḍha"}) and _in(c, "substitute", {"neda", "sādha"})
def sutra_5_3_64(c) : return _in(c, "stem", {"yuvan", "alpa"}) and _eq(c, "suffix", "kan") and bool(c.get("optional"))
def sutra_5_3_65(c) : return _eq(c, "stem_class", "vin_matu") and _eq(c, "operation", "luk")
def sutra_5_3_66(c) : return _eq(c, "semantic", "praśaṃsā") and _eq(c, "suffix", "rūpap")
def sutra_5_3_67(c) : return _eq(c, "semantic", "iṣad_asamāpta") and _in(c, "suffix", {"kalpab", "deśya", "deśīyar"})
def sutra_5_3_68(c) : return _eq(c, "stem_class", "supo") and _eq(c, "suffix", "bahuc") and _eq(c, "position", "purastāt") and bool(c.get("optional"))
def sutra_5_3_69(c) : return _eq(c, "semantic", "prakāra_vacana") and _eq(c, "suffix", "jātīyar")
def sutra_5_3_70(c) : return _eq(c, "section", "prāgivāt") and _eq(c, "suffix", "ka")
def sutra_5_3_71(c) : return _in(c, "stem_class", {"avyaya", "sarvanāman"}) and _eq(c, "suffix", "akac") and _eq(c, "position", "prāk_ṭi")
def sutra_5_3_72(c) : return _eq(c, "stem", "ka") and _eq(c, "substitute", "da")
def sutra_5_3_73(c) : return _eq(c, "semantic", "ajñāta") and _eq(c, "rule", "continuation")
def sutra_5_3_74(c) : return _eq(c, "semantic", "kutsita") and _eq(c, "rule", "continuation")
def sutra_5_3_75(c) : return _eq(c, "domain", "samjna") and _eq(c, "suffix", "kan")
def sutra_5_3_76(c) : return _eq(c, "semantic", "anukampā") and _eq(c, "rule", "continuation")
def sutra_5_3_77(c) : return _eq(c, "semantic", "nīti_tadyuktāt") and _eq(c, "rule", "continuation")
def sutra_5_3_78(c) : return _eq(c, "stem_class", "bahvac_manuṣya_nāma") and _eq(c, "suffix", "ṭhajvā") and bool(c.get("optional"))
def sutra_5_3_79(c) : return _in(c, "suffix", {"ghan", "ilac"}) and _eq(c, "rule", "continuation")
def sutra_5_3_80(c) : return _eq(c, "dialect", "pracya") and _eq(c, "stem", "upa") and _in(c, "suffix", {"aḍac", "vuc"})
def sutra_5_3_81(c) : return _eq(c, "stem_class", "jāti_nāman") and _eq(c, "suffix", "kan")
def sutra_5_3_82(c) : return _eq(c, "stem_final", "ajina") and _eq(c, "operation", "uttara_pada_lopa")
def sutra_5_3_83(c) : return _eq(c, "suffix", "ṭhāc") and _eq(c, "stem_final", "ūrdhva_dvitīya_ac")
def sutra_5_3_84(c) : return _in(c, "stem", {"śevala", "supari", "viśāla", "varuṇa", "āryamā"}) and _eq(c, "stem_final", "tṛtīya")
def sutra_5_3_85(c) : return _eq(c, "semantic", "alpa") and _eq(c, "rule", "continuation")
def sutra_5_3_86(c) : return _eq(c, "semantic", "hrasva") and _eq(c, "rule", "continuation")
def sutra_5_3_87(c) : return _eq(c, "domain", "samjna") and _eq(c, "suffix", "kan")
def sutra_5_3_88(c) : return _in(c, "stem", {"kuṭī", "śamī", "śuṇḍā"}) and _eq(c, "suffix", "ra")
def sutra_5_3_89(c) : return _eq(c, "stem_class", "kutvā") and _eq(c, "suffix", "ḍupac")
def sutra_5_3_90(c) : return _in(c, "stem", {"kāsū", "goṇī"}) and _eq(c, "suffix", "ṣṭarac")
def sutra_5_3_91(c) : return _in(c, "stem", {"vatsa", "ukṣā", "aśva", "ṛṣabha"}) and _eq(c, "semantic", "tanutva")
def sutra_5_3_92(c) : return _in(c, "stem", {"kim", "yad", "tad"}) and _eq(c, "semantic", "dvayor_eka_nirddhāraṇa") and _eq(c, "suffix", "ḍatarac")
def sutra_5_3_93(c) : return _eq(c, "semantic", "bahūnāṃ_jāti_paripraśna") and _eq(c, "suffix", "ḍatamac") and bool(c.get("optional"))
def sutra_5_3_94(c) : return _eq(c, "stem_class", "ekāt") and _eq(c, "dialect", "pracya")
def sutra_5_3_95(c) : return _eq(c, "semantic", "avakṣepaṇa") and _eq(c, "suffix", "kan")
def sutra_5_3_96(c) : return _eq(c, "semantic", "iva_pratikṛti") and _eq(c, "rule", "continuation")
def sutra_5_3_97(c) : return _eq(c, "domain", "samjna") and _eq(c, "rule", "continuation")
def sutra_5_3_98(c) : return _eq(c, "operation", "lup") and _eq(c, "semantic", "manuṣya")
def sutra_5_3_99(c) : return _eq(c, "semantic", "jīvika_apaṇya") and _eq(c, "rule", "continuation")
def sutra_5_3_100(c): return _eq(c, "stem_class", "devapathādi") and _eq(c, "rule", "continuation")
def sutra_5_3_101(c): return _eq(c, "stem", "vastra") and _eq(c, "suffix", "ḍhañ")
def sutra_5_3_102(c): return _eq(c, "stem", "śilā") and _eq(c, "suffix", "ḍha")
def sutra_5_3_103(c): return _eq(c, "stem_class", "śākhādi") and _eq(c, "suffix", "yat")
def sutra_5_3_104(c): return _eq(c, "semantic", "bhavya_dravya") and _eq(c, "rule", "continuation")
def sutra_5_3_105(c): return _eq(c, "stem", "kuśāgra") and _eq(c, "suffix", "cha")
def sutra_5_3_106(c): return _eq(c, "stem_class", "samāsa") and _eq(c, "semantic", "tad_viṣaya")
def sutra_5_3_107(c): return _eq(c, "stem_class", "śarkarādi") and _eq(c, "suffix", "aṇ")
def sutra_5_3_108(c): return _eq(c, "stem_class", "aṅgulyādi") and _eq(c, "suffix", "ṭhak")
def sutra_5_3_109(c): return _eq(c, "stem", "ekaśālā") and _eq(c, "suffix", "ṭhac") and bool(c.get("optional"))
def sutra_5_3_110(c): return _in(c, "stem", {"karka", "lohita"}) and _eq(c, "suffix", "īkak")
def sutra_5_3_111(c): return _in(c, "stem", {"pratna", "pūrva", "viśvema"}) and _eq(c, "suffix", "thāl") and bool(c.get("is_vedic"))
def sutra_5_3_112(c): return _eq(c, "stem", "pūgā") and _eq(c, "suffix", "ñya") and not _eq(c, "purva_pada", "grāmaṇī")
def sutra_5_3_113(c): return _in(c, "stem_class", {"vrāta", "cphañ"}) and not _eq(c, "gender", "strī")
def sutra_5_3_114(c): return _eq(c, "stem_class", "āyudhajīvi") and _eq(c, "suffix", "ñyaḍ") and _eq(c, "dialect", "vāhīka")
def sutra_5_3_115(c): return _eq(c, "stem", "vṛka") and _eq(c, "suffix", "ṭeṇyaṇ")
def sutra_5_3_116(c): return _eq(c, "stem_class", "dāmanyādi") and _eq(c, "stem_final", "trigarta_ṣaṣṭha") and _eq(c, "suffix", "cha")
def sutra_5_3_117(c): return _in(c, "stem_class", {"parśvādi", "yaudheyādi"}) and _in(c, "suffix", {"aṇ", "añ"})
def sutra_5_3_118(c): return _in(c, "stem", {"abhijit", "vidabhṛt", "śālāvat", "śikhāvat"}) and _eq(c, "suffix", "yañ")
def sutra_5_3_119(c): return _eq(c, "samjna", "tadrāja") and _eq(c, "stem_class", "ñyādi")


# ===========================================================================
# Adhyāya 5.4 — vīpsā, samāsānta, bahuvrīhi endings (160 sūtras)
# ===========================================================================

def sutra_5_4_1(c)  : return _eq(c, "stem", "pādaśata") and _eq(c, "semantic", "vīpsā") and _in(c, "suffix", {"vun", "lopa"})
def sutra_5_4_2(c)  : return _in(c, "stem", {"daṇḍa", "vyavasarga"}) and _eq(c, "rule", "continuation")
def sutra_5_4_3(c)  : return _eq(c, "stem_class", "sthūlādi") and _eq(c, "semantic", "prakāra_vacana") and _eq(c, "suffix", "kan")
def sutra_5_4_4(c)  : return _eq(c, "semantic", "anatyantagati") and _eq(c, "suffix_pre", "kta")
def sutra_5_4_5(c)  : return _eq(c, "semantic", "sāmi_vacana") and _eq(c, "rule", "blocking")
def sutra_5_4_6(c)  : return _eq(c, "stem", "bṛhatī") and _eq(c, "semantic", "ācchādana")
def sutra_5_4_7(c)  : return _in(c, "purva_pada", {"aṣaḍakṣa", "āśitaṅgu", "alaṅkarma", "alaṃpuruṣa"}) and _eq(c, "suffix", "kha")
def sutra_5_4_8(c)  : return _eq(c, "stem_class", "añcer") and not _eq(c, "domain", "dik_strī") and bool(c.get("optional"))
def sutra_5_4_9(c)  : return _eq(c, "stem_class", "jāti_anta") and _eq(c, "semantic", "bandhu") and _eq(c, "suffix", "cha")
def sutra_5_4_10(c) : return _eq(c, "stem_final", "sthāna_anta") and bool(c.get("sa_sthāna")) and bool(c.get("optional"))
def sutra_5_4_11(c) : return _in(c, "stem", {"kim", "et", "tiṅ", "avyaya", "ghan"}) and _eq(c, "semantic", "adravya_prakarṣa") and _eq(c, "suffix", "ām_vat")
def sutra_5_4_12(c) : return _eq(c, "stem", "amu") and bool(c.get("is_vedic"))
def sutra_5_4_13(c) : return _eq(c, "stem", "anugā") and _eq(c, "suffix", "ṭhak")
def sutra_5_4_14(c) : return _eq(c, "suffix_class", "ṇacaḥ") and _eq(c, "gender", "stri") and _eq(c, "suffix", "añ")
def sutra_5_4_15(c) : return _eq(c, "stem", "aṇinu") and _eq(c, "rule", "continuation")
def sutra_5_4_16(c) : return _eq(c, "stem", "visārin") and _eq(c, "semantic", "matsya")
def sutra_5_4_17(c) : return _eq(c, "stem_class", "saṅkhya") and _eq(c, "semantic", "kriyā_abhyāvṛtti_gaṇana") and _eq(c, "suffix", "kṛtvasuc")
def sutra_5_4_18(c) : return _in(c, "stem", {"dvi", "tri", "catur"}) and _eq(c, "suffix", "suc")
def sutra_5_4_19(c) : return _eq(c, "stem", "eka") and _eq(c, "suffix", "sakṛt")
def sutra_5_4_20(c) : return _eq(c, "stem", "bahu") and _eq(c, "suffix", "dhā") and bool(c.get("aviprakṛṣṭa_kāla")) and bool(c.get("optional"))
def sutra_5_4_21(c) : return _eq(c, "semantic", "tat_prakṛta_vacana") and _eq(c, "suffix", "mayaṭ")
def sutra_5_4_22(c) : return _eq(c, "semantic", "samūhavat") and _eq(c, "rule", "continuation")
def sutra_5_4_23(c) : return _in(c, "stem_final", {"ananta", "āvasatha", "iti", "hama", "bheṣaja"}) and _eq(c, "suffix", "ñya")
def sutra_5_4_24(c) : return _eq(c, "stem_final", "devatānta") and _eq(c, "semantic", "tādarthya") and _eq(c, "suffix", "yat")
def sutra_5_4_25(c) : return _in(c, "stem", {"pāda", "arghā"}) and _eq(c, "rule", "continuation")
def sutra_5_4_26(c) : return _eq(c, "stem", "atithi") and _eq(c, "suffix", "ñya")
def sutra_5_4_27(c) : return _eq(c, "stem", "deva") and _eq(c, "suffix", "tal")
def sutra_5_4_28(c) : return _eq(c, "stem", "avi") and _eq(c, "suffix", "ka")
def sutra_5_4_29(c) : return _eq(c, "stem_class", "yāvādi") and _eq(c, "suffix", "kan")
def sutra_5_4_30(c) : return _eq(c, "stem", "lohita") and _eq(c, "semantic", "maṇi")
def sutra_5_4_31(c) : return _eq(c, "semantic", "varṇa_anitya") and _eq(c, "rule", "continuation")
def sutra_5_4_32(c) : return _eq(c, "semantic", "rakta") and _eq(c, "rule", "continuation")
def sutra_5_4_33(c) : return _eq(c, "stem", "kāla") and _eq(c, "rule", "continuation")
def sutra_5_4_34(c) : return _eq(c, "stem_class", "vinayādi") and _eq(c, "suffix", "ṭhak")
def sutra_5_4_35(c) : return _eq(c, "stem", "vāc") and _eq(c, "semantic", "vyāhṛta_artha")
def sutra_5_4_36(c) : return _eq(c, "stem_class", "tadyukta") and _eq(c, "semantic", "karman") and _eq(c, "suffix", "aṇ")
def sutra_5_4_37(c) : return _eq(c, "stem", "oṣadhi") and not _eq(c, "semantic", "jāti")
def sutra_5_4_38(c) : return _eq(c, "stem_class", "prajñādi") and _eq(c, "rule", "continuation")
def sutra_5_4_39(c) : return _eq(c, "stem", "mṛd") and _eq(c, "suffix", "tikan")
def sutra_5_4_40(c) : return _in(c, "stem", {"sa", "sna"}) and _eq(c, "semantic", "praśaṃsā")
def sutra_5_4_41(c) : return _in(c, "stem", {"vṛka", "jyeṣṭha"}) and _in(c, "suffix", {"tila", "tāila"}) and bool(c.get("is_vedic"))
def sutra_5_4_42(c) : return _eq(c, "semantic", "bahu_alpa_artha") and _eq(c, "stem_class", "non_karaka") and _eq(c, "suffix", "śas") and bool(c.get("optional"))
def sutra_5_4_43(c) : return _eq(c, "stem_class", "saṅkhya_ekavacana") and _eq(c, "semantic", "vīpsā")
def sutra_5_4_44(c) : return _eq(c, "case", "pancami") and _eq(c, "semantic", "pratiyoga") and _eq(c, "suffix", "tasi")
def sutra_5_4_45(c) : return _eq(c, "semantic", "apādāna") and _in(c, "stem", {"ahī", "ruh"})
def sutra_5_4_46(c) : return _eq(c, "case", "tritiya") and _in(c, "stem_class", {"ati_graha", "avyathana", "kṣepa"}) and not _eq(c, "role", "kartr")
def sutra_5_4_47(c) : return _eq(c, "semantic", "hīyamāna_pāpa_yoga") and _eq(c, "rule", "continuation")
def sutra_5_4_48(c) : return _eq(c, "case", "ṣaṣṭhi") and _eq(c, "semantic", "vyāśraya")
def sutra_5_4_49(c) : return _eq(c, "stem", "roga") and _eq(c, "semantic", "apanayana")
def sutra_5_4_50(c) : return _eq(c, "semantic", "abhūta_tad_bhāva") and _in(c, "stem_yoga", {"kṛ", "bhū", "as"}) and _eq(c, "suffix", "cvi")
def sutra_5_4_51(c) : return _in(c, "stem_final", {"arur", "manas", "cakṣus", "ceto", "rahas", "rajas"}) and _eq(c, "operation", "lopa")
def sutra_5_4_52(c) : return _eq(c, "suffix", "sāti") and _eq(c, "semantic", "kārtsnya") and bool(c.get("optional"))
def sutra_5_4_53(c) : return _eq(c, "semantic", "abhividhi") and _eq(c, "stem_yoga", "sampad")
def sutra_5_4_54(c) : return _eq(c, "semantic", "tad_adhīna_vacana") and _eq(c, "rule", "continuation")
def sutra_5_4_55(c) : return _eq(c, "semantic", "deya") and _eq(c, "suffix", "trā")
def sutra_5_4_56(c) : return _in(c, "stem", {"deva", "manuṣya", "puruṣa", "martya"}) and _in(c, "case", {"dvitiya", "saptami"})
def sutra_5_4_57(c) : return _eq(c, "semantic", "avyakta_anukaraṇa") and _eq(c, "stem_class", "dvyac_avara_ardha") and _eq(c, "suffix", "ḍāc")
def sutra_5_4_58(c) : return _eq(c, "stem", "kṛñ") and _in(c, "purva_pada", {"dvitīya", "tṛtīya", "śambabīja"}) and _eq(c, "semantic", "kṛṣi")
def sutra_5_4_59(c) : return _eq(c, "stem_class", "saṅkhya_guṇa_anta") and _eq(c, "rule", "continuation")
def sutra_5_4_60(c) : return _eq(c, "stem", "samaya") and _eq(c, "semantic", "yāpanā")
def sutra_5_4_61(c) : return _in(c, "stem", {"sapatra", "niṣpatra"}) and _eq(c, "semantic", "ati_vyathana")
def sutra_5_4_62(c) : return _eq(c, "stem", "niṣkula") and _eq(c, "semantic", "niṣkoṣaṇa")
def sutra_5_4_63(c) : return _in(c, "stem", {"sukha", "priya"}) and _eq(c, "semantic", "ānulomya")
def sutra_5_4_64(c) : return _eq(c, "stem", "duḥkha") and _eq(c, "semantic", "prātilomya")
def sutra_5_4_65(c) : return _eq(c, "stem", "śūla") and _eq(c, "semantic", "pāka")
def sutra_5_4_66(c) : return _eq(c, "stem", "satya") and _eq(c, "semantic", "aśapatha")
def sutra_5_4_67(c) : return _eq(c, "stem", "madra") and _eq(c, "semantic", "parivāpaṇa")
def sutra_5_4_68(c) : return _eq(c, "section", "samāsānta") and _eq(c, "rule", "adhikara")
def sutra_5_4_69(c) : return _eq(c, "semantic", "pūjana") and _eq(c, "rule", "blocking")
def sutra_5_4_70(c) : return _eq(c, "stem", "kim") and _eq(c, "semantic", "kṣepa")
def sutra_5_4_71(c) : return _eq(c, "compound_type", "naṅ_tatpurusha") and _eq(c, "rule", "continuation")
def sutra_5_4_72(c) : return _eq(c, "stem", "path") and bool(c.get("optional"))
def sutra_5_4_73(c) : return _eq(c, "compound_type", "bahuvrihi") and _eq(c, "semantic", "saṅkhyeya") and _in(c, "stem_class", {"ḍac", "bahu_gaṇa"})
def sutra_5_4_74(c) : return _in(c, "stem", {"ṛk", "pūr", "ap_dhūr", "patha"}) and _eq(c, "stem_final", "anakṣa")
def sutra_5_4_75(c) : return _in(c, "purva_pada", {"prati", "anu", "ava"}) and _in(c, "stem", {"sāma", "loma"}) and _eq(c, "suffix", "ac")
def sutra_5_4_76(c) : return _eq(c, "stem", "akṣṇa") and _eq(c, "semantic", "adarśana")
def sutra_5_4_77(c) : return _eq(c, "stem_class", "acatura_etc_list") and _eq(c, "rule", "samāsānta_ac")
def sutra_5_4_78(c) : return _in(c, "stem", {"brahman", "hastin"}) and _eq(c, "stem_final", "varcas")
def sutra_5_4_79(c) : return _in(c, "stem", {"ava", "samadhi"}) and _eq(c, "stem_final", "tamas")
def sutra_5_4_80(c) : return _eq(c, "stem", "śvas") and _in(c, "stem_final", {"vasīyas", "śreyas"})
def sutra_5_4_81(c) : return _eq(c, "stem", "anvavatapta") and _eq(c, "stem_final", "rahas")
def sutra_5_4_82(c) : return _eq(c, "purva_pada", "prati") and _eq(c, "stem_final", "uras") and _eq(c, "case", "saptami")
def sutra_5_4_83(c) : return _eq(c, "stem", "anugava") and _eq(c, "semantic", "āyāma")
def sutra_5_4_84(c) : return _in(c, "stem", {"dvistāvā", "tristāvā"}) and _eq(c, "stem_final", "vedi")
def sutra_5_4_85(c) : return _eq(c, "purva_pada", "upasarga") and _eq(c, "stem_final", "adhvan")
def sutra_5_4_86(c) : return _eq(c, "compound_type", "tatpurusha") and _eq(c, "stem_final", "aṅguli") and _eq(c, "purva_pada", "saṅkhya_avyaya")
def sutra_5_4_87(c) : return _eq(c, "stem", "ahar") and _in(c, "purva_pada", {"sarva", "ekadeśa", "saṅkhya", "puṇya"})
def sutra_5_4_88(c) : return _eq(c, "stem", "ahnan") and _in(c, "purva_pada_class", {"ahar"})
def sutra_5_4_89(c) : return _eq(c, "stem_class", "non_saṅkhyādi") and _eq(c, "semantic", "samāhāra") and _eq(c, "rule", "blocking")
def sutra_5_4_90(c) : return _in(c, "stem", {"uttama", "eka"}) and _eq(c, "rule", "continuation")
def sutra_5_4_91(c) : return _in(c, "stem", {"rāja", "ahas", "sakhi"}) and _eq(c, "suffix", "ṭac")
def sutra_5_4_92(c) : return _eq(c, "stem", "go") and _eq(c, "operation", "ataddhita_luk")
def sutra_5_4_93(c) : return _eq(c, "stem", "agra") and _eq(c, "stem_final", "uras")
def sutra_5_4_94(c) : return _in(c, "stem_final", {"aśma", "āyas", "saras"}) and _eq(c, "stem_class", "anaḥ") and _in(c, "domain", {"jāti", "samjna"})
def sutra_5_4_95(c) : return _in(c, "stem", {"grāma", "kauṭa"}) and _eq(c, "stem_final", "takṣan")
def sutra_5_4_96(c) : return _eq(c, "stem", "ati") and _eq(c, "stem_final", "śvan")
def sutra_5_4_97(c) : return _eq(c, "semantic", "upamāna") and _eq(c, "stem_class", "aprāṇi")
def sutra_5_4_98(c) : return _in(c, "purva_pada", {"uttara", "mṛga"}) and _eq(c, "stem_final", "sakthi")
def sutra_5_4_99(c) : return _eq(c, "stem", "nau") and _eq(c, "stem_class", "dvigu")
def sutra_5_4_100(c): return _eq(c, "stem", "ardha") and _eq(c, "rule", "continuation")
def sutra_5_4_101(c): return _eq(c, "stem", "khārī") and _eq(c, "dialect", "pracya")
def sutra_5_4_102(c): return _in(c, "stem", {"dvi", "tri"}) and _eq(c, "stem_final", "añjali")
def sutra_5_4_103(c): return _eq(c, "stem_final", "anasanta") and _eq(c, "gender", "neuter") and bool(c.get("is_vedic"))
def sutra_5_4_104(c): return _eq(c, "stem", "brahman") and _eq(c, "semantic", "jānapada_ākhya")
def sutra_5_4_105(c): return _in(c, "stem", {"ku", "mahat"}) and bool(c.get("optional"))
def sutra_5_4_106(c): return _eq(c, "compound_type", "dvandva") and _eq(c, "stem_final", "ca_uda_ṣaha_anta") and _eq(c, "semantic", "samāhāra")
def sutra_5_4_107(c): return _eq(c, "compound_type", "avyayībhāva") and _eq(c, "stem_class", "śarat_prabhṛti")
def sutra_5_4_108(c): return _eq(c, "stem_final", "anaḥ") and _eq(c, "rule", "continuation")
def sutra_5_4_109(c): return _eq(c, "gender", "napuṃsaka") and bool(c.get("optional"))
def sutra_5_4_110(c): return _in(c, "stem", {"nadī", "paurṇamāsī", "āgrahāyaṇī"}) and _eq(c, "rule", "continuation")
def sutra_5_4_111(c): return _eq(c, "stem_class", "jhayanta") and _eq(c, "rule", "continuation")
def sutra_5_4_112(c): return _eq(c, "stem", "gireḥ") and _eq(c, "author", "senaka")
def sutra_5_4_113(c): return _eq(c, "compound_type", "bahuvrihi") and _in(c, "stem_final", {"sakthi", "akṣi"}) and _eq(c, "stem_class", "svāṅga") and _eq(c, "suffix", "ṣac")
def sutra_5_4_114(c): return _eq(c, "stem", "aṅguli") and _eq(c, "stem_final", "dāru")
def sutra_5_4_115(c): return _in(c, "stem", {"dvi", "tri"}) and _eq(c, "stem_final", "mūrdhan") and _eq(c, "suffix", "ṣa")
def sutra_5_4_116(c): return _in(c, "stem_class", {"pūraṇī", "pramāṇī"}) and _eq(c, "suffix", "ap")
def sutra_5_4_117(c): return _in(c, "stem", {"antar", "bahis"}) and _eq(c, "stem_final", "loma")
def sutra_5_4_118(c): return _eq(c, "stem_final", "nāsikā") and _eq(c, "domain", "samjna") and not _eq(c, "stem_class", "asthūla") and _eq(c, "substitute", "nas")
def sutra_5_4_119(c): return _eq(c, "purva_pada_class", "upasarga") and _eq(c, "rule", "continuation")
def sutra_5_4_120(c): return _in(c, "stem", {"suprātar", "suśvas", "sudivas", "sārikukṣa", "caturaśra"}) and _eq(c, "rule", "continuation")
def sutra_5_4_121(c): return _in(c, "purva_pada_class", {"naṅ", "duḥ", "su"}) and _in(c, "stem_final", {"hali", "sakthi"}) and bool(c.get("optional"))
def sutra_5_4_122(c): return _in(c, "stem", {"prajā", "medha"}) and _eq(c, "suffix", "asic") and _eq(c, "rule", "always")
def sutra_5_4_123(c): return _eq(c, "stem", "bahuprajā") and bool(c.get("is_vedic"))
def sutra_5_4_124(c): return _eq(c, "stem", "dharma") and _eq(c, "suffix", "anic") and _eq(c, "stem_class", "kevala")
def sutra_5_4_125(c): return _eq(c, "stem", "jambhā") and _in(c, "stem_final", {"suharita", "tṛṇa", "soma"})
def sutra_5_4_126(c): return _eq(c, "stem", "dakṣiṇa") and _eq(c, "suffix", "ermā") and _eq(c, "semantic", "lubdha_yoga")
def sutra_5_4_127(c): return _eq(c, "suffix", "ic") and _eq(c, "semantic", "karma_vyatihāra")
def sutra_5_4_128(c): return _eq(c, "stem_class", "dvidaṇḍyādi") and _eq(c, "rule", "continuation")
def sutra_5_4_129(c): return _in(c, "purva_pada", {"pra", "sam"}) and _eq(c, "stem_final", "jānu") and _eq(c, "substitute", "jñu")
def sutra_5_4_130(c): return _eq(c, "stem", "ūrdhva") and bool(c.get("optional"))
def sutra_5_4_131(c): return _eq(c, "stem", "ūdhas") and _eq(c, "suffix", "anaṅ")
def sutra_5_4_132(c): return _eq(c, "stem", "dhanus") and _eq(c, "rule", "continuation")
def sutra_5_4_133(c): return bool(c.get("optional")) and _eq(c, "domain", "samjna")
def sutra_5_4_134(c): return _eq(c, "stem", "jāyā") and _eq(c, "suffix", "niṅ")
def sutra_5_4_135(c): return _eq(c, "stem", "gandha") and _in(c, "stem_final", {"udagra", "pūti", "su", "surabhi"})
def sutra_5_4_136(c): return _eq(c, "semantic", "alpa_ākhyā") and _eq(c, "rule", "continuation")
def sutra_5_4_137(c): return _eq(c, "semantic", "upamāna") and _eq(c, "rule", "continuation")
def sutra_5_4_138(c): return _eq(c, "stem", "pād") and _eq(c, "operation", "lopa") and not _eq(c, "stem_class", "hasti_ādi")
def sutra_5_4_139(c): return _in(c, "stem", {"kumbhapadī"}) and _eq(c, "rule", "continuation")
def sutra_5_4_140(c): return _eq(c, "purva_pada_class", "saṅkhya_su") and _eq(c, "rule", "continuation")
def sutra_5_4_141(c): return _eq(c, "stem", "vayas") and _eq(c, "stem_final", "danta") and _eq(c, "substitute", "datṛ")
def sutra_5_4_142(c): return bool(c.get("is_vedic")) and _eq(c, "rule", "continuation")
def sutra_5_4_143(c): return _eq(c, "gender", "strī") and _eq(c, "domain", "samjna")
def sutra_5_4_144(c): return _in(c, "stem", {"śyāvā", "rokā"}) and bool(c.get("optional"))
def sutra_5_4_145(c): return _in(c, "stem_final", {"agrānta", "śuddha", "śubhra", "vṛṣa", "varāha"}) and _eq(c, "rule", "continuation")
def sutra_5_4_146(c): return _eq(c, "stem", "kakuda") and _eq(c, "semantic", "avasthā") and _eq(c, "operation", "lopa")
def sutra_5_4_147(c): return _eq(c, "stem", "trikakud") and _eq(c, "semantic", "parvata")
def sutra_5_4_148(c): return _in(c, "purva_pada", {"ud", "vi"}) and _eq(c, "stem_final", "kākuda")
def sutra_5_4_149(c): return _eq(c, "stem", "pūrṇa") and bool(c.get("optional"))
def sutra_5_4_150(c): return _in(c, "stem", {"suhṛd", "durhṛd"}) and _in(c, "semantic", {"mitra", "amitra"})
def sutra_5_4_151(c): return _eq(c, "stem_class", "uraḥprabhṛti") and _eq(c, "suffix", "kap")
def sutra_5_4_152(c): return _eq(c, "stem_final", "in") and _eq(c, "gender", "strī")
def sutra_5_4_153(c): return _in(c, "stem_final", {"nadī", "ṛt"}) and _eq(c, "rule", "continuation")
def sutra_5_4_154(c): return _eq(c, "stem", "śeṣa") and bool(c.get("optional"))
def sutra_5_4_155(c): return _eq(c, "domain", "samjna") and _eq(c, "rule", "blocking")
def sutra_5_4_156(c): return _eq(c, "stem_final", "īyasa") and _eq(c, "rule", "continuation")
def sutra_5_4_157(c): return _eq(c, "stem", "bhrātṛ") and _eq(c, "semantic", "vandita")
def sutra_5_4_158(c): return _eq(c, "stem_final", "ṛta") and bool(c.get("is_vedic"))
def sutra_5_4_159(c): return _in(c, "stem", {"nāḍī", "tantrī"}) and _eq(c, "stem_class", "svāṅga")
def sutra_5_4_160(c): return _eq(c, "stem", "niṣpravāṇi") and _eq(c, "rule", "continuation")


# ---------------------------------------------------------------------------
# Fixtures — compact tables, expanded via _build_compact_fixtures
# ---------------------------------------------------------------------------

def _build_compact_fixtures(raw):
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


_FX_5_1_RAW = [
    ("5.1.1", "section:prāk_krīta",           "suffix:cha"),
    ("5.1.2", "stem_class:ugavādi",           "suffix:at"),
    ("5.1.3", "stem:kambala",                 "domain:samjna"),
    ("5.1.4", "stem_class:haviṣ_apūpādi",     "optional:1"),
    ("5.1.5", "semantic:tasmai_hita",         "rule:continuation"),
    ("5.1.6", "stem_class:śarīrāvayava",      "suffix:yat"),
    ("5.1.7", "stem:khala",                   "rule:continuation"),
    ("5.1.8", "stem:aja",                     "suffix:thyan"),
    ("5.1.9", "stem_final:ātman",             "suffix:kha"),
    ("5.1.10","stem:sarva",                   "suffix:ṇa"),
    ("5.1.11","stem:māṇava",                  "suffix:khañ"),
    ("5.1.12","semantic:tadartha_vikṛti",     "rule:continuation"),
    ("5.1.13","stem:chadis",                  "suffix:ḍhañ"),
    ("5.1.14","stem:ṛṣabha",                  "suffix:ñya"),
    ("5.1.15","stem:carmaṇa",                 "suffix:añ"),
    ("5.1.16","semantic:tad_asya_tad_asmin_syat","rule:continuation"),
    ("5.1.17","stem:parikhā",                 "suffix:ḍhañ"),
    ("5.1.18","section:prāgvateḥ",            "suffix:ṭhañ"),
    ("5.1.19","semantic:ārha",                "stem_class:non_gopuccha", "suffix:ṭhak"),
    ("5.1.20","in_compound:0",                "stem_class:niṣkādi"),
    ("5.1.21","stem_final:śata",              "suffix:ṭhan"),
    ("5.1.22","stem_class:saṅkhya_atiśadanta","suffix:kan"),
    ("5.1.23","stem_class:vatu",              "augment:iḍ",            "optional:1"),
    ("5.1.24","stem:viṃśati",                 "suffix:ḍvun"),
    ("5.1.25","stem:kaṃsa",                   "suffix:ṭiṭhan"),
    ("5.1.26","stem:śūrpa",                   "suffix:añ",             "optional:1"),
    ("5.1.27","stem:śatamāna",                "suffix:aṇ"),
    ("5.1.28","stem_class:adhyardha_pūrva_dvigu","operation:luk"),
    ("5.1.29","stem:kārṣāpaṇa",               "optional:1"),
    ("5.1.30","stem:dvi_tri_pūrva_niṣka",     "rule:continuation"),
    ("5.1.31","stem:bista",                   "rule:continuation"),
    ("5.1.32","stem:viṃśatika",               "suffix:kha"),
    ("5.1.33","stem:khārī",                   "suffix:īkan"),
    ("5.1.34","stem:paṇa",                    "suffix:at"),
    ("5.1.35","stem:śāṇa",                    "optional:1"),
    ("5.1.36","stem_class:dvi_tri_pūrva",     "suffix:aṇ"),
    ("5.1.37","semantic:tena_krīta",          "rule:continuation"),
    ("5.1.38","semantic:saṃyoga_utpāta",      "rule:continuation"),
    ("5.1.39","stem_class:go_dvyac_aśva",     "suffix:yat"),
    ("5.1.40","stem:putra",                   "suffix:cha"),
    ("5.1.41","stem:sarvabhūmi",              "suffix:aṇ"),
    ("5.1.42","semantic:tasya_īśvara",        "rule:continuation"),
    ("5.1.43","semantic:tatra_vidita",        "rule:continuation"),
    ("5.1.44","stem:loka",                    "suffix:ṭhañ"),
    ("5.1.45","semantic:tasya_vāpa",          "rule:continuation"),
    ("5.1.46","stem:pātra",                   "suffix:ṣṭhan"),
    ("5.1.47","semantic:vṛddhi_āya_lābha_śulka_upadā","rule:continuation"),
    ("5.1.48","stem:pūraṇa",                  "suffix:ṭhan"),
    ("5.1.49","stem:bhāga",                   "suffix:yat"),
    ("5.1.50","stem_class:bhārādi_vaṃśādi",   "semantic:harati"),
    ("5.1.51","stem:vasna",                   "suffix:ṭhan"),
    ("5.1.52","semantic:sambhavati_avaharati_pacati","rule:continuation"),
    ("5.1.53","stem:āḍhaka",                  "suffix:kha",            "optional:1"),
    ("5.1.54","stem_class:dvigu",             "suffix:ṭhaṃś"),
    ("5.1.55","stem:kulija",                  "operation:luk"),
    ("5.1.56","semantic:aṃśa_vasna_bhṛti",    "rule:continuation"),
    ("5.1.57","semantic:tad_asya_parimāṇa",   "rule:continuation"),
    ("5.1.58","stem_class:saṅkhya",           "domain:samjna"),
    ("5.1.59","stem_class:saṅkhya_paṅkti",    "rule:continuation"),
    ("5.1.60","stem:pañcat",                  "semantic:varga",        "optional:1"),
    ("5.1.61","stem:saptan",                  "suffix:añ",             "is_vedic:1"),
    ("5.1.62","stem:triṃśat",                 "semantic:brāhmaṇa",     "suffix:ḍaṇ"),
    ("5.1.63","semantic:tad_arhati",          "rule:continuation"),
    ("5.1.64","stem_class:chedādi",           "rule:always"),
    ("5.1.65","stem_class:śīrṣaccheda",       "suffix:yat"),
    ("5.1.66","stem_class:daṇḍādi",           "rule:continuation"),
    ("5.1.67","is_vedic:1",                   "rule:continuation"),
    ("5.1.68","stem:pātra",                   "suffix:ghaṃś"),
    ("5.1.69","stem:kaḍaṅgara",               "rule:continuation"),
    ("5.1.70","stem:sthālībila",              "rule:continuation"),
    ("5.1.71","stem:yajña",                   "suffix:gha"),
    ("5.1.72","stem:pārāyaṇa",                "semantic:vartayati"),
    ("5.1.73","semantic:saṃśaya_āpanna",      "rule:continuation"),
    ("5.1.74","stem:yojana",                  "semantic:gacchati"),
    ("5.1.75","stem:path",                    "suffix:ṣkan"),
    ("5.1.76","stem:pantha",                  "suffix:ṇa",             "rule:always"),
    ("5.1.77","stem:uttarapatha",             "semantic:āhṛta"),
    ("5.1.78","semantic:kāla",                "rule:continuation"),
    ("5.1.79","semantic:tena_nirvṛtta",       "rule:continuation"),
    ("5.1.80","semantic:tam_adhīṣṭa",         "rule:continuation"),
    ("5.1.81","stem:māsa",                    "semantic:vayas",        "suffix:yat"),
    ("5.1.82","stem_class:dvigu",             "suffix:yap"),
    ("5.1.83","stem:ṣaṇmāsa",                 "suffix:ṇyat"),
    ("5.1.84","semantic:avayas",              "suffix:ṭhaṃś"),
    ("5.1.85","stem:samā",                    "suffix:kha"),
    ("5.1.86","stem_class:dvigu",             "optional:1"),
    ("5.1.87","stem:rātri",                   "rule:continuation"),
    ("5.1.88","stem:varṣa",                   "operation:luk"),
    ("5.1.89","semantic:cittavat",            "rule:always"),
    ("5.1.90","stem:ṣaṣṭika",                 "semantic:ṣaṣṭi_rātreṇa_pacyate"),
    ("5.1.91","stem_final:vatsarānta",        "suffix:cha",            "is_vedic:1"),
    ("5.1.92","purva_pada:sam",               "suffix:kha"),
    ("5.1.93","semantic:tena_parijayya_labhya_kārya_sukara","rule:continuation"),
    ("5.1.94","semantic:tad_asya_brahmacarya","rule:continuation"),
    ("5.1.95","semantic:yajñākhya_dakṣiṇā",   "rule:continuation"),
    ("5.1.96","semantic:tatra_dīyate_kārya",  "rule:bhava_vat"),
    ("5.1.97","stem_class:vyuṣṭādi",          "suffix:aṇ"),
    ("5.1.98","stem:yathākatha",              "suffix:ṇa"),
    ("5.1.99","semantic:sampādini",           "rule:continuation"),
    ("5.1.100","stem:karmaveṣa",              "suffix:yat"),
    ("5.1.101","stem_class:saṃtāpādi",        "semantic:tasmai_prabhavati"),
    ("5.1.102","stem:yoga",                   "suffix:yat"),
    ("5.1.103","stem:karman",                 "suffix:ukañ"),
    ("5.1.104","stem:samaya",                 "semantic:tasya_prāpta"),
    ("5.1.105","stem:ṛtu",                    "suffix:aṇ"),
    ("5.1.106","is_vedic:1",                  "suffix:ghas"),
    ("5.1.107","stem:kāla",                   "suffix:yat"),
    ("5.1.108","semantic:prakṛṣṭa",           "suffix:ṭhañ"),
    ("5.1.109","semantic:prayojana",          "rule:continuation"),
    ("5.1.110","stem:viśākhā",                "semantic:mantha"),
    ("5.1.111","stem_class:anupravacanādi",   "suffix:cha"),
    ("5.1.112","stem:samāpana",               "has_sapurva:1"),
    ("5.1.113","stem:aikāgārika",             "semantic:caura"),
    ("5.1.114","stem:ākālika",                "suffix:ḍa"),
    ("5.1.115","semantic:tena_tulya_kriyā",   "suffix:vati"),
    ("5.1.116","semantic:tatra_tasya_iva",    "rule:continuation"),
    ("5.1.117","semantic:tad_arha",           "rule:continuation"),
    ("5.1.118","stem_class:upasarga",         "is_vedic:1",            "semantic:dhātvartha"),
    ("5.1.119","semantic:tasya_bhāva",        "suffix:tva"),
    ("5.1.120","rule:ā_ca_tvāt",              "section:bhāva"),
    ("5.1.121","compound_type:naṅ_tatpurusha","stem:acatura",          "rule:blocking"),
    ("5.1.122","stem_class:pṛthvādi",         "suffix:imanic"),
    ("5.1.123","stem_class:varṇa_dṛḍhādi",    "suffix:ṣyañ"),
    ("5.1.124","stem_class:guṇavacana_brāhmaṇādi","semantic:karman"),
    ("5.1.125","stem_class:stenādi",          "operation:yat_n_lopa"),
    ("5.1.126","stem:sakhi",                  "suffix:ya"),
    ("5.1.127","stem:kapi",                   "suffix:ḍhak"),
    ("5.1.128","stem_final:pati",             "suffix:yak"),
    ("5.1.129","stem_class:prāṇabhṛj_jāti_vayo_vacana","suffix:añ"),
    ("5.1.130","stem_final:hāyana",           "suffix:aṇ"),
    ("5.1.131","stem_final:igantā",           "upadha:laghu"),
    ("5.1.132","upadha:y",                    "stem_class:guru_uttama","suffix:vuñ"),
    ("5.1.133","compound_type:dvandva",       "stem_class:manojñādi"),
    ("5.1.134","stem:gotra",                  "semantic:ślāghā_tyākāra"),
    ("5.1.135","stem_class:hotrā",            "suffix:cha"),
    ("5.1.136","stem:brahman",                "suffix:tva"),
]


FIXTURES: dict[str, tuple[dict, dict]] = _build_compact_fixtures(_FX_5_1_RAW)


_FX_5_2_RAW = [
    ("5.2.1", "stem_class:dhānya",            "semantic:bhavana_kshetra","suffix:khañ"),
    ("5.2.2", "stem:vrīhi",                   "suffix:ḍhak"),
    ("5.2.3", "stem:yava",                    "suffix:at"),
    ("5.2.4", "stem:tila",                    "optional:1"),
    ("5.2.5", "stem:sarvacarman",             "semantic:kṛta",         "suffix:kha"),
    ("5.2.6", "stem:yathāmukha",              "semantic:darśana"),
    ("5.2.7", "stem:tat_sarvādi",             "stem_final:path"),
    ("5.2.8", "stem:āprapada",                "semantic:prāpnoti"),
    ("5.2.9", "stem:anupada",                 "rule:continuation"),
    ("5.2.10","stem:paravara",                "semantic:anubhavati"),
    ("5.2.11","stem:avārapāra",               "semantic:gāmī"),
    ("5.2.12","stem:samāṃsamā",               "semantic:vijāyate"),
    ("5.2.13","stem:adyaśvīnā",               "semantic:avaṣṭabdha"),
    ("5.2.14","stem:āgavīna",                 None),
    ("5.2.15","stem:anugu",                   "semantic:alaṃgāmī"),
    ("5.2.16","stem:adhvan",                  "suffix:yat"),
    ("5.2.17","stem:abhyamitra",              "suffix:cha"),
    ("5.2.18","stem:goṣṭha",                  "suffix:khañ",           "semantic:bhūtapūrva"),
    ("5.2.19","stem:aśva",                    "semantic:ekāhagama"),
    ("5.2.20","stem:śālīna",                  "semantic:adhṛṣṭa"),
    ("5.2.21","stem:vrāta",                   "semantic:jīvati"),
    ("5.2.22","stem:sāptapadīna",             "semantic:sakhya"),
    ("5.2.23","stem:haiyaṃgavīna",            "domain:samjna"),
    ("5.2.24","semantic:tasya_pāka_mūla",     "stem_class:pīlvādi"),
    ("5.2.25","stem:pakṣa",                   "suffix:ti"),
    ("5.2.26","semantic:tena_vitta",          "suffix:cuñcup"),
    ("5.2.27","stem:vi",                      "suffix:nāñ"),
    ("5.2.28","stem:vi",                      "suffix:śāla"),
    ("5.2.29","stem:sam",                     "suffix:kaṭac"),
    ("5.2.30","stem:ava",                     "suffix:kuṭāra"),
    ("5.2.31","stem:nata",                    "semantic:nāsikā",       "domain:samjna"),
    ("5.2.32","stem:ni",                      "suffix:biḍac"),
    ("5.2.33","suffix:inac",                  "rule:continuation"),
    ("5.2.34","stem:upadhi",                  "suffix:tyak"),
    ("5.2.35","stem:ghaṭa",                   "semantic:karman",       "suffix:ṭhac"),
    ("5.2.36","stem_class:tārakādi",          "semantic:tad_asya_saṃjāta","suffix:itac"),
    ("5.2.37","semantic:pramāṇa",             "suffix:dvayasac"),
    ("5.2.38","stem:puruṣa",                  "suffix:aṇ"),
    ("5.2.39","stem:yad",                     "semantic:parimāṇa",     "suffix:vatup"),
    ("5.2.40","stem:kim",                     "substitute:va",         "augment:gha"),
    ("5.2.41","stem:kim",                     "semantic:saṅkhya_parimāṇa","suffix:ḍati"),
    ("5.2.42","stem_class:saṅkhya",           "semantic:avayava",      "suffix:tayap"),
    ("5.2.43","stem:dvi",                     "substitute:ayaj"),
    ("5.2.44","stem:ubha",                    "accent:udatta",         "rule:always"),
    ("5.2.45","semantic:tad_asminn_adhikam",  "stem_final:daśānta",    "suffix:ḍa"),
    ("5.2.46","stem_final:śadanta_viṃśateḥ", "rule:continuation"),
    ("5.2.47","stem_class:saṅkhya",           "semantic:guṇa_nimāne",  "suffix:mayaṭ"),
    ("5.2.48","stem_class:saṅkhya",           "semantic:tasya_pūraṇa", "suffix:ḍaṭ"),
    ("5.2.49","stem_final:nānta",             "stem_class:non_saṅkhyādi","augment:maṭ"),
    ("5.2.50","is_vedic:1",                   "suffix:thaṭ"),
    ("5.2.51","stem:ṣaṭ",                     "augment:thuk"),
    ("5.2.52","stem:bahu",                    "augment:tithuk"),
    ("5.2.53","stem:vatu",                    "augment:ithuk"),
    ("5.2.54","stem:dvi",                     "suffix:tīya"),
    ("5.2.55","stem:tri",                     "operation:samprasāraṇa"),
    ("5.2.56","stem_class:viṃśatyādi",        "suffix:tamaṭ",          "optional:1"),
    ("5.2.57","stem:śata",                    "rule:always"),
    ("5.2.58","stem_class:ṣaṣṭyādi_non_saṅkhyādi","rule:continuation"),
    ("5.2.59","stem_class:matu",              "stem:sūkta",            "suffix:cha"),
    ("5.2.60","stem:adhyāya",                 "operation:luk"),
    ("5.2.61","stem_class:vimuktādi",         "suffix:aṇ"),
    ("5.2.62","stem_class:goṣadādi",          "suffix:vun"),
    ("5.2.63","stem:patha",                   "semantic:kuśala"),
    ("5.2.64","stem_class:ākarṣādi",          "suffix:kan"),
    ("5.2.65","stem:dhana",                   "semantic:kāma"),
    ("5.2.66","stem_class:svāṅga",            "semantic:prasita"),
    ("5.2.67","stem:udara",                   "suffix:ṭhag",           "semantic:ādyūna"),
    ("5.2.68","stem:sasya",                   "semantic:parijāta"),
    ("5.2.69","stem:aṃśa",                    "semantic:hārī"),
    ("5.2.70","stem:tantra",                  "semantic:acirāpahṛta"),
    ("5.2.71","stem:brāhmaṇa",                "domain:samjna"),
    ("5.2.72","stem:śīta",                    "semantic:kāri"),
    ("5.2.73","semantic:adhika",              "rule:continuation"),
    ("5.2.74","stem:anukā",                   "semantic:kamitā"),
    ("5.2.75","stem:pārśva",                  "semantic:anvicchati"),
    ("5.2.76","stem:ayaḥśūla",                "suffix:ṭhak"),
    ("5.2.77","stem:tāvatittha",              "semantic:grahaṇa",      "optional:1"),
    ("5.2.78","semantic:grāmaṇī",             "rule:continuation"),
    ("5.2.79","stem:śṛṅkhala",                "semantic:bandhana",     "stem_final:karabha"),
    ("5.2.80","stem:utka",                    "semantic:unmanas"),
    ("5.2.81","stem_class:kāla_prayojana",    "semantic:roga"),
    ("5.2.82","semantic:tad_asminn_anna_prāya","domain:samjna"),
    ("5.2.83","stem:kulmāṣa",                 "suffix:añ"),
    ("5.2.84","stem:śrotriya",                "semantic:chando_adhīte"),
    ("5.2.85","stem:śrāddha",                 "semantic:bhukta",       "suffix:ini"),
    ("5.2.86","stem:pūrva",                   "suffix:ini"),
    ("5.2.87","has_sapurva:1",                "rule:continuation"),
    ("5.2.88","stem_class:iṣṭādi",            "rule:continuation"),
    ("5.2.89","is_vedic:1",                   "stem:paripanthi",       "semantic:paryavasthātṛ"),
    ("5.2.90","stem:anupadi",                 "semantic:anveṣṭṛ"),
    ("5.2.91","stem:sākṣād",                  "semantic:draṣṭṛ",       "domain:samjna"),
    ("5.2.92","stem:kṣetriya",                "semantic:para_kṣetra_cikitsya"),
    ("5.2.93","stem:indriya",                 "semantic:indra_liṅga"),
    ("5.2.95","stem_class:rasādi",            "rule:continuation"),
    ("5.2.96","stem_class:prāṇistha",         "stem_final:ā",          "suffix:lajan",          "optional:1"),
    ("5.2.97","stem_class:sidhmādi",          "rule:continuation"),
    ("5.2.98","stem:vatsa",                   "semantic:kāma"),
    ("5.2.99","stem_class:phenādi",           "suffix:lac"),
    ("5.2.100","stem_class:lomādi_pāmādi_picchādi","suffix:śanelac"),
    ("5.2.101","stem:prajñā",                 "suffix:ṇa"),
    ("5.2.102","stem:tapas",                  "suffix:vini"),
    ("5.2.103","rule:continuation",           "suffix:aṇ"),
    ("5.2.104","stem:sikatā",                 "rule:continuation"),
    ("5.2.105","semantic:deśa",               "suffix:lup"),
    ("5.2.106","stem:danta",                  "semantic:unnata",       "suffix:urac"),
    ("5.2.107","stem:ūṣa",                    "suffix:ra"),
    ("5.2.108","stem:dyu",                    "suffix:ma"),
    ("5.2.109","stem:keśa",                   "suffix:va",             "optional:1"),
    ("5.2.110","stem:gāṇḍī",                  "semantic:ajagā",        "domain:samjna"),
    ("5.2.111","stem:kāṇḍa",                  "augment:īra_īrac"),
    ("5.2.112","stem:rajas",                  "suffix:valac"),
    ("5.2.113","stem:dantaśikha",             "domain:samjna"),
    ("5.2.114","stem:jyotsnā",                "suffix:matup"),
    ("5.2.115","stem_final:ata",              "suffix:ini"),
    ("5.2.116","stem_class:vrīhyādi",         "rule:continuation"),
    ("5.2.117","stem_class:tundādi",          "suffix:ilac"),
    ("5.2.118","purva_pada:eka_go",           "suffix:ṭhañ",           "rule:always"),
    ("5.2.119","stem:niṣka",                  "stem_final:śata_sahasra_anta"),
    ("5.2.120","stem:rūpa",                   "semantic:āhata"),
    ("5.2.121","stem:asu",                    "suffix:vini"),
    ("5.2.122","is_vedic:1",                  "rule:bahulam"),
    ("5.2.123","stem:ūrṇā",                   "suffix:yus"),
    ("5.2.124","stem:vāc",                    "suffix:gmini"),
    ("5.2.125","suffix:ālaj",                 "semantic:bahu_bhāṣin"),
    ("5.2.126","stem:svāmin",                 "semantic:aiśvarya"),
    ("5.2.127","stem_class:arśa_ādi",         "suffix:ac"),
    ("5.2.128","stem_class:dvandva_upatāpa_garhya_prāṇistha","suffix:ini"),
    ("5.2.129","stem:vāta",                   "augment:kuk"),
    ("5.2.130","semantic:vayas",              "stem_class:pūraṇa"),
    ("5.2.131","stem_class:sukhādi",          "rule:continuation"),
    ("5.2.132","stem_final:dharma",           "rule:continuation"),
    ("5.2.133","stem:hasta",                  "semantic:jati"),
    ("5.2.134","stem:varṇa",                  "semantic:brahmacārin"),
    ("5.2.135","stem_class:puṣkarādi",        "semantic:deśa"),
    ("5.2.136","stem_class:balādi",           "suffix:matup"),
    ("5.2.137","domain:samjna",               "suffix:manma"),
    ("5.2.138","stem:kaṃ",                    "suffix:babhayu"),
    ("5.2.139","stem:tundi",                  "suffix:bha"),
    ("5.2.140","stem:ahaṃ",                   "suffix:yus"),
]


FIXTURES.update(_build_compact_fixtures(_FX_5_2_RAW))


_FX_5_3_RAW = [
    ("5.3.1", "section:prāgdiśo_vibhakti",    "samjna:vibhakti"),
    ("5.3.2", "stem_class:kim_sarvanāma_bahu_non_dvyādi","rule:continuation"),
    ("5.3.3", "stem:idam",                    "substitute:i"),
    ("5.3.4", "stem:eta",                     "substitute:ra"),
    ("5.3.5", "stem:etad",                    "substitute:aś"),
    ("5.3.6", "stem:sarva",                   "substitute:sa",         "optional:1"),
    ("5.3.7", "case:pancami",                 "suffix:tasil"),
    ("5.3.8", "suffix:tasi",                  "rule:continuation"),
    ("5.3.9", "stem:pari",                    "rule:continuation"),
    ("5.3.10","case:saptami",                 "suffix:tral"),
    ("5.3.11","stem:idam",                    "augment:ha"),
    ("5.3.12","stem:kim",                     "augment:at"),
    ("5.3.13","is_vedic:1",                   "augment:ha",            "optional:1"),
    ("5.3.14","stem_class:itarād",            "rule:continuation"),
    ("5.3.15","stem:sarva",                   "semantic:kāla",         "suffix:dā"),
    ("5.3.16","stem:idam",                    "suffix:rhil"),
    ("5.3.17","stem:adhunā",                  None),
    ("5.3.18","stem:dānīm",                   "rule:continuation"),
    ("5.3.19","stem:tad",                     "suffix:dā"),
    ("5.3.20","stem:tayor",                   "is_vedic:1"),
    ("5.3.21","semantic:anadyatana",          "suffix:rhil",           "optional:1"),
    ("5.3.22","stem:sadya",                   "rule:continuation"),
    ("5.3.23","semantic:prakāra_vacana",      "suffix:thāl"),
    ("5.3.24","stem:idam",                    "suffix:tham_uh"),
    ("5.3.25","stem:kim",                     "rule:continuation"),
    ("5.3.26","suffix:thā",                   "semantic:hetu",         "is_vedic:1"),
    ("5.3.27","stem_class:dik_shabda",        "case:saptami",          "suffix:astāti"),
    ("5.3.28","stem:dakṣiṇā",                 "suffix:atasuc"),
    ("5.3.29","stem:para",                    "optional:1"),
    ("5.3.30","stem:añcer",                   "operation:luk"),
    ("5.3.31","stem:upari",                   "substitute:upariṣṭāt"),
    ("5.3.32","stem:paścāt",                  None),
    ("5.3.33","stem:paśca",                   "is_vedic:1"),
    ("5.3.34","stem:uttara",                  "suffix:āti"),
    ("5.3.35","suffix:enab",                  "case:non_pancami",      "optional:1"),
    ("5.3.36","stem:dakṣiṇa",                 "suffix:āc"),
    ("5.3.37","suffix:āhi",                   "semantic:dūra"),
    ("5.3.38","stem:uttara",                  "rule:continuation"),
    ("5.3.39","stem:pūrva",                   "stem_final:asi_pur_adha_vas"),
    ("5.3.40","suffix:astāti",                "rule:continuation"),
    ("5.3.41","stem:avara",                   "optional:1"),
    ("5.3.42","stem_class:saṅkhya",           "semantic:vidha_artha",  "suffix:dhā"),
    ("5.3.43","semantic:adhikaraṇa_vicāla",   "rule:continuation"),
    ("5.3.44","stem:eka",                     "suffix:dhyamuñ"),
    ("5.3.45","stem:dvi",                     "suffix:dhamuñ"),
    ("5.3.46","stem:edhā",                    "rule:continuation"),
    ("5.3.47","semantic:yāpya",               "suffix:pāśap"),
    ("5.3.48","stem_class:pūraṇa",            "semantic:bhāga",        "suffix:tīyādan"),
    ("5.3.49","stem_class:prāg_ekādaśa",      "is_vedic:0"),
    ("5.3.50","stem:ṣaṣṭha",                  "suffix:ña"),
    ("5.3.51","semantic:māna_paśu_aṅga",      "suffix:kan"),
    ("5.3.52","stem:eka",                     "suffix:ākinic",         "semantic:asahāya"),
    ("5.3.53","semantic:bhūtapūrva",          "suffix:caraṭ"),
    ("5.3.54","case:ṣaṣṭhi",                  "suffix:rūpya"),
    ("5.3.56","stem_class:tin",               "rule:continuation"),
    ("5.3.57","dvivacana_vibhajya_upapade:1", "suffix:tarap"),
    ("5.3.58","stem_class:ajādi",             "stem_class_alt:guṇa_vacana","rule:continuation"),
    ("5.3.59","augment:tu",                   "is_vedic:1"),
    ("5.3.60","stem:praśasya",                "substitute:śra"),
    ("5.3.61","substitute:jya",               "rule:continuation"),
    ("5.3.62","stem:vṛddha",                  "rule:continuation"),
    ("5.3.63","stem:antika",                  "substitute:neda"),
    ("5.3.64","stem:yuvan",                   "suffix:kan",            "optional:1"),
    ("5.3.65","stem_class:vin_matu",          "operation:luk"),
    ("5.3.66","semantic:praśaṃsā",            "suffix:rūpap"),
    ("5.3.67","semantic:iṣad_asamāpta",       "suffix:kalpab"),
    ("5.3.68","stem_class:supo",              "suffix:bahuc",          "position:purastāt",     "optional:1"),
    ("5.3.69","semantic:prakāra_vacana",      "suffix:jātīyar"),
    ("5.3.70","section:prāgivāt",             "suffix:ka"),
    ("5.3.71","stem_class:avyaya",            "suffix:akac",           "position:prāk_ṭi"),
    ("5.3.72","stem:ka",                      "substitute:da"),
    ("5.3.73","semantic:ajñāta",              "rule:continuation"),
    ("5.3.74","semantic:kutsita",             "rule:continuation"),
    ("5.3.75","domain:samjna",                "suffix:kan"),
    ("5.3.76","semantic:anukampā",            "rule:continuation"),
    ("5.3.77","semantic:nīti_tadyuktāt",      "rule:continuation"),
    ("5.3.78","stem_class:bahvac_manuṣya_nāma","suffix:ṭhajvā",        "optional:1"),
    ("5.3.79","suffix:ghan",                  "rule:continuation"),
    ("5.3.80","dialect:pracya",               "stem:upa",              "suffix:aḍac"),
    ("5.3.81","stem_class:jāti_nāman",        "suffix:kan"),
    ("5.3.82","stem_final:ajina",             "operation:uttara_pada_lopa"),
    ("5.3.83","suffix:ṭhāc",                  "stem_final:ūrdhva_dvitīya_ac"),
    ("5.3.84","stem:śevala",                  "stem_final:tṛtīya"),
    ("5.3.85","semantic:alpa",                "rule:continuation"),
    ("5.3.86","semantic:hrasva",              "rule:continuation"),
    ("5.3.87","domain:samjna",                "suffix:kan"),
    ("5.3.88","stem:kuṭī",                    "suffix:ra"),
    ("5.3.89","stem_class:kutvā",             "suffix:ḍupac"),
    ("5.3.90","stem:kāsū",                    "suffix:ṣṭarac"),
    ("5.3.91","stem:vatsa",                   "semantic:tanutva"),
    ("5.3.92","stem:kim",                     "semantic:dvayor_eka_nirddhāraṇa","suffix:ḍatarac"),
    ("5.3.93","semantic:bahūnāṃ_jāti_paripraśna","suffix:ḍatamac",     "optional:1"),
    ("5.3.94","stem_class:ekāt",              "dialect:pracya"),
    ("5.3.95","semantic:avakṣepaṇa",          "suffix:kan"),
    ("5.3.96","semantic:iva_pratikṛti",       "rule:continuation"),
    ("5.3.97","domain:samjna",                "rule:continuation"),
    ("5.3.98","operation:lup",                "semantic:manuṣya"),
    ("5.3.99","semantic:jīvika_apaṇya",       "rule:continuation"),
    ("5.3.100","stem_class:devapathādi",      "rule:continuation"),
    ("5.3.101","stem:vastra",                 "suffix:ḍhañ"),
    ("5.3.102","stem:śilā",                   "suffix:ḍha"),
    ("5.3.103","stem_class:śākhādi",          "suffix:yat"),
    ("5.3.104","semantic:bhavya_dravya",      "rule:continuation"),
    ("5.3.105","stem:kuśāgra",                "suffix:cha"),
    ("5.3.106","stem_class:samāsa",           "semantic:tad_viṣaya"),
    ("5.3.107","stem_class:śarkarādi",        "suffix:aṇ"),
    ("5.3.108","stem_class:aṅgulyādi",        "suffix:ṭhak"),
    ("5.3.109","stem:ekaśālā",                "suffix:ṭhac",           "optional:1"),
    ("5.3.110","stem:karka",                  "suffix:īkak"),
    ("5.3.111","stem:pratna",                 "suffix:thāl",           "is_vedic:1"),
    ("5.3.112","stem:pūgā",                   "suffix:ñya",            "purva_pada:non_grāmaṇī"),
    ("5.3.113","stem_class:vrāta",            "gender:non_strī"),
    ("5.3.114","stem_class:āyudhajīvi",       "suffix:ñyaḍ",           "dialect:vāhīka"),
    ("5.3.115","stem:vṛka",                   "suffix:ṭeṇyaṇ"),
    ("5.3.116","stem_class:dāmanyādi",        "stem_final:trigarta_ṣaṣṭha","suffix:cha"),
    ("5.3.117","stem_class:parśvādi",         "suffix:aṇ"),
    ("5.3.118","stem:abhijit",                "suffix:yañ"),
    ("5.3.119","samjna:tadrāja",              "stem_class:ñyādi"),
]


FIXTURES.update(_build_compact_fixtures(_FX_5_3_RAW))


_FX_5_4_RAW = [
    ("5.4.1", "stem:pādaśata",                "semantic:vīpsā",        "suffix:vun"),
    ("5.4.2", "stem:daṇḍa",                   "rule:continuation"),
    ("5.4.3", "stem_class:sthūlādi",          "semantic:prakāra_vacana","suffix:kan"),
    ("5.4.4", "semantic:anatyantagati",       "suffix_pre:kta"),
    ("5.4.5", "semantic:sāmi_vacana",         "rule:blocking"),
    ("5.4.6", "stem:bṛhatī",                  "semantic:ācchādana"),
    ("5.4.7", "purva_pada:aṣaḍakṣa",          "suffix:kha"),
    ("5.4.8", "stem_class:añcer",             "domain:non_dik_strī",   "optional:1"),
    ("5.4.9", "stem_class:jāti_anta",         "semantic:bandhu",       "suffix:cha"),
    ("5.4.10","stem_final:sthāna_anta",       "sa_sthāna:1",           "optional:1"),
    ("5.4.11","stem:kim",                     "semantic:adravya_prakarṣa","suffix:ām_vat"),
    ("5.4.12","stem:amu",                     "is_vedic:1"),
    ("5.4.13","stem:anugā",                   "suffix:ṭhak"),
    ("5.4.14","suffix_class:ṇacaḥ",           "gender:stri",           "suffix:añ"),
    ("5.4.15","stem:aṇinu",                   "rule:continuation"),
    ("5.4.16","stem:visārin",                 "semantic:matsya"),
    ("5.4.17","stem_class:saṅkhya",           "semantic:kriyā_abhyāvṛtti_gaṇana","suffix:kṛtvasuc"),
    ("5.4.18","stem:dvi",                     "suffix:suc"),
    ("5.4.19","stem:eka",                     "suffix:sakṛt"),
    ("5.4.20","stem:bahu",                    "suffix:dhā",            "aviprakṛṣṭa_kāla:1",    "optional:1"),
    ("5.4.21","semantic:tat_prakṛta_vacana",  "suffix:mayaṭ"),
    ("5.4.22","semantic:samūhavat",           "rule:continuation"),
    ("5.4.23","stem_final:ananta",            "suffix:ñya"),
    ("5.4.24","stem_final:devatānta",         "semantic:tādarthya",    "suffix:yat"),
    ("5.4.25","stem:pāda",                    "rule:continuation"),
    ("5.4.26","stem:atithi",                  "suffix:ñya"),
    ("5.4.27","stem:deva",                    "suffix:tal"),
    ("5.4.28","stem:avi",                     "suffix:ka"),
    ("5.4.29","stem_class:yāvādi",            "suffix:kan"),
    ("5.4.30","stem:lohita",                  "semantic:maṇi"),
    ("5.4.31","semantic:varṇa_anitya",        "rule:continuation"),
    ("5.4.32","semantic:rakta",               "rule:continuation"),
    ("5.4.33","stem:kāla",                    "rule:continuation"),
    ("5.4.34","stem_class:vinayādi",          "suffix:ṭhak"),
    ("5.4.35","stem:vāc",                     "semantic:vyāhṛta_artha"),
    ("5.4.36","stem_class:tadyukta",          "semantic:karman",       "suffix:aṇ"),
    ("5.4.37","stem:oṣadhi",                  "semantic:non_jāti"),
    ("5.4.38","stem_class:prajñādi",          "rule:continuation"),
    ("5.4.39","stem:mṛd",                     "suffix:tikan"),
    ("5.4.40","stem:sa",                      "semantic:praśaṃsā"),
    ("5.4.41","stem:vṛka",                    "suffix:tila",           "is_vedic:1"),
    ("5.4.42","semantic:bahu_alpa_artha",     "stem_class:non_karaka", "suffix:śas",            "optional:1"),
    ("5.4.43","stem_class:saṅkhya_ekavacana", "semantic:vīpsā"),
    ("5.4.44","case:pancami",                 "semantic:pratiyoga",    "suffix:tasi"),
    ("5.4.45","semantic:apādāna",             "stem:ahī"),
    ("5.4.46","case:tritiya",                 "stem_class:ati_graha",  "role:non_kartr"),
    ("5.4.47","semantic:hīyamāna_pāpa_yoga",  "rule:continuation"),
    ("5.4.48","case:ṣaṣṭhi",                  "semantic:vyāśraya"),
    ("5.4.49","stem:roga",                    "semantic:apanayana"),
    ("5.4.50","semantic:abhūta_tad_bhāva",    "stem_yoga:kṛ",          "suffix:cvi"),
    ("5.4.51","stem_final:arur",              "operation:lopa"),
    ("5.4.52","suffix:sāti",                  "semantic:kārtsnya",     "optional:1"),
    ("5.4.53","semantic:abhividhi",           "stem_yoga:sampad"),
    ("5.4.54","semantic:tad_adhīna_vacana",   "rule:continuation"),
    ("5.4.55","semantic:deya",                "suffix:trā"),
    ("5.4.56","stem:deva",                    "case:dvitiya"),
    ("5.4.57","semantic:avyakta_anukaraṇa",   "stem_class:dvyac_avara_ardha","suffix:ḍāc"),
    ("5.4.58","stem:kṛñ",                     "purva_pada:dvitīya",    "semantic:kṛṣi"),
    ("5.4.59","stem_class:saṅkhya_guṇa_anta", "rule:continuation"),
    ("5.4.60","stem:samaya",                  "semantic:yāpanā"),
    ("5.4.61","stem:sapatra",                 "semantic:ati_vyathana"),
    ("5.4.62","stem:niṣkula",                 "semantic:niṣkoṣaṇa"),
    ("5.4.63","stem:sukha",                   "semantic:ānulomya"),
    ("5.4.64","stem:duḥkha",                  "semantic:prātilomya"),
    ("5.4.65","stem:śūla",                    "semantic:pāka"),
    ("5.4.66","stem:satya",                   "semantic:aśapatha"),
    ("5.4.67","stem:madra",                   "semantic:parivāpaṇa"),
    ("5.4.68","section:samāsānta",            "rule:adhikara"),
    ("5.4.69","semantic:pūjana",              "rule:blocking"),
    ("5.4.70","stem:kim",                     "semantic:kṣepa"),
    ("5.4.71","compound_type:naṅ_tatpurusha", "rule:continuation"),
    ("5.4.72","stem:path",                    "optional:1"),
    ("5.4.73","compound_type:bahuvrihi",      "semantic:saṅkhyeya",    "stem_class:ḍac"),
    ("5.4.74","stem:ṛk",                      "stem_final:anakṣa"),
    ("5.4.75","purva_pada:prati",             "stem:sāma",             "suffix:ac"),
    ("5.4.76","stem:akṣṇa",                   "semantic:adarśana"),
    ("5.4.77","stem_class:acatura_etc_list",  "rule:samāsānta_ac"),
    ("5.4.78","stem:brahman",                 "stem_final:varcas"),
    ("5.4.79","stem:ava",                     "stem_final:tamas"),
    ("5.4.80","stem:śvas",                    "stem_final:vasīyas"),
    ("5.4.81","stem:anvavatapta",             "stem_final:rahas"),
    ("5.4.82","purva_pada:prati",             "stem_final:uras",       "case:saptami"),
    ("5.4.83","stem:anugava",                 "semantic:āyāma"),
    ("5.4.84","stem:dvistāvā",                "stem_final:vedi"),
    ("5.4.85","purva_pada:upasarga",          "stem_final:adhvan"),
    ("5.4.86","compound_type:tatpurusha",     "stem_final:aṅguli",     "purva_pada:saṅkhya_avyaya"),
    ("5.4.87","stem:ahar",                    "purva_pada:sarva"),
    ("5.4.88","stem:ahnan",                   "purva_pada_class:ahar"),
    ("5.4.89","stem_class:non_saṅkhyādi",     "semantic:samāhāra",     "rule:blocking"),
    ("5.4.90","stem:uttama",                  "rule:continuation"),
    ("5.4.91","stem:rāja",                    "suffix:ṭac"),
    ("5.4.92","stem:go",                      "operation:ataddhita_luk"),
    ("5.4.93","stem:agra",                    "stem_final:uras"),
    ("5.4.94","stem_final:aśma",              "stem_class:anaḥ",       "domain:jāti"),
    ("5.4.95","stem:grāma",                   "stem_final:takṣan"),
    ("5.4.96","stem:ati",                     "stem_final:śvan"),
    ("5.4.97","semantic:upamāna",             "stem_class:aprāṇi"),
    ("5.4.98","purva_pada:uttara",            "stem_final:sakthi"),
    ("5.4.99","stem:nau",                     "stem_class:dvigu"),
    ("5.4.100","stem:ardha",                  "rule:continuation"),
    ("5.4.101","stem:khārī",                  "dialect:pracya"),
    ("5.4.102","stem:dvi",                    "stem_final:añjali"),
    ("5.4.103","stem_final:anasanta",         "gender:neuter",         "is_vedic:1"),
    ("5.4.104","stem:brahman",                "semantic:jānapada_ākhya"),
    ("5.4.105","stem:ku",                     "optional:1"),
    ("5.4.106","compound_type:dvandva",       "stem_final:ca_uda_ṣaha_anta","semantic:samāhāra"),
    ("5.4.107","compound_type:avyayībhāva",   "stem_class:śarat_prabhṛti"),
    ("5.4.108","stem_final:anaḥ",             "rule:continuation"),
    ("5.4.109","gender:napuṃsaka",            "optional:1"),
    ("5.4.110","stem:nadī",                   "rule:continuation"),
    ("5.4.111","stem_class:jhayanta",         "rule:continuation"),
    ("5.4.112","stem:gireḥ",                  "author:senaka"),
    ("5.4.113","compound_type:bahuvrihi",     "stem_final:sakthi",     "stem_class:svāṅga",     "suffix:ṣac"),
    ("5.4.114","stem:aṅguli",                 "stem_final:dāru"),
    ("5.4.115","stem:dvi",                    "stem_final:mūrdhan",    "suffix:ṣa"),
    ("5.4.116","stem_class:pūraṇī",           "suffix:ap"),
    ("5.4.117","stem:antar",                  "stem_final:loma"),
    ("5.4.118","stem_final:nāsikā",           "domain:samjna",         "stem_class:non_asthūla","substitute:nas"),
    ("5.4.119","purva_pada_class:upasarga",   "rule:continuation"),
    ("5.4.120","stem:suprātar",               "rule:continuation"),
    ("5.4.121","purva_pada_class:naṅ",        "stem_final:hali",       "optional:1"),
    ("5.4.122","stem:prajā",                  "suffix:asic",           "rule:always"),
    ("5.4.123","stem:bahuprajā",              "is_vedic:1"),
    ("5.4.124","stem:dharma",                 "suffix:anic",           "stem_class:kevala"),
    ("5.4.125","stem:jambhā",                 "stem_final:suharita"),
    ("5.4.126","stem:dakṣiṇa",                "suffix:ermā",           "semantic:lubdha_yoga"),
    ("5.4.127","suffix:ic",                   "semantic:karma_vyatihāra"),
    ("5.4.128","stem_class:dvidaṇḍyādi",      "rule:continuation"),
    ("5.4.129","purva_pada:pra",              "stem_final:jānu",       "substitute:jñu"),
    ("5.4.130","stem:ūrdhva",                 "optional:1"),
    ("5.4.131","stem:ūdhas",                  "suffix:anaṅ"),
    ("5.4.132","stem:dhanus",                 "rule:continuation"),
    ("5.4.133","optional:1",                  "domain:samjna"),
    ("5.4.134","stem:jāyā",                   "suffix:niṅ"),
    ("5.4.135","stem:gandha",                 "stem_final:udagra"),
    ("5.4.136","semantic:alpa_ākhyā",         "rule:continuation"),
    ("5.4.137","semantic:upamāna",            "rule:continuation"),
    ("5.4.138","stem:pād",                    "operation:lopa",        "stem_class:non_hasti_ādi"),
    ("5.4.139","stem:kumbhapadī",             "rule:continuation"),
    ("5.4.140","purva_pada_class:saṅkhya_su", "rule:continuation"),
    ("5.4.141","stem:vayas",                  "stem_final:danta",      "substitute:datṛ"),
    ("5.4.142","is_vedic:1",                  "rule:continuation"),
    ("5.4.143","gender:strī",                 "domain:samjna"),
    ("5.4.144","stem:śyāvā",                  "optional:1"),
    ("5.4.145","stem_final:agrānta",          "rule:continuation"),
    ("5.4.146","stem:kakuda",                 "semantic:avasthā",      "operation:lopa"),
    ("5.4.147","stem:trikakud",               "semantic:parvata"),
    ("5.4.148","purva_pada:ud",               "stem_final:kākuda"),
    ("5.4.149","stem:pūrṇa",                  "optional:1"),
    ("5.4.150","stem:suhṛd",                  "semantic:mitra"),
    ("5.4.151","stem_class:uraḥprabhṛti",     "suffix:kap"),
    ("5.4.152","stem_final:in",               "gender:strī"),
    ("5.4.153","stem_final:nadī",             "rule:continuation"),
    ("5.4.154","stem:śeṣa",                   "optional:1"),
    ("5.4.155","domain:samjna",               "rule:blocking"),
    ("5.4.156","stem_final:īyasa",            "rule:continuation"),
    ("5.4.157","stem:bhrātṛ",                 "semantic:vandita"),
    ("5.4.158","stem_final:ṛta",              "is_vedic:1"),
    ("5.4.159","stem:nāḍī",                   "stem_class:svāṅga"),
    ("5.4.160","stem:niṣpravāṇi",             "rule:continuation"),
]


FIXTURES.update(_build_compact_fixtures(_FX_5_4_RAW))


# ---------------------------------------------------------------------------
# Registry metadata
# ---------------------------------------------------------------------------

def _build_meta(prefix: str, raw_table):
    out: dict[str, SutraMeta] = {}
    for row in raw_table:
        sid = row[0]
        op = _SAMJNA
        joined = "|".join(str(s) for s in row[1:] if s)
        if "operation:" in joined or "augment:" in joined or "substitute:" in joined:
            op = _VIDHI
        if "optional:1" in joined:
            op = _VIBHASHA
        if "rule:blocking" in joined:
            op = _PRATISEDHA
        if "rule:adhikara" in joined or "rule:always" in joined or "rule:continuation" in joined:
            if "stem:" not in joined and "stem_class:" not in joined and "suffix:" not in joined:
                op = _PARIBHASHA
        summary = f"Adhyāya {prefix[:-1]}: {sid} taddhita/samāsānta rule"
        out[sid] = SutraMeta(op, summary, (f"taddhita:{prefix[:-1]}",))
    return out


META: dict[str, SutraMeta] = {}
META.update(_build_meta("5.1.", _FX_5_1_RAW))
META.update(_build_meta("5.2.", _FX_5_2_RAW))
META.update(_build_meta("5.3.", _FX_5_3_RAW))
META.update(_build_meta("5.4.", _FX_5_4_RAW))


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
