from .grammar import Pada

def determine_available_padas(markers: frozenset[str], lemma: str = "", prefixes: tuple[str, ...] = (), has_reflexive_result: bool = False) -> set[Pada]:
    """
    Partial Adhyāya 1.3 voice scaffold. This is not full 1.3 implementation.
    """
    # 1.3.13: bhāva-karmaṇoḥ (Atmanepada in passive/reflexive)
    # We assume this is handled by a higher-level check, but adding for completeness.

    # Specific Atmanepada rules (1.3.17 - 1.3.71)
    # 1.3.17: ner-viśaḥ
    if lemma == "viś" and "ni" in prefixes: return {Pada.ATMANEPADA}
    # 1.3.18: parivyawebhyaḥ kriyaḥ
    if lemma == "krī" and any(p in prefixes for p in {"pari", "vi", "ava"}): return {Pada.ATMANEPADA}
    # 1.3.19: vipa-paribhyāṃ jñaḥ
    if lemma == "jñā" and any(p in prefixes for p in {"vi", "parā"}): return {Pada.ATMANEPADA}
    # 1.3.21: krīḍo'nu-sam-paribhyaś-ca
    if lemma == "krīḍ" and any(p in prefixes for p in {"anu", "sam", "pari"}): return {Pada.ATMANEPADA}
    # 1.3.23: na-śasaḥ (exception for 1.3.22)
    # 1.3.24: ud-vido jñāne
    if lemma == "vid" and "ud" in prefixes: return {Pada.ATMANEPADA}
    # 1.3.25: upān-mantra-karaṇe
    if lemma == "vad" and "upa" in prefixes: return {Pada.ATMANEPADA}
    # 1.3.29: samo gamyṛ-cchibhyām
    if lemma in {"gam", "ṛ"} and "sam" in prefixes: return {Pada.ATMANEPADA}
    # 1.3.32: gandhana-avakṣepaṇa-sevana... kṣiyaḥ
    if lemma == "kṣi": return {Pada.ATMANEPADA}
    # 1.3.40: krōḍa-calana-śabdārthebhyaśca
    if lemma in {"kram", "cal", "śabd"} and "upa" in prefixes: return {Pada.ATMANEPADA}

    # 1.3.12: anudātta-ṅita ātmanepadam
    if "ṅ" in markers or "anudatta" in markers:
        return {Pada.ATMANEPADA}

    # 1.3.72: svarita-ñitaḥ kartrabhiprāye kriyāphale
    if "ñ" in markers or "svarita" in markers:
        return {Pada.ATMANEPADA} if has_reflexive_result else {Pada.PARASMAIPADA}

    # 1.3.78: śeṣāt kartari parasmaipadam
    return {Pada.PARASMAIPADA}
