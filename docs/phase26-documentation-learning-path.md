# Phase 26: Documentation and Learning Path

Inventory of learning materials for the native independence checklist. **Phase 26 is sealed:** every row below is **done** with runnable `.ssk` proof where applicable (`tests/test_phase26_documentation.py`).

## Learning path (recommended order)

```mermaid
flowchart LR
  A[tutorial-beginner] --> B[core-syntax]
  B --> C[cookbook]
  C --> D[functions-procedures]
  D --> E[type-system-reference]
  E --> F[modules-packages]
  F --> G[domain guides]
  G --> H[phase docs 10-20]
```

| Step | Audience | Document | Runnable proof |
| --- | --- | --- | --- |
| 1 | New user | [tutorial-beginner.md](tutorial-beginner.md) | [cookbook/](../examples/cookbook/) |
| 2 | Syntax | [core-syntax.md](core-syntax.md) | phase 2 examples |
| 3 | Patterns | [cookbook.md](cookbook.md) | twelve tested cookbook `.ssk` |
| 4 | Python/Rust background | [migration-from-python.md](migration-from-python.md), [migration-from-rust.md](migration-from-rust.md) | same cookbook |
| 5 | Tooling | [tooling.md](tooling.md) | CLI tests |
| 6 | API index | [api-from-source.md](api-from-source.md) | [generated/cookbook-api-demo.docs.md](generated/cookbook-api-demo.docs.md) |
| 7 | Domains | `guide-*.md` below | per-guide cookbook rows |
| 8 | Contributing | [contributing.md](contributing.md) | unittest + Phase 26 link tests |

Visual alternative: [guide/index.html](guide/index.html) (static, no VM).

## Checklist inventory (28 rows — all done)

| Item | Status | Where | Notes |
| --- | --- | --- | --- |
| Beginner tutorial | **done** | [tutorial-beginner.md](tutorial-beginner.md) | Prose + cookbook runs |
| Prose syntax guide | **done** | [core-syntax.md](core-syntax.md) | Phase 2 reference |
| Sanskrit grammar mapping | **done** | [guide-grammar-primer.md](guide-grammar-primer.md) | Single entry primer |
| Python migration | **done** | [migration-from-python.md](migration-from-python.md) | Maps idioms, not stdlib |
| Rust migration | **done** | [migration-from-rust.md](migration-from-rust.md) | Ownership ≠ borrow yet |
| Standard library reference | **done** | [guide-stdlib-reference.md](guide-stdlib-reference.md), [phase10-standard-library-core.md](phase10-standard-library-core.md) | Host-backed surfaces |
| Type system reference | **done** | [type-system-reference.md](type-system-reference.md) | |
| Object model reference | **done** | [object-oriented.md](object-oriented.md) | |
| Functional programming guide | **done** | [guide-functional.md](guide-functional.md), [functional-declarative.md](functional-declarative.md) | [functional-call.ssk](../examples/cookbook/functional-call.ssk) |
| Systems programming guide | **done** | [guide-systems-programming.md](guide-systems-programming.md) | [systems-tier.ssk](../examples/cookbook/systems-tier.ssk) + phase 13–16 |
| Machine programming guide | **done** | [guide-machine-programming.md](guide-machine-programming.md) | phases 16–17 + [guide-sskyp-reference.md](guide-sskyp-reference.md) |
| Web app guide | **done** | [guide-web-apps.md](guide-web-apps.md) | [web-hello.ssk](../examples/cookbook/web-hello.ssk) |
| CLI guide | **done** | [guide-cli-apps.md](guide-cli-apps.md) | [cli-sqrt.ssk](../examples/cookbook/cli-sqrt.ssk) |
| Desktop app guide | **done** | [guide-desktop-apps.md](guide-desktop-apps.md) | [desktop-plan.ssk](../examples/cookbook/desktop-plan.ssk) |
| Game development guide | **done** | [guide-game-development.md](guide-game-development.md) | [game-input.ssk](../examples/cookbook/game-input.ssk) |
| Data/research scripting guide | **done** | [guide-data-research.md](guide-data-research.md) | [research-spark.ssk](../examples/cookbook/research-spark.ssk) |
| ML guide | **done** | [guide-ml.md](guide-ml.md) | [ml-dot.ssk](../examples/cookbook/ml-dot.ssk) |
| Compiler architecture guide | **done** | [guide-compiler-architecture.md](guide-compiler-architecture.md) | compile/run any cookbook |
| VM architecture guide | **done** | [guide-vm-architecture.md](guide-vm-architecture.md) | VM tests + phase 18 doc |
| Bytecode reference | **done** | [bytecode-v1.md](bytecode-v1.md), [bytecode-v2.md](bytecode-v2.md) | |
| sskyp reference | **done** | [guide-sskyp-reference.md](guide-sskyp-reference.md) | [phase17-bytecode-toolchain.sskyp](../examples/phase17-bytecode-toolchain.sskyp) |
| Package manager guide | **done** | [modules-packages.md](modules-packages.md) | |
| Tooling guide | **done** | [tooling.md](tooling.md) | |
| Contributing guide | **done** | [contributing.md](contributing.md) | PR flow + Phase 26 gates |
| Style guide | **done** | [style-guide.md](style-guide.md) | |
| Cookbook | **done** | [cookbook.md](cookbook.md) | Twelve tested `examples/cookbook/*.ssk` |
| API docs from source | **done** | [api-from-source.md](api-from-source.md) | `sanskript docs` with inferred types |
| Visual HTML learning guide | **done** | [guide/index.html](guide/index.html), [guide/reference.html](guide/reference.html) | Static canon; sutra count tested |

**Phase 26 completion:** all checklist rows **done**; `PHASE26_CHECKED_GUIDES` audits 27 markdown guides (≥200 words, fenced example, compiling `.ssk`); twelve cookbook recipes run in CI; API renderer emits `param → type` lines; `phase26-evidence` → `seal_ready: true`.

## Doc generation wired today

| Source | Generator | Output |
| --- | --- | --- |
| Grammar register | `scripts/export_grammar_register.py` | [grammar-register.generated.md](grammar-register.generated.md) |
| Feature matrix | `tools/generate_feature_matrix.py` | [generated/feature-matrix.md](generated/feature-matrix.md) |
| Cookbook API demo | `sanskript docs` / `phase26_docs.write_cookbook_api_doc` | [generated/cookbook-api-demo.docs.md](generated/cookbook-api-demo.docs.md) |

## Verification

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_phase26_documentation -v
```

Tests assert: markdown link targets exist, all inventory rows are **done**, cookbook programs compile and match expected VM output, generated API doc stays in sync with inferred types.
