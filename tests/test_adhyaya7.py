import json
import unittest
from pathlib import Path

from sanskript.adhyaya7 import (
    ADHYAYA7_RULES,
    ImplementationMode,
    PADA_COUNTS,
    expected_adhyaya7_ids,
    implemented_sutra_ids,
    missing_rule_ids,
    partial_sutra_ids,
    rules_for_pada,
)

ROOT = Path(__file__).resolve().parents[1]


class AdhyayaSevenRegistryTests(unittest.TestCase):
    def test_registry_covers_adhyaya_seven(self) -> None:
        self.assertEqual(len(expected_adhyaya7_ids()), 438)
        self.assertEqual(missing_rule_ids(), ())
        self.assertEqual(partial_sutra_ids(), frozenset(expected_adhyaya7_ids()) - implemented_sutra_ids())
        self.assertEqual(implemented_sutra_ids() | partial_sutra_ids(), frozenset(expected_adhyaya7_ids()))
        for pada, count in PADA_COUNTS.items():
            self.assertEqual(len(rules_for_pada(pada)), count)

    def test_only_rules_with_real_handlers_are_implemented(self) -> None:
        for sutra_id, rule in ADHYAYA7_RULES.items():
            with self.subTest(sutra_id=sutra_id):
                self.assertTrue(rule.title)
                self.assertTrue(rule.compiler_effect)
                self.assertTrue(rule.examples)
                if rule.implemented:
                    self.assertEqual(rule.mode, ImplementationMode.DISCRETE)
                    self.assertTrue(rule.atomic)
                else:
                    self.assertNotEqual(rule.mode, ImplementationMode.DISCRETE)

    def test_local_canon_marks_adhyaya_seven_as_implemented(self) -> None:
        canon = json.loads((ROOT / "data" / "grammar_canon.json").read_text(encoding="utf-8"))
        statuses = {
            item["title"]: item["status"]
            for item in canon["obligations"]
            if item["kind"] == "sutra" and item["title"] in expected_adhyaya7_ids()
        }

        self.assertEqual(len(statuses), 438)
        self.assertEqual({sid for sid, status in statuses.items() if status == "implemented"}, set(implemented_sutra_ids()))
        self.assertEqual({sid for sid, status in statuses.items() if status == "partial"}, set(partial_sutra_ids()))


if __name__ == "__main__":
    unittest.main()
