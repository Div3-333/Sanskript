import unittest

from sanskript.derivation import (
    DerivationFamily,
    KrtSuffix,
    TaddhitaSuffix,
    derive,
    derive_taddhita,
    forms_by_family,
)


class DerivationTests(unittest.TestCase):
    def test_krt_registry_covers_major_suffix_families(self) -> None:
        suffixes = {form.suffix for form in forms_by_family(DerivationFamily.KRT)}

        self.assertTrue(
            {
                KrtSuffix.KTVA,
                KrtSuffix.TUMUN,
                KrtSuffix.KTA,
                KrtSuffix.TAVYA,
                KrtSuffix.ANIYA,
                KrtSuffix.SHATR,
                KrtSuffix.SHANAC,
                KrtSuffix.GHAN,
            }.issubset(suffixes)
        )

    def test_known_krt_forms_are_retrievable(self) -> None:
        self.assertEqual(derive("bhū", KrtSuffix.KTVA).surface, "bhūtvā")
        self.assertEqual(derive("dṛś", KrtSuffix.TUMUN).surface, "draṣṭum")
        self.assertEqual(derive("labh", KrtSuffix.SHANAC).surface, "labhamāna")

    def test_taddhita_registry_covers_current_topics(self) -> None:
        suffixes = {form.suffix for form in forms_by_family(DerivationFamily.TADDHITA)}

        self.assertEqual(suffixes, {TaddhitaSuffix.APATYA, TaddhitaSuffix.MATUP, TaddhitaSuffix.ATISHAYANA})
        self.assertEqual(derive("bala", TaddhitaSuffix.MATUP).surface, "balavān")

    def test_taddhita_engine_derives_rule_level_forms(self) -> None:
        apatya = derive_taddhita("manu", sutra_id="4.1.92")
        matup = derive_taddhita("bala", sutra_id="5.2.94")
        degree = derive_taddhita("guru", sutra_id="5.3.55")

        self.assertEqual((apatya.surface, apatya.semantic), ("mānava", "apatya"))
        self.assertEqual(apatya.operations, ("initial-vrddhi", "final-u-to-ava"))
        self.assertEqual((matup.surface, matup.semantic), ("balavān", "possession"))
        self.assertEqual(matup.operations, ("matup-realized-as-vān",))
        self.assertEqual((degree.surface, degree.semantic), ("gariṣṭha", "atishayana"))


if __name__ == "__main__":
    unittest.main()
