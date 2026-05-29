# Sanskript Tooling Guide

Command-line tools for the current Python-hosted toolchain. All commands assume:

```powershell
$env:PYTHONPATH='src'
python -m sanskript <command> ...
```

## Core workflow

| Command | Purpose | Example |
| --- | --- | --- |
| `run` | Execute `.ssk`, `.sskbc`, or `.sskyp` | `run examples/cookbook/hello-counter.ssk` |
| `compile` | Source → `.sskbc` bytecode | `compile examples/cookbook/hello-counter.ssk` |
| `disassemble` | Bytecode → `.sskyp` yantra-pāṭha | `disassemble examples/cookbook/hello-counter.sskbc` |
| `assemble` | Yantra-pāṭha → bytecode | `assemble out.sskyp` |
| `lint` | Surface diagnostics | `lint examples/phase12-diagnostics.ssk` |
| `repl` | Interactive sentence loop | `repl` |

## Documentation and packaging

| Command | Purpose |
| --- | --- |
| `docs` | Emit module/function list from a `.ssk` file |
| `web` | Static HTML runner embedding bytecode |
| `install` | Vendor a dependency into `vendor/` (requires `ssk.toml`) |
| `pack` | Zip a source tree or file |

API docs workflow: [api-from-source.md](api-from-source.md).

## Toolchain phases (advanced)

| Command | Phase doc |
| --- | --- |
| `phase17-verify` / `phase17-optimize` / `phase17-link` | [phase17-bytecode-machine-prose.md](phase17-bytecode-machine-prose.md) |
| `phase18-vm-check` | [phase18-vm-runtime-self-hosting.md](phase18-vm-runtime-self-hosting.md) |
| `self-host-check` | [phase19-compiler-self-hosting.md](phase19-compiler-self-hosting.md) |
| `native-build` / `phase20-evidence` | [phase20-native-backends.md](phase20-native-backends.md) |

## Repository maintenance scripts

Generated docs and inventories (run from repo root):

| Script | Output |
| --- | --- |
| `python scripts/export_grammar_register.py` | [grammar-register.generated.md](grammar-register.generated.md) |
| `python tools/generate_feature_matrix.py` | [generated/feature-matrix.md](generated/feature-matrix.md) |
| `python tools/generate_module_inventory.py` | [generated/module-inventory.md](generated/module-inventory.md) |
| `python tools/generate_independence_dashboard.py` | [generated/independence-dashboard.md](generated/independence-dashboard.md) |

Phase 26 tests keep [generated/cookbook-api-demo.docs.md](generated/cookbook-api-demo.docs.md)
in sync with [examples/cookbook/api-demo.ssk](../examples/cookbook/api-demo.ssk).

## Performance and lexicon

| Command / script | Purpose |
| --- | --- |
| `performance` | VM iteration budget smoke test |
| `build-lexicon` | Rebuild controlled lexicon artifact |
| `synthesize` / `analyze` | Grammar-register dev utilities |

## Environment tips (Windows)

- Set `PYTHONPATH=src` in each shell session (or your IDE run config).
- Prefer forward slashes in examples: `examples/cookbook/hello-counter.ssk`.
- Compile output defaults beside the source: `hello-counter.sskbc`.

## Testing your changes

```powershell
python -m unittest discover -s tests
```

Phase 26 documentation tests: `tests/test_phase26_documentation.py`.
Seal evidence: `python -m sanskript phase26-evidence` → `artifacts/phase26/evidence/phase26-evidence.json`.

## Phase 24 developer tools

Full depth table and honesty policy: [phase24-tooling.md](phase24-tooling.md).
`TOOL_CATALOG` in `src/sanskript/phase24_tooling.py` is the machine-readable source
of truth (`PHASE24_SCAFFOLD_TOOL_IDS` is empty after full seal). Run `phase24-check`
or `phase24-spec` for the evidence matrix (`artifacts/phase24/phase24-evidence.json`).

| Command | Depth | Notes |
| --- | --- | --- |
| `format`, `test`, `bench`, `build`, `coverage`, `docs`, `highlight`, `new`, … | functional | See phase24-tooling.md |
| `install`, `pack`, `profile` | partial | Local vendor install; wall-clock opcode estimates |
| `debug` | functional | `TracingVM` breakpoints (`--breakpoints`) and single-step (`--step`) |
| `lsp` | functional | Capabilities JSON (default); `lsp --stdio` JSON-RPC (`initialize`, hover stub) |
| `installer` | functional | Zip bundle + launcher (`installer linux -o path.zip`) — not native MSI/DEB |
| `migrate-python`, `migrate-rust` | functional | Writes `.ssk` skeleton output (`-o` path) |
| `phase24-check`, `phase24-spec` | evidence / spec JSON | Exits non-zero on smoke or anti-fake violations |

```powershell
python -m sanskript.cli debug examples/phase24-tooling.ssk --breakpoints 0
python -m sanskript.cli lsp --stdio
python -m sanskript.cli installer linux -o artifacts/phase24/installer-linux.zip
python -m sanskript.cli migrate-python src/sanskript/vm.py -o out.ssk
python -m sanskript.cli phase24-check --out-dir artifacts/phase24
python -m pytest tests/test_phase24_tooling.py -q
```

## See also

- [tutorial-beginner.md](tutorial-beginner.md)
- [modules-packages.md](modules-packages.md)
- [phase26-documentation-learning-path.md](phase26-documentation-learning-path.md)
