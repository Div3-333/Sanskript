# Sanskript

Sanskript is an experiment in building a programming language whose source form is not merely decorated with Sanskrit words, but is governed by Sanskrit grammar.

The project goal is a controlled, Paninian Sanskrit programming language: a valid subset of Sanskrit where inflection, semantic roles, verbal frames, compounds, and sandhi carry real computational meaning.

## Design Promise

Sanskript should not become "Python in a Sanskrit coat." We will prefer a smaller language that is beautiful and grammatical over a larger one that is choppy, mixed, or theatrical.

The current implementation is only a seed. It proves the compiler shape:

1. Normalize Sanskrit text.
2. Analyze each word morphologically.
3. Recover kāraka-style semantic roles from inflection and verb frames.
4. Build an AST from sentence meaning rather than token position.
5. Interpret or later compile that AST.

## Tiny Current Example

```text
gaṇakaḥ pañca phale nidadhāti.
gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
gaṇakaḥ phalaṃ darśayati.
```

Roughly:

```text
The calculator places five in the result.
The calculator increases the result by two.
The calculator displays the result.
```

Run it:

```powershell
$env:PYTHONPATH='src'; python -m sanskript examples/prathama.ssk
```

Expected output:

```text
7
```

## Project Status

This is not yet the final language. It is the first executable scaffold for a stricter design:

- IAST is the current canonical input form.
- Devanagari support is planned.
- Sandhi is currently permissive; later phases should make it explicit and validated.
- Every accepted construction should eventually carry a grammar note and review status.

See [docs/charter.md](docs/charter.md) and [docs/language-design.md](docs/language-design.md).
The controlled grammar register lives at [docs/grammar-register.md](docs/grammar-register.md).
The morphology-to-semantics plan lives at [docs/feature-lattice.md](docs/feature-lattice.md).
The PDF-derived grammar canon lives at [docs/grammar-canon.md](docs/grammar-canon.md).
The canon implementation roadmap lives at [docs/implementation-plan.md](docs/implementation-plan.md).
The visual beginner guide lives at [docs/guide/index.html](docs/guide/index.html).
The granular reference guide lives at [docs/guide/reference.html](docs/guide/reference.html).

Current grammar infrastructure includes phonology, transliteration, first-pass sandhi modules, and a strict real-handler truth gate for sutras.

Adhyaya 1-3 now also have a shared dry-style engine layer in `src/sanskript/adhyaya123_engines.py`. It exposes a reusable sutra-predicate selection bridge plus domain engines for technical names/it-markers, metarules, samasa, karaka-vibhakti, subanta sup forms, lopa/root substitution, sanadi-dhatu/vikarana, krt derivation, and tinanta lakara conjugation. These engines reuse the truth-gated sutra predicates instead of copying rule logic.

The derivation layer has begun moving beyond example lookup: Adhyāya 4–5 now have five shared engines for strī-pratyaya formation, taddhita rule selection, semantic relation interpretation, taddhita surface realization, and samāsānta endings. These engines consume the existing per-sūtra predicates instead of duplicating them, while the core apatya, matup, and atiśayana anchors still record sutra id, semantic relation, suffix, surface form, and stem operations.

The truth gate now requires **discrete Pāṇinian predicates** — every implemented sutra is a hand-written Python function that checks specific Pāṇinian conditions (root class, case, role, semantic context, lakāra, suffix, …) against a linguistically real positive example and rejects a linguistically real negative example. The previous slug-roundtrip scaffold has been retired.

Real-implementation modules (Adhyāya 1–5 in full via discrete predicates; Adhyāya 6 partial):

| Module                         | Range            | Sutras |
| ------------------------------ | ---------------- | ------ |
| `sutra_logic.py` main registry | Adhyāya 1–3 anchors, 6 (+ sandhi) |    227 |
| `sutra_handlers_1_2.py`        | misc Adhyāya 1   |     28 |
| `sutra_impl_1_1.py`            | 1.1 (gaps)       |     29 |
| `sutra_impl_1_rest.py`         | 1.2 + 1.3 + 1.4  |    201 |
| `sutra_impl_2.py`              | Adhyāya 2 (all)  |    190 |
| `sutra_impl_3_1.py`            | 3.1              |    137 |
| `sutra_impl_3_2.py`            | 3.2              |    180 |
| `sutra_impl_3_3.py`            | 3.3              |    167 |
| `sutra_impl_3_4.py`            | 3.4              |    102 |
| `sutra_impl_4.py`              | Adhyāya 4 (all)  |    633 |
| `sutra_impl_5.py`              | Adhyāya 5 (all)  |    553 |
| **Total real predicates**      |                  | **2447** |

The regression test `tests/test_sutra_logic.py::RealDiscreteImplementationTests`
enforces that every wired sutra is routed through one of these real-implementation modules, that no `_evaluate(...)` slug round-trip is reintroduced, and that each predicate fires on its positive fixture and rejects its negative fixture.

## Development Checks

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
```
