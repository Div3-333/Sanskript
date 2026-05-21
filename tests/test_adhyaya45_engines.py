import unittest

from sanskript.adhyaya45_engines import (
    SamasantaEngine,
    SemanticRelationEngine,
    StriPratyayaEngine,
    TaddhitaSelectionEngine,
    TaddhitaSurfaceEngine,
    derive_adhyaya45_taddhita,
    derive_samasanta,
    derive_stri,
    resolve_adhyaya45_source,
)
from sanskript.derivation import TaddhitaSuffix, derive_taddhita
from sanskript.sutra_impl_4 import handler_for as adhyaya4_handler
from sanskript.sutra_impl_4 import positive_features as adhyaya4_positive
from sanskript.sutra_impl_5 import handler_for as adhyaya5_handler
from sanskript.sutra_impl_5 import positive_features as adhyaya5_positive


class AdhyayaFourFiveEngineTests(unittest.TestCase):
    def test_stri_engine_reuses_adhyaya_four_predicates(self) -> None:
        result = derive_stri("bāla", sutra_id="4.1.4")

        self.assertEqual(result.surface, "bālā")
        self.assertEqual(result.suffix, "ṭāp")
        self.assertEqual(result.sutra_ids, ("4.1.4",))
        self.assertIn("StriPratyayaEngine", result.engines)
        self.assertTrue(adhyaya4_handler("4.1.4")(adhyaya4_positive("4.1.4")))

    def test_taddhita_selection_and_surface_engines_reuse_predicates(self) -> None:
        selector = TaddhitaSelectionEngine()
        surface = TaddhitaSurfaceEngine()
        selection = selector.select("laghu", sutra_id="5.3.57")
        result = surface.derive(selection)

        self.assertEqual(selection.sutra.sutra_id, "5.3.57")
        self.assertEqual(result.surface, "laghutara")
        self.assertEqual(result.semantic, "degree")
        self.assertIn("TaddhitaSurfaceEngine", result.engines)
        self.assertTrue(adhyaya5_handler("5.3.57")(adhyaya5_positive("5.3.57")))

    def test_taddhita_engine_preserves_existing_anchor_derivations(self) -> None:
        apatya = derive_adhyaya45_taddhita("manu", sutra_id="4.1.92")
        matup = derive_adhyaya45_taddhita("bala", sutra_id="5.2.94")
        degree = derive_adhyaya45_taddhita("guru", sutra_id="5.3.55")

        self.assertEqual((apatya.surface, apatya.semantic), ("mānava", "apatya"))
        self.assertEqual((matup.surface, matup.semantic), ("balavān", "possession"))
        self.assertEqual((degree.surface, degree.semantic), ("gariṣṭha", "atishayana"))
        self.assertEqual(derive_taddhita("bala", suffix=TaddhitaSuffix.MATUP).surface, "balavān")

    def test_semantic_engine_classifies_rule_domains(self) -> None:
        engine = SemanticRelationEngine()

        self.assertEqual(engine.relation_for("4.1.92", {}), "apatya")
        self.assertEqual(engine.relation_for("5.2.94", {}), "possession")
        self.assertEqual(engine.relation_for("5.3.57", {}), "degree")
        self.assertIn("compound-final", engine.describe("samāsānta"))

    def test_samasanta_engine_derives_compound_final_surfaces(self) -> None:
        result = derive_samasanta(members=("prati", "sāma"), sutra_id="5.4.75")

        self.assertEqual(result.source, "pratisāma")
        self.assertEqual(result.surface, "pratisāma")
        self.assertEqual(result.sutra_ids, ("5.4.75",))
        self.assertIn("SamasantaEngine", result.engines)

    def test_source_resolver_does_not_treat_semantics_as_stems(self) -> None:
        self.assertEqual(resolve_adhyaya45_source({"semantic": "tasmai_hita", "rule": "continuation"}), "")

    def test_continuation_rules_inherit_prior_suffix_and_form_surface(self) -> None:
        kaumara = derive_adhyaya45_taddhita(
            "",
            sutra_id="4.2.13",
            features={"semantic": "kaumāra_apūrva_vacana", "rule": "continuation"},
        )
        hita = derive_adhyaya45_taddhita(
            "",
            sutra_id="5.1.5",
            features={"semantic": "tasmai_hita", "rule": "continuation"},
        )

        self.assertEqual((kaumara.source, kaumara.surface, kaumara.suffix), ("kumāra", "kaumāra", "añ"))
        self.assertIn("anuvritti:4.2.12", kaumara.operations)
        self.assertEqual((hita.source, hita.surface, hita.suffix), ("bala", "balat", "at"))
        self.assertIn("anuvritti:5.1.2", hita.operations)

    def test_public_engine_classes_are_the_five_adapters(self) -> None:
        engines = (
            StriPratyayaEngine(),
            TaddhitaSelectionEngine(),
            TaddhitaSurfaceEngine(),
            SemanticRelationEngine(),
            SamasantaEngine(),
        )

        self.assertEqual(len(engines), 5)


if __name__ == "__main__":
    unittest.main()
