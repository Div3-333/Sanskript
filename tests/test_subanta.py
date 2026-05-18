import unittest

from sanskript.grammar import Case, Gender, GrammaticalNumber, PartOfSpeech, Person, Role
from sanskript.karaka import explain_case, role_for_case
from sanskript.morphology import analyze_token
from sanskript.subanta import (
    DeclensionStem,
    StemPattern,
    decline,
    sup_ending,
)


class SubantaTests(unittest.TestCase):
    def test_sup_technical_endings_cover_all_nominal_case_number_slots(self) -> None:
        for case in (
            Case.NOMINATIVE,
            Case.ACCUSATIVE,
            Case.INSTRUMENTAL,
            Case.DATIVE,
            Case.ABLATIVE,
            Case.GENITIVE,
            Case.LOCATIVE,
        ):
            for number in GrammaticalNumber:
                self.assertIsInstance(sup_ending(case, number), str)

    def test_a_masculine_declension(self) -> None:
        forms = decline(DeclensionStem("deva", StemPattern.A_MASCULINE, Gender.MASCULINE, "deity"))

        self.assertEqual(forms[(Case.NOMINATIVE, GrammaticalNumber.SINGULAR)], "devaḥ")
        self.assertEqual(forms[(Case.ACCUSATIVE, GrammaticalNumber.PLURAL)], "devān")
        self.assertEqual(forms[(Case.LOCATIVE, GrammaticalNumber.PLURAL)], "deveṣu")

    def test_a_neuter_declension_integrates_with_lexicon(self) -> None:
        self.assertEqual(analyze_token("phalāni").case, Case.ACCUSATIVE)
        self.assertEqual(analyze_token("phalāni").number, GrammaticalNumber.PLURAL)
        self.assertEqual(analyze_token("phalena").role, Role.KARANA)
        self.assertEqual(analyze_token("phalāt").role, Role.APADANA)

    def test_aa_feminine_declension(self) -> None:
        forms = decline(DeclensionStem("latā", StemPattern.AA_FEMININE, Gender.FEMININE, "creeper"))

        self.assertEqual(forms[(Case.NOMINATIVE, GrammaticalNumber.SINGULAR)], "latā")
        self.assertEqual(forms[(Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR)], "latayā")
        self.assertEqual(forms[(Case.LOCATIVE, GrammaticalNumber.PLURAL)], "latāsu")

    def test_pronouns_enter_morphology_with_person(self) -> None:
        self.assertEqual(analyze_token("aham").pos, PartOfSpeech.PRONOUN)
        self.assertEqual(analyze_token("aham").person, Person.FIRST)
        self.assertEqual(analyze_token("tvam").person, Person.SECOND)
        self.assertEqual(analyze_token("tena").role, Role.KARANA)

    def test_karaka_case_explanations(self) -> None:
        self.assertEqual(role_for_case(Case.DATIVE), Role.SAMPRADANA)
        self.assertEqual(explain_case(Case.ABLATIVE).role, Role.APADANA)
        self.assertIn("module", explain_case(Case.GENITIVE).compiler_use)


if __name__ == "__main__":
    unittest.main()
