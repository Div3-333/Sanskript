import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

steps = [
    "sanskript.grammar",
    "sanskript.tinanta",
    "sanskript.vocabulary_catalog",
    "sanskript.grammar_register",
    "sanskript.morphology_lexicon",
    "sanskript.morphology_synth",
    "sanskript.morphology_facade",
    "sanskript.parser",
]

for name in steps:
    t = time.time()
    print(f"importing {name}...", flush=True)
    __import__(name)
    print(f"  ok {time.time()-t:.2f}s", flush=True)
