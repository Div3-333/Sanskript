# Beginner Tutorial

This tutorial walks from zero to a running program in grammatical Sanskript prose.
For a visual companion, open [guide/index.html](guide/index.html).

## What you are writing

Sanskript programs are **sentences**, not brace blocks. Each statement is a complete
vākya ending with `.` or danda `।`. Verbs such as `nidadhāti` (place), `vardhayati`
(increase), and `darśayati` (display) carry the computation; case endings mark roles
(karma, karaṇa, adhikaraṇa).

## Prerequisites

- Python 3.11+ with the repo on `PYTHONPATH`
- A terminal in the repository root

```powershell
$env:PYTHONPATH='src'
```

## Step 1 — Run the smallest program

Create or open `examples/cookbook/hello-counter.ssk`:

```text
gaṇakaḥ pañca phale nidadhāti.
gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
gaṇakaḥ phalaṃ darśayati.
```

Run it:

```powershell
python -m sanskript run examples/cookbook/hello-counter.ssk
```

Expected output:

```text
7
```

Reading the three lines:

1. The calculator (`gaṇakaḥ`) places five (`pañca`) in the result (`phale`).
2. It increases the result by two (`dvābhyāṃ`).
3. It displays the result.

## Step 2 — Bind a different name

The same pattern works with `mūlya` (value) instead of `phala` (result). See
[examples/cookbook/scaled-sum.ssk](../examples/cookbook/scaled-sum.ssk) — output is
still `7` (three plus four).

## Step 3 — Add a branch

When the stored value equals three, multiply by ten; otherwise add one. See
[examples/cookbook/conditional-branch.ssk](../examples/cookbook/conditional-branch.ssk)
(output `13`). Syntax reference: [control-flow.md](control-flow.md).

## Step 4 — Text without quotes

```text
vākyam svāgatam mitra iti phale nidadhāti.
gaṇakaḥ phalaṃ darśayati.
```

Run [examples/cookbook/greet.ssk](../examples/cookbook/greet.ssk) — output
`svāgatam mitra`. The quotative particle `iti` marks a text literal.

## Step 5 — Compile once, run bytecode

```powershell
python -m sanskript compile examples/cookbook/hello-counter.ssk
python -m sanskript run examples/cookbook/hello-counter.sskbc
```

Bytecode is portable JSON (`.sskbc`). Machine prose (`.sskyp`) is documented in
[phase17-bytecode-machine-prose.md](phase17-bytecode-machine-prose.md).

## Next steps

| Topic | Document |
| --- | --- |
| Syntax tables | [core-syntax.md](core-syntax.md) |
| Types | [type-system-reference.md](type-system-reference.md) |
| Functions | [functions-procedures.md](functions-procedures.md) |
| More complete programs | [cookbook.md](cookbook.md) |
| From Python or Rust | [migration-from-python.md](migration-from-python.md), [migration-from-rust.md](migration-from-rust.md) |
| CLI commands | [tooling.md](tooling.md) |
| Full learning inventory | [phase26-documentation-learning-path.md](phase26-documentation-learning-path.md) |
