import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DocumentationTests(unittest.TestCase):
    def test_visual_beginner_guide_is_present(self) -> None:
        guide = ROOT / "docs" / "guide" / "index.html"
        artwork = ROOT / "docs" / "guide" / "assets" / "grammar-tablet.png"
        html = guide.read_text(encoding="utf-8")

        self.assertIn("Write programs as grammatical Sanskrit", html)
        self.assertIn("assets/grammar-tablet.png", html)
        self.assertIn("The current canon marks 255 sutras implemented through real named handlers", html)
        self.assertGreater(artwork.stat().st_size, 10_000)


if __name__ == "__main__":
    unittest.main()
