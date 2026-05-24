import unittest
from pathlib import Path

from sanskript.register_docs import render_register_sync


ROOT = Path(__file__).resolve().parents[1]


class RegisterDocsTests(unittest.TestCase):
    def test_generated_register_doc_is_in_sync(self) -> None:
        generated = ROOT / "docs" / "grammar-register.generated.md"

        self.assertTrue(generated.exists())
        self.assertEqual(generated.read_text(encoding="utf-8"), render_register_sync())


if __name__ == "__main__":
    unittest.main()
