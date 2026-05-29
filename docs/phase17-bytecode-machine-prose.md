# Phase 17: Bytecode And Machine Prose

Phase 17 defines the frozen bytecode + machine-prose toolchain contract for Sanskript bytecode v2 and `.sskyp`.

## Frozen specification

- Spec entrypoint: `sanskript phase17-spec`
- Version: `17.0.0`
- Canonical file formats:
  - `.sskbc` JSON bytecode
  - `.sskyp` Sanskrit machine-prose assembly
  - `.sskypb` binary container (`SSKYP17\0` + length + sha256 + canonical JSON payload)
- Frozen metadata/layout contract includes:
  - stack and call-frame layout
  - constant/symbol/debug/exception/ownership table layout
  - function/module/type/object layout metadata

## Toolchain components

Implemented in `src/sanskript/phase17_toolchain.py`:

- verifier: `verify_program_phase17`
- optimizer: `optimize_program_phase17`
- linker: `link_programs_phase17`
- loader: `load_program_any`
- serializer/deserializer:
  - `serialize_canonical_json` / `deserialize_canonical_json`
  - `serialize_binary` / `deserialize_binary`
- assembler/disassembler:
  - `assemble` / `disassemble`
  - `parse_machine_prose` / `render_machine_prose`

## Strict opcode <-> machine-prose parity

- `opcode_machine_prose_evidence` records:
  - `mapped`: opcodes with a proven bijective prose sentence,
  - `unsupported`: opcodes not currently representable in canonical prose, with failure reason.
- For each mapped opcode, the gate enforces:
  - rendering round-trips to the exact original instruction (opcode + operand),
  - no two opcodes share the same prose sentence.

This gate is executed inside `verify_program_phase17`.

## Conformance round-trip

`roundtrip_conformance` enforces payload equality through:

1. bytecode object -> canonical JSON -> bytecode object
2. bytecode object -> `.sskyp` -> bytecode object
3. bytecode object -> `.sskypb` -> bytecode object

The check fails if any stage changes the program payload, even when structurally valid.

## CLI workflow

- Verify and round-trip check:
  - `sanskript phase17-verify path/to/program.sskbc`
  - `sanskript phase17-verify path/to/program.sskyp`
  - `sanskript phase17-verify path/to/program.sskypb`
- Optimize:
  - `sanskript phase17-optimize in.sskbc -o out.sskyp`
- Link:
  - `sanskript phase17-link a.sskbc b.sskyp -o linked.sskypb`

## Example

- `examples/phase17-bytecode-toolchain.sskyp` demonstrates a hand-authored machine-prose program and function.

## Migration notes

| Host bytecode task | Phase 17 Sanskript toolchain API |
|---|---|
| JSON dump/load helpers | `serialize_canonical_json`, `deserialize_canonical_json` |
| ad-hoc binary wrapper | `serialize_binary`, `deserialize_binary` |
| custom text assembler | `assemble`, `parse_machine_prose` |
| disassembly printer | `disassemble`, `render_machine_prose` |
| ad-hoc integrity checks | `verify_program_phase17`, `roundtrip_conformance` |
| manual merge scripts | `link_programs_phase17` |
