from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sanskript.bytecode import BytecodeProgram, Instruction, OpCode
from sanskript.native_backends import (
    TargetTriple,
    build_native_artifacts,
    calling_convention_layout,
    choose_calling_convention,
    choose_format,
    plan_to_dict,
)


class NativeBackendsTests(unittest.TestCase):
    def test_choose_calling_convention_rejects_unsupported_arch(self) -> None:
        with self.assertRaisesRegex(ValueError, "no calling convention mapping"):
            choose_calling_convention(TargetTriple("riscv64", "unknown", "linux", "gnu"))

    def test_calling_convention_layout_rejects_negative_arg_count(self) -> None:
        with self.assertRaisesRegex(ValueError, "arg_count must be non-negative"):
            calling_convention_layout("sysv64", -1)

    def test_build_native_artifacts_surfaces_unsupported_target_for_native_backend(self) -> None:
        program = BytecodeProgram((Instruction(OpCode.HALT),))
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            with self.assertRaisesRegex(ValueError, "no calling convention mapping"):
                build_native_artifacts(
                    program=program,
                    out_dir=out_dir,
                    target=TargetTriple("riscv64", "unknown", "linux", "gnu"),
                    backend="native-object",
                    artifact_kind="executable",
                )

    def test_portable_backend_accepts_unsupported_target_via_abi_fallback(self) -> None:
        program = BytecodeProgram((Instruction(OpCode.HALT),))
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            plan = build_native_artifacts(
                program=program,
                out_dir=out_dir,
                target=TargetTriple("riscv64", "unknown", "solaris", "gnu"),
                backend="portable-bytecode",
                artifact_kind="executable",
            )
            self.assertIsNotNone(plan.bytecode_path)
            self.assertTrue(any("abi-fallback" in note for note in plan.notes))

    def test_choose_format_rejects_os_format_mismatch(self) -> None:
        with self.assertRaisesRegex(ValueError, "does not match target os"):
            choose_format(
                TargetTriple("x86_64", "unknown", "linux", "gnu"),
                requested="coff",
            )

    def test_native_object_rejects_unknown_target_os(self) -> None:
        program = BytecodeProgram((Instruction(OpCode.HALT),))
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            with self.assertRaisesRegex(ValueError, "does not support target os"):
                build_native_artifacts(
                    program=program,
                    out_dir=out_dir,
                    target=TargetTriple("x86_64", "unknown", "solaris", "gnu"),
                    backend="native-object",
                    artifact_kind="executable",
                )

    def test_native_object_notes_explicitly_mark_stub_scaffold(self) -> None:
        program = BytecodeProgram((Instruction(OpCode.HALT),))
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            plan = build_native_artifacts(
                program=program,
                out_dir=out_dir,
                target=TargetTriple("x86_64", "pc", "windows", "msvc"),
                backend="native-object",
                artifact_kind="executable",
            )
            self.assertTrue(
                any("scaffold stub only" in note for note in plan.notes)
                or plan.implementation_state == "functional"
            )

    def test_plan_to_dict_surfaces_implementation_truth_claims(self) -> None:
        program = BytecodeProgram((Instruction(OpCode.HALT),))
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            portable = build_native_artifacts(
                program=program,
                out_dir=out_dir / "portable",
                target=TargetTriple("x86_64", "unknown", "linux", "gnu"),
                backend="portable-bytecode",
                artifact_kind="executable",
            )
            native = build_native_artifacts(
                program=program,
                out_dir=out_dir / "native",
                target=TargetTriple("x86_64", "unknown", "linux", "gnu"),
                backend="native-object",
                artifact_kind="executable",
            )
            portable_payload = plan_to_dict(portable)
            native_payload = plan_to_dict(native)
            self.assertEqual(portable_payload["implementation_state"], "functional")
            self.assertTrue(portable_payload["truth_claims"]["produces_vm_executable_artifact"])
            self.assertEqual(native_payload["implementation_state"], "scaffold")
            self.assertFalse(native_payload["truth_claims"]["produces_real_linkable_native_object"])
            self.assertTrue(
                native_payload["truth_claims"]["native_link_success_requires_real_object_writer"]
            )


if __name__ == "__main__":
    unittest.main()
