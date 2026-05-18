import unittest
from sanskript.phonology import GUNA_SOUNDS, SOUNDS, is_guna

class TestSutra_1_1_2(unittest.TestCase):
    """
    1.1.2 adeṅ guṇaḥ (at eṅ guṇaḥ)
    The term guṇa denotes the sounds a, e, and o.
    """

    def test_guna_sounds(self):
        self.assertEqual(GUNA_SOUNDS, {"a", "e", "o"})
        # Accepted guṇa sounds
        self.assertTrue(is_guna("a"), "a should be a guṇa sound")
        self.assertTrue(is_guna("e"), "e should be a guṇa sound")
        self.assertTrue(is_guna("o"), "o should be a guṇa sound")

    def test_non_guna_sounds(self):
        for sound in set(SOUNDS) - GUNA_SOUNDS:
            self.assertFalse(is_guna(sound), f"{sound} should NOT be a guṇa sound")

if __name__ == "__main__":
    unittest.main()
