from __future__ import annotations

import http.server
import io
import json
import os
import socket
import tempfile
import time
import threading
import unittest
import urllib.request
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from sanskript.cli import main as cli_main
from sanskript.errors import RuntimeSanskriptError
from sanskript.runtime_values import NIL, OptionValue, is_truthy
from sanskript.stdlib_core import call_native_function


class _JsonEchoHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # type: ignore[override]
        payload = {"ok": True, "path": self.path}
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):  # type: ignore[override]
        size = int(self.headers.get("Content-Length", "0"))
        data = self.rfile.read(size).decode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


class Phase14StdlibTests(unittest.TestCase):
    def test_http_client_get_and_post_json(self) -> None:
        with http.server.ThreadingHTTPServer(("127.0.0.1", 0), _JsonEchoHandler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                url = f"http://127.0.0.1:{server.server_address[1]}/ping"
                got = call_native_function("std.http.get", [url])
                self.assertEqual(got["status"], 200)
                self.assertIn('"ok": true', got["body"])

                posted = call_native_function("std.http.post_json", [url, {"name": "dev"}])
                self.assertEqual(posted["status"], 200)
                self.assertIn('"name":"dev"', posted["body"])
            finally:
                server.shutdown()
                thread.join(timeout=2)

    def test_data_plot_web_db_async_task_baselines(self) -> None:
        rows = [{"n": 1}, {"n": 3}, {"n": 5}]
        self.assertEqual(call_native_function("std.data.column", [rows, "n"]), [1, 3, 5])
        self.assertEqual(call_native_function("std.data.describe", [[1, 3, 5]])["mean"], 3.0)
        graph = call_native_function("std.plot.ascii", [[1, 2, 1, 3], 4, 3])
        self.assertIn("*", graph)
        route = call_native_function(
            "std.web.route_match",
            ["/users/42", {"/users/{id}": "user_show"}],
        )
        self.assertEqual(route["params"]["id"], "42")

        with tempfile.TemporaryDirectory() as tmp:
            db_path = str(Path(tmp) / "phase14.sqlite")
            call_native_function(
                "std.db.sqlite_exec",
                [db_path, "create table if not exists users (id integer, name text)", []],
            )
            call_native_function("std.db.sqlite_exec", [db_path, "insert into users values (?, ?)", [1, "dev"]])
            rows = call_native_function("std.db.sqlite_query", [db_path, "select name from users where id = ?", [1]])
            self.assertEqual(rows[0]["name"], "dev")

            text_path = Path(tmp) / "a.txt"
            text_path.write_text("hello", encoding="utf-8")
            self.assertEqual(call_native_function("std.async.read_text", [str(text_path)]), "hello")

        self.assertEqual(call_native_function("std.async.sleep_ms", [1]), 1)
        self.assertEqual(call_native_function("std.task.run_after_ms", [1, "done"]), "done")
        self.assertEqual(
            call_native_function("std.task.schedule", [[[5, "b"], [1, "a"]]]),
            ["a", "b"],
        )

    def test_template_web_render_and_error_surface(self) -> None:
        rendered = call_native_function(
            "std.template.render",
            ["namaste {{name}}", {"name": "mitra"}],
        )
        self.assertEqual(rendered, "namaste mitra")
        html = call_native_function(
            "std.web.render",
            ["<h1>{{title}}</h1>", {"title": "Surakshita"}],
        )
        self.assertEqual(html, "<h1>Surakshita</h1>")
        with self.assertRaisesRegex(RuntimeSanskriptError, "missing key 'name'"):
            call_native_function("std.template.render", ["namaste {{name}}", {}])

    def test_file_text_and_option_safety_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "note.txt")
            call_native_function("std.file.write_text", [path, "  namaste  "])
            call_native_function("std.file.append_text", [path, "\nmitra"])
            text = call_native_function("std.file.read_text", [path])
            cleaned = call_native_function("std.text.strip", [text])
            self.assertEqual(cleaned, "namaste  \nmitra")
            self.assertTrue(call_native_function("std.path.exists", [path]))

        self.assertFalse(is_truthy(OptionValue(False, None)))
        self.assertTrue(is_truthy(OptionValue(True, "value")))

    def test_http_server_once_end_user_flow(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        request_error: list[Exception] = []
        payload_holder: dict[str, object] = {}

        def serve() -> None:
            payload_holder["value"] = call_native_function(
                "std.http.server_once",
                ["127.0.0.1", port, "ok"],
            )

        def make_request() -> None:
            deadline = time.time() + 2.0
            while time.time() < deadline:
                try:
                    with urllib.request.urlopen(f"http://127.0.0.1:{port}/hello", timeout=1) as response:
                        self.assertEqual(response.read().decode("utf-8"), "ok")
                    return
                except Exception as exc:
                    request_error.append(exc)
                    time.sleep(0.02)

        server_thread = threading.Thread(target=serve, daemon=True)
        server_thread.start()
        time.sleep(0.05)
        requester = threading.Thread(target=make_request, daemon=True)
        requester.start()
        server_thread.join(timeout=4.0)
        requester.join(timeout=3)
        payload = payload_holder.get("value")
        self.assertIsNotNone(payload)
        if request_error:
            self.fail(f"requester failed before server accepted request: {request_error[-1]}")
        self.assertEqual(payload["status"], 200)
        self.assertEqual(payload["method"], "GET")
        self.assertEqual(payload["path"], "/hello")


class Phase14CliTests(unittest.TestCase):
    def test_docs_and_pack_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "main.ssk"
            source.write_text("gaṇakaḥ ekam darśayati.", encoding="utf-8")
            docs = root / "docs.md"
            bundle = root / "bundle.zip"
            self.assertEqual(cli_main(["docs", str(source), "-o", str(docs)]), 0)
            self.assertTrue(docs.is_file())
            self.assertEqual(cli_main(["pack", str(source), "-o", str(bundle)]), 0)
            self.assertTrue(bundle.is_file())

    def test_install_command_vendors_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dep_dir = root / "dep"
            dep_dir.mkdir()
            (dep_dir / "dep.ssk").write_text("gaṇakaḥ ekam darśayati.", encoding="utf-8")
            (root / "ssk.toml").write_text(
                """
                [package]
                name = "demo"
                version = "0.1.0"

                [dependencies.local]
                dep = { path = "dep/dep.ssk" }
                """,
                encoding="utf-8",
            )
            old_cwd = Path.cwd()
            try:
                os.chdir(root)
                self.assertEqual(cli_main(["install", str(dep_dir), "--name", "dep"]), 0)
            finally:
                os.chdir(old_cwd)
            self.assertTrue((root / "vendor" / "dep").exists())

    def test_repl_run_web_and_native_build_user_flows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "main.ssk"
            source.write_text("gaṇakaḥ ekaṃ darśayati.", encoding="utf-8")

            run_stdout = io.StringIO()
            with redirect_stdout(run_stdout):
                self.assertEqual(cli_main(["run", str(source)]), 0)
            self.assertEqual(run_stdout.getvalue().strip(), "1")

            repl_stdout = io.StringIO()
            repl_stderr = io.StringIO()
            with (
                patch("builtins.input", side_effect=["gaṇakaḥ ekaṃ darśayati.", ":quit"]),
                redirect_stdout(repl_stdout),
                redirect_stderr(repl_stderr),
            ):
                self.assertEqual(cli_main(["repl", "--prompt", "phase14> "]), 0)
            self.assertIn("Sanskript REPL", repl_stdout.getvalue())
            self.assertIn("1", repl_stdout.getvalue())
            self.assertEqual(repl_stderr.getvalue(), "")

            web_out = root / "app.html"
            with redirect_stdout(io.StringIO()):
                self.assertEqual(cli_main(["web", str(source), "-o", str(web_out)]), 0)
            self.assertTrue(web_out.is_file())

            native_out = root / "native-linux"
            native_stdout = io.StringIO()
            with redirect_stdout(native_stdout):
                self.assertEqual(
                    cli_main(
                        [
                            "native-build",
                            str(source),
                            "--backend",
                            "portable-bytecode",
                            "--target",
                            "x86_64-unknown-linux-gnu",
                            "--out-dir",
                            str(native_out),
                        ]
                    ),
                    0,
                )
            native_payload = json.loads(native_stdout.getvalue())
            self.assertEqual(native_payload["backend"], "portable-bytecode")
            self.assertEqual(native_payload["target"], "x86_64-unknown-linux-gnu")
            self.assertTrue((native_out / "program.sskbc").is_file())


class Phase14ExampleTests(unittest.TestCase):
    def test_phase14_example_present(self) -> None:
        root = Path(__file__).resolve().parents[1]
        example = root / "examples" / "phase14-surakshita.ssk"
        if not example.is_file():
            self.skipTest("phase14 example missing")
        text = example.read_text(encoding="utf-8")
        self.assertIn("std.plot.ascii", text)

    def test_phase14_example_executes(self) -> None:
        root = Path(__file__).resolve().parents[1]
        example = root / "examples" / "phase14-surakshita.ssk"
        if not example.is_file():
            self.skipTest("phase14 example missing")
        self.assertEqual(cli_main(["run", str(example)]), 0)


if __name__ == "__main__":
    unittest.main()
