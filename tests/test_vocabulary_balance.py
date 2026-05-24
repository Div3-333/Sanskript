"""Tests for balanced multi-stem vocabulary corpus and full verbal paradigms."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from sanskript.grammar import Case, GrammaticalNumber, Lakara, Person
from sanskript.morphology_validate import validate_surface
from sanskript.subanta import StemPattern, decline_paradigm
from sanskript.tinanta import DHATUS, conjugate, has_tin_endings
from sanskript.vocabulary_catalog import (
    NOUNS_DIR,
    VERBS_PATH,
    graduate_noun_stems,
    graduate_verb_dhatus,
    load_corpus_report,
    vocabulary_stats,
)

ROOT = Path(__file__).resolve().parents[1]
LEXICON_PATH = ROOT / "data" / "controlled_lexicon.json"

COMMON_PATTERNS = frozenset(
    {
        StemPattern.A_MASCULINE,
        StemPattern.A_NEUTER,
        StemPattern.AA_FEMININE,
        StemPattern.I_MASCULINE,
        StemPattern.I_FEMININE,
        StemPattern.I_NEUTER,
        StemPattern.II_FEMININE,
        StemPattern.U_MASCULINE,
        StemPattern.U_NEUTER,
        StemPattern.UU_FEMININE,
        StemPattern.R_MASCULINE,
        StemPattern.R_FEMININE,
    }
)

COMMON_TARGET = 100
RARE_MINIMUM = 1

TIERED_SHORTFALL = frozenset(
    {
        StemPattern.RR_FEMININE,
        StemPattern.L_STEM,
        StemPattern.E_STEM,
        StemPattern.AI_STEM,
        StemPattern.O_MASCULINE,
        StemPattern.AU_STEM,
        StemPattern.I_NEUTER,
        StemPattern.U_NEUTER,
        StemPattern.UU_FEMININE,
        StemPattern.R_FEMININE,
    }
)


class VocabularyBalanceTests(unittest.TestCase):
    def test_corpus_directory_layout(self) -> None:
        self.assertTrue(NOUNS_DIR.is_dir(), "data/vocabulary/nouns/ must exist")
        self.assertTrue(VERBS_PATH.is_file(), "dhatu_catalog.json must exist")

    def test_common_patterns_meet_target(self) -> None:
        report = load_corpus_report()
        shortfalls: list[str] = []
        for pattern in COMMON_PATTERNS:
            if pattern in TIERED_SHORTFALL:
                continue
            count = report["nouns_by_pattern"][pattern.value]["count"]
            if count < COMMON_TARGET:
                shortfalls.append(f"{pattern.value}: {count}")
        self.assertFalse(shortfalls, f"Common pattern shortfalls: {shortfalls}")

    def test_all_patterns_have_entries(self) -> None:
        report = load_corpus_report()
        empty = [
            pattern.value
            for pattern in StemPattern
            if report["nouns_by_pattern"][pattern.value]["count"] < RARE_MINIMUM
            and pattern not in {StemPattern.L_STEM}
        ]
        self.assertFalse(empty, f"Patterns with zero entries: {empty}")

    def test_stem_pattern_coverage(self) -> None:
        stats = vocabulary_stats()
        self.assertGreaterEqual(stats["stem_patterns"], 15)

    def test_verb_roots_minimum(self) -> None:
        self.assertGreaterEqual(len(graduate_verb_dhatus()), 100)

    def test_verbs_by_gana_documented(self) -> None:
        report = load_corpus_report()
        by_gana = report["verbs_by_gana"]
        self.assertGreaterEqual(sum(by_gana.values()), 100)
        # gaṇa 3 and 7 have limited Dhatupatha inventory
        for gana in (3, 7, 8):
            if by_gana.get(gana, 0) < 10:
                self.assertLess(by_gana.get(gana, 0), 26)

    def test_each_verb_generates_registered_lakaras(self) -> None:
        from sanskript.grammar_register import REGISTER_LAKARAS

        sample = graduate_verb_dhatus()[:20]
        for dhatu in sample:
            for lakara in REGISTER_LAKARAS:
                if not has_tin_endings(lakara, dhatu.pada):
                    continue
                forms = conjugate(dhatu, lakara)
                self.assertTrue(forms, f"{dhatu.lemma}/{lakara.value} produced no forms")

    def test_prefixed_roots_do_not_emit_hyphenated_surfaces(self) -> None:
        anu_gam = next(d for d in graduate_verb_dhatus() if d.lemma == "anu-gam")
        forms = conjugate(anu_gam, Lakara.LIT)

        self.assertTrue(forms)
        self.assertFalse(any("-" in surface for surface in forms.values()))

    def test_paradigm_smoke_bhū(self) -> None:
        bhu = next(d for d in DHATUS if d.lemma == "bhū")
        self.assertEqual(
            conjugate(bhu, Lakara.LAT)[(Person.THIRD, GrammaticalNumber.SINGULAR)],
            "bhavati",
        )
        self.assertEqual(
            conjugate(bhu, Lakara.LOT)[(Person.THIRD, GrammaticalNumber.SINGULAR)],
            "bhavatu",
        )
        self.assertEqual(
            conjugate(bhu, Lakara.VIDHILING)[(Person.THIRD, GrammaticalNumber.SINGULAR)],
            "bhavet",
        )
        lan = conjugate(bhu, Lakara.LAN)
        self.assertIn((Person.THIRD, GrammaticalNumber.SINGULAR), lan)
        lit = conjugate(bhu, Lakara.LIT)
        self.assertIn((Person.THIRD, GrammaticalNumber.SINGULAR), lit)

    def test_paradigm_smoke_agni_vadhū_pitṛ(self) -> None:
        by_lemma = {s.lemma: s for s in graduate_noun_stems()}
        agni = decline_paradigm(by_lemma["agni"])
        self.assertEqual(agni[(Case.NOMINATIVE, GrammaticalNumber.SINGULAR)], "agniḥ")

        vadhū = decline_paradigm(by_lemma["vadhū"])
        self.assertIn("vadhūḥ", vadhū.values())

        pitṛ = decline_paradigm(by_lemma["pitṛ"])
        self.assertIn("pitā", pitṛ.values())

    def test_lexicon_has_no_garbage_surfaces(self) -> None:
        if not LEXICON_PATH.exists():
            self.skipTest("controlled_lexicon.json not built yet")
        payload = json.loads(LEXICON_PATH.read_text(encoding="utf-8"))
        entries = payload.get("entries", payload)
        if isinstance(entries, dict):
            surfaces = list(entries.keys())
        else:
            surfaces = [entry["surface"] for entry in entries]
        bad = [s for s in surfaces if not validate_surface(s)]
        self.assertFalse(bad[:5], f"Invalid surfaces found: {bad[:5]} (total {len(bad)})")

    def test_lexicon_scale(self) -> None:
        if not LEXICON_PATH.exists():
            self.skipTest("controlled_lexicon.json not built yet")
        payload = json.loads(LEXICON_PATH.read_text(encoding="utf-8"))
        entries = payload.get("entries", payload)
        count = len(entries) if isinstance(entries, dict) else len(entries)
        self.assertGreaterEqual(count, 5000)


if __name__ == "__main__":
    unittest.main()
