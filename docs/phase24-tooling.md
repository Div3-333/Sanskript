# Phase 24: Tooling (Full Seal)

Phase 24 consolidates developer tooling behind explicit CLI commands and a
machine-readable evidence matrix. All 27 catalog tools are **functional** or
**partial** with honest `truth_claims`; `verify_phase24_anti_fake()` enforces
implementation depth (breakpoints on the tracing debugger, stdio LSP handlers,
installer zip artifacts, migration skeleton output).

## Status markers

| Marker | Meaning |
|--------|---------|
| functional | CLI dispatches; adversarial smoke passes |
| partial | Works with documented limits (local vendor install, wall-clock profiler) |
| scaffold | Not used in Phase 24 full seal — reserved for future over-claim guards |

`TOOL_CATALOG` in `src/sanskript/phase24_tooling.py` is the machine-readable source
of truth. `PHASE24_SCAFFOLD_TOOL_IDS` is empty after full seal.

## Implementation depth

| Tool | CLI | State | Notes |
|------|-----|-------|-------|
| Compiler | `compile` | functional | Portable `.sskbc` |
| Runner | `run` | functional | `.ssk` / `.sskbc` / `.sskyp` |
| REPL | `repl` | functional | Single-line eval |
| Formatter | `format` | functional | Parse-validates before layout; invalid syntax exits non-zero |
| Linter | `lint` | functional | Warning/error levels |
| Test runner | `test` | functional | Discovers `std.test.*`; empty root → exit 1 |
| Benchmark | `bench`, `performance` | functional | Quiet VM timing; empty corpus → exit 1 |
| Package manager | `install`, `pack` | partial | Local vendor install + zip bundle |
| Build tool | `build` | functional | Compiles project `.ssk` → `dist/bytecode`; empty tree → exit 1 |
| Docs generator | `docs` | functional | Module/function index markdown |
| Coverage | `coverage` | functional | Opcode/IP coverage via tracing VM |
| Profiler | `profile` | partial | Wall-clock opcode estimates |
| Debugger | `debug` | functional | Breakpoints + step in `TracingVM`; Phase 18 artifacts optional |
| Language server | `lsp` | functional | Capabilities JSON; `lsp --stdio` JSON-RPC (initialize, hover) |
| Syntax highlighter | `highlight` | functional | TextMate grammar JSON |
| Editor integration | `editor-integration` | functional | Grammar + VS Code launch for `lsp --stdio` |
| Project templates | `new` | functional | `app` / `lib` skeletons |
| Dependency updater | `deps-update` | functional | Refreshes `ssk.lock` |
| Release builder | `release` | functional | Zip + sidecar manifest |
| Installer | `installer` | functional | Zip bundle + launcher (not native MSI/DEB) |
| Playground | `playground` | functional | Local HTML runner |
| Web playground | `web`, `web-playground` | functional | Static browser bundle |
| Trace viewer | `trace-view` | functional | HTML from trace JSON |
| Bytecode inspector | `inspect-bytecode` | functional | Structured opcode report |
| `.sskyp` inspector | `inspect-sskyp` | functional | Prose inventory + roundtrip sample |
| Python migration | `migrate-python` | functional | Writes `.ssk` skeleton from `def`/`class` hints |
| Rust migration | `migrate-rust` | functional | Writes `.ssk` skeleton from `fn`/`struct` hints |

## Reproducible commands

From repo root:

```powershell
$env:PYTHONPATH = "src"
python -m sanskript.cli format examples/phase6-functions.ssk
python -m sanskript.cli test examples/phase24-tooling.ssk
python -m sanskript.cli bench --iterations 5
python -m sanskript.cli build .
python -m sanskript.cli coverage examples/phase6-functions.ssk
python -m sanskript.cli debug examples/phase24-tooling.ssk --breakpoints 0
python -m sanskript.cli lsp --stdio
python -m sanskript.cli installer linux -o artifacts/phase24/installer-linux.zip
python -m sanskript.cli phase24-check --out-dir artifacts/phase24
python -m pytest tests/test_phase24_tooling.py -q
```

## Evidence matrix

`phase24-check` writes `artifacts/phase24/phase24-evidence.json` with per-tool
`implementation_state`, in-process smoke metrics, and `anti_fake_violations`.
Exits non-zero when any smoke fails or anti-fake checks fail.

## Adversarial policy

`tests/test_phase24_tooling.py` includes `Phase24CliAdversarialTests` that reject
exit-0 no-ops: empty test roots, empty build trees, invalid format input, polluted
bench stdout, and breakpoint-less debugger claims.
