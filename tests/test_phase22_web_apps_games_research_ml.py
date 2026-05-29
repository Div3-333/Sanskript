"""Phase 22 full seal: all checklist rows proven via ``sanskript run`` + host substitutes."""

from __future__ import annotations

import io
import json
import re
import socket
import tempfile
import threading
import time
import unittest
import urllib.request
from contextlib import redirect_stdout
from pathlib import Path

from sanskript.cli import main as cli_main
from sanskript.phase22_web_apps import PHASE22_CHECKLIST_SLUGS
from sanskript.stdlib_core import call_native_function


ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "docs" / "native-sanskript-independence-checklist.md"
PHASE22_DOC = ROOT / "docs" / "phase22-web-apps-games-research-ml.md"
FULL_SEAL = ROOT / "examples" / "phase22-full-seal.ssk"
PHASE22_DIR = ROOT / "examples" / "phase22"
RESEARCH_BASELINE = ROOT / "examples" / "phase22-research-cli-baseline.ssk"
HTTP_SERVICE = ROOT / "examples" / "phase22-http-service.ssk"
HTTP_ROUTER_AUTH = ROOT / "examples" / "phase22-http-router-auth.ssk"
HTML_TEMPLATE = ROOT / "examples" / "phase22-html-template.ssk"

# Display labels in native-sanskript-independence-checklist.md (44 rows).
PHASE22_CHECKLIST_LABELS: tuple[str, ...] = (
    "HTTP client.",
    "HTTP server.",
    "Router.",
    "Middleware.",
    "Request/response types.",
    "Cookies.",
    "Sessions.",
    "Authentication helpers.",
    "HTML generation.",
    "Template engine.",
    "CSS asset pipeline.",
    "JavaScript/WASM bridge for browser targets.",
    "DOM access for web targets.",
    "Event handling for web targets.",
    "Canvas 2D support.",
    "WebGL/WebGPU bridge or native equivalent.",
    "Desktop windowing abstraction.",
    "GUI widgets.",
    "Menus and shortcuts.",
    "Clipboard.",
    "Notifications.",
    "File dialogs.",
    "Game loop.",
    "Input handling.",
    "Audio playback.",
    "Asset loading.",
    "Sprite support.",
    "2D physics integration or native engine.",
    "3D scene support.",
    "Database client.",
    "SQLite support.",
    "Postgres support.",
    "Dataframe-like tables.",
    "CSV/Parquet readers.",
    "Plotting.",
    "Linear algebra.",
    "Tensor basics.",
    "Automatic differentiation plan.",
    "Model serialization.",
    "Python ML interop as temporary bridge only.",
    "Native ML kernels roadmap.",
    "Notebook or literate-programming workflow.",
    "Research script templates.",
    "Reproducible environment support.",
    "Static web export (`sanskript web`).",
    "Phase 22 inventory registry.",
)


def _free_tcp_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _run_example_with_port_placeholder(example: Path, port: int) -> tuple[int, str]:
    source = example.read_text(encoding="utf-8").replace("__P22_PORT__", str(port))
    with tempfile.NamedTemporaryFile("w", suffix=".ssk", delete=False, encoding="utf-8") as handle:
        handle.write(source)
        temp_path = Path(handle.name)
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            code = cli_main(["run", str(temp_path)])
        return code, buf.getvalue()
    finally:
        temp_path.unlink(missing_ok=True)


class Phase22FullSealTests(unittest.TestCase):
    def test_phase22_checklist_slug_count_matches_labels(self) -> None:
        self.assertEqual(len(PHASE22_CHECKLIST_SLUGS), 46)
        self.assertEqual(len(PHASE22_CHECKLIST_LABELS), 46)

    def test_phase22_doc_declares_full_seal(self) -> None:
        self.assertTrue(PHASE22_DOC.is_file())
        text = PHASE22_DOC.read_text(encoding="utf-8")
        self.assertIn("SEAL-READY", text)
        self.assertIn("phase22-full-seal.ssk", text)

    def test_phase22_checklist_all_rows_checked_with_tiers(self) -> None:
        text = CHECKLIST.read_text(encoding="utf-8")
        start = text.index("## Phase 22:")
        end = text.index("## Phase 23:", start)
        section = text[start:end]
        self.assertIn("host_scaffold_acceptable", section)
        for label in PHASE22_CHECKLIST_LABELS:
            self.assertRegex(section, rf"- \[x\] {re.escape(label)}", label)

    def test_phase22_inventory_tiers_honest(self) -> None:
        rows = {row["name"]: row for row in call_native_function("std.phase22.inventory", [])}
        for name in (
            "std.http.server_route_once",
            "std.http.client_roundtrip",
            "std.phase22.seal_run",
        ):
            self.assertEqual(rows[name]["tier"], "functional_host", name)
        for name in ("std.game.loop_run", "std.web.canvas_raster", "std.gui.simulate"):
            self.assertEqual(rows[name]["tier"], "host_substitute", name)
        for name in ("std.db.postgres_plan", "std.data.parquet_plan"):
            self.assertEqual(rows[name]["tier"], "plan_only", name)
            self.assertTrue(rows[name].get("substitute"), name)

    def test_phase22_seal_run_native_passes(self) -> None:
        payload = call_native_function("std.phase22.seal_run", [])
        self.assertEqual(payload["verdict"], "SEAL-READY")
        self.assertEqual(payload["marker_count"], 46)
        self.assertEqual(payload["checklist_count"], 46)
        self.assertEqual(len(payload["errors"]), 0)
        for slug in PHASE22_CHECKLIST_SLUGS:
            self.assertIn(f"P22_SEAL:{slug}:ok", payload["markers"])

    def test_phase22_full_seal_example_executes(self) -> None:
        for candidate in (PHASE22_DIR / "full-seal.ssk", FULL_SEAL):
            if candidate.is_file():
                seal_path = candidate
                break
        else:
            self.skipTest("phase22 full seal example missing")
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cli_main(["run", str(seal_path)])
        self.assertEqual(code, 0)
        out = buf.getvalue()
        payload = json.loads(out.strip().splitlines()[-1])
        self.assertEqual(payload["verdict"], "SEAL-READY")
        for slug in PHASE22_CHECKLIST_SLUGS:
            self.assertIn(f"P22_SEAL:{slug}:ok", payload["markers"])

    def test_phase22_examples_directory_runs(self) -> None:
        if not PHASE22_DIR.is_dir():
            self.skipTest("examples/phase22 missing")
        for name in ("http-client.ssk", "http-router-auth.ssk", "full-seal.ssk"):
            path = PHASE22_DIR / name
            if not path.is_file():
                self.skipTest(f"{name} missing")
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(cli_main(["run", str(path)]), 0, name)

    def test_phase22_research_cli_baseline_executes(self) -> None:
        if not RESEARCH_BASELINE.is_file():
            self.skipTest("phase22 research baseline missing")
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cli_main(["run", str(RESEARCH_BASELINE)])
        self.assertEqual(code, 0)
        out = buf.getvalue()
        self.assertIn("mean", out)
        self.assertIn("*", out)

    def test_phase22_html_template_example_executes(self) -> None:
        if not HTML_TEMPLATE.is_file():
            self.skipTest("phase22 html template example missing")
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cli_main(["run", str(HTML_TEMPLATE)])
        self.assertEqual(code, 0)
        out = buf.getvalue()
        self.assertIn("<h1>Phase22</h1>", out)
        self.assertIn("package=phase22-html", out)

    def test_phase22_http_router_auth_driver_executes(self) -> None:
        if not HTTP_ROUTER_AUTH.is_file():
            self.skipTest("phase22 router/auth driver missing")
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cli_main(["run", str(HTTP_ROUTER_AUTH)])
        self.assertEqual(code, 0)
        out = buf.getvalue()
        self.assertIn('"handler":"show"', out)
        self.assertIn('"id":"9"', out)
        self.assertIn("dev", out)

    def test_phase22_http_service_listen_route_respond(self) -> None:
        if not HTTP_SERVICE.is_file():
            self.skipTest("phase22 http service example missing")
        port = _free_tcp_port()
        holder: dict[str, object] = {}

        def run_program() -> None:
            holder["code"], holder["out"] = _run_example_with_port_placeholder(HTTP_SERVICE, port)

        thread = threading.Thread(target=run_program, daemon=True)
        thread.start()
        time.sleep(0.08)
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=3) as response:
                body = response.read().decode("utf-8")
        finally:
            thread.join(timeout=8.0)
        self.assertEqual(body, "ok")
        self.assertEqual(holder.get("code"), 0)
        payload = json.loads(str(holder.get("out", "")).strip().splitlines()[-1])
        self.assertEqual(payload["handler"], "health")
        self.assertEqual(payload["path"], "/health")
        self.assertEqual(payload["status"], 200)


if __name__ == "__main__":
    unittest.main()
