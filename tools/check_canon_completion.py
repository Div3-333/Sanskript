from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANON_PATH = ROOT / "data" / "grammar_canon.json"
COMPLETE_STATUSES = {"implemented"}


def load_obligations() -> list[dict[str, object]]:
    canon = json.loads(CANON_PATH.read_text(encoding="utf-8"))
    return list(canon["obligations"])


def completion_counts(obligations: list[dict[str, object]]) -> Counter[str]:
    return Counter(str(item["status"]) for item in obligations)


def incomplete_obligations(obligations: list[dict[str, object]]) -> list[dict[str, object]]:
    return [item for item in obligations if item["status"] not in COMPLETE_STATUSES]


def main() -> int:
    obligations = load_obligations()
    incomplete = incomplete_obligations(obligations)
    counts = completion_counts(obligations)

    print("Canon completion gate")
    for status, count in sorted(counts.items()):
        print(f"{status}: {count}")

    if incomplete:
        print(f"BLOCKED: {len(incomplete)} canon obligations are not fully implemented.")
        return 1

    print("OK: every canon obligation is fully implemented.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
