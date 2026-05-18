# Local Grammar Sources

Place the grammar PDFs used as Sanskript's canon in this directory:

- `aShTAdhyAyI.pdf`
- `vyakarana.pdf`
- `संस्कृतं.pdf`

The PDFs are intentionally not committed by default. Run this from the repo root to regenerate the derived canon:

```powershell
python -m pip install -e ".[canon]"
python tools\build_grammar_canon.py
```
