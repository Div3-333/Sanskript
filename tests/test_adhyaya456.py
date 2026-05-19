import json
import unittest
from pathlib import Path

from sanskript.accent import Accent, assign_svarita, profile_accent
from sanskript.adhyaya456 import (
    ADHYAYA456_RULES,
    ImplementationMode,
    PADA_COUNTS,
    expected_adhyaya456_ids,
    implemented_sutra_ids,
    missing_rule_ids,
    partial_implementation_note_for,
    partial_sutra_ids,
    rules_for_pada,
)
from sanskript.anga import apply_anga_operation, operation_named, operations_for_range
from sanskript.derivation import TaddhitaSuffix, derive
from sanskript.sandhi import join_words


ROOT = Path(__file__).resolve().parents[1]


class AdhyayaFourFiveSixRegistryTests(unittest.TestCase):
    def test_registry_covers_adhyaya_four_five_and_six(self) -> None:
        self.assertEqual(len(expected_adhyaya456_ids()), 1925)
        self.assertEqual(missing_rule_ids(), ())
        self.assertEqual(implemented_sutra_ids(), frozenset())
        self.assertEqual(partial_sutra_ids(), frozenset(expected_adhyaya456_ids()))
        self.assertEqual(implemented_sutra_ids() | partial_sutra_ids(), frozenset(expected_adhyaya456_ids()))
        for pada, count in PADA_COUNTS.items():
            self.assertEqual(len(rules_for_pada(pada)), count)

    def test_rules_remain_partial_until_real_handlers_exist(self) -> None:
        for sutra_id, rule in ADHYAYA456_RULES.items():
            with self.subTest(sutra_id=sutra_id):
                self.assertFalse(rule.implemented)
                self.assertNotEqual(rule.mode, ImplementationMode.DISCRETE)
                self.assertTrue(rule.title)
                self.assertTrue(rule.compiler_effect)
                self.assertTrue(rule.examples)

    def test_local_canon_marks_adhyaya_four_five_and_six_as_partial(self) -> None:
        canon = json.loads((ROOT / "data" / "grammar_canon.json").read_text(encoding="utf-8"))
        statuses = {
            item["title"]: item["status"]
            for item in canon["obligations"]
            if item["kind"] == "sutra" and item["title"] in expected_adhyaya456_ids()
        }

        self.assertEqual(len(statuses), 1925)
        self.assertEqual({sid for sid, status in statuses.items() if status == "implemented"}, set(implemented_sutra_ids()))
        self.assertEqual({sid for sid, status in statuses.items() if status == "partial"}, set(partial_sutra_ids()))


class AdhyayaFourFiveSixBehaviorTests(unittest.TestCase):
    def test_taddhita_anchors_cover_descent_possession_and_degree(self) -> None:
        self.assertEqual(derive("upagu", TaddhitaSuffix.APATYA).surface, "aupagava")
        self.assertEqual(derive("bala", TaddhitaSuffix.MATUP).surface, "balavān")
        self.assertEqual(derive("go", TaddhitaSuffix.MATUP).surface, "gomān")
        self.assertEqual(derive("laghu", TaddhitaSuffix.ATISHAYANA).surface, "laghiṣṭha")

    def test_vowel_sandhi_anchors_cover_adhyaya_six_one(self) -> None:
        self.assertEqual(join_words("deva", "atra").value, "devātra")
        self.assertEqual(join_words("deva", "atra").rule, "savarṇa-dīrgha")
        self.assertEqual(join_words("deva", "iti").value, "deveti")
        self.assertEqual(join_words("deva", "iti").rule, "guṇa")
        self.assertEqual(join_words("deva", "eva").value, "devaiva")
        self.assertEqual(join_words("deva", "eva").rule, "vṛddhi")
        self.assertEqual(join_words("hare", "atra").value, "harayatra")
        self.assertEqual(join_words("hare", "atra").rule, "ayavāyāva")

    def test_accent_and_anga_anchors_cover_adhyaya_six_two_to_four(self) -> None:
        profile = profile_accent(("rāja", "puruṣa"), udatta_index=1, sutra_range="6.2")
        svarita_profile = assign_svarita(profile, "rāja")

        self.assertEqual(profile.primary.token, "puruṣa")
        self.assertEqual(svarita_profile.assignments[0].accent, Accent.SVARITA)
        self.assertTrue(operations_for_range("6.3"))
        self.assertTrue(operations_for_range("6.4"))
        self.assertEqual(apply_anga_operation("deva", operation_named("final-a-lengthening")), "devā")
        self.assertEqual(apply_anga_operation("deva", operation_named("final-lopa")), "dev")


if __name__ == "__main__":
    unittest.main()
