# Phase 16: Arakshita Machine-Level Capability

Phase 16 extends Sanskript bytecode/VM with machine-facing operations while keeping
execution semantics explicit and testable.

## Implemented Opcode Surface

- Raw address/pointer operations: `ptr_from_int`, `ptr_to_int`, `ptr_add`, `ptr_sub`
- Width + endian memory operations:
  - loads: `load_u8`, `load_u16_le`, `load_u16_be`, `load_u32_le`, `load_u32_be`
  - stores: `store_u8`, `store_u16_le`, `store_u16_be`, `store_u32_le`, `store_u32_be`
  - volatile: `volatile_load_u32_le`, `volatile_store_u32_le`
- Bit-level arithmetic:
  - `bit_and`, `bit_or`, `bit_xor`, `bit_not`
  - `shift_left`, `shift_right`, `rotate_left32`, `rotate_right32`
- Register/stack-frame concepts:
  - `reg_set`, `reg_get`, `sp_set`, `sp_get`, `fp_set`, `fp_get`
  - `call_conv`, `prologue`, `epilogue`
- Machine prose and control:
  - `inline_asm`, `label`, `jump_label`, `jump_if_zero_label`, `jump_indirect`
  - `call` (direct), `call_indirect` (indirect)
- System/IO/memory model:
  - `syscall`, `trap`, `mmio_read`, `mmio_write`
  - `atomic_cas_u32_le`, `fence`

Host-runtime caveat:

- `syscall` is intentionally rejected by the current host VM backend
  (`RuntimeSanskriptError`) and must be lowered through native backend paths for
  platform execution. This is a deliberate bootstrap boundary, not silent
  machine-level support in the host runtime.
- `inline_asm`, `prologue`, `epilogue`, and `fence` are represented and
  executable in the VM surface; they are semantic placeholders in the host VM
  and do not claim host CPU-level side effects.

## Object/Linking Scaffolding

Native backend planning now emits:

- object stub (`program.<fmt>.o`)
- symbol table (`symbols.json`)
- relocation table (`relocations.json`)
- linker IO manifest (`linker-io.json`)
- debug symbols (`debug-symbols.json`)
- stack map (`stack-map.json`)

This is intentionally scaffold-level, but machine-readable and executable through
`sanskript native-build`.

## Disassembly / Assembly

- `sanskript disassemble program.sskbc` renders `.sskyp` machine prose.
- `sanskript assemble program.sskyp` assembles it back into `.sskbc`.
- Phase 16 opcodes are included in the `.sskyp` renderer/parser path.

## Validation

See `tests/test_phase16_arakshita.py` for:

- runtime VM semantics over machine-level opcodes,
- `.sskyp` round-trip for Phase 16 instructions,
- native artifact scaffold emission checks,
- tier boundary tests (`surakshita`/`rakshita`/`arakshita`) and explicit host
  syscall rejection coverage.

Reference example:

- `examples/phase16-arakshita-machine-level.sskyp` demonstrates canonical
  machine-prose usage for pointer/memory/register/label paths with explicit
  arakṣita tier declaration.
