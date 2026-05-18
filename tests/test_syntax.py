import unittest

from sanskript.morphology import analyze_sentence
from sanskript.syntax import SentenceKind, check_subject_verb_agreement, profile_sentence


class SyntaxTests(unittest.TestCase):
    def test_statement_profile_uses_roles_and_finite_verb(self) -> None:
        profile = profile_sentence(analyze_sentence("gaṇakaḥ pañca phale nidadhāti."))

        self.assertEqual(profile.kind, SentenceKind.STATEMENT)
        self.assertEqual(profile.finite_verbs, ("nidadhāti",))
        self.assertIn("phale", profile.participants)

    def test_question_particle_marks_interrogative_sentence(self) -> None:
        profile = profile_sentence(analyze_sentence("kim gaṇakaḥ phalaṃ darśayati?"))

        self.assertEqual(profile.kind, SentenceKind.QUESTION)
        self.assertIn("kim", profile.particles)

    def test_relative_correlative_pair_marks_relative_sentence(self) -> None:
        profile = profile_sentence(analyze_sentence("yatra phale pañca nidadhāti tatra ca."))

        self.assertEqual(profile.kind, SentenceKind.RELATIVE)
        self.assertIn("yatra", profile.particles)
        self.assertIn("tatra", profile.particles)

    def test_subject_verb_agreement_defaults_nouns_to_third_person(self) -> None:
        agreement = check_subject_verb_agreement(analyze_sentence("gaṇakaḥ pañca phale nidadhāti."))

        self.assertTrue(agreement.agrees)
        self.assertEqual(agreement.subject, "gaṇakaḥ")
        self.assertEqual(agreement.verb, "nidadhāti")


if __name__ == "__main__":
    unittest.main()
