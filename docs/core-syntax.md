# Core Syntax (Phase 2)

Phase 2 adds variable binding, scope, booleans, comparisons, and literal forms
in grammatical Sanskrit prose (directives and verb frames).

## Binding

| Form | Meaning |
|------|---------|
| `gaṇitam TARGET VALUE` | Mutable binding |
| `acalachihnam TARGET VALUE` | Immutable binding |
| `nityam TARGET VALUE` | Immutable binding (prefix style) |
| `ghoṣaṇam TARGET` | Forward declaration in the current scope |

Assignment without `=` uses verb frames (`nidadhāti`, `vardhayati`, …) or
`āhvānam` / `gaṇitam` directives.

**Shadowing:** declaring the same name twice in one scope is a compile-time error.

## Block scope

```
khaṇḍaḥ
  … statements …
antam
```

Names bound inside the block are not visible outside it.

## Module export

Inside a `kṣetram`:

```
niḥsāram functionName.
```

Exported names must match a `vidhānam` in that module.

## Module files and imports (Phase 9 subset)

Use `ānayanam` to import module files from other `.ssk` files:

| Form | Meaning |
|------|---------|
| `ānayanam gaṇita` | Load `gaṇita.ssk`; module available as `gaṇita` |
| `ānayanam gaṇita nāmnā m` | Module alias (`m`) |
| `ānayanam gaṇita antaḥ vṛddhi` | Selective import into local call name |
| `ānayanam gaṇita antaḥ vṛddhi nāmnā vardhana` | Selective import with alias |
| `ānayanam pkg/gaṇita` | Package directory path (`pkg/gaṇita.ssk`) |

When a module declares at least one `niḥsāram`, only exported functions are public.
If no exports are declared, all module functions remain callable (backward compatibility).

## Booleans

| Form | Meaning |
|------|---------|
| `satyam` / `asatyam` | Boolean literals |
| `na EXPR` | Negation |
| `EXPR ca EXPR` | Short-circuit conjunction |
| `EXPR vā EXPR` | Short-circuit disjunction |

Conditions in `yadi` / `punaḥ` use explicit comparisons or boolean combinations.

## Comparisons

| Marker | Meaning |
|--------|---------|
| `samam` | Equality |
| `asamam` | Inequality |
| `nyūnam` / `laghutaram` | Less than |
| `mahattaram` | Greater than |
| `tulyam` | Less than or equal |
| `sadr̥śam` | Identity (text equality for now) |
| `CONTAINER asti KEY` | Map membership |

## Literals

| Form | Meaning |
|------|---------|
| `śūnyam` | Nil (distinct from integer `śūnya` / 0) |
| `vākyam … iti` | Text |
| `samūhalakṣaṇaḥ NAME v1 v2 …` | List literal |
| `kośalakṣaṇaḥ NAME k1 v1 k2 v2 …` | Map literal |
| `akṣarāṇi NAME HEX…` | Bytes (hex) |
| `vastulakṣaṇaḥ NAME f1 v1 f2 v2 …` | Record literal (field/value pairs) |
| `pariveṣṭanam … antam` | Explicit grouping |

## Statement-only

| Form | Meaning |
|------|---------|
| `tyāgaḥ VALUE` | Evaluate and discard (void) |
| `darśanam` / `darśayati` | Emit output |

## Examples

- `examples/dvādaśa-phase2-boolean.ssk` — conditionals and booleans
- `examples/dvādaśa-phase2-kṣetram.ssk` — module export

## Migration Notes

If you wrote Python, write Sanskript instead:

| Python | Sanskript |
|--------|-----------|
| `x = 5` | `gaṇitam x pañca.` |
| `x: int = 5` (const) | `acalachihnam x pañca.` |
| `if x == 5:` | `yadi xaṃ samam pañca.` |
| `print(x)` | `darśanam x.` |
| `x += 3` | `gaṇakaḥ xaṃ tribhiḥ vardhayati.` |
| `lst = [1, 2, 3]` | `samūhalakṣaṇaḥ lst eka dvi tri.` |
| `d = {"a": 1}` | `kośalakṣaṇaḥ d a eka.` |
| `obj = {"name": 5}` | `vastulakṣaṇaḥ obj nāma pañca.` |
| `b = bytes.fromhex("ff")` | `akṣarāṇi b ff.` |
| `_ = expr` | `tyāgaḥ expr.` |
