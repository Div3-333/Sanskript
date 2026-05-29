# Phase 18: VM/Runtime Self-Hosting Bootstrap

Phase 18 now provides executable, reproducible bootstrap evidence for VM/runtime
self-hosting stages S1 and S2.

Current scope is intentionally honest:

- S1 and S2 prove output parity against the current host VM path.
- Evidence artifacts are generated deterministically with hashes.
- The VM path is still host-backed (`independent_vm_runtime = false`), so host
  dispatch retirement is not yet claimed.

## What Is Implemented

- Language-neutral VM/runtime specification writer (`VmSpec`).
- Ported VM execution facade (`SanskriptPortedVM`) with:
  - trace output,
  - debug state dump,
  - instruction profile,
  - execution snapshot.
- S1 bootstrap check: host runtime runs the ported VM facade.
- S2 bootstrap check: `.sskyp` round-trip rebuild then ported VM execution.
- Reproducible evidence bundle with SHA-256 fingerprints for program payloads,
  `.sskyp`, and outputs.
- Retirement gate that requires independent differential proof before declaring
  host dispatch retirement.

## CLI Evidence Command

Run (strict honesty gate mode):

`sanskript phase18-vm-check examples/phase18-vm-bootstrap.sskbc`

Optional output directory:

`sanskript phase18-vm-check examples/phase18-vm-bootstrap.sskbc --artifact-dir artifacts/phase18`

Parity-only mode (explicitly allows host-backed bootstrap to exit success):

`sanskript phase18-vm-check examples/phase18-vm-bootstrap.sskbc --artifact-dir artifacts/phase18 --allow-host-fallback`

This writes:

- `artifacts/phase18/phase18-bootstrap-evidence.json`
- per-program artifacts:
  - `trace.json`
  - `debug.json`
  - `profile.json`
  - `snapshot.json`
- report-level metadata:
  - `reproducible_steps`
  - `honesty_gates`

## Reading Results

- `output_match = true` confirms parity for that stage.
- `independent_vm = false` means execution still uses host VM dispatch.
- `differential_proof = false` means retirement criteria are intentionally not
  met yet.
- `retirement_report.retirement_ready = false` is expected until independent VM
  runtime execution is available.
- `honesty_gates.allow_independence_claim = false` is the required value while
  host fallback paths are present.

## Reproducible Local Evidence (without installing entrypoints)

From repo root:

```powershell
$env:PYTHONPATH = "src"
python -c "from sanskript.cli import main; raise SystemExit(main(['phase18-vm-check','examples/phase18-vm-bootstrap.sskbc','--artifact-dir','artifacts/phase18']))"
python -m unittest tests/test_phase18_vm_runtime.py
```

Expected behavior:

- strict mode exits `2` while independence gates are unresolved,
- `artifacts/phase18/phase18-bootstrap-evidence.json` is regenerated with
  deterministic hashes and honesty gate details,
- tests validate that parity evidence exists but independence is not overclaimed.
