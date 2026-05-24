"""Strong/weak stem grade selection for tiṅanta paradigms."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .grammar import GrammaticalNumber, Lakara, Person

if TYPE_CHECKING:
    from .tinanta import Dhatu


def _is_sarvadhatuka(lakara: Lakara) -> bool:
    return lakara in {Lakara.LAT, Lakara.LOT, Lakara.LAN, Lakara.VIDHILING}


def _is_ardhadhatuka(lakara: Lakara) -> bool:
    if lakara == Lakara.LIT:
        return True
    return not _is_sarvadhatuka(lakara)

# Strong grade in liṭ: 1st dual/plural, 3rd plural (periphrastic perfect model).
_LIT_STRONG_SLOTS = frozenset(
    {
        (Person.FIRST, GrammaticalNumber.DUAL),
        (Person.FIRST, GrammaticalNumber.PLURAL),
        (Person.THIRD, GrammaticalNumber.PLURAL),
    }
)

# Catalog-driven strong stems for common roots in liṭ (reduplicated strong grade).
_STRONG_STEM_BY_ROOT: dict[str, str] = {
    "bhū": "babhū",
    "kṛ": "cakṛ",
    "gam": "jagam",
    "dā": "dadā",
    "stu": "tuṣṭu",
    "pā": "papā",
    "vid": "vivid",
    "i": "ayā",
    "as": "āsa",
    "ad": "adā",
    "han": "jaghān",
}


def stem_grade(dhatu: Dhatu, lakara: Lakara, person: Person, number: GrammaticalNumber) -> str:
    """Return ``strong`` or ``weak`` for the requested paradigm slot."""
    if lakara == Lakara.LIT:
        return "strong" if (person, number) in _LIT_STRONG_SLOTS else "weak"
    if lakara in {Lakara.LUN, Lakara.LRN}:
        return "weak"
    if _is_sarvadhatuka(lakara):
        return "strong"
    if _is_ardhadhatuka(lakara):
        return "weak"
    return "strong"


def conjunct_stem(
    dhatu: Dhatu,
    lakara: Lakara,
    person: Person,
    number: GrammaticalNumber,
    *,
    effective_dhatu: Dhatu | None = None,
) -> str:
    """Select present stem (sārvadhātuka) vs root/weak grade (ardhadhātuka)."""
    root = (effective_dhatu or dhatu).lemma
    grade = stem_grade(dhatu, lakara, person, number)

    if _is_sarvadhatuka(lakara):
        return (effective_dhatu or dhatu).present_stem

    if lakara == Lakara.LIT and grade == "strong":
        return _STRONG_STEM_BY_ROOT.get(root, root)

    # Ardhadhātuka: root as weak stem (guṇa applied in join_stem_ending).
    return root


__all__ = ["conjunct_stem", "stem_grade"]
