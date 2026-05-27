# Object-Oriented Programming (Phase 7)

Phase 7 adds a full object-oriented layer on the existing `vastu` (record) runtime substrate.
Instances remain `RecordValue` objects tagged with `__class__` and an MRO chain in `__mro__`.

## Class Declaration (`vargaḥ`)

```text
vargaḥ Dīpakaḥ jyoti i32 metoda vardhaya darśaya.
```

Extended forms:

| Syntax | Meaning |
|---|---|
| `uttarāt Base` | Inheritance (single base; sealed bases cannot be extended) |
| `gopita field type` | Private field |
| `rakṣita field type` | Protected field |
| `prakāśya field type` | Public field (default) |
| `sthira metoda m₁ …` | Static methods → `Class__static__m` |
| `varga-metoda m₁ …` | Class methods (receiver is class name text) |
| `guṇa p₁ …` | Computed properties via `get_p` methods |
| `abhāvya` | Abstract class (cannot `nirmāṇam`) |
| `mudrita` | Sealed class (no subclasses) |
| `miśra M₁ M₂` | Mixins (composition-first; fields/methods merged) |
| `sādhayati Trait` | Trait/protocol implementation |
| `T paribaddha Trait` | Generic type-parameter trait bound |
| `saha Component field` | Composition-first field embedding |

## Instance Construction (`nirmāṇam`)

```text
nirmāṇam dīpaḥ Dīpakaḥ 5.
```

Lowers to `class_new`, stores `__mro__`, then calls `Dīpakaḥ__init__` when present.

## Instance Methods (`paddhati-āhvānam`)

```text
paddhati-āhvānam phalam dīpaḥ darśaya.
```

Dynamic dispatch walks `__mro__` and resolves overload-suffixed symbols (e.g. `Dīpakaḥ__vardhaya_2`).

## Static and Class Methods

```text
sthira-paddhati-āhvānam z Counter zero.
varga-paddhati-āhvānam c Counter make 3.
```

## Computed Properties

```text
guṇa-āharaṇam m p size.
```

Requires `guṇa size` on the class and a `Class__get_size` implementation.

## Destructors / Finalizers

```text
antima-saṃskāraṃ dīpaḥ.
```

Calls `Class__finalize__` when defined; missing finalizer is a no-op.

## Reflection

```text
varga-prakāra-āharaṇam cn dīpaḥ.
paddhati-prakāra-āharaṇam mn dīpaḥ darśaya.
```

## Traits and Protocols (`abhilakṣaṇaṃ`)

Standard protocol trait names (nominal):

- `Samānatā` — equality (`samāna`)
- `Kramanirṇaya` — ordering (`pūrva`, `anantara`)
- `Saṅkhyābandha` — hashing (`saṅkhyābandha`)
- `Darśana` — display (`darśaya`)
- `Anukrama` — iteration (`agream`, `antaram`)
- `Sandarbha` — context (`praveśa`, `niḥsaraṇa`)
- `Saṃkīrtana` — serialization (`saṃkīrtana`, `visarjana`)

Declare with `abhilakṣaṇaṃ` and assert implementation via `sādhayati` on records or `sādhayati` on classes.

## Dispatch Model

- **Dynamic dispatch**: `METHOD_CALL` + MRO + `resolve_method_target` in the VM.
- **Static dispatch**: `CALL` to a resolved symbol when the class is known at compile time.
- **Composition-first**: prefer `saha` embedding and `miśra` over deep inheritance when modeling has-a relationships.

## Machine Prose (`.sskyp`)

| Opcode | Yantra-pāṭha |
|---|---|
| `class_new` | `{Name} iti varga-nirmāṇam kriyate.` |
| `method_call` | `{method} iti paddhati-āhvānam kriyate.` |

## Migration Notes (Python / Rust)

| Host concept | Sanskript |
|---|---|
| `class Foo:` | `vargaḥ Foo … metoda …` |
| `def __init__` | `vidhānam Foo__init__ svayam …` |
| `self.method()` | `paddhati-āhvānam … receiver method` |
| `@staticmethod` | `sthira metoda …` / `sthira-paddhati-āhvānam` |
| `@classmethod` | `varga-metoda …` / `varga-paddhati-āhvānam` |
| `@property` | `guṇa name` + `Foo__get_name` |
| `abc.ABC` | `abhāvya` on `vargaḥ` |
| `typing.Protocol` | `abhilakṣaṇaṃ` + `sādhayati` |
| Rust `trait` | `abhilakṣaṇaṃ` + `sādhayati` |
| Rust `Drop` | `antima-saṃskāraṃ` / `__finalize__` |

Implementation module: `src/sanskript/oop.py`. Tests: `tests/test_phase7_oop.py`. Example: `examples/phase7-oop.ssk`.
