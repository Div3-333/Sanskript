from __future__ import annotations

from .ast import Literal, Reference, Statement, Value
from .compiler import compile_statements
from .errors import RuntimeSanskriptError
from .parser import parse_program
from .vm import SanskriptVM


def run(source: str) -> list[str]:
    interpreter = Interpreter()
    return interpreter.execute(parse_program(source))


class Interpreter:
    def __init__(self) -> None:
        self.vm = SanskriptVM()

    @property
    def environment(self) -> dict[str, int]:
        return self.vm.environment

    @property
    def output(self) -> list[str]:
        return self.vm.output

    def execute(self, statements: list[Statement]) -> list[str]:
        return self.vm.execute(compile_statements(statements))

    def execute_statement(self, statement: Statement) -> None:
        self.execute([statement])

    def evaluate(self, value: Value) -> int:
        if isinstance(value, Literal):
            return value.value

        if isinstance(value, Reference):
            try:
                return self.environment[value.name]
            except KeyError as exc:
                raise RuntimeSanskriptError(f"Unknown stored value: {value.name!r}") from exc

        raise RuntimeSanskriptError(f"Unknown value: {value!r}")
