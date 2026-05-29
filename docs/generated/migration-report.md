# Phase 27 Migration Report

_Generated at 2026-05-29T05:07:35+00:00 by `phase27_migration_report`._

**Seal status:** `full_seal` (honest tracking: **True**, full seal: **True**).

## Summary

- Python files remaining: **257**
- Rust files remaining: **5**
- Average native replacement: **5.79%**

## Port blockers

- 257 Python modules still implement host logic (see remaining_files.python).
- 5 Rust modules remain for conformance/reference (see remaining_files.rust).
- Phase 27 checklist is open: no compiler/parser/VM/CLI component is natively ported end-to-end.
- SanskriptPortedVM (Phase 18) is a host-dispatched facade; independent_vm=False.
- module_inventory migration_label=port_directly must not be read as already ported.
- known_host_dependency:python_ast -> src/sanskript/ast.py
- known_host_dependency:python_bytecode -> src/sanskript/bytecode.py
- known_host_dependency:python_cli -> src/sanskript/cli.py
- known_host_dependency:python_compiler -> src/sanskript/compiler.py
- known_host_dependency:python_parser -> src/sanskript/parser.py
- known_host_dependency:python_vm -> src/sanskript/vm.py
- known_host_dependency:rust_vm_crate -> ssk-vm/Cargo.toml
- in_progress:grammar_loaders (27.0% via Sanskript .sskbc; host modules remain)
- in_progress:sutra_registry (27.0% via Sanskript .sskbc; host modules remain)
- extraction_boundary:vm (2.0% native; host still runs logic)
- in_progress:examples_runner (27.0% via Sanskript .sskbc; host modules remain)
- in_progress:test_harness (27.0% via Sanskript .sskbc; host modules remain)

## Components

| Component | Status | % native | Host impl |
| --- | --- | ---: | --- |
| Grammar data loaders | in_progress | 27.0 | python |
| Sutra registry | in_progress | 27.0 | python |
| Sutra predicate engine | host_only | 0.0 | python |
| Derivational engines | host_only | 0.0 | python |
| Morphology helpers | host_only | 0.0 | python |
| Source tokenizer | host_only | 0.0 | python |
| Parser | host_only | 0.0 | python |
| AST model | host_only | 0.0 | python |
| Compiler | host_only | 0.0 | python |
| Bytecode schema | host_only | 0.0 | python |
| VM | extraction_boundary | 2.0 | mixed |
| .sskyp assembler/disassembler | host_only | 0.0 | python |
| CLI | host_only | 0.0 | python |
| Docs generator | host_only | 0.0 | python |
| Examples runner | in_progress | 27.0 | python |
| Test harness | in_progress | 27.0 | python |
| Web playground core | host_only | 0.0 | python |
| Browser runtime core | host_only | 0.0 | none |
| Build/release scripts | host_only | 0.0 | python |

## Refresh

```powershell
$env:PYTHONPATH='src'
python -m sanskript.cli migration-report
```
