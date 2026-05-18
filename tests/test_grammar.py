import unittest

from sanskript.grammar import (
    CONSTRUCTIONS,
    NUMERAL_FORMS,
    VERB_FRAMES,
    Case,
    GrammaticalNumber,
    Lakara,
    Pada,
    Person,
)
from sanskript.morphology import analyze_token, build_lexicon


class GrammarRegisterTests(unittest.TestCase):
    def test_nominal_case_axis_tracks_eight_cases(self) -> None:
        self.assertEqual(
            {case.value for case in Case},
            {
                "nominative",
                "accusative",
                "instrumental",
                "dative",
                "ablative",
                "genitive",
                "locative",
                "vocative",
            },
        )

    def test_every_verb_frame_has_a_registered_construction(self) -> None:
        for frame in VERB_FRAMES.values():
            self.assertIn(frame.construction_id, CONSTRUCTIONS)

    def test_lexicon_is_generated_from_registry(self) -> None:
        lexicon = build_lexicon()

        self.assertEqual(lexicon["mūlye"].lemma, "mūlya")
        self.assertEqual(lexicon["mūlye"].case, Case.LOCATIVE)
        self.assertEqual(lexicon["tribhiḥ"].value, 3)
        self.assertEqual(lexicon["darśayati"].lemma, "dṛś")
        self.assertEqual(lexicon["nyūnayati"].lemma, "nyūnaya")
        self.assertEqual(lexicon["nyūnayati"].lakara, Lakara.LAT)

    def test_current_verb_frames_are_finite_present_third_singular(self) -> None:
        for frame in VERB_FRAMES.values():
            self.assertEqual(frame.lakara, Lakara.LAT)
            self.assertEqual(frame.person, Person.THIRD)
            self.assertEqual(frame.number, GrammaticalNumber.SINGULAR)
            self.assertEqual(frame.pada, Pada.PARASMAIPADA)

    def test_small_numerals_cover_object_and_instrumental_roles(self) -> None:
        by_case = {
            Case.ACCUSATIVE: {form.value for form in NUMERAL_FORMS if form.case == Case.ACCUSATIVE},
            Case.INSTRUMENTAL: {form.value for form in NUMERAL_FORMS if form.case == Case.INSTRUMENTAL},
        }

        self.assertEqual(by_case[Case.ACCUSATIVE], set(range(0, 11)))
        self.assertEqual(by_case[Case.INSTRUMENTAL], set(range(0, 11)))

    def test_iast_forms_survive_utf8_round_trip(self) -> None:
        self.assertEqual(analyze_token("gaṇakaḥ").lemma, "gaṇaka")
        self.assertEqual(analyze_token("dvābhyāṃ").value, 2)
        self.assertEqual(analyze_token("phalaṃ").lemma, "phala")


if __name__ == "__main__":
    unittest.main()
