import unittest
from sanskript.phonology import guna_replacement_for_ik, is_ik, vrddhi_replacement_for_ik

class TestSutra_1_1_3(unittest.TestCase):
    """
    1.1.3 iko guṇavṛddhī (ikaḥ guṇavṛddhī)
    Guṇa and vṛddhi replacements apply to the 'ik' pratyāhāra (i, u, ṛ, ḷ).
    """

    def test_ik_sounds(self):
        # Accepted ik sounds (short and long)
        self.assertTrue(is_ik("i"), "i should be an ik sound")
        self.assertTrue(is_ik("ī"), "ī should be an ik sound")
        self.assertTrue(is_ik("u"), "u should be an ik sound")
        self.assertTrue(is_ik("ū"), "ū should be an ik sound")
        self.assertTrue(is_ik("ṛ"), "ṛ should be an ik sound")
        self.assertTrue(is_ik("ṝ"), "ṝ should be an ik sound")
        self.assertTrue(is_ik("ḷ"), "ḷ should be an ik sound")

    def test_non_ik_sounds(self):
        # Rejected sounds (not ik)
        self.assertFalse(is_ik("a"), "a should NOT be an ik sound")
        self.assertFalse(is_ik("ā"), "ā should NOT be an ik sound")
        self.assertFalse(is_ik("e"), "e should NOT be an ik sound")
        self.assertFalse(is_ik("o"), "o should NOT be an ik sound")
        self.assertFalse(is_ik("ai"), "ai should NOT be an ik sound")
        self.assertFalse(is_ik("au"), "au should NOT be an ik sound")
        self.assertFalse(is_ik("k"), "k should NOT be an ik sound")

    def test_guna_replacement_is_restricted_to_ik(self):
        self.assertEqual(guna_replacement_for_ik("i"), "e")
        self.assertEqual(guna_replacement_for_ik("ī"), "e")
        self.assertEqual(guna_replacement_for_ik("u"), "o")
        self.assertEqual(guna_replacement_for_ik("ū"), "o")
        self.assertEqual(guna_replacement_for_ik("ṛ"), "ar")
        self.assertEqual(guna_replacement_for_ik("ṝ"), "ar")
        self.assertEqual(guna_replacement_for_ik("ḷ"), "al")

        with self.assertRaisesRegex(ValueError, "requires an ik sound"):
            guna_replacement_for_ik("a")

    def test_vrddhi_replacement_is_restricted_to_ik(self):
        self.assertEqual(vrddhi_replacement_for_ik("i"), "ai")
        self.assertEqual(vrddhi_replacement_for_ik("ī"), "ai")
        self.assertEqual(vrddhi_replacement_for_ik("u"), "au")
        self.assertEqual(vrddhi_replacement_for_ik("ū"), "au")
        self.assertEqual(vrddhi_replacement_for_ik("ṛ"), "ār")
        self.assertEqual(vrddhi_replacement_for_ik("ṝ"), "ār")
        self.assertEqual(vrddhi_replacement_for_ik("ḷ"), "āl")

        with self.assertRaisesRegex(ValueError, "requires an ik sound"):
            vrddhi_replacement_for_ik("a")

if __name__ == "__main__":
    unittest.main()
