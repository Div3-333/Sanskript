from __future__ import annotations

import re

from .bytecode import (
    BYTECODE_VERSION_2,
    BytecodeProgram,
    BytecodeValidationError,
    FunctionBytecode,
    Instruction,
    ModuleBytecode,
    OpCode,
    qualified_function_name,
    validate_bytecode,
)


_INT_TO_WORD = {
    0: "śūnya",
    1: "eka",
    2: "dvi",
    3: "tri",
    4: "catur",
    5: "pañca",
    6: "ṣaṭ",
    7: "sapta",
    8: "aṣṭa",
    9: "nava",
    10: "daśa",
    11: "ekādaśa",
    12: "dvādaśa",
    13: "trayodaśa",
    14: "caturdaśa",
    15: "pañcadaśa",
    16: "ṣoḍaśa",
    17: "saptadaśa",
    18: "aṣṭādaśa",
    19: "navadaśa",
    20: "viṃśati",
}
_WORD_TO_INT = {word: value for value, word in _INT_TO_WORD.items()}
_WORD_TO_INT.update({"dvitīya": 2, "dvitiyam": 2, "dvitīyam": 2})


def program_to_yantra_patha(program: BytecodeProgram) -> str:
    """Render bytecode as canonical Sanskrit-prose machine text."""

    sections: list[str] = ["saṃskaraṇam dvitīyam.", "", "mukhyaḥ pāṭhaḥ ārabhyate."]
    sections.extend(_render_instruction(item) for item in program.instructions)
    sections.append("pāṭhaḥ samāpyate.")

    for function in program.functions:
        sections.append("")
        sections.extend(_render_function(function))

    for module in program.modules:
        sections.append("")
        sections.append(f"{module.name} iti kṣetram ārabhyate.")
        for function in module.functions:
            display_name = _module_function_display_name(module.name, function.name)
            sections.extend(_render_function(FunctionBytecode(display_name, function.instructions)))
        sections.append("kṣetram samāpyate.")

    return "\n".join(sections) + "\n"


def program_from_yantra_patha(source: str) -> BytecodeProgram:
    """Parse canonical Sanskrit-prose machine text into bytecode."""

    parser = _YantraPathaParser(source)
    program = parser.parse()
    validate_bytecode(program, version=BYTECODE_VERSION_2)
    return program


def _render_function(function: FunctionBytecode) -> list[str]:
    body = [f"{function.name} iti vidhānam ārabhyate."]
    body.extend(_render_instruction(item) for item in function.instructions)
    body.append("vidhānam samāpyate.")
    return body


def _render_instruction(instruction: Instruction) -> str:
    opcode = instruction.opcode
    operand = instruction.operand

    if opcode == OpCode.PUSH_INT:
        return f"{_format_int(_expect_int(operand, opcode))} iti pūrṇāṅkaḥ nikṣipyate."
    if opcode == OpCode.LOAD_NAME:
        return f"{_expect_name(operand, opcode)} iti nāma āhriyate."
    if opcode == OpCode.STORE_NAME:
        return f"{_expect_name(operand, opcode)} iti nāma sthāpyate."
    if opcode == OpCode.ADD:
        return "yogaḥ kriyate."
    if opcode == OpCode.SUBTRACT:
        return "vyavakalanam kriyate."
    if opcode == OpCode.MULTIPLY:
        return "guṇanam kriyate."
    if opcode == OpCode.DIVIDE:
        return "bhāgaḥ kriyate."
    if opcode == OpCode.COMPARE_EQ:
        return "sāmyam parīkṣyate."
    if opcode == OpCode.COMPARE_LT:
        return "nyūnatvam parīkṣyate."
    if opcode == OpCode.EMIT:
        return "darśanam kriyate."
    if opcode == OpCode.JUMP:
        return f"{_format_int(_expect_int(operand, opcode))} iti lakṣyaṃ gamyate."
    if opcode == OpCode.JUMP_IF_ZERO:
        return f"śūnye sati {_format_int(_expect_int(operand, opcode))} iti lakṣyaṃ gamyate."
    if opcode == OpCode.CALL:
        target = _expect_name(operand, opcode)
        if "." in target:
            module_name, function_name = target.split(".", 1)
            return f"{module_name} iti kṣetre {function_name} iti vidhānam āhūyate."
        return f"{target} iti vidhānam āhūyate."
    if opcode == OpCode.RETURN:
        return "pratyāvartanam kriyate."
    if opcode == OpCode.POP:
        return "tyāgaḥ kriyate."
    if opcode == OpCode.HALT:
        return "virāmaḥ kriyate."

    raise BytecodeValidationError(f"Cannot render unknown opcode {opcode!r}")


class _YantraPathaParser:
    def __init__(self, source: str) -> None:
        self.sentences = _split_sentences(source)
        self.main: list[Instruction] = []
        self.functions: list[FunctionBytecode] = []
        self.modules: list[ModuleBytecode] = []
        self.current_stream: list[Instruction] | None = None
        self.current_function: str | None = None
        self.current_module: str | None = None
        self.current_module_functions: list[FunctionBytecode] = []

    def parse(self) -> BytecodeProgram:
        for sentence in self.sentences:
            if self._consume_structure(sentence):
                continue
            instruction = _parse_instruction(sentence)
            if self.current_stream is None:
                self.main.append(instruction)
            else:
                self.current_stream.append(instruction)

        if self.current_function is not None:
            raise BytecodeValidationError(f"Function {self.current_function!r} was not closed")
        if self.current_module is not None:
            self._close_module()
        return BytecodeProgram(tuple(self.main), tuple(self.functions), tuple(self.modules))

    def _consume_structure(self, sentence: str) -> bool:
        tokens = sentence.split()
        if tokens in (["saṃskaraṇam", "dvitīyam"], ["saṃskaraṇam", "dvitiyam"]):
            return True
        if tokens == ["mukhyaḥ", "pāṭhaḥ", "ārabhyate"]:
            self.current_stream = self.main
            return True
        if tokens == ["pāṭhaḥ", "samāpyate"]:
            self.current_stream = None
            return True
        if tokens == ["kṣetram", "samāpyate"]:
            self._close_module()
            return True
        if len(tokens) == 4 and tokens[1:] == ["iti", "kṣetram", "ārabhyate"]:
            if self.current_module is not None:
                self._close_module()
            self.current_module = tokens[0]
            self.current_module_functions = []
            return True
        if tokens == ["vidhānam", "samāpyate"]:
            self._close_function()
            return True
        if len(tokens) == 4 and tokens[1:] == ["iti", "vidhānam", "ārabhyate"]:
            if self.current_function is not None:
                raise BytecodeValidationError(
                    f"Function {self.current_function!r} was not closed before {tokens[0]!r}"
                )
            self.current_function = tokens[0]
            self.current_stream = []
            return True
        return False

    def _close_function(self) -> None:
        if self.current_function is None or self.current_stream is None:
            raise BytecodeValidationError("vidhānam samāpyate appeared outside a function")
        name = self.current_function
        if self.current_module is not None:
            name = qualified_function_name(self.current_module, name)
        function = FunctionBytecode(name, tuple(self.current_stream))
        if self.current_module is None:
            self.functions.append(function)
        else:
            self.current_module_functions.append(function)
        self.current_function = None
        self.current_stream = None

    def _close_module(self) -> None:
        if self.current_function is not None:
            raise BytecodeValidationError(
                f"Function {self.current_function!r} must close before its module closes"
            )
        if self.current_module is None:
            raise BytecodeValidationError("kṣetram samāpyate appeared outside a module")
        self.modules.append(ModuleBytecode(self.current_module, tuple(self.current_module_functions)))
        self.current_module = None
        self.current_module_functions = []


def _parse_instruction(sentence: str) -> Instruction:
    tokens = sentence.split()
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "pūrṇāṅkaḥ", "nikṣipyate"]:
        return Instruction(OpCode.PUSH_INT, _parse_int(tokens[:-3]))
    if len(tokens) == 4 and tokens[1:] == ["iti", "nāma", "āhriyate"]:
        return Instruction(OpCode.LOAD_NAME, tokens[0])
    if len(tokens) == 4 and tokens[1:] == ["iti", "nāma", "sthāpyate"]:
        return Instruction(OpCode.STORE_NAME, tokens[0])
    if tokens == ["yogaḥ", "kriyate"]:
        return Instruction(OpCode.ADD)
    if tokens == ["vyavakalanam", "kriyate"]:
        return Instruction(OpCode.SUBTRACT)
    if tokens == ["guṇanam", "kriyate"]:
        return Instruction(OpCode.MULTIPLY)
    if tokens == ["bhāgaḥ", "kriyate"]:
        return Instruction(OpCode.DIVIDE)
    if tokens == ["sāmyam", "parīkṣyate"]:
        return Instruction(OpCode.COMPARE_EQ)
    if tokens == ["nyūnatvam", "parīkṣyate"]:
        return Instruction(OpCode.COMPARE_LT)
    if tokens == ["darśanam", "kriyate"]:
        return Instruction(OpCode.EMIT)
    if len(tokens) >= 6 and tokens[:2] == ["śūnye", "sati"] and tokens[-3:] == [
        "iti",
        "lakṣyaṃ",
        "gamyate",
    ]:
        return Instruction(OpCode.JUMP_IF_ZERO, _parse_int(tokens[2:-3]))
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "lakṣyaṃ", "gamyate"]:
        return Instruction(OpCode.JUMP, _parse_int(tokens[:-3]))
    if len(tokens) == 4 and tokens[1:] == ["iti", "vidhānam", "āhūyate"]:
        return Instruction(OpCode.CALL, tokens[0])
    if len(tokens) == 7 and tokens[1:3] == ["iti", "kṣetre"] and tokens[4:] == [
        "iti",
        "vidhānam",
        "āhūyate",
    ]:
        return Instruction(OpCode.CALL, qualified_function_name(tokens[0], tokens[3]))
    if tokens == ["pratyāvartanam", "kriyate"]:
        return Instruction(OpCode.RETURN)
    if tokens == ["tyāgaḥ", "kriyate"]:
        return Instruction(OpCode.POP)
    if tokens == ["virāmaḥ", "kriyate"]:
        return Instruction(OpCode.HALT)
    raise BytecodeValidationError(f"Unknown yantra-pāṭha sentence: {sentence!r}")


def _split_sentences(source: str) -> list[str]:
    return [
        sentence.strip()
        for sentence in re.split(r"[.।]\s*", source)
        if sentence.strip()
    ]


def _format_int(value: int) -> str:
    if value < 0:
        return f"ṛṇa {_format_int(-value)}"
    return _INT_TO_WORD.get(value, str(value))


def _parse_int(tokens: list[str]) -> int:
    if not tokens:
        raise BytecodeValidationError("Expected a Sanskrit integer phrase")
    if tokens[0] == "ṛṇa":
        return -_parse_int(tokens[1:])
    if len(tokens) == 1:
        token = tokens[0]
        if token in _WORD_TO_INT:
            return _WORD_TO_INT[token]
        try:
            return int(token)
        except ValueError as exc:
            raise BytecodeValidationError(f"Unknown Sanskrit integer phrase: {' '.join(tokens)!r}") from exc
    raise BytecodeValidationError(f"Unknown Sanskrit integer phrase: {' '.join(tokens)!r}")


def _module_function_display_name(module_name: str, function_name: str) -> str:
    prefix = f"{module_name}."
    if function_name.startswith(prefix):
        return function_name[len(prefix) :]
    return function_name


def _expect_int(operand: object, opcode: OpCode) -> int:
    if not isinstance(operand, int) or isinstance(operand, bool):
        raise BytecodeValidationError(f"{opcode.value} expected an integer operand")
    return operand


def _expect_name(operand: object, opcode: OpCode) -> str:
    if not isinstance(operand, str) or not operand:
        raise BytecodeValidationError(f"{opcode.value} expected a name operand")
    return operand


__all__ = ["program_from_yantra_patha", "program_to_yantra_patha"]
