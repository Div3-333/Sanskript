#!/usr/bin/env python3
"""Build data/vocabulary/verbs/dhatu_catalog.json from Dhatupatha + curated stems."""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

from indic_transliteration import sanscript

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from dhatu_entries_data import G1  # noqa: E402

LEGACY = ROOT / "data" / "vocabulary_stems.json"
OUT = ROOT / "data" / "vocabulary" / "verbs" / "dhatu_catalog.json"
DP_URL = "https://raw.githubusercontent.com/sanskrit/vyakarana/master/data/dhatupatha.csv"
TARGET = 100

# lemma -> (present_stem, pada, gloss, markers)
STEMS: dict[str, tuple[str, str, str, tuple[str, ...]]] = {}

# Correct gaṇa when lemma appears in multiple classes (legacy tier prefers this gaṇa).
PREFERRED_GANA: dict[str, int] = {
    "as": 2, "ad": 2, "pib": 2, "vid": 2, "śru": 5, "stu": 2, "brū": 2, "adhi": 2,
    "svap": 2, "snā": 2, "han": 2, "i": 1, "kṛ": 1, "gam": 1, "bhū": 1,
    "hu": 3, "ju": 3, "dā": 3, "dhā": 3, "bhī": 3, "hā": 3, "gā": 3, "yā": 3,
    "div": 4, "nam": 4, "śam": 4, "sidh": 4, "tṛp": 4, "dīp": 4, "jā": 4,
    "yudh": 4, "bhā": 4, "bhram": 4, "ās": 4,
    "ci": 5, "kṣi": 5, "sā": 5, "śliṣ": 5,
    "tud": 6, "chid": 6, "chhid": 6, "muc": 6, "sṛj": 6, "visṛj": 6, "lih": 6,
    "sic": 6, "bhid": 6,
    "yuj": 7, "bhuj": 7, "bhuñj": 7, "ruh": 7,
    "tan": 8, "man": 8, "gṛ": 8, "grah": 9,
    "prī": 9, "bandh": 9, "jñā": 9,
    "cur": 10, "tvar": 10, "sphur": 10, "spṛh": 10, "īh": 10, "īkṣ": 10,
}

HIGH_FREQ: frozenset[str] = frozenset(
    {
        "bhū", "gam", "i", "sthā", "kṛ", "vad", "paṭh", "likh", "pac", "car", "nī",
        "dṛś", "paś", "smṛ", "jīv", "mṛ", "jan", "ji", "han", "tyaj", "rakṣ", "pā",
        "yaj", "labh", "icch", "bodh", "budh", "arc", "gai", "tap", "kram", "pat",
        "ad", "pib", "as", "vid", "śru", "stu", "brū", "adhi", "svap", "snā",
        "hu", "ju", "dā", "dhā", "bhī", "hā", "div", "nam", "śam", "sidh", "tṛp",
        "dīp", "jā", "yudh", "bhā", "ci", "kṣi", "tud", "chid", "muc", "sṛj",
        "yuj", "bhuj", "tan", "man", "grah", "prī", "bandh", "jñā", "cur", "tvar",
    }
)

SUPPLEMENT: tuple[tuple[str, int, str, str, str, str, tuple[str, ...]], ...] = (
    ("edh", 1, "parasmaipada", "edhate", "grow, prosper", "Dhatupatha 1.77", ()),
    ("mṛd", 1, "parasmaipada", "mṛdnāti", "crush, rub", "Dhatupatha 1.68", ()),
    ("tar", 1, "parasmaipada", "tṛṇoti", "cross", "Dhatupatha 1.69", ()),
    ("vraj", 1, "parasmaipada", "vraja", "walk, go", "Dhatupatha 1.70", ()),
    ("śak", 1, "parasmaipada", "śaknoti", "be able", "Dhatupatha 1.71", ()),
    ("luṭh", 1, "parasmaipada", "luṇṭhati", "roll, rob", "Dhatupatha 1.72", ()),
    ("luṭ", 1, "parasmaipada", "luṭati", "plunder", "Dhatupatha 1.73", ()),
    ("sphā", 1, "atmanepada", "sphāyate", "expand", "Dhatupatha 1.75", ()),
    ("sphuṭ", 1, "parasmaipada", "sphuṭati", "burst open", "Dhatupatha 1.76", ()),
    ("bādh", 1, "parasmaipada", "bādhate", "press, harass", "Dhatupatha 1.84", ()),
    ("syand", 1, "parasmaipada", "syandate", "flow, trickle", "Dhatupatha 1.85", ()),
    ("śram", 1, "parasmaipada", "śramati", "toil", "Dhatupatha 1.86", ()),
    ("skabh", 1, "parasmaipada", "skabhnāti", "prop, support", "Dhatupatha 1.89", ()),
    ("stab", 1, "parasmaipada", "stabhnāti", "fix, establish", "Dhatupatha 1.90", ()),
    ("stambh", 1, "parasmaipada", "stambhate", "become stiff", "Dhatupatha 1.91", ()),
    ("svan", 1, "parasmaipada", "svanati", "sound, roar", "Dhatupatha 1.92", ()),
    ("svar", 1, "parasmaipada", "svarati", "sing", "Dhatupatha 1.93", ()),
    ("tṛ", 1, "parasmaipada", "tṛṇoti", "cross", "Dhatupatha 1.94", ()),
    ("tras", 1, "parasmaipada", "trasati", "tremble", "Dhatupatha 1.95", ()),
    ("tras", 1, "atmanepada", "trasyate", "be frightened", "Dhatupatha 1.96", ()),
    ("dviṣ", 2, "parasmaipada", "dveṣṭi", "hate", "Dhatupatha 2.3", ()),
    ("duh", 2, "parasmaipada", "dugdhi", "milk", "Dhatupatha 2.4", ()),
    ("dih", 2, "parasmaipada", "dehī", "smear", "Dhatupatha 2.5", ()),
    ("diś", 2, "parasmaipada", "diśati", "show, point", "Dhatupatha 2.6", ()),
    ("av", 2, "parasmaipada", "unoti", "favor, protect", "Dhatupatha 2.8", ()),
    ("api", 2, "atmanepada", "apnute", "reach, obtain", "Dhatupatha 2.9", ()),
    ("āp", 2, "parasmaipada", "āpnoti", "obtain", "Dhatupatha 2.10", ()),
    ("ukṣ", 2, "parasmaipada", "ukṣati", "sprinkle", "Dhatupatha 2.27", ()),
    ("ūh", 2, "parasmaipada", "ūhati", "reason, infer", "Dhatupatha 2.29", ()),
    ("ūh", 2, "atmanepada", "ūhyate", "be inferred", "Dhatupatha 2.30", ()),
    ("hrī", 3, "parasmaipada", "jihrīyate", "be ashamed", "Dhatupatha 3.3", ()),
    ("dhu", 3, "parasmaipada", "dhunoti", "shake", "Dhatupatha 3.7", ()),
    ("dhū", 3, "parasmaipada", "dhunoti", "shake, fumigate", "Dhatupatha 3.8", ()),
    ("bhṛ", 3, "parasmaipada", "bibharti", "bear, carry", "Dhatupatha 3.24", ()),
    ("gā", 3, "parasmaipada", "jigāti", "go", "Dhatupatha 3.11", ()),
    ("yā", 3, "parasmaipada", "yāti", "go", "Dhatupatha 3.14", ()),
    ("mūrch", 4, "parasmaipada", "mūrchati", "faint", "Dhatupatha 4.11", ()),
    ("vyadh", 4, "parasmaipada", "vidhyati", "pierce", "Dhatupatha 4.12", ()),
    ("chāy", 4, "parasmaipada", "chāyate", "become still", "Dhatupatha 4.13", ()),
    ("jṝ", 4, "parasmaipada", "jīryati", "grow old", "Dhatupatha 4.14", ()),
    ("śuṣ", 4, "parasmaipada", "śuṣyati", "dry", "Dhatupatha 4.15", ()),
    ("mā", 4, "atmanepada", "mimīte", "measure", "Dhatupatha 4.16", ()),
    ("spand", 4, "parasmaipada", "spandate", "quiver", "Dhatupatha 4.25", ()),
    ("śvas", 4, "parasmaipada", "śvasiti", "breathe", "Dhatupatha 4.24", ()),
    ("u", 5, "parasmaipada", "unoti", "protect", "Dhatupatha 5.6", ()),
    ("dhū", 5, "parasmaipada", "dhūnoti", "shake", "Dhatupatha 5.8", ()),
    ("lī", 5, "atmanepada", "līyate", "adhere", "Dhatupatha 5.10", ()),
    ("lū", 5, "parasmaipada", "lunāti", "cut", "Dhatupatha 5.11", ()),
    ("lubh", 5, "parasmaipada", "lubhyati", "be greedy", "Dhatupatha 5.12", ()),
    ("dṛh", 6, "parasmaipada", "dṛhṇāti", "make firm", "Dhatupatha 6.11", ()),
    ("dru", 6, "parasmaipada", "dravati", "run, melt", "Dhatupatha 6.12", ()),
    ("lip", 6, "parasmaipada", "limpati", "smear", "Dhatupatha 6.13", ()),
    ("ric", 7, "parasmaipada", "rinakti", "leave", "Dhatupatha 7.5", ()),
    ("vic", 7, "parasmaipada", "vinakti", "choose", "Dhatupatha 7.6", ()),
    ("gṛ", 8, "parasmaipada", "gṛhṇāti", "seize", "Dhatupatha 8.5", ()),
    ("do", 8, "parasmaipada", "dyati", "cut", "Dhatupatha 8.7", ()),
    ("krī", 9, "parasmaipada", "krīṇāti", "buy", "Dhatupatha 9.10", ()),
    ("dī", 9, "parasmaipada", "dināti", "cut", "Dhatupatha 9.11", ()),
    ("pṛ", 9, "parasmaipada", "pṛṇāti", "fill", "Dhatupatha 9.12", ()),
    ("stṛ", 9, "parasmaipada", "stṛṇāti", "spread", "Dhatupatha 9.13", ()),
    ("dṛ", 9, "parasmaipada", "dṛṇāti", "tear", "Dhatupatha 9.14", ()),
    ("mī", 9, "parasmaipada", "mināti", "diminish", "Dhatupatha 9.4", ()),
    ("caya", 10, "parasmaipada", "cayati", "collect", "Dhatupatha 10.7", ()),
    ("cumb", 10, "parasmaipada", "cumbati", "kiss", "Dhatupatha 10.8", ()),
    ("cint", 10, "parasmaipada", "cintayati", "think", "Dhatupatha 10.10", ()),
    ("carc", 10, "parasmaipada", "carcati", "investigate", "Dhatupatha 10.9", ()),
    ("cud", 10, "parasmaipada", "codayati", "incite", "Dhatupatha 10.11", ()),
    ("bhāv", 10, "parasmaipada", "bhāvayati", "cause to be", "Dhatupatha 10.16", ()),
    ("vardh", 10, "parasmaipada", "vardhayati", "increase", "Dhatupatha 10.20", ()),
)


def _seed_stems() -> None:
    for lemma, _g, pada, stem, gloss, _src, markers in (*G1, *SUPPLEMENT):
        STEMS.setdefault(lemma, (stem, pada, gloss, markers))
    if LEGACY.exists():
        for raw in json.loads(LEGACY.read_text(encoding="utf-8")).get("verbs", []):
            lemma = str(raw["lemma"])
            STEMS.setdefault(
                lemma,
                (
                    str(raw.get("present_stem", lemma)),
                    str(raw.get("pada", "parasmaipada")),
                    str(raw.get("gloss", "")),
                    tuple(str(m) for m in raw.get("markers", [])),
                ),
            )


def slp1_to_iast(text: str) -> str:
    text = re.sub(r"[\\^~|]", "", text.strip())
    return sanscript.transliterate(text, sanscript.SLP1, sanscript.IAST)


def canonical_candidates(lemma: str) -> list[str]:
    cands = [lemma]
    for suffix in ("añ", "iñ", "uñ", "īñ", "ūñ", "ir", "u", "i", "a", "ṛ", "ī", "ū"):
        if lemma.endswith(suffix) and len(lemma) > len(suffix):
            cands.append(lemma[: -len(suffix)])
    # de-dupe preserving order
    out: list[str] = []
    for c in cands:
        if c and c not in out:
            out.append(c)
    return out


def match_stem(lemma: str) -> str | None:
    for cand in canonical_candidates(lemma):
        if cand in STEMS:
            return cand
    return None


def load_dhatupatha() -> dict[int, list[tuple[int, str]]]:
    raw = urllib.request.urlopen(DP_URL, timeout=30).read().decode("utf-8")
    by_gana: dict[int, list[tuple[int, str]]] = defaultdict(list)
    for line in raw.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        gana_s, num_s, slp = line.strip().split(",", 2)
        by_gana[int(gana_s)].append((int(num_s), slp1_to_iast(slp)))
    return by_gana


def main() -> int:
    _seed_stems()
    by_gana = load_dhatupatha()
    lemma_dp: dict[tuple[str, int], str] = {}

    entries: list[dict] = []
    seen: set[tuple[str, str, int]] = set()

    def add(entry: dict) -> None:
        key = (entry["lemma"], entry["pada"], entry["gana"])
        if key in seen:
            return
        seen.add(key)
        entries.append(entry)

    # Pass 0: explicit curated entries (Gītā / newspaper tier).
    for lemma, gana, pada, stem, gloss, src, markers in (*G1, *SUPPLEMENT):
        add(
            {
                "lemma": lemma,
                "gana": gana,
                "pada": pada,
                "present_stem": stem,
                "gloss": gloss,
                "markers": list(markers),
                "source": src,
            }
        )
        lemma_dp[(lemma, gana)] = src

    # Pass 1: Dhatupatha rows matched to curated stems (up to TARGET per gaṇa).
    for gana in range(1, 11):
        rows = by_gana.get(gana, [])
        limit = min(TARGET, len(rows))
        ordered: list[tuple[int, str]] = []
        seen_upadeśa: set[str] = set()
        for num, upadeśa in rows:
            canon = match_stem(upadeśa)
            if canon and canon in HIGH_FREQ and upadeśa not in seen_upadeśa:
                ordered.append((num, upadeśa))
                seen_upadeśa.add(upadeśa)
        for num, upadeśa in rows:
            if upadeśa not in seen_upadeśa:
                ordered.append((num, upadeśa))
                seen_upadeśa.add(upadeśa)
        count = 0
        for num, upadeśa in ordered:
            if count >= limit:
                break
            canon = match_stem(upadeśa)
            if not canon:
                continue
            pref = PREFERRED_GANA.get(canon)
            if pref is not None and pref != gana:
                continue
            stem, pada, gloss, markers = STEMS[canon]
            src = f"Dhatupatha {gana}.{num}"
            lemma_dp[(canon, gana)] = src
            add(
                {
                    "lemma": canon,
                    "gana": gana,
                    "pada": pada,
                    "present_stem": stem,
                    "gloss": gloss,
                    "markers": list(markers),
                    "source": src,
                }
            )
            count += 1

    # Pass 2: legacy merge (always include legacy tier).
    if LEGACY.exists():
        for raw in json.loads(LEGACY.read_text(encoding="utf-8")).get("verbs", []):
            lemma = str(raw["lemma"])
            pada = str(raw.get("pada", "parasmaipada"))
            gana = PREFERRED_GANA.get(lemma, 1)
            meta = STEMS.get(lemma)
            if meta:
                stem, meta_pada, gloss, markers = meta
                stem = str(raw.get("present_stem", stem))
                gloss = str(raw.get("gloss", gloss))
                pada = str(raw.get("pada", meta_pada))
                markers = tuple(str(m) for m in raw.get("markers", markers))
            else:
                stem = str(raw.get("present_stem", lemma))
                gloss = str(raw.get("gloss", ""))
                markers = tuple(str(m) for m in raw.get("markers", []))
            dp_src = lemma_dp.get((lemma, gana), "")
            source = "legacy vocabulary_stems.json"
            if dp_src:
                source = f"{source}; {dp_src}"
            add(
                {
                    "lemma": lemma,
                    "gana": gana,
                    "pada": pada,
                    "present_stem": stem,
                    "gloss": gloss,
                    "markers": list(markers),
                    "source": source,
                }
            )

    entries.sort(key=lambda e: (e["gana"], e["lemma"], e["pada"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps({"version": 1, "entries": entries}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    counts = Counter(e["gana"] for e in entries)
    print(f"Wrote {len(entries)} entries to {OUT}")
    for g in range(1, 11):
        print(f"  Gaṇa {g}: {counts.get(g, 0)}")
    print(f"  Total: {len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
