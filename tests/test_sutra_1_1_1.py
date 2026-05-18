import unittest
from sanskript.phonology import SOUNDS, VRDDHI_SOUNDS, is_vrddhi

class TestSutra_1_1_1(unittest.TestCase):
    """
    1.1.1 vṛddhirādaic (vṛddhiḥ ādaic)
    The term vṛddhi denotes the sounds ā, ai, and au.
    """

    def test_vrddhi_sounds(self):
        self.assertEqual(VRDDHI_SOUNDS, {"ā", "ai", "au"})
        # Accepted vṛddhi sounds
        self.assertTrue(is_vrddhi("ā"), "ā should be a vṛddhi sound")
        self.assertTrue(is_vrddhi("ai"), "ai should be a vṛddhi sound")
        self.assertTrue(is_vrddhi("au"), "au should be a vṛddhi sound")

    def test_non_vrddhi_sounds(self):
        for sound in set(SOUNDS) - VRDDHI_SOUNDS:
            self.assertFalse(is_vrddhi(sound), f"{sound} should NOT be a vṛddhi sound")

if __name__ == "__main__":
    unittest.main()
