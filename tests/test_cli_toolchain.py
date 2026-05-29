import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from sanskript.cli import main
from sanskript.compiler import compile_source
from sanskript.vm import SanskriptVM
from sanskript.bytecode import load_bytecode_file


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
# VM parity skipped when integration harness substitutes placeholders before run.
_VM_RUN_SKIP_EXAMPLES = frozenset(
    {
        "phase22-http-service.ssk",
        # Canonical execution is .sskbc (see examples/phase27-port-*.sskbc).
        "phase27-port-controlled-lexicon.ssk",
        "phase27-port-examples-runner.ssk",
        "phase27-port-sutra-registry.ssk",
    }
)


class CliToolchainTests(unittest.TestCase):
    def test_compile_writes_default_sskbc_and_run_loads_bytecode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "program.ssk"
            source.write_text((EXAMPLES / "caturtha.ssk").read_text(encoding="utf-8"), encoding="utf-8")

            compile_stdout = io.StringIO()
            with redirect_stdout(compile_stdout):
                self.assertEqual(main(["compile", str(source)]), 0)

            bytecode_path = source.with_suffix(".sskbc")
            self.assertTrue(bytecode_path.exists())
            self.assertIn(str(bytecode_path), compile_stdout.getvalue())

            run_stdout = io.StringIO()
            with redirect_stdout(run_stdout):
                self.assertEqual(main(["run", str(bytecode_path)]), 0)

            self.assertEqual(run_stdout.getvalue().strip().splitlines(), ["7"])

    def test_compile_supports_explicit_output_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "program.ssk"
            output = Path(tmp) / "artifacts" / "program.sskbc"
            source.write_text((EXAMPLES / "pancama.ssk").read_text(encoding="utf-8"), encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["compile", str(source), "-o", str(output)]), 0)

            self.assertTrue(output.exists())
            self.assertEqual(SanskriptVM().execute(load_bytecode_file(output)), ["7"])

    def test_all_examples_compile_to_portable_bytecode(self) -> None:
        for example in sorted(EXAMPLES.glob("*.ssk")):
            with self.subTest(example=example.name):
                with tempfile.TemporaryDirectory() as tmp:
                    output = Path(tmp) / f"{example.stem}.sskbc"
                    with redirect_stdout(io.StringIO()):
                        self.assertEqual(main(["compile", str(example), "-o", str(output)]), 0)
                    if example.name in _VM_RUN_SKIP_EXAMPLES:
                        continue
                    source_output = SanskriptVM().execute(
                        compile_source(example.read_text(encoding="utf-8"))
                    )
                    bytecode_output = SanskriptVM().execute(load_bytecode_file(output))
                    self.assertEqual(bytecode_output, source_output)

    def test_run_prints_unicode_text_output(self) -> None:
        run_stdout = io.StringIO()

        with redirect_stdout(run_stdout):
            self.assertEqual(main(["run", str(EXAMPLES / "dashama-vakyam.ssk")]), 0)

        self.assertEqual(run_stdout.getvalue().strip().splitlines(), ["svāgatam mitra"])

    def test_phase17_verify_optimize_and_link_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = EXAMPLES / "prathama.ssk"
            a = root / "a.sskbc"
            b = root / "b.sskbc"
            optimized = root / "opt.sskypb"
            linked = root / "linked.sskyp"
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["compile", str(source), "-o", str(a)]), 0)
                self.assertEqual(main(["compile", str(source), "-o", str(b)]), 0)
                self.assertEqual(main(["phase17-verify", str(a)]), 0)
                self.assertEqual(main(["phase17-optimize", str(a), "-o", str(optimized)]), 0)
                self.assertEqual(main(["phase17-link", str(a), str(b), "-o", str(linked)]), 0)
            self.assertTrue(optimized.exists())
            self.assertTrue(linked.exists())

    def test_main_without_command_prints_help_and_exits_two(self) -> None:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(main([]), 2)
        self.assertIn("usage: sanskript", stdout.getvalue())

    def test_format_normalizes_source_and_check_detects_diff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "messy.ssk"
            source.write_text("gaṇakaḥ   pañca phale nidadhāti.", encoding="utf-8")
            self.assertEqual(main(["format", str(source), "--check"]), 1)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["format", str(source)]), 0)
            self.assertEqual(main(["format", str(source), "--check"]), 0)
            self.assertIn("gaṇakaḥ pañca phale nidadhāti.", source.read_text(encoding="utf-8"))

    def test_format_stdout_does_not_require_output_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "messy.ssk"
            source.write_text("gaṇakaḥ   pañca phale nidadhāti.", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                self.assertEqual(main(["format", str(source), "--stdout"]), 0)
            self.assertIn("gaṇakaḥ pañca phale nidadhāti.", stdout.getvalue())

    def test_debug_emits_execution_summary_and_artifact_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "main.ssk"
            source.write_text("gaṇakaḥ ekaṃ darśayati.", encoding="utf-8")
            trace = root / "trace.json"
            debug = root / "debug.json"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                self.assertEqual(
                    main(
                        [
                            "debug",
                            str(source),
                            "--trace",
                            str(trace),
                            "--debug",
                            str(debug),
                        ]
                    ),
                    0,
                )
            self.assertTrue(trace.is_file())
            self.assertTrue(debug.is_file())
            trace_payload = json.loads(trace.read_text(encoding="utf-8"))
            debug_payload = json.loads(debug.read_text(encoding="utf-8"))
            self.assertEqual(trace_payload["output"], ["1"])
            self.assertEqual(debug_payload["output"], ["1"])
            self.assertGreater(debug_payload["instruction_count"], 0)

    def test_debug_default_prints_trace_json(self) -> None:
        source = EXAMPLES / "caturtha.ssk"
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(main(["debug", str(source)]), 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["output"], ["7"])
        self.assertEqual(payload["status"], "completed")
        self.assertGreater(payload["steps_recorded"], 0)
        self.assertTrue(payload["events"])

    def test_lint_error_level_fails_on_choppy_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "choppy.ssk"
            source.write_text("phale pañca.", encoding="utf-8")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                self.assertEqual(main(["lint", str(source), "--lint-level", "error"]), 1)
            self.assertIn("SANSKRIPT_LINT", stderr.getvalue())

    def test_phase18_vm_check_exits_nonzero_when_retirement_not_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "phase18"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "phase18-vm-check",
                        str(EXAMPLES / "phase18-vm-bootstrap.sskbc"),
                        "--artifact-dir",
                        str(out_dir),
                    ]
                )
            self.assertEqual(code, 2)
            report_path = out_dir / "phase18-bootstrap-evidence.json"
            self.assertTrue(report_path.exists())
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertFalse(report["independent_vm_runtime"])
            self.assertFalse(report["retirement_report"]["retirement_ready"])
            self.assertTrue(report["retirement_report"]["blocked_reasons"])


if __name__ == "__main__":
    unittest.main()
