"""Phase 23 concurrency and async coverage (stress + negative misuse)."""

from __future__ import annotations

import io
import json
import re
import tempfile
import threading
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from sanskript.cli import main as cli_main
from sanskript.ast import Program, TypeAliasDecl
from sanskript.compiler import compile_source
from sanskript.errors import RuntimeSanskriptError, TypeCheckError
from sanskript.type_checker import check_program
from sanskript.phase23_concurrency import (
    PHASE23_BLOCKING_ASYNC_SURFACES,
    PHASE23_HOST_CHECKLIST_SLUGS,
    PHASE23_HOST_SEAL_BAR,
    PHASE23_VM_MISSING_SURFACES,
    _RACE_ACCESS_LOG,
    phase23_full_seal_payload,
    phase23_seal_verdict,
    verify_phase23_anti_fake,
    verify_phase23_full_seal,
)
from sanskript.runtime_values import NIL, OpaqueHandle, OptionValue
from sanskript.stdlib_core import call_native_function, list_native_functions
from sanskript.vm import SanskriptVM

ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "docs" / "native-sanskript-independence-checklist.md"
PHASE23_DOC = ROOT / "docs" / "phase23-concurrency-async.md"
FULL_SEAL = ROOT / "examples" / "phase23-full-seal.ssk"

# Host-tier seal bar rows (functional_host + scaffold) — must be [x] in checklist.
PHASE23_HOST_SEAL_CHECKED = (
    "Threads.",
    "Fibers/coroutines.",
    "Futures/promises.",
    "Timers.",
    "Async file I/O.",
    "Async networking.",
    "Cancellation.",
    "Channels.",
    "Queues.",
    "Mutexes.",
    "Read-write locks.",
    "Semaphores.",
    "Atomics.",
    "Thread pools.",
    "Work stealing if needed.",
    "Data race checking for `rakṣita`.",
    "Unsafe concurrent memory rules for `arakṣita`.",
    "Browser worker support.",
)

# VM tier blockers — must stay [ ] until OP_AWAIT / in-language scheduler exist.
PHASE23_VM_MISSING_UNCHECKED = (
    "Async functions.",
    "Await.",
    "Event loop.",
    "Structured concurrency.",
)


class Phase23RegistryTests(unittest.TestCase):
    def test_phase23_namespaces_registered(self) -> None:
        names = list_native_functions()
        for prefix in (
            "std.thread.",
            "std.fiber.",
            "std.async.",
            "std.sync.mutex.",
            "std.sync.rwlock.",
            "std.sync.semaphore.",
            "std.sync.queue.",
            "std.concurrent.",
            "std.web.worker.",
            "std.phase23.",
        ):
            self.assertTrue(any(name.startswith(prefix) for name in names), prefix)


class Phase23ThreadFiberAsyncTests(unittest.TestCase):
    def setUp(self) -> None:
        _RACE_ACCESS_LOG.clear()

    def test_thread_spawn_join_and_pool_work_stealing(self) -> None:
        thread = call_native_function(
            "std.thread.spawn",
            [{"symbol": "std.math.max", "args": [3, 7]}],
        )
        self.assertIsInstance(thread, OpaqueHandle)
        joined = call_native_function("std.thread.join", [thread, 500])
        self.assertIsInstance(joined, OptionValue)
        self.assertTrue(joined.present)
        self.assertEqual(joined.value, 7)

        pool = call_native_function("std.thread.pool.new", [2])
        future = call_native_function(
            "std.thread.pool.submit",
            [pool, {"symbol": "std.math.min", "args": [9, 4]}],
        )
        stolen = call_native_function("std.thread.pool.steal_work", [pool])
        self.assertIsInstance(stolen, dict)
        polled = call_native_function("std.async.future.poll", [future])
        call_native_function("std.thread.pool.shutdown", [pool])
        self.assertTrue(polled["ready"])

    def test_fiber_coroutine_steps(self) -> None:
        fiber = call_native_function("std.fiber.create", [["a", "b", "c"]])
        seen: list[object] = []
        for _ in range(4):
            step = call_native_function("std.fiber.resume", [fiber])
            seen.append(step)
            if step["done"]:
                break
        self.assertEqual([row["value"] for row in seen[:3]], ["a", "b", "c"])
        self.assertTrue(seen[-1]["done"])

    def test_async_event_loop_timer_and_await(self) -> None:
        future = call_native_function(
            "std.async.timer.after_ms",
            [30, {"symbol": "std.math.sqrt", "args": [16]}],
        )
        time.sleep(0.08)
        call_native_function("std.async.event_loop.drain", [500])
        polled = call_native_function("std.async.future.poll", [future])
        self.assertTrue(polled["ready"])
        self.assertEqual(float(polled["value"]), 4.0)
        waited = call_native_function("std.async.await", [future, 10])
        self.assertEqual(float(waited), 4.0)

    def test_async_scope_structured_concurrency(self) -> None:
        results = call_native_function(
            "std.async.scope.run",
            [
                [
                    {"symbol": "std.math.max", "args": [1, 3]},
                    {"symbol": "std.math.min", "args": [8, 2]},
                ]
            ],
        )
        self.assertEqual(results, [3, 2])

    def test_async_file_io_and_network_probe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "phase23.txt")
            call_native_function("std.async.write_text", [path, "async-io"])
            text = call_native_function("std.async.read_text", [path])
            self.assertEqual(text, "async-io")
        probe = call_native_function("std.async.net.connect", ["127.0.0.1", 9, 50])
        self.assertIn("ok", probe)
        self.assertIn("latency_ms", probe)

    def test_cancellation_token(self) -> None:
        token = call_native_function("std.async.cancel.new", [])
        self.assertFalse(call_native_function("std.async.cancel.is_cancelled", [token]))
        call_native_function("std.async.cancel.request", [token])
        self.assertTrue(call_native_function("std.async.cancel.is_cancelled", [token]))
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.async.cancel.check", [token])


class Phase23SyncPrimitivesTests(unittest.TestCase):
    def test_mutex_rwlock_semaphore_queue(self) -> None:
        mutex = call_native_function("std.sync.mutex.new", [])
        self.assertTrue(call_native_function("std.sync.mutex.acquire", [mutex, 50]))
        self.assertTrue(call_native_function("std.sync.mutex.release", [mutex]))

        rw = call_native_function("std.sync.rwlock.new", [])
        self.assertTrue(call_native_function("std.sync.rwlock.acquire_read", [rw, 50]))
        self.assertTrue(call_native_function("std.sync.rwlock.release", [rw]))
        self.assertTrue(call_native_function("std.sync.rwlock.acquire_write", [rw, 50]))
        self.assertTrue(call_native_function("std.sync.rwlock.release", [rw]))

        sem = call_native_function("std.sync.semaphore.new", [1])
        self.assertTrue(call_native_function("std.sync.semaphore.acquire", [sem, 50]))
        self.assertTrue(call_native_function("std.sync.semaphore.release", [sem]))

        queue = call_native_function("std.sync.queue.new", [2])
        self.assertTrue(call_native_function("std.sync.queue.enqueue", [queue, {"n": 1}]))
        got = call_native_function("std.sync.queue.dequeue", [queue, 50])
        self.assertEqual(got, {"n": 1})

    def test_atomics_and_channels_still_available(self) -> None:
        atom = call_native_function("std.sync.atomic.new", [1])
        self.assertEqual(call_native_function("std.sync.atomic.fetch_add", [atom, 4]), 1)
        ch = call_native_function("std.sync.channel.new", [1])
        self.assertTrue(call_native_function("std.sync.channel.send", [ch, 42]))
        self.assertEqual(call_native_function("std.sync.channel.recv", [ch, 50]), 42)

    def test_atomic_fetch_add_parallel_stress(self) -> None:
        atom = call_native_function("std.sync.atomic.new", [0])
        workers = 8
        increments = 50
        barrier = threading.Barrier(workers)
        errors: list[BaseException] = []

        def worker() -> None:
            try:
                barrier.wait(timeout=10)
                for _ in range(increments):
                    call_native_function("std.sync.atomic.fetch_add", [atom, 1])
            except BaseException as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(workers)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=30)
        self.assertEqual(errors, [])
        self.assertEqual(
            call_native_function("std.sync.atomic.load", [atom]),
            workers * increments,
        )

    def test_channel_producer_consumer_stress(self) -> None:
        channel = call_native_function("std.sync.channel.new", [64])
        message_count = 200
        received: list[int] = []
        lock = threading.Lock()

        def consumer() -> None:
            for _ in range(message_count):
                value = call_native_function("std.sync.channel.recv", [channel, 5000])
                if isinstance(value, OptionValue) and not value.present:
                    raise AssertionError("channel recv timed out")
                with lock:
                    received.append(int(value))

        consumer_thread = threading.Thread(target=consumer)
        consumer_thread.start()
        producers = [
            threading.Thread(
                target=lambda i=i: call_native_function(
                    "std.sync.channel.send", [channel, i]
                )
            )
            for i in range(message_count)
        ]
        for producer in producers:
            producer.start()
        for producer in producers:
            producer.join(timeout=30)
        consumer_thread.join(timeout=30)
        self.assertEqual(len(received), message_count)
        self.assertEqual(set(received), set(range(message_count)))

    def test_atomic_fetch_add_thread_safe_under_contention(self) -> None:
        atom = call_native_function("std.sync.atomic.new", [0])
        thread_count = 8
        adds_per_thread = 400
        barrier = threading.Barrier(thread_count)
        errors: list[BaseException] = []

        def worker() -> None:
            try:
                barrier.wait(timeout=5)
                for _ in range(adds_per_thread):
                    call_native_function("std.sync.atomic.fetch_add", [atom, 1])
            except BaseException as exc:  # noqa: BLE001
                errors.append(exc)

        workers = [threading.Thread(target=worker) for _ in range(thread_count)]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(timeout=30)
        self.assertEqual(errors, [])
        self.assertEqual(
            call_native_function("std.sync.atomic.load", [atom]),
            thread_count * adds_per_thread,
        )


class Phase23BlockingAsyncHonestyTests(unittest.TestCase):
    def test_async_sleep_ms_blocks_calling_host_thread(self) -> None:
        """std.async.sleep_ms uses time.sleep on the caller — not VM cooperative await."""
        start = time.monotonic()
        returned = call_native_function("std.async.sleep_ms", [60])
        elapsed = time.monotonic() - start
        self.assertEqual(returned, 60)
        self.assertGreaterEqual(elapsed, 0.045)

    def test_async_sleep_ms_holds_thread_until_delay_elapses(self) -> None:
        done = threading.Event()
        elapsed_ms: list[int] = []

        def sleeper() -> None:
            start = time.monotonic()
            call_native_function("std.async.sleep_ms", [90])
            elapsed_ms.append(int((time.monotonic() - start) * 1000))
            done.set()

        thread = threading.Thread(target=sleeper)
        thread.start()
        early = time.monotonic()
        while not done.is_set() and time.monotonic() - early < 0.04:
            time.sleep(0.005)
        self.assertFalse(done.is_set(), "sleep should block the worker thread for ~90ms")
        thread.join(timeout=2.0)
        self.assertTrue(done.is_set())
        self.assertGreaterEqual(elapsed_ms[0], 70)


class Phase23RaceAndTierTests(unittest.TestCase):
    def setUp(self) -> None:
        _RACE_ACCESS_LOG.clear()

    def test_rakshita_data_race_detection(self) -> None:
        call_native_function(
            "std.concurrent.race.record",
            [
                [
                    {"var": "counter", "mode": "write", "thread_id": 1},
                    {"var": "counter", "mode": "write", "thread_id": 2},
                ]
            ],
        )
        races = call_native_function("std.concurrent.race.detect", [])
        self.assertEqual(len(races), 1)
        self.assertEqual(races[0]["kind"], "write-write")
        call_native_function("std.concurrent.race.clear", [])

    def test_arakshita_unsafe_concurrent_policy(self) -> None:
        self.assertTrue(
            call_native_function(
                "std.concurrent.arakshita.check",
                [{"tier": "arakshita", "operation": "channel_send", "unsafe_region": True}],
            )
        )
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function(
                "std.concurrent.arakshita.check",
                [{"tier": "arakshita", "operation": "channel_send", "unsafe_region": False}],
            )

    def test_arakshita_channel_alias_rejected_at_compile_time(self) -> None:
        program = Program((), type_aliases=(TypeAliasDecl("ch", "channel"),), safety_tier="arakshita")
        with self.assertRaises(TypeCheckError):
            check_program(program)


class Phase23NegativeMisuseTests(unittest.TestCase):
    def test_mutex_release_without_acquire_fails(self) -> None:
        mutex = call_native_function("std.sync.mutex.new", [])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.sync.mutex.release", [mutex])

    def test_queue_non_send_safe_payload_rejected(self) -> None:
        queue = call_native_function("std.sync.queue.new", [1])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.sync.queue.enqueue", [queue, bytearray(b"x")])

    def test_web_worker_send_and_terminate(self) -> None:
        worker = call_native_function("std.web.worker.spawn", ["phase23-worker"])
        call_native_function("std.web.worker.post_message", [worker, "ping"])
        reply = call_native_function("std.web.worker.recv", [worker, 500])
        self.assertIsInstance(reply, dict)
        self.assertEqual(reply.get("echo"), "pong")
        self.assertTrue(call_native_function("std.web.worker.terminate", [worker]))
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.web.worker.post_message", [worker, "late"])

    def test_stress_many_thread_spawns(self) -> None:
        threads = [
            call_native_function(
                "std.thread.spawn",
                [{"symbol": "std.math.max", "args": [i, i + 1]}],
            )
            for i in range(12)
        ]
        for handle in threads:
            joined = call_native_function("std.thread.join", [handle, 1000])
            self.assertTrue(joined.present)

    def test_fiber_many_resume_stress(self) -> None:
        fiber = call_native_function("std.fiber.create", [list(range(64))])
        values: list[object] = []
        for _ in range(65):
            step = call_native_function("std.fiber.resume", [fiber])
            values.append(step["value"])
            if step["done"]:
                break
        self.assertEqual(values[:64], list(range(64)))
        self.assertTrue(values[-1] == 63 or values[-1] == 62)

    def test_thread_pool_steal_work_stress(self) -> None:
        pool = call_native_function("std.thread.pool.new", [2])
        futures = [
            call_native_function(
                "std.thread.pool.submit",
                [pool, {"symbol": "std.math.max", "args": [i, i + 1]}],
            )
            for i in range(8)
        ]
        stolen = [call_native_function("std.thread.pool.steal_work", [pool]) for _ in range(8)]
        self.assertGreater(sum(1 for item in stolen if item is not NIL), 0)
        for future in futures:
            deadline = time.monotonic() + 3.0
            while time.monotonic() < deadline:
                if call_native_function("std.async.future.poll", [future])["ready"]:
                    break
                time.sleep(0.01)
            else:
                self.fail("pool future not ready before shutdown")
        call_native_function("std.thread.pool.shutdown", [pool])

    def test_web_worker_message_burst_stress(self) -> None:
        worker = call_native_function("std.web.worker.spawn", ["phase23-burst"])
        for _ in range(16):
            call_native_function("std.web.worker.post_message", [worker, "ping"])
        replies = 0
        for _ in range(16):
            reply = call_native_function("std.web.worker.recv", [worker, 500])
            if isinstance(reply, dict) and reply.get("ok"):
                replies += 1
        call_native_function("std.web.worker.terminate", [worker])
        self.assertGreaterEqual(replies, 8)

    def test_rakshita_race_detect_many_events_stress(self) -> None:
        events = [
            {"var": f"v{i % 4}", "mode": "write" if i % 2 else "read", "thread_id": i % 3}
            for i in range(120)
        ]
        call_native_function("std.concurrent.race.record", [events])
        races = call_native_function("std.concurrent.race.detect", [])
        self.assertGreater(len(races), 0)
        call_native_function("std.concurrent.race.clear", [])


class Phase23FullSealTests(unittest.TestCase):
    def test_phase23_host_checklist_slug_count(self) -> None:
        self.assertEqual(len(PHASE23_HOST_CHECKLIST_SLUGS), 19)

    def test_phase23_doc_declares_host_tier_full_seal(self) -> None:
        self.assertTrue(PHASE23_DOC.is_file())
        text = PHASE23_DOC.read_text(encoding="utf-8")
        self.assertIn("SEALED at host tier", text)
        self.assertIn("phase23-full-seal.ssk", text)
        self.assertIn("vm_missing", text)

    def test_phase23_seal_run_native_passes(self) -> None:
        payload = call_native_function("std.phase23.seal_run", [])
        self.assertEqual(payload["verdict"], "SEALED_AT_HOST_TIER")
        self.assertEqual(payload["marker_count"], 19)
        self.assertEqual(payload["checklist_count"], 19)
        self.assertEqual(len(payload["errors"]), 0)
        for slug in PHASE23_HOST_CHECKLIST_SLUGS:
            self.assertIn(f"P23_SEAL:{slug}:ok", payload["markers"])

    def test_phase23_full_seal_example_executes(self) -> None:
        if not FULL_SEAL.is_file():
            self.skipTest("phase23 full seal example missing")
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cli_main(["run", str(FULL_SEAL)])
        self.assertEqual(code, 0)
        out = buf.getvalue()
        payload = json.loads(out.strip().splitlines()[-1])
        self.assertEqual(payload["verdict"], "SEALED_AT_HOST_TIER")
        for slug in PHASE23_HOST_CHECKLIST_SLUGS:
            self.assertIn(f"P23_SEAL:{slug}:ok", payload["markers"])


class Phase23SealGatekeeperTests(unittest.TestCase):
    def test_phase23_doc_declares_dual_tier_host_seal(self) -> None:
        self.assertTrue(PHASE23_DOC.is_file())
        doc_text = PHASE23_DOC.read_text(encoding="utf-8")
        verdict = phase23_seal_verdict()
        self.assertEqual(verdict["verdict"], "dual_tier_host_seal")
        self.assertIn("SEALED at host tier", doc_text)
        self.assertIn(verdict["verdict"], doc_text)
        self.assertIn("vm_missing", doc_text)
        self.assertIn("OP_AWAIT", doc_text)
        section = CHECKLIST.read_text(encoding="utf-8").split("## Phase 23:")[1].split("## Phase 24:")[0]
        self.assertIn("SEALED at host tier", section)
        self.assertIn(verdict["verdict"], section)
        self.assertIn("vm_missing", section)

    def test_phase23_checklist_ticks_host_rows_leaves_vm_missing_open(self) -> None:
        section = CHECKLIST.read_text(encoding="utf-8").split("## Phase 23:")[1].split("## Phase 24:")[0]
        for needle in PHASE23_HOST_SEAL_CHECKED:
            self.assertRegex(section, rf"- \[x\] {re.escape(needle)}")
        for needle in PHASE23_VM_MISSING_UNCHECKED:
            self.assertRegex(section, rf"- \[ \] {re.escape(needle)}")

    def test_phase23_anti_fake_gatekeeper_clean(self) -> None:
        self.assertEqual(verify_phase23_anti_fake(), [])

    def test_phase23_inventory_honest_dual_tier(self) -> None:
        rows = {row["name"]: row for row in call_native_function("std.phase23.inventory", [])}
        for name in PHASE23_HOST_SEAL_BAR:
            row = rows[name]
            self.assertEqual(row["host_tier"], "functional_host", name)
            self.assertTrue(row.get("thread_safe"), name)
        for name in PHASE23_VM_MISSING_SURFACES:
            if name == "async_future":
                continue
            row = rows[name]
            self.assertEqual(row["vm_tier"], "vm_missing", name)
            notes = " ".join(str(n) for n in row["notes"]).casefold()
            self.assertTrue("op_await" in notes or "vm" in notes, name)
        for name in PHASE23_BLOCKING_ASYNC_SURFACES:
            row = rows[name]
            notes = " ".join(str(n) for n in row["notes"]).casefold()
            self.assertIn("blocking", notes, name)

    def test_phase23_seal_verdict_host_sealed_vm_blocked(self) -> None:
        verdict = call_native_function("std.phase23.seal_verdict", [])
        self.assertEqual(verdict["verdict"], "dual_tier_host_seal")
        self.assertTrue(verdict["host_tier"]["sealed"])
        self.assertTrue(verdict["host_tier"]["atomics_thread_safe"])
        self.assertTrue(verdict["host_tier"]["channels_thread_safe"])
        self.assertFalse(verdict["vm_tier"]["sealed"])
        self.assertTrue(verdict["no_fake_async"])
        self.assertGreater(len(verdict["vm_tier"]["blockers"]), 0)
        self.assertEqual(verdict, phase23_seal_verdict())

    def test_verify_phase23_full_seal_passes(self) -> None:
        self.assertEqual(verify_phase23_full_seal(), [])

    def test_phase23_full_seal_payload_ready(self) -> None:
        payload = phase23_full_seal_payload()
        self.assertTrue(payload["full_seal_ready"])
        self.assertEqual(payload["status"], "dual_tier_host_seal")
        self.assertEqual(payload["violations"], [])

    def test_cli_phase23_seal_command(self) -> None:
        import io
        import sys

        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            code = cli_main(["phase23-seal"])
        finally:
            sys.stdout = old_stdout
        self.assertEqual(code, 0)
        out = buf.getvalue()
        self.assertIn("full_seal_ready=True", out)
        self.assertIn("dual_tier_host_seal", out)


class Phase23ExampleTests(unittest.TestCase):
    def test_phase23_example_present(self) -> None:
        root = Path(__file__).resolve().parents[1]
        example = root / "examples" / "phase23-concurrency-async.ssk"
        if not example.is_file():
            self.skipTest("phase23 example missing")
        text = example.read_text(encoding="utf-8")
        self.assertIn("std.sync.rwlock.acquire_read", text)
        self.assertIn("std.async.sleep_ms", text)
        self.assertIn("phase 23", text.casefold())
        self.assertIn("phalaṃ darśayati", text)

    def test_phase23_example_executes(self) -> None:
        root = Path(__file__).resolve().parents[1]
        example = root / "examples" / "phase23-concurrency-async.ssk"
        if not example.is_file():
            self.skipTest("phase23 example missing")
        self.assertEqual(cli_main(["run", str(example)]), 0)


if __name__ == "__main__":
    unittest.main()
