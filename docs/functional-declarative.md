# Phase 8: Functional And Declarative Programming

Phase 8 adds higher-order collection operations, immutable data, lazy iterators, generators, pipelines, pattern matching expressions, algebraic types, result helpers, declarative queries, grammar rules, memoization, and pure/effect separation — all in grammatical Sanskrit prose.

Validation is now strict end-to-end:
- pipeline/list/query steps must reference declared functions with correct unary/binary arity.
- rule ids must be unique and invocations must target declared rules.
- `gaṇavikalpaḥ` construction must reference a declared `prakāra-vikalpaḥ` type and a declared variant.

## Collection operations

| Directive | Meaning |
|-----------|---------|
| `māpanam target source function` | Map `function(item)` over list |
| `śodhanam target source function` | Filter by truthy `function(item)` |
| `saṅkocanam target source function initial` | Left fold |
| `sarvam target source function` | All elements satisfy predicate |
| `kācit target source function` | Any element satisfies predicate |
| `avalokanam target source function initial` | Scan (prefix fold list) |
| `yuktam target left right` | Zip two lists into pair list |
| `aṅkayuktam target source` | Enumerate with index pairs |

Inputs are never mutated; results are new lists.

## Immutable collections

| Directive | Meaning |
|-----------|---------|
| `nitya-samūhaḥ name` | Empty persistent list |
| `nitye yojanam target source value` | Append immutably into `target` |

## Comprehension and pipeline

| Directive | Meaning |
|-----------|---------|
| `samīkaraṇam target source where_fn yathā with_fn` | Filter then map |
| `pravāhaḥ target source step1 step2 …` | Pipeline of unary transforms |

## Lazy iterators and generators

| Directive | Meaning |
|-----------|---------|
| `alasaḥ target source` | Lazy view over list |
| `alasāt has_more value iterator` | Advance lazy iterator |
| `utpādakaḥ target function` | Create generator handle |
| `utpādakāt has_more value generator` | Resume generator |
| `pradānam value` | Yield inside `saṃskāraṃ utpādaka` function |

Mark generator functions with `saṃskāraṃ utpādaka` before `vidhānam`.

## Pattern matching

| Directive | Meaning |
|-----------|---------|
| `yathā subject` … arms … | Statement match |
| `yathā-artham target subject` … arms … | Expression match (arms assign `target`) |

`yathā-artham` initializes `target` with `subject` before arm execution, so
unmatched or pass-through arms preserve the original value.

## Algebraic types and results

| Directive | Meaning |
|-----------|---------|
| `prakāra-vikalpaḥ Name v1 v2 …` | Declare variant type |
| `bandhanam target result function` | Monadic bind on `result` |
| `prasāraḥ value` | Propagate `result` error (Phase 5) |

## Declarative query and rules

| Directive | Meaning |
|-----------|---------|
| `anveṣaṇam target source field predicate` | Query rows matching field predicate |
| `niyamaḥ id when_fn then_fn` | Register grammar rule |
| `niyama-āhvānam target id context` | Invoke rule |

## Memoization and effects

| Directive | Meaning |
|-----------|---------|
| `saṃskāraṃ smaraṇa` + `vidhānam` | Memoized function |
| `śuddhaḥ vidhānam` | Pure function (no `darśanam`) |
| `sādhanaṃ vidhānam` | Effectful function |

Memoization is call-site transparent: normal `āhvānam` uses memo caches when
the callee is marked with `saṃskāraṃ smaraṇa`. Memoized functions must not be
declared `sādhanaṃ` and must not capture mutable state.

## Example

Map, filter, and fold over a list (from [`examples/phase8-functional.ssk`](../examples/phase8-functional.ssk)):

```text
samūhaḥ saṅkhyāḥ.
yojanam saṅkhyāḥ eka.
yojanam saṅkhyāḥ dvi.

vidhānam dviguṇa mūlya.
pratyāvartanam mūlya guṇanam dvi.
samāpanam.

vidhānam catvārāt-adhikaḥ mūlya.
pratyāvartanam mūlya.
samāpanam.

vidhānam saṅkalanam prathama dvitīya.
pratyāvartanam prathama yoga dvitīya.
samāpanam.

māpanam dviguṇitaṃ saṅkhyāḥ dviguṇa.
śodhanam cayanam dviguṇitaṃ catvārāt-adhikaḥ.
saṅkocanam yogaḥ cayanam saṅkalanam śūnya.
```

Run: `python -m sanskript run examples/phase8-functional.ssk` (host VM).

## Migration from Python

| Python | Sanskript |
|--------|-----------|
| `map(f, xs)` | `māpanam` |
| `filter(f, xs)` | `śodhanam` |
| `functools.reduce` | `saṅkocanam` |
| `all` / `any` | `sarvam` / `kācit` |
| `itertools.accumulate` | `avalokanam` |
| `zip` | `yuktam` |
| `enumerate` | `aṅkayuktam` |
| `[f(x) for x in xs if p(x)]` | `samīkaraṇam` |
| `yield` | `pradānam` |
| `match` / `case` | `yathā` / `yathā-artham` |
| `@dataclass` variants | `prakāra-vikalpaḥ` |
| `Result` bind | `bandhanam` |
| `@lru_cache` | `saṃskāraṃ smaraṇa` |

### Migration notes (hardening)

- Replace ad-hoc pipeline helper names with explicit unary helpers; multi-argument reducers remain `saṅkocanam`/`avalokanam` only.
- Declare rules before `niyama-āhvānam`, and keep ids unique in each compilation unit.
- Add `prakāra-vikalpaḥ` before any `gaṇavikalpaḥ` construction, and use only declared variant names.

Bytecode and `.sskyp` machine prose: see `yantra_patha.py` renderers for `list_*`, `immutable_list_*`, `lazy_iter_*`, `generator_*`, `pipeline_chain`, `result_bind`, `data_query`, `rule_*`, `memo_call`.
