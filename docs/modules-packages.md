# Modules, Packages, And Namespaces (Phase 9)

Sanskript programs scale across files using Sanskrit prose import directives,
package manifests, lockfiles, and namespace-aware resolution.

## Module files and `kṣetram`

Each `.ssk` file may declare one or more modules:

```
kṣetram gaṇita.
vidhānam vṛddhi.
gaṇakaḥ daśa phale nidadhāti.
gaṇakaḥ phalaṃ ekena vardhayati.
samāpanam.
niḥsāram vṛddhi.
samāpanam.
```

**Python equivalent:** a module with one public function.

## Imports

| Form | Meaning |
|------|---------|
| `ānayanam gaṇita.` | Import module by path or name |
| `ānayanam gaṇita nāmnā m.` | Import with alias |
| `ānayanam gaṇita antaḥ vṛddhi nāmnā v.` | Selective import |
| `ānayanam ./sahodara.` | Relative import |
| `ānayanam @lib/upakaraṇa.` | Absolute import from project `lib/` |
| `ānayanam @stdlib/prathama.` | Standard-library namespace |
| `ānayanam serde viśeṣe json.` | Feature-gated import |

## Re-exports

```
punaranayanam gaṇita antaḥ vṛddhi.
niḥsāram vṛddhi.
```

Re-exports surface a symbol from another loaded module through the current export
list (`niḥsāram`).

## Package directories and initialization

A package directory may contain `samārambha.ssk` or `__init__.ssk`. When any file
inside the package is imported, initialization modules load first.

## Manifest (`ssk.toml`)

```toml
[package]
name = "demo"
version = "1.0.0"
signature = "<hmac-sha256 digest>"

[features]
json = true

[dependencies.local]
helper = { path = "lib/helper" }

[dependencies.registry]
serde = { version = "0.1.0", registry = "ssk" }

[dependencies.vendored]
legacy = { path = "vendor/legacy", locked = true }

[profile.release]
requires = "json"

[platform.windows]
extra = "win_extra.ssk"

[namespace]
stdlib = "stdlib"
user = "lib"
```

## Sanskrit prose manifest (`saṃskaraṇa.sskm`)

```
pūtikā saṃskaraṇam demo.
saṃskaraṇa-avāntara 1.0.0.
āśraya panthanāt ./lib/helper.
āśraya sañcikāyāḥ serde 0.1.0.
viśeṣa json sat.
```

## Lockfile (`ssk.lock`)

The lockfile pins resolved dependency paths and `sha256` hashes. The loader
rejects tampered vendored trees when hashes diverge.

## Package signing

Set `SANSKRIPT_SIGNING_KEY` and record `signature` in the manifest. The loader
calls `verify_package_signature` before resolving dependencies.

## Dependency kinds

| Kind | Resolution |
|------|------------|
| Local path | `[dependencies.local]` or `āśraya panthanāt` |
| Registry | `.ssk/registry/<name>/<version>` or vendored fallback |
| Vendored | `vendor/<name>` with optional lock hash |

## Namespace conflict resolution

Two imports that bind the same local name (`nāmnā`) to different files raise
`SANSKRIPT_IMPORT_CONFLICT` with both resolved paths.

## Migration from Python

| Python | Sanskript |
|--------|-----------|
| `import pkg` | `ānayanam pkg.` |
| `from pkg import fn` | `ānayanam pkg antaḥ fn.` |
| `from . import sibling` | `ānayanam ./sibling.` |
| `pyproject.toml` | `ssk.toml` / `saṃskaraṇa.sskm` |
| `poetry.lock` | `ssk.lock` |
