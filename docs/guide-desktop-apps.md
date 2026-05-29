# Desktop Applications Guide

Sanskript does **not** ship a native windowing toolkit today. Desktop work means understanding the **planned widget surface**, running **capability plans** through host simulation, and keeping checklist language honest until a real GUI product exists.

## What exists now

| API | Status | Purpose |
| --- | --- | --- |
| `std.gui.capabilities_plan` | host_substitute | JSON plan of widgets/menus/shortcuts |
| `std.gui.simulate` | scaffold | DOM-like event simulation (shared bridge) |
| Native windowing | missing | independence milestones still open |

## Runnable capability plan

```text
āhvānam std.gui.capabilities_plan phalaṃ nidadhāti.
āhvānam std.serialize vākyam json iti phalaṃ darśayati.
```

Cookbook: [desktop-plan.ssk](../examples/cookbook/desktop-plan.ssk)

```powershell
$env:PYTHONPATH='src'
python -m sanskript run examples/cookbook/desktop-plan.ssk
```

Stdout is one JSON line listing widgets (`button`, `label`, `text_field`, `checkbox`) and honesty fields (`implementation_state`, `substitute`).

## How this relates to web scaffolds

Phase 22 groups GUI with web/games under one host bridge. Web templates are further along for **runnable** proof — see [guide-web-apps.md](guide-web-apps.md). Desktop remains plan-first by design so we do not tick “GUI widgets” in the independence checklist without executable UI code.

## Roadmap cues

- [phase22-web-apps-games-research-ml.md](phase22-web-apps-games-research-ml.md) — inventory rows
- [phase21-cross-platform-system-support.md](phase21-cross-platform-system-support.md) — platform matrix

## Related

- [guide-game-development.md](guide-game-development.md) — input/loop scaffolds
- [contributing.md](contributing.md) — do not mark GUI rows done without runnable UI
