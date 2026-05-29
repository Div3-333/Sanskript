# Systems Programming Guide

This is a **reading map**, not a seal claim. Low-level memory, capabilities, and machine-level
features are documented per phase; most enforcement still runs in the Python-hosted compiler and VM.

## Phase documents (read in order)

| Phase | Topic | Document | Example |
| --- | --- | --- | --- |
| 13 | Memory model by tier (`surakṣita` / `rakṣita` / `arakṣita`) | [phase13-memory-model-by-tier.md](phase13-memory-model-by-tier.md) | [phase13-memory-model.ssk](../examples/phase13-memory-model.ssk) |
| 14 | End-user capability bootstrap (`std.file`, `std.web`, …) | [phase14-surakshita-capability.md](phase14-surakshita-capability.md) | [phase14-surakshita.ssk](../examples/phase14-surakshita.ssk) |
| 15 | Rakṣita systems (OS-facing stubs) | [phase15-rakshita-systems.md](phase15-rakshita-systems.md) | [phase15-rakshita-systems.ssk](../examples/phase15-rakshita-systems.ssk) |
| 16 | Arakṣita machine-level (`.sskyp`, unsafe entry) | [phase16-arakshita-machine-level.md](phase16-arakshita-machine-level.md) | [phase16-arakshita-machine-level.sskyp](../examples/phase16-arakshita-machine-level.sskyp) |

Bytecode and VM depth (after tiers):

- [phase17-bytecode-machine-prose.md](phase17-bytecode-machine-prose.md)
- [phase18-vm-runtime-self-hosting.md](phase18-vm-runtime-self-hosting.md)

Opening lines of the tier smoke program ([phase13-memory-model.ssk](../examples/phase13-memory-model.ssk)):

```text
rakṣitam.

āhvānam std.memory.alloc.heap aṣṭa catur vākyam abi iti asatyam vākyam sysv64 iti vākyam global iti block nidadhāti.
āhvānam std.memory.layout.describe block varṇanam nidadhāti.
```

## Host boundaries (honest)

| Layer | What runs today | What is not native yet |
| --- | --- | --- |
| Static checks | `type_checker.py` ownership/borrow/tier rules | Full native-only checker binary |
| Runtime | `vm.py` tier gates + `std.memory.*` in host Python | Bare-metal allocator without host |
| OS / FFI | Phase 15 natives are stubs or host bridges | libc/socket/process product paths |
| Machine | Phase 16 `.sskyp` + arakṣita opcodes in tests | Self-hosted machine codegen shipping |

Do not treat `std.memory.*` or `std.process.*` checklist rows as product features until phase
tests and independence milestones show runnable proof without host disclaimers. See
[native-sanskript-independence-checklist.md](native-sanskript-independence-checklist.md).

## Type and style references

- [type-system-reference.md](type-system-reference.md) — tiers and annotations
- [style-guide.md](style-guide.md) — naming and register conventions

## Runnable tier smoke (cookbook)

```powershell
$env:PYTHONPATH='src'
python -m sanskript run examples/cookbook/systems-tier.ssk
```

Expected stdout: `surakṣita` (declares `surakṣitam` then displays the tier label).

## Related learning path

- [phase26-documentation-learning-path.md](phase26-documentation-learning-path.md)
- [cookbook.md](cookbook.md) — all tested recipes including `systems-tier.ssk`
