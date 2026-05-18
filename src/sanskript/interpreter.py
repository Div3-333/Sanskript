from __future__ import annotations

from .ast import Assign, Display, Increase, Literal, Reference, Statement, Value
from .errors import RuntimeSanskriptError
from .parser import parse_program


def run(source: str) -> list[str]:
    interpreter = Interpreter()
    return interpreter.execute(parse_program(source))


class Interpreter:
    def __init__(self) -> None:
        self.environment: dict[str, int] = {}
        self.output: list[str] = []

    def execute(self, statements: list[Statement]) -> list[str]:
        for statement in statements:
            self.execute_statement(statement)
        return self.output

    def execute_statement(self, statement: Statement) -> None:
        if isinstance(statement, Assign):
            self.environment[statement.target] = self.evaluate(statement.value)
            return

        if isinstance(statement, Increase):
            current = self.environment.get(statement.target)
            if current is None:
                raise RuntimeSanskriptError(f"Nothing has been placed in {statement.target!r} yet")
            self.environment[statement.target] = current + self.evaluate(statement.amount)
            return

        if isinstance(statement, Display):
            self.output.append(str(self.evaluate(statement.value)))
            return

        raise RuntimeSanskriptError(f"Unknown statement: {statement!r}")

    def evaluate(self, value: Value) -> int:
        if isinstance(value, Literal):
            return value.value

        if isinstance(value, Reference):
            try:
                return self.environment[value.name]
            except KeyError as exc:
                raise RuntimeSanskriptError(f"Unknown stored value: {value.name!r}") from exc

        raise RuntimeSanskriptError(f"Unknown value: {value!r}")

