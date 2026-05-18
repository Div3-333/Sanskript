import unittest

from sanskript.sandhi import join_words


class SandhiTests(unittest.TestCase):
    def test_savarna_dirgha_sandhi(self) -> None:
        result = join_words("deva", "atra")

        self.assertEqual(result.value, "devātra")
        self.assertEqual(result.rule, "savarṇa-dīrgha")

    def test_guna_sandhi(self) -> None:
        result = join_words("deva", "iti")

        self.assertEqual(result.value, "deveti")
        self.assertEqual(result.rule, "guṇa")

    def test_vrddhi_sandhi(self) -> None:
        result = join_words("deva", "eva")

        self.assertEqual(result.value, "devaiva")
        self.assertEqual(result.rule, "vṛddhi")

    def test_ayavayava_sandhi(self) -> None:
        result = join_words("hare", "atra")

        self.assertEqual(result.value, "harayatra")
        self.assertEqual(result.rule, "ayavāyāva")

    def test_visarga_vowel_sandhi(self) -> None:
        result = join_words("rāmaḥ", "atra")

        self.assertEqual(result.value, "rāmotra")
        self.assertEqual(result.rule, "visarga-vowel")


if __name__ == "__main__":
    unittest.main()
