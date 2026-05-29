import unittest

from sanskript.sandhi import join_sentence, join_words, split_joined_token, split_joined_token_chain


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

    def test_visarga_sibilant_sandhi(self) -> None:
        result = join_words("rāmaḥ", "śivaḥ")

        self.assertEqual(result.value, "rāmaśśivaḥ")
        self.assertEqual(result.rule, "visarga-sibilant")

    def test_join_sentence_tracks_each_join_step(self) -> None:
        result = join_sentence(["deva", "iti", "atra"])

        self.assertEqual([item.value for item in result], ["deveti", "deveti atra"])
        self.assertEqual([item.rule for item in result], ["guṇa", "identity"])

    def test_split_joined_token_reconstructs_vowel_join(self) -> None:
        self.assertEqual(split_joined_token("deveti"), ("deva", "iti"))

    def test_split_joined_token_reconstructs_visarga_vowel_join(self) -> None:
        self.assertEqual(split_joined_token("gaṇakotra"), ("gaṇakaḥ", "atra"))

    def test_split_joined_token_reconstructs_visarga_sibilant_join(self) -> None:
        self.assertEqual(split_joined_token("rāmaśśivaḥ"), ("rāmaḥ", "śivaḥ"))

    def test_split_joined_token_returns_none_for_non_sandhi_surface(self) -> None:
        self.assertIsNone(split_joined_token("gaṇakaḥ"))

    def test_split_joined_token_chain_recovers_multiple_boundaries(self) -> None:
        def validator(token: str) -> bool:
            return token in {"gaṇakaḥ", "atra", "api"}

        joined = join_words("gaṇakaḥ", "atra").value
        joined = join_words(joined, "api").value
        self.assertEqual(joined, "gaṇakotrāpi")
        self.assertEqual(
            split_joined_token_chain(joined, part_validator=validator),
            ["gaṇakaḥ", "atra", "api"],
        )

    def test_split_joined_token_chain_roundtrip_is_lossless(self) -> None:
        original_parts = ["gaṇakaḥ", "atra", "api"]
        joined = join_words(original_parts[0], original_parts[1]).value
        joined = join_words(joined, original_parts[2]).value
        recovered = split_joined_token_chain(
            joined,
            part_validator=lambda token: token in {"gaṇakaḥ", "atra", "api"},
        )
        rebuilt = recovered[0]
        for part in recovered[1:]:
            rebuilt = join_words(rebuilt, part).value
        self.assertEqual(rebuilt, joined)

    def test_split_joined_token_prefers_lexically_valid_parts(self) -> None:
        def validator(token: str) -> bool:
            return token in {"gaṇakaḥ", "atra", "api"}

        self.assertEqual(
            split_joined_token_chain("gaṇakotrāpi", part_validator=validator),
            ["gaṇakaḥ", "atra", "api"],
        )


if __name__ == "__main__":
    unittest.main()
