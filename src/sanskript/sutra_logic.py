from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any

from . import sutra_handlers_1_2 as h12
from .anga import DerivationContext, Suffix, guna, operations_for_range, vrddhi
from .avyaya import is_avyaya_suffix, is_controlled_avyaya, upasarga_surfaces
from .categories import (
    assign_technical_names,
    get_vowel_weight,
    has_single_sound_boundary,
    is_avasana,
    is_gha_suffix,
    is_ghu_root,
    is_nistha_suffix,
    is_pada,
    is_samhita,
    is_sankhya_term,
    is_sarvanama_stem,
    is_sarvanamasthana_suffix,
    is_shat_numeral,
)
from .accent import Accent, profile_accent
from .derivation import KrtSuffix, TaddhitaSuffix, derive
from .grammar import Analysis, Case, Gender, GrammaticalNumber, Lakara, Pada, PartOfSpeech, Person, Role, Samjna
from .karaka import get_karaka_role, get_vibhakti
from .markers import analyze_it_markers
from .metarules import (
    augment_boundary,
    default_final_substitution_index,
    following_initial_substitution_index,
    genitive_marks_substitution_site,
    is_vibhasha_expression,
    mid_augment_index,
    whole_term_replacement_applies,
)
from .phonology import (
    best_substitute,
    guna_replacement_for_ik,
    hrasva_substitute_for_ec,
    is_anunasika,
    is_consonant,
    is_guna,
    is_ik,
    is_pragrhya,
    is_aprkta,
    is_samyoga,
    is_savarna,
    is_ti,
    is_upadha,
    is_vowel,
    is_vrddha_word,
    is_vrddhi,
    pratyahara,
    rapara_substitute_for_ur,
    savarna_reference,
    tapara_matches_duration,
    vrddhi_replacement_for_ik,
)
from .samasa import SamasaSense, SamasaType, apply_ekashesha, create_compound, is_samartha
from .sandhi import join_words
from .subanta import decline_aa_feminine
from .tinanta import (
    Dhatu,
    DhatuType,
    TimeContext,
    TinEnding,
    apply_luk_elision,
    create_derived_dhatu,
    get_lakara_for_time,
    get_substituted_dhatu,
    get_vikarana,
    is_ardhadhatuka,
    is_sarvadhatuka,
    join_stem_ending,
    tin_ending,
)
from .transliteration import devanagari_to_iast
from .voice import determine_available_padas


SOURCE_URL = "https://sanskritdocuments.org/~sanskrit/learning_tools/ashtadhyayi/"


class SutraOperator(str, Enum):
    ADHIKARA = "adhikara"
    ATIDESA = "atidesa"
    SAMJNA = "samjna"
    PARIBHASHA = "paribhasha"
    VIBHASHA = "vibhasha"
    PRATISEDHA = "pratisedha"
    VIDHI = "vidhi"


@dataclass(frozen=True)
class SutraRecord:
    id: str
    sutra_krama: str
    rule_type: str
    term: str
    special_case: str
    influence: str
    sutra_text_devanagari: str
    sutra_text_iast: str
    padaccheda: str
    source: str
    source_url: str

    @property
    def pada(self) -> str:
        return self.id.rsplit(".", 1)[0]


@dataclass(frozen=True)
class SutraContext:
    features: Mapping[str, Any]
    domain: str = "*"
    sutra_id: str | None = None

    def get(self, name: str, default: Any = None) -> Any:
        return self.features.get(name, default)


@dataclass(frozen=True)
class SutraDecision:
    sutra_id: str
    applies: bool
    operator: SutraOperator
    action: str
    assigned: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class DiscreteSutraLogic:
    sutra_id: str
    operator: SutraOperator
    summary: str
    evaluator: Callable[[SutraContext], bool]
    positive: SutraContext
    negative: SutraContext
    assigned: tuple[str, ...]


def canon_data_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "ashtadhyayi_sutras.json"


@lru_cache(maxsize=1)
def sutra_records() -> dict[str, SutraRecord]:
    records: dict[str, SutraRecord] = {}
    data = json.loads(canon_data_path().read_text(encoding="utf-8"))
    for item in data:
        sutra_id = item["id"]
        text = item["sutra_text_devanagari"].strip()
        records[sutra_id] = SutraRecord(
            id=sutra_id,
            sutra_krama=item["sutra_krama"],
            rule_type=item["rule_type"].strip(),
            term=item["term"].strip(),
            special_case=item["special_case"].strip(),
            influence=item["influence"].strip(),
            sutra_text_devanagari=text,
            sutra_text_iast=devanagari_to_iast(text).replace(" ।", "").strip(),
            padaccheda=item["padaccheda"].strip(),
            source=item["source"],
            source_url=item["source_url"],
        )
    return records


def sutra_record(sutra_id: str) -> SutraRecord:
    try:
        return sutra_records()[sutra_id]
    except KeyError as exc:
        raise ValueError(f"No canonical sutra record for {sutra_id!r}") from exc


def implemented_logic_ids() -> frozenset[str]:
    return frozenset(SUTRA_LOGIC)


def has_discrete_sutra_logic(sutra_id: str) -> bool:
    return sutra_id in SUTRA_LOGIC


def positive_context_for(sutra_id: str) -> SutraContext:
    return _logic_for(sutra_id).positive


def negative_context_for(sutra_id: str) -> SutraContext:
    return _logic_for(sutra_id).negative


def atomic_evidence_for(sutra_id: str) -> dict[str, object]:
    logic = _logic_for(sutra_id)
    record = sutra_record(sutra_id)
    return {
        "sutra_text_devanagari": record.sutra_text_devanagari,
        "sutra_text_iast": record.sutra_text_iast,
        "source": f"{record.source}: {record.source_url}",
        "anuvritti": (record.influence or record.pada, record.rule_type or logic.operator.value),
        "conditions": (logic.summary,),
        "exceptions": (),
        "operation": logic.summary,
        "positive_example": f"{sutra_id}: {logic.positive.features}",
        "negative_example": f"{sutra_id}: {logic.negative.features}",
    }


def evaluate_sutra(sutra_id: str, context: SutraContext) -> SutraDecision:
    logic = _logic_for(sutra_id)
    if context.sutra_id is not None and context.sutra_id != sutra_id:
        return _reject(logic, "context names a different sutra")
    if context.domain not in {"*", sutra_id, sutra_id.rsplit(".", 1)[0]}:
        return _reject(logic, "domain mismatch")
    try:
        applies = logic.evaluator(context)
    except (KeyError, TypeError, ValueError):
        applies = False
    if not applies:
        return _reject(logic, "sutra-specific predicate rejected the context")
    return SutraDecision(
        sutra_id=sutra_id,
        applies=True,
        operator=logic.operator,
        action=logic.summary,
        assigned=logic.assigned,
        reason="sutra-specific executable predicate accepted the context",
    )


def _logic_for(sutra_id: str) -> DiscreteSutraLogic:
    try:
        return SUTRA_LOGIC[sutra_id]
    except KeyError as exc:
        raise ValueError(f"No real discrete sutra logic has been implemented for {sutra_id!r}") from exc


def _reject(logic: DiscreteSutraLogic, reason: str) -> SutraDecision:
    return SutraDecision(
        sutra_id=logic.sutra_id,
        applies=False,
        operator=logic.operator,
        action="reject",
        assigned=(),
        reason=reason,
    )


def _ctx(sutra_id: str, **features: Any) -> SutraContext:
    return SutraContext(features=features, domain=sutra_id.rsplit(".", 1)[0], sutra_id=sutra_id)


def _analysis(
    surface: str,
    lemma: str,
    pos: PartOfSpeech,
    *,
    case: Case | None = None,
    gender: Gender | None = None,
    number: GrammaticalNumber | None = None,
) -> Analysis:
    return Analysis(surface=surface, lemma=lemma, pos=pos, case=case, gender=gender, number=number)


def _compound_members(kind: str) -> list[Analysis]:
    if kind == "avyayibhava":
        return [
            Analysis("upa", "upa", PartOfSpeech.INDECLINABLE),
            _analysis("gramam", "grama", PartOfSpeech.NOUN, case=Case.ACCUSATIVE, gender=Gender.MASCULINE),
        ]
    return [
        _analysis("devasya", "deva", PartOfSpeech.NOUN, case=Case.GENITIVE, gender=Gender.MASCULINE),
        _analysis("purusah", "purusa", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.MASCULINE),
    ]


def _compound_from_case(case: Case) -> list[Analysis]:
    return [
        _analysis("deva", "deva", PartOfSpeech.NOUN, case=case, gender=Gender.MASCULINE),
        _analysis("purusah", "purusa", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.MASCULINE),
    ]


def _avyayibhava_members(indeclinable: str, second: str = "grama", case: Case = Case.ACCUSATIVE) -> list[Analysis]:
    return [
        Analysis(indeclinable, indeclinable, PartOfSpeech.INDECLINABLE),
        _analysis(second, second, PartOfSpeech.NOUN, case=case, gender=Gender.MASCULINE),
    ]


def _compound_pair(
    left: str,
    right: str,
    *,
    left_case: Case | None = None,
    right_case: Case | None = Case.NOMINATIVE,
    left_pos: PartOfSpeech = PartOfSpeech.NOUN,
    right_pos: PartOfSpeech = PartOfSpeech.NOUN,
    left_value: int | None = None,
) -> list[Analysis]:
    return [
        Analysis(left, left, left_pos, case=left_case, gender=Gender.MASCULINE, value=left_value),
        Analysis(right, right, right_pos, case=right_case, gender=Gender.MASCULINE),
    ]


def _numeral_compound() -> list[Analysis]:
    return [
        Analysis("panca", "pancan", PartOfSpeech.NUMERAL, case=Case.ACCUSATIVE, value=5),
        _analysis("phalani", "phala", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.NEUTER),
    ]


def _dvandva_members() -> list[Analysis]:
    return [
        _analysis("ramah", "rama", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.MASCULINE),
        _analysis("sita", "sita", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.FEMININE),
    ]


def _basic_dhatu(lemma: str = "bhū", stem: str = "bhava", pada: Pada = Pada.PARASMAIPADA) -> Dhatu:
    return Dhatu(lemma, stem, pada, "test root")


def _add(
    registry: dict[str, DiscreteSutraLogic],
    sutra_id: str,
    operator: SutraOperator,
    summary: str,
    evaluator: Callable[[SutraContext], bool],
    positive: SutraContext,
    negative: SutraContext,
    *assigned: str,
) -> None:
    registry[sutra_id] = DiscreteSutraLogic(
        sutra_id=sutra_id,
        operator=operator,
        summary=summary,
        evaluator=evaluator,
        positive=positive,
        negative=negative,
        assigned=(f"sutra:{sutra_id}", *assigned),
    )



# Named sutra handlers for executable predicates.
def sutra_1_1_1(c) -> bool:
    return is_vrddhi(str(c.get("sound")))

def sutra_1_1_2(c) -> bool:
    return is_guna(str(c.get("sound")))

def sutra_1_1_3(c) -> bool:
    return is_ik(str(c.get("sound"))) and guna_replacement_for_ik(str(c.get("sound"))) and vrddhi_replacement_for_ik(str(c.get("sound")))

def sutra_1_1_4(c) -> bool:
    return guna("i", DerivationContext(suffix=Suffix("ta", is_ardhadhatuka=bool(c.get("ardhadhatuka"))), has_dhatu_lopa=bool(c.get("dhatu_lopa")))) == "i"

def sutra_1_1_5(c) -> bool:
    return guna("i", DerivationContext(suffix=Suffix("ta", markers=frozenset({str(c.get("marker"))})))) == "i"

def sutra_1_1_6(c) -> bool:
    return guna("i", DerivationContext(root_lemma=str(c.get("root")), is_it_augment=bool(c.get("it_augment")), suffix=Suffix("ta"))) == "i"

def sutra_1_1_7(c) -> bool:
    return is_samyoga(list(c.get("sounds", ())))

def sutra_1_1_8(c) -> bool:
    return is_anunasika(str(c.get("sound")))

def sutra_1_1_9(c) -> bool:
    return is_savarna(str(c.get("left")), str(c.get("right")))

def sutra_1_1_10(c) -> bool:
    return is_vowel(str(c.get("left"))) != is_vowel(str(c.get("right"))) and not is_savarna(str(c.get("left")), str(c.get("right")))

def sutra_1_1_11(c) -> bool:
    return is_pragrhya(c.get("analysis"))

def sutra_1_1_12(c) -> bool:
    return is_pragrhya(c.get("analysis"))

def sutra_1_1_15(c) -> bool:
    return is_pragrhya(str(c.get("token")))

def sutra_1_1_19(c) -> bool:
    return is_pragrhya(c.get("analysis"))

def sutra_1_1_20(c) -> bool:
    return is_ghu_root(str(c.get("root")))

def sutra_1_1_21(c) -> bool:
    return has_single_sound_boundary(str(c.get("term")))

def sutra_1_1_22(c) -> bool:
    return is_gha_suffix(str(c.get("suffix")))

def sutra_1_1_23(c) -> bool:
    return is_sankhya_term(str(c.get("term")))

def sutra_1_1_24(c) -> bool:
    return is_shat_numeral(str(c.get("term"))) and str(c.get("term")) != "ḍati"

def sutra_1_1_25(c) -> bool:
    return is_shat_numeral(str(c.get("term"))) and str(c.get("term")) == "ḍati"

def sutra_1_1_26(c) -> bool:
    return is_nistha_suffix(str(c.get("suffix")))

def sutra_1_1_27(c) -> bool:
    return is_sarvanama_stem(str(c.get("stem")))

def sutra_1_1_37(c) -> bool:
    return is_controlled_avyaya(str(c.get("surface")))

def sutra_1_1_40(c) -> bool:
    return is_avyaya_suffix(str(c.get("suffix")))

def sutra_1_1_41(c) -> bool:
    return create_compound(_compound_members(str(c.get("compound")))).type == SamasaType.AVYAYIBHAVA

def sutra_1_1_42(c) -> bool:
    return is_sarvanamasthana_suffix(str(c.get("suffix")))

def sutra_1_1_43(c) -> bool:
    return is_sarvanamasthana_suffix(str(c.get("suffix")), c.get("gender"))

def sutra_1_1_44(c) -> bool:
    return is_vibhasha_expression(str(c.get("text")))

def sutra_1_1_46(c) -> bool:
    return augment_boundary(str(c.get("marker"))) == c.get("boundary")

def sutra_1_1_47(c) -> bool:
    return mid_augment_index(str(c.get("base"))) == c.get("index")

def sutra_1_1_48(c) -> bool:
    return hrasva_substitute_for_ec(str(c.get("sound"))) == c.get("replacement")

def sutra_1_1_49(c) -> bool:
    return genitive_marks_substitution_site(str(c.get("case")))

def sutra_1_1_50(c) -> bool:
    return best_substitute(str(c.get("target")), tuple(c.get("candidates", ()))) == c.get("expected")

def sutra_1_1_51(c) -> bool:
    return rapara_substitute_for_ur(str(c.get("target")), str(c.get("replacement"))) == c.get("expected")

def sutra_1_1_52(c) -> bool:
    return default_final_substitution_index(str(c.get("term"))) == c.get("index")

def sutra_1_1_53(c) -> bool:
    return whole_term_replacement_applies(str(c.get("substitute")), str(c.get("marker")))

def sutra_1_1_54(c) -> bool:
    return following_initial_substitution_index(str(c.get("term"))) == c.get("index")

def sutra_1_1_55(c) -> bool:
    return whole_term_replacement_applies(str(c.get("substitute")), str(c.get("marker")))

def sutra_1_1_64(c) -> bool:
    return is_ti(str(c.get("word"))) == c.get("ti")

def sutra_1_1_65(c) -> bool:
    return is_upadha(str(c.get("word"))) == c.get("upadha")

def sutra_1_1_69(c) -> bool:
    return bool(savarna_reference(str(c.get("sound")), bool(c.get("is_pratyaya"))))

def sutra_1_1_70(c) -> bool:
    return tapara_matches_duration(str(c.get("sound")), str(c.get("candidate")))

def sutra_1_1_71(c) -> bool:
    return tuple(pratyahara(str(c.get("name")))) == tuple(c.get("sounds", ()))

def sutra_1_1_73(c) -> bool:
    return is_vrddha_word(str(c.get("word")))

def sutra_1_1_74(c) -> bool:
    return is_vrddha_word(str(c.get("word")), tyadadi=bool(c.get("tyadadi")))

def sutra_1_1_75(c) -> bool:
    return is_vrddha_word(str(c.get("word")), eastern_name=bool(c.get("eastern_name")))

def sutra_1_3_4(c) -> bool:
    return not analyze_it_markers(str(c.get("upadesha")), str(c.get("kind", "vibhakti"))).markers

def sutra_1_3_9(c) -> bool:
    return analyze_it_markers(str(c.get("upadesha")), str(c.get("kind", "suffix"))).lemma == c.get("lemma")

def sutra_1_4_3(c) -> bool:
    return Samjna.NADII in assign_technical_names(c.get("analysis")).samjnas

def sutra_1_4_7(c) -> bool:
    return Samjna.GHI in assign_technical_names(c.get("analysis")).samjnas

def sutra_1_4_10(c) -> bool:
    return get_vowel_weight(str(c.get("word")), int(c.get("index", 0))) == Samjna.LAGHU

def sutra_1_4_11(c) -> bool:
    return get_vowel_weight(str(c.get("word")), int(c.get("index", 0))) == Samjna.GURU

def sutra_1_4_12(c) -> bool:
    return get_vowel_weight(str(c.get("word")), int(c.get("index", 0))) == Samjna.GURU

def sutra_1_4_13(c) -> bool:
    return c.get("suffix") is not None and Samjna.ANGA in assign_technical_names(c.get("analysis"), str(c.get("suffix"))).samjnas

def sutra_1_4_14(c) -> bool:
    return is_pada(c.get("analysis"))

def sutra_1_4_17(c) -> bool:
    return Samjna.PADA in assign_technical_names(c.get("analysis"), str(c.get("suffix"))).samjnas

def sutra_1_4_18(c) -> bool:
    return Samjna.BHA in assign_technical_names(c.get("analysis"), str(c.get("suffix"))).samjnas

def sutra_1_4_58(c) -> bool:
    return str(c.get("prefix")) in upasarga_surfaces()

def sutra_1_4_59(c) -> bool:
    return str(c.get("prefix")) in upasarga_surfaces() and bool(c.get("verb_connection"))

def sutra_1_4_60(c) -> bool:
    return str(c.get("prefix")) in upasarga_surfaces() and bool(c.get("gati_relation"))

def sutra_1_4_109(c) -> bool:
    return is_samhita(str(c.get("word")))

def sutra_1_4_110(c) -> bool:
    return is_avasana(str(c.get("word")), int(c.get("index", 0)))

def sutra_1_3_78(c) -> bool:
    return Pada.PARASMAIPADA in determine_available_padas(c.get("markers", frozenset()), str(c.get("lemma")), tuple(c.get("prefixes", ())), bool(c.get("reflexive")))

def sutra_2_1_1(c) -> bool:
    return is_samartha(list(c.get("members", ())))

def sutra_2_1_4(c) -> bool:
    return create_compound(list(c.get("members", ()))).type != SamasaType.KEVALA

def sutra_2_1_5(c) -> bool:
    return create_compound(list(c.get("members", ()))).type == SamasaType.AVYAYIBHAVA

def sutra_2_1_6(c) -> bool:
    return create_compound(list(c.get("members", ()))).sense == SamasaSense.SAMIPA

def sutra_2_1_7(c) -> bool:
    return create_compound(list(c.get("members", ()))).sense == SamasaSense.YATHA

def sutra_2_1_8(c) -> bool:
    return create_compound(list(c.get("members", ()))).sense == SamasaSense.AVADHARANA

def sutra_2_1_9(c) -> bool:
    return create_compound(list(c.get("members", ()))).sense == SamasaSense.MATRA

def sutra_2_1_10(c) -> bool:
    return create_compound(list(c.get("members", ()))).sense == SamasaSense.PARINA

def sutra_2_1_11(c) -> bool:
    return bool(c.get("optional")) and create_compound(list(c.get("members", ()))).type == SamasaType.AVYAYIBHAVA

def sutra_2_1_12(c) -> bool:
    return create_compound(list(c.get("members", ()))).sense == SamasaSense.PANCAMI_AVYAYIBHAVA

def sutra_2_1_13(c) -> bool:
    return create_compound(list(c.get("members", ()))).sense == SamasaSense.MARYADA_ABHIVIDHI

def sutra_2_1_14(c) -> bool:
    return create_compound(list(c.get("members", ()))).sense == SamasaSense.ABHIMUKHYA

def sutra_2_1_15(c) -> bool:
    return create_compound(list(c.get("members", ()))).sense == SamasaSense.ANU_SAMAYA

def sutra_2_1_16(c) -> bool:
    return create_compound(list(c.get("members", ()))).sense == SamasaSense.AYAMA

def sutra_2_1_17(c) -> bool:
    return create_compound(list(c.get("members", ()))).sense == SamasaSense.LEXICAL_AVYAYIBHAVA

def sutra_2_1_18(c) -> bool:
    compound = create_compound(list(c.get("members", ())))
    return compound.is_optional and compound.sense == SamasaSense.SHASH_TAT

def sutra_2_1_19(c) -> bool:
    return create_compound(list(c.get("members", ()))).sense == SamasaSense.VAMSHYA

def sutra_2_1_20(c) -> bool:
    return create_compound(list(c.get("members", ()))).sense == SamasaSense.NADI

def sutra_2_1_21(c) -> bool:
    compound = create_compound(list(c.get("members", ())), forced_type=SamasaType.BAHUVRIHI)
    return bool(c.get("proper_name")) and compound.type == SamasaType.BAHUVRIHI

def sutra_2_1_22(c) -> bool:
    return create_compound(list(c.get("members", ()))).type == SamasaType.TATPURUSHA

def sutra_2_1_23(c) -> bool:
    return create_compound(list(c.get("members", ()))).type == SamasaType.DVIGU

def sutra_2_1_57(c) -> bool:
    return create_compound(list(c.get("members", ()))).type == SamasaType.KARMADHARAYA

def sutra_2_2_29(c) -> bool:
    return create_compound(list(c.get("members", ()))).type == SamasaType.DVANDVA

def sutra_2_2_30(c) -> bool:
    return create_compound(list(c.get("members", ()))).surface.startswith(str(c.get("first_lemma")))

def sutra_2_3_1(c) -> bool:
    return get_vibhakti(is_already_expressed=bool(c.get("expressed"))) == c.get("case")

def sutra_2_3_50(c) -> bool:
    return get_vibhakti(role=c.get("role")) == Case.GENITIVE

def sutra_2_4_1(c) -> bool:
    return create_compound(list(c.get("members", ()))).result_analysis.number == GrammaticalNumber.SINGULAR

def sutra_2_4_17(c) -> bool:
    return Samjna.AVYAYA in create_compound(list(c.get("members", ()))).result_analysis.samjnas

def sutra_2_4_18(c) -> bool:
    result = create_compound(list(c.get("members", ()))).result_analysis
    return result.gender == Gender.NEUTER and result.number == GrammaticalNumber.SINGULAR

def sutra_2_4_26(c) -> bool:
    return create_compound(list(c.get("members", ()))).result_analysis.gender == c.get("gender")

def sutra_2_4_71(c) -> bool:
    return create_compound(list(c.get("members", ()))).surface == c.get("surface")

def sutra_2_4_72(c) -> bool:
    return apply_luk_elision(_basic_dhatu(str(c.get("lemma")), str(c.get("lemma"))), TinEnding(Lakara.LAT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "ti"))

def sutra_3_2_123(c) -> bool:
    return c.get("time") == TimeContext.PRESENT and get_lakara_for_time(c.get("time")) == Lakara.LAT

def sutra_3_4_79(c) -> bool:
    return join_stem_ending(str(c.get("stem")), TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "ta")) == c.get("surface")

def sutra_3_4_80(c) -> bool:
    return join_stem_ending(str(c.get("stem")), TinEnding(Lakara.LAT, Pada.ATMANEPADA, Person.SECOND, GrammaticalNumber.SINGULAR, "thās")) == c.get("surface")

def sutra_3_4_86(c) -> bool:
    return join_stem_ending(str(c.get("stem")), TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "ti")) == c.get("surface")

def sutra_3_4_87(c) -> bool:
    return join_stem_ending(str(c.get("stem")), TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.SINGULAR, "si")) == c.get("surface")

def sutra_3_4_88(c) -> bool:
    return join_stem_ending(str(c.get("stem")), TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.SINGULAR, "si")) == c.get("surface")

def sutra_3_4_92(c) -> bool:
    return join_stem_ending(str(c.get("stem")), TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.FIRST, GrammaticalNumber.SINGULAR, "mi")) == c.get("surface")

def sutra_3_4_100(c) -> bool:
    return join_stem_ending(str(c.get("stem")), TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "ti")) == c.get("surface")

def sutra_3_4_101(c) -> bool:
    return join_stem_ending(str(c.get("stem")), TinEnding(Lakara.LOT, Pada.PARASMAIPADA, Person.SECOND, GrammaticalNumber.DUAL, "thaḥ")) == c.get("surface")

def sutra_3_4_108(c) -> bool:
    return join_stem_ending(str(c.get("stem")), TinEnding(Lakara.VIDHILING, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.PLURAL, "nti")) == c.get("surface")

def sutra_3_4_113(c) -> bool:
    return is_sarvadhatuka(c.get("lakara"))

def sutra_3_4_114(c) -> bool:
    return is_ardhadhatuka(c.get("lakara"))

def sutra_3_4_115(c) -> bool:
    return is_ardhadhatuka(c.get("lakara"))

def sutra_4_1_2(c) -> bool:
    return decline_aa_feminine(str(c.get("lemma")))[(Case.NOMINATIVE, GrammaticalNumber.SINGULAR)] == c.get("surface")

def sutra_4_1_92(c) -> bool:
    return derive(str(c.get("source")), TaddhitaSuffix.APATYA).surface == c.get("surface")

def sutra_5_2_94(c) -> bool:
    return derive(str(c.get("source")), TaddhitaSuffix.MATUP).surface == c.get("surface")

def sutra_5_3_55(c) -> bool:
    return derive(str(c.get("source")), TaddhitaSuffix.ATISHAYANA).surface == c.get("surface")

def sutra_6_2_1(c) -> bool:
    return profile_accent(tuple(c.get("tokens", ())), int(c.get("udatta_index", 0)), "6.2").primary.accent == Accent.UDATTA

def sutra_6_3_1(c) -> bool:
    return bool([op for op in operations_for_range(str(c.get("range"))) if op.name == "uttarapada-domain"])

def sutra_6_4_1(c) -> bool:
    return any(op.name == "final-a-lengthening" for op in operations_for_range(str(c.get("range"))))

def sutra_6_4_2(c) -> bool:
    return is_consonant(str(c.get("sound")))


# Named handlers for loop-captured executable predicates.
def _it_marker_is_present(c, marker: str) -> bool:
    return marker in analyze_it_markers(str(c.get("upadesha")), str(c.get("kind", "suffix"))).markers

def sutra_1_3_2(c) -> bool:
    return _it_marker_is_present(c, "a")

def sutra_1_3_3(c) -> bool:
    return _it_marker_is_present(c, "k")

def sutra_1_3_5(c) -> bool:
    return _it_marker_is_present(c, "ñi")

def sutra_1_3_6(c) -> bool:
    return _it_marker_is_present(c, "ṣ")

def sutra_1_3_7(c) -> bool:
    return _it_marker_is_present(c, "c")

def sutra_1_3_8(c) -> bool:
    return _it_marker_is_present(c, "k")

def _atmanepada_available(c) -> bool:
    return Pada.ATMANEPADA in determine_available_padas(
        c.get("markers", frozenset()),
        str(c.get("lemma")),
        tuple(c.get("prefixes", ())),
        bool(c.get("reflexive")),
    )

def sutra_1_3_12(c) -> bool:
    return _atmanepada_available(c)

def sutra_1_3_13(c) -> bool:
    return _atmanepada_available(c)

def sutra_1_3_17(c) -> bool:
    return _atmanepada_available(c)

def sutra_1_3_18(c) -> bool:
    return _atmanepada_available(c)

def sutra_1_3_19(c) -> bool:
    return _atmanepada_available(c)

def sutra_1_3_21(c) -> bool:
    return _atmanepada_available(c)

def sutra_1_3_24(c) -> bool:
    return _atmanepada_available(c)

def sutra_1_3_25(c) -> bool:
    return _atmanepada_available(c)

def sutra_1_3_29(c) -> bool:
    return _atmanepada_available(c)

def sutra_1_3_32(c) -> bool:
    return _atmanepada_available(c)

def sutra_1_3_40(c) -> bool:
    return _atmanepada_available(c)

def sutra_1_3_72(c) -> bool:
    return _atmanepada_available(c)

def _karaka_role_is(c, role: Role) -> bool:
    return get_karaka_role(str(c.get("verb")), str(c.get("context"))) == role

def sutra_1_4_24(c) -> bool:
    return _karaka_role_is(c, Role.APADANA)

def sutra_1_4_25(c) -> bool:
    return _karaka_role_is(c, Role.APADANA)

def sutra_1_4_26(c) -> bool:
    return _karaka_role_is(c, Role.APADANA)

def sutra_1_4_27(c) -> bool:
    return _karaka_role_is(c, Role.APADANA)

def sutra_1_4_28(c) -> bool:
    return _karaka_role_is(c, Role.APADANA)

def sutra_1_4_29(c) -> bool:
    return _karaka_role_is(c, Role.APADANA)

def sutra_1_4_32(c) -> bool:
    return _karaka_role_is(c, Role.SAMPRADANA)

def sutra_1_4_33(c) -> bool:
    return _karaka_role_is(c, Role.SAMPRADANA)

def sutra_1_4_42(c) -> bool:
    return _karaka_role_is(c, Role.KARANA)

def sutra_1_4_45(c) -> bool:
    return _karaka_role_is(c, Role.ADHIKARANA)

def sutra_1_4_49(c) -> bool:
    return _karaka_role_is(c, Role.KARMAN)

def sutra_1_4_54(c) -> bool:
    return _karaka_role_is(c, Role.KARTR)

def _compound_sense_is(c, sense: SamasaSense) -> bool:
    return create_compound(list(c.get("members", ()))).sense == sense

def sutra_2_1_24(c) -> bool:
    return _compound_sense_is(c, SamasaSense.DVIT_TAT)

def sutra_2_1_30(c) -> bool:
    return _compound_sense_is(c, SamasaSense.TRT_TAT)

def sutra_2_1_36(c) -> bool:
    return _compound_sense_is(c, SamasaSense.SAP_TAT)

def _role_vibhakti_is(c, case: Case) -> bool:
    return get_vibhakti(c.get("role")) == case

def _companion_vibhakti_is(c, case: Case) -> bool:
    return get_vibhakti(companion_lemma=str(c.get("companion"))) == case

def _semantic_vibhakti_is(c, case: Case) -> bool:
    return get_vibhakti(semantic_context=str(c.get("semantic"))) == case

def sutra_2_3_2(c) -> bool:
    return _role_vibhakti_is(c, Case.ACCUSATIVE)

def sutra_2_3_5(c) -> bool:
    return _companion_vibhakti_is(c, Case.ACCUSATIVE)

def sutra_2_3_13(c) -> bool:
    return _role_vibhakti_is(c, Case.INSTRUMENTAL)

def sutra_2_3_14(c) -> bool:
    return _role_vibhakti_is(c, Case.INSTRUMENTAL)

def sutra_2_3_16(c) -> bool:
    return _companion_vibhakti_is(c, Case.DATIVE)

def sutra_2_3_19(c) -> bool:
    return _companion_vibhakti_is(c, Case.INSTRUMENTAL)

def sutra_2_3_20(c) -> bool:
    return _semantic_vibhakti_is(c, Case.INSTRUMENTAL)

def sutra_2_3_23(c) -> bool:
    return _semantic_vibhakti_is(c, Case.INSTRUMENTAL)

def sutra_2_3_28(c) -> bool:
    return _role_vibhakti_is(c, Case.ABLATIVE)

def sutra_2_3_36(c) -> bool:
    return _role_vibhakti_is(c, Case.DATIVE)

def _dhatu_substitution_is(c, source: str, expected: str) -> bool:
    lemma = str(c.get("lemma"))
    return lemma == source and get_substituted_dhatu(_basic_dhatu(lemma, lemma), c.get("lakara")).lemma == expected

def sutra_2_4_36(c) -> bool:
    return _dhatu_substitution_is(c, "ad", "jagdh")

def sutra_2_4_37(c) -> bool:
    return _dhatu_substitution_is(c, "han", "vadh")

def sutra_2_4_42(c) -> bool:
    return _dhatu_substitution_is(c, "han", "vadh")

def sutra_2_4_45(c) -> bool:
    return _dhatu_substitution_is(c, "i", "gā")

def sutra_2_4_47(c) -> bool:
    return _dhatu_substitution_is(c, "cakṣ", "khyā")

def sutra_2_4_48(c) -> bool:
    return _dhatu_substitution_is(c, "i", "gā")

def sutra_2_4_52(c) -> bool:
    return _dhatu_substitution_is(c, "as", "bhū")

def _derived_dhatu_is(c, label: str, kind: DhatuType) -> bool:
    return c.get("kind") == label and create_derived_dhatu(_basic_dhatu(), kind).type == kind

def sutra_3_1_5(c) -> bool:
    return _derived_dhatu_is(c, "san", DhatuType.DESIDERATIVE)

def sutra_3_1_8(c) -> bool:
    return _derived_dhatu_is(c, "kyac", DhatuType.DENOMINATIVE)

def sutra_3_1_22(c) -> bool:
    return _derived_dhatu_is(c, "yaṅ", DhatuType.INTENSIVE)

def sutra_3_1_25(c) -> bool:
    return _derived_dhatu_is(c, "ṇic", DhatuType.CAUSATIVE)

def _vikarana_is(c, source: int, expected: str) -> bool:
    return int(c.get("varga")) == source and get_vikarana(int(c.get("varga"))) == expected

def sutra_3_1_68(c) -> bool:
    return _vikarana_is(c, 1, "a")

def sutra_3_1_69(c) -> bool:
    return _vikarana_is(c, 4, "ya")

def sutra_3_1_73(c) -> bool:
    return _vikarana_is(c, 5, "nu")

def sutra_3_1_77(c) -> bool:
    return _vikarana_is(c, 6, "a")

def sutra_3_1_78(c) -> bool:
    return _vikarana_is(c, 7, "na")

def sutra_3_1_79(c) -> bool:
    return _vikarana_is(c, 8, "u")

def sutra_3_1_81(c) -> bool:
    return _vikarana_is(c, 9, "nā")

def _derived_surface_is(c, expected: str) -> bool:
    return derive(str(c.get("source")), c.get("suffix")).surface == expected

def sutra_3_1_91(c) -> bool:
    return _derived_surface_is(c, "bhūtvā")

def sutra_3_1_93(c) -> bool:
    return _derived_surface_is(c, "bhavitum")

def sutra_3_2_1(c) -> bool:
    return _derived_surface_is(c, "kāra")

def sutra_3_2_3(c) -> bool:
    return _derived_surface_is(c, "da")

def sutra_3_2_16(c) -> bool:
    return _derived_surface_is(c, "cara")

def sutra_3_2_102(c) -> bool:
    return _derived_surface_is(c, "dṛṣṭa")

def sutra_3_2_135(c) -> bool:
    return _derived_surface_is(c, "kāraka")

def sutra_3_3_18(c) -> bool:
    return _derived_surface_is(c, "bhāva")

def sutra_3_3_94(c) -> bool:
    return _derived_surface_is(c, "kṛti")

def sutra_3_3_115(c) -> bool:
    return _derived_surface_is(c, "bhavana")

def sutra_3_3_121(c) -> bool:
    return _derived_surface_is(c, "rama")

def sutra_3_4_69(c) -> bool:
    return _derived_surface_is(c, "pacat")

def sutra_3_4_71(c) -> bool:
    return _derived_surface_is(c, "babhūvas")

def sutra_3_4_72(c) -> bool:
    return _derived_surface_is(c, "pecāna")

def _lakara_for_time_is(c, source: TimeContext, expected: Lakara) -> bool:
    return c.get("time") == source and get_lakara_for_time(c.get("time")) == expected

def sutra_3_2_110(c) -> bool:
    return _lakara_for_time_is(c, TimeContext.PAST, Lakara.LUN)

def sutra_3_2_111(c) -> bool:
    return _lakara_for_time_is(c, TimeContext.PAST_BEFORE_TODAY, Lakara.LAN)

def sutra_3_3_15(c) -> bool:
    return _lakara_for_time_is(c, TimeContext.FUTURE, Lakara.LRT)

def sutra_3_3_33(c) -> bool:
    return _lakara_for_time_is(c, TimeContext.FUTURE_AFTER_TODAY, Lakara.LUT)

def sutra_3_3_139(c) -> bool:
    return _lakara_for_time_is(c, TimeContext.CONDITIONAL, Lakara.LRN)

def sutra_3_3_161(c) -> bool:
    return _lakara_for_time_is(c, TimeContext.POTENTIAL, Lakara.VIDHILING)

def sutra_3_3_162(c) -> bool:
    return _lakara_for_time_is(c, TimeContext.IMPERATIVE, Lakara.LOT)

def _sandhi_rule_is(c, expected: str) -> bool:
    return join_words(str(c.get("left")), str(c.get("right"))).rule == expected

def sutra_6_1_78(c) -> bool:
    return _sandhi_rule_is(c, "ayavāyāva")

def sutra_6_1_87(c) -> bool:
    return _sandhi_rule_is(c, "guṇa")

def sutra_6_1_88(c) -> bool:
    return _sandhi_rule_is(c, "vṛddhi")

def sutra_6_1_101(c) -> bool:
    return _sandhi_rule_is(c, "savarṇa-dīrgha")

SUTRA_HANDLER_BY_ID: dict[str, Callable[[SutraContext], bool]] = {
    "1.3.2": sutra_1_3_2,
    "1.3.3": sutra_1_3_3,
    "1.3.5": sutra_1_3_5,
    "1.3.6": sutra_1_3_6,
    "1.3.7": sutra_1_3_7,
    "1.3.8": sutra_1_3_8,
    "1.3.12": sutra_1_3_12,
    "1.3.13": sutra_1_3_13,
    "1.3.17": sutra_1_3_17,
    "1.3.18": sutra_1_3_18,
    "1.3.19": sutra_1_3_19,
    "1.3.21": sutra_1_3_21,
    "1.3.24": sutra_1_3_24,
    "1.3.25": sutra_1_3_25,
    "1.3.29": sutra_1_3_29,
    "1.3.32": sutra_1_3_32,
    "1.3.40": sutra_1_3_40,
    "1.3.72": sutra_1_3_72,
    "1.4.24": sutra_1_4_24,
    "1.4.25": sutra_1_4_25,
    "1.4.26": sutra_1_4_26,
    "1.4.27": sutra_1_4_27,
    "1.4.28": sutra_1_4_28,
    "1.4.29": sutra_1_4_29,
    "1.4.32": sutra_1_4_32,
    "1.4.33": sutra_1_4_33,
    "1.4.42": sutra_1_4_42,
    "1.4.45": sutra_1_4_45,
    "1.4.49": sutra_1_4_49,
    "1.4.54": sutra_1_4_54,
    "2.1.24": sutra_2_1_24,
    "2.1.30": sutra_2_1_30,
    "2.1.36": sutra_2_1_36,
    "2.3.2": sutra_2_3_2,
    "2.3.5": sutra_2_3_5,
    "2.3.13": sutra_2_3_13,
    "2.3.14": sutra_2_3_14,
    "2.3.16": sutra_2_3_16,
    "2.3.19": sutra_2_3_19,
    "2.3.20": sutra_2_3_20,
    "2.3.23": sutra_2_3_23,
    "2.3.28": sutra_2_3_28,
    "2.3.36": sutra_2_3_36,
    "2.4.36": sutra_2_4_36,
    "2.4.37": sutra_2_4_37,
    "2.4.42": sutra_2_4_42,
    "2.4.45": sutra_2_4_45,
    "2.4.47": sutra_2_4_47,
    "2.4.48": sutra_2_4_48,
    "2.4.52": sutra_2_4_52,
    "3.1.5": sutra_3_1_5,
    "3.1.8": sutra_3_1_8,
    "3.1.22": sutra_3_1_22,
    "3.1.25": sutra_3_1_25,
    "3.1.68": sutra_3_1_68,
    "3.1.69": sutra_3_1_69,
    "3.1.73": sutra_3_1_73,
    "3.1.77": sutra_3_1_77,
    "3.1.78": sutra_3_1_78,
    "3.1.79": sutra_3_1_79,
    "3.1.81": sutra_3_1_81,
    "3.1.91": sutra_3_1_91,
    "3.1.93": sutra_3_1_93,
    "3.2.1": sutra_3_2_1,
    "3.2.3": sutra_3_2_3,
    "3.2.16": sutra_3_2_16,
    "3.2.102": sutra_3_2_102,
    "3.2.110": sutra_3_2_110,
    "3.2.111": sutra_3_2_111,
    "3.2.135": sutra_3_2_135,
    "3.3.15": sutra_3_3_15,
    "3.3.18": sutra_3_3_18,
    "3.3.33": sutra_3_3_33,
    "3.3.94": sutra_3_3_94,
    "3.3.115": sutra_3_3_115,
    "3.3.121": sutra_3_3_121,
    "3.3.139": sutra_3_3_139,
    "3.3.161": sutra_3_3_161,
    "3.3.162": sutra_3_3_162,
    "3.4.69": sutra_3_4_69,
    "3.4.71": sutra_3_4_71,
    "3.4.72": sutra_3_4_72,
    "6.1.78": sutra_6_1_78,
    "6.1.87": sutra_6_1_87,
    "6.1.88": sutra_6_1_88,
    "6.1.101": sutra_6_1_101,
}

def _build_registry() -> dict[str, DiscreteSutraLogic]:
    registry: dict[str, DiscreteSutraLogic] = {}

    _add(registry, "1.1.1", SutraOperator.SAMJNA, "assigns vrddhi to exactly a/ai/au long-strength vowels", sutra_1_1_1, _ctx("1.1.1", sound="ai"), _ctx("1.1.1", sound="e"), "samjna:vrddhi")
    _add(registry, "1.1.2", SutraOperator.SAMJNA, "assigns guna to exactly a/e/o", sutra_1_1_2, _ctx("1.1.2", sound="e"), _ctx("1.1.2", sound="ai"), "samjna:guna")
    _add(registry, "1.1.3", SutraOperator.VIDHI, "restricts guna/vrddhi replacement targets to ik vowels", sutra_1_1_3, _ctx("1.1.3", sound="i"), _ctx("1.1.3", sound="a"), "target:ik")
    _add(registry, "1.1.4", SutraOperator.PRATISEDHA, "blocks guna and vrddhi under dhatu-lopa before ardhadhatuka suffixes", sutra_1_1_4, _ctx("1.1.4", dhatu_lopa=True, ardhadhatuka=True), _ctx("1.1.4", dhatu_lopa=False, ardhadhatuka=True), "block:guna-vrddhi")
    _add(registry, "1.1.5", SutraOperator.PRATISEDHA, "blocks guna and vrddhi before kit or ngit suffixes", sutra_1_1_5, _ctx("1.1.5", marker="k"), _ctx("1.1.5", marker="p"), "block:kit-ngit")
    _add(registry, "1.1.6", SutraOperator.PRATISEDHA, "blocks strengthening for listed didhi/vevi roots and it augment contexts", sutra_1_1_6, _ctx("1.1.6", root="dīdī", it_augment=False), _ctx("1.1.6", root="bhū", it_augment=False), "block:listed-root")
    _add(registry, "1.1.7", SutraOperator.SAMJNA, "assigns samyoga to adjacent consonant clusters", sutra_1_1_7, _ctx("1.1.7", sounds=("k", "t")), _ctx("1.1.7", sounds=("k", "a")), "samjna:samyoga")
    _add(registry, "1.1.8", SutraOperator.SAMJNA, "assigns anunasika to sounds pronounced with oral and nasal release", sutra_1_1_8, _ctx("1.1.8", sound="n"), _ctx("1.1.8", sound="k"), "samjna:anunasika")
    _add(registry, "1.1.9", SutraOperator.SAMJNA, "assigns savarna to sounds with matching place and effort", sutra_1_1_9, _ctx("1.1.9", left="a", right="a"), _ctx("1.1.9", left="i", right="u"), "samjna:savarna")
    _add(registry, "1.1.10", SutraOperator.PRATISEDHA, "blocks savarna between vowel and consonant classes", sutra_1_1_10, _ctx("1.1.10", left="a", right="k"), _ctx("1.1.10", left="a", right="a"), "block:ac-hal-savarna")
    _add(registry, "1.1.11", SutraOperator.SAMJNA, "marks dual endings in i/u/e channels as pragrhya", sutra_1_1_11, _ctx("1.1.11", analysis=_analysis("devī", "deva", PartOfSpeech.NOUN, number=GrammaticalNumber.DUAL)), _ctx("1.1.11", analysis=_analysis("nadī", "nadī", PartOfSpeech.NOUN, number=GrammaticalNumber.SINGULAR)), "samjna:pragrhya")
    _add(registry, "1.1.12", SutraOperator.SAMJNA, "marks adas forms ending in mi/mu as pragrhya", sutra_1_1_12, _ctx("1.1.12", analysis=_analysis("amī", "adas", PartOfSpeech.PRONOUN)), _ctx("1.1.12", analysis=_analysis("amī", "anya", PartOfSpeech.PRONOUN)), "samjna:pragrhya")
    _add(registry, "1.1.15", SutraOperator.SAMJNA, "marks the particle o as pragrhya", sutra_1_1_15, _ctx("1.1.15", token="o"), _ctx("1.1.15", token="a"), "samjna:pragrhya")
    _add(registry, "1.1.19", SutraOperator.SAMJNA, "marks locative i/u-final forms as pragrhya", sutra_1_1_19, _ctx("1.1.19", analysis=_analysis("nadī", "nadī", PartOfSpeech.NOUN, case=Case.LOCATIVE)), _ctx("1.1.19", analysis=_analysis("nadī", "nadī", PartOfSpeech.NOUN, case=Case.NOMINATIVE)), "samjna:pragrhya")
    _add(registry, "1.1.20", SutraOperator.SAMJNA, "assigns ghu to da/dha roots while excluding dap/daip", sutra_1_1_20, _ctx("1.1.20", root="dā"), _ctx("1.1.20", root="dāp"), "samjna:ghu")
    _add(registry, "1.1.21", SutraOperator.PARIBHASHA, "treats one sound as both beginning and end", sutra_1_1_21, _ctx("1.1.21", term="a"), _ctx("1.1.21", term="agni"), "meta:single-boundary")
    _add(registry, "1.1.22", SutraOperator.SAMJNA, "assigns gha to tarap and tamap suffixes", sutra_1_1_22, _ctx("1.1.22", suffix="tarap"), _ctx("1.1.22", suffix="kta"), "samjna:gha")
    _add(registry, "1.1.23", SutraOperator.SAMJNA, "assigns sankhya to bahu/gana/vatu/dati terms", sutra_1_1_23, _ctx("1.1.23", term="bahu"), _ctx("1.1.23", term="deva"), "samjna:sankhya")
    _add(registry, "1.1.24", SutraOperator.SAMJNA, "assigns sat to controlled numerals ending in s/n", sutra_1_1_24, _ctx("1.1.24", term="pañcan"), _ctx("1.1.24", term="rājan"), "samjna:sat")
    _add(registry, "1.1.25", SutraOperator.SAMJNA, "extends sat to dati", sutra_1_1_25, _ctx("1.1.25", term="ḍati"), _ctx("1.1.25", term="pañcan"), "samjna:sat")
    _add(registry, "1.1.26", SutraOperator.SAMJNA, "assigns nistha to kta and ktavatu suffixes", sutra_1_1_26, _ctx("1.1.26", suffix="kta"), _ctx("1.1.26", suffix="lyuṭ"), "samjna:nistha")
    _add(registry, "1.1.27", SutraOperator.SAMJNA, "assigns sarvanama to the sarvadi pronoun list", sutra_1_1_27, _ctx("1.1.27", stem="sarva"), _ctx("1.1.27", stem="deva"), "samjna:sarvanama")
    _add(registry, "1.1.37", SutraOperator.SAMJNA, "assigns avyaya to controlled svaradi/nipata forms", sutra_1_1_37, _ctx("1.1.37", surface="ca"), _ctx("1.1.37", surface="deva"), "samjna:avyaya")
    _add(registry, "1.1.40", SutraOperator.SAMJNA, "assigns avyaya to ktva/tosun/kasun suffixes", sutra_1_1_40, _ctx("1.1.40", suffix="ktvā"), _ctx("1.1.40", suffix="kta"), "samjna:avyaya")
    _add(registry, "1.1.41", SutraOperator.SAMJNA, "assigns avyaya to avyayibhava compounds", sutra_1_1_41, _ctx("1.1.41", compound="avyayibhava"), _ctx("1.1.41", compound="tatpurusha"), "samjna:avyaya")
    _add(registry, "1.1.42", SutraOperator.SAMJNA, "assigns sarvanamasthana to si", sutra_1_1_42, _ctx("1.1.42", suffix="śi"), _ctx("1.1.42", suffix="kta"), "samjna:sarvanamasthana")
    _add(registry, "1.1.43", SutraOperator.SAMJNA, "assigns sarvanamasthana to sut endings except neuter", sutra_1_1_43, _ctx("1.1.43", suffix="su", gender=Gender.MASCULINE), _ctx("1.1.43", suffix="su", gender=Gender.NEUTER), "samjna:sarvanamasthana")
    _add(registry, "1.1.44", SutraOperator.VIBHASHA, "recognizes na/va/vibhasha wording as optionality", sutra_1_1_44, _ctx("1.1.44", text="na vā"), _ctx("1.1.44", text="nityam"), "operator:vibhasha")
    _add(registry, "1.1.46", SutraOperator.PARIBHASHA, "places tit augments initially and kit augments finally", sutra_1_1_46, _ctx("1.1.46", marker="ṭ", boundary="initial"), _ctx("1.1.46", marker="m", boundary="initial"), "meta:augment-boundary")
    _add(registry, "1.1.47", SutraOperator.PARIBHASHA, "places mit augments after the final vowel", sutra_1_1_47, _ctx("1.1.47", base="bhavati", index=6), _ctx("1.1.47", base="krt", index=1), "meta:mid-augment")
    _add(registry, "1.1.48", SutraOperator.VIDHI, "maps ec vowels to their hrasva substitute channel", sutra_1_1_48, _ctx("1.1.48", sound="e", replacement="i"), _ctx("1.1.48", sound="a", replacement="i"), "substitute:hrasva")
    _add(registry, "1.1.49", SutraOperator.PARIBHASHA, "uses genitive as the substitution-site case", sutra_1_1_49, _ctx("1.1.49", case="genitive"), _ctx("1.1.49", case="locative"), "meta:substitution-site")
    _add(registry, "1.1.50", SutraOperator.PARIBHASHA, "chooses the closest substitute by place and effort", sutra_1_1_50, _ctx("1.1.50", target="i", candidates=("a", "e", "o"), expected="e"), _ctx("1.1.50", target="i", candidates=("a", "o"), expected="e"), "meta:closest-substitute")
    _add(registry, "1.1.51", SutraOperator.VIDHI, "adds r/l after a-type substitutes for r-vocalic targets", sutra_1_1_51, _ctx("1.1.51", target="ṛ", replacement="a", expected="ar"), _ctx("1.1.51", target="i", replacement="a", expected="ar"), "substitute:rapara")
    _add(registry, "1.1.52", SutraOperator.PARIBHASHA, "defaults substitution to the final sound", sutra_1_1_52, _ctx("1.1.52", term="agni", index=3), _ctx("1.1.52", term="", index=0), "meta:final-substitution")
    _add(registry, "1.1.53", SutraOperator.PARIBHASHA, "makes ngit substitutes replace the whole term", sutra_1_1_53, _ctx("1.1.53", substitute="a", marker="ṅ"), _ctx("1.1.53", substitute="a", marker="k"), "meta:whole-replacement")
    _add(registry, "1.1.54", SutraOperator.PARIBHASHA, "targets the initial sound of the following term", sutra_1_1_54, _ctx("1.1.54", term="agni", index=0), _ctx("1.1.54", term="", index=0), "meta:following-initial")
    _add(registry, "1.1.55", SutraOperator.PARIBHASHA, "makes multisound or sit substitutes replace the whole term", sutra_1_1_55, _ctx("1.1.55", substitute="ab", marker=""), _ctx("1.1.55", substitute="a", marker=""), "meta:whole-replacement")
    _add(registry, "1.1.64", SutraOperator.SAMJNA, "defines ti as the last vowel and following sounds", sutra_1_1_64, _ctx("1.1.64", word="bhavati", ti="i"), _ctx("1.1.64", word="bhavati", ti="a"), "samjna:ti")
    _add(registry, "1.1.65", SutraOperator.SAMJNA, "defines upadha as the penultimate sound", sutra_1_1_65, _ctx("1.1.65", word="agni", upadha="n"), _ctx("1.1.65", word="a", upadha="a"), "samjna:upadha")
    _add(registry, "1.1.69", SutraOperator.PARIBHASHA, "lets non-suffix sounds refer to their savarna class", sutra_1_1_69, _ctx("1.1.69", sound="a", is_pratyaya=False), _ctx("1.1.69", sound="a", is_pratyaya=True), "meta:savarna-reference")
    _add(registry, "1.1.70", SutraOperator.PARIBHASHA, "restricts tapara reference to equal duration", sutra_1_1_70, _ctx("1.1.70", sound="a", candidate="i"), _ctx("1.1.70", sound="a", candidate="ā"), "meta:duration")
    _add(registry, "1.1.71", SutraOperator.PARIBHASHA, "forms pratyahara from start sound through marker", sutra_1_1_71, _ctx("1.1.71", name="ac", sounds=("a", "i", "u", "ṛ", "ḷ", "e", "o", "ai", "au")), _ctx("1.1.71", name="ac", sounds=("a", "i")), "meta:pratyahara")
    _add(registry, "1.1.73", SutraOperator.SAMJNA, "assigns vrddha when the first vowel is vrddhi", sutra_1_1_73, _ctx("1.1.73", word="āgama"), _ctx("1.1.73", word="agni"), "samjna:vrddha")
    _add(registry, "1.1.74", SutraOperator.SAMJNA, "assigns vrddha to tyadadi terms by list membership", sutra_1_1_74, _ctx("1.1.74", word="tyad", tyadadi=True), _ctx("1.1.74", word="tyad", tyadadi=False), "samjna:vrddha")
    _add(registry, "1.1.75", SutraOperator.SAMJNA, "assigns vrddha to eastern names beginning with e/o", sutra_1_1_75, _ctx("1.1.75", word="eka", eastern_name=True), _ctx("1.1.75", word="eka", eastern_name=False), "samjna:vrddha")

    _add(registry, "1.2.1", SutraOperator.SAMJNA, "marks suffixes after gang/kutadi roots as ngit", h12.sutra_1_2_1, _ctx("1.2.1", root="gāṅ", markers=()), _ctx("1.2.1", root="gāṅ", markers=("ñ",)), "samjna:ngit")
    _add(registry, "1.2.2", SutraOperator.SAMJNA, "marks it augment after vij as ngit", h12.sutra_1_2_2, _ctx("1.2.2", root="vij", it=True), _ctx("1.2.2", root="vij", it=False), "samjna:ngit")
    _add(registry, "1.2.4", SutraOperator.SAMJNA, "marks apit sarvadhatuka suffixes as ngit", h12.sutra_1_2_4, _ctx("1.2.4", markers=()), _ctx("1.2.4", markers=("p",)), "samjna:ngit")
    _add(registry, "1.2.5", SutraOperator.SAMJNA, "marks lit after non-cluster roots as kit", h12.sutra_1_2_5, _ctx("1.2.5", root="bhū"), _ctx("1.2.5", root="krt"), "samjna:kit")
    _add(registry, "1.2.6", SutraOperator.SAMJNA, "marks lit after indh/bhu as kit", h12.sutra_1_2_6, _ctx("1.2.6", root="indh"), _ctx("1.2.6", root="pac"), "samjna:kit")
    _add(registry, "1.2.7", SutraOperator.SAMJNA, "marks ktva after listed roots as kit", h12.sutra_1_2_7, _ctx("1.2.7", root="mṛḍ"), _ctx("1.2.7", root="bhū"), "samjna:kit")
    _add(registry, "1.2.8", SutraOperator.SAMJNA, "marks ktva/san with it augment after listed roots as kit", h12.sutra_1_2_8, _ctx("1.2.8", root="rud", it=True), _ctx("1.2.8", root="rud", it=False), "samjna:kit")
    _add(registry, "1.2.9", SutraOperator.SAMJNA, "marks san after ik-final roots before jhal as kit", h12.sutra_1_2_9, _ctx("1.2.9", root="ci"), _ctx("1.2.9", root="gam"), "samjna:kit")
    _add(registry, "1.2.11", SutraOperator.SAMJNA, "marks lin/sic in atmanepada as kit", h12.sutra_1_2_11, _ctx("1.2.11", root="pac", atmanepada=True), _ctx("1.2.11", root="pac", atmanepada=False), "samjna:kit")
    _add(registry, "1.2.12", SutraOperator.SAMJNA, "marks sic after short r-final roots as kit", h12.sutra_1_2_12, _ctx("1.2.12", root="kṛ"), _ctx("1.2.12", root="pac"), "samjna:kit")
    _add(registry, "1.2.13", SutraOperator.SAMJNA, "marks sic after gam as kit in the controlled context", h12.sutra_1_2_13, _ctx("1.2.13", root="gam"), _ctx("1.2.13", root="pac"), "samjna:kit")
    _add(registry, "1.2.14", SutraOperator.SAMJNA, "marks sic after han as kit in the controlled context", h12.sutra_1_2_14, _ctx("1.2.14", root="han"), _ctx("1.2.14", root="pac"), "samjna:kit")
    _add(registry, "1.2.15", SutraOperator.SAMJNA, "marks sic after yam as kit in the controlled context", h12.sutra_1_2_15, _ctx("1.2.15", root="yam"), _ctx("1.2.15", root="pac"), "samjna:kit")
    _add(registry, "1.2.17", SutraOperator.SAMJNA, "marks sic after stha as kit in the controlled context", h12.sutra_1_2_17, _ctx("1.2.17", root="sthā"), _ctx("1.2.17", root="pac"), "samjna:kit")
    _add(registry, "1.2.18", SutraOperator.PRATISEDHA, "blocks kit status for set ktva", h12.sutra_1_2_18, _ctx("1.2.18", root="bhū", it=True), _ctx("1.2.18", root="mṛḍ", it=False), "block:kit")
    _add(registry, "1.2.19", SutraOperator.PRATISEDHA, "blocks kit status for nistha after shi", h12.sutra_1_2_19, _ctx("1.2.19", root="śīṅ"), _ctx("1.2.19", root="bhū"), "block:kit")
    _add(registry, "1.2.20", SutraOperator.PRATISEDHA, "blocks kit status for nistha after mrs", h12.sutra_1_2_20, _ctx("1.2.20", root="mṛṣ"), _ctx("1.2.20", root="bhū"), "block:kit")
    _add(registry, "1.2.26", SutraOperator.VIBHASHA, "marks san/ktva with it augment after controlled ral roots as optionally kit", h12.sutra_1_2_26, _ctx("1.2.26", root="kic"), _ctx("1.2.26", root="gam"), "samjna:kit")
    _add(registry, "1.2.41", SutraOperator.SAMJNA, "assigns aprkta to single-sound suffixes", h12.sutra_1_2_41, _ctx("1.2.41", analysis=Analysis("s", "s", PartOfSpeech.INDECLINABLE)), _ctx("1.2.41", analysis=Analysis("tas", "tas", PartOfSpeech.INDECLINABLE)), "samjna:aprkta")
    _add(registry, "1.2.64", SutraOperator.VIDHI, "uses one remainder for homonymous forms", h12.sutra_1_2_64, _ctx("1.2.64", analyses=(Analysis("go", "go", PartOfSpeech.NOUN), Analysis("go", "go", PartOfSpeech.NOUN)), lemma="go"), _ctx("1.2.64", analyses=(Analysis("go", "go", PartOfSpeech.NOUN), Analysis("aja", "aja", PartOfSpeech.NOUN)), lemma="go"), "operation:ekashesha")
    _add(registry, "1.2.65", SutraOperator.VIDHI, "keeps the elder term over the younger term", h12.sutra_1_2_65, _ctx("1.2.65", analyses=(Analysis("arya", "arya", PartOfSpeech.NOUN), Analysis("aryayaṇa", "aryayaṇa", PartOfSpeech.NOUN))), _ctx("1.2.65", analyses=(Analysis("putra", "putra", PartOfSpeech.NOUN), Analysis("duhitṛ", "duhitṛ", PartOfSpeech.NOUN))), "operation:ekashesha")
    _add(registry, "1.2.67", SutraOperator.VIDHI, "keeps masculine over feminine in ekashesha", h12.sutra_1_2_67, _ctx("1.2.67", analyses=(_analysis("rāma", "rāma", PartOfSpeech.NOUN, gender=Gender.MASCULINE), _analysis("sītā", "sītā", PartOfSpeech.NOUN, gender=Gender.FEMININE))), _ctx("1.2.67", analyses=(_analysis("sītā", "sītā", PartOfSpeech.NOUN, gender=Gender.FEMININE), _analysis("latā", "latā", PartOfSpeech.NOUN, gender=Gender.FEMININE))), "operation:ekashesha")
    _add(registry, "1.2.68", SutraOperator.VIDHI, "keeps bhratr/putra over paired kin terms", h12.sutra_1_2_68, _ctx("1.2.68", analyses=(Analysis("bhrātṛ", "bhrātṛ", PartOfSpeech.NOUN), Analysis("svasṛ", "svasṛ", PartOfSpeech.NOUN)), lemma="bhrātṛ"), _ctx("1.2.68", analyses=(Analysis("pitṛ", "pitṛ", PartOfSpeech.NOUN), Analysis("mātṛ", "mātṛ", PartOfSpeech.NOUN)), lemma="bhrātṛ"), "operation:ekashesha")
    _add(registry, "1.2.69", SutraOperator.VIDHI, "keeps neuter over non-neuter in ekashesha", h12.sutra_1_2_69, _ctx("1.2.69", analyses=(_analysis("phala", "phala", PartOfSpeech.NOUN, gender=Gender.NEUTER), _analysis("rāma", "rāma", PartOfSpeech.NOUN, gender=Gender.MASCULINE))), _ctx("1.2.69", analyses=(_analysis("rāma", "rāma", PartOfSpeech.NOUN, gender=Gender.MASCULINE), _analysis("sītā", "sītā", PartOfSpeech.NOUN, gender=Gender.FEMININE))), "operation:ekashesha")
    _add(registry, "1.2.70", SutraOperator.VIDHI, "keeps pitr over matr in ekashesha", h12.sutra_1_2_70, _ctx("1.2.70", analyses=(Analysis("pitṛ", "pitṛ", PartOfSpeech.NOUN), Analysis("mātṛ", "mātṛ", PartOfSpeech.NOUN))), _ctx("1.2.70", analyses=(Analysis("putra", "putra", PartOfSpeech.NOUN), Analysis("duhitṛ", "duhitṛ", PartOfSpeech.NOUN))), "operation:ekashesha")
    _add(registry, "1.2.71", SutraOperator.VIDHI, "keeps shvashura over shvashru in ekashesha", h12.sutra_1_2_71, _ctx("1.2.71", analyses=(Analysis("śvaśura", "śvaśura", PartOfSpeech.NOUN), Analysis("śvaśrū", "śvaśrū", PartOfSpeech.NOUN))), _ctx("1.2.71", analyses=(Analysis("pitṛ", "pitṛ", PartOfSpeech.NOUN), Analysis("mātṛ", "mātṛ", PartOfSpeech.NOUN))), "operation:ekashesha")
    _add(registry, "1.2.72", SutraOperator.VIDHI, "keeps tyadadi pronouns in ekashesha", h12.sutra_1_2_72, _ctx("1.2.72", analyses=(Analysis("tad", "tad", PartOfSpeech.PRONOUN), Analysis("deva", "deva", PartOfSpeech.NOUN))), _ctx("1.2.72", analyses=(Analysis("deva", "deva", PartOfSpeech.NOUN), Analysis("rāma", "rāma", PartOfSpeech.NOUN))), "operation:ekashesha")
    _add(registry, "1.2.73", SutraOperator.VIDHI, "keeps feminine animal term in specified ekashesha domain", h12.sutra_1_2_73, _ctx("1.2.73", analyses=(_analysis("go", "go", PartOfSpeech.NOUN, gender=Gender.FEMININE), _analysis("aja", "aja", PartOfSpeech.NOUN, gender=Gender.MASCULINE))), _ctx("1.2.73", analyses=(_analysis("rāma", "rāma", PartOfSpeech.NOUN, gender=Gender.MASCULINE), _analysis("sītā", "sītā", PartOfSpeech.NOUN, gender=Gender.FEMININE))), "operation:ekashesha")

    for sutra_id, raw, expected_marker, kind, negative in (
        ("1.3.2", "a~", "a", "suffix", "a"),
        ("1.3.3", "tak", "k", "suffix", "ta"),
        ("1.3.5", "ñibhū", "ñi", "root", "bhū"),
        ("1.3.6", "ṣa", "ṣ", "suffix", "sa"),
        ("1.3.7", "ca", "c", "suffix", "pa"),
        ("1.3.8", "ka", "k", "suffix", "laṭ"),
    ):
        _add(
            registry,
            sutra_id,
            SutraOperator.SAMJNA,
            f"extracts it marker {expected_marker} from upadesha by {sutra_id}",
            SUTRA_HANDLER_BY_ID[sutra_id],
            _ctx(sutra_id, upadesha=raw, kind=kind),
            _ctx(sutra_id, upadesha=negative, kind=kind),
            "samjna:it",
        )
    _add(registry, "1.3.4", SutraOperator.PRATISEDHA, "blocks tusmah-final it marking in vibhakti endings", sutra_1_3_4, _ctx("1.3.4", upadesha="tas", kind="vibhakti"), _ctx("1.3.4", upadesha="tas", kind="suffix"), "block:it")
    _add(registry, "1.3.9", SutraOperator.VIDHI, "removes it markers from the usable surface", sutra_1_3_9, _ctx("1.3.9", upadesha="tak", lemma="ta"), _ctx("1.3.9", upadesha="tak", lemma="tak"), "operation:lopa")

    _add(registry, "1.4.3", SutraOperator.SAMJNA, "assigns nadi to feminine i/u-final stems", sutra_1_4_3, _ctx("1.4.3", analysis=_analysis("nadī", "nadī", PartOfSpeech.NOUN, gender=Gender.FEMININE)), _ctx("1.4.3", analysis=_analysis("agni", "agni", PartOfSpeech.NOUN, gender=Gender.MASCULINE)), "samjna:nadi")
    _add(registry, "1.4.7", SutraOperator.SAMJNA, "assigns ghi to remaining i/u-final stems except sakhi", sutra_1_4_7, _ctx("1.4.7", analysis=_analysis("agni", "agni", PartOfSpeech.NOUN, gender=Gender.MASCULINE)), _ctx("1.4.7", analysis=_analysis("sakhi", "sakhi", PartOfSpeech.NOUN, gender=Gender.MASCULINE)), "samjna:ghi")
    _add(registry, "1.4.10", SutraOperator.SAMJNA, "assigns laghu to short vowels", sutra_1_4_10, _ctx("1.4.10", word="aga", index=0), _ctx("1.4.10", word="āgama", index=0), "samjna:laghu")
    _add(registry, "1.4.11", SutraOperator.SAMJNA, "assigns guru to a vowel before a consonant cluster", sutra_1_4_11, _ctx("1.4.11", word="akta", index=0), _ctx("1.4.11", word="aga", index=0), "samjna:guru")
    _add(registry, "1.4.12", SutraOperator.SAMJNA, "assigns guru to long vowels and diphthongs", sutra_1_4_12, _ctx("1.4.12", word="āgama", index=0), _ctx("1.4.12", word="aga", index=0), "samjna:guru")
    _add(registry, "1.4.13", SutraOperator.SAMJNA, "assigns anga to the base before a suffix", sutra_1_4_13, _ctx("1.4.13", analysis=_analysis("deva", "deva", PartOfSpeech.NOUN), suffix="su"), _ctx("1.4.13", analysis=_analysis("deva", "deva", PartOfSpeech.NOUN), suffix=None), "samjna:anga")
    _add(registry, "1.4.14", SutraOperator.SAMJNA, "assigns pada to sup/tin-ending analyses", sutra_1_4_14, _ctx("1.4.14", analysis=_analysis("devah", "deva", PartOfSpeech.NOUN, case=Case.NOMINATIVE)), _ctx("1.4.14", analysis=_analysis("deva", "deva", PartOfSpeech.NOUN)), "samjna:pada")
    _add(registry, "1.4.17", SutraOperator.SAMJNA, "keeps pada before selected svadi non-sarvanamasthana suffixes", sutra_1_4_17, _ctx("1.4.17", analysis=_analysis("devah", "deva", PartOfSpeech.NOUN, case=Case.NOMINATIVE), suffix="su"), _ctx("1.4.17", analysis=_analysis("deva", "deva", PartOfSpeech.NOUN), suffix="su"), "samjna:pada")
    _add(registry, "1.4.18", SutraOperator.SAMJNA, "assigns bha before y or vowel-initial suffixes", sutra_1_4_18, _ctx("1.4.18", analysis=_analysis("devah", "deva", PartOfSpeech.NOUN, case=Case.NOMINATIVE), suffix="ya"), _ctx("1.4.18", analysis=_analysis("devah", "deva", PartOfSpeech.NOUN, case=Case.NOMINATIVE), suffix="ta"), "samjna:bha")

    for sutra_id, verb, context, role in (
        ("1.4.24", "", "separation_point", Role.APADANA),
        ("1.4.25", "bhī", "cause_of_fear", Role.APADANA),
        ("1.4.26", "parā-ji", "unbearable", Role.APADANA),
        ("1.4.27", "", "warded_off_object", Role.APADANA),
        ("1.4.28", "", "hidden_from", Role.APADANA),
        ("1.4.29", "", "teacher", Role.APADANA),
        ("1.4.32", "", "intended_recipient", Role.SAMPRADANA),
        ("1.4.33", "ruc", "pleased_one", Role.SAMPRADANA),
        ("1.4.42", "", "most_effective_means", Role.KARANA),
        ("1.4.45", "", "substratum", Role.ADHIKARANA),
        ("1.4.49", "", "most_desired", Role.KARMAN),
        ("1.4.54", "", "independent_agent", Role.KARTR),
    ):
        _add(registry, sutra_id, SutraOperator.SAMJNA, f"assigns karaka role {role.value} for {context}", SUTRA_HANDLER_BY_ID[sutra_id], _ctx(sutra_id, verb=verb, context=context), _ctx(sutra_id, verb=verb, context="unrelated"), f"karaka:{role.value}")
    _add(registry, "1.4.58", SutraOperator.SAMJNA, "recognizes pra and related prefixes as gati material", sutra_1_4_58, _ctx("1.4.58", prefix="pra"), _ctx("1.4.58", prefix="ca"), "samjna:gati")
    _add(registry, "1.4.59", SutraOperator.SAMJNA, "recognizes upasarga when prefixes are in verbal connection", sutra_1_4_59, _ctx("1.4.59", prefix="pra", verb_connection=True), _ctx("1.4.59", prefix="pra", verb_connection=False), "samjna:upasarga")
    _add(registry, "1.4.60", SutraOperator.SAMJNA, "preserves gati relation metadata for controlled upasargas", sutra_1_4_60, _ctx("1.4.60", prefix="upa", gati_relation=True), _ctx("1.4.60", prefix="upa", gati_relation=False), "samjna:gati")
    _add(registry, "1.4.109", SutraOperator.SAMJNA, "assigns samhita to close phonological proximity", sutra_1_4_109, _ctx("1.4.109", word="agnim"), _ctx("1.4.109", word=""), "samjna:samhita")
    _add(registry, "1.4.110", SutraOperator.SAMJNA, "assigns avasana to cessation after the final sound", sutra_1_4_110, _ctx("1.4.110", word="agni", index=4), _ctx("1.4.110", word="agni", index=1), "samjna:avasana")

    for sutra_id, markers, lemma, prefixes, reflexive, expected in (
        ("1.3.12", frozenset({"ṅ"}), "", (), False, Pada.ATMANEPADA),
        ("1.3.13", frozenset({"ṅ"}), "", (), False, Pada.ATMANEPADA),
        ("1.3.17", frozenset(), "viś", ("ni",), False, Pada.ATMANEPADA),
        ("1.3.18", frozenset(), "krī", ("pari",), False, Pada.ATMANEPADA),
        ("1.3.19", frozenset(), "jñā", ("vi",), False, Pada.ATMANEPADA),
        ("1.3.21", frozenset(), "krīḍ", ("sam",), False, Pada.ATMANEPADA),
        ("1.3.24", frozenset(), "vid", ("ud",), False, Pada.ATMANEPADA),
        ("1.3.25", frozenset(), "vad", ("upa",), False, Pada.ATMANEPADA),
        ("1.3.29", frozenset(), "gam", ("sam",), False, Pada.ATMANEPADA),
        ("1.3.32", frozenset(), "kṣi", (), False, Pada.ATMANEPADA),
        ("1.3.40", frozenset(), "kram", ("upa",), False, Pada.ATMANEPADA),
        ("1.3.72", frozenset({"svarita"}), "", (), True, Pada.ATMANEPADA),
    ):
        _add(
            registry,
            sutra_id,
            SutraOperator.VIDHI,
            f"selects {expected.value} in the controlled voice domain",
            SUTRA_HANDLER_BY_ID[sutra_id],
            _ctx(sutra_id, markers=markers, lemma=lemma, prefixes=prefixes, reflexive=reflexive),
            _ctx(sutra_id, markers=frozenset(), lemma="bhū", prefixes=(), reflexive=False),
            f"pada:{expected.value}",
        )
    _add(
        registry,
        "1.3.78",
        SutraOperator.VIDHI,
        "defaults the remaining active-agent domain to parasmaipada",
        sutra_1_3_78,
        _ctx("1.3.78", markers=frozenset(), lemma="bhū", prefixes=(), reflexive=False),
        _ctx("1.3.78", markers=frozenset({"ṅ"}), lemma="", prefixes=(), reflexive=False),
        "pada:parasmaipada",
    )

    _add(registry, "2.1.1", SutraOperator.PARIBHASHA, "requires samartha relation for pada-vidhi", sutra_2_1_1, _ctx("2.1.1", members=tuple(_compound_members("tatpurusha"))), _ctx("2.1.1", members=()), "domain:samartha")
    _add(registry, "2.1.4", SutraOperator.VIDHI, "compounds co-present sup-marked members", sutra_2_1_4, _ctx("2.1.4", members=tuple(_compound_from_case(Case.GENITIVE))), _ctx("2.1.4", members=()), "domain:samasa")
    _add(registry, "2.1.5", SutraOperator.SAMJNA, "classifies indeclinable-first compounds as avyayibhava", sutra_2_1_5, _ctx("2.1.5", members=tuple(_compound_members("avyayibhava"))), _ctx("2.1.5", members=tuple(_compound_members("tatpurusha"))), "samasa:avyayibhava")
    _add(registry, "2.1.6", SutraOperator.VIDHI, "assigns samipa-style sense to upa avyayibhava", sutra_2_1_6, _ctx("2.1.6", members=tuple(_compound_members("avyayibhava"))), _ctx("2.1.6", members=tuple(_compound_members("tatpurusha"))), "sense:samipa")
    _add(registry, "2.1.7", SutraOperator.VIDHI, "assigns yatha similarity sense in avyayibhava", sutra_2_1_7, _ctx("2.1.7", members=tuple(_avyayibhava_members("yathā"))), _ctx("2.1.7", members=tuple(_compound_members("tatpurusha"))), "sense:yatha")
    _add(registry, "2.1.8", SutraOperator.VIDHI, "assigns yavat limitation sense in avyayibhava", sutra_2_1_8, _ctx("2.1.8", members=tuple(_avyayibhava_members("yāvat"))), _ctx("2.1.8", members=tuple(_avyayibhava_members("yathā"))), "sense:avadharana")
    _add(registry, "2.1.9", SutraOperator.VIDHI, "assigns supprati measure sense in avyayibhava", sutra_2_1_9, _ctx("2.1.9", members=tuple(_avyayibhava_members("supprati"))), _ctx("2.1.9", members=tuple(_avyayibhava_members("yāvat"))), "sense:matra")
    _add(registry, "2.1.10", SutraOperator.VIDHI, "assigns pariṇa sense to aksha/shalaka number compounds", sutra_2_1_10, _ctx("2.1.10", members=tuple(_avyayibhava_members("akṣa", "pariṇā"))), _ctx("2.1.10", members=tuple(_avyayibhava_members("akṣa"))), "sense:parina")
    _add(registry, "2.1.11", SutraOperator.VIBHASHA, "marks controlled avyayibhava compounding as optional", sutra_2_1_11, _ctx("2.1.11", members=tuple(_avyayibhava_members("yathā")), optional=True), _ctx("2.1.11", members=tuple(_avyayibhava_members("yathā")), optional=False), "operator:vibhasha")
    _add(registry, "2.1.12", SutraOperator.VIDHI, "assigns panchami-governed apa/pari/bahir avyayibhava sense", sutra_2_1_12, _ctx("2.1.12", members=tuple(_avyayibhava_members("apa", "grāma", Case.ABLATIVE))), _ctx("2.1.12", members=tuple(_avyayibhava_members("apa", "grāma", Case.ACCUSATIVE))), "sense:panchami")
    _add(registry, "2.1.13", SutraOperator.VIDHI, "assigns maryada/abhividhi sense to aang compounds", sutra_2_1_13, _ctx("2.1.13", members=tuple(_avyayibhava_members("āṅ"))), _ctx("2.1.13", members=tuple(_avyayibhava_members("upa"))), "sense:maryada-abhividhi")
    _add(registry, "2.1.14", SutraOperator.VIDHI, "assigns abhimukhya sense to abhi/prati compounds", sutra_2_1_14, _ctx("2.1.14", members=tuple(_avyayibhava_members("abhi"))), _ctx("2.1.14", members=tuple(_avyayibhava_members("āṅ"))), "sense:abhimukhya")
    _add(registry, "2.1.15", SutraOperator.VIDHI, "assigns anu-samaya sense to anu compounds", sutra_2_1_15, _ctx("2.1.15", members=tuple(_avyayibhava_members("anu"))), _ctx("2.1.15", members=tuple(_avyayibhava_members("abhi"))), "sense:anu-samaya")
    _add(registry, "2.1.16", SutraOperator.VIDHI, "assigns ayama sense to yasya-ayama compounds", sutra_2_1_16, _ctx("2.1.16", members=tuple(_avyayibhava_members("yasya", "āyāma"))), _ctx("2.1.16", members=tuple(_avyayibhava_members("yasya"))), "sense:ayama")
    _add(registry, "2.1.17", SutraOperator.VIDHI, "recognizes tishthadgu lexical avyayibhava compounds", sutra_2_1_17, _ctx("2.1.17", members=tuple(_avyayibhava_members("tiṣṭhadgu"))), _ctx("2.1.17", members=tuple(_avyayibhava_members("anu"))), "sense:lexical-avyayibhava")
    _add(registry, "2.1.18", SutraOperator.VIBHASHA, "makes para/madhya genitive tatpurusha compounding optional", sutra_2_1_18, _ctx("2.1.18", members=tuple(_compound_pair("pāra", "grāma", left_case=Case.GENITIVE))), _ctx("2.1.18", members=tuple(_compound_from_case(Case.GENITIVE))), "operator:vibhasha")
    _add(registry, "2.1.19", SutraOperator.VIDHI, "compounds numerals with vamshya lineage terms", sutra_2_1_19, _ctx("2.1.19", members=tuple(_compound_pair("tri", "vaṃśya", left_pos=PartOfSpeech.NUMERAL, left_value=3))), _ctx("2.1.19", members=tuple(_compound_pair("tri", "purusa", left_pos=PartOfSpeech.NUMERAL, left_value=3))), "sense:vamshya")
    _add(registry, "2.1.20", SutraOperator.VIDHI, "compounds controlled river names", sutra_2_1_20, _ctx("2.1.20", members=tuple(_compound_pair("gaṅgā", "yamunā"))), _ctx("2.1.20", members=tuple(_compound_pair("gaṅgā", "purusa"))), "sense:nadi")
    _add(registry, "2.1.21", SutraOperator.VIDHI, "licenses anyapadartha bahuvrihi compounds in naming", sutra_2_1_21, _ctx("2.1.21", members=tuple(_compound_pair("pīta", "ambara")), proper_name=True), _ctx("2.1.21", members=tuple(_compound_pair("pīta", "ambara")), proper_name=False), "samasa:bahuvrihi")
    _add(registry, "2.1.22", SutraOperator.SAMJNA, "classifies case-governed compounds as tatpurusha", sutra_2_1_22, _ctx("2.1.22", members=tuple(_compound_from_case(Case.GENITIVE))), _ctx("2.1.22", members=tuple(_compound_members("avyayibhava"))), "samasa:tatpurusha")
    _add(registry, "2.1.23", SutraOperator.SAMJNA, "classifies numeral-first tatpurusha compounds as dvigu", sutra_2_1_23, _ctx("2.1.23", members=tuple(_numeral_compound())), _ctx("2.1.23", members=tuple(_compound_from_case(Case.GENITIVE))), "samasa:dvigu")
    for sutra_id, case, sense in (
        ("2.1.24", Case.ACCUSATIVE, SamasaSense.DVIT_TAT),
        ("2.1.30", Case.INSTRUMENTAL, SamasaSense.TRT_TAT),
        ("2.1.36", Case.LOCATIVE, SamasaSense.SAP_TAT),
    ):
        _add(registry, sutra_id, SutraOperator.VIDHI, f"assigns {sense.value} tatpurusha sense", SUTRA_HANDLER_BY_ID[sutra_id], _ctx(sutra_id, members=tuple(_compound_from_case(case))), _ctx(sutra_id, members=tuple(_compound_from_case(Case.GENITIVE))), f"sense:{sense.value}")
    _add(registry, "2.1.57", SutraOperator.VIBHASHA, "classifies same-case qualifier compounds as karmadharaya", sutra_2_1_57, _ctx("2.1.57", members=(_analysis("sita", "sita", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.FEMININE), _analysis("lata", "lata", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.FEMININE))), _ctx("2.1.57", members=tuple(_compound_from_case(Case.GENITIVE))), "samasa:karmadharaya")
    _add(registry, "2.2.29", SutraOperator.SAMJNA, "classifies same-case coordinate compounds as dvandva", sutra_2_2_29, _ctx("2.2.29", members=tuple(_dvandva_members())), _ctx("2.2.29", members=tuple(_compound_from_case(Case.GENITIVE))), "samasa:dvandva")
    _add(registry, "2.2.30", SutraOperator.PARIBHASHA, "keeps the first member before the final member in compound surface", sutra_2_2_30, _ctx("2.2.30", members=tuple(_compound_from_case(Case.GENITIVE)), first_lemma="deva"), _ctx("2.2.30", members=tuple(_compound_from_case(Case.GENITIVE)), first_lemma="purusa"), "meta:upasarjana-order")
    _add(registry, "2.3.1", SutraOperator.VIDHI, "uses nominative when a role is already expressed", sutra_2_3_1, _ctx("2.3.1", expressed=True, case=Case.NOMINATIVE), _ctx("2.3.1", expressed=False, case=Case.NOMINATIVE), "vibhakti:nominative")
    for sutra_id, role, case in (
        ("2.3.2", Role.KARMAN, Case.ACCUSATIVE),
        ("2.3.13", Role.KARTR, Case.INSTRUMENTAL),
        ("2.3.14", Role.KARANA, Case.INSTRUMENTAL),
        ("2.3.28", Role.APADANA, Case.ABLATIVE),
        ("2.3.36", Role.SAMPRADANA, Case.DATIVE),
    ):
        _add(registry, sutra_id, SutraOperator.VIDHI, f"selects {case.value} for {role.value}", SUTRA_HANDLER_BY_ID[sutra_id], _ctx(sutra_id, role=role), _ctx(sutra_id, role=None), f"vibhakti:{case.value}")
    for sutra_id, companion, case in (
        ("2.3.5", "antarā", Case.ACCUSATIVE),
        ("2.3.16", "namas", Case.DATIVE),
        ("2.3.19", "saha", Case.INSTRUMENTAL),
    ):
        _add(registry, sutra_id, SutraOperator.VIDHI, f"selects {case.value} with upapada {companion}", SUTRA_HANDLER_BY_ID[sutra_id], _ctx(sutra_id, companion=companion), _ctx(sutra_id, companion="anya"), f"vibhakti:{case.value}")
    for sutra_id, semantic, case in (
        ("2.3.20", "defective_limb", Case.INSTRUMENTAL),
        ("2.3.23", "cause", Case.INSTRUMENTAL),
    ):
        _add(registry, sutra_id, SutraOperator.VIDHI, f"selects {case.value} in semantic context {semantic}", SUTRA_HANDLER_BY_ID[sutra_id], _ctx(sutra_id, semantic=semantic), _ctx(sutra_id, semantic="other"), f"vibhakti:{case.value}")
    _add(registry, "2.3.50", SutraOperator.VIDHI, "falls back to genitive for residual relation", sutra_2_3_50, _ctx("2.3.50", role=None), _ctx("2.3.50", role=Role.KARMAN), "vibhakti:genitive")
    _add(registry, "2.4.1", SutraOperator.VIDHI, "marks dvigu compounds singular", sutra_2_4_1, _ctx("2.4.1", members=tuple(_numeral_compound())), _ctx("2.4.1", members=tuple(_dvandva_members())), "number:singular")
    _add(registry, "2.4.17", SutraOperator.VIDHI, "marks avyayibhava result as avyaya", sutra_2_4_17, _ctx("2.4.17", members=tuple(_compound_members("avyayibhava"))), _ctx("2.4.17", members=tuple(_compound_from_case(Case.GENITIVE))), "samjna:avyaya")
    _add(registry, "2.4.18", SutraOperator.VIDHI, "marks avyayibhava result neuter singular", sutra_2_4_18, _ctx("2.4.18", members=tuple(_compound_members("avyayibhava"))), _ctx("2.4.18", members=tuple(_dvandva_members())), "gender:neuter", "number:singular")
    _add(registry, "2.4.26", SutraOperator.PARIBHASHA, "uses the final member for dvandva/tatpurusha gender", sutra_2_4_26, _ctx("2.4.26", members=tuple(_compound_from_case(Case.GENITIVE)), gender=Gender.MASCULINE), _ctx("2.4.26", members=tuple(_compound_from_case(Case.GENITIVE)), gender=Gender.FEMININE), "meta:final-gender")
    for sutra_id, lemma, lakara, output in (
        ("2.4.36", "ad", Lakara.LRT, "jagdh"),
        ("2.4.37", "han", Lakara.ASHIRLING, "vadh"),
        ("2.4.42", "han", Lakara.LUN, "vadh"),
        ("2.4.45", "i", Lakara.LUN, "gā"),
        ("2.4.47", "cakṣ", Lakara.LAT, "khyā"),
        ("2.4.48", "i", Lakara.ASHIRLING, "gā"),
        ("2.4.52", "as", Lakara.LRT, "bhū"),
    ):
        _add(registry, sutra_id, SutraOperator.VIDHI, f"substitutes root {output} for {lemma}", SUTRA_HANDLER_BY_ID[sutra_id], _ctx(sutra_id, lemma=lemma, lakara=lakara), _ctx(sutra_id, lemma="bhū", lakara=lakara), f"dhatu:{output}")
    _add(registry, "2.4.71", SutraOperator.VIDHI, "elides internal sup endings inside compounds", sutra_2_4_71, _ctx("2.4.71", members=tuple(_compound_from_case(Case.GENITIVE)), surface="devapurusah"), _ctx("2.4.71", members=tuple(_compound_from_case(Case.GENITIVE)), surface="devasya purusah"), "operation:sup-lopa")
    _add(registry, "2.4.72", SutraOperator.VIDHI, "applies luk elision for controlled adadi roots", sutra_2_4_72, _ctx("2.4.72", lemma="ad"), _ctx("2.4.72", lemma="bhū"), "operation:luk")

    for sutra_id, dhatu_type, expected in (
        ("3.1.5", DhatuType.DESIDERATIVE, "san"),
        ("3.1.8", DhatuType.DENOMINATIVE, "kyac"),
        ("3.1.22", DhatuType.INTENSIVE, "yaṅ"),
        ("3.1.25", DhatuType.CAUSATIVE, "ṇic"),
    ):
        _add(registry, sutra_id, SutraOperator.VIDHI, f"creates {expected} derived dhatu", SUTRA_HANDLER_BY_ID[sutra_id], _ctx(sutra_id, kind=expected), _ctx(sutra_id, kind="basic"), f"dhatu-type:{expected}")
    for sutra_id, varga, vik in (
        ("3.1.68", 1, "a"), ("3.1.69", 4, "ya"), ("3.1.73", 5, "nu"), ("3.1.77", 6, "a"),
        ("3.1.78", 7, "na"), ("3.1.79", 8, "u"), ("3.1.81", 9, "nā"),
    ):
        _add(registry, sutra_id, SutraOperator.VIDHI, f"selects vikarana {vik} for class {varga}", SUTRA_HANDLER_BY_ID[sutra_id], _ctx(sutra_id, varga=varga), _ctx(sutra_id, varga=0), f"vikarana:{vik}")
    for sutra_id, source, suffix, surface in (
        ("3.1.91", "bhū", KrtSuffix.KTVA, "bhūtvā"),
        ("3.1.93", "bhū", KrtSuffix.TUMUN, "bhavitum"),
        ("3.2.1", "kṛ", KrtSuffix.AN, "kāra"),
        ("3.2.3", "dā", KrtSuffix.KA, "da"),
        ("3.2.16", "car", KrtSuffix.TA, "cara"),
        ("3.2.102", "dṛś", KrtSuffix.KTA, "dṛṣṭa"),
        ("3.2.135", "kṛ", KrtSuffix.NVUL, "kāraka"),
        ("3.3.18", "bhū", KrtSuffix.GHAN, "bhāva"),
        ("3.3.94", "kṛ", KrtSuffix.KTIN, "kṛti"),
        ("3.3.115", "bhū", KrtSuffix.LYUT, "bhavana"),
        ("3.3.121", "ram", KrtSuffix.GHA, "rama"),
        ("3.4.69", "pac", KrtSuffix.SATR, "pacat"),
        ("3.4.71", "bhū", KrtSuffix.KVASU, "babhūvas"),
        ("3.4.72", "pac", KrtSuffix.KANAC, "pecāna"),
    ):
        _add(registry, sutra_id, SutraOperator.VIDHI, f"derives {surface} with {suffix.value}", SUTRA_HANDLER_BY_ID[sutra_id], _ctx(sutra_id, source=source, suffix=suffix), _ctx(sutra_id, source="bhū", suffix=KrtSuffix.KA), f"derived:{surface}")
    for sutra_id, time, lakara in (
        ("3.2.110", TimeContext.PAST, Lakara.LUN),
        ("3.2.111", TimeContext.PAST_BEFORE_TODAY, Lakara.LAN),
        ("3.3.15", TimeContext.FUTURE, Lakara.LRT),
        ("3.3.33", TimeContext.FUTURE_AFTER_TODAY, Lakara.LUT),
        ("3.3.139", TimeContext.CONDITIONAL, Lakara.LRN),
        ("3.3.161", TimeContext.POTENTIAL, Lakara.VIDHILING),
        ("3.3.162", TimeContext.IMPERATIVE, Lakara.LOT),
    ):
        _add(registry, sutra_id, SutraOperator.VIDHI, f"selects lakara {lakara.value} for {time.value}", SUTRA_HANDLER_BY_ID[sutra_id], _ctx(sutra_id, time=time), _ctx(sutra_id, time=TimeContext.PRESENT), f"lakara:{lakara.value}")
    _add(registry, "3.2.123", SutraOperator.VIDHI, "selects lat for present time", sutra_3_2_123, _ctx("3.2.123", time=TimeContext.PRESENT), _ctx("3.2.123", time=TimeContext.PAST), "lakara:lat")
    _add(registry, "3.4.79", SutraOperator.VIDHI, "changes atmanepada ta to te in selected lakaras", sutra_3_4_79, _ctx("3.4.79", stem="labha", surface="labhate"), _ctx("3.4.79", stem="labha", surface="labhata"), "ending:te")
    _add(registry, "3.4.80", SutraOperator.VIDHI, "changes thas to se in atmanepada", sutra_3_4_80, _ctx("3.4.80", stem="labha", surface="labhase"), _ctx("3.4.80", stem="labha", surface="labhathās"), "ending:se")
    _add(registry, "3.4.86", SutraOperator.VIDHI, "changes lot ti to tu", sutra_3_4_86, _ctx("3.4.86", stem="bhava", surface="bhavatu"), _ctx("3.4.86", stem="bhava", surface="bhavati"), "ending:tu")
    _add(registry, "3.4.87", SutraOperator.VIDHI, "changes lot si to hi unless later elided", sutra_3_4_87, _ctx("3.4.87", stem="bhū", surface="bhūhi"), _ctx("3.4.87", stem="bhū", surface="bhūsi"), "ending:hi")
    _add(registry, "3.4.88", SutraOperator.VIDHI, "elides hi after an a-final stem", sutra_3_4_88, _ctx("3.4.88", stem="bhava", surface="bhava"), _ctx("3.4.88", stem="bhava", surface="bhavahi"), "operation:hi-lopa")
    _add(registry, "3.4.92", SutraOperator.VIDHI, "adds a augment for first-person lot", sutra_3_4_92, _ctx("3.4.92", stem="bhava", surface="bhavāni"), _ctx("3.4.92", stem="bhava", surface="bhavami"), "augment:ā")
    _add(registry, "3.4.100", SutraOperator.VIDHI, "elides final i in nit lakara endings", sutra_3_4_100, _ctx("3.4.100", stem="bhava", surface="bhavet"), _ctx("3.4.100", stem="bhava", surface="bhaveti"), "operation:i-lopa")
    _add(registry, "3.4.101", SutraOperator.VIDHI, "substitutes tam for thas in lot/nit endings", sutra_3_4_101, _ctx("3.4.101", stem="bhava", surface="bhavatam"), _ctx("3.4.101", stem="bhava", surface="bhavathaḥ"), "ending:tam")
    _add(registry, "3.4.108", SutraOperator.VIDHI, "substitutes jus for jhi/nti in vidhiling", sutra_3_4_108, _ctx("3.4.108", stem="bhava", surface="bhavejus"), _ctx("3.4.108", stem="bhava", surface="bhaventi"), "ending:jus")
    _add(registry, "3.4.113", SutraOperator.SAMJNA, "marks selected lakaras as sarvadhatuka", sutra_3_4_113, _ctx("3.4.113", lakara=Lakara.LAT), _ctx("3.4.113", lakara=Lakara.LRT), "samjna:sarvadhatuka")
    _add(registry, "3.4.114", SutraOperator.SAMJNA, "marks remaining lakaras as ardhadhatuka", sutra_3_4_114, _ctx("3.4.114", lakara=Lakara.LRT), _ctx("3.4.114", lakara=Lakara.LAT), "samjna:ardhadhatuka")
    _add(registry, "3.4.115", SutraOperator.SAMJNA, "marks lit as ardhadhatuka", sutra_3_4_115, _ctx("3.4.115", lakara=Lakara.LIT), _ctx("3.4.115", lakara=Lakara.LAT), "samjna:ardhadhatuka")

    _add(registry, "4.1.2", SutraOperator.VIDHI, "derives controlled aa-stem feminine forms", sutra_4_1_2, _ctx("4.1.2", lemma="latā", surface="latā"), _ctx("4.1.2", lemma="latā", surface="lata"), "suffix:tap")
    _add(registry, "4.1.92", SutraOperator.VIDHI, "derives apatya descendant taddhita", sutra_4_1_92, _ctx("4.1.92", source="upagu", surface="aupagava"), _ctx("4.1.92", source="bala", surface="balavān"), "taddhita:apatya")
    _add(registry, "5.2.94", SutraOperator.VIDHI, "derives possession adjectives with matup", sutra_5_2_94, _ctx("5.2.94", source="bala", surface="balavān"), _ctx("5.2.94", source="upagu", surface="aupagava"), "taddhita:matup")
    _add(registry, "5.3.55", SutraOperator.VIDHI, "derives degree forms with atishayana", sutra_5_3_55, _ctx("5.3.55", source="laghu", surface="laghiṣṭha"), _ctx("5.3.55", source="bala", surface="balavān"), "taddhita:atishayana")
    for sutra_id, left, right, rule in (
        ("6.1.78", "hare", "atra", "ayavāyāva"),
        ("6.1.87", "deva", "iti", "guṇa"),
        ("6.1.88", "deva", "eva", "vṛddhi"),
        ("6.1.101", "deva", "atra", "savarṇa-dīrgha"),
    ):
        _add(registry, sutra_id, SutraOperator.VIDHI, f"applies {rule} sandhi", SUTRA_HANDLER_BY_ID[sutra_id], _ctx(sutra_id, left=left, right=right), _ctx(sutra_id, left="deva", right="gacchati"), f"sandhi:{rule}")
    _add(registry, "6.2.1", SutraOperator.ADHIKARA, "opens compound accent handling", sutra_6_2_1, _ctx("6.2.1", tokens=("rāja", "puruṣa"), udatta_index=1), _ctx("6.2.1", tokens=(), udatta_index=0), "accent:udatta")
    _add(registry, "6.3.1", SutraOperator.ADHIKARA, "opens uttarapada operation handling", sutra_6_3_1, _ctx("6.3.1", range="6.3"), _ctx("6.3.1", range="6.2"), "domain:uttarapada")
    _add(registry, "6.4.1", SutraOperator.ADHIKARA, "opens anga operation handling", sutra_6_4_1, _ctx("6.4.1", range="6.4"), _ctx("6.4.1", range="6.2"), "domain:anga")
    _add(registry, "6.4.2", SutraOperator.VIDHI, "recognizes consonant-sensitive anga conditions", sutra_6_4_2, _ctx("6.4.2", sound="k"), _ctx("6.4.2", sound="a"), "condition:hal")

    return registry


SUTRA_LOGIC = _build_registry()
