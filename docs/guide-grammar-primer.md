# Sanskrit Grammar Primer for Programmers

Sanskript source is not “Sanskrit-themed syntax.” Accepted programs must use **controlled** nominal and verbal forms from the grammar register. This primer ties everyday program frames to the linguistic ideas behind them so you can read error messages and write idiomatic code.

## Three layers to know

| Layer | What it governs | Where to read more |
| --- | --- | --- |
| Register | Which word forms the compiler accepts | [grammar-register.md](grammar-register.md), [grammar-register.generated.md](grammar-register.generated.md) |
| Kāraka roles | Who does what to whom (agent, object, location, …) | [feature-lattice.md](feature-lattice.md) |
| Sandhi & script | How tokens join on the surface | [phase1-script-sandhi](../examples/phase1-script-sandhi.ssk), sandhi tests |

The compiler rejects undeclared morphology with `SANSKRIPT_MORPHOLOGY` — that is intentional. Add lemmas to `data/verb_frames.json` / the register, then run `python scripts/build_controlled_lexicon.py`.

## Frames you already use

**Assignment (adhikaraṇa + karman).** Locative holder + accusative value:

```text
gaṇakaḥ pañca phale nidadhāti.
```

`gaṇakaḥ` is the agent; `phale` is the location of the stored value; `pañca` is the object placed there.

**Increase / decrease.** Instrumental increment on the object:

```text
gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
```

**Display.** Accusative object shown to the user:

```text
gaṇakaḥ phalaṃ darśayati.
```

**Conditionals.** `yadi` … `anyathā` … `antam` mirror if/else with Sanskrit particles instead of braces.

**Procedures.** `vidhānam` … `pratyāvartanam` … `samāpanam` declare callable units; `āhvānam` performs calls including stdlib natives.

## Runnable proof

Start with the tested cookbook (assign → add → show):

```powershell
$env:PYTHONPATH='src'
python -m sanskript run examples/cookbook/hello-counter.ssk
```

Expected output: `7`.

## Honest limits

- The register is a **subset** of Classical Sanskrit morphology, not Panini-complete derivation in source form.
- Expert-reviewed (`polished`) entries are still growing; see status columns in the register doc.
- English comments (`//`) are allowed in examples but user-facing teaching prose should prefer Sanskrit frames where possible.

## Related

- [tutorial-beginner.md](tutorial-beginner.md) — first programs
- [style-guide.md](style-guide.md) — naming and register tone
- [phase26-documentation-learning-path.md](phase26-documentation-learning-path.md) — full doc inventory
