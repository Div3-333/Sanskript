# Migrating from Rust

Rust programmers often reach for ownership, traits, and explicit types first.
Sanskript currently emphasizes **prose frames**, gradual typing directives, and a
bytecode VM boundary. This guide highlights honest overlaps and gaps.

## Mental model

| Rust habit | Sanskript habit (today) |
| --- | --- |
| `let mut x = 5;` | `gaṇitam x pañca` or verb-frame assign |
| `let x = 5;` (immutable) | `acalachihnam x pañca` / `nityam` |
| `x += 2` | `gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.` |
| `println!("{x}")` | `gaṇakaḥ phalaṃ darśayati.` |
| `if x == 3 { … } else { … }` | `yadi` … `anyathā` … `antam` |
| `fn f(a: i32, b: i32) -> i32` | `vidhānam f a b .` + `pratyāvartanam` |
| `mod` / `pub` | `kṣetram` + `niḥsāram` exports |
| `Result<T,E>` | `phala` / `doṣa` types (Phase 3); `vikṣepaḥ` / `vipattim` sentences |
| `unsafe { … }` | `surakṣitam` / `arakṣitaḥ` tiers (Phase 14–16) — mostly scaffold |

## Example: checked arithmetic flow

**Rust (conceptual)**

```rust
let mut x = 5;
x += 2;
println!("{x}");
```

**Sanskript** ([hello-counter](../examples/cookbook/hello-counter.ssk))

```text
gaṇakaḥ pañca phale nidadhāti.
gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
gaṇakaḥ phalaṃ darśayati.
```

Run: `python -m sanskript run examples/cookbook/hello-counter.ssk` → `7`.

## Example: enum-style branching

Rust `match` on integers maps to `yadi` chains today; full pattern matching on algebraic
types is still growing. See [conditional-branch](../examples/cookbook/conditional-branch.ssk)
and [control-flow.md](control-flow.md).

## Memory and machine tiers

| Rust layer | Sanskript doc |
| --- | --- |
| Stack locals | [phase13-memory-model-by-tier.md](phase13-memory-model-by-tier.md) |
| `unsafe` / FFI | [phase14-surakshita-capability.md](phase14-surakshita-capability.md), [phase16-arakshita-machine-level.md](phase16-arakshita-machine-level.md) |
| Native codegen | [phase20-native-backends.md](phase20-native-backends.md) (scaffold evidence) |

The `ssk-vm` Rust crate is a **host scaffold**, not the primary execution path; day-to-day
runs use `python -m sanskript` against the Python-hosted VM.

## Types and traits

- Type aliases and records: [type-system-reference.md](type-system-reference.md)
- Traits / impl blocks → `vargaḥ` classes: [object-oriented.md](object-oriented.md)
- No `Send`/`Sync` surface yet; concurrency story is Phase 15+

## Tooling parity

| Rust tool | Sanskript today |
| --- | --- |
| `cargo build` | `sanskript compile` → `.sskbc` |
| `cargo run` | `sanskript run` |
| `cargo doc` | `sanskript docs` (module/function list) — see [api-from-source.md](api-from-source.md) |
| `rustfmt` | [style-guide.md](style-guide.md) (prose conventions) |

## What is not ported yet

- Borrow checker semantics (ownership is tier- and capability-scaffolded, not borrow-checked)
- Crate ecosystem / crates.io analogue (local packages only)
- `no_std` / embedded profiles (native backends are evidence scaffolds)

## Further reading

- [tutorial-beginner.md](tutorial-beginner.md)
- [bytecode-v2.md](bytecode-v2.md)
- [phase26-documentation-learning-path.md](phase26-documentation-learning-path.md)
