# Functional Programming Guide

Sanskript supports map/filter/fold pipelines, immutable lists, comprehensions, lazy iterators, generators, and algebraic types — all expressed as Sanskrit directives. The directive tables and semantics are specified in [functional-declarative.md](functional-declarative.md); the large integration example is [phase8-functional.ssk](../examples/phase8-functional.ssk).

## Start small: procedures before combinators

Before `māpanam` / `saṅkocanam`, use `vidhānam` + `āhvānam` so types and control flow stay obvious:

```text
vidhānam yogaḥ a b .
pratyāvartanam a yoga b .
samāpanam .
āhvānam yogaḥ 10 5 darśayati .
```

Runnable cookbook: [functional-call.ssk](../examples/cookbook/functional-call.ssk) → output `15`.

```powershell
$env:PYTHONPATH='src'
python -m sanskript run examples/cookbook/functional-call.ssk
```

## Collection combinators (when lists are typed)

| Directive | Role |
| --- | --- |
| `māpanam` | map |
| `śodhanam` | filter |
| `saṅkocanam` | fold |
| `sarvam` / `kācit` | all / any |
| `samīkaraṇam` | filter + map comprehension |

Phase 8 wires these end-to-end with static checks: pipeline steps must reference declared unary/binary functions. Run the full showcase:

```powershell
python -m sanskript run examples/phase8-functional.ssk
```

First lines include `20`, `1`, and `[2, 4, 6, 8]` for map/filter/reduce over `saṅkhyāḥ`.

## Purity annotations

- `śuddhaḥ` on `vidhānam` marks a pure function (no I/O side effects).
- `sādhanaṃ` marks effectful procedures.

The type checker tracks effect at call sites; see [type-system-reference.md](type-system-reference.md).

## Immutable and lazy streams

`nitya-samūhaḥ` / `nitye yojanam` build persistent lists; `alasaḥ` / `alasāt` introduce lazy iteration; generators use `utpādaka` / `pradānam`. These appear in the tail of `phase8-functional.ssk`.

## Related

- [functions-procedures.md](functions-procedures.md) — calling conventions
- [cookbook.md](cookbook.md) — all runnable recipes
- [phase26-documentation-learning-path.md](phase26-documentation-learning-path.md)
