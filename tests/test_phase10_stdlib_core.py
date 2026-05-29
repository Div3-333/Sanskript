"""Phase 10 standard library core — unit and VM integration tests."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode
from sanskript.errors import CompileError, RuntimeSanskriptError
from sanskript.runtime_values import BytesValue, NIL
from sanskript.compiler import compile_source, compile_program_to_ir, lower_ir_to_bytecode
from sanskript.parser import parse_program
from sanskript.stdlib_core import call_native_function, has_native_function, list_native_functions
from sanskript.vm import SanskriptVM

# Every Phase 10 checklist library must expose at least one registered entry.
PHASE10_PREFIXES = (
    "std.text.",
    "std.unicode.",
    "std.bytes.",
    "std.math.",
    "std.stats.",
    "std.random.",
    "std.datetime.",
    "std.timezone.",
    "std.path.",
    "std.file.",
    "std.io.",
    "std.stream.",
    "std.terminal.",
    "std.cli.",
    "std.env.",
    "std.process.",
    "std.pipe.",
    "std.signal.",
    "std.log.",
    "std.config.",
    "std.json.",
    "std.csv.",
    "std.toml.",
    "std.yaml.",
    "std.xml.",
    "std.binary.",
    "std.compress.",
    "std.hash.",
    "std.crypto.",
    "std.secure.",
    "std.encoding.",
    "std.regex.",
    "std.template.",
    "std.serialize",
    "std.deserialize",
    "std.test.",
    "std.bench.",
)


class StdlibRegistryTests(unittest.TestCase):
    def test_all_phase10_namespaces_registered(self) -> None:
        names = list_native_functions()
        for prefix in PHASE10_PREFIXES:
            if prefix.endswith("."):
                ok = any(name.startswith(prefix) for name in names)
            else:
                ok = prefix in names
            self.assertTrue(ok, f"missing registry entries for {prefix}")


class StdlibCoreUnitTests(unittest.TestCase):
    # --- json / csv (existing) ---
    def test_json_round_trip(self) -> None:
        text = call_native_function("std.json.stringify", [{"n": 3, "ok": True}])
        self.assertEqual(text, '{"n":3,"ok":true}')
        parsed = call_native_function("std.json.parse", [text])
        self.assertEqual(parsed, {"n": 3, "ok": True})

    def test_json_parse_error(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.json.parse", ["{broken"])

    def test_csv_stringify_requires_headers(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.csv.stringify", [[]])

    # --- text / unicode ---
    def test_text_split_join(self) -> None:
        parts = call_native_function("std.text.split", ["a,b", ","])
        joined = call_native_function("std.text.join", [",", parts])
        self.assertEqual(joined, "a,b")

    def test_unicode_normalize_and_grapheme(self) -> None:
        text = "é"
        nfc = call_native_function("std.unicode.normalize", [text, "NFC"])
        self.assertEqual(call_native_function("std.unicode.grapheme_len", [nfc]), 1)

    def test_unicode_codepoint_error(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.unicode.codepoint_at", ["ab", 9])

    # --- bytes ---
    def test_bytes_round_trip(self) -> None:
        raw = call_native_function("std.bytes.from_text", ["नमस्ते"])
        self.assertEqual(call_native_function("std.bytes.len", [raw]), len("नमस्ते".encode("utf-8")))
        self.assertEqual(call_native_function("std.bytes.to_text", [raw]), "नमस्ते")

    def test_bytes_hex_decode_error(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.bytes.hex_decode", ["zz"])

    # --- math / stats ---
    def test_math_clamp_error(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.math.clamp", [5, 10, 2])

    def test_stats_mean_and_stdev(self) -> None:
        self.assertEqual(call_native_function("std.stats.mean", [[1, 2, 3]]), 2.0)
        self.assertAlmostEqual(call_native_function("std.stats.stdev", [[1, 2, 3]]), 1.0)

    def test_stats_stdev_error(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.stats.stdev", [[1]])

    # --- random ---
    def test_random_seed_deterministic(self) -> None:
        call_native_function("std.random.seed", [42])
        a = call_native_function("std.random.randint", [1, 6])
        call_native_function("std.random.seed", [42])
        b = call_native_function("std.random.randint", [1, 6])
        self.assertEqual(a, b)

    # --- datetime / timezone ---
    def test_datetime_diff_seconds(self) -> None:
        diff = call_native_function(
            "std.datetime.diff_seconds",
            ["2020-01-01T00:00:10+00:00", "2020-01-01T00:00:00+00:00"],
        )
        self.assertEqual(diff, 10.0)

    def test_timezone_convert(self) -> None:
        out = call_native_function(
            "std.timezone.convert",
            ["2020-06-01T12:00:00+00:00", "UTC"],
        )
        self.assertIn("2020-06-01", out)

    # --- path / file / io ---
    def test_file_text_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "phase10.txt")
            call_native_function("std.file.write_text", [path, "line1\n"])
            call_native_function("std.file.append_text", [path, "line2"])
            text = call_native_function("std.file.read_text", [path])
            lines = call_native_function("std.io.read_lines", [path])
            self.assertEqual(text, "line1\nline2")
            self.assertEqual(lines, ["line1", "line2"])

    def test_file_read_missing_error(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.file.read_text", ["/nonexistent/phase10-missing.txt"])

    # --- formats ---
    def test_toml_yaml_xml_round_trip(self) -> None:
        toml_in = '[app]\nname = "sanskript"\ncount = 2\n'
        toml_val = call_native_function("std.toml.parse", [toml_in])
        self.assertEqual(toml_val["app"]["name"], "sanskript")
        yaml_in = "title: demo\ncount: 3\n"
        yaml_val = call_native_function("std.yaml.parse", [yaml_in])
        self.assertEqual(yaml_val["count"], 3)
        xml_in = '<root id="1"><child>x</child></root>'
        xml_val = call_native_function("std.xml.parse", [xml_in])
        self.assertEqual(xml_val["tag"], "root")
        self.assertEqual(xml_val["@id"], "1")

    def test_yaml_parse_error(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.yaml.parse", ["- orphan\nkey: value"])

    # --- binary / compression / hash / crypto / secure / encoding ---
    def test_binary_pack_unpack(self) -> None:
        packed = call_native_function("std.binary.pack", ["!ii", [7, 9]])
        vals = call_native_function("std.binary.unpack", ["!ii", packed])
        self.assertEqual(vals, [7, 9])

    def test_compress_gzip_round_trip(self) -> None:
        raw = call_native_function("std.bytes.from_text", ["payload"])
        gz = call_native_function("std.compress.gzip", [raw])
        out = call_native_function("std.compress.gunzip", [gz])
        self.assertEqual(call_native_function("std.bytes.to_text", [out]), "payload")

    def test_hash_and_crypto(self) -> None:
        self.assertEqual(
            len(call_native_function("std.hash.md5", ["x"])),
            32,
        )
        self.assertEqual(
            call_native_function("std.crypto.hmac_sha256", ["key", "msg"]),
            call_native_function("std.crypto.hmac_sha256", ["key", "msg"]),
        )

    def test_encoding_base64_error(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.encoding.base64_decode", ["%%%"])

    # --- regex / template / serialize ---
    def test_regex_and_template(self) -> None:
        self.assertTrue(call_native_function("std.regex.match", [r"^\d+$", "42"]))
        rendered = call_native_function(
            "std.template.render",
            ["Hello {{ name }}!", {"name": "dev"}],
        )
        self.assertEqual(rendered, "Hello dev!")
        ser = call_native_function("std.serialize", ["json", {"a": 1}])
        des = call_native_function("std.deserialize", ["json", ser])
        self.assertEqual(des, {"a": 1})

    def test_regex_invalid_pattern(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.regex.match", ["(", "x"])

    # --- test / bench utilities ---
    def test_test_assertions(self) -> None:
        self.assertTrue(call_native_function("std.test.assert_eq", [1, 1]))
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.test.assert_false", [True])

    def test_bench_elapsed_non_negative(self) -> None:
        start = call_native_function("std.bench.now_ms", [])
        elapsed = call_native_function("std.bench.elapsed_ms", [start])
        self.assertGreaterEqual(elapsed, 0.0)

    # --- cli / env / config ---
    def test_cli_parse_flags(self) -> None:
        parsed = call_native_function("std.cli.parse_flags", [["run", "--help"]])
        self.assertEqual(parsed["positionals"], ["run"])
        self.assertTrue(parsed["flags"]["help"])

    def test_config_load_json(self) -> None:
        val = call_native_function('std.config.load_json', ['{"k":1}'])
        self.assertEqual(val, {"k": 1})


class StdlibCoreVmIntegrationTests(unittest.TestCase):
    def test_vm_native_text_math_calls(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_TEXT, "  namaste  "),
                Instruction(OpCode.CALL, "std.text.strip"),
                Instruction(OpCode.CALL, "std.text.upper"),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.PUSH_INT, 121),
                Instruction(OpCode.CALL, "std.math.sqrt"),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        self.assertEqual(SanskriptVM().execute(program), ["NAMASTE", "11.0"])

    def test_vm_native_json_and_csv_calls(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_TEXT, '{"a":2}'),
                Instruction(OpCode.CALL, "std.json.parse"),
                Instruction(OpCode.PUSH_TEXT, "a"),
                Instruction(OpCode.MAP_GET),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.PUSH_TEXT, "name,age\ndev,10\n"),
                Instruction(OpCode.CALL, "std.csv.parse"),
                Instruction(OpCode.PUSH_INT, 0),
                Instruction(OpCode.LIST_GET),
                Instruction(OpCode.PUSH_TEXT, "name"),
                Instruction(OpCode.MAP_GET),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        self.assertEqual(SanskriptVM().execute(program), ["2", "dev"])

    def test_vm_native_env_and_cli_calls(self) -> None:
        key = "SANSKRIPT_PHASE10_TEST_KEY"
        old = os.environ.get(key)
        old_argv = list(sys.argv)
        try:
            os.environ[key] = "visible"
            sys.argv = ["sanskript", "arg1", "arg2"]
            program = BytecodeProgram(
                (
                    Instruction(OpCode.PUSH_TEXT, key),
                    Instruction(OpCode.CALL, "std.env.get"),
                    Instruction(OpCode.EMIT),
                    Instruction(OpCode.CALL, "std.cli.args"),
                    Instruction(OpCode.PUSH_INT, 1),
                    Instruction(OpCode.LIST_GET),
                    Instruction(OpCode.EMIT),
                    Instruction(OpCode.HALT),
                )
            )
            self.assertEqual(SanskriptVM().execute(program), ["visible", "arg2"])
        finally:
            if old is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old
            sys.argv = old_argv

    def test_vm_bytes_and_hash_pipeline(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_TEXT, "data"),
                Instruction(OpCode.CALL, "std.bytes.from_text"),
                Instruction(OpCode.CALL, "std.bytes.to_text"),
                Instruction(OpCode.CALL, "std.hash.sha256"),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        out = SanskriptVM().execute(program)
        self.assertEqual(len(out[0]), 64)

    def test_vm_native_error_surface(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_INT, -1),
                Instruction(OpCode.CALL, "std.math.sqrt"),
                Instruction(OpCode.HALT),
            )
        )
        with self.assertRaises(RuntimeSanskriptError):
            SanskriptVM().execute(program)

    def test_vm_template_render(self) -> None:
        program = BytecodeProgram(
            (
                Instruction(OpCode.PUSH_TEXT, "Hi {{x}}"),
                Instruction(OpCode.MAP_NEW),
                Instruction(OpCode.PUSH_TEXT, "x"),
                Instruction(OpCode.PUSH_TEXT, "dev"),
                Instruction(OpCode.MAP_SET),
                Instruction(OpCode.CALL, "std.template.render"),
                Instruction(OpCode.EMIT),
                Instruction(OpCode.HALT),
            )
        )
        self.assertEqual(SanskriptVM().execute(program), ["Hi dev"])


class StdlibSourceIntegrationTests(unittest.TestCase):
    @staticmethod
    def _compile_without_typecheck(source: str) -> BytecodeProgram:
        program = parse_program(source)
        return lower_ir_to_bytecode(compile_program_to_ir(program))

    @staticmethod
    def _call_targets(program: BytecodeProgram) -> set[str]:
        return {
            str(inst.operand)
            for inst in program.instructions
            if inst.opcode == OpCode.CALL and isinstance(inst.operand, str)
        }

    def test_source_qualified_std_call_parses_and_runs(self) -> None:
        program = parse_program("āhvānam std.text.upper vākyam namaste iti darśayati.")
        display = program.statements[0]
        call_value = display.value
        self.assertEqual(call_value.module, "std.text")
        self.assertEqual(call_value.name, "upper")

        bytecode = self._compile_without_typecheck("āhvānam std.text.upper vākyam namaste iti darśayati.")
        self.assertIn(
            Instruction(OpCode.CALL, "std.text.upper"),
            bytecode.instructions,
        )
        self.assertEqual(SanskriptVM().execute(bytecode), ["NAMASTE"])

    def test_source_json_regex_template_and_test_utils(self) -> None:
        source = """
        āhvānam std.json.parse vākyam {"n":7} iti vastu nidadhāti.
        āhvānam std.serialize vākyam json iti vastu darśayati.
        kośaḥ sandarbhe.
        sthāpanam sandarbhe name vākyam dev iti.
        āhvānam std.template.render vākyam Hi {{ name }} iti sandarbhe darśayati.
        āhvānam std.regex.match vākyam ^\\d+$ iti vākyam 42 iti satyam nidadhāti.
        āhvānam std.test.assert_true satyam.
        """
        out = SanskriptVM().execute(self._compile_without_typecheck(source))
        self.assertEqual(out[0], '{"n":7}')
        self.assertEqual(out[1], "Hi dev")

    def test_source_file_cli_logging_and_process(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "phase10-src.txt").replace("\\", "/")
            source = f"""
            āhvānam std.file.write_text vākyam {path} iti vākyam line1 iti.
            āhvānam std.file.read_text vākyam {path} iti darśayati.
            āhvānam std.log.set_level vākyam INFO iti.
            āhvānam std.log.info vākyam phase10-source-log iti.
            samūhaḥ ādeśe.
            yojanam ādeśe vākyam python iti.
            yojanam ādeśe vākyam -c iti.
            yojanam ādeśe vākyam print('phase10-source') iti.
            āhvānam std.process.run ādeśe phala nidadhāti.
            āhvānam std.serialize vākyam json iti phala darśayati.
            āhvānam std.cli.program_name darśayati.
            """
            out = SanskriptVM().execute(self._compile_without_typecheck(source))
            self.assertIn("line1", out[0])
            self.assertIn("phase10-source", out[1])
            self.assertTrue(out[2])

    def test_source_stdlib_call_lowering_is_generic_across_namespaces(self) -> None:
        source = """
        āhvānam std.cli.program_name darśayati.
        āhvānam std.file.write_text vākyam ./phase10-generic.txt iti vākyam ok iti.
        āhvānam std.file.read_text vākyam ./phase10-generic.txt iti darśayati.
        āhvānam std.json.parse vākyam {"x":1} iti vastu nidadhāti.
        āhvānam std.csv.parse vākyam name,age
        dev,10
        iti paṅktayaḥ nidadhāti.
        āhvānam std.toml.parse vākyam [app]\nname = "sanskript"\n iti tdata nidadhāti.
        āhvānam std.yaml.parse vākyam count: 2 iti ydata nidadhāti.
        āhvānam std.regex.match vākyam ^\\d+$ iti vākyam 108 iti satyam nidadhāti.
        kośaḥ sandarbhe.
        sthāpanam sandarbhe name vākyam mitra iti.
        āhvānam std.template.render vākyam namaste {{ name }} iti sandarbhe darśayati.
        samūhaḥ ādeśe.
        yojanam ādeśe vākyam python iti.
        yojanam ādeśe vākyam -c iti.
        yojanam ādeśe vākyam print('phase10-generic') iti.
        āhvānam std.process.run ādeśe phala nidadhāti.
        āhvānam std.log.set_level vākyam INFO iti.
        āhvānam std.log.info vākyam phase10-generic-log iti.
        āhvānam std.test.assert_true satyam.
        """
        bytecode = self._compile_without_typecheck(source)
        targets = self._call_targets(bytecode)
        expected = {
            "std.cli.program_name",
            "std.file.write_text",
            "std.file.read_text",
            "std.json.parse",
            "std.csv.parse",
            "std.toml.parse",
            "std.yaml.parse",
            "std.regex.match",
            "std.template.render",
            "std.process.run",
            "std.log.set_level",
            "std.log.info",
            "std.test.assert_true",
        }
        self.assertTrue(expected.issubset(targets))
        runnable = """
        āhvānam std.cli.program_name darśayati.
        āhvānam std.file.write_text vākyam ./phase10-generic.txt iti vākyam ok iti.
        āhvānam std.file.read_text vākyam ./phase10-generic.txt iti darśayati.
        āhvānam std.json.parse vākyam {"x":1} iti vastu nidadhāti.
        āhvānam std.csv.parse vākyam name,age
        dev,10
        iti paṅktayaḥ nidadhāti.
        āhvānam std.regex.match vākyam ^\\d+$ iti vākyam 108 iti satyam nidadhāti.
        kośaḥ sandarbhe.
        sthāpanam sandarbhe name vākyam mitra iti.
        āhvānam std.template.render vākyam namaste {{ name }} iti sandarbhe darśayati.
        samūhaḥ ādeśe.
        yojanam ādeśe vākyam python iti.
        yojanam ādeśe vākyam -c iti.
        yojanam ādeśe vākyam print('phase10-generic') iti.
        āhvānam std.process.run ādeśe phala nidadhāti.
        āhvānam std.log.set_level vākyam INFO iti.
        āhvānam std.log.info vākyam phase10-generic-log iti.
        āhvānam std.test.assert_true satyam.
        """
        out = SanskriptVM().execute(self._compile_without_typecheck(runnable))
        self.assertTrue(out)

    def test_source_qualified_target_without_function_rejected(self) -> None:
        with self.assertRaises(CompileError):
            compile_source("āhvānam std.file darśayati.")

    def test_source_unknown_std_function_rejected_during_compile(self) -> None:
        with self.assertRaises(CompileError):
            compile_source("āhvānam std.ghost.nope darśayati.")


class StdlibProcessTests(unittest.TestCase):
    def test_process_run_echo(self) -> None:
        cmd = ["python", "-c", "print('phase10')"]
        result = call_native_function("std.process.run", [cmd])
        self.assertEqual(result["exit"], 0)
        self.assertIn("phase10", result["stdout"])

    def test_process_run_empty_error(self) -> None:
        with self.assertRaises(RuntimeSanskriptError):
            call_native_function("std.process.run", [[]])


if __name__ == "__main__":
    unittest.main()
