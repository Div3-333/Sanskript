import unittest

from sanskript.ast import Assign, Decrease, Display, Increase, Literal, Reference
from sanskript.grammar import CONSTRUCTIONS, VERB_FRAMES, FrameOperation, Role
from sanskript.parser import parse_sentence


class FrameRegistryTests(unittest.TestCase):
    def test_controlled_frames_are_loaded_from_registry_data(self) -> None:
        self.assertGreaterEqual(len(VERB_FRAMES), 8)
        for frame in VERB_FRAMES.values():
            self.assertIn(frame.construction_id, CONSTRUCTIONS)
            self.assertTrue(frame.required_roles)

    def test_every_frame_operation_has_role_bindings(self) -> None:
        for frame in VERB_FRAMES.values():
            if frame.operation == FrameOperation.ASSIGN:
                self.assertEqual(frame.target_role, Role.ADHIKARANA)
                self.assertEqual(frame.value_role, Role.KARMAN)
            elif frame.operation in {FrameOperation.INCREASE, FrameOperation.DECREASE}:
                self.assertEqual(frame.target_role, Role.KARMAN)
                self.assertEqual(frame.amount_role, Role.KARANA)
            elif frame.operation == FrameOperation.DISPLAY:
                self.assertEqual(frame.value_role, Role.KARMAN)
            else:  # pragma: no cover - enum exhaustiveness guard
                self.fail(f"Unhandled frame operation {frame.operation}")

    def test_assignment_synonym_uses_same_ast_constructor(self) -> None:
        self.assertEqual(
            parse_sentence("gaṇakaḥ pañca phale sthāpayati."),
            Assign(target="phala", value=Literal(5)),
        )

    def test_increase_synonym_uses_same_ast_constructor(self) -> None:
        self.assertEqual(
            parse_sentence("gaṇakaḥ phalaṃ dvābhyāṃ yojayati."),
            Increase(target="phala", amount=Literal(2)),
        )

    def test_decrease_synonym_uses_same_ast_constructor(self) -> None:
        self.assertEqual(
            parse_sentence("gaṇakaḥ phalaṃ tribhiḥ vyavakalayati."),
            Decrease(target="phala", amount=Literal(3)),
        )

    def test_display_synonym_uses_same_ast_constructor(self) -> None:
        self.assertEqual(
            parse_sentence("gaṇakaḥ phalaṃ prakāśayati."),
            Display(value=Reference("phala")),
        )


if __name__ == "__main__":
    unittest.main()
