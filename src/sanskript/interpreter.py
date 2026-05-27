from __future__ import annotations

from .ast import Literal, Program, Reference, Statement, TextLiteral, Value
from .runtime_values import SanskriptValue, to_display_string
from .compiler import compile_program
from .compiler import compile_statements
from .errors import RuntimeSanskriptError
from .parser import parse_program
from .source_pipeline import prepare_source
from .vm import SanskriptVM


def run(source: str) -> list[str]:
    """Execute source after Phase-1 preparation (comments, script normalize, modes)."""
    interpreter = Interpreter()
    return interpreter.execute(interpreter.parse(source))


def parse(source: str) -> Program:
    """Parse after running the full Phase-1 source pipeline."""
    prepared = prepare_source(source)
    return parse_program(prepared.text)


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

    def parse(self, source: str) -> Program:
        prepared = prepare_source(source)
        return parse_program(prepared.text)

    def execute(self, program: Program | list[Statement]) -> list[str]:
        if isinstance(program, Program):
            self._statements = list(program.statements)
            bytecode = compile_program(program)
        else:
            self._statements = list(program)
            bytecode = compile_program(Program(tuple(self._statements)))
        self.vm.execute(bytecode)
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
