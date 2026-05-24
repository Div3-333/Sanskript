import unittest

from sanskript.vocabulary_catalog import graduate_noun_stems, graduate_verb_dhatus, vocabulary_stats


class VocabularyCatalogTests(unittest.TestCase):
    def test_has_at_least_100_noun_and_verb_stems(self) -> None:
        stats = vocabulary_stats()
        self.assertGreaterEqual(stats["noun_stems"], 100)
        self.assertGreaterEqual(stats["verb_roots"], 100)
        self.assertGreaterEqual(stats["stem_patterns"], 15)

    def test_noun_stems_use_supported_paradigms(self) -> None:
        from sanskript.subanta import StemPattern

        for stem in graduate_noun_stems():
            self.assertIn(stem.pattern, set(StemPattern))
            if stem.pattern == StemPattern.UU_FEMININE:
                self.assertTrue(stem.lemma.endswith("ū"), stem.lemma)

    def test_imports_existing_subanta_and_controlled_nouns(self) -> None:
        lemmas = {stem.lemma for stem in graduate_noun_stems()}
        self.assertIn("gaṇaka", lemmas)
        self.assertIn("phala", lemmas)
        self.assertIn("nara", lemmas)

    def test_graduate_verbs_exclude_core_register_duplicates(self) -> None:
        lemmas = {dhatu.lemma for dhatu in graduate_verb_dhatus()}
        self.assertNotIn("bhū", lemmas)
        self.assertNotIn("kṛ", lemmas)
        self.assertIn("gam", lemmas)
        self.assertIn("yaj", lemmas)


if __name__ == "__main__":
    unittest.main()
