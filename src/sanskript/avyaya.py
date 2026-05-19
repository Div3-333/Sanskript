from __future__ import annotations

from dataclasses import dataclass

from .grammar import Analysis, IndeclinableKind, PartOfSpeech


@dataclass(frozen=True)
class Avyaya:
    surface: str
    lemma: str
    kind: IndeclinableKind
    gloss: str
    scope_hint: str


AVYAYA_FORMS: tuple[Avyaya, ...] = (
    Avyaya("ca", "ca", IndeclinableKind.CONJUNCTION, "and", "joins a previous item to the current clause"),
    Avyaya("vā", "vā", IndeclinableKind.ALTERNATIVE, "or", "marks an alternative branch or choice"),
    Avyaya("api", "api", IndeclinableKind.EMPHASIS, "also, even", "adds inclusive emphasis"),
    Avyaya("eva", "eva", IndeclinableKind.EMPHASIS, "just, exactly", "marks exactness or restriction"),
    Avyaya("na", "na", IndeclinableKind.NEGATION, "not", "negates a finite assertion"),
    Avyaya("mā", "mā", IndeclinableKind.PROHIBITIVE, "do not", "marks a negative command"),
    Avyaya("kim", "kim", IndeclinableKind.QUESTION, "what, whether", "marks interrogative force"),
    Avyaya("katham", "katham", IndeclinableKind.QUESTION, "how", "asks for manner or method"),
    Avyaya("kadā", "kadā", IndeclinableKind.QUESTION, "when", "asks for time"),
    Avyaya("yatra", "yatra", IndeclinableKind.RELATIVE, "where", "opens a relative place phrase"),
    Avyaya("yadā", "yadā", IndeclinableKind.RELATIVE, "when", "opens a relative time phrase"),
    Avyaya("tatra", "tatra", IndeclinableKind.CORRELATIVE, "there", "answers yatra with a correlated locus"),
    Avyaya("tadā", "tadā", IndeclinableKind.CORRELATIVE, "then", "answers yadā with a correlated time"),
    Avyaya("atra", "atra", IndeclinableKind.ADVERB, "here", "locative adverb for current scope"),
    Avyaya("punaḥ", "punar", IndeclinableKind.ADVERB, "again", "marks repeated action"),
    Avyaya("iti", "iti", IndeclinableKind.QUOTATIVE, "thus", "closes quoted or named material"),
    Avyaya("atha", "atha", IndeclinableKind.SEQUENCER, "now, then", "begins the next step"),
)


AVYAYA_SUFFIXES = frozenset({"ktvā", "tosun", "kasun"})


UPASARGAS: tuple[Avyaya, ...] = (
    Avyaya("pra", "pra", IndeclinableKind.PREFIX, "forth", "forward or intensifying verbal prefix"),
    Avyaya("parā", "parā", IndeclinableKind.PREFIX, "away", "awayward verbal prefix"),
    Avyaya("apa", "apa", IndeclinableKind.PREFIX, "off", "separative verbal prefix"),
    Avyaya("sam", "sam", IndeclinableKind.PREFIX, "together", "collective verbal prefix"),
    Avyaya("anu", "anu", IndeclinableKind.PREFIX, "after", "following or repeated verbal prefix"),
    Avyaya("ava", "ava", IndeclinableKind.PREFIX, "down", "downward verbal prefix"),
    Avyaya("nis", "nis", IndeclinableKind.PREFIX, "out", "outward verbal prefix"),
    Avyaya("dus", "dus", IndeclinableKind.PREFIX, "badly", "difficult or adverse prefix"),
    Avyaya("vi", "vi", IndeclinableKind.PREFIX, "apart", "division or distinction prefix"),
    Avyaya("ā", "ā", IndeclinableKind.PREFIX, "toward", "approaching verbal prefix"),
    Avyaya("ni", "ni", IndeclinableKind.PREFIX, "down into", "settling or inward verbal prefix"),
    Avyaya("adhi", "adhi", IndeclinableKind.PREFIX, "over", "over or concerning verbal prefix"),
    Avyaya("ati", "ati", IndeclinableKind.PREFIX, "beyond", "excessive or crossing prefix"),
    Avyaya("su", "su", IndeclinableKind.PREFIX, "well", "good or favorable prefix"),
    Avyaya("ud", "ud", IndeclinableKind.PREFIX, "up", "upward verbal prefix"),
    Avyaya("abhi", "abhi", IndeclinableKind.PREFIX, "toward", "facing or directed prefix"),
    Avyaya("prati", "prati", IndeclinableKind.PREFIX, "back, against", "returning or corresponding prefix"),
    Avyaya("pari", "pari", IndeclinableKind.PREFIX, "around", "surrounding verbal prefix"),
    Avyaya("upa", "upa", IndeclinableKind.PREFIX, "near", "approaching or subordinate prefix"),
)


def is_controlled_avyaya(surface: str) -> bool:
    return any(form.surface == surface for form in AVYAYA_FORMS + UPASARGAS)


def is_avyaya_suffix(suffix: str) -> bool:
    return suffix in AVYAYA_SUFFIXES


def iter_avyaya_analyses() -> tuple[Analysis, ...]:
    seen = {form.surface for form in AVYAYA_FORMS}
    lexical_items = AVYAYA_FORMS + tuple(form for form in UPASARGAS if form.surface not in seen)
    return tuple(
        Analysis(
            surface=form.surface,
            lemma=form.lemma,
            pos=PartOfSpeech.INDECLINABLE,
            indeclinable_kind=form.kind,
        )
        for form in lexical_items
    )


def avyaya_for(surface: str) -> Avyaya:
    for form in AVYAYA_FORMS + UPASARGAS:
        if form.surface == surface:
            return form
    raise ValueError(f"Unknown controlled avyaya: {surface!r}")


def upasarga_surfaces() -> tuple[str, ...]:
    return tuple(form.surface for form in UPASARGAS)
