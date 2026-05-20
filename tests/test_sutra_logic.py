import unittest
import inspect

from sanskript.adhyaya1 import implemented_sutra_ids as adhyaya1_implemented_sutra_ids
from sanskript.adhyaya23 import expected_adhyaya23_ids
from sanskript.adhyaya456 import implemented_sutra_ids as adhyaya456_implemented_sutra_ids
from sanskript.derivation import KrtSuffix
from sanskript.grammar import Case
from sanskript.tinanta import DhatuType
import sanskript.sutra_handlers_adhyaya23 as h23
import sanskript.sutra_impl_1_1 as impl1_1
import sanskript.sutra_impl_1_rest as impl1_rest
import sanskript.sutra_impl_2 as impl2
import sanskript.sutra_impl_3_1 as impl3_1
import sanskript.sutra_impl_3_2 as impl3_2
import sanskript.sutra_impl_3_3 as impl3_3
import sanskript.sutra_impl_3_4 as impl3_4
import sanskript.sutra_impl_4 as impl4
import sanskript.sutra_impl_5 as impl5

REAL_IMPLEMENTATION_MODULES = (
    impl1_1,
    impl1_rest,
    impl2,
    impl3_1,
    impl3_2,
    impl3_3,
    impl3_4,
    impl4,
    impl5,
)
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

EXPECTED_REAL_LOGIC_IDS = (
    adhyaya1_implemented_sutra_ids()
    | frozenset(expected_adhyaya23_ids())
    | adhyaya456_implemented_sutra_ids()
)


class SutraLogicTests(unittest.TestCase):
    def test_canonical_index_contains_full_sutra_patha(self) -> None:
        records = sutra_records()

        self.assertEqual(len(records), 3983)
        self.assertEqual(sutra_record("1.1.1").sutra_text_iast, "vṛddhirādaic")
        self.assertEqual(sutra_record("8.4.68").sutra_text_iast, "a a iti")

    def test_truth_gate_is_not_the_old_generated_adhyaya_one_to_six_metric(self) -> None:
        self.assertEqual(implemented_logic_ids(), EXPECTED_REAL_LOGIC_IDS)
        self.assertEqual(len(implemented_logic_ids()), 2447)
        self.assertTrue(has_discrete_sutra_logic("2.1.1"))
        self.assertTrue(has_discrete_sutra_logic("4.1.1"))
        self.assertTrue(has_discrete_sutra_logic("5.1.1"))

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

    def test_adhyaya23_handlers_are_not_index_cycle_scaffolds(self) -> None:
        source = inspect.getsource(h23)

        self.assertNotIn("index %", source)
        self.assertNotIn("pada{index}", source)
        self.assertNotIn("vibhakti_{sutra_id", source)
        self.assertEqual(h23._spec("2.3.42").payload["cases"], (Case.ABLATIVE,))
        self.assertEqual(h23._spec("3.1.5").payload["suffix"], "san")
        self.assertEqual(h23._spec("3.1.5").payload["kind"], DhatuType.DESIDERATIVE)
        self.assertEqual(h23._spec("3.1.68").payload["vikarana"], "a")
        self.assertEqual(h23._spec("3.2.102").payload["suffix"], KrtSuffix.KTA)
        self.assertEqual(h23._spec("3.3.115").payload["suffix"], KrtSuffix.LYUT)

    def test_no_collapsed_duplicate_bodies_in_adhyaya_1(self) -> None:
        """No two distinct Adhyāya-1 sūtras may share the same one-line
        evaluator body. Each sūtra encodes a distinct Pāṇinian condition; if
        the bodies collapse, the truth-gate cannot tell the sūtras apart.

        A small allow-list covers cases where Pāṇini explicitly defines two
        sūtras to point at the same upstream predicate (e.g. 1.1.11/12/19
        all assigning pragṛhya via the shared phonology engine)."""
        ALLOWED_SHARED_BODIES = frozenset({
            'return is_pragrhya(c.get("analysis"))',
            'return whole_term_replacement_applies(str(c.get("substitute")), str(c.get("marker")))',
            'return _it_marker_is_present(c, "k")',
        })
        bodies: dict[str, str] = {}
        for sid, logic in SUTRA_LOGIC.items():
            if not sid.startswith("1."):
                continue
            src = inspect.getsource(logic.evaluator)
            body = "\n".join(
                line for line in src.split("\n")
                if line.strip() and not line.strip().startswith(("def ", '"""', "#"))
            ).strip()
            bodies[sid] = body

        by_body: dict[str, list[str]] = {}
        for sid, body in bodies.items():
            by_body.setdefault(body, []).append(sid)

        offenders: list[tuple[str, list[str]]] = [
            (body, sorted(sids))
            for body, sids in by_body.items()
            if len(sids) >= 2 and body not in ALLOWED_SHARED_BODIES
        ]
        self.assertEqual(
            offenders, [],
            f"Adhyāya-1 sūtras share identical evaluator bodies: {offenders}",
        )


class RealDiscreteImplementationTests(unittest.TestCase):
    """Every real-implementation module must provide honest Pāṇinian
    predicates and real linguistic fixtures — no slug-roundtrip scaffold
    is allowed to slip back in."""

    def test_no_real_impl_module_contains_slug_roundtrip(self) -> None:
        for module in REAL_IMPLEMENTATION_MODULES:
            with self.subTest(module=module.__name__):
                source = inspect.getsource(module)
                self.assertNotIn("return _evaluate(", source)
                self.assertNotIn('"wrong_semantic"', source)

    def test_every_real_impl_predicate_fires_on_its_fixtures(self) -> None:
        for module in REAL_IMPLEMENTATION_MODULES:
            for sid in sorted(module.IMPLEMENTED_IDS):
                with self.subTest(module=module.__name__, sutra_id=sid):
                    predicate = module.handler_for(sid)
                    self.assertTrue(
                        predicate(module.positive_features(sid)),
                        f"{sid} predicate rejected its own positive fixture",
                    )
                    self.assertFalse(
                        predicate(module.negative_features(sid)),
                        f"{sid} predicate accepted its negative fixture",
                    )

    def test_each_real_impl_sutra_is_wired_through_its_module(self) -> None:
        for module in REAL_IMPLEMENTATION_MODULES:
            for sid in sorted(module.IMPLEMENTED_IDS):
                with self.subTest(module=module.__name__, sutra_id=sid):
                    self.assertEqual(
                        SUTRA_LOGIC[sid].evaluator.__module__,
                        module.__name__,
                        f"{sid} should be wired through {module.__name__}",
                    )

    def test_adhyaya_2_is_fully_covered_by_sutra_impl_2(self) -> None:
        adhyaya2_in_h23 = {sid for sid in h23.EXTRA_SUTRA_IDS if sid.startswith("2.")}

        self.assertEqual(adhyaya2_in_h23, set(impl2.IMPLEMENTED_IDS))

    def test_adhyaya_3_1_is_fully_covered_by_sutra_impl_3_1(self) -> None:
        adhyaya3_1_in_h23 = {sid for sid in h23.EXTRA_SUTRA_IDS if sid.startswith("3.1.")}

        self.assertEqual(adhyaya3_1_in_h23, set(impl3_1.IMPLEMENTED_IDS))

    def test_adhyaya_3_2_is_fully_covered_by_sutra_impl_3_2(self) -> None:
        adhyaya3_2_in_h23 = {sid for sid in h23.EXTRA_SUTRA_IDS if sid.startswith("3.2.")}

        self.assertEqual(adhyaya3_2_in_h23, set(impl3_2.IMPLEMENTED_IDS))

    def test_adhyaya_3_3_is_fully_covered_by_sutra_impl_3_3(self) -> None:
        adhyaya3_3_in_h23 = {sid for sid in h23.EXTRA_SUTRA_IDS if sid.startswith("3.3.")}

        self.assertEqual(adhyaya3_3_in_h23, set(impl3_3.IMPLEMENTED_IDS))

    def test_adhyaya_3_4_is_fully_covered_by_sutra_impl_3_4(self) -> None:
        adhyaya3_4_in_h23 = {sid for sid in h23.EXTRA_SUTRA_IDS if sid.startswith("3.4.")}

        self.assertEqual(adhyaya3_4_in_h23, set(impl3_4.IMPLEMENTED_IDS))

    def test_adhyaya_4_is_fully_covered_by_sutra_impl_4(self) -> None:
        self.assertEqual(len(impl4.IMPLEMENTED_IDS), 633)
        for pada in ("4.1", "4.2", "4.3", "4.4"):
            with self.subTest(pada=pada):
                pada_ids = {sid for sid in impl4.IMPLEMENTED_IDS if sid.startswith(f"{pada}.")}
                self.assertGreater(len(pada_ids), 0)

    def test_adhyaya_5_is_fully_covered_by_sutra_impl_5(self) -> None:
        self.assertEqual(len(impl5.IMPLEMENTED_IDS), 553)
        for pada in ("5.1", "5.2", "5.3", "5.4"):
            with self.subTest(pada=pada):
                pada_ids = {sid for sid in impl5.IMPLEMENTED_IDS if sid.startswith(f"{pada}.")}
                self.assertGreater(len(pada_ids), 0)

    def test_sutra_impl_1_1_covers_previously_missing_pada_one_one_sutras(self) -> None:
        """sutra_impl_1_1 owns the 29 Adhyāya 1.1 sūtras that were absent
        from the inline registry (1.1.13/14/16/17/18/28-36/38/39/45/
        56-63/66-68/72). All must be wired and route through impl1_1."""
        expected = frozenset({
            "1.1.13", "1.1.14", "1.1.16", "1.1.17", "1.1.18",
            "1.1.28", "1.1.29", "1.1.30", "1.1.31", "1.1.32",
            "1.1.33", "1.1.34", "1.1.35", "1.1.36",
            "1.1.38", "1.1.39", "1.1.45",
            "1.1.56", "1.1.57", "1.1.58", "1.1.59", "1.1.60",
            "1.1.61", "1.1.62", "1.1.63",
            "1.1.66", "1.1.67", "1.1.68", "1.1.72",
        })
        self.assertEqual(set(impl1_1.IMPLEMENTED_IDS), expected)
        for sid in expected:
            with self.subTest(sutra_id=sid):
                self.assertTrue(has_discrete_sutra_logic(sid))


if __name__ == "__main__":
    unittest.main()
