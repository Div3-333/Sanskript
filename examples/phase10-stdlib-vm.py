from __future__ import annotations

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode
from sanskript.vm import SanskriptVM


program = BytecodeProgram(
    (
        Instruction(OpCode.PUSH_TEXT, '{"name":"dev","score":9}'),
        Instruction(OpCode.CALL, "std.json.parse"),
        Instruction(OpCode.PUSH_TEXT, "name"),
        Instruction(OpCode.MAP_GET),
        Instruction(OpCode.EMIT),
        Instruction(OpCode.PUSH_TEXT, "  namaste  "),
        Instruction(OpCode.CALL, "std.text.strip"),
        Instruction(OpCode.CALL, "std.text.upper"),
        Instruction(OpCode.EMIT),
        Instruction(OpCode.HALT),
    )
)

print(SanskriptVM().execute(program))
