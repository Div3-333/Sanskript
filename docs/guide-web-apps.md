# Web Apps Guide (Honest Scope)

Sanskript does **not** ship a production HTTP server or browser DOM platform today. This guide
covers what you can run now: host-backed `std.web.*` helpers in the VM and the `web` CLI for
static HTML that embeds bytecode.

For seal gates and blockers, see [phase22-web-apps-games-research-ml.md](phase22-web-apps-games-research-ml.md).

## Runnable cookbook example

Source: [web-hello.ssk](../examples/cookbook/web-hello.ssk)

| Step | Command |
| --- | --- |
| Run in VM | `python -m sanskript run examples/cookbook/web-hello.ssk` |
| Compile | `python -m sanskript compile examples/cookbook/web-hello.ssk` |

Expected stdout (one line):

```text
<h1>Hello</h1>
```

The program:

1. Builds a route table (`kośaḥ` / `sthāpanam`) and matches `/hello` with `std.web.route_match`.
2. Renders a tiny HTML fragment with `std.web.render` and `{{title}}` substitution.

`std.web.route_match` is **string pattern matching**, not socket I/O. The match result is stored
but not displayed in this minimal recipe.

## Static HTML export (`web` CLI)

Embed bytecode in a self-contained HTML page (stdout-only in the browser; no live DOM API):

```powershell
$env:PYTHONPATH='src'
python -m sanskript web examples/cookbook/web-hello.ssk -o artifacts/web-hello.html
```

Open the file in a browser to see VM `darśayati` output. Details: [tooling.md](tooling.md#documentation-and-packaging).

## What is host-backed vs native

| Surface | Status | Notes |
| --- | --- | --- |
| `std.web.route_match`, `std.web.render` | bootstrap | Python host in `stdlib_impl.py` |
| `std.web.dom_simulate`, `std.web.bridge_plan` | scaffold | Simulation/plan only |
| `sanskript web` | bootstrap | Static runner HTML, not a SPA framework |

Larger showcase (many `std.*` calls, not a product): [phase22-web-apps-games-research.ssk](../examples/phase22-web-apps-games-research.ssk).

## Related docs

- [cookbook.md](cookbook.md) — tested recipes
- [phase14-surakshita-capability.md](phase14-surakshita-capability.md) — first `std.web.*` ergonomics
- [tooling.md](tooling.md) — CLI reference
