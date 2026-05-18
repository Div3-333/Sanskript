import unittest

from sanskript.grammar import GrammaticalNumber, Lakara, Pada, Person
from sanskript.morphology import analyze_token
from sanskript.tinanta import DHATUS, conjugate, tin_ending


class TinantaTests(unittest.TestCase):
    def test_tin_endings_cover_present_command_and_potential_parasmaipada(self) -> None:
        for lakara in (Lakara.LAT, Lakara.LOT, Lakara.VIDHILING):
            for person in Person:
                for number in GrammaticalNumber:
                    self.assertIsInstance(tin_ending(lakara, Pada.PARASMAIPADA, person, number), str)

    def test_present_tense_parasmaipada_forms(self) -> None:
        bhu = next(dhatu for dhatu in DHATUS if dhatu.lemma == "bhū")
        forms = conjugate(bhu, Lakara.LAT)

        self.assertEqual(forms[(Person.THIRD, GrammaticalNumber.SINGULAR)], "bhavati")
        self.assertEqual(forms[(Person.SECOND, GrammaticalNumber.PLURAL)], "bhavatha")
        self.assertEqual(forms[(Person.FIRST, GrammaticalNumber.SINGULAR)], "bhavāmi")

    def test_command_and_potential_forms(self) -> None:
        bhu = next(dhatu for dhatu in DHATUS if dhatu.lemma == "bhū")

        self.assertEqual(conjugate(bhu, Lakara.LOT)[(Person.THIRD, GrammaticalNumber.SINGULAR)], "bhavatu")
        self.assertEqual(conjugate(bhu, Lakara.LOT)[(Person.SECOND, GrammaticalNumber.SINGULAR)], "bhava")
        self.assertEqual(conjugate(bhu, Lakara.VIDHILING)[(Person.THIRD, GrammaticalNumber.SINGULAR)], "bhavet")

    def test_atmanepada_present_forms(self) -> None:
        labh = next(dhatu for dhatu in DHATUS if dhatu.lemma == "labh")
        forms = conjugate(labh, Lakara.LAT)

        self.assertEqual(forms[(Person.THIRD, GrammaticalNumber.SINGULAR)], "labhate")
        self.assertEqual(forms[(Person.FIRST, GrammaticalNumber.SINGULAR)], "labhe")
        self.assertEqual(forms[(Person.FIRST, GrammaticalNumber.PLURAL)], "labhamahe")

    def test_tinanta_forms_enter_morphology(self) -> None:
        self.assertEqual(analyze_token("darśayatu").lakara, Lakara.LOT)
        self.assertEqual(analyze_token("darśayet").lakara, Lakara.VIDHILING)
        self.assertEqual(analyze_token("labhate").pada, Pada.ATMANEPADA)


if __name__ == "__main__":
    unittest.main()
