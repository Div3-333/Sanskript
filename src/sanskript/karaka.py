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


def get_vibhakti(role: Role | None = None, companion_lemma: str | None = None, is_already_expressed: bool = False, semantic_context: str | None = None) -> Case:
    """
    Partial vibhakti assignment scaffold for selected 2.3 contexts.

    Order of precedence: Kāraka-vibhakti overrides Upapada-vibhakti
    (Upapada-vibhakteḥ kāraka-vibhaktir-balīyasī).
    """
    # 2.3.1: anabhihite
    if is_already_expressed:
        return Case.NOMINATIVE

    # Karaka Vibhaktis (Primary)
    karaka_case = None
    if role == Role.KARMAN: karaka_case = Case.ACCUSATIVE
    elif role == Role.KARTR or role == Role.KARANA: karaka_case = Case.INSTRUMENTAL
    elif role == Role.SAMPRADANA: karaka_case = Case.DATIVE
    elif role == Role.APADANA: karaka_case = Case.ABLATIVE
    elif role == Role.ADHIKARANA: karaka_case = Case.LOCATIVE

    # Upapada Vibhaktis (Secondary)
    upapada_case = None

    # 2.3.5: antarāntareṇa yuktē (Accusative)
    if companion_lemma in {"antarā", "antareṇa"}:
        upapada_case = Case.ACCUSATIVE

    # 2.3.16: namaḥ-svasti... (Dative)
    elif companion_lemma in {"namas", "svasti", "svāhā", "svadhā", "alam", "vaṣaṭ"}:
        upapada_case = Case.DATIVE

    # 2.3.19: saha-yukte (Instrumental)
    elif companion_lemma == "saha":
        upapada_case = Case.INSTRUMENTAL

    # 2.3.20: yenāṅga-vikāraḥ (Instrumental for defective limbs)
    if semantic_context == "defective_limb":
        upapada_case = Case.INSTRUMENTAL

    # 2.3.23: hētau (Instrumental for cause/reason)
    if semantic_context == "cause":
        upapada_case = Case.INSTRUMENTAL

    # Precedence Rule: Karaka > Upapada
    # Example: namaskurmo devān (namas + kṛ). Devān is Karman, so Accusative overrides Dative.
    return karaka_case if karaka_case else (upapada_case if upapada_case else Case.GENITIVE)


def explain_case(case: Case) -> KarakaExplanation:
    return KARAKA_EXPLANATIONS[case]
