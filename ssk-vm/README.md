# ssk-vm

Portable Sanskript bytecode virtual machine (Rust). Implements [bytecode v1](../docs/bytecode-v1.md) and [bytecode v2](../docs/bytecode-v2.md).

## Build and test

```bash
cd ssk-vm
cargo test
```

Conformance fixtures live in `../data/bytecode/conformance/`. The integration test `tests/conformance.rs` runs every `*.json` file against the same contract as Python's `tests/test_bytecode_conformance.py`.

## Run a program file

```bash
cargo build
./target/debug/ssk-vm ../data/bytecode/conformance/assign_increment_emit.json
```

When the JSON includes `expected_output`, the binary validates output and `expected_environment` before printing.

## Python bridge

`tests/test_rust_vm.py` runs `cargo test` when `cargo` is on `PATH` (skipped otherwise).
