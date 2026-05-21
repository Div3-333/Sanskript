import json
import unittest
from collections import Counter
from pathlib import Path

from sanskript.adhyaya1 import expected_adhyaya1_ids
from sanskript.adhyaya1 import implemented_sutra_ids as adhyaya1_implemented_sutra_ids
from sanskript.adhyaya1 import partial_sutra_ids as adhyaya1_partial_sutra_ids
from sanskript.adhyaya23 import expected_adhyaya23_ids
from sanskript.adhyaya23 import implemented_sutra_ids as adhyaya23_implemented_sutra_ids
from sanskript.adhyaya23 import partial_sutra_ids as adhyaya23_partial_sutra_ids
from sanskript.adhyaya456 import expected_adhyaya456_ids
from sanskript.adhyaya456 import implemented_sutra_ids as adhyaya456_implemented_sutra_ids
from sanskript.adhyaya456 import partial_sutra_ids as adhyaya456_partial_sutra_ids
from sanskript.adhyaya7 import expected_adhyaya7_ids
from sanskript.adhyaya7 import implemented_sutra_ids as adhyaya7_implemented_sutra_ids
from sanskript.adhyaya7 import partial_sutra_ids as adhyaya7_partial_sutra_ids
from sanskript.adhyaya8 import expected_adhyaya8_ids
from sanskript.adhyaya8 import implemented_sutra_ids as adhyaya8_implemented_sutra_ids
from sanskript.adhyaya8 import partial_sutra_ids as adhyaya8_partial_sutra_ids


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

    def test_coverage_summary_matches_actual_obligations(self) -> None:
        obligations = self.canon["obligations"]

        self.assertEqual(
            self.canon["coverage_summary"]["by_status"],
            dict(sorted(Counter(item["status"] for item in obligations).items())),
        )

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

    def test_only_discrete_sutras_are_marked_implemented(self) -> None:
        obligations = {
            item["title"]: item["status"]
            for item in self.canon["obligations"]
            if item["kind"] == "sutra"
        }
        adhyaya_one_implemented = set(adhyaya1_implemented_sutra_ids())
        adhyaya_one_partial = set(adhyaya1_partial_sutra_ids())
        adhyaya_two_three_implemented = set(adhyaya23_implemented_sutra_ids())
        adhyaya_four_five_six_implemented = set(adhyaya456_implemented_sutra_ids())
        adhyaya_two_three_partial = set(adhyaya23_partial_sutra_ids())
        adhyaya_four_five_six_partial = set(adhyaya456_partial_sutra_ids())
        adhyaya_seven_implemented = set(adhyaya7_implemented_sutra_ids())
        adhyaya_seven_partial = set(adhyaya7_partial_sutra_ids())
        adhyaya_eight_implemented = set(adhyaya8_implemented_sutra_ids())
        adhyaya_eight_partial = set(adhyaya8_partial_sutra_ids())
        implemented = {title for title, status in obligations.items() if status == "implemented"}
        partial = {title for title, status in obligations.items() if status == "partial"}

        self.assertEqual(implemented & set(expected_adhyaya1_ids()), adhyaya_one_implemented)
        self.assertEqual(partial & set(expected_adhyaya1_ids()), adhyaya_one_partial)
        self.assertEqual(implemented & set(expected_adhyaya23_ids()), adhyaya_two_three_implemented)
        self.assertEqual(implemented & set(expected_adhyaya456_ids()), adhyaya_four_five_six_implemented)
        self.assertEqual(implemented & set(expected_adhyaya7_ids()), adhyaya_seven_implemented)
        self.assertEqual(implemented & set(expected_adhyaya8_ids()), adhyaya_eight_implemented)
        self.assertEqual(partial & set(expected_adhyaya23_ids()), adhyaya_two_three_partial)
        self.assertEqual(partial & set(expected_adhyaya456_ids()), adhyaya_four_five_six_partial)
        self.assertEqual(partial & set(expected_adhyaya7_ids()), adhyaya_seven_partial)
        self.assertEqual(partial & set(expected_adhyaya8_ids()), adhyaya_eight_partial)
        expected_implemented_count = (
            len(adhyaya_one_implemented)
            + len(adhyaya_two_three_implemented)
            + len(adhyaya_four_five_six_implemented)
            + len(adhyaya_seven_implemented)
            + len(adhyaya_eight_implemented)
        )
        self.assertEqual(len(implemented), expected_implemented_count)

    def test_sound_and_sandhi_batch_tracks_hundreds_of_sutras(self) -> None:
        batch_partial = [
            item
            for item in self.canon["obligations"]
            if item["kind"] == "sutra" and item["status"] == "batch_partial"
        ]
        padas = {item["title"].rsplit(".", 1)[0] for item in batch_partial}

        self.assertEqual(len(batch_partial), 0)
        self.assertFalse(
            {
                "4.1", "4.2", "4.3", "4.4", "5.1", "5.2", "5.3", "5.4",
                "6.1", "6.2", "6.3", "6.4", "7.1", "7.2", "7.3", "7.4",
                "8.1", "8.2", "8.3", "8.4",
            }
            & padas
        )

    def test_no_sutra_identifier_is_left_pending_after_batch_scaffolds(self) -> None:
        pending_sutras = [
            item
            for item in self.canon["obligations"]
            if item["kind"] == "sutra" and item["status"] == "pending_design"
        ]

        self.assertEqual(pending_sutras, [])

    def test_no_canon_item_is_left_without_partial_treatment(self) -> None:
        pending = [item for item in self.canon["obligations"] if item["status"] == "pending_design"]

        self.assertEqual(pending, [])


if __name__ == "__main__":
    unittest.main()
