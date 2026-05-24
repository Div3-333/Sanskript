"""Render generated documentation from the live grammar register."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from .grammar import CONTROLLED_NOUNS, NUMERAL_FORMS, VERB_FRAMES
from .grammar_register import runtime_register_entries
from .vocabulary_catalog import vocabulary_stats


def render_register_sync() -> str:
    runtime_entries = runtime_register_entries()
    counts = Counter(entry.construction_id or "unclassified" for entry in runtime_entries)
    stats = vocabulary_stats()

    lines = [
        "# Grammar Register Sync",
        "",
        "This file is generated from the live Sanskript grammar register. Run",
        "`python scripts/export_grammar_register.py` after changing controlled nouns,",
        "verb frames, numerals, avyayas, or runtime derivation entries.",
        "",
        "## Runtime Register",
        "",
        f"- Runtime entries: `{len(runtime_entries)}`",
        f"- Controlled verb frames: `{len(VERB_FRAMES)}`",
        f"- Controlled nominal stems: `{len(CONTROLLED_NOUNS)}`",
        f"- Controlled numeral forms: `{len(NUMERAL_FORMS)}`",
        f"- Graduate vocabulary stems: `{stats['noun_stems']}` nouns, `{stats['verb_roots']}` dhātus",
        "",
        "## Construction Counts",
        "",
        "| Construction | Entries |",
        "| --- | ---: |",
    ]
    for construction_id, count in sorted(counts.items()):
        lines.append(f"| `{construction_id}` | {count} |")

    lines.extend(
        [
            "",
            "## Verb Frames",
            "",
            "| Surface | Lemma | Operation | Required Roles | Construction |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for frame in sorted(VERB_FRAMES.values(), key=lambda item: item.surface):
        roles = ", ".join(sorted(role.value for role in frame.required_roles))
        lines.append(
            f"| `{frame.surface}` | `{frame.lemma}` | `{frame.operation.value}` | "
            f"{roles} | `{frame.construction_id}` |"
        )

    lines.extend(
        [
            "",
            "## Controlled Nominal Stems",
            "",
            "| Lemma | Gender | Forms |",
            "| --- | --- | --- |",
        ]
    )
    for stem in CONTROLLED_NOUNS:
        forms = ", ".join(f"`{form.surface}`" for form in stem.forms)
        lines.append(f"| `{stem.lemma}` | {stem.gender.value} | {forms} |")

    lines.append("")
    return "\n".join(lines)


def write_register_sync(path: Path | None = None) -> Path:
    root = Path(__file__).resolve().parents[2]
    output = path or root / "docs" / "grammar-register.generated.md"
    output.write_text(render_register_sync(), encoding="utf-8")
    return output


__all__ = ["render_register_sync", "write_register_sync"]
