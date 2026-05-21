import unittest

from sanskript.adhyaya678_engines import AdhyayaSixSevenEightExecutionEngine
from sanskript.paninian_engine import PaninianDerivationEngine, PaninianState
from sanskript.sutra_logic import positive_context_for


class Adhyaya678RealEffectTests(unittest.TestCase):
    def test_synthetic_tripadi_sound_fixtures_execute_without_diagnostics(self) -> None:
        engine = AdhyayaSixSevenEightExecutionEngine()

        for sutra_id in ("8.2.4", "8.2.5", "8.2.6", "8.2.7", "8.2.23", "8.2.76"):
            with self.subTest(sutra_id=sutra_id):
                result = engine.derive(sutra_id, positive_context_for(sutra_id).features)

                self.assertTrue(result.applies)
                self.assertFalse(result.diagnostics)
                self.assertNotEqual(result.input, result.output)
                self.assertIn("asiddha-tripadi", result.operations)

    def test_eight_three_sound_families_execute_real_boundaries(self) -> None:
        engine = AdhyayaSixSevenEightExecutionEngine()

        samples = {
            "8.3.1": "s-to-ru",
            "8.3.23": "visarjanīyasya-sa",
            "8.3.39": "ṣatva",
            "8.3.65": "ṣatva",
        }
        for sutra_id, operation in samples.items():
            with self.subTest(sutra_id=sutra_id):
                result = engine.derive(sutra_id, positive_context_for(sutra_id).features)

                self.assertTrue(result.applies)
                self.assertFalse(result.diagnostics)
                self.assertNotEqual(result.input, result.output)
                self.assertIn(operation, result.operations)
                self.assertIn("asiddha-tripadi", result.operations)

    def test_pratisedha_tripadi_no_longer_uses_abstract_diagnostic_fallback(self) -> None:
        result = AdhyayaSixSevenEightExecutionEngine().derive(
            "8.3.102",
            positive_context_for("8.3.102").features,
        )

        self.assertTrue(result.applies)
        self.assertFalse(result.diagnostics)
        self.assertEqual(result.operations, ("pratisedha", "asiddha-tripadi"))

    def test_anga_sound_operations_execute_surfaces(self) -> None:
        engine = AdhyayaSixSevenEightExecutionEngine()

        samples = {
            "6.1.32": "hu",
            "6.1.75": "ā",
            "6.1.77": "y",
        }
        for sutra_id, expected in samples.items():
            with self.subTest(sutra_id=sutra_id):
                result = engine.derive(sutra_id, positive_context_for(sutra_id).features)

                self.assertTrue(result.applies)
                self.assertEqual(result.output, expected)
                self.assertNotEqual(result.input, result.output)

    def test_coordinator_persists_eight_three_surface_change(self) -> None:
        features = dict(positive_context_for("8.3.39").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("8.3.39",),
        )

        self.assertEqual(derivation.form, "niṣkara")
        self.assertFalse(derivation.steps[0].diagnostics)
        self.assertIn("ṣatva", derivation.steps[0].operation)


if __name__ == "__main__":
    unittest.main()
