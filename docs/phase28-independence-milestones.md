# Phase 28: Independence Milestones (M0–M20)

Phase 28 turns the long-form independence checklist into **automated, falsifiable
milestones**. A milestone is ticked only when `milestone-check` (or the unit
tests) produce passing evidence. Host-replay bootstrap from Phases 18–19 does
**not** close compiler or VM independence milestones.

## Commands

```powershell
$env:PYTHONPATH = "src"
python -m sanskript.cli milestone-check --artifact-dir artifacts/phase28
python -m unittest tests/test_phase28_independence_milestones.py
```

Artifacts:

- `artifacts/phase28/phase28-milestone-evidence.json` — full per-milestone proof rows
- `artifacts/phase28/phase28-checklist-markers.md` — checklist-shaped tick/blocker view

By default the CLI exits **2** while any milestone remains open (honesty gate).
Pass `--allow-partial` to record evidence without implying closure.

## Milestone definitions and proof methods

| ID | Goal | Automated proof method |
| --- | --- | --- |
| M0 | Host runs all examples | Compile + VM-run every `examples/**/*.ssk` |
| M1 | Bytecode examples have source prose | Canonical SHA-256 match: `.ssk` vs sibling `.sskbc` |
| M2 | `.sskyp` examples round-trip | `yantra_patha` encode/decode with stable `program_sha256` |
| M3 | Stdlib covers core domains | Registry + smoke for text, collections, files, JSON, CLI, HTTP, tests |
| M4 | Useful CLI app in Sanskript | `examples/phase10-stdlib-cli-io.ssk` runs with `std.cli.*` + `std.file.*` |
| M5 | Useful web app in Sanskript | `write_web_app` emits HTML for `examples/prathama.ssk` |
| M6 | Desktop/productivity app | Example using `std.gui.*` end-to-end |
| M7 | Game loop + assets | Example using `std.game.*` end-to-end |
| M8 | Research/data scripts | `examples/phase11-algorithms-data-structures.ssk` runs with `std.alg.*` |
| M9 | VM core in `rakṣita` | Phase 18 independent VM + rakṣita VM sources (not host Python) |
| M10 | Bytecode verify in Sanskript | Sanskript-authored verifier (not `phase17_toolchain` host) |
| M11 | Compiler frontend in Sanskript | Beyond `S0-host-replay` self-host stage |
| M12 | Compiler backend in Sanskript | Sanskript-authored lowering (not `compiler.py` host) |
| M13 | Self-compile compiler | Phase 19 `independent_self_compile=true` |
| M14 | Self-run VM | Phase 18 `independent_vm_runtime` + retirement readiness |
| M15 | Self build + test | Fresh-checkout build/test without Python host |
| M16 | Native binary (one platform) | Phase 20 functional linked executable |
| M17 | Native binaries (Win/macOS/Linux) | Linked binaries for all three families |
| M18 | Web without handwritten JS app code | Functional WASM/JS bridge without host shell JS |
| M19 | No required Python/Rust for dev | `module_inventory.json` reports zero required host modules |
| M20 | Host languages optional only | M19 plus bootstrap-only host policy |

Implementation: `src/sanskript/phase28_milestones.py`.

## Honesty gates

The evidence JSON includes `honesty_gates`:

- `allow_full_independence_claim` is **false** until every M0-M20 row passes
  with `claim_allowed: true`.
- `host_bootstrap_only` lists rows that have executable evidence but cannot yet
  be cited as full independence (currently M9-M17 and M19-M20).
- `unresolved_reasons` names rows that are either unproven or only
  bootstrap/scaffold evidence.

## Current baseline (automated audit)

Run `milestone-check` for the live evidence set. Current results distinguish
evidence from claim rights:

- **Full `[x]` evidence claims:** M0-M8 and M18.
- **Partial `[~]` bootstrap/scaffold evidence:** M9-M17 and M19-M20.
- **Full independence:** still blocked; the command without `--allow-partial`
  must fail until the host compiler/VM/tooling path is retired.

Do not manually tick checklist items without matching JSON evidence.

## Related phases

- Phase 18 — VM bootstrap parity (`phase18-vm-check`)
- Phase 19 — compiler host-replay (`self-host-check`)
- Phase 20 — native backend evidence (`phase20-evidence`)
- Phase 27 — migration port tracking (`migration-report`)
