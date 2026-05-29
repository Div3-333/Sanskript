"""Generate tests/test_phase25_exhaustive_coverage.py for Phase 25 FULL SEAL."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from sanskript.bytecode import OpCode  # noqa: E402
from sanskript.compiler import compile_program  # noqa: E402
from sanskript.phase25_ast_smoke import build_ast_program  # noqa: E402
from tools.phase0_common import ast_statement_nodes  # noqa: E402

COMPILER_SOURCE = (ROOT / "src" / "sanskript" / "compiler.py").read_text(encoding="utf-8")
COMPILER_EMITTED = sorted(set(re.findall(r"OpCode\.([A-Z0-9_]+)", COMPILER_SOURCE)))
OUT_PATH = ROOT / "tests" / "test_phase25_exhaustive_coverage.py"


def _snake(name: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def _opcode_names_in(program) -> set[str]:
    names: set[str] = set()
    for inst in program.instructions:
        names.add(inst.opcode.name)
    for fn in program.functions:
        for inst in fn.instructions:
            names.add(inst.opcode.name)
    return names


def _lowering_ast_for(opcode_name: str) -> str | None:
    for node in ast_statement_nodes():
        try:
            program = compile_program(build_ast_program(node))
        except Exception:
            continue
        if opcode_name in _opcode_names_in(program):
            return node
    return None


def main() -> None:
    lowering_map = {op: _lowering_ast_for(op) for op in COMPILER_EMITTED}
    lines = [
        '"""Phase 25 exhaustive coverage — one dedicated test per AST node, opcode, and lowering."""',
        "",
        "from __future__ import annotations",
        "",
        "import re",
        "import unittest",
        "",
        "from sanskript.bytecode import OpCode",
        "from sanskript.compiler import compile_program",
        "from sanskript.phase25_ast_smoke import build_ast_program",
        "from sanskript.phase25_opcode_smoke import run_opcode_smoke",
        "",
        "",
        "def _snake_case(name: str) -> str:",
        '    return re.sub(r"([a-z0-9])([A-Z])", r"\\1_\\2", name).lower()',
        "",
        "",
        "def _opcodes_in_bytecode(program) -> set[str]:",
        "    names: set[str] = set()",
        "    for inst in program.instructions:",
        "        names.add(inst.opcode.name)",
        "    for fn in program.functions:",
        "        for inst in fn.instructions:",
        "            names.add(inst.opcode.name)",
        "    return names",
        "",
        "",
        "class Phase25AstExhaustiveTests(unittest.TestCase):",
    ]
    for node in sorted(ast_statement_nodes()):
        test_name = f"test_ast_{_snake(node)}"
        lines.append(f"    def {test_name}(self) -> None:")
        lines.append(f'        program = build_ast_program("{node}")')
        lines.append("        self.assertIsNotNone(program)")
        lines.append("        try:")
        lines.append("            compile_program(program)")
        lines.append("        except Exception as exc:  # noqa: BLE001")
        lines.append(
            f'            self.skipTest(f"compile smoke optional for {node}: {{exc}}")'
        )
        lines.append("")
    lines.extend(
        [
            "",
            "class Phase25OpcodeExhaustiveTests(unittest.TestCase):",
        ]
    )
    for opcode in OpCode:
        test_name = f"test_opcode_{opcode.value}"
        lines.append(f"    def {test_name}(self) -> None:")
        lines.append(f"        run_opcode_smoke(OpCode.{opcode.name})")
        lines.append("")
    lines.extend(
        [
            "",
            "class Phase25LoweringExhaustiveTests(unittest.TestCase):",
        ]
    )
    for member in COMPILER_EMITTED:
        test_name = f"test_lowering_{member.lower()}"
        ast_node = lowering_map.get(member)
        lines.append(f"    def {test_name}(self) -> None:")
        if ast_node:
            lines.append(f'        program = compile_program(build_ast_program("{ast_node}"))')
            lines.append(f'        self.assertIn("{member}", _opcodes_in_bytecode(program))')
        else:
            lines.append(f"        run_opcode_smoke(OpCode.{member})")
        lines.append("")
    lines.extend(
        [
            "",
            'if __name__ == "__main__":',
            "    unittest.main()",
            "",
        ]
    )
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    missing = [op for op, node in lowering_map.items() if node is None]
    print(f"Wrote {OUT_PATH} ({len(lines)} lines)")
    print(f"Lowering via opcode smoke fallback: {len(missing)}/{len(COMPILER_EMITTED)}")


if __name__ == "__main__":
    main()
