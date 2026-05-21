"""
Discrete Pāṇinian predicates for Adhyāya 7.1 (103 sūtras).

Hand-written per sūtra from data/ashtadhyayi_sutras.json. Domain: agama,
ending augments, and substitutions before tiṅ / vibhakti endings (7.1).
"""
from __future__ import annotations

from .anga import operations_for_range
from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api, _predicate_name

_VIDHI = "vidhi"
_PRATISEDHA = "pratisedha"
_VIBHASHA = "vibhasha"
_PARIBHASHA = "paribhasha"

_AYANE_ADI = frozenset({"āyana", "eyana", "īyana", "iya"})
_PHADAKHA = 'phaḍakha'
_ASHVAKSIRA = frozenset(['aśva', 'kṣīra', 'lavaṇa', 'vṛṣa'])
_SNATVYADI = frozenset(['snā', 'tvā', 'ādya'])
_TAPTANAPTA = frozenset(['napta', 'natha', 'nā', 'tapta'])
_RDUSHANA = frozenset(['anehas', 'purudaṃsa', 'śanas', 'ṛdu'])
_DRIKSVAVAS = frozenset(['dṛk', 'svatavas', 'svavas'])
_PATHIMATHY = frozenset(['kṣāma', 'mathi', 'pathi', 'ṛbhu'])


def _num_op_available(c) -> bool:
    """True when the 7.1 num-augment operation is in scope."""
    return any(op.name == "num-augment" for op in operations_for_range(str(c.get("range", ""))))


def sutra_7_1_1(c) -> bool:
    """yu/vo take special treatment before an/āk endings."""
    return _eq(c, "range", "7.1") and _in(c, "stem_final", {"yu", "vo"}) and _in(c, "ending", {"an", "āk"})


def sutra_7_1_2(c) -> bool:
    """āyana/eyana/īyana/iya before phaḍakha-class pratyayas."""
    return _eq(c, "range", "7.1") and _in(c, "stem_class", _AYANE_ADI) and _eq(c, "suffix_class", _PHADAKHA)


def sutra_7_1_3(c) -> bool:
    """jha-class ending gets anta augment."""
    return _eq(c, "range", "7.1") and _eq(c, "ending_class", "jha") and _eq(c, "augment", "anta")


def sutra_7_1_4(c) -> bool:
    """t augment after reduplicated (abhyasta) stem."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_class", "abhyasta") and _eq(c, "augment", "t")


def sutra_7_1_5(c) -> bool:
    """t augment blocked in ātmanepada."""
    return _eq(c, "range", "7.1") and _eq(c, "paradigm", "atmanepada") and _eq(c, "augment", "t") and _eq(c, "rule_blocked", True)


def sutra_7_1_6(c) -> bool:
    """śī root takes rut augment."""
    return _eq(c, "range", "7.1") and _eq(c, "dhatu_lemma", "śī") and _eq(c, "augment", "rut")


def sutra_7_1_7(c) -> bool:
    """optional agama for vettṛ."""
    return _eq(c, "range", "7.1") and _eq(c, "dhatu_lemma", "vettṛ") and bool(c.get("optional"))


def sutra_7_1_8(c) -> bool:
    """bahula augment rules in chandas."""
    return _eq(c, "range", "7.1") and _eq(c, "domain", "chandas") and _eq(c, "rule_strength", "bahula")


def sutra_7_1_9(c) -> bool:
    """bhis ending becomes ais."""
    return _eq(c, "range", "7.1") and _eq(c, "ending", "bhis") and _eq(c, "substitute", "ais")


def sutra_7_1_10(c) -> bool:
    """bahula in chandas (continued domain)."""
    return _eq(c, "range", "7.1") and _eq(c, "domain", "chandas") and _eq(c, "rule_strength", "bahula") and _eq(c, "section", "7.1.10")


def sutra_7_1_11(c) -> bool:
    """not for idam/adas before ak endings."""
    return _eq(c, "range", "7.1") and _in(c, "stem", {"idam", "adas"}) and _eq(c, "ending", "ak") and _eq(c, "rule_blocked", True)


def sutra_7_1_12(c) -> bool:
    """ṭāṅsiṅasām get inātsyāḥ substitution."""
    return _eq(c, "range", "7.1") and _eq(c, "suffix_marker", "ṭāṅ") and _eq(c, "substitute", "inātsyāḥ")


def sutra_7_1_13(c) -> bool:
    """ṅi marker becomes ya."""
    return _eq(c, "range", "7.1") and _eq(c, "suffix_marker", "ṅi") and _eq(c, "substitute", "ya")


def sutra_7_1_14(c) -> bool:
    """sarvanāma stem before smai ending."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_class", "sarvanāma") and _eq(c, "ending", "smai")


def sutra_7_1_15(c) -> bool:
    """ṅasiṅ endings become smāt/sminau."""
    return _eq(c, "range", "7.1") and _in(c, "suffix_marker", {"ṅasi", "ṅi"}) and _in(c, "substitute", {"smāt", "sminau"})


def sutra_7_1_16(c) -> bool:
    """optional rule for pūrvādi through ninth (navabhyaḥ)."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_class", "pūrvādi") and bool(c.get("optional"))


def sutra_7_1_17(c) -> bool:
    """jas ending becomes śī."""
    return _eq(c, "range", "7.1") and _eq(c, "ending", "jas") and _eq(c, "substitute", "śī")


def sutra_7_1_18(c) -> bool:
    """auṅ (aṅ) becomes āpaḥ."""
    return _eq(c, "range", "7.1") and _eq(c, "suffix_marker", "auṅ") and _eq(c, "substitute", "āpaḥ")


def sutra_7_1_19(c) -> bool:
    """also applies to neuter (napuṃsaka)."""
    return _eq(c, "range", "7.1") and _eq(c, "gender", "napuṃsaka") and _eq(c, "also", True)


def sutra_7_1_20(c) -> bool:
    """jaś/śas endings become śi."""
    return _eq(c, "range", "7.1") and _in(c, "ending", {"jaś", "śas"}) and _eq(c, "substitute", "śi")


def sutra_7_1_21(c) -> bool:
    """aṣṭan stems take auś substitute."""
    return _eq(c, "range", "7.1") and _eq(c, "stem", "aṣṭan") and _eq(c, "substitute", "auś")


def sutra_7_1_22(c) -> bool:
    """ṣaḍ stems take luk (zero) substitute."""
    return _eq(c, "range", "7.1") and _eq(c, "stem", "ṣaḍ") and _eq(c, "operation", "lopa")


def sutra_7_1_23(c) -> bool:
    """svamor from neuter stems."""
    return _eq(c, "range", "7.1") and _eq(c, "ending", "svamor") and _eq(c, "gender", "napuṃsaka")


def sutra_7_1_24(c) -> bool:
    """after a, substitute am."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_final", "a") and _eq(c, "substitute", "am")


def sutra_7_1_25(c) -> bool:
    """aḍ after ḍatarādi and five stems."""
    return _eq(c, "range", "7.1") and _eq(c, "augment", "aḍ") and _in(c, "stem_class", {"ḍatarādi", "pañcama"})


def sutra_7_1_26(c) -> bool:
    """not from other (itarāt) in chandas."""
    return _eq(c, "range", "7.1") and _eq(c, "domain", "chandas") and _eq(c, "source", "itarāt") and _eq(c, "rule_blocked", True)


def sutra_7_1_27(c) -> bool:
    """yuṣmad/asmad before ṅas → aś."""
    return _eq(c, "range", "7.1") and _in(c, "stem", {"yuṣmad", "asmad"}) and _eq(c, "ending", "ṅas") and _eq(c, "substitute", "aś")


def sutra_7_1_28(c) -> bool:
    """ṅi in first two persons → am."""
    return _eq(c, "range", "7.1") and _eq(c, "suffix_marker", "ṅi") and _eq(c, "person", "prathama_dvitīya") and _eq(c, "substitute", "am")


def sutra_7_1_29(c) -> bool:
    """śas ending does not take preceding rule."""
    return _eq(c, "range", "7.1") and _eq(c, "ending", "śas") and _eq(c, "rule_blocked", True)


def sutra_7_1_30(c) -> bool:
    """bhyas ending becomes bhym."""
    return _eq(c, "range", "7.1") and _eq(c, "ending", "bhyas") and _eq(c, "substitute", "bhym")


def sutra_7_1_31(c) -> bool:
    """pañcamī (ablative) ending gets at augment."""
    return _eq(c, "range", "7.1") and _eq(c, "vibhakti", "pañcamī") and _eq(c, "augment", "at")


def sutra_7_1_32(c) -> bool:
    """also in singular (ekavacana)."""
    return _eq(c, "range", "7.1") and _eq(c, "number", "ekavacana") and _eq(c, "also", True)


def sutra_7_1_33(c) -> bool:
    """sām stem takes ākam substitute."""
    return _eq(c, "range", "7.1") and _eq(c, "stem", "sām") and _eq(c, "substitute", "ākam")


def sutra_7_1_34(c) -> bool:
    """long ā before au from ṇal (num) augment."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_final", "ā") and _eq(c, "suffix_marker", "ṇal") and _eq(c, "substitute", "au") and _num_op_available(c)


def sutra_7_1_35(c) -> bool:
    """tu-/hy- stems: tātaṅ in āśī (blessing), optional."""
    return _eq(c, "range", "7.1") and _in(c, "stem", {"tu", "hi"}) and _eq(c, "semantic", "āśī") and bool(c.get("optional"))


def sutra_7_1_36(c) -> bool:
    """vid stem: śatuḥ becomes vasuḥ."""
    return _eq(c, "range", "7.1") and _eq(c, "stem", "vid") and _eq(c, "ending", "śatuḥ") and _eq(c, "substitute", "vasuḥ")


def sutra_7_1_37(c) -> bool:
    """in samāsa after anañ, ktva → lyap."""
    return _eq(c, "range", "7.1") and _eq(c, "compound_type", "samāsa") and _eq(c, "condition", "anañpūrva") and _eq(c, "suffix", "ktva") and _eq(c, "substitute", "lyap")


def sutra_7_1_38(c) -> bool:
    """ktvā also (api) in chandas."""
    return _eq(c, "range", "7.1") and _eq(c, "suffix", "ktvā") and _eq(c, "domain", "chandas") and _eq(c, "also", True)


def sutra_7_1_39(c) -> bool:
    """sup endings: suluk, savarṇa, ācch-etc. pratyāhāra domain."""
    return _eq(c, "range", "7.1") and _eq(c, "suffix_class", "sup") and _eq(c, "domain", "suluk_savarṇa_ācch")


def sutra_7_1_40(c) -> bool:
    """am ending becomes maś."""
    return _eq(c, "range", "7.1") and _eq(c, "ending", "am") and _eq(c, "substitute", "maś")


def sutra_7_1_41(c) -> bool:
    """lopa of taḥ in ātmanepada."""
    return _eq(c, "range", "7.1") and _eq(c, "operation", "lopa") and _eq(c, "target", "taḥ") and _eq(c, "paradigm", "atmanepada")


def sutra_7_1_42(c) -> bool:
    """dhvam becomes dhvāt."""
    return _eq(c, "range", "7.1") and _eq(c, "ending", "dhvam") and _eq(c, "substitute", "dhvāt")


def sutra_7_1_43(c) -> bool:
    """yajadhvainam form also (iti)."""
    return _eq(c, "range", "7.1") and _eq(c, "form", "yajadhvainam") and _eq(c, "also", True)


def sutra_7_1_44(c) -> bool:
    """tasya becomes tāt (genitive relation)."""
    return _eq(c, "range", "7.1") and _eq(c, "ending", "tasya") and _eq(c, "substitute", "tāt")


def sutra_7_1_45(c) -> bool:
    """tapta/napta/natha/nā stems listed."""
    return _eq(c, "range", "7.1") and _in(c, "stem", _TAPTANAPTA) and _eq(c, "also", True)


def sutra_7_1_46(c) -> bool:
    """idanta before mas ending."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_class", "idanta") and _eq(c, "ending", "mas")


def sutra_7_1_47(c) -> bool:
    """ktva suffix becomes yak."""
    return _eq(c, "range", "7.1") and _eq(c, "suffix", "ktva") and _eq(c, "substitute", "yak")


def sutra_7_1_48(c) -> bool:
    """iṣṭvīnam form also."""
    return _eq(c, "range", "7.1") and _eq(c, "form", "iṣṭvīnam") and _eq(c, "also", True)


def sutra_7_1_49(c) -> bool:
    """snātvyādi roots/forms also."""
    return _eq(c, "range", "7.1") and _in(c, "stem", _SNATVYADI) and _eq(c, "also", True)


def sutra_7_1_50(c) -> bool:
    """ā before jas: asuk augment."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_final", "ā") and _eq(c, "ending", "jas") and _eq(c, "augment", "asuk")


def sutra_7_1_51(c) -> bool:
    """aśva/kṣīra/vṛṣa/lavaṇa in ātmaprīti with kyac."""
    return _eq(c, "range", "7.1") and _in(c, "stem", _ASHVAKSIRA) and _eq(c, "semantic", "ātmaprīti") and _eq(c, "suffix_marker", "kyac")


def sutra_7_1_52(c) -> bool:
    """sarvanāma before āmi: suṭ augment."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_class", "sarvanāma") and _eq(c, "suffix", "āmi") and _eq(c, "augment", "suṭ")


def sutra_7_1_53(c) -> bool:
    """tri stem: trayas substitute."""
    return _eq(c, "range", "7.1") and _eq(c, "stem", "tri") and _eq(c, "substitute", "trayaḥ")


def sutra_7_1_54(c) -> bool:
    """hrasva river/water nouns take nuṭ (num) augment."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_class", "hrasvanadyāp") and _eq(c, "augment", "nuṭ") and _num_op_available(c)


def sutra_7_1_55(c) -> bool:
    """also after ṣaṭ and catur."""
    return _eq(c, "range", "7.1") and _in(c, "stem", {"ṣaṭ", "catur"}) and _eq(c, "also", True)


def sutra_7_1_56(c) -> bool:
    """śrī/grāmaṇī in chandas."""
    return _eq(c, "range", "7.1") and _in(c, "stem", {"śrī", "grāmaṇī"}) and _eq(c, "domain", "chandas")


def sutra_7_1_57(c) -> bool:
    """go at end of pāda (pādānte)."""
    return _eq(c, "range", "7.1") and _eq(c, "stem", "go") and _eq(c, "position", "pādānte")


def sutra_7_1_58(c) -> bool:
    """idit roots take num augment before dhātu."""
    return _eq(c, "range", "7.1") and _eq(c, "marker", "idit") and _eq(c, "augment", "num") and _eq(c, "applies_to", "dhātu") and _num_op_available(c)


def sutra_7_1_59(c) -> bool:
    """śe (imperative) for muc-ādi roots."""
    return _eq(c, "range", "7.1") and _eq(c, "lakara", "lot") and _eq(c, "stem_class", "mucādi") and _eq(c, "ending", "śe")


def sutra_7_1_60(c) -> bool:
    """mas/jina/śa before jhali ending."""
    return _eq(c, "range", "7.1") and _in(c, "stem", {"mas", "jina", "śa"}) and _eq(c, "ending_class", "jhali")


def sutra_7_1_61(c) -> bool:
    """radhi/jabha before ac (vowel) ending."""
    return _eq(c, "range", "7.1") and _in(c, "dhatu_lemma", {"radhi", "jabha"}) and _eq(c, "following", "ac")


def sutra_7_1_62(c) -> bool:
    """no iṭ in a+liṭ for radh."""
    return _eq(c, "range", "7.1") and _eq(c, "dhatu_lemma", "radh") and _eq(c, "lakara", "liṭ") and _eq(c, "augment", "iṭ") and _eq(c, "rule_blocked", True)


def sutra_7_1_63(c) -> bool:
    """rabh before aśabliṭ endings."""
    return _eq(c, "range", "7.1") and _eq(c, "dhatu_lemma", "rabh") and _eq(c, "suffix_class", "aśabliṭ")


def sutra_7_1_64(c) -> bool:
    """also for labh root."""
    return _eq(c, "range", "7.1") and _eq(c, "dhatu_lemma", "labh") and _eq(c, "also", True)


def sutra_7_1_65(c) -> bool:
    """āṅ prefix before yi (yak) suffix."""
    return _eq(c, "range", "7.1") and _eq(c, "prefix", "āṅ") and _eq(c, "suffix_marker", "yi")


def sutra_7_1_66(c) -> bool:
    """upa before praise (praśaṃsā) sense."""
    return _eq(c, "range", "7.1") and _eq(c, "prefix", "upa") and _eq(c, "semantic", "praśaṃsā")


def sutra_7_1_67(c) -> bool:
    """upasarga before khal/ghañ suffixes."""
    return _eq(c, "range", "7.1") and bool(c.get("has_upasarga")) and _in(c, "suffix_marker", {"khal", "ghañ"})


def sutra_7_1_68(c) -> bool:
    """not for su/dur alone (kevala)."""
    return _eq(c, "range", "7.1") and _in(c, "prefix", {"su", "dur"}) and bool(c.get("kevala")) and _eq(c, "rule_blocked", True)


def sutra_7_1_69(c) -> bool:
    """optional for ciṇ and ṇamul."""
    return _eq(c, "range", "7.1") and _in(c, "suffix_marker", {"ciṇ", "ṇamul"}) and bool(c.get("optional"))


def sutra_7_1_70(c) -> bool:
    """ugit/ac before sarvanāmasthāna, not dhātu."""
    return _eq(c, "range", "7.1") and _in(c, "marker", {"ugit", "ac"}) and _eq(c, "domain", "sarvanāmasthāna") and not _eq(c, "applies_to", "dhātu")


def sutra_7_1_71(c) -> bool:
    """yuj not in samāsa."""
    return _eq(c, "range", "7.1") and _eq(c, "dhatu_lemma", "yuj") and _eq(c, "compound_type", "samāsa") and _eq(c, "rule_blocked", True)


def sutra_7_1_72(c) -> bool:
    """neuter jhalac ending treatment."""
    return _eq(c, "range", "7.1") and _eq(c, "gender", "napuṃsaka") and _eq(c, "ending_class", "jhalac")


def sutra_7_1_73(c) -> bool:
    """ik before ac in vibhakti."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_final_class", "ik") and _eq(c, "following", "ac") and _eq(c, "domain", "vibhakti")


def sutra_7_1_74(c) -> bool:
    """tṛtīyādi: masculine-like for spoken-neuter (Gālava)."""
    return _eq(c, "range", "7.1") and _eq(c, "vibhakti", "tṛtīyādi") and _eq(c, "semantic", "bhāṣitapuṃska") and _eq(c, "authority", "gālava")


def sutra_7_1_75(c) -> bool:
    """asthi/dadhi/sakthi/akṣṇām: anṅ with udātta."""
    return _eq(c, "range", "7.1") and _in(c, "stem", {"asthi", "dadhi", "sakthi", "akṣṇām"}) and _eq(c, "augment", "anṅ") and _eq(c, "accent", "udātta")


def sutra_7_1_76(c) -> bool:
    """also seen in chandas."""
    return _eq(c, "range", "7.1") and _eq(c, "domain", "chandas") and _eq(c, "also", True)


def sutra_7_1_77(c) -> bool:
    """ī also in dual (dvivacana)."""
    return _eq(c, "range", "7.1") and _eq(c, "substitute", "ī") and _eq(c, "number", "dvivacana") and _eq(c, "also", True)


def sutra_7_1_78(c) -> bool:
    """not śatuḥ after abhyasta."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_class", "abhyasta") and _eq(c, "ending", "śatuḥ") and _eq(c, "rule_blocked", True)


def sutra_7_1_79(c) -> bool:
    """optional for neuter."""
    return _eq(c, "range", "7.1") and _eq(c, "gender", "napuṃsaka") and bool(c.get("optional"))


def sutra_7_1_80(c) -> bool:
    """ā before śī/nadī: num augment."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_final", "ā") and _in(c, "stem_class", {"śī", "nadī"}) and _eq(c, "augment", "num") and _num_op_available(c)


def sutra_7_1_81(c) -> bool:
    """śap/śyan: nitya (obligatory) augment."""
    return _eq(c, "range", "7.1") and _in(c, "suffix_marker", {"śap", "śyan"}) and _eq(c, "rule_strength", "nitya")


def sutra_7_1_82(c) -> bool:
    """sau before avan-aḍuh (go/do compound)."""
    return _eq(c, "range", "7.1") and _eq(c, "augment", "sau") and _eq(c, "stem_class", "avan-aḍuh")


def sutra_7_1_83(c) -> bool:
    """dṛk/svavas/svatavas in chandas."""
    return _eq(c, "range", "7.1") and _in(c, "stem", _DRIKSVAVAS) and _eq(c, "domain", "chandas")


def sutra_7_1_84(c) -> bool:
    """div stem: aut substitute."""
    return _eq(c, "range", "7.1") and _eq(c, "stem", "div") and _eq(c, "substitute", "aut")


def sutra_7_1_85(c) -> bool:
    """pathi/mathi/ṛbhu/kṣāma take āt augment."""
    return _eq(c, "range", "7.1") and _in(c, "stem", _PATHIMATHY) and _eq(c, "augment", "āt")


def sutra_7_1_86(c) -> bool:
    """i before at in sarvanāmasthāna."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_final", "i") and _eq(c, "substitute", "at") and _eq(c, "domain", "sarvanāmasthāna")


def sutra_7_1_87(c) -> bool:
    """tha becomes ntha."""
    return _eq(c, "range", "7.1") and _eq(c, "ending", "tha") and _eq(c, "substitute", "ntha")


def sutra_7_1_88(c) -> bool:
    """lopa of ṭa after bhās (bhāṣa)."""
    return _eq(c, "range", "7.1") and _eq(c, "stem", "bhās") and _eq(c, "operation", "lopa") and _eq(c, "target", "ṭa")


def sutra_7_1_89(c) -> bool:
    """puṃs stem: asuṅ augment."""
    return _eq(c, "range", "7.1") and _eq(c, "stem", "puṃs") and _eq(c, "augment", "asuṅ")


def sutra_7_1_90(c) -> bool:
    """go stem: ṇit augment."""
    return _eq(c, "range", "7.1") and _eq(c, "stem", "go") and _eq(c, "augment", "ṇit")


def sutra_7_1_91(c) -> bool:
    """ṇal augment is uttama or optional."""
    return _eq(c, "range", "7.1") and _eq(c, "suffix_marker", "ṇal") and bool(c.get("optional")) or _eq(c, "position", "uttama")


def sutra_7_1_92(c) -> bool:
    """sakhi stem not in sambuddha."""
    return _eq(c, "range", "7.1") and _eq(c, "stem", "sakhi") and not _eq(c, "domain", "sambuddha")


def sutra_7_1_93(c) -> bool:
    """anṅ before sau (savarna?)."""
    return _eq(c, "range", "7.1") and _eq(c, "augment", "anṅ") and _eq(c, "following", "sau")


def sutra_7_1_94(c) -> bool:
    """ṛdu/śanas/purudaṃsa/anehas: anṅ augment."""
    return _eq(c, "range", "7.1") and _in(c, "stem", _RDUSHANA) and _eq(c, "augment", "anṅ")


def sutra_7_1_95(c) -> bool:
    """tṛjvat for kroṣṭu stem."""
    return _eq(c, "range", "7.1") and _eq(c, "stem", "kroṣṭu") and _eq(c, "form", "tṛjvat")


def sutra_7_1_96(c) -> bool:
    """also in feminine (strī)."""
    return _eq(c, "range", "7.1") and _eq(c, "gender", "strī") and _eq(c, "also", True)


def sutra_7_1_97(c) -> bool:
    """optional ik before ac in tṛtīyādi."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_final_class", "ik") and _eq(c, "following", "ac") and _eq(c, "vibhakti", "tṛtīyādi") and bool(c.get("optional"))


def sutra_7_1_98(c) -> bool:
    """catur/an-aḍuh: ām with udātta."""
    return _eq(c, "range", "7.1") and _in(c, "stem", {"catur", "an-aḍuh"}) and _eq(c, "substitute", "ām") and _eq(c, "accent", "udātta")


def sutra_7_1_99(c) -> bool:
    """am augment in sambuddha (vocative)."""
    return _eq(c, "range", "7.1") and _eq(c, "augment", "am") and _eq(c, "domain", "sambuddha")


def sutra_7_1_100(c) -> bool:
    """ṝ before it of dhātu."""
    return _eq(c, "range", "7.1") and _eq(c, "stem_final", "ṝ") and _eq(c, "following", "it") and _eq(c, "applies_to", "dhātu")


def sutra_7_1_101(c) -> bool:
    """also after upadhā (penultimate)."""
    return _eq(c, "range", "7.1") and bool(c.get("has_upadhā")) and _eq(c, "also", True)


def sutra_7_1_102(c) -> bool:
    """ut augment before labial (oṣṭhya)."""
    return _eq(c, "range", "7.1") and _eq(c, "augment", "ut") and _eq(c, "condition", "oṣṭhyapūrva")


def sutra_7_1_103(c) -> bool:
    """bahula augment rules in chandas (closing)."""
    return _eq(c, "range", "7.1") and _eq(c, "domain", "chandas") and _eq(c, "rule_strength", "bahula") and _eq(c, "section", "7.1.103")


FIXTURES: dict[str, tuple[dict, dict]] = {
    "7.1.1": ({'range': '7.1', 'stem_final': 'yu', 'ending': 'an', 'operation': 'agama'}, {'range': '7.1', 'stem_final': 'yu', 'ending': 'ām', 'operation': 'agama'}),
    "7.1.2": ({'range': '7.1', 'stem_class': 'āyana', 'suffix_class': 'phaḍakha', 'operation': 'agama'}, {'range': '7.1', 'stem_class': 'ordinary', 'suffix_class': 'phaḍakha', 'operation': 'agama'}),
    "7.1.3": ({'range': '7.1', 'ending_class': 'jha', 'augment': 'anta', 'operation': 'agama'}, {'range': '7.1', 'ending_class': 'jhali', 'augment': 'anta', 'operation': 'agama'}),
    "7.1.4": ({'range': '7.1', 'stem_class': 'abhyasta', 'augment': 't', 'operation': 'agama'}, {'range': '7.1', 'stem_class': 'abhyasta', 'augment': 'num', 'operation': 'agama'}),
    "7.1.5": ({'range': '7.1', 'paradigm': 'atmanepada', 'augment': 't', 'rule_blocked': True}, {'range': '7.1', 'paradigm': 'parasmaipada', 'augment': 't', 'rule_blocked': True}),
    "7.1.6": ({'range': '7.1', 'dhatu_lemma': 'śī', 'augment': 'rut', 'operation': 'agama'}, {'range': '7.1', 'dhatu_lemma': 'śī', 'augment': 'num', 'operation': 'agama'}),
    "7.1.7": ({'range': '7.1', 'dhatu_lemma': 'vettṛ', 'optional': True, 'operation': 'agama'}, {'range': '7.1', 'dhatu_lemma': 'vettṛ', 'optional': False, 'operation': 'agama'}),
    "7.1.8": ({'range': '7.1', 'domain': 'chandas', 'rule_strength': 'bahula'}, {'range': '7.1', 'domain': 'loka', 'rule_strength': 'bahula'}),
    "7.1.9": ({'range': '7.1', 'ending': 'bhis', 'substitute': 'ais', 'operation': 'substitution'}, {'range': '7.1', 'ending': 'bhi', 'substitute': 'ais', 'operation': 'substitution'}),
    "7.1.10": ({'range': '7.1', 'domain': 'chandas', 'rule_strength': 'bahula', 'section': '7.1.10'}, {'range': '7.1', 'domain': 'chandas', 'rule_strength': 'nitya', 'section': '7.1.10'}),
    "7.1.11": ({'range': '7.1', 'stem': 'idam', 'ending': 'ak', 'rule_blocked': True}, {'range': '7.1', 'stem': 'idam', 'ending': 'am', 'rule_blocked': True}),
    "7.1.12": ({'range': '7.1', 'suffix_marker': 'ṭāṅ', 'substitute': 'inātsyāḥ', 'operation': 'substitution'}, {'range': '7.1', 'suffix_marker': 'siṅ', 'substitute': 'inātsyāḥ', 'operation': 'substitution'}),
    "7.1.13": ({'range': '7.1', 'suffix_marker': 'ṅi', 'substitute': 'ya', 'operation': 'substitution'}, {'range': '7.1', 'suffix_marker': 'ṅī', 'substitute': 'ya', 'operation': 'substitution'}),
    "7.1.14": ({'range': '7.1', 'stem_class': 'sarvanāma', 'ending': 'smai', 'operation': 'agama'}, {'range': '7.1', 'stem_class': 'pratipadika', 'ending': 'smai', 'operation': 'agama'}),
    "7.1.15": ({'range': '7.1', 'suffix_marker': 'ṅasi', 'substitute': 'smāt', 'operation': 'substitution'}, {'range': '7.1', 'suffix_marker': 'ṅasi', 'substitute': 'jas', 'operation': 'substitution'}),
    "7.1.16": ({'range': '7.1', 'stem_class': 'pūrvādi', 'optional': True, 'operation': 'agama'}, {'range': '7.1', 'stem_class': 'pūrvādi', 'optional': False, 'operation': 'agama'}),
    "7.1.17": ({'range': '7.1', 'ending': 'jas', 'substitute': 'śī', 'operation': 'substitution'}, {'range': '7.1', 'ending': 'jasi', 'substitute': 'śī', 'operation': 'substitution'}),
    "7.1.18": ({'range': '7.1', 'suffix_marker': 'auṅ', 'substitute': 'āpaḥ', 'operation': 'substitution'}, {'range': '7.1', 'suffix_marker': 'aṅ', 'substitute': 'āpaḥ', 'operation': 'substitution'}),
    "7.1.19": ({'range': '7.1', 'gender': 'napuṃsaka', 'also': True, 'operation': 'agama'}, {'range': '7.1', 'gender': 'puṃ', 'also': True, 'operation': 'agama'}),
    "7.1.20": ({'range': '7.1', 'ending': 'jaś', 'substitute': 'śi', 'operation': 'substitution'}, {'range': '7.1', 'ending': 'jaś', 'substitute': 'jas', 'operation': 'substitution'}),
    "7.1.21": ({'range': '7.1', 'stem': 'aṣṭan', 'substitute': 'auś', 'operation': 'substitution'}, {'range': '7.1', 'stem': 'saptan', 'substitute': 'auś', 'operation': 'substitution'}),
    "7.1.22": ({'range': '7.1', 'stem': 'ṣaḍ', 'operation': 'lopa'}, {'range': '7.1', 'stem': 'ṣaṭ', 'operation': 'lopa'}),
    "7.1.23": ({'range': '7.1', 'ending': 'svamor', 'gender': 'napuṃsaka', 'operation': 'agama'}, {'range': '7.1', 'ending': 'svamor', 'gender': 'strī', 'operation': 'agama'}),
    "7.1.24": ({'range': '7.1', 'stem_final': 'a', 'substitute': 'am', 'operation': 'substitution'}, {'range': '7.1', 'stem_final': 'ā', 'substitute': 'am', 'operation': 'substitution'}),
    "7.1.25": ({'range': '7.1', 'augment': 'aḍ', 'stem_class': 'ḍatarādi', 'operation': 'agama'}, {'range': '7.1', 'augment': 'aḍ', 'stem_class': 'ordinary', 'operation': 'agama'}),
    "7.1.26": ({'range': '7.1', 'domain': 'chandas', 'source': 'itarāt', 'rule_blocked': True}, {'range': '7.1', 'domain': 'loka', 'source': 'itarāt', 'rule_blocked': True}),
    "7.1.27": ({'range': '7.1', 'stem': 'yuṣmad', 'ending': 'ṅas', 'substitute': 'aś', 'operation': 'substitution'}, {'range': '7.1', 'stem': 'yuṣmad', 'ending': 'ṅas', 'substitute': 'jas', 'operation': 'substitution'}),
    "7.1.28": ({'range': '7.1', 'suffix_marker': 'ṅi', 'person': 'prathama_dvitīya', 'substitute': 'am', 'operation': 'substitution'}, {'range': '7.1', 'suffix_marker': 'ṅi', 'person': 'trtīya', 'substitute': 'am', 'operation': 'substitution'}),
    "7.1.29": ({'range': '7.1', 'ending': 'śas', 'rule_blocked': True}, {'range': '7.1', 'ending': 'śasi', 'rule_blocked': True}),
    "7.1.30": ({'range': '7.1', 'ending': 'bhyas', 'substitute': 'bhym', 'operation': 'substitution'}, {'range': '7.1', 'ending': 'bhyām', 'substitute': 'bhym', 'operation': 'substitution'}),
    "7.1.31": ({'range': '7.1', 'vibhakti': 'pañcamī', 'augment': 'at', 'operation': 'agama'}, {'range': '7.1', 'vibhakti': 'ṣaṣṭhī', 'augment': 'at', 'operation': 'agama'}),
    "7.1.32": ({'range': '7.1', 'number': 'ekavacana', 'also': True, 'operation': 'agama'}, {'range': '7.1', 'number': 'dvivacana', 'also': True, 'operation': 'agama'}),
    "7.1.33": ({'range': '7.1', 'stem': 'sām', 'substitute': 'ākam', 'operation': 'substitution'}, {'range': '7.1', 'stem': 'sāman', 'substitute': 'ākam', 'operation': 'substitution'}),
    "7.1.34": ({'range': '7.1', 'stem_final': 'ā', 'suffix_marker': 'ṇal', 'substitute': 'au', 'operation': 'augment'}, {'range': '7.1', 'stem_final': 'a', 'suffix_marker': 'ṇal', 'substitute': 'au', 'operation': 'augment'}),
    "7.1.35": ({'range': '7.1', 'stem': 'tu', 'semantic': 'āśī', 'optional': True, 'augment': 'tātaṅ'}, {'range': '7.1', 'stem': 'tu', 'semantic': 'karma', 'optional': True, 'augment': 'tātaṅ'}),
    "7.1.36": ({'range': '7.1', 'stem': 'vid', 'ending': 'śatuḥ', 'substitute': 'vasuḥ', 'operation': 'substitution'}, {'range': '7.1', 'stem': 'vid', 'ending': 'śatru', 'substitute': 'vasuḥ', 'operation': 'substitution'}),
    "7.1.37": ({'range': '7.1', 'compound_type': 'samāsa', 'condition': 'anañpūrva', 'suffix': 'ktva', 'substitute': 'lyap', 'operation': 'substitution'}, {'range': '7.1', 'compound_type': 'samāsa', 'condition': 'anañpūrva', 'suffix': 'ktvā', 'substitute': 'lyap', 'operation': 'substitution'}),
    "7.1.38": ({'range': '7.1', 'suffix': 'ktvā', 'domain': 'chandas', 'also': True, 'operation': 'agama'}, {'range': '7.1', 'suffix': 'ktvā', 'domain': 'loka', 'also': True, 'operation': 'agama'}),
    "7.1.39": ({'range': '7.1', 'suffix_class': 'sup', 'domain': 'suluk_savarṇa_ācch', 'operation': 'agama'}, {'range': '7.1', 'suffix_class': 'tiṅ', 'domain': 'suluk_savarṇa_ācch', 'operation': 'agama'}),
    "7.1.40": ({'range': '7.1', 'ending': 'am', 'substitute': 'maś', 'operation': 'substitution'}, {'range': '7.1', 'ending': 'ām', 'substitute': 'maś', 'operation': 'substitution'}),
    "7.1.41": ({'range': '7.1', 'operation': 'lopa', 'target': 'taḥ', 'paradigm': 'atmanepada'}, {'range': '7.1', 'operation': 'lopa', 'target': 'taḥ', 'paradigm': 'parasmaipada'}),
    "7.1.42": ({'range': '7.1', 'ending': 'dhvam', 'substitute': 'dhvāt', 'operation': 'substitution'}, {'range': '7.1', 'ending': 'dhvām', 'substitute': 'dhvāt', 'operation': 'substitution'}),
    "7.1.43": ({'range': '7.1', 'form': 'yajadhvainam', 'also': True, 'operation': 'agama'}, {'range': '7.1', 'form': 'yajadhvam', 'also': True, 'operation': 'agama'}),
    "7.1.44": ({'range': '7.1', 'ending': 'tasya', 'substitute': 'tāt', 'operation': 'substitution'}, {'range': '7.1', 'ending': 'tasmin', 'substitute': 'tāt', 'operation': 'substitution'}),
    "7.1.45": ({'range': '7.1', 'stem': 'tapta', 'also': True, 'operation': 'agama'}, {'range': '7.1', 'stem': 'tapa', 'also': True, 'operation': 'agama'}),
    "7.1.46": ({'range': '7.1', 'stem_class': 'idanta', 'ending': 'mas', 'operation': 'agama'}, {'range': '7.1', 'stem_class': 'idanta', 'ending': 'jas', 'operation': 'agama'}),
    "7.1.47": ({'range': '7.1', 'suffix': 'ktva', 'substitute': 'yak', 'operation': 'substitution'}, {'range': '7.1', 'suffix': 'ktvā', 'substitute': 'yak', 'operation': 'substitution'}),
    "7.1.48": ({'range': '7.1', 'form': 'iṣṭvīnam', 'also': True, 'operation': 'agama'}, {'range': '7.1', 'form': 'iṣṭvām', 'also': True, 'operation': 'agama'}),
    "7.1.49": ({'range': '7.1', 'stem': 'snā', 'also': True, 'operation': 'agama'}, {'range': '7.1', 'stem': 'pā', 'also': True, 'operation': 'agama'}),
    "7.1.50": ({'range': '7.1', 'stem_final': 'ā', 'ending': 'jas', 'augment': 'asuk', 'operation': 'agama'}, {'range': '7.1', 'stem_final': 'a', 'ending': 'jas', 'augment': 'asuk', 'operation': 'agama'}),
    "7.1.51": ({'range': '7.1', 'stem': 'aśva', 'semantic': 'ātmaprīti', 'suffix_marker': 'kyac', 'operation': 'agama'}, {'range': '7.1', 'stem': 'aśva', 'semantic': 'karma', 'suffix_marker': 'kyac', 'operation': 'agama'}),
    "7.1.52": ({'range': '7.1', 'stem_class': 'sarvanāma', 'suffix': 'āmi', 'augment': 'suṭ', 'operation': 'agama'}, {'range': '7.1', 'stem_class': 'pratipadika', 'suffix': 'āmi', 'augment': 'suṭ', 'operation': 'agama'}),
    "7.1.53": ({'range': '7.1', 'stem': 'tri', 'substitute': 'trayaḥ', 'operation': 'substitution'}, {'range': '7.1', 'stem': 'catur', 'substitute': 'trayaḥ', 'operation': 'substitution'}),
    "7.1.54": ({'range': '7.1', 'stem_class': 'hrasvanadyāp', 'augment': 'nuṭ', 'operation': 'augment'}, {'range': '7.1', 'stem_class': 'dīrghanadyāp', 'augment': 'nuṭ', 'operation': 'augment'}),
    "7.1.55": ({'range': '7.1', 'stem': 'ṣaṭ', 'also': True, 'operation': 'agama'}, {'range': '7.1', 'stem': 'pañcan', 'also': True, 'operation': 'agama'}),
    "7.1.56": ({'range': '7.1', 'stem': 'śrī', 'domain': 'chandas', 'operation': 'agama'}, {'range': '7.1', 'stem': 'śrī', 'domain': 'loka', 'operation': 'agama'}),
    "7.1.57": ({'range': '7.1', 'stem': 'go', 'position': 'pādānte', 'operation': 'agama'}, {'range': '7.1', 'stem': 'go', 'position': 'pādādi', 'operation': 'agama'}),
    "7.1.58": ({'range': '7.1', 'marker': 'idit', 'augment': 'num', 'applies_to': 'dhātu', 'operation': 'augment'}, {'range': '7.1', 'marker': 'idit', 'augment': 'num', 'applies_to': 'pratyaya', 'operation': 'augment'}),
    "7.1.59": ({'range': '7.1', 'lakara': 'lot', 'stem_class': 'mucādi', 'ending': 'śe', 'operation': 'agama'}, {'range': '7.1', 'lakara': 'laṭ', 'stem_class': 'mucādi', 'ending': 'śe', 'operation': 'agama'}),
    "7.1.60": ({'range': '7.1', 'stem': 'mas', 'ending_class': 'jhali', 'operation': 'agama'}, {'range': '7.1', 'stem': 'mas', 'ending_class': 'jha', 'operation': 'agama'}),
    "7.1.61": ({'range': '7.1', 'dhatu_lemma': 'radhi', 'following': 'ac', 'operation': 'agama'}, {'range': '7.1', 'dhatu_lemma': 'radhi', 'following': 'hal', 'operation': 'agama'}),
    "7.1.62": ({'range': '7.1', 'dhatu_lemma': 'radh', 'lakara': 'liṭ', 'augment': 'iṭ', 'rule_blocked': True}, {'range': '7.1', 'dhatu_lemma': 'rabh', 'lakara': 'liṭ', 'augment': 'iṭ', 'rule_blocked': True}),
    "7.1.63": ({'range': '7.1', 'dhatu_lemma': 'rabh', 'suffix_class': 'aśabliṭ', 'operation': 'agama'}, {'range': '7.1', 'dhatu_lemma': 'rabh', 'suffix_class': 'sic', 'operation': 'agama'}),
    "7.1.64": ({'range': '7.1', 'dhatu_lemma': 'labh', 'also': True, 'operation': 'agama'}, {'range': '7.1', 'dhatu_lemma': 'grah', 'also': True, 'operation': 'agama'}),
    "7.1.65": ({'range': '7.1', 'prefix': 'āṅ', 'suffix_marker': 'yi', 'operation': 'agama'}, {'range': '7.1', 'prefix': 'upa', 'suffix_marker': 'yi', 'operation': 'agama'}),
    "7.1.66": ({'range': '7.1', 'prefix': 'upa', 'semantic': 'praśaṃsā', 'operation': 'agama'}, {'range': '7.1', 'prefix': 'upa', 'semantic': 'karma', 'operation': 'agama'}),
    "7.1.67": ({'range': '7.1', 'has_upasarga': True, 'suffix_marker': 'khal', 'operation': 'agama'}, {'range': '7.1', 'has_upasarga': False, 'suffix_marker': 'khal', 'operation': 'agama'}),
    "7.1.68": ({'range': '7.1', 'prefix': 'su', 'kevala': True, 'rule_blocked': True}, {'range': '7.1', 'prefix': 'su', 'kevala': False, 'rule_blocked': True}),
    "7.1.69": ({'range': '7.1', 'suffix_marker': 'ciṇ', 'optional': True, 'operation': 'agama'}, {'range': '7.1', 'suffix_marker': 'ciṇ', 'optional': False, 'operation': 'agama'}),
    "7.1.70": ({'range': '7.1', 'marker': 'ugit', 'domain': 'sarvanāmasthāna', 'applies_to': 'pratyaya', 'operation': 'agama'}, {'range': '7.1', 'marker': 'ugit', 'domain': 'sarvanāmasthāna', 'applies_to': 'dhātu', 'operation': 'agama'}),
    "7.1.71": ({'range': '7.1', 'dhatu_lemma': 'yuj', 'compound_type': 'samāsa', 'rule_blocked': True}, {'range': '7.1', 'dhatu_lemma': 'yuj', 'compound_type': 'tatpuruṣa', 'rule_blocked': True}),
    "7.1.72": ({'range': '7.1', 'gender': 'napuṃsaka', 'ending_class': 'jhalac', 'operation': 'agama'}, {'range': '7.1', 'gender': 'puṃ', 'ending_class': 'jhalac', 'operation': 'agama'}),
    "7.1.73": ({'range': '7.1', 'stem_final_class': 'ik', 'following': 'ac', 'domain': 'vibhakti', 'operation': 'agama'}, {'range': '7.1', 'stem_final_class': 'ik', 'following': 'hal', 'domain': 'vibhakti', 'operation': 'agama'}),
    "7.1.74": ({'range': '7.1', 'vibhakti': 'tṛtīyādi', 'semantic': 'bhāṣitapuṃska', 'authority': 'gālava', 'operation': 'agama'}, {'range': '7.1', 'vibhakti': 'tṛtīyādi', 'semantic': 'bhāṣitapuṃska', 'authority': 'other', 'operation': 'agama'}),
    "7.1.75": ({'range': '7.1', 'stem': 'asthi', 'augment': 'anṅ', 'accent': 'udātta', 'operation': 'agama'}, {'range': '7.1', 'stem': 'asthi', 'augment': 'anṅ', 'accent': 'anudātta', 'operation': 'agama'}),
    "7.1.76": ({'range': '7.1', 'domain': 'chandas', 'also': True, 'operation': 'agama'}, {'range': '7.1', 'domain': 'loka', 'also': True, 'operation': 'agama'}),
    "7.1.77": ({'range': '7.1', 'substitute': 'ī', 'number': 'dvivacana', 'also': True, 'operation': 'substitution'}, {'range': '7.1', 'substitute': 'ī', 'number': 'ekavacana', 'also': True, 'operation': 'substitution'}),
    "7.1.78": ({'range': '7.1', 'stem_class': 'abhyasta', 'ending': 'śatuḥ', 'rule_blocked': True}, {'range': '7.1', 'stem_class': 'ordinary', 'ending': 'śatuḥ', 'rule_blocked': True}),
    "7.1.79": ({'range': '7.1', 'gender': 'napuṃsaka', 'optional': True, 'operation': 'agama'}, {'range': '7.1', 'gender': 'napuṃsaka', 'optional': False, 'operation': 'agama'}),
    "7.1.80": ({'range': '7.1', 'stem_final': 'ā', 'stem_class': 'nadī', 'augment': 'num', 'operation': 'augment'}, {'range': '7.1', 'stem_final': 'a', 'stem_class': 'nadī', 'augment': 'num', 'operation': 'augment'}),
    "7.1.81": ({'range': '7.1', 'suffix_marker': 'śap', 'rule_strength': 'nitya', 'operation': 'agama'}, {'range': '7.1', 'suffix_marker': 'śap', 'rule_strength': 'vibhāṣā', 'operation': 'agama'}),
    "7.1.82": ({'range': '7.1', 'augment': 'sau', 'stem_class': 'avan-aḍuh', 'operation': 'agama'}, {'range': '7.1', 'augment': 'sau', 'stem_class': 'ordinary', 'operation': 'agama'}),
    "7.1.83": ({'range': '7.1', 'stem': 'dṛk', 'domain': 'chandas', 'operation': 'agama'}, {'range': '7.1', 'stem': 'dṛk', 'domain': 'loka', 'operation': 'agama'}),
    "7.1.84": ({'range': '7.1', 'stem': 'div', 'substitute': 'aut', 'operation': 'substitution'}, {'range': '7.1', 'stem': 'diva', 'substitute': 'aut', 'operation': 'substitution'}),
    "7.1.85": ({'range': '7.1', 'stem': 'pathi', 'augment': 'āt', 'operation': 'agama'}, {'range': '7.1', 'stem': 'pathi', 'augment': 'at', 'operation': 'agama'}),
    "7.1.86": ({'range': '7.1', 'stem_final': 'i', 'substitute': 'at', 'domain': 'sarvanāmasthāna', 'operation': 'substitution'}, {'range': '7.1', 'stem_final': 'i', 'substitute': 'at', 'domain': 'vibhakti', 'operation': 'substitution'}),
    "7.1.87": ({'range': '7.1', 'ending': 'tha', 'substitute': 'ntha', 'operation': 'substitution'}, {'range': '7.1', 'ending': 'thā', 'substitute': 'ntha', 'operation': 'substitution'}),
    "7.1.88": ({'range': '7.1', 'stem': 'bhās', 'operation': 'lopa', 'target': 'ṭa'}, {'range': '7.1', 'stem': 'bhāṣ', 'operation': 'lopa', 'target': 'ṭa'}),
    "7.1.89": ({'range': '7.1', 'stem': 'puṃs', 'augment': 'asuṅ', 'operation': 'agama'}, {'range': '7.1', 'stem': 'puṃs', 'augment': 'num', 'operation': 'agama'}),
    "7.1.90": ({'range': '7.1', 'stem': 'go', 'augment': 'ṇit', 'operation': 'agama'}, {'range': '7.1', 'stem': 'go', 'augment': 'num', 'operation': 'agama'}),
    "7.1.91": ({'range': '7.1', 'suffix_marker': 'ṇal', 'optional': True, 'operation': 'augment'}, {'range': '7.1', 'suffix_marker': 'ṇal', 'optional': False, 'position': 'madhya', 'operation': 'augment'}),
    "7.1.92": ({'range': '7.1', 'stem': 'sakhi', 'domain': 'vibhakti', 'operation': 'agama'}, {'range': '7.1', 'stem': 'sakhi', 'domain': 'sambuddha', 'operation': 'agama'}),
    "7.1.93": ({'range': '7.1', 'augment': 'anṅ', 'following': 'sau', 'operation': 'agama'}, {'range': '7.1', 'augment': 'anṅ', 'following': 'au', 'operation': 'agama'}),
    "7.1.94": ({'range': '7.1', 'stem': 'ṛdu', 'augment': 'anṅ', 'operation': 'agama'}, {'range': '7.1', 'stem': 'ṛdu', 'augment': 'num', 'operation': 'agama'}),
    "7.1.95": ({'range': '7.1', 'stem': 'kroṣṭu', 'form': 'tṛjvat', 'operation': 'agama'}, {'range': '7.1', 'stem': 'kroṣṭu', 'form': 'tṛvat', 'operation': 'agama'}),
    "7.1.96": ({'range': '7.1', 'gender': 'strī', 'also': True, 'operation': 'agama'}, {'range': '7.1', 'gender': 'puṃ', 'also': True, 'operation': 'agama'}),
    "7.1.97": ({'range': '7.1', 'stem_final_class': 'ik', 'following': 'ac', 'vibhakti': 'tṛtīyādi', 'optional': True, 'operation': 'agama'}, {'range': '7.1', 'stem_final_class': 'ik', 'following': 'ac', 'vibhakti': 'tṛtīyādi', 'optional': False, 'operation': 'agama'}),
    "7.1.98": ({'range': '7.1', 'stem': 'catur', 'substitute': 'ām', 'accent': 'udātta', 'operation': 'substitution'}, {'range': '7.1', 'stem': 'catur', 'substitute': 'ām', 'accent': 'anudātta', 'operation': 'substitution'}),
    "7.1.99": ({'range': '7.1', 'augment': 'am', 'domain': 'sambuddha', 'operation': 'agama'}, {'range': '7.1', 'augment': 'am', 'domain': 'vibhakti', 'operation': 'agama'}),
    "7.1.100": ({'range': '7.1', 'stem_final': 'ṝ', 'following': 'it', 'applies_to': 'dhātu', 'operation': 'agama'}, {'range': '7.1', 'stem_final': 'ṝ', 'following': 'it', 'applies_to': 'pratyaya', 'operation': 'agama'}),
    "7.1.101": ({'range': '7.1', 'has_upadhā': True, 'also': True, 'operation': 'agama'}, {'range': '7.1', 'has_upadhā': False, 'also': True, 'operation': 'agama'}),
    "7.1.102": ({'range': '7.1', 'augment': 'ut', 'condition': 'oṣṭhyapūrva', 'operation': 'agama'}, {'range': '7.1', 'augment': 'ut', 'condition': 'halpūrva', 'operation': 'agama'}),
    "7.1.103": ({'range': '7.1', 'domain': 'chandas', 'rule_strength': 'bahula', 'section': '7.1.103'}, {'range': '7.1', 'domain': 'loka', 'rule_strength': 'bahula', 'section': '7.1.103'}),
}


META: dict[str, SutraMeta] = {
    "7.1.1": SutraMeta("vidhi", 'युवोरनाकौ ।', ("agama:7.1", "pada:7.1")),
    "7.1.2": SutraMeta("vidhi", 'आयनेयीनीयियः फढखच्छघां प्रत्ययादीनाम्\u200c ।', ("agama:7.1", "pada:7.1")),
    "7.1.3": SutraMeta("vidhi", 'झोऽन्तः ।', ("agama:7.1", "pada:7.1")),
    "7.1.4": SutraMeta("vidhi", 'अदभ्यस्तात्\u200c ।', ("agama:7.1", "pada:7.1")),
    "7.1.5": SutraMeta("pratisedha", 'आत्मनेपदेष्वनतः ।', ("agama:7.1", "pada:7.1")),
    "7.1.6": SutraMeta("vidhi", 'शीङो रुट् ।', ("agama:7.1", "pada:7.1")),
    "7.1.7": SutraMeta("vibhasha", 'वेत्तेर्विभाषा ।', ("agama:7.1", "pada:7.1")),
    "7.1.8": SutraMeta("paribhasha", 'बहुलं छन्दसि ।', ("agama:7.1", "pada:7.1")),
    "7.1.9": SutraMeta("vidhi", 'अतो भिस ऐस् ।', ("agama:7.1", "pada:7.1")),
    "7.1.10": SutraMeta("paribhasha", 'बहुलं छन्दसि ।', ("agama:7.1", "pada:7.1")),
    "7.1.11": SutraMeta("pratisedha", 'नेदमदसोरकोः ।', ("agama:7.1", "pada:7.1")),
    "7.1.12": SutraMeta("vidhi", 'टाङसिङसामिनात्स्याः ।', ("agama:7.1", "pada:7.1")),
    "7.1.13": SutraMeta("vidhi", 'ङेर्यः ।', ("agama:7.1", "pada:7.1")),
    "7.1.14": SutraMeta("vidhi", 'सर्वनाम्नः स्मै ।', ("agama:7.1", "pada:7.1")),
    "7.1.15": SutraMeta("vidhi", 'ङसिङ्योः स्मात्स्मिनौ ।', ("agama:7.1", "pada:7.1")),
    "7.1.16": SutraMeta("vibhasha", 'पूर्वादिभ्यो नवभ्यो वा ।', ("agama:7.1", "pada:7.1")),
    "7.1.17": SutraMeta("vidhi", 'जसः शी ।', ("agama:7.1", "pada:7.1")),
    "7.1.18": SutraMeta("vidhi", 'औङ आपः ।', ("agama:7.1", "pada:7.1")),
    "7.1.19": SutraMeta("vidhi", 'नपुंसकाच्च ।', ("agama:7.1", "pada:7.1")),
    "7.1.20": SutraMeta("vidhi", 'जश्शसोः शिः ।', ("agama:7.1", "pada:7.1")),
    "7.1.21": SutraMeta("vidhi", 'अष्टाभ्य औश् ।', ("agama:7.1", "pada:7.1")),
    "7.1.22": SutraMeta("vidhi", 'षड्भ्यो लुक् ।', ("agama:7.1", "pada:7.1")),
    "7.1.23": SutraMeta("vidhi", 'स्वमोर्नपुंसकात्\u200c ।', ("agama:7.1", "pada:7.1")),
    "7.1.24": SutraMeta("vidhi", 'अतोऽम् ।', ("agama:7.1", "pada:7.1")),
    "7.1.25": SutraMeta("vidhi", 'अद्ड् डतरादिभ्यः पञ्चभ्यः ।', ("agama:7.1", "pada:7.1")),
    "7.1.26": SutraMeta("pratisedha", 'नेतराच्छन्दसि ।', ("agama:7.1", "pada:7.1")),
    "7.1.27": SutraMeta("vidhi", 'युष्मदस्मद्भ्यां ङसोऽश् ।', ("agama:7.1", "pada:7.1")),
    "7.1.28": SutraMeta("vidhi", 'ङे प्रथमयोरम् ।', ("agama:7.1", "pada:7.1")),
    "7.1.29": SutraMeta("pratisedha", 'शसो न ।', ("agama:7.1", "pada:7.1")),
    "7.1.30": SutraMeta("vidhi", 'भ्यसो भ्यम् ।', ("agama:7.1", "pada:7.1")),
    "7.1.31": SutraMeta("vidhi", 'पञ्चम्या अत्\u200c ।', ("agama:7.1", "pada:7.1")),
    "7.1.32": SutraMeta("vidhi", 'एकवचनस्य च ।', ("agama:7.1", "pada:7.1")),
    "7.1.33": SutraMeta("vidhi", 'साम आकम् ।', ("agama:7.1", "pada:7.1")),
    "7.1.34": SutraMeta("vidhi", 'आत औ णलः ।', ("agama:7.1", "pada:7.1")),
    "7.1.35": SutraMeta("vibhasha", 'तुह्योस्तातङाशिष्यन्यतरस्याम् ।', ("agama:7.1", "pada:7.1")),
    "7.1.36": SutraMeta("vidhi", 'विदेः शतुर्वसुः ।', ("agama:7.1", "pada:7.1")),
    "7.1.37": SutraMeta("vidhi", 'समासेऽनञ्पूर्वे क्त्वो ल्यप्\u200c ।', ("agama:7.1", "pada:7.1")),
    "7.1.38": SutraMeta("vidhi", 'क्त्वाऽपि छन्दसि ।', ("agama:7.1", "pada:7.1")),
    "7.1.39": SutraMeta("vidhi", 'सुपां सुलुक्पूर्वसवर्णाऽऽच्छेयाडाड्यायाजालः ।', ("agama:7.1", "pada:7.1")),
    "7.1.40": SutraMeta("vidhi", 'अमो मश् ।', ("agama:7.1", "pada:7.1")),
    "7.1.41": SutraMeta("vidhi", 'लोपस्त आत्मनेपदेषु ।', ("agama:7.1", "pada:7.1")),
    "7.1.42": SutraMeta("vidhi", 'ध्वमो ध्वात्\u200c ।', ("agama:7.1", "pada:7.1")),
    "7.1.43": SutraMeta("vidhi", 'यजध्वैनमिति च ।', ("agama:7.1", "pada:7.1")),
    "7.1.44": SutraMeta("vidhi", 'तस्य तात्\u200c ।', ("agama:7.1", "pada:7.1")),
    "7.1.45": SutraMeta("vidhi", 'तप्तनप्तनथनाश्च ।', ("agama:7.1", "pada:7.1")),
    "7.1.46": SutraMeta("vidhi", 'इदन्तो मसि ।', ("agama:7.1", "pada:7.1")),
    "7.1.47": SutraMeta("vidhi", 'क्त्वो यक् ।', ("agama:7.1", "pada:7.1")),
    "7.1.48": SutraMeta("vidhi", 'इष्ट्वीनमिति च ।', ("agama:7.1", "pada:7.1")),
    "7.1.49": SutraMeta("vidhi", 'स्नात्व्यादयश्च ।', ("agama:7.1", "pada:7.1")),
    "7.1.50": SutraMeta("vidhi", 'आज्जसेरसुक् ।', ("agama:7.1", "pada:7.1")),
    "7.1.51": SutraMeta("vidhi", 'अश्वक्षीरवृषलवणानामात्मप्रीतौ क्यचि ।', ("agama:7.1", "pada:7.1")),
    "7.1.52": SutraMeta("vidhi", 'आमि सर्वनाम्नः सुट् ।', ("agama:7.1", "pada:7.1")),
    "7.1.53": SutraMeta("vidhi", 'त्रेस्त्रयः ।', ("agama:7.1", "pada:7.1")),
    "7.1.54": SutraMeta("vidhi", 'ह्रस्वनद्यापो नुट् ।', ("agama:7.1", "pada:7.1")),
    "7.1.55": SutraMeta("vidhi", 'षट्चतुर्भ्यश्च ।', ("agama:7.1", "pada:7.1")),
    "7.1.56": SutraMeta("vidhi", 'श्रीग्रामण्योश्छन्दसि ।', ("agama:7.1", "pada:7.1")),
    "7.1.57": SutraMeta("vidhi", 'गोः पादान्ते ।', ("agama:7.1", "pada:7.1")),
    "7.1.58": SutraMeta("vidhi", 'इदितो नुम् धातोः ।', ("agama:7.1", "pada:7.1")),
    "7.1.59": SutraMeta("vidhi", 'शे मुचादीनाम् ।', ("agama:7.1", "pada:7.1")),
    "7.1.60": SutraMeta("vidhi", 'मस्जिनशोर्झलि ।', ("agama:7.1", "pada:7.1")),
    "7.1.61": SutraMeta("vidhi", 'रधिजभोरचि ।', ("agama:7.1", "pada:7.1")),
    "7.1.62": SutraMeta("pratisedha", 'नेट्यलिटि रधेः ।', ("agama:7.1", "pada:7.1")),
    "7.1.63": SutraMeta("vidhi", 'रभेरशब्लिटोः ।', ("agama:7.1", "pada:7.1")),
    "7.1.64": SutraMeta("vidhi", 'लभेश्च ।', ("agama:7.1", "pada:7.1")),
    "7.1.65": SutraMeta("vidhi", 'आङो यि ।', ("agama:7.1", "pada:7.1")),
    "7.1.66": SutraMeta("vidhi", 'उपात्\u200c प्रशंसायाम् ।', ("agama:7.1", "pada:7.1")),
    "7.1.67": SutraMeta("vidhi", 'उपसर्गात्\u200c खल्घञोः ।', ("agama:7.1", "pada:7.1")),
    "7.1.68": SutraMeta("pratisedha", 'न सुदुर्भ्यां केवलाभ्याम् ।', ("agama:7.1", "pada:7.1")),
    "7.1.69": SutraMeta("vibhasha", 'विभाषा चिण्णमुलोः ।', ("agama:7.1", "pada:7.1")),
    "7.1.70": SutraMeta("vidhi", 'उगिदचां सर्वनामस्थानेऽधातोः ।', ("agama:7.1", "pada:7.1")),
    "7.1.71": SutraMeta("pratisedha", 'युजेरसमासे ।', ("agama:7.1", "pada:7.1")),
    "7.1.72": SutraMeta("vidhi", 'नपुंसकस्य झलचः ।', ("agama:7.1", "pada:7.1")),
    "7.1.73": SutraMeta("vidhi", 'इकोऽचि विभक्तौ ।', ("agama:7.1", "pada:7.1")),
    "7.1.74": SutraMeta("vidhi", 'तृतीयाऽऽदिषु भाषितपुंस्कं पुंवद्गालवस्य ।', ("agama:7.1", "pada:7.1")),
    "7.1.75": SutraMeta("vidhi", 'अस्थिदधिसक्थ्यक्ष्णामनङुदात्तः ।', ("agama:7.1", "pada:7.1")),
    "7.1.76": SutraMeta("vidhi", 'छन्दस्यपि दृश्यते ।', ("agama:7.1", "pada:7.1")),
    "7.1.77": SutraMeta("vidhi", 'ई च द्विवचने ।', ("agama:7.1", "pada:7.1")),
    "7.1.78": SutraMeta("pratisedha", 'नाभ्यस्ताच्छतुः ।', ("agama:7.1", "pada:7.1")),
    "7.1.79": SutraMeta("vibhasha", 'वा नपुंसकस्य ।', ("agama:7.1", "pada:7.1")),
    "7.1.80": SutraMeta("vidhi", 'आच्छीनद्योर्नुम् ।', ("agama:7.1", "pada:7.1")),
    "7.1.81": SutraMeta("vidhi", 'शप्श्यनोर्नित्यम् ।', ("agama:7.1", "pada:7.1")),
    "7.1.82": SutraMeta("vidhi", 'सावनडुहः ।', ("agama:7.1", "pada:7.1")),
    "7.1.83": SutraMeta("vidhi", 'दृक्स्ववस्स्वतवसां छन्दसि ।', ("agama:7.1", "pada:7.1")),
    "7.1.84": SutraMeta("vidhi", 'दिव औत्\u200c ।', ("agama:7.1", "pada:7.1")),
    "7.1.85": SutraMeta("vidhi", 'पथिमथ्यृभुक्षामात्\u200c ।', ("agama:7.1", "pada:7.1")),
    "7.1.86": SutraMeta("vidhi", 'इतोऽत्\u200c सर्वनामस्थाने ।', ("agama:7.1", "pada:7.1")),
    "7.1.87": SutraMeta("vidhi", 'थो न्थः ।', ("agama:7.1", "pada:7.1")),
    "7.1.88": SutraMeta("vidhi", 'भस्य टेर्लोपः ।', ("agama:7.1", "pada:7.1")),
    "7.1.89": SutraMeta("vidhi", 'पुंसोऽसुङ् ।', ("agama:7.1", "pada:7.1")),
    "7.1.90": SutraMeta("vidhi", 'गोतो णित्\u200c ।', ("agama:7.1", "pada:7.1")),
    "7.1.91": SutraMeta("vibhasha", 'णलुत्तमो वा ।', ("agama:7.1", "pada:7.1")),
    "7.1.92": SutraMeta("vidhi", 'सख्युरसम्बुद्धौ ।', ("agama:7.1", "pada:7.1")),
    "7.1.93": SutraMeta("vidhi", 'अनङ् सौ ।', ("agama:7.1", "pada:7.1")),
    "7.1.94": SutraMeta("vidhi", 'ऋदुशनस्पुरुदंसोऽनेहसां च ।', ("agama:7.1", "pada:7.1")),
    "7.1.95": SutraMeta("vidhi", 'तृज्वत्\u200c क्रोष्टुः ।', ("agama:7.1", "pada:7.1")),
    "7.1.96": SutraMeta("vidhi", 'स्त्रियां च ।', ("agama:7.1", "pada:7.1")),
    "7.1.97": SutraMeta("vibhasha", 'विभाषा तृतीयाऽऽदिष्वचि ।', ("agama:7.1", "pada:7.1")),
    "7.1.98": SutraMeta("vidhi", 'चतुरनडुहोरामुदात्तः ।', ("agama:7.1", "pada:7.1")),
    "7.1.99": SutraMeta("vidhi", 'अम् सम्बुद्धौ ।', ("agama:7.1", "pada:7.1")),
    "7.1.100": SutraMeta("vidhi", 'ॠत इद्धातोः ।', ("agama:7.1", "pada:7.1")),
    "7.1.101": SutraMeta("vidhi", 'उपधायाश्च ।', ("agama:7.1", "pada:7.1")),
    "7.1.102": SutraMeta("vidhi", 'उदोष्ठ्यपूर्वस्य ।', ("agama:7.1", "pada:7.1")),
    "7.1.103": SutraMeta("paribhasha", 'बहुलं छन्दसि ।', ("agama:7.1", "pada:7.1")),
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
        raise AssertionError("sutra_impl_7_1 self-check failed: " + ", ".join(failures))
    return {
        "sutras": len(FIXTURES),
        "meta": len(META),
        "predicates": len([n for n in globals() if n.startswith("sutra_7_1_")]),
    }


(
    IMPLEMENTED_IDS,
    has_real_implementation,
    handler_for,
    positive_features,
    negative_features,
) = make_module_api(FIXTURES, globals())

_COUNTS = _self_check()

