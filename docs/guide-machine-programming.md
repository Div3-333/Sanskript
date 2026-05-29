# Machine Programming Guide

Machine-level work in Sanskript spans **bytecode v2**, **Sanskrit machine prose** (`.sskyp`), and **arakṣita** unsafe entry points. This guide orders the reading path; deep specs remain in phase documents.

## Reading order

| Step | Topic | Document | Runnable artifact |
| --- | --- | --- | --- |
| 1 | Portable bytecode layout | [bytecode-v2.md](bytecode-v2.md) | `.sskbc` from `sanskript compile` |
| 2 | Machine prose toolchain | [phase17-bytecode-machine-prose.md](phase17-bytecode-machine-prose.md) | [phase17-bytecode-toolchain.sskyp](../examples/phase17-bytecode-toolchain.sskyp) |
| 3 | Yantra reference (standalone) | [guide-sskyp-reference.md](guide-sskyp-reference.md) | same `.sskyp` example |
| 4 | Arakṣita tier | [phase16-arakshita-machine-level.md](phase16-arakshita-machine-level.md) | [phase16-arakshita-machine-level.sskyp](../examples/phase16-arakshita-machine-level.sskyp) |
| 5 | VM execution | [guide-vm-architecture.md](guide-vm-architecture.md) | [phase18-vm-bootstrap.sskbc](../examples/phase18-vm-bootstrap.sskbc) |

## What “machine programming” means here

- **Bytecode** is the portable contract between compiler and VM. You can inspect it as JSON (`.sskbc`) without running Python source again.
- **Machine prose** is a human-auditable Sanskrit sentence per opcode for conformance and teaching.
- **Arakṣita** unlocks unsafe memory and foreign calls under explicit tier markers — not the default teaching path.

## High-level `.ssk` before machine prose

Compile and run a single-file program first (same pipeline as production `.ssk`):

```ssk
gaṇakaḥ pañca phale nidadhāti.
gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
gaṇakaḥ phalaṃ darśayati.
```

Source: [hello-counter.ssk](../examples/cookbook/hello-counter.ssk) → stdout `7`. Then inspect bytecode:

```powershell
$env:PYTHONPATH='src'
python -m sanskript compile examples/cookbook/hello-counter.ssk
```

## Minimal `.sskyp` excerpt

From the phase 17 example (increment and return):

```text
saṃskaraṇam dvitīyam.
mukhyaḥ pāṭhaḥ ārabhyate.
tri iti pūrṇāṅkaḥ nikṣipyate.
n iti nāma sthāpyate.
n iti nāma āhriyate.
inc iti vidhānam āhūyate.
darśanam kriyate.
```

Assemble/disassemble via CLI flags documented in [tooling.md](tooling.md) (`phase17-spec`, conformance tools).

## Safety reminder

Machine-level features do **not** imply native codegen shipping. Phase 20+ tracks native backends; until then, execution is host-VM replay with honest gates in [native-sanskript-independence-checklist.md](native-sanskript-independence-checklist.md).

## Related

- [guide-systems-programming.md](guide-systems-programming.md) — memory tiers before machine prose
- [guide-compiler-architecture.md](guide-compiler-architecture.md) — how `.ssk` becomes bytecode
