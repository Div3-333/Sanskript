# Phase 15: Rakṣita Systems Capability

Phase 15 hardens Sanskript's `rakṣita` tier for systems work with explicit ownership discipline, unsafe proofs, deterministic resource handling, and baseline sync/FFI/net APIs.

## Enforcement Model

- Ownership/move/borrow/lifetime checks remain static in `type_checker.py`.
- `rakṣita` unsafe regions now require a proof annotation:
  - `arakṣitaḥ adhikāraḥ ārabhyate pramāṇam vākyam <proof> iti.`
  - Trailing text without `pramāṇam` does not count as proof and is rejected by rakṣita checks.
- Heap instructions remain blocked outside unsafe regions in `rakṣita`.
- Panic vs recoverable errors stay split:
  - `vipattim` -> `PanicError` (unrecoverable)
  - `vikṣepaḥ` -> `ThrownError` (recoverable via `āgrahītvā`)

## New Standard-Library Systems Primitives

### Thread-Safety Markers

- `std.thread.marker.send`
- `std.thread.marker.share`

Both validate send/share safety for nested values. Mutable bytearrays and unsupported opaque handles are rejected.

### Atomics / Locks / Channels

- `std.sync.atomic.new/load/store/fetch_add/compare_exchange`
- `std.sync.lock.new/acquire/release`
- `std.sync.channel.new/send/recv/try_recv`

Channels reject non-send-safe payloads.

### Safe FFI Boundary

- `std.ffi.call_checked(symbol, args)`
- `std.ffi.abi_stable_struct(schema)`

`call_checked` is allowlist-based and arity-checked. `abi_stable_struct` validates deterministic field layout/offsets and supported ABI scalar types.
Additionally:
- `call_checked` rejects non-ABI-safe arguments (opaque handles, mutable buffers, and nested unsafe payloads).
- `abi_stable_struct` rejects duplicate field names, non-integer offsets, and optional `size` mismatches.

### Network / Filesystem Baseline

- Filesystem baseline remains from Phase 10 (`std.file.*`, `std.path.*`).
- Network baseline in Phase 15:
  - `std.net.resolve_host`
  - `std.net.tcp_probe`

## Migration Notes

- Existing `rakṣita` programs must add proof text on `unsafe_enter`.
- Cross-thread or channel payloads may need conversion to send-safe forms.
- FFI calls should migrate to explicit allowlisted symbols and ABI-checked structs.
