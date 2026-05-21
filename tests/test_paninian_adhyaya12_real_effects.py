import unittest

from sanskript.grammar import Case, Pada, Samjna
from sanskript.paninian_engine import PaninianDerivationEngine, PaninianState
from sanskript.samasa import SamasaType
from sanskript.sutra_logic import positive_context_for


class PaninianAdhyayaOneTwoRealEffectTests(unittest.TestCase):
    def derive_fixture(self, sutra_id: str):
        features = dict(positive_context_for(sutra_id).features)
        return PaninianDerivationEngine().derive(PaninianState(features=features), sutra_ids=(sutra_id,))

    def test_2_4_77_sic_luk_changes_surface_instead_of_echoing_fixture(self) -> None:
        derivation = self.derive_fixture("2.4.77")
        step = derivation.steps[0]

        self.assertEqual(step.engine, "PratyayaLopaEngine")
        self.assertEqual(step.before, "bhū+sic")
        self.assertEqual(step.after, "bhū")
        self.assertEqual(derivation.form, "bhū")
        self.assertIn("luk:sic", step.operation)
        self.assertEqual(derivation.final.features["elided_suffix"], "sic")
        self.assertEqual(derivation.final.features["pada"], Pada.PARASMAIPADA)

    def test_2_4_72_shap_luk_removes_vikarana_surface(self) -> None:
        derivation = self.derive_fixture("2.4.72")
        step = derivation.steps[0]

        self.assertEqual(step.engine, "PratyayaLopaEngine")
        self.assertEqual(step.before, "ad+a")
        self.assertEqual(step.after, "ad")
        self.assertIn("luk:shap", step.operation)
        self.assertEqual(derivation.final.features["lopa_target"], "shap")

    def test_2_1_55_materializes_karmadharaya_compound(self) -> None:
        derivation = self.derive_fixture("2.1.55")
        step = derivation.steps[0]

        self.assertEqual(step.engine, "SamasaDerivationEngine")
        self.assertEqual(step.after, "vyāghrapuruṣa")
        self.assertIn("samasa-sutra:2.1.55", step.operation)
        self.assertEqual(derivation.final.features["compound_type"], SamasaType.KARMADHARAYA)
        self.assertEqual(derivation.final.features["compound_members"], ("vyāghra", "puruṣa"))

    def test_2_2_19_materializes_upapada_compound(self) -> None:
        derivation = self.derive_fixture("2.2.19")
        step = derivation.steps[0]

        self.assertEqual(step.engine, "SamasaDerivationEngine")
        self.assertEqual(step.before, "go + ka")
        self.assertEqual(step.after, "goka")
        self.assertIn("internal-sup-lopa", step.operation)
        self.assertEqual(derivation.final.features["compound_type"], SamasaType.TATPURUSHA)

    def test_1_4_14_uses_analysis_surface_and_specific_samjna_state(self) -> None:
        derivation = self.derive_fixture("1.4.14")
        step = derivation.steps[0]

        self.assertEqual(step.engine, "SamjnaTechnicalEngine")
        self.assertEqual(step.before, "devah")
        self.assertIn("samjna:pada", step.operation)
        self.assertIn(Samjna.PADA, derivation.final.features["samjnas"])

    def test_1_1_54_targets_following_initial_not_final_sound(self) -> None:
        derivation = self.derive_fixture("1.1.54")

        self.assertEqual(derivation.steps[0].engine, "MetaruleGovernanceEngine")
        self.assertEqual(derivation.final.features["substitution_index"], 0)
        self.assertEqual(derivation.final.features["target_scope"], "following-initial")
        self.assertEqual(derivation.final.features["derivation_family"], "metarule-governance")

    def test_2_3_52_records_real_genitive_case_selection(self) -> None:
        derivation = self.derive_fixture("2.3.52")

        self.assertEqual(derivation.steps[0].engine, "KarakaVibhaktiEngine")
        self.assertEqual(derivation.final.features["assigned_case"], Case.GENITIVE)
        self.assertEqual(derivation.final.features["case_basis"], "adhigama")
        self.assertEqual(derivation.final.features["derivation_family"], "vibhakti-selection")

    def test_2_4_53_derives_bru_to_vac_substitution(self) -> None:
        derivation = self.derive_fixture("2.4.53")
        step = derivation.steps[0]

        self.assertEqual(step.engine, "PratyayaLopaEngine")
        self.assertEqual(step.before, "brū")
        self.assertEqual(step.after, "vac")
        self.assertEqual(derivation.final.features["root_substitution"], "vac")

    def test_2_4_85_materializes_lut_first_person_replacements(self) -> None:
        derivation = self.derive_fixture("2.4.85")

        self.assertEqual(derivation.steps[0].after, "ḍā/rau/ras")
        self.assertEqual(derivation.final.features["tin_replacement"], ("ḍā", "rau", "ras"))
        self.assertEqual(derivation.final.features["derivation_family"], "tin-substitution")


if __name__ == "__main__":
    unittest.main()
