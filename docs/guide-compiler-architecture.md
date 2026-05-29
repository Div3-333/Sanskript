# Compiler Architecture Guide

The Sanskript compiler is a multi-pass pipeline from **normalized Sanskrit source** to **bytecode v2**, with static checking before code generation. Today the driver is Python (`src/sanskript/compiler.py`); Phase 19 tracks self-hosting with honest S0 host-replay gates.

## Pipeline overview

```mermaid
flowchart LR
  A[source_pipeline] --> B[parser]
  B --> C[AST Program]
  C --> D[type_checker]
  D --> E[compiler IR]
  E --> F[bytecode v2]
  F --> G[vm / tools]
```

| Stage | Module | Output |
| --- | --- | --- |
| Normalize | `source_pipeline.py`, `script_normalize.py` | UTF-8 text + spans |
| Parse | `parser.py`, `parser_core.py` | `Program` AST |
| Check | `type_checker.py` | diagnostics or proceed |
| Lower | `compiler.py`, `ir.py` | `BytecodeProgram` |
| Package | `module_loader.py`, `package_resolver.py` | merged units |

## Runnable end-to-end proof

Any cookbook file exercises compile + run. Example:

```powershell
$env:PYTHONPATH='src'
python -m sanskript compile examples/cookbook/hello-counter.ssk
python -m sanskript run examples/cookbook/hello-counter.ssk
```

`compile` writes `.sskbc` beside the source; inspect JSON to see opcodes and constants.

## Self-hosting status (honest)

[phase19-compiler-self-hosting.md](phase19-compiler-self-hosting.md) documents S0 bootstrap: the compiler can replay its own bytecode evidence through the VM, but **logic still executes on the host**. Do not describe the toolchain as Sanskript-native until Phase 27+ migration rows close.

## Morphology and grammar coupling

Parsing consults `morphology_facade.py` and the controlled lexicon. Compiler errors with `SANSKRIPT_MORPHOLOGY` originate here — fix data/register, not bytecode.

## Related

- [guide-vm-architecture.md](guide-vm-architecture.md) — execution side
- [guide-machine-programming.md](guide-machine-programming.md) — `.sskyp` conformance
- [implementation-plan.md](implementation-plan.md) — milestone context
