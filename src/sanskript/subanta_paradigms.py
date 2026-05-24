"""Full nominal declension paradigms beyond a/ā-stems."""

from __future__ import annotations

from .grammar import Case, GrammaticalNumber

CaseNumber = tuple[Case, GrammaticalNumber]


def _base(lemma: str, *, strip: int = 1) -> str:
    return lemma[:-strip] if len(lemma) > strip else lemma


def _forms(entries: dict[CaseNumber, str]) -> dict[CaseNumber, str]:
    return dict(entries)


def decline_i_masculine(lemma: str) -> dict[CaseNumber, str]:
    base = _base(lemma)
    return _forms(
        {
            (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): base + "iḥ",
            (Case.NOMINATIVE, GrammaticalNumber.DUAL): base + "ī",
            (Case.NOMINATIVE, GrammaticalNumber.PLURAL): base + "ayaḥ",
            (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): base + "im",
            (Case.ACCUSATIVE, GrammaticalNumber.DUAL): base + "ī",
            (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): base + "īn",
            (Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR): base + "inā",
            (Case.INSTRUMENTAL, GrammaticalNumber.DUAL): base + "ibhyām",
            (Case.INSTRUMENTAL, GrammaticalNumber.PLURAL): base + "ibhiḥ",
            (Case.DATIVE, GrammaticalNumber.SINGULAR): base + "aye",
            (Case.DATIVE, GrammaticalNumber.DUAL): base + "ibhyām",
            (Case.DATIVE, GrammaticalNumber.PLURAL): base + "ibhyas",
            (Case.ABLATIVE, GrammaticalNumber.SINGULAR): base + "eḥ",
            (Case.ABLATIVE, GrammaticalNumber.DUAL): base + "ibhyām",
            (Case.ABLATIVE, GrammaticalNumber.PLURAL): base + "ibhyas",
            (Case.GENITIVE, GrammaticalNumber.SINGULAR): base + "eḥ",
            (Case.GENITIVE, GrammaticalNumber.DUAL): base + "yoḥ",
            (Case.GENITIVE, GrammaticalNumber.PLURAL): base + "īnām",
            (Case.LOCATIVE, GrammaticalNumber.SINGULAR): base + "au",
            (Case.LOCATIVE, GrammaticalNumber.DUAL): base + "yoḥ",
            (Case.LOCATIVE, GrammaticalNumber.PLURAL): base + "iṣu",
            (Case.VOCATIVE, GrammaticalNumber.SINGULAR): base + "e",
            (Case.VOCATIVE, GrammaticalNumber.DUAL): base + "ī",
            (Case.VOCATIVE, GrammaticalNumber.PLURAL): base + "ayaḥ",
        }
    )


def decline_i_neuter(lemma: str) -> dict[CaseNumber, str]:
    forms = decline_i_masculine(lemma)
    base = _base(lemma)
    forms.update(
        {
            (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): lemma,
            (Case.NOMINATIVE, GrammaticalNumber.PLURAL): base + "īni",
            (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): lemma,
            (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): base + "īni",
            (Case.VOCATIVE, GrammaticalNumber.SINGULAR): lemma,
            (Case.VOCATIVE, GrammaticalNumber.PLURAL): base + "īni",
        }
    )
    return forms


def decline_ii_feminine(lemma: str) -> dict[CaseNumber, str]:
    base = _base(lemma)
    return _forms(
        {
            (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): base + "īḥ",
            (Case.NOMINATIVE, GrammaticalNumber.DUAL): base + "ī",
            (Case.NOMINATIVE, GrammaticalNumber.PLURAL): base + "yaḥ",
            (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): base + "īm",
            (Case.ACCUSATIVE, GrammaticalNumber.DUAL): base + "ī",
            (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): base + "īḥ",
            (Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR): base + "yā",
            (Case.INSTRUMENTAL, GrammaticalNumber.DUAL): base + "ibhyām",
            (Case.INSTRUMENTAL, GrammaticalNumber.PLURAL): base + "ibhiḥ",
            (Case.DATIVE, GrammaticalNumber.SINGULAR): base + "yai",
            (Case.DATIVE, GrammaticalNumber.DUAL): base + "ibhyām",
            (Case.DATIVE, GrammaticalNumber.PLURAL): base + "ibhyas",
            (Case.ABLATIVE, GrammaticalNumber.SINGULAR): base + "yāḥ",
            (Case.ABLATIVE, GrammaticalNumber.DUAL): base + "ibhyām",
            (Case.ABLATIVE, GrammaticalNumber.PLURAL): base + "ibhyas",
            (Case.GENITIVE, GrammaticalNumber.SINGULAR): base + "yāḥ",
            (Case.GENITIVE, GrammaticalNumber.DUAL): base + "yoḥ",
            (Case.GENITIVE, GrammaticalNumber.PLURAL): base + "īnām",
            (Case.LOCATIVE, GrammaticalNumber.SINGULAR): base + "yām",
            (Case.LOCATIVE, GrammaticalNumber.DUAL): base + "yoḥ",
            (Case.LOCATIVE, GrammaticalNumber.PLURAL): base + "iṣu",
            (Case.VOCATIVE, GrammaticalNumber.SINGULAR): base + "i",
            (Case.VOCATIVE, GrammaticalNumber.DUAL): base + "ī",
            (Case.VOCATIVE, GrammaticalNumber.PLURAL): base + "yaḥ",
        }
    )


def decline_u_masculine(lemma: str) -> dict[CaseNumber, str]:
    base = _base(lemma)
    return _forms(
        {
            (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): base + "uḥ",
            (Case.NOMINATIVE, GrammaticalNumber.DUAL): base + "ū",
            (Case.NOMINATIVE, GrammaticalNumber.PLURAL): base + "avaḥ",
            (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): base + "um",
            (Case.ACCUSATIVE, GrammaticalNumber.DUAL): base + "ū",
            (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): base + "ūn",
            (Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR): base + "unā",
            (Case.INSTRUMENTAL, GrammaticalNumber.DUAL): base + "ubhyām",
            (Case.INSTRUMENTAL, GrammaticalNumber.PLURAL): base + "ubhiḥ",
            (Case.DATIVE, GrammaticalNumber.SINGULAR): base + "ave",
            (Case.DATIVE, GrammaticalNumber.DUAL): base + "ubhyām",
            (Case.DATIVE, GrammaticalNumber.PLURAL): base + "ubhyas",
            (Case.ABLATIVE, GrammaticalNumber.SINGULAR): base + "oḥ",
            (Case.ABLATIVE, GrammaticalNumber.DUAL): base + "ubhyām",
            (Case.ABLATIVE, GrammaticalNumber.PLURAL): base + "ubhyas",
            (Case.GENITIVE, GrammaticalNumber.SINGULAR): base + "oḥ",
            (Case.GENITIVE, GrammaticalNumber.DUAL): base + "voḥ",
            (Case.GENITIVE, GrammaticalNumber.PLURAL): base + "ūnām",
            (Case.LOCATIVE, GrammaticalNumber.SINGULAR): base + "au",
            (Case.LOCATIVE, GrammaticalNumber.DUAL): base + "voḥ",
            (Case.LOCATIVE, GrammaticalNumber.PLURAL): base + "uṣu",
            (Case.VOCATIVE, GrammaticalNumber.SINGULAR): base + "o",
            (Case.VOCATIVE, GrammaticalNumber.DUAL): base + "ū",
            (Case.VOCATIVE, GrammaticalNumber.PLURAL): base + "avaḥ",
        }
    )


def decline_u_neuter(lemma: str) -> dict[CaseNumber, str]:
    forms = decline_u_masculine(lemma)
    base = _base(lemma)
    forms.update(
        {
            (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): lemma,
            (Case.NOMINATIVE, GrammaticalNumber.PLURAL): base + "ūni",
            (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): lemma,
            (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): base + "ūni",
            (Case.VOCATIVE, GrammaticalNumber.SINGULAR): lemma,
            (Case.VOCATIVE, GrammaticalNumber.PLURAL): base + "ūni",
        }
    )
    return forms


def decline_uu_feminine(lemma: str) -> dict[CaseNumber, str]:
    """Long ū-stem feminine (vadhū, etc.)."""
    base = _base(lemma)
    return _forms(
        {
            (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): base + "ūḥ",
            (Case.NOMINATIVE, GrammaticalNumber.DUAL): base + "ū",
            (Case.NOMINATIVE, GrammaticalNumber.PLURAL): base + "uvaḥ",
            (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): base + "ūm",
            (Case.ACCUSATIVE, GrammaticalNumber.DUAL): base + "ū",
            (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): base + "ūḥ",
            (Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR): base + "vā",
            (Case.INSTRUMENTAL, GrammaticalNumber.DUAL): base + "ubhyām",
            (Case.INSTRUMENTAL, GrammaticalNumber.PLURAL): base + "ubhiḥ",
            (Case.DATIVE, GrammaticalNumber.SINGULAR): base + "vai",
            (Case.DATIVE, GrammaticalNumber.DUAL): base + "ubhyām",
            (Case.DATIVE, GrammaticalNumber.PLURAL): base + "ubhyas",
            (Case.ABLATIVE, GrammaticalNumber.SINGULAR): base + "vāḥ",
            (Case.ABLATIVE, GrammaticalNumber.DUAL): base + "ubhyām",
            (Case.ABLATIVE, GrammaticalNumber.PLURAL): base + "ubhyas",
            (Case.GENITIVE, GrammaticalNumber.SINGULAR): base + "vāḥ",
            (Case.GENITIVE, GrammaticalNumber.DUAL): base + "voḥ",
            (Case.GENITIVE, GrammaticalNumber.PLURAL): base + "ūnām",
            (Case.LOCATIVE, GrammaticalNumber.SINGULAR): base + "vām",
            (Case.LOCATIVE, GrammaticalNumber.DUAL): base + "voḥ",
            (Case.LOCATIVE, GrammaticalNumber.PLURAL): base + "uṣu",
            (Case.VOCATIVE, GrammaticalNumber.SINGULAR): base + "u",
            (Case.VOCATIVE, GrammaticalNumber.DUAL): base + "ū",
            (Case.VOCATIVE, GrammaticalNumber.PLURAL): base + "uvaḥ",
        }
    )


def decline_r_masculine(lemma: str) -> dict[CaseNumber, str]:
    base = _base(lemma)
    weak = base + "r"
    strong = base + "ar"
    nom_sg = base + "ā"
    return _forms(
        {
            (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): nom_sg,
            (Case.NOMINATIVE, GrammaticalNumber.DUAL): strong + "au",
            (Case.NOMINATIVE, GrammaticalNumber.PLURAL): strong + "aḥ",
            (Case.VOCATIVE, GrammaticalNumber.SINGULAR): base + "aḥ",
            (Case.VOCATIVE, GrammaticalNumber.DUAL): strong + "au",
            (Case.VOCATIVE, GrammaticalNumber.PLURAL): strong + "aḥ",
            (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): strong + "am",
            (Case.ACCUSATIVE, GrammaticalNumber.DUAL): strong + "au",
            (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): strong + "aḥ",
            (Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR): weak + "ā",
            (Case.INSTRUMENTAL, GrammaticalNumber.DUAL): weak + "bhyām",
            (Case.INSTRUMENTAL, GrammaticalNumber.PLURAL): weak + "bhiḥ",
            (Case.DATIVE, GrammaticalNumber.SINGULAR): weak + "e",
            (Case.DATIVE, GrammaticalNumber.DUAL): weak + "bhyām",
            (Case.DATIVE, GrammaticalNumber.PLURAL): weak + "bhyas",
            (Case.ABLATIVE, GrammaticalNumber.SINGULAR): base + "uḥ",
            (Case.ABLATIVE, GrammaticalNumber.DUAL): weak + "bhyām",
            (Case.ABLATIVE, GrammaticalNumber.PLURAL): weak + "bhyas",
            (Case.GENITIVE, GrammaticalNumber.SINGULAR): base + "uḥ",
            (Case.GENITIVE, GrammaticalNumber.DUAL): weak + "oḥ",
            (Case.GENITIVE, GrammaticalNumber.PLURAL): weak + "ām",
            (Case.LOCATIVE, GrammaticalNumber.SINGULAR): base + "ari",
            (Case.LOCATIVE, GrammaticalNumber.DUAL): weak + "oḥ",
            (Case.LOCATIVE, GrammaticalNumber.PLURAL): weak + "su",
        }
    )


def decline_rr_feminine(lemma: str) -> dict[CaseNumber, str]:
    return decline_r_masculine(lemma)


def decline_l_stem(lemma: str) -> dict[CaseNumber, str]:
    if lemma.endswith("ḷ"):
        return decline_r_masculine(lemma[:-1] + "ṛ")
    return decline_r_masculine(lemma)


def decline_e_stem(lemma: str) -> dict[CaseNumber, str]:
    base = _base(lemma)
    return _forms(
        {
            (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): base + "eḥ",
            (Case.NOMINATIVE, GrammaticalNumber.DUAL): base + "ī",
            (Case.NOMINATIVE, GrammaticalNumber.PLURAL): base + "ayaḥ",
            (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): base + "em",
            (Case.ACCUSATIVE, GrammaticalNumber.DUAL): base + "ī",
            (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): base + "īn",
            (Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR): base + "inā",
            (Case.INSTRUMENTAL, GrammaticalNumber.DUAL): base + "ibhyām",
            (Case.INSTRUMENTAL, GrammaticalNumber.PLURAL): base + "ibhiḥ",
            (Case.DATIVE, GrammaticalNumber.SINGULAR): base + "aye",
            (Case.DATIVE, GrammaticalNumber.DUAL): base + "ibhyām",
            (Case.DATIVE, GrammaticalNumber.PLURAL): base + "ibhyas",
            (Case.ABLATIVE, GrammaticalNumber.SINGULAR): base + "eḥ",
            (Case.ABLATIVE, GrammaticalNumber.DUAL): base + "ibhyām",
            (Case.ABLATIVE, GrammaticalNumber.PLURAL): base + "ibhyas",
            (Case.GENITIVE, GrammaticalNumber.SINGULAR): base + "eḥ",
            (Case.GENITIVE, GrammaticalNumber.DUAL): base + "yoḥ",
            (Case.GENITIVE, GrammaticalNumber.PLURAL): base + "īnām",
            (Case.LOCATIVE, GrammaticalNumber.SINGULAR): base + "au",
            (Case.LOCATIVE, GrammaticalNumber.DUAL): base + "yoḥ",
            (Case.LOCATIVE, GrammaticalNumber.PLURAL): base + "iṣu",
            (Case.VOCATIVE, GrammaticalNumber.SINGULAR): lemma,
            (Case.VOCATIVE, GrammaticalNumber.DUAL): base + "ī",
            (Case.VOCATIVE, GrammaticalNumber.PLURAL): base + "ayaḥ",
        }
    )


def decline_ai_stem(lemma: str) -> dict[CaseNumber, str]:
    base = _base(lemma, strip=2)
    return _forms(
        {
            (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): base + "aiḥ",
            (Case.NOMINATIVE, GrammaticalNumber.DUAL): base + "ai",
            (Case.NOMINATIVE, GrammaticalNumber.PLURAL): base + "ayaḥ",
            (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): base + "aim",
            (Case.ACCUSATIVE, GrammaticalNumber.DUAL): base + "ai",
            (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): base + "īn",
            (Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR): base + "inā",
            (Case.INSTRUMENTAL, GrammaticalNumber.DUAL): base + "ibhyām",
            (Case.INSTRUMENTAL, GrammaticalNumber.PLURAL): base + "ibhiḥ",
            (Case.DATIVE, GrammaticalNumber.SINGULAR): base + "aye",
            (Case.DATIVE, GrammaticalNumber.DUAL): base + "ibhyām",
            (Case.DATIVE, GrammaticalNumber.PLURAL): base + "ibhyas",
            (Case.ABLATIVE, GrammaticalNumber.SINGULAR): base + "eḥ",
            (Case.ABLATIVE, GrammaticalNumber.DUAL): base + "ibhyām",
            (Case.ABLATIVE, GrammaticalNumber.PLURAL): base + "ibhyas",
            (Case.GENITIVE, GrammaticalNumber.SINGULAR): base + "eḥ",
            (Case.GENITIVE, GrammaticalNumber.DUAL): base + "yoḥ",
            (Case.GENITIVE, GrammaticalNumber.PLURAL): base + "īnām",
            (Case.LOCATIVE, GrammaticalNumber.SINGULAR): base + "au",
            (Case.LOCATIVE, GrammaticalNumber.DUAL): base + "yoḥ",
            (Case.LOCATIVE, GrammaticalNumber.PLURAL): base + "iṣu",
            (Case.VOCATIVE, GrammaticalNumber.SINGULAR): lemma,
            (Case.VOCATIVE, GrammaticalNumber.DUAL): base + "ai",
            (Case.VOCATIVE, GrammaticalNumber.PLURAL): base + "ayaḥ",
        }
    )


def decline_o_masculine(lemma: str) -> dict[CaseNumber, str]:
    base = _base(lemma)
    return _forms(
        {
            (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): base + "oḥ",
            (Case.NOMINATIVE, GrammaticalNumber.DUAL): base + "ū",
            (Case.NOMINATIVE, GrammaticalNumber.PLURAL): base + "avaḥ",
            (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): base + "om",
            (Case.ACCUSATIVE, GrammaticalNumber.DUAL): base + "ū",
            (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): base + "ūn",
            (Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR): base + "onā",
            (Case.INSTRUMENTAL, GrammaticalNumber.DUAL): base + "obhyām",
            (Case.INSTRUMENTAL, GrammaticalNumber.PLURAL): base + "obhiḥ",
            (Case.DATIVE, GrammaticalNumber.SINGULAR): base + "ave",
            (Case.DATIVE, GrammaticalNumber.DUAL): base + "obhyām",
            (Case.DATIVE, GrammaticalNumber.PLURAL): base + "obhyas",
            (Case.ABLATIVE, GrammaticalNumber.SINGULAR): base + "oḥ",
            (Case.ABLATIVE, GrammaticalNumber.DUAL): base + "obhyām",
            (Case.ABLATIVE, GrammaticalNumber.PLURAL): base + "obhyas",
            (Case.GENITIVE, GrammaticalNumber.SINGULAR): base + "oḥ",
            (Case.GENITIVE, GrammaticalNumber.DUAL): base + "voḥ",
            (Case.GENITIVE, GrammaticalNumber.PLURAL): base + "ūnām",
            (Case.LOCATIVE, GrammaticalNumber.SINGULAR): base + "au",
            (Case.LOCATIVE, GrammaticalNumber.DUAL): base + "voḥ",
            (Case.LOCATIVE, GrammaticalNumber.PLURAL): base + "uṣu",
            (Case.VOCATIVE, GrammaticalNumber.SINGULAR): lemma,
            (Case.VOCATIVE, GrammaticalNumber.DUAL): base + "ū",
            (Case.VOCATIVE, GrammaticalNumber.PLURAL): base + "avaḥ",
        }
    )


def decline_au_stem(lemma: str) -> dict[CaseNumber, str]:
    base = _base(lemma, strip=2)
    return _forms(
        {
            (Case.NOMINATIVE, GrammaticalNumber.SINGULAR): base + "auḥ",
            (Case.NOMINATIVE, GrammaticalNumber.DUAL): base + "au",
            (Case.NOMINATIVE, GrammaticalNumber.PLURAL): base + "avaḥ",
            (Case.ACCUSATIVE, GrammaticalNumber.SINGULAR): base + "aum",
            (Case.ACCUSATIVE, GrammaticalNumber.DUAL): base + "au",
            (Case.ACCUSATIVE, GrammaticalNumber.PLURAL): base + "ūn",
            (Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR): base + "unā",
            (Case.INSTRUMENTAL, GrammaticalNumber.DUAL): base + "ubhyām",
            (Case.INSTRUMENTAL, GrammaticalNumber.PLURAL): base + "ubhiḥ",
            (Case.DATIVE, GrammaticalNumber.SINGULAR): base + "ave",
            (Case.DATIVE, GrammaticalNumber.DUAL): base + "ubhyām",
            (Case.DATIVE, GrammaticalNumber.PLURAL): base + "ubhyas",
            (Case.ABLATIVE, GrammaticalNumber.SINGULAR): base + "oḥ",
            (Case.ABLATIVE, GrammaticalNumber.DUAL): base + "ubhyām",
            (Case.ABLATIVE, GrammaticalNumber.PLURAL): base + "ubhyas",
            (Case.GENITIVE, GrammaticalNumber.SINGULAR): base + "oḥ",
            (Case.GENITIVE, GrammaticalNumber.DUAL): base + "voḥ",
            (Case.GENITIVE, GrammaticalNumber.PLURAL): base + "ūnām",
            (Case.LOCATIVE, GrammaticalNumber.SINGULAR): base + "au",
            (Case.LOCATIVE, GrammaticalNumber.DUAL): base + "voḥ",
            (Case.LOCATIVE, GrammaticalNumber.PLURAL): base + "uṣu",
            (Case.VOCATIVE, GrammaticalNumber.SINGULAR): lemma,
            (Case.VOCATIVE, GrammaticalNumber.DUAL): base + "au",
            (Case.VOCATIVE, GrammaticalNumber.PLURAL): base + "avaḥ",
        }
    )


__all__ = [
    "decline_ai_stem",
    "decline_au_stem",
    "decline_e_stem",
    "decline_i_masculine",
    "decline_i_neuter",
    "decline_ii_feminine",
    "decline_l_stem",
    "decline_o_masculine",
    "decline_r_masculine",
    "decline_rr_feminine",
    "decline_u_masculine",
    "decline_u_neuter",
    "decline_uu_feminine",
]
