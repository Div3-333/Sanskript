"""Phase 1: Sanskrit source surface (scripts, comments, formatter, linter)."""

from __future__ import annotations

import os
import unittest
from pathlib import Path

from sanskript import run
from sanskript.comments import strip_comments
from sanskript.errors import MorphologyError, ParseError
from sanskript.formatter import format_source
from sanskript.identifiers import IdentifierError, canonical_identifier
from sanskript.learning_mode import enrich_error, parse_learning_directive
from sanskript.linter import lint_source
from sanskript.parser import parse_program
from sanskript.script_normalize import (
    Script,
    detect_script,
    harvard_kyoto_to_iast,
    normalize_to_iast,
    slp1_to_iast,
    transliterate_for_diagnostics,
)
from sanskript.source_context import SourceSpan, span_at
from sanskript.source_pipeline import prepare_source

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


class Phase1SourceSurfaceTests(unittest.TestCase):
    def test_devanagari_example_runs(self) -> None:
        source = (EXAMPLES / "shodasha-devanagari.ssk").read_text(encoding="utf-8")
        self.assertEqual(run(source), ["7"])

    def test_harvard_kyoto_normalization(self) -> None:
        hk = "gaNakaH paJca phale nidadhAti."
        prepared = prepare_source(hk)
        self.assertEqual(detect_script(hk), Script.HARVARD_KYOTO)
        self.assertIn("gaṇakaḥ", prepared.text)

    def test_comments_stripped(self) -> None:
        source = "// व्याख्या: प्रारम्भः\ngaṇakaḥ eka phale nidadhāti.\n"
        stripped = strip_comments(source)
        self.assertEqual(len(stripped.comments), 1)
        self.assertNotIn("//", stripped.text)
        self.assertIn("nidadhāti", stripped.text)

    def test_formatter_one_sentence_per_line(self) -> None:
        messy = "gaṇakaḥ   pañca phale nidadhāti.  gaṇakaḥ phalaṃ darśayati"
        formatted = format_source(messy)
        lines = [line for line in formatted.splitlines() if line.strip()]
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].endswith("."))

    def test_linter_flags_choppy_sentence(self) -> None:
        findings = lint_source("phale pañca.")
        codes = {item.code for item in findings}
        self.assertIn("MISSING_VERB", codes)

    def test_parse_error_carries_span(self) -> None:
        with self.assertRaises(ParseError) as raised:
            parse_program("gaṇakaḥ pañca phale.")
        self.assertIsNotNone(raised.exception.span)

    def test_learning_mode_adds_hint(self) -> None:
        settings = parse_learning_directive("śikṣām.\ngaṇakaḥ pañca phale.")
        self.assertTrue(settings.enabled)
        err = ParseError("Expected exactly one finite verb, found 0 in 'gaṇakaḥ pañca phale'")
        enriched = enrich_error(err, original="śikṣām.", script=Script.IAST)
        self.assertIn("verb", (enriched.hint or "").lower())

    def test_token_provenance_and_span_at(self) -> None:
        text = "gaṇakaḥ pañca phale nidadhāti."
        span = span_at(text, 0, len("gaṇakaḥ"))
        self.assertEqual(span.line, 1)
        self.assertIn("gaṇakaḥ", span.snippet)

    def test_reversible_transliteration_roundtrip_iast_dev(self) -> None:
        iast = "gaṇakaḥ"
        dev = transliterate_for_diagnostics(iast, target=Script.DEVANAGARI)
        back = normalize_to_iast(dev).text
        self.assertEqual(back, iast)

    def test_slp1_to_iast_anusvara(self) -> None:
        self.assertEqual(slp1_to_iast("phala.m"), "phalaṃ")

    def test_prepare_source_strict_directive(self) -> None:
        prepared = prepare_source("paninianam.\ngaṇakaḥ pañca phale nidadhāti.")
        self.assertTrue(prepared.strict_paninian)

    def test_prepare_source_recovers_joined_sandhi_token(self) -> None:
        prepared = prepare_source("sandhīnam.\ngaṇakotra nidadhāti.")
        self.assertIn("gaṇakaḥ atra", prepared.text)

    def test_harvard_kyoto_sandhi_example_runs(self) -> None:
        source = (EXAMPLES / "phase1-script-sandhi.ssk").read_text(encoding="utf-8")
        self.assertEqual(run(source), ["1"])

    def test_devanagari_sandhi_example_runs(self) -> None:
        source = (EXAMPLES / "phase1-broad-script-sandhi.ssk").read_text(encoding="utf-8")
        self.assertEqual(run(source), ["3"])

    def test_morphology_error_in_learning_mode(self) -> None:
        prev = os.environ.pop("SANSKRIPT_LEARNING", None)
        os.environ["SANSKRIPT_LEARNING"] = "1"
        try:
            with self.assertRaises(MorphologyError) as raised:
                parse_program("śikṣām.\nnotasanskritform phale nidadhāti.")
            self.assertTrue(raised.exception.hint)
        finally:
            if prev is None:
                os.environ.pop("SANSKRIPT_LEARNING", None)
            else:
                os.environ["SANSKRIPT_LEARNING"] = prev

    def test_identifier_pipeline_rejects_operator_like_names(self) -> None:
        with self.assertRaises(IdentifierError):
            canonical_identifier("counter+")


class Phase1FormatterReparseTests(unittest.TestCase):
    """Formatted source must re-parse without error (round-trip quality gate)."""

    def test_formatted_source_reparses(self) -> None:
        source = "gaṇakaḥ pañca phale nidadhāti. gaṇakaḥ phalaṃ darśayati."
        formatted = format_source(source)
        self.assertTrue(formatted.strip(), "format_source returned empty string")
        try:
            parse_program(formatted)
        except Exception as exc:
            self.fail(f"Formatted source failed to re-parse: {exc}\nFormatted:\n{formatted}")

    def test_formatted_normalizes_whitespace(self) -> None:
        messy = "  gaṇakaḥ   pañca   phale  nidadhāti.  "
        formatted = format_source(messy)
        for line in formatted.splitlines():
            if line.strip():
                self.assertNotRegex(line, r"  ", "Double space left in formatted output")

    def test_formatted_ends_with_period(self) -> None:
        source = "gaṇakaḥ pañca phale nidadhāti"
        formatted = format_source(source)
        last_line = [l for l in formatted.splitlines() if l.strip()][-1]
        self.assertTrue(last_line.endswith(".") or last_line.endswith("।"))


class Phase1LinterRuleTests(unittest.TestCase):
    """Tests for individual lint rules."""

    def test_missing_verb_rule(self) -> None:
        findings = lint_source("gaṇakaḥ pañca phalaṃ.")
        codes = {f.code for f in findings}
        self.assertIn("MISSING_VERB", codes)

    def test_multiple_verbs_rule(self) -> None:
        from sanskript.grammar import PartOfSpeech
        from sanskript.morphology_facade import get_default_facade
        facade = get_default_facade()
        source = "gaṇakaḥ pañca phale nidadhāti darśayati."
        findings = lint_source(source)
        codes = {f.code for f in findings}
        self.assertIn("MULTIPLE_VERBS", codes)

    def test_choppy_sentence_rule(self) -> None:
        findings = lint_source("phale.")
        codes = {f.code for f in findings}
        self.assertIn("CHOPPY_SENTENCE", codes)

    def test_sparse_sentence_rule(self) -> None:
        findings = lint_source("phale pañca.")
        codes = {f.code for f in findings}
        self.assertIn("SPARSE_SENTENCE", codes)

    def test_lint_finding_has_line_number(self) -> None:
        source = "gaṇakaḥ pañca phale nidadhāti.\nphale."
        findings = lint_source(source)
        lines = {f.line for f in findings}
        self.assertIn(2, lines)


if __name__ == "__main__":
    unittest.main()
