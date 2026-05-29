# Phase 13: Memory Model By Tier

Phase 13 establishes enforceable memory semantics across `surakṣita`, `rakṣita`, and `arakṣita` instead of declaration-only vocabulary.

## Enforcement surfaces

- Static ownership / borrow / lifetime checks: `src/sanskript/type_checker.py`.
- Unsafe-entry proof requirement in `rakṣita`: `src/sanskript/type_checker.py`.
- Runtime unsafe scope and heap gating by tier: `src/sanskript/vm.py`.
- Runtime layout/allocation/aliasing/move/clone/drop semantics: `src/sanskript/stdlib_impl.py` under `std.memory.*`.
- Atomic and fence semantics: `std.memory.atomic.*` and `std.sync.atomic.*`.

## Tier semantics

- `surakṣita`: direct heap opcodes are rejected by VM.
- `rakṣita`: heap/pointer opcodes require `unsafe_enter`/`unsafe_exit`; static checker enforces ownership+borrow+lifetime rules.
- `arakṣita`: full low-level memory opcodes and direct pointer-style access are permitted.
- Tier crossing is explicit: only dotted native calls and compiled bytecode transitions are allowed; unsafe blocks must be explicit and balanced.

## Memory vocabulary and runtime entities

- **Value/object/reference**: language-level runtime values and record instances.
- **Address/pointer**: integer-addressed byte locations in VM heap operations.
- **Handle**: `OpaqueHandle` for memory blocks, references, borrows, atomics, locks, channels.
- **Region/lifetime**: declared with `āyuḥ`; borrow/use checks bind borrows to owner lifetime/region.

## Layout and allocation semantics

`std.memory.alloc.heap|stack|arena(size, alignment, layout, packed, abi, region)`:

- Enforces non-negative size.
- Enforces power-of-two alignment.
- Enforces packed-layout constraint (`packed => alignment=1` and `layout=packed`).
- Stores ABI/layout metadata for introspection (`std.memory.layout.describe`).
- Enforces ABI/layout compatibility (`abi` layout accepts only ABI names, `repr-c` only `c|native`, native/packed only `native`).
- Supports explicit allocator and region tags for auditability.

## Ownership, copy/move/clone/drop/finalization semantics

- `std.memory.copy`/`std.memory.clone` produce distinct owned blocks.
- `std.memory.move` invalidates source ownership and transfers data to a new owner handle.
- `std.memory.drop` and `std.memory.dealloc` deterministically invalidate memory.
- Access after move/drop raises runtime errors.
- Class-instance finalization guard remains enforced in VM object dispatch.

## Borrow, aliasing, and lifetime semantics

- `std.memory.borrow.shared` allows multiple readers but blocks mutable borrow.
- `std.memory.borrow.mut` requires uniqueness (no active shared/mut borrow).
- `std.memory.borrow.release` decrements borrow state.
- Mutation/deallocation during active borrows fails.
- `std.memory.alias.state` reports active borrow aliases and atomic-marked locations.
- Static lifetime checks reject undeclared lifetimes and owner/borrow lifetime mismatch.

## Unsafe and low-level semantics

- `rakṣita` unsafe blocks require proof text and must balance enter/exit.
- Heap operations in `rakṣita` fail outside unsafe regions.
- `arakṣita` low-level load/store/volatile/atomic/fence opcodes remain VM-enforced.
- Raw pointer opcodes (`ptr_from_int`, etc.) remain arakṣita-only VM operations.
- Volatile references are explicit: `std.memory.volatile.ref` must be used with `std.memory.volatile.load_u8` / `std.memory.volatile.store_u8`.

## Atomic and fence semantics

- `std.memory.atomic.new/load/store/fetch_add/compare_exchange` provide explicit atomic state transitions.
- `std.memory.atomic.ref(ref)` binds an atomic handle to a memory location.
- Once bound as atomic, non-atomic `std.memory.load_u8` / `std.memory.store_u8` on that location are rejected to prevent mixed-access races.
- `std.memory.atomic.fence(order)` validates memory-order vocabulary (`acquire`, `release`, `acq_rel`, `seq_cst`) and records monotonic fence sequence.

## Migration notes

- Existing `std.sync.atomic.*` calls continue to work; `std.memory.atomic.*` is Phase 13 memory-model vocabulary.
- Replace ad hoc ownership comments with explicit `owned`/`borrow`/`borrow_mut` bindings and lifetime declarations.
- Prefer `std.memory.layout.describe` for ABI/layout diagnostics instead of host-side assumptions.
