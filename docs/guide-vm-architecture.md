# VM Architecture Guide

The Sanskript VM (`src/sanskript/vm.py`) executes bytecode v2 programs: stack operations, calls, natives, tier checks, and tracing hooks. Phase 18 documents bootstrap/self-host evidence; execution remains **host-Python-backed** until native runtimes pass independence milestones.

## Execution model

1. Loader reads `.sskbc` or in-memory `BytecodeProgram`.
2. Interpreter loop dispatches opcodes.
3. `CALL` to dotted names resolves via `stdlib_impl.py` when `has_native_function`.
4. `darśayati` lowers to stdout writes of stringified values.

## Runnable proof

```powershell
$env:PYTHONPATH='src'
python -m sanskript run examples/cookbook/hello-counter.ssk
```

Under the hood: `compile_source` → `check_program` → `SanskriptVM().execute(...)`. Tests in `tests/test_phase26_documentation.py` pin expected stdout tuples for every cookbook recipe.

## Bootstrap artifact

[phase18-vm-bootstrap.sskbc](../examples/phase18-vm-bootstrap.sskbc) is evidence output for self-host replay — consult [phase18-vm-runtime-self-hosting.md](phase18-vm-runtime-self-hosting.md) for gate definitions (`independent_vm_runtime=false` until stated otherwise in milestone JSON).

## Safety tiers at runtime

VM enforces `surakṣita` / `rakṣita` / `arakṣita` policies coordinated with `type_checker.py` and stdlib registration. Smoke:

```powershell
python -m sanskript run examples/cookbook/systems-tier.ssk
```

Prints `surakṣita`.

## Rust conformance VM

`ssk-vm` (Rust) provides additional conformance testing; it is not the default `sanskript run` path. See phase 20 native backend docs.

## Related

- [bytecode-v2.md](bytecode-v2.md)
- [guide-compiler-architecture.md](guide-compiler-architecture.md)
- [phase18-vm-runtime-self-hosting.md](phase18-vm-runtime-self-hosting.md) — bootstrap evidence
