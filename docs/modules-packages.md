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
signature = "hmac-sha256:<digest>:<signature>"

[features]
json = true

[dependencies.local]
helper = { path = "lib/helper" }

[dependencies.registry]
serde = { version = "0.1.0", registry = "ssk" }

[dependencies.vendored]
legacy = { path = "vendor/legacy", locked = true }

[security]
lock_required = true
signature_required = true

[profile.release]
requires = "json"

[platform]
windows = "platform/windows-extra.ssk"
linux = "platform/linux-extra.ssk"
macos = "platform/macos-extra.ssk"

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

The lockfile pins resolved dependency paths and deterministic `sha256` hashes
for files and directory trees. The loader rejects tampered dependencies when
hashes diverge, rejects lock paths that escape the package root, and rejects
incomplete lockfiles when lock enforcement is active.

When `signature_required = true`, `ssk.lock` must carry the same signature as
`[package].signature`; a mismatch is treated as tampering and aborts resolution.

## Package signing

Set `SANSKRIPT_SIGNING_KEY` and record `signature` in the manifest using the
format `hmac-sha256:<digest>:<signature>`. The loader verifies both digest and
HMAC before resolving dependencies. Digest binding is manifest-aware for both
`ssk.toml` and `saṃskaraṇa.sskm`/`samskarana.sskm`, so changing security flags,
dependency declarations, or namespace values invalidates the signature. There is
no built-in default signing key.

## Platform feature gates

Platform modules under `[platform]` are loaded only for the active platform
(`windows`, `linux`, `macos`, or exact `sys.platform` tag). Non-active
platform bindings are not imported. Manifest validation rejects unknown platform
keys to prevent silent gate bypass through typos.

## Single-file compile proof

Before multi-module manifests, confirm `vidhānam` / `āhvānam` in one file:

```ssk
vidhānam saṃyojanam a b.
pratyāvartanam a b.
samāpanam.
```

Runnable: [phase6-functions.ssk](../examples/phase6-functions.ssk)

```powershell
$env:PYTHONPATH='src'
python -m sanskript compile examples/phase6-functions.ssk
python -m sanskript run examples/phase6-functions.ssk
```

## Fresh checkout reproducibility

`examples/phase9-modules/` includes both `ssk.toml` and `ssk.lock`, with
`lock_required = true`, so dependency resolution is deterministic on a clean
checkout.

Validation commands:

```bash
python -m pytest tests/test_phase9_modules.py -q
python -m pytest tests/test_cli_toolchain.py tests/test_phase_examples.py -q
python -m sanskript.cli run examples/phase9-modules/main.ssk
```

Phase 9 hardening evidence includes dedicated failure-mode tests in
`tests/test_phase9_modules.py` for:
- prose-manifest signature tamper rejection,
- lock-signature mismatch rejection under `signature_required`,
- lock-path/root escape rejection,
- outside-root lock generation rejection,
- unsupported `[platform]` key rejection,
- dependency conflict rejection across case-variants.

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
