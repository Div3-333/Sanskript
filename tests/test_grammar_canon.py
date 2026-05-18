import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANON_PATH = ROOT / "data" / "grammar_canon.json"


class GrammarCanonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.canon = json.loads(CANON_PATH.read_text(encoding="utf-8"))
        cls.sources = {source["id"]: source for source in cls.canon["sources"]}

    def test_all_three_pdf_sources_are_indexed(self) -> None:
        self.assertEqual(
            set(self.sources),
            {"ashtadhyayi", "vyakarana_pravesha", "sanskrit_for_beginners"},
        )

    def test_ashtadhyayi_sutra_index_is_complete_enough_to_be_canonical(self) -> None:
        sutra_index = self.sources["ashtadhyayi"]["sutra_index"]

        self.assertEqual(sutra_index["first"], "1.1.1")
        self.assertEqual(sutra_index["last"], "8.4.68")
        self.assertGreaterEqual(sutra_index["count"], 3900)
        self.assertIn("1.4", sutra_index["by_pada"])
        self.assertIn("6.1", sutra_index["by_pada"])

    def test_learn_sanskrit_topics_include_major_grammar_domains(self) -> None:
        topics = {
            entry["title"]
            for source in self.sources.values()
            for entry in source["outline"]
        }

        for topic in {
            "The Shiva Sutras",
            "kāraka",
            "vibhakti",
            "kṛt",
            "taddhita",
            "samāsa",
            "karmaṇi and bhāve prayoga",
            "The eight cases",
            "Relative phrases",
            "Participles",
        }:
            self.assertIn(topic, topics)

    def test_canon_keeps_a_copyright_boundary(self) -> None:
        policy = self.canon["policy"]

        self.assertIn("does not copy full PDF text", policy["copyright_boundary"])

    def test_every_indexed_item_has_an_obligation(self) -> None:
        obligations = self.canon["obligations"]
        topic_count = sum(len(source["outline"]) for source in self.sources.values())
        sutra_count = len(self.sources["ashtadhyayi"]["sutra_index"]["ids"])

        self.assertEqual(len(obligations), topic_count + sutra_count)
        self.assertEqual(self.canon["coverage_summary"]["total"], len(obligations))

    def test_sound_topics_are_marked_partial_after_phonology_work(self) -> None:
        partial_titles = {
            item["title"]
            for item in self.canon["obligations"]
            if item["status"] == "partial"
        }

        self.assertIn("The Shiva Sutras", partial_titles)
        self.assertIn("Vowels", partial_titles)
        self.assertIn("Consonants", partial_titles)
        self.assertIn("Romanized Sanskrit", partial_titles)

    def test_first_sound_sutras_are_marked_partial_not_complete(self) -> None:
        partial_sutras = {
            item["title"]
            for item in self.canon["obligations"]
            if item["kind"] == "sutra" and item["status"] == "partial"
        }

        self.assertEqual(partial_sutras, {"1.1.1", "1.1.2", "1.1.9"})


if __name__ == "__main__":
    unittest.main()
