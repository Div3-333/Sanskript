from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from sanskript.bytecode import BytecodeProgram, FunctionBytecode, Instruction, OpCode
from sanskript.errors import RuntimeSanskriptError
from sanskript.native_backends import build_native_artifacts, host_target_triple, plan_to_dict
from sanskript.vm import SanskriptVM
from sanskript.yantra_patha import program_from_yantra_patha, program_to_yantra_patha


class Phase16ArakshitaTests(unittest.TestCase):
    def test_machine_memory_bitwise_register_and_atomic_paths(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.CALL_CONV, "sysv64"),
                Instruction(OpCode.PROLOGUE),
                Instruction(OpCode.PUSH_INT, 4),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.STORE_NAME, "ptr"),
                Instruction(OpCode.LOAD_NAME, "ptr"),
                Instruction(OpCode.PUSH_INT, 0x01020304),
                Instruction(OpCode.STORE_U32_LE),
                Instruction(OpCode.LOAD_NAME, "ptr"),
                Instruction(OpCode.LOAD_U32_LE),
                Instruction(OpCode.PUSH_INT, 8),
                Instruction(OpCode.ROTATE_LEFT32),
                Instruction(OpCode.REG_SET, "r0"),
                Instruction(OpCode.REG_GET, "r0"),
                Instruction(OpCode.PUSH_INT, 0x02030401),
                Instruction(OpCode.COMPARE_EQ),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.PUSH_INT, 64),
                Instruction(OpCode.SP_SET),
                Instruction(OpCode.SP_GET),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.LOAD_NAME, "ptr"),
                Instruction(OpCode.PUSH_INT, 0x01020304),
                Instruction(OpCode.PUSH_INT, 0xAABBCCDD),
                Instruction(OpCode.ATOMIC_CAS_U32_LE),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.LOAD_NAME, "ptr"),
                Instruction(OpCode.LOAD_U32_LE),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.EPILOGUE),
                Instruction(OpCode.HALT),
            ),
            safety_tier="arakshita",
        )
        self.assertEqual(SanskriptVM().execute(program), ["1", "64", "1", "2864434397"])

    def test_labels_jumps_mmio_and_indirect_call_with_syscall_host_fallback(self) -> None:
        fn = (
            Instruction(OpCode.PUSH_INT, 7),
            Instruction(OpCode.RETURN),
        )
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_TEXT, "callee"),
                Instruction(OpCode.CALL_INDIRECT),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.LABEL, "loop"),
                Instruction(OpCode.PUSH_INT, 100),
                Instruction(OpCode.PUSH_INT, 55),
                Instruction(OpCode.MMIO_WRITE),
                Instruction(OpCode.PUSH_INT, 100),
                Instruction(OpCode.MMIO_READ),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.SYSCALL, "yield"),
                Instruction(OpCode.POP),
                Instruction(OpCode.HALT),
            ),
            functions=(FunctionBytecode("callee", fn),),
            safety_tier="arakshita",
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "syscall is not implemented in the host VM backend"):
            SanskriptVM().execute(program)

    def test_endian_volatile_and_fence_semantics_are_executable(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 8),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.STORE_NAME, "ptr"),
                Instruction(OpCode.LOAD_NAME, "ptr"),
                Instruction(OpCode.PUSH_INT, 0x1234),
                Instruction(OpCode.STORE_U16_LE),
                Instruction(OpCode.LOAD_NAME, "ptr"),
                Instruction(OpCode.LOAD_U16_LE),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.LOAD_NAME, "ptr"),
                Instruction(OpCode.LOAD_U16_BE),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.LOAD_NAME, "ptr"),
                Instruction(OpCode.PUSH_INT, 0x01020304),
                Instruction(OpCode.VOLATILE_STORE_U32_LE),
                Instruction(OpCode.FENCE, "seq_cst"),
                Instruction(OpCode.LOAD_NAME, "ptr"),
                Instruction(OpCode.VOLATILE_LOAD_U32_LE),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.LOAD_NAME, "ptr"),
                Instruction(OpCode.LOAD_U32_BE),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            ),
            safety_tier="arakshita",
        )
        # 0x1234 stored LE reads as 0x3412 in BE view.
        self.assertEqual(
            SanskriptVM().execute(program),
            ["4660", "13330", "16909060", "67305985"],
        )

    def test_tier_boundaries_reject_machine_level_outside_allowed_context(self) -> None:
        surakshita = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 4),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.HALT),
            ),
            safety_tier="surakshita",
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "not allowed in surakṣita"):
            SanskriptVM().execute(surakshita)

        rakshita_without_unsafe = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 4),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.HALT),
            ),
            safety_tier="rakshita",
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "requires unsafe_enter"):
            SanskriptVM().execute(rakshita_without_unsafe)

        rakshita_ptr = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 7),
                Instruction(OpCode.PTR_FROM_INT),
                Instruction(OpCode.HALT),
            ),
            safety_tier="rakshita",
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "only allowed in arakṣita"):
            SanskriptVM().execute(rakshita_ptr)

    def test_jump_label_resolution_is_scoped_per_instruction_stream(self) -> None:
        callee = (
            Instruction(OpCode.PUSH_INT, 0),
            Instruction(OpCode.JUMP_LABEL, "loop"),
            Instruction(OpCode.PUSH_INT, 777),  # unreachable if label resolution is correct
            Instruction(OpCode.EMIT),  # unreachable if label resolution is correct
            Instruction(OpCode.LABEL, "loop"),
            Instruction(OpCode.PUSH_INT, 123),
            Instruction(OpCode.EMIT),
            Instruction(OpCode.PUSH_INT, 0),
            Instruction(OpCode.RETURN),
        )
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_TEXT, "callee"),
                Instruction(OpCode.CALL_INDIRECT),
                Instruction(OpCode.HALT),
            ),
            functions=(FunctionBytecode("callee", callee),),
            safety_tier="arakshita",
        )
        self.assertEqual(SanskriptVM().execute(program), ["123"])

    def test_yantra_roundtrip_for_phase16_opcodes(self) -> None:
        original = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.PTR_FROM_INT),
                Instruction(OpCode.PTR_TO_INT),
                Instruction(OpCode.PUSH_INT, 2),
                Instruction(OpCode.SHIFT_LEFT),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            ),
            safety_tier="arakshita",
        )
        rendered = program_to_yantra_patha(original)
        restored = program_from_yantra_patha(rendered)
        self.assertEqual(restored.instructions, original.instructions)
        self.assertEqual(restored.safety_tier, "arakshita")

    def test_native_backend_emits_symbol_relocation_and_linker_io_scaffolds(self) -> None:
        program = BytecodeProgram((Instruction(OpCode.HALT),), safety_tier="arakshita")
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            plan = build_native_artifacts(
                program=program,
                out_dir=out_dir,
                target=host_target_triple(),
                backend="native-object",
                artifact_kind="executable",
                attempt_link=False,
            )
            payload = plan_to_dict(plan)
            self.assertTrue(Path(payload["symbol_table_path"]).exists())
            self.assertTrue(Path(payload["relocations_path"]).exists())
            self.assertTrue(Path(payload["linker_io_path"]).exists())
            symbols = json.loads(Path(payload["symbol_table_path"]).read_text(encoding="utf-8"))
            self.assertTrue(any(item["name"] == "_sanskript_main" for item in symbols["symbols"]))


if __name__ == "__main__":
    unittest.main()
