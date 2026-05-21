import unittest

from sanskript.grammar import Lakara
from sanskript.paninian_engine import PaninianDerivationEngine, PaninianState
from sanskript.sutra_logic import implemented_logic_ids, positive_context_for


REAL_EFFECT_KEYS = {
    "derived_form",
    "derived_stem",
    "derivation_family",
    "derivation_operations",
    "engine_operation",
    "applied_suffix",
    "suffix_class",
    "blocked_operations",
    "suffix_position",
    "accent_pattern",
    "derivation_domain",
}


class PaninianAdhyaya3RealEffectTests(unittest.TestCase):
    def derive_one(self, sutra_id: str):
        features = dict(positive_context_for(sutra_id).features)
        return PaninianDerivationEngine().derive(PaninianState(features=features), sutra_ids=(sutra_id,))

    def test_3_2_66_havya_derives_real_krt_form(self) -> None:
        derivation = self.derive_one("3.2.66")
        step = derivation.steps[0]

        self.assertEqual(step.engine, "KrtDerivationEngine")
        self.assertEqual(step.after, "havyata")
        self.assertEqual(derivation.final.features["derived_form"], "havyata")
        self.assertEqual(derivation.final.features["applied_suffix"], "ṭa")
        self.assertTrue(step.changed)

    def test_3_1_sanadi_rule_creates_derived_dhatu_stem(self) -> None:
        derivation = self.derive_one("3.1.6")
        step = derivation.steps[0]

        self.assertEqual(step.engine, "DhatuSanadiEngine")
        self.assertEqual(step.after, "mimāṃsa")
        self.assertEqual(derivation.final.features["derived_stem"], "mimāṃsa")
        self.assertEqual(derivation.final.features["derivation_family"], "sanadi-dhatu")

    def test_lakara_rule_derives_tinanta_form(self) -> None:
        derivation = self.derive_one("3.3.15")
        step = derivation.steps[0]

        self.assertEqual(step.engine, "TinantaLakaraEngine")
        self.assertEqual(step.after, "bhaviṣyati")
        self.assertEqual(derivation.final.features["lakara"], Lakara.LRT)
        self.assertEqual(derivation.final.features["derivation_family"], "tinanta")

    def test_pratisedha_rule_blocks_instead_of_copying_fixture(self) -> None:
        derivation = self.derive_one("3.4.18")
        step = derivation.steps[0]

        self.assertEqual(step.engine, "AdhyayaThreeRealizationEngine")
        self.assertEqual(step.blocked_by, ("3.4.18",))
        self.assertIn("laṅ", derivation.final.features["blocked_operations"])
        self.assertEqual(derivation.final.features["derivation_family"], "pratisedha")

    def test_meta_governance_rule_has_durable_derivational_state(self) -> None:
        derivation = self.derive_one("3.1.92")
        step = derivation.steps[0]

        self.assertEqual(step.engine, "MetaruleGovernanceEngine")
        self.assertEqual(derivation.final.features["derivation_domain"], "upapada-krt")
        self.assertEqual(derivation.final.features["derivation_family"], "adhyaya3-governance")

    def test_all_adhyaya3_sutras_have_real_or_gating_effects(self) -> None:
        engine = PaninianDerivationEngine()
        weak: list[str] = []

        for sutra_id in sorted(
            (sid for sid in implemented_logic_ids() if sid.startswith("3.")),
            key=lambda sid: tuple(int(part) for part in sid.split(".")),
        ):
            features = dict(positive_context_for(sutra_id).features)
            derivation = engine.derive(PaninianState(features=features), sutra_ids=(sutra_id,))
            if not derivation.steps:
                weak.append(sutra_id)
                continue
            step = derivation.steps[0]
            if step.engine == "Adhyaya3Dispatch" or step.diagnostics:
                weak.append(sutra_id)
                continue
            if step.changed or step.blocked_by:
                continue
            if any(derivation.final.features.get(key) not in (None, "", (), frozenset()) for key in REAL_EFFECT_KEYS):
                continue
            weak.append(sutra_id)

        self.assertEqual(weak, [])


if __name__ == "__main__":
    unittest.main()
