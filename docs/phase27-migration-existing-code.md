# Phase 27: Migration Of Existing Project Code

Phase 27 tracks **honest** porting of the current Python (and partial Rust) host
implementation to native Sanskript. It does **not** claim closure while the
compiler, parser, and VM still execute on the host.

## Truth Baseline (2026-05-29)

| Claim | Status |
| --- | --- |
| Compiler/parser/VM run on Python host | **true** |
| Rust `ssk-vm` crate is conformance reference only | **true** |
| Phase 27 checklist items ported to native | **false** (all unchecked except report) |
| Independent native toolchain | **false** |

Average native replacement across tracked components is **~5.8%** with three
**in_progress** bytecode ports at **27%** each (`grammar_loaders`, `sutra_registry`,
`examples_runner`, plus `test_harness` tied to the runner port). Status remains
`in_progress`, not `ported`, while host Python modules still implement full logic.

## Machine-Readable Report

```powershell
$env:PYTHONPATH = "src"
python -m sanskript.cli migration-report
python -m sanskript.cli migration-seal
python -m pytest tests/test_phase27_migration.py -q
```

`migration-seal` runs the **FULL SEAL gatekeeper**: anti-fake `port_status` audit,
runtime wrapper probes (`SanskriptPortedVM`, self-host S0), Phase 27 checklist
honesty, and host execution of every `// parīkṣā:` manifest row (real regression,
not a native port claim).

Report generator: `src/sanskript/phase27_migration_report.py`

Default outputs:

- `data/meta/migration_report.json`
- `docs/generated/migration-report.md`

The JSON includes:

- `remaining_files` — Python/Rust paths still in the repo
- `components[]` — per-area `port_status`, `percent_complete`, `why_host_remains`
- `known_host_dependencies` — canonical entrypoints that must exist for regression
- `staged_port_plan` — ordered stages with dependency blockers
- `extraction_boundaries` — host-side contracts that are not native ports

## Staged Port Plan (Honest %)

| Stage | Component | % | Status | Blocked by |
| ---: | --- | ---: | --- | --- |
| 1 | Grammar data loaders | 27 | in_progress | — |
| 2 | Sutra registry | 27 | in_progress | grammar_loaders |
| 3 | Sutra predicate engine | 0 | host_only | sutra_registry |
| 4 | Derivational engines | 0 | host_only | sutra_predicate_engine |
| 5 | Morphology helpers | 0 | host_only | derivational_engines |
| 6 | Source tokenizer | 0 | host_only | morphology_helpers |
| 7 | Parser | 0 | host_only | source_tokenizer |
| 8 | AST model | 0 | host_only | parser |
| 9 | Compiler | 0 | host_only | parser, ast, bytecode |
| 10 | Bytecode schema | 0 | host_only | — |
| 11 | VM | 2 | extraction_boundary | bytecode, compiler |
| 12 | `.sskyp` assembler/disassembler | 0 | host_only | bytecode |
| 13 | CLI | 0 | host_only | compiler, vm |
| 14 | Docs generator | 0 | host_only | test_harness |
| 15 | Examples runner | 27 | in_progress | cli, compiler |
| 16 | Test harness | 27 | in_progress | cli, vm |
| 17 | Web playground | 0 | host_only | vm, compiler |
| 18 | Browser runtime | 0 | host_only | vm, bytecode |
| 19 | Build/release scripts | 0 | host_only | cli, test_harness |

Percentages measure **native Sanskript code replacing host implementation**, not
feature completeness of the existing host toolchain.

## Native Bytecode Ports (Canonical Execution)

Three components delegate manifest/registry/loader **counts** to Sanskript-authored
`.sskbc` modules (host VM dispatches; Python must not re-parse JSON for these surfaces):

| Port | `.ssk` | `.sskbc` | Host delegate |
| --- | --- | --- | --- |
| Controlled lexicon loader | `examples/phase27-port-controlled-lexicon.ssk` | `.sskbc` | `morphology_lexicon.lexicon_entry_count_manifest()` |
| Sutra registry JSON consumer | `examples/phase27-port-sutra-registry.ssk` | `.sskbc` | `sutra_logic.sutra_registry_slice_via_port()` |
| Examples runner driver | `examples/phase27-port-examples-runner.ssk` | `.sskbc` | `phase27_migration_report` manifest row count |

Conformance probes: `src/sanskript/phase27_ports.py` (`verify_all_ports`). Report rows
use `port_status=in_progress` at **27%** — never `ported` while host modules remain.

## Extraction Boundaries (Not Native Ports)

1. **Regression manifest** — `examples/phase27-migration-test-manifest.ssk` lists
   golden sources via `// parīkṣā:` lines; `data/migration/phase27-test-manifest.json`
   is the machine-readable twin. pytest still runs tests.
2. **`migration-report` CLI** — emits JSON from the host; documents remaining files.

## Sanskript-Authored Test Manifest

The manifest is the first migration artifact meant to be owned as Sanskript
surface area:

- Prose/header: `examples/phase27-migration-test-manifest.ssk`
- JSON twin: `data/migration/phase27-test-manifest.json`

Future work: parse `// parīkṣā:` lines in the Sanskript frontend and drive a
native test runner (M15) without duplicating paths in Python.

## What Remains On The Host (Summary)

From `data/meta/module_inventory.json` (regenerate with
`python tools/generate_module_inventory.py`):

- **~224** Python modules under `src/sanskript/`, `tools/`, and `tests/`
- **5** Rust modules under `ssk-vm/`

Primary entrypoints (regression guards):

- `src/sanskript/compiler.py`
- `src/sanskript/parser.py`
- `src/sanskript/vm.py`
- `src/sanskript/cli.py`
- `ssk-vm/Cargo.toml`

## Recommended Build Order

1. Keep golden examples/manifest stable; extend only with host-verified paths.
2. Follow Phase 19 porting path (`S0` → `S1` parser/lowering → `S2` compiler).
3. Port VM subset with host/self output conformance (Phase 18 evidence).
4. Replace pytest discovery with Sanskript runner executing manifest rows.
5. Retire Python inventory scripts only after native equivalents emit the same JSON.

## Anti-Regression

- Do not mark checklist items `[x]` until the component runs without Python/Rust
  implementation code for normal use.
- Do not raise `percent_complete` for data-only artifacts (JSON schemas, examples).
- Regenerate `migration-report` after large refactors and commit the JSON diff in CI
  when Phase 27 gates become mandatory.
