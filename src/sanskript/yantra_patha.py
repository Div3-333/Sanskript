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
from .fixed_width import (
    SPEC_BY_ADD_CHECKED,
    SPEC_BY_ADD_SATURATING,
    SPEC_BY_ADD_WRAPPING,
    SPEC_BY_PUSH_OPCODE,
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
_WORD_TO_INT.setdefault("śūnyam", 0)
_WORD_TO_INT.setdefault("shunyam", 0)
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

_PHASE3_RENDER_SENTENCES: dict[OpCode, str] = {
    OpCode("i32_add_wrapping"): "saṅkhyā-lagvoḥ yogaḥ parivṛttaḥ kriyate.",
    OpCode("u32_add_wrapping"): "saṅkhyā-nirṇāśayoḥ yogaḥ parivṛttaḥ kriyate.",
    OpCode("i32_add_saturating"): "saṅkhyā-lagvoḥ yogaḥ sīmitaḥ kriyate.",
    OpCode("u32_add_saturating"): "saṅkhyā-nirṇāśayoḥ yogaḥ sīmitaḥ kriyate.",
    OpCode("push_rational"): "rāśi-saṅkhyā nirmīyate.",
    OpCode("rational_add"): "rāśi-saṅkhyayoḥ yogaḥ kriyate.",
    OpCode("push_decimal"): "daśāṃśa-saṅkhyā nikṣipyate.",
    OpCode("decimal_add"): "daśāṃśa-saṅkhyayoḥ yogaḥ kriyate.",
    OpCode("push_complex"): "saṅkīrṇa-saṅkhyā nikṣipyate.",
    OpCode("complex_add"): "saṅkīrṇa-saṅkhyayoḥ yogaḥ kriyate.",
    OpCode("push_scalar"): "akṣara-bījam nikṣipyate.",
    OpCode("text_scalar_at"): "vākyāt akṣara-bījam gṛhyate.",
    OpCode("frozen_set_new"): "nityaḥ samāhāraḥ nirmīyate.",
    OpCode("frozen_set_add"): "nitya-samāhāre yojanam kriyate.",
    OpCode("frozen_set_len"): "nitya-samāhārasya parimāṇam gṛhyate.",
    OpCode("ordered_map_new"): "krama-kośaḥ nirmīyate.",
    OpCode("ordered_map_set"): "krama-kośe sthāpanam kriyate.",
    OpCode("ordered_map_get"): "krama-kośāt mūlyam gṛhyate.",
    OpCode("default_map_new"): "svataḥ-kośaḥ nirmīyate.",
    OpCode("default_map_set"): "svataḥ-kośe sthāpanam kriyate.",
    OpCode("default_map_get"): "svataḥ-kośāt mūlyam gṛhyate.",
    OpCode("counter_new"): "gaṇanā-sañcayaḥ nirmīyate.",
    OpCode("counter_add"): "gaṇanā-sañcaye vardhanam kriyate.",
    OpCode("counter_get"): "gaṇanā-sañcayāt mūlyam gṛhyate.",
    OpCode("queue_new"): "panktī nirmīyate.",
    OpCode("queue_enqueue"): "panktyām praveśaḥ kriyate.",
    OpCode("queue_dequeue"): "panktyāḥ niṣkramaḥ kriyate.",
    OpCode("stack_new"): "stūpaḥ nirmīyate.",
    OpCode("stack_push"): "stūpe yojanam kriyate.",
    OpCode("stack_pop"): "stūpāt aṅkam gṛhyate.",
    OpCode("heap_new"): "nyūna-śikharaḥ nirmīyate.",
    OpCode("heap_push"): "nyūna-śikhare yojanam kriyate.",
    OpCode("heap_pop"): "nyūna-śikharāt aṅkam gṛhyate.",
    OpCode("pq_new"): "prādhānya-panktī nirmīyate.",
    OpCode("pq_push"): "prādhānya-panktyām yojanam kriyate.",
    OpCode("pq_pop"): "prādhānya-panktyāḥ aṅkam gṛhyate.",
    OpCode("tree_new"): "vṛkṣaḥ nirmīyate.",
    OpCode("tree_insert"): "vṛkṣe niveśaḥ kriyate.",
    OpCode("tree_contains"): "vṛkṣe sattā parīkṣyate.",
    OpCode("graph_new"): "jālakaḥ nirmīyate.",
    OpCode("graph_add_edge"): "jālake sandhiḥ yujyate.",
    OpCode("graph_has_edge"): "jālake sandhi-sattā parīkṣyate.",
    OpCode("enum_new"): "gaṇavikalpaḥ nirmīyate.",
    OpCode("tagged_union_new"): "cihna-saṅghaṭaḥ nirmīyate.",
    OpCode("tagged_union_tag"): "cihna-saṅghaṭāt cihnam gṛhyate.",
    OpCode("tagged_union_payload"): "cihna-saṅghaṭāt mūlyam gṛhyate.",
    OpCode("typed_error_new"): "lakṣita-doṣaḥ nirmīyate.",
    OpCode("named_tuple_new"): "nāma-yuktiḥ nirmīyate.",
    OpCode("named_tuple_get"): "nāma-yuktau aṅkam gṛhyate.",
    OpCode("handle_new"): "sambandha-hastaḥ nirmīyate.",
}

_PHASE3_PARSE_SENTENCES: dict[tuple[str, ...], OpCode] = {
    tuple(sentence.rstrip(".").split()): opcode for opcode, sentence in _PHASE3_RENDER_SENTENCES.items()
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
    if opcode == OpCode.TEXT_CONCAT:
        return "vākyayoḥ saṃyogaḥ kriyate."
    if opcode == OpCode.TEXT_LEN:
        return "vākyasya parimāṇam gṛhyate."
    if opcode == OpCode.TEXT_GET:
        return "vākyāt aṅkam gṛhyate."
    if opcode == OpCode.TEXT_SLICE:
        return "vākyasya chedaḥ kriyate."
    if opcode == OpCode.TEXT_CONTAINS:
        return "vākye sattā parīkṣyate."
    if opcode == OpCode.LIST_NEW:
        return "śūnyaḥ samūhaḥ nirmīyate."
    if opcode == OpCode.LIST_APPEND:
        return "samūhe yojanam kriyate."
    if opcode == OpCode.LIST_LEN:
        return "samūhasya parimāṇam gṛhyate."
    if opcode == OpCode.LIST_GET:
        return "samūhāt aṅkam gṛhyate."
    if opcode == OpCode.LIST_MAP:
        return f"{_expect_name(operand, opcode)} iti kāryeṇa samūhaḥ māpyate."
    if opcode == OpCode.LIST_FILTER:
        return f"{_expect_name(operand, opcode)} iti kāryeṇa samūhaḥ śodhyate."
    if opcode == OpCode.LIST_REDUCE:
        return f"{_expect_name(operand, opcode)} iti kāryeṇa samūhaḥ saṅkucyate."
    if opcode == OpCode.LIST_ALL:
        return f"{_expect_name(operand, opcode)} iti kāryeṇa samūhaḥ sarvam parīkṣyate."
    if opcode == OpCode.LIST_SCAN:
        return f"{_expect_name(operand, opcode)} iti kāryeṇa samūhaḥ avalokyate."
    if opcode == OpCode.LIST_ZIP:
        return "dvayoḥ samūhayoḥ yuktam kriyate."
    if opcode == OpCode.LIST_ENUMERATE:
        return "samūhaḥ aṅkayuktaḥ kriyate."
    if opcode == OpCode.LIST_ANY:
        return f"{_expect_name(operand, opcode)} iti kāryeṇa samūhaḥ kācit parīkṣyate."
    if opcode == OpCode.LIST_COMPREHENSION:
        return f"{_expect_name(operand, opcode)} iti samīkaraṇam kriyate."
    if opcode == OpCode.IMMUTABLE_LIST_NEW:
        return "nityaḥ samūhaḥ nirmīyate."
    if opcode == OpCode.IMMUTABLE_LIST_APPEND:
        return "nitye samūhe yojanam kriyate."
    if opcode == OpCode.IMMUTABLE_LIST_LEN:
        return "nityasya samūhasya parimāṇam gṛhyate."
    if opcode == OpCode.IMMUTABLE_LIST_GET:
        return "nityāt samūhāt aṅkam gṛhyate."
    if opcode == OpCode.LAZY_ITER_NEW:
        return "alasaḥ iteratoraḥ nirmīyate."
    if opcode == OpCode.LAZY_ITER_NEXT:
        return "alasāt anukramaḥ gṛhyate."
    if opcode == OpCode.GENERATOR_NEW:
        return f"{_expect_name(operand, opcode)} iti utpādakaḥ nirmīyate."
    if opcode == OpCode.GENERATOR_NEXT:
        return "utpādakāt pradānam gṛhyate."
    if opcode == OpCode.GENERATOR_YIELD:
        return "pradānam kriyate."
    if opcode == OpCode.PIPELINE_CHAIN:
        return f"{_expect_name(operand, opcode)} iti pravāhaḥ sañcālyate."
    if opcode == OpCode.RESULT_BIND:
        return f"{_expect_name(operand, opcode)} iti phale bandhanam kriyate."
    if opcode == OpCode.DATA_QUERY:
        return f"{_expect_name(operand, opcode)} iti anveṣaṇam kriyate."
    if opcode == OpCode.RULE_REGISTER:
        return f"{_expect_name(operand, opcode)} iti niyamaḥ sthāpyate."
    if opcode == OpCode.RULE_INVOKE:
        return f"{_expect_name(operand, opcode)} iti niyamaḥ āhūyate."
    if opcode == OpCode.MEMO_CALL:
        return f"{_expect_name(operand, opcode)} iti smaraṇena āhūyate."
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
    if opcode == OpCode.CLASS_NEW:
        return f"{_expect_name(operand, opcode)} iti varga-nirmāṇam kriyate."
    if opcode == OpCode.METHOD_CALL:
        return f"{_expect_name(operand, opcode)} iti paddhati-āhvānam kriyate."
    if opcode == OpCode.PUSH_BIGINT:
        return f"{_format_int(_expect_int(operand, opcode))} iti ati-pūrṇāṅkaḥ nikṣipyate."
    if opcode == OpCode.PUSH_I32:
        return f"{_format_int(_expect_int(operand, opcode))} iti saṅkhyā-lagu nikṣipyate."
    if opcode == OpCode.PUSH_U32:
        return f"{_format_int(_expect_int(operand, opcode))} iti saṅkhyā-nirṇāśa nikṣipyate."
    if opcode == OpCode.I32_ADD_CHECKED:
        return "saṅkhyā-lagvoḥ yogaḥ parīkṣitaḥ kriyate."
    if opcode == OpCode.U32_ADD_CHECKED:
        return "saṅkhyā-nirṇāśayoḥ yogaḥ parīkṣitaḥ kriyate."
    if opcode.value in SPEC_BY_PUSH_OPCODE and opcode not in {OpCode.PUSH_I32, OpCode.PUSH_U32}:
        return f"{_format_int(_expect_int(operand, opcode))} iti {SPEC_BY_PUSH_OPCODE[opcode.value].yantra_push_suffix} nikṣipyate."
    if opcode.value in SPEC_BY_ADD_CHECKED and opcode not in {OpCode.I32_ADD_CHECKED, OpCode.U32_ADD_CHECKED}:
        return SPEC_BY_ADD_CHECKED[opcode.value].yantra_add_checked
    if opcode.value in SPEC_BY_ADD_WRAPPING:
        spec = SPEC_BY_ADD_WRAPPING[opcode.value]
        return f"{spec.yantra_push_suffix}yoḥ yogaḥ parivṛttaḥ kriyate."
    if opcode.value in SPEC_BY_ADD_SATURATING:
        spec = SPEC_BY_ADD_SATURATING[opcode.value]
        return f"{spec.yantra_push_suffix}yoḥ yogaḥ sīmitaḥ kriyate."
    if opcode == OpCode.PUSH_BYTES:
        return f"{_expect_text(operand, opcode)} iti akṣara-śreṇī nikṣipyate."
    if opcode == OpCode.BYTE_NEW:
        return "śūnyā akṣara-śreṇī nirmīyate."
    if opcode == OpCode.BYTE_LEN:
        return "akṣara-śreṇyāḥ parimāṇam gṛhyate."
    if opcode == OpCode.BYTE_GET:
        return "akṣara-śreṇyāḥ aṅkam gṛhyate."
    if opcode == OpCode.BYTEARRAY_NEW:
        return "śūnyaḥ akṣara-saṃgrahaḥ nirmīyate."
    if opcode == OpCode.BYTEARRAY_SET:
        return "akṣara-saṃgrahe sthāpanam kriyate."
    if opcode == OpCode.BYTEARRAY_GET:
        return "akṣara-saṃgrahāt aṅkam gṛhyate."
    if opcode == OpCode.TUPLE_NEW:
        return f"{_format_int(_expect_int(operand, opcode))} iti yuktiḥ nirmīyate."
    if opcode == OpCode.TUPLE_GET:
        return f"{_format_int(_expect_int(operand, opcode))} iti yuktau aṅkam gṛhyate."
    if opcode == OpCode.SET_NEW:
        return "śūnyaḥ samāhāraḥ nirmīyate."
    if opcode == OpCode.SET_ADD:
        return "samāhāre yojanam kriyate."
    if opcode == OpCode.SET_CONTAINS:
        return "samāhāre sattā parīkṣyate."
    if opcode == OpCode.SET_LEN:
        return "samāhārasya parimāṇam gṛhyate."
    if opcode == OpCode.DEQUE_NEW:
        return "śūnyaḥ dviguṇa-samūhaḥ nirmīyate."
    if opcode == OpCode.DEQUE_PUSH_BACK:
        return "dviguṇa-samūhe pṛṣṭhe yojanam kriyate."
    if opcode == OpCode.DEQUE_PUSH_FRONT:
        return "dviguṇa-samūhe agre yojanam kriyate."
    if opcode == OpCode.DEQUE_POP_BACK:
        return "dviguṇa-samūhāt pṛṣṭhād aṅkam gṛhyate."
    if opcode == OpCode.DEQUE_POP_FRONT:
        return "dviguṇa-samūhāt agrāt aṅkam gṛhyate."
    if opcode == OpCode.DEQUE_LEN:
        return "dviguṇa-samūhasya parimāṇam gṛhyate."
    if opcode == OpCode.OPTION_NONE:
        return "śūnyaḥ vikalpaḥ nirmīyate."
    if opcode == OpCode.OPTION_SOME:
        return "vikalpe yojanam kriyate."
    if opcode == OpCode.OPTION_IS_SOME:
        return "vikalpasya sattā parīkṣyate."
    if opcode == OpCode.OPTION_UNWRAP:
        return "vikalpāt mūlyam gṛhyate."
    if opcode == OpCode.RESULT_OK:
        return "phale saphalatā sthāpyate."
    if opcode == OpCode.RESULT_ERR:
        return "phale doṣaḥ sthāpyate."
    if opcode == OpCode.RESULT_IS_OK:
        return "phalasya saphalatā parīkṣyate."
    if opcode == OpCode.RESULT_UNWRAP_OK:
        return "saphalāt phalāt mūlyam gṛhyate."
    if opcode == OpCode.RESULT_UNWRAP_ERR:
        return "doṣāt phalāt mūlyam gṛhyate."
    if opcode == OpCode.TEXT_GRAPHEME_LEN:
        return "vākyasya graṇī-parimāṇam gṛhyate."
    if opcode == OpCode.FLOAT_IS_NAN:
        return "daśāṃśasya anirṇayaḥ parīkṣyate."
    if opcode == OpCode.FLOAT_IS_INF:
        return "daśāṃśasya anantaḥ parīkṣyate."
    if opcode == OpCode.OPAQUE_NEW:
        return f"{_expect_name(operand, opcode)} iti āvaraṇaṃ nirmīyate."
    if opcode == OpCode.ARRAY_NEW:
        return f"{_format_int(_expect_int(operand, opcode))} iti niyata-samūhaḥ nirmīyate."
    if opcode == OpCode.SLICE_VIEW:
        return "samūhasya chedaḥ dṛśyaḥ kriyate."
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
    if opcode == OpCode.PTR_FROM_INT:
        return "aṅkāt sūcikā nirmīyate."
    if opcode == OpCode.PTR_TO_INT:
        return "sūcikāyāḥ aṅkaḥ gṛhyate."
    if opcode == OpCode.PTR_ADD:
        return "sūcikāyāṃ yogaḥ kriyate."
    if opcode == OpCode.PTR_SUB:
        return "sūcikāyāṃ vyavakalanam kriyate."
    if opcode == OpCode.LOAD_U8:
        return "smṛteḥ eka-bhāraḥ āhriyate."
    if opcode == OpCode.LOAD_U16_LE:
        return "smṛteḥ dvi-bhāraḥ laghu-kramena āhriyate."
    if opcode == OpCode.LOAD_U16_BE:
        return "smṛteḥ dvi-bhāraḥ guru-kramena āhriyate."
    if opcode == OpCode.LOAD_U32_LE:
        return "smṛteḥ catur-bhāraḥ laghu-kramena āhriyate."
    if opcode == OpCode.LOAD_U32_BE:
        return "smṛteḥ catur-bhāraḥ guru-kramena āhriyate."
    if opcode == OpCode.STORE_U8:
        return "smṛtau eka-bhāra-sthāpanam kriyate."
    if opcode == OpCode.STORE_U16_LE:
        return "smṛtau dvi-bhāra-sthāpanam laghu-kramena kriyate."
    if opcode == OpCode.STORE_U16_BE:
        return "smṛtau dvi-bhāra-sthāpanam guru-kramena kriyate."
    if opcode == OpCode.STORE_U32_LE:
        return "smṛtau catur-bhāra-sthāpanam laghu-kramena kriyate."
    if opcode == OpCode.STORE_U32_BE:
        return "smṛtau catur-bhāra-sthāpanam guru-kramena kriyate."
    if opcode == OpCode.VOLATILE_LOAD_U32_LE:
        return "smṛteḥ kampita-catur-bhāraḥ laghu-kramena āhriyate."
    if opcode == OpCode.VOLATILE_STORE_U32_LE:
        return "smṛtau kampita-catur-bhāra-sthāpanam laghu-kramena kriyate."
    if opcode == OpCode.BIT_AND:
        return "aṅkayoḥ bit-sandhiḥ kriyate."
    if opcode == OpCode.BIT_OR:
        return "aṅkayoḥ bit-vikalpaḥ kriyate."
    if opcode == OpCode.BIT_XOR:
        return "aṅkayoḥ bit-vyatirekaḥ kriyate."
    if opcode == OpCode.BIT_NOT:
        return "aṅkasya bit-nivṛttiḥ kriyate."
    if opcode == OpCode.SHIFT_LEFT:
        return "aṅkasya vāma-saraṇam kriyate."
    if opcode == OpCode.SHIFT_RIGHT:
        return "aṅkasya dakṣiṇa-saraṇam kriyate."
    if opcode == OpCode.ROTATE_LEFT32:
        return "aṅkasya vāma-parivartanam kriyate."
    if opcode == OpCode.ROTATE_RIGHT32:
        return "aṅkasya dakṣiṇa-parivartanam kriyate."
    if opcode == OpCode.REG_SET:
        return f"{_expect_name(operand, opcode)} iti pañjikā-sthāpanam kriyate."
    if opcode == OpCode.REG_GET:
        return f"{_expect_name(operand, opcode)} iti pañjikā-āharaṇam kriyate."
    if opcode == OpCode.SP_SET:
        return "pada-sūcikā sthāpyate."
    if opcode == OpCode.SP_GET:
        return "pada-sūcikā āhriyate."
    if opcode == OpCode.FP_SET:
        return "koṣṭha-sūcikā sthāpyate."
    if opcode == OpCode.FP_GET:
        return "koṣṭha-sūcikā āhriyate."
    if opcode == OpCode.CALL_CONV:
        return f"{_expect_name(operand, opcode)} iti āhvāna-maryādā nirdiśyate."
    if opcode == OpCode.PROLOGUE:
        return "prastāvaḥ kriyate."
    if opcode == OpCode.EPILOGUE:
        return "samāpanāṅgaṃ kriyate."
    if opcode == OpCode.INLINE_ASM:
        return f"{_expect_text(operand, opcode)} iti yantra-gadyaṃ nikṣipyate."
    if opcode == OpCode.LABEL:
        return f"{_expect_name(operand, opcode)} iti cihnam nirdiśyate."
    if opcode == OpCode.JUMP_LABEL:
        return f"{_expect_name(operand, opcode)} iti cihnaṃ gamyate."
    if opcode == OpCode.JUMP_IF_ZERO_LABEL:
        return f"śūnye sati {_expect_name(operand, opcode)} iti cihnaṃ gamyate."
    if opcode == OpCode.JUMP_INDIRECT:
        return "parokṣeṇa lakṣyaṃ gamyate."
    if opcode == OpCode.CALL_INDIRECT:
        return "parokṣeṇa vidhānam āhūyate."
    if opcode == OpCode.SYSCALL:
        return f"{_expect_name(operand, opcode)} iti praṇālī-āhvānam kriyate."
    if opcode == OpCode.TRAP:
        return f"{_format_int(_expect_int(operand, opcode))} iti trapaḥ kriyate."
    if opcode == OpCode.MMIO_READ:
        return "yantra-sañjñāt āharaṇam kriyate."
    if opcode == OpCode.MMIO_WRITE:
        return "yantra-sañjñāyāṃ sthāpanam kriyate."
    if opcode == OpCode.ATOMIC_CAS_U32_LE:
        return "aṇu-parivartana-sādṛśyam laghu-kramena kriyate."
    if opcode == OpCode.FENCE:
        return f"{_expect_name(operand, opcode)} iti smṛti-setuḥ kriyate."
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
    if opcode == OpCode.COMPARE_NE:
        return "asāmyam parīkṣyate."
    if opcode == OpCode.COMPARE_LT:
        return "nyūnatvam parīkṣyate."
    if opcode == OpCode.COMPARE_GT:
        return "adhikatvam parīkṣyate."
    if opcode == OpCode.COMPARE_LE:
        return "nyūna-sāmyam parīkṣyate."
    if opcode == OpCode.COMPARE_IDENTITY:
        return "tattva-sāmyaṃ parīkṣyate."
    if opcode == OpCode.PUSH_NIL:
        return "abhāvaḥ nikṣipyate."
    if opcode == OpCode.SCOPE_ENTER:
        return "paridhiḥ ārabhyate."
    if opcode == OpCode.SCOPE_EXIT:
        return "paridhiḥ samāpyate."
    if opcode == OpCode.BREAK_LOOP:
        return f"{_expect_name(operand, opcode)} iti cakra-bhaṅgaḥ kriyate."
    if opcode == OpCode.CONTINUE_LOOP:
        return f"{_expect_name(operand, opcode)} iti cakra-punarāvṛttiḥ kriyate."
    if opcode == OpCode.DEFER_PUSH:
        return f"{_format_int(_expect_int(operand, opcode))} iti vilambita-kriyā sthāpyate."
    if opcode == OpCode.DEFER_RUN:
        return "vilambita-kriyā pravartyate."
    if opcode == OpCode.MATCH_EQ:
        return "sāmya-rūpaḥ parīkṣyate."
    if opcode == OpCode.MATCH_TUPLE_LEN:
        return f"{_format_int(_expect_int(operand, opcode))} iti yukti-parimāṇam parīkṣyate."
    if opcode == OpCode.MATCH_RECORD_HAS:
        return f"{_expect_text(operand, opcode)} iti vastu-aṅga-sattā parīkṣyate."
    if opcode == OpCode.EMIT:
        return "darśanam kriyate."
    if opcode == OpCode.JUMP:
        return f"{_format_int(_expect_int(operand, opcode))} iti lakṣyaṃ gamyate."
    if opcode == OpCode.JUMP_IF_ZERO:
        return f"śūnye sati {_format_int(_expect_int(operand, opcode))} iti lakṣyaṃ gamyate."
    if opcode in {OpCode.CALL, OpCode.TAIL_CALL}:
        target = _expect_name(operand, opcode)
        verb = "anukramya" if opcode == OpCode.TAIL_CALL else "āhūyate"
        if "." in target:
            module_name, function_name = target.split(".", 1)
            return f"{module_name} iti kṣetre {function_name} iti vidhānam {verb}."
        return f"{target} iti vidhānam {verb}."
    if opcode == OpCode.PUSH_FUNC:
        return f"{_expect_name(operand, opcode)} iti vidhāna-cihnam nikṣipyate."
    if opcode == OpCode.RETURN:
        return "pratyāvartanam kriyate."
    if opcode == OpCode.POP:
        return "tyāgaḥ kriyate."
    if opcode == OpCode.THROW:
        return "vikṣepaḥ kriyate."
    if opcode == OpCode.PANIC:
        return "vipattim kriyate."
    if opcode == OpCode.TRY_BEGIN:
        return f"āgrahītvā {_format_int(_expect_int(operand, opcode))} iti lakṣyaṃ ārabhyate."
    if opcode == OpCode.TRY_END:
        return "āgrahītvaḥ samāpyate."
    if opcode == OpCode.HALT:
        return "virāmaḥ kriyate."
    if opcode in _PHASE3_RENDER_SENTENCES:
        if opcode in {OpCode("push_decimal")}:
            return f"{_expect_text(operand, opcode)} iti {_PHASE3_RENDER_SENTENCES[opcode]}"
        if opcode in {OpCode("push_scalar"), OpCode("named_tuple_new")}:
            return f"{_format_int(_expect_int(operand, opcode))} iti {_PHASE3_RENDER_SENTENCES[opcode]}"
        if opcode in {OpCode("enum_new"), OpCode("tagged_union_new"), OpCode("typed_error_new"), OpCode("named_tuple_get"), OpCode("handle_new")}:
            return f"{_expect_name(operand, opcode)} iti {_PHASE3_RENDER_SENTENCES[opcode]}"
        return _PHASE3_RENDER_SENTENCES[opcode]

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
                raise BytecodeValidationError(
                    f"Instruction appeared outside any active stream: {sentence!r}"
                )
            self.current_stream.append(instruction)

        if self.current_function is not None:
            raise BytecodeValidationError(f"Function {self.current_function!r} was not closed")
        if self.current_module is not None:
            raise BytecodeValidationError(f"Module {self.current_module!r} was not closed")
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
    if tokens == ["vākyayoḥ", "saṃyogaḥ", "kriyate"]:
        return Instruction(OpCode.TEXT_CONCAT)
    if tokens == ["vākyasya", "parimāṇam", "gṛhyate"]:
        return Instruction(OpCode.TEXT_LEN)
    if tokens == ["vākyāt", "aṅkam", "gṛhyate"]:
        return Instruction(OpCode.TEXT_GET)
    if tokens == ["vākyasya", "chedaḥ", "kriyate"]:
        return Instruction(OpCode.TEXT_SLICE)
    if tokens == ["vākye", "sattā", "parīkṣyate"]:
        return Instruction(OpCode.TEXT_CONTAINS)
    if tokens == ["śūnyaḥ", "samūhaḥ", "nirmīyate"]:
        return Instruction(OpCode.LIST_NEW)
    if tokens == ["samūhe", "yojanam", "kriyate"]:
        return Instruction(OpCode.LIST_APPEND)
    if tokens == ["samūhasya", "parimāṇam", "gṛhyate"]:
        return Instruction(OpCode.LIST_LEN)
    if tokens == ["samūhāt", "aṅkam", "gṛhyate"]:
        return Instruction(OpCode.LIST_GET)
    if len(tokens) >= 5 and tokens[1:] == ["iti", "kāryeṇa", "samūhaḥ", "māpyate"]:
        return Instruction(OpCode.LIST_MAP, tokens[0])
    if len(tokens) >= 5 and tokens[1:] == ["iti", "kāryeṇa", "samūhaḥ", "śodhyate"]:
        return Instruction(OpCode.LIST_FILTER, tokens[0])
    if len(tokens) >= 5 and tokens[1:] == ["iti", "kāryeṇa", "samūhaḥ", "saṅkucyate"]:
        return Instruction(OpCode.LIST_REDUCE, tokens[0])
    if len(tokens) >= 6 and tokens[1:] == ["iti", "kāryeṇa", "samūhaḥ", "sarvam", "parīkṣyate"]:
        return Instruction(OpCode.LIST_ALL, tokens[0])
    if len(tokens) >= 6 and tokens[1:] == ["iti", "kāryeṇa", "samūhaḥ", "kācit", "parīkṣyate"]:
        return Instruction(OpCode.LIST_ANY, tokens[0])
    if len(tokens) >= 4 and tokens[1:] == ["iti", "samīkaraṇam", "kriyate"]:
        return Instruction(OpCode.LIST_COMPREHENSION, tokens[0])
    if len(tokens) >= 5 and tokens[1:] == ["iti", "kāryeṇa", "samūhaḥ", "avalokyate"]:
        return Instruction(OpCode.LIST_SCAN, tokens[0])
    if tokens == ["dvayoḥ", "samūhayoḥ", "yuktam", "kriyate"]:
        return Instruction(OpCode.LIST_ZIP)
    if tokens == ["samūhaḥ", "aṅkayuktaḥ", "kriyate"]:
        return Instruction(OpCode.LIST_ENUMERATE)
    if tokens == ["nityaḥ", "samūhaḥ", "nirmīyate"]:
        return Instruction(OpCode.IMMUTABLE_LIST_NEW)
    if tokens == ["nitye", "samūhe", "yojanam", "kriyate"]:
        return Instruction(OpCode.IMMUTABLE_LIST_APPEND)
    if tokens == ["nityasya", "samūhasya", "parimāṇam", "gṛhyate"]:
        return Instruction(OpCode.IMMUTABLE_LIST_LEN)
    if tokens == ["nityāt", "samūhāt", "aṅkam", "gṛhyate"]:
        return Instruction(OpCode.IMMUTABLE_LIST_GET)
    if tokens == ["alasaḥ", "iteratoraḥ", "nirmīyate"]:
        return Instruction(OpCode.LAZY_ITER_NEW)
    if tokens == ["alasāt", "anukramaḥ", "gṛhyate"]:
        return Instruction(OpCode.LAZY_ITER_NEXT)
    if len(tokens) >= 4 and tokens[1:] == ["iti", "utpādakaḥ", "nirmīyate"]:
        return Instruction(OpCode.GENERATOR_NEW, tokens[0])
    if tokens == ["utpādakāt", "pradānam", "gṛhyate"]:
        return Instruction(OpCode.GENERATOR_NEXT)
    if tokens == ["pradānam", "kriyate"]:
        return Instruction(OpCode.GENERATOR_YIELD)
    if len(tokens) >= 4 and tokens[1:] == ["iti", "pravāhaḥ", "sañcālyate"]:
        return Instruction(OpCode.PIPELINE_CHAIN, tokens[0])
    if len(tokens) >= 5 and tokens[1:] == ["iti", "phale", "bandhanam", "kriyate"]:
        return Instruction(OpCode.RESULT_BIND, tokens[0])
    if len(tokens) >= 4 and tokens[1:] == ["iti", "anveṣaṇam", "kriyate"]:
        return Instruction(OpCode.DATA_QUERY, tokens[0])
    if len(tokens) >= 4 and tokens[1:] == ["iti", "niyamaḥ", "sthāpyate"]:
        return Instruction(OpCode.RULE_REGISTER, tokens[0])
    if len(tokens) >= 4 and tokens[1:] == ["iti", "niyamaḥ", "āhūyate"]:
        return Instruction(OpCode.RULE_INVOKE, tokens[0])
    if len(tokens) >= 4 and tokens[1:] == ["iti", "smaraṇena", "āhūyate"]:
        return Instruction(OpCode.MEMO_CALL, tokens[0])
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
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "varga-nirmāṇam", "kriyate"]:
        return Instruction(OpCode.CLASS_NEW, tokens[0])
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "paddhati-āhvānam", "kriyate"]:
        return Instruction(OpCode.METHOD_CALL, tokens[0])
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "ati-pūrṇāṅkaḥ", "nikṣipyate"]:
        return Instruction(OpCode.PUSH_BIGINT, _parse_int(tokens[:-3]))
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "saṅkhyā-lagu", "nikṣipyate"]:
        return Instruction(OpCode.PUSH_I32, _parse_int(tokens[:-3]))
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "saṅkhyā-nirṇāśa", "nikṣipyate"]:
        return Instruction(OpCode.PUSH_U32, _parse_int(tokens[:-3]))
    if tokens == ["saṅkhyā-lagvoḥ", "yogaḥ", "parīkṣitaḥ", "kriyate"]:
        return Instruction(OpCode.I32_ADD_CHECKED)
    if tokens == ["saṅkhyā-nirṇāśayoḥ", "yogaḥ", "parīkṣitaḥ", "kriyate"]:
        return Instruction(OpCode.U32_ADD_CHECKED)
    if (
        len(tokens) >= 4
        and tokens[-1] == "nikṣipyate"
        and tokens[-2] in {"saṅkhyā-1", "saṅkhyā-2", "saṅkhyā-4", "saṅkhyā-8", "saṅkhyā-16", "saṅkhyā-nirṇāśa-1", "saṅkhyā-nirṇāśa-2", "saṅkhyā-nirṇāśa-4", "saṅkhyā-nirṇāśa-8", "saṅkhyā-nirṇāśa-16", "yantra-saṅkhyā", "yantra-saṅkhyā-nirṇāśa"}
        and tokens[-3] == "iti"
    ):
        phrase = tokens[-2]
        for spec in SPEC_BY_PUSH_OPCODE.values():
            if spec.yantra_push_suffix == phrase:
                return Instruction(OpCode(spec.push_opcode), _parse_int(tokens[:-3]))
    if len(tokens) == 4 and tokens[-1] == "kriyate" and tokens[1] == "yogaḥ" and tokens[2] in {"parivṛttaḥ", "sīmitaḥ"}:
        phrase = tokens[0]
        for spec in SPEC_BY_ADD_WRAPPING.values():
            if f"{spec.yantra_push_suffix}yoḥ" == phrase and tokens[2] == "parivṛttaḥ":
                return Instruction(OpCode(spec.add_wrapping_opcode))
        for spec in SPEC_BY_ADD_SATURATING.values():
            if f"{spec.yantra_push_suffix}yoḥ" == phrase and tokens[2] == "sīmitaḥ":
                return Instruction(OpCode(spec.add_saturating_opcode))
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "akṣara-śreṇī", "nikṣipyate"]:
        return Instruction(OpCode.PUSH_BYTES, " ".join(tokens[:-3]))
    if tokens == ["śūnyā", "akṣara-śreṇī", "nirmīyate"]:
        return Instruction(OpCode.BYTE_NEW)
    if tokens == ["akṣara-śreṇyāḥ", "parimāṇam", "gṛhyate"]:
        return Instruction(OpCode.BYTE_LEN)
    if tokens == ["akṣara-śreṇyāḥ", "aṅkam", "gṛhyate"]:
        return Instruction(OpCode.BYTE_GET)
    if tokens == ["śūnyaḥ", "akṣara-saṃgrahaḥ", "nirmīyate"]:
        return Instruction(OpCode.BYTEARRAY_NEW)
    if tokens == ["akṣara-saṃgrahe", "sthāpanam", "kriyate"]:
        return Instruction(OpCode.BYTEARRAY_SET)
    if tokens == ["akṣara-saṃgrahāt", "aṅkam", "gṛhyate"]:
        return Instruction(OpCode.BYTEARRAY_GET)
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "yuktiḥ", "nirmīyate"]:
        return Instruction(OpCode.TUPLE_NEW, _parse_int(tokens[:-3]))
    if len(tokens) >= 5 and tokens[-4:] == ["iti", "yuktau", "aṅkam", "gṛhyate"]:
        return Instruction(OpCode.TUPLE_GET, _parse_int(tokens[:-4]))
    if tokens == ["śūnyaḥ", "samāhāraḥ", "nirmīyate"]:
        return Instruction(OpCode.SET_NEW)
    if tokens == ["samāhāre", "yojanam", "kriyate"]:
        return Instruction(OpCode.SET_ADD)
    if tokens == ["samāhāre", "sattā", "parīkṣyate"]:
        return Instruction(OpCode.SET_CONTAINS)
    if tokens == ["samāhārasya", "parimāṇam", "gṛhyate"]:
        return Instruction(OpCode.SET_LEN)
    if tokens == ["śūnyaḥ", "dviguṇa-samūhaḥ", "nirmīyate"]:
        return Instruction(OpCode.DEQUE_NEW)
    if tokens == ["dviguṇa-samūhe", "pṛṣṭhe", "yojanam", "kriyate"]:
        return Instruction(OpCode.DEQUE_PUSH_BACK)
    if tokens == ["dviguṇa-samūhe", "agre", "yojanam", "kriyate"]:
        return Instruction(OpCode.DEQUE_PUSH_FRONT)
    if tokens == ["dviguṇa-samūhāt", "pṛṣṭhād", "aṅkam", "gṛhyate"]:
        return Instruction(OpCode.DEQUE_POP_BACK)
    if tokens == ["dviguṇa-samūhāt", "agrāt", "aṅkam", "gṛhyate"]:
        return Instruction(OpCode.DEQUE_POP_FRONT)
    if tokens == ["dviguṇa-samūhasya", "parimāṇam", "gṛhyate"]:
        return Instruction(OpCode.DEQUE_LEN)
    if tokens == ["śūnyaḥ", "vikalpaḥ", "nirmīyate"]:
        return Instruction(OpCode.OPTION_NONE)
    if tokens == ["vikalpe", "yojanam", "kriyate"]:
        return Instruction(OpCode.OPTION_SOME)
    if tokens == ["vikalpasya", "sattā", "parīkṣyate"]:
        return Instruction(OpCode.OPTION_IS_SOME)
    if tokens == ["vikalpāt", "mūlyam", "gṛhyate"]:
        return Instruction(OpCode.OPTION_UNWRAP)
    if tokens == ["phale", "saphalatā", "sthāpyate"]:
        return Instruction(OpCode.RESULT_OK)
    if tokens == ["phale", "doṣaḥ", "sthāpyate"]:
        return Instruction(OpCode.RESULT_ERR)
    if tokens == ["phalasya", "saphalatā", "parīkṣyate"]:
        return Instruction(OpCode.RESULT_IS_OK)
    if tokens == ["saphalāt", "phalāt", "mūlyam", "gṛhyate"]:
        return Instruction(OpCode.RESULT_UNWRAP_OK)
    if tokens == ["doṣāt", "phalāt", "mūlyam", "gṛhyate"]:
        return Instruction(OpCode.RESULT_UNWRAP_ERR)
    if tokens == ["vākyasya", "graṇī-parimāṇam", "gṛhyate"]:
        return Instruction(OpCode.TEXT_GRAPHEME_LEN)
    if tokens == ["daśāṃśasya", "anirṇayaḥ", "parīkṣyate"]:
        return Instruction(OpCode.FLOAT_IS_NAN)
    if tokens == ["daśāṃśasya", "anantaḥ", "parīkṣyate"]:
        return Instruction(OpCode.FLOAT_IS_INF)
    if len(tokens) == 4 and tokens[1:] == ["iti", "āvaraṇaṃ", "nirmīyate"]:
        return Instruction(OpCode.OPAQUE_NEW, tokens[0])
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "niyata-samūhaḥ", "nirmīyate"]:
        return Instruction(OpCode.ARRAY_NEW, _parse_int(tokens[:-3]))
    if tokens == ["samūhasya", "chedaḥ", "dṛśyaḥ", "kriyate"]:
        return Instruction(OpCode.SLICE_VIEW)
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
    if tokens == ["aṅkāt", "sūcikā", "nirmīyate"]:
        return Instruction(OpCode.PTR_FROM_INT)
    if tokens == ["sūcikāyāḥ", "aṅkaḥ", "gṛhyate"]:
        return Instruction(OpCode.PTR_TO_INT)
    if tokens == ["sūcikāyāṃ", "yogaḥ", "kriyate"]:
        return Instruction(OpCode.PTR_ADD)
    if tokens == ["sūcikāyāṃ", "vyavakalanam", "kriyate"]:
        return Instruction(OpCode.PTR_SUB)
    if tokens == ["smṛteḥ", "eka-bhāraḥ", "āhriyate"]:
        return Instruction(OpCode.LOAD_U8)
    if tokens == ["smṛteḥ", "dvi-bhāraḥ", "laghu-kramena", "āhriyate"]:
        return Instruction(OpCode.LOAD_U16_LE)
    if tokens == ["smṛteḥ", "dvi-bhāraḥ", "guru-kramena", "āhriyate"]:
        return Instruction(OpCode.LOAD_U16_BE)
    if tokens == ["smṛteḥ", "catur-bhāraḥ", "laghu-kramena", "āhriyate"]:
        return Instruction(OpCode.LOAD_U32_LE)
    if tokens == ["smṛteḥ", "catur-bhāraḥ", "guru-kramena", "āhriyate"]:
        return Instruction(OpCode.LOAD_U32_BE)
    if tokens == ["smṛtau", "eka-bhāra-sthāpanam", "kriyate"]:
        return Instruction(OpCode.STORE_U8)
    if tokens == ["smṛtau", "dvi-bhāra-sthāpanam", "laghu-kramena", "kriyate"]:
        return Instruction(OpCode.STORE_U16_LE)
    if tokens == ["smṛtau", "dvi-bhāra-sthāpanam", "guru-kramena", "kriyate"]:
        return Instruction(OpCode.STORE_U16_BE)
    if tokens == ["smṛtau", "catur-bhāra-sthāpanam", "laghu-kramena", "kriyate"]:
        return Instruction(OpCode.STORE_U32_LE)
    if tokens == ["smṛtau", "catur-bhāra-sthāpanam", "guru-kramena", "kriyate"]:
        return Instruction(OpCode.STORE_U32_BE)
    if tokens == ["smṛteḥ", "kampita-catur-bhāraḥ", "laghu-kramena", "āhriyate"]:
        return Instruction(OpCode.VOLATILE_LOAD_U32_LE)
    if tokens == ["smṛtau", "kampita-catur-bhāra-sthāpanam", "laghu-kramena", "kriyate"]:
        return Instruction(OpCode.VOLATILE_STORE_U32_LE)
    if tokens == ["aṅkayoḥ", "bit-sandhiḥ", "kriyate"]:
        return Instruction(OpCode.BIT_AND)
    if tokens == ["aṅkayoḥ", "bit-vikalpaḥ", "kriyate"]:
        return Instruction(OpCode.BIT_OR)
    if tokens == ["aṅkayoḥ", "bit-vyatirekaḥ", "kriyate"]:
        return Instruction(OpCode.BIT_XOR)
    if tokens == ["aṅkasya", "bit-nivṛttiḥ", "kriyate"]:
        return Instruction(OpCode.BIT_NOT)
    if tokens == ["aṅkasya", "vāma-saraṇam", "kriyate"]:
        return Instruction(OpCode.SHIFT_LEFT)
    if tokens == ["aṅkasya", "dakṣiṇa-saraṇam", "kriyate"]:
        return Instruction(OpCode.SHIFT_RIGHT)
    if tokens == ["aṅkasya", "vāma-parivartanam", "kriyate"]:
        return Instruction(OpCode.ROTATE_LEFT32)
    if tokens == ["aṅkasya", "dakṣiṇa-parivartanam", "kriyate"]:
        return Instruction(OpCode.ROTATE_RIGHT32)
    if len(tokens) == 4 and tokens[1:] == ["iti", "pañjikā-sthāpanam", "kriyate"]:
        return Instruction(OpCode.REG_SET, tokens[0])
    if len(tokens) == 4 and tokens[1:] == ["iti", "pañjikā-āharaṇam", "kriyate"]:
        return Instruction(OpCode.REG_GET, tokens[0])
    if tokens == ["pada-sūcikā", "sthāpyate"]:
        return Instruction(OpCode.SP_SET)
    if tokens == ["pada-sūcikā", "āhriyate"]:
        return Instruction(OpCode.SP_GET)
    if tokens == ["koṣṭha-sūcikā", "sthāpyate"]:
        return Instruction(OpCode.FP_SET)
    if tokens == ["koṣṭha-sūcikā", "āhriyate"]:
        return Instruction(OpCode.FP_GET)
    if len(tokens) >= 4 and tokens[1:] == ["iti", "āhvāna-maryādā", "nirdiśyate"]:
        return Instruction(OpCode.CALL_CONV, tokens[0])
    if tokens == ["prastāvaḥ", "kriyate"]:
        return Instruction(OpCode.PROLOGUE)
    if tokens == ["samāpanāṅgaṃ", "kriyate"]:
        return Instruction(OpCode.EPILOGUE)
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "yantra-gadyaṃ", "nikṣipyate"]:
        return Instruction(OpCode.INLINE_ASM, " ".join(tokens[:-3]))
    if len(tokens) == 4 and tokens[1:] == ["iti", "cihnam", "nirdiśyate"]:
        return Instruction(OpCode.LABEL, tokens[0])
    if len(tokens) == 4 and tokens[1:] == ["iti", "cihnaṃ", "gamyate"]:
        return Instruction(OpCode.JUMP_LABEL, tokens[0])
    if len(tokens) == 6 and tokens[:2] == ["śūnye", "sati"] and tokens[3:] == ["iti", "cihnaṃ", "gamyate"]:
        return Instruction(OpCode.JUMP_IF_ZERO_LABEL, tokens[2])
    if tokens == ["parokṣeṇa", "lakṣyaṃ", "gamyate"]:
        return Instruction(OpCode.JUMP_INDIRECT)
    if tokens == ["parokṣeṇa", "vidhānam", "āhūyate"]:
        return Instruction(OpCode.CALL_INDIRECT)
    if len(tokens) >= 4 and tokens[1:] == ["iti", "praṇālī-āhvānam", "kriyate"]:
        return Instruction(OpCode.SYSCALL, tokens[0])
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "trapaḥ", "kriyate"]:
        return Instruction(OpCode.TRAP, _parse_int(tokens[:-3]))
    if tokens == ["yantra-sañjñāt", "āharaṇam", "kriyate"]:
        return Instruction(OpCode.MMIO_READ)
    if tokens == ["yantra-sañjñāyāṃ", "sthāpanam", "kriyate"]:
        return Instruction(OpCode.MMIO_WRITE)
    if tokens == ["aṇu-parivartana-sādṛśyam", "laghu-kramena", "kriyate"]:
        return Instruction(OpCode.ATOMIC_CAS_U32_LE)
    if len(tokens) >= 4 and tokens[1:] == ["iti", "smṛti-setuḥ", "kriyate"]:
        return Instruction(OpCode.FENCE, tokens[0])
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
    if tokens == ["asāmyam", "parīkṣyate"]:
        return Instruction(OpCode.COMPARE_NE)
    if tokens == ["nyūnatvam", "parīkṣyate"]:
        return Instruction(OpCode.COMPARE_LT)
    if tokens == ["adhikatvam", "parīkṣyate"]:
        return Instruction(OpCode.COMPARE_GT)
    if tokens == ["nyūna-sāmyam", "parīkṣyate"]:
        return Instruction(OpCode.COMPARE_LE)
    if tokens == ["tattva-sāmyaṃ", "parīkṣyate"]:
        return Instruction(OpCode.COMPARE_IDENTITY)
    if tokens == ["abhāvaḥ", "nikṣipyate"]:
        return Instruction(OpCode.PUSH_NIL)
    if tokens == ["paridhiḥ", "ārabhyate"]:
        return Instruction(OpCode.SCOPE_ENTER)
    if tokens == ["paridhiḥ", "samāpyate"]:
        return Instruction(OpCode.SCOPE_EXIT)
    if len(tokens) >= 4 and tokens[1:] == ["iti", "cakra-bhaṅgaḥ", "kriyate"]:
        return Instruction(OpCode.BREAK_LOOP, tokens[0])
    if len(tokens) >= 4 and tokens[1:] == ["iti", "cakra-punarāvṛttiḥ", "kriyate"]:
        return Instruction(OpCode.CONTINUE_LOOP, tokens[0])
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "vilambita-kriyā", "sthāpyate"]:
        return Instruction(OpCode.DEFER_PUSH, _parse_int(tokens[:-3]))
    if tokens == ["vilambita-kriyā", "pravartyate"]:
        return Instruction(OpCode.DEFER_RUN)
    if tokens == ["sāmya-rūpaḥ", "parīkṣyate"]:
        return Instruction(OpCode.MATCH_EQ)
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "yukti-parimāṇam", "parīkṣyate"]:
        return Instruction(OpCode.MATCH_TUPLE_LEN, _parse_int(tokens[:-3]))
    if len(tokens) >= 4 and tokens[-3:] == ["iti", "vastu-aṅga-sattā", "parīkṣyate"]:
        return Instruction(OpCode.MATCH_RECORD_HAS, " ".join(tokens[:-3]))
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
    if len(tokens) == 4 and tokens[1:] == ["iti", "vidhānam", "anukramya"]:
        return Instruction(OpCode.TAIL_CALL, tokens[0])
    if len(tokens) == 7 and tokens[1:3] == ["iti", "kṣetre"] and tokens[4:] == [
        "iti",
        "vidhānam",
        "anukramya",
    ]:
        return Instruction(OpCode.TAIL_CALL, qualified_function_name(tokens[0], tokens[3]))
    if len(tokens) >= 4 and tokens[1:] == ["iti", "vidhāna-cihnam", "nikṣipyate"]:
        return Instruction(OpCode.PUSH_FUNC, tokens[0])
    if tokens == ["pratyāvartanam", "kriyate"]:
        return Instruction(OpCode.RETURN)
    if tokens == ["tyāgaḥ", "kriyate"]:
        return Instruction(OpCode.POP)
    if tokens == ["vikṣepaḥ", "kriyate"]:
        return Instruction(OpCode.THROW)
    if tokens == ["vipattim", "kriyate"]:
        return Instruction(OpCode.PANIC)
    if (
        len(tokens) >= 5
        and tokens[-1] == "ārabhyate"
        and tokens[-3] == "iti"
        and tokens[0] in {"āgrahītvā", "āgrahītva", "agrahitva"}
        and tokens[-2] in {"lakṣyaṃ", "lakṣyam", "lakshyam"}
    ):
        return Instruction(OpCode.TRY_BEGIN, _parse_int(tokens[1:-3]))
    if tokens == ["āgrahītvaḥ", "samāpyate"]:
        return Instruction(OpCode.TRY_END)
    if tokens == ["virāmaḥ", "kriyate"]:
        return Instruction(OpCode.HALT)
    if tuple(tokens) in _PHASE3_PARSE_SENTENCES:
        return Instruction(_PHASE3_PARSE_SENTENCES[tuple(tokens)])
    if len(tokens) >= 4 and tokens[-1] in {"nikṣipyate", "nirmīyate", "gṛhyate"} and tokens[-3] == "iti":
        suffix = " ".join(tokens[-2:])
        if suffix == "daśāṃśa-saṅkhyā nikṣipyate":
            return Instruction(OpCode("push_decimal"), " ".join(tokens[:-3]))
        if suffix == "akṣara-bījam nikṣipyate":
            return Instruction(OpCode("push_scalar"), _parse_int(tokens[:-3]))
        if suffix == "gaṇavikalpaḥ nirmīyate":
            return Instruction(OpCode("enum_new"), tokens[0])
        if suffix == "cihna-saṅghaṭaḥ nirmīyate":
            return Instruction(OpCode("tagged_union_new"), tokens[0])
        if suffix == "lakṣita-doṣaḥ nirmīyate":
            return Instruction(OpCode("typed_error_new"), tokens[0])
        if suffix == "nāma-yuktiḥ nirmīyate":
            return Instruction(OpCode("named_tuple_new"), _parse_int(tokens[:-3]))
        if suffix == "nāma-yuktau aṅkam gṛhyate":
            return Instruction(OpCode("named_tuple_get"), tokens[0])
        if suffix == "sambandha-hastaḥ nirmīyate":
            return Instruction(OpCode("handle_new"), tokens[0])
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
    import math as _math
    if _math.isnan(value):
        return "na-saṅkhyā"
    if _math.isinf(value):
        return "ṛṇa anatam" if value < 0 else "anatam"
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
    import math as _math
    if tokens == ["anatam"]:
        return _math.inf
    if tokens == ["ṛṇa", "anatam"]:
        return -_math.inf
    if tokens == ["na-saṅkhyā"]:
        return _math.nan
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
