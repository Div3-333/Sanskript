from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode
from sanskript.cli import main
from sanskript.compiler import compile_statements
from sanskript.diagnostics import diagnostic_from_error
from sanskript.errors import PanicError, RuntimeSanskriptError, ThrownError, TypeCheckError
from sanskript.ast import Display, Reference
from sanskript.source_context import SourceSpan
from sanskript.vm import SanskriptVM


class Phase12DiagnosticsTests(unittest.TestCase):
    def test_error_model_marks_recoverable_and_unrecoverable(self) -> None:
        self.assertTrue(ThrownError("recoverable").recoverable)
        self.assertFalse(PanicError("fatal").recoverable)

    def test_cli_json_diagnostics_for_compile_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.ssk"
            bad.write_text("asatya-vakyam.", encoding="utf-8")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(
                    [
                        "--diagnostics-format",
                        "json",
                        "compile",
                        str(bad),
                    ]
                )
            self.assertEqual(code, 1)
            payload = json.loads(stderr.getvalue().strip().splitlines()[0])
            self.assertIn("code", payload)
            self.assertEqual(payload["severity"], "error")
            self.assertIn("recoverable", payload)
            self.assertIn("notes", payload)
            self.assertIn("fixes", payload)
            self.assertIn("suggestions", payload)
            self.assertIn("stack_trace", payload)
            self.assertEqual(payload["fixes"], payload["suggestions"])
            self.assertIn("range", payload)
            self.assertEqual(payload["range"]["start"]["line"], 1)
            self.assertGreaterEqual(payload["range"]["end"]["column"], payload["range"]["start"]["column"] + 1)

    def test_cli_ide_diagnostics_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.ssk"
            bad.write_text("asatya-vakyam.", encoding="utf-8")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(["--diagnostics-format", "ide", "run", str(bad)])
            self.assertEqual(code, 1)
            payload = json.loads(stderr.getvalue().strip().splitlines()[0])
            self.assertIn("range", payload)
            self.assertIn("severity", payload)
            self.assertIn("data", payload)
            self.assertIn("snippet", payload["data"])
            self.assertIn("fixes", payload["data"])
            self.assertGreaterEqual(payload["range"]["end"]["character"], payload["range"]["start"]["character"] + 1)

    def test_cli_json_diagnostics_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.ssk"
            bad.write_text("asatya-vakyam.", encoding="utf-8")
            first = io.StringIO()
            with redirect_stderr(first):
                self.assertEqual(main(["--diagnostics-format", "json", "compile", str(bad)]), 1)
            second = io.StringIO()
            with redirect_stderr(second):
                self.assertEqual(main(["--diagnostics-format", "json", "compile", str(bad)]), 1)
            self.assertEqual(first.getvalue().strip(), second.getvalue().strip())

    def test_lint_error_level_fails_build(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "linty.ssk"
            source.write_text("a.", encoding="utf-8")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(["--diagnostics-format", "json", "lint", str(source), "--lint-level", "error"])
            self.assertEqual(code, 1)
            payload = json.loads(stderr.getvalue().strip().splitlines()[0])
            self.assertIn("SANSKRIPT_LINT_", payload["code"])
            self.assertEqual(payload["severity"], "error")
            self.assertTrue(payload["category"].startswith("lint."))

    def test_lint_warning_level_emits_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "linty.ssk"
            source.write_text("a.", encoding="utf-8")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(["--diagnostics-format", "json", "lint", str(source), "--lint-level", "warning"])
            self.assertEqual(code, 0)
            payload = json.loads(stderr.getvalue().strip().splitlines()[0])
            self.assertEqual(payload["severity"], "warning")
            self.assertTrue(payload["category"].startswith("lint."))

    def test_crash_report_written_for_uncaught_exception(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "crash.json"
            stderr = io.StringIO()
            with patch("sanskript.cli._run_file", side_effect=RuntimeError("boom")):
                with redirect_stderr(stderr):
                    code = main(["--diagnostics-format", "json", "--crash-report", str(report), "run", "x.ssk"])
            self.assertEqual(code, 1)
            self.assertTrue(report.exists())
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(payload["exception_type"], "RuntimeError")

    def test_vm_debug_assertion_can_raise_panic(self) -> None:
        vm = SanskriptVM()
        with patch.dict(os.environ, {"SANSKRIPT_DEBUG_ASSERT": "1"}):
            vm = SanskriptVM()
        vm._unsafe_depth = -1
        with self.assertRaises(PanicError):
            vm._debug_assert_state(0)

    def test_runtime_error_diagnostic_contains_stack_trace_context(self) -> None:
        with self.assertRaises(RuntimeSanskriptError) as raised:
            SanskriptVM().execute(compile_statements([Display(Reference("phala"))]))
        self.assertTrue(raised.exception.stack_trace)
        self.assertTrue(raised.exception.notes)
        payload = diagnostic_from_error(raised.exception).to_machine_dict()
        self.assertTrue(payload["stack_trace"])
        self.assertTrue(payload["notes"])

    def test_text_diagnostic_prints_fixes_notes_and_stack(self) -> None:
        err = RuntimeSanskriptError(
            "fail",
            hint="use valid symbol",
            notes=("opcode=display",),
            fixes=("bind the name before display",),
            stack_trace=("<main>:display@0",),
        )
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            with patch("sanskript.cli._run_file", side_effect=err):
                self.assertEqual(main(["--diagnostics-format", "text", "run", "x.ssk"]), 1)
        rendered = stderr.getvalue()
        self.assertIn("hint: use valid symbol", rendered)
        self.assertIn("note: opcode=display", rendered)
        self.assertIn("fix: bind the name before display", rendered)
        self.assertIn("stack: <main>:display@0", rendered)

    def test_diagnostic_end_span_tracks_multiline_snippet(self) -> None:
        exc = RuntimeSanskriptError(
            "boom",
            span=SourceSpan(start=0, end=3, line=3, column=4, snippet="a\nbc"),
        )
        diag = diagnostic_from_error(exc)
        machine = diag.to_machine_dict()
        ide = diag.to_ide_dict()
        self.assertEqual(machine["range"]["start"], {"line": 3, "column": 4})
        self.assertEqual(machine["range"]["end"], {"line": 4, "column": 3})
        self.assertEqual(ide["range"]["start"], {"line": 2, "character": 3})
        self.assertEqual(ide["range"]["end"], {"line": 3, "character": 2})

    def test_devanagari_parse_diagnostic_emits_script_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad-dev.ssk"
            bad.write_text("असत्यवाक्यम्।", encoding="utf-8")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(["--diagnostics-format", "json", "compile", str(bad)])
            self.assertEqual(code, 1)
            payload = json.loads(stderr.getvalue().strip().splitlines()[0])
            self.assertIn(payload.get("script"), {"devanagari", "iast"})
            self.assertIn("range", payload)

    def test_type_error_machine_snapshot_contains_fixes(self) -> None:
        exc = TypeCheckError(
            "Cannot move 'x' while it is borrowed",
            notes=("ownership=borrow",),
            fixes=("release borrow aliases before move",),
        )
        payload = diagnostic_from_error(exc).to_machine_dict()
        self.assertEqual(payload["code"], "SANSKRIPT_TYPE")
        self.assertEqual(payload["notes"], ["ownership=borrow"])
        self.assertEqual(payload["fixes"], ["release borrow aliases before move"])
        self.assertEqual(payload["suggestions"], ["release borrow aliases before move"])

    def test_rakshita_pointer_guard_diagnostic_contains_runtime_context(self) -> None:
        program = BytecodeProgram(
            instructions=(Instruction(OpCode.HEAP_LOAD), Instruction(OpCode.HALT)),
            safety_tier="rakshita",
        )
        with self.assertRaises(RuntimeSanskriptError) as raised:
            SanskriptVM().execute(program)
        payload = diagnostic_from_error(raised.exception).to_machine_dict()
        self.assertEqual(payload["code"], "SANSKRIPT_RUNTIME")
        self.assertIn("unsafe_enter", payload["message"])
        self.assertTrue(payload["stack_trace"])
        self.assertTrue(any(note.startswith("opcode=heap_load") for note in payload["notes"]))

    def test_panic_snapshot_reports_unrecoverable_category(self) -> None:
        payload = diagnostic_from_error(PanicError("fatal invariant")).to_machine_dict()
        self.assertEqual(payload["code"], "SANSKRIPT_PANIC")
        self.assertEqual(payload["category"], "panic")
        self.assertFalse(payload["recoverable"])

    def test_phase12_example_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path("examples/phase12-diagnostics.ssk")
            out = Path(tmp) / "phase12.sskbc"
            self.assertEqual(main(["compile", str(source), "-o", str(out)]), 0)
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                self.assertEqual(main(["run", str(source)]), 0)


if __name__ == "__main__":
    unittest.main()
