# Sanskript Cookbook

Complete, runnable programs. Each entry compiles and executes under the host VM.
Sources live in [examples/cookbook/](../examples/cookbook/). Phase 26 tests pin stdout for every recipe below.

## How to run any recipe

```powershell
$env:PYTHONPATH='src'
python -m sanskript run examples/cookbook/<recipe>.ssk
```

## Core recipes

### Hello counter

| | |
| --- | --- |
| Source | [hello-counter.ssk](../examples/cookbook/hello-counter.ssk) |
| Output | `7` |
| Teaches | `nidadhāti`, `vardhayati`, `darśayati` frames |

```text
gaṇakaḥ pañca phale nidadhāti.
gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
gaṇakaḥ phalaṃ darśayati.
```

### Scaled sum

| | |
| --- | --- |
| Source | [scaled-sum.ssk](../examples/cookbook/scaled-sum.ssk) |
| Output | `7` |

### Conditional branch

| | |
| --- | --- |
| Source | [conditional-branch.ssk](../examples/cookbook/conditional-branch.ssk) |
| Output | `13` |

### Greet (text)

| | |
| --- | --- |
| Source | [greet.ssk](../examples/cookbook/greet.ssk) |
| Output | `svāgatam mitra` |

### Web hello

| | |
| --- | --- |
| Source | [web-hello.ssk](../examples/cookbook/web-hello.ssk) |
| Output | `<h1>Hello</h1>` |
| Guide | [guide-web-apps.md](guide-web-apps.md) |

## Domain recipes (Phase 26 seal)

| Recipe | Output | Guide |
| --- | --- | --- |
| [cli-sqrt.ssk](../examples/cookbook/cli-sqrt.ssk) | `4.0` | [guide-cli-apps.md](guide-cli-apps.md) |
| [desktop-plan.ssk](../examples/cookbook/desktop-plan.ssk) | JSON capability plan | [guide-desktop-apps.md](guide-desktop-apps.md) |
| [game-input.ssk](../examples/cookbook/game-input.ssk) | `{"any":true,"pressed":{"jump":true}}` | [guide-game-development.md](guide-game-development.md) |
| [research-spark.ssk](../examples/cookbook/research-spark.ssk) | `▁▃▅▆█` | [guide-data-research.md](guide-data-research.md) |
| [ml-dot.ssk](../examples/cookbook/ml-dot.ssk) | `25.0` | [guide-ml.md](guide-ml.md) |
| [functional-call.ssk](../examples/cookbook/functional-call.ssk) | `15` | [guide-functional.md](guide-functional.md) |
| [systems-tier.ssk](../examples/cookbook/systems-tier.ssk) | `surakṣita` | [guide-systems-programming.md](guide-systems-programming.md) |

## Deeper examples (repository)

| Program | Path | Topic |
| --- | --- | --- |
| Functions | [phase6-functions.ssk](../examples/phase6-functions.ssk) | `vidhānam`, `āhvānam`, tracing |
| OOP | [phase7-oop.ssk](../examples/phase7-oop.ssk) | `vargaḥ`, methods |
| Modules | [phase9-modules/](../examples/phase9-modules/) | `kṣetram`, `ānayanam` |
| Stdlib I/O | [phase10-stdlib-cli-io.ssk](../examples/phase10-stdlib-cli-io.ssk) | CLI host calls |
| Functional | [phase8-functional.ssk](../examples/phase8-functional.ssk) | map/filter/fold |

## API documentation demo

[api-demo.ssk](../examples/cookbook/api-demo.ssk) defines `dviguṇa` and `triṣṭaya` for the
`sanskript docs` extractor (names + inferred types). Generated listing:
[generated/cookbook-api-demo.docs.md](generated/cookbook-api-demo.docs.md).

```powershell
python -m sanskript docs examples/cookbook/api-demo.ssk -o docs/generated/cookbook-api-demo.docs.md
```

See [api-from-source.md](api-from-source.md).

## Related docs

- [tutorial-beginner.md](tutorial-beginner.md)
- [tooling.md](tooling.md)
- [phase26-documentation-learning-path.md](phase26-documentation-learning-path.md)
