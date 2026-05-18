import unittest

from sanskript.transliteration import devanagari_to_iast, iast_to_devanagari, tokenize_iast


class TransliterationTests(unittest.TestCase):
    def test_iast_to_devanagari_for_current_source_forms(self) -> None:
        self.assertEqual(iast_to_devanagari("gaṇakaḥ"), "गणकः")
        self.assertEqual(iast_to_devanagari("phalaṃ"), "फलं")
        self.assertEqual(iast_to_devanagari("nyūnayati"), "न्यूनयति")

    def test_devanagari_to_iast_for_current_source_forms(self) -> None:
        self.assertEqual(devanagari_to_iast("गणकः"), "gaṇakaḥ")
        self.assertEqual(devanagari_to_iast("फलं"), "phalaṃ")
        self.assertEqual(devanagari_to_iast("न्यूनयति"), "nyūnayati")

    def test_iast_tokenizer_prefers_longest_tokens(self) -> None:
        self.assertEqual(tokenize_iast("ai au kh ṭh"), ["ai", " ", "au", " ", "kh", " ", "ṭh"])


if __name__ == "__main__":
    unittest.main()
