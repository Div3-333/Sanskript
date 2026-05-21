# Language Design

## Name

The working name is Sanskript. The spelling is intentionally project-like, but the source language should use Sanskrit forms, not project branding.

## Input Script

The first implementation accepts IAST transliteration. This keeps the compiler small while we design the grammar.

Planned script layers:

1. IAST canonical input.
2. Devanagari input normalized to the same internal representation.
3. Optional ASCII development aliases only for tests and tooling, never as the literary standard.

## Program Form

A program is a sequence of sentences. The current sentence terminator is `.` or danda `।`.

Example:

```text
gaṇakaḥ pañca phale nidadhāti.
gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
gaṇakaḥ phalaṃ darśayati.
```

## Semantic Model

Sanskript starts from verbal frames. Each known verb declares the roles it can accept.

Current prototype frames:

| Verb | Surface sense | Required roles | Computational sense |
| --- | --- | --- | --- |
| `nidadhāti` | places | karma + adhikaraṇa | assign value to a named location |
| `vardhayati` | increases | karma + karaṇa | increment a stored value |
| `darśayati` | shows | karma | display a value |
| `nyūnayati` | lessens | karma + karaṇa | decrement a stored value |

The compiler recovers these roles from analyzed word forms. The current subset is declared in [grammar-register.md](grammar-register.md). Some core examples:

| Role | Prototype marker | Example | Meaning |
| --- | --- | --- | --- |
| kartṛ | nominative | `gaṇakaḥ` | agent |
| karma | accusative | `phalaṃ` | acted-on object |
| karaṇa | instrumental | `dvābhyāṃ` | means or increment |
| adhikaraṇa | locative | `phale` | storage location |

The role mapping is intentionally attached to verb frames. Case alone is not enough for a mature Sanskrit parser.

## Independence Architecture

Sanskript semantics do not lower to Python source or Python AST. The current compiler path is:

```text
Sanskrit source -> morphology -> Sanskript AST -> Sanskript IR -> Sanskript bytecode -> Sanskript VM
```

The VM is currently hosted in Python, but it consumes only Sanskript-owned bytecode instructions from `bytecode.py`. Python is therefore an implementation host, not the semantic target. The durable language boundary is:

- `ast.py`: sentence-level semantic statements recovered from Sanskrit roles;
- `ir.py`: Sanskript intermediate representation with storage, adjustment, and output operations;
- `compiler.py`: AST-to-IR and IR-to-bytecode lowering;
- `bytecode.py`: owned opcodes such as `push_int`, `load_name`, `store_name`, `add`, `subtract`, and `emit`;
- `vm.py`: bytecode execution state, stack, environment, and output.

Future non-Python runtimes should implement the bytecode contract rather than reinterpret the Sanskrit source directly.

## Identifiers

The current prototype uses ordinary Sanskrit nouns as storage names. For example:

- `phala` means result, fruit, or outcome.
- `phale` marks the result-location.
- `phalaṃ` marks the result as the object of an action.

The language should avoid arbitrary variable sigils. If the source code needs a new name, the preferred path is a grammatical Sanskrit noun or compound.

## Morphological Feature Lattice

Sanskript should use Sanskrit's combinatoric richness as a feature lattice, not as an arbitrary opcode table. Case, number, gender, person, lakāra, pada, and prayoga should each carry computational meaning only where Sanskrit gives us a defensible semantic basis.

See [feature-lattice.md](feature-lattice.md).

## Canon Coverage

The supplied PDFs are indexed in [grammar-canon.md](grammar-canon.md). New features should cite the relevant canon topic or sutra range before they graduate from experimental status.

Non-executable outline material, such as source metadata, prefaces, reviews, and script/tooling chapters, is tracked in `canon_topics.py`. These entries are partial canon treatments, not release-complete implementations.

## Word Order

Because the prototype uses morphology, these two sentences compile to the same assignment:

```text
gaṇakaḥ pañca phale nidadhāti.
phale gaṇakaḥ pañca nidadhāti.
```

This is a crucial design property. Word order can later carry discourse nuance, but it should not become the hidden operator system.

## Avyaya And Sentence Force

Indeclinables are now treated as grammar-bearing forms, not punctuation aliases. The initial controlled layer recognizes particles such as `ca`, `vā`, `api`, `eva`, `na`, `mā`, `kim`, `yatra`, `tatra`, `yadā`, and `tadā`.

These forms currently feed sentence profiling:

- `kim`, `katham`, and `kadā` mark question profiles.
- `yatra` and `yadā` mark relative profiles, with `tatra` and `tadā` as correlatives.
- `ca` and `vā` mark coordination or alternatives.
- `na` and `mā` are reserved for assertion and command negation.

Upasargas are tracked in a separate registry so future verbal derivation can attach them to dhātus without treating prefixes as arbitrary string operators.

## Metarules

The Aṣṭādhyāyī does not behave like a flat list of rewrite rules. Sanskript therefore has a metarule scaffold for technical markers, optionality, prohibition, domain carry, and late sentence-edge operations. The current truth gate marks 3613 sutras as implemented, each backed by a named handler in `sutra_logic.evaluate_sutra`. The previous generated Adhyaya 1-6 metric is rejected because metadata profiles are not discrete Paninian logic.

## Future Safety Tiers

The planned memory model can use Sanskrit grammar as the safety surface rather than a borrowed systems-language syntax. A possible split:

- `surakṣita` Sanskript: high-level, fully checked ownership, lifetimes, effects, and memory regions.
- `rakṣita` Sanskript: explicit manual control like Rust/C, with checked declarations for ownership transfer, borrowing, mutation, and release.
- `arakṣita` Sanskript: raw machine-facing operations for pointers, address arithmetic, layout, and unchecked calls.

The grammar gives useful handles: genitive for ownership, dative for transfer/recipient, instrumental for pointer-like tools, locative for memory regions, ablative for release/source, and moods/prohibitions for unsafe permission boundaries.

## Accent And Aṅga

The remaining sound-form sutra ranges are now represented by two explicit substrates:

- `accent.py` records udātta, anudātta, svarita, and pracaya as metadata over token domains.
- `anga.py` records controlled stem operations such as guṇa, vṛddhi, final lengthening, lopa, augment, nasalization, and retroflexion.

This gives `6.2` through `6.4` useful runtime scaffolding while keeping the truth layer honest: these ranges remain partial until each sutra receives individual executable treatment.

## Sandhi

Sandhi is currently normalized lightly, not fully enforced. The language should eventually support stricter modes:

- `learning`: accept separated words and report suggested sandhi.
- `strict`: require grammatical external sandhi where appropriate.
- `analysis`: show the split, rule, and semantic role analysis.

## Error Philosophy

Errors should be grammatical first, computational second.

Good:

```text
nidadhāti needs an adhikaraṇa participant, such as phale.
```

Better future form:

```text
nidadhāti expects a locative locus for the storage target.
```

Bad:

```text
Syntax error near token 3.
```
