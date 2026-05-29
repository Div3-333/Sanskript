from __future__ import annotations

import unittest

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode
from sanskript.compiler import compile_source
from sanskript.errors import RuntimeSanskriptError, TypeCheckError
from sanskript.stdlib_core import call_native_function
from sanskript.vm import SanskriptVM


class Phase13MemoryModelTests(unittest.TestCase):
    def test_layout_and_allocation_semantics_enforced(self) -> None:
        block = call_native_function(
            "std.memory.alloc.heap",
            [8, 4, "abi", False, "sysv64", "global"],
        )
        layout = call_native_function("std.memory.layout.describe", [block])
        self.assertEqual(layout["size"], 8)
        self.assertEqual(layout["alignment"], 4)
        self.assertEqual(layout["layout"], "abi")
        self.assertEqual(layout["allocator"], "heap")
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function(
                "std.memory.alloc.heap",
                [8, 8, "abi", False, "c", "global"],
            )

    def test_aliasing_and_borrow_rules_enforced(self) -> None:
        block = call_native_function(
            "std.memory.alloc.heap",
            [4, 4, "native", False, "native", "r1"],
        )
        _shared = call_native_function("std.memory.borrow.shared", [block, "a"])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.memory.borrow.mut", [block, "a"])

    def test_mut_borrow_blocks_dealloc_and_mutation_until_release(self) -> None:
        block = call_native_function(
            "std.memory.alloc.heap",
            [4, 4, "native", False, "native", "r2"],
        )
        ref = call_native_function("std.memory.ref", [block, 0])
        borrow = call_native_function("std.memory.borrow.mut", [block, "a"])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.memory.dealloc", [block])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.memory.store_u8", [ref, 7])
        call_native_function("std.memory.borrow.release", [borrow])
        self.assertTrue(call_native_function("std.memory.store_u8", [ref, 7]))

    def test_mut_borrow_blocks_copy_and_clone_until_release(self) -> None:
        block = call_native_function(
            "std.memory.alloc.heap",
            [4, 4, "native", False, "native", "r2-copy"],
        )
        borrow = call_native_function("std.memory.borrow.mut", [block, "a"])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.memory.copy", [block])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.memory.clone", [block])
        call_native_function("std.memory.borrow.release", [borrow])
        copied = call_native_function("std.memory.copy", [block])
        self.assertEqual(
            call_native_function("std.memory.layout.describe", [copied])["size"],
            4,
        )

    def test_move_clone_drop_semantics_enforced(self) -> None:
        block = call_native_function(
            "std.memory.alloc.heap",
            [2, 1, "packed", True, "native", "r3"],
        )
        moved = call_native_function("std.memory.move", [block])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.memory.layout.describe", [block])
        cloned = call_native_function("std.memory.clone", [moved])
        self.assertTrue(call_native_function("std.memory.drop", [moved]))
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.memory.layout.describe", [moved])
        # Clone remains valid after source drop.
        self.assertEqual(
            call_native_function("std.memory.layout.describe", [cloned])["size"],
            2,
        )

    def test_atomic_and_fence_semantics(self) -> None:
        atom = call_native_function("std.memory.atomic.new", [11])
        self.assertEqual(call_native_function("std.memory.atomic.load", [atom]), 11)
        self.assertEqual(call_native_function("std.memory.atomic.fetch_add", [atom, 3]), 11)
        self.assertEqual(call_native_function("std.memory.atomic.load", [atom]), 14)
        fence_a = call_native_function("std.memory.atomic.fence", ["acquire"])
        fence_b = call_native_function("std.memory.atomic.fence", ["seq_cst"])
        self.assertGreater(fence_b, fence_a)
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.memory.atomic.fence", ["relaxed"])

    def test_volatile_access_requires_volatile_api(self) -> None:
        block = call_native_function(
            "std.memory.alloc.heap",
            [2, 1, "packed", True, "native", "mmio"],
        )
        vol = call_native_function("std.memory.volatile.ref", [block, 0])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.memory.store_u8", [vol, 1])
        self.assertTrue(call_native_function("std.memory.volatile.store_u8", [vol, 1]))
        self.assertEqual(call_native_function("std.memory.volatile.load_u8", [vol]), 1)

    def test_atomic_ref_blocks_non_atomic_access_on_same_location(self) -> None:
        block = call_native_function(
            "std.memory.alloc.heap",
            [4, 4, "native", False, "native", "r-atomic"],
        )
        ref = call_native_function("std.memory.ref", [block, 0])
        atom = call_native_function("std.memory.atomic.ref", [ref])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.memory.store_u8", [ref, 2])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.memory.load_u8", [ref])
        self.assertTrue(call_native_function("std.memory.atomic.store", [atom, 9]))
        self.assertEqual(call_native_function("std.memory.atomic.load", [atom]), 9)
        self.assertEqual(call_native_function("std.memory.alias.state", [block])["atomic_locations"], 1)

    def test_unsafe_and_lifetime_still_enforced_by_checker(self) -> None:
        with self.assertRaises(TypeCheckError):
            compile_source(
                """
                rakṣitam.
                arakṣitaḥ adhikāraḥ ārabhyate.
                avakāśaḥ s eka.
                arakṣitaḥ adhikāraḥ samāpyate.
                """
            )

    def test_phase13_source_example_executes(self) -> None:
        program = compile_source(
            """
            rakṣitam.
            arakṣitaḥ adhikāraḥ ārabhyate pramāṇam vākyam phase13-heap-proof iti.
            avakāśaḥ sthāna eka.
            smṛtisthāpanam sthāna sapta.
            smṛtyāharaṇam phala sthāna.
            smṛtimokṣaḥ sthāna.
            arakṣitaḥ adhikāraḥ samāpyate.
            gaṇakaḥ phalaṃ darśayati.
            """
        )
        self.assertEqual(SanskriptVM().execute(program), ["7"])

    def test_vm_heap_access_requires_unsafe_in_rakshita(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            SanskriptVM().execute(
                BytecodeProgram(
                    (
                        Instruction(OpCode.PUSH_INT, 4),
                        Instruction(OpCode.HEAP_ALLOC),
                        Instruction(OpCode.HALT),
                    ),
                    safety_tier="rakshita",
                )
            )

    def test_vm_raw_pointer_ops_are_arakshita_only(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            SanskriptVM().execute(
                BytecodeProgram(
                    (
                        Instruction(OpCode.PUSH_INT, 7),
                        Instruction(OpCode.PTR_FROM_INT),
                        Instruction(OpCode.HALT),
                    ),
                    safety_tier="rakshita",
                )
            )


if __name__ == "__main__":
    unittest.main()
