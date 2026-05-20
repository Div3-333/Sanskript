from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DerivationFamily(str, Enum):
    KRT = "kṛt"
    TADDHITA = "taddhita"


class KrtSuffix(str, Enum):
    KTVA = "ktvā"
    TUMUN = "tumun"
    KTA = "kta"
    KTAVATU = "ktavatu"
    TAVYA = "tavya"
    ANIYA = "anīya"
    SHATR = "śatṛ"
    SHANAC = "śānac"
    GHAN = "ghañ"
    NVUL = "ṇvul"
    TRC = "tṛc"
    AN = "aṇ"
    KA = "ka"
    TA = "ṭa"
    LYUT = "lyuṭ"
    GHA = "gha"
    KTIN = "ktin"
    SATR = "śatṛ"
    SANAC = "śānac"
    KVASU = "kvasu"
    KANAC = "kānac"


class TaddhitaSuffix(str, Enum):
    APATYA = "apatya"
    MATUP = "matu̐p"
    ATISHAYANA = "atiśāyana"


@dataclass(frozen=True)
class DerivedForm:
    source: str
    suffix: KrtSuffix | TaddhitaSuffix
    family: DerivationFamily
    surface: str
    gloss: str
    sutra_id: str = ""
    semantic: str = ""
    operations: tuple[str, ...] = ()


@dataclass(frozen=True)
class TaddhitaRule:
    sutra_id: str
    suffix: TaddhitaSuffix
    semantic: str
    source_gloss: str


TADDHITA_RULES: dict[str, TaddhitaRule] = {
    "4.1.92": TaddhitaRule("4.1.92", TaddhitaSuffix.APATYA, "apatya", "descendant or offspring of the source stem"),
    "5.2.94": TaddhitaRule("5.2.94", TaddhitaSuffix.MATUP, "possession", "possessing the source object or quality"),
    "5.3.55": TaddhitaRule("5.3.55", TaddhitaSuffix.ATISHAYANA, "atishayana", "surpassing degree or superlative quality"),
}


KRT_FORMS: tuple[DerivedForm, ...] = (
    DerivedForm("bhū", KrtSuffix.KTVA, DerivationFamily.KRT, "bhūtvā", "having become"),
    DerivedForm("bhū", KrtSuffix.TUMUN, DerivationFamily.KRT, "bhavitum", "to become"),
    DerivedForm("bhū", KrtSuffix.KTA, DerivationFamily.KRT, "bhūta", "become, been"),
    DerivedForm("bhū", KrtSuffix.TAVYA, DerivationFamily.KRT, "bhavitavya", "to be become or to be"),
    DerivedForm("dṛś", KrtSuffix.TUMUN, DerivationFamily.KRT, "draṣṭum", "to see"),
    DerivedForm("dṛś", KrtSuffix.KTA, DerivationFamily.KRT, "dṛṣṭa", "seen"),
    DerivedForm("nī", KrtSuffix.ANIYA, DerivationFamily.KRT, "nayanīya", "to be led"),
    DerivedForm("pac", KrtSuffix.SHATR, DerivationFamily.KRT, "pacat", "cooking"),
    DerivedForm("labh", KrtSuffix.SHANAC, DerivationFamily.KRT, "labhamāna", "obtaining"),
    DerivedForm("kṛ", KrtSuffix.GHAN, DerivationFamily.KRT, "kāra", "doing, making"),
)


TADDHITA_FORMS: tuple[DerivedForm, ...] = (
    DerivedForm("bala", TaddhitaSuffix.MATUP, DerivationFamily.TADDHITA, "balavān", "possessing strength", "5.2.94", "possession", ("matup-realized-as-vān",)),
    DerivedForm("go", TaddhitaSuffix.MATUP, DerivationFamily.TADDHITA, "gomān", "possessing cattle", "5.2.94", "possession", ("matup-realized-as-mān",)),
    DerivedForm("upagu", TaddhitaSuffix.APATYA, DerivationFamily.TADDHITA, "aupagava", "descendant of Upagu", "4.1.92", "apatya", ("initial-vrddhi", "final-u-to-ava")),
    DerivedForm("laghu", TaddhitaSuffix.ATISHAYANA, DerivationFamily.TADDHITA, "laghiṣṭha", "lightest", "5.3.55", "atishayana", ("final-u-to-iṣṭha",)),
)


VRDDHI_INITIAL = {
    "a": "ā",
    "ā": "ā",
    "i": "ai",
    "ī": "ai",
    "u": "au",
    "ū": "au",
    "ṛ": "ār",
    "ṝ": "ār",
    "e": "ai",
    "o": "au",
}


def _apply_initial_vrddhi(stem: str) -> tuple[str, bool]:
    for index, char in enumerate(stem):
        replacement = VRDDHI_INITIAL.get(char)
        if replacement is not None:
            return stem[:index] + replacement + stem[index + 1 :], True
    return stem, False


def _derive_apatya(source: str) -> tuple[str, tuple[str, ...]]:
    stem, strengthened = _apply_initial_vrddhi(source)
    operations: list[str] = ["initial-vrddhi"] if strengthened else []
    if stem.endswith("u"):
        operations.append("final-u-to-ava")
        return stem[:-1] + "ava", tuple(operations)
    if stem.endswith("i"):
        operations.append("final-i-to-eya")
        return stem[:-1] + "eya", tuple(operations)
    if stem.endswith("a"):
        operations.append("apatya-aṇ")
        return stem, tuple(operations)
    operations.append("apatya-a")
    return stem + "a", tuple(operations)


def _derive_matup(source: str) -> tuple[str, tuple[str, ...]]:
    if source == "go":
        return "gomān", ("matup-realized-as-mān",)
    if source.endswith("a"):
        return source[:-1] + "avān", ("matup-realized-as-vān",)
    if source.endswith("ā"):
        return source + "vān", ("matup-realized-as-vān",)
    return source + "mān", ("matup-realized-as-mān",)


def _derive_atishayana(source: str) -> tuple[str, tuple[str, ...]]:
    lexical = {
        "laghu": "laghiṣṭha",
        "guru": "gariṣṭha",
        "dīrgha": "drāghiṣṭha",
        "alpa": "alpiṣṭha",
    }
    if source in lexical:
        return lexical[source], ("lexical-superlative-stem", "iṣṭha")
    if source.endswith("u"):
        return source[:-1] + "iṣṭha", ("final-u-to-iṣṭha",)
    if source.endswith("a"):
        return source[:-1] + "iṣṭha", ("final-a-to-iṣṭha",)
    return source + "iṣṭha", ("iṣṭha",)


def derive_taddhita(source: str, sutra_id: str | None = None, suffix: TaddhitaSuffix | None = None) -> DerivedForm:
    """Derive a controlled taddhita form through a rule-level engine.

    Unlike the older registry lookup, this function selects a Paninian rule,
    applies the stem operation required by the taddhita suffix, and returns
    the rule id, semantic relation, surface, and operations used.
    """
    if sutra_id is None and suffix is None:
        raise ValueError("derive_taddhita requires sutra_id or suffix")

    from .adhyaya45_engines import derive_adhyaya45_taddhita

    engine_result = derive_adhyaya45_taddhita(source, sutra_id=sutra_id, suffix=suffix)
    selected_suffix = engine_result.suffix
    if not isinstance(selected_suffix, TaddhitaSuffix):
        raise ValueError(f"{engine_result.sutra_ids[0]} did not select a controlled TaddhitaSuffix")
    return DerivedForm(
        source,
        selected_suffix,
        DerivationFamily.TADDHITA,
        engine_result.surface,
        engine_result.gloss,
        engine_result.sutra_ids[0],
        engine_result.semantic,
        engine_result.operations,
    )


def derive(source: str, suffix: KrtSuffix | TaddhitaSuffix) -> DerivedForm:
    """
    Partial kṛt derivation registry. This is not full Adhyāya 3.1 implementation.
    3.1.91: dhātoḥ (Adhikara: these suffixes apply to roots).
    3.1.93: kṛd-atiriṅ (Suffixes other than tiṅ are called kṛt).
    """
    # 3.1.94: vā'sarūpo'striyām (Optionally different suffixes apply)
    for form in KRT_FORMS + TADDHITA_FORMS:
        if form.source == source and form.suffix == suffix:
            return form

    if isinstance(suffix, KrtSuffix):
        surface = source
        # 3.2.135: ṇvul-tṛcau
        if suffix == KrtSuffix.NVUL:
             surface = source + "aka"
             if source == "kṛ": surface = "kāraka"
        elif suffix == KrtSuffix.TRC:
             surface = source + "tṛ"
             if source == "kṛ": surface = "kartṛ"

        # 3.2.1: karmaṇy-aṇ
        elif suffix == KrtSuffix.AN:
             surface = source + "a"
             if source == "kṛ": surface = "kāra"

        # 3.3.18: bhāve ghañ (Vṛddhi + a)
        elif suffix == KrtSuffix.GHAN:
             surface = source + "a"
             if source == "kṛ": surface = "kāra"
             elif source == "pac": surface = "pāka"
             elif source == "bhū": surface = "bhāva"

        # 3.3.115: lyuṭ (ana)
        elif suffix == KrtSuffix.LYUT:
             surface = source + "ana"
             if source == "bhū": surface = "bhavana"
             elif source == "pac": surface = "pacana"

        # 3.3.121: halś-ca (Gha suffix for hal-ending roots)
        elif suffix == KrtSuffix.GHA:
             surface = source + "a" # No vṛddhi
             if source == "ram": surface = "rama" # e.g. ramaṇa/rama

        # 3.3.94: striyām ktin (ti suffix)
        elif suffix == KrtSuffix.KTIN:
             surface = source + "ti"
             if source == "kṛ": surface = "kṛti"
             elif source == "gam": surface = "gati"

        # 3.4.69: śatṛ (at)
        elif suffix == KrtSuffix.SATR:
             surface = source + "at"
             if source == "bhū": surface = "bhavat"
             elif source == "pac": surface = "pacat"

        # 3.4.69: śānac (māna)
        elif suffix == KrtSuffix.SANAC:
             surface = source + "māna"
             if source == "labh": surface = "labhamāna"

        # 3.4.71: kvasu (vas)
        elif suffix == KrtSuffix.KVASU:
             surface = source + "vas"
             if source == "bhū": surface = "babhūvas"

        # 3.4.72: kānac (āna)
        elif suffix == KrtSuffix.KANAC:
             surface = source + "āna"
             if source == "pac": surface = "pecāna"

        # 3.2.3: āto'nupasarge kaḥ
        elif suffix == KrtSuffix.KA:
             surface = source + "a"
             if source == "dā": surface = "da" # e.g. dadāti -> da

        # 3.2.16: careṣ-ṭaḥ
        elif suffix == KrtSuffix.TA:
             surface = source + "a"
             if source == "car": surface = "cara"

        # 3.2.102: niṣṭhā
        elif suffix == KrtSuffix.KTA:
            # 1.1.26: kta-ktavatū niṣṭhā
            surface = source + "ta"
            if source == "bhū": surface = "bhūta"
            elif source == "dṛś": surface = "dṛṣṭa"

        elif suffix == KrtSuffix.KTAVATU:
            surface = source + "tavat"
            if source == "bhū": surface = "bhūtavat"

        # Generic rule-based derivation for KRT
        if surface == source:
            if suffix == KrtSuffix.TUMUN: surface += "itum"
            elif suffix == KrtSuffix.KTVA: surface += "itvā"
        elif suffix == KrtSuffix.ANIYA:
             if surface.endswith("i") or surface.endswith("u"):
                 surface = surface[:-1] + ("anīya")
             else:
                 surface += "anīya"

        return DerivedForm(source, suffix, DerivationFamily.KRT, surface, f"{suffix.name} of {source}")

    if isinstance(suffix, TaddhitaSuffix):
        return derive_taddhita(source, suffix=suffix)

    raise ValueError(f"No controlled derived form for {source!r} with suffix {suffix.value!r}")


def forms_by_family(family: DerivationFamily) -> tuple[DerivedForm, ...]:
    return tuple(form for form in KRT_FORMS + TADDHITA_FORMS if form.family == family)
