import io
import json
import re
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from sanskript.cli import main
from sanskript.compiler import compile_source
from sanskript.webapp import render_web_app


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


class WebAppExportTests(unittest.TestCase):
    def test_render_web_app_embeds_portable_bytecode(self) -> None:
        program = compile_source((EXAMPLES / "prathama.ssk").read_text(encoding="utf-8"))
        html = render_web_app(program, title="Gaṇita")
        match = re.search(
            r'<script id="sanskript-program" type="application/json">(.*?)</script>',
            html,
            flags=re.DOTALL,
        )

        self.assertIsNotNone(match)
        payload = json.loads(match.group(1))
        self.assertEqual(payload["version"], 2)
        self.assertEqual(payload["instructions"][-1]["op"], "halt")
        self.assertIn("runSanskript", html)
        self.assertIn("<h1>Gaṇita</h1>", html)

    def test_cli_web_writes_static_html_runner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "index.html"

            with redirect_stdout(io.StringIO()):
                self.assertEqual(
                    main(
                        [
                            "web",
                            str(EXAMPLES / "prathama.ssk"),
                            "-o",
                            str(output),
                            "--title",
                            "Prathama",
                        ]
                    ),
                    0,
                )

            text = output.read_text(encoding="utf-8")
            self.assertIn("Prathama", text)
            self.assertIn("sanskript-program", text)
            self.assertIn('"op": "emit"', text)

    def test_web_runner_supports_text_bytecode(self) -> None:
        program = compile_source(
            """
            vākyam svāgatam mitra iti phale nidadhāti.
            gaṇakaḥ phalaṃ darśayati.
            """
        )
        html = render_web_app(program, title="Text")

        self.assertIn('"op": "push_text"', html)
        self.assertIn("svāgatam mitra", html)
        self.assertIn("case \"push_text\"", html)


if __name__ == "__main__":
    unittest.main()
