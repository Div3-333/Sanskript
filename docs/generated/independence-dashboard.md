# Sanskript Independence Dashboard

_Generated at 2026-05-29T05:05:30+00:00 by `tools/generate_independence_dashboard.py`._

**Overall independence readiness: 34.8%** (blended feature + module signals).

## Phase 0 checklist

- Items complete: **10 / 10** (100.0%)

## Progress by axis

| Axis | % complete |
| --- | ---: |
| authoring | 18.7 |
| compiling | 44.1 |
| execution | 50.9 |
| testing | 66.8 |
| documentation | 51.0 |
| packaging | 6.5 |
| deployment | 5.5 |

## Feature matrix signals

| Status | Count |
| --- | ---: |
| complete | 5 |
| foundation | 182 |
| partial | 97 |
| planned | 52 |

## Module inventory signals

- Modules inventoried: **262**
- Average replaceability score: **28.8** / 100

## How to refresh

```powershell
$env:PYTHONPATH='src'
python tools/generate_feature_matrix.py
python tools/generate_module_inventory.py
python tools/generate_independence_dashboard.py
```
