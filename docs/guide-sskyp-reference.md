# `.sskyp` Machine Prose Reference

`.sskyp` files are **Sanskrit machine-prose assembly** paired 1:1 with bytecode v2 opcodes for auditing, teaching, and conformance. The frozen contract is Phase 17 (`src/sanskript/phase17_toolchain.py`).

## File header vocabulary

| Token | Meaning |
| --- | --- |
| `saṃskaraṇam` | format/version declaration |
| `mukhyaḥ pāṭhaḥ` | main entry path |
| `ārabhyate` / `samāpyate` | path begin/end |
| `pūrṇāṅkaḥ nikṣipyate` | push integer constant |
| `nāma sthāpyate` / `āhriyate` | store/load local |
| `vidhānam āhūyate` | call function |
| `darśanam kriyate` | display |
| `virāmaḥ kriyate` | halt |

## High-level source (compiles today)

Machine prose documents bytecode produced from `.ssk`. Runnable high-level proof:

```ssk
gaṇakaḥ pañca phale nidadhāti.
gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
gaṇakaḥ phalaṃ darśayati.
```

[hello-counter.ssk](../examples/cookbook/hello-counter.ssk) prints `7` under the host VM.

## Example program

See [phase17-bytecode-toolchain.sskyp](../examples/phase17-bytecode-toolchain.sskyp):

```text
saṃskaraṇam dvitīyam.
mukhyaḥ pāṭhaḥ ārabhyate.
tri iti pūrṇāṅkaḥ nikṣipyate.
n iti nāma sthāpyate.
n iti nāma āhriyate.
inc iti vidhānam āhūyate.
darśanam kriyate.
virāmaḥ kriyate.
pāṭhaḥ samāpyate.
```

## Toolchain commands

| Task | Entry |
| --- | --- |
| Spec dump | `python -m sanskript phase17-spec` |
| Assemble | APIs in `phase17_toolchain.assemble` |
| Disassemble | `disassemble` from bytecode objects |
| Verify | `verify_program_phase17` (opcode ↔ prose parity) |

Binary container `.sskypb` uses prefix `SSKYP17\0` + length + sha256 + JSON payload (documented in [phase17-bytecode-machine-prose.md](phase17-bytecode-machine-prose.md)).

## Relationship to `.ssk`

High-level `.ssk` compiles to `.sskbc`; machine prose is an alternate **view** of the same program facts, not a second language with different semantics. Round-trip gates ensure mapped opcodes bijectively match sentences.

## Related

- [guide-machine-programming.md](guide-machine-programming.md)
- [bytecode-v2.md](bytecode-v2.md)
- [tooling.md](tooling.md)
