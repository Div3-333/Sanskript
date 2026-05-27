# Functions And Procedures (Phase 6)

Phase 6 completes callable behavior: first-class functions, closures, effects,
overloading, partial application, compile-time macros, and tier-specific linkage.

## Function headers (prose)

```text
saṃskāraṃ trace .
vidhānam śuddhaḥ parivartanīya-gṛhī n counter .
pratyāvartanam yoga n 1 .
samāpanam .
```

| Modifier | Meaning |
|----------|---------|
| `śuddhaḥ` | Pure function (`effect=pure`) — no `darśanam` or heap effects |
| `sādhanaṃ` | Effectful procedure |
| `parivartanīya-gṛhī x y` | Mutable shared capture for closure variables |
| `pratyāvartana-nāmāni a b` | Named return slots |
| `antarbhūtam` | Inline body at call sites (`rakṣita` tier) |
| `nagnā` + `abi name` | Naked/ABI export (`arakṣita` tier) |
| `kālavyāpāre` | Compile-time macro (literal arguments only) |
| `saṃskāraṃ name` | Decorator applied before `vidhānam` (`trace` built-in) |

## Keyword arguments (case roles)

Pass arguments with the fourth-case pattern `VALUE iti paramName`:

```text
āhvānam add2 3 iti a 10 iti b .
```

The compiler orders arguments to match the callee signature.

## Named returns

```text
pratyāvartanam phala iti artha 42 .
```

## Tail calls

When a function ends with `pratyāvartanam` of a call to itself, the compiler emits
`tail_call` so the VM reuses the current frame.

## Partial application and currying

```text
gaṇitam plus1 āṃśikam āhvānam add3 1 .
anukrameṇa āṃśikam āhvānam pair 5 .
```

`anukrameṇa` binds one parameter at a time (currying) through partial wrappers.

## Overloading

Multiple `vidhānam` declarations with the same name and different arity resolve
at compile time (`sum` / `sum_2` bytecode names). Method overloading uses the same
arity/suffix rules in `TypeChecker.resolve_overload` for `MethodCall`.

## Mutable capture

Immutable capture snapshots values at closure creation. Variables listed under
`parivartanīya-gṛhī` share `MutableCell` storage so nested functions observe
outer updates.

## Pure and effectful

- Type-checker rejects `darśanam` and heap ops inside `śuddhaḥ` functions.
- VM rejects `emit` when `_current_effect == "pure"`.
- Pure functions cannot use `parivartanīya-gṛhī`.

## Example program

See `examples/phase6-functions.ssk`.

## Migration notes (Python / Rust)

| Concept | Python | Rust | Sanskript prose |
|---------|--------|------|-----------------|
| Def | `def f(x):` | `fn f(x)` | `vidhānam f x .` |
| Pure | typing + linter | `#[pure]` (tooling) | `vidhānam śuddhaḥ f …` |
| Keyword args | `f(b=10, a=3)` | `f(b: 10, a: 3)` (named) | `āhvānam f 3 iti a 10 iti b` |
| Closure mut | `nonlocal` | `RefCell` / `&mut` capture | `parivartanīya-gṛhī` |
| Tail call | CPython: no TCO | `#[tail_recursion]` / loop | `tail_call` opcode |
| Overload | separate names / `@overload` | inherent + trait | same `vidhānam` name, arity |
| Partial | `functools.partial` | closures | `āṃśikam āhvānam …` |
| Decorator | `@decorator` | attributes/proc macros | `saṃskāraṃ` + `vidhānam` |
| Macro | `def macro` / template | `macro_rules!` | `kālavyāpāre vidhānam` |
| Inline | hint | `#[inline]` | `antarbhūtam vidhānam` (`rakṣita`) |
| ABI export | `extern "C"` | `extern "C"` | `nagnā vidhānam … abi sym` (`arakṣita`) |

## Tests

`tests/test_phase6_functions.py` — 28 tests covering runtime, parser tokens,
type-check negatives, bytecode opcodes, and tier metadata.
