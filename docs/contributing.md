# Contributing to Sanskript

Thank you for helping improve the language, toolchain, and docs. This repository is still
**host-Python-backed** for compile/run; contributions should keep tests honest about that boundary.

## Before you open a PR

1. Set `PYTHONPATH` to `src` (PowerShell: `$env:PYTHONPATH='src'`).
2. Run the full test suite:

   ```powershell
   python -m unittest discover -s tests
   ```

3. If you touched docs with internal links, run Phase 26 checks:

   ```powershell
   python -m unittest tests.test_phase26_documentation -v
   python -m sanskript phase26-evidence
   ```

   The evidence command exits 0 only when every checklist **[x]** guide has ≥200 words,
   a fenced example, and compiling `examples/*.ssk` proof (`seal_ready: true`).

4. If you changed grammar register or lexicon data, rebuild artifacts (see below) and include
   only intentional diffs in generated files.

## What to change where

| Area | Location | Expectation |
| --- | --- | --- |
| Parser / compiler / VM | `src/sanskript/` | Add or extend `tests/test_phase*.py` |
| Stdlib natives | `stdlib_impl.py`, phase modules | Register natives; test behavior, not inventory-only |
| Examples | `examples/` | Must compile; phase examples are CI-tested |
| Cookbook | `examples/cookbook/*.ssk` | Register in `phase26_docs.COOKBOOK_RECIPES` with expected VM output |
| User docs | `docs/` | Keep links relative; runnable claims need a `.ssk` that runs |
| Controlled lexicon | `data/controlled_lexicon.json` | Regenerate via `build-lexicon` when morphology changes |

## Cookbook and documentation rules

- A cookbook recipe must **compile and run** with predictable `darśayati` output registered in
  `phase26_docs.COOKBOOK_RECIPES` (expected stdout tuple).
- Phase 26 domain guides must link a cookbook `.ssk` or a phase example that CI already runs.
- Independence checklist rows for **shipped products** (native GUI, browser game, trained ML) stay
  open until milestone JSON says otherwise — cookbook proof covers **API/teaching** only.

## Regenerating generated docs

From repo root:

```powershell
python scripts/export_grammar_register.py
python tools/generate_feature_matrix.py
python tools/generate_module_inventory.py
python -m sanskript docs examples/cookbook/api-demo.ssk -o docs/generated/cookbook-api-demo.docs.md
```

## Code style

Follow [style-guide.md](style-guide.md). Prefer extending existing helpers over parallel copies.
Keep Sanskrit register consistent with `data/controlled_lexicon.json`.

## Reporting issues

Include: command line, `.ssk` or test name, expected vs actual output, and Python version.
For compiler errors, paste the diagnostic block from `sanskript lint` when available.

## Related

- [tooling.md](tooling.md) — CLI commands
- [phase26-documentation-learning-path.md](phase26-documentation-learning-path.md) — doc inventory
