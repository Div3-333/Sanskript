import unittest

from sanskript.anga import apply_anga_operation, guna, operation_named, operations_for_range, vrddhi


class AngaTests(unittest.TestCase):
    def test_guna_and_vrddhi_replacements_are_controlled(self) -> None:
        self.assertEqual(guna("i"), "e")
        self.assertEqual(guna("ṛ"), "ar")
        self.assertEqual(vrddhi("u"), "au")

    def test_operations_are_indexed_by_remaining_sutra_ranges(self) -> None:
        for sutra_range in ("6.2", "6.3", "6.4", "7.1", "7.2", "7.3", "7.4"):
            self.assertGreaterEqual(len(operations_for_range(sutra_range)), 1)

    def test_apply_final_lengthening_and_retroflexion(self) -> None:
        self.assertEqual(apply_anga_operation("deva", operation_named("final-a-lengthening")), "devā")
        self.assertEqual(apply_anga_operation("nayana", operation_named("ṇati-retroflexion")), "ṇayana")


if __name__ == "__main__":
    unittest.main()
