"""Phase 21 cross-platform system support tests."""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from sanskript.cli import main
from sanskript.compiler import compile_program
from sanskript.module_loader import load_program_from_path
from sanskript.errors import RuntimeSanskriptError
from sanskript.phase21_cross_platform import (
    PHASE21_CHECKLIST_ROWS,
    Phase21EvidenceRequest,
    browser_fetch_simulation,
    generate_phase21_evidence,
    host_platform_family,
    join_path_for_platform,
    normalize_path_for_platform,
    parse_phase21_checklist_markers,
    phase21_platform_matrix,
    phase21_seal_verdict,
    platform_compile_plan,
    probe_file_watch_capability,
    probe_network_capability,
    probe_process_capability,
    probe_storage_capability,
    probe_terminal_capability,
)
from sanskript.runtime_values import NilValue
from sanskript.stdlib_core import call_native_function, has_native_function, list_native_functions
from sanskript.vm import SanskriptVM

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "phase21-cross-platform.ssk"
CHECKLIST = ROOT / "docs" / "native-sanskript-independence-checklist.md"


class Phase21RegistryTests(unittest.TestCase):
    def test_phase21_std_namespaces_registered(self) -> None:
        names = list_native_functions()
        for prefix in (
            "std.path.for_platform",
            "std.path.web_normalize",
            "std.watch.",
            "std.storage.web_",
            "std.platform.",
            "std.process.run_for_platform",
            "std.process.web_",
            "std.net.dns_lookup",
            "std.net.tls_",
            "std.net.browser_fetch_plan",
            "std.net.browser_fetch_sim",
            "std.console.log",
            "std.terminal.is_tty",
        ):
            self.assertTrue(any(name.startswith(prefix) or name == prefix for name in names), prefix)


class Phase21PathTests(unittest.TestCase):
    def test_windows_mac_linux_path_join_semantics(self) -> None:
        win = join_path_for_platform("windows", "Users", "App", "main.ssk")
        self.assertIn("\\", win)
        linux = join_path_for_platform("linux", "usr", "bin", "sanskript")
        self.assertEqual(linux, "usr/bin/sanskript")
        mac = join_path_for_platform("macos", "Applications", "Sanskript.app")
        self.assertEqual(mac, "Applications/Sanskript.app")

    def test_web_virtual_path_normalize(self) -> None:
        joined = join_path_for_platform("web", "app", "data")
        self.assertTrue(joined.startswith("/virtual/"))
        norm = normalize_path_for_platform("web", "app/../etc/./hosts")
        self.assertTrue(norm.startswith("/"))
        self.assertIn("etc", norm)
        self.assertNotIn("..", norm)

    def test_path_for_platform_negative_unknown_platform(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.path.for_platform", ["bsd", ["a"]])

    def test_path_separator_values(self) -> None:
        self.assertEqual(call_native_function("std.path.separator", ["windows"]), "\\")
        self.assertEqual(call_native_function("std.path.separator", ["linux"]), "/")


class Phase21ProcessTests(unittest.TestCase):
    def test_run_for_platform_matches_host(self) -> None:
        host = host_platform_family()
        if host == "web":
            self.skipTest("web host not expected for VM")
        cmd = [sys.executable, "-c", "print('phase21')"]
        result = call_native_function("std.process.run_for_platform", [host, cmd])
        self.assertIsInstance(result, dict)
        self.assertEqual(result["exit"], 0)
        self.assertIn("phase21", result["stdout"])

    def test_run_for_platform_rejects_foreign_platform(self) -> None:
        host = host_platform_family()
        foreign = "linux" if host == "windows" else "windows"
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function(
                "std.process.run_for_platform",
                [foreign, [sys.executable, "-c", "print(1)"]],
            )

    def test_foreign_network_probe_not_functional(self) -> None:
        host = host_platform_family()
        if host == "web":
            self.skipTest("desktop host required")
        foreign = "linux" if host == "windows" else "windows"
        row = probe_network_capability(foreign)  # type: ignore[arg-type]
        self.assertEqual(row["implementation_state"], "scaffold")
        self.assertFalse(row.get("did_real_work"))

    def test_web_worker_message_roundtrip(self) -> None:
        worker = call_native_function("std.process.web_worker_new", [])
        self.assertTrue(call_native_function("std.process.web_post_message", [worker, "ping"]))
        self.assertEqual(call_native_function("std.process.web_recv", [worker]), "ping")
        empty = call_native_function("std.process.web_recv", [worker])
        self.assertIsInstance(empty, NilValue)


class Phase21WatchTests(unittest.TestCase):
    def test_snapshot_diff_detects_modification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "watch.txt"
            path.write_text("v1", encoding="utf-8")
            before = call_native_function("std.watch.snapshot", [str(path)])
            path.write_text("v2-longer-content", encoding="utf-8")
            after = call_native_function("std.watch.snapshot", [str(path)])
            changes = call_native_function("std.watch.diff", [before, after])
        self.assertGreaterEqual(len(changes), 1)
        self.assertEqual(changes[0]["kind"], "modified")

    def test_poll_once_detects_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "poll.txt"
            path.write_text("start", encoding="utf-8")

            def _write_later() -> None:
                path.write_text("changed", encoding="utf-8")

            import threading

            timer = threading.Timer(0.05, _write_later)
            timer.start()
            try:
                changes = call_native_function("std.watch.poll_once", [str(path), 500])
            finally:
                timer.cancel()
        self.assertTrue(changes)


class Phase21NetStorageTerminalTests(unittest.TestCase):
    def test_dns_lookup_localhost(self) -> None:
        addrs = call_native_function("std.net.dns_lookup", ["localhost", "A"])
        self.assertIsInstance(addrs, list)
        self.assertTrue(addrs)

    def test_dns_lookup_rejects_unknown_kind(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.net.dns_lookup", ["localhost", "MX"])

    def test_tls_available_is_bool(self) -> None:
        self.assertIsInstance(call_native_function("std.net.tls_available", []), bool)

    def test_browser_fetch_plan_is_scaffold_not_functional(self) -> None:
        plan = call_native_function("std.net.browser_fetch_plan", ["https://example.test/"])
        self.assertEqual(plan["implementation_state"], "scaffold")
        self.assertTrue(plan.get("plan_only"))
        self.assertTrue(plan["requires_browser_runtime"])

    def test_browser_fetch_sim_attempts_real_http(self) -> None:
        result = call_native_function("std.net.browser_fetch_sim", ["https://example.com/"])
        self.assertEqual(result["delivery_tier"], "hosted_simulation")
        self.assertTrue(result.get("ok") or result.get("attempted"))

    def test_web_storage_roundtrip(self) -> None:
        ns = "phase21-test"
        self.assertTrue(call_native_function("std.storage.web_set", [ns, "k", "v"]))
        self.assertEqual(call_native_function("std.storage.web_get", [ns, "k"]), "v")
        self.assertEqual(call_native_function("std.storage.web_keys", [ns]), ["k"])
        self.assertTrue(call_native_function("std.storage.web_remove", [ns, "k"]))
        self.assertTrue(call_native_function("std.storage.web_clear", [ns]))

    def test_web_storage_persists_to_disk(self) -> None:
        from sanskript.phase21_cross_platform import web_storage_load, web_storage_root
        from sanskript import stdlib_impl as stdlib

        ns = "phase21-persist-disk"
        with tempfile.TemporaryDirectory() as tmp:
            import os

            os.environ["SANSKRIPT_WEB_STORAGE"] = tmp
            stdlib._WEB_STORAGE.clear()
            self.assertTrue(call_native_function("std.storage.web_set", [ns, "persist", "yes"]))
            stdlib._WEB_STORAGE.clear()
            self.assertEqual(web_storage_load(ns).get("persist"), "yes")
            self.assertTrue((web_storage_root() / f"{ns}.json").is_file())

    def test_platform_detect_and_feature(self) -> None:
        detected = call_native_function("std.platform.detect", [])
        self.assertIn("platform_key", detected)
        self.assertTrue(call_native_function("std.platform.feature", ["path.join"]))

    def test_platform_compile_plan_targets(self) -> None:
        for family in ("windows", "linux", "macos", "web"):
            plan = call_native_function("std.platform.compile_plan", [family])
            self.assertEqual(plan["target_platform"], family)

    def test_console_log_writes_tagged_line(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            call_native_function("std.console.log", ["info", "phase21"])
        self.assertIn("[console:info]", buf.getvalue())

    def test_terminal_is_tty_unknown_stream_fails(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.terminal.is_tty", ["network"])


class Phase21AntiFakeTests(unittest.TestCase):
    @staticmethod
    def _truth(row: dict) -> dict:
        nested = row.get("truth_claims")
        if isinstance(nested, dict):
            return nested
        return {
            "exercised_on_host": row.get("exercised_on_host"),
            "did_real_work": row.get("did_real_work"),
            "delivery_tier": row.get("delivery_tier"),
            "returns_success_without_work": row.get("returns_success_without_work"),
            "host_only_hidden_as_cross_platform": row.get("host_only_hidden_as_cross_platform"),
        }

    def test_foreign_process_probe_not_functional(self) -> None:
        host = host_platform_family()
        for family in phase21_platform_matrix():
            if family == "web":
                row = probe_process_capability(family)
                self.assertEqual(row["implementation_state"], "functional")
                self.assertEqual(self._truth(row)["delivery_tier"], "hosted_simulation")
                self.assertTrue(self._truth(row)["did_real_work"])
                continue
            if family != host:
                row = probe_process_capability(family)
                self.assertEqual(row["implementation_state"], "scaffold")
                self.assertFalse(self._truth(row)["exercised_on_host"])
                self.assertFalse(self._truth(row)["did_real_work"])

    def test_file_watch_host_detects_change_without_inflation(self) -> None:
        host = host_platform_family()
        if host == "web":
            self.skipTest("file watch host probe requires desktop host")
        row = probe_file_watch_capability(host)
        self.assertEqual(row["implementation_state"], "functional")
        self.assertTrue(row.get("detected_change"))
        claims = self._truth(row)
        self.assertTrue(claims["did_real_work"])
        self.assertFalse(claims["returns_success_without_work"])
        if host == "windows":
            self.assertEqual(row.get("backend"), "ReadDirectoryChangesW")

    def test_web_storage_and_network_evidence_are_hosted_simulation_functional(self) -> None:
        storage = probe_storage_capability("web")
        self.assertEqual(storage["implementation_state"], "functional")
        self.assertTrue(storage.get("hosted_simulation"))
        self.assertEqual(self._truth(storage)["delivery_tier"], "hosted_simulation")
        network = probe_network_capability("web")
        self.assertEqual(network["implementation_state"], "functional")
        self.assertIn("browser_fetch_sim", network.get("api", ""))

    def test_foreign_terminal_probe_not_functional(self) -> None:
        host = host_platform_family()
        for family in phase21_platform_matrix():
            if family == "web":
                row = probe_terminal_capability(family)
                self.assertEqual(row["implementation_state"], "functional")
                self.assertEqual(self._truth(row)["delivery_tier"], "hosted_simulation")
                continue
            if family != host:
                row = probe_terminal_capability(family)
                self.assertEqual(row["implementation_state"], "scaffold")
                self.assertFalse(self._truth(row)["did_real_work"])

    def test_evidence_web_hosted_rows_have_simulation_tier(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = generate_phase21_evidence(request=Phase21EvidenceRequest(out_dir=Path(tmp)))
        for row in payload["rows"]:
            if row.get("platform") != "web":
                continue
            if row.get("capability") not in {"storage", "network", "process"}:
                continue
            claims = row.get("truth_claims") or row
            self.assertEqual(claims.get("delivery_tier"), "hosted_simulation")
            self.assertTrue(claims.get("did_real_work"))
            self.assertFalse(claims.get("returns_success_without_work"))


class Phase21EvidenceTests(unittest.TestCase):
    def test_evidence_matrix_writes_json_and_release_plans(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            payload = generate_phase21_evidence(request=Phase21EvidenceRequest(out_dir=out))
            self.assertEqual(payload["phase"], 21)
            self.assertGreaterEqual(len(payload["rows"]), 12)
            self.assertTrue((out / "phase21-evidence.json").exists())
            self.assertTrue((out / "phase21-test-matrix.json").exists())
            functional = [
                row
                for row in payload["rows"]
                if row.get("implementation_state") == "functional"
                and Phase21AntiFakeTests._truth(row).get("did_real_work")
            ]
            self.assertTrue(functional)
            path_rows = [r for r in payload["rows"] if r.get("capability") == "path"]
            self.assertEqual(len(path_rows), 4)

    def test_cli_phase21_evidence_emits_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "phase21.json"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "phase21-evidence",
                        "--out-dir",
                        str(Path(tmp) / "evidence"),
                        "--plan-json",
                        str(plan),
                    ]
                )
            self.assertEqual(code, 0)
            self.assertTrue(plan.exists())
            payload = json.loads(plan.read_text(encoding="utf-8"))
            self.assertEqual(payload["phase"], 21)


class Phase21FullSealGatekeeperTests(unittest.TestCase):
    def test_checklist_has_23_rows_and_all_checked(self) -> None:
        text = CHECKLIST.read_text(encoding="utf-8")
        markers = parse_phase21_checklist_markers(text)
        self.assertEqual(len(PHASE21_CHECKLIST_ROWS), 23)
        self.assertEqual(len(markers), 23)
        unchecked = [row["id"] for row in PHASE21_CHECKLIST_ROWS if not markers.get(row["id"])]
        self.assertEqual(unchecked, [], msg=f"unchecked: {unchecked}")

    def test_phase21_seal_verdict_ready(self) -> None:
        verdict = phase21_seal_verdict()
        self.assertTrue(verdict["seal_ready"], msg=verdict.get("blockers"))
        self.assertEqual(verdict["checklist_checked"], 23)
        self.assertEqual(verdict["evidence_ok"], 23)

    def test_browser_fetch_simulation_module(self) -> None:
        result = browser_fetch_simulation("https://example.com/")
        self.assertEqual(result["delivery_tier"], "hosted_simulation")
        self.assertTrue(result.get("ok") or result.get("attempted"))

    def test_cli_phase21_seal_check_passes(self) -> None:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = main(["phase21-seal-check"])
        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertTrue(payload["seal_ready"])


class Phase21ExampleTests(unittest.TestCase):
    def test_example_compiles_and_runs(self) -> None:
        source = EXAMPLE.read_text(encoding="utf-8")
        self.assertIn("std.platform.detect", source)
        output = SanskriptVM().execute(compile_program(load_program_from_path(EXAMPLE)))
        joined = "\n".join(output)
        self.assertIn("host_platform", joined)
        self.assertTrue("virtual" in joined.lower() or "sādhyakāraḥ" in joined or "\\" in joined)


if __name__ == "__main__":
    unittest.main()
