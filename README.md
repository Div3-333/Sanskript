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

Current grammar infrastructure includes phonology, transliteration, first-pass sandhi modules, and a strict real-handler truth gate for sutras. The canon currently marks 186 sutras as `implemented`; the old generated 3174 count has been rejected because metadata profiles are not the same as discrete Paninian executable logic.

## Development Checks

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
```
