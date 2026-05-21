import unittest

from sanskript.adhyaya678_engines import SAVARNA_DIRGHA
from sanskript.grammar import Analysis, Case, Gender, GrammaticalNumber, Lakara, Pada, PartOfSpeech, Role
from sanskript.paninian_effects import has_meaningful_effect
from sanskript.paninian_engine import PaninianDerivationEngine, PaninianState, derive_paninian
from sanskript.sutra_logic import positive_context_for


class PaninianDerivationEngineTests(unittest.TestCase):
    def test_sequence_reuses_samasa_and_lopa_engines(self) -> None:
        deva = Analysis("devasya", "deva", PartOfSpeech.NOUN, case=Case.GENITIVE, gender=Gender.MASCULINE)
        purusa = Analysis("purusah", "purusa", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.MASCULINE)

        derivation = PaninianDerivationEngine().derive(
            PaninianState(members=(deva, purusa)),
            sutra_ids=("2.1.22", "2.4.71"),
        )

        self.assertEqual(derivation.form, "devapurusah")
        self.assertEqual(derivation.sutra_ids, ("2.1.22", "2.4.71"))
        self.assertTrue(all(step.engine == "SamasaDerivationEngine" for step in derivation.steps))

    def test_sequence_reuses_taddhita_surface_engine(self) -> None:
        derivation = derive_paninian(source="bala", sutra_ids=("5.2.94",), features={"semantic": "possession"})

        self.assertEqual(derivation.form, "balav\u0101n")
        self.assertEqual(derivation.steps[0].engine, "TaddhitaSurfaceEngine")
        self.assertIn("matup", derivation.steps[0].operation)

    def test_sequence_reuses_late_sandhi_engine(self) -> None:
        derivation = derive_paninian(
            features={
                "left": "deva",
                "right": "atra",
                "strict_engine": True,
                "expected_rule": SAVARNA_DIRGHA,
            },
            sutra_ids=("6.1.101",),
        )

        self.assertEqual(derivation.form, "dev\u0101tra")
        self.assertEqual(derivation.steps[0].engine, "SandhiDerivationEngine")
        self.assertEqual(derivation.steps[0].operation, SAVARNA_DIRGHA)

    def test_automatic_selection_resolves_role_to_vibhakti(self) -> None:
        derivation = PaninianDerivationEngine().derive(
            PaninianState(role=Role.KARMAN),
            prefixes=("2.3.",),
            max_steps=1,
        )

        self.assertEqual(derivation.sutra_ids, ("2.3.2",))
        self.assertEqual(derivation.final.features["case"], Case.ACCUSATIVE)
        self.assertIn("vibhakti", derivation.steps[0].operation)

    def test_samjna_sutra_records_phonological_state(self) -> None:
        features = dict(positive_context_for("1.1.1").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("1.1.1",),
        )
        step = derivation.steps[0]
        self.assertIn("vrddhi", derivation.final.features.get("phonological_labels", ()))
        self.assertTrue(
            has_meaningful_effect(
                before=step.before,
                after=step.after,
                features=derivation.final.features,
            )
        )

    def test_upapada_sutra_records_derivational_context(self) -> None:
        features = dict(positive_context_for("3.2.66").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("3.2.66",),
        )
        step = derivation.steps[0]
        self.assertEqual(derivation.final.features.get("upapada"), "havya")
        self.assertEqual(step.engine, "KrtDerivationEngine")
        self.assertTrue(
            has_meaningful_effect(
                before=step.before,
                after=step.after,
                features=derivation.final.features,
            )
        )

    def test_krt_sutra_derives_surface_from_source_and_suffix(self) -> None:
        features = dict(positive_context_for("3.2.16").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("3.2.16",),
        )
        step = derivation.steps[0]
        self.assertEqual(derivation.form, "cara")
        self.assertEqual(step.engine, "KrtDerivationEngine")
        self.assertIn("krt", step.operation)

    def test_lakara_fixture_routes_through_pratyaya_lopa_engine(self) -> None:
        features = dict(positive_context_for("2.4.40").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("2.4.40",),
        )
        step = derivation.steps[0]
        self.assertEqual(step.engine, "PratyayaLopaEngine")
        self.assertEqual(derivation.final.features.get("lakara"), Lakara.LIT)

    def test_pada_and_suffix_fixture_recorded_for_2_4_77(self) -> None:
        features = dict(positive_context_for("2.4.77").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("2.4.77",),
        )
        step = derivation.steps[0]
        self.assertEqual(step.engine, "PratyayaLopaEngine")
        self.assertEqual(derivation.final.features.get("pada"), Pada.PARASMAIPADA)
        self.assertEqual(derivation.final.features.get("suffix"), "sic")
        self.assertEqual(derivation.final.features.get("dhatu_lemma"), "bhū")

    def test_companion_vibhakti_fixture_records_case(self) -> None:
        features = dict(positive_context_for("2.3.35").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("2.3.35",),
        )
        step = derivation.steps[0]
        self.assertEqual(step.engine, "KarakaVibhaktiEngine")
        self.assertEqual(derivation.final.features.get("case"), Case.ACCUSATIVE)

    def test_pratisedha_sutra_records_blocked_operations(self) -> None:
        features = dict(positive_context_for("1.1.4").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("1.1.4",),
        )
        self.assertIn("guna-vrddhi", derivation.final.features.get("blocked_operations", ()))
        step = derivation.steps[0]
        self.assertTrue(
            has_meaningful_effect(
                before=step.before,
                after=step.after,
                features=derivation.final.features,
            )
        )

    def test_pragrhya_sutra_marks_phonological_state(self) -> None:
        features = dict(positive_context_for("1.1.11").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("1.1.11",),
        )
        self.assertIn("pragrhya", derivation.final.features.get("phonological_labels", ()))
        step = derivation.steps[0]
        self.assertTrue(
            has_meaningful_effect(
                before=step.before,
                after=step.after,
                features=derivation.final.features,
            )
        )

    def test_it_lopa_sutra_changes_upadesha_surface(self) -> None:
        features = dict(positive_context_for("1.3.9").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("1.3.9",),
        )
        self.assertEqual(derivation.form, "ta")
        self.assertEqual(derivation.final.features.get("lemma"), "ta")
        step = derivation.steps[0]
        self.assertTrue(
            has_meaningful_effect(
                before=step.before,
                after=step.after,
                features=derivation.final.features,
            )
        )

    def test_substitution_site_sutra_records_genitive_reference(self) -> None:
        features = dict(positive_context_for("1.1.49").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("1.1.49",),
        )
        self.assertEqual(derivation.final.features.get("reference_case"), Case.GENITIVE)
        step = derivation.steps[0]
        self.assertTrue(
            has_meaningful_effect(
                before=step.before,
                after=step.after,
                features=derivation.final.features,
            )
        )

    def test_kit_sutra_records_phonological_marker(self) -> None:
        features = dict(positive_context_for("1.2.5").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("1.2.5",),
        )
        self.assertIn("kit", derivation.final.features.get("phonological_labels", ()))
        step = derivation.steps[0]
        self.assertTrue(
            has_meaningful_effect(
                before=step.before,
                after=step.after,
                features=derivation.final.features,
            )
        )

    def test_laghu_sutra_records_samjna_weight(self) -> None:
        from sanskript.grammar import Samjna

        features = dict(positive_context_for("1.4.10").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("1.4.10",),
        )
        self.assertIn(Samjna.LAGHU, derivation.final.features.get("samjnas", ()))
        step = derivation.steps[0]
        self.assertTrue(
            has_meaningful_effect(
                before=step.before,
                after=step.after,
                features=derivation.final.features,
            )
        )

    def test_late_reduplication_propagates_surface(self) -> None:
        features = dict(positive_context_for("6.1.1").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("6.1.1",),
        )
        step = derivation.steps[0]
        self.assertNotEqual(step.before, step.after)
        self.assertEqual(derivation.form, step.after)
        self.assertTrue(
            has_meaningful_effect(
                before=step.before,
                after=step.after,
                features=derivation.final.features,
            )
        )

    def test_late_samjna_records_assigns_samjna_state(self) -> None:
        features = dict(positive_context_for("6.1.4").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("6.1.4",),
        )
        self.assertEqual(derivation.final.features.get("assigns_samjna"), "abhyāsa")
        self.assertTrue(
            has_meaningful_effect(
                before=derivation.steps[0].before,
                after=derivation.steps[0].after,
                features=derivation.final.features,
            )
        )

    def test_late_pratisedha_records_blocked_sutra(self) -> None:
        features = dict(positive_context_for("6.1.20").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("6.1.20",),
        )
        self.assertIn("6.1.20", derivation.final.blocked_sutras)
        self.assertIn("6.1.20", derivation.steps[0].blocked_by)

    def test_late_anga_substitution_propagates_surface(self) -> None:
        features = {
            "range": "7.1",
            "stem": "deva",
            "ending": "jas",
            "substitute": "śī",
            "operation": "substitution",
        }
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("7.1.17",),
        )
        step = derivation.steps[0]
        self.assertEqual(derivation.form, "devaśī")
        self.assertEqual(step.engine, "AngaDerivationEngine")
        self.assertIn("substitution", step.operation)

    def test_late_tripadi_records_asiddha_and_blocked(self) -> None:
        features = dict(positive_context_for("8.2.7").features)
        derivation = PaninianDerivationEngine().derive(
            PaninianState(features=features),
            sutra_ids=("8.2.7",),
        )
        self.assertEqual(derivation.final.features.get("asiddha_scope"), "tripadi")
        self.assertIn("8.2.7", derivation.final.blocked_sutras)
        self.assertIn("asiddha-tripadi", derivation.steps[0].operation)


class AdhyayaFourFiveWeakSutraTests(unittest.TestCase):
    """Former predicate-only 4.x/5.x sutras must route through real 4/5 engines."""

    def _derive_fixture(self, sutra_id: str) -> tuple:
        features = dict(positive_context_for(sutra_id).features)
        form = (
            features.get("form")
            or features.get("surface")
            or features.get("source")
            or features.get("lemma")
            or features.get("stem")
            or ""
        )
        derivation = PaninianDerivationEngine().derive(
            PaninianState(form=form, source=features.get("source") or form, features=features),
            sutra_ids=(sutra_id,),
        )
        step = derivation.steps[-1]
        return derivation, step

    def test_4_1_2_inline_stri_derivation(self) -> None:
        derivation, step = self._derive_fixture("4.1.2")
        self.assertEqual(derivation.form, "latā")
        self.assertNotIn("Dispatch", step.engine)
        self.assertIn(step.engine, ("StriPratyayaEngine", "subanta.decline_aa_feminine"))

    def test_4_2_13_continuation_inherits_real_taddhita_suffix(self) -> None:
        derivation, step = self._derive_fixture("4.2.13")
        self.assertNotIn("Dispatch", step.engine)
        self.assertEqual(derivation.form, "kaumāra")
        self.assertIn("anuvritti:4.2.12", step.operation)
        self.assertIn("añ-taddhita", step.operation)
        self.assertNotIn("continuation-domain", step.operation)
        self.assertEqual(derivation.final.features.get("source"), "kumāra")
        self.assertEqual(derivation.final.features.get("suffix"), "añ")
        self.assertEqual(derivation.final.features.get("anuvritti_from"), "4.2.12")

    def test_4_1_88_luk_records_phonological_state(self) -> None:
        derivation, step = self._derive_fixture("4.1.88")
        self.assertEqual(step.engine, "TaddhitaSurfaceEngine")
        self.assertIn("luk", derivation.final.features.get("phonological_labels", ()))

    def test_5_1_5_continuation_inherits_real_taddhita_suffix(self) -> None:
        derivation, step = self._derive_fixture("5.1.5")
        self.assertEqual(step.engine, "TaddhitaSurfaceEngine")
        self.assertEqual(derivation.form, "balat")
        self.assertIn("anuvritti:5.1.2", step.operation)
        self.assertIn("at-generic-taddhita-surface", step.operation)
        self.assertNotIn("continuation-domain", step.operation)
        self.assertEqual(derivation.final.features.get("active_semantic"), "tasmai_hita")
        self.assertEqual(derivation.final.features.get("source"), "bala")
        self.assertEqual(derivation.final.features.get("suffix"), "at")

    def test_5_4_3_samasanta_surface_from_stem_class(self) -> None:
        derivation, step = self._derive_fixture("5.4.3")
        self.assertEqual(step.engine, "SamasantaEngine")
        self.assertEqual(derivation.form, "sthūlaka")
        self.assertTrue(
            has_meaningful_effect(
                before=step.before,
                after=step.after,
                features=derivation.final.features,
            )
        )


class AdhyayaOneClosureTests(unittest.TestCase):
    def test_meta_karaka_sutras_record_reusable_state(self) -> None:
        engine = PaninianDerivationEngine()
        samples = (
            ("1.1.66", "reference_case", "locative"),
            ("1.1.68", "refers_to_own_form", True),
            ("1.4.24", "role", Role.APADANA),
            ("1.4.32", "role", Role.SAMPRADANA),
            ("1.3.1", "root_class", "dhatu"),
            ("1.2.43", "samasa_role", "upasarjana"),
            ("1.4.2", "rule_priority", True),
        )
        for sutra_id, key, expected in samples:
            with self.subTest(sutra_id=sutra_id):
                features = dict(positive_context_for(sutra_id).features)
                derivation = engine.derive(PaninianState(features=features), sutra_ids=(sutra_id,))
                step = derivation.steps[0]
                self.assertTrue(
                    has_meaningful_effect(
                        before=step.before,
                        after=step.after,
                        features=derivation.final.features,
                        blocked_by=step.blocked_by,
                    )
                )
                self.assertEqual(derivation.final.features.get(key), expected)

    def test_all_adhyaya_one_sutras_have_meaningful_coordinator_effect(self) -> None:
        from sanskript.sutra_logic import implemented_logic_ids

        engine = PaninianDerivationEngine()
        weak: list[str] = []
        for sutra_id in implemented_logic_ids():
            if not sutra_id.startswith("1."):
                continue
            features = dict(positive_context_for(sutra_id).features)
            derivation = engine.derive(PaninianState(features=features), sutra_ids=(sutra_id,))
            if not derivation.steps:
                weak.append(sutra_id)
                continue
            step = derivation.steps[0]
            if not has_meaningful_effect(
                before=step.before,
                after=step.after,
                features=derivation.final.features,
                blocked_by=step.blocked_by,
            ):
                weak.append(sutra_id)
        self.assertEqual(weak, [])


if __name__ == "__main__":
    unittest.main()
