# Data and Research Scripting Guide

Research scripting in Sanskript means: load or define small datasets in source, call `std.data.*` for summaries, and render **terminal plots** with `std.plot.*`. Notebooks, Parquet, and Postgres remain planning surfaces.

## Runnable sparkline

Terminal sparkline over five integers (no GUI):

```text
samūhalakṣaṇaḥ citra eka dve trīṇi catvāri pañca.
āhvānam std.plot.sparkline citra darśayati.
```

Cookbook: [research-spark.ssk](../examples/cookbook/research-spark.ssk) → `▁▃▅▆█`

```powershell
$env:PYTHONPATH='src'
python -m sanskript run examples/cookbook/research-spark.ssk
```

## Describe + ASCII chart (phase baseline)

[phase22-research-cli-baseline.ssk](../examples/phase22-research-cli-baseline.ssk) prints `{count:5, min:1.0, max:5.0, mean:3.0}` then a small ASCII canvas — good template for lab scripts.

```powershell
python -m sanskript run examples/phase22-research-cli-baseline.ssk
```

## Data natives map

| API | Status |
| --- | --- |
| `std.data.describe` | bootstrap |
| `std.data.column` | bootstrap |
| `std.data.csv_read` / `csv_write` | host file I/O |
| `std.data.frame` | in-memory table |
| `std.data.parquet_plan` | scaffold |
| `std.notebook.split_cells` | scaffold |
| `std.research.template_render` | bootstrap |

## JSON export path

Use `std.serialize` with `json` format when you need machine-readable logs (also used in desktop/game cookbooks).

## Related

- [guide-ml.md](guide-ml.md) — linalg/tensor/ML pack
- [guide-stdlib-reference.md](guide-stdlib-reference.md)
- [phase11-algorithms-data-structures.md](phase11-algorithms-data-structures.md)
