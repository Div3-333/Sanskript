from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from typing import Any

from .adhyaya123_engines import (
    AdhyayaThreeRealizationEngine,
    KarakaVibhaktiEngine,
    KrtDerivationEngine,
    MetaruleGovernanceEngine,
    PratyayaLopaEngine,
    SamasaDerivationEngine,
    SamjnaTechnicalEngine,
    SubantaSupEngine,
    TinantaLakaraEngine,
)
from .adhyaya45_engines import (
    derive_adhyaya45_taddhita,
    derive_samasanta,
    derive_stri,
    resolve_adhyaya45_source,
)
from .adhyaya678_engines import AdhyayaSixSevenEightExecutionEngine
from .paninian_effects import (
    CONTEXT_STATE_KEYS,
    features_from_adhyaya45_result,
    features_from_engine_result,
    has_meaningful_effect,
    merge_step_effects,
)
from .derivation import KrtSuffix, TaddhitaSuffix
from .grammar import Analysis, Case, Gender, GrammaticalNumber, Lakara, Pada, PartOfSpeech, Person, Role
from .samasa import SamasaType
from .subanta import DeclensionStem
from .sutra_logic import SutraContext, SutraDecision, SutraOperator, evaluate_sutra, implemented_logic_ids, positive_context_for
from .tinanta import Dhatu, DhatuType, TimeContext, TinEnding


FeatureMap = Mapping[str, Any]


@dataclass(frozen=True)
class PaninianStep:
    sutra_id: str
    operator: str
    engine: str
    operation: str
    before: str
    after: str
    reason: str
    assigned: tuple[str, ...] = ()
    blocked_by: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()

    @property
    def changed(self) -> bool:
        return self.before != self.after


@dataclass(frozen=True)
class PaninianState:
    form: str = ""
    features: FeatureMap = field(default_factory=dict)
    members: tuple[Analysis, ...] = ()
    source: str = ""
    dhatu: Dhatu | None = None
    stem: DeclensionStem | None = None
    suffix: KrtSuffix | TaddhitaSuffix | str | None = None
    case: Case | None = None
    number: GrammaticalNumber | None = None
    person: Person | None = None
    lakara: Lakara | None = None
    pada: Pada | None = None
    gender: Gender | None = None
    role: Role | None = None
    history: tuple[PaninianStep, ...] = ()
    blocked_sutras: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "features", dict(self.features))
        object.__setattr__(self, "members", tuple(self.members))
        object.__setattr__(self, "history", tuple(self.history))
        object.__setattr__(self, "blocked_sutras", tuple(self.blocked_sutras))

    @property
    def applied_sutras(self) -> tuple[str, ...]:
        return tuple(step.sutra_id for step in self.history)

    def feature_query(self) -> dict[str, Any]:
        query = dict(self.features)
        if self.form:
            query.setdefault("form", self.form)
            query.setdefault("surface", self.form)
        if self.members:
            query.setdefault("members", self.members)
        if self.source:
            query.setdefault("source", self.source)
        if self.dhatu is not None:
            query.setdefault("lemma", self.dhatu.lemma)
            query.setdefault("dhatu_lemma", self.dhatu.lemma)
            query.setdefault("dhatu", self.dhatu.lemma)
            query.setdefault("pada", self.dhatu.pada)
        if self.stem is not None:
            query.setdefault("source", self.stem.lemma)
            query.setdefault("stem", self.stem.lemma)
            query.setdefault("gender", self.stem.gender)
        if self.suffix is not None:
            query.setdefault("suffix", self.suffix.value if hasattr(self.suffix, "value") else self.suffix)
        if self.case is not None:
            query.setdefault("case", self.case)
        if self.number is not None:
            query.setdefault("number", self.number)
        if self.person is not None:
            query.setdefault("person", self.person)
        if self.lakara is not None:
            query.setdefault("lakara", self.lakara)
        if self.pada is not None:
            query.setdefault("pada", self.pada)
        if self.gender is not None:
            query.setdefault("gender", self.gender)
        if self.role is not None:
            query.setdefault("role", self.role)
        return query

    def advance(
        self,
        step: PaninianStep,
        *,
        form: str | None = None,
        features: FeatureMap | None = None,
        dhatu: Dhatu | None = None,
    ) -> "PaninianState":
        merged_features = dict(self.features)
        if features:
            merged_features.update(features)
        next_form = self.form if form is None else form
        if next_form:
            merged_features["form"] = next_form
            merged_features["surface"] = next_form
        next_case = merged_features.get("case", self.case)
        if isinstance(next_case, str):
            next_case = self._enum_from_value(Case, next_case)
        next_role = merged_features.get("role", self.role)
        if isinstance(next_role, str):
            next_role = self._enum_from_value(Role, next_role)
        next_gender = merged_features.get("gender", self.gender)
        if isinstance(next_gender, str):
            next_gender = self._enum_from_value(Gender, next_gender)
        next_lakara = merged_features.get("lakara", self.lakara)
        if isinstance(next_lakara, str):
            next_lakara = self._enum_from_value(Lakara, next_lakara)
        next_pada = merged_features.get("pada", self.pada)
        if isinstance(next_pada, str):
            next_pada = self._enum_from_value(Pada, next_pada)
        next_person = merged_features.get("person", self.person)
        if isinstance(next_person, str):
            next_person = self._enum_from_value(Person, next_person)
        next_number = merged_features.get("number", self.number)
        if isinstance(next_number, str):
            next_number = self._enum_from_value(GrammaticalNumber, next_number)
        return replace(
            self,
            form=next_form,
            features=merged_features,
            dhatu=dhatu if dhatu is not None else self.dhatu,
            case=next_case if isinstance(next_case, Case) else self.case,
            role=next_role if isinstance(next_role, Role) else self.role,
            gender=next_gender if isinstance(next_gender, Gender) else self.gender,
            lakara=next_lakara if isinstance(next_lakara, Lakara) else self.lakara,
            pada=next_pada if isinstance(next_pada, Pada) else self.pada,
            person=next_person if isinstance(next_person, Person) else self.person,
            number=next_number if isinstance(next_number, GrammaticalNumber) else self.number,
            history=self.history + (step,),
            blocked_sutras=tuple(dict.fromkeys(self.blocked_sutras + step.blocked_by)),
        )

    @staticmethod
    def _enum_from_value(enum_type, value: Any):
        if isinstance(value, enum_type):
            return value
        for item in enum_type:
            if value in {item.value, item.name, item.name.lower()}:
                return item
        return None


@dataclass(frozen=True)
class RuleCandidate:
    sutra_id: str
    context: dict[str, Any]
    decision: SutraDecision
    explicit: bool = False

    @property
    def operator(self) -> SutraOperator:
        return self.decision.operator

    @property
    def specificity(self) -> int:
        useful = 0
        for value in self.context.values():
            if value in (None, "", "__miss__"):
                continue
            if isinstance(value, bool) and value is False:
                continue
            useful += 1
        return useful + len(self.decision.assigned)


@dataclass(frozen=True)
class PaninianDerivation:
    initial: PaninianState
    final: PaninianState
    candidates_seen: tuple[str, ...]

    @property
    def form(self) -> str:
        return self.final.form

    @property
    def steps(self) -> tuple[PaninianStep, ...]:
        return self.final.history

    @property
    def sutra_ids(self) -> tuple[str, ...]:
        return tuple(step.sutra_id for step in self.steps)

    @property
    def operations(self) -> tuple[str, ...]:
        return tuple(step.operation for step in self.steps)


def _sutra_sort_key(sutra_id: str) -> tuple[int, int, int]:
    parts = [int(part) for part in sutra_id.split(".")]
    while len(parts) < 3:
        parts.append(0)
    return (parts[0], parts[1], parts[2])


def _is_useful_query_key(key: str) -> bool:
    return key not in {"form", "surface", "expected_surface", "output", "strict_engine"}


def _values_match(left: Any, right: Any) -> bool:
    if left == right:
        return True
    left_value = getattr(left, "value", left)
    right_value = getattr(right, "value", right)
    return left_value == right_value


def _context_contains_query(base: FeatureMap, query: FeatureMap) -> bool:
    for key, value in query.items():
        if not _is_useful_query_key(key):
            continue
        if key in base and _values_match(base[key], value):
            return True
    return False


def _merge_context(base: FeatureMap, query: FeatureMap) -> dict[str, Any]:
    merged = dict(base)
    merged.update(query)
    return merged


class RuleSelectionEngine:
    """Select sutra predicates by reusing the truth-gated registry."""

    def select(
        self,
        state: PaninianState,
        *,
        sutra_ids: Sequence[str] | None = None,
        prefixes: Sequence[str] | None = None,
    ) -> tuple[RuleCandidate, ...]:
        query = state.feature_query()
        explicit = sutra_ids is not None
        ids = tuple(sutra_ids or sorted(implemented_logic_ids(), key=_sutra_sort_key))
        active_prefixes = tuple(prefixes or ())
        candidates: list[RuleCandidate] = []
        for sutra_id in ids:
            if active_prefixes and not sutra_id.startswith(active_prefixes):
                continue
            if sutra_id in state.blocked_sutras:
                continue
            candidate = self._candidate(sutra_id, query, explicit=explicit)
            if candidate is not None:
                candidates.append(candidate)
        return tuple(candidates)

    def _candidate(self, sutra_id: str, query: FeatureMap, *, explicit: bool) -> RuleCandidate | None:
        try:
            base = positive_context_for(sutra_id).features
        except ValueError:
            return None
        if not explicit and not _context_contains_query(base, query):
            return None
        contexts = []
        if explicit and query:
            contexts.append(dict(query))
        contexts.append(_merge_context(base, query))
        for features in contexts:
            context = SutraContext(features, sutra_id=sutra_id)
            decision = evaluate_sutra(sutra_id, context)
            if decision.applies:
                return RuleCandidate(sutra_id, dict(features), decision, explicit=explicit)
        return None


class PrecedenceEngine:
    """Resolve utsarga/apavada and vipratisedha through reusable ranking."""

    OPERATOR_RANK: dict[SutraOperator, int] = {
        SutraOperator.ADHIKARA: 0,
        SutraOperator.ATIDESA: 1,
        SutraOperator.SAMJNA: 2,
        SutraOperator.PARIBHASHA: 3,
        SutraOperator.VIBHASHA: 4,
        SutraOperator.VIDHI: 5,
        SutraOperator.PRATISEDHA: 6,
    }

    def resolve(self, candidates: Iterable[RuleCandidate]) -> RuleCandidate | None:
        pool = tuple(candidates)
        if not pool:
            return None
        return sorted(pool, key=self.priority)[-1]

    def priority(self, candidate: RuleCandidate) -> tuple[int, int, int, int, tuple[int, int, int]]:
        serial = _sutra_sort_key(candidate.sutra_id)
        tripadi = 1 if serial >= (8, 2, 1) else 0
        explicit = 1 if candidate.explicit else 0
        operator = self.OPERATOR_RANK.get(candidate.operator, 0)
        return (explicit, candidate.specificity, operator, tripadi, serial)


class TransformationDispatcher:
    """Dispatch selected sutras into the domain engines that perform work."""

    def __init__(self) -> None:
        self.technical = SamjnaTechnicalEngine()
        self.governance = MetaruleGovernanceEngine()
        self.samasa = SamasaDerivationEngine()
        self.karaka = KarakaVibhaktiEngine()
        self.subanta = SubantaSupEngine()
        self.lopa = PratyayaLopaEngine()
        self.krt = KrtDerivationEngine()
        self.tinanta = TinantaLakaraEngine()
        self.adhyaya3 = AdhyayaThreeRealizationEngine(krt=self.krt, tinanta=self.tinanta)
        self.late = AdhyayaSixSevenEightExecutionEngine()

    def apply(self, state: PaninianState, candidate: RuleCandidate) -> PaninianState:
        sutra_id = candidate.sutra_id
        if sutra_id.startswith(("6.", "7.", "8.")):
            return self._apply_late(state, candidate)
        if sutra_id.startswith(("4.", "5.")):
            return self._apply_adhyaya45(state, candidate)
        if sutra_id.startswith("3."):
            return self._apply_adhyaya3(state, candidate)
        if sutra_id.startswith("2."):
            return self._apply_adhyaya2(state, candidate)
        if sutra_id.startswith("1."):
            return self._apply_adhyaya1(state, candidate)
        return self._trace_only(state, candidate, "TransformationDispatcher")

    def _features(self, state: PaninianState, candidate: RuleCandidate) -> dict[str, Any]:
        features = dict(candidate.context)
        features.update(state.features)
        if state.form:
            features.setdefault("form", state.form)
            features.setdefault("surface", state.form)
        if state.members:
            features.setdefault("members", state.members)
        if state.source:
            features.setdefault("source", state.source)
        return features

    def _step(
        self,
        candidate: RuleCandidate,
        engine: str,
        operation: str,
        before: str,
        after: str,
        *,
        assigned: tuple[str, ...] | None = None,
        diagnostics: Iterable[str] = (),
        blocked_by: Iterable[str] = (),
    ) -> PaninianStep:
        return PaninianStep(
            sutra_id=candidate.sutra_id,
            operator=candidate.operator.value,
            engine=engine,
            operation=operation or candidate.decision.action,
            before=before,
            after=after,
            reason=candidate.decision.reason,
            assigned=assigned if assigned is not None else candidate.decision.assigned,
            blocked_by=tuple(blocked_by),
            diagnostics=tuple(diagnostics),
        )

    def _finalize(
        self,
        state: PaninianState,
        candidate: RuleCandidate,
        engine: str,
        operation: str,
        before: str,
        *,
        after: str | None = None,
        extra_features: FeatureMap | None = None,
        assigned: tuple[str, ...] | None = None,
        diagnostics: Iterable[str] = (),
        blocked_by: Iterable[str] = (),
    ) -> PaninianState:
        features = self._features(state, candidate)
        merged_assigned = assigned if assigned is not None else candidate.decision.assigned
        merged_after, effect_features, phon_op = merge_step_effects(
            assigned=merged_assigned,
            context=features,
            form=before,
            existing_features=state.features,
        )
        if extra_features:
            for key, value in extra_features.items():
                if key in {"samjnas", "phonological_labels", "blocked_operations"} and not value:
                    if effect_features.get(key):
                        continue
                effect_features[key] = value
        resolved_after = before if after is None else after
        if phon_op and merged_after != before:
            resolved_after = merged_after
            operation = phon_op if operation == candidate.decision.action else f"{operation} + {phon_op}"
        step = self._step(
            candidate,
            engine,
            operation,
            before,
            resolved_after,
            assigned=merged_assigned,
            diagnostics=diagnostics,
            blocked_by=blocked_by,
        )
        effect_features["last_sutra"] = candidate.sutra_id
        next_form = resolved_after if resolved_after != before else None
        return state.advance(step, form=next_form, features=effect_features)

    def _trace_only(self, state: PaninianState, candidate: RuleCandidate, engine: str) -> PaninianState:
        before = state.form or str(
            candidate.context.get("form")
            or candidate.context.get("surface")
            or candidate.context.get("source")
            or candidate.context.get("term")
            or ""
        )
        return self._finalize(state, candidate, engine, candidate.decision.action, before)

    def _apply_late(self, state: PaninianState, candidate: RuleCandidate) -> PaninianState:
        features = self._features(state, candidate)
        result = self.late.derive(candidate.sutra_id, features)
        before = result.input or state.form or str(features.get("form") or features.get("source") or "")
        after = result.output or before
        operation = " + ".join(result.operations) if result.operations else candidate.decision.action
        blocked_by = tuple(result.blocked_by)
        if not blocked_by and (features.get("rule_blocked") or features.get("blocks_rule")):
            blocked_by = (candidate.sutra_id,)
        step = self._step(
            candidate,
            result.engine,
            operation,
            before,
            after,
            diagnostics=result.diagnostics,
            blocked_by=blocked_by,
        )
        effect_features = features_from_engine_result(
            result,
            context=features,
            assigned=candidate.decision.assigned,
            existing_features=state.features,
        )
        next_form = after if after != before or after else None
        return state.advance(step, form=next_form, features=effect_features)

    def _apply_adhyaya45(self, state: PaninianState, candidate: RuleCandidate) -> PaninianState:
        features = self._features(state, candidate)
        source = resolve_adhyaya45_source(features) or state.source or str(features.get("source") or state.form or "")
        before = state.form or source
        third = _sutra_sort_key(candidate.sutra_id)[2]
        if candidate.sutra_id.startswith("4.1.") and third <= 75:
            result = derive_stri(source, sutra_id=candidate.sutra_id, features=features)
        elif candidate.sutra_id.startswith("5.4."):
            result = derive_samasanta(source or None, sutra_id=candidate.sutra_id, features=features)
        else:
            suffix = state.suffix or features.get("suffix")
            result = derive_adhyaya45_taddhita(source, sutra_id=candidate.sutra_id, suffix=suffix, features=features)
        operation = " + ".join(result.operations) if result.operations else result.semantic
        after = result.surface or before
        step = self._step(candidate, result.engines[-1], operation, before, after)
        effect_features = features_from_adhyaya45_result(
            result,
            context=features,
            sutra_id=candidate.sutra_id,
            existing_features=state.features,
        )
        next_form = after if after != before or after else None
        return state.advance(step, form=next_form, features=effect_features)

    def _apply_adhyaya3(self, state: PaninianState, candidate: RuleCandidate) -> PaninianState:
        features = self._features(state, candidate)
        before = state.form or str(features.get("source") or features.get("lemma") or "")
        dhatu = state.dhatu or self._dhatu_from_features(features)
        dhatu_type = self._dhatu_type_from_features(features)
        lakara = state.lakara or features.get("lakara")
        if isinstance(lakara, str):
            lakara = self._enum_from_value(Lakara, lakara)
        pada = state.pada or features.get("pada")
        if isinstance(pada, str):
            pada = self._enum_from_value(Pada, pada)
        suffix = self._suffix_from_candidate(state, candidate)
        krt_suffix = self._krt_suffix(suffix)

        realized = self.adhyaya3.derive_for_sutra(
            candidate.sutra_id,
            features,
            candidate.decision.assigned,
            before=before,
            dhatu=dhatu,
            source=state.source,
            suffix=suffix,
            lakara=lakara if isinstance(lakara, Lakara) else None,
            pada=pada if isinstance(pada, Pada) else None,
            person=state.person,
            number=state.number,
            operator=candidate.operator.value,
        )
        if realized is not None:
            operation = " + ".join(realized.operations) if realized.operations else candidate.decision.action
            step = self._step(
                candidate,
                realized.engines[0],
                operation,
                realized.input_form,
                realized.output_form,
                blocked_by=realized.blocked_by,
            )
            next_form = realized.output_form if realized.output_form != realized.input_form or realized.output_form else None
            return state.advance(step, form=next_form, features=realized.features, dhatu=realized.dhatu)

        if dhatu is None and dhatu_type is not None and candidate.sutra_id.startswith("3.1."):
            roots = features.get("roots")
            lemma = "bhū"
            if isinstance(roots, (list, tuple)) and roots:
                lemma = str(roots[0])
            dhatu = self._dhatu_from_features({**features, "lemma": lemma})

        if features.get("varga") is not None and candidate.sutra_id.startswith("3.1."):
            from .adhyaya123_engines import DhatuSanadiEngine

            varga = int(features.get("varga", 1) or 1)
            result = DhatuSanadiEngine().vikarana(varga)
            operation = " + ".join(result.operations) if result.operations else f"vikarana:{result.vikarana}"
            return self._finalize(
                state,
                candidate,
                result.engines[0],
                operation,
                before,
                extra_features={"varga": varga, "vikarana": result.vikarana},
            )

        if dhatu is not None and dhatu_type is not None and candidate.sutra_id.startswith("3.1."):
            result = self.krt_to_dhatu(dhatu, dhatu_type)
            step = self._step(candidate, result.engines[0], " + ".join(result.operations), before or dhatu.lemma, result.output.present_stem)
            return state.advance(step, form=result.output.present_stem, features={"lemma": result.output.lemma}, dhatu=result.output)

        source = self._derivation_source(state, features, before)
        if source and krt_suffix is not None:
            try:
                result = self.krt.derive(source, krt_suffix)
            except (KeyError, TypeError, ValueError) as exc:
                return self._trace_with_diagnostic(state, candidate, "KrtDerivationEngine", before, str(exc))
            suffix_value = krt_suffix.value if hasattr(krt_suffix, "value") else str(krt_suffix)
            step = self._step(candidate, result.engines[0], " + ".join(result.operations), source, result.derived.surface)
            return state.advance(
                step,
                form=result.derived.surface,
                features={"source": source, "suffix": suffix_value, "last_sutra": candidate.sutra_id},
            )

        if dhatu is not None and lakara is not None:
            person = state.person or features.get("person") or Person.THIRD
            number = state.number or features.get("number") or GrammaticalNumber.SINGULAR
            if isinstance(person, str):
                person = self._enum_from_value(Person, person) or Person.THIRD
            if isinstance(number, str):
                number = self._enum_from_value(GrammaticalNumber, number) or GrammaticalNumber.SINGULAR
            try:
                result = self.tinanta.conjugate(dhatu, lakara, person=person, number=number)
            except (KeyError, TypeError, ValueError) as exc:
                return self._trace_with_diagnostic(state, candidate, "TinantaLakaraEngine", before, str(exc))
            after = result.requested_form or before
            operation = " + ".join(result.operations) if result.operations else f"lakara:{lakara.value}"
            step = self._step(candidate, "TinantaLakaraEngine", operation, before or dhatu.present_stem, after)
            extra: dict[str, Any] = {"lakara": lakara, "last_sutra": candidate.sutra_id}
            if pada is not None:
                extra["pada"] = pada
            return state.advance(step, form=after, features=extra)

        if self._has_derivational_fixture(features, suffix=suffix, lakara=lakara, pada=pada):
            return self._record_derivation_context(
                state,
                candidate,
                before,
                engine=self._adhyaya3_context_engine(features, suffix=suffix, lakara=lakara, pada=pada),
                suffix=suffix,
                lakara=lakara,
                pada=pada,
            )

        return self._trace_only(state, candidate, "Adhyaya3Dispatch")

    def krt_to_dhatu(self, dhatu: Dhatu, dhatu_type: DhatuType):
        from .adhyaya123_engines import DhatuSanadiEngine

        return DhatuSanadiEngine().derive(dhatu, dhatu_type)

    def _apply_adhyaya2(self, state: PaninianState, candidate: RuleCandidate) -> PaninianState:
        features = self._features(state, candidate)
        before = state.form or str(features.get("surface") or features.get("source") or "")
        members = state.members or tuple(features.get("members") or ())
        if members and candidate.sutra_id.startswith(("2.1.", "2.2.", "2.4.")):
            forced_type = features.get("compound_type")
            if isinstance(forced_type, str):
                forced_type = self._enum_from_value(SamasaType, forced_type)
            try:
                result = self.samasa.derive(members, forced_type=forced_type)
            except (KeyError, TypeError, ValueError) as exc:
                return self._trace_with_diagnostic(state, candidate, "SamasaDerivationEngine", before, str(exc))
            operation = " + ".join(result.operations)
            step = self._step(candidate, "SamasaDerivationEngine", operation, before or " ".join(m.surface for m in members), result.compound.surface)
            return state.advance(
                step,
                form=result.compound.surface,
                features={"compound_type": result.compound.type, "last_sutra": candidate.sutra_id},
            )

        if candidate.sutra_id.startswith(("2.1.", "2.2.")):
            try:
                result = self.samasa.derive_for_sutra(candidate.sutra_id, features)
            except (KeyError, TypeError, ValueError) as exc:
                return self._trace_with_diagnostic(state, candidate, "SamasaDerivationEngine", before, str(exc))
            if result is not None:
                operation = " + ".join(result.operations)
                step = self._step(candidate, "SamasaDerivationEngine", operation, result.compound.gloss, result.compound.surface)
                extra_features: dict[str, Any] = {
                    "compound_type": result.compound.type,
                    "compound_members": tuple(member.lemma for member in result.compound.members),
                    "last_sutra": candidate.sutra_id,
                }
                if result.compound.sense is not None:
                    extra_features["compound_sense"] = result.compound.sense
                if result.compound.result_analysis is not None:
                    extra_features["analysis"] = result.compound.result_analysis
                    if result.compound.result_analysis.gender is not None:
                        extra_features["gender"] = result.compound.result_analysis.gender
                    if result.compound.result_analysis.number is not None:
                        extra_features["number"] = result.compound.result_analysis.number
                return state.advance(step, form=result.compound.surface, features=extra_features)

        if candidate.sutra_id.startswith("2.4."):
            try:
                result = self.samasa.derive_for_sutra(candidate.sutra_id, features)
            except (KeyError, TypeError, ValueError) as exc:
                return self._trace_with_diagnostic(state, candidate, "SamasaDerivationEngine", before, str(exc))
            if result is not None:
                operation = " + ".join(result.operations)
                step = self._step(candidate, "SamasaDerivationEngine", operation, result.compound.gloss, result.compound.surface)
                extra_features: dict[str, Any] = {
                    "compound_type": result.compound.type,
                    "compound_members": tuple(member.lemma for member in result.compound.members),
                    "last_sutra": candidate.sutra_id,
                }
                if result.compound.result_analysis is not None:
                    extra_features["analysis"] = result.compound.result_analysis
                    if result.compound.result_analysis.gender is not None:
                        extra_features["gender"] = result.compound.result_analysis.gender
                    if result.compound.result_analysis.number is not None:
                        extra_features["number"] = result.compound.result_analysis.number
                return state.advance(step, form=result.compound.surface, features=extra_features)

        dhatu = state.dhatu or self._dhatu_from_features(features)
        if dhatu is None and features.get("dhatu_lemma"):
            dhatu = self._dhatu_from_features({**features, "lemma": features["dhatu_lemma"]})
        lakara = state.lakara or features.get("lakara")
        if isinstance(lakara, str):
            lakara = self._enum_from_value(Lakara, lakara)
        pada = state.pada or features.get("pada")
        if isinstance(pada, str):
            pada = self._enum_from_value(Pada, pada)

        if candidate.sutra_id.startswith("2.3."):
            role = state.role or features.get("role")
            if isinstance(role, str):
                role = self._enum_from_value(Role, role)
            semantic_context = (
                features.get("semantic_context")
                or features.get("semantic")
                or self._semantic_context_for_vibhakti(candidate.sutra_id, features)
            )
            try:
                result = self.karaka.select_case(
                    verb_lemma=str(features.get("verb_lemma") or features.get("verb") or ""),
                    role=role,
                    companion_lemma=features.get("companion"),
                    is_already_expressed=bool(features.get("expressed")),
                    semantic_context=semantic_context,
                )
            except (KeyError, TypeError, ValueError) as exc:
                return self._trace_with_diagnostic(state, candidate, "KarakaVibhaktiEngine", before, str(exc))
            operation = " + ".join(result.operations) if result.operations else f"vibhakti:{result.case.value}"
            extra_features: dict[str, Any] = {
                "case": result.case,
                "role": result.role,
                "assigned_case": result.case,
                "allowed_cases": tuple(sorted(case.value for case in result.allowed_cases)),
                "case_rule": candidate.sutra_id,
                "derivation_family": "vibhakti-selection",
            }
            if features.get("companion"):
                extra_features["companion"] = features["companion"]
            if features.get("expressed"):
                extra_features["expressed"] = True
                extra_features["anabhihita_gate"] = "blocked"
            if semantic_context:
                extra_features["case_basis"] = semantic_context
            return self._finalize(
                state,
                candidate,
                "KarakaVibhaktiEngine",
                operation,
                before,
                extra_features=extra_features,
            )

        if dhatu is not None and lakara is not None and candidate.sutra_id.startswith("2.4."):
            try:
                result = self.lopa.substitute_dhatu(dhatu, lakara)
            except (KeyError, TypeError, ValueError) as exc:
                return self._trace_with_diagnostic(state, candidate, "PratyayaLopaEngine", before, str(exc))
            operation = " + ".join(result.operations) if result.operations else candidate.decision.action
            after = result.output.lemma
            step = self._step(candidate, "PratyayaLopaEngine", operation, before or dhatu.lemma, after)
            extra = {
                "lemma": result.output.lemma,
                "lakara": lakara,
                "last_sutra": candidate.sutra_id,
                "root_substitution": result.output.lemma,
                "derivation_family": "dhatu-substitution",
            }
            if features.get("suffix"):
                extra["suffix"] = features["suffix"]
            if pada is not None:
                extra["pada"] = pada
            return state.advance(step, form=after, features=extra, dhatu=result.output)

        if candidate.sutra_id.startswith("2.4."):
            try:
                lopa_result = self.lopa.derive_for_sutra(candidate.sutra_id, features)
            except (KeyError, TypeError, ValueError) as exc:
                return self._trace_with_diagnostic(state, candidate, "PratyayaLopaEngine", before, str(exc))
            if lopa_result is not None:
                operation = " + ".join(lopa_result.operations)
                blocked_by = (candidate.sutra_id,) if lopa_result.blocked_operations else ()
                extra = dict(lopa_result.extra_features)
                if lopa_result.blocked_operations:
                    extra["blocked_operations"] = lopa_result.blocked_operations
                step = self._step(
                    candidate,
                    "PratyayaLopaEngine",
                    operation,
                    lopa_result.source or before,
                    lopa_result.output or before,
                    blocked_by=blocked_by,
                )
                next_form = lopa_result.output if lopa_result.output != lopa_result.source else None
                return state.advance(step, form=next_form, features=extra)

        if candidate.sutra_id.startswith("2.4.") and self._has_derivational_fixture(
            features, suffix=features.get("suffix"), lakara=lakara, pada=pada
        ):
            return self._record_derivation_context(
                state,
                candidate,
                before,
                engine="PratyayaLopaEngine",
                suffix=features.get("suffix"),
                lakara=lakara,
                pada=pada,
                dhatu_lemma=features.get("dhatu_lemma"),
            )

        if candidate.sutra_id == "2.4.35" and features.get("is_ardhadhatuka"):
            return self._finalize(
                state,
                candidate,
                "PratyayaLopaEngine",
                "adhikara:ardhadhatuka",
                before,
                extra_features={
                    "adhikara_scope": "ardhadhatuka",
                    "is_ardhadhatuka": True,
                    "derivation_domain": "ardhadhatuka",
                    "derivation_family": "pratyaya-governance",
                },
            )

        if candidate.sutra_id == "2.4.39" and features.get("is_chandas"):
            return self._finalize(
                state,
                candidate,
                "PratyayaLopaEngine",
                "vibhasha:chandas-ardhadhatuka",
                before,
                extra_features={
                    "domain": "chandas",
                    "optional": True,
                    "operation": "bahulam",
                    "optional_substitution": True,
                    "derivation_domain": "chandas-ardhadhatuka",
                    "derivation_family": "pratyaya-governance",
                },
            )

        if features.get("scope") or features.get("gender") is not None:
            engine = "MetaruleGovernanceEngine" if features.get("scope") else "SamasaDerivationEngine"
            extra_scope: dict[str, Any] = {}
            if features.get("scope"):
                extra_scope["scope"] = features["scope"]
            if features.get("gender") is not None:
                extra_scope["gender"] = features["gender"]
            return self._finalize(
                state,
                candidate,
                engine,
                candidate.decision.action,
                before,
                extra_features=extra_scope,
            )

        compound_type = features.get("compound_type")
        if compound_type is not None and candidate.sutra_id.startswith(("2.1.", "2.2.", "2.4.")):
            if isinstance(compound_type, str):
                compound_type = self._enum_from_value(SamasaType, compound_type)
            return self._finalize(
                state,
                candidate,
                "SamasaDerivationEngine",
                f"samasa:{compound_type.value if compound_type else 'context'}",
                before,
                extra_features={"compound_type": compound_type},
            )

        return self._trace_only(state, candidate, "Adhyaya2Dispatch")

    def _semantic_context_for_vibhakti(self, sutra_id: str, features: FeatureMap) -> str:
        if sutra_id == "2.3.54" and features.get("is_bhava_vacana"):
            return "bhava_vacana"
        if sutra_id == "2.3.57" and features.get("is_samartha"):
            return "vyavahara"
        if sutra_id == "2.3.58" and features.get("is_divasa"):
            return "tadartha"
        if sutra_id == "2.3.67" and features.get("kt_suffix") and features.get("is_vartamana"):
            return "vartamana_kta"
        if sutra_id == "2.3.68" and features.get("is_adhikarana_krit"):
            return "adhikarana_krit"
        return str(features.get("semantic_context") or features.get("semantic") or "")

    def _apply_adhyaya1(self, state: PaninianState, candidate: RuleCandidate) -> PaninianState:
        features = self._features(state, candidate)
        sutra_id = candidate.sutra_id
        analysis_feature = features.get("analysis")
        before = state.form or str(
            features.get("term")
            or features.get("surface")
            or features.get("source")
            or features.get("upadesha")
            or (analysis_feature.surface if isinstance(analysis_feature, Analysis) else "")
            or ""
        )
        if state.stem is not None and (state.case is not None or state.number is not None):
            try:
                result = self.subanta.decline(state.stem, case=state.case, number=state.number)
            except (KeyError, TypeError, ValueError) as exc:
                return self._trace_with_diagnostic(state, candidate, "SubantaSupEngine", before, str(exc))
            after = result.requested_form or before
            operation = " + ".join(result.operations)
            step = self._step(candidate, "SubantaSupEngine", operation, before or state.stem.lemma, after)
            return state.advance(step, form=after, features={"last_sutra": candidate.sutra_id})

        gov = self.governance.derive_for_sutra(sutra_id, features)
        if gov is not None:
            operation = " + ".join(gov.operations) if gov.operations else candidate.decision.action
            extra = dict(gov.extra_features)
            if gov.target_index is not None:
                extra.setdefault("substitution_index", gov.target_index)
            extra.setdefault("target_scope", gov.target_scope)
            extra.setdefault("derivation_family", "metarule-governance")
            extra.setdefault("governance_effect", operation)
            return self._finalize(
                state,
                candidate,
                "MetaruleGovernanceEngine",
                operation,
                before,
                after=gov.output_form,
                assigned=gov.assigned or candidate.decision.assigned,
                extra_features=extra,
            )

        tech = self.technical.derive_for_sutra(sutra_id, features)
        if tech is not None:
            operation = " + ".join(tech.operations) if tech.operations else candidate.decision.action
            extra: dict[str, Any] = {"samjnas": tech.samjnas}
            if tech.marker_analysis is not None:
                extra["upadesha"] = str(features.get("upadesha") or "")
                extra["lemma"] = tech.marker_analysis.lemma
                if tech.marker_analysis.markers:
                    extra["marker"] = next(iter(tech.marker_analysis.markers))
            if tech.analysis is not None:
                extra["analysis"] = tech.analysis
            after = before
            if tech.marker_analysis and tech.marker_analysis.lemma and tech.marker_analysis.lemma != before:
                after = tech.marker_analysis.lemma
            return self._finalize(
                state,
                candidate,
                "SamjnaTechnicalEngine",
                operation,
                before,
                after=after,
                assigned=tech.assigned or candidate.decision.assigned,
                extra_features=extra,
            )

        if any(key in features for key in ("substitute", "marker", "reference_case")) and before:
            result = self.governance.substitution_site(
                before,
                substitute=str(features.get("substitute") or ""),
                marker=str(features.get("marker") or ""),
                reference_case=features.get("reference_case") or "genitive",
            )
            operation = " + ".join(result.operations) if result.operations else result.behavior.value
            return self._finalize(
                state,
                candidate,
                "MetaruleGovernanceEngine",
                operation,
                before,
                after=result.output_form,
                extra_features={"substitution_index": result.target_index, "target_scope": result.target_scope},
            )

        analysis = features.get("analysis")
        if not isinstance(analysis, Analysis) and before:
            analysis = Analysis(before, str(features.get("lemma") or before), PartOfSpeech.NOUN)
        result = self.technical.classify(
            str(features.get("term")) if features.get("term") else None,
            suffix=str(features.get("suffix")) if features.get("suffix") else None,
            analysis=analysis,
            suffix_surface=str(features.get("suffix_surface")) if features.get("suffix_surface") else None,
            gender=state.gender or features.get("gender"),
            marker_upadesha=str(features.get("upadesha")) if features.get("upadesha") else None,
            marker_kind=str(features.get("kind") or "suffix"),
            is_taddhita_marker=bool(features.get("is_taddhita")),
        )
        operation = " + ".join(result.operations) if result.operations else candidate.decision.action
        return self._finalize(
            state,
            candidate,
            "SamjnaTechnicalEngine",
            operation,
            before,
            assigned=result.assigned or candidate.decision.assigned,
            extra_features={"samjnas": result.samjnas},
        )

    def _trace_with_diagnostic(
        self,
        state: PaninianState,
        candidate: RuleCandidate,
        engine: str,
        before: str,
        diagnostic: str,
    ) -> PaninianState:
        step = self._step(candidate, engine, candidate.decision.action, before, before, diagnostics=(diagnostic,))
        return state.advance(step, features={"last_sutra": candidate.sutra_id})

    def _assigned_tags(self, candidate: RuleCandidate) -> dict[str, str]:
        tags: dict[str, str] = {}
        for tag in candidate.decision.assigned:
            if ":" not in tag or tag.startswith("sutra:"):
                continue
            head, _, tail = tag.partition(":")
            if head and tail:
                tags[head] = tail
        return tags

    def _suffix_from_candidate(
        self,
        state: PaninianState,
        candidate: RuleCandidate,
    ) -> KrtSuffix | str | None:
        features = self._features(state, candidate)
        suffix = state.suffix or features.get("suffix")
        if suffix is not None:
            return suffix
        assigned_suffix = self._assigned_tags(candidate).get("suffix")
        if assigned_suffix:
            return self._krt_suffix(assigned_suffix) or assigned_suffix
        return None

    def _derivation_source(self, state: PaninianState, features: FeatureMap, before: str) -> str:
        return (
            state.source
            or str(features.get("source") or features.get("dhatu_lemma") or features.get("lemma") or before or "")
        ).strip()

    def _has_derivational_fixture(
        self,
        features: FeatureMap,
        *,
        suffix: KrtSuffix | str | None = None,
        lakara: Lakara | None = None,
        pada: Pada | None = None,
    ) -> bool:
        if suffix is not None or lakara is not None or pada is not None:
            return True
        for key in ("scope", "varga", "vikarana", "kind", "gender", "is_optional"):
            value = features.get(key)
            if value not in (None, "", (), False):
                return True
        return any(key in features and features[key] not in (None, "", ()) for key in CONTEXT_STATE_KEYS)

    def _adhyaya3_context_engine(
        self,
        features: FeatureMap,
        *,
        suffix: KrtSuffix | str | None = None,
        lakara: Lakara | None = None,
        pada: Pada | None = None,
    ) -> str:
        if features.get("scope"):
            return "MetaruleGovernanceEngine"
        if suffix is not None or features.get("upapada") or features.get("source") or features.get("dhatu_lemma"):
            return "KrtDerivationEngine"
        if lakara is not None or pada is not None or features.get("varga") is not None:
            return "TinantaLakaraEngine"
        return "DhatuSanadiEngine"

    def _record_derivation_context(
        self,
        state: PaninianState,
        candidate: RuleCandidate,
        before: str,
        *,
        engine: str,
        suffix: KrtSuffix | str | None = None,
        lakara: Lakara | None = None,
        pada: Pada | None = None,
        dhatu_lemma: str | None = None,
    ) -> PaninianState:
        features = self._features(state, candidate)
        extra: dict[str, Any] = {}
        if features.get("upapada"):
            extra["upapada"] = features["upapada"]
        if suffix is not None:
            extra["suffix"] = suffix.value if hasattr(suffix, "value") else suffix
        elif features.get("suffix") is not None:
            value = features["suffix"]
            extra["suffix"] = value.value if hasattr(value, "value") else value
        if lakara is not None:
            extra["lakara"] = lakara
        if pada is not None:
            extra["pada"] = pada
        lemma = dhatu_lemma or features.get("dhatu_lemma")
        if lemma:
            extra["dhatu_lemma"] = lemma
        if features.get("source"):
            extra["source"] = features["source"]
        if features.get("scope"):
            extra["scope"] = features["scope"]
        if features.get("varga") is not None:
            extra["varga"] = features["varga"]
        if features.get("gender") is not None:
            extra["gender"] = features["gender"]

        assigned = self._assigned_tags(candidate)
        operation = candidate.decision.action
        after: str | None = None
        if "derived" in assigned:
            after = assigned["derived"]
            operation = f"krt:{after}"
        elif suffix is not None:
            suffix_label = suffix.value if hasattr(suffix, "value") else str(suffix)
            operation = f"suffix:{suffix_label}"

        return self._finalize(
            state,
            candidate,
            engine,
            operation,
            before,
            after=after,
            extra_features=extra or None,
        )

    def _dhatu_from_features(self, features: FeatureMap) -> Dhatu | None:
        lemma = features.get("lemma") or features.get("dhatu") or features.get("dhatu_lemma")
        if not isinstance(lemma, str) or not lemma:
            return None
        pada = features.get("pada")
        if isinstance(pada, str):
            pada = self._enum_from_value(Pada, pada)
        if not isinstance(pada, Pada):
            pada = Pada.PARASMAIPADA
        stem = str(features.get("present_stem") or features.get("stem") or lemma)
        return Dhatu(lemma, stem, pada, str(features.get("gloss") or lemma), varga=int(features.get("varga", 1) or 1))

    def _dhatu_type_from_features(self, features: FeatureMap) -> DhatuType | None:
        value = features.get("dhatu_type") or features.get("kind")
        if isinstance(value, DhatuType):
            return value
        if not isinstance(value, str):
            return None
        aliases = {
            "san": DhatuType.DESIDERATIVE,
            "kyac": DhatuType.DENOMINATIVE,
            "yan": DhatuType.INTENSIVE,
            "yaṅ": DhatuType.INTENSIVE,
            "nic": DhatuType.CAUSATIVE,
            "ṇic": DhatuType.CAUSATIVE,
        }
        return aliases.get(value) or self._enum_from_value(DhatuType, value)

    def _krt_suffix(self, value: KrtSuffix | TaddhitaSuffix | str | None) -> KrtSuffix | None:
        if isinstance(value, KrtSuffix):
            return value
        if not isinstance(value, str):
            return None
        return self._enum_from_value(KrtSuffix, value)

    def _enum_from_value(self, enum_type, value: Any):
        if isinstance(value, enum_type):
            return value
        for item in enum_type:
            if value in {item.value, item.name, item.name.lower()}:
                return item
        return None


class PaninianDerivationEngine:
    """Dry coordinator over the already implemented sutra/domain engines."""

    def __init__(
        self,
        selector: RuleSelectionEngine | None = None,
        precedence: PrecedenceEngine | None = None,
        dispatcher: TransformationDispatcher | None = None,
    ) -> None:
        self.selector = selector or RuleSelectionEngine()
        self.precedence = precedence or PrecedenceEngine()
        self.dispatcher = dispatcher or TransformationDispatcher()

    def derive(
        self,
        state: PaninianState,
        *,
        sutra_ids: Sequence[str] | None = None,
        prefixes: Sequence[str] | None = None,
        max_steps: int = 32,
    ) -> PaninianDerivation:
        initial = state
        seen_candidates: list[str] = []
        if sutra_ids is not None:
            final = self.derive_sequence(state, sutra_ids=sutra_ids)
            return PaninianDerivation(initial, final, tuple(sutra_ids))

        current = state
        for _ in range(max_steps):
            candidates = tuple(
                candidate
                for candidate in self.selector.select(current, prefixes=prefixes)
                if candidate.sutra_id not in current.applied_sutras
            )
            seen_candidates.extend(candidate.sutra_id for candidate in candidates)
            selected = self.precedence.resolve(candidates)
            if selected is None:
                break
            next_state = self.dispatcher.apply(current, selected)
            if next_state == current:
                break
            if next_state.history and not next_state.history[-1].changed:
                current = next_state
                break
            current = next_state
        return PaninianDerivation(initial, current, tuple(dict.fromkeys(seen_candidates)))

    def derive_sequence(self, state: PaninianState, *, sutra_ids: Sequence[str]) -> PaninianState:
        current = state
        for sutra_id in sutra_ids:
            candidates = self.selector.select(current, sutra_ids=(sutra_id,))
            selected = self.precedence.resolve(candidates)
            if selected is None:
                continue
            current = self.dispatcher.apply(current, selected)
        return current

    def apply_sutra(self, state: PaninianState, sutra_id: str) -> PaninianState:
        return self.derive_sequence(state, sutra_ids=(sutra_id,))


def derive_paninian(
    form: str = "",
    *,
    features: FeatureMap | None = None,
    sutra_ids: Sequence[str] | None = None,
    **state_kwargs: Any,
) -> PaninianDerivation:
    state = PaninianState(form=form, features=dict(features or {}), **state_kwargs)
    return PaninianDerivationEngine().derive(state, sutra_ids=sutra_ids)


__all__ = [
    "PaninianDerivation",
    "PaninianDerivationEngine",
    "PaninianState",
    "PaninianStep",
    "PrecedenceEngine",
    "RuleCandidate",
    "RuleSelectionEngine",
    "TransformationDispatcher",
    "derive_paninian",
]
