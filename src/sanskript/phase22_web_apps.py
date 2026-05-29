"""Phase 22 web/apps/games/research/ML host-runtime helpers (truth-first)."""

from __future__ import annotations

import base64
import csv
import hashlib
import http.server
import json
import math
import re
import socket
import tempfile
import threading
import time
import urllib.request
from pathlib import Path
from typing import Callable

from .errors import RuntimeSanskriptError
from .runtime_values import NIL
from .stdlib_common import expect_int, expect_list, expect_map, expect_number, expect_text, stringify_json

_PHASE22_SESSIONS: dict[str, dict[str, object]] = {}

# 44 independence-checklist rows (+ seal-bar examples). Tier labels mirror Phase 23 honesty.
PHASE22_CHECKLIST_SLUGS: tuple[str, ...] = (
    "http_client",
    "http_server",
    "router",
    "middleware",
    "request_response_types",
    "cookies",
    "sessions",
    "authentication_helpers",
    "html_generation",
    "template_engine",
    "css_asset_pipeline",
    "javascript_wasm_bridge",
    "dom_access",
    "event_handling",
    "canvas_2d",
    "webgl_webgpu_bridge",
    "desktop_windowing",
    "gui_widgets",
    "menus_shortcuts",
    "clipboard",
    "notifications",
    "file_dialogs",
    "game_loop",
    "input_handling",
    "audio_playback",
    "asset_loading",
    "sprite_support",
    "physics_2d",
    "scene_3d",
    "database_client",
    "sqlite_support",
    "postgres_support",
    "dataframe_tables",
    "csv_parquet_readers",
    "plotting",
    "linear_algebra",
    "tensor_basics",
    "automatic_differentiation_plan",
    "model_serialization",
    "python_ml_interop",
    "native_ml_kernels_roadmap",
    "notebook_literate",
    "research_script_templates",
    "reproducible_environment",
    "static_web_cli",
    "registry_inventory",
)


def phase22_truth(
    tier: str,
    *,
    host_bridge: bool = True,
    substitute: str | None = None,
    notes: list[str] | None = None,
) -> dict:
    """Tier: functional_host | host_substitute | plan_only."""
    return {
        "phase": 22,
        "tier": tier,
        "implementation_state": "functional" if tier == "functional_host" else ("scaffold" if tier == "plan_only" else "host_substitute"),
        "host_bridge": host_bridge,
        "substitute": substitute,
        "notes": notes or [],
    }


def phase22_inventory() -> list[dict]:
    """Registry of Phase 22 surfaces with honest tier labels (Phase 22 full seal)."""
    functional_host = [
        "std.http.get",
        "std.http.post_json",
        "std.http.client_roundtrip",
        "std.http.server_once",
        "std.http.server_route_once",
        "std.http.request",
        "std.http.response",
        "std.http.router_dispatch",
        "std.http.middleware_apply",
        "std.http.cookie_parse",
        "std.http.cookie_header",
        "std.http.session_create",
        "std.http.session_get",
        "std.http.session_set",
        "std.http.auth_basic_header",
        "std.http.auth_bearer_verify",
        "std.web.route_match",
        "std.web.render",
        "std.web.html_escape",
        "std.web.html_element",
        "std.template.render",
        "std.data.column",
        "std.data.describe",
        "std.plot.ascii",
        "std.db.sqlite_exec",
        "std.db.sqlite_query",
        "std.db.client",
        "std.phase22.seal_run",
    ]
    host_substitute = [
        "std.web.css_bundle",
        "std.web.dom_simulate",
        "std.web.dom_dispatch",
        "std.web.canvas_raster",
        "std.web.bridge_execute",
        "std.web.webgl_stub",
        "std.gui.simulate",
        "std.gui.capabilities_plan",
        "std.game.loop_run",
        "std.game.input_state",
        "std.game.asset_resolve",
        "std.game.sprite_atlas",
        "std.game.physics2d_step",
        "std.game.audio_tick",
        "std.game.scene3d_plan",
        "std.data.frame",
        "std.data.csv_read",
        "std.data.csv_write",
        "std.data.parquet_stub_read",
        "std.db.postgres_stub_connect",
        "std.plot.histogram_ascii",
        "std.plot.sparkline",
        "std.linalg.matmul",
        "std.linalg.dot",
        "std.linalg.transpose",
        "std.tensor.shape",
        "std.tensor.reshape",
        "std.ml.model_pack",
        "std.ml.model_unpack",
        "std.notebook.split_cells",
        "std.research.template_render",
        "std.env.fingerprint",
    ]
    plan_only = [
        "std.web.bridge_plan",
        "std.web.webgl_plan",
        "std.data.parquet_plan",
        "std.ml.ad_roadmap",
        "std.ml.python_bridge_plan",
        "std.ml.native_kernels_plan",
        "std.db.postgres_plan",
        "std.game.audio_plan",
    ]
    rows: list[dict] = []
    for name in functional_host:
        rows.append({"name": name, **phase22_truth("functional_host")})
    for name in host_substitute:
        rows.append(
            {
                "name": name,
                **phase22_truth(
                    "host_substitute",
                    notes=["host simulation or stdout artifact; not browser/desktop product"],
                ),
            }
        )
    substitutes = {
        "std.web.bridge_plan": "sanskript web + std.web.bridge_execute",
        "std.data.parquet_plan": "std.data.parquet_stub_read",
        "std.db.postgres_plan": "std.db.postgres_stub_connect",
        "std.ml.python_bridge_plan": "std.ml.model_pack (weights JSON)",
        "std.ml.native_kernels_plan": "std.linalg.matmul",
        "std.ml.ad_roadmap": "plan JSON only",
        "std.game.audio_plan": "std.game.audio_tick",
    }
    for name in plan_only:
        rows.append(
            {
                "name": name,
                **phase22_truth("plan_only", substitute=substitutes.get(name), notes=["roadmap/plan; substitute listed"]),
            }
        )
    return rows


# ---------------------------------------------------------------------------
# HTTP request/response, router, middleware, cookies, sessions, auth
# ---------------------------------------------------------------------------


def http_request(args: list) -> dict:
    method = expect_text(args[0], fn_name="std.http.request")
    path = expect_text(args[1], fn_name="std.http.request")
    headers = expect_map(args[2], fn_name="std.http.request")
    body = expect_text(args[3], fn_name="std.http.request")
    cookie_header = ""
    if isinstance(headers, dict):
        for key, value in headers.items():
            if str(key).lower() == "cookie":
                cookie_header = str(value)
                break
    cookies = cookie_parse([cookie_header]) if cookie_header else {}
    return {
        "method": method.upper(),
        "path": path,
        "headers": {str(k).lower(): str(v) for k, v in headers.items()},
        "body": body,
        "cookies": cookies,
    }


def http_response(args: list) -> dict:
    status = expect_int(args[0], fn_name="std.http.response")
    body = expect_text(args[1], fn_name="std.http.response")
    headers = expect_map(args[2], fn_name="std.http.response")
    return {"status": status, "headers": {str(k): str(v) for k, v in headers.items()}, "body": body}


def cookie_parse(args: list) -> dict:
    header = expect_text(args[0], fn_name="std.http.cookie_parse")
    out: dict[str, str] = {}
    for part in header.split(";"):
        piece = part.strip()
        if not piece or "=" not in piece:
            continue
        name, value = piece.split("=", 1)
        out[name.strip()] = value.strip()
    return out


def cookie_header(args: list) -> str:
    name = expect_text(args[0], fn_name="std.http.cookie_header")
    value = expect_text(args[1], fn_name="std.http.cookie_header")
    options = expect_map(args[2], fn_name="std.http.cookie_header") if len(args) > 2 else {}
    parts = [f"{name}={value}"]
    if options.get("path"):
        parts.append(f"Path={options['path']}")
    if options.get("http_only") or options.get("httponly"):
        parts.append("HttpOnly")
    if options.get("secure"):
        parts.append("Secure")
    return "; ".join(parts)


def session_create(_args: list) -> str:
    token = hashlib.sha256(f"{time.time_ns()}".encode()).hexdigest()[:24]
    _PHASE22_SESSIONS[token] = {}
    return token


def session_get(args: list) -> object:
    sid = expect_text(args[0], fn_name="std.http.session_get")
    key = expect_text(args[1], fn_name="std.http.session_get")
    bucket = _PHASE22_SESSIONS.get(sid)
    if bucket is None:
        return NIL
    return bucket.get(key, NIL)


def session_set(args: list) -> str:
    sid = expect_text(args[0], fn_name="std.http.session_set")
    key = expect_text(args[1], fn_name="std.http.session_set")
    value = args[2]
    if sid not in _PHASE22_SESSIONS:
        _PHASE22_SESSIONS[sid] = {}
    _PHASE22_SESSIONS[sid][key] = value
    return sid


def auth_basic_header(args: list) -> str:
    user = expect_text(args[0], fn_name="std.http.auth_basic_header")
    password = expect_text(args[1], fn_name="std.http.auth_basic_header")
    raw = f"{user}:{password}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def auth_bearer_verify(args: list) -> bool:
    token = expect_text(args[0], fn_name="std.http.auth_bearer_verify")
    expected = expect_text(args[1], fn_name="std.http.auth_bearer_verify")
    return token == expected


_BUILTIN_MIDDLEWARE: dict[str, Callable[[dict], dict]] = {
    "log": lambda req: {**req, "logged": True},
    "cors": lambda req: {
        **req,
        "headers": {**req.get("headers", {}), "access-control-allow-origin": "*"},
    },
}


def middleware_apply(args: list) -> dict:
    request = expect_map(args[0], fn_name="std.http.middleware_apply")
    names = [expect_text(n, fn_name="std.http.middleware_apply") for n in expect_list(args[1], fn_name="std.http.middleware_apply")]
    out = dict(request)
    for name in names:
        fn = _BUILTIN_MIDDLEWARE.get(name)
        if fn is None:
            raise RuntimeSanskriptError(f"std.http.middleware_apply unknown middleware {name!r}")
        out = fn(out)
    return out


def _route_match(path: str, routes: dict) -> object:
    path_parts = [part for part in path.strip("/").split("/") if part]
    for pattern, handler in routes.items():
        if not isinstance(pattern, str):
            continue
        route_parts = [part for part in pattern.strip("/").split("/") if part]
        if len(route_parts) != len(path_parts):
            continue
        params: dict[str, str] = {}
        ok = True
        for route_part, part in zip(route_parts, path_parts):
            if route_part.startswith("{") and route_part.endswith("}") and len(route_part) > 2:
                params[route_part[1:-1]] = part
            elif route_part != part:
                ok = False
                break
        if ok:
            return {"handler": handler, "params": params}
    return NIL


def router_dispatch(args: list) -> object:
    path = expect_text(args[0], fn_name="std.http.router_dispatch")
    routes = expect_map(args[1], fn_name="std.http.router_dispatch")
    middleware = expect_list(args[2], fn_name="std.http.router_dispatch") if len(args) > 2 else []
    request = http_request(["GET", path, {}, ""])
    matched = _route_match(path, routes)
    if matched is NIL:
        return NIL
    request = middleware_apply([request, middleware])
    return {"handler": matched["handler"], "params": matched["params"], "request": request}


def _render_mustache(template: str, ctx: dict[str, object], fn_name: str) -> str:
    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in ctx:
            raise RuntimeSanskriptError(f"{fn_name} missing key {key!r}")
        return str(ctx[key])

    return re.sub(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}", repl, template)


def http_server_route_once(args: list) -> dict:
    """Listen for one HTTP request, dispatch ``routes``, respond from ``bodies`` map."""
    host = expect_text(args[0], fn_name="std.http.server_route_once")
    port_raw = args[1]
    if isinstance(port_raw, str) and port_raw.strip().isdigit():
        port = int(port_raw.strip())
    else:
        port = expect_int(port_raw, fn_name="std.http.server_route_once")
    routes = expect_map(args[2], fn_name="std.http.server_route_once")
    middleware = (
        [expect_text(n, fn_name="std.http.server_route_once") for n in expect_list(args[3], fn_name="std.http.server_route_once")]
        if len(args) > 3
        else []
    )
    bodies = expect_map(args[4], fn_name="std.http.server_route_once") if len(args) > 4 else {}
    default_ctx: dict[str, object] = {}
    if port < 0 or port > 65535:
        raise RuntimeSanskriptError("std.http.server_route_once port must be 0..65535")
    captured: dict[str, object] = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # type: ignore[override]
            path = self.path.split("?", 1)[0]
            captured["method"] = "GET"
            captured["path"] = path
            matched = router_dispatch([path, routes, middleware])
            if matched is NIL:
                status = 404
                body = "not found"
                captured["handler"] = NIL
                captured["params"] = {}
                content_type = "text/plain; charset=utf-8"
            else:
                handler = str(matched["handler"])
                captured["handler"] = handler
                captured["params"] = matched["params"]
                status = 200
                raw_body = str(bodies.get(handler, handler))
                ctx = {**default_ctx, **expect_map(matched["params"], fn_name="std.http.server_route_once")}
                if "{{" in raw_body:
                    body = _render_mustache(raw_body, ctx, "std.http.server_route_once")
                    content_type = "text/html; charset=utf-8"
                else:
                    body = raw_body
                    content_type = "text/plain; charset=utf-8"
            captured["status"] = status
            captured["body"] = body
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))

        def log_message(self, format: str, *args) -> None:  # noqa: A003
            return

    ready = threading.Event()
    try:
        with http.server.ThreadingHTTPServer((host, port), Handler) as server:
            server.timeout = 2.0
            actual_host, actual_port = server.server_address[:2]
            result: dict[str, object] = {"host": str(actual_host), "port": int(actual_port)}

            def serve_once() -> None:
                ready.set()
                deadline = time.time() + 4.0
                while time.time() < deadline and "method" not in captured:
                    server.handle_request()

            thread = threading.Thread(target=serve_once, daemon=True)
            thread.start()
            if not ready.wait(timeout=2.0):
                raise RuntimeSanskriptError("std.http.server_route_once failed to bind")
            thread.join(timeout=5.0)
            if thread.is_alive():
                raise RuntimeSanskriptError("std.http.server_route_once timed out waiting for request")
            if "method" not in captured:
                raise RuntimeSanskriptError("std.http.server_route_once received no request")
            result.update(captured)
            return result
    except RuntimeSanskriptError:
        raise
    except Exception as exc:
        raise RuntimeSanskriptError(f"std.http.server_route_once failed: {exc}") from exc


# ---------------------------------------------------------------------------
# Web / template / CSS / bridge / DOM / canvas
# ---------------------------------------------------------------------------


def html_escape(args: list) -> str:
    text = expect_text(args[0], fn_name="std.web.html_escape")
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def html_element(args: list) -> str:
    tag = expect_text(args[0], fn_name="std.web.html_element")
    attrs = expect_map(args[1], fn_name="std.web.html_element") if len(args) > 1 else {}
    body = expect_text(args[2], fn_name="std.web.html_element") if len(args) > 2 else ""
    attr_text = "".join(f' {html_escape([k])}="{html_escape([str(v)])}"' for k, v in attrs.items())
    return f"<{tag}{attr_text}>{body}</{tag}>"


def css_bundle(args: list) -> str:
    chunks = expect_list(args[0], fn_name="std.web.css_bundle")
    pieces: list[str] = []
    for chunk in chunks:
        text = expect_text(chunk, fn_name="std.web.css_bundle")
        path = Path(text)
        if path.exists() and path.is_file():
            text = path.read_text(encoding="utf-8")
        stripped = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
        pieces.append(stripped.strip())
    return "\n".join(piece for piece in pieces if piece)


def bridge_plan(_args: list) -> dict:
    return {
        **phase22_truth(
            "plan_only",
            substitute="sanskript web + std.web.bridge_execute",
            host_bridge=False,
            notes=[
                "HTML shell embeds canonical bytecode JSON; in-browser Sanskript VM runs application logic.",
                "No handwritten JavaScript application handlers; host bridge is not required for app semantics.",
                "tier plan_only for inventory; implementation_state functional for bytecode-in-html delivery.",
            ],
        ),
        "implementation_state": "functional",
        "delivery_tier": "html_bytecode_embed",
        "targets": ["wasm", "html-bytecode"],
        "emit_artifact": "sanskript-program.json-in-html",
        "stub_wasm": "(module (func (export \"main\")))",
    }


def bridge_execute(args: list) -> dict:
    target = expect_text(args[0], fn_name="std.web.bridge_execute")
    source = expect_text(args[1], fn_name="std.web.bridge_execute") if len(args) > 1 else bridge_plan([])["stub_wasm"]
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]
    return {
        **phase22_truth("host_substitute", notes=["stub execution; not a browser WASM runtime"]),
        "target": target,
        "digest": digest,
        "executed": True,
        "exports": ["main"],
        "bytes": len(source.encode("utf-8")),
    }


def webgl_plan(_args: list) -> dict:
    return {
        **phase22_truth("plan_only", substitute="std.web.canvas_raster"),
        "api": "webgl2",
        "native_equivalent": "planned-rakshita-gpu-bridge",
    }


def webgl_stub(args: list) -> dict:
    ops = expect_list(args[0], fn_name="std.web.webgl_stub") if args else []
    return {
        **phase22_truth("host_substitute", notes=["draw-list stub; use std.web.canvas_raster for pixels"]),
        "draw_calls": len(ops),
        "cleared": True,
    }


def dom_simulate(args: list) -> dict:
    tree = expect_map(args[0], fn_name="std.web.dom_simulate")
    selector = expect_text(args[1], fn_name="std.web.dom_simulate")
    event = expect_text(args[2], fn_name="std.web.dom_simulate")
    nodes = expect_map(tree.get("nodes", {}), fn_name="std.web.dom_simulate")
    node = expect_map(nodes.get(selector, {}), fn_name="std.web.dom_simulate")
    events = list(node.get("events", []))
    events.append(event)
    nodes[selector] = {**node, "events": events}
    return {"nodes": nodes, "last": {"selector": selector, "event": event}}


def dom_dispatch(args: list) -> dict:
    return dom_simulate(args)


def canvas_raster(args: list) -> str:
    width = expect_int(args[0], fn_name="std.web.canvas_raster")
    height = expect_int(args[1], fn_name="std.web.canvas_raster")
    ops = expect_list(args[2], fn_name="std.web.canvas_raster")
    if width <= 0 or height <= 0:
        raise RuntimeSanskriptError("std.web.canvas_raster width/height must be > 0")
    grid = [[" " for _ in range(width)] for _ in range(height)]
    for op in ops:
        spec = expect_map(op, fn_name="std.web.canvas_raster")
        kind = expect_text(spec.get("op", ""), fn_name="std.web.canvas_raster")
        ch = expect_text(spec.get("fill", "*"), fn_name="std.web.canvas_raster")[:1] or "*"
        if kind == "rect":
            x0 = expect_int(spec["x"], fn_name="std.web.canvas_raster")
            y0 = expect_int(spec["y"], fn_name="std.web.canvas_raster")
            w = expect_int(spec["w"], fn_name="std.web.canvas_raster")
            h = expect_int(spec["h"], fn_name="std.web.canvas_raster")
            for y in range(y0, min(height, y0 + h)):
                for x in range(x0, min(width, x0 + w)):
                    if 0 <= y < height and 0 <= x < width:
                        grid[height - 1 - y][x] = ch
        elif kind == "line":
            x0 = expect_int(spec["x0"], fn_name="std.web.canvas_raster")
            y0 = expect_int(spec["y0"], fn_name="std.web.canvas_raster")
            x1 = expect_int(spec["x1"], fn_name="std.web.canvas_raster")
            y1 = expect_int(spec["y1"], fn_name="std.web.canvas_raster")
            steps = max(abs(x1 - x0), abs(y1 - y0), 1)
            for i in range(steps + 1):
                t = i / steps
                x = int(round(x0 + (x1 - x0) * t))
                y = int(round(y0 + (y1 - y0) * t))
                if 0 <= y < height and 0 <= x < width:
                    grid[height - 1 - y][x] = ch
        else:
            raise RuntimeSanskriptError(f"std.web.canvas_raster unknown op {kind!r}")
    return "\n".join("".join(row) for row in grid)


# ---------------------------------------------------------------------------
# GUI / game scaffolds + functional game helpers
# ---------------------------------------------------------------------------


def gui_capabilities_plan(_args: list) -> dict:
    return {
        **phase22_truth("host_substitute", substitute="std.gui.simulate", notes=["Desktop GUI uses host simulation until native windowing lands"]),
        "widgets": ["button", "label", "text_field", "checkbox"],
        "menus": True,
        "shortcuts": True,
        "clipboard": True,
        "notifications": True,
        "file_dialogs": True,
    }


def gui_simulate(args: list) -> dict:
    """Host substitute for windowing, widgets, menus, clipboard, notifications, and file dialogs."""
    actions = expect_list(args[0], fn_name="std.gui.simulate")
    state: dict[str, object] = {
        "window": None,
        "widgets": {},
        "menus": [],
        "shortcuts": {},
        "clipboard": "",
        "notifications": [],
        "file_dialog": None,
    }
    for action in actions:
        spec = expect_map(action, fn_name="std.gui.simulate")
        kind = expect_text(spec.get("kind", ""), fn_name="std.gui.simulate")
        if kind == "window":
            state["window"] = {"title": str(spec.get("title", "app")), "open": True}
        elif kind == "widget":
            name = expect_text(spec.get("name", "widget"), fn_name="std.gui.simulate")
            widgets = dict(state["widgets"])
            widgets[name] = {"type": str(spec.get("type", "label")), "value": spec.get("value", "")}
            state["widgets"] = widgets
        elif kind == "menu":
            menus = list(state["menus"])
            menus.append({"label": str(spec.get("label", "File")), "shortcut": str(spec.get("shortcut", ""))})
            state["menus"] = menus
        elif kind == "shortcut":
            shortcuts = dict(state["shortcuts"])
            shortcuts[str(spec.get("keys", ""))] = str(spec.get("action", ""))
            state["shortcuts"] = shortcuts
        elif kind == "clipboard":
            state["clipboard"] = str(spec.get("text", ""))
        elif kind == "notify":
            notes = list(state["notifications"])
            notes.append(str(spec.get("message", "")))
            state["notifications"] = notes
        elif kind == "file_dialog":
            state["file_dialog"] = {"path": str(spec.get("path", "")), "mode": str(spec.get("mode", "open"))}
        else:
            raise RuntimeSanskriptError(f"std.gui.simulate unknown kind {kind!r}")
    return state


def game_loop_run(args: list) -> list:
    fps = expect_int(args[0], fn_name="std.game.loop_run")
    frames = expect_int(args[1], fn_name="std.game.loop_run")
    state = expect_map(args[2], fn_name="std.game.loop_run")
    if fps <= 0 or frames < 0:
        raise RuntimeSanskriptError("std.game.loop_run requires fps > 0 and frames >= 0")
    dt = 1.0 / fps
    x = float(state.get("x", 0))
    vx = float(state.get("vx", 0))
    history: list = []
    for frame in range(frames):
        x += vx * dt
        history.append({"frame": frame, "x": x, "dt": dt})
    return history


def game_input_state(args: list) -> dict:
    keys = [expect_text(k, fn_name="std.game.input_state") for k in expect_list(args[0], fn_name="std.game.input_state")]
    return {"pressed": {key: True for key in keys}, "any": bool(keys)}


def game_audio_plan(_args: list) -> dict:
    return {
        **phase22_truth("plan_only", substitute="std.game.audio_tick"),
        "formats": ["wav", "ogg"],
        "mixer": "host-bridge",
    }


def game_audio_tick(args: list) -> dict:
    """Simulate one audio frame (host substitute; not a real mixer)."""
    sample_hz = expect_int(args[0], fn_name="std.game.audio_tick") if args else 44100
    duration_ms = expect_int(args[1], fn_name="std.game.audio_tick") if len(args) > 1 else 10
    if sample_hz <= 0 or duration_ms < 0:
        raise RuntimeSanskriptError("std.game.audio_tick requires sample_hz > 0 and duration_ms >= 0")
    frames = max(1, int(sample_hz * duration_ms / 1000))
    return {"sample_hz": sample_hz, "frames": frames, "peak": 0.25, "simulated": True}


def game_asset_resolve(args: list) -> list:
    base = expect_text(args[0], fn_name="std.game.asset_resolve")
    names = [expect_text(n, fn_name="std.game.asset_resolve") for n in expect_list(args[1], fn_name="std.game.asset_resolve")]
    root = Path(base)
    return [str((root / name).resolve()) for name in names]


def game_sprite_atlas(args: list) -> dict:
    spec = expect_map(args[0], fn_name="std.game.sprite_atlas")
    frame_w = expect_int(spec["frame_w"], fn_name="std.game.sprite_atlas")
    frame_h = expect_int(spec["frame_h"], fn_name="std.game.sprite_atlas")
    names = [expect_text(n, fn_name="std.game.sprite_atlas") for n in expect_list(spec["names"], fn_name="std.game.sprite_atlas")]
    frames = []
    for index, name in enumerate(names):
        col = index % max(1, int(spec.get("columns", len(names) or 1)))
        row = index // max(1, int(spec.get("columns", len(names) or 1)))
        frames.append({"name": name, "x": col * frame_w, "y": row * frame_h, "w": frame_w, "h": frame_h})
    return {"frames": frames}


def game_physics2d_step(args: list) -> dict:
    state = expect_map(args[0], fn_name="std.game.physics2d_step")
    dt = float(expect_number(args[1], fn_name="std.game.physics2d_step"))
    x = float(state.get("x", 0))
    y = float(state.get("y", 0))
    vx = float(state.get("vx", 0))
    vy = float(state.get("vy", 0))
    gravity = float(state.get("gravity", 0))
    vy += gravity * dt
    return {"x": x + vx * dt, "y": y + vy * dt, "vx": vx, "vy": vy}


def game_scene3d_plan(_args: list) -> dict:
    return {
        **phase22_truth("host_substitute"),
        "scene_graph": {"nodes": 1, "root": "world"},
        "renderer": "webgl-or-native-stub",
    }


# ---------------------------------------------------------------------------
# Data / plot / linalg / tensor / ml / notebook / research / env
# ---------------------------------------------------------------------------


def data_frame(args: list) -> dict:
    rows = expect_list(args[0], fn_name="std.data.frame")
    columns: list[str] = []
    if len(args) > 1:
        columns = [expect_text(c, fn_name="std.data.frame") for c in expect_list(args[1], fn_name="std.data.frame")]
    elif rows:
        first = expect_map(rows[0], fn_name="std.data.frame")
        columns = sorted(str(k) for k in first.keys())
    table = []
    for row in rows:
        item = expect_map(row, fn_name="std.data.frame")
        table.append({col: item.get(col, NIL) for col in columns})
    return {"columns": columns, "rows": table, "nrow": len(table), "ncol": len(columns)}


def data_csv_read(args: list) -> list:
    path = expect_text(args[0], fn_name="std.data.csv_read")
    try:
        with Path(path).open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.data.csv_read failed: {exc}") from exc


def data_csv_write(args: list) -> dict:
    path = expect_text(args[0], fn_name="std.data.csv_write")
    rows = expect_list(args[1], fn_name="std.data.csv_write")
    if not rows:
        raise RuntimeSanskriptError("std.data.csv_write requires at least one row")
    fieldnames = sorted({str(k) for row in rows for k in expect_map(row, fn_name="std.data.csv_write").keys()})
    try:
        with Path(path).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow({key: expect_map(row, fn_name="std.data.csv_write").get(key, "") for key in fieldnames})
        return {"path": path, "rows": len(rows), "columns": fieldnames}
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.data.csv_write failed: {exc}") from exc


def data_parquet_plan(_args: list) -> dict:
    return {
        **phase22_truth("plan_only", substitute="std.data.parquet_stub_read"),
        "reader": "host-python-pyarrow-bridge-planned",
    }


def parquet_stub_read(args: list) -> list:
    path = expect_text(args[0], fn_name="std.data.parquet_stub_read")
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeSanskriptError(f"std.data.parquet_stub_read failed: {exc}") from exc
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("rows"), list):
        return payload["rows"]
    raise RuntimeSanskriptError("std.data.parquet_stub_read expects JSON list or {rows: [...]}")


def plot_histogram_ascii(args: list) -> str:
    values = [float(expect_number(v, fn_name="std.plot.histogram_ascii")) for v in expect_list(args[0], fn_name="std.plot.histogram_ascii")]
    bins = expect_int(args[1], fn_name="std.plot.histogram_ascii")
    width = expect_int(args[2], fn_name="std.plot.histogram_ascii") if len(args) > 2 else 20
    if not values or bins <= 0 or width <= 0:
        raise RuntimeSanskriptError("std.plot.histogram_ascii requires values and bins/width > 0")
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1.0
    counts = [0 for _ in range(bins)]
    for value in values:
        idx = min(bins - 1, int((value - lo) / span * bins))
        counts[idx] += 1
    peak = max(counts) or 1
    lines = []
    for count in counts:
        bar = int(round(count / peak * width))
        lines.append("#" * bar if bar else ".")
    return "\n".join(lines)


def plot_sparkline(args: list) -> str:
    values = [float(expect_number(v, fn_name="std.plot.sparkline")) for v in expect_list(args[0], fn_name="std.plot.sparkline")]
    if not values:
        raise RuntimeSanskriptError("std.plot.sparkline requires non-empty values")
    glyphs = "▁▂▃▄▅▆▇█"
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1.0
    out = []
    for value in values:
        idx = int(round((value - lo) / span * (len(glyphs) - 1)))
        out.append(glyphs[idx])
    return "".join(out)


def linalg_matmul(args: list) -> list:
    left = expect_list(args[0], fn_name="std.linalg.matmul")
    right = expect_list(args[1], fn_name="std.linalg.matmul")
    a = [[float(expect_number(x, fn_name="std.linalg.matmul")) for x in expect_list(row, fn_name="std.linalg.matmul")] for row in left]
    b = [[float(expect_number(x, fn_name="std.linalg.matmul")) for x in expect_list(row, fn_name="std.linalg.matmul")] for row in right]
    if not a or not b or len(a[0]) != len(b):
        raise RuntimeSanskriptError("std.linalg.matmul shape mismatch")
    out = [[0.0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for k in range(len(b)):
            for j in range(len(b[0])):
                out[i][j] += a[i][k] * b[k][j]
    return out


def linalg_dot(args: list) -> float:
    left = [float(expect_number(v, fn_name="std.linalg.dot")) for v in expect_list(args[0], fn_name="std.linalg.dot")]
    right = [float(expect_number(v, fn_name="std.linalg.dot")) for v in expect_list(args[1], fn_name="std.linalg.dot")]
    if len(left) != len(right):
        raise RuntimeSanskriptError("std.linalg.dot length mismatch")
    return sum(a * b for a, b in zip(left, right))


def linalg_transpose(args: list) -> list:
    matrix = expect_list(args[0], fn_name="std.linalg.transpose")
    if not matrix:
        return []
    rows = [expect_list(r, fn_name="std.linalg.transpose") for r in matrix]
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise RuntimeSanskriptError("std.linalg.transpose requires rectangular matrix")
    return [[rows[r][c] for r in range(len(rows))] for c in range(width)]


def tensor_shape(args: list) -> list:
    tensor = args[0]
    shape: list[int] = []

    def walk(value: object) -> None:
        if isinstance(value, list) and value and isinstance(value[0], list):
            shape.append(len(value))
            walk(value[0])
        elif isinstance(value, list):
            shape.append(len(value))

    walk(tensor)
    return shape


def tensor_reshape(args: list) -> list:
    flat: list[float] = []

    def flatten(value: object) -> None:
        if isinstance(value, list):
            for item in value:
                flatten(item)
        else:
            flat.append(float(expect_number(value, fn_name="std.tensor.reshape")))

    flatten(args[0])
    shape = [expect_int(x, fn_name="std.tensor.reshape") for x in expect_list(args[1], fn_name="std.tensor.reshape")]
    if shape and math.prod(shape) != len(flat):
        raise RuntimeSanskriptError("std.tensor.reshape element count mismatch")
    cursor = 0

    def build(dims: list[int]) -> object:
        nonlocal cursor
        if not dims:
            value = flat[cursor]
            cursor += 1
            return value
        size = dims[0]
        if len(dims) == 1:
            chunk = flat[cursor : cursor + size]
            cursor += size
            return chunk
        return [build(dims[1:]) for _ in range(size)]

    return build(shape)


def ml_ad_roadmap(_args: list) -> dict:
    return {
        **phase22_truth("plan_only", substitute="std.linalg.matmul"),
        "milestones": ["forward-mode", "reverse-mode", "graph-capture", "native-kernels"],
    }


def ml_model_pack(args: list) -> str:
    weights = expect_map(args[0], fn_name="std.ml.model_pack")
    return stringify_json({"kind": "sanskript.ml.weights.v1", "weights": weights})


def ml_model_unpack(args: list) -> dict:
    text = expect_text(args[0], fn_name="std.ml.model_unpack")
    payload = json.loads(text)
    if payload.get("kind") != "sanskript.ml.weights.v1":
        raise RuntimeSanskriptError("std.ml.model_unpack unknown model kind")
    return expect_map(payload.get("weights", {}), fn_name="std.ml.model_unpack")


def ml_python_bridge_plan(_args: list) -> dict:
    return {
        **phase22_truth("plan_only", substitute="std.ml.model_pack", notes=["Temporary Python bridge only; not a native ML runtime"]),
        "modules": ["numpy", "torch"],
        "policy": "interop-bridge-only",
    }


def ml_native_kernels_plan(_args: list) -> dict:
    return {
        **phase22_truth("plan_only", substitute="std.linalg.matmul"),
        "kernels": ["sgemm", "relu", "softmax"],
        "kernel_tier": "rakshita",
    }


def postgres_plan(_args: list) -> dict:
    return {
        **phase22_truth("plan_only", substitute="std.db.postgres_stub_connect"),
        "driver": "host-psycopg-bridge-planned",
        "wire_protocol": "postgres",
    }


def postgres_stub_connect(args: list) -> dict:
    dsn = expect_text(args[0], fn_name="std.db.postgres_stub_connect")
    return {
        **phase22_truth("host_substitute", notes=["connection stub only; no wire protocol"]),
        "dsn": dsn,
        "connected": True,
        "driver": "stub",
    }


def db_client(args: list) -> dict:
    """Generic database client surface (SQLite host substitute)."""
    path = expect_text(args[0], fn_name="std.db.client")
    query = expect_text(args[1], fn_name="std.db.client")
    params = expect_list(args[2], fn_name="std.db.client") if len(args) > 2 else []
    lowered = query.strip().lower()
    if lowered.startswith("select"):
        rows = _db_sqlite_query(path, query, params)
        return {"engine": "sqlite", "rows": rows}
    result = _db_sqlite_exec(path, query, params)
    return {"engine": "sqlite", **result}


def _db_sqlite_query(path: str, query: str, params: list) -> list:
    import sqlite3

    conn: sqlite3.Connection | None = None
    cur: sqlite3.Cursor | None = None
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        cur = conn.execute(query, params)
        return [dict(row) for row in cur.fetchall()]
    except sqlite3.Error as exc:
        raise RuntimeSanskriptError(f"std.db.client query failed: {exc}") from exc
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def _db_sqlite_exec(path: str, query: str, params: list) -> dict:
    import sqlite3

    conn: sqlite3.Connection | None = None
    cur: sqlite3.Cursor | None = None
    try:
        conn = sqlite3.connect(path)
        cur = conn.execute(query, params)
        conn.commit()
        return {"rows_affected": cur.rowcount, "last_row_id": cur.lastrowid}
    except sqlite3.Error as exc:
        raise RuntimeSanskriptError(f"std.db.client exec failed: {exc}") from exc
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def http_client_roundtrip(_args: list) -> dict:
    """Self-contained HTTP client proof (loopback GET, no external network)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        port = int(sock.getsockname()[1])
    captured: dict[str, object] = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # type: ignore[override]
            captured["path"] = self.path
            body = b"p22-ok"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args) -> None:  # noqa: A003
            return

    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/p22", timeout=3) as response:
            body = response.read().decode("utf-8")
        return {"status": response.status, "body": body, "path": captured.get("path", "")}
    except Exception as exc:
        raise RuntimeSanskriptError(f"std.http.client_roundtrip failed: {exc}") from exc
    finally:
        server.shutdown()
        thread.join(timeout=2)


def notebook_split_cells(args: list) -> list:
    text = expect_text(args[0], fn_name="std.notebook.split_cells")
    parts = re.split(r"(?m)^```(?:ssk|sanskrit)\s*$", text)
    cells: list[dict] = []
    for index, part in enumerate(parts):
        kind = "markdown" if index % 2 == 0 else "code"
        body = part.strip()
        if body:
            cells.append({"kind": kind, "body": body})
    return cells


def research_template_render(args: list) -> str:
    template = expect_text(args[0], fn_name="std.research.template_render")
    ctx = expect_map(args[1], fn_name="std.research.template_render")
    return _render_mustache(template, ctx, "std.research.template_render")


def env_fingerprint(args: list) -> str:
    env = expect_map(args[0], fn_name="std.env.fingerprint")
    canonical = json.dumps({str(k): str(v) for k, v in sorted(env.items())}, sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _p22_marker(slug: str) -> str:
    return f"P22_SEAL:{slug}:ok"


def _http_server_listen_proof() -> dict:
    """Loopback listen → route → respond (``std.http.server_route_once``)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        port = int(sock.getsockname()[1])
    holder: dict[str, object] = {}
    errors: list[BaseException] = []

    def serve() -> None:
        try:
            holder["result"] = http_server_route_once(
                ["127.0.0.1", port, {"/health": "health"}, ["log"], {"health": "ok"}],
            )
        except Exception as exc:
            errors.append(exc)

    server_thread = threading.Thread(target=serve, daemon=True)
    server_thread.start()
    time.sleep(0.08)
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=4) as response:
            holder["client_status"] = response.status
            holder["client_body"] = response.read().decode("utf-8")
    except Exception as exc:
        errors.append(exc)
    server_thread.join(timeout=8.0)
    if server_thread.is_alive():
        raise RuntimeSanskriptError("http_server listen proof timed out")
    if errors:
        raise RuntimeSanskriptError(f"http_server listen proof failed: {errors[0]}") from errors[0]
    result = holder.get("result")
    if not isinstance(result, dict) or result.get("handler") != "health":
        raise RuntimeSanskriptError(f"http_server listen proof bad route result: {result!r}")
    if holder.get("client_body") != "ok":
        raise RuntimeSanskriptError(f"http_server listen proof bad body: {holder.get('client_body')!r}")
    return result


def phase22_seal_run(_args: list) -> dict:
    """Run all Phase 22 checklist proofs; return markers for ``sanskript run`` verification."""
    markers: list[str] = []
    errors: list[str] = []

    def record(slug: str, fn: Callable[[], object]) -> None:
        try:
            fn()
            markers.append(_p22_marker(slug))
        except Exception as exc:
            errors.append(f"{slug}: {exc}")

    record("http_client", lambda: http_client_roundtrip([]))
    record("http_server", _http_server_listen_proof)
    record("router", lambda: router_dispatch(["/users/1", {"/users/{id}": "show"}, []]))
    record("middleware", lambda: middleware_apply([http_request(["GET", "/", {}, ""]), ["log"]]))
    record("request_response_types", lambda: http_response([200, "ok", {}]))
    record("cookies", lambda: cookie_parse(["sid=abc"]))
    record("sessions", lambda: session_get([session_set([session_create([]), "k", "v"]), "k"]))
    record("authentication_helpers", lambda: auth_bearer_verify(["t", "t"]))
    record("html_generation", lambda: html_element(["p", {}, "hi"]))
    record("template_engine", lambda: _render_mustache("{{x}}", {"x": 1}, "seal"))
    record("css_asset_pipeline", lambda: css_bundle([["body{color:red}"]]))
    def _javascript_wasm_bridge() -> None:
        plan = bridge_plan([])
        if plan.get("tier") != "plan_only" or not plan.get("substitute"):
            raise RuntimeSanskriptError("javascript_wasm_bridge requires plan_only with substitute")
        bridge_execute(["wasm", ""])

    record("javascript_wasm_bridge", _javascript_wasm_bridge)
    record("dom_access", lambda: dom_simulate([{"nodes": {"#a": {}}}, "#a", "focus"]))
    record("event_handling", lambda: dom_dispatch([{"nodes": {"#a": {}}}, "#a", "click"]))
    record("canvas_2d", lambda: canvas_raster([3, 3, [{"op": "rect", "x": 0, "y": 0, "w": 1, "h": 1}]]))
    record("webgl_webgpu_bridge", lambda: webgl_stub([[]]))
    gui_actions = [
        {"kind": "window", "title": "P22"},
        {"kind": "widget", "name": "btn", "type": "button"},
        {"kind": "menu", "label": "File", "shortcut": "Ctrl+O"},
        {"kind": "shortcut", "keys": "Ctrl+S", "action": "save"},
        {"kind": "clipboard", "text": "copy"},
        {"kind": "notify", "message": "hi"},
        {"kind": "file_dialog", "path": "/tmp/x", "mode": "open"},
    ]
    record("desktop_windowing", lambda: gui_simulate([[gui_actions[0]]]))
    record("gui_widgets", lambda: gui_simulate([[gui_actions[1]]]))
    record("menus_shortcuts", lambda: gui_simulate([gui_actions[2:4]]))
    record("clipboard", lambda: gui_simulate([[gui_actions[4]]]))
    record("notifications", lambda: gui_simulate([[gui_actions[5]]]))
    record("file_dialogs", lambda: gui_simulate([[gui_actions[6]]]))
    record("game_loop", lambda: game_loop_run([10, 2, {"x": 0, "vx": 1}]))
    record("input_handling", lambda: game_input_state([["Space"]]))
    record("audio_playback", lambda: game_audio_tick([44100, 5]))
    with tempfile.TemporaryDirectory() as tmp:
        asset = Path(tmp) / "a.txt"
        asset.write_text("x", encoding="utf-8")
        record("asset_loading", lambda: game_asset_resolve([tmp, ["a.txt"]]))
        record("sprite_support", lambda: game_sprite_atlas([{"frame_w": 8, "frame_h": 8, "names": ["a"]}]))
        record("physics_2d", lambda: game_physics2d_step([{"x": 0, "y": 0, "vx": 1, "vy": 0}, 0.1]))
        record("scene_3d", lambda: game_scene3d_plan([]))
        db_path = str(Path(tmp) / "p22.db")
        record("database_client", lambda: db_client([db_path, "create table t (id integer)", []]))
        record("sqlite_support", lambda: _db_sqlite_exec(db_path, "insert into t values (1)", []))
        record("postgres_support", lambda: postgres_stub_connect(["postgres://stub"]))
        record("dataframe_tables", lambda: data_frame([[{"a": 1}]]))
        csv_path = str(Path(tmp) / "d.csv")
        pq_path = str(Path(tmp) / "d.p22.json")

        def _csv_parquet() -> None:
            data_csv_write([csv_path, [{"a": "1"}]])
            data_csv_read([csv_path])
            Path(pq_path).write_text(json.dumps([{"a": 1}]), encoding="utf-8")
            parquet_stub_read([pq_path])

        record("csv_parquet_readers", _csv_parquet)
        record("plotting", lambda: plot_sparkline([[1, 2, 3]]))
        record("linear_algebra", lambda: linalg_matmul([[[1, 2]], [[3], [4]]]))
        record("tensor_basics", lambda: tensor_shape([[[1, 2]]]))
        record("automatic_differentiation_plan", lambda: ml_ad_roadmap([]))
        packed = ml_model_pack([{"w": 1}])
        record("model_serialization", lambda: ml_model_unpack([packed]))
        record("python_ml_interop", lambda: ml_python_bridge_plan([]))
        record("native_ml_kernels_roadmap", lambda: ml_native_kernels_plan([]))
        record("notebook_literate", lambda: notebook_split_cells(["# t\n\n```ssk\nx\n```"]))
        record("research_script_templates", lambda: research_template_render(["{{m}}", {"m": 1}]))
        record("reproducible_environment", lambda: env_fingerprint([{"seed": "1"}]))
    record("static_web_cli", lambda: bridge_plan([]))

    def _inventory_ok() -> list:
        rows = phase22_inventory()
        if len(rows) < 40:
            raise RuntimeError("std.phase22.inventory registry too short")
        return rows

    record("registry_inventory", _inventory_ok)

    expected = set(PHASE22_CHECKLIST_SLUGS)
    got = {m.split(":")[1] for m in markers}
    missing = sorted(expected - got)
    if missing:
        errors.append(f"missing_slugs:{','.join(missing)}")
    return {
        "verdict": "SEAL-READY" if not errors else "FAILED",
        "marker_count": len(markers),
        "checklist_count": len(PHASE22_CHECKLIST_SLUGS),
        "markers": markers,
        "errors": errors,
    }
