import json
import tempfile
import unittest
from pathlib import Path

from sanskript.grammar import Case, Gender, GrammaticalNumber, Lakara, PartOfSpeech, Person, Role
from sanskript.grammar_register import register_digest, register_entries, register_intents, runtime_register_entries
from sanskript.morphology_facade import MorphologyFacade
from sanskript.morphology_lexicon import (
    DEFAULT_LEXICON_PATH,
    DEFAULT_OVERRIDES_PATH,
    build_lexicon_artifact,
    load_controlled_lexicon,
    load_lexicon_overrides,
    merge_lexicon_with_overrides,
    record_to_analysis,
    LexiconRecord,
)
from sanskript.morphology_synth import (
    DerivationIntent,
    DerivationKind,
    RecipePlanner,
    auto_derive,
    synthesize,
)
from sanskript.morphology_validate import validate_surface
from sanskript.parser import parse_program


class MorphologySynthTests(unittest.TestCase):
    def test_subanta_synthesis_produces_phale(self) -> None:
        result = synthesize(
            DerivationIntent.subanta(
                lemma="phala",
                case=Case.LOCATIVE,
                number=GrammaticalNumber.SINGULAR,
                gender=Gender.NEUTER,
            )
        )
        self.assertEqual(result.surface, "phale")
        self.assertEqual(result.engine, "PaninianDerivationEngine")
        self.assertEqual(result.analysis.role, Role.ADHIKARANA)
        self.assertTrue(result.sutra_ids)

    def test_tinanta_synthesis_produces_vardhayati(self) -> None:
        result = synthesize(
            DerivationIntent.tinanta(
                lemma="vṛdh",
                lakara=Lakara.LAT,
                person=Person.THIRD,
                number=GrammaticalNumber.SINGULAR,
            )
        )
        self.assertEqual(result.surface, "vardhayati")
        self.assertEqual(result.engine, "PaninianDerivationEngine")

    def test_krt_synthesis_produces_drista(self) -> None:
        result = synthesize(DerivationIntent.krt(source="dṛś", suffix="kta"))
        self.assertEqual(result.surface, "dṛṣṭa")
        self.assertEqual(result.engine, "KrtDerivationEngine")

    def test_krt_synthesis_produces_bhutva(self) -> None:
        result = synthesize(DerivationIntent.krt(source="bhū", suffix="ktvā"))
        self.assertEqual(result.surface, "bhūtvā")
        self.assertEqual(result.engine, "KrtDerivationEngine")

    def test_taddhita_synthesis_produces_balavan(self) -> None:
        result = synthesize(
            DerivationIntent.taddhita(source="bala", semantic="possession", sutra_ids=("5.2.94",))
        )
        self.assertEqual(result.surface, "balavān")
        self.assertEqual(result.engine, "TaddhitaCatalogEngine")

    def test_samasa_synthesis_produces_devapurusa(self) -> None:
        from sanskript.grammar import Gender
        from sanskript.samasa import SamasaType

        result = synthesize(
            DerivationIntent.samasa(
                member_lemmas=("deva", "purusa"),
                compound_type=SamasaType.TATPURUSHA,
                features={
                    "member_specs": (
                        {
                            "surface": "devasya",
                            "lemma": "deva",
                            "case": Case.GENITIVE,
                            "gender": Gender.MASCULINE,
                            "number": GrammaticalNumber.SINGULAR,
                        },
                        {
                            "surface": "purusah",
                            "lemma": "purusa",
                            "case": Case.NOMINATIVE,
                            "gender": Gender.MASCULINE,
                            "number": GrammaticalNumber.SINGULAR,
                        },
                    )
                },
            )
        )
        self.assertEqual(result.surface, "devapurusah")
        self.assertEqual(result.engine, "PaninianDerivationEngine")

    def test_sandhi_synthesis_joins_deva_atra(self) -> None:
        result = synthesize(DerivationIntent.sandhi(left="deva", right="atra"))
        self.assertEqual(result.surface, "devātra")
        self.assertEqual(result.engine, "PaninianDerivationEngine")

    def test_auto_derive_matches_synthesize(self) -> None:
        from sanskript.morphology_synth import auto_derive

        intent = DerivationIntent.subanta(
            lemma="phala",
            case=Case.LOCATIVE,
            number=GrammaticalNumber.SINGULAR,
            gender=Gender.NEUTER,
        )
        self.assertEqual(synthesize(intent).surface, auto_derive(intent).surface)

    def test_recipe_planner_maps_kinds_to_paninian_engine(self) -> None:
        planner = RecipePlanner()
        self.assertEqual(
            planner.plan(
                DerivationIntent.subanta(lemma="phala", case=Case.LOCATIVE, number=GrammaticalNumber.SINGULAR)
            ).engine,
            "PaninianDerivationEngine",
        )
        self.assertEqual(
            planner.plan(
                DerivationIntent.tinanta(lemma="vṛdh", lakara=Lakara.LAT, person=Person.THIRD, number=GrammaticalNumber.SINGULAR)
            ).engine,
            "PaninianDerivationEngine",
        )

    def test_register_intents_cover_prathama_program(self) -> None:
        surfaces = {synthesize(entry.intent).surface for entry in runtime_register_entries()}
        needed = {
            "gaṇakaḥ",
            "pañca",
            "phale",
            "nidadhāti",
            "phalaṃ",
            "dvābhyāṃ",
            "vardhayati",
            "darśayati",
            "ca",
            "eva",
        }
        self.assertTrue(needed <= surfaces)


class ControlledLexiconTests(unittest.TestCase):
    def test_build_lexicon_artifact_contains_prathama_vocabulary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = build_lexicon_artifact(Path(tmp) / "controlled_lexicon.json", entries=runtime_register_entries())
            lexicon = load_controlled_lexicon(path)
            self.assertIn("phale", lexicon)
            self.assertEqual(lexicon["phale"].lemma, "phala")
            self.assertEqual(lexicon["phale"].role, Role.ADHIKARANA)

    def test_facade_loads_artifact_and_parses_program(self) -> None:
        facade = MorphologyFacade()
        analyses = facade.analyze_sentence("gaṇakaḥ pañca phale nidadhāti.")
        self.assertEqual(len(analyses), 4)
        statements = parse_program("gaṇakaḥ pañca phale nidadhāti.")
        self.assertEqual(len(statements), 1)

    def test_checked_in_lexicon_matches_register(self) -> None:
        checked_in = json.loads(DEFAULT_LEXICON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            checked_in["metadata"]["register_digest"],
            register_digest(),
            "register changed; run scripts/build_controlled_lexicon.py",
        )
        self.assertEqual(
            checked_in["metadata"]["recipe_catalog_size"],
            len(register_entries()),
            "checked-in lexicon metadata is stale; run scripts/build_controlled_lexicon.py",
        )

    def test_lexicon_has_no_garbage_surfaces(self) -> None:
        lexicon = load_controlled_lexicon(DEFAULT_LEXICON_PATH)
        for surface in lexicon:
            validate_surface(surface)
        self.assertNotIn("asthiaagamagamagamagamagamagamagamagama", lexicon)
        self.assertGreaterEqual(len(lexicon), 5500, "expanded vocabulary lexicon should be thousands of surfaces")

    def test_lexicon_overrides_merge_on_top_of_synthesis(self) -> None:
        base = {
            "phale": synthesize(
                DerivationIntent.subanta(
                    lemma="phala",
                    case=Case.LOCATIVE,
                    number=GrammaticalNumber.SINGULAR,
                    gender=Gender.NEUTER,
                )
            ).analysis
        }
        override = record_to_analysis(
            LexiconRecord(
                surface="override-token",
                lemma="phala",
                pos="noun",
                case="locative",
                role="adhikaraṇa",
            )
        )
        merged = merge_lexicon_with_overrides(base, {"override-token": override})
        self.assertIn("phale", merged)
        self.assertIn("override-token", merged)
        self.assertEqual(merged["override-token"].lemma, "phala")
        self.assertIsInstance(load_lexicon_overrides(), dict)


if __name__ == "__main__":
    unittest.main()
