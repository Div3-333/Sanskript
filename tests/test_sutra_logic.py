import unittest

from sanskript.sutra_logic import (
    SUTRA_LOGIC,
    evaluate_sutra,
    has_discrete_sutra_logic,
    implemented_logic_ids,
    negative_context_for,
    positive_context_for,
    sutra_record,
    sutra_records,
)


EXPECTED_REAL_LOGIC_IDS = frozenset(
    """
    1.1.1 1.1.2 1.1.3 1.1.4 1.1.5 1.1.6 1.1.7 1.1.8 1.1.9 1.1.10 1.1.11 1.1.12
    1.1.15 1.1.19 1.1.20 1.1.21 1.1.22 1.1.23 1.1.24 1.1.25 1.1.26 1.1.27
    1.1.37 1.1.40 1.1.41 1.1.42 1.1.43 1.1.44 1.1.46 1.1.47 1.1.48 1.1.49
    1.1.50 1.1.51 1.1.52 1.1.53 1.1.54 1.1.55 1.1.64 1.1.65 1.1.69 1.1.70
    1.1.71 1.1.73 1.1.74 1.1.75
    1.2.1 1.2.2 1.2.4 1.2.5 1.2.6 1.2.7 1.2.8 1.2.9 1.2.11 1.2.12 1.2.13
    1.2.14 1.2.15 1.2.17 1.2.18 1.2.19 1.2.20 1.2.26 1.2.41 1.2.64 1.2.65
    1.2.67 1.2.68 1.2.69 1.2.70 1.2.71 1.2.72 1.2.73
    1.3.2 1.3.3 1.3.4 1.3.5 1.3.6 1.3.7 1.3.8 1.3.9 1.3.12 1.3.13
    1.3.17 1.3.18 1.3.19 1.3.21 1.3.24 1.3.25 1.3.29 1.3.32 1.3.40 1.3.72 1.3.78
    1.4.3 1.4.7 1.4.10 1.4.11 1.4.12 1.4.13 1.4.14 1.4.17 1.4.18 1.4.24
    1.4.25 1.4.26 1.4.27 1.4.28 1.4.29 1.4.32 1.4.33 1.4.42 1.4.45 1.4.49
    1.4.54 1.4.58 1.4.59 1.4.60 1.4.109 1.4.110
    2.1.1 2.1.4 2.1.5 2.1.6 2.1.7 2.1.8 2.1.9 2.1.10 2.1.11 2.1.12 2.1.13
    2.1.14 2.1.15 2.1.16 2.1.17 2.1.18 2.1.19 2.1.20 2.1.21 2.1.22 2.1.23
    2.1.24 2.1.30 2.1.36 2.1.57
    2.2.29 2.2.30
    2.3.1 2.3.2 2.3.3 2.3.4 2.3.5 2.3.6 2.3.7 2.3.8 2.3.9 2.3.10 2.3.11 2.3.12
    2.3.13 2.3.14 2.3.15 2.3.16 2.3.17 2.3.18 2.3.19 2.3.20 2.3.21 2.3.22
    2.3.23 2.3.24 2.3.25 2.3.26 2.3.27 2.3.28 2.3.29 2.3.30 2.3.31 2.3.32
    2.3.33 2.3.34 2.3.35 2.3.36 2.3.50
    2.4.1 2.4.17 2.4.18 2.4.26 2.4.36 2.4.37 2.4.42 2.4.45 2.4.47 2.4.48 2.4.52 2.4.71 2.4.72
    3.1.5 3.1.8 3.1.22 3.1.25 3.1.68 3.1.69 3.1.73 3.1.77 3.1.78 3.1.79 3.1.81 3.1.91 3.1.93
    3.2.1 3.2.3 3.2.16 3.2.102 3.2.110 3.2.111 3.2.123 3.2.135
    3.3.15 3.3.18 3.3.33 3.3.94 3.3.115 3.3.121 3.3.139 3.3.161 3.3.162
    3.4.69 3.4.71 3.4.72 3.4.79 3.4.80 3.4.86 3.4.87 3.4.88 3.4.92 3.4.100 3.4.101 3.4.108 3.4.113 3.4.114 3.4.115
    4.1.2 4.1.92 5.2.94 5.3.55
    6.1.78 6.1.87 6.1.88 6.1.101 6.2.1 6.3.1 6.4.1 6.4.2
    """.split()
)


class SutraLogicTests(unittest.TestCase):
    def test_canonical_index_contains_full_sutra_patha(self) -> None:
        records = sutra_records()

        self.assertEqual(len(records), 3983)
        self.assertEqual(sutra_record("1.1.1").sutra_text_iast, "vṛddhirādaic")
        self.assertEqual(sutra_record("8.4.68").sutra_text_iast, "a a iti")

    def test_truth_gate_is_not_the_old_generated_adhyaya_one_to_six_metric(self) -> None:
        self.assertEqual(implemented_logic_ids(), EXPECTED_REAL_LOGIC_IDS)
        self.assertEqual(len(implemented_logic_ids()), 255)
        self.assertTrue(has_discrete_sutra_logic("2.1.1"))
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

    def test_truth_gated_handlers_are_named_functions(self) -> None:
        for sutra_id in sorted(EXPECTED_REAL_LOGIC_IDS):
            with self.subTest(sutra_id=sutra_id):
                evaluator = SUTRA_LOGIC[sutra_id].evaluator
                self.assertEqual(evaluator.__name__, f"sutra_{sutra_id.replace('.', '_')}")


if __name__ == "__main__":
    unittest.main()
