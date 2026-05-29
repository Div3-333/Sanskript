# Phase 22: Web, Apps, Games, Research, And ML

**Verdict: SEAL-READY (`host_scaffold_acceptable`).** All **46** independence-checklist rows are proven with `sanskript run` and emit `P22_SEAL:<slug>:ok` markers from `std.phase22.seal_run`. Browser DOM, desktop GUI, Postgres wire protocol, Parquet readers, and native ML kernels remain **host substitutes** or **plan_only** — not shipped product platforms.

## Full seal (all checklist rows)

| Artifact | Command | Test |
| --- | --- | --- |
| All 46 rows | `python -m sanskript.cli run examples/phase22-full-seal.ssk` | `tests/test_phase22_web_apps_games_research_ml.py::Phase22FullSealTests::test_phase22_full_seal_example_executes` |
| Seal matrix native | (inside full-seal JSON) | `...::test_phase22_seal_run_native_passes` |

## Seal bar (dedicated examples)

| Artifact | Command | Test |
| --- | --- | --- |
| HTTP micro-service (listen → route → respond) | `python -m sanskript.cli run examples/phase22-http-service.ssk` | `...::test_phase22_http_service_listen_route_respond` |
| Router + middleware + cookies + sessions + auth driver | `python -m sanskript.cli run examples/phase22-http-router-auth.ssk` | `...::test_phase22_http_router_auth_driver_executes` |
| HTML generation + template stdout | `python -m sanskript.cli run examples/phase22-html-template.ssk` | `...::test_phase22_html_template_example_executes` |
| Research CLI baseline | `python -m sanskript.cli run examples/phase22-research-cli-baseline.ssk` | `...::test_phase22_research_cli_baseline_executes` |

Native bridge: `std.http.server_route_once` dispatches one request through `std.http.router_dispatch` and returns JSON on stdout (host Python `http.server`).

## Tier labels

| Tier | Meaning |
| --- | --- |
| **functional_host** | Callable from Sanskript; semantics on CPython host (HTTP loopback, SQLite, seal runner). |
| **host_substitute** | Runnable simulation or stdout artifact; not browser/desktop/ML product. |
| **plan_only** | Roadmap JSON with documented substitute (e.g. Postgres → SQLite, Parquet → CSV). |

## Impossible without substitute (honest)

These checklist rows are **[x] with substitutes**, not native/browser products:

| Row | Cannot ship today | Working substitute |
| --- | --- | --- |
| JavaScript/WASM bridge | No WASM linker in VM | `std.web.bridge_plan` + `sanskript web` static HTML |
| DOM / events | No browser API in VM | `std.web.dom_simulate` / `std.web.dom_dispatch` |
| WebGL/WebGPU | No GPU bridge | `std.web.webgl_plan` + `std.web.canvas_raster` |
| Desktop GUI / widgets / menus / clipboard / notifications / file dialogs | No windowing toolkit | `std.gui.simulate` in-memory state machine |
| Postgres | No psycopg wire driver | `std.db.postgres_plan` + `std.db.sqlite_*` |
| Parquet | No pyarrow reader in VM | `std.data.parquet_plan` + `std.data.csv_read/write` |
| Python ML / native kernels | No training runtime | `std.ml.*_plan` + `std.ml.model_pack` + `std.linalg.matmul` |
| 3D scene / audio mixer | No engine | `std.game.scene3d_plan` / `std.game.audio_plan` + 2D/audio_tick simulation |

## Related Work

- Phase 14 ergonomics: `docs/phase14-surakshita-capability.md`
- Host-bridge regression: `tests/test_phase22_web_apps_games_research.py`
- Phase 23: real async/concurrency prerequisites
