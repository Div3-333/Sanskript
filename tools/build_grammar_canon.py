from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sanskript.adhyaya1 import implementation_note_for as adhyaya1_implementation_note_for
from sanskript.adhyaya1 import implemented_sutra_ids as adhyaya1_implemented_sutra_ids
from sanskript.adhyaya1 import partial_implementation_note_for as adhyaya1_partial_implementation_note_for
from sanskript.adhyaya1 import partial_sutra_ids as adhyaya1_partial_sutra_ids
from sanskript.adhyaya23 import implementation_note_for as adhyaya23_implementation_note_for
from sanskript.adhyaya23 import implemented_sutra_ids as adhyaya23_implemented_sutra_ids
from sanskript.adhyaya23 import partial_implementation_note_for as adhyaya23_partial_implementation_note_for
from sanskript.adhyaya23 import partial_sutra_ids as adhyaya23_partial_sutra_ids
from sanskript.adhyaya456 import implementation_note_for as adhyaya456_implementation_note_for
from sanskript.adhyaya456 import implemented_sutra_ids as adhyaya456_implemented_sutra_ids
from sanskript.adhyaya456 import partial_implementation_note_for as adhyaya456_partial_implementation_note_for
from sanskript.adhyaya456 import partial_sutra_ids as adhyaya456_partial_sutra_ids
from sanskript.canon_topics import treatment_for

SOURCES_DIR = ROOT / "sources"
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
CANON_JSON = DATA_DIR / "grammar_canon.json"
CANON_MD = DOCS_DIR / "grammar-canon.md"


SOURCE_IDS = {
    "aShTAdhyAyI.pdf": "ashtadhyayi",
    "vyakarana.pdf": "vyakarana_pravesha",
    "संस्कृतं.pdf": "sanskrit_for_beginners",
}


SOURCE_LABELS = {
    "ashtadhyayi": "Aṣṭādhyāyī or Sūtrapāṭha of Pāṇini",
    "vyakarana_pravesha": "vyākaraṇa-praveśaḥ",
    "sanskrit_for_beginners": "Sanskrit for Beginners",
}


PARTIAL_TOPIC_TITLES = {
    "Consonant sandhi between words",
    "Consonant sandhi within a word",
    "-at, -āna, and -vas",
    "-ta and -tavat",
    "-tavya, -anīya, and -ya",
    "-tum",
    "-tvā and -ya",
    "-a stems",
    "-ā, -ī, and -ū stems",
    "apatya",
    "atiśāyana",
    "avyayībhāva",
    "Basic vowels",
    "Basic nominal endings",
    "bahuvrīhi",
    "Compound vowels",
    "Compounds",
    "Consonants",
    "Consonant clusters",
    "Agreement",
    "Adverbs",
    "Devanagari",
    "Derived roots",
    "dvandva",
    "Forms of nau",
    "ghañ",
    "kṛt",
    "kta",
    "kṛtya",
    "matu̐p",
    "Nominal suffixes",
    "Nominals",
    "Nominals 1: Normal stems",
    "Nominals 2: Pronouns and numbers",
    "Other sounds",
    "Other root suffixes",
    "Other prefixes",
    "Prefixes",
    "Pronominal adjectives",
    "Questions",
    "Romanized Sanskrit",
    "Semivowels",
    "Sentence structure",
    "Sentences",
    "Short and long vowels",
    "Sounds",
    "Syllables",
    "The Shiva Sutras",
    "The eight cases",
    "The sandhi system",
    "The sound system",
    "The compound system",
    "The suffix system",
    "Types of uninflected words",
    "Uninflected words",
    "Verbless sentences",
    "tatpuruṣa",
    "taddhita",
    "Vowel sandhi",
    "Vowel marks",
    "Vowels",
    "Vowels and consonants",
    "The upasarga",
    "ca, vā, and others",
    "dhātu",
    "guṇa",
    "asmad and yuṣmad",
    "kāraka",
    "lakāra",
    "parasmaipada and ātmanepada",
    "prakriyā",
    "prātipadika",
    "subanta",
    "sup-pratyāhāra",
    "tiṅ-pratyāhāra",
    "tiṅ-siddhi",
    "tiṅanta",
    "visarga sandhi",
    "vibhakti",
    "vikaraṇa",
    "savarṇa sounds",
    "śatṛ and śānac",
    "Suffixes",
    "it letters",
    "vidhi rules",
    "The asiddha section",
    "hal sandhi",
    "ṣatva and ṇatva",
    "kim and yad",
    "anusvāra and visarga",
    "How Devanagari works",
    "Modern pronunciation",
    "Numerals and punctuation",
}


BATCHED_PADA_PREFIXES = {
    "1.1": "sound definitions and technical terms are now handled by the phonology/pratyāhāra subsystem at batch level.",
    "1.2": "metarule, it-marker, optionality, and substitution-control infrastructure now exists at batch level.",
    "7.1": "aṅga augment and suffix-trigger infrastructure now exists at batch level.",
    "7.2": "guṇa/vṛddhi and aṅga strengthening infrastructure now exists at batch level.",
    "7.3": "internal aṅga replacement and nasalization infrastructure now exists at batch level.",
    "7.4": "late aṅga replacement and retroflexion infrastructure now exists at batch level.",
    "8.1": "sentence-edge, discourse-particle, and clause-operation infrastructure now exists at batch level.",
    "8.2": "consonant/visarga sandhi infrastructure now exists at batch level.",
    "8.3": "visarga and sibilant sandhi infrastructure now exists at batch level.",
    "8.4": "late sound-change infrastructure now exists at batch level.",
}


TOPIC_IMPLEMENTATION_NOTES = {
    "Uninflected words": "Initial avyaya registry covers particles, adverbs, and prefix-like indeclinables.",
    "Types of uninflected words": "Initial avyaya registry distinguishes conjunction, alternative, emphasis, negation, question, relative, correlative, prefix, adverb, quotative, and sequencer uses.",
    "The upasarga": "Initial upasarga registry covers the standard controlled verbal prefixes.",
    "Other prefixes": "Prefix-like indeclinables are tracked as non-inflecting forms.",
    "ca, vā, and others": "Core discourse particles are recognized by morphology and sentence profiling.",
    "Adverbs": "Initial adverbial avyayas such as atra, tatra, tadā, and punaḥ are registered.",
    "Sentences": "Initial sentence profiler classifies statements, questions, relative clauses, coordinated clauses, and verbless profiles.",
    "Sentence structure": "Sentence profiles now expose finite verbs, participants, and particles.",
    "Agreement": "Initial subject-finite-verb agreement checks compare person and number.",
    "Verbless sentences": "Sentences without a finite verb receive an explicit syntactic profile.",
    "Questions": "Question particles such as kim, katham, and kadā are recognized.",
    "Relative phrases": "Relative-correlative particles such as yatra/tatra and yadā/tadā are recognized.",
    "The eight cases": "The existing subanta/kāraka layer maps cases into compiler roles.",
    "it letters": "Metarule scaffolding tracks technical markers as derivational controls.",
    "vidhi rules": "Metarule scaffolding records rule behavior such as substitution, optionality, prohibition, and override.",
    "The asiddha section": "Late-operation scaffolding separates sentence-edge and word-formation domains.",
    "hal sandhi": "Existing consonant sandhi infrastructure covers this topic at batch level.",
    "ṣatva and ṇatva": "Late sound-change infrastructure tracks this topic at batch level.",
    "kim and yad": "Question and relative forms are recognized in the syntax/avyaya layer.",
    "Sounds": "Phonology, accent, and sound-change registries now cover this topic at batch level.",
    "Syllables": "Accent profiles provide the first controlled syllable/accent metadata layer.",
    "anusvāra and visarga": "Normalization and visarga sandhi cover this topic at batch level.",
    "Modern pronunciation": "The phonology inventory provides controlled pronunciation categories.",
    "Devanagari": "Transliteration support maps controlled IAST and Devanagari forms.",
    "How Devanagari works": "The transliteration layer records Devanagari input/output behavior.",
    "Vowels and consonants": "The phonology inventory classifies vowels and consonants.",
    "Vowel marks": "Devanagari conversion covers vowel mark behavior at batch level.",
    "Consonant clusters": "Transliteration and phonology recognize consonant sequences at batch level.",
    "Numerals and punctuation": "The morphology and sentence splitter recognize controlled numerals and punctuation.",
}


PARTIAL_SUTRA_IDS: dict[str, str] = {
    sutra_id: adhyaya1_partial_implementation_note_for(sutra_id)
    for sutra_id in sorted(adhyaya1_partial_sutra_ids())
}
PARTIAL_SUTRA_IDS.update(
    {
        sutra_id: adhyaya23_partial_implementation_note_for(sutra_id)
        for sutra_id in sorted(adhyaya23_partial_sutra_ids())
    }
)
PARTIAL_SUTRA_IDS.update(
    {
        sutra_id: adhyaya456_partial_implementation_note_for(sutra_id)
        for sutra_id in sorted(adhyaya456_partial_sutra_ids())
    }
)


IMPLEMENTED_SUTRA_IDS = {
    sutra_id: adhyaya1_implementation_note_for(sutra_id)
    for sutra_id in sorted(adhyaya1_implemented_sutra_ids())
}
IMPLEMENTED_SUTRA_IDS.update(
    {
        sutra_id: adhyaya23_implementation_note_for(sutra_id)
        for sutra_id in sorted(adhyaya23_implemented_sutra_ids())
    }
)
IMPLEMENTED_SUTRA_IDS.update(
    {
        sutra_id: adhyaya456_implementation_note_for(sutra_id)
        for sutra_id in sorted(adhyaya456_implemented_sutra_ids())
    }
)


DEVANAGARI_DIGITS = {0x966 + i: ord(str(i)) for i in range(10)}
SUTRA_ID_RE = re.compile(r"(?<!\d)([1-8]\.[1-4]\.\d{1,3})(?!\d)")


@dataclass(frozen=True)
class OutlineEntry:
    title: str
    level: int
    page: int | None

    def to_json(self) -> dict[str, Any]:
        return {"title": self.title, "level": self.level, "page": self.page}


def main() -> int:
    DATA_DIR.mkdir(exist_ok=True)
    DOCS_DIR.mkdir(exist_ok=True)

    sources = []
    for pdf_path in sorted(SOURCES_DIR.glob("*.pdf"), key=lambda path: path.name):
        source_id = SOURCE_IDS.get(pdf_path.name, pdf_path.stem)
        sources.append(analyze_source(pdf_path, source_id))

    canon = {
        "schema_version": 1,
        "policy": {
            "principle": "All grammar topics extractable from the local source PDFs are canonical requirements for Sanskript design.",
            "copyright_boundary": "The ledger stores metadata, outline topics, and sutra identifiers; it does not copy full PDF text.",
            "coverage_statuses": {
                "canon_indexed": "Indexed from a source PDF and accepted as part of the language-design canon.",
                "implemented": "Complete discrete Paninian executable logic with positive and negative behavioral tests.",
                "partial": "Some compiler support exists, but the topic is not fully implemented.",
                "batch_partial": "A whole sutra cluster is supported by a subsystem scaffold, but individual sutras are not complete.",
                "pending_design": "Not yet implemented; must be addressed before the language can be considered complete.",
            },
        },
        "sources": sources,
    }
    canon["obligations"] = build_obligations(sources)
    canon["coverage_summary"] = summarize_obligations(canon["obligations"])

    CANON_JSON.write_text(json.dumps(canon, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    CANON_MD.write_text(render_markdown(canon), encoding="utf-8")
    return 0


def analyze_source(pdf_path: Path, source_id: str) -> dict[str, Any]:
    reader = PdfReader(str(pdf_path))
    text_char_count = 0
    sutra_ids: list[str] = []

    for page in reader.pages:
        text = page.extract_text() or ""
        text_char_count += len(text)
        if source_id == "ashtadhyayi":
            sutra_ids.extend(SUTRA_ID_RE.findall(text.translate(DEVANAGARI_DIGITS)))

    unique_sutra_ids = dedupe(sutra_ids)
    source: dict[str, Any] = {
        "id": source_id,
        "label": SOURCE_LABELS.get(source_id, pdf_path.stem),
        "file_name": pdf_path.name,
        "sha256": sha256(pdf_path),
        "page_count": len(reader.pages),
        "text_char_count": text_char_count,
        "outline": [entry.to_json() for entry in outline_entries(reader)],
    }

    if source_id == "ashtadhyayi":
        source["sutra_index"] = {
            "count": len(unique_sutra_ids),
            "first": unique_sutra_ids[0] if unique_sutra_ids else None,
            "last": unique_sutra_ids[-1] if unique_sutra_ids else None,
            "by_pada": dict(sorted(Counter(sid.rsplit(".", 1)[0] for sid in unique_sutra_ids).items())),
            "ids": unique_sutra_ids,
        }

    return source


def build_obligations(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    obligations: list[dict[str, Any]] = []
    for source in sources:
        outline_stack: list[str] = []
        for entry in source["outline"]:
            level = entry["level"]
            outline_stack = outline_stack[:level]
            outline_stack.append(entry["title"])
            status = "partial" if is_partial_topic(entry["title"]) else "pending_design"
            obligations.append(
                {
                    "id": f"topic:{source['id']}:{slugify('/'.join(outline_stack))}",
                    "kind": "topic",
                    "source": source["id"],
                    "title": entry["title"],
                    "path": outline_stack.copy(),
                    "page": entry["page"],
                    "status": status,
                    "implementation_note": implementation_note(status, entry["title"]),
                }
            )

        for sutra_id in source.get("sutra_index", {}).get("ids", []):
            status = sutra_status(sutra_id)
            obligations.append(
                {
                    "id": f"sutra:{source['id']}:{sutra_id}",
                    "kind": "sutra",
                    "source": source["id"],
                    "title": sutra_id,
                    "path": [sutra_id],
                    "page": None,
                    "status": status,
                    "implementation_note": sutra_note(sutra_id, status),
                }
            )

    return obligations


def summarize_obligations(obligations: list[dict[str, Any]]) -> dict[str, Any]:
    by_status = Counter(item["status"] for item in obligations)
    by_kind = Counter(item["kind"] for item in obligations)
    return {
        "total": len(obligations),
        "by_status": dict(sorted(by_status.items())),
        "by_kind": dict(sorted(by_kind.items())),
    }


def implementation_note(status: str, title: str) -> str:
    if status == "partial":
        if title in TOPIC_IMPLEMENTATION_NOTES:
            return TOPIC_IMPLEMENTATION_NOTES[title]
        treatment = treatment_for(title)
        if treatment is not None:
            return f"Canon topic treatment: {treatment.note}."
        return f"Initial subsystem support covers part of this topic: {title}."
    return "Indexed from the source outline; not implemented yet."


def is_partial_topic(title: str) -> bool:
    return title in PARTIAL_TOPIC_TITLES or treatment_for(title) is not None


def sutra_status(sutra_id: str) -> str:
    if sutra_id in IMPLEMENTED_SUTRA_IDS:
        return "implemented"
    if sutra_id in PARTIAL_SUTRA_IDS:
        return "partial"
    if sutra_id.rsplit(".", 1)[0] in BATCHED_PADA_PREFIXES:
        return "batch_partial"
    return "pending_design"


def sutra_note(sutra_id: str, status: str) -> str:
    if status == "implemented":
        return IMPLEMENTED_SUTRA_IDS[sutra_id]
    if sutra_id in PARTIAL_SUTRA_IDS:
        return PARTIAL_SUTRA_IDS[sutra_id]
    pada = sutra_id.rsplit(".", 1)[0]
    if status == "batch_partial":
        return BATCHED_PADA_PREFIXES[pada]
    return "Indexed as an Aṣṭādhyāyī requirement; not individually implemented yet."


def slugify(value: str) -> str:
    parts = re.findall(r"[\w]+", value.lower(), flags=re.UNICODE)
    return "-".join(parts) if parts else "untitled"


def outline_entries(reader: PdfReader) -> list[OutlineEntry]:
    entries: list[OutlineEntry] = []

    def walk(items: list[Any], level: int) -> None:
        for item in items:
            if isinstance(item, list):
                walk(item, level + 1)
                continue
            title = str(getattr(item, "title", item)).strip()
            try:
                page = reader.get_destination_page_number(item) + 1
            except Exception:
                page = None
            entries.append(OutlineEntry(title=title, level=level, page=page))

    walk(getattr(reader, "outline", []) or [], 0)
    return entries


def dedupe(items: list[str]) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        unique.append(item)
    return unique


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def render_markdown(canon: dict[str, Any]) -> str:
    lines = [
        "# Grammar Canon",
        "",
        "Generated from the local PDFs in `sources/` by `tools/build_grammar_canon.py`.",
        "",
        "This file is the project contract for the user's requirement that Sanskript use all grammar from the supplied PDFs. It records the canon without copying the full PDF text.",
        "",
        "## Policy",
        "",
        "- Every indexed topic or sutra identifier is a language-design requirement.",
        "- A topic starts as `pending_design` unless code and tests explicitly cover it.",
        "- The language is not complete until this canon is implemented or consciously scoped with a documented reason.",
        "",
        "## Sources",
        "",
        "| Source | Pages | Text chars | Indexed items | SHA-256 |",
        "| --- | ---: | ---: | ---: | --- |",
    ]

    for source in canon["sources"]:
        indexed_items = len(source.get("outline", [])) + len(source.get("sutra_index", {}).get("ids", []))
        lines.append(
            f"| {source['label']} | {source['page_count']} | {source['text_char_count']} | "
            f"{indexed_items} | `{source['sha256'][:12]}...` |"
        )

    summary = canon["coverage_summary"]
    lines.extend(
        [
            "",
            "## Coverage Summary",
            "",
            f"- Total obligations: `{summary['total']}`",
            f"- Topic obligations: `{summary['by_kind'].get('topic', 0)}`",
            f"- Sutra obligations: `{summary['by_kind'].get('sutra', 0)}`",
            f"- Implemented: `{summary['by_status'].get('implemented', 0)}`",
            f"- Partial: `{summary['by_status'].get('partial', 0)}`",
            f"- Batch partial: `{summary['by_status'].get('batch_partial', 0)}`",
            f"- Pending design: `{summary['by_status'].get('pending_design', 0)}`",
        ]
    )

    lines.extend(["", "## Aṣṭādhyāyī Sutra Index", ""])
    ashtadhyayi = next((source for source in canon["sources"] if source["id"] == "ashtadhyayi"), None)
    if ashtadhyayi:
        sutra_index = ashtadhyayi["sutra_index"]
        lines.extend(
            [
                f"- Sutra identifiers indexed: `{sutra_index['count']}`",
                f"- First identifier: `{sutra_index['first']}`",
                f"- Last identifier: `{sutra_index['last']}`",
                "",
                "| Pāda | Count |",
                "| --- | ---: |",
            ]
        )
        for pada, count in sutra_index["by_pada"].items():
            lines.append(f"| `{pada}` | {count} |")

    lines.extend(["", "## Outline Topics", ""])
    for source in canon["sources"]:
        lines.extend([f"### {source['label']}", ""])
        for entry in source["outline"]:
            indent = "  " * entry["level"]
            page = f"p. {entry['page']}" if entry["page"] is not None else "page unknown"
            status = "partial" if is_partial_topic(entry["title"]) else "pending_design"
            lines.append(f"{indent}- `{page}` {entry['title']} — `{status}`")
        lines.append("")

    lines.extend(
        [
            "## Current Truth Gate",
            "",
            "The current interpreter has runnable Sanskrit-aware subsystems, but no Aṣṭādhyāyī sutra is marked `implemented` until it has discrete Paninian executable logic:",
            "",
            "- Adhyāya 1 has executable helper anchors and semantic scaffolds, but the sutras are `partial` until each one has exact source text, inherited domain, conditions, exceptions, rule-specific executable behavior, positive tests, and negative tests;",
            "- Adhyāya 2 has source-text metadata records, but those records are `partial` because metadata is not executable sutra logic;",
            "- Adhyāya 3 through 6 are currently `partial` scaffolds, not complete implementations;",
            "- finite present third-person singular parasmaipada verb frames for assignment, increase, decrease, and display;",
            "- karman, karaṇa, and adhikaraṇa role recovery from controlled forms;",
            "- small cardinal numerals 0 through 10 in object and instrumental roles;",
            "- controlled nominal storage names `phala`, `mūlya`, and `pada`.",
            "",
            "Everything else in this canon remains a tracked requirement.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
