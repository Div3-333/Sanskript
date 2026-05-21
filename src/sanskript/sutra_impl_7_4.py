"""Discrete Pāṇinian predicates for Adhyāya 7.4 (ṇati / ṇ-agama / lopa).

Hand-written per sūtra from ``data/ashtadhyayi_sutras.json`` (``_canon74.tsv``).
Domain: ṇati retroflexion, controlled ṇ-agama, and lopa in pada 7.4.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .anga import apply_anga_operation, operation_named, operations_for_range
from .phonology import is_consonant, is_upadha
from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api

_SAMJNA = "samjna"
_PARIBHASHA = "paribhasha"
_VIDHI = "vidhi"
_PRATISEDHA = "pratisedha"
_VIBHASHA = "vibhasha"

_NATI_OP = operation_named("ṇati-retroflexion")

_GANA_7_4_3 = frozenset({'bhraj', 'bhas', 'bhasa', 'bhash', 'dipa', 'jiva', 'mila', 'pida'})
_GANA_7_4_11 = frozenset({'ricch', 'rit', 'rut'})
_GANA_7_4_12 = frozenset({'shrid', 'rid', 'rapra'})
_GANA_7_4_34 = frozenset({'ashanaya', 'udanyadhana', 'bubhuksha', 'pipasa', 'garddhi'})
_GANA_7_4_65 = frozenset({'dadharti', 'dardharti', 'dardharshi', 'bobhutu', 'tetikte', 'alarshi', 'apaniphanat', 'samsanishyadat', 'karikrat', 'kanikradat', 'bharibhrat', 'davidhvatah', 'davidyutat', 'taritritah', 'sarisripatam', 'varivrijat', 'marmrijya', 'aganiganti'})
_GANA_7_4_84 = frozenset({'nik', 'vanchu', 'srams', 'dhvams', 'bhrams', 'kas', 'pat', 'pad', 'skand'})
_GANA_7_4_86 = frozenset({'jap', 'jabh', 'adah', 'adash', 'abhanj', 'apash'})
_GANA_7_4_95 = frozenset({'smr', 'rit', 'var', 'prath', 'mrad', 'strir', 'spash'})
_GANA_7_4_97 = frozenset({'i'})

def _in_nati_range(c: Mapping[str, Any]) -> bool:
    """True when context range 7.4 exposes ṇati-retroflexion operations."""
    return any(op.name == "ṇati-retroflexion" for op in operations_for_range(str(c.get("range"))))

def _retroflex_n(form: str) -> str:
    """Apply controlled n→ṇ retroflexion (7.4 domain)."""
    return apply_anga_operation(form, _NATI_OP)


def _hrasva_upadha(c: Mapping[str, Any]) -> bool:
    """Penultimate (upadhā) is present and not a consonant (hrasva context)."""
    stem = str(c.get("stem_form", ""))
    if stem:
        penult = is_upadha(stem)
        return penult is not None and not is_consonant(penult)
    return bool(c.get("upadhā"))


def _retroflex_context(c: Mapping[str, Any]) -> bool:
    """ṇati/retroflex operation is licensed and n→ṇ applies when a form is given."""
    if not _in_nati_range(c):
        return False
    op = c.get("operation")
    if op not in ("ṇati", "retroflex"):
        return False
    form = str(c.get("stem_form", ""))
    if form and "n" in form:
        return _retroflex_n(form) != form
    return True


def sutra_7_4_1(c) -> bool:
    """ṇau caṅi upadhāyāḥ hrasvaḥ: ṇati when ṇau+caṅ and penultimate is light."""
    return (
        _eq(c, "range", "7.4")
        and _in_nati_range(c)
        and _eq(c, "suffix", "ṇau")
        and _eq(c, "environment", "caṅ")
        and _eq(c, "vowel_weight", "hrasva")
        and _hrasva_upadha(c)
    )

def sutra_7_4_2(c) -> bool:
    """na aglopiśāsṛditām: blocks ṇati for aglu-pi-śās-ṛdit suffixes."""
    return _eq(c, "range", "7.4") and bool(c.get("rule_blocked")) and _eq(c, "environment", "aglopiśāsṛdit")

def sutra_7_4_3(c) -> bool:
    """bhāj-bhās-bhāṣ-dīp-jīv-mīl-pīḍām anyatarasyām: optional ṇati in listed roots."""
    return (
        _eq(c, "range", "7.4")
        and _in(c, "stem", _GANA_7_4_3)
        and bool(c.get("optional"))
        and _retroflex_context(c)
    )

def sutra_7_4_4(c) -> bool:
    """lopaḥ pibateḥ īc ca abhyāsasya: ī-lopa of abhyāsa pib before īt."""
    return _eq(c, "range", "7.4") and _eq(c, "operation", "lopa") and _eq(c, "environment", "abhyāsa") and _eq(c, "dhatu", "pib") and _eq(c, "augment", "īt")

def sutra_7_4_5(c) -> bool:
    """tiṣṭhater it: it augment after tiṣṭh."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "stha") and _eq(c, "augment", "it")

def sutra_7_4_6(c) -> bool:
    """jighrater vā: optional it after jighr."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "jighr") and _eq(c, "augment", "it") and bool(c.get("optional"))

def sutra_7_4_7(c) -> bool:
    """ur ṛt: ṛt after u (jighr class)."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_final", "u") and _eq(c, "augment", "ṛt")

def sutra_7_4_8(c) -> bool:
    """nityaṃ chandasi: obligatory in chandas."""
    return _eq(c, "range", "7.4") and _eq(c, "environment", "chandas") and _eq(c, "rule", "nitya")

def sutra_7_4_9(c) -> bool:
    """dayater digi liṭi: day in dig before liṭ."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "day") and _eq(c, "environment", "dig") and _eq(c, "lakara", "liṭ")

def sutra_7_4_10(c) -> bool:
    """ṛtaś ca saṃyogāder guṇaḥ: guṇa of ṛ after saṃyogādi."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_final", "ṛ") and _eq(c, "operation", "guṇa") and _eq(c, "environment", "saṃyogādi")

def sutra_7_4_11(c) -> bool:
    """ṛcchati-ṛtām: gaṇa of ṛ-dhātus with ṇati/ṛt."""
    return _eq(c, "range", "7.4") and _in(c, "stem", _GANA_7_4_11) and _retroflex_context(c)

def sutra_7_4_12(c) -> bool:
    """śṛd-ṛ-prāṃ hrasvo vā: optional hrasva in śṛdṛ-pra gaṇa."""
    return _eq(c, "range", "7.4") and _in(c, "stem", _GANA_7_4_12) and _eq(c, "vowel_weight", "hrasva") and bool(c.get("optional"))

def sutra_7_4_13(c) -> bool:
    """ke ṇaḥ: ṇa after ke (k-gaṇa)."""
    return _eq(c, "range", "7.4") and _eq(c, "environment", "ke") and _retroflex_context(c)

def sutra_7_4_14(c) -> bool:
    """na kapi: no ṇati in kapi."""
    return _eq(c, "range", "7.4") and _eq(c, "environment", "kapi") and bool(c.get("rule_blocked"))

def sutra_7_4_15(c) -> bool:
    """āpo 'nyatarasyām: optional āp substitution."""
    return _eq(c, "range", "7.4") and _eq(c, "stem", "ap") and bool(c.get("optional")) and _eq(c, "operation", "substitution")

def sutra_7_4_16(c) -> bool:
    """ṛdṛśo 'ṅi guṇaḥ: guṇa of ṛ in ṛdṛś before aṅ."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "ridrish") and _eq(c, "suffix", "aṅ") and _eq(c, "operation", "guṇa")

def sutra_7_4_17(c) -> bool:
    """asyateḥ thuk: thuk after asy."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "as") and _eq(c, "augment", "thuk")

def sutra_7_4_18(c) -> bool:
    """śvayater aḥ: aḥ after śvay."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "śvay") and _eq(c, "augment", "aḥ")

def sutra_7_4_19(c) -> bool:
    """pataḥ pum: pum augment after pat."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "pat") and _eq(c, "augment", "pum")

def sutra_7_4_20(c) -> bool:
    """vac um: um after vac."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "vac") and _eq(c, "augment", "um")

def sutra_7_4_21(c) -> bool:
    """śīṅaḥ sārvadhātuke guṇaḥ: guṇa of śī before sarvadhatuka."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "śī") and _eq(c, "environment", "sārvadhātuka") and _eq(c, "operation", "guṇa")

def sutra_7_4_22(c) -> bool:
    """ayaṅ yi kṅiti: ayaṅ before yi in kṅit."""
    return _eq(c, "range", "7.4") and _eq(c, "augment", "ayaṅ") and _eq(c, "environment", "yi") and _eq(c, "suffix", "kṅit")

def sutra_7_4_23(c) -> bool:
    """upasargāt hrasva ūhateḥ: hrasva after upasarga in ūh."""
    return _eq(c, "range", "7.4") and _eq(c, "environment", "upasarga") and _eq(c, "vowel_weight", "hrasva") and _eq(c, "dhatu", "ūh")

def sutra_7_4_24(c) -> bool:
    """eter liṅi: et in liṅ."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "i") and _eq(c, "lakara", "liṅ")

def sutra_7_4_25(c) -> bool:
    """akṛtsārvadhātukayoḥ dīrghaḥ: lengthening in non-kṛt sarvadhatuka."""
    return _eq(c, "range", "7.4") and _eq(c, "vowel_weight", "dīrgha") and _eq(c, "environment", "akṛtsārvadhātuka")

def sutra_7_4_26(c) -> bool:
    """cvau ca: ca after cvau."""
    return _eq(c, "range", "7.4") and _eq(c, "suffix", "cvau") and _eq(c, "rule", "ca")

def sutra_7_4_27(c) -> bool:
    """rīṅ ṛtaḥ: rīṅ after ṛt."""
    return _eq(c, "range", "7.4") and _eq(c, "augment", "rīṅ") and _eq(c, "stem_final", "ṛ")

def sutra_7_4_28(c) -> bool:
    """riṅ śayagliṅkṣu: riṅ in śayaglṅkṣ."""
    return _eq(c, "range", "7.4") and _eq(c, "augment", "riṅ") and _eq(c, "environment", "śayagliṅkṣu")

def sutra_7_4_29(c) -> bool:
    """guṇo 'rtisaṃyogādyoḥ: guṇa in ṛti-saṃyogādi."""
    return _eq(c, "range", "7.4") and _eq(c, "operation", "guṇa") and _eq(c, "environment", "artisaṃyogādi")

def sutra_7_4_30(c) -> bool:
    """yaṅi ca: ca after yaṅ."""
    return _eq(c, "range", "7.4") and _eq(c, "suffix", "yaṅ") and _eq(c, "rule", "ca")

def sutra_7_4_31(c) -> bool:
    """ī ghrādhmoḥ: ī in ghrā-dhm."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "ghradhm") and _eq(c, "stem_final", "ī")

def sutra_7_4_32(c) -> bool:
    """asya cvau: cvau after as."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "as") and _eq(c, "suffix", "cvau")

def sutra_7_4_33(c) -> bool:
    """kyaci ca: ca after kyac."""
    return _eq(c, "range", "7.4") and _eq(c, "suffix", "kyac") and _eq(c, "rule", "ca")

def sutra_7_4_34(c) -> bool:
    """aśanāyodanyadhana in bubhukṣādi: forms in hunger/thirst gaṇa."""
    return _eq(c, "range", "7.4") and _in(c, "stem", _GANA_7_4_34) and _eq(c, "environment", "bubhukṣādi")

def sutra_7_4_35(c) -> bool:
    """na chandasi aputrasya: no rule in chandas except putra."""
    return _eq(c, "range", "7.4") and _eq(c, "environment", "chandas") and bool(c.get("rule_blocked")) and _eq(c, "semantic", "aputra")

def sutra_7_4_36(c) -> bool:
    """durasya-draviṇasya-vṛṣaṇyati-riṣaṇyati: yu after listed."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "durasya") and _eq(c, "suffix", "yu")

def sutra_7_4_37(c) -> bool:
    """aśvāghasyāt: āt after aśvāgha."""
    return _eq(c, "range", "7.4") and _eq(c, "stem", "aśvāgha") and _eq(c, "augment", "āt")

def sutra_7_4_38(c) -> bool:
    """devasumnayoḥ yajuṣi kāṭhake: devasumna in yajus kāṭhaka."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "devasumna") and _eq(c, "environment", "yajus") and _eq(c, "authority", "kāṭhaka")

def sutra_7_4_39(c) -> bool:
    """kavyadhvarapṛtanasya ṛci lopaḥ: lopa in ṛc of kavyadhvara-pṛtana."""
    return _eq(c, "range", "7.4") and _eq(c, "operation", "lopa") and _eq(c, "environment", "ṛc") and _eq(c, "stem_group", "kavyadhvarapṛtana")

def sutra_7_4_40(c) -> bool:
    """dyati-syati-māsthām iti kiti: it in dyati-gaṇa before kit."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "dyatisyatimāsthām") and _eq(c, "augment", "it") and _eq(c, "suffix", "kit")

def sutra_7_4_41(c) -> bool:
    """śācchoḥ anyatarasyām: optional śāccha."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "śāccha") and bool(c.get("optional"))

def sutra_7_4_42(c) -> bool:
    """dadhāter hiḥ: hi after dadhā."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "dhā") and _eq(c, "augment", "hi")

def sutra_7_4_43(c) -> bool:
    """jahāteś ca ktvi: ca lopa in jahā before ktv."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "hā") and _eq(c, "suffix", "ktv") and _eq(c, "operation", "lopa")

def sutra_7_4_44(c) -> bool:
    """vibhāṣā chandasi: optional in chandas."""
    return _eq(c, "range", "7.4") and _eq(c, "environment", "chandas") and bool(c.get("optional"))

def sutra_7_4_45(c) -> bool:
    """sudhit-vasudhit-nemadhit and dhī forms."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "sudhit") and _eq(c, "rule", "ca")

def sutra_7_4_46(c) -> bool:
    """do dad ghoḥ: dad after do before gho."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_final", "d") and _eq(c, "substitute", "dad") and _eq(c, "environment", "gho")

def sutra_7_4_47(c) -> bool:
    """ac upasargāt taḥ: ta after ac upasarga."""
    return _eq(c, "range", "7.4") and _eq(c, "environment", "upasarga") and _eq(c, "suffix", "ac") and _eq(c, "augment", "ta")

def sutra_7_4_48(c) -> bool:
    """apo bhi: bhi after ap."""
    return _eq(c, "range", "7.4") and _eq(c, "stem", "ap") and _eq(c, "suffix", "bhi")

def sutra_7_4_49(c) -> bool:
    """saḥ syāt ārdhadhātuke: si in ārdhadhātuka after sa."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_final", "s") and _eq(c, "suffix", "si") and _eq(c, "environment", "ārdhadhātuka")

def sutra_7_4_50(c) -> bool:
    """tāsastyor lopaḥ: lopa of tās/ti."""
    return _eq(c, "range", "7.4") and _eq(c, "operation", "lopa") and _eq(c, "suffix_group", "tāsasti")

def sutra_7_4_51(c) -> bool:
    """ri ca: ca after ri."""
    return _eq(c, "range", "7.4") and _eq(c, "suffix", "ri") and _eq(c, "rule", "ca")

def sutra_7_4_52(c) -> bool:
    """ha eti: eti after ha."""
    return _eq(c, "range", "7.4") and _eq(c, "augment", "ha") and _eq(c, "suffix", "eti")

def sutra_7_4_53(c) -> bool:
    """yīvarṇayor dīdhīvevyoḥ: dīdhī in yī-varṇa dīdhīvevya."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "yīvarṇa") and _eq(c, "operation", "dīdhī")

def sutra_7_4_54(c) -> bool:
    """sani mīmāghurabhalabhaśakapadām ac is: is in san after mīmā-gaṇa."""
    return _eq(c, "range", "7.4") and _eq(c, "suffix", "san") and _eq(c, "stem_group", "mīmāghurabha") and _eq(c, "augment", "is")

def sutra_7_4_55(c) -> bool:
    """āpjñapyṛdhām īt: īt in āpjñapyṛdhā gaṇa."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "āpjñapyṛdhā") and _eq(c, "augment", "īt")

def sutra_7_4_56(c) -> bool:
    """dambha ic ca: ic ca after dambh."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "dambh") and _eq(c, "augment", "ic") and _eq(c, "rule", "ca")

def sutra_7_4_57(c) -> bool:
    """muco 'karmakasya guṇo vā: optional guṇa of muc akarmaka."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "muc") and _eq(c, "voice", "akarmaka") and _eq(c, "operation", "guṇa") and bool(c.get("optional"))

def sutra_7_4_58(c) -> bool:
    """atra lopo 'bhyāsasya: lopa here of abhyāsa."""
    return _eq(c, "range", "7.4") and _eq(c, "operation", "lopa") and _eq(c, "environment", "abhyāsa") and _eq(c, "rule", "atra")

def sutra_7_4_59(c) -> bool:
    """hrasvaḥ: hrasva (anuvṛtti continuation)."""
    return _eq(c, "range", "7.4") and _eq(c, "vowel_weight", "hrasva") and _eq(c, "environment", "abhyāsa")

def sutra_7_4_60(c) -> bool:
    """halādiḥ śeṣaḥ: hal-initial remainder (abhyāsa lopa scope)."""
    return _eq(c, "range", "7.4") and _eq(c, "environment", "abhyāsa") and _eq(c, "condition", "halādi") and _eq(c, "rule", "śeṣa")

def sutra_7_4_61(c) -> bool:
    """śarpūrvāḥ khayaḥ: khaya after śar-pūrva."""
    return _eq(c, "range", "7.4") and _eq(c, "condition", "śarpūrva") and _eq(c, "suffix", "khaya")

def sutra_7_4_62(c) -> bool:
    """kuhoś cuḥ: cu after kuh."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "kuh") and _eq(c, "substitute", "cu")

def sutra_7_4_63(c) -> bool:
    """na kavater yaṅi: no yaṅ of kavat."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "kavat") and _eq(c, "suffix", "yaṅ") and bool(c.get("rule_blocked"))

def sutra_7_4_64(c) -> bool:
    """kṛṣeḥ chandasi: kṛṣ in chandas."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "kṛṣ") and _eq(c, "environment", "chandas")

def sutra_7_4_65(c) -> bool:
    """dadharti-gaṇa: operations in listed reduplicated dhātus."""
    return _eq(c, "range", "7.4") and _in(c, "stem", _GANA_7_4_65) and _retroflex_context(c)

def sutra_7_4_66(c) -> bool:
    """ur at: at after u."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_final", "u") and _eq(c, "augment", "at")

def sutra_7_4_67(c) -> bool:
    """dyutisvāpyoḥ samprasāraṇam: samprasāraṇa of dyuti-svāpya."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "dyutisvāpya") and _eq(c, "operation", "samprasāraṇa")

def sutra_7_4_68(c) -> bool:
    """vyatho liṭi: vyath in liṭ."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "vyath") and _eq(c, "lakara", "liṭ")

def sutra_7_4_69(c) -> bool:
    """dīrgha iṇaḥ kiti: dīrgha of iṇ before kit."""
    return _eq(c, "range", "7.4") and _eq(c, "vowel_weight", "dīrgha") and _eq(c, "environment", "iṇ") and _eq(c, "suffix", "kit")

def sutra_7_4_70(c) -> bool:
    """ata ādeḥ: ādeśa from a-ending."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_final", "a") and _eq(c, "operation", "ādeśa")

def sutra_7_4_71(c) -> bool:
    """tasmān nuḍ dvihalaḥ: nuṭ after tasmād before dvihal."""
    return _eq(c, "range", "7.4") and _eq(c, "environment", "tasmāt") and _eq(c, "augment", "nuṭ") and _eq(c, "condition", "dvihal")

def sutra_7_4_72(c) -> bool:
    """aśnoteś ca: ca after aśnot."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "aśnot") and _eq(c, "rule", "ca")

def sutra_7_4_73(c) -> bool:
    """bhavater aḥ: aḥ after bhav."""
    return _eq(c, "range", "7.4") and _eq(c, "dhatu", "bhū") and _eq(c, "augment", "aḥ")

def sutra_7_4_74(c) -> bool:
    """sasūveti nigame: sasūva in nigama."""
    return _eq(c, "range", "7.4") and _eq(c, "form", "sasūva") and _eq(c, "environment", "nigama")

def sutra_7_4_75(c) -> bool:
    """nijāṃ trayāṇāṃ guṇaḥ ślau: guṇa of nij tri in ślu."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "nij") and _eq(c, "operation", "guṇa") and _eq(c, "suffix", "ślu")

def sutra_7_4_76(c) -> bool:
    """bhṛñām it: it in bhṛñ gaṇa."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "bhṛñ") and _eq(c, "augment", "it")

def sutra_7_4_77(c) -> bool:
    """artipipartyoś ca: ca after arti-piparti."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "artipiparti") and _eq(c, "rule", "ca")

def sutra_7_4_78(c) -> bool:
    """bahulaṃ chandasi: bahula in chandas."""
    return _eq(c, "range", "7.4") and _eq(c, "rule", "bahula") and _eq(c, "environment", "chandas")

def sutra_7_4_79(c) -> bool:
    """sanyataḥ: ata after san."""
    return _eq(c, "range", "7.4") and _eq(c, "suffix", "san") and _eq(c, "augment", "ata")

def sutra_7_4_80(c) -> bool:
    """oḥ puñaji apare: puñaji after o, not first."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_final", "o") and _eq(c, "suffix", "puñaji") and _eq(c, "position", "apara")

def sutra_7_4_81(c) -> bool:
    """sravati-gaṇa optional operations."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "sravati") and bool(c.get("optional"))

def sutra_7_4_82(c) -> bool:
    """guṇo yaṅlukoḥ: guṇa in yaṅ-luk."""
    return _eq(c, "range", "7.4") and _eq(c, "operation", "guṇa") and _eq(c, "environment", "yaṅluk")

def sutra_7_4_83(c) -> bool:
    """dīrgho 'kitaḥ: dīrgha when not kit."""
    return _eq(c, "range", "7.4") and _eq(c, "vowel_weight", "dīrgha") and _eq(c, "environment", "akita")

def sutra_7_4_84(c) -> bool:
    """nīk-vañcu-gaṇa: operations in listed roots."""
    return _eq(c, "range", "7.4") and _in(c, "stem", _GANA_7_4_84) and _retroflex_context(c)

def sutra_7_4_85(c) -> bool:
    """nuk ato 'nunāsikāntasya: nuk after a of anunāsikānta."""
    return _eq(c, "range", "7.4") and _eq(c, "augment", "nuk") and _eq(c, "environment", "anunāsikānta")

def sutra_7_4_86(c) -> bool:
    """japajabhagaṇa: ca in listed roots."""
    return _eq(c, "range", "7.4") and _in(c, "stem", _GANA_7_4_86) and _eq(c, "rule", "ca")

def sutra_7_4_87(c) -> bool:
    """caraphaloś ca: ca after caraphal."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "caraphal") and _eq(c, "rule", "ca")

def sutra_7_4_88(c) -> bool:
    """ut parasyātaḥ: ut of para's ata."""
    return _eq(c, "range", "7.4") and _eq(c, "augment", "ut") and _eq(c, "relation", "parasya") and _eq(c, "stem_final", "a")

def sutra_7_4_89(c) -> bool:
    """ti ca: ca after ti."""
    return _eq(c, "range", "7.4") and _eq(c, "suffix", "ti") and _eq(c, "rule", "ca")

def sutra_7_4_90(c) -> bool:
    """rīgṛdupadhasya ca: ca after ṛgṛdupadhā."""
    return _eq(c, "range", "7.4") and _eq(c, "condition", "ṛgṛdupadhā") and _eq(c, "rule", "ca")

def sutra_7_4_91(c) -> bool:
    """rugrīkau ca luki: ca in luk after rug-rīka."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "rugrīka") and _eq(c, "environment", "luk") and _eq(c, "rule", "ca")

def sutra_7_4_92(c) -> bool:
    """ṛtaś ca: ca after ṛt (continuation)."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_final", "ṛ") and _eq(c, "rule", "ca")

def sutra_7_4_93(c) -> bool:
    """sanvat laghuni caṅpare 'naglope: ṇati when sanvat, light, caṅ follows, no aglopa."""
    return (
        _eq(c, "range", "7.4")
        and _eq(c, "environment", "sanvat")
        and _eq(c, "vowel_weight", "hrasva")
        and _eq(c, "suffix", "caṅ")
        and _retroflex_context(c)
        and bool(c.get("aglopa")) is False
    )

def sutra_7_4_94(c) -> bool:
    """dīrgho laghoḥ: dīrgha of light vowel (ṇati context)."""
    return _eq(c, "range", "7.4") and _eq(c, "vowel_weight", "dīrgha") and _eq(c, "environment", "laghu")

def sutra_7_4_95(c) -> bool:
    """at smṛdṛtvarapṛthamradastrirspśām: at in listed gaṇa."""
    return _eq(c, "range", "7.4") and _in(c, "stem", _GANA_7_4_95) and _eq(c, "augment", "at")

def sutra_7_4_96(c) -> bool:
    """vibhāṣā veṣṭiceṣṭyoḥ: optional in veṣṭi-ceṣṭi."""
    return _eq(c, "range", "7.4") and _eq(c, "stem_group", "veṣṭiceṣṭi") and bool(c.get("optional"))

def sutra_7_4_97(c) -> bool:
    """ī ca gaṇaḥ: ī gaṇa marker (chandasi class)."""
    return _eq(c, "range", "7.4") and _in(c, "stem", _GANA_7_4_97) and _eq(c, "rule", "gaṇa") and _eq(c, "stem_final", "ī")

def _fx_pair(pos: dict, neg: dict) -> tuple[dict, dict]:
    return (pos, neg)

FIXTURES: dict[str, tuple[dict, dict]] = {
    "7.4.1": _fx_pair({'range': '7.4', 'suffix': 'ṇau', 'environment': 'caṅ', 'vowel_weight': 'hrasva', 'upadhā': 'a'}, {'range': '7.4', 'suffix': 'ṇau', 'environment': 'caṅ', 'vowel_weight': 'dīrgha', 'upadhā': 'a'}),
    "7.4.2": _fx_pair({'range': '7.4', 'rule_blocked': True, 'environment': 'aglopiśāsṛdit'}, {'range': '7.4', 'rule_blocked': False, 'environment': 'aglopiśāsṛdit'}),
    "7.4.3": _fx_pair(
        {'range': '7.4', 'stem': 'bhraj', 'optional': True, 'operation': 'ṇati', 'stem_form': 'bhrañj'},
        {'range': '7.4', 'stem': 'pac', 'optional': True, 'operation': 'lopa'},
    ),
    "7.4.4": _fx_pair({'range': '7.4', 'operation': 'lopa', 'environment': 'abhyāsa', 'dhatu': 'pib', 'augment': 'īt'}, {'range': '7.4', 'operation': 'lopa', 'environment': 'lot', 'dhatu': 'pib', 'augment': 'īt'}),
    "7.4.5": _fx_pair({'range': '7.4', 'dhatu': 'stha', 'augment': 'it', 'operation': 'agama'}, {'range': '7.4', 'dhatu': 'pac', 'augment': 'it', 'operation': 'agama'}),
    "7.4.6": _fx_pair({'range': '7.4', 'dhatu': 'jighr', 'augment': 'it', 'optional': True}, {'range': '7.4', 'dhatu': 'jighr', 'augment': 'it', 'optional': False}),
    "7.4.7": _fx_pair({'range': '7.4', 'stem_final': 'u', 'augment': 'ṛt', 'operation': 'agama'}, {'range': '7.4', 'stem_final': 'i', 'augment': 'ṛt', 'operation': 'agama'}),
    "7.4.8": _fx_pair({'range': '7.4', 'environment': 'chandas', 'rule': 'nitya'}, {'range': '7.4', 'environment': 'loka', 'rule': 'nitya'}),
    "7.4.9": _fx_pair({'range': '7.4', 'dhatu': 'day', 'environment': 'dig', 'lakara': 'liṭ'}, {'range': '7.4', 'dhatu': 'day', 'environment': 'dig', 'lakara': 'laṭ'}),
    "7.4.10": _fx_pair({'range': '7.4', 'stem_final': 'ṛ', 'operation': 'guṇa', 'environment': 'saṃyogādi'}, {'range': '7.4', 'stem_final': 'ṛ', 'operation': 'lopa', 'environment': 'saṃyogādi'}),
    "7.4.11": _fx_pair({'range': '7.4', 'stem': 'ricch', 'operation': 'ṇati'}, {'range': '7.4', 'stem': 'pac', 'operation': 'ṇati'}),
    "7.4.12": _fx_pair({'range': '7.4', 'stem': 'shrid', 'vowel_weight': 'hrasva', 'optional': True}, {'range': '7.4', 'stem': 'shrid', 'vowel_weight': 'dīrgha', 'optional': True}),
    "7.4.13": _fx_pair({'range': '7.4', 'environment': 'ke', 'operation': 'ṇati', 'suffix': 'ṇa'}, {'range': '7.4', 'environment': 'ṅi', 'operation': 'ṇati', 'suffix': 'ṇa'}),
    "7.4.14": _fx_pair({'range': '7.4', 'environment': 'kapi', 'rule_blocked': True}, {'range': '7.4', 'environment': 'kapi', 'rule_blocked': False}),
    "7.4.15": _fx_pair({'range': '7.4', 'stem': 'ap', 'optional': True, 'operation': 'substitution'}, {'range': '7.4', 'stem': 'ud', 'optional': True, 'operation': 'substitution'}),
    "7.4.16": _fx_pair({'range': '7.4', 'stem_group': 'ridrish', 'suffix': 'aṅ', 'operation': 'guṇa'}, {'range': '7.4', 'stem_group': 'ridrish', 'suffix': 'śu', 'operation': 'guṇa'}),
    "7.4.17": _fx_pair({'range': '7.4', 'dhatu': 'as', 'augment': 'thuk'}, {'range': '7.4', 'dhatu': 'as', 'augment': 'it'}),
    "7.4.18": _fx_pair({'range': '7.4', 'dhatu': 'śvay', 'augment': 'aḥ'}, {'range': '7.4', 'dhatu': 'pac', 'augment': 'aḥ'}),
    "7.4.19": _fx_pair({'range': '7.4', 'dhatu': 'pat', 'augment': 'pum'}, {'range': '7.4', 'dhatu': 'pat', 'augment': 'it'}),
    "7.4.20": _fx_pair({'range': '7.4', 'dhatu': 'vac', 'augment': 'um'}, {'range': '7.4', 'dhatu': 'bhū', 'augment': 'um'}),
    "7.4.21": _fx_pair({'range': '7.4', 'dhatu': 'śī', 'environment': 'sārvadhātuka', 'operation': 'guṇa'}, {'range': '7.4', 'dhatu': 'śī', 'environment': 'ārdhadhātuka', 'operation': 'guṇa'}),
    "7.4.22": _fx_pair({'range': '7.4', 'augment': 'ayaṅ', 'environment': 'yi', 'suffix': 'kṅit'}, {'range': '7.4', 'augment': 'ayaṅ', 'environment': 'yi', 'suffix': 'śu'}),
    "7.4.23": _fx_pair({'range': '7.4', 'environment': 'upasarga', 'vowel_weight': 'hrasva', 'dhatu': 'ūh'}, {'range': '7.4', 'environment': 'upasarga', 'vowel_weight': 'dīrgha', 'dhatu': 'ūh'}),
    "7.4.24": _fx_pair({'range': '7.4', 'dhatu': 'i', 'lakara': 'liṅ', 'operation': 'substitution'}, {'range': '7.4', 'dhatu': 'i', 'lakara': 'laṭ', 'operation': 'substitution'}),
    "7.4.25": _fx_pair({'range': '7.4', 'vowel_weight': 'dīrgha', 'environment': 'akṛtsārvadhātuka'}, {'range': '7.4', 'vowel_weight': 'hrasva', 'environment': 'akṛtsārvadhātuka'}),
    "7.4.26": _fx_pair({'range': '7.4', 'suffix': 'cvau', 'rule': 'ca'}, {'range': '7.4', 'suffix': 'ṇau', 'rule': 'ca'}),
    "7.4.27": _fx_pair({'range': '7.4', 'augment': 'rīṅ', 'stem_final': 'ṛ'}, {'range': '7.4', 'augment': 'rīṅ', 'stem_final': 'a'}),
    "7.4.28": _fx_pair({'range': '7.4', 'augment': 'riṅ', 'environment': 'śayagliṅkṣu'}, {'range': '7.4', 'augment': 'riṅ', 'environment': 'lot'}),
    "7.4.29": _fx_pair({'range': '7.4', 'operation': 'guṇa', 'environment': 'artisaṃyogādi'}, {'range': '7.4', 'operation': 'lopa', 'environment': 'artisaṃyogādi'}),
    "7.4.30": _fx_pair({'range': '7.4', 'suffix': 'yaṅ', 'rule': 'ca'}, {'range': '7.4', 'suffix': 'ṇau', 'rule': 'ca'}),
    "7.4.31": _fx_pair({'range': '7.4', 'stem_group': 'ghradhm', 'stem_final': 'ī', 'operation': 'substitution'}, {'range': '7.4', 'stem_group': 'ghradhm', 'stem_final': 'i', 'operation': 'substitution'}),
    "7.4.32": _fx_pair({'range': '7.4', 'dhatu': 'as', 'suffix': 'cvau'}, {'range': '7.4', 'dhatu': 'as', 'suffix': 'śu'}),
    "7.4.33": _fx_pair({'range': '7.4', 'suffix': 'kyac', 'rule': 'ca'}, {'range': '7.4', 'suffix': 'ṇau', 'rule': 'ca'}),
    "7.4.34": _fx_pair({'range': '7.4', 'stem': 'bubhuksha', 'environment': 'bubhukṣādi'}, {'range': '7.4', 'stem': 'pac', 'environment': 'bubhukṣādi'}),
    "7.4.35": _fx_pair({'range': '7.4', 'environment': 'chandas', 'rule_blocked': True, 'semantic': 'aputra'}, {'range': '7.4', 'environment': 'chandas', 'rule_blocked': False, 'semantic': 'aputra'}),
    "7.4.36": _fx_pair({'range': '7.4', 'stem_group': 'durasya', 'suffix': 'yu', 'operation': 'agama'}, {'range': '7.4', 'stem_group': 'pac', 'suffix': 'yu', 'operation': 'agama'}),
    "7.4.37": _fx_pair({'range': '7.4', 'stem': 'aśvāgha', 'augment': 'āt'}, {'range': '7.4', 'stem': 'ratha', 'augment': 'āt'}),
    "7.4.38": _fx_pair({'range': '7.4', 'stem_group': 'devasumna', 'environment': 'yajus', 'authority': 'kāṭhaka'}, {'range': '7.4', 'stem_group': 'devasumna', 'environment': 'yajus', 'authority': 'śākala'}),
    "7.4.39": _fx_pair({'range': '7.4', 'operation': 'lopa', 'environment': 'ṛc', 'stem_group': 'kavyadhvarapṛtana'}, {'range': '7.4', 'operation': 'ṇati', 'environment': 'ṛc', 'stem_group': 'kavyadhvarapṛtana'}),
    "7.4.40": _fx_pair({'range': '7.4', 'stem_group': 'dyatisyatimāsthām', 'augment': 'it', 'suffix': 'kit'}, {'range': '7.4', 'stem_group': 'dyatisyatimāsthām', 'augment': 'it', 'suffix': 'śu'}),
    "7.4.41": _fx_pair({'range': '7.4', 'stem_group': 'śāccha', 'optional': True}, {'range': '7.4', 'stem_group': 'śāccha', 'optional': False}),
    "7.4.42": _fx_pair({'range': '7.4', 'dhatu': 'dhā', 'augment': 'hi'}, {'range': '7.4', 'dhatu': 'pac', 'augment': 'hi'}),
    "7.4.43": _fx_pair({'range': '7.4', 'dhatu': 'hā', 'suffix': 'ktv', 'operation': 'lopa'}, {'range': '7.4', 'dhatu': 'hā', 'suffix': 'ktv', 'operation': 'ṇati'}),
    "7.4.44": _fx_pair({'range': '7.4', 'environment': 'chandas', 'optional': True}, {'range': '7.4', 'environment': 'loka', 'optional': True}),
    "7.4.45": _fx_pair({'range': '7.4', 'stem_group': 'sudhit', 'rule': 'ca'}, {'range': '7.4', 'stem_group': 'pac', 'rule': 'ca'}),
    "7.4.46": _fx_pair({'range': '7.4', 'stem_final': 'd', 'substitute': 'dad', 'environment': 'gho'}, {'range': '7.4', 'stem_final': 'd', 'substitute': 'd', 'environment': 'gho'}),
    "7.4.47": _fx_pair({'range': '7.4', 'environment': 'upasarga', 'suffix': 'ac', 'augment': 'ta'}, {'range': '7.4', 'environment': 'upasarga', 'suffix': 'ac', 'augment': 'nuṭ'}),
    "7.4.48": _fx_pair({'range': '7.4', 'stem': 'ap', 'suffix': 'bhi'}, {'range': '7.4', 'stem': 'ap', 'suffix': 'su'}),
    "7.4.49": _fx_pair({'range': '7.4', 'stem_final': 's', 'suffix': 'si', 'environment': 'ārdhadhātuka'}, {'range': '7.4', 'stem_final': 's', 'suffix': 'si', 'environment': 'sārvadhātuka'}),
    "7.4.50": _fx_pair({'range': '7.4', 'operation': 'lopa', 'suffix_group': 'tāsasti'}, {'range': '7.4', 'operation': 'ṇati', 'suffix_group': 'tāsasti'}),
    "7.4.51": _fx_pair({'range': '7.4', 'suffix': 'ri', 'rule': 'ca'}, {'range': '7.4', 'suffix': 'ṇau', 'rule': 'ca'}),
    "7.4.52": _fx_pair({'range': '7.4', 'augment': 'ha', 'suffix': 'eti'}, {'range': '7.4', 'augment': 'ha', 'suffix': 'anti'}),
    "7.4.53": _fx_pair({'range': '7.4', 'stem_group': 'yīvarṇa', 'operation': 'dīdhī'}, {'range': '7.4', 'stem_group': 'yīvarṇa', 'operation': 'lopa'}),
    "7.4.54": _fx_pair({'range': '7.4', 'suffix': 'san', 'stem_group': 'mīmāghurabha', 'augment': 'is'}, {'range': '7.4', 'suffix': 'śu', 'stem_group': 'mīmāghurabha', 'augment': 'is'}),
    "7.4.55": _fx_pair({'range': '7.4', 'stem_group': 'āpjñapyṛdhā', 'augment': 'īt'}, {'range': '7.4', 'stem_group': 'āpjñapyṛdhā', 'augment': 'it'}),
    "7.4.56": _fx_pair({'range': '7.4', 'dhatu': 'dambh', 'augment': 'ic', 'rule': 'ca'}, {'range': '7.4', 'dhatu': 'pac', 'augment': 'ic', 'rule': 'ca'}),
    "7.4.57": _fx_pair({'range': '7.4', 'dhatu': 'muc', 'voice': 'akarmaka', 'operation': 'guṇa', 'optional': True}, {'range': '7.4', 'dhatu': 'muc', 'voice': 'sakarmaka', 'operation': 'guṇa', 'optional': True}),
    "7.4.58": _fx_pair({'range': '7.4', 'operation': 'lopa', 'environment': 'abhyāsa', 'rule': 'atra'}, {'range': '7.4', 'operation': 'lopa', 'environment': 'lot', 'rule': 'atra'}),
    "7.4.59": _fx_pair({'range': '7.4', 'vowel_weight': 'hrasva', 'environment': 'abhyāsa'}, {'range': '7.4', 'vowel_weight': 'dīrgha', 'environment': 'abhyāsa'}),
    "7.4.60": _fx_pair({'range': '7.4', 'environment': 'abhyāsa', 'condition': 'halādi', 'rule': 'śeṣa'}, {'range': '7.4', 'environment': 'abhyāsa', 'condition': 'vowelādi', 'rule': 'śeṣa'}),
    "7.4.61": _fx_pair({'range': '7.4', 'condition': 'śarpūrva', 'suffix': 'khaya'}, {'range': '7.4', 'condition': 'śarpūrva', 'suffix': 'ṇau'}),
    "7.4.62": _fx_pair({'range': '7.4', 'stem_group': 'kuh', 'substitute': 'cu'}, {'range': '7.4', 'stem_group': 'kuh', 'substitute': 'ku'}),
    "7.4.63": _fx_pair({'range': '7.4', 'dhatu': 'kavat', 'suffix': 'yaṅ', 'rule_blocked': True}, {'range': '7.4', 'dhatu': 'kavat', 'suffix': 'yaṅ', 'rule_blocked': False}),
    "7.4.64": _fx_pair({'range': '7.4', 'dhatu': 'kṛṣ', 'environment': 'chandas'}, {'range': '7.4', 'dhatu': 'kṛṣ', 'environment': 'loka'}),
    "7.4.65": _fx_pair({'range': '7.4', 'stem': 'dadharti', 'operation': 'ṇati'}, {'range': '7.4', 'stem': 'pac', 'operation': 'ṇati'}),
    "7.4.66": _fx_pair({'range': '7.4', 'stem_final': 'u', 'augment': 'at'}, {'range': '7.4', 'stem_final': 'u', 'augment': 'ṛt'}),
    "7.4.67": _fx_pair({'range': '7.4', 'stem_group': 'dyutisvāpya', 'operation': 'samprasāraṇa'}, {'range': '7.4', 'stem_group': 'dyutisvāpya', 'operation': 'guṇa'}),
    "7.4.68": _fx_pair({'range': '7.4', 'dhatu': 'vyath', 'lakara': 'liṭ'}, {'range': '7.4', 'dhatu': 'vyath', 'lakara': 'laṭ'}),
    "7.4.69": _fx_pair({'range': '7.4', 'vowel_weight': 'dīrgha', 'environment': 'iṇ', 'suffix': 'kit'}, {'range': '7.4', 'vowel_weight': 'hrasva', 'environment': 'iṇ', 'suffix': 'kit'}),
    "7.4.70": _fx_pair({'range': '7.4', 'stem_final': 'a', 'operation': 'ādeśa'}, {'range': '7.4', 'stem_final': 'a', 'operation': 'lopa'}),
    "7.4.71": _fx_pair({'range': '7.4', 'environment': 'tasmāt', 'augment': 'nuṭ', 'condition': 'dvihal'}, {'range': '7.4', 'environment': 'tasmāt', 'augment': 'it', 'condition': 'dvihal'}),
    "7.4.72": _fx_pair({'range': '7.4', 'dhatu': 'aśnot', 'rule': 'ca'}, {'range': '7.4', 'dhatu': 'aśnot', 'rule': 'na'}),
    "7.4.73": _fx_pair({'range': '7.4', 'dhatu': 'bhū', 'augment': 'aḥ'}, {'range': '7.4', 'dhatu': 'bhū', 'augment': 'it'}),
    "7.4.74": _fx_pair({'range': '7.4', 'form': 'sasūva', 'environment': 'nigama'}, {'range': '7.4', 'form': 'sasūva', 'environment': 'loka'}),
    "7.4.75": _fx_pair({'range': '7.4', 'stem_group': 'nij', 'operation': 'guṇa', 'suffix': 'ślu'}, {'range': '7.4', 'stem_group': 'nij', 'operation': 'lopa', 'suffix': 'ślu'}),
    "7.4.76": _fx_pair({'range': '7.4', 'stem_group': 'bhṛñ', 'augment': 'it'}, {'range': '7.4', 'stem_group': 'bhṛñ', 'augment': 'īt'}),
    "7.4.77": _fx_pair({'range': '7.4', 'stem_group': 'artipiparti', 'rule': 'ca'}, {'range': '7.4', 'stem_group': 'pac', 'rule': 'ca'}),
    "7.4.78": _fx_pair({'range': '7.4', 'rule': 'bahula', 'environment': 'chandas'}, {'range': '7.4', 'rule': 'bahula', 'environment': 'loka'}),
    "7.4.79": _fx_pair({'range': '7.4', 'suffix': 'san', 'augment': 'ata'}, {'range': '7.4', 'suffix': 'śu', 'augment': 'ata'}),
    "7.4.80": _fx_pair({'range': '7.4', 'stem_final': 'o', 'suffix': 'puñaji', 'position': 'apara'}, {'range': '7.4', 'stem_final': 'o', 'suffix': 'puñaji', 'position': 'para'}),
    "7.4.81": _fx_pair({'range': '7.4', 'stem_group': 'sravati', 'optional': True}, {'range': '7.4', 'stem_group': 'sravati', 'optional': False}),
    "7.4.82": _fx_pair({'range': '7.4', 'operation': 'guṇa', 'environment': 'yaṅluk'}, {'range': '7.4', 'operation': 'lopa', 'environment': 'yaṅluk'}),
    "7.4.83": _fx_pair({'range': '7.4', 'vowel_weight': 'dīrgha', 'environment': 'akita'}, {'range': '7.4', 'vowel_weight': 'dīrgha', 'environment': 'kita'}),
    "7.4.84": _fx_pair({'range': '7.4', 'stem': 'nik', 'operation': 'ṇati'}, {'range': '7.4', 'stem': 'pac', 'operation': 'ṇati'}),
    "7.4.85": _fx_pair({'range': '7.4', 'augment': 'nuk', 'environment': 'anunāsikānta'}, {'range': '7.4', 'augment': 'it', 'environment': 'anunāsikānta'}),
    "7.4.86": _fx_pair({'range': '7.4', 'stem': 'jap', 'rule': 'ca'}, {'range': '7.4', 'stem': 'pac', 'rule': 'ca'}),
    "7.4.87": _fx_pair({'range': '7.4', 'stem_group': 'caraphal', 'rule': 'ca'}, {'range': '7.4', 'stem_group': 'caraphal', 'rule': 'na'}),
    "7.4.88": _fx_pair({'range': '7.4', 'augment': 'ut', 'relation': 'parasya', 'stem_final': 'a'}, {'range': '7.4', 'augment': 'it', 'relation': 'parasya', 'stem_final': 'a'}),
    "7.4.89": _fx_pair({'range': '7.4', 'suffix': 'ti', 'rule': 'ca'}, {'range': '7.4', 'suffix': 'ṇau', 'rule': 'ca'}),
    "7.4.90": _fx_pair({'range': '7.4', 'condition': 'ṛgṛdupadhā', 'rule': 'ca'}, {'range': '7.4', 'condition': 'ikopadhā', 'rule': 'ca'}),
    "7.4.91": _fx_pair({'range': '7.4', 'stem_group': 'rugrīka', 'environment': 'luk', 'rule': 'ca'}, {'range': '7.4', 'stem_group': 'rugrīka', 'environment': 'lot', 'rule': 'ca'}),
    "7.4.92": _fx_pair({'range': '7.4', 'stem_final': 'ṛ', 'rule': 'ca'}, {'range': '7.4', 'stem_final': 'a', 'rule': 'ca'}),
    "7.4.93": _fx_pair({'range': '7.4', 'environment': 'sanvat', 'vowel_weight': 'hrasva', 'suffix': 'caṅ', 'operation': 'ṇati', 'aglopa': False}, {'range': '7.4', 'environment': 'sanvat', 'vowel_weight': 'hrasva', 'suffix': 'caṅ', 'operation': 'ṇati', 'aglopa': True}),
    "7.4.94": _fx_pair({'range': '7.4', 'vowel_weight': 'dīrgha', 'environment': 'laghu'}, {'range': '7.4', 'vowel_weight': 'hrasva', 'environment': 'laghu'}),
    "7.4.95": _fx_pair({'range': '7.4', 'stem': 'smr', 'augment': 'at'}, {'range': '7.4', 'stem': 'pac', 'augment': 'at'}),
    "7.4.96": _fx_pair({'range': '7.4', 'stem_group': 'veṣṭiceṣṭi', 'optional': True}, {'range': '7.4', 'stem_group': 'veṣṭiceṣṭi', 'optional': False}),
    "7.4.97": _fx_pair({'range': '7.4', 'stem': 'i', 'rule': 'gaṇa', 'stem_final': 'ī'}, {'range': '7.4', 'stem': 'i', 'rule': 'vidhi', 'stem_final': 'ī'}),
}

META: dict[str, SutraMeta] = {
    "7.4.1": SutraMeta(_SAMJNA, "णौ चङ्युपधाया ह्रस्वः ।", ("domain:nati_lopa", "pada:7.4", "7_4_1")),
    "7.4.2": SutraMeta(_PRATISEDHA, "नाग्लोपिशास्वृदिताम् ।", ("domain:nati_lopa", "pada:7.4", "7_4_2")),
    "7.4.3": SutraMeta(_VIDHI, "भ्राजभासभाषदीपजीवमीलपीडामन्यतरस्याम्‌ ।", ("domain:nati_lopa", "pada:7.4", "7_4_3")),
    "7.4.4": SutraMeta(_VIDHI, "लोपः पिबतेरीच्चाभ्यासस्य ।", ("domain:nati_lopa", "pada:7.4", "7_4_4")),
    "7.4.5": SutraMeta(_VIDHI, "तिष्ठतेरित्‌ ।", ("domain:nati_lopa", "pada:7.4", "7_4_5")),
    "7.4.6": SutraMeta(_VIDHI, "जिघ्रतेर्वा ।", ("domain:nati_lopa", "pada:7.4", "7_4_6")),
    "7.4.7": SutraMeta(_VIDHI, "उर्ऋत्‌ ।", ("domain:nati_lopa", "pada:7.4", "7_4_7")),
    "7.4.8": SutraMeta(_VIDHI, "नित्यं छन्दसि ।", ("domain:nati_lopa", "pada:7.4", "7_4_8")),
    "7.4.9": SutraMeta(_VIDHI, "दयतेर्दिगि लिटि ।", ("domain:nati_lopa", "pada:7.4", "7_4_9")),
    "7.4.10": SutraMeta(_VIDHI, "ऋतश्च संयोगादेर्गुणः ।", ("domain:nati_lopa", "pada:7.4", "7_4_10")),
    "7.4.11": SutraMeta(_VIDHI, "ऋच्छत्यॄताम् ।", ("domain:nati_lopa", "pada:7.4", "7_4_11")),
    "7.4.12": SutraMeta(_VIDHI, "शृदॄप्रां ह्रस्वो वा ।", ("domain:nati_lopa", "pada:7.4", "7_4_12")),
    "7.4.13": SutraMeta(_VIDHI, "केऽणः ।", ("domain:nati_lopa", "pada:7.4", "7_4_13")),
    "7.4.14": SutraMeta(_VIDHI, "न कपि ।", ("domain:nati_lopa", "pada:7.4", "7_4_14")),
    "7.4.15": SutraMeta(_VIDHI, "आपोऽन्यतरस्याम् ।", ("domain:nati_lopa", "pada:7.4", "7_4_15")),
    "7.4.16": SutraMeta(_VIDHI, "ऋदृशोऽङि गुणः ।", ("domain:nati_lopa", "pada:7.4", "7_4_16")),
    "7.4.17": SutraMeta(_VIDHI, "अस्यतेस्थुक् ।", ("domain:nati_lopa", "pada:7.4", "7_4_17")),
    "7.4.18": SutraMeta(_VIDHI, "श्वयतेरः ।", ("domain:nati_lopa", "pada:7.4", "7_4_18")),
    "7.4.19": SutraMeta(_VIDHI, "पतः पुम् ।", ("domain:nati_lopa", "pada:7.4", "7_4_19")),
    "7.4.20": SutraMeta(_VIDHI, "वच उम् ।", ("domain:nati_lopa", "pada:7.4", "7_4_20")),
    "7.4.21": SutraMeta(_VIDHI, "शीङः सार्वधातुके गुणः ।", ("domain:nati_lopa", "pada:7.4", "7_4_21")),
    "7.4.22": SutraMeta(_VIDHI, "अयङ् यि क्ङिति ।", ("domain:nati_lopa", "pada:7.4", "7_4_22")),
    "7.4.23": SutraMeta(_VIDHI, "उपसर्गाद्ध्रस्व ऊहतेः ।", ("domain:nati_lopa", "pada:7.4", "7_4_23")),
    "7.4.24": SutraMeta(_VIDHI, "एतेर्लिङि ।", ("domain:nati_lopa", "pada:7.4", "7_4_24")),
    "7.4.25": SutraMeta(_VIDHI, "अकृत्सार्वधातुकयोर्दीर्घः ।", ("domain:nati_lopa", "pada:7.4", "7_4_25")),
    "7.4.26": SutraMeta(_VIDHI, "च्वौ च ।", ("domain:nati_lopa", "pada:7.4", "7_4_26")),
    "7.4.27": SutraMeta(_VIDHI, "रीङ् ऋतः ।", ("domain:nati_lopa", "pada:7.4", "7_4_27")),
    "7.4.28": SutraMeta(_VIDHI, "रिङ् शयग्लिङ्क्षु ।", ("domain:nati_lopa", "pada:7.4", "7_4_28")),
    "7.4.29": SutraMeta(_VIDHI, "गुणोऽर्तिसंयोगाद्योः ।", ("domain:nati_lopa", "pada:7.4", "7_4_29")),
    "7.4.30": SutraMeta(_VIDHI, "यङि च ।", ("domain:nati_lopa", "pada:7.4", "7_4_30")),
    "7.4.31": SutraMeta(_VIDHI, "ई घ्राध्मोः ।", ("domain:nati_lopa", "pada:7.4", "7_4_31")),
    "7.4.32": SutraMeta(_VIDHI, "अस्य च्वौ ।", ("domain:nati_lopa", "pada:7.4", "7_4_32")),
    "7.4.33": SutraMeta(_VIDHI, "क्यचि च ।", ("domain:nati_lopa", "pada:7.4", "7_4_33")),
    "7.4.34": SutraMeta(_VIDHI, "अशनायोदन्यधनाया बुभुक्षापिपासागर्द्धेषु ।", ("domain:nati_lopa", "pada:7.4", "7_4_34")),
    "7.4.35": SutraMeta(_VIDHI, "न च्छन्दस्यपुत्रस्य ।", ("domain:nati_lopa", "pada:7.4", "7_4_35")),
    "7.4.36": SutraMeta(_VIDHI, "दुरस्युर्द्रविणस्युर्वृषण्यतिरिषण्यति ।", ("domain:nati_lopa", "pada:7.4", "7_4_36")),
    "7.4.37": SutraMeta(_VIDHI, "अश्वाघस्यात्‌ ।", ("domain:nati_lopa", "pada:7.4", "7_4_37")),
    "7.4.38": SutraMeta(_VIDHI, "देवसुम्नयोर्यजुषि काठके ।", ("domain:nati_lopa", "pada:7.4", "7_4_38")),
    "7.4.39": SutraMeta(_VIDHI, "कव्यध्वरपृतनस्यर्चि लोपः ।", ("domain:nati_lopa", "pada:7.4", "7_4_39")),
    "7.4.40": SutraMeta(_VIDHI, "द्यतिस्यतिमास्थामित्ति किति ।", ("domain:nati_lopa", "pada:7.4", "7_4_40")),
    "7.4.41": SutraMeta(_VIDHI, "शाछोरन्यतरस्याम् ।", ("domain:nati_lopa", "pada:7.4", "7_4_41")),
    "7.4.42": SutraMeta(_VIDHI, "दधातेर्हिः ।", ("domain:nati_lopa", "pada:7.4", "7_4_42")),
    "7.4.43": SutraMeta(_VIDHI, "जहातेश्च क्त्वि ।", ("domain:nati_lopa", "pada:7.4", "7_4_43")),
    "7.4.44": SutraMeta(_VIBHASHA, "विभाषा छन्दसि ।", ("domain:nati_lopa", "pada:7.4", "7_4_44")),
    "7.4.45": SutraMeta(_VIDHI, "सुधितवसुधितनेमधितधिष्वधिषीय च ।", ("domain:nati_lopa", "pada:7.4", "7_4_45")),
    "7.4.46": SutraMeta(_VIDHI, "दो दद् घोः ।", ("domain:nati_lopa", "pada:7.4", "7_4_46")),
    "7.4.47": SutraMeta(_VIDHI, "अच उपसर्गात्तः ।", ("domain:nati_lopa", "pada:7.4", "7_4_47")),
    "7.4.48": SutraMeta(_VIDHI, "अपो भि ।", ("domain:nati_lopa", "pada:7.4", "7_4_48")),
    "7.4.49": SutraMeta(_VIDHI, "सः स्यार्द्धधातुके ।", ("domain:nati_lopa", "pada:7.4", "7_4_49")),
    "7.4.50": SutraMeta(_VIDHI, "तासस्त्योर्लोपः ।", ("domain:nati_lopa", "pada:7.4", "7_4_50")),
    "7.4.51": SutraMeta(_VIDHI, "रि च ।", ("domain:nati_lopa", "pada:7.4", "7_4_51")),
    "7.4.52": SutraMeta(_VIDHI, "ह एति ।", ("domain:nati_lopa", "pada:7.4", "7_4_52")),
    "7.4.53": SutraMeta(_VIDHI, "यीवर्णयोर्दीधीवेव्योः ।", ("domain:nati_lopa", "pada:7.4", "7_4_53")),
    "7.4.54": SutraMeta(_VIDHI, "सनि मीमाघुरभलभशकपतपदामच इस् ।", ("domain:nati_lopa", "pada:7.4", "7_4_54")),
    "7.4.55": SutraMeta(_VIDHI, "आप्ज्ञप्यृधामीत्‌ ।", ("domain:nati_lopa", "pada:7.4", "7_4_55")),
    "7.4.56": SutraMeta(_VIDHI, "दम्भ इच्च ।", ("domain:nati_lopa", "pada:7.4", "7_4_56")),
    "7.4.57": SutraMeta(_VIDHI, "मुचोऽकर्मकस्य गुणो वा ।", ("domain:nati_lopa", "pada:7.4", "7_4_57")),
    "7.4.58": SutraMeta(_VIDHI, "अत्र लोपोऽभ्यासस्य ।", ("domain:nati_lopa", "pada:7.4", "7_4_58")),
    "7.4.59": SutraMeta(_VIDHI, "ह्रस्वः ।", ("domain:nati_lopa", "pada:7.4", "7_4_59")),
    "7.4.60": SutraMeta(_VIDHI, "हलादिः शेषः ।", ("domain:nati_lopa", "pada:7.4", "7_4_60")),
    "7.4.61": SutraMeta(_VIDHI, "शर्पूर्वाः खयः ।", ("domain:nati_lopa", "pada:7.4", "7_4_61")),
    "7.4.62": SutraMeta(_VIDHI, "कुहोश्चुः ।", ("domain:nati_lopa", "pada:7.4", "7_4_62")),
    "7.4.63": SutraMeta(_VIDHI, "न कवतेर्यङि ।", ("domain:nati_lopa", "pada:7.4", "7_4_63")),
    "7.4.64": SutraMeta(_VIDHI, "कृषेश्छन्दसि ।", ("domain:nati_lopa", "pada:7.4", "7_4_64")),
    "7.4.65": SutraMeta(_VIDHI, "दाधर्तिदर्धर्तिदर्धर्षिबोभूतुतेतिक्तेऽलर्ष्यापनीफणत्संसनिष्यदत्करिक्रत्कनिक्रदद्भरिभ्रद्दविध्वतोदविद्युतत्तरित्रतःसरीसृपतंवरीवृजन्मर्मृज्यागनीगन्तीति च ।", ("domain:nati_lopa", "pada:7.4", "7_4_65")),
    "7.4.66": SutraMeta(_VIDHI, "उरत्‌ ।", ("domain:nati_lopa", "pada:7.4", "7_4_66")),
    "7.4.67": SutraMeta(_VIDHI, "द्युतिस्वाप्योः सम्प्रसारणम् ।", ("domain:nati_lopa", "pada:7.4", "7_4_67")),
    "7.4.68": SutraMeta(_VIDHI, "व्यथो लिटि ।", ("domain:nati_lopa", "pada:7.4", "7_4_68")),
    "7.4.69": SutraMeta(_VIDHI, "दीर्घ इणः किति ।", ("domain:nati_lopa", "pada:7.4", "7_4_69")),
    "7.4.70": SutraMeta(_VIDHI, "अत आदेः ।", ("domain:nati_lopa", "pada:7.4", "7_4_70")),
    "7.4.71": SutraMeta(_VIDHI, "तस्मान्नुड् द्विहलः ।", ("domain:nati_lopa", "pada:7.4", "7_4_71")),
    "7.4.72": SutraMeta(_VIDHI, "अश्नोतेश्च ।", ("domain:nati_lopa", "pada:7.4", "7_4_72")),
    "7.4.73": SutraMeta(_VIDHI, "भवतेरः ।", ("domain:nati_lopa", "pada:7.4", "7_4_73")),
    "7.4.74": SutraMeta(_VIDHI, "ससूवेति निगमे ।", ("domain:nati_lopa", "pada:7.4", "7_4_74")),
    "7.4.75": SutraMeta(_VIDHI, "निजां त्रयाणां गुणः श्लौ ।", ("domain:nati_lopa", "pada:7.4", "7_4_75")),
    "7.4.76": SutraMeta(_VIDHI, "भृञामित्‌ ।", ("domain:nati_lopa", "pada:7.4", "7_4_76")),
    "7.4.77": SutraMeta(_VIDHI, "अर्तिपिपर्त्योश्च ।", ("domain:nati_lopa", "pada:7.4", "7_4_77")),
    "7.4.78": SutraMeta(_PARIBHASHA, "बहुलं छन्दसि ।", ("domain:nati_lopa", "pada:7.4", "7_4_78")),
    "7.4.79": SutraMeta(_VIDHI, "सन्यतः ।", ("domain:nati_lopa", "pada:7.4", "7_4_79")),
    "7.4.80": SutraMeta(_VIDHI, "ओः पुयण्ज्यपरे ।", ("domain:nati_lopa", "pada:7.4", "7_4_80")),
    "7.4.81": SutraMeta(_VIDHI, "स्रवतिशृणोतिद्रवतिप्रवतिप्लवतिच्यवतीनां वा ।", ("domain:nati_lopa", "pada:7.4", "7_4_81")),
    "7.4.82": SutraMeta(_VIDHI, "गुणो यङ्लुकोः ।", ("domain:nati_lopa", "pada:7.4", "7_4_82")),
    "7.4.83": SutraMeta(_VIDHI, "दीर्घोऽकितः ।", ("domain:nati_lopa", "pada:7.4", "7_4_83")),
    "7.4.84": SutraMeta(_VIDHI, "नीग्वञ्चुस्रंसुध्वंसुभ्रंसुकसपतपदस्कन्दाम् ।", ("domain:nati_lopa", "pada:7.4", "7_4_84")),
    "7.4.85": SutraMeta(_VIDHI, "नुगतोऽनुनासिकान्तस्य ।", ("domain:nati_lopa", "pada:7.4", "7_4_85")),
    "7.4.86": SutraMeta(_VIDHI, "जपजभदहदशभञ्जपशां च ।", ("domain:nati_lopa", "pada:7.4", "7_4_86")),
    "7.4.87": SutraMeta(_VIDHI, "चरफलोश्च ।", ("domain:nati_lopa", "pada:7.4", "7_4_87")),
    "7.4.88": SutraMeta(_VIDHI, "उत्‌ परस्यातः ।", ("domain:nati_lopa", "pada:7.4", "7_4_88")),
    "7.4.89": SutraMeta(_VIDHI, "ति च ।", ("domain:nati_lopa", "pada:7.4", "7_4_89")),
    "7.4.90": SutraMeta(_VIDHI, "रीगृदुपधस्य च ।", ("domain:nati_lopa", "pada:7.4", "7_4_90")),
    "7.4.91": SutraMeta(_VIDHI, "रुग्रिकौ च लुकि ।", ("domain:nati_lopa", "pada:7.4", "7_4_91")),
    "7.4.92": SutraMeta(_VIDHI, "ऋतश्च ।", ("domain:nati_lopa", "pada:7.4", "7_4_92")),
    "7.4.93": SutraMeta(_VIDHI, "सन्वल्लघुनि चङ्परेऽनग्लोपे ।", ("domain:nati_lopa", "pada:7.4", "7_4_93")),
    "7.4.94": SutraMeta(_VIDHI, "दीर्घो लघोः ।", ("domain:nati_lopa", "pada:7.4", "7_4_94")),
    "7.4.95": SutraMeta(_VIDHI, "अत्‌ स्मृदृत्वरप्रथम्रदस्तॄस्पशाम् ।", ("domain:nati_lopa", "pada:7.4", "7_4_95")),
    "7.4.96": SutraMeta(_VIBHASHA, "विभाषा वेष्टिचेष्ट्योः ।", ("domain:nati_lopa", "pada:7.4", "7_4_96")),
    "7.4.97": SutraMeta(_SAMJNA, "ई च गणः ।", ("domain:nati_lopa", "pada:7.4", "7_4_97")),
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
        raise AssertionError("sutra_impl_7_4 self_check failed:\n" + "\n".join(failures))
    handlers = [n for n in globals() if n.startswith("sutra_7_4_") and callable(globals()[n])]
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

