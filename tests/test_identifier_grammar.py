import unittest

from sanskript.errors import ParseError
from sanskript.identifiers import IdentifierError, canonical_identifier, is_identifier
from sanskript.morphology_facade import get_default_facade
from sanskript.parser import parse_program


class IdentifierGrammarTests(unittest.TestCase):
    def test_inflected_nominal_identifier_canonicalizes_to_lemma(self) -> None:
        self.assertEqual(canonical_identifier("phalaṃ", facade=get_default_facade()), "phala")
        self.assertEqual(canonical_identifier("ekam", facade=get_default_facade()), "ekam")

    def test_sanskrit_compounds_and_qualified_names_are_surface_valid(self) -> None:
        self.assertEqual(canonical_identifier("gaṇita-phala"), "gaṇita-phala")
        self.assertTrue(is_identifier("std.gaṇita"))
        self.assertTrue(is_identifier("dīpakaḥ__init__"))

    def test_literals_and_operator_punctuation_are_not_identifiers(self) -> None:
        for token in ("1", "1phala", "phala+eka", "phala=", ".phala", "phala.", "phala-"):
            with self.subTest(token=token):
                with self.assertRaises(IdentifierError):
                    canonical_identifier(token)

    def test_parser_uses_identifier_grammar_without_avyaya_pollution(self) -> None:
        program = parse_program(
            """
            vidhānam dviguṇa mūlya.
            pratyāvartanam mūlya yoga mūlya.
            samāpanam.
            """
        )

        self.assertEqual(program.functions[0].name, "dviguṇa")
        self.assertEqual(program.functions[0].params, ("mūlya",))

    def test_invalid_identifier_in_directive_is_parse_error(self) -> None:
        with self.assertRaises(ParseError):
            parse_program("gaṇitam 1phala eka.")


if __name__ == "__main__":
    unittest.main()
