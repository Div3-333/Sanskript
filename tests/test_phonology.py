import unittest

from sanskript.phonology import (
    SOUNDS,
    ArticulationPlace,
    VowelLength,
    is_consonant,
    is_guna,
    is_simple_vowel_savarna,
    is_vowel,
    is_vrddhi,
    pratyahara,
    sounds_by_place,
)


class PhonologyTests(unittest.TestCase):
    def test_ac_pratyahara_contains_simple_vowels_and_diphthongs(self) -> None:
        self.assertEqual(pratyahara("ac"), ("a", "i", "u", "ṛ", "ḷ", "e", "o", "ai", "au"))

    def test_hal_pratyahara_contains_consonants_not_vowels(self) -> None:
        hal = pratyahara("hal")

        self.assertIn("h", hal)
        self.assertIn("y", hal)
        self.assertIn("k", hal)
        self.assertIn("s", hal)
        self.assertNotIn("a", hal)

    def test_ik_and_yan_match_sanskrit_sound_classes(self) -> None:
        self.assertEqual(pratyahara("ik"), ("i", "u", "ṛ", "ḷ"))
        self.assertEqual(pratyahara("yaṇ"), ("y", "v", "r", "l"))

    def test_vowel_and_consonant_classification(self) -> None:
        self.assertTrue(is_vowel("ai"))
        self.assertTrue(is_consonant("dh"))
        self.assertEqual(SOUNDS["ai"].length, VowelLength.DIPHTHONG)

    def test_articulation_places_are_queryable(self) -> None:
        self.assertEqual(
            sounds_by_place(ArticulationPlace.LABIAL),
            ("u", "ū", "o", "au", "p", "ph", "b", "bh", "m", "v"),
        )

    def test_guna_and_vrddhi_sound_categories(self) -> None:
        self.assertTrue(is_guna("a"))
        self.assertTrue(is_guna("e"))
        self.assertTrue(is_vrddhi("ā"))
        self.assertTrue(is_vrddhi("ai"))
        self.assertFalse(is_guna("ai"))

    def test_conservative_vowel_savarna_helper(self) -> None:
        self.assertTrue(is_simple_vowel_savarna("a", "ā"))
        self.assertTrue(is_simple_vowel_savarna("i", "ī"))
        self.assertFalse(is_simple_vowel_savarna("i", "u"))


if __name__ == "__main__":
    unittest.main()
