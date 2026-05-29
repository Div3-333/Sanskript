# Phase 14 Surakshita Capability

Phase 14 provides a practical high-level baseline for day-to-day Sanskript app work: files, templates, package CLI, and **host-bootstrap** helpers for HTTP/DB/async demos.

This phase is validated by executable tests and examples in this repo. Claims are intentionally constrained to user-visible behavior (commands and runnable programs), not only API surface presence.

**Not Phase 22:** Web apps, games, GUI, and ML are **not** seal-ready. See [`phase22-web-apps-games-research-ml.md`](phase22-web-apps-games-research-ml.md) for explicit blockers. Phase 14 `std.http.*`, `std.web.*`, `std.data.*`, `std.plot.*`, and `std.db.*` are bootstrap stubs — not product HTTP servers, dataframe stacks, or browser DOM platforms.

## What Is Included

- Managed runtime defaults and null-safe option/result values (`src/sanskript/runtime_values.py`).
- Ergonomic text/collection/map/file/format APIs via `std.*` (`src/sanskript/stdlib_impl.py`).
- HTTP client and one-request server baseline:
  - `std.http.get`
  - `std.http.post_json`
  - `std.http.server_once`
- Data/visualization baseline:
  - `std.data.column`
  - `std.data.describe`
  - `std.plot.ascii`
- Web baseline:
  - `std.web.route_match`
  - `std.web.render`
- DB baseline:
  - `std.db.sqlite_exec`
  - `std.db.sqlite_query`
- Async/task baseline:
  - `std.async.sleep_ms`
  - `std.async.read_text`
  - `std.task.run_after_ms`
  - `std.task.schedule`
- CLI usability baseline (`src/sanskript/cli.py`):
  - `sanskript repl`
  - `sanskript run`
  - `sanskript web`
  - `sanskript docs`
  - `sanskript install`
  - `sanskript pack`
  - `sanskript native-build` (cross-target artifact planning + portable bytecode output)

## End-User Reality Checklist

- Managed defaults and option safety:
  - Option truthiness and nil handling are runtime-level defaults (`OptionValue`, `NIL`) exercised in `tests/test_phase14_surakshita.py`.
- Ergonomic text/collections/maps/errors:
  - String shaping, map/route extraction, and template-key failure paths are executed in `tests/test_phase14_surakshita.py`.
- Script/REPL/CLI:
  - `run`, `repl`, `docs`, `install`, `pack`, and `web` commands are covered by CLI tests.
- File/template/package/CLI testing:
  - File read/write/append, string templates, `install`/`pack`/`docs`, and CLI `run`/`repl`/`web` flows are exercised by tests.
- Host-bootstrap HTTP/DB/async (Phase 22 blockers remain):
  - `std.http.get`/`post_json`, one-shot `server_once`, `route_match`, SQLite exec/query, `async.sleep_ms`, and `task.run_after_ms` are tested via `call_native_function` and `examples/phase14-surakshita.ssk` — not as shipped web/game/ML products.
- Modules and package install:
  - Module import and package wiring are represented by Phase 9 module examples plus Phase 14 `install` flow tests.
- Cross-platform app artifacts:
  - `native-build --backend portable-bytecode --target ...` is tested as a user flow for deterministic artifact generation without overstating native-link maturity.

## Practical Flows

- Run script:
  - `python -m sanskript.cli run examples/phase14-surakshita.ssk`
- Experiment live:
  - `python -m sanskript.cli repl`
- Generate docs:
  - `python -m sanskript.cli docs examples/phase6-functions.ssk -o artifacts/phase14/functions.md`
- Install a local package into vendor baseline:
  - `python -m sanskript.cli install ../some-local-lib --name some_local_lib`
- Create a baseline artifact:
  - `python -m sanskript.cli pack examples`
- Build a browser app artifact:
  - `python -m sanskript.cli web examples/phase14-surakshita.ssk -o artifacts/phase14/app.html`
- Build cross-target portable runtime artifact:
  - `python -m sanskript.cli native-build examples/phase14-surakshita.ssk --backend portable-bytecode --target x86_64-unknown-linux-gnu --out-dir artifacts/phase14/native-linux`

## Migration Notes

- Python `requests.get/post(json=...)` -> `std.http.get` / `std.http.post_json`.
- Python `http.server` prototypes -> `std.http.server_once` for bootstrapping handlers/tests.
- Python `sqlite3` quick scripts -> `std.db.sqlite_exec` + `std.db.sqlite_query`.
- Python `asyncio.sleep` + simple file read tasks -> `std.async.sleep_ms` + `std.async.read_text`.
- Python ad-hoc scheduling loops -> `std.task.schedule` / `std.task.run_after_ms`.
- Python markdown inventory scripts -> `sanskript docs`.
- Manual zip packaging -> `sanskript pack`.
