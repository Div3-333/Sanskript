"""
Discrete Pāṇini-correct implementations for Adhyāya 2 sutra predicates.
Each function sutra_X_Y_Z(c) -> bool returns True iff sutra X.Y.Z fires
in the derivation context c (a plain dict).

Context keys used across Adhyāya 2:
  members         list[Analysis]   – padās being compounded
  first           str              – lemma of first member
  second          str              – lemma of second member
  first_case      Case | None      – case of first member
  second_case     Case | None      – case of second member
  compound_type   SamasaType|None  – type being tested
  sense           SamasaSense|None – semantic sense being tested
  scope           str              – domain tag ("samasa", "svara", …)
  is_amantrita    bool             – first member is vocative-address
  is_samjna       bool             – proper-name (saṃjñā) context
  is_kshepa       bool             – contempt / reproof context
  is_praising     bool             – praise context
  is_optional     bool             – vikalpa licensed
  is_chandas      bool             – Vedic register
  kt_suffix       str|None         – kṛt suffix involved ("kta","kṛtya",…)
  upasarga        str|None         – verbal prefix
  upapada         str|None         – upapada governing the kṛt
  is_samahara     bool             – samāhāra-dvandva context
  is_am           bool             – am-substitution context
  dhatu_lemma     str|None         – root (for Adhyāya 2.4 substitutions)
  lakara          Lakara|None      – for 2.4 dhātu-alternation rules
  pada            Pada|None        – parasmaipada / ātmanepada
  is_ardhadhatuka bool             – ārdhadhātuka context
  member_index    int              – 0 = first member, -1 = last
  role            Role|None        – kāraka role (for 2.3)
  case            Case|None        – case being tested (for 2.3)
  companion_lemma str|None         – upapada / companion word (2.3)
  semantic_context str|None        – fine-grained semantic tag (2.3)
  is_already_expressed bool        – kāraka already expressed by verb (2.3)
  verb_lemma      str|None         – dhātu governing the kāraka (2.3)
"""
from __future__ import annotations
from .grammar import Analysis, Case, Gender, GrammaticalNumber, Lakara, Pada, PartOfSpeech, Role
from .samasa import SamasaSense, SamasaType
from .sutra_impl_base import make_module_api

# ---------------------------------------------------------------------------
# Gaṇa sets used across Adhyāya 2
# ---------------------------------------------------------------------------

# 2.1.40: śauṇḍādi – words meaning "addicted to / expert in"
SHAUNDADI = frozenset({
    "śauṇḍa","āḍhya","mukhya","kusīda","vaśa","kāma","abhijña",
    "nipuṇa","kuśala","paṭu","pravīṇa","dhanin","sukhita","rakta",
    "āsakta","ānanda","priya","dhanya","kṛtajña","viśārada",
    "dhurya","samartha","śūra","vīra","dakṣa",
})

# 2.1.41: siddha/śuṣka/pakva/bandha class (also with locative)
SIDDHADI = frozenset({"siddha","śuṣka","pakva","bandha","prabaddha","vibandha"})

# 2.1.31: pūrva-sadṛśa-sama class for instrumental tatpuruṣa
PURVASADRSHADI = frozenset({
    "pūrva","sadṛśa","sama","onārtha","kalaha","nipuṇa","miśra","ślakṣṇa",
    "tulya","saha","sārdha","anurūpa","yogya",
})

# 2.1.49: pūrvakālaikasarvajarat class (karmadhāraya with samānādhikaraṇa)
PURVAKALAADI = frozenset({
    "pūrvakāla","eka","sarva","jarat","purāṇa","nava","kevala",
    "prathama","carama","jaghanya","uttara","adhara","anye",
})

# 2.1.58: ordinal/rank class
ORDINALADI = frozenset({
    "pūrva","apara","prathama","carama","jaghanya","samāna",
    "madhya","madhyama","vīra",
})

# 2.1.61: honorific adjectives
SANMAHATADI = frozenset({"sat","mahat","parama","uttama","utkṛṣṭa"})

# 2.1.62: honorific nouns (male elite)
VRNDADITADI = frozenset({"vṛndāraka","nāga","kuñjara"})

# 2.2.9: yājaka-class (agent nouns governing genitive)
YAJAKADI = frozenset({
    "yājaka","ādhyāpaka","upādhyāya","sevaka","kariṣyat",
    "kārayitṛ","praśāsitṛ","niyoktṛ",
})

# 2.2.32: ghi-class nouns (for dvandva ordering)
GHI_CLASS = frozenset({
    "agni","vāyu","marutā","aśvin","aśva","ahi","kapi","muni","rṣi",
    "pitṛ","bhrātṛ","svasṛ","jāmātṛ","kartṛ","hotṛ","potṛ",
})

# 2.3 upapada sets
SWAMI_ADI = frozenset({
    "svāmin","īśvara","adhipati","dāyāda","sākṣin","pratibhū","prasūta",
})

# 2.3.51: jña in instrument sense
JNA_VERBS = frozenset({"jñā"})

# 2.3.52: adhī/gam verbs taking genitive of object learned
ADHIADI_VERBS = frozenset({"adhi-i","adhī","gam","āp","ī","vraj","smṛ"})

# ---------------------------------------------------------------------------
# 2.1 – Samāsa adhikāra + avyayībhāva + karmadhāraya details
# ---------------------------------------------------------------------------

def sutra_2_1_2(c) -> bool:
    """subāmantrite parāṅgavat svare: vocative sup treated like final member
    for accent. Fires in svara-processing when first member is āmantrita."""
    return (c.get("is_amantrita", False)
            and c.get("scope") == "svara")

def sutra_2_1_3(c) -> bool:
    """prāk kaḍārāt samāsaḥ: adhikāra — samāsa rules apply from here through
    2.2.38. Fires whenever the derivation is in a samāsa formation context."""
    return c.get("scope") == "samasa" or c.get("is_samasa_context", False)

# ── tṛtīyā-tatpuruṣa extra conditions ──────────────────────────────────────

def sutra_2_1_25(c) -> bool:
    """svayaṃ ktena: 'self' + kta-participle forms tatpuruṣa.
    Fires when first member is 'svayam' and kt_suffix is 'kta'."""
    first = c.get("first", "")
    return first in {"svayam","svayaṃ"} and c.get("kt_suffix") == "kta"

def sutra_2_1_26(c) -> bool:
    """khaṭvā kṣepe: 'khaṭvā' (bad woman) in contempt context with
    karmadhāraya. Fires when first member is 'khaṭvā' and context is kṣepa."""
    return c.get("first") == "khaṭvā" and c.get("is_kshepa", False)

def sutra_2_1_27(c) -> bool:
    """sāmi: 'half' (sāmi) + noun forms tatpuruṣa (half a thing).
    Fires when first member is 'sāmi'."""
    return c.get("first") in {"sāmi","sārdha","ardha"}

def sutra_2_1_28(c) -> bool:
    """kālāḥ: time-words in accusative form tatpuruṣa (duration/extent).
    Fires when first_case is accusative and second denotes time."""
    members = list(c.get("members", ()))
    if len(members) < 2:
        return False
    time_words = frozenset({
        "kāla","māsa","saṃvatsara","varṣa","ahar","rātri","kṣaṇa",
        "muhūrta","pala","yāma","pakṣa","ṛtu","yuga","ayana",
    })
    return (members[0].case == Case.ACCUSATIVE
            and members[1].lemma in time_words)

def sutra_2_1_29(c) -> bool:
    """atyantasaṃyoge ca: accusative first member in sense of 'perpetual/
    extreme connection' also forms tatpuruṣa. Extends 2.1.28."""
    members = list(c.get("members", ()))
    if len(members) < 2:
        return False
    return (members[0].case == Case.ACCUSATIVE
            and c.get("sense") == SamasaSense.DVIT_TAT
            and c.get("is_atyanta", False))

def sutra_2_1_31(c) -> bool:
    """pūrvasadṛśasamonārthakalahanipuṇamiśraślakṣṇaiḥ: instrumental first
    member with pūrva/sadṛśa/sama/kalaha/nipuṇa/miśra/ślakṣṇa class words
    forms tatpuruṣa."""
    members = list(c.get("members", ()))
    second = c.get("second", "")
    if len(members) < 2:
        return False
    return (members[0].case == Case.INSTRUMENTAL
            and second in PURVASADRSHADI)

def sutra_2_1_32(c) -> bool:
    """kartṛkaraṇe kṛtā bahulam: agent or instrument [expressed by kṛt]
    with kṛt compound — optionally (bahulam) in various ways."""
    kt = c.get("kt_suffix", "")
    first_case = c.get("first_case") or (
        c.get("members", [None])[0].case if c.get("members") else None)
    return (bool(kt) and
            first_case in {Case.INSTRUMENTAL, Case.NOMINATIVE} and
            c.get("is_kartri_karana", False))

def sutra_2_1_33(c) -> bool:
    """kṛtyair adhikārthavacane: kṛtya-participle (tavya/anīya/ya) as second
    member in 'exceeding' sense. First member instrumental."""
    members = list(c.get("members", ()))
    if len(members) < 2:
        return False
    return (members[0].case == Case.INSTRUMENTAL
            and c.get("kt_suffix") in {"tavya","anīya","ya","kelima"}
            and c.get("is_adhikartha", False))

def sutra_2_1_34(c) -> bool:
    """annena vyañjanam: condiment (vyañjana) with food (anna) — instrumental
    tatpuruṣa 'seasoned with food'."""
    second = c.get("second","")
    members = list(c.get("members",[]))
    if len(members) < 2:
        return False
    return (members[0].case == Case.INSTRUMENTAL
            and second in {"vyañjana","sūpa","rasayana","āmla"})

def sutra_2_1_35(c) -> bool:
    """bhakṣyeṇa miśrīkaraṇam: mixing with an edible (bhakṣya) —
    instrumental tatpuruṣa in sense of 'mixed with'."""
    members = list(c.get("members",[]))
    if len(members) < 2:
        return False
    return (members[0].case == Case.INSTRUMENTAL
            and c.get("is_mishrana", False))

def sutra_2_1_37(c) -> bool:
    """pañcamī bhayena: ablative first member with 'bhaya' (fear/danger)
    forms tatpuruṣa — 'fear of X'."""
    members = list(c.get("members",[]))
    second = c.get("second","")
    if len(members) < 2:
        return False
    return (members[0].case == Case.ABLATIVE
            and second in {"bhaya","trāsa","bhīti","śaṅkā","śankā"})

def sutra_2_1_38(c) -> bool:
    """apetāpoḍhamuktapatitāpatrastair alpaśaḥ: ablative first member with
    'departed/freed/fallen/alarmed' type second — rarely (alpaśaḥ)."""
    members = list(c.get("members",[]))
    second = c.get("second","")
    if len(members) < 2:
        return False
    departed_class = frozenset({
        "apeta","apoḍha","mukta","patita","āpatrastta","āpattrasta",
        "vimuktā","tyakta","galita","cyuta","bhraṣṭa","vipanna",
    })
    return (members[0].case == Case.ABLATIVE
            and second in departed_class)

def sutra_2_1_39(c) -> bool:
    """stokāntikadūrārthakṛcchrāṇi ktena: 'little/near/far/difficult' with
    kta (past participle) — ablative tatpuruṣa."""
    members = list(c.get("members",[]))
    first = c.get("first","")
    if len(members) < 2:
        return False
    stokadi = frozenset({"stoka","antika","dūra","kṛcchra","asādhāraṇa"})
    return (members[0].case == Case.ABLATIVE
            and first in stokadi
            and c.get("kt_suffix") == "kta")

def sutra_2_1_40(c) -> bool:
    """saptamī śauṇḍaiḥ: locative first member with śauṇḍādi second member
    (words for 'addicted to / skilled in') forms tatpuruṣa."""
    members = list(c.get("members",[]))
    second = c.get("second","")
    if len(members) < 2:
        return False
    return (members[0].case == Case.LOCATIVE
            and second in SHAUNDADI)

def sutra_2_1_41(c) -> bool:
    """siddhaśuṣkapakvabandhaiś ca: also with siddha/śuṣka/pakva/bandha
    as second member (extends 2.1.40 for locative tatpuruṣa)."""
    members = list(c.get("members",[]))
    second = c.get("second","")
    if len(members) < 2:
        return False
    return (members[0].case == Case.LOCATIVE
            and second in SIDDHADI)

def sutra_2_1_42(c) -> bool:
    """dhvāṅkṣeṇa kṣepe: 'dhvāṅkṣa' (crow) as instrumental second in
    contempt/reproof context."""
    return (c.get("second") == "dhvāṅkṣa"
            and c.get("is_kshepa", False))

def sutra_2_1_43(c) -> bool:
    """kṛtyair ṛṇe: kṛtya-participle as second member in 'debt' sense
    — locative tatpuruṣa."""
    members = list(c.get("members",[]))
    if len(members) < 2:
        return False
    return (members[0].case == Case.LOCATIVE
            and c.get("kt_suffix") in {"tavya","anīya","ya"}
            and c.get("is_rna_context", False))

def sutra_2_1_44(c) -> bool:
    """saṃjñāyām: in proper-name (saṃjñā) context, locative tatpuruṣa
    applies more freely."""
    members = list(c.get("members",[]))
    if len(members) < 2:
        return False
    return (members[0].case == Case.LOCATIVE
            and c.get("is_samjna", False))

def sutra_2_1_45(c) -> bool:
    """ktena'horātrāvayavāḥ: divisions of day/night (ahorātra-avayava)
    with kta form a locative tatpuruṣa."""
    first = c.get("first","")
    day_night_parts = frozenset({
        "prabhāta","āhna","madhyāhna","aparāhna","sāyāhna","sāyam",
        "niśā","niśītha","ardharātra","prātar","aparahna","uṣas",
    })
    return (first in day_night_parts
            and c.get("kt_suffix") == "kta")

def sutra_2_1_46(c) -> bool:
    """tatra: the demonstrative 'tatra' (there/in that) forms a locative
    tatpuruṣa as first member."""
    return c.get("first") in {"tatra","atra","yatra","kutra","sarvatra"}

def sutra_2_1_47(c) -> bool:
    """kṣepe: in contempt/reproach sense, locative tatpuruṣa forms freely."""
    members = list(c.get("members",[]))
    if len(members) < 2:
        return False
    return (members[0].case == Case.LOCATIVE
            and c.get("is_kshepa", False))

def sutra_2_1_48(c) -> bool:
    """pātresamitādayaś ca: 'pātresamita' and listed compounds — lexical
    idiomatic locative tatpuruṣas."""
    first = c.get("first","")
    patre_samitadi = frozenset({
        "pātrasamita","kuṇḍapāyya","grāmeyaka","nagarīya","kuṭumba",
        "deśīya","pratyayika","prādeśika",
    })
    return first in patre_samitadi or c.get("is_patre_samitadi", False)

def sutra_2_1_49(c) -> bool:
    """pūrvakālaikasarvajarat... samānādhikaraṇena: pūrvakāla/eka/sarva/
    jarat/purāṇa/nava/kevala with same-referent word — karmadhāraya."""
    first = c.get("first","")
    return first in PURVAKALAADI

def sutra_2_1_50(c) -> bool:
    """diksaṃkhye saṃjñāyām: direction-word or numeral + noun in a proper
    name — karmadhāraya (or dvigu for numerals)."""
    first = c.get("first","")
    directions = frozenset({
        "pūrva","paścima","uttara","dakṣiṇa","madhya","anta","pārśva",
        "agra","ūrdhva","adhas","tira","paras",
    })
    is_direction = first in directions
    is_number = c.get("is_numeral_first", False)
    return (is_direction or is_number) and c.get("is_samjna", False)

def sutra_2_1_51(c) -> bool:
    """taddhitārtha-uttarapada-samāhāre ca: also in taddhita-sense, as a
    final member, or in aggregate meaning — dvigu or karmadhāraya."""
    return (c.get("is_taddhitartha", False)
            or c.get("is_uttarapada", False)
            or c.get("is_samahara", False))

def sutra_2_1_52(c) -> bool:
    """saṃkhyāpūrvo dvigu: a numeral as first member forms a dvigu compound.
    The compound is singular and neuter (per 2.4.1)."""
    members = list(c.get("members",[]))
    if len(members) < 2:
        return False
    return (members[0].pos == PartOfSpeech.NUMERAL
            or c.get("is_numeral_first", False))

def sutra_2_1_53(c) -> bool:
    """kutsitāni kutsanaiḥ: contemptible things with contemptuous second
    member — karmadhāraya. First member denotes something despised."""
    return (c.get("is_kutsita_first", False)
            and c.get("is_kutsana_second", False))

def sutra_2_1_54(c) -> bool:
    """pāpāṇake kutsitaiḥ: 'pāpa' and 'āṇaka' specifically with
    contemptible second members."""
    first = c.get("first","")
    return first in {"pāpa","āṇaka"} and c.get("is_kutsita", False)

def sutra_2_1_55(c) -> bool:
    """upamānāni sāmānyavacanaiḥ: simile-standard (upamāna) with a word
    expressing the common property — karmadhāraya/upamāna compound."""
    return (c.get("is_upamana_first", False)
            and c.get("is_samanya_second", False))

def sutra_2_1_56(c) -> bool:
    """upamitaṃ vyāghrādibhiḥ sāmānyāprayoge: compared to tiger etc. when
    the common property is NOT expressed — upamāna karmadhāraya."""
    second = c.get("second","")
    vyaghraadi = frozenset({
        "vyāghra","siṃha","ṛkṣa","vṛka","śārdūla","gaura",
        "mahiṣa","varāha","hastī","haya",
    })
    return (second in vyaghraadi
            and not c.get("is_samanya_expressed", False))

def sutra_2_1_58(c) -> bool:
    """pūrvāparaprathama... vīrāś ca: rank/ordinal/directional adjectives
    (pūrva/apara/prathama/carama/jaghanya/samāna/madhya/madhyama/vīra)
    as second member in karmadhāraya."""
    second = c.get("second","")
    return second in ORDINALADI

def sutra_2_1_59(c) -> bool:
    """śreṇyādayaḥ kṛtādibhiḥ: śreṇī and similar collective nouns with
    kṛta-class as second member — karmadhāraya."""
    first = c.get("first","")
    shrenyadi = frozenset({
        "śreṇi","śreṇī","gaṇa","varga","samuha","samūha","jāti",
    })
    krtadi = frozenset({
        "kṛta","ākṛta","sañcita","pūrita","āpūrita","racita",
    })
    return first in shrenyadi and c.get("second","") in krtadi

def sutra_2_1_60(c) -> bool:
    """ktena nañviśiṣṭenānañ: with kta that is qualified by nañ (na-),
    when the compound itself is not nañ — anañ-kta karmadhāraya."""
    return (c.get("kt_suffix") == "kta"
            and c.get("is_nañ_qualified", False)
            and not c.get("is_nañ_compound", False))

def sutra_2_1_61(c) -> bool:
    """san-mahat-parama-uttama-utkṛṣṭāḥ pūjyamānaiḥ: honorific adjectives
    (sat/mahat/parama/uttama/utkṛṣṭa) with praised persons/things."""
    first = c.get("first","")
    return first in SANMAHATADI and c.get("is_praising", False)

def sutra_2_1_62(c) -> bool:
    """vṛndārakanāgakuñjaraiḥ pūjyamānam: vṛndāraka/nāga/kuñjara (noble
    animal terms used honorifically) with a praised second member."""
    second = c.get("second","")
    return second in VRNDADITADI and c.get("is_praising", False)

def sutra_2_1_63(c) -> bool:
    """katara-katamau jātiparipraśne: 'katara'/'katama' in class-questioning
    context — karmadhāraya."""
    first = c.get("first","")
    return (first in {"katara","katama"}
            and c.get("is_jati_pariprashn", False))

def sutra_2_1_64(c) -> bool:
    """kiṃ kṣepe: 'kim' (what) as first member in contempt context
    — karmadhāraya (e.g. kim-brāhmaṇa 'so-called brahmin')."""
    return (c.get("first") == "kim"
            and c.get("is_kshepa", False))

def sutra_2_1_65(c) -> bool:
    """poṭā-yuvati-stoka... class: specific listed words form karmadhāraya
    with their respective second members."""
    # These are lexically listed compound types
    special_pairs = frozenset({
        "poṭā","yuvati","stoka","katipaya","gṛṣṭi","dhenu",
        "vaśā","vehat","baṣkayanī","pravaktṛ","śrotrin",
    })
    first = c.get("first","")
    return first in special_pairs

def sutra_2_1_66(c) -> bool:
    """praśaṃsāvacanaiś ca: also with words expressing praise as second
    member — karmadhāraya extension."""
    return c.get("is_prashansa_second", False)

def sutra_2_1_67(c) -> bool:
    """yuvā khalatipalitavalinajarat ībhiḥ: 'young' (yuvā) with bald/
    gray/wrinkled/aged words — karmadhāraya."""
    first = c.get("first","")
    second = c.get("second","")
    ageing = frozenset({"khalati","palita","valina","jaratī","jarā","vṛddha"})
    return first == "yuvā" and second in ageing

def sutra_2_1_68(c) -> bool:
    """kṛtyatulya-ākhyā ajātyā: a name equating subject to kṛtya/equal-class
    when not a genus (ajāti) — karmadhāraya."""
    return (c.get("is_kritya_tulya", False)
            and not c.get("is_jati", False))

def sutra_2_1_69(c) -> bool:
    """varṇo varṇena: color word with color word forms karmadhāraya
    (e.g., 'dark blue' = nīla + śyāma)."""
    color_words = frozenset({
        "nīla","śyāma","kṛṣṇa","śveta","rakta","pīta","harita",
        "śabala","citrā","babhru","kapila","aruna","lohita",
    })
    first = c.get("first","")
    second = c.get("second","")
    return first in color_words and second in color_words

def sutra_2_1_70(c) -> bool:
    """kumāraḥ śramaṇādibhiḥ: 'kumāra' (youth) with śramaṇa-class forms
    karmadhāraya (terms of address or honorary compounds)."""
    first = c.get("first","")
    shramana_class = frozenset({
        "śramaṇa","tapasvin","vātarasana","muni","ṛṣi","yati",
        "sannyāsin","bhikṣu","parivrājaka",
    })
    return (first == "kumāra"
            and c.get("second","") in shramana_class)

def sutra_2_1_71(c) -> bool:
    """catuṣpādo garbhiṇyā: four-footed animal (catuṣpāda) with pregnant-
    female word — karmadhāraya."""
    four_footed = frozenset({
        "go","aśva","gavaya","mahiṣa","aja","avi","uṣṭra","gardabha","khara",
    })
    preg_words = frozenset({"garbhiṇī","satvā","āsanna-prasavā"})
    return (c.get("first","") in four_footed
            and c.get("second","") in preg_words)

def sutra_2_1_72(c) -> bool:
    """mayūravyaṃsakādayaś ca: 'mayūravyaṃsaka' and other listed idiomatic
    karmadhāraya compounds (lexically fixed)."""
    mayuradi = frozenset({
        "mayūravyaṃsaka","kākapeyā","andhamūṣika","mūṣikāhvaya",
    })
    first = c.get("first","")
    compound = f"{first}+{c.get('second','')}"
    return (first in mayuradi
            or compound in mayuradi
            or c.get("is_mayuradi", False))


# ---------------------------------------------------------------------------
# 2.2 – Bahuvrīhi, Dvandva, Compound member ordering
# ---------------------------------------------------------------------------

def sutra_2_2_1(c) -> bool:
    """pūrvāparadharo-uttaramekadeshinaikādhikaraṇe: 'front/back/lower/upper'
    with a part-denoting word, same referent — tatpuruṣa."""
    part_words = frozenset({
        "pūrva","apara","adhara","uttara",
    })
    return (c.get("first","") in part_words
            and c.get("is_ekadeshin", False)
            and c.get("is_ekadhikarana", False))

def sutra_2_2_2(c) -> bool:
    """ardhaṃ napuṃsakam: 'ardha' (half) is neuter in compounds.
    Fires when first member is 'ardha' and gender check is needed."""
    return c.get("first") == "ardha"

def sutra_2_2_3(c) -> bool:
    """dvitīyatṛtīyacaturtha-turyāṇy anyatarasyām: second/third/fourth/
    'quarter' in ordinal sense — optionally tatpuruṣa."""
    ordinals = frozenset({"dvitīya","tṛtīya","caturtha","turya","turīya"})
    return c.get("first","") in ordinals or c.get("second","") in ordinals

def sutra_2_2_4(c) -> bool:
    """prāptāpanne ca dvitīyayā: 'obtained/reached' (prāpta/āpanna) with
    accusative — tatpuruṣa."""
    second = c.get("second","")
    members = list(c.get("members",[]))
    if len(members) < 2:
        return False
    return (second in {"prāpta","āpanna","labdha","prāpnuvat"}
            and members[0].case == Case.ACCUSATIVE)

def sutra_2_2_5(c) -> bool:
    """kālāḥ parimāṇinā: time-words with measure/quantity word — tatpuruṣa
    (instrumental of measure)."""
    time_w = frozenset({
        "kāla","māsa","varṣa","saṃvatsara","rātri","ahar","pakṣa",
    })
    members = list(c.get("members",[]))
    if len(members) < 2:
        return False
    return (members[0].lemma in time_w
            and members[1].case == Case.INSTRUMENTAL)

def sutra_2_2_6(c) -> bool:
    """nañ: negative prefix 'na' (nañ) forms tatpuruṣa (nañ-tatpuruṣa)
    or bahuvrīhi with any second member."""
    first = c.get("first","")
    return first in {"na","nañ","a","an","nis","nir","dus","duh"}

def sutra_2_2_7(c) -> bool:
    """īṣadakṛtā: 'slightly' (īṣat) with a past participle (akṛta sense) —
    nañ-type compound with mild negation."""
    return (c.get("first") in {"īṣat","alaṃ","kiñcit"}
            and c.get("kt_suffix") == "kta")

def sutra_2_2_8(c) -> bool:
    """ṣaṣṭhī: genitive first member with genitive governs tatpuruṣa.
    The basic ṣaṣṭhī-tatpuruṣa rule."""
    members = list(c.get("members",[]))
    if len(members) < 2:
        return False
    return members[0].case == Case.GENITIVE

def sutra_2_2_9(c) -> bool:
    """yājakādibhiś ca: with yājaka-class (those who perform for others) as
    second member — genitive tatpuruṣa extends."""
    return c.get("second","") in YAJAKADI

def sutra_2_2_10(c) -> bool:
    """na nirdhāraṇe: NOT in partitive/nidhāraṇa context (exception to 2.2.8
    — genitive tatpuruṣa does not apply when genitive expresses a selection
    from a group)."""
    return not c.get("is_nirdhana", False)

def sutra_2_2_11(c) -> bool:
    """pūraṇaguṇasuhitārtha... samānādhikaraṇena: ordinal/quality/sated/
    sense words with same-referent — karmadhāraya."""
    second = c.get("second","")
    puranaadi = frozenset({
        "pūraṇa","guṇa","suhita","avyaya","tavya","samāna",
    })
    return second in puranaadi

def sutra_2_2_12(c) -> bool:
    """ktena ca pūjāyām: with past participle (kta) in praise sense —
    genitive tatpuruṣa (e.g., 'best of kings')."""
    return (c.get("kt_suffix") == "kta"
            and c.get("is_puja", False))

def sutra_2_2_13(c) -> bool:
    """adhikaraṇavācinā ca: with a word denoting the location/substratum
    (adhikaraṇa) — genitive tatpuruṣa extends."""
    return c.get("is_adhikarana_second", False)

def sutra_2_2_14(c) -> bool:
    """karmaṇi ca: in the karman (object) relation — genitive tatpuruṣa."""
    return (c.get("role") == Role.KARMAN
            or c.get("is_karma_relation", False))

def sutra_2_2_15(c) -> bool:
    """tṛjakābhyāṃ kartari: with tṛc (agent-noun suffix -tṛ) and ka-suffix,
    in agent (kartṛ) relation — genitive tatpuruṣa."""
    return (c.get("kt_suffix") in {"tṛc","ka","tṛ"}
            and (c.get("role") == Role.KARTR
                 or c.get("is_kartri_relation", False)))

def sutra_2_2_16(c) -> bool:
    """kartari ca: in the kartṛ (agent) relation [genitive tatpuruṣa] —
    extends 2.2.15 to other agent contexts."""
    return c.get("role") == Role.KARTR or c.get("is_kartri_relation", False)

def sutra_2_2_17(c) -> bool:
    """nityaṃ krīḍājīvikayoḥ: always compounded in 'play' or 'livelihood'
    sense — tatpuruṣa is obligatory (nitya) here."""
    return c.get("is_krida", False) or c.get("is_jivika", False)

def sutra_2_2_18(c) -> bool:
    """kugati-prādayaḥ: ku/gati (motion-prefixes)/prā and other upasarga-type
    words always compound — adhikāra for prefixed compounds."""
    prefix_class = frozenset({
        "ku","su","dur","us","vi","sam","anu","ava","nis","nir",
        "pra","parā","pari","adhi","api","ati","ni","ut","upa",
        "ā","abhi","prāti","gati",
    })
    first = c.get("first","")
    return first in prefix_class or c.get("is_upasarga_first", False)

def sutra_2_2_19(c) -> bool:
    """upapadadam atiṅ: upapada + kṛt (not tiṅ) forms tatpuruṣa —
    upapada kṛt compounds."""
    return (c.get("upapada") is not None
            and c.get("kt_suffix") is not None
            and not c.get("is_ting", False))

def sutra_2_2_20(c) -> bool:
    """amai-v-āvyayena: 'am' (accusative singular) plus an indeclinable
    (avyaya) — compounds with am-form."""
    return (c.get("is_am", False)
            and c.get("is_avyaya_second", False))

def sutra_2_2_21(c) -> bool:
    """tṛtīyāprabhṛtīny anyatarasyām: third-case (instrumental) and
    following [in ordering] — optionally in compound ordering."""
    members = list(c.get("members",[]))
    if len(members) < 2:
        return False
    return (members[0].case in {Case.INSTRUMENTAL, Case.DATIVE,
                                 Case.ABLATIVE, Case.GENITIVE, Case.LOCATIVE}
            and c.get("is_optional", False))

def sutra_2_2_22(c) -> bool:
    """ktvā ca: ktvā-gerund (absolutive) also [compounds optionally]."""
    return c.get("kt_suffix") == "ktvā"

def sutra_2_2_23(c) -> bool:
    """śeṣo bahuvrīhiḥ: everything remaining [not covered by tatpuruṣa,
    dvandva, etc.] is a bahuvrīhi — the residual compound type."""
    ct = c.get("compound_type")
    # Fires when no other samāsa type is licensed
    return ct == SamasaType.BAHUVRIHI or c.get("is_bahuvrihi_context", False)

def sutra_2_2_24(c) -> bool:
    """anekam anyapadārthe: multiple [members referring to] another thing
    (not either member) — bahuvrīhi compound."""
    members = list(c.get("members",[]))
    return (len(members) >= 2
            and c.get("is_anyapadartha", False))

def sutra_2_2_25(c) -> bool:
    """saṃkhyayā'vyayāsannādūrādhikasaṃkhyāḥ saṃkhyeye: numeral with
    avyaya/near/far/excess-numeral in a numeral-denotation context."""
    return (c.get("is_numeral_second", False)
            or c.get("is_samkhyeya", False))

def sutra_2_2_26(c) -> bool:
    """dinnāmāny antarāle: directional names in 'between' (antarāla) sense
    — dvandva."""
    direction_names = frozenset({
        "pūrva","paścima","uttara","dakṣiṇa","agni","vāyu","īśāna","nairṛti",
    })
    members = list(c.get("members",[]))
    return (all(m.lemma in direction_names for m in members)
            and c.get("is_antarala", False))

def sutra_2_2_27(c) -> bool:
    """tatra tenedamiti sarūpe: when second member is of the same form
    (sarūpa) as first — bahuvrīhi is licenced."""
    return c.get("is_sarupa", False)

def sutra_2_2_28(c) -> bool:
    """tena saheti tulyayoge: 'together with' (saha) in equal-relation
    (tulyayoga) — bahuvrīhi (saha-bahuvrīhi)."""
    return (c.get("first") in {"saha","sa"}
            and c.get("is_tulya_yoga", False))

def sutra_2_2_31(c) -> bool:
    """rājadantādiṣu param: in rājadanta and similar [compounds], the
    latter [member comes] first (inverted ordering)."""
    raja_dantadi = frozenset({
        "rājadanta","grāmakauṭa","sarpaviṣa","ahibhī","yavāgū",
    })
    compound = f"{c.get('first','')}{c.get('second','')}"
    return (compound in raja_dantadi
            or c.get("is_raja_dantadi", False))

def sutra_2_2_32(c) -> bool:
    """dvandve ghi: in dvandva, the ghi-class word [comes first / appears
    in its stem form]. Ordering rule."""
    members = list(c.get("members",[]))
    if len(members) < 2:
        return False
    ct = c.get("compound_type")
    return (ct == SamasaType.DVANDVA
            and any(m.lemma in GHI_CLASS for m in members))

def sutra_2_2_33(c) -> bool:
    """ajādyad-antam: [in dvandva, of two], the one beginning with a vowel
    (or ending in 'a') comes last."""
    members = list(c.get("members",[]))
    ct = c.get("compound_type")
    if len(members) < 2 or ct != SamasaType.DVANDVA:
        return False
    second = members[1].lemma
    return second and second[0] in "aāiīuūeēoō"

def sutra_2_2_34(c) -> bool:
    """alpāc-taram: [in dvandva,] the one with fewer vowels comes first
    (brevity ordering rule)."""
    members = list(c.get("members",[]))
    ct = c.get("compound_type")
    if len(members) < 2 or ct != SamasaType.DVANDVA:
        return False
    def vowel_count(s):
        return sum(1 for ch in s if ch in "aāiīuūeēoō")
    return vowel_count(members[0].lemma) <= vowel_count(members[1].lemma)

def sutra_2_2_35(c) -> bool:
    """saptamīviśeṣaṇe bahuvrīhau: a locative [first member] qualifying
    [second member] — bahuvrīhi."""
    members = list(c.get("members",[]))
    if len(members) < 2:
        return False
    ct = c.get("compound_type")
    return (ct == SamasaType.BAHUVRIHI
            and members[0].case == Case.LOCATIVE)

def sutra_2_2_36(c) -> bool:
    """niṣṭhā: a niṣṭhā (kta/ktavat) form [as second member in bahuvrīhi]
    — the niṣṭhā form retains its properties."""
    return (c.get("kt_suffix") in {"kta","ktavat"}
            and c.get("compound_type") == SamasaType.BAHUVRIHI)

def sutra_2_2_37(c) -> bool:
    """vā'hitāgnyādiṣu: optionally in āhitāgni and similar [lexical
    bahuvrīhi] compounds."""
    ahitagni_etc = frozenset({
        "āhitāgni","adhīta","upahūta","dīkṣita","vṛṣala",
    })
    compound = c.get("compound_id","")
    return (compound in ahitagni_etc
            or c.get("is_ahitagnyadi", False))

def sutra_2_2_38(c) -> bool:
    """kaḍārāḥ karmadhāraye: 'kaḍāra' [and similar words] in karmadhāraya —
    the final rule of the samāsa adhikāra section (2.1.3-2.2.38)."""
    kadaradi = frozenset({
        "kaḍāra","paṭu","nipuṇa","cheka","prāgalbha",
    })
    return c.get("second","") in kadaradi


# ---------------------------------------------------------------------------
# 2.3 – Vibhakti (case assignment for kārakas and special relations)
# ---------------------------------------------------------------------------

def sutra_2_3_37(c) -> bool:
    """yasya ca bhāvena bhāvalakṣaṇam: genitive when the presence/state
    of X is the mark/criterion for something — genitive of characteristic."""
    return c.get("is_bhava_lakshana", False)

def sutra_2_3_38(c) -> bool:
    """ṣaṣṭhī cānādare: genitive also in disrespect/contempt context."""
    return c.get("is_anadara", False)

def sutra_2_3_39(c) -> bool:
    """svāmīśvarādhipatidāyādasākṣipratibhūprasūtaiś ca: genitive with
    svāmin/īśvara/adhipati/dāyāda/sākṣin/pratibhū/prasūta."""
    companion = c.get("companion_lemma","")
    return companion in SWAMI_ADI

def sutra_2_3_40(c) -> bool:
    """āyuktakuśalābhyāṃ cāsevāyām: genitive with 'āyukta'/'kuśala' in
    non-employment (asevā) context."""
    companion = c.get("companion_lemma","")
    return (companion in {"āyukta","kuśala"}
            and c.get("semantic_context") == "aseva")

def sutra_2_3_41(c) -> bool:
    """yataś ca nirdhāraṇam: genitive (or locative) for the set from which
    selection (nirdhāraṇa) is made."""
    return c.get("semantic_context") == "nirdhana"

def sutra_2_3_42(c) -> bool:
    """pañcamī vibhakte: ablative for a separated/divided entity
    (vibhakta = separated)."""
    return (c.get("case") == Case.ABLATIVE
            and c.get("semantic_context") == "vibhakta")

def sutra_2_3_43(c) -> bool:
    """sādhunipuṇābhyām arcāyāṃ saptamyaprateh: 'sādhu'/'nipuṇa' govern
    locative in praise context, not dative."""
    companion = c.get("companion_lemma","")
    return (companion in {"sādhu","nipuṇa"}
            and c.get("semantic_context") == "arca"
            and c.get("case") == Case.LOCATIVE)

def sutra_2_3_44(c) -> bool:
    """prasitotsukaābhyāṃ tṛtīyā ca: 'prasita'/'utsuka' govern instrumental
    (tṛtīyā) as well."""
    companion = c.get("companion_lemma","")
    return (companion in {"prasita","utsuka"}
            and c.get("case") == Case.INSTRUMENTAL)

def sutra_2_3_45(c) -> bool:
    """nakṣatre ca lupi: genitive with asterism (nakṣatra) when sup is
    elided (lupi)."""
    return (c.get("is_nakshatra", False)
            and c.get("is_luk", False))

def sutra_2_3_46(c) -> bool:
    """prātipadikārtha-liṅga-parimāṇa-vacana-mātre prathamā: nominative
    (prathama) for prātipadika-only meaning, gender, measure, number
    without a kāraka relation."""
    return (c.get("case") == Case.NOMINATIVE
            and c.get("semantic_context") in {
                "pratipadika_only","linga_matra","parimana","vacana_matra",
                None,
            })

def sutra_2_3_47(c) -> bool:
    """sambodhane ca: nominative also in address (sambodhana/vocative)."""
    return c.get("case") == Case.VOCATIVE

def sutra_2_3_48(c) -> bool:
    """sā'mantritam: [that vocative case-form] is called āmantrita (address).
    Saṃjñā-sūtra — fires when case is vocative and samjña is assigned."""
    return (c.get("case") == Case.VOCATIVE
            and c.get("scope") == "samjna")

def sutra_2_3_49(c) -> bool:
    """ekavacanaṃ saṃbuddhiḥ: singular vocative is called saṃbuddhi.
    Saṃjñā-sūtra."""
    return (c.get("case") == Case.VOCATIVE
            and c.get("number") == GrammaticalNumber.SINGULAR
            and c.get("scope") == "samjna")

def sutra_2_3_51(c) -> bool:
    """jño'vidarthasyay karaṇe: 'jñā' (know) in not-knowing sense takes
    instrumental for the instrument of knowledge."""
    verb = c.get("verb_lemma","")
    return (verb in JNA_VERBS
            and c.get("semantic_context") == "avid"
            and c.get("case") == Case.INSTRUMENTAL)

def sutra_2_3_52(c) -> bool:
    """adhīgarthādayeśāṃ karmaṇi: verbs of learning/remembering
    (adhi-i, gam, etc.) take genitive for the object learned."""
    verb = c.get("verb_lemma","")
    return (verb in ADHIADI_VERBS
            and c.get("case") == Case.GENITIVE
            and c.get("semantic_context") == "adhigama")

def sutra_2_3_53(c) -> bool:
    """kṛñaḥ pratiyatne: 'kṛ' (do) in 'counter-effort' (pratiyatna) context
    — takes ablative."""
    return (c.get("verb_lemma","") in {"kṛ","kar"}
            and c.get("semantic_context") == "pratiyatna"
            and c.get("case") == Case.ABLATIVE)

def sutra_2_3_54(c) -> bool:
    """rujārthānāṃ bhāvavacanānām ajvareḥ: verbs meaning 'to pain/hurt'
    denoting a state take genitive, except jvara (fever)."""
    ruj_verbs = frozenset({"ruj","pid","bādh","śuc","tap","dah"})
    verb = c.get("verb_lemma","")
    return (verb in ruj_verbs
            and c.get("is_bhava_vacana", False)
            and verb != "jvara"
            and c.get("case") == Case.GENITIVE)

def sutra_2_3_55(c) -> bool:
    """āśiṣi nāthaḥ: 'nātha' (lord) in a blessing (āśiṣ) context —
    takes genitive."""
    return (c.get("companion_lemma") == "nātha"
            and c.get("semantic_context") == "ashish")

def sutra_2_3_56(c) -> bool:
    """jāsinikrahaṇanāṭakrāthapiṣāṃ hiṃsāyām: verbs jāsi/ni/prahaṇa/nāṭa/
    krātha/piṣa in violence (hiṃsā) sense take genitive."""
    himsa_verbs = frozenset({
        "jāsi","ni","prahaṇa","nāṭa","krātha","piṣa",
        "han","vadh","ghāt","hiṃs",
    })
    return (c.get("verb_lemma","") in himsa_verbs
            and c.get("semantic_context") == "himsa"
            and c.get("case") == Case.GENITIVE)

def sutra_2_3_57(c) -> bool:
    """vyavahṛpaṇoḥ samarthayoḥ: 'vyavahṛ' and 'paṇ' (transact/wager)
    when equally capable — take genitive."""
    return (c.get("verb_lemma","") in {"vyavahṛ","paṇ"}
            and c.get("is_samartha", False)
            and c.get("case") == Case.GENITIVE)

def sutra_2_3_58(c) -> bool:
    """divastas-tadarthasya: genitive of a day-word when it denotes
    a specific purpose (tadārtha)."""
    return (c.get("is_divasa", False)
            and c.get("semantic_context") == "tadartha"
            and c.get("case") == Case.GENITIVE)

def sutra_2_3_59(c) -> bool:
    """vibhāṣopasarge: optionally when an upasarga (prefix) is present."""
    return (c.get("upasarga") is not None
            and c.get("is_optional", False))

def sutra_2_3_60(c) -> bool:
    """dvitīyā brāhmaṇe: accusative with 'brāhmaṇa' in Vedic register
    (brāhmaṇa texts)."""
    return (c.get("is_chandas", False)
            and c.get("case") == Case.ACCUSATIVE)

def sutra_2_3_61(c) -> bool:
    """preṣyabravao haviṣo devatāsampradāne: 'send'/'say' verbs in context
    of offering havis to a deity — dative for the deity."""
    preshy_verbs = frozenset({"preṣ","pra-iṣ","brū","vac","ah"})
    return (c.get("verb_lemma","") in preshy_verbs
            and c.get("semantic_context") == "devatā_sampradāna"
            and c.get("case") == Case.DATIVE)

def sutra_2_3_62(c) -> bool:
    """caturthyarthe bahulaṃ chandasi: optionally (bahulam) dative in
    Vedic (chandas) contexts."""
    return (c.get("is_chandas", False)
            and c.get("case") == Case.DATIVE)

def sutra_2_3_63(c) -> bool:
    """yājeś ca karaṇe: 'yaj' (sacrifice) takes instrumental for the
    instrument of sacrifice."""
    return (c.get("verb_lemma") in {"yaj","ijy"}
            and c.get("case") == Case.INSTRUMENTAL)

def sutra_2_3_64(c) -> bool:
    """kṛtvo'rthaprayoge kāle'dhikaraṇe: for time-expressions in the
    'how many times' sense, locative is used."""
    return (c.get("semantic_context") == "krtvo_artha"
            and c.get("case") == Case.LOCATIVE)

def sutra_2_3_65(c) -> bool:
    """kartṛkarmaṇoḥ kṛti: genitive for agent and object with kṛt-derived
    nouns (agent nouns, action nouns)."""
    return (c.get("is_krit_noun", False)
            and c.get("case") == Case.GENITIVE
            and c.get("role") in {Role.KARTR, Role.KARMAN})

def sutra_2_3_66(c) -> bool:
    """ubhayaprāptau karmaṇi: when both [agent and instrument] are licensed,
    accusative goes with the object (karman)."""
    return (c.get("is_ubhaya_prapta", False)
            and c.get("case") == Case.ACCUSATIVE)

def sutra_2_3_67(c) -> bool:
    """ktasya ca vartamāne: genitive with kta (past participle) in a present-
    time sense."""
    return (c.get("kt_suffix") == "kta"
            and c.get("is_vartamana", False)
            and c.get("case") == Case.GENITIVE)

def sutra_2_3_68(c) -> bool:
    """adhikaraṇavācinaś ca: genitive also with an adhikaraṇa-denoting
    (location/substratum) kṛt noun."""
    return (c.get("is_adhikarana_krit", False)
            and c.get("case") == Case.GENITIVE)

def sutra_2_3_69(c) -> bool:
    """na lokāvyayanniṣṭhākhalarthatṛnām: NOT genitive (exception) for
    loka/avyaya/niṣṭhā/khal/arthatṛn — these take instrumental or other."""
    excepted_kt = frozenset({"niṣṭhā","khal","arthatṛn","kvip"})
    excepted_words = frozenset({"loka","avyaya"})
    return not (c.get("kt_suffix","") in excepted_kt
                or c.get("second","") in excepted_words)

def sutra_2_3_70(c) -> bool:
    """akenoḥ bhaviṣyadādhamaryaṇyayoḥ: accusative/genitive with 'eka'/'anu'
    in future/debtor sense."""
    companion = c.get("companion_lemma","")
    return (companion in {"eka","anu"}
            and c.get("semantic_context") in {"bhavishyat","adhamarna"})

def sutra_2_3_71(c) -> bool:
    """kṛtyānāṃ kartari vā: optionally genitive for the agent (kartṛ) with
    kṛtya (gerundive) suffixes."""
    return (c.get("kt_suffix") in {"tavya","anīya","ya","ṇyat","kyap"}
            and c.get("role") == Role.KARTR
            and c.get("case") == Case.GENITIVE)

def sutra_2_3_72(c) -> bool:
    """tulyārthair atulopamābhyāṃ tṛtīyā'nyatarasyām: instrumental
    optionally with 'equal-sense' words and with atula/upamā."""
    companion = c.get("companion_lemma","")
    return (companion in {"atula","upamā","tulya","sama","sadṛśa"}
            and c.get("case") == Case.INSTRUMENTAL)

def sutra_2_3_73(c) -> bool:
    """caturthī cāśiṣy āyuṣyamadrabhadrakuśalasukhārthahitaiḥ: dative
    also in blessing/prosperity wishes with āyuṣya/bhadra/kuśala/sukha/
    hita words."""
    blessing_words = frozenset({
        "āyuṣya","mandra","bhadra","kuśala","sukha","hita","maṅgala",
        "śubha","śreyas","kṣema","svāsthya",
    })
    return (c.get("companion_lemma","") in blessing_words
            and c.get("semantic_context") == "ashish"
            and c.get("case") == Case.DATIVE)


# ---------------------------------------------------------------------------
# 2.4 – Sup-luk (case-ending deletion in compounds), gender of compounds,
#        and dhātu alternations for ārdhadhātuka
# ---------------------------------------------------------------------------

def sutra_2_4_2(c) -> bool:
    """dvandvaś ca prāṇitūryasaināṅgānām: dvandva of living beings/musical
    instruments/army divisions — singular neuter (samāhāra)."""
    if c.get("compound_type") != SamasaType.DVANDVA:
        return False
    samahara_cats = frozenset({"praṇi","turya","sena_anga"})
    return (c.get("semantic_category","") in samahara_cats
            or c.get("is_samahara", False))

def sutra_2_4_3(c) -> bool:
    """anuvāde caraṇānām: dvandva of a school (caraṇa) in citation context
    — samāhāra singular neuter."""
    return (c.get("compound_type") == SamasaType.DVANDVA
            and c.get("semantic_category") == "carana"
            and c.get("is_anuvada", False))

def sutra_2_4_4(c) -> bool:
    """adhvaryukratur anapuṃsakam: in compound of adhvaryu + kratu, not
    neuter (retains masculine gender)."""
    members = list(c.get("members",[]))
    lemmas = {m.lemma for m in members}
    return {"adhvaryu","kratu"} <= lemmas

def sutra_2_4_5(c) -> bool:
    """adhyayanato'viprakṛṣṭākhyānām: dvandva of study-schools whose names
    are not far apart — samāhāra."""
    return (c.get("compound_type") == SamasaType.DVANDVA
            and c.get("is_adhyayana_carana", False)
            and not c.get("is_viprakrishta", False))

def sutra_2_4_6(c) -> bool:
    """jātir aprāṇinām: class-noun (jāti) of non-living things — samāhāra
    dvandva is neuter singular."""
    return (c.get("compound_type") == SamasaType.DVANDVA
            and c.get("is_jati", False)
            and not c.get("is_praṇi", False))

def sutra_2_4_7(c) -> bool:
    """viśiṣṭaliṅgo nadī deśo'grāmāḥ: a river or region with a
    distinctive gender (viśiṣṭaliṅga) and not a village — gender
    of last member prevails in dvandva."""
    return (c.get("is_nadi_or_desha", False)
            and not c.get("is_grama", False))

def sutra_2_4_8(c) -> bool:
    """kṣudrajanttavaḥ: small creatures (kṣudrajantus) — samāhāra dvandva
    is neuter singular."""
    return c.get("is_kshudra_jantava", False)

def sutra_2_4_9(c) -> bool:
    """yeṣāṃ ca virodhāḥ śāśvatikaḥ: when there is perpetual opposition
    (śāśvata-virodhā) between the members — dvandva retains plural."""
    return c.get("is_shasvata_virodha", False)

def sutra_2_4_10(c) -> bool:
    """śūdrāṇām anirvasitānām: for unresettled śūdras [dvandva ordering
    rule — they come first]."""
    return c.get("is_shudra_anirvasita", False)

def sutra_2_4_11(c) -> bool:
    """gavāśvaprabhṛtīni ca: also cow/horse and similar [domestic animals
    — samāhāra neuter dvandva]."""
    cattle_class = frozenset({"go","aśva","khara","gardabha","uṣṭra"})
    members = list(c.get("members",[]))
    return (c.get("compound_type") == SamasaType.DVANDVA
            and any(m.lemma in cattle_class for m in members))

def sutra_2_4_12(c) -> bool:
    """vibhāṣā vṛkṣamṛga... pūrvāparādharānārāṃ: optionally samāhāra for
    tree/animal/grain/spice/cattle/bird/horse-mare/direction groups."""
    opt_cats = frozenset({
        "vriksha","mrga","trna","dhanya","vyanjana","pashu",
        "shakuni","ashva_vadava","purvaapara",
    })
    return (c.get("compound_type") == SamasaType.DVANDVA
            and c.get("semantic_category","") in opt_cats)

def sutra_2_4_13(c) -> bool:
    """vipratisidhdhāṃ cānadhikaraṇavāci: when there is conflict and the
    compound does NOT denote a location — samāhāra neuter."""
    return (c.get("is_vipratishiddha", False)
            and not c.get("is_adhikarana_vachana", False))

def sutra_2_4_14(c) -> bool:
    """na dadhipayāādīni: NOT samāhāra for dadhi/payas and similar
    (exception — these remain individual)."""
    no_samahara = frozenset({"dadhi","payas","ghṛta","madhu","taila"})
    members = list(c.get("members",[]))
    return not any(m.lemma in no_samahara for m in members)

def sutra_2_4_15(c) -> bool:
    """adhikaraṇaitāvatve ca: also when there is a locative-extent
    (adhikaraṇa-etāvattva) relationship — samāhāra."""
    return c.get("is_adhikarana_etavatva", False)

def sutra_2_4_16(c) -> bool:
    """vibhāṣā samīpe: optionally samāhāra in 'proximity' (samīpa) context."""
    return (c.get("sense") == SamasaSense.SAMIPA
            and c.get("is_optional", False))

def sutra_2_4_19(c) -> bool:
    """tatpuruṣo'nañ karmadhārayaḥ: adhikāra — from here, tatpuruṣa
    excluding nañ is karmadhāraya."""
    ct = c.get("compound_type")
    first = c.get("first","")
    return (ct in {SamasaType.TATPURUSHA, SamasaType.KARMADHARAYA}
            and first not in {"na","nañ","a","an"})

def sutra_2_4_20(c) -> bool:
    """saṃjñāyāṃ kanthauśīnareṣu: in proper names of the kantha/uśīnara
    type — specific compound forms."""
    kanth_etc = frozenset({"kantha","uśīnara","kāśī","magadha"})
    return (c.get("is_samjna", False)
            and c.get("second","") in kanth_etc)

def sutra_2_4_21(c) -> bool:
    """upajñopakramaṃ tadādyācikḥyāsāyām: in the sense of 'invented/begun
    by X' when wishing to communicate the originator."""
    return c.get("semantic_context") == "upajnopakrama"

def sutra_2_4_22(c) -> bool:
    """chāyā bāhulye: 'chāyā' (shadow/reflection) in abundance/multiplicity
    context."""
    return (c.get("first") == "chāyā"
            and c.get("semantic_context") == "bahulya")

def sutra_2_4_23(c) -> bool:
    """sabhā rājā'manuṣyapūrvā: 'sabhā' (assembly) preceded by a non-human
    or rājan word — specific compound gender."""
    return (c.get("second") == "sabhā"
            and (c.get("is_raja_first", False)
                 or c.get("is_amanusha_first", False)))

def sutra_2_4_24(c) -> bool:
    """aśālā ca: also without 'śālā' (hall) in a compound — gender rule."""
    return (c.get("second","") != "śālā"
            and c.get("is_ashala_context", False))

def sutra_2_4_25(c) -> bool:
    """vibhāṣā senāsurācchāyāśālāniśānām: optionally for senā/surā/chāyā/
    śālā/niśā — gender of compound."""
    opt_words = frozenset({"senā","surā","chāyā","śālā","niśā"})
    return (c.get("first","") in opt_words
            or c.get("second","") in opt_words)

def sutra_2_4_28(c) -> bool:
    """hemantaśiśirāv ahorātre ca chandasi: hemanta/śiśira + ahorātra —
    in Vedic (chandasi) they are masculine."""
    return (c.get("first","") in {"hemanta","śiśira"}
            and c.get("second","") == "ahorātra"
            and c.get("is_chandas", False))

def sutra_2_4_29(c) -> bool:
    """rātrāhnāhāḥ puṃsi: rātri/ahna/ahas — masculine (puṃsi) in certain
    compound positions."""
    return c.get("first","") in {"rātri","ahna","ahas","rātra"}

def sutra_2_4_30(c) -> bool:
    """apatha napuṃsakam: 'apatha' (wrong path) is neuter."""
    return c.get("compound_lemma","") == "apatha" or c.get("first") == "a" and c.get("second") == "patha"

def sutra_2_4_31(c) -> bool:
    """ardharcāḥ puṃsi ca: ardha-ṛca (half-verse) and similar are
    masculine too (puṃsi ca)."""
    return c.get("compound_lemma","") in {"ardharca","ardharātra"}

def sutra_2_4_32(c) -> bool:
    """idamo'nvādeśe'śanudāttastat ṛtīyādau: 'idam' in anv-ādeśa
    (coreferential substitution) before third-case etc. — accent rule."""
    return (c.get("first") == "idam"
            and c.get("is_anvadesha", False)
            and c.get("case") in {Case.INSTRUMENTAL, Case.DATIVE,
                                   Case.ABLATIVE, Case.GENITIVE, Case.LOCATIVE})

def sutra_2_4_33(c) -> bool:
    """etadastrataso-stratasau cānudāttau: 'etad'+'astra'/'tasa'/'tras'
    substitutes are anudātta (unaccented)."""
    return (c.get("first") in {"etad","etad+astra"}
            and c.get("is_anudatta_context", False))

def sutra_2_4_34(c) -> bool:
    """dvitīyāṭaus-svenaḥ: accusative dual — specific ending substitution
    in idam-paradigm."""
    return (c.get("case") == Case.ACCUSATIVE
            and c.get("number") == GrammaticalNumber.DUAL
            and c.get("first") == "idam")

def sutra_2_4_35(c) -> bool:
    """ārdhadhātuke: adhikāra — from here, rules apply in ārdhadhātuka
    (secondary-stem) context."""
    return c.get("is_ardhadhatuka", True)

def sutra_2_4_38(c) -> bool:
    """ghañapoś ca: also in ghañ and ap [suffixed forms] — dhātu alternation
    applies."""
    return c.get("suffix","") in {"ghañ","ap","a"}

def sutra_2_4_39(c) -> bool:
    """bahulaṃ chandasi: variously (bahulam) in Vedic register."""
    return c.get("is_chandas", False)

def sutra_2_4_40(c) -> bool:
    """liṭy anyatarasyām: optionally in liṭ (perfect) — dhātu alternation."""
    return (c.get("lakara") == Lakara.LIT
            and c.get("is_optional", True))

def sutra_2_4_41(c) -> bool:
    """veño vayiḥ: 've' (weave) → 'vayi' in certain contexts."""
    return c.get("dhatu_lemma","") in {"ve","vay"}

def sutra_2_4_43(c) -> bool:
    """luṅi ca: also in luṅ (aorist) — dhātu alternation applies."""
    return c.get("lakara") == Lakara.LUN

def sutra_2_4_44(c) -> bool:
    """ātmanepadesy anyatarasyām: optionally in ātmanepada forms."""
    return (c.get("pada") == Pada.ATMANEPADA
            and c.get("is_optional", True))

def sutra_2_4_46(c) -> bool:
    """ṇau gamira-bodhane: 'gam' (go) in ṇic (causative) context,
    in non-awakening (abodhana) sense."""
    return (c.get("dhatu_lemma","") in {"gam","gā"}
            and c.get("is_causative", False)
            and not c.get("is_bodhana", False))

def sutra_2_4_49(c) -> bool:
    """gāṅ liṭi: 'gā' (go, sing) in liṭ (perfect)."""
    return (c.get("dhatu_lemma","") in {"gā","gai"}
            and c.get("lakara") == Lakara.LIT)

def sutra_2_4_50(c) -> bool:
    """vibhāṣā luṅlṛṅoḥ: optionally in luṅ and lṛṅ."""
    return (c.get("lakara") in {Lakara.LUN, Lakara.LRN}
            and c.get("is_optional", True))

def sutra_2_4_51(c) -> bool:
    """ṇau ca saṃścaṅoḥ: also in ṇic [causative] before saṃ/caṅ."""
    return (c.get("is_causative", False)
            and c.get("suffix","") in {"saṃ","caṅ","ṇic"})

def sutra_2_4_53(c) -> bool:
    """bruvo vaciḥ: 'brū' (speak) → 'vac' in certain conjugational contexts."""
    return c.get("dhatu_lemma","") in {"brū","bruv"}

def sutra_2_4_54(c) -> bool:
    """cakṣiṅaḥ khyāñ: 'cakṣ' → 'khyā' in non-perfect forms."""
    return c.get("dhatu_lemma","") in {"cakṣ","khyā"}

def sutra_2_4_55(c) -> bool:
    """vā liṭi: optionally in liṭ (perfect) — dhātu alternation."""
    return (c.get("dhatu_lemma","") in {"brū","cakṣ"}
            and c.get("lakara") == Lakara.LIT)

def sutra_2_4_56(c) -> bool:
    """ajervyaghañapoḥ: 'aj' (drive) changes form in non-ghañ/ap
    suffixed contexts."""
    return (c.get("dhatu_lemma","") == "aj"
            and c.get("suffix","") not in {"ghañ","ap"})

def sutra_2_4_57(c) -> bool:
    """vā yau: optionally in yā [suffix] context."""
    return (c.get("suffix","") == "yā"
            and c.get("is_optional", True))

def sutra_2_4_58(c) -> bool:
    """ṇyakṣatriyārṣañito yūni lugaṇiñoḥ: luk of aṇi/ñi for kṣatriya and
    ṛṣi-lineage words in 'young descendant' (yūna) context."""
    return (c.get("is_kshatriya_rshi", False)
            and c.get("is_yuna", False)
            and c.get("suffix","") in {"aṇ","iñ","ñi","ṇi"})

def sutra_2_4_59(c) -> bool:
    """pailādibhyaś ca: also from paila and similar [luk of taddhita]."""
    pailadi = frozenset({"paila","vaiśampāyana","jaimini","baudhāyana"})
    return c.get("base_lemma","") in pailadi

def sutra_2_4_60(c) -> bool:
    """iñaḥ prācām: luk of iñ for the eastern grammarians (prācām)."""
    return (c.get("suffix","") == "iñ"
            and c.get("is_pracham", False))

def sutra_2_4_61(c) -> bool:
    """na taulvalibhyaḥ: NOT luk from taulvali and similar."""
    taulvali_etc = frozenset({"taulvali","aulvali"})
    return c.get("base_lemma","") not in taulvali_etc

def sutra_2_4_62(c) -> bool:
    """tadrājasya bahuṣu tenai-v-āsriyām: luk of tad-rāja (tribal-king
    suffix) in plural, except in feminine."""
    return (c.get("is_tadraja", False)
            and c.get("number") == GrammaticalNumber.PLURAL
            and c.get("gender") != Gender.FEMININE)

def sutra_2_4_63(c) -> bool:
    """yaskādibhyo gotre: luk for yaska and similar in gotra (lineage)
    context."""
    yaskadi = frozenset({
        "yaska","māṇḍavya","māṭhara","śākalya","sākaṭāyana",
    })
    return (c.get("base_lemma","") in yaskadi
            and c.get("semantic_context") == "gotra")

def sutra_2_4_64(c) -> bool:
    """yañañoś ca: also luk of yañ/añ suffixes [in gotra context]."""
    return (c.get("suffix","") in {"yañ","añ"}
            and c.get("semantic_context") == "gotra")

def sutra_2_4_65(c) -> bool:
    """atribhṛgukutsavasiṣṭhagotamāṅgirobhyaś ca: also from Atri/Bhṛgu/
    Kutsa/Vasiṣṭha/Gautama/Aṅgiras lineages."""
    rshy_lineages = frozenset({
        "atri","bhṛgu","kutsa","vasiṣṭha","gautama","aṅgiras","aṅgira",
    })
    return c.get("base_lemma","") in rshy_lineages

def sutra_2_4_66(c) -> bool:
    """bahvacaḥ iñaḥ prācyabhārateṣu: for polysyllabic stems with iñ
    suffix, among eastern/Bharata [groups]."""
    return (c.get("suffix","") == "iñ"
            and c.get("is_bahvach", False)
            and c.get("is_pracya_bharata", False))

def sutra_2_4_67(c) -> bool:
    """na gopavanādibhyaḥ: NOT luk from gopavana and similar."""
    no_luk = frozenset({"gopavana","udavāha","śaṇḍika"})
    return c.get("base_lemma","") not in no_luk

def sutra_2_4_68(c) -> bool:
    """tikakitavādibhyo dvandve: luk of tika/kitava and similar in dvandva
    compounds."""
    tikakitavadi = frozenset({"tika","kitava","akṣadyū"})
    return (c.get("base_lemma","") in tikakitavadi
            and c.get("compound_type") == SamasaType.DVANDVA)

def sutra_2_4_69(c) -> bool:
    """upakādibhyo'nyatarasyām advandve: optionally from upaka and similar,
    NOT in dvandva."""
    upakadi = frozenset({"upaka","kubera","śalya","nakula","sahadeva"})
    return (c.get("base_lemma","") in upakadi
            and c.get("compound_type") != SamasaType.DVANDVA)

def sutra_2_4_70(c) -> bool:
    """āgastyakauṇḍinyayor agastikuṇḍinac: 'Agastya'/'Kauṇḍinya' get
    special forms 'agasti'/'kuṇḍina' + c(suffix)."""
    return c.get("base_lemma","") in {"āgastya","kauṇḍinya"}

def sutra_2_4_73(c) -> bool:
    """bahulaṃ chandasi: variously in Vedic register — luk applies broadly."""
    return c.get("is_chandas", False)

def sutra_2_4_74(c) -> bool:
    """yaṅo'ci ca: luk of yaṅ (intensive stem) before vowel-initial
    suffixes (ac)."""
    return (c.get("is_yang", False)
            and c.get("is_vowel_initial_suffix", False))

def sutra_2_4_75(c) -> bool:
    """juhotyādibhyaḥ śluḥ: ślu (deletion) of śap for juhotyādi class
    (gaṇa 3 verbs — reduplicating)."""
    varga = c.get("varga", 0)
    return (varga == 3
            or c.get("dhatu_lemma","") in {
                "hu","bhī","hrī","dhā","dā","mā","pā","hā","sthā",
                "jā","bhi","hi","yaj",
            })

def sutra_2_4_76(c) -> bool:
    """bahulaṃ chandasi: variously in Vedic — ślu deletion applies broadly."""
    return c.get("is_chandas", False)

def sutra_2_4_77(c) -> bool:
    """gātisthāghupābhūbhyaḥ sicaḥ parasmaipadeṣu: luk of sic (aorist
    sigmatic suffix) for gā/tiṣṭhā/ghu/pā/bhū in parasmaipada."""
    gadi = frozenset({"gā","sthā","ghu","pā","bhū","dā","hā"})
    return (c.get("dhatu_lemma","") in gadi
            and c.get("suffix","") == "sic"
            and c.get("pada") == Pada.PARASMAIPADA)

def sutra_2_4_78(c) -> bool:
    """vibhāṣā ghrādheṭśācchasāḥ: optionally for ghrā/dhe/śā/cha — luk
    of sic."""
    return (c.get("dhatu_lemma","") in {"ghrā","dhe","śā","cha","ghā"}
            and c.get("suffix","") == "sic"
            and c.get("is_optional", True))

def sutra_2_4_79(c) -> bool:
    """tanādibhyas tathāsoḥ: luk of sic for tanādi (gaṇa 8) before tathā/
    so forms."""
    tanaadi = frozenset({"tan","san","man","van","kṣan","ghan"})
    return (c.get("dhatu_lemma","") in tanaadi
            and c.get("suffix","") in {"sic","so","tathā"})

def sutra_2_4_80(c) -> bool:
    """mantre ghasahvraṇaśavṛdahādvṛckṛgamijani-bhyo leḥ: in mantra, luk
    of li (lyap?) for ghas/hṛ/vṛ/śā/vṛdh/ah/dṛh/kṛ/gam/jan."""
    mantra_roots = frozenset({
        "ghas","hṛ","vṛ","śā","vṛdh","ah","dṛh","kṛ","gam","jan","dvṛc",
    })
    return (c.get("dhatu_lemma","") in mantra_roots
            and c.get("is_mantra", False)
            and c.get("suffix","") in {"li","lyap","liṭ"})

def sutra_2_4_81(c) -> bool:
    """āmaḥ: luk of 'āma' suffix [in perfect periphrastic forms]."""
    return c.get("suffix","") == "āma"

def sutra_2_4_82(c) -> bool:
    """avyayādāpsupaḥ: luk of āp and sup suffixes after avyaya."""
    return (c.get("is_avyaya", False)
            and c.get("suffix","") in {"āp","sup"})

def sutra_2_4_83(c) -> bool:
    """nāvyayībhāvādato'mtvapañcamyāḥ: NOT luk from avyayībhāva of 'a'-
    ending stem except for the am and pañcamī forms."""
    ct = c.get("compound_type")
    suffix = c.get("suffix","")
    if ct != SamasaType.AVYAYIBHAVA:
        return True  # rule doesn't restrict non-avyayibhava
    # For avyayibhava ending in 'a', only am and pañcamī get luk
    if c.get("ends_in_a", False):
        return suffix in {"am","at"}
    return True

def sutra_2_4_84(c) -> bool:
    """tṛtīyāsaptamyor bahulam: variously (bahulam) for instrumental and
    locative [in avyayibhava of 'a'-ending]."""
    return (c.get("case") in {Case.INSTRUMENTAL, Case.LOCATIVE}
            and c.get("compound_type") == SamasaType.AVYAYIBHAVA)

def sutra_2_4_85(c) -> bool:
    """luṭaḥ prathamasya ḍāraurasaḥ: the first-person forms of luṭ (1st
    future) substitute ḍā/rau/ras for tā/rau/ras."""
    return (c.get("lakara") == Lakara.LUT
            and c.get("person","") in {"first","third"}
            and c.get("is_dara_substitution", False))


# ===========================================================================
# Linguistic fixtures + module API.
#
# Every sutra in this module has a hand-curated (positive, negative) pair of
# real Sanskrit contexts that the predicate must classify correctly. These
# fixtures replace the slug-roundtrip scaffolds previously generated by
# sutra_handlers_adhyaya23._evaluate / _features for Adhyāya 2.
# ===========================================================================


def _m(case=None, lemma="x", surface=None, gender=None, number=None,
       pos=PartOfSpeech.NOUN, value=None) -> Analysis:
    """Compact Analysis builder for fixtures."""
    return Analysis(
        surface=surface if surface is not None else lemma,
        lemma=lemma,
        pos=pos,
        case=case,
        gender=gender,
        number=number,
        value=value,
    )


_LOC_AKSA = _m(Case.LOCATIVE, "akṣa", "akṣeṣu", Gender.MASCULINE)
_NOM_RAMA = _m(Case.NOMINATIVE, "rāma", "rāmaḥ", Gender.MASCULINE)
_NOM_X    = _m(Case.NOMINATIVE, "phala", "phalaḥ", Gender.NEUTER)
_ACC_X    = _m(Case.ACCUSATIVE, "phala", "phalam", Gender.NEUTER)
_INS_X    = _m(Case.INSTRUMENTAL, "bāhu", "bāhunā", Gender.MASCULINE)
_ABL_X    = _m(Case.ABLATIVE, "vṛkṣa", "vṛkṣāt", Gender.MASCULINE)
_GEN_X    = _m(Case.GENITIVE, "rājan", "rājñaḥ", Gender.MASCULINE)


FIXTURES: dict[str, tuple[dict, dict]] = {
    # 2.1 — samāsa adhikāra and tatpuruṣa / karmadhāraya details
    "2.1.2":  ({"is_amantrita": True, "scope": "svara"},
               {"is_amantrita": False, "scope": "samasa"}),
    "2.1.3":  ({"scope": "samasa"},
               {"scope": "meta"}),
    "2.1.25": ({"first": "svayam", "kt_suffix": "kta"},
               {"first": "rāma", "kt_suffix": None}),
    "2.1.26": ({"first": "khaṭvā", "is_kshepa": True},
               {"first": "khaṭvā", "is_kshepa": False}),
    "2.1.27": ({"first": "sāmi"},
               {"first": "pūrṇa"}),
    "2.1.28": ({"members": (_ACC_X, _m(Case.NOMINATIVE, "māsa", "māsaḥ")),
                "first": "phala", "second": "māsa"},
               {"members": (_NOM_X, _NOM_RAMA), "first": "phala", "second": "rāma"}),
    "2.1.29": ({"members": (_ACC_X, _m(Case.NOMINATIVE, "kāla", "kālam")),
                "sense": SamasaSense.DVIT_TAT, "is_atyanta": True},
               {"members": (_ACC_X, _NOM_RAMA),
                "sense": SamasaSense.DVIT_TAT, "is_atyanta": False}),
    "2.1.31": ({"members": (_INS_X, _m(Case.NOMINATIVE, "sadṛśa", "sadṛśaḥ")),
                "first": "māsa", "second": "sadṛśa"},
               {"members": (_INS_X, _NOM_RAMA), "first": "māsa", "second": "rāma"}),
    "2.1.32": ({"kt_suffix": "kta", "first_case": Case.INSTRUMENTAL,
                "is_kartri_karana": True},
               {"kt_suffix": "kta", "first_case": Case.GENITIVE,
                "is_kartri_karana": False}),
    "2.1.33": ({"members": (_INS_X, _m(Case.NOMINATIVE, "kārya", "kāryaḥ")),
                "kt_suffix": "tavya", "is_adhikartha": True},
               {"members": (_INS_X, _NOM_RAMA),
                "kt_suffix": "tavya", "is_adhikartha": False}),
    "2.1.34": ({"members": (_INS_X, _m(Case.NOMINATIVE, "vyañjana", "vyañjanam")),
                "second": "vyañjana"},
               {"members": (_INS_X, _NOM_RAMA), "second": "rāma"}),
    "2.1.35": ({"members": (_INS_X, _m(Case.NOMINATIVE, "bhakṣya", "bhakṣyam")),
                "is_mishrana": True},
               {"members": (_INS_X, _NOM_RAMA), "is_mishrana": False}),
    "2.1.37": ({"members": (_ABL_X, _m(Case.NOMINATIVE, "bhaya", "bhayam")),
                "second": "bhaya"},
               {"members": (_ABL_X, _NOM_RAMA), "second": "rāma"}),
    "2.1.38": ({"members": (_ABL_X, _m(Case.NOMINATIVE, "mukta", "muktaḥ")),
                "second": "mukta"},
               {"members": (_ABL_X, _NOM_RAMA), "second": "rāma"}),
    "2.1.39": ({"members": (_ABL_X, _m(Case.NOMINATIVE, "āgata", "āgataḥ")),
                "first": "stoka", "kt_suffix": "kta"},
               {"members": (_ABL_X, _NOM_RAMA), "first": "rāma", "kt_suffix": None}),
    "2.1.40": ({"members": (_LOC_AKSA, _m(Case.NOMINATIVE, "śauṇḍa", "śauṇḍaḥ")),
                "second": "śauṇḍa"},
               {"members": (_LOC_AKSA, _NOM_RAMA), "second": "rāma"}),
    "2.1.41": ({"members": (_LOC_AKSA, _m(Case.NOMINATIVE, "siddha", "siddhaḥ")),
                "second": "siddha"},
               {"members": (_LOC_AKSA, _NOM_RAMA), "second": "rāma"}),
    "2.1.42": ({"second": "dhvāṅkṣa", "is_kshepa": True},
               {"second": "dhvāṅkṣa", "is_kshepa": False}),
    "2.1.43": ({"members": (_LOC_AKSA, _m(Case.NOMINATIVE, "deya", "deyaḥ")),
                "kt_suffix": "tavya", "is_rna_context": True},
               {"members": (_LOC_AKSA, _NOM_RAMA),
                "kt_suffix": "tavya", "is_rna_context": False}),
    "2.1.44": ({"members": (_LOC_AKSA, _NOM_RAMA), "is_samjna": True},
               {"members": (_LOC_AKSA, _NOM_RAMA), "is_samjna": False}),
    "2.1.45": ({"first": "prabhāta", "kt_suffix": "kta"},
               {"first": "rāma", "kt_suffix": "kta"}),
    "2.1.46": ({"first": "tatra"},
               {"first": "rāma"}),
    "2.1.47": ({"members": (_LOC_AKSA, _NOM_RAMA), "is_kshepa": True},
               {"members": (_LOC_AKSA, _NOM_RAMA), "is_kshepa": False}),
    "2.1.48": ({"first": "pātrasamita"},
               {"first": "rāma"}),
    "2.1.49": ({"first": "pūrvakāla"},
               {"first": "rāma"}),
    "2.1.50": ({"first": "pūrva", "is_samjna": True},
               {"first": "pūrva", "is_samjna": False}),
    "2.1.51": ({"is_taddhitartha": True},
               {"is_taddhitartha": False, "is_uttarapada": False, "is_samahara": False}),
    "2.1.52": ({"members": (_m(Case.ACCUSATIVE, "pañcan", "pañca", pos=PartOfSpeech.NUMERAL, value=5),
                            _m(Case.NOMINATIVE, "phala", "phalam", Gender.NEUTER))},
               {"members": (_NOM_RAMA, _NOM_X)}),
    "2.1.53": ({"is_kutsita_first": True, "is_kutsana_second": True},
               {"is_kutsita_first": False, "is_kutsana_second": False}),
    "2.1.54": ({"first": "pāpa", "is_kutsita": True},
               {"first": "rāma", "is_kutsita": False}),
    "2.1.55": ({"is_upamana_first": True, "is_samanya_second": True},
               {"is_upamana_first": False, "is_samanya_second": False}),
    "2.1.56": ({"second": "vyāghra", "is_samanya_expressed": False},
               {"second": "vyāghra", "is_samanya_expressed": True}),
    "2.1.58": ({"second": "pūrva"},
               {"second": "rāma"}),
    "2.1.59": ({"first": "śreṇi", "second": "kṛta"},
               {"first": "rāma", "second": "phala"}),
    "2.1.60": ({"kt_suffix": "kta", "is_nañ_qualified": True, "is_nañ_compound": False},
               {"kt_suffix": "kta", "is_nañ_qualified": True, "is_nañ_compound": True}),
    "2.1.61": ({"first": "sat", "is_praising": True},
               {"first": "sat", "is_praising": False}),
    "2.1.62": ({"second": "vṛndāraka", "is_praising": True},
               {"second": "vṛndāraka", "is_praising": False}),
    "2.1.63": ({"first": "katara", "is_jati_pariprashn": True},
               {"first": "katara", "is_jati_pariprashn": False}),
    "2.1.64": ({"first": "kim", "is_kshepa": True},
               {"first": "kim", "is_kshepa": False}),
    "2.1.65": ({"first": "poṭā"},
               {"first": "rāma"}),
    "2.1.66": ({"is_prashansa_second": True},
               {"is_prashansa_second": False}),
    "2.1.67": ({"first": "yuvā", "second": "khalati"},
               {"first": "yuvā", "second": "rāma"}),
    "2.1.68": ({"is_kritya_tulya": True, "is_jati": False},
               {"is_kritya_tulya": True, "is_jati": True}),
    "2.1.69": ({"first": "nīla", "second": "śyāma"},
               {"first": "nīla", "second": "rāma"}),
    "2.1.70": ({"first": "kumāra", "second": "śramaṇa"},
               {"first": "kumāra", "second": "rāma"}),
    "2.1.71": ({"first": "go", "second": "garbhiṇī"},
               {"first": "go", "second": "rāma"}),
    "2.1.72": ({"first": "mayūravyaṃsaka"},
               {"first": "rāma"}),

    # 2.2 — bahuvrīhi, dvandva, ordering
    "2.2.1":  ({"first": "pūrva", "is_ekadeshin": True, "is_ekadhikarana": True},
               {"first": "pūrva", "is_ekadeshin": False, "is_ekadhikarana": False}),
    "2.2.2":  ({"first": "ardha"},
               {"first": "rāma"}),
    "2.2.3":  ({"first": "dvitīya"},
               {"first": "rāma", "second": "phala"}),
    "2.2.4":  ({"members": (_ACC_X, _m(Case.NOMINATIVE, "prāpta", "prāptaḥ")),
                "second": "prāpta"},
               {"members": (_NOM_X, _NOM_RAMA), "second": "rāma"}),
    "2.2.5":  ({"members": (_m(Case.NOMINATIVE, "māsa", "māsaḥ"),
                            _m(Case.INSTRUMENTAL, "parimāṇa", "parimāṇena"))},
               {"members": (_NOM_RAMA, _NOM_X)}),
    "2.2.6":  ({"first": "na"},
               {"first": "rāma"}),
    "2.2.7":  ({"first": "īṣat", "kt_suffix": "kta"},
               {"first": "īṣat", "kt_suffix": None}),
    "2.2.8":  ({"members": (_GEN_X, _NOM_X)},
               {"members": (_NOM_RAMA, _NOM_X)}),
    "2.2.9":  ({"second": "yājaka"},
               {"second": "rāma"}),
    "2.2.10": ({"is_nirdhana": False},
               {"is_nirdhana": True}),
    "2.2.11": ({"second": "pūraṇa"},
               {"second": "rāma"}),
    "2.2.12": ({"kt_suffix": "kta", "is_puja": True},
               {"kt_suffix": "kta", "is_puja": False}),
    "2.2.13": ({"is_adhikarana_second": True},
               {"is_adhikarana_second": False}),
    "2.2.14": ({"role": Role.KARMAN},
               {"role": Role.KARTR, "is_karma_relation": False}),
    "2.2.15": ({"kt_suffix": "tṛc", "role": Role.KARTR},
               {"kt_suffix": "tṛc", "role": Role.KARMAN, "is_kartri_relation": False}),
    "2.2.16": ({"role": Role.KARTR},
               {"role": Role.KARMAN, "is_kartri_relation": False}),
    "2.2.17": ({"is_krida": True},
               {"is_krida": False, "is_jivika": False}),
    "2.2.18": ({"first": "pra"},
               {"first": "rāma"}),
    "2.2.19": ({"upapada": "go", "kt_suffix": "ka", "is_ting": False},
               {"upapada": None, "kt_suffix": None, "is_ting": True}),
    "2.2.20": ({"is_am": True, "is_avyaya_second": True},
               {"is_am": False, "is_avyaya_second": False}),
    "2.2.21": ({"members": (_INS_X, _NOM_X), "is_optional": True},
               {"members": (_NOM_RAMA, _NOM_X), "is_optional": False}),
    "2.2.22": ({"kt_suffix": "ktvā"},
               {"kt_suffix": "kta"}),
    "2.2.23": ({"compound_type": SamasaType.BAHUVRIHI},
               {"compound_type": SamasaType.TATPURUSHA, "is_bahuvrihi_context": False}),
    "2.2.24": ({"members": (_NOM_RAMA, _NOM_X), "is_anyapadartha": True},
               {"members": (_NOM_RAMA, _NOM_X), "is_anyapadartha": False}),
    "2.2.25": ({"is_numeral_second": True},
               {"is_numeral_second": False, "is_samkhyeya": False}),
    "2.2.26": ({"members": (_m(lemma="pūrva"), _m(lemma="uttara")), "is_antarala": True},
               {"members": (_m(lemma="rāma"), _m(lemma="phala")), "is_antarala": False}),
    "2.2.27": ({"is_sarupa": True},
               {"is_sarupa": False}),
    "2.2.28": ({"first": "saha", "is_tulya_yoga": True},
               {"first": "saha", "is_tulya_yoga": False}),
    "2.2.31": ({"first": "rāja", "second": "danta"},
               {"first": "rāma", "second": "phala"}),
    "2.2.32": ({"compound_type": SamasaType.DVANDVA,
                "members": (_m(lemma="agni"), _m(lemma="vāyu"))},
               {"compound_type": SamasaType.DVANDVA,
                "members": (_m(lemma="rāma"), _m(lemma="kṛṣṇa"))}),
    "2.2.33": ({"compound_type": SamasaType.DVANDVA,
                "members": (_m(lemma="rāma"), _m(lemma="ahas"))},
               {"compound_type": SamasaType.DVANDVA,
                "members": (_m(lemma="rāma"), _m(lemma="kṛṣṇa"))}),
    "2.2.34": ({"compound_type": SamasaType.DVANDVA,
                "members": (_m(lemma="ka"), _m(lemma="deva"))},
               {"compound_type": SamasaType.DVANDVA,
                "members": (_m(lemma="deva"), _m(lemma="ka"))}),
    "2.2.35": ({"compound_type": SamasaType.BAHUVRIHI,
                "members": (_LOC_AKSA, _NOM_RAMA)},
               {"compound_type": SamasaType.BAHUVRIHI,
                "members": (_NOM_X, _NOM_RAMA)}),
    "2.2.36": ({"kt_suffix": "kta", "compound_type": SamasaType.BAHUVRIHI},
               {"kt_suffix": "kta", "compound_type": SamasaType.TATPURUSHA}),
    "2.2.37": ({"compound_id": "āhitāgni"},
               {"compound_id": "rāmagṛha", "is_ahitagnyadi": False}),
    "2.2.38": ({"second": "kaḍāra"},
               {"second": "rāma"}),

    # 2.3 — vibhakti
    "2.3.37": ({"is_bhava_lakshana": True},
               {"is_bhava_lakshana": False}),
    "2.3.38": ({"is_anadara": True},
               {"is_anadara": False}),
    "2.3.39": ({"companion_lemma": "svāmin"},
               {"companion_lemma": "rāma"}),
    "2.3.40": ({"companion_lemma": "āyukta", "semantic_context": "aseva"},
               {"companion_lemma": "āyukta", "semantic_context": "other"}),
    "2.3.41": ({"semantic_context": "nirdhana"},
               {"semantic_context": "other"}),
    "2.3.42": ({"case": Case.ABLATIVE, "semantic_context": "vibhakta"},
               {"case": Case.NOMINATIVE, "semantic_context": "vibhakta"}),
    "2.3.43": ({"companion_lemma": "sādhu", "semantic_context": "arca",
                "case": Case.LOCATIVE},
               {"companion_lemma": "sādhu", "semantic_context": "arca",
                "case": Case.DATIVE}),
    "2.3.44": ({"companion_lemma": "prasita", "case": Case.INSTRUMENTAL},
               {"companion_lemma": "prasita", "case": Case.LOCATIVE}),
    "2.3.45": ({"is_nakshatra": True, "is_luk": True},
               {"is_nakshatra": True, "is_luk": False}),
    "2.3.46": ({"case": Case.NOMINATIVE, "semantic_context": "pratipadika_only"},
               {"case": Case.ACCUSATIVE, "semantic_context": "pratipadika_only"}),
    "2.3.47": ({"case": Case.VOCATIVE},
               {"case": Case.NOMINATIVE}),
    "2.3.48": ({"case": Case.VOCATIVE, "scope": "samjna"},
               {"case": Case.VOCATIVE, "scope": "other"}),
    "2.3.49": ({"case": Case.VOCATIVE, "number": GrammaticalNumber.SINGULAR,
                "scope": "samjna"},
               {"case": Case.VOCATIVE, "number": GrammaticalNumber.PLURAL,
                "scope": "samjna"}),
    "2.3.51": ({"verb_lemma": "jñā", "semantic_context": "avid",
                "case": Case.INSTRUMENTAL},
               {"verb_lemma": "jñā", "semantic_context": "other",
                "case": Case.INSTRUMENTAL}),
    "2.3.52": ({"verb_lemma": "gam", "case": Case.GENITIVE,
                "semantic_context": "adhigama"},
               {"verb_lemma": "gam", "case": Case.NOMINATIVE,
                "semantic_context": "adhigama"}),
    "2.3.53": ({"verb_lemma": "kṛ", "semantic_context": "pratiyatna",
                "case": Case.ABLATIVE},
               {"verb_lemma": "kṛ", "semantic_context": "other",
                "case": Case.ABLATIVE}),
    "2.3.54": ({"verb_lemma": "ruj", "is_bhava_vacana": True,
                "case": Case.GENITIVE},
               {"verb_lemma": "ruj", "is_bhava_vacana": False,
                "case": Case.GENITIVE}),
    "2.3.55": ({"companion_lemma": "nātha", "semantic_context": "ashish"},
               {"companion_lemma": "nātha", "semantic_context": "other"}),
    "2.3.56": ({"verb_lemma": "han", "semantic_context": "himsa",
                "case": Case.GENITIVE},
               {"verb_lemma": "han", "semantic_context": "other",
                "case": Case.GENITIVE}),
    "2.3.57": ({"verb_lemma": "vyavahṛ", "is_samartha": True,
                "case": Case.GENITIVE},
               {"verb_lemma": "vyavahṛ", "is_samartha": False,
                "case": Case.GENITIVE}),
    "2.3.58": ({"is_divasa": True, "semantic_context": "tadartha",
                "case": Case.GENITIVE},
               {"is_divasa": True, "semantic_context": "other",
                "case": Case.GENITIVE}),
    "2.3.59": ({"upasarga": "pra", "is_optional": True},
               {"upasarga": None, "is_optional": True}),
    "2.3.60": ({"is_chandas": True, "case": Case.ACCUSATIVE},
               {"is_chandas": True, "case": Case.GENITIVE}),
    "2.3.61": ({"verb_lemma": "preṣ", "semantic_context": "devatā_sampradāna",
                "case": Case.DATIVE},
               {"verb_lemma": "preṣ", "semantic_context": "other",
                "case": Case.DATIVE}),
    "2.3.62": ({"is_chandas": True, "case": Case.DATIVE},
               {"is_chandas": True, "case": Case.GENITIVE}),
    "2.3.63": ({"verb_lemma": "yaj", "case": Case.INSTRUMENTAL},
               {"verb_lemma": "yaj", "case": Case.NOMINATIVE}),
    "2.3.64": ({"semantic_context": "krtvo_artha", "case": Case.LOCATIVE},
               {"semantic_context": "krtvo_artha", "case": Case.NOMINATIVE}),
    "2.3.65": ({"is_krit_noun": True, "case": Case.GENITIVE, "role": Role.KARTR},
               {"is_krit_noun": True, "case": Case.NOMINATIVE, "role": Role.KARTR}),
    "2.3.66": ({"is_ubhaya_prapta": True, "case": Case.ACCUSATIVE},
               {"is_ubhaya_prapta": True, "case": Case.NOMINATIVE}),
    "2.3.67": ({"kt_suffix": "kta", "is_vartamana": True, "case": Case.GENITIVE},
               {"kt_suffix": "kta", "is_vartamana": False, "case": Case.GENITIVE}),
    "2.3.68": ({"is_adhikarana_krit": True, "case": Case.GENITIVE},
               {"is_adhikarana_krit": True, "case": Case.NOMINATIVE}),
    "2.3.69": ({"kt_suffix": "kta", "second": "rāma"},
               {"kt_suffix": "niṣṭhā", "second": "rāma"}),
    "2.3.70": ({"companion_lemma": "eka", "semantic_context": "bhavishyat"},
               {"companion_lemma": "eka", "semantic_context": "other"}),
    "2.3.71": ({"kt_suffix": "tavya", "role": Role.KARTR, "case": Case.GENITIVE},
               {"kt_suffix": "tavya", "role": Role.KARTR, "case": Case.NOMINATIVE}),
    "2.3.72": ({"companion_lemma": "atula", "case": Case.INSTRUMENTAL},
               {"companion_lemma": "atula", "case": Case.NOMINATIVE}),
    "2.3.73": ({"companion_lemma": "āyuṣya", "semantic_context": "ashish",
                "case": Case.DATIVE},
               {"companion_lemma": "āyuṣya", "semantic_context": "other",
                "case": Case.DATIVE}),

    # 2.4 — sup-luk, compound gender, dhātu alternation
    "2.4.2":  ({"compound_type": SamasaType.DVANDVA, "semantic_category": "praṇi",
                "members": (_NOM_RAMA, _NOM_X)},
               {"compound_type": SamasaType.TATPURUSHA, "semantic_category": "praṇi",
                "members": (_NOM_RAMA, _NOM_X)}),
    "2.4.3":  ({"compound_type": SamasaType.DVANDVA,
                "semantic_category": "carana", "is_anuvada": True},
               {"compound_type": SamasaType.DVANDVA,
                "semantic_category": "carana", "is_anuvada": False}),
    "2.4.4":  ({"members": (_m(lemma="adhvaryu"), _m(lemma="kratu"))},
               {"members": (_m(lemma="rāma"), _m(lemma="kṛṣṇa"))}),
    "2.4.5":  ({"compound_type": SamasaType.DVANDVA,
                "is_adhyayana_carana": True, "is_viprakrishta": False},
               {"compound_type": SamasaType.DVANDVA,
                "is_adhyayana_carana": True, "is_viprakrishta": True}),
    "2.4.6":  ({"compound_type": SamasaType.DVANDVA,
                "is_jati": True, "is_praṇi": False,
                "members": (_NOM_X, _NOM_X)},
               {"compound_type": SamasaType.DVANDVA,
                "is_jati": True, "is_praṇi": True,
                "members": (_NOM_X, _NOM_X)}),
    "2.4.7":  ({"is_nadi_or_desha": True, "is_grama": False},
               {"is_nadi_or_desha": True, "is_grama": True}),
    "2.4.8":  ({"is_kshudra_jantava": True},
               {"is_kshudra_jantava": False}),
    "2.4.9":  ({"is_shasvata_virodha": True},
               {"is_shasvata_virodha": False}),
    "2.4.10": ({"is_shudra_anirvasita": True},
               {"is_shudra_anirvasita": False}),
    "2.4.11": ({"compound_type": SamasaType.DVANDVA,
                "members": (_m(lemma="go"), _m(lemma="aśva"))},
               {"compound_type": SamasaType.DVANDVA,
                "members": (_m(lemma="rāma"), _m(lemma="kṛṣṇa"))}),
    "2.4.12": ({"compound_type": SamasaType.DVANDVA, "semantic_category": "vriksha"},
               {"compound_type": SamasaType.DVANDVA, "semantic_category": "other"}),
    "2.4.13": ({"is_vipratishiddha": True, "is_adhikarana_vachana": False},
               {"is_vipratishiddha": True, "is_adhikarana_vachana": True}),
    "2.4.14": ({"members": (_m(lemma="rāma"), _m(lemma="kṛṣṇa"))},
               {"members": (_m(lemma="dadhi"), _m(lemma="payas"))}),
    "2.4.15": ({"is_adhikarana_etavatva": True},
               {"is_adhikarana_etavatva": False}),
    "2.4.16": ({"sense": SamasaSense.SAMIPA, "is_optional": True},
               {"sense": SamasaSense.SAMIPA, "is_optional": False}),
    "2.4.19": ({"compound_type": SamasaType.TATPURUSHA, "first": "rāja"},
               {"compound_type": SamasaType.TATPURUSHA, "first": "na"}),
    "2.4.20": ({"is_samjna": True, "second": "kantha"},
               {"is_samjna": False, "second": "kantha"}),
    "2.4.21": ({"semantic_context": "upajnopakrama"},
               {"semantic_context": "other"}),
    "2.4.22": ({"first": "chāyā", "semantic_context": "bahulya"},
               {"first": "chāyā", "semantic_context": "other"}),
    "2.4.23": ({"second": "sabhā", "is_raja_first": True},
               {"second": "sabhā", "is_raja_first": False, "is_amanusha_first": False}),
    "2.4.24": ({"second": "kuṭi", "is_ashala_context": True},
               {"second": "śālā", "is_ashala_context": True}),
    "2.4.25": ({"first": "senā"},
               {"first": "rāma", "second": "kṛṣṇa"}),
    "2.4.28": ({"first": "hemanta", "second": "ahorātra", "is_chandas": True},
               {"first": "hemanta", "second": "ahorātra", "is_chandas": False}),
    "2.4.29": ({"first": "rātri"},
               {"first": "rāma"}),
    "2.4.30": ({"compound_lemma": "apatha"},
               {"compound_lemma": "x", "first": "rāma", "second": "phala"}),
    "2.4.31": ({"compound_lemma": "ardharca"},
               {"compound_lemma": "rāma"}),
    "2.4.32": ({"first": "idam", "is_anvadesha": True, "case": Case.INSTRUMENTAL},
               {"first": "idam", "is_anvadesha": False, "case": Case.NOMINATIVE}),
    "2.4.33": ({"first": "etad", "is_anudatta_context": True},
               {"first": "etad", "is_anudatta_context": False}),
    "2.4.34": ({"case": Case.ACCUSATIVE, "number": GrammaticalNumber.DUAL,
                "first": "idam"},
               {"case": Case.ACCUSATIVE, "number": GrammaticalNumber.SINGULAR,
                "first": "idam"}),
    "2.4.35": ({"is_ardhadhatuka": True},
               {"is_ardhadhatuka": False}),
    "2.4.38": ({"suffix": "ghañ"},
               {"suffix": "kta"}),
    "2.4.39": ({"is_chandas": True},
               {"is_chandas": False}),
    "2.4.40": ({"lakara": Lakara.LIT, "is_optional": True},
               {"lakara": Lakara.LAT, "is_optional": True}),
    "2.4.41": ({"dhatu_lemma": "ve"},
               {"dhatu_lemma": "rāma"}),
    "2.4.43": ({"lakara": Lakara.LUN},
               {"lakara": Lakara.LAT}),
    "2.4.44": ({"pada": Pada.ATMANEPADA, "is_optional": True},
               {"pada": Pada.PARASMAIPADA, "is_optional": True}),
    "2.4.46": ({"dhatu_lemma": "gam", "is_causative": True, "is_bodhana": False},
               {"dhatu_lemma": "gam", "is_causative": True, "is_bodhana": True}),
    "2.4.49": ({"dhatu_lemma": "gā", "lakara": Lakara.LIT},
               {"dhatu_lemma": "gā", "lakara": Lakara.LAT}),
    "2.4.50": ({"lakara": Lakara.LUN, "is_optional": True},
               {"lakara": Lakara.LAT, "is_optional": True}),
    "2.4.51": ({"is_causative": True, "suffix": "ṇic"},
               {"is_causative": True, "suffix": "kta"}),
    "2.4.53": ({"dhatu_lemma": "brū"},
               {"dhatu_lemma": "rāma"}),
    "2.4.54": ({"dhatu_lemma": "cakṣ"},
               {"dhatu_lemma": "rāma"}),
    "2.4.55": ({"dhatu_lemma": "brū", "lakara": Lakara.LIT},
               {"dhatu_lemma": "brū", "lakara": Lakara.LAT}),
    "2.4.56": ({"dhatu_lemma": "aj", "suffix": "ti"},
               {"dhatu_lemma": "aj", "suffix": "ghañ"}),
    "2.4.57": ({"suffix": "yā", "is_optional": True},
               {"suffix": "kta", "is_optional": True}),
    "2.4.58": ({"is_kshatriya_rshi": True, "is_yuna": True, "suffix": "aṇ"},
               {"is_kshatriya_rshi": False, "is_yuna": False, "suffix": "aṇ"}),
    "2.4.59": ({"base_lemma": "paila"},
               {"base_lemma": "rāma"}),
    "2.4.60": ({"suffix": "iñ", "is_pracham": True},
               {"suffix": "iñ", "is_pracham": False}),
    "2.4.61": ({"base_lemma": "rāma"},
               {"base_lemma": "taulvali"}),
    "2.4.62": ({"is_tadraja": True, "number": GrammaticalNumber.PLURAL,
                "gender": Gender.MASCULINE},
               {"is_tadraja": True, "number": GrammaticalNumber.PLURAL,
                "gender": Gender.FEMININE}),
    "2.4.63": ({"base_lemma": "yaska", "semantic_context": "gotra"},
               {"base_lemma": "yaska", "semantic_context": "other"}),
    "2.4.64": ({"suffix": "yañ", "semantic_context": "gotra"},
               {"suffix": "yañ", "semantic_context": "other"}),
    "2.4.65": ({"base_lemma": "atri"},
               {"base_lemma": "rāma"}),
    "2.4.66": ({"suffix": "iñ", "is_bahvach": True, "is_pracya_bharata": True},
               {"suffix": "iñ", "is_bahvach": False, "is_pracya_bharata": False}),
    "2.4.67": ({"base_lemma": "rāma"},
               {"base_lemma": "gopavana"}),
    "2.4.68": ({"base_lemma": "tika", "compound_type": SamasaType.DVANDVA},
               {"base_lemma": "tika", "compound_type": SamasaType.TATPURUSHA}),
    "2.4.69": ({"base_lemma": "upaka", "compound_type": SamasaType.TATPURUSHA},
               {"base_lemma": "upaka", "compound_type": SamasaType.DVANDVA}),
    "2.4.70": ({"base_lemma": "āgastya"},
               {"base_lemma": "rāma"}),
    "2.4.73": ({"is_chandas": True},
               {"is_chandas": False}),
    "2.4.74": ({"is_yang": True, "is_vowel_initial_suffix": True},
               {"is_yang": True, "is_vowel_initial_suffix": False}),
    "2.4.75": ({"varga": 3},
               {"varga": 1, "dhatu_lemma": "rāma"}),
    "2.4.76": ({"is_chandas": True},
               {"is_chandas": False}),
    "2.4.77": ({"dhatu_lemma": "bhū", "suffix": "sic", "pada": Pada.PARASMAIPADA},
               {"dhatu_lemma": "bhū", "suffix": "sic", "pada": Pada.ATMANEPADA}),
    "2.4.78": ({"dhatu_lemma": "ghrā", "suffix": "sic", "is_optional": True},
               {"dhatu_lemma": "rāma", "suffix": "sic", "is_optional": True}),
    "2.4.79": ({"dhatu_lemma": "tan", "suffix": "sic"},
               {"dhatu_lemma": "rāma", "suffix": "kta"}),
    "2.4.80": ({"dhatu_lemma": "ghas", "is_mantra": True, "suffix": "liṭ"},
               {"dhatu_lemma": "ghas", "is_mantra": False, "suffix": "liṭ"}),
    "2.4.81": ({"suffix": "āma"},
               {"suffix": "kta"}),
    "2.4.82": ({"is_avyaya": True, "suffix": "sup"},
               {"is_avyaya": False, "suffix": "sup"}),
    "2.4.83": ({"compound_type": SamasaType.AVYAYIBHAVA, "ends_in_a": True,
                "suffix": "am"},
               {"compound_type": SamasaType.AVYAYIBHAVA, "ends_in_a": True,
                "suffix": "ti"}),
    "2.4.84": ({"case": Case.INSTRUMENTAL, "compound_type": SamasaType.AVYAYIBHAVA},
               {"case": Case.NOMINATIVE, "compound_type": SamasaType.AVYAYIBHAVA}),
    "2.4.85": ({"lakara": Lakara.LUT, "person": "first",
                "is_dara_substitution": True},
               {"lakara": Lakara.LUT, "person": "first",
                "is_dara_substitution": False}),
}


(
    IMPLEMENTED_IDS,
    has_real_implementation,
    handler_for,
    positive_features,
    negative_features,
) = make_module_api(FIXTURES, globals())
