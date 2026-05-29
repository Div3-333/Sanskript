"""Phase 15 rakṣita systems capability tests."""

from __future__ import annotations

import unittest

from sanskript.compiler import compile_source
from sanskript.errors import RuntimeSanskriptError, TypeCheckError, PanicError, ThrownError
from sanskript.runtime_values import OpaqueHandle, OptionValue, ResultValue
from sanskript.stdlib_core import call_native_function, list_native_functions
from sanskript.vm import SanskriptVM


class Phase15RegistryTests(unittest.TestCase):
    def test_phase15_namespaces_registered(self) -> None:
        names = list_native_functions()
        for prefix in ("std.sync.", "std.thread.marker.", "std.ffi.", "std.net."):
            self.assertTrue(any(name.startswith(prefix) for name in names), prefix)


class Phase15SafetyTests(unittest.TestCase):
    def test_rakshita_unsafe_requires_proof_annotation(self) -> None:
        with self.assertRaises(TypeCheckError):
            compile_source(
                """
                rakṣitam.
                arakṣitaḥ adhikāraḥ ārabhyate.
                avakāśaḥ s eka.
                arakṣitaḥ adhikāraḥ samāpyate.
                """
            )

    def test_rakshita_unsafe_with_proof_compiles(self) -> None:
        program = compile_source(
            """
            rakṣitam.
            arakṣitaḥ adhikāraḥ ārabhyate pramāṇam vākyam owner-not-aliased iti.
            avakāśaḥ s eka.
            smṛtimokṣaḥ s.
            arakṣitaḥ adhikāraḥ samāpyate.
            """
        )
        self.assertEqual(program.safety_tier, "rakshita")

    def test_try_handler_does_not_inherit_unsafe_scope(self) -> None:
        program = compile_source(
            """
            rakṣitam.
            āgrahītvā doṣaḥ.
            arakṣitaḥ adhikāraḥ ārabhyate pramāṇam vākyam catch-scope-proof iti.
            vikṣepaḥ vākyam escaped iti.
            anyathā.
            avakāśaḥ sthāna eka.
            smṛtimokṣaḥ sthāna.
            antam.
            """
        )
        with self.assertRaises(RuntimeSanskriptError):
            SanskriptVM().execute(program)

    def test_rakshita_unsafe_requires_explicit_proof_marker(self) -> None:
        with self.assertRaises(TypeCheckError):
            compile_source(
                """
                rakṣitam.
                arakṣitaḥ adhikāraḥ ārabhyate owner-not-aliased iti.
                avakāśaḥ s eka.
                smṛtimokṣaḥ s.
                arakṣitaḥ adhikāraḥ samāpyate.
                """
            )


class Phase15SyncFfiNetTests(unittest.TestCase):
    def test_atomic_lock_channel_primitives(self) -> None:
        atom = call_native_function("std.sync.atomic.new", [3])
        self.assertIsInstance(atom, OpaqueHandle)
        self.assertEqual(call_native_function("std.sync.atomic.fetch_add", [atom, 2]), 3)
        self.assertEqual(call_native_function("std.sync.atomic.load", [atom]), 5)
        cas = call_native_function("std.sync.atomic.compare_exchange", [atom, 5, 9])
        self.assertIsInstance(cas, ResultValue)
        self.assertTrue(cas.ok)
        self.assertEqual(call_native_function("std.sync.atomic.load", [atom]), 9)

        lock = call_native_function("std.sync.lock.new", [])
        self.assertTrue(call_native_function("std.sync.lock.acquire", [lock, 50]))
        self.assertTrue(call_native_function("std.sync.lock.release", [lock]))

        ch = call_native_function("std.sync.channel.new", [1])
        self.assertTrue(call_native_function("std.sync.channel.send", [ch, {"k": 1}]))
        self.assertEqual(call_native_function("std.sync.channel.recv", [ch, 5]), {"k": 1})
        empty = call_native_function("std.sync.channel.try_recv", [ch])
        self.assertIsInstance(empty, OptionValue)
        self.assertFalse(empty.present)

    def test_send_share_and_ffi_boundary(self) -> None:
        self.assertTrue(call_native_function("std.thread.marker.send", [{"k": [1, 2]}]))
        self.assertFalse(call_native_function("std.thread.marker.send", [bytearray(b"abc")]))
        self.assertFalse(
            call_native_function("std.thread.marker.send", [OpaqueHandle(kind="mem.block", handle_id=9999)])
        )

        self.assertTrue(
            call_native_function(
                "std.ffi.abi_stable_struct",
                [
                    {
                        "name": "Pair",
                        "fields": [
                            {"name": "a", "type": "i32", "offset": 0},
                            {"name": "b", "type": "i32", "offset": 4},
                        ],
                    }
                ],
            )
        )
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function(
                "std.ffi.abi_stable_struct",
                [
                    {
                        "name": "BadDup",
                        "fields": [
                            {"name": "a", "type": "i32", "offset": 0},
                            {"name": "a", "type": "i32", "offset": 4},
                        ],
                    }
                ],
            )
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function(
                "std.ffi.abi_stable_struct",
                [
                    {
                        "name": "BadSize",
                        "size": 16,
                        "fields": [
                            {"name": "a", "type": "i32", "offset": 0},
                            {"name": "b", "type": "i32", "offset": 4},
                        ],
                    }
                ],
            )
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function(
                "std.ffi.call_checked",
                ["std.file.read_text", [OpaqueHandle(kind="channel", handle_id=1)]],
            )
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.ffi.call_checked", ["std.process.run", [["echo", "x"]]])

    def test_lock_channel_misuse_is_rejected(self) -> None:
        lock = call_native_function("std.sync.lock.new", [])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.sync.lock.release", [lock])
        ch = call_native_function("std.sync.channel.new", [0])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.sync.channel.send", [ch, bytearray(b"mutable")])

    def test_network_and_error_split(self) -> None:
        resolved = call_native_function("std.net.resolve_host", ["localhost"])
        self.assertTrue(isinstance(resolved, list) and resolved)
        self.assertFalse(call_native_function("std.net.tcp_probe", ["127.0.0.1", 9, 50]))

        with self.assertRaises(ThrownError):
            SanskriptVM().execute(compile_source("vikṣepaḥ vākyam recoverable iti."))
        with self.assertRaises(PanicError):
            SanskriptVM().execute(compile_source("vipattim vākyam fatal iti."))


if __name__ == "__main__":
    unittest.main()
