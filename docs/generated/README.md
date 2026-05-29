# Generated documentation

Files in this directory are produced by repository tooling. Regenerate from the repo root:

```powershell
$env:PYTHONPATH='src'
python tools/generate_feature_matrix.py
python tools/generate_module_inventory.py
python tools/generate_independence_dashboard.py
python scripts/export_grammar_register.py
python -m sanskript docs examples/cookbook/api-demo.ssk -o docs/generated/cookbook-api-demo.docs.md
```

| File | Source |
| --- | --- |
| `feature-matrix.md` | `tools/generate_feature_matrix.py` |
| `module-inventory.md` | `tools/generate_module_inventory.py` |
| `independence-dashboard.md` | `tools/generate_independence_dashboard.py` |
| `cookbook-api-demo.docs.md` | `examples/cookbook/api-demo.ssk` via `sanskript docs` |
