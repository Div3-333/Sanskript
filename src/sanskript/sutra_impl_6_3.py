"""
Discrete Pāṇinian predicates for Adhyāya 6.3 (uttarapada / internal compound).

Hand-written per sūtra from padaccheda in data/ashtadhyayi_sutras.json.
Domain: second-member (uttarapada) operations — aluk, substitution, augment,
lopa, prakṛti retention, and related compound-internal rules opened by 6.3.1.

Context keys include range, operation, uttarapada_rule, compound_type,
vibhakti_source, pūrva_pada, substitute, augment, semantic, is_optional, …
"""
from __future__ import annotations

from .anga import operations_for_range
from .sutra_impl_base import SutraMeta, _eq, make_module_api

_SAMJNA = "samjna"
_PARIBHASHA = "paribhasha"
_VIDHI = "vidhi"
_PRATISEDHA = "pratisedha"
_VIBHASHA = "vibhasha"


def _in_uttarapada_range(c) -> bool:
    return any(op.name == "uttarapada-domain" for op in operations_for_range(str(c.get("range"))))



def sutra_6_3_1(c) -> bool:
    """alug uttarapade: adhikāra over uttarapada operations (range 6.3)."""
    return _in_uttarapada_range(c)

def sutra_6_3_2(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'stokādi') and _eq(c, 'vibhakti_source', 'pañcama')

def sutra_6_3_3(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'ojassahombastamasa') and _eq(c, 'vibhakti_source', 'trtiya')

def sutra_6_3_4(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'manas') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'saṃjñā')

def sutra_6_3_5(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'ājñāyin')

def sutra_6_3_6(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'ātman') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'pūraṇa')

def sutra_6_3_7(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'vaiyākaraṇākhya') and _eq(c, 'vibhakti_source', 'caturthī')

def sutra_6_3_8(c) -> bool:
    return _eq(c, 'anuvritti', 'para') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3")

def sutra_6_3_9(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada_type', 'halanta') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'saṃjñā') and _eq(c, 'vibhakti_source', 'saptamī')

def sutra_6_3_10(c) -> bool:
    return _eq(c, 'dialect', 'prācya') and _eq(c, 'operation', 'aluk') and _eq(c, 'position', 'halādi') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'kāranāman')

def sutra_6_3_11(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'madhya') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'guru')

def sutra_6_3_12(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'amūrdhamastaka') and _eq(c, 'pūrva_pada_type', 'svāṅga') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'akāma')

def sutra_6_3_13(c) -> bool:
    return bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'bandha')

def sutra_6_3_14(c) -> bool:
    return _eq(c, 'compound_type', 'tatpuruṣa') and _eq(c, 'operation', 'bahulam') and _eq(c, "range", "6.3") and _eq(c, 'suffix_class', 'kṛt')

def sutra_6_3_15(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'je') and _eq(c, 'stem_group', 'prāvṛṭśaratkāladiva')

def sutra_6_3_16(c) -> bool:
    return bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'varṣakṣaraśaravara') and _eq(c, "range", "6.3")

def sutra_6_3_17(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada_type', 'kālanāman') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'ghakālatana')

def sutra_6_3_18(c) -> bool:
    return _eq(c, 'excludes', 'kāla') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'śayavāsavāsi')

def sutra_6_3_19(c) -> bool:
    return _eq(c, "range", "6.3") and bool(c.get('rule_blocked')) is True and _eq(c, 'semantic', 'insiddhabadhnāti')

def sutra_6_3_20(c) -> bool:
    return _eq(c, 'domain', 'bhāṣā') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'stha')

def sutra_6_3_21(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'ākrośa') and _eq(c, 'vibhakti_source', 'ṣaṣṭhī')

def sutra_6_3_22(c) -> bool:
    return bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'putra') and _eq(c, "range", "6.3")

def sutra_6_3_23(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada_final', 'ṛ') and _eq(c, "range", "6.3") and _eq(c, 'relation', 'vidyāyoni')

def sutra_6_3_24(c) -> bool:
    return bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'svasṛpatya')

def sutra_6_3_25(c) -> bool:
    return _eq(c, 'augment', 'ān') and _eq(c, 'compound_type', 'dvandva') and _eq(c, 'operation', 'augment') and _eq(c, 'pūrva_pada_final', 'ṛ') and _eq(c, "range", "6.3")

def sutra_6_3_26(c) -> bool:
    return _eq(c, 'compound_type', 'devatā_dvandva') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3")

def sutra_6_3_27(c) -> bool:
    return _eq(c, 'augment', 'īt') and _eq(c, 'operation', 'augment') and _eq(c, 'pūrva_pada', 'agni') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'somavaruna')

def sutra_6_3_28(c) -> bool:
    return _eq(c, 'augment', 'it') and _eq(c, 'operation', 'vṛddhi') and _eq(c, "range", "6.3")

def sutra_6_3_29(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, 'pūrva_pada', 'div') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'dyāv')

def sutra_6_3_30(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'divas') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'pṛthivī')

def sutra_6_3_31(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, 'pūrva_pada', 'uṣas') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'uṣās')

def sutra_6_3_32(c) -> bool:
    return _eq(c, 'direction', 'udīc') and _eq(c, 'operation', 'substitution') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'mātarapitara')

def sutra_6_3_33(c) -> bool:
    return bool(c.get('is_chandas')) is True and _eq(c, 'operation', 'substitution') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'pitarāmātara')

def sutra_6_3_34(c) -> bool:
    return _eq(c, 'gender', 'strī') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'relation', 'samānādhikaraṇa') and _eq(c, 'semantic', 'apūraṇīpriyādi')

def sutra_6_3_35(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada_type', 'kṛtvasuc') and _eq(c, "range", "6.3") and _eq(c, 'suffix_group', 'tasilādi')

def sutra_6_3_36(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'kyaṅmānin')

def sutra_6_3_37(c) -> bool:
    return _eq(c, 'excludes', 'kopadhā') and _eq(c, "range", "6.3") and bool(c.get('rule_blocked')) is True

def sutra_6_3_38(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'saṃjñāpūraṇya')

def sutra_6_3_39(c) -> bool:
    return _eq(c, 'condition', 'vṛddhinimitta') and _eq(c, 'excludes', 'raktavikāra') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'suffix_class', 'taddhita')

def sutra_6_3_40(c) -> bool:
    return _eq(c, 'excludes', 'mānin') and _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada_final', 'ī') and _eq(c, 'pūrva_pada_type', 'svāṅga') and _eq(c, "range", "6.3")

def sutra_6_3_41(c) -> bool:
    return _eq(c, 'anuvritti', 'jāti') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3")

def sutra_6_3_42(c) -> bool:
    return _eq(c, 'compound_type', 'karmadhārayajātīyadeśīya') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3")

def sutra_6_3_43(c) -> bool:
    return _eq(c, 'condition', 'anekāca') and _eq(c, 'operation', 'hrasva') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'gharūpakalpacelaḍbruvagotramatahata') and _eq(c, 'suffix', 'ṅya')

def sutra_6_3_44(c) -> bool:
    return _eq(c, 'anuvritti', 'śeṣa') and _eq(c, 'condition', 'nadyā') and bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3")

def sutra_6_3_45(c) -> bool:
    return _eq(c, 'marker', 'ugit') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3")

def sutra_6_3_46(c) -> bool:
    return _eq(c, 'augment', 'ā') and _eq(c, 'operation', 'augment') and _eq(c, 'pūrva_pada', 'mahat') and _eq(c, "range", "6.3") and _eq(c, 'relation', 'samānādhikaraṇajātīya')

def sutra_6_3_47(c) -> bool:
    return _eq(c, 'excludes', 'bahuvrīhyashīti') and _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'dvyashṭan') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'saṃkhyā')

def sutra_6_3_48(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, 'pūrva_pada', 'tri') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'traya')

def sutra_6_3_49(c) -> bool:
    return bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'scope', 'sarva') and _eq(c, 'stem_group', 'catvāriṃśatprabhṛti')

def sutra_6_3_50(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, 'pūrva_pada', 'hṛdaya') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'lekhayadaṇlāsa') and _eq(c, 'substitute', 'hṛt')

def sutra_6_3_51(c) -> bool:
    return bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'śokashyañroga')

def sutra_6_3_52(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, 'pūrva_pada', 'pāda') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'ājyātigopahata') and _eq(c, 'substitute', 'pad')

def sutra_6_3_53(c) -> bool:
    return _eq(c, 'excludes', 'tadartha') and _eq(c, 'operation', 'substitution') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'yati') and _eq(c, 'substitute', 'pad')

def sutra_6_3_54(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'himakāṣihati')

def sutra_6_3_55(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'ṛc') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'śa')

def sutra_6_3_56(c) -> bool:
    return bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'ghoṣamiśraśabda')

def sutra_6_3_57(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, 'pūrva_pada', 'udaka') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'saṃjñā') and _eq(c, 'substitute', 'udaḥ')

def sutra_6_3_58(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'peṣaṃvāsavāhanadhi')

def sutra_6_3_59(c) -> bool:
    return _eq(c, 'condition', 'ekahalādi') and bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'pūrayitavya')

def sutra_6_3_60(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'manthaudanasaktubinduvajrabhārahāravīvadhagāha')

def sutra_6_3_61(c) -> bool:
    return _eq(c, 'authority', 'gālava') and _eq(c, 'condition', 'ik') and _eq(c, 'operation', 'hrasva') and _eq(c, "range", "6.3") and _eq(c, 'suffix', 'aṅya')

def sutra_6_3_62(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'eka') and _eq(c, 'suffix_class', 'taddhita')

def sutra_6_3_63(c) -> bool:
    return _eq(c, 'domain', 'saṃjñā_chandas') and _eq(c, 'operation', 'bahulam') and _eq(c, "range", "6.3") and _eq(c, 'suffix_group', 'ṅyāpa')

def sutra_6_3_64(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'suffix', 'tva')

def sutra_6_3_65(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'citatūlabhāri') and _eq(c, 'stem_group', 'iṣṭakeśīkāmāla')

def sutra_6_3_66(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada_type', 'anavyaya') and _eq(c, "range", "6.3") and _eq(c, 'suffix', 'khi')

def sutra_6_3_67(c) -> bool:
    return _eq(c, 'augment', 'um') and _eq(c, 'operation', 'augment') and _eq(c, 'pūrva_pada_type', 'arurdviṣadajanta') and _eq(c, "range", "6.3")

def sutra_6_3_68(c) -> bool:
    return _eq(c, 'augment', 'am') and _eq(c, 'condition', 'ekāca') and _eq(c, 'condition_ic', 'ic') and _eq(c, 'operation', 'augment') and _eq(c, "range", "6.3") and _eq(c, 'rule', 'pratyayavat')

def sutra_6_3_69(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'vācaṃyamapuraṃdara')

def sutra_6_3_70(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'satyāgada') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'kāra')

def sutra_6_3_71(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'śyenatila') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'pāta') and _eq(c, 'suffix', 'ña')

def sutra_6_3_72(c) -> bool:
    return bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'rātri') and _eq(c, "range", "6.3") and _eq(c, 'suffix_class', 'kṛt')

def sutra_6_3_73(c) -> bool:
    return _eq(c, 'operation', 'na_lopa') and _eq(c, 'pūrva_pada', 'nañ') and _eq(c, "range", "6.3")

def sutra_6_3_74(c) -> bool:
    return _eq(c, 'augment', 'nuṭ') and _eq(c, 'following', 'aci') and _eq(c, 'operation', 'augment') and _eq(c, 'pūrva_pada', 'tasmāt') and _eq(c, "range", "6.3")

def sutra_6_3_75(c) -> bool:
    return _eq(c, 'operation', 'prakṛti') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'nabhrānnapānnavēdānāsatyānamucinakulanakhanapuṃsakanakṣatranakranāka')

def sutra_6_3_76(c) -> bool:
    return _eq(c, 'augment', 'āduk') and _eq(c, 'operation', 'augment') and _eq(c, 'pūrva_pada', 'eka') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'ekādi')

def sutra_6_3_77(c) -> bool:
    return bool(c.get('is_optional')) is True and _eq(c, 'operation', 'substitution') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'aprāṇi') and _eq(c, 'substitute', 'naga')

def sutra_6_3_78(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, 'pūrva_pada', 'saha') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'saṃjñā') and _eq(c, 'substitute', 'saḥ')

def sutra_6_3_79(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'granthāntādhika')

def sutra_6_3_80(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'anupākhyā') and _eq(c, 'vibhakti_source', 'dvitīya')

def sutra_6_3_81(c) -> bool:
    return _eq(c, 'compound_type', 'avyayībhāva') and _eq(c, 'excludes', 'kāla') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3")

def sutra_6_3_82(c) -> bool:
    return bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'scope', 'upasarjana')

def sutra_6_3_83(c) -> bool:
    return _eq(c, 'operation', 'prakṛti') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'āśis') and _eq(c, 'stem_group', 'agovatsahala')

def sutra_6_3_84(c) -> bool:
    return bool(c.get('is_chandas')) is True and _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'samāna') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'amūrdhaprabhṛtyudarka')

def sutra_6_3_85(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'jyotirjanapadarātrinābhināmagotrūpasthānavarṇavayovacanabandhu')

def sutra_6_3_86(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'caraṇa') and _eq(c, 'suffix_class', 'brahmacārin')

def sutra_6_3_87(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'tīrtha') and _eq(c, 'substitute', 'ye')

def sutra_6_3_88(c) -> bool:
    return bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'udara')

def sutra_6_3_89(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'dṛgdṛśavatu')

def sutra_6_3_90(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'idaṅkima') and _eq(c, 'substitute', 'īś')

def sutra_6_3_91(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, 'pūrva_pada_type', 'sarvanāman') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'ā')

def sutra_6_3_92(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, 'pūrva_pada_final', 'ṭa') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'viṣvagdeva') and _eq(c, 'suffix', 'va') and _eq(c, 'suffix_pair', 'añca')

def sutra_6_3_93(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, 'pūrva_pada', 'sama') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'sami')

def sutra_6_3_94(c) -> bool:
    return _eq(c, 'operation', 'no_lopa') and _eq(c, 'pūrva_pada', 'tiras') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'tiri')

def sutra_6_3_95(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, 'pūrva_pada', 'saha') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'sadhri')

def sutra_6_3_96(c) -> bool:
    return bool(c.get('is_chandas')) is True and _eq(c, 'operation', 'substitution') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'mādastha') and _eq(c, 'substitute', 'sadh')

def sutra_6_3_97(c) -> bool:
    return _eq(c, 'augment', 'īt') and _eq(c, 'operation', 'augment') and _eq(c, 'pūrva_pada', 'ap') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'dvyantarupasarga')

def sutra_6_3_98(c) -> bool:
    return _eq(c, 'augment', 'ū') and _eq(c, 'operation', 'augment') and _eq(c, 'pūrva_pada', 'ano') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'deśa')

def sutra_6_3_99(c) -> bool:
    return _eq(c, 'augment', 'uk') and _eq(c, 'excludes', 'ṣaṣṭhītrtiyāstha') and _eq(c, 'operation', 'augment') and _eq(c, 'pūrva_pada', 'anya') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'āśīrāśāsthāsthānotsukotikārakarāgaccha')

def sutra_6_3_100(c) -> bool:
    return bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'artha')

def sutra_6_3_101(c) -> bool:
    return _eq(c, 'compound_type', 'tatpuruṣa') and _eq(c, 'following', 'aci') and _eq(c, 'operation', 'substitution') and _eq(c, 'pūrva_pada', 'ko') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'kat')

def sutra_6_3_102(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'rathavada')

def sutra_6_3_103(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'tṛṇa') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'jāti')

def sutra_6_3_104(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'pathyakṣa') and _eq(c, 'substitute', 'kā')

def sutra_6_3_105(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'īṣadartha')

def sutra_6_3_106(c) -> bool:
    return bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'puruṣa')

def sutra_6_3_107(c) -> bool:
    return _eq(c, 'operation', 'substitution') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'uṣṇa') and _eq(c, 'substitute', 'kavam')

def sutra_6_3_108(c) -> bool:
    return bool(c.get('is_chandas')) is True and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'pathi')

def sutra_6_3_109(c) -> bool:
    return _eq(c, "range", "6.3") and _eq(c, 'rule', 'yathopadiṣṭa') and _eq(c, 'stem_group', 'pṛṣodarādi')

def sutra_6_3_110(c) -> bool:
    return _eq(c, 'condition', 'saṃkhyāvisāyapūrva') and bool(c.get('is_optional')) is True and _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'ahan') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'ahan') and _eq(c, 'suffix', 'ṅau')

def sutra_6_3_111(c) -> bool:
    return _eq(c, 'condition', 'ḍhralopa') and _eq(c, 'condition_aṇ', 'aṇ') and _eq(c, 'operation', 'dīrgha') and _eq(c, "range", "6.3") and _eq(c, 'scope', 'pūrva')

def sutra_6_3_112(c) -> bool:
    return _eq(c, 'augment', 'ot') and _eq(c, 'condition', 'avarna') and _eq(c, 'operation', 'augment') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'sahivaha')

def sutra_6_3_113(c) -> bool:
    return _eq(c, 'authority', 'sāḍhya') and _eq(c, 'domain', 'nigama') and _eq(c, 'operation', 'substitution') and _eq(c, "range", "6.3") and _eq(c, 'substitute', 'sāḍhā')

def sutra_6_3_114(c) -> bool:
    return _eq(c, 'domain', 'saṃhitā') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3")

def sutra_6_3_115(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'lakṣaṇa') and _eq(c, 'pūrva_pada_type', 'aviṣṭāṣṭapañcamaṇibhinnachinnachidrasruvasvastika') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'karṇa')

def sutra_6_3_116(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'nahivṛtivṛṣivyadhirucisahitani') and _eq(c, 'suffix', 'kvau')

def sutra_6_3_117(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'saṃjñā') and _eq(c, 'stem_group', 'koṭarakiṃśulakādi')

def sutra_6_3_118(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'vala')

def sutra_6_3_119(c) -> bool:
    return _eq(c, 'condition', 'bahvaca') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'anajirādi') and _eq(c, 'suffix', 'mat')

def sutra_6_3_120(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'śarādi')

def sutra_6_3_121(c) -> bool:
    return _eq(c, 'condition', 'ik') and _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'apīla') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'vaha')

def sutra_6_3_122(c) -> bool:
    return _eq(c, 'excludes', 'manuṣya') and _eq(c, 'operation', 'bahulam') and _eq(c, 'pūrva_pada_type', 'upasarga') and _eq(c, "range", "6.3") and _eq(c, 'suffix', 'gha')

def sutra_6_3_123(c) -> bool:
    return _eq(c, 'condition', 'ik') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'kāśa')

def sutra_6_3_124(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'da') and _eq(c, "range", "6.3") and _eq(c, 'suffix', 'ti')

def sutra_6_3_125(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'aṣṭan') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'saṃjñā')

def sutra_6_3_126(c) -> bool:
    return bool(c.get('is_chandas')) is True and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3")

def sutra_6_3_127(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'citi') and _eq(c, "range", "6.3") and _eq(c, 'suffix', 'kap')

def sutra_6_3_128(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'viśva') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'vasurāṭ')

def sutra_6_3_129(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'nara') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'saṃjñā')

def sutra_6_3_130(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'mitra') and _eq(c, "range", "6.3") and _eq(c, 'semantic', 'ṛṣi')

def sutra_6_3_131(c) -> bool:
    return _eq(c, 'domain', 'mantra') and _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'somāśvendriyaviśvadevya') and _eq(c, "range", "6.3") and _eq(c, 'suffix', 'mat')

def sutra_6_3_132(c) -> bool:
    return _eq(c, 'excludes', 'prathama') and _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada', 'oṣadhi') and _eq(c, "range", "6.3") and _eq(c, 'scope', 'vibhakti')

def sutra_6_3_133(c) -> bool:
    return _eq(c, 'domain', 'ṛc') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'stem_group', 'tunughamakṣutaṅkutroruṣya')

def sutra_6_3_134(c) -> bool:
    return _eq(c, 'condition', 'ik') and _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'suffix', 'su')

def sutra_6_3_135(c) -> bool:
    return _eq(c, 'condition', 'dvyaca') and _eq(c, 'following', 'tiṅ') and _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada_final', 'a') and _eq(c, "range", "6.3")

def sutra_6_3_136(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, 'pūrva_pada_type', 'nipāta') and _eq(c, "range", "6.3")

def sutra_6_3_137(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'rule', 'dṛśyate') and _eq(c, 'scope', 'anya')

def sutra_6_3_138(c) -> bool:
    return _eq(c, 'operation', 'aluk') and _eq(c, "range", "6.3") and _eq(c, 'suffix', 'cau')

def sutra_6_3_139(c) -> bool:
    return _eq(c, 'operation', 'samprasāraṇa') and _eq(c, "range", "6.3")

def _fx_pair(sid: str, pos: dict, neg: dict | None = None):
    if neg is None:
        neg = dict(pos)
        k = next(iter(pos))
        v = pos[k]
        if k == "range":
            neg[k] = "6.2"
        elif isinstance(v, bool):
            neg[k] = not v
        elif isinstance(v, str):
            neg[k] = "other"
    return (pos, neg)

FIXTURES: dict[str, tuple[dict, dict]] = {
    "6.3.1": _fx_pair("6.3.1", {'range': '6.3', 'uttarapada_rule': 'adhikāra'}, {'range': '6.2', 'uttarapada_rule': 'adhikāra'}),
    "6.3.2": _fx_pair("6.3.2", {'range': '6.3', 'operation': 'aluk', 'vibhakti_source': 'pañcama', 'stem_group': 'stokādi'}),
    "6.3.3": _fx_pair("6.3.3", {'range': '6.3', 'operation': 'aluk', 'stem_group': 'ojassahombastamasa', 'vibhakti_source': 'trtiya'}),
    "6.3.4": _fx_pair("6.3.4", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'manas', 'semantic': 'saṃjñā'}),
    "6.3.5": _fx_pair("6.3.5", {'range': '6.3', 'operation': 'aluk', 'semantic': 'ājñāyin'}),
    "6.3.6": _fx_pair("6.3.6", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'ātman', 'semantic': 'pūraṇa'}),
    "6.3.7": _fx_pair("6.3.7", {'range': '6.3', 'operation': 'aluk', 'semantic': 'vaiyākaraṇākhya', 'vibhakti_source': 'caturthī'}),
    "6.3.8": _fx_pair("6.3.8", {'range': '6.3', 'operation': 'aluk', 'anuvritti': 'para'}),
    "6.3.9": _fx_pair("6.3.9", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada_type': 'halanta', 'vibhakti_source': 'saptamī', 'semantic': 'saṃjñā'}),
    "6.3.10": _fx_pair("6.3.10", {'range': '6.3', 'operation': 'aluk', 'semantic': 'kāranāman', 'dialect': 'prācya', 'position': 'halādi'}),
    "6.3.11": _fx_pair("6.3.11", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'madhya', 'semantic': 'guru'}),
    "6.3.12": _fx_pair("6.3.12", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'amūrdhamastaka', 'pūrva_pada_type': 'svāṅga', 'semantic': 'akāma'}),
    "6.3.13": _fx_pair("6.3.13", {'range': '6.3', 'operation': 'aluk', 'semantic': 'bandha', 'is_optional': True}),
    "6.3.14": _fx_pair("6.3.14", {'range': '6.3', 'operation': 'bahulam', 'compound_type': 'tatpuruṣa', 'suffix_class': 'kṛt'}),
    "6.3.15": _fx_pair("6.3.15", {'range': '6.3', 'operation': 'aluk', 'stem_group': 'prāvṛṭśaratkāladiva', 'semantic': 'je'}),
    "6.3.16": _fx_pair("6.3.16", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'varṣakṣaraśaravara', 'is_optional': True}),
    "6.3.17": _fx_pair("6.3.17", {'range': '6.3', 'operation': 'aluk', 'semantic': 'ghakālatana', 'pūrva_pada_type': 'kālanāman'}),
    "6.3.18": _fx_pair("6.3.18", {'range': '6.3', 'operation': 'aluk', 'semantic': 'śayavāsavāsi', 'excludes': 'kāla'}),
    "6.3.19": _fx_pair("6.3.19", {'range': '6.3', 'rule_blocked': True, 'semantic': 'insiddhabadhnāti'}, {'range': '6.3', 'rule_blocked': False, 'semantic': 'insiddhabadhnāti'}),
    "6.3.20": _fx_pair("6.3.20", {'range': '6.3', 'operation': 'aluk', 'semantic': 'stha', 'domain': 'bhāṣā'}),
    "6.3.21": _fx_pair("6.3.21", {'range': '6.3', 'operation': 'aluk', 'vibhakti_source': 'ṣaṣṭhī', 'semantic': 'ākrośa'}),
    "6.3.22": _fx_pair("6.3.22", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'putra', 'is_optional': True}),
    "6.3.23": _fx_pair("6.3.23", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada_final': 'ṛ', 'relation': 'vidyāyoni'}),
    "6.3.24": _fx_pair("6.3.24", {'range': '6.3', 'operation': 'aluk', 'stem_group': 'svasṛpatya', 'is_optional': True}),
    "6.3.25": _fx_pair("6.3.25", {'range': '6.3', 'operation': 'augment', 'augment': 'ān', 'pūrva_pada_final': 'ṛ', 'compound_type': 'dvandva'}),
    "6.3.26": _fx_pair("6.3.26", {'range': '6.3', 'operation': 'aluk', 'compound_type': 'devatā_dvandva'}),
    "6.3.27": _fx_pair("6.3.27", {'range': '6.3', 'operation': 'augment', 'augment': 'īt', 'pūrva_pada': 'agni', 'stem_group': 'somavaruna'}),
    "6.3.28": _fx_pair("6.3.28", {'range': '6.3', 'operation': 'vṛddhi', 'augment': 'it'}),
    "6.3.29": _fx_pair("6.3.29", {'range': '6.3', 'operation': 'substitution', 'pūrva_pada': 'div', 'substitute': 'dyāv'}),
    "6.3.30": _fx_pair("6.3.30", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'divas', 'semantic': 'pṛthivī'}),
    "6.3.31": _fx_pair("6.3.31", {'range': '6.3', 'operation': 'substitution', 'substitute': 'uṣās', 'pūrva_pada': 'uṣas'}),
    "6.3.32": _fx_pair("6.3.32", {'range': '6.3', 'operation': 'substitution', 'substitute': 'mātarapitara', 'direction': 'udīc'}),
    "6.3.33": _fx_pair("6.3.33", {'range': '6.3', 'operation': 'substitution', 'substitute': 'pitarāmātara', 'is_chandas': True}),
    "6.3.34": _fx_pair("6.3.34", {'range': '6.3', 'operation': 'aluk', 'gender': 'strī', 'relation': 'samānādhikaraṇa', 'semantic': 'apūraṇīpriyādi'}),
    "6.3.35": _fx_pair("6.3.35", {'range': '6.3', 'operation': 'aluk', 'suffix_group': 'tasilādi', 'pūrva_pada_type': 'kṛtvasuc'}),
    "6.3.36": _fx_pair("6.3.36", {'range': '6.3', 'operation': 'aluk', 'stem_group': 'kyaṅmānin'}),
    "6.3.37": _fx_pair("6.3.37", {'range': '6.3', 'rule_blocked': True, 'excludes': 'kopadhā'}, {'range': '6.3', 'rule_blocked': False, 'excludes': 'kopadhā'}),
    "6.3.38": _fx_pair("6.3.38", {'range': '6.3', 'operation': 'aluk', 'semantic': 'saṃjñāpūraṇya'}),
    "6.3.39": _fx_pair("6.3.39", {'range': '6.3', 'operation': 'aluk', 'condition': 'vṛddhinimitta', 'suffix_class': 'taddhita', 'excludes': 'raktavikāra'}),
    "6.3.40": _fx_pair("6.3.40", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada_type': 'svāṅga', 'pūrva_pada_final': 'ī', 'excludes': 'mānin'}),
    "6.3.41": _fx_pair("6.3.41", {'range': '6.3', 'operation': 'aluk', 'anuvritti': 'jāti'}),
    "6.3.42": _fx_pair("6.3.42", {'range': '6.3', 'operation': 'aluk', 'compound_type': 'karmadhārayajātīyadeśīya'}),
    "6.3.43": _fx_pair("6.3.43", {'range': '6.3', 'operation': 'hrasva', 'semantic': 'gharūpakalpacelaḍbruvagotramatahata', 'suffix': 'ṅya', 'condition': 'anekāca'}),
    "6.3.44": _fx_pair("6.3.44", {'range': '6.3', 'operation': 'aluk', 'condition': 'nadyā', 'anuvritti': 'śeṣa', 'is_optional': True}),
    "6.3.45": _fx_pair("6.3.45", {'range': '6.3', 'operation': 'aluk', 'marker': 'ugit'}),
    "6.3.46": _fx_pair("6.3.46", {'range': '6.3', 'operation': 'augment', 'augment': 'ā', 'pūrva_pada': 'mahat', 'relation': 'samānādhikaraṇajātīya'}),
    "6.3.47": _fx_pair("6.3.47", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'dvyashṭan', 'semantic': 'saṃkhyā', 'excludes': 'bahuvrīhyashīti'}),
    "6.3.48": _fx_pair("6.3.48", {'range': '6.3', 'operation': 'substitution', 'pūrva_pada': 'tri', 'substitute': 'traya'}),
    "6.3.49": _fx_pair("6.3.49", {'range': '6.3', 'operation': 'aluk', 'stem_group': 'catvāriṃśatprabhṛti', 'scope': 'sarva', 'is_optional': True}),
    "6.3.50": _fx_pair("6.3.50", {'range': '6.3', 'operation': 'substitution', 'pūrva_pada': 'hṛdaya', 'substitute': 'hṛt', 'semantic': 'lekhayadaṇlāsa'}),
    "6.3.51": _fx_pair("6.3.51", {'range': '6.3', 'operation': 'aluk', 'semantic': 'śokashyañroga', 'is_optional': True}),
    "6.3.52": _fx_pair("6.3.52", {'range': '6.3', 'operation': 'substitution', 'pūrva_pada': 'pāda', 'substitute': 'pad', 'semantic': 'ājyātigopahata'}),
    "6.3.53": _fx_pair("6.3.53", {'range': '6.3', 'operation': 'substitution', 'substitute': 'pad', 'semantic': 'yati', 'excludes': 'tadartha'}),
    "6.3.54": _fx_pair("6.3.54", {'range': '6.3', 'operation': 'aluk', 'semantic': 'himakāṣihati'}),
    "6.3.55": _fx_pair("6.3.55", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'ṛc', 'semantic': 'śa'}),
    "6.3.56": _fx_pair("6.3.56", {'range': '6.3', 'operation': 'aluk', 'semantic': 'ghoṣamiśraśabda', 'is_optional': True}),
    "6.3.57": _fx_pair("6.3.57", {'range': '6.3', 'operation': 'substitution', 'pūrva_pada': 'udaka', 'substitute': 'udaḥ', 'semantic': 'saṃjñā'}),
    "6.3.58": _fx_pair("6.3.58", {'range': '6.3', 'operation': 'aluk', 'semantic': 'peṣaṃvāsavāhanadhi'}),
    "6.3.59": _fx_pair("6.3.59", {'range': '6.3', 'operation': 'aluk', 'condition': 'ekahalādi', 'semantic': 'pūrayitavya', 'is_optional': True}),
    "6.3.60": _fx_pair("6.3.60", {'range': '6.3', 'operation': 'aluk', 'semantic': 'manthaudanasaktubinduvajrabhārahāravīvadhagāha'}),
    "6.3.61": _fx_pair("6.3.61", {'range': '6.3', 'operation': 'hrasva', 'condition': 'ik', 'suffix': 'aṅya', 'authority': 'gālava'}),
    "6.3.62": _fx_pair("6.3.62", {'range': '6.3', 'operation': 'substitution', 'substitute': 'eka', 'suffix_class': 'taddhita'}),
    "6.3.63": _fx_pair("6.3.63", {'range': '6.3', 'operation': 'bahulam', 'suffix_group': 'ṅyāpa', 'domain': 'saṃjñā_chandas'}),
    "6.3.64": _fx_pair("6.3.64", {'range': '6.3', 'operation': 'aluk', 'suffix': 'tva'}),
    "6.3.65": _fx_pair("6.3.65", {'range': '6.3', 'operation': 'aluk', 'stem_group': 'iṣṭakeśīkāmāla', 'semantic': 'citatūlabhāri'}),
    "6.3.66": _fx_pair("6.3.66", {'range': '6.3', 'operation': 'aluk', 'suffix': 'khi', 'pūrva_pada_type': 'anavyaya'}),
    "6.3.67": _fx_pair("6.3.67", {'range': '6.3', 'operation': 'augment', 'augment': 'um', 'pūrva_pada_type': 'arurdviṣadajanta'}),
    "6.3.68": _fx_pair("6.3.68", {'range': '6.3', 'operation': 'augment', 'augment': 'am', 'condition': 'ekāca', 'condition_ic': 'ic', 'rule': 'pratyayavat'}),
    "6.3.69": _fx_pair("6.3.69", {'range': '6.3', 'operation': 'aluk', 'stem_group': 'vācaṃyamapuraṃdara'}),
    "6.3.70": _fx_pair("6.3.70", {'range': '6.3', 'operation': 'aluk', 'semantic': 'kāra', 'pūrva_pada': 'satyāgada'}),
    "6.3.71": _fx_pair("6.3.71", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'śyenatila', 'semantic': 'pāta', 'suffix': 'ña'}),
    "6.3.72": _fx_pair("6.3.72", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'rātri', 'suffix_class': 'kṛt', 'is_optional': True}),
    "6.3.73": _fx_pair("6.3.73", {'range': '6.3', 'operation': 'na_lopa', 'pūrva_pada': 'nañ'}),
    "6.3.74": _fx_pair("6.3.74", {'range': '6.3', 'operation': 'augment', 'augment': 'nuṭ', 'pūrva_pada': 'tasmāt', 'following': 'aci'}),
    "6.3.75": _fx_pair("6.3.75", {'range': '6.3', 'operation': 'prakṛti', 'semantic': 'nabhrānnapānnavēdānāsatyānamucinakulanakhanapuṃsakanakṣatranakranāka'}),
    "6.3.76": _fx_pair("6.3.76", {'range': '6.3', 'operation': 'augment', 'substitute': 'ekādi', 'pūrva_pada': 'eka', 'augment': 'āduk'}),
    "6.3.77": _fx_pair("6.3.77", {'range': '6.3', 'operation': 'substitution', 'substitute': 'naga', 'semantic': 'aprāṇi', 'is_optional': True}),
    "6.3.78": _fx_pair("6.3.78", {'range': '6.3', 'operation': 'substitution', 'pūrva_pada': 'saha', 'substitute': 'saḥ', 'semantic': 'saṃjñā'}),
    "6.3.79": _fx_pair("6.3.79", {'range': '6.3', 'operation': 'aluk', 'semantic': 'granthāntādhika'}),
    "6.3.80": _fx_pair("6.3.80", {'range': '6.3', 'operation': 'aluk', 'vibhakti_source': 'dvitīya', 'semantic': 'anupākhyā'}),
    "6.3.81": _fx_pair("6.3.81", {'range': '6.3', 'operation': 'aluk', 'compound_type': 'avyayībhāva', 'excludes': 'kāla'}),
    "6.3.82": _fx_pair("6.3.82", {'range': '6.3', 'operation': 'aluk', 'scope': 'upasarjana', 'is_optional': True}),
    "6.3.83": _fx_pair("6.3.83", {'range': '6.3', 'operation': 'prakṛti', 'semantic': 'āśis', 'stem_group': 'agovatsahala'}),
    "6.3.84": _fx_pair("6.3.84", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'samāna', 'is_chandas': True, 'semantic': 'amūrdhaprabhṛtyudarka'}),
    "6.3.85": _fx_pair("6.3.85", {'range': '6.3', 'operation': 'aluk', 'semantic': 'jyotirjanapadarātrinābhināmagotrūpasthānavarṇavayovacanabandhu'}),
    "6.3.86": _fx_pair("6.3.86", {'range': '6.3', 'operation': 'aluk', 'semantic': 'caraṇa', 'suffix_class': 'brahmacārin'}),
    "6.3.87": _fx_pair("6.3.87", {'range': '6.3', 'operation': 'substitution', 'semantic': 'tīrtha', 'substitute': 'ye'}),
    "6.3.88": _fx_pair("6.3.88", {'range': '6.3', 'operation': 'aluk', 'semantic': 'udara', 'is_optional': True}),
    "6.3.89": _fx_pair("6.3.89", {'range': '6.3', 'operation': 'aluk', 'stem_group': 'dṛgdṛśavatu'}),
    "6.3.90": _fx_pair("6.3.90", {'range': '6.3', 'operation': 'substitution', 'stem_group': 'idaṅkima', 'substitute': 'īś'}),
    "6.3.91": _fx_pair("6.3.91", {'range': '6.3', 'operation': 'substitution', 'substitute': 'ā', 'pūrva_pada_type': 'sarvanāman'}),
    "6.3.92": _fx_pair("6.3.92", {'range': '6.3', 'operation': 'substitution', 'stem_group': 'viṣvagdeva', 'pūrva_pada_final': 'ṭa', 'suffix_pair': 'añca', 'suffix': 'va'}),
    "6.3.93": _fx_pair("6.3.93", {'range': '6.3', 'operation': 'substitution', 'pūrva_pada': 'sama', 'substitute': 'sami'}),
    "6.3.94": _fx_pair("6.3.94", {'range': '6.3', 'operation': 'no_lopa', 'pūrva_pada': 'tiras', 'substitute': 'tiri'}),
    "6.3.95": _fx_pair("6.3.95", {'range': '6.3', 'operation': 'substitution', 'pūrva_pada': 'saha', 'substitute': 'sadhri'}),
    "6.3.96": _fx_pair("6.3.96", {'range': '6.3', 'operation': 'substitution', 'substitute': 'sadh', 'stem_group': 'mādastha', 'is_chandas': True}),
    "6.3.97": _fx_pair("6.3.97", {'range': '6.3', 'operation': 'augment', 'augment': 'īt', 'stem_group': 'dvyantarupasarga', 'pūrva_pada': 'ap'}),
    "6.3.98": _fx_pair("6.3.98", {'range': '6.3', 'operation': 'augment', 'augment': 'ū', 'pūrva_pada': 'ano', 'semantic': 'deśa'}),
    "6.3.99": _fx_pair("6.3.99", {'range': '6.3', 'operation': 'augment', 'augment': 'uk', 'excludes': 'ṣaṣṭhītrtiyāstha', 'pūrva_pada': 'anya', 'semantic': 'āśīrāśāsthāsthānotsukotikārakarāgaccha'}),
    "6.3.100": _fx_pair("6.3.100", {'range': '6.3', 'operation': 'aluk', 'semantic': 'artha', 'is_optional': True}),
    "6.3.101": _fx_pair("6.3.101", {'range': '6.3', 'operation': 'substitution', 'pūrva_pada': 'ko', 'substitute': 'kat', 'compound_type': 'tatpuruṣa', 'following': 'aci'}),
    "6.3.102": _fx_pair("6.3.102", {'range': '6.3', 'operation': 'aluk', 'stem_group': 'rathavada'}),
    "6.3.103": _fx_pair("6.3.103", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'tṛṇa', 'semantic': 'jāti'}),
    "6.3.104": _fx_pair("6.3.104", {'range': '6.3', 'operation': 'substitution', 'substitute': 'kā', 'semantic': 'pathyakṣa'}),
    "6.3.105": _fx_pair("6.3.105", {'range': '6.3', 'operation': 'aluk', 'semantic': 'īṣadartha'}),
    "6.3.106": _fx_pair("6.3.106", {'range': '6.3', 'operation': 'aluk', 'semantic': 'puruṣa', 'is_optional': True}),
    "6.3.107": _fx_pair("6.3.107", {'range': '6.3', 'operation': 'substitution', 'substitute': 'kavam', 'semantic': 'uṣṇa'}),
    "6.3.108": _fx_pair("6.3.108", {'range': '6.3', 'operation': 'aluk', 'semantic': 'pathi', 'is_chandas': True}),
    "6.3.109": _fx_pair("6.3.109", {'range': '6.3', 'rule': 'yathopadiṣṭa', 'stem_group': 'pṛṣodarādi'}),
    "6.3.110": _fx_pair("6.3.110", {'range': '6.3', 'operation': 'aluk', 'condition': 'saṃkhyāvisāyapūrva', 'pūrva_pada': 'ahan', 'substitute': 'ahan', 'suffix': 'ṅau', 'is_optional': True}),
    "6.3.111": _fx_pair("6.3.111", {'range': '6.3', 'operation': 'dīrgha', 'condition': 'ḍhralopa', 'scope': 'pūrva', 'condition_aṇ': 'aṇ'}),
    "6.3.112": _fx_pair("6.3.112", {'range': '6.3', 'operation': 'augment', 'augment': 'ot', 'stem_group': 'sahivaha', 'condition': 'avarna'}),
    "6.3.113": _fx_pair("6.3.113", {'range': '6.3', 'operation': 'substitution', 'substitute': 'sāḍhā', 'domain': 'nigama', 'authority': 'sāḍhya'}),
    "6.3.114": _fx_pair("6.3.114", {'range': '6.3', 'operation': 'aluk', 'domain': 'saṃhitā'}),
    "6.3.115": _fx_pair("6.3.115", {'range': '6.3', 'operation': 'aluk', 'semantic': 'karṇa', 'pūrva_pada': 'lakṣaṇa', 'pūrva_pada_type': 'aviṣṭāṣṭapañcamaṇibhinnachinnachidrasruvasvastika'}),
    "6.3.116": _fx_pair("6.3.116", {'range': '6.3', 'operation': 'aluk', 'semantic': 'nahivṛtivṛṣivyadhirucisahitani', 'suffix': 'kvau'}),
    "6.3.117": _fx_pair("6.3.117", {'range': '6.3', 'operation': 'aluk', 'stem_group': 'koṭarakiṃśulakādi', 'semantic': 'saṃjñā'}),
    "6.3.118": _fx_pair("6.3.118", {'range': '6.3', 'operation': 'aluk', 'semantic': 'vala'}),
    "6.3.119": _fx_pair("6.3.119", {'range': '6.3', 'operation': 'aluk', 'suffix': 'mat', 'condition': 'bahvaca', 'stem_group': 'anajirādi'}),
    "6.3.120": _fx_pair("6.3.120", {'range': '6.3', 'operation': 'aluk', 'stem_group': 'śarādi'}),
    "6.3.121": _fx_pair("6.3.121", {'range': '6.3', 'operation': 'aluk', 'condition': 'ik', 'semantic': 'vaha', 'pūrva_pada': 'apīla'}),
    "6.3.122": _fx_pair("6.3.122", {'range': '6.3', 'operation': 'bahulam', 'pūrva_pada_type': 'upasarga', 'suffix': 'gha', 'excludes': 'manuṣya'}),
    "6.3.123": _fx_pair("6.3.123", {'range': '6.3', 'operation': 'aluk', 'condition': 'ik', 'semantic': 'kāśa'}),
    "6.3.124": _fx_pair("6.3.124", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'da', 'suffix': 'ti'}),
    "6.3.125": _fx_pair("6.3.125", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'aṣṭan', 'semantic': 'saṃjñā'}),
    "6.3.126": _fx_pair("6.3.126", {'range': '6.3', 'operation': 'aluk', 'is_chandas': True}),
    "6.3.127": _fx_pair("6.3.127", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'citi', 'suffix': 'kap'}),
    "6.3.128": _fx_pair("6.3.128", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'viśva', 'stem_group': 'vasurāṭ'}),
    "6.3.129": _fx_pair("6.3.129", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'nara', 'semantic': 'saṃjñā'}),
    "6.3.130": _fx_pair("6.3.130", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'mitra', 'semantic': 'ṛṣi'}),
    "6.3.131": _fx_pair("6.3.131", {'range': '6.3', 'operation': 'aluk', 'domain': 'mantra', 'pūrva_pada': 'somāśvendriyaviśvadevya', 'suffix': 'mat'}),
    "6.3.132": _fx_pair("6.3.132", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada': 'oṣadhi', 'scope': 'vibhakti', 'excludes': 'prathama'}),
    "6.3.133": _fx_pair("6.3.133", {'range': '6.3', 'operation': 'aluk', 'domain': 'ṛc', 'stem_group': 'tunughamakṣutaṅkutroruṣya'}),
    "6.3.134": _fx_pair("6.3.134", {'range': '6.3', 'operation': 'aluk', 'condition': 'ik', 'suffix': 'su'}),
    "6.3.135": _fx_pair("6.3.135", {'range': '6.3', 'operation': 'aluk', 'condition': 'dvyaca', 'pūrva_pada_final': 'a', 'following': 'tiṅ'}),
    "6.3.136": _fx_pair("6.3.136", {'range': '6.3', 'operation': 'aluk', 'pūrva_pada_type': 'nipāta'}),
    "6.3.137": _fx_pair("6.3.137", {'range': '6.3', 'operation': 'aluk', 'scope': 'anya', 'rule': 'dṛśyate'}),
    "6.3.138": _fx_pair("6.3.138", {'range': '6.3', 'operation': 'aluk', 'suffix': 'cau'}),
    "6.3.139": _fx_pair("6.3.139", {'range': '6.3', 'operation': 'samprasāraṇa'}),
}

META: dict[str, SutraMeta] = {
    "6.3.1": SutraMeta(_PARIBHASHA, "अलुगुत्तरपदे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.2": SutraMeta(_VIDHI, "पञ्चम्याः स्तोकादिभ्यः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.3": SutraMeta(_VIDHI, "ओजःसहोऽम्भस्तमसः तृतीयायाः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.4": SutraMeta(_VIDHI, "मनसः संज्ञायाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.5": SutraMeta(_VIDHI, "आज्ञायिनि च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.6": SutraMeta(_VIDHI, "आत्मनश्च पूरणे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.7": SutraMeta(_VIDHI, "वैयाकरणाख्यायां चतुर्थ्याः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.8": SutraMeta(_VIDHI, "परस्य च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.9": SutraMeta(_VIDHI, "हलदन्तात्‌ सप्तम्याः संज्ञायाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.10": SutraMeta(_VIDHI, "कारनाम्नि च प्राचां हलादौ ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.11": SutraMeta(_VIDHI, "मध्याद्गुरौ ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.12": SutraMeta(_VIDHI, "अमूर्धमस्तकात्‌ स्वाङ्गादकामे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.13": SutraMeta(_VIBHASHA, "बन्धे च विभाषा ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.14": SutraMeta(_PARIBHASHA, "तत्पुरुषे कृति बहुलम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.15": SutraMeta(_VIDHI, "प्रावृट्शरत्कालदिवां जे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.16": SutraMeta(_VIBHASHA, "विभाषा वर्षक्षरशरवरात्‌ ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.17": SutraMeta(_VIDHI, "घकालतनेषु कालनाम्नः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.18": SutraMeta(_VIDHI, "शयवासवासिषु अकालात्‌ ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.19": SutraMeta(_PRATISEDHA, "नेन्सिद्धबध्नातिषु ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.20": SutraMeta(_VIDHI, "स्थे च भाषायाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.21": SutraMeta(_VIDHI, "षष्ठ्या आक्रोशे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.22": SutraMeta(_VIBHASHA, "पुत्रेऽन्यतरस्याम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.23": SutraMeta(_VIDHI, "ऋतो विद्यायोनिसम्बन्धेभ्यः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.24": SutraMeta(_VIBHASHA, "विभाषा स्वसृपत्योः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.25": SutraMeta(_VIDHI, "आनङ् ऋतो द्वंद्वे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.26": SutraMeta(_VIDHI, "देवताद्वंद्वे च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.27": SutraMeta(_VIDHI, "ईदग्नेः सोमवरुणयोः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.28": SutraMeta(_VIDHI, "इद्वृद्धौ ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.29": SutraMeta(_VIDHI, "दिवो द्यावा ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.30": SutraMeta(_VIDHI, "दिवसश्च पृथिव्याम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.31": SutraMeta(_VIDHI, "उषासोषसः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.32": SutraMeta(_VIDHI, "मातरपितरावुदीचाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.33": SutraMeta(_VIDHI, "पितरामातरा च च्छन्दसि ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.34": SutraMeta(_VIDHI, "स्त्रियाः पुंवद्भाषितपुंस्कादनूङ् समानाधिकरणे स्त्रियामपूरणीप्रियाऽऽदिषु ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.35": SutraMeta(_VIDHI, "तसिलादिषु आकृत्वसुचः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.36": SutraMeta(_VIDHI, "क्यङ्मानिनोश्च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.37": SutraMeta(_PRATISEDHA, "न कोपधायाः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.38": SutraMeta(_VIDHI, "संज्ञापूरण्योश्च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.39": SutraMeta(_VIDHI, "वृद्धिनिमित्तस्य च तद्धितस्यारक्तविकारे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.40": SutraMeta(_VIDHI, "स्वाङ्गाच्चेतोऽमानिनि ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.41": SutraMeta(_VIDHI, "जातेश्च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.42": SutraMeta(_VIDHI, "पुंवत्‌ कर्मधारयजातीयदेशीयेषु ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.43": SutraMeta(_VIDHI, "घरूपकल्पचेलड्ब्रुवगोत्रमतहतेषु ङ्योऽनेकाचो ह्रस्वः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.44": SutraMeta(_VIBHASHA, "नद्याः शेषस्यान्यतरस्याम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.45": SutraMeta(_VIDHI, "उगितश्च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.46": SutraMeta(_VIDHI, "आन्महतः समानाधिकरणजातीययोः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.47": SutraMeta(_VIDHI, "द्व्यष्टनः संख्यायामबहुव्रीह्यशीत्योः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.48": SutraMeta(_VIDHI, "त्रेस्त्रयः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.49": SutraMeta(_VIBHASHA, "विभाषा चत्वारिंशत्प्रभृतौ सर्वेषाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.50": SutraMeta(_VIDHI, "हृदयस्य हृल्लेखयदण्लासेषु ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.51": SutraMeta(_VIBHASHA, "वा शोकष्यञ्रोगेषु ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.52": SutraMeta(_VIDHI, "पादस्य पदाज्यातिगोपहतेषु ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.53": SutraMeta(_VIDHI, "पद् यत्यतदर्थे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.54": SutraMeta(_VIDHI, "हिमकाषिहतिषु च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.55": SutraMeta(_VIDHI, "ऋचः शे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.56": SutraMeta(_VIBHASHA, "वा घोषमिश्रशब्देषु ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.57": SutraMeta(_VIDHI, "उदकस्योदः संज्ञायाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.58": SutraMeta(_VIDHI, "पेषंवासवाहनधिषु च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.59": SutraMeta(_VIBHASHA, "एकहलादौ पूरयितव्येऽन्यतरस्याम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.60": SutraMeta(_VIDHI, "मन्थौदनसक्तुबिन्दुवज्रभारहारवीवधगाहेषु च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.61": SutraMeta(_VIDHI, "इको ह्रस्वोऽङ्यो गालवस्य ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.62": SutraMeta(_VIDHI, "एक तद्धिते च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.63": SutraMeta(_PARIBHASHA, "ङ्यापोः संज्ञाछन्दसोर्बहुलम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.64": SutraMeta(_VIDHI, "त्वे च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.65": SutraMeta(_VIDHI, "इष्टकेषीकामालानां चिततूलभारिषु ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.66": SutraMeta(_VIDHI, "खित्यनव्ययस्य ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.67": SutraMeta(_VIDHI, "अरुर्द्विषदजन्तस्य मुम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.68": SutraMeta(_VIDHI, "इच एकाचोऽम्प्रत्ययवच्च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.69": SutraMeta(_VIDHI, "वाचंयमपुरंदरौ च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.70": SutraMeta(_VIDHI, "कारे सत्यागदस्य ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.71": SutraMeta(_VIDHI, "श्येनतिलस्य पाते ञे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.72": SutraMeta(_VIBHASHA, "रात्रेः कृति विभाषा ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.73": SutraMeta(_VIDHI, "नलोपो नञः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.74": SutraMeta(_VIDHI, "तस्मान्नुडचि ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.75": SutraMeta(_VIDHI, "नभ्राण्नपान्नवेदानासत्यानमुचिनकुलनखनपुंसकनक्षत्रनक्रनाकेषु प्रकृत्या ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.76": SutraMeta(_VIDHI, "एकादिश्चैकस्य चादुक् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.77": SutraMeta(_VIBHASHA, "नगोऽप्राणिष्वन्यतरस्याम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.78": SutraMeta(_VIDHI, "सहस्य सः संज्ञायाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.79": SutraMeta(_VIDHI, "ग्रन्थान्ताधिके च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.80": SutraMeta(_VIDHI, "द्वितीये चानुपाख्ये ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.81": SutraMeta(_VIDHI, "अव्ययीभावे चाकाले ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.82": SutraMeta(_VIBHASHA, "वोपसर्जनस्य ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.83": SutraMeta(_VIDHI, "प्रकृत्याऽऽशिष्यगोवत्सहलेषु ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.84": SutraMeta(_VIDHI, "समानस्य छन्दस्यमूर्धप्रभृत्युदर्केषु ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.85": SutraMeta(_VIDHI, "ज्योतिर्जनपदरात्रिनाभिनामगोत्ररूपस्थानवर्णवयोवचनबन्धुषु ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.86": SutraMeta(_VIDHI, "चरणे ब्रह्मचारिणि ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.87": SutraMeta(_VIDHI, "तीर्थे ये ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.88": SutraMeta(_VIBHASHA, "विभाषोदरे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.89": SutraMeta(_VIDHI, "दृग्दृशवतुषु ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.90": SutraMeta(_VIDHI, "इदङ्किमोरीश्की ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.91": SutraMeta(_VIDHI, "आ सर्वनाम्नः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.92": SutraMeta(_VIDHI, "विष्वग्देवयोश्च टेरद्र्यञ्चतौ वप्रत्यये ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.93": SutraMeta(_VIDHI, "समः समि ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.94": SutraMeta(_VIDHI, "तिरसस्तिर्यलोपे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.95": SutraMeta(_VIDHI, "सहस्य सध्रिः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.96": SutraMeta(_VIDHI, "सध मादस्थयोश्छन्दसि ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.97": SutraMeta(_VIDHI, "द्व्यन्तरुपसर्गेभ्योऽप ईत्‌ ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.98": SutraMeta(_VIDHI, "ऊदनोर्देशे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.99": SutraMeta(_VIDHI, "अषष्ठ्यतृतीयास्थस्यान्यस्य दुगाशिराशाऽऽस्थाऽऽस्थितोत्सुकोतिकारकरागच्छेषु ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.100": SutraMeta(_VIBHASHA, "अर्थे विभाषा ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.101": SutraMeta(_VIDHI, "कोः कत्‌ तत्पुरुषेऽचि ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.102": SutraMeta(_VIDHI, "रथवदयोश्च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.103": SutraMeta(_VIDHI, "तृणे च जातौ ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.104": SutraMeta(_VIDHI, "का पथ्यक्षयोः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.105": SutraMeta(_VIDHI, "ईषदर्थे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.106": SutraMeta(_VIBHASHA, "विभाषा पुरुषे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.107": SutraMeta(_VIDHI, "कवं चोष्णे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.108": SutraMeta(_VIDHI, "पथि च च्छन्दसि ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.109": SutraMeta(_PARIBHASHA, "पृषोदरादीनि यथोपदिष्टम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.110": SutraMeta(_VIBHASHA, "संख्याविसायपूर्वस्याह्नस्याहन्नन्यतरस्यां ङौ ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.111": SutraMeta(_VIDHI, "ढ्रलोपे पूर्वस्य दीर्घोऽणः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.112": SutraMeta(_VIDHI, "सहिवहोरोदवर्णस्य ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.113": SutraMeta(_VIDHI, "साढ्यै साढ्वा साढेति निगमे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.114": SutraMeta(_VIDHI, "संहितायाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.115": SutraMeta(_VIDHI, "कर्णे लक्षणस्याविष्टाष्टपञ्चमणिभिन्नछिन्नछिद्रस्रुवस्वस्तिकस्य ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.116": SutraMeta(_VIDHI, "नहिवृतिवृषिव्यधिरुचिसहितनिषु क्वौ ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.117": SutraMeta(_VIDHI, "वनगिर्योः संज्ञायां कोटरकिंशुलकादीनाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.118": SutraMeta(_VIDHI, "वले ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.119": SutraMeta(_VIDHI, "मतौ बह्वचोऽनजिरादीनाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.120": SutraMeta(_VIDHI, "शरादीनां च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.121": SutraMeta(_VIDHI, "इकः वहे अपीलोः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.122": SutraMeta(_PARIBHASHA, "उपसर्गस्य घञ्यमनुष्ये बहुलम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.123": SutraMeta(_VIDHI, "इकः काशे ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.124": SutraMeta(_VIDHI, "दस्ति ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.125": SutraMeta(_VIDHI, "अष्टनः संज्ञायाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.126": SutraMeta(_VIDHI, "छन्दसि च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.127": SutraMeta(_VIDHI, "चितेः कपि ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.128": SutraMeta(_VIDHI, "विश्वस्य वसुराटोः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.129": SutraMeta(_VIDHI, "नरे संज्ञायाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.130": SutraMeta(_VIDHI, "मित्रे चर्षौ ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.131": SutraMeta(_VIDHI, "मन्त्रे सोमाश्वेन्द्रियविश्वदेव्यस्य मतौ ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.132": SutraMeta(_VIDHI, "ओषधेश्च विभक्तावप्रथमायाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.133": SutraMeta(_VIDHI, "ऋचि तुनुघमक्षुतङ्कुत्रोरुष्याणाम् ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.134": SutraMeta(_VIDHI, "इकः सुञि ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.135": SutraMeta(_VIDHI, "द्व्यचोऽतस्तिङः ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.136": SutraMeta(_VIDHI, "निपातस्य च ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.137": SutraMeta(_VIDHI, "अन्येषामपि दृश्यते ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.138": SutraMeta(_VIDHI, "चौ ।", ("domain:uttarapada", "pada:6.3")),
    "6.3.139": SutraMeta(_VIDHI, "सम्प्रसारणस्य ।", ("domain:uttarapada", "pada:6.3")),
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
        raise AssertionError("sutra_impl_6_3 self_check failed:\n" + "\n".join(failures))
    return {
        "sutras": len(FIXTURES),
        "predicates": len([n for n in globals() if n.startswith("sutra_6_3_")]),
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
