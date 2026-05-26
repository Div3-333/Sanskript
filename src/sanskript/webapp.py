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
        callStack: [],
        safetyTier: program.safety_tier || "surakshita",
        heap: Object.create(null),
        heapNext: 1,
        unsafeDepth: 0
      }};

      const isFloat = (value) =>
        value !== null && typeof value === "object" && value.__sanskriptFloat === true;
      const makeFloat = (value) => ({{ __sanskriptFloat: true, value }});
      const isRecord = (value) =>
        value !== null && typeof value === "object" && value.__sanskriptRecord === true;
      const makeRecord = () => ({{ __sanskriptRecord: true, fields: Object.create(null) }});
      const isMapValue = (value) =>
        value !== null && typeof value === "object" && !Array.isArray(value) && !isFloat(value) && !isRecord(value);
      const isInt = (value) => Number.isInteger(value) && typeof value === "number";
      const numericPayload = (value) => {{
        if (isFloat(value)) return {{ value: value.value, isFloat: true }};
        if (typeof value === "number" && Number.isFinite(value)) {{
          return {{ value, isFloat: false }};
        }}
        throw new Error("Expected numeric stack value: " + displayValue(value));
      }};
      const isTruthy = (value) => {{
        if (isFloat(value)) return value.value !== 0;
        if (value === false || value === 0 || value === "") return false;
        if (Array.isArray(value)) return value.length > 0;
        if (isMapValue(value)) return Object.keys(value).length > 0;
        if (isRecord(value)) return Object.keys(value.fields).length > 0;
        return true;
      }};
      const valuesEqual = (left, right) => {{
        if ((isFloat(left) || typeof left === "number") && (isFloat(right) || typeof right === "number")) {{
          return numericPayload(left).value === numericPayload(right).value;
        }}
        if (Array.isArray(left) && Array.isArray(right)) {{
          return left.length === right.length && left.every((value, index) => valuesEqual(value, right[index]));
        }}
        if (isMapValue(left) && isMapValue(right)) {{
          const leftKeys = Object.keys(left);
          const rightKeys = Object.keys(right);
          return leftKeys.length === rightKeys.length && leftKeys.every((key) =>
            Object.prototype.hasOwnProperty.call(right, key) && valuesEqual(left[key], right[key])
          );
        }}
        if (isRecord(left) && isRecord(right)) {{
          const leftKeys = Object.keys(left.fields);
          const rightKeys = Object.keys(right.fields);
          return leftKeys.length === rightKeys.length && leftKeys.every((key) =>
            Object.prototype.hasOwnProperty.call(right.fields, key) && valuesEqual(left.fields[key], right.fields[key])
          );
        }}
        return left === right;
      }};
      const displayValue = (value) => {{
        if (isFloat(value)) {{
          const text = String(value.value);
          return Number.isInteger(value.value) ? text + ".0" : text;
        }}
        if (typeof value === "boolean") return value ? "satyam" : "asatyam";
        if (Array.isArray(value)) return "[" + value.map(displayValue).join(", ") + "]";
        if (isMapValue(value)) {{
          return "{{" + Object.keys(value).map((key) => displayValue(key) + ":" + displayValue(value[key])).join(", ") + "}}";
        }}
        if (isRecord(value)) {{
          return "vastu{{" + Object.keys(value.fields).map((key) => displayValue(key) + ":" + displayValue(value.fields[key])).join(", ") + "}}";
        }}
        return String(value);
      }};
      const pop = () => {{
        if (state.stack.length === 0) throw new Error("Sanskript VM stack underflow");
        return state.stack.pop();
      }};
      const popInt = () => {{
        const value = pop();
        if (!isInt(value)) throw new Error("Expected integer stack value: " + displayValue(value));
        return value;
      }};
      const popNumber = () => numericPayload(pop());
      const popList = () => {{
        const value = pop();
        if (!Array.isArray(value)) throw new Error("Expected list, got " + displayValue(value));
        return value;
      }};
      const popMap = () => {{
        const value = pop();
        if (!isMapValue(value)) throw new Error("Expected map, got " + displayValue(value));
        return value;
      }};
      const popRecord = () => {{
        const value = pop();
        if (!isRecord(value)) throw new Error("Expected record, got " + displayValue(value));
        return value;
      }};
      const mapKey = (value) => {{
        if (typeof value === "string" || isInt(value)) return String(value);
        throw new Error("Map key must be text or integer, got " + displayValue(value));
      }};
      const fieldKey = (value) => {{
        if (typeof value === "string" && value.length > 0) return value;
        throw new Error("Record field must be non-empty text, got " + displayValue(value));
      }};
      const requireHeapAccess = (op) => {{
        if (state.safetyTier === "surakshita") {{
          throw new Error(op + " is not allowed in surakshita programs");
        }}
        if (state.safetyTier === "rakshita" && state.unsafeDepth === 0) {{
          throw new Error(op + " in rakshita programs requires unsafe_enter");
        }}
      }};
      const ensureHeapAddress = (address) => {{
        if (!Object.prototype.hasOwnProperty.call(state.heap, String(address))) {{
          throw new Error("Invalid heap address: " + address);
        }}
      }};
      const lookup = (name) => {{
        if (Object.prototype.hasOwnProperty.call(state.locals, name)) return state.locals[name];
        if (Object.prototype.hasOwnProperty.call(state.globals, name)) return state.globals[name];
        throw new Error("Unknown stored value: " + name);
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
        throw new Error("Unknown function: " + target);
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
          case "push_bool":
            state.stack.push(instruction.operand !== 0);
            break;
          case "push_float":
            state.stack.push(makeFloat(instruction.operand));
            break;
          case "list_new":
            state.stack.push([]);
            break;
          case "list_append": {{
            const value = pop();
            const items = popList();
            items.push(value);
            state.stack.push(items);
            break;
          }}
          case "list_len": {{
            state.stack.push(popList().length);
            break;
          }}
          case "list_get": {{
            const index = popInt();
            const items = popList();
            if (index < 0 || index >= items.length) throw new Error("List index " + index + " out of range");
            state.stack.push(items[index]);
            break;
          }}
          case "map_new":
            state.stack.push(Object.create(null));
            break;
          case "map_set": {{
            const value = pop();
            const key = mapKey(pop());
            const table = popMap();
            table[key] = value;
            state.stack.push(table);
            break;
          }}
          case "map_get": {{
            const key = mapKey(pop());
            const table = popMap();
            if (!(key in table)) throw new Error("Map has no entry for key " + key);
            state.stack.push(table[key]);
            break;
          }}
          case "map_contains": {{
            const key = mapKey(pop());
            const table = popMap();
            state.stack.push(key in table ? 1 : 0);
            break;
          }}
          case "record_new":
            state.stack.push(makeRecord());
            break;
          case "record_set": {{
            const value = pop();
            const field = fieldKey(pop());
            const record = popRecord();
            record.fields[field] = value;
            state.stack.push(record);
            break;
          }}
          case "record_get": {{
            const field = fieldKey(pop());
            const record = popRecord();
            if (!(field in record.fields)) throw new Error("Record has no field " + field);
            state.stack.push(record.fields[field]);
            break;
          }}
          case "record_contains": {{
            const field = fieldKey(pop());
            const record = popRecord();
            state.stack.push(field in record.fields ? 1 : 0);
            break;
          }}
          case "load_name":
            state.stack.push(lookup(instruction.operand));
            break;
          case "store_name":
            store(instruction.operand, pop());
            break;
          case "add": {{
            const right = popNumber();
            const left = popNumber();
            const value = left.value + right.value;
            state.stack.push(left.isFloat || right.isFloat ? makeFloat(value) : value);
            break;
          }}
          case "subtract": {{
            const right = popNumber();
            const left = popNumber();
            const value = left.value - right.value;
            state.stack.push(left.isFloat || right.isFloat ? makeFloat(value) : value);
            break;
          }}
          case "multiply": {{
            const right = popNumber();
            const left = popNumber();
            const value = left.value * right.value;
            state.stack.push(left.isFloat || right.isFloat ? makeFloat(value) : value);
            break;
          }}
          case "divide": {{
            const right = popNumber();
            if (right.value === 0) throw new Error("Division by zero");
            const left = popNumber();
            if (left.isFloat || right.isFloat) state.stack.push(makeFloat(left.value / right.value));
            else state.stack.push(Math.trunc(left.value / right.value));
            break;
          }}
          case "compare_eq": {{
            const right = pop();
            const left = pop();
            state.stack.push(valuesEqual(left, right) ? 1 : 0);
            break;
          }}
          case "compare_lt": {{
            const right = popInt();
            const left = popInt();
            state.stack.push(left < right ? 1 : 0);
            break;
          }}
          case "heap_alloc": {{
            requireHeapAccess("heap_alloc");
            const size = popInt();
            if (size < 0) throw new Error("heap_alloc size must be non-negative");
            const address = state.heapNext;
            state.heapNext += Math.max(1, size);
            for (let offset = 0; offset < size; offset += 1) state.heap[address + offset] = 0;
            state.stack.push(address);
            break;
          }}
          case "heap_store": {{
            requireHeapAccess("heap_store");
            const value = popInt();
            const address = popInt();
            ensureHeapAddress(address);
            state.heap[address] = value;
            break;
          }}
          case "heap_load": {{
            requireHeapAccess("heap_load");
            const address = popInt();
            ensureHeapAddress(address);
            state.stack.push(state.heap[address]);
            break;
          }}
          case "heap_free": {{
            requireHeapAccess("heap_free");
            const address = popInt();
            delete state.heap[address];
            break;
          }}
          case "unsafe_enter":
            state.unsafeDepth += 1;
            break;
          case "unsafe_exit":
            if (state.unsafeDepth === 0) throw new Error("unsafe_exit without matching unsafe_enter");
            state.unsafeDepth -= 1;
            break;
          case "emit":
            state.output.push(displayValue(pop()));
            break;
          case "jump":
            ip = instruction.operand;
            continue;
          case "jump_if_zero":
            if (!isTruthy(pop())) {{
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
            throw new Error("Unknown opcode: " + instruction.op);
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
