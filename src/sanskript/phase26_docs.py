"""Phase 26 documentation helpers: cookbook registry and API doc rendering."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .compiler import compile_source
from .errors import SanskriptError
from .module_loader import load_program_from_path
from .type_checker import TypeChecker, check_program

ROOT = Path(__file__).resolve().parents[2]
COOKBOOK_DIR = ROOT / "examples" / "cookbook"
GENERATED_DIR = ROOT / "docs" / "generated"
DOCS_DIR = ROOT / "docs"

MARKDOWN_LINK_RE = re.compile(r"\]\(([^)]+)\)")


@dataclass(frozen=True)
class CookbookRecipe:
    slug: str
    title: str
    source: Path
    expected_output: tuple[str, ...]
    summary: str


COOKBOOK_RECIPES: tuple[CookbookRecipe, ...] = (
    CookbookRecipe(
        slug="hello-counter",
        title="Hello counter (assign, add, display)",
        source=COOKBOOK_DIR / "hello-counter.ssk",
        expected_output=("7",),
        summary="Classic calculator frame: place five, add two, show seven.",
    ),
    CookbookRecipe(
        slug="scaled-sum",
        title="Scaled sum (two increments)",
        source=COOKBOOK_DIR / "scaled-sum.ssk",
        expected_output=("7",),
        summary="Bind three, add four in the instrument role, display.",
    ),
    CookbookRecipe(
        slug="conditional-branch",
        title="Conditional branch (yadi / anyathā)",
        source=COOKBOOK_DIR / "conditional-branch.ssk",
        expected_output=("13",),
        summary="Multiply by ten when equal to three, otherwise add one.",
    ),
    CookbookRecipe(
        slug="greet",
        title="Text greeting (iti quotative)",
        source=COOKBOOK_DIR / "greet.ssk",
        expected_output=("svāgatam mitra",),
        summary="Store a text value without quotes; display it.",
    ),
    CookbookRecipe(
        slug="web-hello",
        title="Web hello (route match + template render)",
        source=COOKBOOK_DIR / "web-hello.ssk",
        expected_output=("<h1>Hello</h1>",),
        summary="std.web.route_match and std.web.render; host-backed, not HTTP.",
    ),
    CookbookRecipe(
        slug="cli-sqrt",
        title="CLI/stdlib math (sqrt)",
        source=COOKBOOK_DIR / "cli-sqrt.ssk",
        expected_output=("4.0",),
        summary="stdlib math from a one-liner; see guide-cli-apps.md.",
    ),
    CookbookRecipe(
        slug="desktop-plan",
        title="Desktop GUI capability plan (JSON)",
        source=COOKBOOK_DIR / "desktop-plan.ssk",
        expected_output=(
            '{"clipboard":true,"file_dialogs":true,"host_bridge":true,'
            '"implementation_state":"host_substitute","menus":true,'
            '"notes":["Desktop GUI uses host simulation until native windowing lands"],'
            '"notifications":true,"phase":22,"shortcuts":true,'
            '"substitute":"std.gui.simulate","tier":"host_substitute",'
            '"widgets":["button","label","text_field","checkbox"]}',
        ),
        summary="std.gui.capabilities_plan serialized; simulation only.",
    ),
    CookbookRecipe(
        slug="game-input",
        title="Game input state (host-backed)",
        source=COOKBOOK_DIR / "game-input.ssk",
        expected_output=('{"any":true,"pressed":{"jump":true}}',),
        summary="std.game.input_state; not a shipped game loop product.",
    ),
    CookbookRecipe(
        slug="research-spark",
        title="Research sparkline",
        source=COOKBOOK_DIR / "research-spark.ssk",
        expected_output=("▁▃▅▆█",),
        summary="std.plot.sparkline over a small series.",
    ),
    CookbookRecipe(
        slug="ml-dot",
        title="ML/linear algebra dot product",
        source=COOKBOOK_DIR / "ml-dot.ssk",
        expected_output=("25.0",),
        summary="std.linalg.dot; tensor/ML roadmap uses same host bridge.",
    ),
    CookbookRecipe(
        slug="functional-call",
        title="Functional procedure call",
        source=COOKBOOK_DIR / "functional-call.ssk",
        expected_output=("15",),
        summary="vidhānam + āhvānam without list combinators.",
    ),
    CookbookRecipe(
        slug="systems-tier",
        title="Safety tier declaration",
        source=COOKBOOK_DIR / "systems-tier.ssk",
        expected_output=("surakṣita",),
        summary="surakṣitam tier smoke; see guide-systems-programming.md.",
    ),
)

API_DEMO_SOURCE = COOKBOOK_DIR / "api-demo.ssk"
API_DEMO_GENERATED = GENERATED_DIR / "cookbook-api-demo.docs.md"

# Phase 26 learning-path inventory rows (27); all must be **done** when sealed.
PHASE26_CHECKLIST_ITEMS: tuple[str, ...] = (
    "Beginner tutorial",
    "Prose syntax guide",
    "Sanskrit grammar mapping",
    "Python migration",
    "Rust migration",
    "Standard library reference",
    "Type system reference",
    "Object model reference",
    "Functional programming guide",
    "Systems programming guide",
    "Machine programming guide",
    "Web app guide",
    "CLI guide",
    "Desktop app guide",
    "Game development guide",
    "Data/research scripting guide",
    "ML guide",
    "Compiler architecture guide",
    "VM architecture guide",
    "Bytecode reference",
    "sskyp reference",
    "Package manager guide",
    "Tooling guide",
    "Contributing guide",
    "Style guide",
    "Cookbook",
    "API docs from source",
    "Visual HTML learning guide",
)

PHASE26_DOMAIN_GUIDES: tuple[Path, ...] = (
    DOCS_DIR / "guide-grammar-primer.md",
    DOCS_DIR / "guide-stdlib-reference.md",
    DOCS_DIR / "guide-functional.md",
    DOCS_DIR / "guide-machine-programming.md",
    DOCS_DIR / "guide-cli-apps.md",
    DOCS_DIR / "guide-desktop-apps.md",
    DOCS_DIR / "guide-game-development.md",
    DOCS_DIR / "guide-data-research.md",
    DOCS_DIR / "guide-ml.md",
    DOCS_DIR / "guide-compiler-architecture.md",
    DOCS_DIR / "guide-vm-architecture.md",
    DOCS_DIR / "guide-sskyp-reference.md",
    DOCS_DIR / "guide-web-apps.md",
    DOCS_DIR / "guide-systems-programming.md",
)

PHASE26_MARKDOWN_FILES: tuple[Path, ...] = (
    DOCS_DIR / "phase26-documentation-learning-path.md",
    DOCS_DIR / "tutorial-beginner.md",
    DOCS_DIR / "migration-from-python.md",
    DOCS_DIR / "migration-from-rust.md",
    DOCS_DIR / "cookbook.md",
    DOCS_DIR / "tooling.md",
    DOCS_DIR / "api-from-source.md",
    DOCS_DIR / "contributing.md",
    *PHASE26_DOMAIN_GUIDES,
)


def _format_function_signature(fn: object, checker: TypeChecker) -> str:
    from .ast import FunctionDef

    assert isinstance(fn, FunctionDef)
    param_parts: list[str] = []
    for index, name in enumerate(fn.params):
        ty = "unknown"
        if index < len(fn.param_types) and fn.param_types[index]:
            ty = fn.param_types[index]
        param_parts.append(f"{name}: {ty}")
    param_str = ", ".join(param_parts) if param_parts else "(none)"
    if fn.return_type:
        ret = fn.return_type
    else:
        ret = checker._type_name(checker.get_inferred_return_type(fn.name))
    return f"`{fn.name}`({param_str}) → `{ret}`"


def render_source_api_markdown(source: Path) -> str:
    program = load_program_from_path(source)
    check_program(program)
    checker = TypeChecker(program)
    checker.check()
    lines = [f"# API for `{source.name}`", "", "## Modules", ""]
    if program.modules:
        lines.extend([f"- `{module.name}`" for module in program.modules])
    else:
        lines.append("- (none)")
    lines.extend(["", "## Functions", ""])
    if program.functions:
        for fn in program.functions:
            lines.append(f"- {_format_function_signature(fn, checker)}")
    else:
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)


def write_cookbook_api_doc(path: Path | None = None) -> Path:
    target = path or API_DEMO_GENERATED
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_source_api_markdown(API_DEMO_SOURCE), encoding="utf-8")
    return target


def iter_markdown_links(text: str) -> list[str]:
    links: list[str] = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        links.append(target.split("#", 1)[0])
    return links


def resolve_doc_link(doc_path: Path, target: str) -> Path:
    return (doc_path.parent / target).resolve()


def phase26_inventory_done_count(inventory_text: str) -> int:
    return len(re.findall(r"\|\s\*\*done\*\*\s\|", inventory_text))


PHASE26_MIN_GUIDE_WORDS = 200

# Every independence-checklist [x] markdown guide (27); HTML visual guide is separate.
PHASE26_CHECKED_GUIDES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("tutorial-beginner.md", ("examples/cookbook/hello-counter.ssk",)),
    ("core-syntax.md", ("examples/dvādaśa-phase2-boolean.ssk",)),
    ("guide-grammar-primer.md", ("examples/cookbook/hello-counter.ssk",)),
    ("migration-from-python.md", ("examples/cookbook/hello-counter.ssk",)),
    ("migration-from-rust.md", ("examples/cookbook/hello-counter.ssk",)),
    ("guide-stdlib-reference.md", ("examples/cookbook/cli-sqrt.ssk",)),
    ("type-system-reference.md", ("examples/phase3-data-types.ssk",)),
    ("object-oriented.md", ("examples/phase7-oop.ssk",)),
    ("guide-functional.md", ("examples/cookbook/functional-call.ssk",)),
    ("guide-systems-programming.md", ("examples/cookbook/systems-tier.ssk",)),
    ("guide-machine-programming.md", ("examples/cookbook/hello-counter.ssk",)),
    ("guide-web-apps.md", ("examples/cookbook/web-hello.ssk",)),
    ("guide-cli-apps.md", ("examples/cookbook/cli-sqrt.ssk",)),
    ("guide-desktop-apps.md", ("examples/cookbook/desktop-plan.ssk",)),
    ("guide-game-development.md", ("examples/cookbook/game-input.ssk",)),
    ("guide-data-research.md", ("examples/cookbook/research-spark.ssk",)),
    ("guide-ml.md", ("examples/cookbook/ml-dot.ssk",)),
    ("guide-compiler-architecture.md", ("examples/cookbook/hello-counter.ssk",)),
    ("guide-vm-architecture.md", ("examples/cookbook/hello-counter.ssk",)),
    ("bytecode-v1.md", ("examples/cookbook/hello-counter.ssk",)),
    ("bytecode-v2.md", ("examples/caturtha.ssk",)),
    ("guide-sskyp-reference.md", ("examples/cookbook/hello-counter.ssk",)),
    ("modules-packages.md", ("examples/phase6-functions.ssk",)),
    ("tooling.md", ("examples/cookbook/hello-counter.ssk",)),
    ("contributing.md", ("examples/cookbook/api-demo.ssk",)),
    ("style-guide.md", ("examples/prathama.ssk",)),
    ("cookbook.md", (
        "examples/cookbook/hello-counter.ssk",
        "examples/cookbook/scaled-sum.ssk",
        "examples/cookbook/conditional-branch.ssk",
        "examples/cookbook/greet.ssk",
        "examples/cookbook/web-hello.ssk",
    )),
    ("api-from-source.md", ("examples/cookbook/api-demo.ssk",)),
)

EXAMPLE_PATH_RE = re.compile(r"examples/[^\s`)\"']+\.ssk")


def count_guide_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text, flags=re.UNICODE))


def guide_has_fenced_example(text: str) -> bool:
    return bool(re.search(r"```(?:ssk|sanskrit)?\s", text) or re.search(r"```\s*\n", text))


def _example_compiles(rel_path: str) -> bool:
    path = (ROOT / rel_path.replace("/", "\\")).resolve()
    if not path.is_file():
        return False
    try:
        compile_source(path.read_text(encoding="utf-8"))
        return True
    except SanskriptError:
        return False


def audit_checked_guide(name: str, examples: tuple[str, ...]) -> dict[str, object]:
    path = DOCS_DIR / name
    issues: list[str] = []
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    word_count = count_guide_words(text)
    if word_count < PHASE26_MIN_GUIDE_WORDS:
        issues.append(f"word_count {word_count} < {PHASE26_MIN_GUIDE_WORDS}")
    if not guide_has_fenced_example(text):
        issues.append("missing fenced code example")
    examples_compile = {rel: _example_compiles(rel) for rel in examples}
    for rel, ok in examples_compile.items():
        if not ok:
            issues.append(f"example does not compile: {rel}")
    return {
        "guide": name,
        "doc_exists": path.is_file(),
        "word_count": word_count,
        "min_words": PHASE26_MIN_GUIDE_WORDS,
        "has_fenced_example": guide_has_fenced_example(text),
        "runnable_examples": list(examples),
        "examples_compile": examples_compile,
        "example_paths_in_doc": EXAMPLE_PATH_RE.findall(text),
        "ok": path.is_file() and not issues,
        "issues": issues,
    }


def _cookbook_compile_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for recipe in COOKBOOK_RECIPES:
        rel = str(recipe.source.relative_to(ROOT)).replace("\\", "/")
        rows.append({"slug": recipe.slug, "source": rel, "compiles": _example_compiles(rel)})
    return rows


def _inventory_honesty() -> dict[str, object]:
    inventory_path = DOCS_DIR / "phase26-documentation-learning-path.md"
    text = inventory_path.read_text(encoding="utf-8")
    inflated: list[str] = []
    for name, _examples in PHASE26_CHECKED_GUIDES:
        if f"| {name.replace('.md', '')} " in text or name in text:
            row = audit_checked_guide(name, _examples)
            if not row["ok"]:
                inflated.append(name)
    return {
        "inventory_path": str(inventory_path.relative_to(ROOT)),
        "inflated_done_rows": inflated,
        "ok": not inflated,
    }


def build_phase26_evidence() -> dict[str, object]:
    checked = [audit_checked_guide(name, examples) for name, examples in PHASE26_CHECKED_GUIDES]
    return {
        "phase": 26,
        "checked_guides": checked,
        "cookbook": _cookbook_compile_rows(),
        "inventory_honesty": _inventory_honesty(),
        "learning_path_files": [str(p.relative_to(ROOT)).replace("\\", "/") for p in PHASE26_MARKDOWN_FILES],
        "seal_verdict": phase26_seal_verdict(
            {
                "checked_guides": checked,
                "cookbook": _cookbook_compile_rows(),
                "inventory_honesty": _inventory_honesty(),
            }
        ),
    }


def phase26_seal_verdict(evidence: dict[str, object]) -> dict[str, object]:
    blockers: list[str] = []
    checked = evidence.get("checked_guides") or []
    for row in checked:
        if not row.get("ok"):
            blockers.append(f"{row.get('guide')}: {row.get('issues')}")
    inventory = evidence.get("inventory_honesty") or {}
    if not inventory.get("ok"):
        blockers.append(f"inflated inventory rows: {inventory.get('inflated_done_rows')}")
    cookbook = evidence.get("cookbook") or []
    if any(not row.get("compiles") for row in cookbook):
        blockers.append("cookbook recipe failed compile smoke")
    expected_guides = len(PHASE26_CHECKED_GUIDES)
    if len(checked) != expected_guides:
        blockers.append(f"checked_guide_count {len(checked)} != {expected_guides}")
    seal_ready = not blockers
    return {
        "seal_ready": seal_ready,
        "harness_ready": True,
        "blockers": blockers,
        "warnings": [],
        "checked_guide_count": len(checked),
        "expected_guide_count": expected_guides,
        "repro_commands": [
            "PYTHONPATH=src python -m unittest tests.test_phase26_documentation -v",
            "PYTHONPATH=src python -m sanskript.cli phase26-evidence",
        ],
    }


def write_phase26_evidence(path: Path) -> Path:
    payload = build_phase26_evidence()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


__all__ = [
    "API_DEMO_GENERATED",
    "API_DEMO_SOURCE",
    "COOKBOOK_DIR",
    "COOKBOOK_RECIPES",
    "PHASE26_CHECKED_GUIDES",
    "PHASE26_CHECKLIST_ITEMS",
    "PHASE26_DOMAIN_GUIDES",
    "PHASE26_MARKDOWN_FILES",
    "PHASE26_MIN_GUIDE_WORDS",
    "audit_checked_guide",
    "build_phase26_evidence",
    "count_guide_words",
    "guide_has_fenced_example",
    "iter_markdown_links",
    "phase26_inventory_done_count",
    "phase26_seal_verdict",
    "render_source_api_markdown",
    "resolve_doc_link",
    "write_cookbook_api_doc",
    "write_phase26_evidence",
]
