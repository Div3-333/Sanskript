# Sanskript Bytecode Specification v1

This document defines the portable runtime contract for Sanskript. Any conforming virtual machine must execute programs that validate against this spec. Compilers may target v1 without embedding Python semantics.

## Edition

| Field | Value |
| --- | --- |
| Version | `1` |
| Schema | [`data/bytecode/schema-v1.json`](../data/bytecode/schema-v1.json) |
| Reference VM | `src/sanskript/vm.py` |

## Program model

A **program** is a finite sequence of **instructions** terminated by `halt`. The reference compiler always emits an explicit final `halt`.

### Machine state

| Component | Type | Description |
| --- | --- | --- |
| `stack` | LIFO of integers | Expression and transfer stack |
| `environment` | map name → integer | Named storage (Sanskript nouns as keys) |
| `output` | list of strings | Emitted values, in order |
| `ip` | instruction index | Program counter, 0-based |

Execution starts with `ip = 0`, empty stack, empty environment, and empty output.

### Instruction format

Each instruction is an object:

```json
{ "op": "push_int", "operand": 42 }
```

| Field | Required | Type |
| --- | --- | --- |
| `op` | yes | string opcode name |
| `operand` | depends on opcode | integer, string name, or omitted |

On disk, a program file is:

```json
{
  "version": 1,
  "instructions": [ ... ]
}
```

Sanskript uses `.sskbc` for bytecode files. v1 and v2 share this extension; the JSON `version` field chooses the decoding rules.

## Opcodes (v1)

Stack notation: `before → after` (stack top on the right).

| Opcode | Operand | Stack | Effect |
| --- | --- | --- | --- |
| `push_int` | integer | `… → …, n` | Push constant |
| `load_name` | string | `… → …, v` | Push `environment[name]` or error if unbound |
| `store_name` | string | `…, v → …` | Pop one value into `environment[name]` |
| `add` | — | `…, a, b → …, a+b` | Pop `b`, then `a`; push sum |
| `subtract` | — | `…, a, b → …, a-b` | Pop `b`, then `a`; push difference |
| `emit` | — | `…, v → …` | Pop one value, append `str(v)` to `output` |
| `halt` | — | `… → …` | Stop execution (operand must be absent) |

### Errors (normative)

Implementations must fail with a clear runtime error (not silent corruption) when:

- Stack underflow on any pop
- `load_name` for an unbound name
- Unknown opcode
- Operand type mismatch (e.g. `push_int` without integer operand)

Grammatical hints are encouraged in host implementations but are not part of the on-wire format.

## Static validation

Before execution, conforming toolchains should run `validate_bytecode(program)`:

1. `version` must be `1` when decoding from JSON.
2. Every `op` must be a known v1 opcode.
3. Operand presence and type must match the opcode table.
4. A stack-depth simulation must show no underflow along the linear path (v1 has no branches).
5. The final instruction should be `halt` (warning if missing).

## Conformance

The suite in `tests/test_bytecode_conformance.py` and fixtures under `data/bytecode/conformance/` are the reference behavior. A new VM port passes when:

1. All conformance tests pass against the same JSON fixtures.
2. Round-trip `encode → decode → execute` matches the reference output.

## Versioning

Future versions may add opcodes or optional metadata. Encoders must set `version` explicitly; decoders must reject unknown major versions.
