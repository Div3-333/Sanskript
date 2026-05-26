from __future__ import annotations

import html
import json
from pathlib import Path

from .bytecode import BytecodeProgram, encode_program, load_bytecode_file
from .compiler import compile_source
from .yantra_patha import program_from_yantra_patha


def load_program_for_web(source: Path) -> BytecodeProgram:
    if source.suffix == ".sskbc":
        return load_bytecode_file(source)
    if source.suffix == ".sskyp":
        return program_from_yantra_patha(source.read_text(encoding="utf-8"))
    return compile_source(source.read_text(encoding="utf-8"))


def render_web_app(program: BytecodeProgram, *, title: str = "Sanskript App") -> str:
    payload = json.dumps(encode_program(program), ensure_ascii=False)
    safe_payload = payload.replace("</", "<\\/")
    safe_title = html.escape(title, quote=True)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #1f2328;
      --muted: #667085;
      --line: #d7dce2;
      --paper: #fbfaf7;
      --panel: #ffffff;
      --accent: #256f5d;
      --accent-strong: #174b3f;
      --warn: #a43f3f;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--paper);
    }}
    main {{
      width: min(960px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 32px 0;
    }}
    header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 20px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 16px;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(1.4rem, 3vw, 2.1rem);
      font-weight: 720;
      letter-spacing: 0;
    }}
    button {{
      appearance: none;
      border: 1px solid var(--accent-strong);
      background: var(--accent);
      color: white;
      min-height: 40px;
      padding: 0 16px;
      border-radius: 8px;
      font: inherit;
      font-weight: 650;
      cursor: pointer;
    }}
    button:focus-visible {{
      outline: 3px solid #9bd5c8;
      outline-offset: 2px;
    }}
    section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }}
    h2 {{
      margin: 0 0 12px;
      font-size: 1rem;
      letter-spacing: 0;
    }}
    pre {{
      margin: 0;
      min-height: 160px;
      padding: 16px;
      overflow: auto;
      border-radius: 8px;
      background: #111827;
      color: #f7fafc;
      font: 0.95rem/1.6 ui-monospace, SFMono-Regular, Consolas, monospace;
      white-space: pre-wrap;
    }}
    .status {{
      margin: 12px 0 0;
      color: var(--muted);
      font-size: 0.95rem;
    }}
    .error {{ color: var(--warn); }}
    @media (max-width: 560px) {{
      header {{ align-items: stretch; flex-direction: column; }}
      button {{ width: 100%; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>{safe_title}</h1>
      <button id="run" type="button">Run</button>
    </header>
    <section aria-labelledby="output-title">
      <h2 id="output-title">Output</h2>
      <pre id="output" aria-live="polite"></pre>
      <p class="status" id="status">Ready.</p>
    </section>
  </main>
  <script id="sanskript-program" type="application/json">{safe_payload}</script>
  <script>
    const program = JSON.parse(document.getElementById("sanskript-program").textContent);
    const outputElement = document.getElementById("output");
    const statusElement = document.getElementById("status");

    function runSanskript(program) {{
      const state = {{
        globals: Object.create(null),
        locals: Object.create(null),
        stack: [],
        output: [],
        instructions: program.instructions,
        callStack: []
      }};

      const pop = () => {{
        if (state.stack.length === 0) throw new Error("Sanskript VM stack underflow");
        return state.stack.pop();
      }};
      const popInt = () => {{
        const value = pop();
        if (!Number.isInteger(value)) throw new Error(`Expected integer stack value: ${{value}}`);
        return value;
      }};
      const lookup = (name) => {{
        if (Object.prototype.hasOwnProperty.call(state.locals, name)) return state.locals[name];
        if (Object.prototype.hasOwnProperty.call(state.globals, name)) return state.globals[name];
        throw new Error(`Unknown stored value: ${{name}}`);
      }};
      const store = (name, value) => {{
        if (Object.prototype.hasOwnProperty.call(state.locals, name)) state.locals[name] = value;
        else state.globals[name] = value;
      }};
      const resolve = (target) => {{
        if (target.includes(".")) {{
          const [moduleName, functionName] = target.split(".", 2);
          const module = (program.modules || []).find((item) => item.name === moduleName);
          const found = module && (module.functions || []).find((item) => item.name === target || item.name === functionName);
          if (found) return found;
        }} else {{
          const found = (program.functions || []).find((item) => item.name === target);
          if (found) return found;
        }}
        throw new Error(`Unknown function: ${{target}}`);
      }};

      let ip = 0;
      while (ip < state.instructions.length) {{
        const instruction = state.instructions[ip];
        switch (instruction.op) {{
          case "push_int":
            state.stack.push(instruction.operand);
            break;
          case "push_text":
            state.stack.push(instruction.operand);
            break;
          case "load_name":
            state.stack.push(lookup(instruction.operand));
            break;
          case "store_name":
            store(instruction.operand, pop());
            break;
          case "add": {{
            const right = popInt();
            const left = popInt();
            state.stack.push(left + right);
            break;
          }}
          case "subtract": {{
            const right = popInt();
            const left = popInt();
            state.stack.push(left - right);
            break;
          }}
          case "multiply": {{
            const right = popInt();
            const left = popInt();
            state.stack.push(left * right);
            break;
          }}
          case "divide": {{
            const right = popInt();
            if (right === 0) throw new Error("Division by zero");
            const left = popInt();
            state.stack.push(Math.trunc(left / right));
            break;
          }}
          case "compare_eq": {{
            const right = pop();
            const left = pop();
            state.stack.push(left === right ? 1 : 0);
            break;
          }}
          case "compare_lt": {{
            const right = popInt();
            const left = popInt();
            state.stack.push(left < right ? 1 : 0);
            break;
          }}
          case "emit":
            state.output.push(String(pop()));
            break;
          case "jump":
            ip = instruction.operand;
            continue;
          case "jump_if_zero":
            if (popInt() === 0) {{
              ip = instruction.operand;
              continue;
            }}
            break;
          case "call": {{
            const fn = resolve(instruction.operand);
            const params = fn.params || [];
            const args = [];
            for (const _ of params) args.push(pop());
            args.reverse();
            const locals = Object.create(null);
            params.forEach((name, index) => {{ locals[name] = args[index]; }});
            state.callStack.push({{
              returnIp: ip + 1,
              instructions: state.instructions,
              locals: {{ ...state.locals }}
            }});
            state.locals = locals;
            state.instructions = fn.instructions;
            ip = 0;
            continue;
          }}
          case "return": {{
            const value = pop();
            const frame = state.callStack.pop();
            if (!frame) throw new Error("RETURN outside of a function call");
            state.instructions = frame.instructions;
            state.locals = frame.locals;
            state.stack.push(value);
            ip = frame.returnIp;
            continue;
          }}
          case "pop":
            pop();
            break;
          case "halt":
            if (state.callStack.length > 0) {{
              const frame = state.callStack.pop();
              state.instructions = frame.instructions;
              state.locals = frame.locals;
              ip = frame.returnIp;
              continue;
            }}
            return state.output;
          default:
            throw new Error(`Unknown opcode: ${{instruction.op}}`);
        }}
        ip += 1;
      }}
      return state.output;
    }}

    function render() {{
      statusElement.className = "status";
      statusElement.textContent = "Running...";
      try {{
        const output = runSanskript(program);
        outputElement.textContent = output.join("\\n");
        statusElement.textContent = "Finished.";
      }} catch (error) {{
        outputElement.textContent = "";
        statusElement.className = "status error";
        statusElement.textContent = error.message;
      }}
    }}

    document.getElementById("run").addEventListener("click", render);
    render();
  </script>
</body>
</html>
"""


def write_web_app(program: BytecodeProgram, path: Path, *, title: str = "Sanskript App") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_web_app(program, title=title), encoding="utf-8")


__all__ = ["load_program_for_web", "render_web_app", "write_web_app"]
