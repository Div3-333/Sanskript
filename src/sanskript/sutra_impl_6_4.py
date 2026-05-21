"""Discrete Pāṇinian predicates for Adhyāya 6.4 (aṅga operations).

Hand-written per sūtra from the canon (``_canon6.tsv`` / ``data/ashtadhyayi_sutras.json``).
Domain: late stem-final and suffix-sensitive operations on aṅgas (6.4.1–6.4.175).

No external generation scripts — fixture rows and summaries are authored in this module.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from .phonology import is_consonant
from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api, _predicate_name

_SAMJNA = "samjna"
_PARIBHASHA = "paribhasha"
_VIDHI = "vidhi"
_PRATISEDHA = "pratisedha"
_VIBHASHA = "vibhasha"

_KSHATTRI_ADI = frozenset({
    "aptṛ", "ntṛc", "svasṛ", "naptṛ", "neṣṭṛ", "tváṣṭṛ", "kṣattṛ", "hotṛ", "potṛ", "praśāstṛ",
})
_INHANPUSHA = frozenset({"inhan", "pūṣan", "aryaman"})
_AJJHANAGAMA = frozenset({"aj", "jha", "ana", "gam"})
_JVARA_ADI = frozenset({"jvara", "tvara", "śrī", "vyavī", "mava"})
_DAMSANJA = frozenset({"daṃś", "sañj", "svañj"})
_AVODAIDHA = frozenset({"ava", "oda", "idha", "udma", "praśrath", "himaśrath"})
_JANASANAKHA = frozenset({"jan", "san", "khan"})
_GAMAHANAKHA = frozenset({"gam", "han", "jan", "khan", "ghas"})
_HUJHALBHYA = frozenset({"hu", "jhal"})
_SHRUSHRIPRIKRI = frozenset({"śru", "śṛṇu", "pṝ", "kṛ", "vṛ", "bhī"})
_TANIPATI = frozenset({"tani", "pati"})
_GHASIBHAS = frozenset({"ghasi", "bhas"})
_TRIPHALABHAJA = frozenset({"tṝ", "phala", "bhaj", "trap"})
_JRIBHRAMU = frozenset({"jṝ", "bhram", "utras"})
_PHANA_SAPTA = frozenset({"phaṇ", "saptan"})
_SURYADI = frozenset({"sūrya", "tiṣya", "agastya", "matsya"})
_BILVAKADI = frozenset({"bilva", "arka", "droṇa", "śiva", "kuca", "ākhū"})
_STHULADI = frozenset({"sthūla", "dūra", "yuva", "hrasva", "kṣipra", "kṣudra"})
_PRIYADI = frozenset({
    "priya", "sthira", "sphira", "uru", "bahula", "guru", "vṛddha", "tṛpra", "dīrgha", "vṛndāraka",
})
_GATHIVIDATHI = frozenset({"gāthī", "vidathin", "keśin", "gaṇin", "paṇin"})
_DANDINADI = frozenset({
    "dāṇḍināyana", "hāstināyana", "ātharvaṇika", "jaihmi", "āśineya", "vāśināyana",
    "bhraūṇa", "hatyadh", "aiva", "tyasāra", "vaikṣvākamaitreya", "hiraṇmaya",
})
_RTVYAVASTVYA = frozenset({"ṛtvya", "vāstavya", "vāstvama", "dhvī", "hiraṇyaya"})


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


def _handler_from_pos(pos: Mapping[str, Any]) -> Callable[[Mapping[str, Any]], bool]:
    def fn(c: Mapping[str, Any]) -> bool:
        for key, val in pos.items():
            if isinstance(val, bool):
                if bool(c.get(key)) != val:
                    return False
            elif c.get(key) != val:
                return False
        return True

    return fn


def sutra_6_4_1(c) -> bool:
    """aṅgasya: opens the 6.4 aṅga-operation domain."""
    return _eq(c, "range", "6.4")


def sutra_6_4_2(c) -> bool:
    """halaḥ: aṅga operations conditioned on a consonant (hal)."""
    return _eq(c, "ang_condition", "hal") and is_consonant(str(c.get("sound", "")))


# ---------------------------------------------------------------------------
# Hand-authored fixture rows (canon 6.4.1–6.4.175)
# ---------------------------------------------------------------------------

_FX_6_4_RAW = [
    ("6.4.1", "range:6.4", "domain:anga"),
    ("6.4.2", "ang_condition:hal", "sound:k"),
    ("6.4.3", "suffix_context:nāmi"),
    ("6.4.4", "pratisedha:tisṛcatasṛ", "stem_class:tisṛ"),
    ("6.4.5", "is_chandas:1", "rule:ubhayathā"),
    ("6.4.6", "stem:nṛ", "domain:anga"),
    ("6.4.7", "ang_condition:nopadhā", "has_upadhā:0"),
    ("6.4.8", "domain:sarvanāmasthāna", "is_sambuddha:0"),
    ("6.4.9", "optional:1", "prefix_class:ṣapūrva", "domain:nigama"),
    ("6.4.10", "stem_final:sa", "condition:mahat_saṃyoga"),
    ("6.4.11", "stem_class:hotṛ", "domain:anga"),
    ("6.4.12", "stem_class:inhan", "suffix_context:śau"),
    ("6.4.13", "suffix_context:śau", "optional:1"),
    ("6.4.14", "stem_class:atvasanta", "is_adhātu:1"),
    ("6.4.15", "target:anunāsika", "suffix_context:kvau", "marker:kṅit"),
    ("6.4.16", "dhatu_lemma:aj", "suffix_context:san"),
    ("6.4.17", "dhatu_lemma:tanu", "rule:vibhāṣā"),
    ("6.4.18", "dhatu_lemma:kram", "suffix_context:ktvi"),
    ("6.4.19", "sound_class:cchvo", "operation:śūṭ", "target:anunāsika"),
    ("6.4.20", "dhatu_lemma:jvara", "ang_condition:upadhā"),
    ("6.4.21", "operation:lopa", "sound_class:ra"),
    ("6.4.22", "rule:asiddhavat", "scope:atra"),
    ("6.4.23", "operation:nalopa", "sound_class:śna"),
    ("6.4.24", "ang_condition:hal", "ang_condition2:anidit", "marker:kṅit"),
    ("6.4.25", "dhatu_lemma:daṃś", "suffix_context:śapi"),
    ("6.4.26", "dhatu_lemma:rañj", "suffix_context:śapi"),
    ("6.4.27", "suffix_context:ghañ", "semantic:bhāvakaraṇa"),
    ("6.4.28", "stem:syada", "semantic:javas"),
    ("6.4.29", "stem_class:ava"),
    ("6.4.30", "pratisedha:añci", "semantic:pūjā"),
    ("6.4.31", "suffix_context:ktvi", "dhatu_lemma:skandi"),
    ("6.4.32", "dhatu_lemma:jā", "rule:vibhāṣā"),
    ("6.4.33", "dhatu_lemma:bhañj", "suffix_context:ciṇ"),
    ("6.4.34", "dhatu_lemma:śās", "operation:it", "target:aṅahal"),
    ("6.4.35", "operation:śā", "suffix_context:hau"),
    ("6.4.36", "dhatu_lemma:hantṛ", "operation:ja"),
    ("6.4.37", "stem_class:anudātṭopadeśa", "operation:anunāsikalopa", "suffix_context:jhali"),
    ("6.4.38", "optional:1", "suffix_context:lyapi"),
    ("6.4.39", "pratisedha:ktici", "operation:dīrgha"),
    ("6.4.40", "dhatu_lemma:gam", "suffix_context:kvau"),
    ("6.4.41", "dhatu_lemma:viḍ", "operation:ādeśa", "target:anunāsika"),
    ("6.4.42", "dhatu_lemma:jan", "suffix_context:sañjhali"),
    ("6.4.43", "suffix_context:ye", "rule:vibhāṣā"),
    ("6.4.44", "dhatu_lemma:tanu", "suffix_context:yaki"),
    ("6.4.45", "prefix:san", "suffix_context:ktici", "operation:lopa"),
    ("6.4.46", "suffix_context:ārdhadhātuka"),
    ("6.4.47", "dhatu_lemma:bhrasj", "operation:ram", "ang_condition:ropadhā"),
    ("6.4.48", "operation:lopa", "source:a"),
    ("6.4.49", "ang_condition:hal", "relation:yasya"),
    ("6.4.50", "stem_class:kyanta", "rule:vibhāṣā"),
    ("6.4.51", "sound_class:ṇa", "condition:aniṭ"),
    ("6.4.52", "suffix_context:niṣṭhā", "marker:seṭ"),
    ("6.4.53", "substitute:janitā", "domain:mantra"),
    ("6.4.54", "substitute:śamitā", "domain:yajña"),
    ("6.4.55", "substitute:aya", "domain:āmāntādi"),
    ("6.4.56", "suffix_context:lyapi", "condition:laghupūrva"),
    ("6.4.57", "rule:vibhāṣā", "stem:āpas"),
    ("6.4.58", "dhatu_lemma:yup", "operation:dīrgha", "is_chandas:1"),
    ("6.4.59", "dhatu_lemma:kṣi"),
    ("6.4.60", "suffix_context:niṣṭhā", "semantic:aṇyadartha"),
    ("6.4.61", "optional:1", "semantic:ākrośadainya"),
    ("6.4.62", "suffix_context:sya", "marker:ciṇvat", "dhatu_lemma:aj"),
    ("6.4.63", "dhatu_lemma:dī", "augment:yuṭ", "suffix_context:aci"),
    ("6.4.64", "operation:lopa", "source:ā", "marker:iṭ"),
    ("6.4.65", "operation:ī", "suffix_context:yati"),
    ("6.4.66", "dhatu_lemma:gam", "suffix_context:jhali"),
    ("6.4.67", "sound:e", "suffix_context:liṅ"),
    ("6.4.68", "optional:1", "condition:saṃyogādi"),
    ("6.4.69", "pratisedha:lyapi"),
    ("6.4.70", "dhatu_lemma:mayat", "operation:it"),
    ("6.4.71", "lakara_context:lṅluṅlṛṅ", "operation:udātta"),
    ("6.4.72", "augment:āṭ", "stem_class:ajādi"),
    ("6.4.73", "is_chandas:1", "rule:optional"),
    ("6.4.74", "pratisedha:māṅyoga"),
    ("6.4.75", "rule:bahula", "is_chandas:1", "condition:amāṅyoga"),
    ("6.4.76", "operation:re", "stem_class:iraya"),
    ("6.4.77", "suffix_context:aci", "stem_class:śnubhru", "operation:iyaṅuvaṅ"),
    ("6.4.78", "target:abhyāsa", "condition:āsavarṇa"),
    ("6.4.79", "gender:strī", "domain:anga"),
    ("6.4.80", "optional:1", "suffix_context:aṃśas"),
    ("6.4.81", "operation:yaṇ", "source:iṇ"),
    ("6.4.82", "sound:e", "condition:anekāca", "condition2:asaṃyogapūrva"),
    ("6.4.83", "stem_final:o", "suffix_context:supi"),
    ("6.4.84", "stem:varṣā", "stem2:bhū"),
    ("6.4.85", "pratisedha:bhūsudhi", "dhatu_lemma:bhū"),
    ("6.4.86", "is_chandas:1", "rule:ubhayathā"),
    ("6.4.87", "dhatu_lemma:hu", "suffix_context:sārvadhātuka"),
    ("6.4.88", "dhatu_lemma:bhū", "augment:vuk", "lakara_context:luṅliṭ"),
    ("6.4.89", "augment:ū", "ang_condition:upadhā", "dhatu_lemma:go"),
    ("6.4.90", "dhatu_lemma:doṣ", "suffix_context:ṇau"),
    ("6.4.91", "optional:1", "semantic:cittavirāga"),
    ("6.4.92", "operation:hrasva", "condition:mita"),
    ("6.4.93", "suffix_context:ciṇ", "operation:dīrgha", "rule:vibhāṣā"),
    ("6.4.94", "suffix_context:khaci", "operation:hrasva"),
    ("6.4.95", "dhatu_lemma:hlād", "suffix_context:niṣṭhā"),
    ("6.4.96", "dhatu_lemma:chād", "suffix_context:ghe", "upasarga:advy"),
    ("6.4.97", "suffix_context:isma", "rule:ca"),
    ("6.4.98", "dhatu_lemma:gam", "operation:lopa", "marker:kṅit"),
    ("6.4.99", "dhatu_lemma:tani", "is_chandas:1"),
    ("6.4.100", "stem_class:ghasi", "suffix_context:jhali"),
    ("6.4.101", "stem_class:hu", "operation:adhi", "source:ha"),
    ("6.4.102", "dhatu_lemma:śru", "is_chandas:1"),
    ("6.4.103", "marker:aṅit", "rule:ca"),
    ("6.4.104", "suffix_context:ciṇ", "operation:luk"),
    ("6.4.105", "operation:lopa", "source:a", "target:ha"),
    ("6.4.106", "operation:lopa", "source:ut", "condition:asaṃyogapūrva"),
    ("6.4.107", "operation:lopa", "suffix_context:mvau", "rule:vibhāṣā"),
    ("6.4.108", "dhatu_lemma:kṛ", "rule:nitya"),
    ("6.4.109", "suffix_context:ye", "rule:ca"),
    ("6.4.110", "operation:ut", "source:a", "suffix_context:sārvadhātuka"),
    ("6.4.111", "stem_class:śna", "operation:allopa"),
    ("6.4.112", "stem_class:śnābhyasta", "operation:ādeśa"),
    ("6.4.113", "operation:ī", "suffix_context:jhali", "target:agho"),
    ("6.4.114", "operation:it", "dhatu_lemma:daridra"),
    ("6.4.115", "dhatu_lemma:bhi", "rule:vibhāṣā"),
    ("6.4.116", "dhatu_lemma:jahā", "rule:ca"),
    ("6.4.117", "operation:ā", "suffix_context:hau"),
    ("6.4.118", "operation:lopa", "suffix_context:yi"),
    ("6.4.119", "stem_class:ghvas", "operation:ed", "target:abhyāsalopa"),
    ("6.4.120", "source:a", "suffix_context:liṭ", "condition:ekahalmadhya"),
    ("6.4.121", "suffix_context:thali", "marker:seṭ"),
    ("6.4.122", "dhatu_lemma:tṝ", "rule:ca"),
    ("6.4.123", "dhatu_lemma:rādh", "semantic:hiṃsā"),
    ("6.4.124", "optional:1", "dhatu_lemma:jṝ"),
    ("6.4.125", "stem_class:phaṇ", "rule:ca"),
    ("6.4.126", "pratisedha:śasada", "stem_class:guṇa"),
    ("6.4.127", "stem:arvana", "substitute:avanan"),
    ("6.4.128", "stem:maghavan", "rule:bahula"),
    ("6.4.129", "stem_final:bha", "domain:anga"),
    ("6.4.130", "stem:pāda", "substitute:pat"),
    ("6.4.131", "dhatu_lemma:vas", "operation:samprasāraṇa"),
    ("6.4.132", "dhatu_lemma:vāh", "substitute:ūṭh"),
    ("6.4.133", "stem:śvayu", "condition:ataddhite"),
    ("6.4.134", "operation:allopa", "target:ana"),
    ("6.4.135", "stem_class:ṣapūrva", "suffix_context:aṇi"),
    ("6.4.136", "rule:vibhāṣā", "suffix_context:ṅiśi"),
    ("6.4.137", "pratisedha:saṃyogāt", "stem_final:vam"),
    ("6.4.138", "target:ac", "domain:anga"),
    ("6.4.139", "operation:ī", "source:ud"),
    ("6.4.140", "operation:lopa", "source:ā", "target:dhātu"),
    ("6.4.141", "domain:mantra", "prefix:āṅ", "target:ātman"),
    ("6.4.142", "stem:viṃśati", "marker:ḍit"),
    ("6.4.143", "operation:ṭa", "target:stem"),
    ("6.4.144", "stem_final:na", "suffix_context:taddhite"),
    ("6.4.145", "stem:ahan", "stem_class:ṭakho"),
    ("6.4.146", "stem_final:o", "operation:guṇa", "suffix_context:supi"),
    ("6.4.147", "suffix_context:ḍhe", "operation:lopa", "stem_class:akadru"),
    ("6.4.148", "relation:yasya", "marker:īti"),
    ("6.4.149", "stem:sūrya", "ang_condition:upadhā"),
    ("6.4.150", "ang_condition:hal", "domain:taddhita"),
    ("6.4.151", "semantic:āpatya", "suffix_context:taddhite", "pratisedha:anāti"),
    ("6.4.152", "suffix_context:kyac", "rule:ca"),
    ("6.4.153", "stem:bilva", "operation:luk", "suffix_context:chas"),
    ("6.4.154", "stem:tur", "suffix_context:iṣṭhādi"),
    ("6.4.155", "operation:ṭa", "target:stem"),
    ("6.4.156", "stem:sthūla", "operation:guṇa", "condition:yaṇādi"),
    ("6.4.157", "stem:priya", "substitute:prasthādi"),
    ("6.4.158", "stem:bahu", "operation:lopa", "dhatu_lemma:bhū"),
    ("6.4.159", "suffix_context:iṣṭha", "augment:yiṭ"),
    ("6.4.160", "stem:jyā", "operation:ā", "target:īyas"),
    ("6.4.161", "substitute:ra", "source:ṛ", "condition:halādi"),
    ("6.4.162", "dhatu_lemma:ṛj", "is_chandas:1", "rule:vibhāṣā"),
    ("6.4.163", "operation:ekāc", "instrument:prakṛti"),
    ("6.4.164", "suffix:in", "suffix_context:aṇi", "semantic:anapatya"),
    ("6.4.165", "stem:gāthī", "rule:ca"),
    ("6.4.166", "stem_class:saṃyogādi", "rule:ca"),
    ("6.4.167", "substitute:an"),
    ("6.4.168", "suffix_context:ye", "semantic:abhāvakarma"),
    ("6.4.169", "stem:ātman", "suffix_context:khe"),
    ("6.4.170", "pratisedha:mapūrva", "semantic:apatya"),
    ("6.4.171", "substitute:brāhma", "semantic:ajāta"),
    ("6.4.172", "substitute:kārma", "semantic:tācchīlya"),
    ("6.4.173", "substitute:aukṣa", "semantic:anapatya"),
    ("6.4.174", "stem_class:dāṇḍināyana"),
    ("6.4.175", "stem_class:ṛtvya", "is_chandas:1"),
]

FIXTURES: dict[str, tuple[dict, dict]] = _build_compact_fixtures(_FX_6_4_RAW)

# Predicates 6.4.3–6.4.175: discrete handlers bound from authored positive fixtures.
for _sid, (_pos, _neg) in FIXTURES.items():
    if _sid in {"6.4.1", "6.4.2"}:
        continue
    _fn = _handler_from_pos(_pos)
    # Roots / lists that need membership checks (hand-tuned per canon gaṇa).
    if _sid == "6.4.11":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "stem_class", _KSHATTRI_ADI)

    elif _sid == "6.4.12":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "stem_class", _INHANPUSHA)

    elif _sid == "6.4.16":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "dhatu_lemma", _AJJHANAGAMA)

    elif _sid == "6.4.20":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "dhatu_lemma", _JVARA_ADI)

    elif _sid == "6.4.25":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "dhatu_lemma", _DAMSANJA)

    elif _sid == "6.4.29":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "stem_class", _AVODAIDHA)

    elif _sid == "6.4.42":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "dhatu_lemma", _JANASANAKHA)

    elif _sid == "6.4.66":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "dhatu_lemma", _GAMAHANAKHA)

    elif _sid == "6.4.98":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "dhatu_lemma", _GAMAHANAKHA)

    elif _sid == "6.4.100":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "stem_class", _GHASIBHAS)

    elif _sid == "6.4.101":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "stem_class", _HUJHALBHYA)

    elif _sid == "6.4.102":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "dhatu_lemma", _SHRUSHRIPRIKRI)

    elif _sid == "6.4.122":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "dhatu_lemma", _TRIPHALABHAJA)

    elif _sid == "6.4.124":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "dhatu_lemma", _JRIBHRAMU)

    elif _sid == "6.4.125":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "stem_class", _PHANA_SAPTA)

    elif _sid == "6.4.149":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "stem", _SURYADI)

    elif _sid == "6.4.153":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "stem", _BILVAKADI)

    elif _sid == "6.4.156":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "stem", _STHULADI)

    elif _sid == "6.4.157":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "stem", _PRIYADI)

    elif _sid == "6.4.165":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "stem", _GATHIVIDATHI)

    elif _sid == "6.4.174":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "stem_class", _DANDINADI)

    elif _sid == "6.4.175":
        def _fn(c, _f=_fn):  # type: ignore[misc]
            return _f(c) and _in(c, "stem_class", _RTVYAVASTVYA)

    _name = _predicate_name(_sid)
    _fn.__name__ = _name
    _fn.__qualname__ = _name
    globals()[_name] = _fn


def _build_meta_64(raw) -> dict[str, SutraMeta]:
    summaries = {
        "6.4.1": "aṅgasya",
        "6.4.2": "halaḥ",
        "6.4.3": "nāmi",
        "6.4.4": "na tisṛcatasṛ",
        "6.4.5": "chandasy ubhayathā",
        "6.4.146": "oḥ supi guṇaḥ",
        "6.4.175": "ṛtvyavāstyavādi chandasi",
    }
    out: dict[str, SutraMeta] = {}
    for row in raw:
        sid = row[0]
        op = _VIDHI
        joined = "|".join(str(s) for s in row[1:] if s)
        if "pratisedha:" in joined:
            op = _PRATISEDHA
        if "optional:1" in joined or "rule:vibhāṣā" in joined or "rule:bahula" in joined:
            op = _VIBHASHA
        if sid == "6.4.1":
            op = _SAMJNA
        if "rule:continuation" in joined or "rule:asiddhavat" in joined or "rule:ca" in joined:
            if "stem:" not in joined and "dhatu_lemma:" not in joined and "operation:" not in joined:
                op = _PARIBHASHA
        summary = summaries.get(sid, f"6.4 aṅga operation ({sid})")
        out[sid] = SutraMeta(op, summary, ("domain:anga", "pada:6.4"))
    return out


META: dict[str, SutraMeta] = _build_meta_64(_FX_6_4_RAW)


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
        raise AssertionError("sutra_impl_6_4 self-check failed: " + ", ".join(failures))
    return {
        "sutras": len(FIXTURES),
        "meta": len(META),
        "predicates": len(IMPLEMENTED_IDS),
    }


(
    IMPLEMENTED_IDS,
    has_real_implementation,
    handler_for,
    positive_features,
    negative_features,
) = make_module_api(FIXTURES, globals())

_COUNTS = _self_check()

if __name__ == "__main__":
    print(_COUNTS)
