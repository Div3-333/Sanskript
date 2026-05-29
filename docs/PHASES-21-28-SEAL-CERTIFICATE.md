# Phases 21-28 Seal Certificate

**Repository:** `sanskript`
**Seal date:** 2026-05-29
**Auditor:** automated integration gate (host Python bootstrap)

## Global Proof

```powershell
$env:PYTHONPATH = "src"
python -m pytest -q
python tools/adversarial_audit_phases_1_28.py
```

## Phase Status

- Phase 21: SEALED for current cross-platform support evidence.
- Phase 22: SEALED at hosted/scaffold product tier; browser/desktop/native surfaces remain tier-labelled.
- Phase 23: SEALED at host tier; VM `OP_AWAIT` / in-language event loop remain open.
- Phase 24: SEALED for current CLI/tooling catalog smoke plus anti-fake gates.
- Phase 25: SEALED for current testing/verification harness and exhaustive suites.
- Phase 26: SEALED for documentation and learning-path coverage.
- Phase 27: SEALED for migration honesty; port rows remain open until native replacements exist.
- Phase 28: HONEST PARTIAL. Evidence is recorded, but full independence is not sealed.

## Phase 28 Rule

`python -m sanskript.cli milestone-check --artifact-dir artifacts/phase28` must exit non-zero until all bootstrap/scaffold rows become full independence claims.

Use this command only to record evidence without claiming closure:

```powershell
python -m sanskript.cli milestone-check --artifact-dir artifacts/phase28 --allow-partial
```

Current evidence:

- `artifacts/phase28/phase28-milestone-evidence.json`
- `passed_count: 21` means 21 evidence rows exist, not 21 full independence claims.
- `honesty_gates.allow_full_independence_claim: false`
- M9-M17 and M19-M20 are `[~]` bootstrap/scaffold evidence, not `[x]` independence closure.

## Claim Boundary

Hosted and bootstrap surfaces are useful progress, but they do not mean the repo is independent of Python/Rust yet. Full independence still requires retiring the host compiler/VM/tooling path for normal development.
