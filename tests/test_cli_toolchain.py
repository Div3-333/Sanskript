import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from sanskript.cli import main
from sanskript.compiler import compile_source
from sanskript.vm import SanskriptVM
from sanskript.bytecode import load_bytecode_file


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


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
                    source_output = SanskriptVM().execute(
                        compile_source(example.read_text(encoding="utf-8"))
                    )
                    bytecode_output = SanskriptVM().execute(load_bytecode_file(output))
                    self.assertEqual(bytecode_output, source_output)


if __name__ == "__main__":
    unittest.main()
