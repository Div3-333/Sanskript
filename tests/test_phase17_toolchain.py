from __future__ import annotations

import random
import tempfile
import unittest
from pathlib import Path

from sanskript.bytecode import (
    BytecodeProgram,
    BytecodeValidationError,
    FunctionBytecode,
    Instruction,
    OpCode,
    dump_bytecode_file,
)
from sanskript.phase17_toolchain import (
    PHASE17_SPEC_VERSION,
    SSKYP_BINARY_MAGIC,
    deserialize_binary,
    deserialize_canonical_json,
    disassemble,
    freeze_phase17_spec,
    link_programs_phase17,
    load_program_any,
    opcode_machine_prose_map,
    optimize_program_phase17,
    parse_machine_prose,
    render_machine_prose,
    roundtrip_conformance,
    save_program_any,
    serialize_binary,
    serialize_canonical_json,
    verify_program_phase17,
)


def _program() -> BytecodeProgram:
    return BytecodeProgram(
        instructions=(
            Instruction(OpCode.PUSH_INT, 3),
            Instruction(OpCode.STORE_NAME, "n"),
            Instruction(OpCode.LOAD_NAME, "n"),
            Instruction(OpCode.CALL, "inc"),
            Instruction(OpCode.EMIT),
            Instruction(OpCode.HALT),
        ),
        functions=(
            FunctionBytecode(
                name="inc",
                instructions=(
                    Instruction(OpCode.LOAD_NAME, "x"),
                    Instruction(OpCode.PUSH_INT, 1),
                    Instruction(OpCode.ADD),
                    Instruction(OpCode.RETURN),
                ),
                params=("x",),
            ),
        ),
    )


class Phase17ToolchainTests(unittest.TestCase):
    def test_frozen_spec_layout_encoding_and_formats(self) -> None:
        spec = dict(freeze_phase17_spec())
        self.assertEqual(spec["version"], PHASE17_SPEC_VERSION)
        self.assertEqual(spec["file_formats"]["machine_prose"], ".sskyp")
        self.assertEqual(spec["file_formats"]["binary"], ".sskypb")
        self.assertIn("runtime_metadata", spec["layouts"])
        self.assertIn("opcode_index", spec["encoding"])
        self.assertIn("binary_layout", spec["encoding"])

    def test_verifier_and_opcode_prose_parity(self) -> None:
        report = verify_program_phase17(_program())
        self.assertTrue(report.ok)
        self.assertEqual(report.errors, ())
        self.assertEqual(report.warnings, ())
        mapping = opcode_machine_prose_map()
        self.assertEqual(len(mapping), len(list(OpCode)))
        self.assertEqual(len(set(mapping.values())), len(mapping))

    def test_optimizer_linker_and_conformance_roundtrip(self) -> None:
        optimized = optimize_program_phase17(_program())
        self.assertLessEqual(len(optimized.instructions), len(_program().instructions))

        helper = BytecodeProgram(
            instructions=(Instruction(OpCode.PUSH_INT, 9), Instruction(OpCode.HALT)),
            functions=(
                FunctionBytecode(
                    "double",
                    (
                        Instruction(OpCode.LOAD_NAME, "x"),
                        Instruction(OpCode.LOAD_NAME, "x"),
                        Instruction(OpCode.ADD),
                        Instruction(OpCode.RETURN),
                    ),
                    params=("x",),
                ),
            ),
        )
        linked = link_programs_phase17([optimized, helper])
        self.assertIn("inc", {fn.name for fn in linked.functions})
        self.assertIn("double", {fn.name for fn in linked.functions})
        self.assertEqual(linked.instructions[-1].opcode, OpCode.HALT)
        roundtrip_conformance(linked)

    def test_serializers_deserializers_and_disassembler(self) -> None:
        program = _program()
        canonical = serialize_canonical_json(program)
        restored = deserialize_canonical_json(canonical)
        self.assertEqual(restored, program)

        blob = serialize_binary(program)
        self.assertTrue(blob.startswith(SSKYP_BINARY_MAGIC))
        self.assertEqual(deserialize_binary(blob), program)

        prose = disassemble(program)
        self.assertIn("mukhyaḥ pāṭhaḥ ārabhyate.", prose)

    def test_loader_and_saver_support_all_phase17_formats(self) -> None:
        program = _program()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sskbc_path = root / "prog.sskbc"
            sskyp_path = root / "prog.sskyp"
            sskypb_path = root / "prog.sskypb"
            dump_bytecode_file(program, sskbc_path)
            save_program_any(program, sskyp_path)
            save_program_any(program, sskypb_path)

            self.assertEqual(load_program_any(sskbc_path), program)
            self.assertEqual(load_program_any(sskyp_path), program)
            self.assertEqual(load_program_any(sskypb_path), program)

    def test_binary_deserializer_rejects_corruption_and_truncation(self) -> None:
        blob = serialize_binary(_program())
        corrupted = bytearray(blob)
        corrupted[-1] ^= 0x01
        with self.assertRaises(BytecodeValidationError):
            deserialize_binary(bytes(corrupted))

        for cut in range(1, min(len(blob), 48)):
            with self.subTest(cut=cut):
                with self.assertRaises(BytecodeValidationError):
                    deserialize_binary(blob[:-cut])

    def test_binary_deserialize_rejects_fuzzed_payloads(self) -> None:
        original = serialize_binary(_program())
        rng = random.Random(17)
        rejected = 0
        for _ in range(64):
            mutated = bytearray(original)
            idx = rng.randrange(len(mutated))
            mutated[idx] ^= rng.randrange(1, 256)
            try:
                deserialize_binary(bytes(mutated))
            except BytecodeValidationError:
                rejected += 1
        self.assertEqual(rejected, 64)

    def test_canonical_deserialize_rejects_malformed_json_payloads(self) -> None:
        with self.assertRaises(BytecodeValidationError):
            deserialize_canonical_json("[]")
        with self.assertRaises(ValueError):
            deserialize_canonical_json("{not-json")

    def test_parser_rejects_unclosed_module_and_orphan_instruction(self) -> None:
        malformed = "\n".join(
            (
                "saṃskaraṇam dvitīyam.",
                "mukhyaḥ pāṭhaḥ ārabhyate.",
                "virāmaḥ kriyate.",
                "pāṭhaḥ samāpyate.",
                "gaṇita iti kṣetram ārabhyate.",
                "sthāpaya iti vidhānam ārabhyate.",
                "śūnya iti pūrṇāṅkaḥ nikṣipyate.",
                "pratyāvartanam kriyate.",
                "vidhānam samāpyate.",
            )
        )
        with self.assertRaises(BytecodeValidationError):
            parse_machine_prose(malformed)

        rendered = render_machine_prose(_program())
        with self.assertRaises(BytecodeValidationError):
            parse_machine_prose(rendered + "darśanam kriyate.\n")

    def test_link_rejects_duplicate_function_and_module(self) -> None:
        with self.assertRaises(BytecodeValidationError):
            link_programs_phase17([_program(), _program()])


if __name__ == "__main__":
    unittest.main()
