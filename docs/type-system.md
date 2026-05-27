# Sanskript Type System

This document is the human-readable view of [`data/types/catalog.json`](../data/types/catalog.json). It registers **every standard scalar, composite, collection, memory, concurrency, and I/O type** that Sanskript is expected to support across the three safety tiers described in [language-design.md](language-design.md).

The catalog is **normative for design** and **descriptive for implementation**: only `text` and a host-backed integer model are executable today; everything else is declared so surakṣita / rakṣita / arakṣita tooling can grow without ad hoc naming.

## Safety tiers

| Tier key | IAST | Role | C / Python analogy |
| --- | --- | --- | --- |
| `surakshita` | surakṣita | Fully checked ownership, lifetimes, effects, regions | Python-level safety with Sanskrit grammar |
| `rakshita` | rakṣita | Explicit transfer, borrow, mutation, release | Rust / modern C with checked declarations |
| `arakshita` | arakṣita | Raw pointers, layout, unchecked calls | Machine-facing unsafe surface |

### Tier availability per type

| Level | Meaning |
| --- | --- |
| `full` | First-class in that tier with appropriate checking |
| `restricted` | Allowed only with explicit annotation or unsafe boundary |
| `forbidden` | Rejected unless the compilation unit changes tier |

## Implementation status (runtime today)

| Status | Types (examples) |
| --- | --- |
| **implemented** | `text` (`vākyam … iti`, `push_text`) |
| **partial** | `i32` / `u32` (tagged widths + checked/wrapping/saturating add), `bigint` (`push_bigint`), `bool`, `text` (`text_*`, `text_grapheme_len` stub), `optional` / `result`, `tuple`, `hash_set`, `deque`, `bytes` / `bytearray`, `array` / `slice` substrates, `list`, `hash_map`, `object`, IEEE `float_is_nan` / `float_is_inf`, `decimal` / `complex128` catalog stubs |
| **planned** | Remaining catalog entries (see JSON) |

Collection opcodes (bytecode v2, surakṣita tier):

| Opcode | Effect |
| --- | --- |
| `list_new` | Push `[]` |
| `list_append` | Pop value, pop list; append; push list |
| `list_len` | Pop list; push length |
| `list_get` | Pop index, pop list; push element |
| `map_new` | Push `{}` |
| `map_set` | Pop value, key, map; store; push map |
| `map_get` | Pop key, map; push value |
| `map_contains` | Pop key, map; push `1` or `0` |
| `push_bool` | Push `true` / `false` (operand `0` or `1`) |
| `push_bigint` / `push_i32` / `push_u32` | Tagged numeric widths |
| `i32_add_checked` / `u32_add_checked` | Checked add with overflow error |
| `option_*` / `result_*` | Option and Result VM values |
| `tuple_new` / `tuple_get` | Fixed-arity tuples |
| `set_*` / `deque_*` | Set and deque collections |
| `push_bytes` / `byte_*` / `bytearray_*` | Immutable and mutable bytes |
| `text_grapheme_len` | Scalar-length stub (grapheme clusters planned) |
| `float_is_nan` / `float_is_inf` | IEEE float classification |
| `opaque_new` | Native interop handle substrate |
| `array_new` / `slice_view` | Fixed array and slice substrates |

## Category inventory

### Scalars (C + Python numeric / text core)

`void`, `bool`, `char`, `byte`, `i8`–`i64`, `isize`, `u8`–`u64`, `usize`, `f32`, `f64`, `text`, `complex64`, `complex128`, `decimal`, `bigint`

### Composites

`optional`, `result`, `tuple`, `struct`, `union`, `enum`, `tagged_enum`

### Collections (Python + C ADTs)

`array` (fixed), `slice`, `list`, `vector`, `linked_list`, `stack`, `queue`, `deque`, `hash_map`, `ordered_map`, `hash_set`, `ordered_set`, `frozen_set`, `bitset`, `bytes`, `bytearray`, `string_builder`, `ring_buffer`

### Functional

`iterator`, `generator`, `callable`, `closure`, `range`

### Memory / ownership (tier-split)

| Type | surakṣita | rakṣita | arakṣita |
| --- | --- | --- | --- |
| `owned` | full | full | restricted |
| `borrow` / `borrow_mut` | full / restricted | full | forbidden |
| `raw_ptr` / `raw_ptr_mut` | forbidden | restricted | full |
| `addr`, `mem_region`, `ffi_c_string` | varies | varies | full where needed |

Kāraka mapping (from catalog): **genitive** → ownership / field path; **dative** → transfer; **instrumental** → borrow or pointer tool; **locative** → region or container locus; **ablative** → release.

### Objects and modules

`object`, `class`, `vtable`, `module` — aligned with [language-paradigms.md](language-paradigms.md). The first object substrate is now executable as records: `vastuḥ` creates a managed object, `aṅgasthāpanam` writes a field, `aṅgāharaṇam` reads a field, and `aṅgāsti` checks field presence. Full classes, methods, inheritance/interfaces, and vtables build on that rather than replacing it.

### Concurrency

`atomic`, `mutex`, `rwlock`, `channel`

### I/O handles

`file_handle`, `socket`, `path`

### Meta and special

`type`, `generic`, `null`, `unit`, `never`, `any`

## Grammatical surface (planned)

Types will **not** use C-style `int*` or Python-style `list[int]` in source. Each catalog entry carries a `sanskrit_hint` and will gain:

1. A **register entry** (construction + examples),
2. **Verb frames** for operations (e.g. samūha insertion, kośa lookup),
3. **Bytecode tags** (`bytecode_tag` in JSON) when lowered.

Parameterized forms use a stable internal spelling, e.g. `list(T)`, `hash_map(K, V)`, `owned(T)`.

## API

```python
from sanskript.type_catalog import SafetyTier, get_type_catalog

catalog = get_type_catalog()
text = catalog.by_name("text")
lists = catalog.types_for_tier(SafetyTier.SURAKSHITA, availability=TierAvailability.FULL)
```

## Related artifacts

| File | Purpose |
| --- | --- |
| `data/types/catalog.json` | Machine-readable registry |
| `src/sanskript/type_catalog.py` | Loader and queries |
| `tests/test_type_catalog.py` | Integrity tests |
| `docs/feature-lattice.md` | Morphology → semantics for cases and number |
| `docs/bytecode-v2.md` | Current executable value model (`int` \| `str` on stack) |

## Next implementation order (recommended)

1. `bool`, fixed-width integers, `f64` — extend VM + `compare_*` / arithmetic opcodes  
2. `list`, `hash_map` — samūha / kośa frames + heap model in **surakṣita** tier  
3. `struct` / `enum` — genitive field paths, no brace literals  
4. `owned` / `borrow` — **rakṣita** checker on top of existing procedures  
5. `raw_ptr` / `addr` — **arakṣita** blocks with `mā` prohibitions at boundaries  
