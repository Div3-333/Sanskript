# Phase 19: Compiler Self-Hosting (S0 Bootstrap Path)

This phase currently implements **S0 host-replay equivalence**, not full
independent self-hosting.

## What Is Implemented Now

- Differential host-vs-self replay evidence command:
  - `python -m sanskript.cli self-host-check ...`
- Per-source equivalence proof:
  - canonical bytecode SHA-256
  - canonical `.sskyp` SHA-256
- Seed manifest output:
  - `bootstrap/phase19/bootstrap_seed.json`
- Differential tests:
  - `tests/test_phase19_self_hosting.py`

The seed explicitly records:

- `porting_path.current_stage = "S0-host-replay"`
- `porting_path.independent_self_hosting = false`
- `determinism_contract.claim_level = "host-replay-only"`
- `determinism_contract.independence_blockers` to prevent over-claiming closure
- per-source `source_sha256` plus aggregate `equivalence_proof.overall_equivalence_sha256`
- `equivalence_proof.all_match` for the checked source set

## Reproducible Compile + Proof Steps

From repo root:

```powershell
$env:PYTHONPATH = "src"
python -m sanskript.cli self-host-check examples/phase3-data-types.ssk examples/phase6-functions.ssk examples/phase7-oop.ssk --artifact-dir artifacts/phase19 --seed bootstrap/phase19/bootstrap_seed.json
python -m unittest tests/test_phase19_self_hosting.py
```

Expected behavior:

- command exits `0` if all source rows have `bytecode_match=true` and
  `sskyp_match=true`,
- seed is written with evidence rows and stage metadata,
- test suite verifies the equivalence path and seed contents.

## Real Porting Path (No Fake Closure)

- `S0-host-replay` (implemented): host compiler replay + hash equivalence proof.
- `S1-self-parser-lowering` (planned): Sanskript frontend/lowering running on
  host VM, diffed against host compiler output.
- `S2-self-compiler` (planned): compiler compiled by S1 then recompiles compiler
  sources; outputs must match.
- `S3-seed-minimization` (planned): smallest documented seed set to rebuild S2
  from clean checkout.

Until S1/S2 exist, this phase should be treated as bootstrap evidence only.
