# API Documentation from Source

Sanskript can emit a **minimal API index** from a `.ssk` program using the CLI `docs`
command. This is the first step toward fuller docstrings and cross-linked reference;
it is not yet a complete standard-library browser.

## Generate

```powershell
$env:PYTHONPATH='src'
python -m sanskript docs examples/cookbook/api-demo.ssk -o docs/generated/cookbook-api-demo.docs.md
```

Default output (when `-o` is omitted) is beside the source:
`examples/cookbook/api-demo.docs.md`.

## What is extracted today

From the parsed program AST plus static type inference (`TypeChecker`):

- **Modules** — names declared with `kṣetram`
- **Functions** — each `vidhānam` as `` `name`(params…) → `returnType` ``

Annotate parameters with builtin type names on the header line:

```text
vidhānam dviguṇa a i32 .
vidhānam triṣṭaya a i32 b i32 c i32 .
```

Supported hints: `i32`, `i64`, `u32`, `f64`, `f32`, `text`, `bool`, `bytes`, `void`, `list`, `hash_map`.
Omitted hints render as `unknown`. Return types use declared `return_type` or inference from
the function body (e.g. literal arithmetic → `i32`).

Example output for [api-demo.ssk](../examples/cookbook/api-demo.ssk) is checked in at
[generated/cookbook-api-demo.docs.md](generated/cookbook-api-demo.docs.md):

```markdown
- `dviguṇa`(a: i32) → `i32`
- `triṣṭaya`(a: i32, b: i32, c: i32) → `i32`
```

Parameter types come from optional hints on the `vidhānam` line (`a i32` after each name). Return types use declared `return_type` or inference from `pratyāvartanam` bodies.

## Grammar register (separate pipeline)

Verb frames, controlled nouns, and runtime register entries are **not** produced by
`sanskript docs`. They sync from the live grammar register:

```powershell
python scripts/export_grammar_register.py
```

That writes [grammar-register.generated.md](grammar-register.generated.md). Implementation:
`src/sanskript/register_docs.py`.

## Python helper (tests and scripts)

```python
from sanskript.phase26_docs import render_source_api_markdown, write_cookbook_api_doc

write_cookbook_api_doc()  # refresh docs/generated/cookbook-api-demo.docs.md
```

## Limitations (honest)

- Parameter types are often `unknown` until source-level annotations are parsed
- No docstrings or cross-module link graph yet
- Stdlib native entry points are documented in [phase10-standard-library-core.md](phase10-standard-library-core.md), not extracted from `.ssk`

Porting the docs generator to pure Sanskript is Phase 27 work; see the independence
checklist.

## Related

- [cookbook.md](cookbook.md)
- [tooling.md](tooling.md)
- [phase26-documentation-learning-path.md](phase26-documentation-learning-path.md)
