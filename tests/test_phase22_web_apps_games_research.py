"""Phase 22 web/apps/games/research/ML coverage (positive + negative end-user flows)."""

from __future__ import annotations

import http.server
import json
import tempfile
import threading
import unittest
from pathlib import Path

from sanskript.compiler import compile_source
from sanskript.errors import RuntimeSanskriptError
from sanskript.phase22_web_apps import phase22_inventory
from sanskript.runtime_values import NIL
from sanskript.stdlib_core import call_native_function, list_native_functions
from sanskript.vm import SanskriptVM

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "phase22-web-apps-games-research.ssk"


class _JsonEchoHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # type: ignore[override]
        body = json.dumps({"ok": True, "path": self.path}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # type: ignore[override]
        size = int(self.headers.get("Content-Length", "0"))
        data = self.rfile.read(size).decode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


class Phase22RegistryTests(unittest.TestCase):
    def test_phase22_surfaces_registered(self) -> None:
        names = set(list_native_functions())
        for required in (
            "std.http.router_dispatch",
            "std.web.canvas_raster",
            "std.data.frame",
            "std.ml.model_pack",
            "std.phase22.inventory",
        ):
            self.assertIn(required, names)

    def test_inventory_marks_tiers_honestly(self) -> None:
        rows = {row["name"]: row for row in phase22_inventory()}
        self.assertEqual(rows["std.web.bridge_plan"]["tier"], "plan_only")
        self.assertEqual(rows["std.web.bridge_plan"]["substitute"], "sanskript web + std.web.bridge_execute")
        self.assertEqual(rows["std.http.get"]["tier"], "functional_host")
        self.assertEqual(rows["std.http.router_dispatch"]["tier"], "functional_host")
        self.assertEqual(rows["std.game.loop_run"]["tier"], "host_substitute")
        self.assertTrue(rows["std.db.postgres_plan"]["host_bridge"])


class Phase22HttpWebTests(unittest.TestCase):
    def test_request_response_router_middleware_cookies_sessions_auth(self) -> None:
        req = call_native_function(
            "std.http.request",
            ["GET", "/items/3", {"cookie": "sid=abc"}, ""],
        )
        self.assertEqual(req["cookies"]["sid"], "abc")
        resp = call_native_function("std.http.response", [200, "ok", {"content-type": "text/plain"}])
        self.assertEqual(resp["status"], 200)

        header = call_native_function(
            "std.http.cookie_header",
            ["sid", "abc", {"path": "/", "http_only": True}],
        )
        self.assertIn("HttpOnly", header)
        parsed = call_native_function("std.http.cookie_parse", [header.split(";", 1)[0]])
        self.assertEqual(parsed["sid"], "abc")

        sid = call_native_function("std.http.session_create", [])
        call_native_function("std.http.session_set", [sid, "user", "dev"])
        self.assertEqual(call_native_function("std.http.session_get", [sid, "user"]), "dev")

        basic = call_native_function("std.http.auth_basic_header", ["u", "p"])
        self.assertTrue(basic.startswith("Basic "))
        self.assertTrue(call_native_function("std.http.auth_bearer_verify", ["tok", "tok"]))
        self.assertFalse(call_native_function("std.http.auth_bearer_verify", ["tok", "other"]))

        routed = call_native_function(
            "std.http.router_dispatch",
            ["/users/9", {"/users/{id}": "show"}, ["log", "cors"]],
        )
        self.assertEqual(routed["handler"], "show")
        self.assertEqual(routed["params"]["id"], "9")
        self.assertTrue(routed["request"]["logged"])

        miss = call_native_function("std.http.router_dispatch", ["/nope", {"/": "home"}, []])
        self.assertIs(miss, NIL)

    def test_http_client_end_user_flow(self) -> None:
        with http.server.ThreadingHTTPServer(("127.0.0.1", 0), _JsonEchoHandler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                url = f"http://127.0.0.1:{server.server_address[1]}/ping"
                got = call_native_function("std.http.get", [url])
                self.assertEqual(got["status"], 200)
                posted = call_native_function("std.http.post_json", [url, {"phase": 22}])
                self.assertEqual(posted["status"], 200)
            finally:
                server.shutdown()
                thread.join(timeout=2)

    def test_http_server_once_covered_by_phase14_contract(self) -> None:
        """server_once timing is validated in test_phase14_surakshita; avoid duplicate flake."""
        payload = call_native_function("std.phase22.inventory", [])
        names = {row["name"] for row in payload}
        self.assertIn("std.http.server_once", names)

    def test_html_template_css_dom_canvas(self) -> None:
        escaped = call_native_function("std.web.html_escape", ['<script>"x"</script>'])
        self.assertIn("&lt;script&gt;", escaped)
        tag = call_native_function("std.web.html_element", ["p", {"class": "lead"}, "hi"])
        self.assertIn("<p", tag)
        rendered = call_native_function("std.template.render", ["hi {{name}}", {"name": "loka"}])
        self.assertEqual(rendered, "hi loka")
        bundled = call_native_function("std.web.css_bundle", [["body { color: red; }", "/*x*/h1{}"]])
        self.assertIn("color: red", bundled)
        dom = call_native_function(
            "std.web.dom_dispatch",
            [{"nodes": {"#btn": {"events": []}}}, "#btn", "click"],
        )
        self.assertEqual(dom["last"]["event"], "click")
        canvas = call_native_function(
            "std.web.canvas_raster",
            [4, 3, [{"op": "rect", "x": 0, "y": 0, "w": 2, "h": 2, "fill": "#"}]],
        )
        self.assertIn("#", canvas)

    def test_plan_only_surfaces_document_substitutes(self) -> None:
        for name in (
            "std.web.bridge_plan",
            "std.web.webgl_plan",
            "std.game.audio_plan",
            "std.data.parquet_plan",
            "std.ml.ad_roadmap",
            "std.ml.python_bridge_plan",
            "std.ml.native_kernels_plan",
            "std.db.postgres_plan",
        ):
            plan = call_native_function(name, [])
            self.assertEqual(plan["tier"], "plan_only")
            self.assertTrue(plan.get("substitute"), name)
        gui = call_native_function("std.gui.capabilities_plan", [])
        self.assertEqual(gui["tier"], "host_substitute")
        scene = call_native_function("std.game.scene3d_plan", [])
        self.assertEqual(scene["tier"], "host_substitute")


class Phase22DataGameMlTests(unittest.TestCase):
    def test_dataframe_csv_sqlite_plot(self) -> None:
        rows = [{"id": 1, "v": 2}, {"id": 2, "v": 4}]
        frame = call_native_function("std.data.frame", [rows])
        self.assertEqual(frame["nrow"], 2)
        self.assertEqual(call_native_function("std.data.column", [rows, "v"]), [2, 4])
        hist = call_native_function("std.plot.histogram_ascii", [[1, 2, 8, 9], 4, 10])
        self.assertIn("#", hist)
        spark = call_native_function("std.plot.sparkline", [[1, 3, 2, 5]])
        self.assertTrue(spark)

        with tempfile.TemporaryDirectory() as tmp:
            csv_path = str(Path(tmp) / "data.csv")
            call_native_function("std.data.csv_write", [csv_path, rows])
            loaded = call_native_function("std.data.csv_read", [csv_path])
            self.assertEqual(int(loaded[0]["id"]), 1)

            db_path = str(Path(tmp) / "p22.sqlite")
            call_native_function(
                "std.db.sqlite_exec",
                [db_path, "create table t (id integer, name text)", []],
            )
            call_native_function("std.db.sqlite_exec", [db_path, "insert into t values (?, ?)", [1, "a"]])
            got = call_native_function("std.db.sqlite_query", [db_path, "select name from t where id = ?", [1]])
            self.assertEqual(got[0]["name"], "a")

    def test_game_loop_input_sprite_physics_assets(self) -> None:
        ticks = call_native_function("std.game.loop_run", [10, 3, {"x": 0, "vx": 2}])
        self.assertEqual(len(ticks), 3)
        inp = call_native_function("std.game.input_state", [["ArrowLeft", "Space"]])
        self.assertTrue(inp["pressed"]["Space"])
        atlas = call_native_function(
            "std.game.sprite_atlas",
            [{"frame_w": 16, "frame_h": 16, "columns": 2, "names": ["a", "b", "c"]}],
        )
        self.assertEqual(len(atlas["frames"]), 3)
        moved = call_native_function("std.game.physics2d_step", [{"x": 0, "y": 0, "vx": 1, "vy": 0, "gravity": 0}, 0.5])
        self.assertEqual(moved["x"], 0.5)
        with tempfile.TemporaryDirectory() as tmp:
            asset = Path(tmp) / "sprite.png"
            asset.write_bytes(b"png")
            paths = call_native_function("std.game.asset_resolve", [tmp, ["sprite.png"]])
            self.assertTrue(paths[0].endswith("sprite.png"))

    def test_linalg_tensor_ml_notebook_research_env(self) -> None:
        mat = call_native_function("std.linalg.matmul", [[[1, 2]], [[3], [4]]])
        self.assertEqual(mat[0][0], 11.0)
        self.assertEqual(call_native_function("std.linalg.dot", [[1, 2], [3, 4]]), 11.0)
        self.assertEqual(call_native_function("std.linalg.transpose", [[[1, 2], [3, 4]]]), [[1, 3], [2, 4]])
        self.assertEqual(call_native_function("std.tensor.shape", [[[1, 2], [3, 4]]]), [2, 2])
        reshaped = call_native_function("std.tensor.reshape", [[[1, 2], [3, 4]], [4]])
        self.assertEqual(reshaped, [1, 2, 3, 4])

        packed = call_native_function("std.ml.model_pack", [{"w": [1, 2]}])
        unpacked = call_native_function("std.ml.model_unpack", [packed])
        self.assertEqual(unpacked["w"], [1, 2])

        cells = call_native_function(
            "std.notebook.split_cells",
            ["# Title\n\n```ssk\ngaṇakaḥ 1 darśayati.\n```\n"],
        )
        self.assertTrue(any(cell["kind"] == "code" for cell in cells))
        doc = call_native_function(
            "std.research.template_render",
            ["# {{title}}\n\nmetric={{metric}}", {"title": "Run", "metric": 0.9}],
        )
        self.assertIn("metric=0.9", doc)
        fp = call_native_function("std.env.fingerprint", [{"py": "3.12", "seed": "7"}])
        self.assertEqual(len(fp), 64)

    def test_negative_paths(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.http.middleware_apply", [{"path": "/"}, ["unknown"]])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.plot.histogram_ascii", [[], 2, 5])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.tensor.reshape", [[[1, 2]], [3]])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.data.csv_write", ["/no/such/dir/x.csv", [{"a": 1}]])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.ml.model_unpack", ['{"kind":"other"}'])
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.web.canvas_raster", [0, 2, []])


class Phase22ExampleTests(unittest.TestCase):
    def test_example_source_present(self) -> None:
        self.assertTrue(EXAMPLE.exists())
        source = EXAMPLE.read_text(encoding="utf-8")
        self.assertTrue(
            "std.web.route_match" in source or "std.http.router_dispatch" in source,
            "example must exercise web routing helper",
        )
        self.assertIn("std.plot.sparkline", source)

    def test_example_runs_via_cli(self) -> None:
        from contextlib import redirect_stdout
        import io
        from sanskript.cli import main as cli_main

        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(cli_main(["run", str(EXAMPLE)]), 0)
        self.assertIn("mean", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
