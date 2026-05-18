from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
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
    "Pronominal adjectives",
    "Romanized Sanskrit",
    "Semivowels",
    "Short and long vowels",
    "The Shiva Sutras",
    "The sandhi system",
    "The sound system",
    "The compound system",
    "The suffix system",
    "tatpuruṣa",
    "taddhita",
    "Vowel sandhi",
    "Vowels",
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
}


BATCHED_PADA_PREFIXES = {
    "1.1": "sound definitions and technical terms are now handled by the phonology/pratyāhāra subsystem at batch level.",
    "1.4": "kāraka, saṃjñā, and nominal role infrastructure now exist at batch level.",
    "2.1": "compound and nominal-relation infrastructure now exists at batch level.",
    "2.2": "compound and nominal-relation infrastructure now exists at batch level.",
    "2.3": "vibhakti/kāraka infrastructure now exists at batch level.",
    "2.4": "subanta and inflectional infrastructure now exists at batch level.",
    "3.1": "tiṅanta, dhātu, lakāra, and pratyaya infrastructure now exists at batch level.",
    "3.2": "verbal/participial derivation infrastructure now exists at batch level.",
    "3.3": "verbal suffix infrastructure now exists at batch level.",
    "3.4": "tiṅ, lakāra, and voice/person-number infrastructure now exists at batch level.",
    "4.1": "kṛt/taddhita and derivational registry infrastructure now exists at batch level.",
    "4.2": "kṛt/taddhita and derivational registry infrastructure now exists at batch level.",
    "4.3": "kṛt/taddhita and derivational registry infrastructure now exists at batch level.",
    "4.4": "kṛt/taddhita and derivational registry infrastructure now exists at batch level.",
    "5.1": "taddhita registry infrastructure now exists at batch level.",
    "5.2": "taddhita registry infrastructure now exists at batch level.",
    "5.3": "taddhita registry infrastructure now exists at batch level.",
    "5.4": "taddhita, compounds, and nominal suffix infrastructure now exists at batch level.",
    "6.1": "vowel sandhi and sound-change infrastructure now exist at batch level.",
    "8.2": "consonant/visarga sandhi infrastructure now exists at batch level.",
    "8.3": "visarga and sibilant sandhi infrastructure now exists at batch level.",
    "8.4": "late sound-change infrastructure now exists at batch level.",
}


PARTIAL_SUTRA_IDS = {
    "1.1.1": "Initial vṛddhi sound classifier implemented; full rule interaction is pending.",
    "1.1.2": "Initial guṇa sound classifier implemented; full rule interaction is pending.",
    "1.1.9": "Conservative savarṇa helper implemented for vowel length pairs; full articulation-effort model is pending.",
}


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
                "implemented": "Implemented in code and covered by tests.",
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
            status = "partial" if entry["title"] in PARTIAL_TOPIC_TITLES else "pending_design"
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
        return f"Initial phonology support covers part of this topic: {title}."
    return "Indexed from the source outline; not implemented yet."


def sutra_status(sutra_id: str) -> str:
    if sutra_id in PARTIAL_SUTRA_IDS:
        return "partial"
    if sutra_id.rsplit(".", 1)[0] in BATCHED_PADA_PREFIXES:
        return "batch_partial"
    return "pending_design"


def sutra_note(sutra_id: str, status: str) -> str:
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
            status = "partial" if entry["title"] in PARTIAL_TOPIC_TITLES else "pending_design"
            lines.append(f"{indent}- `{page}` {entry['title']} — `{status}`")
        lines.append("")

    lines.extend(
        [
            "## Current Implemented Slice",
            "",
            "The current interpreter implements only a tiny slice of the canon:",
            "",
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
