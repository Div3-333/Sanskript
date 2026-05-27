import unittest

from sanskript.avyaya import AVYAYA_FORMS, avyaya_for, iter_avyaya_analyses, upasarga_surfaces
from sanskript.grammar import IndeclinableKind, PartOfSpeech


class AvyayaTests(unittest.TestCase):
    def test_core_particles_are_registered_by_kind(self) -> None:
        self.assertEqual(avyaya_for("ca").kind, IndeclinableKind.CONJUNCTION)
        self.assertEqual(avyaya_for("vā").kind, IndeclinableKind.ALTERNATIVE)
        self.assertEqual(avyaya_for("kim").kind, IndeclinableKind.QUESTION)
        self.assertEqual(avyaya_for("yatra").kind, IndeclinableKind.RELATIVE)

    def test_upasarga_registry_covers_standard_prefixes(self) -> None:
        prefixes = upasarga_surfaces()

        for surface in ("pra", "sam", "anu", "vi", "ā", "upa", "prati"):
            self.assertIn(surface, prefixes)
        self.assertGreaterEqual(len(prefixes), 18)

    def test_avyaya_forms_enter_morphology_as_indeclinables(self) -> None:
        analyses = {analysis.surface: analysis for analysis in iter_avyaya_analyses()}

        self.assertEqual(analyses["ca"].pos, PartOfSpeech.INDECLINABLE)
        self.assertEqual(analyses["na"].indeclinable_kind, IndeclinableKind.NEGATION)
        self.assertGreater(len(analyses), len(AVYAYA_FORMS))

    def test_example_identifiers_are_not_registered_as_avyaya(self) -> None:
        surfaces = {form.surface for form in AVYAYA_FORMS}

        for surface in ("a", "x", "n", "greet", "counter", "trace", "namaste", "surakṣitam"):
            with self.subTest(surface=surface):
                self.assertNotIn(surface, surfaces)
                with self.assertRaises(ValueError):
                    avyaya_for(surface)


if __name__ == "__main__":
    unittest.main()
