# Machine Learning Guide

ML support is **incremental**: numeric kernels (`std.linalg`, `std.tensor`), model pack/unpack helpers, and explicit roadmap natives (`std.ml.ad_roadmap`, `std.ml.python_bridge_plan`). There is no training loop product in-tree yet.

## Runnable dot product (vectors)

Build a small integer list and call the host-backed dot product:

```text
samūhalakṣaṇaḥ a 3 4.
āhvānam std.linalg.dot a a darśayati.
```

Full program: [ml-dot.ssk](../examples/cookbook/ml-dot.ssk) → stdout `25.0` (3×3 + 4×4).

```powershell
$env:PYTHONPATH='src'
python -m sanskript run examples/cookbook/ml-dot.ssk
```

## Model pack/unpack (host JSON)

`std.ml.model_pack` accepts a weight map and returns a versioned JSON string; `std.ml.model_unpack` reverses it. Use these for persistence experiments, not for claiming PyTorch parity.

## Tensor helpers

| API | Role |
| --- | --- |
| `std.tensor.shape` | infer nested list shape |
| `std.tensor.reshape` | flat reshape with explicit dims |
| `std.linalg.matmul` | matrix multiply |

## Research crossover

Sparklines and describe summaries for exploratory analysis: [guide-data-research.md](guide-data-research.md). Larger mixed demo: [phase22-web-apps-games-research.ssk](../examples/phase22-web-apps-games-research.ssk).

## Honest gates

Phase 22 checklist keeps **Tensor basics**, **Python ML interop**, and **Native ML kernels** open. Cookbook proof covers **callable numerics**, not trained models.

## Related

- [type-system-reference.md](type-system-reference.md) — numeric types
- [phase22-web-apps-games-research-ml.md](phase22-web-apps-games-research-ml.md)
