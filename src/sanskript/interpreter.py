from __future__ import annotations

from .ast import Literal, Program, Reference, Statement, TextLiteral, Value
from .runtime_values import SanskriptValue, to_display_string
from .compiler import compile_program
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
        self._statements: list[Statement] = []

    @property
    def environment(self) -> dict[str, SanskriptValue]:
        return self.vm.environment

    @property
    def output(self) -> list[str]:
        return self.vm.output

    def execute(self, program: Program | list[Statement]) -> list[str]:
        if isinstance(program, Program):
            self._statements = list(program.statements)
        else:
            self._statements = list(program)
        self.vm.execute(compile_program(Program(tuple(self._statements))))
        return self.output

    def execute_statement(self, statement: Statement) -> None:
        self._statements.append(statement)
        self.vm.execute(compile_program(Program(tuple(self._statements))))

    def evaluate(self, value: Value) -> SanskriptValue:
        if isinstance(value, Literal):
            return value.value

        if isinstance(value, TextLiteral):
            return value.value

        if isinstance(value, Reference):
            try:
                return self.environment[value.name]
            except KeyError as exc:
                raise RuntimeSanskriptError(
                    f"Unknown stored value: {value.name!r}",
                    hint="Assign a value with an adhikaraṇa frame before reading it.",
                ) from exc

        raise RuntimeSanskriptError(f"Unknown value: {value!r}")
