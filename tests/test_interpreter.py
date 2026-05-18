import unittest

from sanskript import run
from sanskript.errors import ParseError
from sanskript.parser import parse_program


class InterpreterTests(unittest.TestCase):
    def test_assignment_increment_and_display(self) -> None:
        source = """
        gaṇakaḥ pañca phale nidadhāti.
        gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
        gaṇakaḥ phalaṃ darśayati.
        """

        self.assertEqual(run(source), ["7"])

    def test_word_order_uses_roles_not_positions(self) -> None:
        source = """
        phale gaṇakaḥ pañca nidadhāti.
        dvābhyāṃ phalaṃ gaṇakaḥ vardhayati.
        phalaṃ gaṇakaḥ darśayati.
        """

        self.assertEqual(run(source), ["7"])

    def test_missing_required_role_is_reported(self) -> None:
        with self.assertRaisesRegex(ParseError, "adhikaraṇa"):
            parse_program("gaṇakaḥ pañca nidadhāti.")


if __name__ == "__main__":
    unittest.main()

