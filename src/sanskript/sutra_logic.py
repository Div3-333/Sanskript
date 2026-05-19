from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any

from .anga import DerivationContext, Suffix, guna, vrddhi
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
from .grammar import Analysis, Case, Gender, GrammaticalNumber, Pada, PartOfSpeech, Role, Samjna
from .karaka import get_karaka_role
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
from .samasa import SamasaType, create_compound
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


def _build_registry() -> dict[str, DiscreteSutraLogic]:
    registry: dict[str, DiscreteSutraLogic] = {}

    _add(registry, "1.1.1", SutraOperator.SAMJNA, "assigns vrddhi to exactly a/ai/au long-strength vowels", lambda c: is_vrddhi(str(c.get("sound"))), _ctx("1.1.1", sound="ai"), _ctx("1.1.1", sound="e"), "samjna:vrddhi")
    _add(registry, "1.1.2", SutraOperator.SAMJNA, "assigns guna to exactly a/e/o", lambda c: is_guna(str(c.get("sound"))), _ctx("1.1.2", sound="e"), _ctx("1.1.2", sound="ai"), "samjna:guna")
    _add(registry, "1.1.3", SutraOperator.VIDHI, "restricts guna/vrddhi replacement targets to ik vowels", lambda c: is_ik(str(c.get("sound"))) and guna_replacement_for_ik(str(c.get("sound"))) and vrddhi_replacement_for_ik(str(c.get("sound"))), _ctx("1.1.3", sound="i"), _ctx("1.1.3", sound="a"), "target:ik")
    _add(registry, "1.1.4", SutraOperator.PRATISEDHA, "blocks guna and vrddhi under dhatu-lopa before ardhadhatuka suffixes", lambda c: guna("i", DerivationContext(suffix=Suffix("ta", is_ardhadhatuka=bool(c.get("ardhadhatuka"))), has_dhatu_lopa=bool(c.get("dhatu_lopa")))) == "i", _ctx("1.1.4", dhatu_lopa=True, ardhadhatuka=True), _ctx("1.1.4", dhatu_lopa=False, ardhadhatuka=True), "block:guna-vrddhi")
    _add(registry, "1.1.5", SutraOperator.PRATISEDHA, "blocks guna and vrddhi before kit or ngit suffixes", lambda c: guna("i", DerivationContext(suffix=Suffix("ta", markers=frozenset({str(c.get("marker"))})))) == "i", _ctx("1.1.5", marker="k"), _ctx("1.1.5", marker="p"), "block:kit-ngit")
    _add(registry, "1.1.6", SutraOperator.PRATISEDHA, "blocks strengthening for listed didhi/vevi roots and it augment contexts", lambda c: guna("i", DerivationContext(root_lemma=str(c.get("root")), is_it_augment=bool(c.get("it_augment")), suffix=Suffix("ta"))) == "i", _ctx("1.1.6", root="dīdī", it_augment=False), _ctx("1.1.6", root="bhū", it_augment=False), "block:listed-root")
    _add(registry, "1.1.7", SutraOperator.SAMJNA, "assigns samyoga to adjacent consonant clusters", lambda c: is_samyoga(list(c.get("sounds", ()))), _ctx("1.1.7", sounds=("k", "t")), _ctx("1.1.7", sounds=("k", "a")), "samjna:samyoga")
    _add(registry, "1.1.8", SutraOperator.SAMJNA, "assigns anunasika to sounds pronounced with oral and nasal release", lambda c: is_anunasika(str(c.get("sound"))), _ctx("1.1.8", sound="n"), _ctx("1.1.8", sound="k"), "samjna:anunasika")
    _add(registry, "1.1.9", SutraOperator.SAMJNA, "assigns savarna to sounds with matching place and effort", lambda c: is_savarna(str(c.get("left")), str(c.get("right"))), _ctx("1.1.9", left="a", right="a"), _ctx("1.1.9", left="i", right="u"), "samjna:savarna")
    _add(registry, "1.1.10", SutraOperator.PRATISEDHA, "blocks savarna between vowel and consonant classes", lambda c: is_vowel(str(c.get("left"))) != is_vowel(str(c.get("right"))) and not is_savarna(str(c.get("left")), str(c.get("right"))), _ctx("1.1.10", left="a", right="k"), _ctx("1.1.10", left="a", right="a"), "block:ac-hal-savarna")
    _add(registry, "1.1.11", SutraOperator.SAMJNA, "marks dual endings in i/u/e channels as pragrhya", lambda c: is_pragrhya(c.get("analysis")), _ctx("1.1.11", analysis=_analysis("devī", "deva", PartOfSpeech.NOUN, number=GrammaticalNumber.DUAL)), _ctx("1.1.11", analysis=_analysis("nadī", "nadī", PartOfSpeech.NOUN, number=GrammaticalNumber.SINGULAR)), "samjna:pragrhya")
    _add(registry, "1.1.12", SutraOperator.SAMJNA, "marks adas forms ending in mi/mu as pragrhya", lambda c: is_pragrhya(c.get("analysis")), _ctx("1.1.12", analysis=_analysis("amī", "adas", PartOfSpeech.PRONOUN)), _ctx("1.1.12", analysis=_analysis("amī", "anya", PartOfSpeech.PRONOUN)), "samjna:pragrhya")
    _add(registry, "1.1.15", SutraOperator.SAMJNA, "marks the particle o as pragrhya", lambda c: is_pragrhya(str(c.get("token"))), _ctx("1.1.15", token="o"), _ctx("1.1.15", token="a"), "samjna:pragrhya")
    _add(registry, "1.1.19", SutraOperator.SAMJNA, "marks locative i/u-final forms as pragrhya", lambda c: is_pragrhya(c.get("analysis")), _ctx("1.1.19", analysis=_analysis("nadī", "nadī", PartOfSpeech.NOUN, case=Case.LOCATIVE)), _ctx("1.1.19", analysis=_analysis("nadī", "nadī", PartOfSpeech.NOUN, case=Case.NOMINATIVE)), "samjna:pragrhya")
    _add(registry, "1.1.20", SutraOperator.SAMJNA, "assigns ghu to da/dha roots while excluding dap/daip", lambda c: is_ghu_root(str(c.get("root"))), _ctx("1.1.20", root="dā"), _ctx("1.1.20", root="dāp"), "samjna:ghu")
    _add(registry, "1.1.21", SutraOperator.PARIBHASHA, "treats one sound as both beginning and end", lambda c: has_single_sound_boundary(str(c.get("term"))), _ctx("1.1.21", term="a"), _ctx("1.1.21", term="agni"), "meta:single-boundary")
    _add(registry, "1.1.22", SutraOperator.SAMJNA, "assigns gha to tarap and tamap suffixes", lambda c: is_gha_suffix(str(c.get("suffix"))), _ctx("1.1.22", suffix="tarap"), _ctx("1.1.22", suffix="kta"), "samjna:gha")
    _add(registry, "1.1.23", SutraOperator.SAMJNA, "assigns sankhya to bahu/gana/vatu/dati terms", lambda c: is_sankhya_term(str(c.get("term"))), _ctx("1.1.23", term="bahu"), _ctx("1.1.23", term="deva"), "samjna:sankhya")
    _add(registry, "1.1.24", SutraOperator.SAMJNA, "assigns sat to controlled numerals ending in s/n", lambda c: is_shat_numeral(str(c.get("term"))) and str(c.get("term")) != "ḍati", _ctx("1.1.24", term="pañcan"), _ctx("1.1.24", term="rājan"), "samjna:sat")
    _add(registry, "1.1.25", SutraOperator.SAMJNA, "extends sat to dati", lambda c: is_shat_numeral(str(c.get("term"))) and str(c.get("term")) == "ḍati", _ctx("1.1.25", term="ḍati"), _ctx("1.1.25", term="pañcan"), "samjna:sat")
    _add(registry, "1.1.26", SutraOperator.SAMJNA, "assigns nistha to kta and ktavatu suffixes", lambda c: is_nistha_suffix(str(c.get("suffix"))), _ctx("1.1.26", suffix="kta"), _ctx("1.1.26", suffix="lyuṭ"), "samjna:nistha")
    _add(registry, "1.1.27", SutraOperator.SAMJNA, "assigns sarvanama to the sarvadi pronoun list", lambda c: is_sarvanama_stem(str(c.get("stem"))), _ctx("1.1.27", stem="sarva"), _ctx("1.1.27", stem="deva"), "samjna:sarvanama")
    _add(registry, "1.1.37", SutraOperator.SAMJNA, "assigns avyaya to controlled svaradi/nipata forms", lambda c: is_controlled_avyaya(str(c.get("surface"))), _ctx("1.1.37", surface="ca"), _ctx("1.1.37", surface="deva"), "samjna:avyaya")
    _add(registry, "1.1.40", SutraOperator.SAMJNA, "assigns avyaya to ktva/tosun/kasun suffixes", lambda c: is_avyaya_suffix(str(c.get("suffix"))), _ctx("1.1.40", suffix="ktvā"), _ctx("1.1.40", suffix="kta"), "samjna:avyaya")
    _add(registry, "1.1.41", SutraOperator.SAMJNA, "assigns avyaya to avyayibhava compounds", lambda c: create_compound(_compound_members(str(c.get("compound")))).type == SamasaType.AVYAYIBHAVA, _ctx("1.1.41", compound="avyayibhava"), _ctx("1.1.41", compound="tatpurusha"), "samjna:avyaya")
    _add(registry, "1.1.42", SutraOperator.SAMJNA, "assigns sarvanamasthana to si", lambda c: is_sarvanamasthana_suffix(str(c.get("suffix"))), _ctx("1.1.42", suffix="śi"), _ctx("1.1.42", suffix="kta"), "samjna:sarvanamasthana")
    _add(registry, "1.1.43", SutraOperator.SAMJNA, "assigns sarvanamasthana to sut endings except neuter", lambda c: is_sarvanamasthana_suffix(str(c.get("suffix")), c.get("gender")), _ctx("1.1.43", suffix="su", gender=Gender.MASCULINE), _ctx("1.1.43", suffix="su", gender=Gender.NEUTER), "samjna:sarvanamasthana")
    _add(registry, "1.1.44", SutraOperator.VIBHASHA, "recognizes na/va/vibhasha wording as optionality", lambda c: is_vibhasha_expression(str(c.get("text"))), _ctx("1.1.44", text="na vā"), _ctx("1.1.44", text="nityam"), "operator:vibhasha")
    _add(registry, "1.1.46", SutraOperator.PARIBHASHA, "places tit augments initially and kit augments finally", lambda c: augment_boundary(str(c.get("marker"))) == c.get("boundary"), _ctx("1.1.46", marker="ṭ", boundary="initial"), _ctx("1.1.46", marker="m", boundary="initial"), "meta:augment-boundary")
    _add(registry, "1.1.47", SutraOperator.PARIBHASHA, "places mit augments after the final vowel", lambda c: mid_augment_index(str(c.get("base"))) == c.get("index"), _ctx("1.1.47", base="bhavati", index=6), _ctx("1.1.47", base="krt", index=1), "meta:mid-augment")
    _add(registry, "1.1.48", SutraOperator.VIDHI, "maps ec vowels to their hrasva substitute channel", lambda c: hrasva_substitute_for_ec(str(c.get("sound"))) == c.get("replacement"), _ctx("1.1.48", sound="e", replacement="i"), _ctx("1.1.48", sound="a", replacement="i"), "substitute:hrasva")
    _add(registry, "1.1.49", SutraOperator.PARIBHASHA, "uses genitive as the substitution-site case", lambda c: genitive_marks_substitution_site(str(c.get("case"))), _ctx("1.1.49", case="genitive"), _ctx("1.1.49", case="locative"), "meta:substitution-site")
    _add(registry, "1.1.50", SutraOperator.PARIBHASHA, "chooses the closest substitute by place and effort", lambda c: best_substitute(str(c.get("target")), tuple(c.get("candidates", ()))) == c.get("expected"), _ctx("1.1.50", target="i", candidates=("a", "e", "o"), expected="e"), _ctx("1.1.50", target="i", candidates=("a", "o"), expected="e"), "meta:closest-substitute")
    _add(registry, "1.1.51", SutraOperator.VIDHI, "adds r/l after a-type substitutes for r-vocalic targets", lambda c: rapara_substitute_for_ur(str(c.get("target")), str(c.get("replacement"))) == c.get("expected"), _ctx("1.1.51", target="ṛ", replacement="a", expected="ar"), _ctx("1.1.51", target="i", replacement="a", expected="ar"), "substitute:rapara")
    _add(registry, "1.1.52", SutraOperator.PARIBHASHA, "defaults substitution to the final sound", lambda c: default_final_substitution_index(str(c.get("term"))) == c.get("index"), _ctx("1.1.52", term="agni", index=3), _ctx("1.1.52", term="", index=0), "meta:final-substitution")
    _add(registry, "1.1.53", SutraOperator.PARIBHASHA, "makes ngit substitutes replace the whole term", lambda c: whole_term_replacement_applies(str(c.get("substitute")), str(c.get("marker"))), _ctx("1.1.53", substitute="a", marker="ṅ"), _ctx("1.1.53", substitute="a", marker="k"), "meta:whole-replacement")
    _add(registry, "1.1.54", SutraOperator.PARIBHASHA, "targets the initial sound of the following term", lambda c: following_initial_substitution_index(str(c.get("term"))) == c.get("index"), _ctx("1.1.54", term="agni", index=0), _ctx("1.1.54", term="", index=0), "meta:following-initial")
    _add(registry, "1.1.55", SutraOperator.PARIBHASHA, "makes multisound or sit substitutes replace the whole term", lambda c: whole_term_replacement_applies(str(c.get("substitute")), str(c.get("marker"))), _ctx("1.1.55", substitute="ab", marker=""), _ctx("1.1.55", substitute="a", marker=""), "meta:whole-replacement")
    _add(registry, "1.1.64", SutraOperator.SAMJNA, "defines ti as the last vowel and following sounds", lambda c: is_ti(str(c.get("word"))) == c.get("ti"), _ctx("1.1.64", word="bhavati", ti="i"), _ctx("1.1.64", word="bhavati", ti="a"), "samjna:ti")
    _add(registry, "1.1.65", SutraOperator.SAMJNA, "defines upadha as the penultimate sound", lambda c: is_upadha(str(c.get("word"))) == c.get("upadha"), _ctx("1.1.65", word="agni", upadha="n"), _ctx("1.1.65", word="a", upadha="a"), "samjna:upadha")
    _add(registry, "1.1.69", SutraOperator.PARIBHASHA, "lets non-suffix sounds refer to their savarna class", lambda c: bool(savarna_reference(str(c.get("sound")), bool(c.get("is_pratyaya")))), _ctx("1.1.69", sound="a", is_pratyaya=False), _ctx("1.1.69", sound="a", is_pratyaya=True), "meta:savarna-reference")
    _add(registry, "1.1.70", SutraOperator.PARIBHASHA, "restricts tapara reference to equal duration", lambda c: tapara_matches_duration(str(c.get("sound")), str(c.get("candidate"))), _ctx("1.1.70", sound="a", candidate="i"), _ctx("1.1.70", sound="a", candidate="ā"), "meta:duration")
    _add(registry, "1.1.71", SutraOperator.PARIBHASHA, "forms pratyahara from start sound through marker", lambda c: tuple(pratyahara(str(c.get("name")))) == tuple(c.get("sounds", ())), _ctx("1.1.71", name="ac", sounds=("a", "i", "u", "ṛ", "ḷ", "e", "o", "ai", "au")), _ctx("1.1.71", name="ac", sounds=("a", "i")), "meta:pratyahara")
    _add(registry, "1.1.73", SutraOperator.SAMJNA, "assigns vrddha when the first vowel is vrddhi", lambda c: is_vrddha_word(str(c.get("word"))), _ctx("1.1.73", word="āgama"), _ctx("1.1.73", word="agni"), "samjna:vrddha")
    _add(registry, "1.1.74", SutraOperator.SAMJNA, "assigns vrddha to tyadadi terms by list membership", lambda c: is_vrddha_word(str(c.get("word")), tyadadi=bool(c.get("tyadadi"))), _ctx("1.1.74", word="tyad", tyadadi=True), _ctx("1.1.74", word="tyad", tyadadi=False), "samjna:vrddha")
    _add(registry, "1.1.75", SutraOperator.SAMJNA, "assigns vrddha to eastern names beginning with e/o", lambda c: is_vrddha_word(str(c.get("word")), eastern_name=bool(c.get("eastern_name"))), _ctx("1.1.75", word="eka", eastern_name=True), _ctx("1.1.75", word="eka", eastern_name=False), "samjna:vrddha")

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
            lambda c, marker=expected_marker: marker in analyze_it_markers(str(c.get("upadesha")), str(c.get("kind", "suffix"))).markers,
            _ctx(sutra_id, upadesha=raw, kind=kind),
            _ctx(sutra_id, upadesha=negative, kind=kind),
            "samjna:it",
        )
    _add(registry, "1.3.4", SutraOperator.PRATISEDHA, "blocks tusmah-final it marking in vibhakti endings", lambda c: not analyze_it_markers(str(c.get("upadesha")), str(c.get("kind", "vibhakti"))).markers, _ctx("1.3.4", upadesha="tas", kind="vibhakti"), _ctx("1.3.4", upadesha="tas", kind="suffix"), "block:it")
    _add(registry, "1.3.9", SutraOperator.VIDHI, "removes it markers from the usable surface", lambda c: analyze_it_markers(str(c.get("upadesha")), str(c.get("kind", "suffix"))).lemma == c.get("lemma"), _ctx("1.3.9", upadesha="tak", lemma="ta"), _ctx("1.3.9", upadesha="tak", lemma="tak"), "operation:lopa")

    _add(registry, "1.4.3", SutraOperator.SAMJNA, "assigns nadi to feminine i/u-final stems", lambda c: Samjna.NADII in assign_technical_names(c.get("analysis")).samjnas, _ctx("1.4.3", analysis=_analysis("nadī", "nadī", PartOfSpeech.NOUN, gender=Gender.FEMININE)), _ctx("1.4.3", analysis=_analysis("agni", "agni", PartOfSpeech.NOUN, gender=Gender.MASCULINE)), "samjna:nadi")
    _add(registry, "1.4.7", SutraOperator.SAMJNA, "assigns ghi to remaining i/u-final stems except sakhi", lambda c: Samjna.GHI in assign_technical_names(c.get("analysis")).samjnas, _ctx("1.4.7", analysis=_analysis("agni", "agni", PartOfSpeech.NOUN, gender=Gender.MASCULINE)), _ctx("1.4.7", analysis=_analysis("sakhi", "sakhi", PartOfSpeech.NOUN, gender=Gender.MASCULINE)), "samjna:ghi")
    _add(registry, "1.4.10", SutraOperator.SAMJNA, "assigns laghu to short vowels", lambda c: get_vowel_weight(str(c.get("word")), int(c.get("index", 0))) == Samjna.LAGHU, _ctx("1.4.10", word="aga", index=0), _ctx("1.4.10", word="āgama", index=0), "samjna:laghu")
    _add(registry, "1.4.11", SutraOperator.SAMJNA, "assigns guru to a vowel before a consonant cluster", lambda c: get_vowel_weight(str(c.get("word")), int(c.get("index", 0))) == Samjna.GURU, _ctx("1.4.11", word="akta", index=0), _ctx("1.4.11", word="aga", index=0), "samjna:guru")
    _add(registry, "1.4.12", SutraOperator.SAMJNA, "assigns guru to long vowels and diphthongs", lambda c: get_vowel_weight(str(c.get("word")), int(c.get("index", 0))) == Samjna.GURU, _ctx("1.4.12", word="āgama", index=0), _ctx("1.4.12", word="aga", index=0), "samjna:guru")
    _add(registry, "1.4.13", SutraOperator.SAMJNA, "assigns anga to the base before a suffix", lambda c: c.get("suffix") is not None and Samjna.ANGA in assign_technical_names(c.get("analysis"), str(c.get("suffix"))).samjnas, _ctx("1.4.13", analysis=_analysis("deva", "deva", PartOfSpeech.NOUN), suffix="su"), _ctx("1.4.13", analysis=_analysis("deva", "deva", PartOfSpeech.NOUN), suffix=None), "samjna:anga")
    _add(registry, "1.4.14", SutraOperator.SAMJNA, "assigns pada to sup/tin-ending analyses", lambda c: is_pada(c.get("analysis")), _ctx("1.4.14", analysis=_analysis("devah", "deva", PartOfSpeech.NOUN, case=Case.NOMINATIVE)), _ctx("1.4.14", analysis=_analysis("deva", "deva", PartOfSpeech.NOUN)), "samjna:pada")
    _add(registry, "1.4.17", SutraOperator.SAMJNA, "keeps pada before selected svadi non-sarvanamasthana suffixes", lambda c: Samjna.PADA in assign_technical_names(c.get("analysis"), str(c.get("suffix"))).samjnas, _ctx("1.4.17", analysis=_analysis("devah", "deva", PartOfSpeech.NOUN, case=Case.NOMINATIVE), suffix="su"), _ctx("1.4.17", analysis=_analysis("deva", "deva", PartOfSpeech.NOUN), suffix="su"), "samjna:pada")
    _add(registry, "1.4.18", SutraOperator.SAMJNA, "assigns bha before y or vowel-initial suffixes", lambda c: Samjna.BHA in assign_technical_names(c.get("analysis"), str(c.get("suffix"))).samjnas, _ctx("1.4.18", analysis=_analysis("devah", "deva", PartOfSpeech.NOUN, case=Case.NOMINATIVE), suffix="ya"), _ctx("1.4.18", analysis=_analysis("devah", "deva", PartOfSpeech.NOUN, case=Case.NOMINATIVE), suffix="ta"), "samjna:bha")

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
        _add(registry, sutra_id, SutraOperator.SAMJNA, f"assigns karaka role {role.value} for {context}", lambda c, expected=role: get_karaka_role(str(c.get("verb")), str(c.get("context"))) == expected, _ctx(sutra_id, verb=verb, context=context), _ctx(sutra_id, verb=verb, context="unrelated"), f"karaka:{role.value}")
    _add(registry, "1.4.58", SutraOperator.SAMJNA, "recognizes pra and related prefixes as gati material", lambda c: str(c.get("prefix")) in upasarga_surfaces(), _ctx("1.4.58", prefix="pra"), _ctx("1.4.58", prefix="ca"), "samjna:gati")
    _add(registry, "1.4.59", SutraOperator.SAMJNA, "recognizes upasarga when prefixes are in verbal connection", lambda c: str(c.get("prefix")) in upasarga_surfaces() and bool(c.get("verb_connection")), _ctx("1.4.59", prefix="pra", verb_connection=True), _ctx("1.4.59", prefix="pra", verb_connection=False), "samjna:upasarga")
    _add(registry, "1.4.60", SutraOperator.SAMJNA, "preserves gati relation metadata for controlled upasargas", lambda c: str(c.get("prefix")) in upasarga_surfaces() and bool(c.get("gati_relation")), _ctx("1.4.60", prefix="upa", gati_relation=True), _ctx("1.4.60", prefix="upa", gati_relation=False), "samjna:gati")
    _add(registry, "1.4.109", SutraOperator.SAMJNA, "assigns samhita to close phonological proximity", lambda c: is_samhita(str(c.get("word"))), _ctx("1.4.109", word="agnim"), _ctx("1.4.109", word=""), "samjna:samhita")
    _add(registry, "1.4.110", SutraOperator.SAMJNA, "assigns avasana to cessation after the final sound", lambda c: is_avasana(str(c.get("word")), int(c.get("index", 0))), _ctx("1.4.110", word="agni", index=4), _ctx("1.4.110", word="agni", index=1), "samjna:avasana")

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
            lambda c, pada=expected: pada in determine_available_padas(c.get("markers", frozenset()), str(c.get("lemma")), tuple(c.get("prefixes", ())), bool(c.get("reflexive"))),
            _ctx(sutra_id, markers=markers, lemma=lemma, prefixes=prefixes, reflexive=reflexive),
            _ctx(sutra_id, markers=frozenset(), lemma="bhū", prefixes=(), reflexive=False),
            f"pada:{expected.value}",
        )
    _add(
        registry,
        "1.3.78",
        SutraOperator.VIDHI,
        "defaults the remaining active-agent domain to parasmaipada",
        lambda c: Pada.PARASMAIPADA in determine_available_padas(c.get("markers", frozenset()), str(c.get("lemma")), tuple(c.get("prefixes", ())), bool(c.get("reflexive"))),
        _ctx("1.3.78", markers=frozenset(), lemma="bhū", prefixes=(), reflexive=False),
        _ctx("1.3.78", markers=frozenset({"ṅ"}), lemma="", prefixes=(), reflexive=False),
        "pada:parasmaipada",
    )

    return registry


SUTRA_LOGIC = _build_registry()
