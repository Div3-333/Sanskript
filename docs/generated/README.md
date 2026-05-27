# Generated documentation

Files in this directory are produced by Phase 0 inventory tools under `tools/`.
Regenerate from the repository root:

```powershell
$env:PYTHONPATH='src'
python tools/generate_feature_matrix.py
python tools/generate_module_inventory.py
python tools/generate_independence_dashboard.py
```
