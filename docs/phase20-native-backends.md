# Phase 20: Native Backends (Truth-First Evidence)

Phase 20 currently provides an executable backend matrix with explicit truth
markers that distinguish functional paths from scaffold paths.

## Current Depth By Backend

- `portable-bytecode`
  - state: `functional`
  - emits executable VM bytecode artifacts (`.sskbc`)
  - supports host and cross-target planning metadata
- `web-wasm-plan`
  - state: `scaffold`
  - emits a WASM/WAT planning artifact (`program.wat`)
  - does not claim a production linker/object pipeline
- `native-object`
  - state: `scaffold`
  - emits object stubs plus symbol/relocation/linker/debug/stack metadata
  - can optionally invoke host linker tooling, but does **not** claim a fully
    linkable object writer yet

`native-build` / `phase20-evidence` JSON now includes:

- `implementation_state`
- `truth_claims` (including explicit `produces_real_linkable_native_object = false`)
- linker command and linker stdout/stderr artifact paths when linker invocation
  is attempted

## Reproducible Commands

From repo root:

```powershell
$env:PYTHONPATH = "src"
python -m sanskript.cli native-build examples/phase6-functions.ssk --backend portable-bytecode --artifact-kind executable --out-dir artifacts/phase20/portable --plan-json artifacts/phase20/portable/plan.json
python -m sanskript.cli phase20-evidence examples/phase6-functions.ssk --out-dir artifacts/phase20/evidence --plan-json artifacts/phase20/evidence/phase20-evidence.json
python -m pytest tests/test_native_backends.py tests/test_phase20_native_backends.py -q
```

## Non-Overclaim Policy

- Phase 20 evidence must never present stubs as complete native object writers.
- Any successful host linker invocation is treated as integration wiring
  evidence, not proof of complete ABI-correct object emission.
- Portable bytecode remains the canonical executable path.
