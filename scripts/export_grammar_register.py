"""Export the live grammar register to docs/grammar-register.generated.md."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sanskript.register_docs import write_register_sync  # noqa: E402


def main() -> int:
    output = write_register_sync()
    print(f"Wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
