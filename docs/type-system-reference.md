# Sanskript Type System Reference (Phase 4)

Static checking runs in `src/sanskript/type_checker.py` before bytecode emission.
The compiler calls `check_program()` from `compile_program()`.

---

## Safety tiers

Programs declare a tier with `surakṣitam`, `rakṣitaḥ`, or `arakṣitaḥ`.
The checker loads `data/types/catalog.json` and rejects types marked **forbidden** for the active tier.

| Tier | IAST | Analogy |
|---|---|---|
| `surakshita` | surakṣita | managed high-level (Python-like) |
| `rakshita` | rakṣita | explicit ownership/borrowing (Rust-like) |
| `arakshita` | arakṣita | raw machine-facing (C/assembly) |

### Tier matrix for key types

| Type | surakṣita | rakṣita | arakṣita |
|---|---|---|---|
| `i32`, `f64`, `bool`, `text`, `list`, `hash_map` | full | full | full/restricted |
| `raw_ptr`, `raw_ptr_mut`, `addr` | **forbidden** | restricted | full |
| `safe_ref` (sāmānyaḥ sandarbhaḥ) | **forbidden** | full | full |
| `borrow`, `borrow_mut` | full/restricted | full | forbidden |
| `async_future`, `coroutine` | full | restricted | restricted/forbidden |
| `any` | restricted | **forbidden** | full |
| `union` | **forbidden** | restricted | full |

---

## Declarations in source

| Prose directive | AST node | Meaning |
|---|---|---|
| `prakāraḥ alias iti target` | `TypeAliasDecl` | Type alias |
| `navaprakāraḥ name iti base` | `NewtypeDecl` | Newtype wrapper |
| `parivartana target type value` | `TypeConvert` | Explicit conversion |
| `nityam name value` | `ConstDecl` | Compile-time constant (immutable) |
| `vastuḥ Name { fields }` | `RecordTypeDecl` | Nominal record type |
| `vastuḥ Name T { fields }` | `GenericRecordDecl` | Generic record with type param |
| `abhilakṣaṇaṃ Name T { methods }` | `TraitDecl` | Interface/trait declaration |
| `sādhayati RecordName TraitName` | `TraitImpl` | Assert record implements trait |
| `prakāra-āharaṇam target type_name` | `TypeReflect` | Type reflection (produces text) |
| `vastu-prakāraḥ Name { fields }` | `RecordTypeDecl` / `GenericRecordDecl` | Nominal or generic record |
| `vargaḥ Name { fields } metoda m₁ …` | `ClassDecl` | Class (Phase 7 bridge) |
| `āyuḥ name [region]` | `LifetimeDecl` | Lifetime/region (rakṣita+) |
| `vidhānam śuddhaḥ name …` | `FunctionDef` + `effect=pure` | Pure function |
| `gaṇitam svāmitvaṃ x …` | `Bind` + `ownership` | Owned binding |

---

## Generic classes (Phase 7 bridge)

Full OOP (methods, vtables, inheritance) is **Phase 7**. Phase 4 defines a minimal
`ClassDecl` AST: fields plus method **names** only. The checker registers the class as
a `ClassInstanceType` and mirrors fields into `RecordNominalType` for `record_*` opcodes.

```text
vargaḥ Point x i32 y i32 metoda distance magnitude .
```

---

## Overload resolution

Multiple `FunctionDef` nodes may share a logical name. `TypeChecker.resolve_overload`:

1. Filter candidates by **arity** (parameter count).
2. If one match, use it.
3. Else match `name_<arg_types>` suffix (e.g. `add_i32_f64`) or trailing type suffix.

---

## Lifetimes and regions (rakṣita)

`LifetimeDecl` registers region names. `Bind(..., lifetime="a")` requires `rakṣita` or
`arakṣita` tier. Lifetime checking records names; full borrow/lifetime diagnostics are
deferred to rakṣita tooling.

---

## Affine and linear resources

| Type | Rule (vocabulary) | surakṣita |
|---|---|---|
| `linear` | Must be consumed exactly once | forbidden |
| `affine` | May be used at most once | forbidden |

Registered in `catalog.json`; aliases to these types are tier-gated like `raw_ptr`.

---

## Metaclass

`metaclass` is catalog-defined for type-of-types reflection. Class identity today uses
nominal `ClassDecl.name`; full metaclass behaviour is Phase 7.

---

## Nominal types

Records are **nominal**: two records with the same field layout but different names are
distinct types. Nominal identity is enforced by `RecordNominalType.name`.

```text
vastuḥ Puruṣaḥ { nāma : text }
vastuḥ Strī    { nāma : text }
-- Puruṣaḥ ≠ Strī even though fields are identical
```

The type checker stores all record declarations in `TypeChecker.records: dict[str, RecordNominalType]`.

---

## Structural types (duck typing on records)

`TypeChecker._structural_match(record_a, record_b)` returns `True` if `record_a` has
at least all fields declared by `record_b` with compatible types. This enables duck-typing
acceptance at function call sites.

```python
# Full { x, y, z } structurally satisfies Partial { x, y }
checker._structural_match(full, partial)  # True
checker._structural_match(partial, full)  # False (missing z)
```

---

## Generic records

```text
vastuḥ Paṭala T { data : T ; size : i32 }
```

`GenericRecordDecl` stores the type-parameter name. The checker registers it in
`TypeChecker.generic_records`. Instantiation with a concrete type is resolved at
call sites.

---

## Generic interfaces / traits

```text
abhilakṣaṇaṃ Iterable T { next : () → T }
```

`TraitDecl` carries `(name, type_param, methods)`. Methods are tuples of
`(method_name, param_types, return_type)`.

`TraitImpl` asserts that a named record satisfies a trait. The checker verifies every
method name exists as a field on the record (structural duck-type check).

---

## Bounded generics

```text
vidhānam process T : Iterable ...
```

`FunctionDef.type_param_bounds` is a tuple of `(param_name, bound_trait)` pairs.
The checker registers the bound on the `GenericType` node; full bound enforcement
(verifying the concrete argument implements the trait) is a future phase feature.

---

## Return type inference

After checking function body statements, the checker collects the type of every `Return`
node. The unified type is stored and accessible via:

```python
checker.get_inferred_return_type(function_name)  # → TypeExpr
```

Unification rules:
- All `i32` → `i32`
- Mixed `i32`/`f64` → `f64`
- Mixed `i32`/`i64` → `i64`
- No returns → `void`
- Mixed non-numeric → `unknown`

---

## Implicit conversions

The following widening conversions are accepted without an explicit `parivartana`:

| From | To |
|---|---|
| `bool` | `i32`, `i64`, `f64` |
| `i32` | `i64`, `f64` |
| `i64` | `f64` |
| `f32` | `f64` |

These are checked inside `TypeChecker._convertible()`.

---

## Numeric promotion in binary expressions

| Left | Right | Result |
|---|---|---|
| `f64` | any numeric | `f64` |
| `f32` | any numeric (not f64) | `f32` |
| `i64` | any int (not f64/f32) | `i64` |
| `i32` | `i32`, `u32` | `i32` |

---

## text / bytes conversion

```text
parivartana raw bytes msg   -- text → bytes  (encode)
parivartana str text raw    -- bytes → text  (decode)
```

Both directions accepted by `TypeChecker._convertible()` without explicit newtype.

---

## Tier-based pointer types

| Type | Sanskrit | Tier |
|---|---|---|
| `safe_ref` | sāmānyaḥ sandarbhaḥ | rakṣita, arakṣita only |
| `raw_ptr` | kacchāṃśaḥ sūcaka | rakṣita (restricted), arakṣita |
| `raw_ptr_mut` | parivartanīya sūcaka | rakṣita (restricted), arakṣita |
| `addr` | sthāna saṅkhyā | rakṣita (restricted), arakṣita |

Declaring a `safe_ref` alias in `surakṣita` raises `TypeCheckError`.

---

## Ownership / borrow vocabulary

Vocabulary is **defined** at this phase; borrow rule enforcement is deferred to the
rakṣita tooling phase.

| Annotation | Sanskrit | Meaning |
|---|---|---|
| `owned` / `svāmitvaṃ` | svāmitvaṃ | exclusive ownership |
| `borrow` / `uddhāram` | uddhāram | shared immutable borrow |
| `borrow_mut` / `parivartanīya-uddhāram` | parivartanīya-uddhāram | exclusive mutable borrow |

`TypeChecker.env.ownership: dict[str, str]` records the annotation string for each binding.

> [x] Ownership vocabulary defined. Borrow checker enforcement deferred to rakṣita tooling phase.

---

## Effect types

| Annotation | Sanskrit | Meaning |
|---|---|---|
| `pure` / `śuddhaḥ` | śuddhaḥ | no observable side effects |
| `effectful` / `sādhanaṃ` | sādhanaṃ | may perform I/O, mutation, etc. |

Set via `FunctionDef.effect`. The checker records but does not enforce purity.

> [x] Effect annotations (śuddhaḥ / sādhanaṃ) defined. Enforcement deferred to effect-system phase.

---

## Type reflection

```text
prakāra-āharaṇam type_info i32
-- type_info is bound as text "i32"
```

`TypeReflect(target, type_name)` stores the type name string as a `text` value in
the local environment. Useful for dynamic dispatch and debugging.

---

## Async / future / generator / coroutine types

These type forms are **defined** in the catalog and checker vocabulary. Full scheduling
and execution engines are deferred to the async runtime phase.

| Name | Sanskrit | Catalog ID |
|---|---|---|
| `async_future` | anāgata-phalam | TY-ASYNC-FUTURE |
| `generator` | — | TY-GENERATOR |
| `coroutine` | kramaśaḥ-karma | TY-COROUTINE |

> [x] async_future, generator, coroutine — defined in catalog + checker builtins. Runtime deferred.

---

## Class instance types

Records serve as the class-instance substrate: `record_new`, `record_set`, `record_get`,
`record_contains` opcodes implement single-dispatch via field lookup. Full class identity,
methods, and metaclass behaviour are planned for Phase 7.

> [x] Class instance types — records as class instances documented. Full OOP deferred to Phase 7.

---

## Type reflection rules

`prakāra-āharaṇam` emits the type name as a `text` value. The checker assigns
`PrimitiveType("text")` to the target binding. Runtime reflection via type name string
is available in all tiers.

---

## Variance rules

> [x] Variance defined (documentation). No compile-time enforcement needed for current phase.

| Position | Rule |
|---|---|
| Function parameter | contravariant — a wider (supertype) param type is safe |
| Function return | covariant — a narrower (subtype) return type is safe |
| Generic container (read-only) | covariant in element type |
| Generic container (mutable) | invariant — element type must match exactly |
| Borrow | covariant in lifetime (shorter lifetime safe for shorter-lived borrow) |

Concretely: `Option<i32>` is compatible with `Option<i32>` only (invariant container).
Numeric promotion in arithmetic is handled separately via `_promote_numeric`.

---

## Option and Result

`Option<T>` wraps optional values. `Result` is required for `prasāra` (error propagation).

Runtime support: `OptionValue`, `ResultValue` in `runtime_values.py`;
opcodes `option_none / option_some / option_is_some / option_unwrap`,
`result_ok / result_err / result_is_ok / result_unwrap_ok / result_unwrap_err`.

---

## Callable and iterator types

- `callable` — named in catalog; `foreach` requires iterable type (`list`, `iterator`, `hash_map`).
- `iterator` — supports `foreach` loops.

---

## Phase 3 Value and Data Type Substrate

The following types have VM + yantra-pātha substrate complete as of Phase 3. The `.ssk` source directives are pending grammar registration. Use the yantra-pātha (`.sskyp`) form or direct bytecode construction for full pipeline access.

### BigInt (`bigint`)

- **Runtime**: `BigIntValue(value: int)` — host Python `int` (arbitrary precision)
- **Opcodes**: `push_bigint <int>`
- **Yantra-pātha**: `N iti ati-pūrṇāṅkaḥ nikṣipyate.`
- **Example**: `push_bigint 999999999999999999999` → `bigint(999999999999999999999)`
- **Migration note**: Python `int` is inherently arbitrary-precision. No distinct hardware layout type tag yet — that is a future emit-time concern.

### i32 (signed 32-bit integer)

- **Runtime**: `I32Value(value: int)` — range `[-2^31, 2^31-1]`
- **Opcodes**: `push_i32 <int>`, `i32_add_checked`, `i32_add_wrapping`, `i32_add_saturating`
- **Helpers**: `checked_i32_add`, `wrap_i32`, `clamp_i32`
- **Yantra-pātha**: `N iti saṅkhyā-lagu nikṣipyate.`
- **Example**: `push_i32 42` → `i32(42)`
- **Checked overflow**: raises `RuntimeSanskriptError` at runtime
- **Wrapping overflow**: wraps modulo 2^32 (two's complement)
- **Saturating overflow**: clamps to `I32_MIN` or `I32_MAX`

### u32 (unsigned 32-bit integer)

- **Runtime**: `U32Value(value: int)` — range `[0, 2^32-1]`
- **Opcodes**: `push_u32 <int>`, `u32_add_checked`, `u32_add_wrapping`, `u32_add_saturating`
- **Helpers**: `checked_u32_add`, `wrap_u32`
- **Yantra-pātha**: `N iti saṅkhyā-nirṇāśa nikṣipyate.`
- **Example**: `push_u32 4294967295` → `u32(4294967295)`

### bytes (immutable byte sequence)

- **Runtime**: `BytesValue(data: bytes)`
- **Opcodes**: `push_bytes <hex>`, `byte_new`, `byte_len`, `byte_get`
- **Yantra-pātha**: `<hex> iti akṣara-śreṇī nikṣipyate.`
- **Example**: `push_bytes "48656c6c6f"` → `bytes(b'Hello')`
- **Source hint**: `akṣarāṇi name hex` directive parses hex or UTF-8 encoded string

### bytearray (mutable byte buffer)

- **Runtime**: `ByteArrayValue(data: bytearray)` — auto-extends on set
- **Opcodes**: `bytearray_new`, `bytearray_set` (index, value 0..255), `bytearray_get`
- **Yantra-pātha**: `śūnyaḥ akṣara-saṃgrahaḥ nirmīyate.` / `akṣara-saṃgrahe sthāpanam kriyate.`
- **Source hint**: planned `parivartanīya-akṣarāṇi` directive

### Optional (option type)

- **Runtime**: `OptionValue(present: bool, value: SanskriptValue | None)`
- **Opcodes**: `option_none`, `option_some`, `option_is_some`, `option_unwrap`
- **Yantra-pātha**: `śūnyaḥ vikalpaḥ nirmīyate.` / `vikalpe yojanam kriyate.` / `vikalpāt mūlyam gṛhyate.`
- **Example**: `option_some` on `42` → display `some(42)`; `option_none` → `none`
- **Panic**: `option_unwrap` on `none` raises `RuntimeSanskriptError`
- **Source**: `vikalpam name asti value` / `vikalpam name śūnyam`
- **Migration note**: maps to Rust `Option<T>` / Python `Optional[T]`; unwrap panics match `unwrap()` without message customization yet.

### Result (ok/err discriminated union)

- **Runtime**: `ResultValue(ok: bool, value: SanskriptValue)`
- **Opcodes**: `result_ok`, `result_err`, `result_is_ok`, `result_unwrap_ok`, `result_unwrap_err`
- **Yantra-pātha**: `phale saphalatā sthāpyate.` / `phale doṣaḥ sthāpyate.`
- **Example**: `result_ok "done"` → `ok(done)`; `result_err "fail"` → `err(fail)`
- **Panic**: `result_unwrap_ok` on `err` (and vice versa) raises `RuntimeSanskriptError`
- **Source**: `phalam name siddha value` / `phalam name doṣa value`
- **Migration note**: aligns with Rust `Result<T,E>`; error payload is any `SanskriptValue`.

### Tuple (fixed-arity product type)

- **Runtime**: `TupleValue(items: tuple[SanskriptValue, ...])`
- **Opcodes**: `tuple_new <arity>` (dynamic pop), `tuple_get <index>` (static operand)
- **Yantra-pātha**: `N iti yuktiḥ nirmīyate.` / `N iti yuktau aṅkam gṛhyate.`
- **Example**: push 1, push 2, `tuple_new 2` → display `(1, 2)`
- **Panic**: `tuple_get` with out-of-bounds index raises `RuntimeSanskriptError`
- **Source**: `yugmam name val1 val2 …`
- **Migration note**: arity fixed at bind time; use named tuples (`named_tuple_new`) for field labels.

### Hash set

- **Runtime**: `SetValue(items: list[SanskriptValue])` — insertion-ordered, equality via `values_equal`
- **Opcodes**: `set_new`, `set_add` (deduplicates), `set_contains`, `set_len`
- **Yantra-pātha**: `śūnyaḥ samāhāraḥ nirmīyate.` / `samāhāre yojanam kriyate.`
- **Example**: add 1, add 2, add 1 → len 2
- **Source hint**: planned `saṅgrahaḥ name val1 val2 ...` directive

### Deque (double-ended queue)

- **Runtime**: `DequeValue(items: deque[SanskriptValue])`
- **Opcodes**: `deque_new`, `deque_push_back`, `deque_push_front`, `deque_pop_back`, `deque_pop_front`, `deque_len`
- **Yantra-pātha**: full dviguṇa-samūha forms
- **Panic**: pop on empty deque raises `RuntimeSanskriptError`

### IEEE 754 Float Semantics

- **NaN ≠ NaN**: `compare_eq(NaN, NaN)` returns 0; `compare_ne(NaN, NaN)` returns 1
- **Inf arithmetic**: `Inf + 1 = Inf`; `FLOAT_IS_INF` returns 1 for ±Inf
- **Yantra-pātha literals**: `anatam` = +Inf, `ṛṇa anatam` = -Inf, `na-saṅkhyā` = NaN
- **Opcodes**: `float_is_nan`, `float_is_inf`

### Grapheme cluster length

- **Opcode**: `text_grapheme_len`
- **Behaviour**: extended grapheme cluster walk (combining marks, ZWJ sequences)
- **Migration note**: for UAX #29 parity add the `grapheme` crate on the native backend.

### Opaque handles

- **Runtime**: `OpaqueHandle(kind: str, handle_id: int)`
- **Opcodes**: `opaque_new <kind>` (pops handle_id from stack)
- **Yantra-pātha**: `<kind> iti āvaraṇaṃ nirmīyate.`
- **Use case**: binding resource handles (file, socket, DB connection) without exposing internals
- **Source**: `handle_new` with kinds `file`, `socket`, `thread`, `process`

### Phase 3 seal (fixed-width, numerics, ADTs)

- **Modules**: `fixed_width.py`, `phase3_values.py`, `vm_phase3.py`, `phase3_opcodes.py`
- **Opcodes**: +85 entries in `schema-v2.json` (all widths, rational/decimal/complex, collections ADTs)
- **Source directives**: `saṅkhyā8`, `ati-pūrṇāṅka`, `vikalpam`, `phalam`, `yugmam`, `saṅgrahaḥ` — see `examples/phase3-data-types.ssk`
- **Migration note**: host Python carriers until native tag words ship in rakṣita/arakṣita tiers.

---

## Errors

Failures raise `TypeCheckError` (`SANSKRIPT_TYPE`) with a short hint when available.
