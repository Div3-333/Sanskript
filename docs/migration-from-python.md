# Migrating from Python

This guide maps familiar Python shapes to **grammatical Sanskript** — not a line-for-line
transliteration. Prefer verb frames and case roles over Python punctuation.

## Mental model

| Python habit | Sanskript habit |
| --- | --- |
| `x = 5` | `gaṇakaḥ pañca phale nidadhāti.` (verb + cases) |
| `x += 2` | `gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.` |
| `print(x)` | `gaṇakaḥ phalaṃ darśayati.` |
| `if` / `else` | `yadi` … `anyathā` … `antam` |
| `def f(a, b): return a+b` | `vidhānam f a b .` … `pratyāvartanam` … `samāpanam` |
| `"hello"` string | `vākyam hello iti phale nidadhāti.` |
| `# comment` | `//` or `व्याख्या:` line prefix |
| `import m` | `ānayanam m` inside a module (see [modules-packages.md](modules-packages.md)) |

## Example: arithmetic script

**Python**

```python
x = 5
x += 2
print(x)
```

**Sanskript** ([hello-counter](../examples/cookbook/hello-counter.ssk))

```text
gaṇakaḥ pañca phale nidadhāti.
gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
gaṇakaḥ phalaṃ darśayati.
```

Run: `python -m sanskript run examples/cookbook/hello-counter.ssk` → `7`.

## Example: conditional

**Python**

```python
x = 3
if x == 3:
    x *= 10
else:
    x += 1
print(x)
```

**Sanskript** ([conditional-branch](../examples/cookbook/conditional-branch.ssk))

```text
gaṇakaḥ trīṇi phale nidadhāti.
yadi phalaṃ samam trīṇi.
gaṇakaḥ phalaṃ daśabhiḥ vardhayati.
anyathā.
gaṇakaḥ phalaṃ ekena vardhayati.
antam.
gaṇakaḥ phalaṃ darśayati.
```

Output: `13`. Comparisons use markers like `samam` (equality); see [control-flow.md](control-flow.md).

## Example: function with return

**Python**

```python
def add(a, b):
    return a + b
print(add(3, 4))
```

**Sanskript** (excerpt from [phase6-functions.ssk](../examples/phase6-functions.ssk))

```text
vidhānam yogaḥ a b .
pratyāvartanam a yoga b .
samāpanam .

gaṇitam yukta āhvānam yogaḥ sapta .
darśanam yukta .
```

Calls use `āhvānam` + function name + arguments, not `f(3, 4)`.

## Standard library and host calls

Phase 10 surfaces such as `std.file.read_text` are invoked with `āhvānam` and text
literals via `vākyam … iti`. See [phase10-standard-library-core.md](phase10-standard-library-core.md).
Many stdlib entry points still execute in the Python host — they are not yet pure Sanskript.

## What is not ported yet

- `async` / `await` ergonomics (see Phase 15 docs)
- NumPy/pandas-style data stacks (no ML migration path yet)
- Pip-style index installs (local `ssk.toml` + vendor paths only)

## Further reading

- [tutorial-beginner.md](tutorial-beginner.md)
- [core-syntax.md](core-syntax.md)
- [cookbook.md](cookbook.md)
