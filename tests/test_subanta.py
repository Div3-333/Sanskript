import unittest

from sanskript.grammar import Case, Gender, GrammaticalNumber, PartOfSpeech, Person, Role
from sanskript.karaka import explain_case, role_for_case
from sanskript.morphology import analyze_token
from sanskript.subanta import (
    DeclensionStem,
    StemPattern,
    decline,
    infer_stem_pattern,
    sup_ending,
    valid_lemma_for_pattern,
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

    def test_i_masculine_declension(self) -> None:
        forms = decline(DeclensionStem("agni", StemPattern.I_MASCULINE, Gender.MASCULINE, "fire"))
        self.assertEqual(forms[(Case.NOMINATIVE, GrammaticalNumber.SINGULAR)], "agniḥ")
        self.assertEqual(forms[(Case.ACCUSATIVE, GrammaticalNumber.PLURAL)], "agnīn")
        self.assertEqual(forms[(Case.LOCATIVE, GrammaticalNumber.PLURAL)], "agniṣu")

    def test_ii_feminine_declension(self) -> None:
        forms = decline(DeclensionStem("nadī", StemPattern.II_FEMININE, Gender.FEMININE, "river"))
        self.assertEqual(forms[(Case.NOMINATIVE, GrammaticalNumber.SINGULAR)], "nadīḥ")
        self.assertEqual(forms[(Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR)], "nadyā")

    def test_i_feminine_declension(self) -> None:
        forms = decline(DeclensionStem("buddhi", StemPattern.I_FEMININE, Gender.FEMININE, "intellect"))
        self.assertEqual(forms[(Case.NOMINATIVE, GrammaticalNumber.SINGULAR)], "buddhiḥ")
        self.assertEqual(forms[(Case.LOCATIVE, GrammaticalNumber.PLURAL)], "buddhiṣu")

    def test_u_masculine_declension(self) -> None:
        forms = decline(DeclensionStem("guru", StemPattern.U_MASCULINE, Gender.MASCULINE, "teacher"))
        self.assertEqual(forms[(Case.NOMINATIVE, GrammaticalNumber.SINGULAR)], "guruḥ")
        self.assertEqual(forms[(Case.GENITIVE, GrammaticalNumber.PLURAL)], "gurūnām")

    def test_u_neuter_declension(self) -> None:
        forms = decline(DeclensionStem("madhu", StemPattern.U_NEUTER, Gender.NEUTER, "honey"))
        self.assertEqual(forms[(Case.NOMINATIVE, GrammaticalNumber.SINGULAR)], "madhu")
        self.assertEqual(forms[(Case.NOMINATIVE, GrammaticalNumber.PLURAL)], "madhūni")

    def test_uu_feminine_declension(self) -> None:
        forms = decline(DeclensionStem("vadhū", StemPattern.UU_FEMININE, Gender.FEMININE, "bride"))
        self.assertEqual(forms[(Case.NOMINATIVE, GrammaticalNumber.SINGULAR)], "vadhūḥ")
        self.assertEqual(forms[(Case.INSTRUMENTAL, GrammaticalNumber.SINGULAR)], "vadhvā")
        self.assertEqual(forms[(Case.GENITIVE, GrammaticalNumber.PLURAL)], "vadhūnām")

    def test_r_stem_declension(self) -> None:
        forms = decline(DeclensionStem("pitṛ", StemPattern.R_MASCULINE, Gender.MASCULINE, "father"))
        self.assertEqual(forms[(Case.NOMINATIVE, GrammaticalNumber.SINGULAR)], "pitā")
        self.assertEqual(forms[(Case.GENITIVE, GrammaticalNumber.SINGULAR)], "pituḥ")
        self.assertEqual(forms[(Case.LOCATIVE, GrammaticalNumber.SINGULAR)], "pitari")

    def test_infer_stem_pattern_covers_all_vowel_final_classes(self) -> None:
        self.assertEqual(infer_stem_pattern("agni", Gender.MASCULINE), StemPattern.I_MASCULINE)
        self.assertEqual(infer_stem_pattern("buddhi", Gender.FEMININE), StemPattern.I_FEMININE)
        self.assertEqual(infer_stem_pattern("nadī", Gender.FEMININE), StemPattern.II_FEMININE)
        self.assertEqual(infer_stem_pattern("guru", Gender.MASCULINE), StemPattern.U_MASCULINE)
        self.assertEqual(infer_stem_pattern("vadhū", Gender.FEMININE), StemPattern.UU_FEMININE)
        self.assertEqual(infer_stem_pattern("pitṛ", Gender.MASCULINE), StemPattern.R_MASCULINE)
        self.assertEqual(infer_stem_pattern("nīḍṝ", Gender.FEMININE), StemPattern.RR_FEMININE)
        self.assertTrue(valid_lemma_for_pattern("vadhū", StemPattern.UU_FEMININE))

    def test_pronouns_enter_morphology_with_person(self) -> None:
        self.assertEqual(analyze_token("aham").pos, PartOfSpeech.PRONOUN)
        self.assertEqual(analyze_token("aham").person, Person.FIRST)
        self.assertEqual(analyze_token("tvam").person, Person.SECOND)
        self.assertEqual(analyze_token("tena").role, Role.KARANA)

    def test_karaka_case_explanations(self) -> None:
        self.assertEqual(role_for_case(Case.DATIVE), Role.SAMPRADANA)
        self.assertEqual(explain_case(Case.ABLATIVE).role, Role.APADANA)
        self.assertIn("possession", explain_case(Case.GENITIVE).compiler_use)


if __name__ == "__main__":
    unittest.main()
