# Sanskript Bytecode Specification v2

Bytecode v2 extends [v1](bytecode-v1.md) with arithmetic, comparisons, control flow, function calls, and function parameters. v1 programs remain valid; decoders accept `version: 1` or `version: 2`.

## Edition

| Field | Value |
| --- | --- |
| Version | `2` |
| Schema | [`data/bytecode/schema-v2.json`](../data/bytecode/schema-v2.json) |
| Reference VM (Python) | `src/sanskript/vm.py` |
| Reference VM (Rust) | `ssk-vm/` (`cargo test` / `ssk-vm <fixture.json>`) |
| Encoder | `encode_program(..., version=2)` in `src/sanskript/bytecode.py` |

## Toolchain workflow

The canonical bytecode file extension is `.sskbc`. The file is plain UTF-8 JSON using the same object shape described below.

The human-readable machine text extension is `.sskyp` ("Sanskript yantra-pāṭha"). It is a reversible Sanskrit-prose assembly form for the same bytecode program. It exists so the lower toolchain does not have to expose C/Python-style operators, braces, labels, or instruction mnemonics as the only readable machine form.

```powershell
$env:PYTHONPATH='src'; python -m sanskript compile examples/caturtha.ssk
$env:PYTHONPATH='src'; python -m sanskript run examples/caturtha.sskbc
$env:PYTHONPATH='src'; python -m sanskript disassemble examples/caturtha.sskbc
$env:PYTHONPATH='src'; python -m sanskript run examples/caturtha.sskyp
$env:PYTHONPATH='src'; python -m sanskript web examples/caturtha.ssk -o C:\tmp\sanskript-app.html
```

`sanskript compile input.ssk` writes `input.sskbc` unless `-o/--output` is supplied. The compiler validates the bytecode before writing. `sanskript run` accepts either `.ssk` source or `.sskbc` bytecode; `.sskbc` execution loads JSON bytecode directly and skips morphology/parser compilation.

`sanskript disassemble input.sskbc` writes `input.sskyp`. `sanskript assemble input.sskyp` writes `input.sskbc`. `.sskyp` files can also be run directly; the CLI assembles the prose form into bytecode in memory and then executes the VM.

`sanskript web input.ssk` writes a static HTML app that embeds the compiled bytecode and runs it in a browser VM. This is the first web target: it renders program output, and later DOM/event APIs can be exposed as Sanskript standard-library surfaces.

Example yantra-pāṭha:

```text
saṃskaraṇam dvitīyam.
mukhyaḥ pāṭhaḥ ārabhyate.
pañca iti pūrṇāṅkaḥ nikṣipyate.
phala iti nāma sthāpyate.
phala iti nāma āhriyate.
darśanam kriyate.
virāmaḥ kriyate.
pāṭhaḥ samāpyate.
```

## Program model

A v2 **program** has:

| Field | Type | Description |
| --- | --- | --- |
| `instructions` | instruction[] | Main entry stream, ends with `halt` |
| `functions` | function[] | Optional top-level procedures |
| `modules` | module[] | Optional grouped procedures |

```json
{
  "version": 2,
  "instructions": [ ... ],
  "functions": [
    { "name": "sthāpaya", "params": ["mūlya"], "instructions": [ ... ] }
  ],
  "modules": [
    {
      "name": "gaṇita",
      "functions": [
        { "name": "gaṇita.vṛddhi", "instructions": [ ... ] }
      ]
    }
  ]
}
```

Function bodies end with `return` (not `halt`). `call` transfers control to a named target; `return` resumes the caller at the instruction after `call` and pushes the popped return value.

Function objects may include `params`, a list of parameter names. The compiler lowers call arguments before `call`; the VM pops the argument values, binds them to the callee's parameters as local values, and restores the caller's locals on `return`.

The yantra-pāṭha renderer expresses the same operations as formal prose sentences, for example `phala iti nāma āhriyate.` for `load_name`, `sapta iti pūrṇāṅkaḥ nikṣipyate.` for `push_int 7`, and `gaṇita iti kṣetre vṛddhi iti vidhānam āhūyate.` for `call gaṇita.vṛddhi`.

### Calling convention (reference VM)

- `call` takes a name operand: bare name for top-level functions, or `module.function` for module procedures.
- Call arguments are ordinary stack values pushed immediately before `call`.
- Functions bind arguments to local parameter names; `load_name` reads locals then globals.
- `store_name` updates a local only when the local already exists, otherwise it writes globals. This preserves procedure-style global mutation while allowing parameter rebinding inside a function.
- After `call`, the compiler emits `pop` to discard the default `0` return value when the result is unused.

## New opcodes (v2)

| Opcode | Operand | Stack | Effect |
| --- | --- | --- | --- |
| `multiply` | — | `…, a, b → …, a*b` | Integer multiply |
| `divide` | — | `…, a, b → …, a//b` | Integer divide; divide-by-zero is a runtime error |
| `compare_eq` | — | `…, a, b → …, 0\|1` | Push `1` if equal else `0` |
| `compare_lt` | — | `…, a, b → …, 0\|1` | Push `1` if `a < b` else `0` |
| `jump` | label (int) | `… → …` | Set `ip` to operand index |
| `jump_if_zero` | label (int) | `…, v → …` | Pop `v`; jump if `v == 0` |
| `call` | name (string) | `…, arg₁, …, argₙ → …` | Bind params and enter function body at `ip = 0` |
| `return` | — | `…, v → …` | Pop return value; resume caller |
| `pop` | — | `…, v → …` | Discard stack top |

v1 opcodes (`push_int`, `load_name`, `store_name`, `add`, `subtract`, `emit`, `halt`) are unchanged.

## Static validation

- Main stream must end with `halt`.
- Function bodies must end with `return` or `halt`.
- Jump targets must be in-range indices for their instruction stream.
- When control-flow opcodes are present, linear stack-depth checking is relaxed for that stream (jumps are not fully verified).

## Source directives (parser)

| Marker | Role |
| --- | --- |
| `yadi … samam …` | Conditional; optional `anyathā` else branch |
| `punaḥ … samam …` | While loop |
| `antam` | Ends the current `yadi` / `punaḥ` block |
| `vidhānam` / `samāpanam` | Procedure start / end |
| `kṣetram` | Module scope |
| `āhvānam` | Call (`āhvānam name`, `āhvānam name arg`, or `āhvānam module name arg`) |
| `pratyāvartanam` | Return from a function |

Function parameters remain prose tokens in the function header:

```text
vidhānam sthāpaya balaṃ.
gaṇakaḥ balaṃ phale nidadhāti.
samāpanam.
āhvānam sthāpaya pañca.
```

## Conformance

Golden fixtures under `data/bytecode/conformance/` target v1. v2 behavior is covered by `tests/test_control_flow.py`, `tests/test_functions.py`, and compiler round-trip tests.
