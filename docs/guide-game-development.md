# Game Development Guide

Game APIs in Sanskript are **host-backed simulations**: input snapshots, deterministic physics steps, loop history, and planning helpers for audio/sprites/3D. They let you script mechanics in Sanskrit and test JSON-shaped state without claiming a shipped engine.

## Runnable input snapshot

```text
samūhalakṣaṇaḥ keys vākyam jump iti.
āhvānam std.game.input_state keys phalaṃ nidadhāti.
āhvānam std.serialize vākyam json iti phalaṃ darśayati.
```

Cookbook: [game-input.ssk](../examples/cookbook/game-input.ssk) → `{"any":true,"pressed":{"jump":true}}`

```powershell
$env:PYTHONPATH='src'
python -m sanskript run examples/cookbook/game-input.ssk
```

## Other game natives (phase 22)

| Function | What it does today |
| --- | --- |
| `std.game.loop_run` | Integrate `x` with constant `vx` over N frames |
| `std.game.physics2d_step` | Euler step with optional gravity |
| `std.game.sprite_atlas` | Layout metadata for sprite sheets |
| `std.game.scene3d_plan` | Scaffold only |

Showcase mixing web + plot + data: [phase22-web-apps-games-research.ssk](../examples/phase22-web-apps-games-research.ssk).

## Canvas-style raster (web bridge)

`std.web.canvas_raster` paints ASCII grids from rect/line ops — useful for board games before GPU bridges land. Documented under [guide-web-apps.md](guide-web-apps.md).

## Honest checklist language

Independence Phase 22 leaves **Game loop** and related rows open until a native or browser loop ships as a product. Cookbook recipes prove **API behavior**, not Steam-ready games.

## Related

- [guide-ml.md](guide-ml.md) — numeric kernels shared with gameplay AI
- [phase22-web-apps-games-research-ml.md](phase22-web-apps-games-research-ml.md)
