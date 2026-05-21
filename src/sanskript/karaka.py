from __future__ import annotations

from dataclasses import dataclass

from .grammar import CASE_TO_ROLE, Case, Role


@dataclass(frozen=True)
class KarakaExplanation:
    case: Case
    role: Role | None
    gloss: str
    compiler_use: str


KARAKA_EXPLANATIONS = {
    Case.NOMINATIVE: KarakaExplanation(Case.NOMINATIVE, Role.KARTR, "svatantraḥ kartā (1.4.54)", "independent agent or actor"),
    Case.ACCUSATIVE: KarakaExplanation(Case.ACCUSATIVE, Role.KARMAN, "kartur-īpsitatamaṃ karma (1.4.49)", "object most desired by agent"),
    Case.INSTRUMENTAL: KarakaExplanation(Case.INSTRUMENTAL, Role.KARANA, "sādhakatamaṃ karaṇam (1.4.42)", "most effective means or instrument"),
    Case.DATIVE: KarakaExplanation(Case.DATIVE, Role.SAMPRADANA, "karmaṇā yam-abhipraiti sa sampradānam (1.4.32)", "recipient intended by the action"),
    Case.ABLATIVE: KarakaExplanation(Case.ABLATIVE, Role.APADANA, "dhruvam-apāye'pādānam (1.4.24)", "fixed point of departure or separation"),
    Case.GENITIVE: KarakaExplanation(Case.GENITIVE, None, "ṣaṣṭhī śeṣe (2.3.50)", "residual relations (possession, etc.)"),
    Case.LOCATIVE: KarakaExplanation(Case.LOCATIVE, Role.ADHIKARANA, "ādhāro'dhikaraṇam (1.4.45)", "substratum or location"),
    Case.VOCATIVE: KarakaExplanation(Case.VOCATIVE, None, "sambodhane ca (2.3.47)", "addressing or calling"),
}


CASE_PRIORITY = (
    Case.NOMINATIVE,
    Case.ACCUSATIVE,
    Case.INSTRUMENTAL,
    Case.DATIVE,
    Case.ABLATIVE,
    Case.GENITIVE,
    Case.LOCATIVE,
    Case.VOCATIVE,
)


UPAPADA_CASES: dict[str, frozenset[Case]] = {
    "antarā": frozenset({Case.ACCUSATIVE}),
    "antareṇa": frozenset({Case.ACCUSATIVE}),
    "namas": frozenset({Case.DATIVE}),
    "svasti": frozenset({Case.DATIVE}),
    "svāhā": frozenset({Case.DATIVE}),
    "svadhā": frozenset({Case.DATIVE}),
    "alam": frozenset({Case.DATIVE}),
    "vaṣaṭ": frozenset({Case.DATIVE}),
    "saha": frozenset({Case.INSTRUMENTAL}),
    "anu": frozenset({Case.ACCUSATIVE}),
    "apa": frozenset({Case.ABLATIVE}),
    "pari": frozenset({Case.ABLATIVE}),
    "prati": frozenset({Case.ABLATIVE}),
    "anya": frozenset({Case.ABLATIVE}),
    "atas": frozenset({Case.GENITIVE}),
    "enapā": frozenset({Case.ACCUSATIVE}),
    "pṛthak": frozenset({Case.INSTRUMENTAL}),
    "vinā": frozenset({Case.INSTRUMENTAL}),
    "nānā": frozenset({Case.INSTRUMENTAL}),
    "dūra": frozenset({Case.ACCUSATIVE, Case.GENITIVE}),
    "antika": frozenset({Case.ACCUSATIVE, Case.GENITIVE}),
}


SEMANTIC_CONTEXT_CASES: dict[str, frozenset[Case]] = {
    "defective_limb": frozenset({Case.INSTRUMENTAL}),
    "cause": frozenset({Case.INSTRUMENTAL}),
    "vedic_hu": frozenset({Case.INSTRUMENTAL}),
    "apavarga": frozenset({Case.INSTRUMENTAL}),
    "between_karakas": frozenset({Case.LOCATIVE, Case.ABLATIVE}),
    "excess_reference": frozenset({Case.LOCATIVE}),
    "motion_goal": frozenset({Case.ACCUSATIVE, Case.DATIVE}),
    "tumun_purpose": frozenset({Case.DATIVE}),
    "disrespect_inanimate_manyate": frozenset({Case.ACCUSATIVE}),
    "agent_or_instrument": frozenset({Case.INSTRUMENTAL}),
    "characteristic_mark": frozenset({Case.INSTRUMENTAL}),
    "name_object": frozenset({Case.ACCUSATIVE}),
    "debt_without_agent": frozenset({Case.ABLATIVE}),
    "quality_relation": frozenset({Case.GENITIVE}),
    "cause_genitive": frozenset({Case.GENITIVE}),
    "pronoun_instrumental": frozenset({Case.INSTRUMENTAL}),
    "stock_measure": frozenset({Case.INSTRUMENTAL}),
    "adhigama": frozenset({Case.GENITIVE}),
    "bhava_vacana": frozenset({Case.GENITIVE}),
    "himsa": frozenset({Case.GENITIVE}),
    "vyavahara": frozenset({Case.GENITIVE}),
    "tadartha": frozenset({Case.GENITIVE}),
    "vartamana_kta": frozenset({Case.GENITIVE}),
    "adhikarana_krit": frozenset({Case.GENITIVE}),
}


def role_for_case(case: Case) -> Role | None:
    return CASE_TO_ROLE.get(case)


def get_karaka_role(verb_lemma: str, semantic_role_context: str) -> Role | None:
    """
    Partial kāraka assignment scaffold for selected 1.4.23-1.4.55 contexts.
    """
    # 1.4.24: dhruvam-apāye'pādānam
    if semantic_role_context == "separation_point":
        return Role.APADANA

    # 1.4.25: bhītrārthānāṃ bhayahetuḥ (cause of fear is apādāna)
    if verb_lemma in {"bhī", "trā"} and semantic_role_context == "cause_of_fear":
        return Role.APADANA

    # 1.4.26: parājer-asodhaḥ (unbearable object of parā-ji)
    if verb_lemma == "parā-ji" and semantic_role_context == "unbearable":
        return Role.APADANA

    # 1.4.27: vāraṇārthānām īpsitaḥ
    if semantic_role_context == "warded_off_object":
        return Role.APADANA

    # 1.4.28: antardhau yenādarśanam icchati
    if semantic_role_context == "hidden_from":
        return Role.APADANA

    # 1.4.30: ākhyātopayoge (Teacher from whom one learns)
    if semantic_role_context == "teacher":
        return Role.APADANA

    # 1.4.32: karmaṇā yam-abhipraiti sa sampradānam
    if semantic_role_context == "intended_recipient":
        return Role.SAMPRADANA

    # 1.4.33: rucyarthānāṃ prīyamāṇaḥ (the one pleased is sampradāna)
    if verb_lemma == "ruc" and semantic_role_context == "pleased_one":
        return Role.SAMPRADANA

    # 1.4.42: sādhakatamaṃ karaṇam
    if semantic_role_context == "most_effective_means":
        return Role.KARANA

    # 1.4.45: ādhāro'dhikaraṇam
    if semantic_role_context == "substratum":
        return Role.ADHIKARANA

    # 1.4.49: kartur-īpsitatamaṃ karma
    if semantic_role_context in {"most_desired", "ipsitatama"}:
        return Role.KARMAN

    # 1.4.54: svatantraḥ kartā
    if semantic_role_context == "independent_agent":
        return Role.KARTR

    return None


def get_allowed_vibhaktis(
    role: Role | None = None,
    companion_lemma: str | None = None,
    is_already_expressed: bool = False,
    semantic_context: str | None = None,
) -> frozenset[Case]:
    """
    Partial vibhakti assignment scaffold for selected 2.3 contexts.

    Order of precedence: Kāraka-vibhakti overrides Upapada-vibhakti
    (Upapada-vibhakteḥ kāraka-vibhaktir-balīyasī).
    """
    # 2.3.1: anabhihite
    if is_already_expressed:
        return frozenset({Case.NOMINATIVE})

    # Karaka Vibhaktis (Primary)
    karaka_case = None
    if role == Role.KARMAN: karaka_case = Case.ACCUSATIVE
    elif role == Role.KARTR or role == Role.KARANA: karaka_case = Case.INSTRUMENTAL
    elif role == Role.SAMPRADANA: karaka_case = Case.DATIVE
    elif role == Role.APADANA: karaka_case = Case.ABLATIVE
    elif role == Role.ADHIKARANA: karaka_case = Case.LOCATIVE

    upapada_cases = UPAPADA_CASES.get(str(companion_lemma), frozenset()) if companion_lemma else frozenset()
    semantic_cases = SEMANTIC_CONTEXT_CASES.get(str(semantic_context), frozenset()) if semantic_context else frozenset()

    # Precedence Rule: Karaka > Upapada
    # Example: namaskurmo devān (namas + kṛ). Devān is Karman, so Accusative overrides Dative.
    if karaka_case:
        return frozenset({karaka_case})
    if upapada_cases or semantic_cases:
        return upapada_cases | semantic_cases
    return frozenset({Case.GENITIVE})


def get_vibhakti(role: Role | None = None, companion_lemma: str | None = None, is_already_expressed: bool = False, semantic_context: str | None = None) -> Case:
    allowed = get_allowed_vibhaktis(role, companion_lemma, is_already_expressed, semantic_context)
    return next(case for case in CASE_PRIORITY if case in allowed)


def explain_case(case: Case) -> KarakaExplanation:
    return KARAKA_EXPLANATIONS[case]
