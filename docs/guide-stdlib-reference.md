# Standard Library Reference Guide

The standard library is a large host-backed surface exposed as `āhvānam std.<namespace>.<function> …` calls. This guide is the **entry map**; the exhaustive namespace listing lives in [phase10-standard-library-core.md](phase10-standard-library-core.md).

## How calls reach the VM

1. Parser recognizes `āhvānam` with a dotted native name.
2. Compiler emits `call std.namespace.function`.
3. `SanskriptVM` dispatches through `stdlib_impl.py` (`NativeSpec` arity table).

Errors are always named with the function, e.g. `RuntimeSanskriptError: std.plot.sparkline requires non-empty values`.

## Core namespaces (teaching order)

| Namespace | Typical tasks | Cookbook / example |
| --- | --- | --- |
| `std.math` | `sqrt`, `clamp`, `pow` | [cli-sqrt.ssk](../examples/cookbook/cli-sqrt.ssk) |
| `std.text` / `std.unicode` | string ops, normalization | [phase10-stdlib-formats-patterns.ssk](../examples/phase10-stdlib-formats-patterns.ssk) |
| `std.file` / `std.io` | read/write, lines | [phase10-stdlib-cli-io.ssk](../examples/phase10-stdlib-cli-io.ssk) |
| `std.json` / `std.serialize` | structured data | [web-hello.ssk](../examples/cookbook/web-hello.ssk) (render path) |
| `std.data` / `std.plot` | describe, ASCII/sparkline plots | [research-spark.ssk](../examples/cookbook/research-spark.ssk) |
| `std.web` | route tables, templates | [web-hello.ssk](../examples/cookbook/web-hello.ssk) |
| `std.game` / `std.gui` | simulation plans | [game-input.ssk](../examples/cookbook/game-input.ssk), [desktop-plan.ssk](../examples/cookbook/desktop-plan.ssk) |
| `std.linalg` / `std.ml` | numeric kernels, model pack | [ml-dot.ssk](../examples/cookbook/ml-dot.ssk) |

## Runnable sparkline (data + plot)

```powershell
$env:PYTHONPATH='src'
python -m sanskript run examples/cookbook/research-spark.ssk
```

Expected stdout: `▁▃▅▆█` (Unicode block elements).

## Safety tiers and stdlib

`surakṣitam` / `rakṣitam` / `arakṣitam` at the top of a file gate which natives and memory operations are legal. See [guide-systems-programming.md](guide-systems-programming.md) and [phase14-surakshita-capability.md](phase14-surakshita-capability.md).

## Expanded namespace map

The table below is a **teaching index** — not every native is listed. For the full matrix, see [phase10-standard-library-core.md](phase10-standard-library-core.md) and `python -m sanskript stdlib-spec` when available.

| Namespace | Representative calls | Runnable proof |
| --- | --- | --- |
| `std.math` | `sqrt`, `pow`, `clamp`, `abs` | [cli-sqrt.ssk](../examples/cookbook/cli-sqrt.ssk) |
| `std.text` | `join`, `split`, `trim` | [phase10-stdlib-formats-patterns.ssk](../examples/phase10-stdlib-formats-patterns.ssk) |
| `std.unicode` | `normalize_nfc` | same phase 10 example |
| `std.file` | `read_text`, `write_text`, `exists` | [phase10-stdlib-cli-io.ssk](../examples/phase10-stdlib-cli-io.ssk) |
| `std.io` | `read_line`, `write_line` | phase 10 CLI I/O |
| `std.process` | `run`, `env_get` | [phase10-stdlib-process-testing.ssk](../examples/phase10-stdlib-process-testing.ssk) |
| `std.json` | `parse`, `stringify` | formats example |
| `std.serialize` | `format json` / `format text` | [desktop-plan.ssk](../examples/cookbook/desktop-plan.ssk) |
| `std.data` | `describe`, `column`, `csv_read` | [phase22-research-cli-baseline.ssk](../examples/phase22-research-cli-baseline.ssk) |
| `std.plot` | `sparkline`, `ascii` | [research-spark.ssk](../examples/cookbook/research-spark.ssk) |
| `std.web` | `route_match`, `render` | [web-hello.ssk](../examples/cookbook/web-hello.ssk) |
| `std.gui` | `capabilities_plan`, `simulate` | [desktop-plan.ssk](../examples/cookbook/desktop-plan.ssk) |
| `std.game` | `input_state`, `loop_tick` | [game-input.ssk](../examples/cookbook/game-input.ssk) |
| `std.linalg` | `dot`, `matmul` | [ml-dot.ssk](../examples/cookbook/ml-dot.ssk) |
| `std.ml` | `model_pack`, `model_unpack` | [guide-ml.md](guide-ml.md) |
| `std.async` | `spawn`, `await` | [phase23-concurrency-async.ssk](../examples/phase23-concurrency-async.ssk) |
| `std.http` | `server_route_once` | [phase22-http-service.ssk](../examples/phase22-http-service.ssk) |

## Calling convention in source

Natives use the instrument frame `āhvānam`:

```text
āhvānam std.math.sqrt 16 darśayati.
```

Module paths are dotted; the VM resolves them through `NativeSpec` arity tables in `stdlib_impl.py`. Wrong arity raises a runtime error naming the function.

## Error messages you will see

| Symptom | Typical cause |
| --- | --- |
| `requires non-empty values` | `std.plot.sparkline` given an empty list |
| `unknown native` | typo in `std.*` path or tier forbids the native |
| `RuntimeSanskriptError: std.*` | argument type/shape rejected by host implementation |

Fix the program or consult the phase doc for that namespace before opening a compiler bug.

## Domain guides (stdlib by use case)

| Use case | Guide | Cookbook |
| --- | --- | --- |
| CLI / files | [guide-cli-apps.md](guide-cli-apps.md) | `cli-sqrt.ssk` |
| Web templates | [guide-web-apps.md](guide-web-apps.md) | `web-hello.ssk` |
| Desktop plans | [guide-desktop-apps.md](guide-desktop-apps.md) | `desktop-plan.ssk` |
| Games | [guide-game-development.md](guide-game-development.md) | `game-input.ssk` |
| Research plots | [guide-data-research.md](guide-data-research.md) | `research-spark.ssk` |
| ML numerics | [guide-ml.md](guide-ml.md) | `ml-dot.ssk` |
| Systems tiers | [guide-systems-programming.md](guide-systems-programming.md) | `systems-tier.ssk` |

## Extracting your own API index

For `.ssk` libraries you author, run `sanskript docs` (see [api-from-source.md](api-from-source.md)). That lists `vidhānam` signatures with `param i32` hints and inferred returns — separate from this stdlib host catalog.

## Host boundary (honest)

Most stdlib functions execute in **Python host code** today. They are tested and stable for learning, but independence milestones still track native ports. Do not mark checklist rows “native” until phase tests show host-free proof.

## Related

- [tooling.md](tooling.md) — CLI `run`, `compile`, `lint`
- [api-from-source.md](api-from-source.md) — extract function signatures from `.ssk`
- [phase22-web-apps-games-research-ml.md](phase22-web-apps-games-research-ml.md) — web/game/ML inventory truth
