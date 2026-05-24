# Engine API Stability

The Aṣṭādhyāyī implementation layer is now treated as a stable backend surface for the controlled language runtime.

Stable public entry points:

| Entry point | Purpose |
| --- | --- |
| `derive_paninian()` | Low-level derivation over `PaninianState` for engine experiments and tests. |
| `synthesize()` | Directed morphology compiler backend for register-approved `DerivationIntent` objects. |
| `auto_derive()` | Family-scoped convenience wrapper that delegates to directed synthesis. |
| `MorphologyFacade.analyze_token()` | Hot-path lookup and bounded fallback analysis for source tokens. |
| `MorphologyFacade.analyze_sentence()` | Sentence-level morphology for parser input. |

Policy:

- The sūtra predicate modules should receive bug fixes and sharper linguistic conditions, not broad rewrites.
- New source-language behavior should be added above the sūtra layer through the grammar register, frame registry, synthesizer recipes, or parser/VM layers.
- Any new accepted source form must be reachable from the grammar register and, when checked in, from `data/controlled_lexicon.json`.
- Any new parser construction must have an example program and a VM-level test.

This keeps the canon work from being destabilized while the end-user language grows.
