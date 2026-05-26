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
_DIGIT_TO_WORD = {value: word for value, word in _INT_TO_WORD.items() if 0 <= value <= 9}
_WORD_TO_DIGIT = {word: value for value, word in _DIGIT_TO_WORD.items()}
_TIER_TO_WORD = {
    "surakshita": "surakṣitaḥ",
    "rakshita": "rakṣitaḥ",
    "arakshita": "arakṣitaḥ",
}
_WORD_TO_TIER = {
    "surakṣitaḥ": "surakshita",
    "surakshitaḥ": "surakshita",
    "rakṣitaḥ": "rakshita",
    "rakshitaḥ": "rakshita",
    "arakṣitaḥ": "arakshita",
    "arakshitaḥ": "arakshita",
}


def program_to_yantra_patha(program: BytecodeProgram) -> str:
    """Render bytecode as canonical Sanskrit-prose machine text."""

    sections: list[str] = ["saṃskaraṇam dvitīyam.", "", "mukhyaḥ pāṭhaḥ ārabhyate."]
    if program.safety_tier != "surakshita":
        sections.append(f"{_TIER_TO_WORD[program.safety_tier]} pāṭhaḥ.")
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
            sections.extend(
                _render_function(
                    FunctionBytecode(display_name, function.instructions, params=function.params)
                )
            )
        sections.append("kṣetram samāpyate.")

    return "\n".join(sections) + "\n"


def program_from_yantra_patha(source: str) -> BytecodeProgram:
    """Parse canonical Sanskrit-prose machine text into bytecode."""

    parser = _YantraPathaParser(source)
    program = parser.parse()
    validate_bytecode(program, version=BYTECODE_VERSION_2)
    return program


def _render_function(function: FunctionBytecode) -> list[str]:
    params = " ".join(function.params)
    header = f"{function.name} {params} iti vidhānam ārabhyate." if params else f"{function.name} iti vidhānam ārabhyate."
    body = [header]
    body.extend(_render_instruction(item) for item in function.instructions)
    body.append("vidhānam samāpyate.")
    return body


def _render_instruction(instruction: Instruction) -> str:
    opcode = instruction.opcode
    operand = instruction.operand

    if opcode == OpCode.PUSH_INT:
        return f"{_format_int(_expect_int(operand, opcode))} iti pūrṇāṅkaḥ nikṣipyate."
    if opcode == OpCode.PUSH_TEXT:
        return f"{_expect_text(operand, opcode)} iti vākyam nikṣipyate."
    if opcode == OpCode.PUSH_BOOL:
        return f"{'satyam' if _expect_bool_operand(operand, opcode) else 'asatyam'} iti satyamūlyam nikṣipyate."
    if opcode == OpCode.PUSH_FLOAT:
        return f"{_format_float(_expect_float(operand, opcode))} iti daśāṃśaḥ nikṣipyate."
    if opcode == OpCode.LIST_NEW:
        return "śūnyaḥ samūhaḥ nirmīyate."
    if opcode == OpCode.LIST_APPEND:
        return "samūhe yojanam kriyate."
    if opcode == OpCode.LIST_LEN:
        return "samūhasya parimāṇam gṛhyate."
    if opcode == OpCode.LIST_GET:
        return "samūhāt aṅkam gṛhyate."
    if opcode == OpCode.MAP_NEW:
        return "śūnyaḥ kośaḥ nirmīyate."
    if opcode == OpCode.MAP_SET:
        return "kośe sthāpanam kriyate."
    if opcode == OpCode.MAP_GET:
        return "kośāt mūlyam gṛhyate."
    if opcode == OpCode.MAP_CONTAINS:
        return "kośe sattā parīkṣyate."
    if opcode == OpCode.RECORD_NEW:
        return "śūnyaṃ vastu nirmīyate."
    if opcode == OpCode.RECORD_SET:
        return "vastuni aṅgasthāpanam kriyate."
    if opcode == OpCode.RECORD_GET:
        return "vastunaḥ aṅgam gṛhyate."
    if opcode == OpCode.RECORD_CONTAINS:
        return "vastuni aṅgasattā parīkṣyate."
    if opcode == OpCode.HEAP_ALLOC:
        return "smṛtau avakāśaḥ kalpyate."
    if opcode == OpCode.HEAP_STORE:
        return "smṛtau sthāpanam kriyate."
    if opcode == OpCode.HEAP_LOAD:
        return "smṛteḥ āharaṇam kriyate."
    if opcode == OpCode.HEAP_FREE:
        return "smṛteḥ mokṣaḥ kriyate."
    if opcode == OpCode.UNSAFE_ENTER:
        return "arakṣitaḥ adhikāraḥ ārabhyate."
    if opcode == OpCode.UNSAFE_EXIT:
        return "arakṣitaḥ adhikāraḥ samāpyate."
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
        self.current_params: tuple[str, ...] = ()
        self.current_module: str | None = None
        self.current_module_functions: list[FunctionBytecode] = []
        self.safety_tier = "surakshita"

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
        return BytecodeProgram(
            tuple(self.main),
            tuple(self.functions),
            tuple(self.modules),
            safety_tier=self.safety_tier,
        )

    def _consume_structure(self, sentence: str) -> bool:
        tokens = sentence.split()
        if tokens in (["saṃskaraṇam", "dvitīyam"], ["saṃskaraṇam", "dvitiyam"]):
            return True
        if tokens == ["mukhyaḥ", "pāṭhaḥ", "ārabhyate"]:
            self.current_stream = self.main
            return True
        if len(tokens) == 2 and tokens[0] in _WORD_TO_TIER and tokens[1] == "pāṭhaḥ":
            self.safety_tier = _WORD_TO_TIER[tokens[0]]
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
        if len(tokens) >= 4 and tokens[-3:] == ["iti", "vidhānam", "ārabhyate"]:
            if self.current_function is not None:
                raise BytecodeValidationError(
                    f"Function {self.current_function!r} was not closed before {tokens[0]!r}"
                )
            self.current_function = tokens[0]
            self.current_params = tuple(tokens[1:-3])
            self.current_stream = []
            return True
        return False

    def _close_function(self) -> None:
        if self.current_function is None or self.current_stream is None:
            raise BytecodeValidationError("vidhānam samāpyate appeared outside a function")
        name = self.current_function
        if self.current_module is not None:
            name = qualified_function_name(self.current_module, name)
        function = FunctionBytecode(name, tuple(self.current_stream), params=self.current_params)
        if self.current_module is None:
            self.functions.append(function)
        else:
            self.current_module_functions.append(function)
        self.current_function = None
        self.current_params = ()
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
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "vākyam", "nikṣipyate"]:
        return Instruction(OpCode.PUSH_TEXT, " ".join(tokens[:-3]))
    if len(tokens) == 4 and tokens[-3:] == ["iti", "satyamūlyam", "nikṣipyate"]:
        if tokens[0] == "satyam":
            return Instruction(OpCode.PUSH_BOOL, 1)
        if tokens[0] == "asatyam":
            return Instruction(OpCode.PUSH_BOOL, 0)
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "daśāṃśaḥ", "nikṣipyate"]:
        return Instruction(OpCode.PUSH_FLOAT, _parse_float(tokens[:-3]))
    if tokens == ["śūnyaḥ", "samūhaḥ", "nirmīyate"]:
        return Instruction(OpCode.LIST_NEW)
    if tokens == ["samūhe", "yojanam", "kriyate"]:
        return Instruction(OpCode.LIST_APPEND)
    if tokens == ["samūhasya", "parimāṇam", "gṛhyate"]:
        return Instruction(OpCode.LIST_LEN)
    if tokens == ["samūhāt", "aṅkam", "gṛhyate"]:
        return Instruction(OpCode.LIST_GET)
    if tokens == ["śūnyaḥ", "kośaḥ", "nirmīyate"]:
        return Instruction(OpCode.MAP_NEW)
    if tokens == ["kośe", "sthāpanam", "kriyate"]:
        return Instruction(OpCode.MAP_SET)
    if tokens == ["kośāt", "mūlyam", "gṛhyate"]:
        return Instruction(OpCode.MAP_GET)
    if tokens == ["kośe", "sattā", "parīkṣyate"]:
        return Instruction(OpCode.MAP_CONTAINS)
    if tokens == ["śūnyaṃ", "vastu", "nirmīyate"]:
        return Instruction(OpCode.RECORD_NEW)
    if tokens == ["vastuni", "aṅgasthāpanam", "kriyate"]:
        return Instruction(OpCode.RECORD_SET)
    if tokens == ["vastunaḥ", "aṅgam", "gṛhyate"]:
        return Instruction(OpCode.RECORD_GET)
    if tokens == ["vastuni", "aṅgasattā", "parīkṣyate"]:
        return Instruction(OpCode.RECORD_CONTAINS)
    if tokens == ["smṛtau", "avakāśaḥ", "kalpyate"]:
        return Instruction(OpCode.HEAP_ALLOC)
    if tokens == ["smṛtau", "sthāpanam", "kriyate"]:
        return Instruction(OpCode.HEAP_STORE)
    if tokens == ["smṛteḥ", "āharaṇam", "kriyate"]:
        return Instruction(OpCode.HEAP_LOAD)
    if tokens == ["smṛteḥ", "mokṣaḥ", "kriyate"]:
        return Instruction(OpCode.HEAP_FREE)
    if tokens == ["arakṣitaḥ", "adhikāraḥ", "ārabhyate"]:
        return Instruction(OpCode.UNSAFE_ENTER)
    if tokens == ["arakṣitaḥ", "adhikāraḥ", "samāpyate"]:
        return Instruction(OpCode.UNSAFE_EXIT)
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


def _format_float(value: float) -> str:
    sign = "ṛṇa " if value < 0 else ""
    absolute = abs(value)
    text = format(absolute, ".12f").rstrip("0").rstrip(".")
    if "." not in text:
        text = f"{text}.0"
    whole_text, fractional_text = text.split(".", 1)
    whole = _format_int(int(whole_text))
    fractional = " ".join(_DIGIT_TO_WORD[int(item)] for item in fractional_text)
    return f"{sign}{whole} bindu {fractional}"


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


def _parse_float(tokens: list[str]) -> float:
    if "bindu" not in tokens:
        return float(_parse_int(tokens))
    split_at = tokens.index("bindu")
    whole_tokens = tokens[:split_at]
    fractional_tokens = tokens[split_at + 1 :]
    if not whole_tokens or not fractional_tokens:
        raise BytecodeValidationError("Expected a Sanskrit decimal phrase")
    negative = whole_tokens[0] == "ṛṇa"
    if negative:
        whole_tokens = whole_tokens[1:]
    whole = _parse_int(whole_tokens)
    digits = "".join(str(_parse_digit(item)) for item in fractional_tokens)
    value = float(f"{whole}.{digits}")
    return -value if negative else value


def _parse_digit(token: str) -> int:
    if token in _WORD_TO_DIGIT:
        return _WORD_TO_DIGIT[token]
    if re.fullmatch(r"\d", token):
        return int(token)
    raise BytecodeValidationError(f"Expected a single decimal digit, got {token!r}")


def _module_function_display_name(module_name: str, function_name: str) -> str:
    prefix = f"{module_name}."
    if function_name.startswith(prefix):
        return function_name[len(prefix) :]
    return function_name


def _expect_int(operand: object, opcode: OpCode) -> int:
    if not isinstance(operand, int) or isinstance(operand, bool):
        raise BytecodeValidationError(f"{opcode.value} expected an integer operand")
    return operand


def _expect_bool_operand(operand: object, opcode: OpCode) -> bool:
    value = _expect_int(operand, opcode)
    if value not in {0, 1}:
        raise BytecodeValidationError(f"{opcode.value} expected 0 or 1")
    return bool(value)


def _expect_float(operand: object, opcode: OpCode) -> float:
    if not isinstance(operand, (int, float)) or isinstance(operand, bool):
        raise BytecodeValidationError(f"{opcode.value} expected a numeric operand")
    return float(operand)


def _expect_name(operand: object, opcode: OpCode) -> str:
    if not isinstance(operand, str) or not operand:
        raise BytecodeValidationError(f"{opcode.value} expected a name operand")
    return operand


def _expect_text(operand: object, opcode: OpCode) -> str:
    if not isinstance(operand, str):
        raise BytecodeValidationError(f"{opcode.value} expected a text operand")
    return operand


__all__ = ["program_from_yantra_patha", "program_to_yantra_patha"]
