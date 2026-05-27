# Sanskript Style Guide

Canonical prose register for executable Sanskript programs.

## Prose register

- Write **one complete vākya per statement**, ending with `.` or danda `।`.
- Prefer **finite verbal predicates** (`nidadhāti`, `vardhayati`, `darśayati`) over fragmentary lists of nouns.
- Use **case roles** (karma, karaṇa, adhikaraṇa) that match the verb frame; do not rely on word order alone.
- Keep **compounds** for names and selectors (`gaṇaka`, `phala`, `mūlya`); avoid symbolic sigils or camelCase.
- **Particles** (`ca`, `eva`, `na`) modify discourse; they do not replace required case marking.

## Accepted scripts

| Script | Use | Canonical compile form |
| --- | --- | --- |
| IAST | Primary literary and tooling standard | IAST |
| Devanagari | Manuscripts, teaching, native readers | normalized to IAST |
| Harvard-Kyoto | ASCII email / legacy corpora | normalized to IAST |
| SLP1 | Lexicon and dhātu catalogs | normalized to IAST |

Diagnostics may show the user’s script via reversible transliteration; the compiler always parses **canonical IAST** internally.

## Comments and documentation

- Line comments: `// …` or a line beginning with `व्याख्या` / `व्याख्या:`.
- Block comments: `(* … *)`.
- Docstrings attach to `vidhānam` bodies in prose (see [language-design.md](language-design.md)).

## Declarations and scope

- Blocks end with `antam` / `samāpanam`, not braces.
- Modules: `kṣetram <name>.`
- Functions: `vidhānam <name> … samāpanam.`
- Nested scopes use marker sentences; indentation is for readability only.

## Directives

| Directive | Effect |
| --- | --- |
| `śikṣām.` | Learning mode: richer hints; same compile rules |
| `paninianam.` | Strict morphology validation |
| `sandhīnam.` | Sandhi-aware token segmentation |
| `surakṣitam.` / `rakṣitam.` / `arakṣitam.` | Safety tier |

Environment: `SANSKRIPT_LEARNING=1`, `SANSKRIPT_STRICT=1`.

## Formatting

Run the canonical formatter (`sanskript.formatter.format_source`):

- One sentence per line.
- Single spaces between words.
- Sentence-final `.` normalized.

Layout is **not semantic**; the linter may warn about choppy or verb-less sentences.

## Naming

- **Nouns** for storage and types; **verbs** for computation and effects.
- **Instrumental** for means/increments, **locative** for loci, **accusative** for objects.
- Prefer register forms from [grammar-register.md](grammar-register.md) over ad-hoc coinages.
- Source identifiers are parsed by `sanskript.identifiers`, not by the avyaya
  register. A name may be a registered nominal/pronominal form, which
  canonicalizes to its lemma, or a simple technical compound made from letters,
  digits after the first character, `_`, `-`, and `.`. Raw numerals, operator
  punctuation, and example-only English names must not be added as particles.

## Examples

Good:

```text
gaṇakaḥ pañca phale nidadhāti.
gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
```

Avoid:

```text
phale pañca.
gaṇaka darśana.
```

See [examples/prathama.ssk](../examples/prathama.ssk) and [examples/shodasha-devanagari.ssk](../examples/shodasha-devanagari.ssk).

## Migration notes (Phase 1 surface syntax)

These notes apply when porting Sanskript programs written against pre-Phase-1 tooling.

### Script normalization

Programs that relied on Devanagari or Harvard-Kyoto source reaching the parser verbatim now go
through `prepare_source` first. Normalisation is **idempotent** and **reversible**; no source
semantics change.

### Comment syntax

`//`-style line comments are stripped before parsing; they are not valid tokens inside expressions.
Legacy sources that used `#` or `--` for comments must migrate to `//` or `(* … *)` block syntax.

### Directive placement

Directives (`śikṣām.`, `paninianam.`, `sandhīnam.`) must appear at the **start** of the file before
any executable vākya. Directives inside function bodies are ignored.

### Formatter idempotency guarantee (Phase 1)

Formatted output from `format_source` is guaranteed to re-parse identically. If a round-trip fails,
it is a bug in the formatter — file an issue.

### Linter warnings

The linter is **non-blocking** (warnings only). CI will not fail on lint findings. Three key rules:

| Code | Meaning |
| --- | --- |
| `MISSING_VERB` | Sentence has no finite verbal predicate |
| `MULTIPLE_VERBS` | More than one finite verb in one vākya |
| `CHOPPY_SENTENCE` | Fewer than three words — prefer full vākyas |
