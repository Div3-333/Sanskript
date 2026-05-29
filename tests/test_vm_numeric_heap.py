"""VM tests for push_float, mixed arithmetic, and arakṣita heap opcodes."""

from __future__ import annotations

import random
import unittest

from sanskript.bytecode import BytecodeProgram, FunctionBytecode, Instruction, OpCode
from sanskript.errors import RuntimeSanskriptError
from sanskript.vm import SanskriptVM


class VmNumericHeapTests(unittest.TestCase):
    def test_push_float_and_add(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_FLOAT, 1.5),
                Instruction(OpCode.PUSH_FLOAT, 2.5),
                Instruction(OpCode.ADD),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        self.assertEqual(SanskriptVM().execute(program), ["4.0"])

    def test_heap_in_arakshita_tier(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.STORE_NAME, "addr"),
                Instruction(OpCode.LOAD_NAME, "addr"),
                Instruction(OpCode.PUSH_INT, 42),
                Instruction(OpCode.HEAP_STORE),
                Instruction(OpCode.LOAD_NAME, "addr"),
                Instruction(OpCode.HEAP_LOAD),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            ),
            safety_tier="arakshita",
        )
        self.assertEqual(SanskriptVM().execute(program), ["42"])

    def test_heap_in_rakshita_requires_unsafe(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.HALT),
            ),
            safety_tier="rakshita",
        )
        with self.assertRaises(RuntimeSanskriptError):
            SanskriptVM().execute(program)

    def test_heap_in_rakshita_inside_unsafe(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.UNSAFE_ENTER),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.UNSAFE_EXIT),
                Instruction(OpCode.HALT),
            ),
            safety_tier="rakshita",
        )
        SanskriptVM().execute(program)

    def test_heap_free_invalidates_address(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.STORE_NAME, "addr"),
                Instruction(OpCode.LOAD_NAME, "addr"),
                Instruction(OpCode.HEAP_FREE),
                Instruction(OpCode.LOAD_NAME, "addr"),
                Instruction(OpCode.HEAP_LOAD),
                Instruction(OpCode.HALT),
            ),
            safety_tier="arakshita",
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "Invalid heap address"):
            SanskriptVM().execute(program)

    def test_heap_free_releases_entire_allocation_region(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 4),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.STORE_NAME, "base"),
                Instruction(OpCode.LOAD_NAME, "base"),
                Instruction(OpCode.HEAP_FREE),
                Instruction(OpCode.LOAD_NAME, "base"),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.ADD),
                Instruction(OpCode.HEAP_LOAD),
                Instruction(OpCode.HALT),
            ),
            safety_tier="arakshita",
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "Invalid heap address"):
            SanskriptVM().execute(program)

    def test_heap_free_rejects_non_base_pointer(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 2),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.ADD),
                Instruction(OpCode.HEAP_FREE),
                Instruction(OpCode.HALT),
            ),
            safety_tier="arakshita",
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "expected allocation base"):
            SanskriptVM().execute(program)

    def test_unsafe_scope_leak_has_diagnostic(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.UNSAFE_ENTER),
                Instruction(OpCode.HALT),
            ),
            safety_tier="rakshita",
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "unsafe scope leak"):
            SanskriptVM().execute(program)

    def test_fuzz_jump_if_zero_branches(self) -> None:
        rng = random.Random(1601)
        for _ in range(100):
            cond = rng.randint(0, 1)
            program = BytecodeProgram(
                (
                    Instruction(OpCode.PUSH_INT, cond),
                    Instruction(OpCode.JUMP_IF_ZERO, 5),
                    Instruction(OpCode.PUSH_INT, 11),
                    Instruction(OpCode.EMIT),
                    Instruction(OpCode.JUMP, 7),
                    Instruction(OpCode.PUSH_INT, 22),
                    Instruction(OpCode.EMIT),
                    Instruction(OpCode.HALT),
                )
            )
            output = SanskriptVM().execute(program)
            self.assertEqual(output, ["22"] if cond == 0 else ["11"])

    def test_call_arity_mismatch_reports_error(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.CALL, "f"),
                Instruction(OpCode.HALT),
            ),
            functions=(
                FunctionBytecode(
                    "f",
                    (
                        Instruction(OpCode.PUSH_INT, 0),
                        Instruction(OpCode.RETURN),
                    ),
                    params=("a", "b"),
                ),
            ),
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "Call arity mismatch"):
            SanskriptVM().execute(program)

    def test_endianness_u32_load_store_roundtrip(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 4),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.STORE_NAME, "addr"),
                Instruction(OpCode.LOAD_NAME, "addr"),
                Instruction(OpCode.PUSH_INT, 0x01020304),
                Instruction(OpCode.STORE_U32_BE),
                Instruction(OpCode.LOAD_NAME, "addr"),
                Instruction(OpCode.LOAD_U32_BE),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.LOAD_NAME, "addr"),
                Instruction(OpCode.LOAD_U32_LE),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            ),
            safety_tier="arakshita",
        )
        self.assertEqual(SanskriptVM().execute(program), ["16909060", "67305985"])

    def test_volatile_load_store_u32_le(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 4),
                Instruction(OpCode.HEAP_ALLOC),
                Instruction(OpCode.STORE_NAME, "addr"),
                Instruction(OpCode.LOAD_NAME, "addr"),
                Instruction(OpCode.PUSH_INT, 0xAABBCCDD),
                Instruction(OpCode.VOLATILE_STORE_U32_LE),
                Instruction(OpCode.LOAD_NAME, "addr"),
                Instruction(OpCode.VOLATILE_LOAD_U32_LE),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            ),
            safety_tier="arakshita",
        )
        self.assertEqual(SanskriptVM().execute(program), [str(0xAABBCCDD)])

    def test_jump_indirect_out_of_range_is_trapped(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 99),
                Instruction(OpCode.JUMP_INDIRECT),
                Instruction(OpCode.HALT),
            )
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "out of range"):
            SanskriptVM().execute(program)

    def test_shift_with_negative_amount_reports_vm_error(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 1),
                Instruction(OpCode.PUSH_INT, -1),
                Instruction(OpCode.SHIFT_LEFT),
                Instruction(OpCode.HALT),
            )
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "non-negative shift amount"):
            SanskriptVM().execute(program)

    def test_pointer_ops_rejected_in_surakshita(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 5),
                Instruction(OpCode.PTR_FROM_INT),
                Instruction(OpCode.HALT),
            ),
            safety_tier="surakshita",
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "only allowed in arak"):
            SanskriptVM().execute(program)

    def test_call_indirect_requires_string_target(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, 7),
                Instruction(OpCode.CALL_INDIRECT),
                Instruction(OpCode.HALT),
            )
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "expects string function target"):
            SanskriptVM().execute(program)

    def test_syscall_never_succeeds_silently(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.SYSCALL),
                Instruction(OpCode.HALT),
            ),
            safety_tier="arakshita",
        )
        with self.assertRaisesRegex(RuntimeSanskriptError, "not implemented"):
            SanskriptVM().execute(program)


if __name__ == "__main__":
    unittest.main()
