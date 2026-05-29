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
    Avyaya("yadi", "yadi", IndeclinableKind.RELATIVE, "if", "opens a conditional block"),
    Avyaya("tarhi", "tarhi", IndeclinableKind.CORRELATIVE, "then", "marks the consequent clause"),
    Avyaya("anyathā", "anyathā", IndeclinableKind.ALTERNATIVE, "otherwise", "marks the alternate branch"),
    Avyaya("samam", "samam", IndeclinableKind.ADVERB, "equally", "marks equality in a condition"),
    Avyaya("pūrvaṃ", "pūrva", IndeclinableKind.ADVERB, "previous value", "used in examples for previous-state variables"),
    Avyaya("purvam", "pūrva", IndeclinableKind.ADVERB, "previous value", "ASCII form used in examples for previous-state variables"),
    Avyaya("vidhānam", "vidhāna", IndeclinableKind.SEQUENCER, "procedure", "declares a named procedure"),
    Avyaya("samāpanam", "samāpana", IndeclinableKind.SEQUENCER, "completion", "closes a procedure or module"),
    Avyaya("āhvānam", "āhvāna", IndeclinableKind.SEQUENCER, "invocation", "calls a named procedure"),
    Avyaya("kṣetram", "kṣetra", IndeclinableKind.SEQUENCER, "field, module", "opens a module scope"),
    Avyaya("antam", "anta", IndeclinableKind.SEQUENCER, "end", "closes a conditional or loop block"),
    Avyaya("pratyāvartanam", "pratyāvartana", IndeclinableKind.SEQUENCER, "return", "returns control to the caller"),
    Avyaya("pratyavartanam", "pratyāvartana", IndeclinableKind.SEQUENCER, "return", "returns control to the caller (ASCII form)"),
    # Natural-language binary operator lexemes (required for strict morphology validation).
    Avyaya("yoga", "yoga", IndeclinableKind.ADVERB, "addition operator", "yoga as an add operator word"),
    Avyaya("vyavakalanam", "vyavakalanam", IndeclinableKind.ADVERB, "subtraction operator", "vyavakalanam as a subtract operator word"),
    Avyaya("hīna", "hīna", IndeclinableKind.ADVERB, "subtraction operator", "hīna as a subtract operator word"),
    Avyaya("hina", "hina", IndeclinableKind.ADVERB, "subtraction operator", "hina as a subtract operator word"),
    Avyaya("guṇanam", "guṇanam", IndeclinableKind.ADVERB, "multiplication operator", "guṇanam as a multiply operator word"),
    Avyaya("gunanam", "gunanam", IndeclinableKind.ADVERB, "multiplication operator", "gunanam as a multiply operator word"),
    Avyaya("gunena", "gunena", IndeclinableKind.ADVERB, "multiplication operator", "gunena as a multiply operator word"),
    Avyaya("bhāga", "bhāga", IndeclinableKind.ADVERB, "division operator", "bhāga as a divide operator word"),
    Avyaya("bhaga", "bhaga", IndeclinableKind.ADVERB, "division operator", "bhaga as a divide operator word"),
    Avyaya("bhāgena", "bhāgena", IndeclinableKind.ADVERB, "division operator", "bhāgena as a divide operator word"),
    Avyaya("bhagena", "bhagena", IndeclinableKind.ADVERB, "division operator", "bhagena as a divide operator word"),
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
