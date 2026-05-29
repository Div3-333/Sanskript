# CLI Applications Guide

Command-line programs in Sanskript combine **calculator frames** (assign / compute / display), **stdlib natives** (`std.cli`, `std.file`, `std.process`), and the **`sanskript` CLI** itself. There is no separate “app runtime” — your `.ssk` file is the program.

## Minimal CLI-style program

Use stdlib math without touching the filesystem:

```text
āhvānam std.math.sqrt 16 darśayati.
```

Cookbook: [cli-sqrt.ssk](../examples/cookbook/cli-sqrt.ssk)

```powershell
$env:PYTHONPATH='src'
python -m sanskript run examples/cookbook/cli-sqrt.ssk
```

Expected output: `4.0`.

## Larger CLI patterns (phase examples)

| Pattern | Example | Notes |
| --- | --- | --- |
| Args / env | [phase10-stdlib-cli-io.ssk](../examples/phase10-stdlib-cli-io.ssk) | writes `tmp-phase10-cli.txt` under cwd |
| Research baseline | [phase22-research-cli-baseline.ssk](../examples/phase22-research-cli-baseline.ssk) | `std.data.describe` + ASCII plot |
| HTTP micro-service | [phase22-http-service.ssk](../examples/phase22-http-service.ssk) | seal-bar server (host socket) |

## Toolchain commands

| Task | Command |
| --- | --- |
| Run | `python -m sanskript run program.ssk` |
| Compile | `python -m sanskript compile program.ssk` |
| Lint | `python -m sanskript lint program.ssk` |
| Docs | `python -m sanskript docs program.ssk -o out.md` |

Full flag reference: [tooling.md](tooling.md).

## Packaging

Modules and lockfiles: [modules-packages.md](modules-packages.md). Example tree: [phase9-modules/](../examples/phase9-modules/).

## Honest limits

- `std.cli.program_name` reflects how the host invoked Python (often `-c` in embedded runs); do not rely on it for stable branding until native driver ships.
- Process and file natives are **host-backed**; sandbox paths in CI may differ from your laptop.

## Related

- [guide-stdlib-reference.md](guide-stdlib-reference.md)
- [cookbook.md](cookbook.md)
