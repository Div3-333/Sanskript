# Sanskript Independence Dashboard

_Generated at 2026-05-27T12:44:21+00:00 by `tools/generate_independence_dashboard.py`._

**Overall independence readiness: 34.3%** (blended feature + module signals).

## Phase 0 checklist

- Items complete: **10 / 10** (100.0%)

## Progress by axis

| Axis | % complete |
| --- | ---: |
| authoring | 19.6 |
| compiling | 42.6 |
| execution | 50.0 |
| testing | 64.8 |
| documentation | 51.2 |
| packaging | 6.5 |
| deployment | 5.5 |

## Feature matrix signals

| Status | Count |
| --- | ---: |
| complete | 2 |
| foundation | 182 |
| partial | 70 |
| planned | 52 |

## Module inventory signals

- Modules inventoried: **212**
- Average replaceability score: **28.2** / 100

## How to refresh

```powershell
$env:PYTHONPATH='src'
python tools/generate_feature_matrix.py
python tools/generate_module_inventory.py
python tools/generate_independence_dashboard.py
```
