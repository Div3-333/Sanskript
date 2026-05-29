# Phase 21: Cross-Platform System Support

**Verdict: SEAL-READY (23/23 checklist rows).** Gate: `python -m sanskript.cli phase21-seal-check` (exit 0).

Phase 21 adds host-executable cross-platform system APIs and an evidence matrix that
separates **functional** behavior from **hosted simulation** and **plan-only** bridges.

## Honest Scope Boundaries

### Functional on the current VM host

- Path semantics per platform family via `std.path.for_platform`, `std.path.web_normalize`, `std.path.separator`.
- Host process execution via `std.process.run` and `std.process.run_for_platform` (host family only).
- Polling file-watch snapshots via `std.watch.snapshot`, `std.watch.diff`, `std.watch.poll_once`.
- Socket networking on the host family: `std.net.resolve_host`, `std.net.tcp_probe`, `std.net.dns_lookup`.
- TLS availability/probe on the host when the Python `ssl` module is present: `std.net.tls_available`, `std.net.tls_probe`.
- Terminal tty detection and ANSI helpers: `std.terminal.is_tty`, `std.terminal.*`.
- Platform feature detection: `std.platform.detect`, `std.platform.feature`, `std.platform.compile_plan`.
- Phase 9 platform package assets (`[platform]` keys in `ssk.toml`).

### Hosted simulation (functional at tier `hosted_simulation`, not browser/OS native)

- Web worker message queue: `std.process.web_worker_new`, `std.process.web_post_message`, `std.process.web_recv`.
- Web storage key/value API: `std.storage.web_*` (file-backed JSON under `$SANSKRIPT_WEB_STORAGE`; browser localStorage/IndexedDB shim documented in `phase21_cross_platform.WEB_STORAGE_BROWSER_SHIM`).
- Browser console logging: `std.console.log`.
- Browser fetch bridge: `std.net.browser_fetch_sim` (host `urllib` HTTP attempt; not `fetch()`).

### Plan-only metadata

- `std.net.browser_fetch_plan` — routing metadata only (no HTTP).
- Web file-watch events (no `std.watch.*` on web family yet).
- Real browser IndexedDB/localStorage, Worker threads, and ReadDirectoryChangesW on non-Linux Windows hosts (polling/inotify used instead).

## Standard Library Surface

| Area | Functions |
|------|-----------|
| Path | `std.path.for_platform`, `std.path.web_normalize`, `std.path.separator` |
| Process | `std.process.run_for_platform`, `std.process.web_worker_new`, `std.process.web_post_message`, `std.process.web_recv` |
| Watch | `std.watch.snapshot`, `std.watch.diff`, `std.watch.poll_once` |
| Storage | `std.storage.web_set/get/remove/clear/keys` |
| Net | `std.net.dns_lookup`, `std.net.tls_available`, `std.net.tls_probe`, `std.net.browser_fetch_plan`, `std.net.browser_fetch_sim` |
| Terminal | `std.terminal.is_tty`, `std.console.log` |
| Platform | `std.platform.detect`, `std.platform.feature`, `std.platform.compile_plan` |

## Reproducible Commands

From repo root:

```powershell
$env:PYTHONPATH = "src"
python -m sanskript.cli run examples/phase21-cross-platform.ssk
python -m sanskript.cli phase21-evidence --out-dir artifacts/phase21/evidence --plan-json artifacts/phase21/evidence/phase21-evidence.json
python -m pytest tests/test_phase21_cross_platform.py -q
python -m sanskript.cli phase21-seal-check
```

## Evidence Artifacts

`phase21-evidence` writes:

- `phase21-evidence.json` — per-platform capability rows with `implementation_state` and `truth_claims`
- `phase21-test-matrix.json` — matrix metadata for CI routing
- `release/<family>/release-plan.json` — release artifact plans per platform family

## Migration Notes

- Prefer `std.path.for_platform` over hand-rolled separator logic when generating paths for another target.
- Use `std.process.run_for_platform` when source must declare the intended process API family; foreign families fail fast on the host.
- Treat `std.storage.web_*` and web worker APIs as portable **simulation** until a browser runtime bridge exists.
