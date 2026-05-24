# Sanskript Bytecode Specification v2

Bytecode v2 extends [v1](bytecode-v1.md) with arithmetic, comparisons, control flow, and procedure calls. v1 programs remain valid; decoders accept `version: 1` or `version: 2`.

## Edition

| Field | Value |
| --- | --- |
| Version | `2` |
| Schema | [`data/bytecode/schema-v2.json`](../data/bytecode/schema-v2.json) |
| Reference VM (Python) | `src/sanskript/vm.py` |
| Reference VM (Rust) | `ssk-vm/` (`cargo test` / `ssk-vm <fixture.json>`) |
| Encoder | `encode_program(..., version=2)` in `src/sanskript/bytecode.py` |

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
    { "name": "vṛddhi", "instructions": [ ... ] }
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

### Calling convention (reference VM)

- `call` takes a name operand: bare name for top-level functions, or `module.function` for module procedures.
- Procedures share the **global** environment: `store_name` always writes globals; `load_name` reads locals then globals.
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
| `call` | name (string) | `… → …` | Enter function body at `ip = 0` |
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
| `āhvānam` | Call (`āhvānam name` or `āhvānam module name`) |

## Conformance

Golden fixtures under `data/bytecode/conformance/` target v1. v2 behavior is covered by `tests/test_control_flow.py`, `tests/test_functions.py`, and compiler round-trip tests.
