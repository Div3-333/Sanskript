# Sanskript

Sanskript is an experiment in building a programming language whose source form is not merely decorated with Sanskrit words, but is governed by Sanskrit grammar.

The project goal is a controlled, Paninian Sanskrit programming language: a valid subset of Sanskrit where inflection, semantic roles, verbal frames, compounds, and sandhi carry real computational meaning.

## Design Promise

Sanskript should not become "Python in a Sanskrit coat." We will prefer a smaller language that is beautiful and grammatical over a larger one that is choppy, mixed, or theatrical.

The current implementation is only a seed. It proves the compiler shape:

1. Normalize Sanskrit text.
2. Analyze each word morphologically.
3. Load controlled verb frames and morphology from data-backed registers.
4. Recover kāraka-style semantic roles from inflection and verb frames.
5. Build an AST from sentence meaning rather than token position.
6. Lower the AST to Sanskript IR, bytecode, and the Sanskript VM.

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

## Compile Once, Run Bytecode

Sanskript source can be compiled into portable JSON bytecode with the `.sskbc` extension:

```powershell
$env:PYTHONPATH='src'; python -m sanskript compile examples/caturtha.ssk
```

This writes `examples/caturtha.sskbc` by default. You can choose the output path:

```powershell
$env:PYTHONPATH='src'; python -m sanskript compile examples/caturtha.ssk -o C:\tmp\caturtha.sskbc
```

Run source or bytecode with the same command:

```powershell
$env:PYTHONPATH='src'; python -m sanskript run examples/caturtha.ssk
$env:PYTHONPATH='src'; python -m sanskript run C:\tmp\caturtha.sskbc
```

Readable VM text can also be kept in Sanskrit-prose yantra-pāṭha form:

```powershell
$env:PYTHONPATH='src'; python -m sanskript disassemble C:\tmp\caturtha.sskbc
$env:PYTHONPATH='src'; python -m sanskript assemble C:\tmp\caturtha.sskyp
$env:PYTHONPATH='src'; python -m sanskript run C:\tmp\caturtha.sskyp
```

Yantra-pāṭha sentences avoid braces, semicolons, symbolic operators, and Python/C-style expression syntax. A machine instruction is rendered as formal Sanskrit meta-prose, such as `pañca iti pūrṇāṅkaḥ nikṣipyate.` or `phala iti nāma āhriyate.`.

Text values are now part of the executable language without quote syntax:

```text
vākyam svāgatam mitra iti phale nidadhāti.
gaṇakaḥ phalaṃ darśayati.
```

Export a first static browser app:

```powershell
$env:PYTHONPATH='src'; python -m sanskript web examples/prathama.ssk -o C:\tmp\sanskript-app.html
```

The generated HTML embeds Sanskript bytecode and runs it in a small browser VM. This is the first web target: it can render program output today, while future DOM/event APIs should be exposed through grammatical Sanskript standard-library surfaces rather than JavaScript syntax.

## Project Status

This is not yet the final language. It is the first executable scaffold for a stricter design:

- IAST is the current canonical input form.
- Devanagari input is normalized on the morphology hot path.
- Sandhi is currently permissive; later phases should make it explicit and validated.
- Verb-frame syntax is driven by `data/verb_frames.json`, while the grammar register and controlled lexicon define the accepted source forms.
- Every accepted construction should carry a grammar note, review status, generated register entry, and parser/runtime test.

See [docs/charter.md](docs/charter.md) and [docs/language-design.md](docs/language-design.md).
The paradigm roadmap lives at [docs/language-paradigms.md](docs/language-paradigms.md).
The controlled grammar register lives at [docs/grammar-register.md](docs/grammar-register.md), with a tested generated sync view at [docs/grammar-register.generated.md](docs/grammar-register.generated.md).
The morphology-to-semantics plan lives at [docs/feature-lattice.md](docs/feature-lattice.md).
The PDF-derived grammar canon lives at [docs/grammar-canon.md](docs/grammar-canon.md).
The canon implementation roadmap lives at [docs/implementation-plan.md](docs/implementation-plan.md).
The stable engine API boundary lives at [docs/engine-api-stability.md](docs/engine-api-stability.md).
The visual beginner guide lives at [docs/guide/index.html](docs/guide/index.html).
The granular reference guide lives at [docs/guide/reference.html](docs/guide/reference.html).

Current grammar infrastructure includes phonology, transliteration, first-pass sandhi modules, and a strict real-handler truth gate for sutras.

Adhyaya 1-3 now also have a shared dry-style engine layer in `src/sanskript/adhyaya123_engines.py`. It exposes a reusable sutra-predicate selection bridge plus domain engines for technical names/it-markers, metarules, samasa, karaka-vibhakti, subanta sup forms, lopa/root substitution, sanadi-dhatu/vikarana, krt derivation, and tinanta lakara conjugation. These engines reuse the truth-gated sutra predicates instead of copying rule logic.

Sanskript now has an explicit implementation-independent runtime boundary: source is parsed into Sanskript AST, lowered into Sanskript IR, lowered again into Sanskript bytecode, and executed by a Sanskript VM. Python hosts this first VM, but the semantics are no longer direct Python interpreter branches.

The command-line toolchain now has a split compile/run boundary: `.ssk` source compiles to `.sskbc` bytecode, and `.sskbc` runs directly in the VM without reparsing Sanskrit source.

The bytecode layer now has a reversible Sanskrit-prose yantra-pāṭha form (`.sskyp`): `.sskbc` can be disassembled into prose, assembled back into bytecode, and run directly. This is the first bootstrapping step toward a future self-hosted VM written in Sanskript itself, while keeping the user-facing and human-readable layers aligned with the no-trench-coat design promise.

Functions now have argument passing and local parameter binding across source, AST, IR, bytecode, the Python VM, the Rust VM scaffold, and yantra-pāṭha. Source keeps the prose shape, for example `vidhānam sthāpaya balaṃ.` and `āhvānam sthāpaya pañca.` rather than symbolic call syntax.

The runtime value model now supports integers and text. Text uses the Sanskrit quotative `iti` at the source layer and `push_text`/`... iti vākyam nikṣipyate.` at the bytecode and yantra-pāṭha layers. This is the first non-numeric value family and the base for user-facing web output.

Sanskript also has an initial static web export command (`sanskript web`) that packages compiled bytecode into a browser runner. This is not yet a full web framework, but it establishes the browser execution target needed for later UI, DOM, state, and event APIs.

The parser hot path now uses a data-driven frame registry: `nidadhāti`/`sthāpayati` assign, `vardhayati`/`yojayati` increase, `nyūnayati`/`vyavakalayati` decrease, and `darśayati`/`prakāśayati` display. New frame surfaces can be added by extending `data/verb_frames.json`, rebuilding the controlled lexicon, and adding examples/tests.

The derivation layer has begun moving beyond example lookup: Adhyāya 4–5 now have five shared engines for strī-pratyaya formation, taddhita rule selection, semantic relation interpretation, taddhita surface realization, and samāsānta endings. These engines consume the existing per-sūtra predicates instead of duplicating them, while the core apatya, matup, and atiśayana anchors still record sutra id, semantic relation, suffix, surface form, and stem operations.

The truth gate now requires **discrete Pāṇinian predicates** — every implemented sutra is a hand-written Python function that checks specific Pāṇinian conditions (root class, case, role, semantic context, lakāra, suffix, …) against a linguistically real positive example and rejects a linguistically real negative example. The previous slug-roundtrip scaffold has been retired.

Real-implementation modules (Adhyāya 1–8 in full via discrete predicates):

| Module                         | Range            | Sutras |
| ------------------------------ | ---------------- | ------ |
| `sutra_logic.py` main registry | Adhyāya 1–3 anchors |    219 |
| `sutra_handlers_1_2.py`        | misc Adhyāya 1   |     28 |
| `sutra_impl_1_1.py`            | 1.1 (gaps)       |     29 |
| `sutra_impl_1_rest.py`         | 1.2 + 1.3 + 1.4  |    201 |
| `sutra_impl_2.py`              | Adhyāya 2 (all)  |    191 |
| `sutra_impl_3_1.py`            | 3.1              |    137 |
| `sutra_impl_3_2.py`            | 3.2              |    180 |
| `sutra_impl_3_3.py`            | 3.3              |    167 |
| `sutra_impl_3_4.py`            | 3.4              |    102 |
| `sutra_impl_4.py`              | Adhyāya 4 (all)  |    633 |
| `sutra_impl_5.py`              | Adhyāya 5 (all)  |    553 |
| `sutra_impl_6_1.py`            | 6.1              |    223 |
| `sutra_impl_6_2.py`            | 6.2              |    199 |
| `sutra_impl_6_3.py`            | 6.3              |    139 |
| `sutra_impl_6_4.py`            | 6.4              |    175 |
| `sutra_impl_7_1.py`            | 7.1 agama        |    103 |
| `sutra_impl_7_2.py`            | 7.2 vikara       |    118 |
| `sutra_impl_7_3.py`            | 7.3 ādeśa        |    120 |
| `sutra_impl_7_4.py`            | 7.4 ṇati/lopa    |     97 |
| `sutra_impl_8_1.py`            | 8.1 samāsānta    |     74 |
| `sutra_impl_8_2.py`            | 8.2 asiddha      |    108 |
| `sutra_impl_8_3.py`            | 8.3 saṃhitā      |    119 |
| `sutra_impl_8_4.py`            | 8.4 avasāna      |     68 |
| **Total real predicates**      |                  | **3983** |

The regression test `tests/test_sutra_logic.py::RealDiscreteImplementationTests`
enforces that every wired sutra is routed through one of these real-implementation modules, that no `_evaluate(...)` slug round-trip is reintroduced, and that each predicate fires on its positive fixture and rejects its negative fixture.

## Development Checks

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
```

```powershell
$env:PYTHONPATH='src'; python -m sanskript performance --iterations 20
```
