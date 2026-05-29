# Phase 25: Testing and Verification — Brutal Review

**Verdict:** `coverage_proof.passed` is required for `seal_ready` (anti-fake gatekeeper). Exhaustive suites live in `tests/test_phase25_exhaustive_coverage.py` (98 AST + 176 opcode + 90 lowering tests). `seal_ready` may still be false when golden output mismatches or checklist `not_met` rows remain; independence proofs stay warnings only.

## What counts as done (harness green)

| Gate | Evidence | Status |
|------|----------|--------|
| Fuzz parser / bytecode verifier / `.sskyp` | Smoke harness (`FUZZ_SMOKE_TRIAL_BUDGET`=48 trials, seed-fixed) — zero crashes; **not** production/continuous fuzz | Pass (smoke only) |
| Property tests (numeric, list, text) | VM-level properties in `phase25_testing_verification.py` | Pass |
| Golden stability (source) | `verify_golden_hashes_stable()` + manifest sha256 for 5 sources (phase10-cli-io output omitted — env-dependent IO) | Pass |
| Golden bytecode / sskyp fixtures | `data/testing/golden/bytecode/`, `sskyp/` + conformance dir (5 fixtures) | Pass |
| Round-trip binary + sskyp | `roundtrip_bytecode_serialization`, `roundtrip_sskyp_assembly` | Pass |
| Differential scaffold determinism | `differential_scaffolds_deterministic()` — fingerprint stable across repeat invocations | Pass |
| Host VM vs conformance | `differential_host_vm_scaffold` — Python VM matches all fixtures (not independent) | Pass (scaffold) |
| Host compiler replay | `differential_host_compiler_scaffold` — S0 host-replay hash match | Pass (not independent) |
| Coverage map | `data/verification/coverage_map.json` via `tools/phase25_coverage_map.py` | Generated |

## What does NOT count (reject “lots of tests”)

- **~1150 `def test_` functions** — volume without per-rule / per-opcode / per-lowering proof.
- **176 opcodes** — only ~133 have a test-file token reference; no dedicated per-opcode suite.
- **98 AST statement nodes** — 14 lack direct test references; only 17 parser rules documented in `PARSER_RULES`.
- **43 `examples/*.ssk`** — golden registry covers **5** sources (~12%); phase10-cli-io is sha256-only (no output golden).
- **Independent VM proof** — Phase 18/19 explicitly set `differential_proof = false` and `independent_self_compile = false`.
- **Rust ssk-vm** — second **host** implementation; useful parity, not Sanskript-native retirement proof.

## Seal blockers (must clear before seal-ready)

1. Per-parser-rule unit tests for every directive surface.
2. Per-compiler-lowering unit tests for every emission path.
3. Per-VM-opcode unit tests (or traced IP coverage proving each opcode on real programs).
4. Golden registry for all phase examples + negative corpora (parser, type-checker, borrow, unsafe).
5. Independent Sanskript VM differential proof (zero host fallback).
6. Independent self-hosted compiler differential proof (beyond S0 host-replay).
7. Continuous fuzz CI (parser, verifier, sskyp) with corpus minimization — harness exists, pipeline does not.
8. Cross-platform CI matrix; concurrency stress suite beyond phase23 scaffold.
9. Source formatter round-trip tests (formatter exists; Phase 25 item not met).

## Repro commands

```bash
PYTHONPATH=src python -m unittest tests.test_phase25_testing_verification -v
PYTHONPATH=src python -m sanskript.cli phase25-evidence
PYTHONPATH=src python tools/phase25_coverage_map.py
PYTHONPATH=src python tools/phase25_test_matrix.py
```

Optional Rust differential (requires `cargo`):

```bash
PYTHONPATH=src python -m unittest tests.test_rust_vm -v
```

## Artifacts

| Path | Role |
|------|------|
| `artifacts/phase25/evidence/phase25-evidence.json` | Full matrix + `seal_verdict` |
| `data/verification/coverage_map.json` | Parser/opcode/lowering inventory |
| `data/testing/golden/manifest.json` | Golden sha256 registry |

## Checklist honesty

`phase25_checklist_truth()` in `src/sanskript/phase25_testing_verification.py` marks items `partial`, `scaffold`, or `not_met` only when harnesses support the claim. Phase 25 completion in `docs/native-sanskript-independence-checklist.md` must not be ticked from test count alone.
