"""Phase 26: documentation learning path, link integrity, runnable cookbook."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from sanskript.cli import main
from sanskript.compiler import compile_source
from sanskript.phase26_docs import (
    API_DEMO_GENERATED,
    API_DEMO_SOURCE,
    COOKBOOK_RECIPES,
    PHASE26_CHECKED_GUIDES,
    PHASE26_CHECKLIST_ITEMS,
    PHASE26_DOMAIN_GUIDES,
    PHASE26_MARKDOWN_FILES,
    build_phase26_evidence,
    iter_markdown_links,
    phase26_inventory_done_count,
    render_source_api_markdown,
    resolve_doc_link,
    write_cookbook_api_doc,
)
from sanskript.vm import SanskriptVM

ROOT = Path(__file__).resolve().parents[1]


class Phase26DocumentationTests(unittest.TestCase):
    def test_phase26_markdown_files_exist(self) -> None:
        for path in PHASE26_MARKDOWN_FILES:
            with self.subTest(doc=path.name):
                self.assertTrue(path.is_file(), f"missing {path}")

    def test_phase26_internal_links_resolve(self) -> None:
        missing: list[str] = []
        for doc_path in PHASE26_MARKDOWN_FILES:
            for target in iter_markdown_links(doc_path.read_text(encoding="utf-8")):
                resolved = resolve_doc_link(doc_path, target)
                if not resolved.exists():
                    missing.append(f"{doc_path.relative_to(ROOT)} -> {target}")
        self.assertEqual(missing, [])

    def test_phase26_inventory_all_items_done(self) -> None:
        inventory = (ROOT / "docs" / "phase26-documentation-learning-path.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(len(PHASE26_CHECKLIST_ITEMS), 28)
        self.assertEqual(phase26_inventory_done_count(inventory), 28)
        self.assertNotIn("**partial**", inventory)
        self.assertNotIn("**missing**", inventory)
        for item in PHASE26_CHECKLIST_ITEMS:
            with self.subTest(item=item):
                self.assertIn(item, inventory)

    def test_phase26_independence_checklist_all_checked(self) -> None:
        checklist = (ROOT / "docs" / "native-sanskript-independence-checklist.md").read_text(
            encoding="utf-8"
        )
        start = checklist.index("## Phase 26:")
        end = checklist.index("## Phase 27:", start)
        section = checklist[start:end]
        unchecked = re.findall(r"^- \[ \]", section, flags=re.MULTILINE)
        self.assertEqual(unchecked, [], f"unchecked Phase 26 rows: {unchecked}")

    def test_cookbook_recipes_compile_and_run(self) -> None:
        vm = SanskriptVM()
        for recipe in COOKBOOK_RECIPES:
            with self.subTest(recipe=recipe.slug):
                self.assertTrue(recipe.source.is_file())
                source = recipe.source.read_text(encoding="utf-8")
                output = vm.execute(compile_source(source))
                self.assertEqual(tuple(output), recipe.expected_output)

    def test_cookbook_recipes_compile_via_cli(self) -> None:
        for recipe in COOKBOOK_RECIPES:
            with self.subTest(recipe=recipe.slug):
                self.assertEqual(main(["compile", str(recipe.source)]), 0)

    def test_generated_cookbook_api_doc_matches_renderer(self) -> None:
        self.assertTrue(API_DEMO_SOURCE.is_file())
        expected = render_source_api_markdown(API_DEMO_SOURCE)
        if not API_DEMO_GENERATED.is_file():
            write_cookbook_api_doc()
        self.assertEqual(API_DEMO_GENERATED.read_text(encoding="utf-8"), expected)
        self.assertIn("dviguṇa", expected)
        self.assertIn("triṣṭaya", expected)
        self.assertIn("→ `i32`", expected)
        self.assertIn("a: i32", expected)
        self.assertIn("b: i32", expected)

    def test_cli_docs_command_matches_renderer(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "api.docs.md"
            self.assertEqual(main(["docs", str(API_DEMO_SOURCE), "-o", str(out)]), 0)
            self.assertEqual(
                out.read_text(encoding="utf-8"),
                render_source_api_markdown(API_DEMO_SOURCE),
            )

    def test_cookbook_md_links_to_examples(self) -> None:
        cookbook = ROOT / "docs" / "cookbook.md"
        text = cookbook.read_text(encoding="utf-8")
        for slug in (
            "hello-counter",
            "scaled-sum",
            "conditional-branch",
            "greet",
            "web-hello",
            "cli-sqrt",
            "desktop-plan",
            "game-input",
            "research-spark",
            "ml-dot",
            "functional-call",
            "systems-tier",
            "api-demo",
        ):
            self.assertIn(f"cookbook/{slug}.ssk", text)

    def test_checked_guides_are_not_stubs(self) -> None:
        """Brutal review: [x] checklist guides need >=200 words and fenced examples."""
        word_re = re.compile(r"\b\w+\b")
        for name, _examples in PHASE26_CHECKED_GUIDES:
            path = ROOT / "docs" / name
            with self.subTest(guide=name):
                text = path.read_text(encoding="utf-8")
                self.assertGreaterEqual(len(word_re.findall(text)), 200, name)
                self.assertIn("```", text, name)

    def test_phase26_seal_ready(self) -> None:
        evidence = build_phase26_evidence()
        seal = evidence["seal_verdict"]
        self.assertTrue(seal["seal_ready"], msg=seal.get("blockers"))
        self.assertEqual(seal["checked_guide_count"], len(PHASE26_CHECKED_GUIDES))
        self.assertTrue(evidence["inventory_honesty"]["ok"])
        for row in evidence["checked_guides"]:
            with self.subTest(guide=row["guide"]):
                self.assertTrue(row["ok"], msg=row.get("issues"))

    def test_tutorial_references_cookbook_paths(self) -> None:
        tutorial = (ROOT / "docs" / "tutorial-beginner.md").read_text(encoding="utf-8")
        self.assertIn("examples/cookbook/hello-counter.ssk", tutorial)

    def test_guide_html_canon_count_matches_runtime(self) -> None:
        for name in ("index.html", "reference.html"):
            html = (ROOT / "docs" / "guide" / name).read_text(encoding="utf-8")
            with self.subTest(guide=name):
                self.assertIn("3983 sutras", html)
                self.assertNotIn("3982 sutras", html)

    def test_phase26_inventory_mentions_checklist(self) -> None:
        inventory = (ROOT / "docs" / "phase26-documentation-learning-path.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Phase 26", inventory)
        self.assertIn("Cookbook", inventory)
        self.assertRegex(inventory, r"\*\*done\*\*|\*\*partial\*\*|\*\*missing\*\*")


class Phase26LinkHygieneTests(unittest.TestCase):
    """Broader link check for new guides pointing at repo files."""

    def test_migration_guides_do_not_reference_missing_examples(self) -> None:
        pattern = re.compile(r"\.\./examples/([^)\s]+)")
        for name in ("migration-from-python.md", "migration-from-rust.md"):
            doc = ROOT / "docs" / name
            for rel in pattern.findall(doc.read_text(encoding="utf-8")):
                target = (ROOT / "examples" / Path(rel)).resolve()
                with self.subTest(doc=name, example=rel):
                    self.assertTrue(target.exists(), f"{name} -> {rel}")


if __name__ == "__main__":
    unittest.main()
