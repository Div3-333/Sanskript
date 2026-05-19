import unittest

from sanskript.sutra_logic import (
    evaluate_sutra,
    has_discrete_sutra_logic,
    implemented_logic_ids,
    negative_context_for,
    positive_context_for,
    sutra_record,
    sutra_records,
)


EXPECTED_REAL_LOGIC_IDS = frozenset(
    {
        "1.1.1", "1.1.2", "1.1.3", "1.1.4", "1.1.5", "1.1.6", "1.1.7", "1.1.8", "1.1.9",
        "1.1.10", "1.1.11", "1.1.12", "1.1.15", "1.1.19", "1.1.20", "1.1.21", "1.1.22",
        "1.1.23", "1.1.24", "1.1.25", "1.1.26", "1.1.27", "1.1.37", "1.1.40", "1.1.41",
        "1.1.42", "1.1.43", "1.1.44", "1.1.46", "1.1.47", "1.1.48", "1.1.49", "1.1.50",
        "1.1.51", "1.1.52", "1.1.53", "1.1.54", "1.1.55", "1.1.64", "1.1.65", "1.1.69",
        "1.1.70", "1.1.71", "1.1.73", "1.1.74", "1.1.75",
        "1.3.2", "1.3.3", "1.3.4", "1.3.5", "1.3.6", "1.3.7", "1.3.8", "1.3.9",
        "1.3.12", "1.3.13", "1.3.17", "1.3.18", "1.3.19", "1.3.21", "1.3.24", "1.3.25",
        "1.3.29", "1.3.32", "1.3.40", "1.3.72", "1.3.78",
        "1.4.3", "1.4.7", "1.4.10", "1.4.11", "1.4.12", "1.4.13", "1.4.14", "1.4.17",
        "1.4.18", "1.4.24", "1.4.25", "1.4.26", "1.4.27", "1.4.28", "1.4.29", "1.4.32",
        "1.4.33", "1.4.42", "1.4.45", "1.4.49", "1.4.54", "1.4.58", "1.4.59", "1.4.60",
        "1.4.109", "1.4.110",
    }
)


class SutraLogicTests(unittest.TestCase):
    def test_canonical_index_contains_full_sutra_patha(self) -> None:
        records = sutra_records()

        self.assertEqual(len(records), 3983)
        self.assertEqual(sutra_record("1.1.1").sutra_text_iast, "vṛddhirādaic")
        self.assertEqual(sutra_record("8.4.68").sutra_text_iast, "a a iti")

    def test_truth_gate_is_not_the_old_generated_adhyaya_one_to_six_metric(self) -> None:
        self.assertEqual(implemented_logic_ids(), EXPECTED_REAL_LOGIC_IDS)
        self.assertEqual(len(implemented_logic_ids()), 93)
        self.assertFalse(has_discrete_sutra_logic("2.1.1"))
        self.assertFalse(has_discrete_sutra_logic("4.1.1"))

    def test_each_truth_gated_sutra_has_positive_and_negative_logic(self) -> None:
        for sutra_id in sorted(EXPECTED_REAL_LOGIC_IDS):
            with self.subTest(sutra_id=sutra_id):
                self.assertTrue(has_discrete_sutra_logic(sutra_id))

                positive = evaluate_sutra(sutra_id, positive_context_for(sutra_id))
                negative = evaluate_sutra(sutra_id, negative_context_for(sutra_id))

                self.assertTrue(positive.applies)
                self.assertIn(f"sutra:{sutra_id}", positive.assigned)
                self.assertNotEqual(positive.action, "reject")
                self.assertFalse(negative.applies)


if __name__ == "__main__":
    unittest.main()
