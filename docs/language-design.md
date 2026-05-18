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

The compiler recovers these roles from analyzed word forms. The current subset is declared in [grammar-register.md](grammar-register.md). Some core examples:

| Role | Prototype marker | Example | Meaning |
| --- | --- | --- | --- |
| kartṛ | nominative | `gaṇakaḥ` | agent |
| karma | accusative | `phalaṃ` | acted-on object |
| karaṇa | instrumental | `dvābhyāṃ` | means or increment |
| adhikaraṇa | locative | `phale` | storage location |

The role mapping is intentionally attached to verb frames. Case alone is not enough for a mature Sanskrit parser.

## Identifiers

The current prototype uses ordinary Sanskrit nouns as storage names. For example:

- `phala` means result, fruit, or outcome.
- `phale` marks the result-location.
- `phalaṃ` marks the result as the object of an action.

The language should avoid arbitrary variable sigils. If the source code needs a new name, the preferred path is a grammatical Sanskrit noun or compound.

## Word Order

Because the prototype uses morphology, these two sentences compile to the same assignment:

```text
gaṇakaḥ pañca phale nidadhāti.
phale gaṇakaḥ pañca nidadhāti.
```

This is a crucial design property. Word order can later carry discourse nuance, but it should not become the hidden operator system.

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
