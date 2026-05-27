"""Phase 10 stdlib demonstration — exercises core namespaces via VM bytecode."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode
from sanskript.stdlib_core import call_native_function, list_native_functions
from sanskript.vm import SanskriptVM


def demo_direct_calls() -> None:
    print("registered std functions:", len(list_native_functions()))
    payload = call_native_function("std.json.parse", ['{"tier":"surakṣita"}'])
    print("json tier:", payload["tier"])
    print("text:", call_native_function("std.text.upper", ["  namaste  "]))
    print("stats mean:", call_native_function("std.stats.mean", [[1, 2, 3, 4]]))
    print("hash:", call_native_function("std.hash.sha256", ["phase10"]))


def demo_vm_pipeline() -> None:
    program = BytecodeProgram(
        (
            Instruction(OpCode.PUSH_TEXT, '{"n":42}'),
            Instruction(OpCode.CALL, "std.json.parse"),
            Instruction(OpCode.PUSH_TEXT, "n"),
            Instruction(OpCode.MAP_GET),
            Instruction(OpCode.EMIT),
            Instruction(OpCode.PUSH_TEXT, "hello"),
            Instruction(OpCode.CALL, "std.text.upper"),
            Instruction(OpCode.EMIT),
            Instruction(OpCode.HALT),
        )
    )
    print("vm output:", SanskriptVM().execute(program))


def demo_file_and_config(tmp: Path) -> None:
    cfg = tmp / "app.toml"
    cfg.write_text('[app]\nname = "demo"\n', encoding="utf-8")
    text = cfg.read_text(encoding="utf-8")
    parsed = call_native_function("std.toml.parse", [text])
    print("toml app name:", parsed["app"]["name"])


def main() -> None:
    demo_direct_calls()
    demo_vm_pipeline()
    with tempfile.TemporaryDirectory() as tmp:
        demo_file_and_config(Path(tmp))
    key = "SANSKRIPT_PHASE10_DEMO"
    old = os.environ.get(key)
    old_argv = list(sys.argv)
    try:
        os.environ[key] = "set"
        sys.argv = ["phase10-stdlib-suite.py", "run"]
        print("env:", call_native_function("std.env.get", [key]))
        print("cli args:", call_native_function("std.cli.args", []))
    finally:
        if old is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = old
        sys.argv = old_argv


if __name__ == "__main__":
    main()
