import unittest

from sanskript.ast import Display, Reference
from sanskript.errors import MorphologyError, RuntimeSanskriptError
from sanskript.morphology_facade import MorphologyFacade
from sanskript.vm import SanskriptVM
from sanskript.compiler import compile_statements


class ErrorMessageTests(unittest.TestCase):
    def test_morphology_error_carries_code_and_hint(self) -> None:
        with self.assertRaises(MorphologyError) as raised:
            MorphologyFacade().analyze_token("notasanskritform")

        message = str(raised.exception)
        self.assertIn("SANSKRIPT_MORPHOLOGY", message)
        self.assertIn("build_controlled_lexicon", message)

    def test_runtime_error_carries_code_and_hint(self) -> None:
        with self.assertRaises(RuntimeSanskriptError) as raised:
            SanskriptVM().execute(compile_statements([Display(Reference("phala"))]))

        message = str(raised.exception)
        self.assertIn("SANSKRIPT_RUNTIME", message)
        self.assertIn("Assign a value", message)


if __name__ == "__main__":
    unittest.main()
