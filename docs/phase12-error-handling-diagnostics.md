# Phase 12: Error Handling And Diagnostics

Phase 12 uses a tiered error model:

- recoverable thrown errors (`ThrownError`, `SANSKRIPT_THROW`)
- unrecoverable panics (`PanicError`, `SANSKRIPT_PANIC`)
- typed domain diagnostics (`MorphologyError`, `ParseError`, `TypeCheckError`,
  `RuntimeSanskriptError`)

## User-facing diagnostics

- Every `SanskriptError` carries:
  - stable code (`SANSKRIPT_*`)
  - optional source span/script provenance
  - contextual notes and VM stack trace
  - fix guidance (`hint` + `fixes`/`suggestions`)
  - machine fields (`category`, `recoverable`)
- CLI output supports:
  - `--diagnostics-format text` (default human-readable)
  - `--diagnostics-format json` (machine-readable payload with
    `category`, `recoverable`, `notes`, `fixes`, `suggestions`, `stack_trace`)
  - `--diagnostics-format ide` (LSP-style diagnostic shape with rich `data`)
- Crash reports:
  - `--crash-report path.json` writes uncaught exception payloads with timestamp,
    exception type, message, and traceback.

## Warnings and lint levels

- `sanskript lint <file.ssk>` emits lint diagnostics.
- `--lint-level warning|error` controls severity policy.
- `sanskript compile/run --lint-level ...` can enforce lint gates before execution.
- Lint diagnostics are categorized as `lint.<rule>` (for example,
  `lint.choppy_sentence`) for machine filtering/snapshot tests.

## Rakṣita / Arakṣita diagnostics

- Borrow/lifetime violations are surfaced as typed `TypeCheckError`s with
  actionable hints.
- Pointer-safety and unsafe-tier misuse are surfaced as typed `TypeCheckError`s
  (compile-time) and `RuntimeSanskriptError`s (runtime guardrails).
- Optional VM debug assertions are enabled with `SANSKRIPT_DEBUG_ASSERT=1` and
  fail as `PanicError` on invariant breakage.

## Migration notes (Python/Rust to Sanskript diagnostics)

- Python exceptions that should be recoverable map to `vikṣepaḥ`/`ThrownError`
  and `āgrahītvā` handling blocks.
- Rust `Result`/`panic!` split maps directly to recoverable `ThrownError` vs
  unrecoverable `PanicError`.
- Tooling integrations should consume `--diagnostics-format json` for CI and
  `--diagnostics-format ide` for editor diagnostics.
