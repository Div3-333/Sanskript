"""Patch schema-v2.json with Phase 8 opcodes."""

from __future__ import annotations

import json
from pathlib import Path

from sanskript.phase8_opcodes import all_phase8_opcode_names

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "data" / "bytecode" / "schema-v2.json"


def main() -> None:
    data = json.loads(SCHEMA.read_text(encoding="utf-8"))
    existing = data["$defs"]["instruction"]["properties"]["op"]["enum"]
    merged = sorted(set(existing) | set(all_phase8_opcode_names()))
    data["$defs"]["instruction"]["properties"]["op"]["enum"] = merged
    SCHEMA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"schema opcodes: {len(merged)} (+{len(merged) - len(existing)})")


if __name__ == "__main__":
    main()
