"""Discrete Pāṇinian predicates for the 201 Adhyāya-1 sūtras (in pādas 1.2,
1.3, 1.4) that were absent from the inline registry in ``sutra_logic``.

Each function tests the specific condition the sūtra names — kit/ṅit
exceptions, accent classes, prātipadika and upasarjana definitions,
ekaśeṣa rules, prefix-+-root ātmanepada/parasmaipada selectors, kāraka
extensions, nipāta/gati/upasarga/karmapravacanīya senses, and tiṅ-suffix
person-number-label saṁjñās. Every predicate is paired with a positive
fixture (Pāṇini's canonical example) and a near-miss negative.

The module is wired into the main truth-gate registry via
:func:`sutra_impl_base.register_module_in_registry`. The shared META
table carries the operator class, summary, and assigned tags per sūtra
so no per-sūtra ``_add(...)`` call is needed in ``sutra_logic``.
"""
from __future__ import annotations

from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _prefix(c) -> str:
    """Return the first explicit prefix in the context, or ''. Handles both
    a ``prefixes`` tuple and a single ``prefix`` string."""
    pres = c.get("prefixes")
    if pres:
        return str(pres[0])
    return str(c.get("prefix", ""))


def _has_prefix(c, *needed: str) -> bool:
    pres = tuple(c.get("prefixes", ()))
    if pres:
        return any(p in pres for p in needed)
    return c.get("prefix") in needed


# ===========================================================================
# Adhyāya 1.2 — kit/ṅit residue, accent saṁjñās, prātipadika/upasarjana,
#                lup/luk number rules, strī-puṁvat (45 sūtras)
# ===========================================================================

# 1.2.3 vibhāṣorṇoḥ: optional kit/ṅit treatment after root ūrṇu
def sutra_1_2_3(c) -> bool:
    return _eq(c, "lemma", "ūrṇu") and bool(c.get("optional"))


# 1.2.10 halantāc ca: san after hal-final ik-root is kit before jhal
def sutra_1_2_10(c) -> bool:
    return (_eq(c, "suffix", "san")
            and bool(c.get("root_ends_hal"))
            and bool(c.get("root_has_ik_upadha"))
            and _eq(c, "following", "jhal"))


# 1.2.16 vibhāṣopayamane: kit/aṅit is optional for marriage-sense yam
def sutra_1_2_16(c) -> bool:
    return _eq(c, "lemma", "yam") and _eq(c, "semantic", "upayamana") and bool(c.get("optional"))


# 1.2.21 udupadhād bhāvādikarmaṇoḥ: optional in bhāva/ādikarman with u-upadhā
def sutra_1_2_21(c) -> bool:
    return _eq(c, "upadha", "u") and _in(c, "semantic", {"bhava", "adikarman"}) and bool(c.get("optional"))


# 1.2.22 pūṅaḥ ktvā ca: ktvā after pū is kit (with ca, also san)
def sutra_1_2_22(c) -> bool:
    return _eq(c, "lemma", "pū") and _in(c, "suffix", {"ktvā", "san"})


# 1.2.23 nopadhāt thaphāntād vā: optional after na-upadhā tha/pha-final
def sutra_1_2_23(c) -> bool:
    return (_eq(c, "upadha", "n")
            and _in(c, "final", {"th", "ph"})
            and bool(c.get("optional")))


# 1.2.24 vañci-luñci-ṛtaś ca: optional kit for the listed roots
def sutra_1_2_24(c) -> bool:
    return _in(c, "lemma", {"vañc", "luñc", "ṛt"}) and bool(c.get("optional"))


# 1.2.25 tṛṣi-mṛṣi-kṛśeḥ kāśyapasya: per Kāśyapa, kit-optional for tṛṣ/mṛṣ/kṛś
def sutra_1_2_25(c) -> bool:
    return _in(c, "lemma", {"tṛṣ", "mṛṣ", "kṛś"}) and bool(c.get("optional"))


# 1.2.27 ūkālo'jjhrasvadīrghaplutaḥ: vowels have three durations (hrasva/dīrgha/pluta)
def sutra_1_2_27(c) -> bool:
    return _in(c, "duration", {"hrasva", "dirgha", "pluta"})


# 1.2.28 acaś ca: same applies to all ac (vowels)
def sutra_1_2_28(c) -> bool:
    return bool(c.get("is_ac")) and _in(c, "duration", {"hrasva", "dirgha", "pluta"})


# 1.2.29 uccair udāttaḥ: high-pitch is udātta
def sutra_1_2_29(c) -> bool:
    return _eq(c, "pitch", "high") and _eq(c, "accent", "udatta")


# 1.2.30 nīcair anudāttaḥ: low-pitch is anudātta
def sutra_1_2_30(c) -> bool:
    return _eq(c, "pitch", "low") and _eq(c, "accent", "anudatta")


# 1.2.31 samāhāraḥ svaritaḥ: combined-pitch is svarita
def sutra_1_2_31(c) -> bool:
    return _eq(c, "pitch", "combined") and _eq(c, "accent", "svarita")


# 1.2.32 tasyāditā udāttam ardha-hrasvam: first half-mātrā of svarita is udātta
def sutra_1_2_32(c) -> bool:
    return _eq(c, "accent", "svarita") and _eq(c, "initial_half", "udatta")


# 1.2.33 ekaśruti dūrāt sambuddhau: from a distance, vocative is monotone
def sutra_1_2_33(c) -> bool:
    return bool(c.get("is_sambuddhi")) and bool(c.get("is_from_distance")) and _eq(c, "accent", "ekashruti")


# 1.2.34 yajñakarmaṇy ajapanyūṅkhasāmasu: in yajña ritual, ekaśruti except in japa/nyūṅkha/sāman
def sutra_1_2_34(c) -> bool:
    return (_eq(c, "context", "yajna_karman")
            and not _in(c, "subdomain", {"japa", "nyunkha", "saman"})
            and _eq(c, "accent", "ekashruti"))


# 1.2.35 uccaistarāṃ vā vaṣaṭkāraḥ: vaṣaṭ optionally has stronger udātta
def sutra_1_2_35(c) -> bool:
    return _eq(c, "word", "vaṣaṭ") and bool(c.get("optional")) and _eq(c, "accent", "udattatara")


# 1.2.36 vibhāṣā chandasi: in Vedic, the same is optional (chandasi vibhāṣā)
def sutra_1_2_36(c) -> bool:
    return bool(c.get("is_vedic")) and bool(c.get("optional"))


# 1.2.37 na subrahmaṇyāyāṃ svaritasya tūdāttaḥ: in subrahmaṇyā chant, svarita becomes udātta
def sutra_1_2_37(c) -> bool:
    return _eq(c, "context", "subrahmanya") and _eq(c, "input_accent", "svarita") and _eq(c, "output_accent", "udatta")


# 1.2.38 devabrahmaṇor anudāttaḥ: deva and brahman take anudātta
def sutra_1_2_38(c) -> bool:
    return _in(c, "word", {"deva", "brahman"}) and _eq(c, "accent", "anudatta")


# 1.2.39 svaritāt saṃhitāyām anudāttānām: after svarita in saṃhitā, anudāttas
def sutra_1_2_39(c) -> bool:
    return _eq(c, "preceding_accent", "svarita") and bool(c.get("in_samhita")) and _eq(c, "accent", "anudatta")


# 1.2.40 udāttasvaritaparasya sannataraḥ: after udātta or svarita, lower than anudātta = sannatara
def sutra_1_2_40(c) -> bool:
    return _in(c, "preceding_accent", {"udatta", "svarita"}) and _eq(c, "accent", "sannatara")


# 1.2.42 tatpuruṣaḥ samānādhikaraṇaḥ karmadhārayaḥ: same-case tatpuruṣa is karmadhāraya
def sutra_1_2_42(c) -> bool:
    return _eq(c, "compound_type", "tatpurusha") and bool(c.get("is_samanadhikarana"))


# 1.2.43 prathamānirdiṣṭaṃ samāsa upasarjanam: the first-named member in a samāsa is upasarjana
def sutra_1_2_43(c) -> bool:
    return bool(c.get("in_compound")) and bool(c.get("is_first_named"))


# 1.2.44 ekavibhakti cāpūrvanipāte: a single-case member is also upasarjana when not in initial position
def sutra_1_2_44(c) -> bool:
    return bool(c.get("is_single_case_member")) and not bool(c.get("is_pre_compound_initial"))


# 1.2.45 arthavad adhātur apratyayaḥ prātipadikam: meaningful non-dhātu non-pratyaya = prātipadika
def sutra_1_2_45(c) -> bool:
    return (bool(c.get("is_meaningful"))
            and not bool(c.get("is_dhatu"))
            and not bool(c.get("is_pratyaya")))


# 1.2.46 kṛt-taddhita-samāsāś ca: kṛt-, taddhita-, and samāsa-derived bases are also prātipadika
def sutra_1_2_46(c) -> bool:
    return _in(c, "derivation_source", {"krt", "taddhita", "samasa"})


# 1.2.47 hrasvo napuṃsake prātipadikasya: neuter prātipadika's final vowel is shortened
def sutra_1_2_47(c) -> bool:
    return _eq(c, "gender", "neuter") and bool(c.get("is_pratipadika")) and bool(c.get("final_vowel_shortened"))


# 1.2.48 go-striyor upasarjanasya: go/strī-final upasarjana is shortened
def sutra_1_2_48(c) -> bool:
    return _in(c, "stem_final", {"go", "stri"}) and bool(c.get("is_upasarjana"))


# 1.2.49 luk taddhitaluki: when taddhita is luk-elided, certain operations still proceed
def sutra_1_2_49(c) -> bool:
    return _eq(c, "operation", "luk") and bool(c.get("is_taddhita"))


# 1.2.50 id goṇyāḥ: in the goṇī domain, id substitution
def sutra_1_2_50(c) -> bool:
    return _eq(c, "domain", "goni") and _eq(c, "substitute", "i")


# 1.2.51 lupi yuktavad vyaktivacane: after lup, the elided suffix's gender/number persists
def sutra_1_2_51(c) -> bool:
    return _eq(c, "operation", "lup") and bool(c.get("preserve_gender_number"))


# 1.2.52 viśeṣaṇānāṃ cājāteḥ: non-jāti adjectives also preserve agreement
def sutra_1_2_52(c) -> bool:
    return bool(c.get("is_adjective")) and not bool(c.get("is_jati"))


# 1.2.53 tad aśiṣyaṃ saṃjñāpramāṇatvāt: conventional saṁjñā is not subject to other operations
def sutra_1_2_53(c) -> bool:
    return bool(c.get("is_conventional_samjna")) and bool(c.get("aśiṣya"))


# 1.2.54 lub-yogāprakhyānāt: lup-elision is inferred from absence of expected form
def sutra_1_2_54(c) -> bool:
    return _eq(c, "operation", "lup") and bool(c.get("from_aprakhyana"))


# 1.2.55 yogapramāṇe ca tad-abhāve'darśanaṃ syāt: where joinings provide evidence, absence means lup
def sutra_1_2_55(c) -> bool:
    return bool(c.get("yoga_pramana")) and bool(c.get("absent"))


# 1.2.56 pradhānapratyayārthavacanam: principal suffix-meaning is primary semantic source
def sutra_1_2_56(c) -> bool:
    return bool(c.get("is_principal_suffix")) and bool(c.get("provides_meaning"))


# 1.2.57 kāla-upasarjane ca tulyam: same applies in temporal subordination
def sutra_1_2_57(c) -> bool:
    return _eq(c, "domain", "kala") and bool(c.get("is_upasarjana"))


# 1.2.58 jāty-ākhyāyām ekasmin bahuvacanam: in class-naming, plural for one (optional)
def sutra_1_2_58(c) -> bool:
    return bool(c.get("is_jati_name")) and _eq(c, "number", "plural") and bool(c.get("referent_one"))


# 1.2.59 asmado dvayoś ca: asmad takes plural even for two
def sutra_1_2_59(c) -> bool:
    return _eq(c, "stem", "asmad") and _eq(c, "number", "plural") and _eq(c, "referent_count", "two")


# 1.2.60 phalgunī-proṣṭhapadānāṃ ca nakṣatre: nakṣatra plural for these two
def sutra_1_2_60(c) -> bool:
    return _in(c, "stem", {"phalguni", "proshthapada"}) and _eq(c, "domain", "nakshatra") and _eq(c, "number", "plural")


# 1.2.61 chandasi punarvasvor ekavacanam: in Vedic, punarvasu in singular
def sutra_1_2_61(c) -> bool:
    return bool(c.get("is_vedic")) and _eq(c, "stem", "punarvasu") and _eq(c, "number", "singular")


# 1.2.62 viśākhayoś ca: same for viśākhā
def sutra_1_2_62(c) -> bool:
    return bool(c.get("is_vedic")) and _eq(c, "stem", "viśākhā") and _eq(c, "number", "singular")


# 1.2.63 tiṣya-punarvasvor nakṣatra-dvandve bahuvacanasya: in dvandva, plural → dual for tiṣya/punarvasu
def sutra_1_2_63(c) -> bool:
    return (_eq(c, "compound_type", "dvandva")
            and _eq(c, "stems", ("tiṣya", "punarvasu"))
            and _eq(c, "input_number", "plural")
            and _eq(c, "output_number", "dual"))


# 1.2.66 strī puṁvac ca: a strī-prātipadika behaves like its masculine counterpart
def sutra_1_2_66(c) -> bool:
    return _eq(c, "gender", "feminine") and bool(c.get("treated_as_masculine"))


# ===========================================================================
# Adhyāya 1.3 — dhātu-saṁjñā, anudeśa/adhikāra paribhāṣās, ātmanepada and
#               parasmaipada selection (72 sūtras)
# ===========================================================================

# 1.3.1 bhūvādayo dhātavaḥ: declared roots in bhū-list are dhātu
def sutra_1_3_1(c) -> bool:
    return bool(c.get("is_in_dhatupatha"))


# 1.3.10 yathāsaṃkhyam anudeśaḥ samānām: same-count lists pair index-wise
def sutra_1_3_10(c) -> bool:
    return (bool(c.get("left_list"))
            and bool(c.get("right_list"))
            and len(c.get("left_list")) == len(c.get("right_list"))
            and _eq(c, "mapping", "index_wise"))


# 1.3.11 svaritenādhikāraḥ: an adhikāra inherits via svarita
def sutra_1_3_11(c) -> bool:
    return _eq(c, "rule_marker", "svarita") and bool(c.get("is_adhikara"))


# 1.3.14 kartari karma-vyatihāre: reciprocal action selects ātmanepada in the kartṛ domain
def sutra_1_3_14(c) -> bool:
    return _eq(c, "voice", "kartari") and bool(c.get("is_reciprocal"))


# 1.3.15 na gati-hiṃsārthebhyaḥ: blocks 1.3.14 for motion/injury senses
def sutra_1_3_15(c) -> bool:
    return _in(c, "semantic", {"gati", "himsa"}) and bool(c.get("is_reciprocal_block"))


# 1.3.16 itaretarānyonyopapadāc ca: presence of itaretara/anyonya upapada keeps the reciprocal domain
def sutra_1_3_16(c) -> bool:
    return _in(c, "upapada", {"itaretara", "anyonya"})


# 1.3.20 āṅo do'nāsye viharaṇe: ā + dā in non-mouth-grasping sense → ātmanepada
def sutra_1_3_20(c) -> bool:
    return (_has_prefix(c, "ā") and _eq(c, "lemma", "dā")
            and _eq(c, "semantic", "viharana_non_mouth"))


# 1.3.22 samavapravibhyaḥ sthaḥ: sam/ava/pra/vi + sthā → ātmanepada
def sutra_1_3_22(c) -> bool:
    return _has_prefix(c, "sam", "ava", "pra", "vi") and _eq(c, "lemma", "sthā")


# 1.3.23 prakāśana-stheyākhyayoś ca: same + 'shining'/'judging' senses
def sutra_1_3_23(c) -> bool:
    return _eq(c, "lemma", "sthā") and _in(c, "semantic", {"prakashana", "stheya"})


# 1.3.26 akarmakāc ca: same applies for intransitive use
def sutra_1_3_26(c) -> bool:
    return _eq(c, "lemma", "sthā") and bool(c.get("is_akarmaka"))


# 1.3.27 udvibhyāṃ tapaḥ: ud/vi + tap → ātmanepada
def sutra_1_3_27(c) -> bool:
    return _has_prefix(c, "ud", "vi") and _eq(c, "lemma", "tap")


# 1.3.28 āṅo yamahanaḥ: ā + yam/han → ātmanepada
def sutra_1_3_28(c) -> bool:
    return _has_prefix(c, "ā") and _in(c, "lemma", {"yam", "han"})


# 1.3.30 nisamupavibhyo hvaḥ: ni/sam/upa/vi + hve → ātmanepada
def sutra_1_3_30(c) -> bool:
    return _has_prefix(c, "ni", "sam", "upa", "vi") and _eq(c, "lemma", "hve")


# 1.3.31 spardhāyām āṅaḥ: ā + hve in competition sense → ātmanepada
def sutra_1_3_31(c) -> bool:
    return _has_prefix(c, "ā") and _eq(c, "lemma", "hve") and _eq(c, "semantic", "spardha")


# 1.3.33 adheḥ prasahane: adhi + (rest/stand) in "endure" sense → ātmanepada
def sutra_1_3_33(c) -> bool:
    return _has_prefix(c, "adhi") and _eq(c, "semantic", "prasahana")


# 1.3.34 veḥ śabda-karmaṇaḥ: vi + (utterance verbs) when object is sound → ātmanepada
def sutra_1_3_34(c) -> bool:
    return _has_prefix(c, "vi") and _eq(c, "karman_kind", "shabda")


# 1.3.35 akarmakāc ca: same applies for intransitive use of 1.3.34's domain
def sutra_1_3_35(c) -> bool:
    return _has_prefix(c, "vi") and bool(c.get("is_akarmaka"))


# 1.3.36 sammānanotsañjanācāryakaraṇa...niyaḥ: ni + listed senses → ātmanepada
NI_SENSES_1_3_36 = frozenset({
    "sammanana", "utsanjana", "acaryakarana", "jnana",
    "bhrti", "viganana", "vyaya",
})
def sutra_1_3_36(c) -> bool:
    return _has_prefix(c, "ni") and _in(c, "semantic", NI_SENSES_1_3_36)


# 1.3.37 kartṛsthe cāśarīre karmaṇi: when karman is non-bodily and resides in kartṛ → ātmanepada
def sutra_1_3_37(c) -> bool:
    return bool(c.get("karman_in_kartri")) and bool(c.get("karman_non_bodily"))


# 1.3.38 vṛttisargatāyaneṣu kramaḥ: kram in "use/devotion/extension" senses → ātmanepada
def sutra_1_3_38(c) -> bool:
    return _eq(c, "lemma", "kram") and _in(c, "semantic", {"vrtti", "sarga", "tayana"})


# 1.3.39 upaparābhyām: upa/parā + kram → ātmanepada
def sutra_1_3_39(c) -> bool:
    return _has_prefix(c, "upa", "parā") and _eq(c, "lemma", "kram")


# 1.3.41 veḥ pāda-viharaṇe: vi + kram in "stepping" sense → ātmanepada
def sutra_1_3_41(c) -> bool:
    return _has_prefix(c, "vi") and _eq(c, "lemma", "kram") and _eq(c, "semantic", "pada_viharana")


# 1.3.42 propābhyāṃ samarthābhyām: pra/upa in suitable senses + kram → ātmanepada
def sutra_1_3_42(c) -> bool:
    return _has_prefix(c, "pra", "upa") and _eq(c, "lemma", "kram") and bool(c.get("is_samartha"))


# 1.3.43 anupasargād vā: without an upasarga, optional for kram
def sutra_1_3_43(c) -> bool:
    return _eq(c, "lemma", "kram") and not c.get("prefixes") and bool(c.get("optional"))


# 1.3.44 apahnave jñaḥ: jñā in "denying" sense → ātmanepada
def sutra_1_3_44(c) -> bool:
    return _eq(c, "lemma", "jñā") and _eq(c, "semantic", "apahnava")


# 1.3.45 akarmakāc ca: same applies for intransitive use of 1.3.44's domain
def sutra_1_3_45(c) -> bool:
    return _eq(c, "lemma", "jñā") and bool(c.get("is_akarmaka"))


# 1.3.46 sampratibhyām anādhyāne: sam/prati + jñā outside "remembering" sense → ātmanepada
def sutra_1_3_46(c) -> bool:
    return (_has_prefix(c, "sam", "prati") and _eq(c, "lemma", "jñā")
            and not _eq(c, "semantic", "adhyana"))


# 1.3.47 bhāsanopasambhāṣājñānayatnavimatyupamantraṇeṣu vadaḥ: vad in listed senses → ātmanepada
VAD_SENSES_1_3_47 = frozenset({
    "bhasana", "upasambhasha", "jnana", "yatna", "vimati", "upamantrana",
})
def sutra_1_3_47(c) -> bool:
    return _eq(c, "lemma", "vad") and _in(c, "semantic", VAD_SENSES_1_3_47)


# 1.3.48 vyaktavācāṃ samuccāraṇe: vad in "speaking-together" of articulate beings → ātmanepada
def sutra_1_3_48(c) -> bool:
    return (_eq(c, "lemma", "vad") and _eq(c, "semantic", "samuccarana")
            and bool(c.get("is_articulate")))


# 1.3.49 anor akarmakāt: anu + vad intransitive → ātmanepada
def sutra_1_3_49(c) -> bool:
    return _has_prefix(c, "anu") and _eq(c, "lemma", "vad") and bool(c.get("is_akarmaka"))


# 1.3.50 vibhāṣā vipralāpe: optional in "quarrelling" sense
def sutra_1_3_50(c) -> bool:
    return _eq(c, "lemma", "vad") and _eq(c, "semantic", "vipralapa") and bool(c.get("optional"))


# 1.3.51 avād graḥ: ava + grah → ātmanepada
def sutra_1_3_51(c) -> bool:
    return _has_prefix(c, "ava") and _eq(c, "lemma", "grah")


# 1.3.52 samaḥ pratijñāne: sam + grah in "promising" sense → ātmanepada
def sutra_1_3_52(c) -> bool:
    return _has_prefix(c, "sam") and _eq(c, "lemma", "grah") and _eq(c, "semantic", "pratijnana")


# 1.3.53 udaścaraḥ sakarmakāt: ud + car, transitive → ātmanepada
def sutra_1_3_53(c) -> bool:
    return _has_prefix(c, "ud") and _eq(c, "lemma", "car") and not bool(c.get("is_akarmaka"))


# 1.3.54 samas tṛtīyāyuktāt: sam-prefix when instrument (3rd-case) is present → ātmanepada
def sutra_1_3_54(c) -> bool:
    return _has_prefix(c, "sam") and bool(c.get("has_instrument"))


# 1.3.55 dāṇaś ca sā cec caturthyarthe: dā with "to-receive" sense involving dative → ātmanepada
def sutra_1_3_55(c) -> bool:
    return _eq(c, "lemma", "dā") and _eq(c, "semantic", "receive") and bool(c.get("has_dative"))


# 1.3.56 upād yamaḥ svakaraṇe: upa + yam in "marrying" sense → ātmanepada
def sutra_1_3_56(c) -> bool:
    return _has_prefix(c, "upa") and _eq(c, "lemma", "yam") and _eq(c, "semantic", "svakarana")


# 1.3.57 jñā-śru-smṛ-dṛśāṃ sanaḥ: san after jñā/śru/smṛ/dṛś → ātmanepada
def sutra_1_3_57(c) -> bool:
    return _eq(c, "suffix", "san") and _in(c, "lemma", {"jñā", "śru", "smṛ", "dṛś"})


# 1.3.58 nānor jñaḥ: but not when prefixed with anu
def sutra_1_3_58(c) -> bool:
    return _eq(c, "lemma", "jñā") and _has_prefix(c, "anu") and bool(c.get("is_block"))


# 1.3.59 pratyāṅbhyāṃ śruvaḥ: prati/ā + śru → ātmanepada
def sutra_1_3_59(c) -> bool:
    return _has_prefix(c, "prati", "ā") and _eq(c, "lemma", "śru")


# 1.3.60 śadeḥ śitaḥ: śad before śit-suffix → ātmanepada
def sutra_1_3_60(c) -> bool:
    return _eq(c, "lemma", "śad") and bool(c.get("suffix_is_shit"))


# 1.3.61 mriyater luṅliṅoś ca: mṛ in luṅ/liṅ → ātmanepada
def sutra_1_3_61(c) -> bool:
    return _eq(c, "lemma", "mṛ") and _in(c, "lakara", {"lun", "lin"})


# 1.3.62 pūrvavat sanaḥ: san-form continues parent root's pada
def sutra_1_3_62(c) -> bool:
    return _eq(c, "suffix", "san") and _eq(c, "pada", c.get("parent_pada"))


# 1.3.63 āmpratyayavat kṛñ-onuprayogasya: anuprayoga of kṛ behaves like ām-suffix
def sutra_1_3_63(c) -> bool:
    return _eq(c, "lemma", "kṛ") and bool(c.get("is_anuprayoga"))


# 1.3.64 propābhyāṃ yujer ayajñapātreṣu: pra/upa + yuj outside ritual-vessel sense → ātmanepada
def sutra_1_3_64(c) -> bool:
    return (_has_prefix(c, "pra", "upa") and _eq(c, "lemma", "yuj")
            and not _eq(c, "semantic", "yajna_patra"))


# 1.3.65 samaḥ kṣṇuvaḥ: sam + kṣṇu → ātmanepada
def sutra_1_3_65(c) -> bool:
    return _has_prefix(c, "sam") and _eq(c, "lemma", "kṣṇu")


# 1.3.66 bhujo'navane: bhuj outside "protecting" sense → ātmanepada
def sutra_1_3_66(c) -> bool:
    return _eq(c, "lemma", "bhuj") and not _eq(c, "semantic", "avana")


# 1.3.67 ṇer aṇau yat karma ṇau cet sa kartā'nādhyāne: causee-becomes-agent rule
def sutra_1_3_67(c) -> bool:
    return (bool(c.get("is_nic"))
            and _eq(c, "non_causal_karman", "becomes_causal_agent")
            and not _eq(c, "semantic", "adhyana"))


# 1.3.68 bhīsmyor hetubhaye: bhī/smi when the fear-cause is present → ātmanepada
def sutra_1_3_68(c) -> bool:
    return _in(c, "lemma", {"bhī", "smi"}) and bool(c.get("hetubhaya"))


# 1.3.69 gṛdhi-vañcyoḥ pralambhane: gṛdh/vañc in "deceiving" sense → ātmanepada
def sutra_1_3_69(c) -> bool:
    return _in(c, "lemma", {"gṛdh", "vañc"}) and _eq(c, "semantic", "pralambhana")


# 1.3.70 liyaḥ sammānana-śālinīkaraṇayoś ca: lī in honor/showy senses → ātmanepada
def sutra_1_3_70(c) -> bool:
    return _eq(c, "lemma", "lī") and _in(c, "semantic", {"sammanana", "shalinikarana"})


# 1.3.71 mithyopapadāt kṛño'bhyāse: kṛ with 'mithyā' in repetition → ātmanepada
def sutra_1_3_71(c) -> bool:
    return _eq(c, "lemma", "kṛ") and _eq(c, "upapada", "mithyā") and bool(c.get("is_abhyasa"))


# 1.3.73 apād vadaḥ: apa + vad → ātmanepada
def sutra_1_3_73(c) -> bool:
    return _has_prefix(c, "apa") and _eq(c, "lemma", "vad")


# 1.3.74 ṇicaś ca: ṇic (causative) of vad → ātmanepada continues
def sutra_1_3_74(c) -> bool:
    return _eq(c, "lemma", "vad") and bool(c.get("is_nic"))


# 1.3.75 samudāṅbhyo yamo'granthe: sam/ud/ā + yam outside book sense → ātmanepada
def sutra_1_3_75(c) -> bool:
    return (_has_prefix(c, "sam", "ud", "ā") and _eq(c, "lemma", "yam")
            and not _eq(c, "semantic", "grantha"))


# 1.3.76 anupasargāj jñaḥ: without an upasarga, jñā → ātmanepada
def sutra_1_3_76(c) -> bool:
    return _eq(c, "lemma", "jñā") and not c.get("prefixes")


# 1.3.77 vibhāṣopapadena pratīyamāne: optional when the action is implied by the upapada
def sutra_1_3_77(c) -> bool:
    return bool(c.get("action_implied_by_upapada")) and bool(c.get("optional"))


# 1.3.79 anuparābhyāṃ kṛñaḥ: anu/parā + kṛ → ātmanepada
def sutra_1_3_79(c) -> bool:
    return _has_prefix(c, "anu", "parā") and _eq(c, "lemma", "kṛ")


# 1.3.80 abhi-prati-atibhyaḥ kṣipaḥ: abhi/prati/ati + kṣip → ātmanepada
def sutra_1_3_80(c) -> bool:
    return _has_prefix(c, "abhi", "prati", "ati") and _eq(c, "lemma", "kṣip")


# 1.3.81 prād vahaḥ: pra + vah → ātmanepada
def sutra_1_3_81(c) -> bool:
    return _has_prefix(c, "pra") and _eq(c, "lemma", "vah")


# 1.3.82 parer mṛṣaḥ: pari + mṛṣ → ātmanepada
def sutra_1_3_82(c) -> bool:
    return _has_prefix(c, "pari") and _eq(c, "lemma", "mṛṣ")


# 1.3.83 vyāṅparibhyo ramaḥ: vi/ā/pari + ram → ātmanepada
def sutra_1_3_83(c) -> bool:
    return _has_prefix(c, "vi", "ā", "pari") and _eq(c, "lemma", "ram")


# 1.3.84 upāc ca: upa + ram → ātmanepada
def sutra_1_3_84(c) -> bool:
    return _has_prefix(c, "upa") and _eq(c, "lemma", "ram")


# 1.3.85 vibhāṣā'karmakāt: optional for intransitive use of 1.3.83/84 domain
def sutra_1_3_85(c) -> bool:
    return _eq(c, "lemma", "ram") and bool(c.get("is_akarmaka")) and bool(c.get("optional"))


# 1.3.86 budha-yudha-naśa-jane-pru-dru-srubhyo ṇeḥ: causatives of these → ātmanepada (active rule)
NIC_ROOTS_1_3_86 = frozenset({"budh", "yudh", "naś", "jan", "pru", "dru", "sru"})
def sutra_1_3_86(c) -> bool:
    return _in(c, "lemma", NIC_ROOTS_1_3_86) and bool(c.get("is_nic"))


# 1.3.87 nigaraṇa-calanārthebhyaḥ: causatives of swallowing/moving verbs
def sutra_1_3_87(c) -> bool:
    return _in(c, "semantic", {"nigarana", "calana"}) and bool(c.get("is_nic"))


# 1.3.88 aṇāv akarmakāc cittavat-kartṛkāt: non-causal intransitive with sentient agent
def sutra_1_3_88(c) -> bool:
    return (not bool(c.get("is_nic")))  and bool(c.get("is_akarmaka")) and bool(c.get("agent_is_sentient"))


# 1.3.89 na pādamyāṅyamāṅyasaparimuharucinṛtivadavasaḥ: blocks 1.3.88 for these listed roots
BLOCK_ROOTS_1_3_89 = frozenset({"pā", "dam", "yam", "yas", "parimuh", "ruc", "nṛt", "vad", "vas"})
def sutra_1_3_89(c) -> bool:
    return _in(c, "lemma", BLOCK_ROOTS_1_3_89) and bool(c.get("is_block"))


# 1.3.90 vā kyaṣaḥ: optional after kyac suffix (denominal)
def sutra_1_3_90(c) -> bool:
    return _eq(c, "suffix", "kyac") and bool(c.get("optional"))


# 1.3.91 dyud-bhyo luṅi: dyut-roots in luṅ → ātmanepada
def sutra_1_3_91(c) -> bool:
    return _eq(c, "root_class", "dyut") and _eq(c, "lakara", "lun")


# 1.3.92 vṛd-bhyaḥ syasanoḥ: vṛt-roots in sya/san → ātmanepada
def sutra_1_3_92(c) -> bool:
    return _eq(c, "root_class", "vrt") and _in(c, "suffix", {"sya", "san"})


# 1.3.93 luṭi ca kḷpaḥ: kḷp in luṭ → ātmanepada
def sutra_1_3_93(c) -> bool:
    return _eq(c, "lemma", "kḷp") and _eq(c, "lakara", "lut")


# ===========================================================================
# Adhyāya 1.4 — saṁjñā paribhāṣās, kāraka extensions, gati/upasarga,
#               karmapravacanīya senses, tiṅ-suffix labels (84 sūtras)
# ===========================================================================

# 1.4.1 ā kaḍārād ekā saṃjñā: only one saṃjñā applies in the indicated range
def sutra_1_4_1(c) -> bool:
    return bool(c.get("in_range_to_kadara")) and len(c.get("competing_samjnas", ())) > 1 and _eq(c, "selected_count", 1)


# 1.4.2 vipratiṣedhe paraṃ kāryam: when rules conflict, the later rule wins
def sutra_1_4_2(c) -> bool:
    return bool(c.get("rules_conflict")) and _eq(c, "selected", "later")


# 1.4.4 neyaṅuvaṅsthānāv astrī: ī/ū-final stems whose ī/ū becomes iyaṅ/uvaṅ are not nadī (except non-strī)
def sutra_1_4_4(c) -> bool:
    return (_in(c, "stem_final", {"ī", "ū"})
            and bool(c.get("becomes_iyan_or_uvan"))
            and not _eq(c, "gender", "feminine"))


# 1.4.5 vā'mi: optional before the suffix 'ām'
def sutra_1_4_5(c) -> bool:
    return _eq(c, "following_suffix", "ām") and bool(c.get("optional"))


# 1.4.6 ṅiti hrasvaś ca: a short i/u-final word before ṅit suffix is also nadī
def sutra_1_4_6(c) -> bool:
    return (_in(c, "stem_final", {"i", "u"})
            and _eq(c, "stem_duration", "hrasva")
            and bool(c.get("following_is_ngit")))


# 1.4.8 patiḥ samāsa eva: pati gets ghi only inside a compound
def sutra_1_4_8(c) -> bool:
    return _eq(c, "stem", "pati") and bool(c.get("in_compound"))


# 1.4.9 ṣaṣṭhī-yuktaś chandasi vā: in Vedic, optional when 6th-case-related
def sutra_1_4_9(c) -> bool:
    return bool(c.get("is_vedic")) and bool(c.get("has_genitive_relation")) and bool(c.get("optional"))


# 1.4.15 naḥ kye: a kya-style suffix following 'n' blocks the pada-saṁjñā
def sutra_1_4_15(c) -> bool:
    return _eq(c, "stem_final", "n") and _eq(c, "following_suffix_class", "kya")


# 1.4.16 siti ca: same blocking applies before sit-marked suffixes
def sutra_1_4_16(c) -> bool:
    return _eq(c, "stem_final", "n") and bool(c.get("following_is_sit"))


# 1.4.19 tasau matvarthe: t/s-final stem followed by a matup-like suffix is bha
def sutra_1_4_19(c) -> bool:
    return _in(c, "stem_final", {"t", "s"}) and _eq(c, "suffix_meaning", "matup")


# 1.4.20 ayasmayādīni chandasi: ayasmayādi terms behave as bha in Vedic
def sutra_1_4_20(c) -> bool:
    return _in(c, "stem", {"ayasmaya", "śyāmaya"}) and bool(c.get("is_vedic"))


# 1.4.21 bahuṣu bahuvacanam: many referents → plural
def sutra_1_4_21(c) -> bool:
    return _eq(c, "referent_count", "many") and _eq(c, "number", "plural")


# 1.4.22 dvyekayor dvivacanaikavacane: two → dual, one → singular
def sutra_1_4_22(c) -> bool:
    return ((_eq(c, "referent_count", "two") and _eq(c, "number", "dual"))
            or (_eq(c, "referent_count", "one") and _eq(c, "number", "singular")))


# 1.4.23 kārake: opens the kāraka section (adhikāra)
def sutra_1_4_23(c) -> bool:
    return _eq(c, "section", "karaka") and bool(c.get("is_adhikara"))


# 1.4.30 janikartuḥ prakṛtiḥ: source-material of "to be born" is apādāna
def sutra_1_4_30(c) -> bool:
    return _eq(c, "context", "birth_source") and _eq(c, "role", "apadana")


# 1.4.31 bhuvaḥ prabhavaḥ: with bhū, the place of origin is apādāna
def sutra_1_4_31(c) -> bool:
    return _eq(c, "verb", "bhū") and _eq(c, "context", "origin_place") and _eq(c, "role", "apadana")


# 1.4.34 ślāgha-hnu-ṅ-sthā-śapāṃ jñīpsyamānaḥ: praise/conceal/stand/swear → intended-knowable is sampradāna
def sutra_1_4_34(c) -> bool:
    return (_in(c, "verb", {"ślāgh", "hnu", "sthā", "śap"})
            and _eq(c, "context", "intended_knowable")
            and _eq(c, "role", "sampradana"))


# 1.4.35 dhāreruttamarṇaḥ: with dhṛ in "owe" sense, the creditor → sampradāna
def sutra_1_4_35(c) -> bool:
    return _eq(c, "verb", "dhṛ") and _eq(c, "context", "creditor") and _eq(c, "role", "sampradana")


# 1.4.36 spṛher īpsitaḥ: with spṛh, the desired object → sampradāna
def sutra_1_4_36(c) -> bool:
    return _eq(c, "verb", "spṛh") and _eq(c, "context", "desired_object") and _eq(c, "role", "sampradana")


# 1.4.37 krudha-druh-erṣyā-asūyārthānāṃ yaṃ prati kopaḥ: with anger/envy verbs, the angered-at → sampradāna
def sutra_1_4_37(c) -> bool:
    return (_in(c, "verb_meaning", {"krudh", "druh", "irshya", "asuya"})
            and _eq(c, "context", "angered_at")
            and _eq(c, "role", "sampradana"))


# 1.4.38 krudha-druhor upasṛṣṭayoḥ karma: but prefixed krudh/druh → karman (not sampradāna)
def sutra_1_4_38(c) -> bool:
    return (_in(c, "verb_meaning", {"krudh", "druh"})
            and bool(c.get("has_upasarga"))
            and _eq(c, "role", "karman"))


# 1.4.39 rādhīkṣyor yasya vipraśnaḥ: with rādh/īkṣ, the one inquired about → sampradāna
def sutra_1_4_39(c) -> bool:
    return (_in(c, "verb", {"rādh", "īkṣ"}) and _eq(c, "context", "inquired_about")
            and _eq(c, "role", "sampradana"))


# 1.4.40 pratyāṅbhyāṃ śruvaḥ pūrvasya kartā: prati/ā + śru — previous-speaker → kartṛ
def sutra_1_4_40(c) -> bool:
    return (_has_prefix(c, "prati", "ā") and _eq(c, "verb", "śru")
            and _eq(c, "context", "previous_speaker")
            and _eq(c, "role", "kartr"))


# 1.4.41 anu-prati-gṛṇaś ca: anu/prati + gṛ — previous-speaker → kartṛ
def sutra_1_4_41(c) -> bool:
    return _has_prefix(c, "anu", "prati") and _eq(c, "verb", "gṛ") and _eq(c, "role", "kartr")


# 1.4.43 divaḥ karma ca: with div, the staked object → karman (in addition to karaṇa)
def sutra_1_4_43(c) -> bool:
    return _eq(c, "verb", "div") and _eq(c, "context", "staked_object") and _eq(c, "role", "karman")


# 1.4.44 parikrayaṇe sampradānam anyatarasyām: optional sampradāna in hiring
def sutra_1_4_44(c) -> bool:
    return _eq(c, "context", "hiring") and _eq(c, "role", "sampradana") and bool(c.get("optional"))


# 1.4.46 adhi-śīṅ-sthā-āsāṃ karma: adhi + (lie/stand/sit) — location → karman
def sutra_1_4_46(c) -> bool:
    return (_has_prefix(c, "adhi") and _in(c, "verb", {"śīṅ", "sthā", "ās"})
            and _eq(c, "role", "karman"))


# 1.4.47 abhi-niviśaś ca: abhi + niviś — location → karman
def sutra_1_4_47(c) -> bool:
    return _has_prefix(c, "abhi") and _eq(c, "verb", "niviś") and _eq(c, "role", "karman")


# 1.4.48 upānvadhyāṅvasaḥ: upa/anu/adhi/ā + vas — location → karman
def sutra_1_4_48(c) -> bool:
    return _has_prefix(c, "upa", "anu", "adhi", "ā") and _eq(c, "verb", "vas") and _eq(c, "role", "karman")


# 1.4.50 tathā-yuktaṃ cānipsītam: undesired-but-connected participant → karman
def sutra_1_4_50(c) -> bool:
    return bool(c.get("is_unwanted_but_connected")) and _eq(c, "role", "karman")


# 1.4.51 akathitaṃ ca: an unexpressed object also takes karman
def sutra_1_4_51(c) -> bool:
    return bool(c.get("is_unexpressed_object")) and _eq(c, "role", "karman")


# 1.4.52 gati-buddhi-pratyavasānārtha-śabda-karmākarmakāṇām aṇi kartā:
#   in non-causal use of motion/cognition/eating/utterance verbs, the
#   non-causal agent becomes the causal karman (so kartā gets demoted)
def sutra_1_4_52(c) -> bool:
    return (_in(c, "verb_class", {"gati", "buddhi", "pratyavasana", "shabda_karman", "akarmaka"})
            and not bool(c.get("is_nic"))
            and _eq(c, "role", "kartr"))


# 1.4.53 hṛkror anyatarasyām: with hṛ/kṛ, optionally karman in this domain
def sutra_1_4_53(c) -> bool:
    return _in(c, "verb", {"hṛ", "kṛ"}) and bool(c.get("optional"))


# 1.4.55 tatprayojako hetuś ca: the instigator (cause) is also kartṛ
def sutra_1_4_55(c) -> bool:
    return _eq(c, "context", "instigator") and _eq(c, "role", "kartr")


# 1.4.56 prāg rīśvarān nipātāḥ: items before the rīśvara section are nipātas
def sutra_1_4_56(c) -> bool:
    return bool(c.get("in_pre_rishvara_section")) and _eq(c, "samjna", "nipata")


# 1.4.57 cādayo'sattve: ca-etc. are nipātas when not used as substantives
def sutra_1_4_57(c) -> bool:
    return _in(c, "word", {"ca", "vā", "ha", "aha"}) and not bool(c.get("is_substantive"))


# 1.4.61 ūry-ādi-cvi-ḍāc ca: ūrī-etc. + cvi/ḍāc derivatives are gati
def sutra_1_4_61(c) -> bool:
    return _in(c, "word_class", {"uryadi", "cvi", "dac"})


# 1.4.62 anukaraṇaṃ cānitiparam: imitation-words (not followed by 'iti') are gati
def sutra_1_4_62(c) -> bool:
    return bool(c.get("is_imitation")) and not bool(c.get("followed_by_iti"))


# 1.4.63 ādarānādarayoḥ sadasatī: sat/asat in respect/disrespect senses are gati
def sutra_1_4_63(c) -> bool:
    return _in(c, "word", {"sat", "asat"}) and _in(c, "semantic", {"adara", "anadara"})


# 1.4.64 bhūṣaṇe'lam: 'alam' in adornment sense is gati
def sutra_1_4_64(c) -> bool:
    return _eq(c, "word", "alam") and _eq(c, "semantic", "bhushana")


# 1.4.65 antar-aparigrahe: 'antar' in non-grasping sense is gati
def sutra_1_4_65(c) -> bool:
    return _eq(c, "word", "antar") and _eq(c, "semantic", "aparigraha")


# 1.4.66 kaṇe-manasī śraddhā-pratīghāte: 'kaṇe'/'manas' in obstruction-of-faith sense
def sutra_1_4_66(c) -> bool:
    return _in(c, "word", {"kaṇe", "manas"}) and _eq(c, "semantic", "shraddha_pratighata")


# 1.4.67 puro'vyayam: 'puras' is avyaya (gati)
def sutra_1_4_67(c) -> bool:
    return _eq(c, "word", "puras")


# 1.4.68 astaṃ ca: 'astam' is also gati
def sutra_1_4_68(c) -> bool:
    return _eq(c, "word", "astam")


# 1.4.69 accha gaty-arthavadeṣu: 'accha' with motion-meaning verbs is gati
def sutra_1_4_69(c) -> bool:
    return _eq(c, "word", "accha") and _eq(c, "verb_meaning", "gati")


# 1.4.70 ado'nupadeśe: 'adas' outside instruction sense is gati
def sutra_1_4_70(c) -> bool:
    return _eq(c, "word", "adas") and not _eq(c, "semantic", "upadesha")


# 1.4.71 tiro'ntardhau: 'tiras' in concealment sense is gati
def sutra_1_4_71(c) -> bool:
    return _eq(c, "word", "tiras") and _eq(c, "semantic", "antardha")


# 1.4.72 vibhāṣā kṛñi: optional gati with kṛ
def sutra_1_4_72(c) -> bool:
    return _eq(c, "verb", "kṛ") and bool(c.get("optional"))


# 1.4.73 upāje'nvāje: 'upāje'/'anvāje' are gati
def sutra_1_4_73(c) -> bool:
    return _in(c, "word", {"upāje", "anvāje"})


# 1.4.74 sākṣāt-prabhṛtīni ca: 'sākṣāt' and similar are gati
def sutra_1_4_74(c) -> bool:
    return _in(c, "word_class", {"sakshatprabhrti"})


# 1.4.75 anatyādhāna urasimanasī: 'urasi'/'manasi' (not in laying-on sense) are gati
def sutra_1_4_75(c) -> bool:
    return _in(c, "word", {"urasi", "manasi"}) and not _eq(c, "semantic", "atyadhana")


# 1.4.76 madhye-padenivacane ca: 'madhye-pade'-type expressions are gati
def sutra_1_4_76(c) -> bool:
    return _in(c, "word_class", {"madhyepade", "nivacana"})


# 1.4.77 nityaṃ haste pāṇāv upayamane: hand-grasping (marriage) → fixed gati of haste/pāṇau
def sutra_1_4_77(c) -> bool:
    return _in(c, "word", {"haste", "pāṇau"}) and _eq(c, "semantic", "upayamana")


# 1.4.78 prādhvaṃ bandhane: 'prādhvam' in binding sense is gati
def sutra_1_4_78(c) -> bool:
    return _eq(c, "word", "prādhvam") and _eq(c, "semantic", "bandhana")


# 1.4.79 jīvikopaniṣadāv aupamye: 'jīvikā'/'upaniṣad' in simile sense are gati
def sutra_1_4_79(c) -> bool:
    return _in(c, "word", {"jīvikā", "upaniṣad"}) and _eq(c, "semantic", "aupamya")


# 1.4.80 te prāg dhātoḥ: gati items go before the dhātu (positional rule)
def sutra_1_4_80(c) -> bool:
    return _eq(c, "samjna", "gati") and _eq(c, "position", "before_dhatu")


# 1.4.81 chandasi pare'pi: in Vedic, gati may follow the dhātu
def sutra_1_4_81(c) -> bool:
    return bool(c.get("is_vedic")) and _eq(c, "samjna", "gati") and _eq(c, "position", "after_dhatu")


# 1.4.82 vyavahitāś ca: gati may be separated from the dhātu
def sutra_1_4_82(c) -> bool:
    return _eq(c, "samjna", "gati") and bool(c.get("is_separated"))


# 1.4.83 karmapravacanīyāḥ: opens the karmapravacanīya section
def sutra_1_4_83(c) -> bool:
    return _eq(c, "section", "karmapravacaniya") and bool(c.get("is_adhikara"))


# 1.4.84 anur lakṣaṇe: 'anu' in 'because-of/sign-of' sense is karmapravacanīya
def sutra_1_4_84(c) -> bool:
    return _eq(c, "word", "anu") and _eq(c, "semantic", "lakshana")


# 1.4.85 tṛtīyā'rthe: 'anu' in instrumental-sense is karmapravacanīya
def sutra_1_4_85(c) -> bool:
    return _eq(c, "word", "anu") and _eq(c, "semantic", "trtiya_artha")


# 1.4.86 hīne: 'anu' in 'inferior-to' sense is karmapravacanīya
def sutra_1_4_86(c) -> bool:
    return _eq(c, "word", "anu") and _eq(c, "semantic", "hina")


# 1.4.87 upo'dhike ca: 'upa' in 'superior-to' sense is karmapravacanīya
def sutra_1_4_87(c) -> bool:
    return _eq(c, "word", "upa") and _eq(c, "semantic", "adhika")


# 1.4.88 apa-parī varjane: 'apa'/'pari' in 'except' sense are karmapravacanīya
def sutra_1_4_88(c) -> bool:
    return _in(c, "word", {"apa", "pari"}) and _eq(c, "semantic", "varjana")


# 1.4.89 āṅ maryādā-vacane: 'ā' in 'up-to' sense is karmapravacanīya
def sutra_1_4_89(c) -> bool:
    return _eq(c, "word", "ā") and _eq(c, "semantic", "maryada")


# 1.4.90 lakṣaṇetthambhūtākhyāna-bhāga-vīpsāsu pratiparyanavaḥ: prati/pari/anu in listed senses
def sutra_1_4_90(c) -> bool:
    return (_in(c, "word", {"prati", "pari", "anu"})
            and _in(c, "semantic", {"lakshana", "ittham_bhuta", "bhaga", "vipsa"}))


# 1.4.91 abhir abhāge: 'abhi' in non-share sense is karmapravacanīya
def sutra_1_4_91(c) -> bool:
    return _eq(c, "word", "abhi") and not _eq(c, "semantic", "bhaga")


# 1.4.92 pratiḥ pratinidhi-pratidānayoḥ: 'prati' in substitute/repayment sense
def sutra_1_4_92(c) -> bool:
    return _eq(c, "word", "prati") and _in(c, "semantic", {"pratinidhi", "pratidana"})


# 1.4.93 adhi-parī anarthakau: 'adhi'/'pari' when meaningless
def sutra_1_4_93(c) -> bool:
    return _in(c, "word", {"adhi", "pari"}) and bool(c.get("is_anarthaka"))


# 1.4.94 suḥ pūjāyām: 'su' in worship sense is karmapravacanīya
def sutra_1_4_94(c) -> bool:
    return _eq(c, "word", "su") and _eq(c, "semantic", "puja")


# 1.4.95 atir atikramaṇe ca: 'ati' in 'crossing-beyond' sense
def sutra_1_4_95(c) -> bool:
    return _eq(c, "word", "ati") and _eq(c, "semantic", "atikramana")


# 1.4.96 apiḥ padārthasambhāvanānvavasarga-garhā-samuccayeṣu: 'api' in listed senses
def sutra_1_4_96(c) -> bool:
    return (_eq(c, "word", "api")
            and _in(c, "semantic", {"padartha_sambhavana", "anvavasarga", "garha", "samuccaya"}))


# 1.4.97 adhir īśvare: 'adhi' in 'lord-over' sense
def sutra_1_4_97(c) -> bool:
    return _eq(c, "word", "adhi") and _eq(c, "semantic", "ishvara")


# 1.4.98 vibhāṣā kṛñi: 'adhi' with kṛ — optional karmapravacanīya
def sutra_1_4_98(c) -> bool:
    return _eq(c, "word", "adhi") and _eq(c, "verb", "kṛ") and bool(c.get("optional"))


# 1.4.99 laḥ parasmaipadam: l-replacements that are parasmaipada labels
def sutra_1_4_99(c) -> bool:
    return _eq(c, "label_origin", "l_substitute") and _eq(c, "pada", "parasmaipada")


# 1.4.100 taṅānāv ātmanepadam: taṅ/āna substitutes are ātmanepada labels
def sutra_1_4_100(c) -> bool:
    return _in(c, "ending_class", {"tan", "ana"}) and _eq(c, "pada", "atmanepada")


# 1.4.101 tiṅas trīṇi trīṇi prathama-madhyamottamāḥ: nine tiṅs split into three triples (prathama/madhyama/uttama)
def sutra_1_4_101(c) -> bool:
    return _eq(c, "suffix_class", "tin") and _in(c, "person_label", {"prathama", "madhyama", "uttama"})


# 1.4.102 tāny ekavacana-dvivacana-bahuvacanāny ekaśaḥ: each triple is sg/du/pl in order
def sutra_1_4_102(c) -> bool:
    return _eq(c, "suffix_class", "tin") and _in(c, "number", {"singular", "dual", "plural"})


# 1.4.103 supaḥ: sup endings (the 21-fold case set)
def sutra_1_4_103(c) -> bool:
    return _eq(c, "suffix_class", "sup")


# 1.4.104 vibhaktiś ca: tiṅ and sup are also vibhakti
def sutra_1_4_104(c) -> bool:
    return _in(c, "suffix_class", {"sup", "tin"}) and bool(c.get("is_vibhakti"))


# 1.4.105 yuṣmady upapade samānādhikaraṇe sthāniny api madhyamaḥ: with yuṣmad → madhyama
def sutra_1_4_105(c) -> bool:
    return _eq(c, "upapada", "yuṣmad") and bool(c.get("is_samanadhikarana")) and _eq(c, "person_label", "madhyama")


# 1.4.106 prahāse ca manyo'pa-pade manyater uttama ekavac ca: with man+upapada → uttama (singular)
def sutra_1_4_106(c) -> bool:
    return (_eq(c, "verb", "man") and _eq(c, "context", "prahasa")
            and _eq(c, "person_label", "uttama") and _eq(c, "number", "singular"))


# 1.4.107 asmady uttamaḥ: with asmad → uttama
def sutra_1_4_107(c) -> bool:
    return _eq(c, "upapada", "asmad") and _eq(c, "person_label", "uttama")


# 1.4.108 śeṣe prathamaḥ: default → prathama
def sutra_1_4_108(c) -> bool:
    return _eq(c, "upapada", "shesha") and _eq(c, "person_label", "prathama")


# ===========================================================================
# Linguistic fixtures (positive, negative) for every sūtra above.
# Each negative is the *near-miss* that lacks exactly the discriminating
# feature the sūtra names.
# ===========================================================================

FIXTURES: dict[str, tuple[dict, dict]] = {
    # 1.2 ---------------------------------------------------------------
    "1.2.3":  ({"lemma": "ūrṇu", "optional": True},
               {"lemma": "ūrṇu", "optional": False}),
    "1.2.10": ({"suffix": "san", "root_ends_hal": True, "root_has_ik_upadha": True, "following": "jhal"},
               {"suffix": "san", "root_ends_hal": False, "root_has_ik_upadha": True, "following": "jhal"}),
    "1.2.16": ({"lemma": "yam", "semantic": "upayamana", "optional": True},
               {"lemma": "yam", "semantic": "upayamana", "optional": False}),
    "1.2.21": ({"upadha": "u", "semantic": "bhava", "optional": True},
               {"upadha": "u", "semantic": "ordinary", "optional": True}),
    "1.2.22": ({"lemma": "pū", "suffix": "ktvā"},
               {"lemma": "bhū", "suffix": "ktvā"}),
    "1.2.23": ({"upadha": "n", "final": "th", "optional": True},
               {"upadha": "n", "final": "k",  "optional": True}),
    "1.2.24": ({"lemma": "vañc", "optional": True},
               {"lemma": "bhū",  "optional": True}),
    "1.2.25": ({"lemma": "tṛṣ", "optional": True},
               {"lemma": "bhū", "optional": True}),
    "1.2.27": ({"duration": "hrasva"}, {"duration": "tone"}),
    "1.2.28": ({"is_ac": True, "duration": "dirgha"},
               {"is_ac": False, "duration": "dirgha"}),
    "1.2.29": ({"pitch": "high", "accent": "udatta"},
               {"pitch": "high", "accent": "anudatta"}),
    "1.2.30": ({"pitch": "low",  "accent": "anudatta"},
               {"pitch": "low",  "accent": "udatta"}),
    "1.2.31": ({"pitch": "combined", "accent": "svarita"},
               {"pitch": "high",     "accent": "svarita"}),
    "1.2.32": ({"accent": "svarita", "initial_half": "udatta"},
               {"accent": "svarita", "initial_half": "anudatta"}),
    "1.2.33": ({"is_sambuddhi": True, "is_from_distance": True, "accent": "ekashruti"},
               {"is_sambuddhi": True, "is_from_distance": False, "accent": "ekashruti"}),
    "1.2.34": ({"context": "yajna_karman", "subdomain": "other", "accent": "ekashruti"},
               {"context": "yajna_karman", "subdomain": "japa",  "accent": "ekashruti"}),
    "1.2.35": ({"word": "vaṣaṭ", "optional": True, "accent": "udattatara"},
               {"word": "vaṣaṭ", "optional": False, "accent": "udattatara"}),
    "1.2.36": ({"is_vedic": True, "optional": True},
               {"is_vedic": False, "optional": True}),
    "1.2.37": ({"context": "subrahmanya", "input_accent": "svarita", "output_accent": "udatta"},
               {"context": "ordinary",    "input_accent": "svarita", "output_accent": "udatta"}),
    "1.2.38": ({"word": "deva",   "accent": "anudatta"},
               {"word": "agni",   "accent": "anudatta"}),
    "1.2.39": ({"preceding_accent": "svarita", "in_samhita": True, "accent": "anudatta"},
               {"preceding_accent": "udatta",  "in_samhita": True, "accent": "anudatta"}),
    "1.2.40": ({"preceding_accent": "udatta",  "accent": "sannatara"},
               {"preceding_accent": "anudatta", "accent": "sannatara"}),
    "1.2.42": ({"compound_type": "tatpurusha", "is_samanadhikarana": True},
               {"compound_type": "tatpurusha", "is_samanadhikarana": False}),
    "1.2.43": ({"in_compound": True, "is_first_named": True},
               {"in_compound": True, "is_first_named": False}),
    "1.2.44": ({"is_single_case_member": True, "is_pre_compound_initial": False},
               {"is_single_case_member": True, "is_pre_compound_initial": True}),
    "1.2.45": ({"is_meaningful": True, "is_dhatu": False, "is_pratyaya": False},
               {"is_meaningful": True, "is_dhatu": True,  "is_pratyaya": False}),
    "1.2.46": ({"derivation_source": "krt"},
               {"derivation_source": "dhatu"}),
    "1.2.47": ({"gender": "neuter",   "is_pratipadika": True, "final_vowel_shortened": True},
               {"gender": "masculine","is_pratipadika": True, "final_vowel_shortened": True}),
    "1.2.48": ({"stem_final": "go",  "is_upasarjana": True},
               {"stem_final": "deva","is_upasarjana": True}),
    "1.2.49": ({"operation": "luk", "is_taddhita": True},
               {"operation": "luk", "is_taddhita": False}),
    "1.2.50": ({"domain": "goni", "substitute": "i"},
               {"domain": "goni", "substitute": "a"}),
    "1.2.51": ({"operation": "lup", "preserve_gender_number": True},
               {"operation": "luk", "preserve_gender_number": True}),
    "1.2.52": ({"is_adjective": True, "is_jati": False},
               {"is_adjective": True, "is_jati": True}),
    "1.2.53": ({"is_conventional_samjna": True, "aśiṣya": True},
               {"is_conventional_samjna": False, "aśiṣya": True}),
    "1.2.54": ({"operation": "lup", "from_aprakhyana": True},
               {"operation": "lup", "from_aprakhyana": False}),
    "1.2.55": ({"yoga_pramana": True, "absent": True},
               {"yoga_pramana": True, "absent": False}),
    "1.2.56": ({"is_principal_suffix": True, "provides_meaning": True},
               {"is_principal_suffix": False, "provides_meaning": True}),
    "1.2.57": ({"domain": "kala", "is_upasarjana": True},
               {"domain": "vyakti", "is_upasarjana": True}),
    "1.2.58": ({"is_jati_name": True, "number": "plural",   "referent_one": True},
               {"is_jati_name": True, "number": "singular", "referent_one": True}),
    "1.2.59": ({"stem": "asmad", "number": "plural", "referent_count": "two"},
               {"stem": "yuṣmad","number": "plural", "referent_count": "two"}),
    "1.2.60": ({"stem": "phalguni", "domain": "nakshatra", "number": "plural"},
               {"stem": "phalguni", "domain": "ordinary",  "number": "plural"}),
    "1.2.61": ({"is_vedic": True,  "stem": "punarvasu", "number": "singular"},
               {"is_vedic": False, "stem": "punarvasu", "number": "singular"}),
    "1.2.62": ({"is_vedic": True,  "stem": "viśākhā", "number": "singular"},
               {"is_vedic": False, "stem": "viśākhā", "number": "singular"}),
    "1.2.63": ({"compound_type": "dvandva", "stems": ("tiṣya", "punarvasu"),
                "input_number": "plural", "output_number": "dual"},
               {"compound_type": "dvandva", "stems": ("tiṣya", "punarvasu"),
                "input_number": "dual",   "output_number": "dual"}),
    "1.2.66": ({"gender": "feminine",  "treated_as_masculine": True},
               {"gender": "masculine", "treated_as_masculine": True}),

    # 1.3 ---------------------------------------------------------------
    "1.3.1":  ({"is_in_dhatupatha": True},
               {"is_in_dhatupatha": False}),
    "1.3.10": ({"left_list": ("a", "b"), "right_list": ("x", "y"), "mapping": "index_wise"},
               {"left_list": ("a", "b"), "right_list": ("x",),     "mapping": "index_wise"}),
    "1.3.11": ({"rule_marker": "svarita", "is_adhikara": True},
               {"rule_marker": "anudatta", "is_adhikara": True}),
    "1.3.14": ({"voice": "kartari", "is_reciprocal": True},
               {"voice": "kartari", "is_reciprocal": False}),
    "1.3.15": ({"semantic": "gati", "is_reciprocal_block": True},
               {"semantic": "ordinary", "is_reciprocal_block": True}),
    "1.3.16": ({"upapada": "itaretara"},
               {"upapada": "anya"}),
    "1.3.20": ({"prefixes": ("ā",), "lemma": "dā", "semantic": "viharana_non_mouth"},
               {"prefixes": ("ā",), "lemma": "dā", "semantic": "ordinary"}),
    "1.3.22": ({"prefixes": ("sam",), "lemma": "sthā"},
               {"prefixes": ("upa",), "lemma": "sthā"}),
    "1.3.23": ({"lemma": "sthā", "semantic": "prakashana"},
               {"lemma": "sthā", "semantic": "ordinary"}),
    "1.3.26": ({"lemma": "sthā", "is_akarmaka": True},
               {"lemma": "sthā", "is_akarmaka": False}),
    "1.3.27": ({"prefixes": ("ud",), "lemma": "tap"},
               {"prefixes": ("ā",),  "lemma": "tap"}),
    "1.3.28": ({"prefixes": ("ā",),  "lemma": "yam"},
               {"prefixes": ("sam",),"lemma": "yam"}),
    "1.3.30": ({"prefixes": ("ni",), "lemma": "hve"},
               {"prefixes": ("anu",),"lemma": "hve"}),
    "1.3.31": ({"prefixes": ("ā",),  "lemma": "hve", "semantic": "spardha"},
               {"prefixes": ("ā",),  "lemma": "hve", "semantic": "ordinary"}),
    "1.3.33": ({"prefixes": ("adhi",), "semantic": "prasahana"},
               {"prefixes": ("adhi",), "semantic": "ordinary"}),
    "1.3.34": ({"prefixes": ("vi",), "karman_kind": "shabda"},
               {"prefixes": ("vi",), "karman_kind": "ordinary"}),
    "1.3.35": ({"prefixes": ("vi",), "is_akarmaka": True},
               {"prefixes": ("vi",), "is_akarmaka": False}),
    "1.3.36": ({"prefixes": ("ni",), "semantic": "sammanana"},
               {"prefixes": ("ni",), "semantic": "ordinary"}),
    "1.3.37": ({"karman_in_kartri": True, "karman_non_bodily": True},
               {"karman_in_kartri": True, "karman_non_bodily": False}),
    "1.3.38": ({"lemma": "kram", "semantic": "vrtti"},
               {"lemma": "kram", "semantic": "ordinary"}),
    "1.3.39": ({"prefixes": ("upa",), "lemma": "kram"},
               {"prefixes": ("sam",), "lemma": "kram"}),
    "1.3.41": ({"prefixes": ("vi",), "lemma": "kram", "semantic": "pada_viharana"},
               {"prefixes": ("vi",), "lemma": "kram", "semantic": "ordinary"}),
    "1.3.42": ({"prefixes": ("pra",), "lemma": "kram", "is_samartha": True},
               {"prefixes": ("pra",), "lemma": "kram", "is_samartha": False}),
    "1.3.43": ({"lemma": "kram", "prefixes": (), "optional": True},
               {"lemma": "kram", "prefixes": ("pra",), "optional": True}),
    "1.3.44": ({"lemma": "jñā", "semantic": "apahnava"},
               {"lemma": "jñā", "semantic": "ordinary"}),
    "1.3.45": ({"lemma": "jñā", "is_akarmaka": True},
               {"lemma": "jñā", "is_akarmaka": False}),
    "1.3.46": ({"prefixes": ("sam",), "lemma": "jñā", "semantic": "ordinary"},
               {"prefixes": ("sam",), "lemma": "jñā", "semantic": "adhyana"}),
    "1.3.47": ({"lemma": "vad", "semantic": "bhasana"},
               {"lemma": "vad", "semantic": "ordinary"}),
    "1.3.48": ({"lemma": "vad", "semantic": "samuccarana", "is_articulate": True},
               {"lemma": "vad", "semantic": "samuccarana", "is_articulate": False}),
    "1.3.49": ({"prefixes": ("anu",), "lemma": "vad", "is_akarmaka": True},
               {"prefixes": ("anu",), "lemma": "vad", "is_akarmaka": False}),
    "1.3.50": ({"lemma": "vad", "semantic": "vipralapa", "optional": True},
               {"lemma": "vad", "semantic": "ordinary",  "optional": True}),
    "1.3.51": ({"prefixes": ("ava",), "lemma": "grah"},
               {"prefixes": ("sam",), "lemma": "grah"}),
    "1.3.52": ({"prefixes": ("sam",), "lemma": "grah", "semantic": "pratijnana"},
               {"prefixes": ("sam",), "lemma": "grah", "semantic": "ordinary"}),
    "1.3.53": ({"prefixes": ("ud",), "lemma": "car", "is_akarmaka": False},
               {"prefixes": ("ud",), "lemma": "car", "is_akarmaka": True}),
    "1.3.54": ({"prefixes": ("sam",), "has_instrument": True},
               {"prefixes": ("sam",), "has_instrument": False}),
    "1.3.55": ({"lemma": "dā", "semantic": "receive", "has_dative": True},
               {"lemma": "dā", "semantic": "receive", "has_dative": False}),
    "1.3.56": ({"prefixes": ("upa",), "lemma": "yam", "semantic": "svakarana"},
               {"prefixes": ("upa",), "lemma": "yam", "semantic": "ordinary"}),
    "1.3.57": ({"suffix": "san", "lemma": "jñā"},
               {"suffix": "san", "lemma": "bhū"}),
    "1.3.58": ({"lemma": "jñā", "prefixes": ("anu",), "is_block": True},
               {"lemma": "jñā", "prefixes": ("sam",), "is_block": True}),
    "1.3.59": ({"prefixes": ("prati",), "lemma": "śru"},
               {"prefixes": ("sam",),   "lemma": "śru"}),
    "1.3.60": ({"lemma": "śad", "suffix_is_shit": True},
               {"lemma": "śad", "suffix_is_shit": False}),
    "1.3.61": ({"lemma": "mṛ", "lakara": "lun"},
               {"lemma": "mṛ", "lakara": "lat"}),
    "1.3.62": ({"suffix": "san", "pada": "atmanepada", "parent_pada": "atmanepada"},
               {"suffix": "san", "pada": "atmanepada", "parent_pada": "parasmaipada"}),
    "1.3.63": ({"lemma": "kṛ", "is_anuprayoga": True},
               {"lemma": "kṛ", "is_anuprayoga": False}),
    "1.3.64": ({"prefixes": ("pra",), "lemma": "yuj", "semantic": "ordinary"},
               {"prefixes": ("pra",), "lemma": "yuj", "semantic": "yajna_patra"}),
    "1.3.65": ({"prefixes": ("sam",), "lemma": "kṣṇu"},
               {"prefixes": ("ud",),  "lemma": "kṣṇu"}),
    "1.3.66": ({"lemma": "bhuj", "semantic": "eating"},
               {"lemma": "bhuj", "semantic": "avana"}),
    "1.3.67": ({"is_nic": True, "non_causal_karman": "becomes_causal_agent", "semantic": "ordinary"},
               {"is_nic": True, "non_causal_karman": "becomes_causal_agent", "semantic": "adhyana"}),
    "1.3.68": ({"lemma": "bhī", "hetubhaya": True},
               {"lemma": "bhī", "hetubhaya": False}),
    "1.3.69": ({"lemma": "gṛdh", "semantic": "pralambhana"},
               {"lemma": "gṛdh", "semantic": "ordinary"}),
    "1.3.70": ({"lemma": "lī", "semantic": "sammanana"},
               {"lemma": "lī", "semantic": "ordinary"}),
    "1.3.71": ({"lemma": "kṛ", "upapada": "mithyā", "is_abhyasa": True},
               {"lemma": "kṛ", "upapada": "mithyā", "is_abhyasa": False}),
    "1.3.73": ({"prefixes": ("apa",), "lemma": "vad"},
               {"prefixes": ("sam",), "lemma": "vad"}),
    "1.3.74": ({"lemma": "vad", "is_nic": True},
               {"lemma": "vad", "is_nic": False}),
    "1.3.75": ({"prefixes": ("sam",), "lemma": "yam", "semantic": "ordinary"},
               {"prefixes": ("sam",), "lemma": "yam", "semantic": "grantha"}),
    "1.3.76": ({"lemma": "jñā", "prefixes": ()},
               {"lemma": "jñā", "prefixes": ("anu",)}),
    "1.3.77": ({"action_implied_by_upapada": True, "optional": True},
               {"action_implied_by_upapada": False, "optional": True}),
    "1.3.79": ({"prefixes": ("anu",), "lemma": "kṛ"},
               {"prefixes": ("sam",), "lemma": "kṛ"}),
    "1.3.80": ({"prefixes": ("abhi",), "lemma": "kṣip"},
               {"prefixes": ("sam",),  "lemma": "kṣip"}),
    "1.3.81": ({"prefixes": ("pra",), "lemma": "vah"},
               {"prefixes": ("sam",), "lemma": "vah"}),
    "1.3.82": ({"prefixes": ("pari",), "lemma": "mṛṣ"},
               {"prefixes": ("sam",),  "lemma": "mṛṣ"}),
    "1.3.83": ({"prefixes": ("vi",),  "lemma": "ram"},
               {"prefixes": ("sam",), "lemma": "ram"}),
    "1.3.84": ({"prefixes": ("upa",), "lemma": "ram"},
               {"prefixes": ("sam",), "lemma": "ram"}),
    "1.3.85": ({"lemma": "ram", "is_akarmaka": True, "optional": True},
               {"lemma": "ram", "is_akarmaka": False, "optional": True}),
    "1.3.86": ({"lemma": "budh", "is_nic": True},
               {"lemma": "bhū",  "is_nic": True}),
    "1.3.87": ({"semantic": "nigarana", "is_nic": True},
               {"semantic": "ordinary", "is_nic": True}),
    "1.3.88": ({"is_nic": False, "is_akarmaka": True, "agent_is_sentient": True},
               {"is_nic": True,  "is_akarmaka": True, "agent_is_sentient": True}),
    "1.3.89": ({"lemma": "pā", "is_block": True},
               {"lemma": "bhū", "is_block": True}),
    "1.3.90": ({"suffix": "kyac", "optional": True},
               {"suffix": "san",  "optional": True}),
    "1.3.91": ({"root_class": "dyut", "lakara": "lun"},
               {"root_class": "dyut", "lakara": "lat"}),
    "1.3.92": ({"root_class": "vrt", "suffix": "sya"},
               {"root_class": "vrt", "suffix": "kta"}),
    "1.3.93": ({"lemma": "kḷp", "lakara": "lut"},
               {"lemma": "kḷp", "lakara": "lat"}),

    # 1.4 ---------------------------------------------------------------
    "1.4.1":  ({"in_range_to_kadara": True,  "competing_samjnas": ("a", "b"), "selected_count": 1},
               {"in_range_to_kadara": True,  "competing_samjnas": ("a", "b"), "selected_count": 2}),
    "1.4.2":  ({"rules_conflict": True, "selected": "later"},
               {"rules_conflict": True, "selected": "earlier"}),
    "1.4.4":  ({"stem_final": "ī", "becomes_iyan_or_uvan": True, "gender": "masculine"},
               {"stem_final": "ī", "becomes_iyan_or_uvan": True, "gender": "feminine"}),
    "1.4.5":  ({"following_suffix": "ām", "optional": True},
               {"following_suffix": "su", "optional": True}),
    "1.4.6":  ({"stem_final": "i", "stem_duration": "hrasva", "following_is_ngit": True},
               {"stem_final": "ī", "stem_duration": "dirgha", "following_is_ngit": True}),
    "1.4.8":  ({"stem": "pati", "in_compound": True},
               {"stem": "pati", "in_compound": False}),
    "1.4.9":  ({"is_vedic": True, "has_genitive_relation": True, "optional": True},
               {"is_vedic": False,"has_genitive_relation": True, "optional": True}),
    "1.4.15": ({"stem_final": "n", "following_suffix_class": "kya"},
               {"stem_final": "a", "following_suffix_class": "kya"}),
    "1.4.16": ({"stem_final": "n", "following_is_sit": True},
               {"stem_final": "n", "following_is_sit": False}),
    "1.4.19": ({"stem_final": "t", "suffix_meaning": "matup"},
               {"stem_final": "t", "suffix_meaning": "krt"}),
    "1.4.20": ({"stem": "ayasmaya", "is_vedic": True},
               {"stem": "ayasmaya", "is_vedic": False}),
    "1.4.21": ({"referent_count": "many", "number": "plural"},
               {"referent_count": "many", "number": "singular"}),
    "1.4.22": ({"referent_count": "two", "number": "dual"},
               {"referent_count": "two", "number": "plural"}),
    "1.4.23": ({"section": "karaka", "is_adhikara": True},
               {"section": "samjna", "is_adhikara": True}),
    "1.4.30": ({"context": "birth_source", "role": "apadana"},
               {"context": "birth_source", "role": "karman"}),
    "1.4.31": ({"verb": "bhū", "context": "origin_place", "role": "apadana"},
               {"verb": "gam", "context": "origin_place", "role": "apadana"}),
    "1.4.34": ({"verb": "ślāgh", "context": "intended_knowable", "role": "sampradana"},
               {"verb": "bhū",   "context": "intended_knowable", "role": "sampradana"}),
    "1.4.35": ({"verb": "dhṛ", "context": "creditor", "role": "sampradana"},
               {"verb": "dhṛ", "context": "ordinary", "role": "sampradana"}),
    "1.4.36": ({"verb": "spṛh", "context": "desired_object", "role": "sampradana"},
               {"verb": "spṛh", "context": "ordinary",      "role": "sampradana"}),
    "1.4.37": ({"verb_meaning": "krudh", "context": "angered_at", "role": "sampradana"},
               {"verb_meaning": "ordinary", "context": "angered_at", "role": "sampradana"}),
    "1.4.38": ({"verb_meaning": "krudh", "has_upasarga": True,  "role": "karman"},
               {"verb_meaning": "krudh", "has_upasarga": False, "role": "karman"}),
    "1.4.39": ({"verb": "rādh", "context": "inquired_about", "role": "sampradana"},
               {"verb": "bhū",  "context": "inquired_about", "role": "sampradana"}),
    "1.4.40": ({"prefixes": ("prati",), "verb": "śru", "context": "previous_speaker", "role": "kartr"},
               {"prefixes": ("sam",),   "verb": "śru", "context": "previous_speaker", "role": "kartr"}),
    "1.4.41": ({"prefixes": ("anu",), "verb": "gṛ", "role": "kartr"},
               {"prefixes": ("sam",), "verb": "gṛ", "role": "kartr"}),
    "1.4.43": ({"verb": "div", "context": "staked_object", "role": "karman"},
               {"verb": "div", "context": "ordinary",      "role": "karman"}),
    "1.4.44": ({"context": "hiring", "role": "sampradana", "optional": True},
               {"context": "hiring", "role": "karman",     "optional": True}),
    "1.4.46": ({"prefixes": ("adhi",), "verb": "sthā", "role": "karman"},
               {"prefixes": ("sam",),  "verb": "sthā", "role": "karman"}),
    "1.4.47": ({"prefixes": ("abhi",), "verb": "niviś", "role": "karman"},
               {"prefixes": ("sam",),  "verb": "niviś", "role": "karman"}),
    "1.4.48": ({"prefixes": ("upa",), "verb": "vas", "role": "karman"},
               {"prefixes": ("sam",), "verb": "vas", "role": "karman"}),
    "1.4.50": ({"is_unwanted_but_connected": True,  "role": "karman"},
               {"is_unwanted_but_connected": False, "role": "karman"}),
    "1.4.51": ({"is_unexpressed_object": True,  "role": "karman"},
               {"is_unexpressed_object": False, "role": "karman"}),
    "1.4.52": ({"verb_class": "gati", "is_nic": False, "role": "kartr"},
               {"verb_class": "gati", "is_nic": True,  "role": "kartr"}),
    "1.4.53": ({"verb": "hṛ", "optional": True},
               {"verb": "bhū","optional": True}),
    "1.4.55": ({"context": "instigator", "role": "kartr"},
               {"context": "ordinary",   "role": "kartr"}),
    "1.4.56": ({"in_pre_rishvara_section": True, "samjna": "nipata"},
               {"in_pre_rishvara_section": False,"samjna": "nipata"}),
    "1.4.57": ({"word": "ca", "is_substantive": False},
               {"word": "ca", "is_substantive": True}),
    "1.4.61": ({"word_class": "cvi"},
               {"word_class": "ordinary"}),
    "1.4.62": ({"is_imitation": True, "followed_by_iti": False},
               {"is_imitation": True, "followed_by_iti": True}),
    "1.4.63": ({"word": "sat",  "semantic": "adara"},
               {"word": "sat",  "semantic": "ordinary"}),
    "1.4.64": ({"word": "alam", "semantic": "bhushana"},
               {"word": "alam", "semantic": "ordinary"}),
    "1.4.65": ({"word": "antar","semantic": "aparigraha"},
               {"word": "antar","semantic": "ordinary"}),
    "1.4.66": ({"word": "manas","semantic": "shraddha_pratighata"},
               {"word": "manas","semantic": "ordinary"}),
    "1.4.67": ({"word": "puras"},
               {"word": "agre"}),
    "1.4.68": ({"word": "astam"},
               {"word": "agni"}),
    "1.4.69": ({"word": "accha", "verb_meaning": "gati"},
               {"word": "accha", "verb_meaning": "ordinary"}),
    "1.4.70": ({"word": "adas", "semantic": "ordinary"},
               {"word": "adas", "semantic": "upadesha"}),
    "1.4.71": ({"word": "tiras","semantic": "antardha"},
               {"word": "tiras","semantic": "ordinary"}),
    "1.4.72": ({"verb": "kṛ", "optional": True},
               {"verb": "bhū","optional": True}),
    "1.4.73": ({"word": "upāje"},
               {"word": "agni"}),
    "1.4.74": ({"word_class": "sakshatprabhrti"},
               {"word_class": "ordinary"}),
    "1.4.75": ({"word": "urasi", "semantic": "ordinary"},
               {"word": "urasi", "semantic": "atyadhana"}),
    "1.4.76": ({"word_class": "madhyepade"},
               {"word_class": "ordinary"}),
    "1.4.77": ({"word": "haste", "semantic": "upayamana"},
               {"word": "haste", "semantic": "ordinary"}),
    "1.4.78": ({"word": "prādhvam", "semantic": "bandhana"},
               {"word": "prādhvam", "semantic": "ordinary"}),
    "1.4.79": ({"word": "jīvikā", "semantic": "aupamya"},
               {"word": "jīvikā", "semantic": "ordinary"}),
    "1.4.80": ({"samjna": "gati", "position": "before_dhatu"},
               {"samjna": "gati", "position": "after_dhatu"}),
    "1.4.81": ({"is_vedic": True,  "samjna": "gati", "position": "after_dhatu"},
               {"is_vedic": False, "samjna": "gati", "position": "after_dhatu"}),
    "1.4.82": ({"samjna": "gati", "is_separated": True},
               {"samjna": "gati", "is_separated": False}),
    "1.4.83": ({"section": "karmapravacaniya", "is_adhikara": True},
               {"section": "karaka",           "is_adhikara": True}),
    "1.4.84": ({"word": "anu", "semantic": "lakshana"},
               {"word": "anu", "semantic": "ordinary"}),
    "1.4.85": ({"word": "anu", "semantic": "trtiya_artha"},
               {"word": "anu", "semantic": "ordinary"}),
    "1.4.86": ({"word": "anu", "semantic": "hina"},
               {"word": "anu", "semantic": "ordinary"}),
    "1.4.87": ({"word": "upa", "semantic": "adhika"},
               {"word": "upa", "semantic": "ordinary"}),
    "1.4.88": ({"word": "apa", "semantic": "varjana"},
               {"word": "apa", "semantic": "ordinary"}),
    "1.4.89": ({"word": "ā",   "semantic": "maryada"},
               {"word": "ā",   "semantic": "ordinary"}),
    "1.4.90": ({"word": "prati", "semantic": "lakshana"},
               {"word": "prati", "semantic": "ordinary"}),
    "1.4.91": ({"word": "abhi", "semantic": "ordinary"},
               {"word": "abhi", "semantic": "bhaga"}),
    "1.4.92": ({"word": "prati", "semantic": "pratinidhi"},
               {"word": "prati", "semantic": "ordinary"}),
    "1.4.93": ({"word": "adhi", "is_anarthaka": True},
               {"word": "adhi", "is_anarthaka": False}),
    "1.4.94": ({"word": "su", "semantic": "puja"},
               {"word": "su", "semantic": "ordinary"}),
    "1.4.95": ({"word": "ati", "semantic": "atikramana"},
               {"word": "ati", "semantic": "ordinary"}),
    "1.4.96": ({"word": "api", "semantic": "garha"},
               {"word": "api", "semantic": "ordinary"}),
    "1.4.97": ({"word": "adhi", "semantic": "ishvara"},
               {"word": "adhi", "semantic": "ordinary"}),
    "1.4.98": ({"word": "adhi", "verb": "kṛ", "optional": True},
               {"word": "adhi", "verb": "bhū","optional": True}),
    "1.4.99": ({"label_origin": "l_substitute", "pada": "parasmaipada"},
               {"label_origin": "l_substitute", "pada": "atmanepada"}),
    "1.4.100":({"ending_class": "tan", "pada": "atmanepada"},
               {"ending_class": "tan", "pada": "parasmaipada"}),
    "1.4.101":({"suffix_class": "tin", "person_label": "prathama"},
               {"suffix_class": "tin", "person_label": "fourth"}),
    "1.4.102":({"suffix_class": "tin", "number": "dual"},
               {"suffix_class": "tin", "number": "fourth"}),
    "1.4.103":({"suffix_class": "sup"},
               {"suffix_class": "krt"}),
    "1.4.104":({"suffix_class": "sup", "is_vibhakti": True},
               {"suffix_class": "krt", "is_vibhakti": True}),
    "1.4.105":({"upapada": "yuṣmad", "is_samanadhikarana": True, "person_label": "madhyama"},
               {"upapada": "yuṣmad", "is_samanadhikarana": False,"person_label": "madhyama"}),
    "1.4.106":({"verb": "man", "context": "prahasa", "person_label": "uttama", "number": "singular"},
               {"verb": "man", "context": "ordinary","person_label": "uttama", "number": "singular"}),
    "1.4.107":({"upapada": "asmad",   "person_label": "uttama"},
               {"upapada": "yuṣmad",  "person_label": "uttama"}),
    "1.4.108":({"upapada": "shesha",  "person_label": "prathama"},
               {"upapada": "asmad",   "person_label": "prathama"}),
}


# ---------------------------------------------------------------------------
# Registry metadata
# ---------------------------------------------------------------------------

_SAMJNA = "samjna"
_PARIBHASHA = "paribhasha"
_VIDHI = "vidhi"
_PRATISEDHA = "pratisedha"
_VIBHASHA = "vibhasha"
_ADHIKARA = "adhikara"


def _meta_samjna(summary: str, tag: str) -> SutraMeta:
    return SutraMeta(_SAMJNA, summary, (tag,))


def _meta_vidhi(summary: str, tag: str) -> SutraMeta:
    return SutraMeta(_VIDHI, summary, (tag,))


def _meta_vibhasha(summary: str, tag: str) -> SutraMeta:
    return SutraMeta(_VIBHASHA, summary, (tag,))


def _meta_pratisedha(summary: str, tag: str) -> SutraMeta:
    return SutraMeta(_PRATISEDHA, summary, (tag,))


def _meta_paribhasha(summary: str, tag: str) -> SutraMeta:
    return SutraMeta(_PARIBHASHA, summary, (tag,))


META: dict[str, SutraMeta] = {
    # 1.2 kit/ṅit + accent + prātipadika + lup/luk + ekaśeṣa-adjacent
    "1.2.3":  _meta_vibhasha("vibhāṣorṇoḥ: optional kit/aṅit after ūrṇu", "samjna:kit-optional"),
    "1.2.10": _meta_vidhi("halantāc ca: san after hal-final ik-root is kit before jhal", "samjna:kit"),
    "1.2.16": _meta_vibhasha("vibhāṣopayamane: optional kit/aṅit for yam in marriage sense", "samjna:kit-optional"),
    "1.2.21": _meta_vibhasha("optional after u-upadhā in bhāva/ādikarman", "samjna:kit-optional"),
    "1.2.22": _meta_vidhi("pūṅaḥ ktvā ca: ktvā/san after pū is kit", "samjna:kit"),
    "1.2.23": _meta_vibhasha("optional after n-upadhā tha/pha-final", "samjna:kit-optional"),
    "1.2.24": _meta_vibhasha("optional kit for vañc/luñc/ṛt", "samjna:kit-optional"),
    "1.2.25": _meta_vibhasha("Kāśyapa's optional kit for tṛṣ/mṛṣ/kṛś", "samjna:kit-optional"),
    "1.2.27": _meta_samjna("ūkālo'jjhrasvadīrghaplutaḥ: vowels have three durations", "samjna:duration"),
    "1.2.28": _meta_samjna("acaś ca: same applies to all ac (vowels)", "samjna:duration"),
    "1.2.29": _meta_samjna("uccair udāttaḥ: high-pitch is udātta", "samjna:accent"),
    "1.2.30": _meta_samjna("nīcair anudāttaḥ: low-pitch is anudātta", "samjna:accent"),
    "1.2.31": _meta_samjna("samāhāraḥ svaritaḥ: combined pitch is svarita", "samjna:accent"),
    "1.2.32": _meta_samjna("tasyādita udāttam ardha-hrasvam: first half-mātrā of svarita is udātta", "samjna:accent"),
    "1.2.33": _meta_samjna("ekaśruti dūrāt sambuddhau: monotone vocative from distance", "samjna:accent"),
    "1.2.34": _meta_samjna("yajñakarmaṇy ajapanyūṅkhasāmasu: ekaśruti in ritual minus japa/nyūṅkha/sāman", "samjna:accent"),
    "1.2.35": _meta_vibhasha("uccaistarāṃ vā vaṣaṭkāraḥ: vaṣaṭ optionally with udāttatara", "samjna:accent"),
    "1.2.36": _meta_vibhasha("vibhāṣā chandasi: same is optional in Vedic", "samjna:accent"),
    "1.2.37": _meta_vidhi("na subrahmaṇyāyāṃ ...: in subrahmaṇyā chant, svarita → udātta", "samjna:accent"),
    "1.2.38": _meta_samjna("devabrahmaṇor anudāttaḥ: deva/brahman take anudātta", "samjna:accent"),
    "1.2.39": _meta_samjna("svaritāt saṃhitāyām anudāttānām: anudātta after svarita in saṃhitā", "samjna:accent"),
    "1.2.40": _meta_samjna("udāttasvaritaparasya sannataraḥ: below-anudātta after udātta/svarita", "samjna:accent"),
    "1.2.42": _meta_samjna("tatpuruṣaḥ samānādhikaraṇaḥ karmadhārayaḥ", "samjna:karmadharaya"),
    "1.2.43": _meta_samjna("prathamānirdiṣṭaṃ samāsa upasarjanam", "samjna:upasarjana"),
    "1.2.44": _meta_samjna("ekavibhakti cāpūrvanipāte: single-case member is upasarjana too", "samjna:upasarjana"),
    "1.2.45": _meta_samjna("arthavad adhātur apratyayaḥ prātipadikam", "samjna:pratipadika"),
    "1.2.46": _meta_samjna("kṛt-taddhita-samāsāś ca: derived bases are also prātipadika", "samjna:pratipadika"),
    "1.2.47": _meta_vidhi("hrasvo napuṃsake prātipadikasya: neuter final vowel is shortened", "operation:hrasva"),
    "1.2.48": _meta_vidhi("go-striyor upasarjanasya: go/strī upasarjana shortened", "operation:hrasva"),
    "1.2.49": _meta_vidhi("luk taddhitaluki: certain operations still proceed under taddhita-luk", "operation:luk"),
    "1.2.50": _meta_vidhi("id goṇyāḥ: id substitution in goṇī domain", "operation:substitution"),
    "1.2.51": _meta_paribhasha("lupi yuktavad: lup preserves gender/number", "meta:lup-preservation"),
    "1.2.52": _meta_paribhasha("viśeṣaṇānāṃ cājāteḥ: non-jāti adjectives preserve agreement", "meta:adjective-agreement"),
    "1.2.53": _meta_paribhasha("tad aśiṣyaṃ saṃjñāpramāṇatvāt: conventional names are aśiṣya", "meta:convention"),
    "1.2.54": _meta_paribhasha("lub-yogāprakhyānāt: lup inferred from absence", "meta:lup-inference"),
    "1.2.55": _meta_paribhasha("yogapramāṇe: absence under yoga evidence is lup", "meta:lup-inference"),
    "1.2.56": _meta_paribhasha("pradhānapratyayārthavacanam: principal suffix-meaning is primary", "meta:suffix-meaning"),
    "1.2.57": _meta_paribhasha("kāla-upasarjane ca tulyam: same in temporal subordination", "meta:upasarjana"),
    "1.2.58": _meta_vibhasha("jāty-ākhyāyām: optional plural for one in class-naming", "samjna:number-optional"),
    "1.2.59": _meta_vidhi("asmado dvayoś ca: asmad plural even for two", "samjna:number"),
    "1.2.60": _meta_vidhi("phalgunī-proṣṭhapadānāṃ ca nakṣatre: nakṣatra plural", "samjna:number"),
    "1.2.61": _meta_vidhi("chandasi punarvasvor ekavacanam: Vedic singular for punarvasu", "samjna:number"),
    "1.2.62": _meta_vidhi("viśākhayoś ca: same for viśākhā", "samjna:number"),
    "1.2.63": _meta_vidhi("tiṣya-punarvasvor nakṣatra-dvandve bahuvacanasya: plural → dual in dvandva", "samjna:number"),
    "1.2.66": _meta_paribhasha("strī puṁvac ca: strī behaves like masculine counterpart", "meta:gender-agreement"),

    # 1.3 dhātu + paribhāṣās + ātmanepada/parasmaipada
    "1.3.1":  _meta_samjna("bhūvādayo dhātavaḥ: dhātu-saṃjñā", "samjna:dhatu"),
    "1.3.10": _meta_paribhasha("yathāsaṃkhyam anudeśaḥ: same-count lists pair index-wise", "meta:yathasamkhya"),
    "1.3.11": _meta_paribhasha("svaritenādhikāraḥ: an adhikāra inherits via svarita", "meta:adhikara-inheritance"),
    "1.3.14": _meta_vidhi("kartari karma-vyatihāre: reciprocal kartari → ātmanepada", "pada:atmanepada"),
    "1.3.15": _meta_pratisedha("na gati-hiṃsārthebhyaḥ: blocks 1.3.14 for motion/injury", "block:atmanepada"),
    "1.3.16": _meta_vidhi("itaretarānyonyopapadāc ca: keeps reciprocal domain with itaretara/anyonya", "pada:atmanepada"),
    "1.3.20": _meta_vidhi("āṅo do'nāsye viharaṇe: ā + dā non-mouth → ātmanepada", "pada:atmanepada"),
    "1.3.22": _meta_vidhi("samavapravibhyaḥ sthaḥ: sam/ava/pra/vi + sthā → ātmanepada", "pada:atmanepada"),
    "1.3.23": _meta_vidhi("prakāśana-stheyākhyayoś ca: sthā in shining/judging → ātmanepada", "pada:atmanepada"),
    "1.3.26": _meta_vidhi("akarmakāc ca: intransitive use extends 1.3.23", "pada:atmanepada"),
    "1.3.27": _meta_vidhi("udvibhyāṃ tapaḥ: ud/vi + tap → ātmanepada", "pada:atmanepada"),
    "1.3.28": _meta_vidhi("āṅo yamahanaḥ: ā + yam/han → ātmanepada", "pada:atmanepada"),
    "1.3.30": _meta_vidhi("nisamupavibhyo hvaḥ: ni/sam/upa/vi + hve → ātmanepada", "pada:atmanepada"),
    "1.3.31": _meta_vidhi("spardhāyām āṅaḥ: ā + hve in competition → ātmanepada", "pada:atmanepada"),
    "1.3.33": _meta_vidhi("adheḥ prasahane: adhi in endure-sense → ātmanepada", "pada:atmanepada"),
    "1.3.34": _meta_vidhi("veḥ śabda-karmaṇaḥ: vi with sound-object → ātmanepada", "pada:atmanepada"),
    "1.3.35": _meta_vidhi("akarmakāc ca: intransitive extension of 1.3.34", "pada:atmanepada"),
    "1.3.36": _meta_vidhi("sammānanotsañjana...niyaḥ: ni in listed senses → ātmanepada", "pada:atmanepada"),
    "1.3.37": _meta_vidhi("kartṛsthe cāśarīre karmaṇi: non-bodily karman in kartṛ → ātmanepada", "pada:atmanepada"),
    "1.3.38": _meta_vidhi("vṛttisargatāyaneṣu kramaḥ: kram in use/devotion/extension → ātmanepada", "pada:atmanepada"),
    "1.3.39": _meta_vidhi("upaparābhyām: upa/parā + kram → ātmanepada", "pada:atmanepada"),
    "1.3.41": _meta_vidhi("veḥ pāda-viharaṇe: vi + kram in stepping → ātmanepada", "pada:atmanepada"),
    "1.3.42": _meta_vidhi("propābhyāṃ samarthābhyām: pra/upa + kram in suitable sense → ātmanepada", "pada:atmanepada"),
    "1.3.43": _meta_vibhasha("anupasargād vā: kram without upasarga optionally → ātmanepada", "pada:atmanepada-optional"),
    "1.3.44": _meta_vidhi("apahnave jñaḥ: jñā in denying → ātmanepada", "pada:atmanepada"),
    "1.3.45": _meta_vidhi("akarmakāc ca: intransitive jñā extension", "pada:atmanepada"),
    "1.3.46": _meta_vidhi("sampratibhyām anādhyāne: sam/prati + jñā outside remembering → ātmanepada", "pada:atmanepada"),
    "1.3.47": _meta_vidhi("bhāsanopasambhāṣā...vadaḥ: vad in listed senses → ātmanepada", "pada:atmanepada"),
    "1.3.48": _meta_vidhi("vyaktavācāṃ samuccāraṇe: vad in articulate joint-speaking → ātmanepada", "pada:atmanepada"),
    "1.3.49": _meta_vidhi("anor akarmakāt: anu + vad intransitive → ātmanepada", "pada:atmanepada"),
    "1.3.50": _meta_vibhasha("vibhāṣā vipralāpe: optional in quarrelling sense", "pada:atmanepada-optional"),
    "1.3.51": _meta_vidhi("avād graḥ: ava + grah → ātmanepada", "pada:atmanepada"),
    "1.3.52": _meta_vidhi("samaḥ pratijñāne: sam + grah in promising → ātmanepada", "pada:atmanepada"),
    "1.3.53": _meta_vidhi("udaścaraḥ sakarmakāt: ud + car transitive → ātmanepada", "pada:atmanepada"),
    "1.3.54": _meta_vidhi("samas tṛtīyāyuktāt: sam + instrument-present → ātmanepada", "pada:atmanepada"),
    "1.3.55": _meta_vidhi("dāṇaś ca sā cec caturthyarthe: dā receive-with-dative → ātmanepada", "pada:atmanepada"),
    "1.3.56": _meta_vidhi("upād yamaḥ svakaraṇe: upa + yam in marrying → ātmanepada", "pada:atmanepada"),
    "1.3.57": _meta_vidhi("jñā-śru-smṛ-dṛśāṃ sanaḥ: san after these → ātmanepada", "pada:atmanepada"),
    "1.3.58": _meta_pratisedha("nānor jñaḥ: blocks 1.3.57 when prefixed with anu", "block:atmanepada"),
    "1.3.59": _meta_vidhi("pratyāṅbhyāṃ śruvaḥ: prati/ā + śru → ātmanepada", "pada:atmanepada"),
    "1.3.60": _meta_vidhi("śadeḥ śitaḥ: śad before śit-suffix → ātmanepada", "pada:atmanepada"),
    "1.3.61": _meta_vidhi("mriyater luṅliṅoś ca: mṛ in luṅ/liṅ → ātmanepada", "pada:atmanepada"),
    "1.3.62": _meta_paribhasha("pūrvavat sanaḥ: san continues parent root's pada", "meta:pada-inheritance"),
    "1.3.63": _meta_paribhasha("āmpratyayavat: anuprayoga of kṛ behaves like ām-suffix", "meta:pada-inheritance"),
    "1.3.64": _meta_vidhi("propābhyāṃ yujer ayajñapātreṣu: pra/upa + yuj outside ritual-vessel → ātmanepada", "pada:atmanepada"),
    "1.3.65": _meta_vidhi("samaḥ kṣṇuvaḥ: sam + kṣṇu → ātmanepada", "pada:atmanepada"),
    "1.3.66": _meta_vidhi("bhujo'navane: bhuj outside protecting → ātmanepada", "pada:atmanepada"),
    "1.3.67": _meta_vidhi("ṇer aṇau: causee becomes causal agent", "operation:karma-shift"),
    "1.3.68": _meta_vidhi("bhīsmyor hetubhaye: bhī/smi with fear-cause → ātmanepada", "pada:atmanepada"),
    "1.3.69": _meta_vidhi("gṛdhi-vañcyoḥ pralambhane: gṛdh/vañc in deceiving → ātmanepada", "pada:atmanepada"),
    "1.3.70": _meta_vidhi("liyaḥ sammānana-śālinīkaraṇayoś ca: lī in honor/showy senses → ātmanepada", "pada:atmanepada"),
    "1.3.71": _meta_vidhi("mithyopapadāt kṛño'bhyāse: kṛ + mithyā in repetition → ātmanepada", "pada:atmanepada"),
    "1.3.73": _meta_vidhi("apād vadaḥ: apa + vad → ātmanepada", "pada:atmanepada"),
    "1.3.74": _meta_vidhi("ṇicaś ca: ṇic of vad → ātmanepada continues", "pada:atmanepada"),
    "1.3.75": _meta_vidhi("samudāṅbhyo yamo'granthe: sam/ud/ā + yam outside book → ātmanepada", "pada:atmanepada"),
    "1.3.76": _meta_vidhi("anupasargāj jñaḥ: jñā without upasarga → ātmanepada", "pada:atmanepada"),
    "1.3.77": _meta_vibhasha("vibhāṣopapadena pratīyamāne: optional when action implied", "pada:atmanepada-optional"),
    "1.3.79": _meta_vidhi("anuparābhyāṃ kṛñaḥ: anu/parā + kṛ → ātmanepada", "pada:atmanepada"),
    "1.3.80": _meta_vidhi("abhi-prati-atibhyaḥ kṣipaḥ: abhi/prati/ati + kṣip → ātmanepada", "pada:atmanepada"),
    "1.3.81": _meta_vidhi("prād vahaḥ: pra + vah → ātmanepada", "pada:atmanepada"),
    "1.3.82": _meta_vidhi("parer mṛṣaḥ: pari + mṛṣ → ātmanepada", "pada:atmanepada"),
    "1.3.83": _meta_vidhi("vyāṅparibhyo ramaḥ: vi/ā/pari + ram → ātmanepada", "pada:atmanepada"),
    "1.3.84": _meta_vidhi("upāc ca: upa + ram → ātmanepada", "pada:atmanepada"),
    "1.3.85": _meta_vibhasha("vibhāṣā'karmakāt: optional for intransitive ram", "pada:atmanepada-optional"),
    "1.3.86": _meta_vidhi("budha-yudha...ṇeḥ: causatives of listed roots → ātmanepada", "pada:atmanepada"),
    "1.3.87": _meta_vidhi("nigaraṇa-calanārthebhyaḥ: causatives of swallowing/moving → ātmanepada", "pada:atmanepada"),
    "1.3.88": _meta_vidhi("aṇāv akarmakāt cittavatkartṛkāt: non-causal intransitive with sentient agent", "pada:atmanepada"),
    "1.3.89": _meta_pratisedha("na pādamy...: blocks 1.3.88 for listed roots", "block:atmanepada"),
    "1.3.90": _meta_vibhasha("vā kyaṣaḥ: optional after kyac", "pada:atmanepada-optional"),
    "1.3.91": _meta_vidhi("dyud-bhyo luṅi: dyut-roots in luṅ → ātmanepada", "pada:atmanepada"),
    "1.3.92": _meta_vidhi("vṛd-bhyaḥ syasanoḥ: vṛt-roots in sya/san → ātmanepada", "pada:atmanepada"),
    "1.3.93": _meta_vidhi("luṭi ca kḷpaḥ: kḷp in luṭ → ātmanepada", "pada:atmanepada"),

    # 1.4 priority + saṃjñā extensions + kāraka + nipāta/gati/karmapravacanīya + tiṅ labels
    "1.4.1":  _meta_paribhasha("ā kaḍārād ekā saṃjñā: only one saṃjñā in the range", "meta:samjna-priority"),
    "1.4.2":  _meta_paribhasha("vipratiṣedhe paraṃ kāryam: later rule wins", "meta:rule-priority"),
    "1.4.4":  _meta_pratisedha("neyaṅuvaṅsthānāv astrī: ī/ū-final non-strī blocks nadī", "block:nadi"),
    "1.4.5":  _meta_vibhasha("vā'mi: optional before ām", "samjna:nadi-optional"),
    "1.4.6":  _meta_samjna("ṅiti hrasvaś ca: short i/u-final before ṅit is nadī", "samjna:nadi"),
    "1.4.8":  _meta_samjna("patiḥ samāsa eva: pati gets ghi only in compounds", "samjna:ghi"),
    "1.4.9":  _meta_vibhasha("ṣaṣṭhī-yuktaś chandasi vā: Vedic optional", "samjna:nadi-optional"),
    "1.4.15": _meta_pratisedha("naḥ kye: n-final before kya blocks pada-saṁjñā", "block:pada"),
    "1.4.16": _meta_pratisedha("siti ca: same before sit", "block:pada"),
    "1.4.19": _meta_samjna("tasau matvarthe: t/s-final + matup-meaning → bha", "samjna:bha"),
    "1.4.20": _meta_samjna("ayasmayādīni chandasi: Vedic bha exceptions", "samjna:bha"),
    "1.4.21": _meta_samjna("bahuṣu bahuvacanam: many → plural", "samjna:number"),
    "1.4.22": _meta_samjna("dvyekayor dvivacanaikavacane: two → dual, one → singular", "samjna:number"),
    "1.4.23": _meta_paribhasha("kārake: opens kāraka section (adhikāra)", "meta:adhikara"),
    "1.4.30": _meta_samjna("janikartuḥ prakṛtiḥ: birth-source → apādāna", "karaka:apadana"),
    "1.4.31": _meta_samjna("bhuvaḥ prabhavaḥ: with bhū, origin → apādāna", "karaka:apadana"),
    "1.4.34": _meta_samjna("ślāghahnu...: intended-knowable → sampradāna", "karaka:sampradana"),
    "1.4.35": _meta_samjna("dhāreruttamarṇaḥ: creditor → sampradāna", "karaka:sampradana"),
    "1.4.36": _meta_samjna("spṛher īpsitaḥ: spṛh's desired → sampradāna", "karaka:sampradana"),
    "1.4.37": _meta_samjna("krudha-druh...kopaḥ: angered-at → sampradāna", "karaka:sampradana"),
    "1.4.38": _meta_vidhi("krudha-druhor upasṛṣṭayoḥ karma: prefixed → karman", "karaka:karman"),
    "1.4.39": _meta_samjna("rādhīkṣyor yasya vipraśnaḥ: inquired-about → sampradāna", "karaka:sampradana"),
    "1.4.40": _meta_samjna("pratyāṅbhyāṃ śruvaḥ pūrvasya kartā: previous-speaker → kartṛ", "karaka:kartr"),
    "1.4.41": _meta_samjna("anu-prati-gṛṇaś ca: previous-speaker → kartṛ (gṛ)", "karaka:kartr"),
    "1.4.43": _meta_vidhi("divaḥ karma ca: staked-object → karman with div", "karaka:karman"),
    "1.4.44": _meta_vibhasha("parikrayaṇe sampradānam anyatarasyām: optional sampradāna in hiring", "karaka:sampradana-optional"),
    "1.4.46": _meta_vidhi("adhi-śīṅ-sthā-āsām karma: location → karman with adhi+rest verbs", "karaka:karman"),
    "1.4.47": _meta_vidhi("abhi-niviśaś ca: same for abhi+niviś", "karaka:karman"),
    "1.4.48": _meta_vidhi("upānvadhyāṅvasaḥ: same for upa/anu/adhi/ā + vas", "karaka:karman"),
    "1.4.50": _meta_samjna("tathā-yuktaṃ cānipsītam: unwanted-but-connected → karman", "karaka:karman"),
    "1.4.51": _meta_samjna("akathitaṃ ca: unexpressed object → karman", "karaka:karman"),
    "1.4.52": _meta_vidhi("gatibuddhi...aṇi kartā: non-causal agent of listed-class becomes karman under ṇic", "karaka:role-shift"),
    "1.4.53": _meta_vibhasha("hṛkror anyatarasyām: optional karman with hṛ/kṛ", "karaka:karman-optional"),
    "1.4.55": _meta_samjna("tatprayojako hetuś ca: instigator → kartṛ", "karaka:kartr"),
    "1.4.56": _meta_paribhasha("prāg rīśvarān nipātāḥ: opens nipāta section", "samjna:nipata"),
    "1.4.57": _meta_samjna("cādayo'sattve: ca-etc. are nipātas when not substantive", "samjna:nipata"),
    "1.4.61": _meta_samjna("ūry-ādi-cvi-ḍāc ca: these are gati", "samjna:gati"),
    "1.4.62": _meta_samjna("anukaraṇaṃ cānitiparam: imitation not followed by iti is gati", "samjna:gati"),
    "1.4.63": _meta_samjna("ādarānādarayoḥ sadasatī: sat/asat in respect/disrespect are gati", "samjna:gati"),
    "1.4.64": _meta_samjna("bhūṣaṇe'lam: alam in adornment is gati", "samjna:gati"),
    "1.4.65": _meta_samjna("antar-aparigrahe: antar in non-grasping is gati", "samjna:gati"),
    "1.4.66": _meta_samjna("kaṇe-manasī śraddhā-pratīghāte: in faith-obstruction sense", "samjna:gati"),
    "1.4.67": _meta_samjna("puro'vyayam: puras is avyaya (gati)", "samjna:gati"),
    "1.4.68": _meta_samjna("astaṃ ca: astam is gati", "samjna:gati"),
    "1.4.69": _meta_samjna("accha gaty-arthavadeṣu: accha with motion verbs is gati", "samjna:gati"),
    "1.4.70": _meta_samjna("ado'nupadeśe: adas outside instruction is gati", "samjna:gati"),
    "1.4.71": _meta_samjna("tiro'ntardhau: tiras in concealment is gati", "samjna:gati"),
    "1.4.72": _meta_vibhasha("vibhāṣā kṛñi: optional gati with kṛ", "samjna:gati-optional"),
    "1.4.73": _meta_samjna("upāje'nvāje: these are gati", "samjna:gati"),
    "1.4.74": _meta_samjna("sākṣātprabhṛtīni ca: sākṣāt-list is gati", "samjna:gati"),
    "1.4.75": _meta_samjna("anatyādhāna urasimanasī: urasi/manasi (not laying-on) is gati", "samjna:gati"),
    "1.4.76": _meta_samjna("madhye-pade-nivacane ca: madhye-pada-type is gati", "samjna:gati"),
    "1.4.77": _meta_samjna("nityaṃ haste pāṇāv upayamane: in marriage, fixed gati", "samjna:gati"),
    "1.4.78": _meta_samjna("prādhvaṃ bandhane: prādhvam in binding is gati", "samjna:gati"),
    "1.4.79": _meta_samjna("jīvikopaniṣadāv aupamye: jīvikā/upaniṣad in simile are gati", "samjna:gati"),
    "1.4.80": _meta_paribhasha("te prāg dhātoḥ: gati precedes dhātu", "meta:gati-position"),
    "1.4.81": _meta_vibhasha("chandasi pare'pi: Vedic allows gati after dhātu", "meta:gati-position-optional"),
    "1.4.82": _meta_paribhasha("vyavahitāś ca: gati may be separated", "meta:gati-position"),
    "1.4.83": _meta_paribhasha("karmapravacanīyāḥ: opens karmapravacanīya section", "meta:adhikara"),
    "1.4.84": _meta_samjna("anur lakṣaṇe: anu in 'sign-of' sense", "samjna:karmapravacaniya"),
    "1.4.85": _meta_samjna("tṛtīyā'rthe: anu in instrumental-sense", "samjna:karmapravacaniya"),
    "1.4.86": _meta_samjna("hīne: anu in 'inferior' sense", "samjna:karmapravacaniya"),
    "1.4.87": _meta_samjna("upo'dhike ca: upa in 'superior' sense", "samjna:karmapravacaniya"),
    "1.4.88": _meta_samjna("apa-parī varjane: apa/pari in 'except'", "samjna:karmapravacaniya"),
    "1.4.89": _meta_samjna("āṅ maryādā-vacane: ā in 'up-to'", "samjna:karmapravacaniya"),
    "1.4.90": _meta_samjna("lakṣaṇetthambhūta...: prati/pari/anu in listed senses", "samjna:karmapravacaniya"),
    "1.4.91": _meta_samjna("abhir abhāge: abhi in non-share", "samjna:karmapravacaniya"),
    "1.4.92": _meta_samjna("pratiḥ pratinidhi-pratidānayoḥ: prati in substitute/repay", "samjna:karmapravacaniya"),
    "1.4.93": _meta_samjna("adhi-parī anarthakau: when meaningless", "samjna:karmapravacaniya"),
    "1.4.94": _meta_samjna("suḥ pūjāyām: su in worship", "samjna:karmapravacaniya"),
    "1.4.95": _meta_samjna("atir atikramaṇe ca: ati in 'crossing-beyond'", "samjna:karmapravacaniya"),
    "1.4.96": _meta_samjna("apiḥ ...samuccayeṣu: api in listed senses", "samjna:karmapravacaniya"),
    "1.4.97": _meta_samjna("adhir īśvare: adhi in lord-over", "samjna:karmapravacaniya"),
    "1.4.98": _meta_vibhasha("vibhāṣā kṛñi: optional karmapravacanīya with kṛ", "samjna:karmapravacaniya-optional"),
    "1.4.99": _meta_samjna("laḥ parasmaipadam: l-substitutes that are parasmaipada labels", "samjna:parasmaipada"),
    "1.4.100":_meta_samjna("taṅānāv ātmanepadam: taṅ/āna are ātmanepada labels", "samjna:atmanepada"),
    "1.4.101":_meta_samjna("tiṅas trīṇi trīṇi prathamamadhyamottamāḥ: tiṅ person triples", "samjna:person"),
    "1.4.102":_meta_samjna("tāny ekavacana...: each triple is sg/du/pl", "samjna:number"),
    "1.4.103":_meta_samjna("supaḥ: sup endings", "samjna:sup"),
    "1.4.104":_meta_samjna("vibhaktiś ca: tiṅ and sup are also vibhakti", "samjna:vibhakti"),
    "1.4.105":_meta_samjna("yuṣmadyupapade ... madhyamaḥ: with yuṣmad → madhyama", "samjna:person"),
    "1.4.106":_meta_samjna("prahāse ca manyo'pa-pade manyater uttama ekavac ca", "samjna:person"),
    "1.4.107":_meta_samjna("asmady uttamaḥ: with asmad → uttama", "samjna:person"),
    "1.4.108":_meta_samjna("śeṣe prathamaḥ: default → prathama", "samjna:person"),
}


# ---------------------------------------------------------------------------
# Public API bound by sutra_impl_base.make_module_api
# ---------------------------------------------------------------------------

(
    IMPLEMENTED_IDS,
    has_real_implementation,
    handler_for,
    positive_features,
    negative_features,
) = make_module_api(FIXTURES, globals())
