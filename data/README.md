# Data

Generated project data lives here.

- `grammar_canon.json` is generated from the local PDFs in `sources/`.
- `vocabulary/nouns/{pattern}.json` — per-stem-class noun corpus (target 100 for common classes; tiered for rare finals).
- `vocabulary/verbs/dhatu_catalog.json` — graduate-tier dhātus organized by gaṇa (1–10), not nominal stem class.
- `verb_frames.json` — controlled finite-verb surfaces with kāraka roles and parser operations.
- `controlled_lexicon.json` — synthesized surfaces from grammar register (rebuild after corpus changes).

Regenerate grammar canon:

```powershell
python tools\build_grammar_canon.py
```

Validate vocabulary corpus and rebuild lexicon:

```powershell
python scripts\build_vocabulary_corpus.py
python scripts\build_controlled_lexicon.py
python scripts\export_grammar_register.py
```

Sources: Macdonell, Whitney, Monier-Williams, Dhatupāṭha references in each entry's `source` field. Rare vowel-final classes (au, ai, e, o, ḷ) use tiered attested minimums rather than padded inventories.
