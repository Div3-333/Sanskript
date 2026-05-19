from __future__ import annotations

from .anga import DerivationContext, Suffix
from .grammar import Analysis, Gender, PartOfSpeech
from .phonology import is_aprkta
from .samasa import apply_ekashesha


def _markers(context) -> frozenset[str]:
    return frozenset(context.get("markers", ()))


def _root(context) -> str:
    return str(context.get("root"))


def _analyses(context) -> list[Analysis]:
    return list(context.get("analyses", ()))


def sutra_1_2_1(context) -> bool:
    return DerivationContext(root_lemma=_root(context), suffix=Suffix("ta", markers=_markers(context))).get_is_ngit()


def sutra_1_2_2(context) -> bool:
    return DerivationContext(root_lemma=_root(context), suffix=Suffix("ta"), is_it_augment=bool(context.get("it"))).get_is_ngit()


def sutra_1_2_4(context) -> bool:
    return DerivationContext(suffix=Suffix("ti", markers=_markers(context), is_sarvadhatuka=True)).get_is_ngit()


def sutra_1_2_5(context) -> bool:
    return DerivationContext(root_lemma=_root(context), suffix=Suffix("liṭ", is_lit=True)).get_is_kit()


def sutra_1_2_6(context) -> bool:
    root = _root(context)
    return root in {"indh", "bhū"} and DerivationContext(root_lemma=root, suffix=Suffix("liṭ", is_lit=True)).get_is_kit()


def sutra_1_2_7(context) -> bool:
    return DerivationContext(root_lemma=_root(context), suffix=Suffix("ktvā", is_ktva=True)).get_is_kit()


def sutra_1_2_8(context) -> bool:
    return DerivationContext(
        root_lemma=_root(context),
        suffix=Suffix("san", is_san=True),
        is_it_augment=bool(context.get("it")),
    ).get_is_kit()


def sutra_1_2_9(context) -> bool:
    return DerivationContext(root_lemma=_root(context), suffix=Suffix("sa", is_san=True)).get_is_kit()


def sutra_1_2_11(context) -> bool:
    return DerivationContext(
        root_lemma=_root(context),
        suffix=Suffix("sic", is_sic=True, is_atmanepada=bool(context.get("atmanepada"))),
    ).get_is_kit()


def sutra_1_2_12(context) -> bool:
    root = _root(context)
    return root.endswith("ṛ") and DerivationContext(
        root_lemma=root,
        suffix=Suffix("sic", is_sic=True, is_atmanepada=True),
    ).get_is_kit()


def _sic_root_is_kit(context, expected: str) -> bool:
    root = _root(context)
    return root == expected and DerivationContext(
        root_lemma=root,
        suffix=Suffix("sic", is_sic=True, is_atmanepada=True),
    ).get_is_kit()


def sutra_1_2_13(context) -> bool:
    return _sic_root_is_kit(context, "gam")


def sutra_1_2_14(context) -> bool:
    return _sic_root_is_kit(context, "han")


def sutra_1_2_15(context) -> bool:
    return _sic_root_is_kit(context, "yam")


def sutra_1_2_17(context) -> bool:
    return _sic_root_is_kit(context, "sthā")


def sutra_1_2_18(context) -> bool:
    return not DerivationContext(
        root_lemma=_root(context),
        suffix=Suffix("ktvā", is_ktva=True),
        is_it_augment=bool(context.get("it")),
    ).get_is_kit()


def _nistha_root_blocks_kit(context, expected: str) -> bool:
    root = _root(context)
    return root == expected and not DerivationContext(
        root_lemma=root,
        suffix=Suffix("kta", is_nistha=True),
        is_it_augment=True,
    ).get_is_kit()


def sutra_1_2_19(context) -> bool:
    return _nistha_root_blocks_kit(context, "śīṅ")


def sutra_1_2_20(context) -> bool:
    return _nistha_root_blocks_kit(context, "mṛṣ")


def sutra_1_2_26(context) -> bool:
    return DerivationContext(root_lemma=_root(context), suffix=Suffix("san", is_san=True), is_it_augment=True).get_is_kit()


def sutra_1_2_41(context) -> bool:
    return is_aprkta(context.get("analysis"))


def sutra_1_2_64(context) -> bool:
    analyses = _analyses(context)
    return len({analysis.surface for analysis in analyses}) == 1 and apply_ekashesha(analyses).lemma == context.get("lemma")


def sutra_1_2_65(context) -> bool:
    return apply_ekashesha(_analyses(context)).lemma == "arya"


def sutra_1_2_67(context) -> bool:
    return apply_ekashesha(_analyses(context)).gender == Gender.MASCULINE


def sutra_1_2_68(context) -> bool:
    return apply_ekashesha(_analyses(context)).lemma == context.get("lemma")


def sutra_1_2_69(context) -> bool:
    return apply_ekashesha(_analyses(context)).gender == Gender.NEUTER


def sutra_1_2_70(context) -> bool:
    return apply_ekashesha(_analyses(context)).lemma == "pitṛ"


def sutra_1_2_71(context) -> bool:
    return apply_ekashesha(_analyses(context)).lemma == "śvaśura"


def sutra_1_2_72(context) -> bool:
    return apply_ekashesha(_analyses(context)).lemma == "tad"


def sutra_1_2_73(context) -> bool:
    return apply_ekashesha(_analyses(context)).gender == Gender.FEMININE


def simple_analysis(surface: str, lemma: str | None = None, gender: Gender | None = None) -> Analysis:
    return Analysis(surface, lemma or surface, PartOfSpeech.NOUN, gender=gender)
