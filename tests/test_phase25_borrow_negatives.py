"""AUTO-GENERATED borrow-checker negative corpus for Phase 25."""

from __future__ import annotations

import unittest

from sanskript.ast import Bind, Literal, Program, Reference
from sanskript.errors import TypeCheckError
from sanskript.type_checker import check_program


def _rakshita(program: Program) -> None:
    check_program(Program(program.statements, safety_tier="rakshita", **{
        k: v for k, v in program.__dict__.items() if k != "statements" and v
    }))


class Phase25BorrowNegativeTests(unittest.TestCase):

    def test_borrow_negative_mutable_reborrow_conflict(self) -> None:
        with self.assertRaises(TypeCheckError):
            check_program(Program(
            (
                Bind("x", Literal(1), ownership="owned"),
                Bind("a", Reference("x"), ownership="borrow_mut"),
                Bind("b", Reference("x"), ownership="borrow_mut"),
            ),
            safety_tier="rakshita",
        ))

    def test_borrow_negative_borrow_requires_named_reference(self) -> None:
        with self.assertRaises(TypeCheckError):
            check_program(Program((Bind("b", Literal(1), ownership="borrow"),), safety_tier="rakshita"))

    def test_borrow_negative_mutable_borrow_conflicts_with_shared(self) -> None:
        with self.assertRaises(TypeCheckError):
            check_program(Program(
            (
                Bind("x", Literal(1), ownership="owned"),
                Bind("a", Reference("x"), ownership="borrow"),
                Bind("b", Reference("x"), ownership="borrow_mut"),
            ),
            safety_tier="rakshita",
        ))

    def test_borrow_negative_cannot_move_borrow_alias(self) -> None:
        with self.assertRaises(TypeCheckError):
            check_program(Program(
            (
                Bind("x", Literal(1), ownership="owned"),
                Bind("b", Reference("x"), ownership="borrow"),
                Bind("m", Reference("b"), ownership="owned"),
            ),
            safety_tier="rakshita",
        ))

    def test_borrow_negative_mutable_borrow_of_immutable_binding(self) -> None:
        with self.assertRaises(TypeCheckError):
            check_program(Program(
            (
                Bind("x", Literal(1), immutable=True, ownership="owned"),
                Bind("b", Reference("x"), ownership="borrow_mut"),
            ),
            safety_tier="rakshita",
        ))


if __name__ == "__main__":
    unittest.main()
