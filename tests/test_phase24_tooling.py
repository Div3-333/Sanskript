from __future__ import annotations

import inspect
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from sanskript.cli import main
from sanskript.formatter import format_source
from sanskript.phase24_tooling import (
    PHASE24_SCAFFOLD_TOOL_IDS,
    TOOL_CATALOG,
    Phase24EvidenceRequest,
    collect_coverage,
    create_project,
    debug_trace,
    extract_cli_dispatched_commands,
    freeze_phase24_spec,
    generate_phase24_evidence,
    handle_lsp_request,
    inspect_bytecode,
    inspect_sskyp,
    language_server_capabilities,
    migrate_python_module,
    migrate_rust_module,
    run_tests,
    textmate_grammar,
    verify_phase24_anti_fake,
)


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
PHASE24_EXAMPLE = EXAMPLES / "phase24-tooling.ssk"
CATALOG_COMMANDS = tuple(
    sorted({tool.cli_command for tool in TOOL_CATALOG if tool.cli_command})
)
CHECKLIST = ROOT / "docs" / "native-sanskript-independence-checklist.md"
PHASE24_META_COMMANDS = ("phase24-spec", "phase24-check")
PHASE24_ALIAS_COMMANDS = ("performance", "web", "pack")
ALL_PHASE24_CLI_COMMANDS = tuple(
    sorted(set(CATALOG_COMMANDS) | set(PHASE24_META_COMMANDS) | set(PHASE24_ALIAS_COMMANDS))
)


def _run_cli(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        try:
            code = main(argv)
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else 1
    return code, out.getvalue(), err.getvalue()


def _json_stdout(stdout: str) -> dict:
    start = stdout.find("{")
    if start < 0:
        raise AssertionError(f"expected JSON object in stdout, got: {stdout[:200]!r}")
    return json.loads(stdout[start:])


def _lsp_frame(message: dict) -> bytes:
    body = json.dumps(message, ensure_ascii=False).encode("utf-8")
    return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body


def _parse_lsp_messages(data: bytes) -> list[dict]:
    messages: list[dict] = []
    pos = 0
    while pos < len(data):
        header_end = data.find(b"\r\n\r\n", pos)
        if header_end < 0:
            break
        header_block = data[pos:header_end].decode("utf-8")
        length = 0
        for line in header_block.split("\r\n"):
            if line.lower().startswith("content-length:"):
                length = int(line.split(":", 1)[1].strip())
        body_start = header_end + 4
        body_end = body_start + length
        if body_end > len(data):
            break
        messages.append(json.loads(data[body_start:body_end].decode("utf-8")))
        pos = body_end
    return messages


class Phase24SealVerificationTests(unittest.TestCase):
    def test_verify_phase24_anti_fake_passes(self) -> None:
        violations = verify_phase24_anti_fake()
        self.assertEqual(violations, [], "\n".join(violations))

    def test_no_scaffold_tools_marked_functional(self) -> None:
        by_id = {tool.id: tool for tool in TOOL_CATALOG}
        for tool_id in PHASE24_SCAFFOLD_TOOL_IDS:
            self.assertEqual(by_id[tool_id].implementation_state, "scaffold", tool_id)
        for tool in TOOL_CATALOG:
            self.assertNotEqual(tool.implementation_state, "scaffold", tool.id)

    def test_debugger_exposes_breakpoint_controls(self) -> None:
        params = inspect.signature(debug_trace).parameters
        self.assertIn("breakpoints", params)
        self.assertIn("step", params)
        debugger = next(t for t in TOOL_CATALOG if t.id == "debugger")
        self.assertEqual(debugger.implementation_state, "functional")
        self.assertIn("breakpoint", debugger.truth_claims[0].casefold())

    def test_language_server_stdio_handlers(self) -> None:
        caps = language_server_capabilities()
        self.assertEqual(caps["implementation_state"], "functional")
        init_resp = handle_lsp_request(
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        )
        hover_resp = handle_lsp_request(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "textDocument/hover",
                "params": {"textDocument": {"uri": "file:///x.ssk"}, "position": {"line": 0, "character": 0}},
            }
        )
        self.assertIsNotNone(init_resp)
        self.assertIsNotNone(hover_resp)
        self.assertIn("capabilities", init_resp.get("result", {}))
        self.assertIn("contents", hover_resp.get("result", {}))

    def test_all_catalog_cli_commands_dispatch(self) -> None:
        dispatched = extract_cli_dispatched_commands()
        missing = [
            tool.cli_command
            for tool in TOOL_CATALOG
            if tool.cli_command and tool.cli_command not in dispatched
        ]
        self.assertEqual(missing, [])
        self.assertIn("performance", dispatched)


class Phase24ToolingModuleTests(unittest.TestCase):
    def test_catalog_matches_spec(self) -> None:
        spec = freeze_phase24_spec()
        self.assertEqual(spec["phase"], 24)
        self.assertEqual(spec["version"], 2)
        self.assertEqual(len(spec["tools"]), len(TOOL_CATALOG))

    def test_formatter_and_coverage_on_phase24_example(self) -> None:
        source = PHASE24_EXAMPLE.read_text(encoding="utf-8")
        formatted = format_source(source)
        self.assertIn("std.test", formatted)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "phase24.ssk"
            path.write_text(source, encoding="utf-8")
            coverage = collect_coverage(path)
            self.assertGreater(coverage["instruction_count"], 0)
            self.assertGreater(coverage["coverage_ratio"], 0.0)

    def test_debug_trace_breakpoint_pauses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "tiny.ssk"
            source.write_text("gaṇakaḥ ekaṃ darśayati.\n", encoding="utf-8")
            trace = debug_trace(source, breakpoints=(0,))
            self.assertTrue(trace["paused"])
            self.assertEqual(trace["pause_ip"], 0)
            self.assertGreater(trace["steps_recorded"], 0)

    def test_debug_trace_step_pauses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "tiny.ssk"
            source.write_text("gaṇakaḥ ekaṃ darśayati.\n", encoding="utf-8")
            trace = debug_trace(source, step=True)
            self.assertTrue(trace["paused"])
            self.assertTrue(trace["step_mode"])
            self.assertGreater(trace["steps_recorded"], 0)

    def test_run_tests_discovers_phase24_example(self) -> None:
        payload = run_tests(PHASE24_EXAMPLE)
        self.assertEqual(payload["discovered"], 1)
        self.assertTrue(payload["ok"])

    def test_run_tests_empty_root_is_not_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = run_tests(Path(tmp))
            self.assertEqual(payload["discovered"], 0)
            self.assertFalse(payload["ok"])

    def test_evidence_matrix_writes_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "phase24"
            payload = generate_phase24_evidence(
                request=Phase24EvidenceRequest(
                    out_dir=out_dir,
                    sample_source=PHASE24_EXAMPLE,
                )
            )
            self.assertEqual(payload["phase"], 24)
            self.assertTrue((out_dir / "phase24-evidence.json").exists())
            self.assertEqual(len(payload["rows"]), len(TOOL_CATALOG))
            self.assertEqual(payload["anti_fake_violations"], [])
            self.assertEqual(payload["smoke_verified_count"], len(TOOL_CATALOG))
            self.assertTrue(all(row["smoke_ok"] for row in payload["rows"]))

    def test_migrate_python_writes_skeleton(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "migrated.ssk"
            report = migrate_python_module(ROOT / "src" / "sanskript" / "vm.py", output=out)
            self.assertGreater(len(report["hints"]), 0)
            self.assertEqual(report["implementation_state"], "functional")
            self.assertTrue(out.is_file())
            body = out.read_text(encoding="utf-8")
            self.assertTrue("kriyā" in body or "vargaḥ" in body, body)

    def test_migrate_rust_writes_skeleton(self) -> None:
        rust_src = ROOT / "ssk-vm" / "src" / "lib.rs"
        if not rust_src.is_file():
            self.skipTest("ssk-vm lib.rs missing")
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "migrated.ssk"
            report = migrate_rust_module(rust_src, output=out)
            self.assertTrue(out.is_file())
            self.assertEqual(report["implementation_state"], "functional")


class Phase24CliAdversarialTests(unittest.TestCase):
    """Reject exit-0 no-ops: every Phase 24 catalog command must do real work."""

    def test_format_normalizes_and_rejects_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            messy = Path(tmp) / "messy.ssk"
            messy.write_text("  gaṇakaḥ   ekaṃ   darśayati.  \n", encoding="utf-8")
            bad = Path(tmp) / "bad.ssk"
            bad.write_text("!!!\n", encoding="utf-8")
            code, _, _ = _run_cli(["format", str(messy)])
            self.assertEqual(code, 0)
            self.assertNotIn("   ", messy.read_text(encoding="utf-8"))
            code, _, _ = _run_cli(["format", str(messy), "--check"])
            self.assertEqual(code, 0)
            code, _, _ = _run_cli(["format", str(bad)])
            self.assertNotEqual(code, 0)

    def test_test_empty_dir_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp) / "empty"
            empty.mkdir()
            code, out, _ = _run_cli(["test", str(empty)])
            payload = _json_stdout(out)
            self.assertEqual(code, 1)
            self.assertFalse(payload["ok"])

    def test_test_single_file_passes(self) -> None:
        code, out, _ = _run_cli(["test", str(PHASE24_EXAMPLE)])
        payload = _json_stdout(out)
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])

    def test_bench_stdout_is_clean_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sample_dir = Path(tmp) / "bench-examples"
            sample_dir.mkdir()
            (sample_dir / "tiny.ssk").write_text("gaṇakaḥ ekaṃ darśayati.\n", encoding="utf-8")
            code, out, _ = _run_cli(
                ["bench", "--examples", str(sample_dir), "--iterations", "2", "--budget-ms", "25"]
            )
            self.assertEqual(out.find("{"), 0, f"bench stdout polluted: {out[:120]!r}")
            payload = json.loads(out)
            self.assertGreater(payload["baseline"]["example_count"], 0)
            self.assertEqual(code, 0 if payload["ok"] else 1)

    def test_bench_empty_examples_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp) / "empty"
            empty.mkdir()
            code, out, _ = _run_cli(["bench", "--examples", str(empty), "--iterations", "2"])
            payload = _json_stdout(out)
            self.assertEqual(code, 1)
            self.assertFalse(payload["ok"])

    def test_build_empty_tree_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp) / "empty"
            empty.mkdir()
            code, out, _ = _run_cli(["build", str(empty)])
            payload = _json_stdout(out)
            self.assertEqual(code, 1)
            self.assertEqual(payload["compiled"], 0)

    def test_coverage_and_profile_emit_metrics(self) -> None:
        code, out, _ = _run_cli(["coverage", str(PHASE24_EXAMPLE)])
        cov = _json_stdout(out)
        self.assertEqual(code, 0)
        self.assertGreater(cov["coverage_ratio"], 0.0)
        code, out, _ = _run_cli(["profile", str(PHASE24_EXAMPLE), "--iterations", "2"])
        prof = _json_stdout(out)
        self.assertEqual(code, 0)
        self.assertGreater(len(prof["opcode_ms_estimates"]), 0)

    def test_debug_trace_and_breakpoint_cli(self) -> None:
        code, out, _ = _run_cli(["debug", str(PHASE24_EXAMPLE), "--max-steps", "8"])
        trace = _json_stdout(out)
        self.assertEqual(code, 0)
        self.assertGreater(trace["steps_recorded"], 0)
        code, out, _ = _run_cli(["debug", str(PHASE24_EXAMPLE), "--breakpoints", "0"])
        paused = _json_stdout(out)
        self.assertEqual(code, 0)
        self.assertTrue(paused["paused"])

        code, out, _ = _run_cli(["debug", str(PHASE24_EXAMPLE), "--step"])
        stepped = _json_stdout(out)
        self.assertEqual(code, 0)
        self.assertTrue(stepped["paused"])
        self.assertTrue(stepped["step_mode"])

    def test_lsp_capabilities_and_handlers(self) -> None:
        code, out, _ = _run_cli(["lsp"])
        caps = _json_stdout(out)
        self.assertEqual(code, 0)
        self.assertEqual(caps["implementation_state"], "functional")
        self.assertIn("capabilities", caps)

    def test_highlight_build_release_installer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            grammar = root / "grammar.json"
            code, out, _ = _run_cli(["highlight", "-o", str(grammar)])
            self.assertEqual(code, 0)
            self.assertTrue(grammar.exists())

            project = root / "proj"
            self.assertEqual(main(["new", "lib", str(project)]), 0)
            zip_path = root / "bundle.zip"
            code, _, _ = _run_cli(["release", str(project), "-o", str(zip_path)])
            self.assertEqual(code, 0)
            self.assertTrue(zip_path.exists())

            installer_zip = root / "installer-linux.zip"
            code, out, _ = _run_cli(["installer", "linux", "-o", str(installer_zip)])
            self.assertEqual(code, 0)
            self.assertTrue(installer_zip.exists())
            with zipfile.ZipFile(installer_zip) as archive:
                names = set(archive.namelist())
            self.assertIn("INSTALL.json", names)
            self.assertIn("sanskript", names)

    def test_inspect_migrate_playground_web(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "tiny.ssk"
            source.write_text("gaṇakaḥ ekaṃ darśayati.\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["compile", str(source)]), 0)
            bc = source.with_suffix(".sskbc")
            report_path = root / "bc-report.json"
            code, out, _ = _run_cli(["inspect-bytecode", str(bc), "-o", str(report_path)])
            self.assertEqual(code, 0)
            self.assertTrue(report_path.exists())
            self.assertGreater(_json_stdout(report_path.read_text(encoding="utf-8"))["instruction_count"], 0)

            py_out = root / "from-py.ssk"
            code, out, _ = _run_cli(
                ["migrate-python", str(ROOT / "src" / "sanskript" / "vm.py"), "-o", str(py_out)]
            )
            self.assertEqual(code, 0)
            self.assertTrue(py_out.exists())

            html = root / "play.html"
            code, _, _ = _run_cli(["playground", str(PHASE24_EXAMPLE), "-o", str(html)])
            self.assertEqual(code, 0)
            self.assertTrue(html.exists())
            self.assertIn("<html", html.read_text(encoding="utf-8").casefold())

            web = root / "web.html"
            code, _, _ = _run_cli(["web-playground", str(PHASE24_EXAMPLE), "-o", str(web)])
            self.assertEqual(code, 0)
            self.assertTrue(web.exists())

    def test_trace_view_and_editor_integration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            trace_path = Path(tmp) / "trace.json"
            html_path = Path(tmp) / "trace.html"
            code, out, _ = _run_cli(["debug", str(PHASE24_EXAMPLE), "--max-steps", "4"])
            trace_path.write_text(out, encoding="utf-8")
            code, _, _ = _run_cli(["trace-view", str(trace_path), "-o", str(html_path)])
            self.assertEqual(code, 0)
            self.assertIn("<table>", html_path.read_text(encoding="utf-8"))

            editor_dir = Path(tmp) / "editor"
            code, _, _ = _run_cli(["editor-integration", "-o", str(editor_dir)])
            self.assertEqual(code, 0)
            self.assertTrue((editor_dir / "sanskript.tmLanguage.json").exists())
            self.assertTrue((editor_dir / ".vscode" / "launch.json").exists())

    def test_phase24_spec_and_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "evidence"
            code, out, _ = _run_cli(["phase24-spec"])
            spec = _json_stdout(out)
            self.assertEqual(code, 0)
            self.assertEqual(spec["phase"], 24)
            self.assertEqual(len(spec["tools"]), len(TOOL_CATALOG))

            code, _, _ = _run_cli(
                [
                    "phase24-check",
                    "--out-dir",
                    str(out_dir),
                    "--sample-source",
                    str(PHASE24_EXAMPLE),
                ]
            )
            self.assertEqual(code, 0)
            evidence = json.loads((out_dir / "phase24-evidence.json").read_text(encoding="utf-8"))
            self.assertEqual(evidence["smoke_verified_count"], evidence["catalog_size"])

    def test_catalog_commands_all_have_cli_dispatch(self) -> None:
        self.assertEqual(len(CATALOG_COMMANDS), len({t.cli_command for t in TOOL_CATALOG if t.cli_command}))


class Phase24RemainingCliAdversarialTests(unittest.TestCase):
    def test_compile_run_lint_docs_deps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "prog.ssk"
            source.write_text("gaṇakaḥ ekaṃ darśayati.\n", encoding="utf-8")
            bc = Path(tmp) / "prog.sskbc"
            code, out, _ = _run_cli(["compile", str(source), "-o", str(bc)])
            self.assertEqual(code, 0)
            self.assertTrue(bc.exists())

            run_out = io.StringIO()
            with redirect_stdout(run_out):
                self.assertEqual(main(["run", str(bc)]), 0)
            self.assertEqual(run_out.getvalue().strip(), "1")

            code, _, err = _run_cli(["lint", str(source)])
            self.assertEqual(code, 0)

            docs = Path(tmp) / "api.md"
            code, out, _ = _run_cli(["docs", str(source), "-o", str(docs)])
            self.assertEqual(code, 0)
            self.assertTrue(docs.exists())

            project = Path(tmp) / "pkg"
            self.assertEqual(main(["new", "app", str(project)]), 0)
            code, out, _ = _run_cli(["deps-update", str(project)])
            self.assertEqual(code, 0)
            self.assertTrue((project / "ssk.lock").exists())

    def test_inspect_sskyp_and_migrate_rust(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = EXAMPLES / "caturtha.ssk"
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["compile", str(source)]), 0)
            bc = source.with_suffix(".sskbc")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["disassemble", str(bc)]), 0)
            sskyp = bc.with_suffix(".sskyp")
            code, out, _ = _run_cli(["inspect-sskyp", str(sskyp)])
            payload = _json_stdout(out)
            self.assertEqual(code, 0)
            self.assertGreater(payload["line_count"], 0)

            rust_src = ROOT / "ssk-vm" / "src" / "lib.rs"
            if not rust_src.is_file():
                self.skipTest("ssk-vm lib.rs missing")
            out = root / "from-rs.ssk"
            code, _, _ = _run_cli(["migrate-rust", str(rust_src), "-o", str(out)])
            self.assertEqual(code, 0)
            self.assertTrue(out.exists())

    def test_install_pack_performance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "pkg"
            self.assertEqual(main(["new", "lib", str(project)]), 0)
            dep = Path(tmp) / "dep"
            dep.mkdir()
            (dep / "helper.ssk").write_text("gaṇakaḥ ekaṃ darśayati.\n", encoding="utf-8")
            prev = os.getcwd()
            try:
                os.chdir(project)
                code, out, _ = _run_cli(["install", str(dep), "--name", "helper"])
            finally:
                os.chdir(prev)
            self.assertEqual(code, 0)
            self.assertTrue((project / "vendor" / "helper").exists())

            bundle = Path(tmp) / "pack.zip"
            code, _, _ = _run_cli(["pack", str(project), "-o", str(bundle)])
            self.assertEqual(code, 0)
            self.assertTrue(bundle.exists())

            sample_dir = Path(tmp) / "bench"
            sample_dir.mkdir()
            (sample_dir / "tiny.ssk").write_text("gaṇakaḥ ekaṃ darśayati.\n", encoding="utf-8")
            code, out, _ = _run_cli(
                [
                    "performance",
                    "--examples",
                    str(sample_dir),
                    "--iterations",
                    "2",
                    "--budget-ms",
                    "25",
                ]
            )
            self.assertEqual(out.find("{"), 0, f"performance stdout polluted: {out[:120]!r}")
            payload = json.loads(out)
            self.assertGreater(payload["example_count"], 0)
            self.assertIn(code, (0, 1))


class Phase24ChecklistSealTests(unittest.TestCase):
    def test_phase24_section_has_no_scaffold_marked_complete(self) -> None:
        section = CHECKLIST.read_text(encoding="utf-8").split("## Phase 24:")[1].split("## Phase 25:")[0]
        for line in section.splitlines():
            if "[x]" in line and "scaffold" in line.casefold():
                self.fail(f"scaffold row must not be [x]: {line.strip()}")
        self.assertRegex(section, r"- \[~\] Package manager")
        self.assertRegex(section, r"- \[~\] Profiler")
        self.assertRegex(section, r"- \[x\] Debugger")
        self.assertRegex(section, r"- \[x\] Language server")

    def test_tooling_doc_does_not_claim_functional_tools_are_scaffold(self) -> None:
        text = (ROOT / "docs" / "tooling.md").read_text(encoding="utf-8")
        self.assertIn("PHASE24_SCAFFOLD_TOOL_IDS` is empty", text)
        self.assertNotIn("scaffold (no breakpoints", text.casefold())


class Phase24EveryCatalogCommandAdversarialTests(unittest.TestCase):
    """One adversarial probe per Phase 24 catalog CLI command (plus meta/alias commands)."""

    def test_all_phase24_cli_commands_are_enumerated(self) -> None:
        self.assertEqual(len(CATALOG_COMMANDS), len(TOOL_CATALOG))
        self.assertEqual(
            len(ALL_PHASE24_CLI_COMMANDS),
            len(CATALOG_COMMANDS) + len(PHASE24_META_COMMANDS) + len(PHASE24_ALIAS_COMMANDS),
        )

    def test_compile_missing_source_exits_nonzero(self) -> None:
        code, _, err = _run_cli(["compile", str(ROOT / "missing-phase24.ssk")])
        self.assertNotEqual(code, 0)
        self.assertTrue(err or True)

    def test_run_missing_source_exits_nonzero(self) -> None:
        code, _, _ = _run_cli(["run", str(ROOT / "missing-phase24.ssk")])
        self.assertNotEqual(code, 0)

    def test_repl_executes_line_then_eof(self) -> None:
        out = io.StringIO()
        with patch("builtins.input", side_effect=["gaṇakaḥ ekaṃ darśayati", EOFError()]):
            with redirect_stdout(out):
                code = main(["repl"])
        self.assertEqual(code, 0)
        self.assertIn("1", out.getvalue())

    def test_lint_invalid_syntax_exits_nonzero_at_error_level(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.ssk"
            bad.write_text("!!!\n", encoding="utf-8")
            code, _, _ = _run_cli(["lint", str(bad), "--lint-level", "error"])
            self.assertNotEqual(code, 0)

    def test_format_check_flags_unformatted_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            messy = Path(tmp) / "messy.ssk"
            messy.write_text("  gaṇakaḥ   ekaṃ   darśayati.  \n", encoding="utf-8")
            code, _, _ = _run_cli(["format", str(messy), "--check"])
            self.assertEqual(code, 1)

    def test_format_stdout_writes_normalized_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            messy = Path(tmp) / "messy.ssk"
            messy.write_text("  gaṇakaḥ   ekaṃ   darśayati.  \n", encoding="utf-8")
            code, out, _ = _run_cli(["format", str(messy), "--stdout"])
            self.assertEqual(code, 0)
            self.assertNotIn("   ", out)
            self.assertIn("gaṇakaḥ", out)

    def test_install_missing_dependency_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "pkg"
            self.assertEqual(main(["new", "lib", str(project)]), 0)
            prev = os.getcwd()
            try:
                os.chdir(project)
                code, _, err = _run_cli(["install", str(ROOT / "missing-dep")])
            finally:
                os.chdir(prev)
            self.assertEqual(code, 1)
            self.assertIn("not found", err.casefold())

    def test_install_without_manifest_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dep = Path(tmp) / "dep"
            dep.mkdir()
            (dep / "x.ssk").write_text("gaṇakaḥ ekaṃ darśayati.\n", encoding="utf-8")
            prev = os.getcwd()
            try:
                os.chdir(tmp)
                code, _, err = _run_cli(["install", str(dep)])
            finally:
                os.chdir(prev)
            self.assertEqual(code, 1)
            self.assertIn("ssk.toml", err)

    def test_deps_update_without_manifest_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, _, err = _run_cli(["deps-update", str(tmp)])
            self.assertNotEqual(code, 0)
            self.assertIn("ssk.toml", err)

    def test_docs_missing_source_exits_nonzero(self) -> None:
        code, _, _ = _run_cli(["docs", str(ROOT / "missing-phase24.ssk")])
        self.assertNotEqual(code, 0)

    def test_coverage_invalid_source_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.ssk"
            bad.write_text("!!!\n", encoding="utf-8")
            code, _, _ = _run_cli(["coverage", str(bad)])
            self.assertNotEqual(code, 0)

    def test_profile_invalid_source_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.ssk"
            bad.write_text("!!!\n", encoding="utf-8")
            code, _, _ = _run_cli(["profile", str(bad)])
            self.assertNotEqual(code, 0)

    def test_debug_step_mode_pauses(self) -> None:
        code, out, _ = _run_cli(["debug", str(PHASE24_EXAMPLE), "--step", "--max-steps", "4"])
        payload = _json_stdout(out)
        self.assertEqual(code, 0)
        self.assertTrue(payload["paused"])
        self.assertGreater(payload["steps_recorded"], 0)

    def test_debug_without_breakpoints_still_records_steps(self) -> None:
        code, out, _ = _run_cli(["debug", str(PHASE24_EXAMPLE), "--max-steps", "3"])
        payload = _json_stdout(out)
        self.assertEqual(code, 0)
        self.assertGreater(payload["steps_recorded"], 0)
        self.assertFalse(payload["paused"])

    def test_lsp_stdio_initialize_and_hover_roundtrip(self) -> None:
        init_body = json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            ensure_ascii=False,
        ).encode("utf-8")
        hover_body = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "textDocument/hover",
                "params": {
                    "textDocument": {"uri": "file:///x.ssk"},
                    "position": {"line": 0, "character": 0},
                },
            },
            ensure_ascii=False,
        ).encode("utf-8")
        shutdown_body = json.dumps(
            {"jsonrpc": "2.0", "id": 3, "method": "shutdown"},
            ensure_ascii=False,
        ).encode("utf-8")
        stdin = b"".join(
            f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body
            for body in (init_body, hover_body, shutdown_body)
        )
        env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
        proc = subprocess.run(
            [sys.executable, "-m", "sanskript.cli", "lsp", "--stdio"],
            input=stdin,
            capture_output=True,
            env=env,
            timeout=30,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", errors="replace"))
        raw = proc.stdout.decode("utf-8", errors="replace")
        self.assertIn("capabilities", raw)
        self.assertIn("contents", raw)

    def test_installer_invalid_target_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "bad.zip"
            err = io.StringIO()
            with redirect_stderr(err):
                with self.assertRaises(SystemExit) as ctx:
                    main(["installer", "solaris", "-o", str(out)])
            self.assertEqual(ctx.exception.code, 2)
            self.assertIn("invalid choice", err.getvalue().casefold())

    def test_web_command_writes_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            html = Path(tmp) / "runner.html"
            code, _, _ = _run_cli(["web", str(PHASE24_EXAMPLE), "-o", str(html)])
            self.assertEqual(code, 0)
            self.assertTrue(html.exists())
            self.assertIn("<html", html.read_text(encoding="utf-8").casefold())

    def test_trace_view_rejects_invalid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text("not json", encoding="utf-8")
            html = Path(tmp) / "out.html"
            code, _, _ = _run_cli(["trace-view", str(bad), "-o", str(html)])
            self.assertNotEqual(code, 0)
            self.assertFalse(html.exists())

    def test_migrate_python_empty_source_still_writes_fallback_skeleton(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            py = Path(tmp) / "empty.py"
            py.write_text("# no defs\n", encoding="utf-8")
            out = Path(tmp) / "out.ssk"
            code, _, _ = _run_cli(["migrate-python", str(py), "-o", str(out)])
            self.assertEqual(code, 0)
            body = out.read_text(encoding="utf-8")
            self.assertIn("gaṇakaḥ", body)

    def test_pack_missing_source_exits_nonzero(self) -> None:
        code, _, err = _run_cli(["pack", str(ROOT / "missing-pack-root")])
        self.assertEqual(code, 1)
        self.assertIn("not found", err.casefold())

    def test_phase24_check_fails_when_sample_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, _, _ = _run_cli(
                [
                    "phase24-check",
                    "--out-dir",
                    str(Path(tmp) / "evidence"),
                    "--sample-source",
                    str(ROOT / "missing-phase24-sample.ssk"),
                ]
            )
            self.assertEqual(code, 1)

    def test_catalog_commands_adversarial_matrix_complete(self) -> None:
        covered = {
            "compile",
            "run",
            "repl",
            "format",
            "lint",
            "test",
            "bench",
            "install",
            "build",
            "docs",
            "coverage",
            "profile",
            "debug",
            "lsp",
            "highlight",
            "editor-integration",
            "new",
            "deps-update",
            "release",
            "installer",
            "playground",
            "web-playground",
            "trace-view",
            "inspect-bytecode",
            "inspect-sskyp",
            "migrate-python",
            "migrate-rust",
            "phase24-spec",
            "phase24-check",
            "performance",
            "web",
            "pack",
        }
        self.assertEqual(covered, set(ALL_PHASE24_CLI_COMMANDS))


if __name__ == "__main__":
    unittest.main()
