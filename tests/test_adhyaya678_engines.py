import unittest

import sanskript.sutra_impl_6_1 as impl6_1
import sanskript.sutra_impl_6_2 as impl6_2
import sanskript.sutra_impl_7_1 as impl7_1
import sanskript.sutra_impl_8_2 as impl8_2
from sanskript.accent import Accent
from sanskript.adhyaya678_engines import (
    SAVARNA_DIRGHA,
    VRDDHI,
    AdhyayaSixOneDerivationEngine,
    AdhyayaSixSevenEightExecutionEngine,
    AngaDerivationEngine,
    SandhiDerivationEngine,
    TripadiAsiddhaEngine,
)
from sanskript.sutra_logic import positive_context_for


class AdhyayaSixSevenEightEngineTests(unittest.TestCase):
    def test_accent_engine_places_primary_accent_from_purvapada_rule(self) -> None:
        engine = AdhyayaSixSevenEightExecutionEngine()

        result = engine.derive(
            "6.2.1",
            {
                "accent_domain": "6.2",
                "accent_rule": "bahuvrihi-prakrtya",
                "accent_pattern": "prakrtya-purvapada",
                "tokens": ("raja", "purusa"),
            },
        )

        self.assertTrue(result.applies)
        self.assertIsNotNone(result.profile)
        self.assertEqual(result.profile.primary.token, "raja")
        self.assertEqual(result.profile.primary.accent, Accent.UDATTA)

    def test_anga_engine_executes_suffix_substitution(self) -> None:
        result = AngaDerivationEngine().derive(
            "7.1.17",
            features={
                "range": "7.1",
                "stem": "deva",
                "ending": "jas",
                "substitute": "\u015b\u012b",
                "operation": "substitution",
            },
        )

        self.assertTrue(result.applies)
        self.assertEqual(result.output, "deva\u015b\u012b")
        self.assertEqual(result.operations, ("substitution",))

    def test_anga_engine_executes_vrddhi_on_stem_vowel(self) -> None:
        result = AngaDerivationEngine().derive(
            "7.2.1",
            source="ci",
            features={
                "range": "7.2",
                "stem_vowel": "i",
                "target_vowel": "ai",
                "operation": VRDDHI,
            },
        )

        self.assertTrue(result.applies)
        self.assertEqual(result.output, "cai")

    def test_sandhi_engine_executes_strict_surface_boundary(self) -> None:
        result = SandhiDerivationEngine().derive(
            "6.1.101",
            "deva",
            "atra",
            features={"strict_engine": True, "expected_rule": SAVARNA_DIRGHA},
        )

        self.assertTrue(result.applies)
        self.assertEqual(result.output, "dev\u0101tra")
        self.assertEqual(result.operations, (SAVARNA_DIRGHA,))

    def test_tripadi_engine_executes_ru_substitution_intermediate(self) -> None:
        result = TripadiAsiddhaEngine().derive(
            "8.2.66",
            features={"range": "8.2", "form": "ramas", "asiddha_rule": "8_2_66", "fires": True},
        )

        self.assertTrue(result.applies)
        self.assertEqual(result.output, "ramaru")
        self.assertIn("s-to-ru", result.operations)

    def test_six_one_engine_executes_reduplication_and_sandhi(self) -> None:
        engine = AdhyayaSixOneDerivationEngine()

        reduplication = engine.derive("6.1.1", positive_context_for("6.1.1").features)
        sandhi = engine.derive("6.1.101", positive_context_for("6.1.101").features)

        self.assertTrue(reduplication.applies)
        self.assertNotEqual(reduplication.operations, ("governance",))
        self.assertIn("reduplication", reduplication.operations[0])
        self.assertTrue(sandhi.applies)
        self.assertEqual(sandhi.operations, (SAVARNA_DIRGHA,))

    def test_all_six_one_positive_fixtures_avoid_governance_fallback(self) -> None:
        engine = AdhyayaSixSevenEightExecutionEngine()
        governance_only = 0
        for sutra_id in sorted(impl6_1.IMPLEMENTED_IDS):
            result = engine.derive(sutra_id, positive_context_for(sutra_id).features)
            if result.operations == ("governance",):
                governance_only += 1
        self.assertEqual(governance_only, 0)

    def test_tripadi_governance_marks_asiddha_scope(self) -> None:
        result = TripadiAsiddhaEngine().derive(
            "8.1.1",
            features={"range": "8.1", "domain": "dvandva", "fires": True},
        )

        self.assertTrue(result.applies)
        self.assertIn("asiddha-tripadi", result.operations)
        self.assertIn("tripadi-governance", result.operations)

    def test_tripadi_rule_blocked_positive_fixture(self) -> None:
        features = dict(positive_context_for("8.2.7").features)
        result = TripadiAsiddhaEngine().derive("8.2.7", features=features)

        self.assertTrue(result.applies)
        self.assertIn("8.2.7", result.blocked_by)
        self.assertIn("asiddha-tripadi", result.operations)

    def test_six_to_eight_registry_predicates_are_engine_backed(self) -> None:
        for module, sutra_id in (
            (impl6_1, "6.1.1"),
            (impl6_2, "6.2.1"),
            (impl7_1, "7.1.17"),
            (impl8_2, "8.2.66"),
        ):
            with self.subTest(module=module.__name__, sutra_id=sutra_id):
                handler = module.handler_for(sutra_id)
                self.assertTrue(getattr(handler, "__sanskript_engine_backed__", False))
                self.assertTrue(handler(module.positive_features(sutra_id)))


if __name__ == "__main__":
    unittest.main()
