import unittest

from sanskript.samasa import COMPOUND_EXAMPLES, SamasaType, classify_compound, examples_for


class SamasaTests(unittest.TestCase):
    def test_all_major_compound_types_have_examples(self) -> None:
        self.assertEqual(
            {example.samasa_type for example in COMPOUND_EXAMPLES},
            {SamasaType.AVYAYIBHAVA, SamasaType.TATPURUSHA, SamasaType.BAHUVRIHI, SamasaType.DVANDVA},
        )

    def test_compound_classification_uses_controlled_registry(self) -> None:
        self.assertEqual(classify_compound("upagrāmam"), SamasaType.AVYAYIBHAVA)
        self.assertEqual(classify_compound("rājapuruṣaḥ"), SamasaType.TATPURUSHA)
        self.assertEqual(classify_compound("pītāmbaraḥ"), SamasaType.BAHUVRIHI)
        self.assertEqual(classify_compound("rāmalakṣmaṇau"), SamasaType.DVANDVA)

    def test_examples_for_compound_type(self) -> None:
        self.assertEqual(examples_for(SamasaType.DVANDVA)[0].members, ("rāmaḥ", "lakṣmaṇaḥ"))


if __name__ == "__main__":
    unittest.main()
