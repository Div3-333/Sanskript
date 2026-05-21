"""
Discrete Pāṇinian predicates for Adhyāya 6.1 (223 sūtras).

Hand-written per sūtra from the canon (data/ashtadhyayi_sutras.json). No
index-rotated or generated placeholders.
"""
from __future__ import annotations

from .sandhi import join_words
from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api

# ---------------------------------------------------------------------------
# Lexical / gaṇa groups (6.1 reduplication & kit domains)
# ---------------------------------------------------------------------------

JAKSHITYADI = frozenset({"jakṣ", "dit", "jih", "śliṣ", "ṣṭhiv", "ṣphij"})
DASHVADI = frozenset({"dāśva", "sāhma", "mīḍha"})
TUJADI = frozenset({"tuj", "dam", "śru"})
VACISVAPIYAJADI = frozenset({"vac", "svap", "yaj"})
GRAHIJYAVAYIVYADHI = frozenset({
    "grah", "ji", "ava", "vi", "adhi", "viṣṭi", "vicati", "vṛśc", "tipṛch",
    "bhṛj", "ji",
})
SVAPISYAMIVYENJADI = frozenset({"svap", "syam", "ivy", "añj"})


def _sandhi_rule_is(c, expected: str) -> bool:
    return join_words(str(c.get("left", "")), str(c.get("right", ""))).rule == expected


# ===========================================================================
# Adhyāya 6.1 — reduplication, sandhi, accent (6.1.1–6.1.223)
# ===========================================================================

def sutra_6_1_1(c) -> bool:
    """ekāco dve prathamasya: in ekāca reduplication, the first vowel is doubled."""
    return (
        _eq(c, "vidhi_class", "reduplication")
        and _eq(c, "redup_scope", "ekāca")
        and _eq(c, "redup_target", "prathama")
        and int(c.get("redup_count", 0)) == 2
    )


def sutra_6_1_2(c) -> bool:
    """ajāder dvitīyasya: in aj-ādi reduplication, the second (vowel) is used."""
    return (
        _eq(c, "vidhi_class", "reduplication")
        and _eq(c, "redup_scope", "ajādi")
        and _eq(c, "redup_target", "dvitīya")
    )


def sutra_6_1_3(c) -> bool:
    """na ndrāḥ saṃyogādayaḥ: ndr- stems do not take saṃyogādi reduplication."""
    return _eq(c, "stem_class", "ndr") and _eq(c, "redup_class_blocked", "samyogādi")


def sutra_6_1_4(c) -> bool:
    """pūrve'bhyāsaḥ: the prior reduplicative syllable is named abhyāsa."""
    return _eq(c, "assigns_samjna", "abhyāsa") and _eq(c, "position", "pūrva")


def sutra_6_1_5(c) -> bool:
    """ubhe abhyastam: both [pūrva and parā] together are named abhyasta."""
    return _eq(c, "assigns_samjna", "abhyasta") and _eq(c, "scope", "ubhe")


def sutra_6_1_6(c) -> bool:
    """jakṣityādayaḥ ṣaṭ: six roots jakṣ-etc. have this reduplication pattern."""
    return _eq(c, "vidhi_class", "reduplication") and _in(c, "dhatu_lemma", JAKSHITYADI)


def sutra_6_1_7(c) -> bool:
    """tujādīnāṃ dīrgho'bhyāsya: abhyāsa is lengthened for tuj-ādi roots."""
    return (
        _eq(c, "operation", "dīrgha")
        and _eq(c, "target", "abhyāsa")
        and _in(c, "dhatu_lemma", TUJADI)
    )


def sutra_6_1_8(c) -> bool:
    """liti dhātor anabhyāsya: liṭ applies to the root, not to the abhyāsa."""
    return (
        _eq(c, "lakara", "liṭ")
        and _eq(c, "applies_to", "dhatu")
        and not bool(c.get("applies_to_abhyāsa"))
    )


def sutra_6_1_9(c) -> bool:
    """sanyāṅoḥ: san and ṅī prefixes take this reduplication treatment."""
    return _eq(c, "vidhi_class", "reduplication") and _in(c, "prefix", {"san", "ṅī"})


def sutra_6_1_10(c) -> bool:
    """ślau: ślu-class reduplication."""
    return _eq(c, "vidhi_class", "reduplication") and _eq(c, "marker", "ślu")


def sutra_6_1_11(c) -> bool:
    """caṅi: caṅ-class reduplication."""
    return _eq(c, "vidhi_class", "reduplication") and _eq(c, "marker", "caṅ")


def sutra_6_1_12(c) -> bool:
    """dāśvān sāhvān mīḍhvāṃś ca: dāśva/sāhma/mīḍha roots in this list."""
    return _eq(c, "vidhi_class", "reduplication") and _in(c, "dhatu_lemma", DASHVADI)


def sutra_6_1_13(c) -> bool:
    """ṣyaṅaḥ samprasāraṇaṃ putrapatyos tatpuruṣe: ṣyaṅ gets samprasāraṇa in
    putra/patya tatpuruṣa."""
    return (
        _eq(c, "suffix", "ṣyaṅ")
        and _eq(c, "operation", "samprasāraṇa")
        and _eq(c, "compound_type", "tatpuruṣa")
        and _in(c, "semantic", {"putra", "patya"})
    )


def sutra_6_1_14(c) -> bool:
    """bandhuni bahuvrīhau: samprasāraṇa in bandhu bahuvrīhi."""
    return (
        _eq(c, "operation", "samprasāraṇa")
        and _eq(c, "compound_type", "bahuvrīhi")
        and _eq(c, "semantic", "bandhu")
    )


def sutra_6_1_15(c) -> bool:
    """vacisvapiyajādīnāṃ kiti: vac/svapi/yaj-ādi get kit in reduplication."""
    return _eq(c, "assigns_samjna", "kit") and _in(c, "dhatu_lemma", VACISVAPIYAJADI)


def sutra_6_1_16(c) -> bool:
    """grahijyādiṣu ṅiti ca: listed roots plus ṅit get kit."""
    return _eq(c, "assigns_samjna", "kit") and (
        _in(c, "dhatu_lemma", GRAHIJYAVAYIVYADHI) or bool(c.get("is_ṅit"))
    )


def sutra_6_1_17(c) -> bool:
    """lity abhyāsasyobhayeṣām: liṭ applies to both root and abhyāsa."""
    return (
        _eq(c, "lakara", "liṭ")
        and bool(c.get("applies_to_abhyāsa"))
        and bool(c.get("applies_to_dhatu"))
    )


def sutra_6_1_18(c) -> bool:
    """svāpeś caṅi: svāp + caṅ reduplication."""
    return _eq(c, "dhatu_lemma", "svāp") and _eq(c, "marker", "caṅ")


def sutra_6_1_19(c) -> bool:
    """svapisyamivyāñjāṃ yaṅi: svapi/syami/vyāñj-ādi take yaṅ reduplication."""
    return _eq(c, "marker", "yaṅ") and _in(c, "dhatu_lemma", SVAPISYAMIVYENJADI)


def sutra_6_1_20(c) -> bool:
    """na vaśaḥ: vaśa is excluded from this rule."""
    return _eq(c, "dhatu_lemma", "vaś") and _eq(c, "rule_blocked", True)


def sutra_6_1_21(c) -> bool:
    """cāyaḥ kī: cāya takes kī (desiderative) reduplication."""
    return _eq(c, "dhatu_lemma", "cāya") and _eq(c, "redup_suffix", "kī")


def sutra_6_1_22(c) -> bool:
    """sphāyaḥ sphī niṣṭhāyām: sphāya/sphī in niṣṭhā."""
    return (
        _in(c, "dhatu_lemma", {"sphāya", "sphī"})
        and _eq(c, "lakara", "niṣṭhā")
    )


def sutra_6_1_23(c) -> bool:
    """styaḥ prapūrvāsya: styā after pra-upasarga."""
    return _eq(c, "dhatu_lemma", "styā") and _eq(c, "upasarga", "pra")


def sutra_6_1_24(c) -> bool:
    """dravamūrtisparśayoḥ śyaḥ: śya after fluid/form/touch sense."""
    return _eq(c, "suffix", "śya") and _in(c, "semantic", {"drava", "mūrti", "sparśa"})


def sutra_6_1_25(c) -> bool:
    """prateś ca: prati also (takes śya in the same domain as 6.1.24)."""
    return _eq(c, "suffix", "śya") and _eq(c, "upasarga", "prati")

def sutra_6_1_26(c) -> bool:
    """विभाषाऽभ्यवपूर्वस्य."""
    return _eq(c, "optional", True) and _eq(c, "upasarga_scope", "abhyavaparva")

def sutra_6_1_27(c) -> bool:
    """शृतं पाके."""
    return _eq(c, "form", "śṛta") and _eq(c, "semantic", "pāka")

def sutra_6_1_28(c) -> bool:
    """प्यायः पी."""
    return _eq(c, "dhatu_lemma", "pyāya") and _eq(c, "redup_suffix", "pī")

def sutra_6_1_29(c) -> bool:
    """लिड्यङोश्च."""
    return _in(c, "marker", {"liḍ", "yaṅ"})

def sutra_6_1_30(c) -> bool:
    """विभाषा श्वेः."""
    return _eq(c, "optional", True) and _eq(c, "stem", "śva")

def sutra_6_1_31(c) -> bool:
    """णौ च संश्चङोः."""
    return _eq(c, "lakara", "ṇau") and _in(c, "marker", {"san", "caṅ"})

def sutra_6_1_32(c) -> bool:
    """ह्वः सम्प्रसारणम्."""
    return _eq(c, "stem", "hv") and _eq(c, "operation", "samprasāraṇa")

def sutra_6_1_33(c) -> bool:
    """अभ्यस्तस्य च."""
    return _eq(c, "assigns_samjna", "abhyasta") and bool(c.get("also"))

def sutra_6_1_34(c) -> bool:
    """बहुलं छन्दसि."""
    return _eq(c, "rule_strength", "bahula") and _eq(c, "domain", "chandas")

def sutra_6_1_35(c) -> bool:
    """चायः की."""
    return _eq(c, "dhatu_lemma", "cāya") and _eq(c, "redup_suffix", "kī")

def sutra_6_1_36(c) -> bool:
    """अपस्पृधेथामानृचुरानृहुश्चिच्युषेतित्याजश्राताःश्रितमाशीराशीर्त्तः."""
    return _in(c, "dhatu_lemma", {"apaspṛdhe", "ānṛc", "ānṛh", "cicyuṣ", "tityaj", "śrāta", "śrita", "āśīr"})

def sutra_6_1_37(c) -> bool:
    """न सम्प्रसारणे सम्प्रसारणम्."""
    return _eq(c, "site", "samprasāraṇa") and _eq(c, "operation_blocked", "samprasāraṇa")

def sutra_6_1_38(c) -> bool:
    """लिटि वयो यः."""
    return _eq(c, "lakara", "liṭ") and _eq(c, "stem", "vay") and _eq(c, "substitute", "ya")

def sutra_6_1_39(c) -> bool:
    """वश्चास्यान्यतरस्याम् किति."""
    return _eq(c, "stem", "vaś") and _eq(c, "option", "anyatarā") and _eq(c, "assigns_samjna", "kit")

def sutra_6_1_40(c) -> bool:
    """वेञः."""
    return _eq(c, "marker", "veñ")

def sutra_6_1_41(c) -> bool:
    """ल्यपि च."""
    return _eq(c, "suffix", "lyap") and bool(c.get("also"))

def sutra_6_1_42(c) -> bool:
    """ज्यश्च."""
    return _eq(c, "stem", "jy") and bool(c.get("also"))

def sutra_6_1_43(c) -> bool:
    """व्यश्च."""
    return _eq(c, "stem", "vy") and bool(c.get("also"))

def sutra_6_1_44(c) -> bool:
    """विभाषा परेः."""
    return _eq(c, "optional", True) and _eq(c, "position", "para")

def sutra_6_1_45(c) -> bool:
    """आदेच उपदेशेऽशिति."""
    return _eq(c, "site", "upadeśa") and _eq(c, "class", "ec") and _eq(c, "condition", "aśiti")

def sutra_6_1_46(c) -> bool:
    """न व्यो लिटि."""
    return _eq(c, "stem_class", "vy") and _eq(c, "lakara", "liṭ") and _eq(c, "rule_blocked", True)

def sutra_6_1_47(c) -> bool:
    """स्फुरतिस्फुलत्योर्घञि."""
    return _in(c, "dhatu_lemma", {"sphurat", "sphulat"}) and _eq(c, "suffix", "ghañ")

def sutra_6_1_48(c) -> bool:
    """क्रीङ्जीनां णौ."""
    return _in(c, "dhatu_lemma", {"krī", "jī"}) and _eq(c, "lakara", "ṇau")

def sutra_6_1_49(c) -> bool:
    """सिध्यतेरपारलौकिके."""
    return _eq(c, "dhatu_lemma", "sidh") and _eq(c, "semantic", "apāralaukika")

def sutra_6_1_50(c) -> bool:
    """मीनातिमिनोतिदीङां ल्यपि च."""
    return _in(c, "dhatu_lemma", {"mīna", "atimina", "noti", "dī"}) and _eq(c, "suffix", "lyap") and bool(c.get("also"))

def sutra_6_1_51(c) -> bool:
    """विभाषा लीयतेः."""
    return _eq(c, "optional", True) and _eq(c, "dhatu_lemma", "lī")

def sutra_6_1_52(c) -> bool:
    """खिदेश्छन्दसि."""
    return _eq(c, "marker", "khid") and _eq(c, "domain", "chandas")

def sutra_6_1_53(c) -> bool:
    """अपगुरो णमुलि."""
    return _eq(c, "dhatu_lemma", "apagur") and _eq(c, "suffix", "ṇamul")

def sutra_6_1_54(c) -> bool:
    """चिस्फुरोर्णौ."""
    return _in(c, "dhatu_lemma", {"ci", "sphur"}) and _eq(c, "lakara", "ṇau")

def sutra_6_1_55(c) -> bool:
    """प्रजने वीयतेः."""
    return _eq(c, "semantic", "prajana") and _eq(c, "dhatu_lemma", "vī")

def sutra_6_1_56(c) -> bool:
    """बिभेतेर्हेतुभये."""
    return _eq(c, "dhatu_lemma", "bibhet") and _eq(c, "semantic", "hetubhaya")

def sutra_6_1_57(c) -> bool:
    """नित्यं स्मयतेः."""
    return _eq(c, "rule_strength", "nitya") and _eq(c, "dhatu_lemma", "smay")

def sutra_6_1_58(c) -> bool:
    """सृजिदृशोर्झल्यमकिति."""
    return _in(c, "dhatu_lemma", {"sṛj", "dṛś"}) and _eq(c, "suffix", "jhali") and _eq(c, "assigns_samjna", "kit") and not bool(c.get("is_kit"))

def sutra_6_1_59(c) -> bool:
    """अनुदात्तस्य चर्दुपधस्यान्यतरस्याम्."""
    return _eq(c, "accent", "anudātta") and _eq(c, "upadha", "ṛdu") and _eq(c, "option", "anyatarā")

def sutra_6_1_60(c) -> bool:
    """शीर्षंश्छन्दसि."""
    return _eq(c, "stem", "śīrṣan") and _eq(c, "domain", "chandas")

def sutra_6_1_61(c) -> bool:
    """ये च तद्धिते."""
    return _eq(c, "suffix", "ya") and _eq(c, "suffix_class", "taddhita") and bool(c.get("also"))

def sutra_6_1_62(c) -> bool:
    """अचि शीर्षः."""
    return _eq(c, "class", "ac") and _eq(c, "stem", "śīrṣan")

def sutra_6_1_63(c) -> bool:
    """पद्दन्नोमास्हृन्निशसन्यूषन्दोषन्यकञ्छकन्नुदन्नासञ्छस्प्रभृतिषु."""
    return _in(c, "stem", {"paddat", "nas", "mās", "hṛt", "niś", "asan", "yūṣan", "doṣan", "yakan", "śakan", "udan", "āsan"}) and _eq(c, "suffix", "śas")

def sutra_6_1_64(c) -> bool:
    """धात्वादेः षः सः."""
    return _eq(c, "site", "dhātuvādi") and _eq(c, "substitute", "ṣ") and _eq(c, "replacement", "s")

def sutra_6_1_65(c) -> bool:
    """णो नः."""
    return _eq(c, "substitute", "ṇ") and _eq(c, "replacement", "n")

def sutra_6_1_66(c) -> bool:
    """लोपो व्योर्वलि."""
    return _eq(c, "operation", "lopa") and _eq(c, "stem_class", "vy") and _eq(c, "suffix", "val")

def sutra_6_1_67(c) -> bool:
    """वेरपृक्तस्य."""
    return _eq(c, "stem", "ve") and _eq(c, "condition", "apṛkta")

def sutra_6_1_68(c) -> bool:
    """हल्ङ्याब्भ्यो दीर्घात्‌ सुतिस्यपृक्तं हल्."""
    return _eq(c, "source", "dīrgha") and _eq(c, "target", "hal") and _eq(c, "condition", "apṛkta")

def sutra_6_1_69(c) -> bool:
    """एङ्ह्रस्वात्‌ सम्बुद्धेः."""
    return _eq(c, "source", "eṅhrasva") and _eq(c, "domain", "sambuddhi")

def sutra_6_1_70(c) -> bool:
    """शेश्छन्दसि बहुलम्."""
    return _eq(c, "stem", "śe") and _eq(c, "domain", "chandas") and _eq(c, "rule_strength", "bahula")

def sutra_6_1_71(c) -> bool:
    """ह्रस्वस्य पिति कृति तुक्."""
    return _eq(c, "vowel_weight", "hrasva") and _eq(c, "condition", "piti") and _eq(c, "suffix_class", "kṛt") and _eq(c, "augment", "tuk")

def sutra_6_1_72(c) -> bool:
    """संहितायाम्."""
    return _eq(c, "domain", "saṃhitā")

def sutra_6_1_73(c) -> bool:
    """छे च."""
    return _eq(c, "domain", "chha") and bool(c.get("also"))

def sutra_6_1_74(c) -> bool:
    """आङ्माङोश्च."""
    return _in(c, "prefix", {"āṅ", "māṅ"}) and bool(c.get("also"))

def sutra_6_1_75(c) -> bool:
    """दीर्घात्‌."""
    return _eq(c, "operation", "dīrgha")

def sutra_6_1_76(c) -> bool:
    """पदान्ताद्वा."""
    return _eq(c, "site", "padānta") and _eq(c, "optional", True)

def sutra_6_1_77(c) -> bool:
    """इको यणचि."""
    return _eq(c, "class", "ik") and _eq(c, "substitute", "yaṇ") and _eq(c, "environment", "ac")

def sutra_6_1_78(c) -> bool:
    """एचोऽयवायावः."""
    return _sandhi_rule_is(c, "ayavāyāva")

def sutra_6_1_79(c) -> bool:
    """वान्तो यि प्रत्यये."""
    return _eq(c, "final", "vānta") and _eq(c, "suffix", "yi") and _eq(c, "site", "pratyaya")

def sutra_6_1_80(c) -> bool:
    """धातोस्तन्निमित्तस्यैव."""
    return _eq(c, "applies_to", "dhatu") and _eq(c, "cause", "tannimitta")

def sutra_6_1_81(c) -> bool:
    """क्षय्यजय्यौ शक्यार्थे."""
    return _in(c, "form", {"kṣayya", "jayya"}) and _eq(c, "semantic", "śakya_artha")

def sutra_6_1_82(c) -> bool:
    """क्रय्यस्तदर्थे."""
    return _eq(c, "form", "krayya") and _eq(c, "semantic", "tad_artha")

def sutra_6_1_83(c) -> bool:
    """भय्यप्रवय्ये च च्छन्दसि."""
    return _in(c, "form", {"bhayya", "pravayya"}) and _eq(c, "domain", "chandas") and bool(c.get("also"))

def sutra_6_1_84(c) -> bool:
    """एकः पूर्वपरयोः."""
    return _eq(c, "substitute", "eka") and _eq(c, "scope", "pūrvapara")

def sutra_6_1_85(c) -> bool:
    """अन्तादिवच्च."""
    return _eq(c, "rule", "antādivat") and bool(c.get("also"))

def sutra_6_1_86(c) -> bool:
    """षत्वतुकोरसिद्धः."""
    return _eq(c, "site", "ṣṭut") and _eq(c, "validity", "asiddha")

def sutra_6_1_87(c) -> bool:
    """आद्गुणः."""
    return _sandhi_rule_is(c, "guṇa")

def sutra_6_1_88(c) -> bool:
    """वृद्धिरेचि."""
    return _sandhi_rule_is(c, "vṛddhi")

def sutra_6_1_89(c) -> bool:
    """एत्येधत्यूठ्सु."""
    return _in(c, "suffix", {"et", "edh", "ot"}) and _eq(c, "augment", "ṭ")

def sutra_6_1_90(c) -> bool:
    """आटश्च."""
    return _eq(c, "site", "āṭ") and bool(c.get("also"))

def sutra_6_1_91(c) -> bool:
    """उपसर्गादृति धातौ."""
    return _eq(c, "after", "upasarga") and _eq(c, "class", "ṛ") and _eq(c, "locus", "dhatu")

def sutra_6_1_92(c) -> bool:
    """वा सुप्यापिशलेः."""
    return _eq(c, "optional", True) and _eq(c, "class", "sup") and _eq(c, "stem_class", "āpiśali")

def sutra_6_1_93(c) -> bool:
    """औतोऽम्शसोः."""
    return _eq(c, "substitute", "ā") and _eq(c, "source", "ot") and _in(c, "suffix", {"aṃ", "śas"})

def sutra_6_1_94(c) -> bool:
    """एङि पररूपम्."""
    return _eq(c, "class", "eṅ") and _eq(c, "substitute", "pararūpa")

def sutra_6_1_95(c) -> bool:
    """ओमाङोश्च."""
    return _in(c, "prefix", {"o", "māṅ"}) and bool(c.get("also"))

def sutra_6_1_96(c) -> bool:
    """उस्यपदान्तात्‌."""
    return _eq(c, "class", "us") and _eq(c, "site", "apadānta")

def sutra_6_1_97(c) -> bool:
    """अतो गुणे."""
    return _eq(c, "source", "a") and _eq(c, "sandhi_rule", "guṇa")

def sutra_6_1_98(c) -> bool:
    """अव्यक्तानुकरणस्यात इतौ."""
    return _eq(c, "semantic", "avyaktānukaraṇa") and _eq(c, "source", "a") and _eq(c, "suffix", "it")

def sutra_6_1_99(c) -> bool:
    """नाम्रेडितस्यान्त्यस्य तु वा."""
    return _eq(c, "stem_class", "āmreḍita") and _eq(c, "position", "antya") and _eq(c, "optional", True)

def sutra_6_1_100(c) -> bool:
    """नित्यमाम्रेडिते डाचि."""
    return _eq(c, "stem_class", "āmreḍita") and _eq(c, "class", "ḍāc") and _eq(c, "rule_strength", "nitya")

def sutra_6_1_101(c) -> bool:
    """अकः सवर्णे दीर्घः."""
    return _sandhi_rule_is(c, "savarṇa-dīrgha")

def sutra_6_1_102(c) -> bool:
    """प्रथमयोः पूर्वसवर्णः."""
    return _eq(c, "scope", "prathama") and _eq(c, "substitute", "pūrvasavarna")

def sutra_6_1_103(c) -> bool:
    """तस्माच्छसो नः पुंसि."""
    return _eq(c, "source", "śas") and _eq(c, "substitute", "na") and _eq(c, "gender", "puṃ")

def sutra_6_1_104(c) -> bool:
    """नादिचि."""
    return _eq(c, "source", "ā") and _eq(c, "class", "ic") and _eq(c, "rule_blocked", True)

def sutra_6_1_105(c) -> bool:
    """दीर्घाज्जसि च."""
    return _eq(c, "operation", "dīrgha") and _eq(c, "class", "jas") and bool(c.get("also"))

def sutra_6_1_106(c) -> bool:
    """वा छन्दसि."""
    return _eq(c, "optional", True) and _eq(c, "domain", "chandas")

def sutra_6_1_107(c) -> bool:
    """अमि पूर्वः."""
    return _eq(c, "class", "am") and _eq(c, "position", "pūrva")

def sutra_6_1_108(c) -> bool:
    """सम्प्रसारणाच्च."""
    return _eq(c, "source", "samprasāraṇa") and bool(c.get("also"))

def sutra_6_1_109(c) -> bool:
    """एङः पदान्तादति."""
    return _eq(c, "source", "eṅ") and _eq(c, "site", "padānta") and _eq(c, "suffix", "ati")

def sutra_6_1_110(c) -> bool:
    """ङसिङसोश्च."""
    return _in(c, "suffix", {"ṅas", "iṅas"}) and bool(c.get("also"))

def sutra_6_1_111(c) -> bool:
    """ऋत उत्‌."""
    return _eq(c, "source", "ṛt") and _eq(c, "substitute", "ut")

def sutra_6_1_112(c) -> bool:
    """ख्यत्यात्‌ परस्य."""
    return _eq(c, "source", "khyati") and _eq(c, "position", "para")

def sutra_6_1_113(c) -> bool:
    """अतो रोरप्लुतादप्लुते."""
    return _eq(c, "source", "a") and _eq(c, "stem", "ro") and _eq(c, "condition", "apluta")

def sutra_6_1_114(c) -> bool:
    """हशि च."""
    return _eq(c, "class", "haś") and bool(c.get("also"))

def sutra_6_1_115(c) -> bool:
    """प्रकृत्याऽन्तःपादमव्यपरे."""
    return _eq(c, "instrument", "prakṛti") and _eq(c, "domain", "antapāda") and _eq(c, "condition", "avyapara")

def sutra_6_1_116(c) -> bool:
    """अव्यादवद्यादवक्रमुरव्रतायमवन्त्ववस्युषु च."""
    return _in(c, "form", {"avyāda", "avadyāda", "avakrama", "uravra", "tāyamavant", "tavasyu"}) and bool(c.get("also"))

def sutra_6_1_117(c) -> bool:
    """यजुष्युरः."""
    return _eq(c, "domain", "yajuṣ") and _eq(c, "substitute", "uraḥ")

def sutra_6_1_118(c) -> bool:
    """आपोजुषाणोवृष्णोवर्षिष्ठेऽम्बेऽम्बालेऽम्बिकेपूर्वे."""
    return _in(c, "form", {"āpas", "juṣāṇa", "vṛṣṇa", "varṣiṣṭha", "ambe", "ambāle", "ambike"}) and _eq(c, "position", "pūrva")

def sutra_6_1_119(c) -> bool:
    """अङ्ग इत्यादौ च."""
    return _eq(c, "stem", "aṅga") and _eq(c, "domain", "ityādi") and bool(c.get("also"))

def sutra_6_1_120(c) -> bool:
    """अनुदात्ते च कुधपरे."""
    return _eq(c, "accent", "anudātta") and _eq(c, "domain", "kudhpara") and bool(c.get("also"))

def sutra_6_1_121(c) -> bool:
    """अवपथासि च."""
    return _eq(c, "domain", "avapathā") and bool(c.get("also"))

def sutra_6_1_122(c) -> bool:
    """सर्वत्र विभाषा गोः."""
    return _eq(c, "optional", True) and _eq(c, "stem", "go")

def sutra_6_1_123(c) -> bool:
    """अवङ् स्फोटायनस्य."""
    return _eq(c, "substitute", "avaṅ") and _eq(c, "authority", "sphoṭāyana")

def sutra_6_1_124(c) -> bool:
    """इन्द्रे च (नित्यम्)."""
    return _eq(c, "stem", "indra") and bool(c.get("also")) and _eq(c, "rule_strength", "nitya")

def sutra_6_1_125(c) -> bool:
    """प्लुतप्रगृह्या अचि नित्यम्."""
    return _eq(c, "stem_class", "plutapragṛhya") and _eq(c, "class", "ac") and _eq(c, "rule_strength", "nitya")

def sutra_6_1_126(c) -> bool:
    """आङोऽनुनासिकश्छन्दसि."""
    return _eq(c, "prefix", "āṅ") and _eq(c, "substitute", "anunāsika") and _eq(c, "domain", "chandas")

def sutra_6_1_127(c) -> bool:
    """इकोऽसवर्णे शाकल्यस्य ह्रस्वश्च."""
    return _eq(c, "class", "ik") and _eq(c, "condition", "asavarṇa") and _eq(c, "authority", "śākalya") and _eq(c, "vowel_weight", "hrasva") and bool(c.get("also"))

def sutra_6_1_128(c) -> bool:
    """ऋत्यकः."""
    return _eq(c, "class", "ṛ") and _eq(c, "substitute", "ak")

def sutra_6_1_129(c) -> bool:
    """अप्लुतवदुपस्थिते."""
    return _eq(c, "condition", "aplutavat") and _eq(c, "state", "upasthita")

def sutra_6_1_130(c) -> bool:
    """ई३ चाक्रवर्मणस्य."""
    return _eq(c, "substitute", "ī3") and _eq(c, "authority", "cākravarmaṇa")

def sutra_6_1_131(c) -> bool:
    """दिव उत्‌."""
    return _eq(c, "stem", "div") and _eq(c, "substitute", "ut")

def sutra_6_1_132(c) -> bool:
    """एतत्तदोः सुलोपोऽकोरनञ्समासे हलि."""
    return _in(c, "stem", {"etad", "tad"}) and _eq(c, "operation", "su-lopa") and _eq(c, "compound_type", "an-añ") and _eq(c, "class", "hal")

def sutra_6_1_133(c) -> bool:
    """स्यश्छन्दसि बहुलम्."""
    return _eq(c, "stem", "sya") and _eq(c, "domain", "chandas") and _eq(c, "rule_strength", "bahula")

def sutra_6_1_134(c) -> bool:
    """सोऽचि लोपे चेत्‌ पादपूरणम्."""
    return _eq(c, "substitute", "sa") and _eq(c, "class", "ac") and _eq(c, "operation", "lopa") and _eq(c, "domain", "pādapūraṇa")

def sutra_6_1_135(c) -> bool:
    """सुट् कात्‌ पूर्वः."""
    return _eq(c, "augment", "suṭ") and _eq(c, "source", "ka") and _eq(c, "position", "pūrva")

def sutra_6_1_136(c) -> bool:
    """अडभ्यासव्यवायेऽपि."""
    return _eq(c, "site", "aḍ") and _in(c, "domain", {"abhyāsa", "vyavāya"}) and bool(c.get("also"))

def sutra_6_1_137(c) -> bool:
    """सम्पर्युपेभ्यः करोतौ भूषणे."""
    return _in(c, "prefix", {"sam", "pari", "upa"}) and _in(c, "dhatu_lemma", {"kṛ", "taw"}) and _eq(c, "semantic", "bhūṣaṇa")

def sutra_6_1_138(c) -> bool:
    """समवाये च."""
    return _eq(c, "semantic", "samavāya") and bool(c.get("also"))

def sutra_6_1_139(c) -> bool:
    """उपात्‌ प्रतियत्नवैकृतवाक्याध्याहारेषु."""
    return _eq(c, "source", "upa") and _in(c, "semantic", {"pratiyoga", "yatna", "vaikṛta", "vākya", "adhyāhāra"})

def sutra_6_1_140(c) -> bool:
    """किरतौ लवने."""
    return _eq(c, "dhatu_lemma", "kir") and _eq(c, "semantic", "lavana")

def sutra_6_1_141(c) -> bool:
    """हिंसायां प्रतेश्च."""
    return _eq(c, "semantic", "hiṃsā") and _eq(c, "upasarga", "prati") and bool(c.get("also"))

def sutra_6_1_142(c) -> bool:
    """अपाच्चतुष्पाच्छकुनिष्वालेखने."""
    return _eq(c, "source", "apa") and _in(c, "domain", {"catuṣpāt", "śakuni"}) and _eq(c, "semantic", "ālekhana")

def sutra_6_1_143(c) -> bool:
    """कुस्तुम्बुरूणि जातिः."""
    return _in(c, "stem", {"kustumburu", "ūṇi"}) and _eq(c, "assigns_samjna", "jāti")

def sutra_6_1_144(c) -> bool:
    """अपरस्पराः क्रियासातत्ये."""
    return _eq(c, "form", "aparasparā") and _eq(c, "semantic", "kriyāsātathya")

def sutra_6_1_145(c) -> bool:
    """गोष्पदं सेवितासेवितप्रमाणेषु."""
    return _eq(c, "form", "goṣpada") and _in(c, "semantic", {"sevita", "asevita", "pramāṇa"})

def sutra_6_1_146(c) -> bool:
    """आस्पदं प्रतिष्ठायाम्‌."""
    return _eq(c, "form", "āspada") and _eq(c, "semantic", "pratiṣṭhā")

def sutra_6_1_147(c) -> bool:
    """आश्चर्यमनित्ये."""
    return _eq(c, "form", "āścarya") and _eq(c, "condition", "anitya")

def sutra_6_1_148(c) -> bool:
    """वर्चस्केऽवस्करः."""
    return _eq(c, "semantic", "varcask") and _eq(c, "form", "avaskara")

def sutra_6_1_149(c) -> bool:
    """अपस्करो रथाङ्गम्."""
    return _eq(c, "form", "apaskara") and _eq(c, "semantic", "rathāṅga")

def sutra_6_1_150(c) -> bool:
    """विष्किरः शकुनिर्विकरो वा."""
    return _eq(c, "form", "viṣkira") and _in(c, "semantic", {"śakuni", "vikara"}) and _eq(c, "optional", True)

def sutra_6_1_151(c) -> bool:
    """ह्रस्वाच्चन्द्रोत्तरपदे मन्त्रे."""
    return _eq(c, "source", "hrasva") and _eq(c, "domain", "candrottarapada") and bool(c.get("in_mantra"))

def sutra_6_1_152(c) -> bool:
    """प्रतिष्कशश्च कशेः."""
    return _eq(c, "form", "pratiṣkaśa") and _eq(c, "stem", "kaśa") and bool(c.get("also"))

def sutra_6_1_153(c) -> bool:
    """प्रस्कण्वहरिश्चन्द्रावृषी."""
    return _in(c, "form", {"praskaṇva", "ahariścandra"}) and _eq(c, "assigns_samjna", "ṛṣi")

def sutra_6_1_154(c) -> bool:
    """मस्करमस्करिणौ वेणुपरिव्राजकयोः."""
    return _in(c, "form", {"maskara", "maskariṇa"}) and _in(c, "domain", {"veṇu", "parivrājaka"})

def sutra_6_1_155(c) -> bool:
    """कास्तीराजस्तुन्दे नगरे."""
    return _eq(c, "form", "kāstīrājastunde") and _eq(c, "domain", "nagara")

def sutra_6_1_156(c) -> bool:
    """कारस्करो वृक्षः."""
    return _eq(c, "form", "kāraskara") and _eq(c, "semantic", "vṛkṣa")

def sutra_6_1_157(c) -> bool:
    """पारस्करप्रभृतीनि च संज्ञायाम्."""
    return _eq(c, "stem_class", "pāraskaraprabhṛti") and _eq(c, "domain", "saṃjñā") and bool(c.get("also"))

def sutra_6_1_158(c) -> bool:
    """अनुदात्तं पदमेकवर्जम्‌."""
    return _eq(c, "accent", "anudātta") and _eq(c, "assigns_samjna", "pada") and _eq(c, "condition", "ekavarjya")

def sutra_6_1_159(c) -> bool:
    """कर्षात्वतो घञोऽन्त उदात्तः."""
    return _eq(c, "source", "karṣātva") and _eq(c, "suffix", "ghañ") and _eq(c, "position", "anta") and _eq(c, "accent", "udātta")

def sutra_6_1_160(c) -> bool:
    """उञ्छादीनां च."""
    return _eq(c, "stem_class", "uñchādi") and bool(c.get("also"))

def sutra_6_1_161(c) -> bool:
    """अनुदात्तस्य च यत्रोदात्तलोपः."""
    return _eq(c, "accent", "anudātta") and _eq(c, "operation", "udāttalopa")

def sutra_6_1_162(c) -> bool:
    """धातोः."""
    return _eq(c, "applies_to", "dhatu")

def sutra_6_1_163(c) -> bool:
    """चितः."""
    return _eq(c, "applies_to", "cit")

def sutra_6_1_164(c) -> bool:
    """तद्धितस्य."""
    return _eq(c, "anga", "taddhita")

def sutra_6_1_165(c) -> bool:
    """कितः."""
    return _eq(c, "marker", "kit")

def sutra_6_1_166(c) -> bool:
    """तिसृभ्यो जसः."""
    return _eq(c, "source", "tisṛ") and _eq(c, "suffix", "jas")

def sutra_6_1_167(c) -> bool:
    """चतुरः शसि."""
    return _eq(c, "stem", "catur") and _eq(c, "suffix", "śas")

def sutra_6_1_168(c) -> bool:
    """सावेकाचस्तृतीयाऽऽदिविभक्तिः."""
    return _eq(c, "source", "sau") and _eq(c, "class", "ekāca") and _eq(c, "assigns_samjna", "vibhakti")

def sutra_6_1_169(c) -> bool:
    """अन्तोदत्तादुत्तरपदादन्यतरस्यामनित्यसमासे."""
    return _eq(c, "source", "antodātta") and _eq(c, "from", "uttarapada") and _eq(c, "compound", "anitya") and _eq(c, "option", "anyatarā")

def sutra_6_1_170(c) -> bool:
    """अञ्चेश्छन्दस्यसर्वनामस्थानम्."""
    return _eq(c, "source", "añci") and _eq(c, "domain", "chandas") and not _eq(c, "assigns_samjna", "sarvānāmasthāna")

def sutra_6_1_171(c) -> bool:
    """ऊडिदम्पदाद्यप्पुम्रैद्युभ्यः."""
    return _eq(c, "source", "ūḍidampadādyap") and _in(c, "suffix", {"mṛ", "aid", "yubhyaḥ"})

def sutra_6_1_172(c) -> bool:
    """अष्टनो दीर्घात्‌."""
    return _eq(c, "source", "aṣṭan") and _eq(c, "operation", "dīrgha")

def sutra_6_1_173(c) -> bool:
    """शतुरनुमो नद्यजादी."""
    return _eq(c, "source", "śatu") and _eq(c, "also", "anum") and _eq(c, "stem_class", "nadyajādi")

def sutra_6_1_174(c) -> bool:
    """उदात्तयणो हल्पूर्वात्‌."""
    return _eq(c, "source", "udāttayaṇ") and _eq(c, "from", "halpūrva")

def sutra_6_1_175(c) -> bool:
    """नोङ्धात्वोः."""
    return _eq(c, "substitute", "na") and _in(c, "marker", {"ūṅ", "dhātv"})

def sutra_6_1_176(c) -> bool:
    """ह्रस्वनुड्भ्यां मतुप्‌."""
    return _eq(c, "source", "hrasvanuṭ") and _eq(c, "suffix", "matup")

def sutra_6_1_177(c) -> bool:
    """नामन्यतरस्याम्‌."""
    return _eq(c, "assigns_samjna", "nāman") and _eq(c, "option", "anyatarā")

def sutra_6_1_178(c) -> bool:
    """ङ्याश्छन्दसि बहुलम्."""
    return _eq(c, "suffix", "ṅyā") and _eq(c, "domain", "chandas") and _eq(c, "rule_strength", "bahula")

def sutra_6_1_179(c) -> bool:
    """षट्त्रिचतुर्भ्यो हलादिः."""
    return _in(c, "source", {"ṣaṭ", "tri", "catur"}) and _eq(c, "substitute", "halādi")

def sutra_6_1_180(c) -> bool:
    """झल्युपोत्तमम्."""
    return _eq(c, "suffix", "jhali") and _eq(c, "rule", "upottama")

def sutra_6_1_181(c) -> bool:
    """विभाषा भाषायाम्."""
    return _eq(c, "optional", True) and _eq(c, "domain", "bhāṣā")

def sutra_6_1_182(c) -> bool:
    """न गोश्वन्त्साववर्णराडङ्क्रुङ्कृद्भ्यः."""
    return _eq(c, "rule_blocked", True) and _in(c, "source", {"go", "śvan", "sā", "savarṇa", "rāṭ", "kru", "kṛd"})

def sutra_6_1_183(c) -> bool:
    """दिवो झल्."""
    return _eq(c, "source", "div") and _eq(c, "substitute", "jhal")

def sutra_6_1_184(c) -> bool:
    """नृ चान्यतरस्याम्."""
    return _eq(c, "stem", "nṛ") and _eq(c, "option", "anyatarā") and bool(c.get("also"))

def sutra_6_1_185(c) -> bool:
    """तित्स्वरितम्."""
    return _eq(c, "assigns_samjna", "tit") and _eq(c, "accent", "svarita")

def sutra_6_1_186(c) -> bool:
    """तास्यनुदात्तेन्ङिददुपदेशाल्लसार्वधातुकमनुदात्तमहन्विङोः."""
    return _eq(c, "source", "tāsyanudātten") and _in(c, "suffix", {"ṅit", "id", "ad"}) and _eq(c, "lakara", "lasārvadhātuka") and _eq(c, "accent", "anudātta") and _in(c, "stem", {"ah", "nv"})

def sutra_6_1_187(c) -> bool:
    """आदिः सिचोऽन्यतरस्याम्."""
    return _eq(c, "substitute", "ādi") and _eq(c, "suffix", "sic") and _eq(c, "option", "anyatarā")

def sutra_6_1_188(c) -> bool:
    """स्वपादिर्हिंसामच्यनिटि."""
    return _in(c, "dhatu_lemma", {"svap", "ādi", "hiṃs", "am"}) and _eq(c, "class", "ac") and not bool(c.get("is_aniṭ"))

def sutra_6_1_189(c) -> bool:
    """अभ्यस्तानामादिः."""
    return _eq(c, "stem_class", "abhyasta") and _eq(c, "substitute", "ādi")

def sutra_6_1_190(c) -> bool:
    """अनुदात्ते च."""
    return _eq(c, "accent", "anudātta") and bool(c.get("also"))

def sutra_6_1_191(c) -> bool:
    """सर्वस्य सुपि."""
    return _eq(c, "scope", "sarva") and _eq(c, "class", "sup")

def sutra_6_1_192(c) -> bool:
    """भीह्रीभृहुमदजनधनदरिद्राजागरां प्रत्ययात् पूर्वम् पिति."""
    return _in(c, "stem", {"bhī", "hrī", "bhṛ", "humad", "ajan", "dhana", "daridra", "āgara"}) and _eq(c, "site", "pratyaya") and _eq(c, "position", "pūrva") and _eq(c, "condition", "piti")

def sutra_6_1_193(c) -> bool:
    """लिति."""
    return _eq(c, "lakara", "lit")

def sutra_6_1_194(c) -> bool:
    """आदिर्णमुल्यन्यतरस्याम्."""
    return _eq(c, "substitute", "ādi") and _eq(c, "suffix", "ṇamul") and _eq(c, "option", "anyatarā")

def sutra_6_1_195(c) -> bool:
    """अचः कर्तृयकि."""
    return _eq(c, "class", "ac") and _eq(c, "suffix", "kartṛyak")

def sutra_6_1_196(c) -> bool:
    """थलि च सेटीडन्तो वा."""
    return _eq(c, "suffix", "thal") and _eq(c, "marker", "seṭ") and _eq(c, "augment", "iṭ") and _eq(c, "position", "anta") and _eq(c, "optional", True)

def sutra_6_1_197(c) -> bool:
    """ञ्णित्यादिर्नित्यम्."""
    return _eq(c, "suffix", "ñṇit") and _eq(c, "substitute", "ādi") and _eq(c, "rule_strength", "nitya")

def sutra_6_1_198(c) -> bool:
    """आमन्त्रितस्य च."""
    return _eq(c, "lakara", "āmantrita") and bool(c.get("also"))

def sutra_6_1_199(c) -> bool:
    """पथिमथोः सर्वनामस्थाने."""
    return _in(c, "stem", {"pathi", "matho"}) and _eq(c, "domain", "sarvānāmasthāna")

def sutra_6_1_200(c) -> bool:
    """अन्तश्च तवै युगपत्‌."""
    return _eq(c, "position", "anta") and _eq(c, "stem", "tava") and _eq(c, "rule", "yugapat")

def sutra_6_1_201(c) -> bool:
    """क्षयो निवासे."""
    return _eq(c, "form", "kṣaya") and _eq(c, "semantic", "nivāsa")

def sutra_6_1_202(c) -> bool:
    """जयः करणम्."""
    return _eq(c, "form", "jaya") and _eq(c, "assigns_samjna", "karaṇa")

def sutra_6_1_203(c) -> bool:
    """वृषादीनां च."""
    return _eq(c, "stem_class", "vṛṣādi") and bool(c.get("also"))

def sutra_6_1_204(c) -> bool:
    """संज्ञायामुपमानम्‌."""
    return _eq(c, "domain", "saṃjñā") and _eq(c, "assigns_samjna", "upamāna")

def sutra_6_1_205(c) -> bool:
    """निष्ठा च द्व्यजनात्‌."""
    return _eq(c, "suffix", "niṣṭhā") and _eq(c, "stem_class", "dvyac") and _eq(c, "source", "an")

def sutra_6_1_206(c) -> bool:
    """शुष्कधृष्टौ."""
    return _in(c, "stem", {"śuṣka", "dhṛṣṭa"})

def sutra_6_1_207(c) -> bool:
    """आशितः कर्ता."""
    return _eq(c, "form", "āśita") and _eq(c, "assigns_samjna", "kartṛ")

def sutra_6_1_208(c) -> bool:
    """रिक्ते विभाषा."""
    return _eq(c, "semantic", "rikta") and _eq(c, "optional", True)

def sutra_6_1_209(c) -> bool:
    """जुष्टार्पिते च छन्दसि."""
    return _in(c, "semantic", {"juṣṭa", "arpita"}) and _eq(c, "domain", "chandas") and bool(c.get("also"))

def sutra_6_1_210(c) -> bool:
    """नित्यं मन्त्रे."""
    return _eq(c, "rule_strength", "nitya") and _eq(c, "domain", "mantra")

def sutra_6_1_211(c) -> bool:
    """युष्मदस्मदोर्ङसि."""
    return _in(c, "stem", {"yuṣmad", "asmad"}) and _eq(c, "suffix", "ṅas")

def sutra_6_1_212(c) -> bool:
    """ङयि च."""
    return _eq(c, "suffix", "ṅay") and bool(c.get("also"))

def sutra_6_1_213(c) -> bool:
    """यतोऽनावः."""
    return _eq(c, "source", "yat") and _eq(c, "condition", "anāva")

def sutra_6_1_214(c) -> bool:
    """ईडवन्दवृशंसदुहां ण्यतः."""
    return _in(c, "stem", {"īḍ", "vand", "vṛś", "aṃsad", "uh"}) and _eq(c, "suffix", "ṇyat")

def sutra_6_1_215(c) -> bool:
    """विभाषा वेण्विन्धानयोः."""
    return _eq(c, "optional", True) and _in(c, "stem", {"veṇu", "indhāna"})

def sutra_6_1_216(c) -> bool:
    """त्यागरागहासकुहश्वठक्रथानाम्."""
    return _in(c, "stem", {"tyāga", "rāga", "hāsa", "kuha", "śvaṭha", "krath"})

def sutra_6_1_217(c) -> bool:
    """उपोत्तमं रिति."""
    return _eq(c, "rule", "upottama") and _eq(c, "class", "ṛ")

def sutra_6_1_218(c) -> bool:
    """चङ्यन्यतरस्याम्."""
    return _eq(c, "marker", "caṅ") and _eq(c, "option", "anyatarā")

def sutra_6_1_219(c) -> bool:
    """मतोः पूर्वमात्‌ संज्ञायां स्त्रियाम्‌."""
    return _eq(c, "source", "mat") and _eq(c, "position", "pūrva") and _eq(c, "substitute", "āt") and _eq(c, "domain", "saṃjñā") and _eq(c, "gender", "strī")

def sutra_6_1_220(c) -> bool:
    """अन्तोऽवत्याः."""
    return _eq(c, "position", "anta") and _eq(c, "stem", "avatī")

def sutra_6_1_221(c) -> bool:
    """ईवत्याः."""
    return _eq(c, "stem", "īvatī")

def sutra_6_1_222(c) -> bool:
    """चौ."""
    return _eq(c, "suffix", "cau")

def sutra_6_1_223(c) -> bool:
    """समासस्य."""
    return _eq(c, "domain", "samāsa")

# ---------------------------------------------------------------------------
# Fixtures + META
# ---------------------------------------------------------------------------

FIXTURES: dict[str, tuple[dict, dict]] = {

    "6.1.1": (
        {"vidhi_class": "reduplication", "redup_scope": "ekāca", "redup_target": "prathama", "redup_count": 2},
        {"vidhi_class": "reduplication", "redup_scope": "ekāca", "redup_target": "prathama", "redup_count": 1},
    ),
    "6.1.2": (
        {"vidhi_class": "reduplication", "redup_scope": "ajādi", "redup_target": "dvitīya"},
        {"vidhi_class": "reduplication", "redup_scope": "ajādi", "redup_target": "prathama"},
    ),
    "6.1.3": (
        {"stem_class": "ndr", "redup_class_blocked": "samyogādi"},
        {"stem_class": "ordinary", "redup_class_blocked": "samyogādi"},
    ),
    "6.1.4": (
        {"assigns_samjna": "abhyāsa", "position": "pūrva"},
        {"assigns_samjna": "abhyasta", "position": "pūrva"},
    ),
    "6.1.5": (
        {"assigns_samjna": "abhyasta", "scope": "ubhe"},
        {"assigns_samjna": "abhyāsa", "scope": "ubhe"},
    ),
    "6.1.6": (
        {"vidhi_class": "reduplication", "dhatu_lemma": "jakṣ"},
        {"vidhi_class": "reduplication", "dhatu_lemma": "bhū"},
    ),
    "6.1.7": (
        {"operation": "dīrgha", "target": "abhyāsa", "dhatu_lemma": "tuj"},
        {"operation": "dīrgha", "target": "abhyāsa", "dhatu_lemma": "bhū"},
    ),
    "6.1.8": (
        {"lakara": "liṭ", "applies_to": "dhatu", "applies_to_abhyāsa": False},
        {"lakara": "liṭ", "applies_to": "dhatu", "applies_to_abhyāsa": True},
    ),
    "6.1.9": (
        {"vidhi_class": "reduplication", "prefix": "san"},
        {"vidhi_class": "reduplication", "prefix": "pra"},
    ),
    "6.1.10": (
        {"vidhi_class": "reduplication", "marker": "ślu"},
        {"vidhi_class": "reduplication", "marker": "caṅ"},
    ),
    "6.1.11": (
        {"vidhi_class": "reduplication", "marker": "caṅ"},
        {"vidhi_class": "reduplication", "marker": "ślu"},
    ),
    "6.1.12": (
        {"vidhi_class": "reduplication", "dhatu_lemma": "dāśva"},
        {"vidhi_class": "reduplication", "dhatu_lemma": "bhū"},
    ),
    "6.1.13": (
        {"suffix": "ṣyaṅ", "operation": "samprasāraṇa", "compound_type": "tatpuruṣa", "semantic": "putra"},
        {"suffix": "ṣyaṅ", "operation": "samprasāraṇa", "compound_type": "tatpuruṣa", "semantic": "other"},
    ),
    "6.1.14": (
        {"operation": "samprasāraṇa", "compound_type": "bahuvrīhi", "semantic": "bandhu"},
        {"operation": "samprasāraṇa", "compound_type": "tatpuruṣa", "semantic": "bandhu"},
    ),
    "6.1.15": (
        {"assigns_samjna": "kit", "dhatu_lemma": "vac"},
        {"assigns_samjna": "kit", "dhatu_lemma": "bhū"},
    ),
    "6.1.16": (
        {"assigns_samjna": "kit", "dhatu_lemma": "grah"},
        {"assigns_samjna": "kit", "dhatu_lemma": "bhū", "is_ṅit": False},
    ),
    "6.1.17": (
        {"lakara": "liṭ", "applies_to_abhyāsa": True, "applies_to_dhatu": True},
        {"lakara": "liṭ", "applies_to_abhyāsa": False, "applies_to_dhatu": True},
    ),
    "6.1.18": (
        {"dhatu_lemma": "svāp", "marker": "caṅ"},
        {"dhatu_lemma": "svāp", "marker": "yaṅ"},
    ),
    "6.1.19": (
        {"marker": "yaṅ", "dhatu_lemma": "svap"},
        {"marker": "yaṅ", "dhatu_lemma": "bhū"},
    ),
    "6.1.20": (
        {"dhatu_lemma": "vaś", "rule_blocked": True},
        {"dhatu_lemma": "vaś", "rule_blocked": False},
    ),
    "6.1.21": (
        {"dhatu_lemma": "cāya", "redup_suffix": "kī"},
        {"dhatu_lemma": "cāya", "redup_suffix": "ślu"},
    ),
    "6.1.22": (
        {"dhatu_lemma": "sphāya", "lakara": "niṣṭhā"},
        {"dhatu_lemma": "sphāya", "lakara": "liṭ"},
    ),
    "6.1.23": (
        {"dhatu_lemma": "styā", "upasarga": "pra"},
        {"dhatu_lemma": "styā", "upasarga": "upa"},
    ),
    "6.1.24": (
        {"suffix": "śya", "semantic": "drava"},
        {"suffix": "śya", "semantic": "other"},
    ),
    "6.1.25": (
        {"suffix": "śya", "upasarga": "prati"},
        {"suffix": "śya", "upasarga": "upa"},
    ),
    "6.1.26": ({'upasarga_scope': 'abhyavaparva', 'optional': True}, {'upasarga_scope': 'abhyavaparva', 'optional': False}),
    "6.1.27": ({'form': 'śṛta', 'semantic': 'pāka'}, {'form': 'śṛta', 'semantic': '__miss__'}),
    "6.1.28": ({'dhatu_lemma': 'pyāya', 'redup_suffix': 'pī'}, {'dhatu_lemma': 'pyāya', 'redup_suffix': '__miss__'}),
    "6.1.29": ({'marker': 'liḍ'}, {'marker': '__miss__'}),
    "6.1.30": ({'stem': 'śva', 'optional': True}, {'stem': 'śva', 'optional': False}),
    "6.1.31": ({'lakara': 'ṇau', 'marker': 'san'}, {'lakara': 'ṇau', 'marker': '__miss__'}),
    "6.1.32": ({'stem': 'hv', 'operation': 'samprasāraṇa'}, {'stem': 'hv', 'operation': '__miss__'}),
    "6.1.33": ({'assigns_samjna': 'abhyasta', 'also': True}, {'assigns_samjna': 'abhyasta', 'also': False}),
    "6.1.34": ({'rule_strength': 'bahula', 'domain': 'chandas'}, {'rule_strength': 'bahula', 'domain': '__miss__'}),
    "6.1.35": ({'dhatu_lemma': 'cāya', 'redup_suffix': 'kī'}, {'dhatu_lemma': 'cāya', 'redup_suffix': '__miss__'}),
    "6.1.36": ({'dhatu_lemma': 'apaspṛdhe'}, {'dhatu_lemma': '__miss__'}),
    "6.1.37": ({'site': 'samprasāraṇa', 'operation_blocked': 'samprasāraṇa'}, {'site': 'samprasāraṇa', 'operation_blocked': '__miss__'}),
    "6.1.38": ({'lakara': 'liṭ', 'stem': 'vay', 'substitute': 'ya'}, {'lakara': 'liṭ', 'stem': 'vay', 'substitute': '__miss__'}),
    "6.1.39": ({'stem': 'vaś', 'option': 'anyatarā', 'assigns_samjna': 'kit'}, {'stem': 'vaś', 'option': 'anyatarā', 'assigns_samjna': '__miss__'}),
    "6.1.40": ({'marker': 'veñ'}, {'marker': '__miss__'}),
    "6.1.41": ({'suffix': 'lyap', 'also': True}, {'suffix': 'lyap', 'also': False}),
    "6.1.42": ({'stem': 'jy', 'also': True}, {'stem': 'jy', 'also': False}),
    "6.1.43": ({'stem': 'vy', 'also': True}, {'stem': 'vy', 'also': False}),
    "6.1.44": ({'position': 'para', 'optional': True}, {'position': 'para', 'optional': False}),
    "6.1.45": ({'site': 'upadeśa', 'class': 'ec', 'condition': 'aśiti'}, {'site': 'upadeśa', 'class': 'ec', 'condition': '__miss__'}),
    "6.1.46": ({'stem_class': 'vy', 'lakara': 'liṭ', 'rule_blocked': True}, {'stem_class': 'vy', 'lakara': 'liṭ', 'rule_blocked': False}),
    "6.1.47": ({'suffix': 'ghañ', 'dhatu_lemma': 'sphurat'}, {'suffix': 'ghañ', 'dhatu_lemma': '__miss__'}),
    "6.1.48": ({'lakara': 'ṇau', 'dhatu_lemma': 'krī'}, {'lakara': 'ṇau', 'dhatu_lemma': '__miss__'}),
    "6.1.49": ({'dhatu_lemma': 'sidh', 'semantic': 'apāralaukika'}, {'dhatu_lemma': 'sidh', 'semantic': '__miss__'}),
    "6.1.50": ({'suffix': 'lyap', 'dhatu_lemma': 'mīna', 'also': True}, {'suffix': 'lyap', 'dhatu_lemma': 'mīna', 'also': False}),
    "6.1.51": ({'dhatu_lemma': 'lī', 'optional': True}, {'dhatu_lemma': 'lī', 'optional': False}),
    "6.1.52": ({'marker': 'khid', 'domain': 'chandas'}, {'marker': 'khid', 'domain': '__miss__'}),
    "6.1.53": ({'dhatu_lemma': 'apagur', 'suffix': 'ṇamul'}, {'dhatu_lemma': 'apagur', 'suffix': '__miss__'}),
    "6.1.54": ({'lakara': 'ṇau', 'dhatu_lemma': 'ci'}, {'lakara': 'ṇau', 'dhatu_lemma': '__miss__'}),
    "6.1.55": ({'semantic': 'prajana', 'dhatu_lemma': 'vī'}, {'semantic': 'prajana', 'dhatu_lemma': '__miss__'}),
    "6.1.56": ({'dhatu_lemma': 'bibhet', 'semantic': 'hetubhaya'}, {'dhatu_lemma': 'bibhet', 'semantic': '__miss__'}),
    "6.1.57": ({'rule_strength': 'nitya', 'dhatu_lemma': 'smay'}, {'rule_strength': 'nitya', 'dhatu_lemma': '__miss__'}),
    "6.1.58": ({'suffix': 'jhali', 'assigns_samjna': 'kit', 'dhatu_lemma': 'sṛj', 'is_kit': False}, {'suffix': 'jhali', 'assigns_samjna': 'kit', 'dhatu_lemma': 'sṛj', 'is_kit': True}),
    "6.1.59": ({'accent': 'anudātta', 'upadha': 'ṛdu', 'option': 'anyatarā'}, {'accent': 'anudātta', 'upadha': 'ṛdu', 'option': '__miss__'}),
    "6.1.60": ({'stem': 'śīrṣan', 'domain': 'chandas'}, {'stem': 'śīrṣan', 'domain': '__miss__'}),
    "6.1.61": ({'suffix': 'ya', 'suffix_class': 'taddhita', 'also': True}, {'suffix': 'ya', 'suffix_class': 'taddhita', 'also': False}),
    "6.1.62": ({'class': 'ac', 'stem': 'śīrṣan'}, {'class': 'ac', 'stem': '__miss__'}),
    "6.1.63": ({'suffix': 'śas', 'stem': 'paddat'}, {'suffix': 'śas', 'stem': '__miss__'}),
    "6.1.64": ({'site': 'dhātuvādi', 'substitute': 'ṣ', 'replacement': 's'}, {'site': 'dhātuvādi', 'substitute': 'ṣ', 'replacement': '__miss__'}),
    "6.1.65": ({'substitute': 'ṇ', 'replacement': 'n'}, {'substitute': 'ṇ', 'replacement': '__miss__'}),
    "6.1.66": ({'operation': 'lopa', 'stem_class': 'vy', 'suffix': 'val'}, {'operation': 'lopa', 'stem_class': 'vy', 'suffix': '__miss__'}),
    "6.1.67": ({'stem': 've', 'condition': 'apṛkta'}, {'stem': 've', 'condition': '__miss__'}),
    "6.1.68": ({'source': 'dīrgha', 'target': 'hal', 'condition': 'apṛkta'}, {'source': 'dīrgha', 'target': 'hal', 'condition': '__miss__'}),
    "6.1.69": ({'source': 'eṅhrasva', 'domain': 'sambuddhi'}, {'source': 'eṅhrasva', 'domain': '__miss__'}),
    "6.1.70": ({'stem': 'śe', 'domain': 'chandas', 'rule_strength': 'bahula'}, {'stem': 'śe', 'domain': 'chandas', 'rule_strength': '__miss__'}),
    "6.1.71": ({'vowel_weight': 'hrasva', 'condition': 'piti', 'suffix_class': 'kṛt', 'augment': 'tuk'}, {'vowel_weight': 'hrasva', 'condition': 'piti', 'suffix_class': 'kṛt', 'augment': '__miss__'}),
    "6.1.72": ({'domain': 'saṃhitā'}, {'domain': '__miss__'}),
    "6.1.73": ({'domain': 'chha', 'also': True}, {'domain': 'chha', 'also': False}),
    "6.1.74": ({'prefix': 'āṅ', 'also': True}, {'prefix': 'āṅ', 'also': False}),
    "6.1.75": ({'operation': 'dīrgha'}, {'operation': '__miss__'}),
    "6.1.76": ({'site': 'padānta', 'optional': True}, {'site': 'padānta', 'optional': False}),
    "6.1.77": ({'class': 'ik', 'substitute': 'yaṇ', 'environment': 'ac'}, {'class': 'ik', 'substitute': 'yaṇ', 'environment': '__miss__'}),
    "6.1.78": ({'left': 'hare', 'right': 'atra'}, {'left': 'deva', 'right': 'gacchati'}),
    "6.1.79": ({'final': 'vānta', 'suffix': 'yi', 'site': 'pratyaya'}, {'final': 'vānta', 'suffix': 'yi', 'site': '__miss__'}),
    "6.1.80": ({'applies_to': 'dhatu', 'cause': 'tannimitta'}, {'applies_to': 'dhatu', 'cause': '__miss__'}),
    "6.1.81": ({'semantic': 'śakya_artha', 'form': 'kṣayya'}, {'semantic': 'śakya_artha', 'form': '__miss__'}),
    "6.1.82": ({'form': 'krayya', 'semantic': 'tad_artha'}, {'form': 'krayya', 'semantic': '__miss__'}),
    "6.1.83": ({'domain': 'chandas', 'form': 'bhayya', 'also': True}, {'domain': 'chandas', 'form': 'bhayya', 'also': False}),
    "6.1.84": ({'substitute': 'eka', 'scope': 'pūrvapara'}, {'substitute': 'eka', 'scope': '__miss__'}),
    "6.1.85": ({'rule': 'antādivat', 'also': True}, {'rule': 'antādivat', 'also': False}),
    "6.1.86": ({'site': 'ṣṭut', 'validity': 'asiddha'}, {'site': 'ṣṭut', 'validity': '__miss__'}),
    "6.1.87": ({'left': 'deva', 'right': 'iti'}, {'left': 'deva', 'right': 'gacchati'}),
    "6.1.88": ({'left': 'deva', 'right': 'eva'}, {'left': 'deva', 'right': 'gacchati'}),
    "6.1.89": ({'augment': 'ṭ', 'suffix': 'et'}, {'augment': 'ṭ', 'suffix': '__miss__'}),
    "6.1.90": ({'site': 'āṭ', 'also': True}, {'site': 'āṭ', 'also': False}),
    "6.1.91": ({"after": "upasarga", "class": "ṛ", "locus": "dhatu"}, {"after": "upasarga", "class": "ṛ", "locus": "suffix"}),
    "6.1.92": ({'class': 'sup', 'stem_class': 'āpiśali', 'optional': True}, {'class': 'sup', 'stem_class': 'āpiśali', 'optional': False}),
    "6.1.93": ({'substitute': 'ā', 'source': 'ot', 'suffix': 'aṃ'}, {'substitute': 'ā', 'source': 'ot', 'suffix': '__miss__'}),
    "6.1.94": ({'class': 'eṅ', 'substitute': 'pararūpa'}, {'class': 'eṅ', 'substitute': '__miss__'}),
    "6.1.95": ({'prefix': 'o', 'also': True}, {'prefix': 'o', 'also': False}),
    "6.1.96": ({'class': 'us', 'site': 'apadānta'}, {'class': 'us', 'site': '__miss__'}),
    "6.1.97": ({'source': 'a', 'sandhi_rule': 'guṇa'}, {'source': 'a', 'sandhi_rule': '__miss__'}),
    "6.1.98": ({'semantic': 'avyaktānukaraṇa', 'source': 'a', 'suffix': 'it'}, {'semantic': 'avyaktānukaraṇa', 'source': 'a', 'suffix': '__miss__'}),
    "6.1.99": ({'stem_class': 'āmreḍita', 'position': 'antya', 'optional': True}, {'stem_class': 'āmreḍita', 'position': 'antya', 'optional': False}),
    "6.1.100": ({'stem_class': 'āmreḍita', 'class': 'ḍāc', 'rule_strength': 'nitya'}, {'stem_class': 'āmreḍita', 'class': 'ḍāc', 'rule_strength': '__miss__'}),
    "6.1.101": ({'left': 'deva', 'right': 'atra'}, {'left': 'deva', 'right': 'gacchati'}),
    "6.1.102": ({'scope': 'prathama', 'substitute': 'pūrvasavarna'}, {'scope': 'prathama', 'substitute': '__miss__'}),
    "6.1.103": ({'source': 'śas', 'substitute': 'na', 'gender': 'puṃ'}, {'source': 'śas', 'substitute': 'na', 'gender': '__miss__'}),
    "6.1.104": ({'source': 'ā', 'class': 'ic', 'rule_blocked': True}, {'source': 'ā', 'class': 'ic', 'rule_blocked': False}),
    "6.1.105": ({'operation': 'dīrgha', 'class': 'jas', 'also': True}, {'operation': 'dīrgha', 'class': 'jas', 'also': False}),
    "6.1.106": ({'domain': 'chandas', 'optional': True}, {'domain': 'chandas', 'optional': False}),
    "6.1.107": ({'class': 'am', 'position': 'pūrva'}, {'class': 'am', 'position': '__miss__'}),
    "6.1.108": ({'source': 'samprasāraṇa', 'also': True}, {'source': 'samprasāraṇa', 'also': False}),
    "6.1.109": ({'source': 'eṅ', 'site': 'padānta', 'suffix': 'ati'}, {'source': 'eṅ', 'site': 'padānta', 'suffix': '__miss__'}),
    "6.1.110": ({'suffix': 'ṅas', 'also': True}, {'suffix': 'ṅas', 'also': False}),
    "6.1.111": ({'source': 'ṛt', 'substitute': 'ut'}, {'source': 'ṛt', 'substitute': '__miss__'}),
    "6.1.112": ({'source': 'khyati', 'position': 'para'}, {'source': 'khyati', 'position': '__miss__'}),
    "6.1.113": ({'source': 'a', 'stem': 'ro', 'condition': 'apluta'}, {'source': 'a', 'stem': 'ro', 'condition': '__miss__'}),
    "6.1.114": ({'class': 'haś', 'also': True}, {'class': 'haś', 'also': False}),
    "6.1.115": ({'instrument': 'prakṛti', 'domain': 'antapāda', 'condition': 'avyapara'}, {'instrument': 'prakṛti', 'domain': 'antapāda', 'condition': '__miss__'}),
    "6.1.116": ({'form': 'avyāda', 'also': True}, {'form': 'avyāda', 'also': False}),
    "6.1.117": ({'domain': 'yajuṣ', 'substitute': 'uraḥ'}, {'domain': 'yajuṣ', 'substitute': '__miss__'}),
    "6.1.118": ({'position': 'pūrva', 'form': 'āpas'}, {'position': 'pūrva', 'form': '__miss__'}),
    "6.1.119": ({'stem': 'aṅga', 'domain': 'ityādi', 'also': True}, {'stem': 'aṅga', 'domain': 'ityādi', 'also': False}),
    "6.1.120": ({'accent': 'anudātta', 'domain': 'kudhpara', 'also': True}, {'accent': 'anudātta', 'domain': 'kudhpara', 'also': False}),
    "6.1.121": ({'domain': 'avapathā', 'also': True}, {'domain': 'avapathā', 'also': False}),
    "6.1.122": ({'stem': 'go', 'optional': True}, {'stem': 'go', 'optional': False}),
    "6.1.123": ({'substitute': 'avaṅ', 'authority': 'sphoṭāyana'}, {'substitute': 'avaṅ', 'authority': '__miss__'}),
    "6.1.124": ({'stem': 'indra', 'rule_strength': 'nitya', 'also': True}, {'stem': 'indra', 'rule_strength': 'nitya', 'also': False}),
    "6.1.125": ({'stem_class': 'plutapragṛhya', 'class': 'ac', 'rule_strength': 'nitya'}, {'stem_class': 'plutapragṛhya', 'class': 'ac', 'rule_strength': '__miss__'}),
    "6.1.126": ({'prefix': 'āṅ', 'substitute': 'anunāsika', 'domain': 'chandas'}, {'prefix': 'āṅ', 'substitute': 'anunāsika', 'domain': '__miss__'}),
    "6.1.127": ({'class': 'ik', 'condition': 'asavarṇa', 'authority': 'śākalya', 'vowel_weight': 'hrasva', 'also': True}, {'class': 'ik', 'condition': 'asavarṇa', 'authority': 'śākalya', 'vowel_weight': 'hrasva', 'also': False}),
    "6.1.128": ({'class': 'ṛ', 'substitute': 'ak'}, {'class': 'ṛ', 'substitute': '__miss__'}),
    "6.1.129": ({'condition': 'aplutavat', 'state': 'upasthita'}, {'condition': 'aplutavat', 'state': '__miss__'}),
    "6.1.130": ({'substitute': 'ī3', 'authority': 'cākravarmaṇa'}, {'substitute': 'ī3', 'authority': '__miss__'}),
    "6.1.131": ({'stem': 'div', 'substitute': 'ut'}, {'stem': 'div', 'substitute': '__miss__'}),
    "6.1.132": ({'operation': 'su-lopa', 'compound_type': 'an-añ', 'class': 'hal', 'stem': 'etad'}, {'operation': 'su-lopa', 'compound_type': 'an-añ', 'class': 'hal', 'stem': '__miss__'}),
    "6.1.133": ({'stem': 'sya', 'domain': 'chandas', 'rule_strength': 'bahula'}, {'stem': 'sya', 'domain': 'chandas', 'rule_strength': '__miss__'}),
    "6.1.134": ({'substitute': 'sa', 'class': 'ac', 'operation': 'lopa', 'domain': 'pādapūraṇa'}, {'substitute': 'sa', 'class': 'ac', 'operation': 'lopa', 'domain': '__miss__'}),
    "6.1.135": ({'augment': 'suṭ', 'source': 'ka', 'position': 'pūrva'}, {'augment': 'suṭ', 'source': 'ka', 'position': '__miss__'}),
    "6.1.136": ({'site': 'aḍ', 'domain': 'abhyāsa', 'also': True}, {'site': 'aḍ', 'domain': 'abhyāsa', 'also': False}),
    "6.1.137": ({'semantic': 'bhūṣaṇa', 'prefix': 'sam', 'dhatu_lemma': 'kṛ'}, {'semantic': 'bhūṣaṇa', 'prefix': 'sam', 'dhatu_lemma': '__miss__'}),
    "6.1.138": ({'semantic': 'samavāya', 'also': True}, {'semantic': 'samavāya', 'also': False}),
    "6.1.139": ({'source': 'upa', 'semantic': 'pratiyoga'}, {'source': 'upa', 'semantic': '__miss__'}),
    "6.1.140": ({'dhatu_lemma': 'kir', 'semantic': 'lavana'}, {'dhatu_lemma': 'kir', 'semantic': '__miss__'}),
    "6.1.141": ({'semantic': 'hiṃsā', 'upasarga': 'prati', 'also': True}, {'semantic': 'hiṃsā', 'upasarga': 'prati', 'also': False}),
    "6.1.142": ({'source': 'apa', 'semantic': 'ālekhana', 'domain': 'catuṣpāt'}, {'source': 'apa', 'semantic': 'ālekhana', 'domain': '__miss__'}),
    "6.1.143": ({'assigns_samjna': 'jāti', 'stem': 'kustumburu'}, {'assigns_samjna': 'jāti', 'stem': '__miss__'}),
    "6.1.144": ({'form': 'aparasparā', 'semantic': 'kriyāsātathya'}, {'form': 'aparasparā', 'semantic': '__miss__'}),
    "6.1.145": ({'form': 'goṣpada', 'semantic': 'sevita'}, {'form': 'goṣpada', 'semantic': '__miss__'}),
    "6.1.146": ({'form': 'āspada', 'semantic': 'pratiṣṭhā'}, {'form': 'āspada', 'semantic': '__miss__'}),
    "6.1.147": ({'form': 'āścarya', 'condition': 'anitya'}, {'form': 'āścarya', 'condition': '__miss__'}),
    "6.1.148": ({'semantic': 'varcask', 'form': 'avaskara'}, {'semantic': 'varcask', 'form': '__miss__'}),
    "6.1.149": ({'form': 'apaskara', 'semantic': 'rathāṅga'}, {'form': 'apaskara', 'semantic': '__miss__'}),
    "6.1.150": ({'form': 'viṣkira', 'optional': True, 'semantic': 'śakuni'}, {'form': 'viṣkira', 'optional': True, 'semantic': '__miss__'}),
    "6.1.151": ({"source": "hrasva", "domain": "candrottarapada", "in_mantra": True}, {"source": "hrasva", "domain": "candrottarapada", "in_mantra": False}),
    "6.1.152": ({'form': 'pratiṣkaśa', 'stem': 'kaśa', 'also': True}, {'form': 'pratiṣkaśa', 'stem': 'kaśa', 'also': False}),
    "6.1.153": ({'assigns_samjna': 'ṛṣi', 'form': 'praskaṇva'}, {'assigns_samjna': 'ṛṣi', 'form': '__miss__'}),
    "6.1.154": ({'form': 'maskara', 'domain': 'veṇu'}, {'form': 'maskara', 'domain': '__miss__'}),
    "6.1.155": ({'form': 'kāstīrājastunde', 'domain': 'nagara'}, {'form': 'kāstīrājastunde', 'domain': '__miss__'}),
    "6.1.156": ({'form': 'kāraskara', 'semantic': 'vṛkṣa'}, {'form': 'kāraskara', 'semantic': '__miss__'}),
    "6.1.157": ({'stem_class': 'pāraskaraprabhṛti', 'domain': 'saṃjñā', 'also': True}, {'stem_class': 'pāraskaraprabhṛti', 'domain': 'saṃjñā', 'also': False}),
    "6.1.158": ({'accent': 'anudātta', 'assigns_samjna': 'pada', 'condition': 'ekavarjya'}, {'accent': 'anudātta', 'assigns_samjna': 'pada', 'condition': '__miss__'}),
    "6.1.159": ({'source': 'karṣātva', 'suffix': 'ghañ', 'position': 'anta', 'accent': 'udātta'}, {'source': 'karṣātva', 'suffix': 'ghañ', 'position': 'anta', 'accent': '__miss__'}),
    "6.1.160": ({'stem_class': 'uñchādi', 'also': True}, {'stem_class': 'uñchādi', 'also': False}),
    "6.1.161": ({'accent': 'anudātta', 'operation': 'udāttalopa'}, {'accent': 'anudātta', 'operation': '__miss__'}),
    "6.1.162": ({'applies_to': 'dhatu'}, {'applies_to': '__miss__'}),
    "6.1.163": ({'applies_to': 'cit'}, {'applies_to': '__miss__'}),
    "6.1.164": ({'anga': 'taddhita'}, {'anga': '__miss__'}),
    "6.1.165": ({'marker': 'kit'}, {'marker': '__miss__'}),
    "6.1.166": ({'source': 'tisṛ', 'suffix': 'jas'}, {'source': 'tisṛ', 'suffix': '__miss__'}),
    "6.1.167": ({'stem': 'catur', 'suffix': 'śas'}, {'stem': 'catur', 'suffix': '__miss__'}),
    "6.1.168": ({'source': 'sau', 'class': 'ekāca', 'assigns_samjna': 'vibhakti'}, {'source': 'sau', 'class': 'ekāca', 'assigns_samjna': '__miss__'}),
    "6.1.169": ({"source": "antodātta", "from": "uttarapada", "compound": "anitya", "option": "anyatarā"}, {"source": "antodātta", "from": "uttarapada", "compound": "nitya", "option": "anyatarā"}),
    "6.1.170": ({"source": "añci", "domain": "chandas", "assigns_samjna": "other"}, {"source": "añci", "domain": "chandas", "assigns_samjna": "sarvānāmasthāna"}),
    "6.1.171": ({'source': 'ūḍidampadādyap', 'suffix': 'mṛ'}, {'source': 'ūḍidampadādyap', 'suffix': '__miss__'}),
    "6.1.172": ({'source': 'aṣṭan', 'operation': 'dīrgha'}, {'source': 'aṣṭan', 'operation': '__miss__'}),
    "6.1.173": ({"source": "śatu", "also": "anum", "stem_class": "nadyajādi"}, {"source": "śatu", "also": "anum", "stem_class": "other"}),
    "6.1.174": ({"source": "udāttayaṇ", "from": "halpūrva"}, {"source": "udāttayaṇ", "from": "other"}),
    "6.1.175": ({'substitute': 'na', 'marker': 'ūṅ'}, {'substitute': 'na', 'marker': '__miss__'}),
    "6.1.176": ({'source': 'hrasvanuṭ', 'suffix': 'matup'}, {'source': 'hrasvanuṭ', 'suffix': '__miss__'}),
    "6.1.177": ({'assigns_samjna': 'nāman', 'option': 'anyatarā'}, {'assigns_samjna': 'nāman', 'option': '__miss__'}),
    "6.1.178": ({'suffix': 'ṅyā', 'domain': 'chandas', 'rule_strength': 'bahula'}, {'suffix': 'ṅyā', 'domain': 'chandas', 'rule_strength': '__miss__'}),
    "6.1.179": ({'substitute': 'halādi', 'source': 'ṣaṭ'}, {'substitute': 'halādi', 'source': '__miss__'}),
    "6.1.180": ({'suffix': 'jhali', 'rule': 'upottama'}, {'suffix': 'jhali', 'rule': '__miss__'}),
    "6.1.181": ({'domain': 'bhāṣā', 'optional': True}, {'domain': 'bhāṣā', 'optional': False}),
    "6.1.182": ({'rule_blocked': True, 'source': 'go'}, {'rule_blocked': True, 'source': '__miss__'}),
    "6.1.183": ({'source': 'div', 'substitute': 'jhal'}, {'source': 'div', 'substitute': '__miss__'}),
    "6.1.184": ({'stem': 'nṛ', 'option': 'anyatarā', 'also': True}, {'stem': 'nṛ', 'option': 'anyatarā', 'also': False}),
    "6.1.185": ({'assigns_samjna': 'tit', 'accent': 'svarita'}, {'assigns_samjna': 'tit', 'accent': '__miss__'}),
    "6.1.186": ({'source': 'tāsyanudātten', 'lakara': 'lasārvadhātuka', 'accent': 'anudātta', 'suffix': 'ṅit', 'stem': 'ah'}, {'source': 'tāsyanudātten', 'lakara': 'lasārvadhātuka', 'accent': 'anudātta', 'suffix': 'ṅit', 'stem': '__miss__'}),
    "6.1.187": ({'substitute': 'ādi', 'suffix': 'sic', 'option': 'anyatarā'}, {'substitute': 'ādi', 'suffix': 'sic', 'option': '__miss__'}),
    "6.1.188": ({'class': 'ac', 'dhatu_lemma': 'svap', 'is_aniṭ': False}, {'class': 'ac', 'dhatu_lemma': 'svap', 'is_aniṭ': True}),
    "6.1.189": ({'stem_class': 'abhyasta', 'substitute': 'ādi'}, {'stem_class': 'abhyasta', 'substitute': '__miss__'}),
    "6.1.190": ({'accent': 'anudātta', 'also': True}, {'accent': 'anudātta', 'also': False}),
    "6.1.191": ({'scope': 'sarva', 'class': 'sup'}, {'scope': 'sarva', 'class': '__miss__'}),
    "6.1.192": ({'site': 'pratyaya', 'position': 'pūrva', 'condition': 'piti', 'stem': 'bhī'}, {'site': 'pratyaya', 'position': 'pūrva', 'condition': 'piti', 'stem': '__miss__'}),
    "6.1.193": ({'lakara': 'lit'}, {'lakara': '__miss__'}),
    "6.1.194": ({'substitute': 'ādi', 'suffix': 'ṇamul', 'option': 'anyatarā'}, {'substitute': 'ādi', 'suffix': 'ṇamul', 'option': '__miss__'}),
    "6.1.195": ({'class': 'ac', 'suffix': 'kartṛyak'}, {'class': 'ac', 'suffix': '__miss__'}),
    "6.1.196": ({'suffix': 'thal', 'marker': 'seṭ', 'augment': 'iṭ', 'position': 'anta', 'optional': True}, {'suffix': 'thal', 'marker': 'seṭ', 'augment': 'iṭ', 'position': 'anta', 'optional': False}),
    "6.1.197": ({'suffix': 'ñṇit', 'substitute': 'ādi', 'rule_strength': 'nitya'}, {'suffix': 'ñṇit', 'substitute': 'ādi', 'rule_strength': '__miss__'}),
    "6.1.198": ({'lakara': 'āmantrita', 'also': True}, {'lakara': 'āmantrita', 'also': False}),
    "6.1.199": ({'domain': 'sarvānāmasthāna', 'stem': 'pathi'}, {'domain': 'sarvānāmasthāna', 'stem': '__miss__'}),
    "6.1.200": ({'position': 'anta', 'stem': 'tava', 'rule': 'yugapat'}, {'position': 'anta', 'stem': 'tava', 'rule': '__miss__'}),
    "6.1.201": ({'form': 'kṣaya', 'semantic': 'nivāsa'}, {'form': 'kṣaya', 'semantic': '__miss__'}),
    "6.1.202": ({'form': 'jaya', 'assigns_samjna': 'karaṇa'}, {'form': 'jaya', 'assigns_samjna': '__miss__'}),
    "6.1.203": ({'stem_class': 'vṛṣādi', 'also': True}, {'stem_class': 'vṛṣādi', 'also': False}),
    "6.1.204": ({'domain': 'saṃjñā', 'assigns_samjna': 'upamāna'}, {'domain': 'saṃjñā', 'assigns_samjna': '__miss__'}),
    "6.1.205": ({'suffix': 'niṣṭhā', 'stem_class': 'dvyac', 'source': 'an'}, {'suffix': 'niṣṭhā', 'stem_class': 'dvyac', 'source': '__miss__'}),
    "6.1.206": ({'stem': 'śuṣka'}, {'stem': '__miss__'}),
    "6.1.207": ({'form': 'āśita', 'assigns_samjna': 'kartṛ'}, {'form': 'āśita', 'assigns_samjna': '__miss__'}),
    "6.1.208": ({'semantic': 'rikta', 'optional': True}, {'semantic': 'rikta', 'optional': False}),
    "6.1.209": ({'domain': 'chandas', 'semantic': 'juṣṭa', 'also': True}, {'domain': 'chandas', 'semantic': 'juṣṭa', 'also': False}),
    "6.1.210": ({'rule_strength': 'nitya', 'domain': 'mantra'}, {'rule_strength': 'nitya', 'domain': '__miss__'}),
    "6.1.211": ({'suffix': 'ṅas', 'stem': 'yuṣmad'}, {'suffix': 'ṅas', 'stem': '__miss__'}),
    "6.1.212": ({'suffix': 'ṅay', 'also': True}, {'suffix': 'ṅay', 'also': False}),
    "6.1.213": ({'source': 'yat', 'condition': 'anāva'}, {'source': 'yat', 'condition': '__miss__'}),
    "6.1.214": ({'suffix': 'ṇyat', 'stem': 'īḍ'}, {'suffix': 'ṇyat', 'stem': '__miss__'}),
    "6.1.215": ({'optional': True, 'stem': 'veṇu'}, {'optional': True, 'stem': '__miss__'}),
    "6.1.216": ({'stem': 'tyāga'}, {'stem': '__miss__'}),
    "6.1.217": ({'rule': 'upottama', 'class': 'ṛ'}, {'rule': 'upottama', 'class': '__miss__'}),
    "6.1.218": ({'marker': 'caṅ', 'option': 'anyatarā'}, {'marker': 'caṅ', 'option': '__miss__'}),
    "6.1.219": ({'source': 'mat', 'position': 'pūrva', 'substitute': 'āt', 'domain': 'saṃjñā', 'gender': 'strī'}, {'source': 'mat', 'position': 'pūrva', 'substitute': 'āt', 'domain': 'saṃjñā', 'gender': '__miss__'}),
    "6.1.220": ({'position': 'anta', 'stem': 'avatī'}, {'position': 'anta', 'stem': '__miss__'}),
    "6.1.221": ({'stem': 'īvatī'}, {'stem': '__miss__'}),
    "6.1.222": ({'suffix': 'cau'}, {'suffix': '__miss__'}),
    "6.1.223": ({'domain': 'samāsa'}, {'domain': '__miss__'}),
}

META: dict[str, SutraMeta] = {

    "6.1.1": SutraMeta("vidhi", "ekāco dve prathamasya", ("sandhi:6.1", "reduplication")),
    "6.1.2": SutraMeta("vidhi", "ajāder dvitīyasya", ("sandhi:6.1", "reduplication")),
    "6.1.3": SutraMeta("pratisedha", "na ndrāḥ saṃyogādayaḥ", ("sandhi:6.1",)),
    "6.1.4": SutraMeta("samjna", "pūrve'bhyāsaḥ", ("sandhi:6.1", "abhyāsa")),
    "6.1.5": SutraMeta("samjna", "ubhe abhyastam", ("sandhi:6.1", "abhyāsta")),
    "6.1.6": SutraMeta("vidhi", "jakṣityādayaḥ ṣaṭ", ("sandhi:6.1",)),
    "6.1.7": SutraMeta("vidhi", "tujādīnāṃ dīrgho'bhyāsya", ("sandhi:6.1",)),
    "6.1.8": SutraMeta("vidhi", "liti dhātor anabhyāsya", ("sandhi:6.1", "liṭ")),
    "6.1.9": SutraMeta("vidhi", "sanyāṅoḥ", ("sandhi:6.1",)),
    "6.1.10": SutraMeta("vidhi", "ślau", ("sandhi:6.1",)),
    "6.1.11": SutraMeta("vidhi", "caṅi", ("sandhi:6.1",)),
    "6.1.12": SutraMeta("vidhi", "dāśvān sāhvān mīḍhvāṃś ca", ("sandhi:6.1",)),
    "6.1.13": SutraMeta("vidhi", "ṣyaṅaḥ samprasāraṇaṃ putrapatyos tatpuruṣe", ("sandhi:6.1",)),
    "6.1.14": SutraMeta("vidhi", "bandhuni bahuvrīhau", ("sandhi:6.1",)),
    "6.1.15": SutraMeta("samjna", "vacisvapiyajādīnāṃ kiti", ("sandhi:6.1", "kit")),
    "6.1.16": SutraMeta("samjna", "grahijyādiṣu ṅiti ca", ("sandhi:6.1", "kit")),
    "6.1.17": SutraMeta("vidhi", "lity abhyāsasyobhayeṣām", ("sandhi:6.1", "liṭ")),
    "6.1.18": SutraMeta("vidhi", "svāpeś caṅi", ("sandhi:6.1",)),
    "6.1.19": SutraMeta("vidhi", "svapisyamivyāñjāṃ yaṅi", ("sandhi:6.1",)),
    "6.1.20": SutraMeta("pratisedha", "na vaśaḥ", ("sandhi:6.1",)),
    "6.1.21": SutraMeta("vidhi", "cāyaḥ kī", ("sandhi:6.1",)),
    "6.1.22": SutraMeta("vidhi", "sphāyaḥ sphī niṣṭhāyām", ("sandhi:6.1",)),
    "6.1.23": SutraMeta("vidhi", "styaḥ prapūrvāsya", ("sandhi:6.1",)),
    "6.1.24": SutraMeta("vidhi", "dravamūrtisparśayoḥ śyaḥ", ("sandhi:6.1",)),
    "6.1.25": SutraMeta("vidhi", "prateś ca", ("sandhi:6.1",)),
    "6.1.26": SutraMeta("vibhasha", "विभाषाऽभ्यवपूर्वस्य", ("sandhi:6.1",)),
    "6.1.27": SutraMeta("vidhi", "शृतं पाके", ("sandhi:6.1",)),
    "6.1.28": SutraMeta("vidhi", "प्यायः पी", ("sandhi:6.1",)),
    "6.1.29": SutraMeta("vidhi", "लिड्यङोश्च", ("sandhi:6.1",)),
    "6.1.30": SutraMeta("vibhasha", "विभाषा श्वेः", ("sandhi:6.1",)),
    "6.1.31": SutraMeta("vidhi", "णौ च संश्चङोः", ("sandhi:6.1",)),
    "6.1.32": SutraMeta("vidhi", "ह्वः सम्प्रसारणम्", ("sandhi:6.1",)),
    "6.1.33": SutraMeta("samjna", "अभ्यस्तस्य च", ("sandhi:6.1",)),
    "6.1.34": SutraMeta("paribhasha", "बहुलं छन्दसि", ("sandhi:6.1",)),
    "6.1.35": SutraMeta("vidhi", "चायः की", ("sandhi:6.1",)),
    "6.1.36": SutraMeta("vidhi", "अपस्पृधेथामानृचुरानृहुश्चिच्युषेतित्याजश्राताःश्रितमाशीराशीर्त्तः", ("sandhi:6.1",)),
    "6.1.37": SutraMeta("vidhi", "न सम्प्रसारणे सम्प्रसारणम्", ("sandhi:6.1",)),
    "6.1.38": SutraMeta("vidhi", "लिटि वयो यः", ("sandhi:6.1",)),
    "6.1.39": SutraMeta("samjna", "वश्चास्यान्यतरस्याम् किति", ("sandhi:6.1",)),
    "6.1.40": SutraMeta("vidhi", "वेञः", ("sandhi:6.1",)),
    "6.1.41": SutraMeta("vidhi", "ल्यपि च", ("sandhi:6.1",)),
    "6.1.42": SutraMeta("vidhi", "ज्यश्च", ("sandhi:6.1",)),
    "6.1.43": SutraMeta("vidhi", "व्यश्च", ("sandhi:6.1",)),
    "6.1.44": SutraMeta("vibhasha", "विभाषा परेः", ("sandhi:6.1",)),
    "6.1.45": SutraMeta("vidhi", "आदेच उपदेशेऽशिति", ("sandhi:6.1",)),
    "6.1.46": SutraMeta("pratisedha", "न व्यो लिटि", ("sandhi:6.1",)),
    "6.1.47": SutraMeta("vidhi", "स्फुरतिस्फुलत्योर्घञि", ("sandhi:6.1",)),
    "6.1.48": SutraMeta("vidhi", "क्रीङ्जीनां णौ", ("sandhi:6.1",)),
    "6.1.49": SutraMeta("vidhi", "सिध्यतेरपारलौकिके", ("sandhi:6.1",)),
    "6.1.50": SutraMeta("vidhi", "मीनातिमिनोतिदीङां ल्यपि च", ("sandhi:6.1",)),
    "6.1.51": SutraMeta("vibhasha", "विभाषा लीयतेः", ("sandhi:6.1",)),
    "6.1.52": SutraMeta("vidhi", "खिदेश्छन्दसि", ("sandhi:6.1",)),
    "6.1.53": SutraMeta("vidhi", "अपगुरो णमुलि", ("sandhi:6.1",)),
    "6.1.54": SutraMeta("vidhi", "चिस्फुरोर्णौ", ("sandhi:6.1",)),
    "6.1.55": SutraMeta("vidhi", "प्रजने वीयतेः", ("sandhi:6.1",)),
    "6.1.56": SutraMeta("vidhi", "बिभेतेर्हेतुभये", ("sandhi:6.1",)),
    "6.1.57": SutraMeta("vidhi", "नित्यं स्मयतेः", ("sandhi:6.1",)),
    "6.1.58": SutraMeta("samjna", "सृजिदृशोर्झल्यमकिति", ("sandhi:6.1",)),
    "6.1.59": SutraMeta("vidhi", "अनुदात्तस्य चर्दुपधस्यान्यतरस्याम्", ("sandhi:6.1",)),
    "6.1.60": SutraMeta("vidhi", "शीर्षंश्छन्दसि", ("sandhi:6.1",)),
    "6.1.61": SutraMeta("vidhi", "ये च तद्धिते", ("sandhi:6.1",)),
    "6.1.62": SutraMeta("vidhi", "अचि शीर्षः", ("sandhi:6.1",)),
    "6.1.63": SutraMeta("vidhi", "पद्दन्नोमास्हृन्निशसन्यूषन्दोषन्यकञ्छकन्नुदन्नासञ्छस्प्रभृतिषु", ("sandhi:6.1",)),
    "6.1.64": SutraMeta("vidhi", "धात्वादेः षः सः", ("sandhi:6.1",)),
    "6.1.65": SutraMeta("vidhi", "णो नः", ("sandhi:6.1",)),
    "6.1.66": SutraMeta("vidhi", "लोपो व्योर्वलि", ("sandhi:6.1",)),
    "6.1.67": SutraMeta("vidhi", "वेरपृक्तस्य", ("sandhi:6.1",)),
    "6.1.68": SutraMeta("vidhi", "हल्ङ्याब्भ्यो दीर्घात्‌ सुतिस्यपृक्तं हल्", ("sandhi:6.1",)),
    "6.1.69": SutraMeta("vidhi", "एङ्ह्रस्वात्‌ सम्बुद्धेः", ("sandhi:6.1",)),
    "6.1.70": SutraMeta("paribhasha", "शेश्छन्दसि बहुलम्", ("sandhi:6.1",)),
    "6.1.71": SutraMeta("vidhi", "ह्रस्वस्य पिति कृति तुक्", ("sandhi:6.1",)),
    "6.1.72": SutraMeta("vidhi", "संहितायाम्", ("sandhi:6.1",)),
    "6.1.73": SutraMeta("vidhi", "छे च", ("sandhi:6.1",)),
    "6.1.74": SutraMeta("vidhi", "आङ्माङोश्च", ("sandhi:6.1",)),
    "6.1.75": SutraMeta("vidhi", "दीर्घात्‌", ("sandhi:6.1",)),
    "6.1.76": SutraMeta("vibhasha", "पदान्ताद्वा", ("sandhi:6.1",)),
    "6.1.77": SutraMeta("vidhi", "इको यणचि", ("sandhi:6.1",)),
    "6.1.78": SutraMeta("vidhi", "एचोऽयवायावः", ("sandhi:6.1",)),
    "6.1.79": SutraMeta("vidhi", "वान्तो यि प्रत्यये", ("sandhi:6.1",)),
    "6.1.80": SutraMeta("vidhi", "धातोस्तन्निमित्तस्यैव", ("sandhi:6.1",)),
    "6.1.81": SutraMeta("vidhi", "क्षय्यजय्यौ शक्यार्थे", ("sandhi:6.1",)),
    "6.1.82": SutraMeta("vidhi", "क्रय्यस्तदर्थे", ("sandhi:6.1",)),
    "6.1.83": SutraMeta("vidhi", "भय्यप्रवय्ये च च्छन्दसि", ("sandhi:6.1",)),
    "6.1.84": SutraMeta("vidhi", "एकः पूर्वपरयोः", ("sandhi:6.1",)),
    "6.1.85": SutraMeta("vidhi", "अन्तादिवच्च", ("sandhi:6.1",)),
    "6.1.86": SutraMeta("vidhi", "षत्वतुकोरसिद्धः", ("sandhi:6.1",)),
    "6.1.87": SutraMeta("vidhi", "आद्गुणः", ("sandhi:6.1",)),
    "6.1.88": SutraMeta("vidhi", "वृद्धिरेचि", ("sandhi:6.1",)),
    "6.1.89": SutraMeta("vidhi", "एत्येधत्यूठ्सु", ("sandhi:6.1",)),
    "6.1.90": SutraMeta("vidhi", "आटश्च", ("sandhi:6.1",)),
    "6.1.91": SutraMeta("vidhi", "उपसर्गादृति धातौ", ("sandhi:6.1",)),
    "6.1.92": SutraMeta("vibhasha", "वा सुप्यापिशलेः", ("sandhi:6.1",)),
    "6.1.93": SutraMeta("vidhi", "औतोऽम्शसोः", ("sandhi:6.1",)),
    "6.1.94": SutraMeta("vidhi", "एङि पररूपम्", ("sandhi:6.1",)),
    "6.1.95": SutraMeta("vidhi", "ओमाङोश्च", ("sandhi:6.1",)),
    "6.1.96": SutraMeta("vidhi", "उस्यपदान्तात्‌", ("sandhi:6.1",)),
    "6.1.97": SutraMeta("vidhi", "अतो गुणे", ("sandhi:6.1",)),
    "6.1.98": SutraMeta("vidhi", "अव्यक्तानुकरणस्यात इतौ", ("sandhi:6.1",)),
    "6.1.99": SutraMeta("vibhasha", "नाम्रेडितस्यान्त्यस्य तु वा", ("sandhi:6.1",)),
    "6.1.100": SutraMeta("vidhi", "नित्यमाम्रेडिते डाचि", ("sandhi:6.1",)),
    "6.1.101": SutraMeta("vidhi", "अकः सवर्णे दीर्घः", ("sandhi:6.1",)),
    "6.1.102": SutraMeta("vidhi", "प्रथमयोः पूर्वसवर्णः", ("sandhi:6.1",)),
    "6.1.103": SutraMeta("vidhi", "तस्माच्छसो नः पुंसि", ("sandhi:6.1",)),
    "6.1.104": SutraMeta("pratisedha", "नादिचि", ("sandhi:6.1",)),
    "6.1.105": SutraMeta("vidhi", "दीर्घाज्जसि च", ("sandhi:6.1",)),
    "6.1.106": SutraMeta("vibhasha", "वा छन्दसि", ("sandhi:6.1",)),
    "6.1.107": SutraMeta("vidhi", "अमि पूर्वः", ("sandhi:6.1",)),
    "6.1.108": SutraMeta("vidhi", "सम्प्रसारणाच्च", ("sandhi:6.1",)),
    "6.1.109": SutraMeta("vidhi", "एङः पदान्तादति", ("sandhi:6.1",)),
    "6.1.110": SutraMeta("vidhi", "ङसिङसोश्च", ("sandhi:6.1",)),
    "6.1.111": SutraMeta("vidhi", "ऋत उत्‌", ("sandhi:6.1",)),
    "6.1.112": SutraMeta("vidhi", "ख्यत्यात्‌ परस्य", ("sandhi:6.1",)),
    "6.1.113": SutraMeta("vidhi", "अतो रोरप्लुतादप्लुते", ("sandhi:6.1",)),
    "6.1.114": SutraMeta("vidhi", "हशि च", ("sandhi:6.1",)),
    "6.1.115": SutraMeta("vidhi", "प्रकृत्याऽन्तःपादमव्यपरे", ("sandhi:6.1",)),
    "6.1.116": SutraMeta("vidhi", "अव्यादवद्यादवक्रमुरव्रतायमवन्त्ववस्युषु च", ("sandhi:6.1",)),
    "6.1.117": SutraMeta("vidhi", "यजुष्युरः", ("sandhi:6.1",)),
    "6.1.118": SutraMeta("vidhi", "आपोजुषाणोवृष्णोवर्षिष्ठेऽम्बेऽम्बालेऽम्बिकेपूर्वे", ("sandhi:6.1",)),
    "6.1.119": SutraMeta("vidhi", "अङ्ग इत्यादौ च", ("sandhi:6.1",)),
    "6.1.120": SutraMeta("vidhi", "अनुदात्ते च कुधपरे", ("sandhi:6.1",)),
    "6.1.121": SutraMeta("vidhi", "अवपथासि च", ("sandhi:6.1",)),
    "6.1.122": SutraMeta("vibhasha", "सर्वत्र विभाषा गोः", ("sandhi:6.1",)),
    "6.1.123": SutraMeta("vidhi", "अवङ् स्फोटायनस्य", ("sandhi:6.1",)),
    "6.1.124": SutraMeta("vidhi", "इन्द्रे च (नित्यम्)", ("sandhi:6.1",)),
    "6.1.125": SutraMeta("vidhi", "प्लुतप्रगृह्या अचि नित्यम्", ("sandhi:6.1",)),
    "6.1.126": SutraMeta("vidhi", "आङोऽनुनासिकश्छन्दसि", ("sandhi:6.1",)),
    "6.1.127": SutraMeta("vidhi", "इकोऽसवर्णे शाकल्यस्य ह्रस्वश्च", ("sandhi:6.1",)),
    "6.1.128": SutraMeta("vidhi", "ऋत्यकः", ("sandhi:6.1",)),
    "6.1.129": SutraMeta("vidhi", "अप्लुतवदुपस्थिते", ("sandhi:6.1",)),
    "6.1.130": SutraMeta("vidhi", "ई३ चाक्रवर्मणस्य", ("sandhi:6.1",)),
    "6.1.131": SutraMeta("vidhi", "दिव उत्‌", ("sandhi:6.1",)),
    "6.1.132": SutraMeta("vidhi", "एतत्तदोः सुलोपोऽकोरनञ्समासे हलि", ("sandhi:6.1",)),
    "6.1.133": SutraMeta("paribhasha", "स्यश्छन्दसि बहुलम्", ("sandhi:6.1",)),
    "6.1.134": SutraMeta("vidhi", "सोऽचि लोपे चेत्‌ पादपूरणम्", ("sandhi:6.1",)),
    "6.1.135": SutraMeta("vidhi", "सुट् कात्‌ पूर्वः", ("sandhi:6.1",)),
    "6.1.136": SutraMeta("vidhi", "अडभ्यासव्यवायेऽपि", ("sandhi:6.1",)),
    "6.1.137": SutraMeta("vidhi", "सम्पर्युपेभ्यः करोतौ भूषणे", ("sandhi:6.1",)),
    "6.1.138": SutraMeta("vidhi", "समवाये च", ("sandhi:6.1",)),
    "6.1.139": SutraMeta("vidhi", "उपात्‌ प्रतियत्नवैकृतवाक्याध्याहारेषु", ("sandhi:6.1",)),
    "6.1.140": SutraMeta("vidhi", "किरतौ लवने", ("sandhi:6.1",)),
    "6.1.141": SutraMeta("vidhi", "हिंसायां प्रतेश्च", ("sandhi:6.1",)),
    "6.1.142": SutraMeta("vidhi", "अपाच्चतुष्पाच्छकुनिष्वालेखने", ("sandhi:6.1",)),
    "6.1.143": SutraMeta("samjna", "कुस्तुम्बुरूणि जातिः", ("sandhi:6.1",)),
    "6.1.144": SutraMeta("vidhi", "अपरस्पराः क्रियासातत्ये", ("sandhi:6.1",)),
    "6.1.145": SutraMeta("vidhi", "गोष्पदं सेवितासेवितप्रमाणेषु", ("sandhi:6.1",)),
    "6.1.146": SutraMeta("vidhi", "आस्पदं प्रतिष्ठायाम्‌", ("sandhi:6.1",)),
    "6.1.147": SutraMeta("vidhi", "आश्चर्यमनित्ये", ("sandhi:6.1",)),
    "6.1.148": SutraMeta("vidhi", "वर्चस्केऽवस्करः", ("sandhi:6.1",)),
    "6.1.149": SutraMeta("vidhi", "अपस्करो रथाङ्गम्", ("sandhi:6.1",)),
    "6.1.150": SutraMeta("vibhasha", "विष्किरः शकुनिर्विकरो वा", ("sandhi:6.1",)),
    "6.1.151": SutraMeta("vidhi", "ह्रस्वाच्चन्द्रोत्तरपदे मन्त्रे", ("sandhi:6.1",)),
    "6.1.152": SutraMeta("vidhi", "प्रतिष्कशश्च कशेः", ("sandhi:6.1",)),
    "6.1.153": SutraMeta("samjna", "प्रस्कण्वहरिश्चन्द्रावृषी", ("sandhi:6.1",)),
    "6.1.154": SutraMeta("vidhi", "मस्करमस्करिणौ वेणुपरिव्राजकयोः", ("sandhi:6.1",)),
    "6.1.155": SutraMeta("vidhi", "कास्तीराजस्तुन्दे नगरे", ("sandhi:6.1",)),
    "6.1.156": SutraMeta("vidhi", "कारस्करो वृक्षः", ("sandhi:6.1",)),
    "6.1.157": SutraMeta("vidhi", "पारस्करप्रभृतीनि च संज्ञायाम्", ("sandhi:6.1",)),
    "6.1.158": SutraMeta("samjna", "अनुदात्तं पदमेकवर्जम्‌", ("sandhi:6.1",)),
    "6.1.159": SutraMeta("vidhi", "कर्षात्वतो घञोऽन्त उदात्तः", ("sandhi:6.1",)),
    "6.1.160": SutraMeta("vidhi", "उञ्छादीनां च", ("sandhi:6.1",)),
    "6.1.161": SutraMeta("vidhi", "अनुदात्तस्य च यत्रोदात्तलोपः", ("sandhi:6.1",)),
    "6.1.162": SutraMeta("vidhi", "धातोः", ("sandhi:6.1",)),
    "6.1.163": SutraMeta("vidhi", "चितः", ("sandhi:6.1",)),
    "6.1.164": SutraMeta("vidhi", "तद्धितस्य", ("sandhi:6.1",)),
    "6.1.165": SutraMeta("vidhi", "कितः", ("sandhi:6.1",)),
    "6.1.166": SutraMeta("vidhi", "तिसृभ्यो जसः", ("sandhi:6.1",)),
    "6.1.167": SutraMeta("vidhi", "चतुरः शसि", ("sandhi:6.1",)),
    "6.1.168": SutraMeta("samjna", "सावेकाचस्तृतीयाऽऽदिविभक्तिः", ("sandhi:6.1",)),
    "6.1.169": SutraMeta("vidhi", "अन्तोदत्तादुत्तरपदादन्यतरस्यामनित्यसमासे", ("sandhi:6.1",)),
    "6.1.170": SutraMeta("samjna", "अञ्चेश्छन्दस्यसर्वनामस्थानम्", ("sandhi:6.1",)),
    "6.1.171": SutraMeta("vidhi", "ऊडिदम्पदाद्यप्पुम्रैद्युभ्यः", ("sandhi:6.1",)),
    "6.1.172": SutraMeta("vidhi", "अष्टनो दीर्घात्‌", ("sandhi:6.1",)),
    "6.1.173": SutraMeta("vidhi", "शतुरनुमो नद्यजादी", ("sandhi:6.1",)),
    "6.1.174": SutraMeta("vidhi", "उदात्तयणो हल्पूर्वात्‌", ("sandhi:6.1",)),
    "6.1.175": SutraMeta("vidhi", "नोङ्धात्वोः", ("sandhi:6.1",)),
    "6.1.176": SutraMeta("vidhi", "ह्रस्वनुड्भ्यां मतुप्‌", ("sandhi:6.1",)),
    "6.1.177": SutraMeta("samjna", "नामन्यतरस्याम्‌", ("sandhi:6.1",)),
    "6.1.178": SutraMeta("paribhasha", "ङ्याश्छन्दसि बहुलम्", ("sandhi:6.1",)),
    "6.1.179": SutraMeta("vidhi", "षट्त्रिचतुर्भ्यो हलादिः", ("sandhi:6.1",)),
    "6.1.180": SutraMeta("vidhi", "झल्युपोत्तमम्", ("sandhi:6.1",)),
    "6.1.181": SutraMeta("vibhasha", "विभाषा भाषायाम्", ("sandhi:6.1",)),
    "6.1.182": SutraMeta("pratisedha", "न गोश्वन्त्साववर्णराडङ्क्रुङ्कृद्भ्यः", ("sandhi:6.1",)),
    "6.1.183": SutraMeta("vidhi", "दिवो झल्", ("sandhi:6.1",)),
    "6.1.184": SutraMeta("vidhi", "नृ चान्यतरस्याम्", ("sandhi:6.1",)),
    "6.1.185": SutraMeta("samjna", "तित्स्वरितम्", ("sandhi:6.1",)),
    "6.1.186": SutraMeta("vidhi", "तास्यनुदात्तेन्ङिददुपदेशाल्लसार्वधातुकमनुदात्तमहन्विङोः", ("sandhi:6.1",)),
    "6.1.187": SutraMeta("vidhi", "आदिः सिचोऽन्यतरस्याम्", ("sandhi:6.1",)),
    "6.1.188": SutraMeta("vidhi", "स्वपादिर्हिंसामच्यनिटि", ("sandhi:6.1",)),
    "6.1.189": SutraMeta("vidhi", "अभ्यस्तानामादिः", ("sandhi:6.1",)),
    "6.1.190": SutraMeta("vidhi", "अनुदात्ते च", ("sandhi:6.1",)),
    "6.1.191": SutraMeta("vidhi", "सर्वस्य सुपि", ("sandhi:6.1",)),
    "6.1.192": SutraMeta("vidhi", "भीह्रीभृहुमदजनधनदरिद्राजागरां प्रत्ययात् पूर्वम् पिति", ("sandhi:6.1",)),
    "6.1.193": SutraMeta("vidhi", "लिति", ("sandhi:6.1",)),
    "6.1.194": SutraMeta("vidhi", "आदिर्णमुल्यन्यतरस्याम्", ("sandhi:6.1",)),
    "6.1.195": SutraMeta("vidhi", "अचः कर्तृयकि", ("sandhi:6.1",)),
    "6.1.196": SutraMeta("vibhasha", "थलि च सेटीडन्तो वा", ("sandhi:6.1",)),
    "6.1.197": SutraMeta("vidhi", "ञ्णित्यादिर्नित्यम्", ("sandhi:6.1",)),
    "6.1.198": SutraMeta("vidhi", "आमन्त्रितस्य च", ("sandhi:6.1",)),
    "6.1.199": SutraMeta("vidhi", "पथिमथोः सर्वनामस्थाने", ("sandhi:6.1",)),
    "6.1.200": SutraMeta("vidhi", "अन्तश्च तवै युगपत्‌", ("sandhi:6.1",)),
    "6.1.201": SutraMeta("vidhi", "क्षयो निवासे", ("sandhi:6.1",)),
    "6.1.202": SutraMeta("samjna", "जयः करणम्", ("sandhi:6.1",)),
    "6.1.203": SutraMeta("vidhi", "वृषादीनां च", ("sandhi:6.1",)),
    "6.1.204": SutraMeta("samjna", "संज्ञायामुपमानम्‌", ("sandhi:6.1",)),
    "6.1.205": SutraMeta("vidhi", "निष्ठा च द्व्यजनात्‌", ("sandhi:6.1",)),
    "6.1.206": SutraMeta("vidhi", "शुष्कधृष्टौ", ("sandhi:6.1",)),
    "6.1.207": SutraMeta("samjna", "आशितः कर्ता", ("sandhi:6.1",)),
    "6.1.208": SutraMeta("vibhasha", "रिक्ते विभाषा", ("sandhi:6.1",)),
    "6.1.209": SutraMeta("vidhi", "जुष्टार्पिते च छन्दसि", ("sandhi:6.1",)),
    "6.1.210": SutraMeta("vidhi", "नित्यं मन्त्रे", ("sandhi:6.1",)),
    "6.1.211": SutraMeta("vidhi", "युष्मदस्मदोर्ङसि", ("sandhi:6.1",)),
    "6.1.212": SutraMeta("vidhi", "ङयि च", ("sandhi:6.1",)),
    "6.1.213": SutraMeta("vidhi", "यतोऽनावः", ("sandhi:6.1",)),
    "6.1.214": SutraMeta("vidhi", "ईडवन्दवृशंसदुहां ण्यतः", ("sandhi:6.1",)),
    "6.1.215": SutraMeta("vibhasha", "विभाषा वेण्विन्धानयोः", ("sandhi:6.1",)),
    "6.1.216": SutraMeta("vidhi", "त्यागरागहासकुहश्वठक्रथानाम्", ("sandhi:6.1",)),
    "6.1.217": SutraMeta("vidhi", "उपोत्तमं रिति", ("sandhi:6.1",)),
    "6.1.218": SutraMeta("vidhi", "चङ्यन्यतरस्याम्", ("sandhi:6.1",)),
    "6.1.219": SutraMeta("vidhi", "मतोः पूर्वमात्‌ संज्ञायां स्त्रियाम्‌", ("sandhi:6.1",)),
    "6.1.220": SutraMeta("vidhi", "अन्तोऽवत्याः", ("sandhi:6.1",)),
    "6.1.221": SutraMeta("vidhi", "ईवत्याः", ("sandhi:6.1",)),
    "6.1.222": SutraMeta("vidhi", "चौ", ("sandhi:6.1",)),
    "6.1.223": SutraMeta("vidhi", "समासस्य", ("sandhi:6.1",)),
}

(
    IMPLEMENTED_IDS,
    has_real_implementation,
    handler_for,
    positive_features,
    negative_features,
) = make_module_api(FIXTURES, globals())
