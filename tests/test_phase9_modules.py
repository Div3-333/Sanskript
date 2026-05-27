from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from sanskript.compiler import compile_program
from sanskript.errors import CompileError
from sanskript.module_loader import load_program_from_path
from sanskript.package_lock import LOCK_FILE, build_lock_from_manifest, load_lock, write_lock
from sanskript.package_manifest import load_manifest
from sanskript.package_resolver import build_package_context, resolve_import_path
from sanskript.package_signing import sign_package, verify_package_signature
from sanskript.vm import SanskriptVM

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = REPO_ROOT / "examples" / "phase9-modules"

MODULE_SOURCE = """
kṣetram gaṇita.
vidhānam vṛddhi.
gaṇakaḥ daśa phale nidadhāti.
gaṇakaḥ phalaṃ ekena vardhayati.
samāpanam.
niḥsāram vṛddhi.
vidhānam guhya.
gaṇakaḥ daśa phale nidadhāti.
gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
samāpanam.
samāpanam.
"""


class Phase9ModuleTests(unittest.TestCase):
    def test_module_file_import_and_alias_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "gaṇita.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "main.ssk").write_text(
                """
                ānayanam gaṇita nāmnā m.
                gaṇakaḥ ekam phale nidadhāti.
                āhvānam m vṛddhi.
                gaṇakaḥ phalaṃ darśayati.
                """,
                encoding="utf-8",
            )
            program = load_program_from_path(root / "main.ssk")
            output = SanskriptVM().execute(compile_program(program))
            self.assertEqual(output, ["11"])

    def test_selective_import_with_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "gaṇita.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "main.ssk").write_text(
                """
                ānayanam gaṇita antaḥ vṛddhi nāmnā vardhana.
                gaṇakaḥ ekam phale nidadhāti.
                āhvānam vardhana.
                gaṇakaḥ phalaṃ darśayati.
                """,
                encoding="utf-8",
            )
            program = load_program_from_path(root / "main.ssk")
            output = SanskriptVM().execute(compile_program(program))
            self.assertEqual(output, ["11"])

    def test_package_directory_import_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pkg = root / "pkg"
            pkg.mkdir()
            (pkg / "gaṇita.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "main.ssk").write_text(
                """
                ānayanam pkg/gaṇita nāmnā m.
                gaṇakaḥ ekam phale nidadhāti.
                āhvānam m vṛddhi.
                gaṇakaḥ phalaṃ darśayati.
                """,
                encoding="utf-8",
            )
            program = load_program_from_path(root / "main.ssk")
            output = SanskriptVM().execute(compile_program(program))
            self.assertEqual(output, ["11"])

    def test_private_module_member_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "gaṇita.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "main.ssk").write_text(
                """
                ānayanam gaṇita.
                gaṇakaḥ ekam phale nidadhāti.
                āhvānam gaṇita guhya.
                gaṇakaḥ phalaṃ darśayati.
                """,
                encoding="utf-8",
            )
            with self.assertRaises(CompileError):
                compile_program(load_program_from_path(root / "main.ssk"))

    def test_missing_import_reports_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "main.ssk").write_text("ānayanam na_asti.", encoding="utf-8")
            with self.assertRaises(CompileError):
                load_program_from_path(root / "main.ssk")

    def test_relative_import_sibling(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "gaṇita.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            sub = root / "app"
            sub.mkdir()
            (sub / "main.ssk").write_text(
                """
                ānayanam ../gaṇita nāmnā m.
                gaṇakaḥ ekam phale nidadhāti.
                āhvānam m vṛddhi.
                gaṇakaḥ phalaṃ darśayati.
                """,
                encoding="utf-8",
            )
            output = SanskriptVM().execute(compile_program(load_program_from_path(sub / "main.ssk")))
            self.assertEqual(output, ["11"])

    def test_absolute_import_user_namespace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lib = root / "lib"
            lib.mkdir()
            (lib / "gaṇita.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "main.ssk").write_text(
                """
                ānayanam @lib/gaṇita nāmnā m.
                gaṇakaḥ ekam phale nidadhāti.
                āhvānam m vṛddhi.
                gaṇakaḥ phalaṃ darśayati.
                """,
                encoding="utf-8",
            )
            output = SanskriptVM().execute(compile_program(load_program_from_path(root / "main.ssk")))
            self.assertEqual(output, ["11"])

    def test_stdlib_namespace_import(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "main.ssk").write_text(
                """
                ānayanam @stdlib/prathama nāmnā std.
                āhvānam std ekam.
                gaṇakaḥ phalaṃ darśayati.
                """,
                encoding="utf-8",
            )
            os.environ["SANSKRIPT_STDLIB"] = str(REPO_ROOT / "data" / "stdlib")
            try:
                output = SanskriptVM().execute(compile_program(load_program_from_path(root / "main.ssk")))
            finally:
                os.environ.pop("SANSKRIPT_STDLIB", None)
            self.assertEqual(output, ["1"])

    def test_reexport_through_facade_module(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "gaṇita.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "facade.ssk").write_text(
                """
                kṣetram facade.
                ānayanam gaṇita.
                punaranayanam gaṇita antaḥ vṛddhi.
                niḥsāram vṛddhi.
                samāpanam.
                """,
                encoding="utf-8",
            )
            (root / "main.ssk").write_text(
                """
                ānayanam facade.
                gaṇakaḥ ekam phale nidadhāti.
                āhvānam facade vṛddhi.
                gaṇakaḥ phalaṃ darśayati.
                """,
                encoding="utf-8",
            )
            output = SanskriptVM().execute(compile_program(load_program_from_path(root / "main.ssk")))
            self.assertEqual(output, ["11"])

    def test_package_initialization_module_loads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pkg = root / "pkg"
            pkg.mkdir()
            (pkg / "samārambha.ssk").write_text(
                """
                kṣetram pkg.
                vidhānam ārambhaḥ.
                gaṇakaḥ śūnyam phale nidadhāti.
                samāpanam.
                niḥsāram ārambhaḥ.
                samāpanam.
                """,
                encoding="utf-8",
            )
            (pkg / "gaṇita.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "main.ssk").write_text(
                """
                ānayanam pkg/gaṇita nāmnā m.
                āhvānam pkg ārambhaḥ.
                gaṇakaḥ phalaṃ darśayati.
                """,
                encoding="utf-8",
            )
            program = load_program_from_path(root / "main.ssk")
            module_names = {module.name for module in program.modules}
            self.assertIn("pkg", module_names)
            self.assertIn("gaṇita", module_names)

    def test_manifest_version_and_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lib = root / "lib"
            lib.mkdir()
            (lib / "dep.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "ssk.toml").write_text(
                """
                [package]
                name = "demo"
                version = "2.3.4"

                [dependencies.local]
                dep = { path = "lib/dep.ssk" }
                """,
                encoding="utf-8",
            )
            ctx = build_package_context(root / "main.ssk")
            self.assertEqual(ctx.manifest.name, "demo")
            self.assertEqual(ctx.manifest.version, "2.3.4")
            self.assertEqual(len(ctx.manifest.dependencies), 1)

    def test_prose_manifest_parsing(self) -> None:
        manifest = load_manifest(EXAMPLES / "saṃskaraṇa-prose.sskm")
        self.assertEqual(manifest.name, "prose-demo")
        self.assertEqual(manifest.version, "0.2.0")
        self.assertTrue(manifest.features.get("json"))

    def test_feature_flag_gated_import(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "gaṇita.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "ssk.toml").write_text(
                """
                [package]
                name = "demo"
                version = "1.0.0"

                [features]
                json = false
                """,
                encoding="utf-8",
            )
            (root / "main.ssk").write_text(
                """
                ānayanam gaṇita viśeṣe json.
                """,
                encoding="utf-8",
            )
            with self.assertRaises(CompileError):
                load_program_from_path(root / "main.ssk")

    def test_build_profile_requires_feature(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ssk.toml").write_text(
                """
                [package]
                name = "demo"
                version = "1.0.0"

                [features]
                json = false

                [profile.release]
                requires = "json"
                """,
                encoding="utf-8",
            )
            (root / "main.ssk").write_text("gaṇakaḥ ekam phale nidadhāti.", encoding="utf-8")
            with self.assertRaises(CompileError):
                load_program_from_path(root / "main.ssk", profile="release")

    def test_lockfile_hash_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dep = root / "lib"
            dep.mkdir()
            target = dep / "dep.ssk"
            target.write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "ssk.toml").write_text(
                """
                [package]
                name = "demo"
                version = "1.0.0"

                [dependencies.local]
                dep = { path = "lib/dep.ssk" }
                """,
                encoding="utf-8",
            )
            manifest = load_manifest(root / "ssk.toml")
            lock = build_lock_from_manifest(root, manifest)
            write_lock(root, lock)
            target.write_text("kṣetram x.\nsamāpanam.\n", encoding="utf-8")
            with self.assertRaises(CompileError):
                build_package_context(root / "main.ssk")

    def test_package_signing_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "main.ssk").write_text("gaṇakaḥ ekam phale nidadhāti.", encoding="utf-8")
            (root / "ssk.toml").write_text(
                """
                [package]
                name = "demo"
                version = "1.0.0"
                """,
                encoding="utf-8",
            )
            signature = sign_package(root)
            (root / "ssk.toml").write_text(
                f"""
                [package]
                name = "demo"
                version = "1.0.0"
                signature = "{signature}"
                """,
                encoding="utf-8",
            )
            verify_package_signature(root, signature)
            (root / "ssk.toml").write_text(
                """
                [package]
                name = "demo"
                version = "1.0.0"
                signature = "bad"
                """,
                encoding="utf-8",
            )
            with self.assertRaises(CompileError):
                build_package_context(root / "main.ssk")

    def test_registry_dependency_from_vendor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor = root / "vendor" / "serde"
            vendor.mkdir(parents=True)
            (vendor / "entry.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "ssk.toml").write_text(
                """
                [package]
                name = "demo"
                version = "1.0.0"

                [dependencies.registry]
                serde = { version = "0.1.0", registry = "ssk" }
                """,
                encoding="utf-8",
            )
            ctx = build_package_context(root / "main.ssk")
            resolved = ctx.import_bindings["serde"]
            self.assertTrue(resolved.exists())

    def test_vendored_dependency_with_lock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor = root / "vendor" / "legacy"
            vendor.mkdir(parents=True)
            (vendor / "legacy.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "ssk.toml").write_text(
                """
                [package]
                name = "demo"
                version = "1.0.0"

                [dependencies.vendored]
                legacy = { path = "vendor/legacy/legacy.ssk", locked = true }
                """,
                encoding="utf-8",
            )
            manifest = load_manifest(root / "ssk.toml")
            write_lock(root, build_lock_from_manifest(root, manifest))
            lock = load_lock(root)
            self.assertIsNotNone(lock)
            self.assertEqual(lock.package_name, "demo")

    def test_import_name_conflict_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "b.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            (root / "main.ssk").write_text(
                """
                ānayanam a nāmnā m.
                ānayanam b nāmnā m.
                """,
                encoding="utf-8",
            )
            with self.assertRaises(CompileError) as ctx_err:
                load_program_from_path(root / "main.ssk")
            self.assertIn("conflict", str(ctx_err.exception).lower())

    def test_platform_specific_module_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            platform = "windows" if sys.platform.startswith("win") else "linux"
            (root / f"mod.{platform}.ssk").write_text(MODULE_SOURCE, encoding="utf-8")
            ctx = build_package_context(root / "main.ssk")
            resolved = resolve_import_path(ctx, root, "mod")
            self.assertTrue(resolved.name.endswith(f".{platform}.ssk"))

    def test_phase9_example_program_runs(self) -> None:
        if not (EXAMPLES / "main.ssk").is_file():
            self.skipTest("phase9 example missing")
        os.environ["SANSKRIPT_STDLIB"] = str(REPO_ROOT / "data" / "stdlib")
        try:
            program = load_program_from_path(EXAMPLES / "main.ssk")
            output = SanskriptVM().execute(compile_program(program))
        finally:
            os.environ.pop("SANSKRIPT_STDLIB", None)
        self.assertTrue(output)


if __name__ == "__main__":
    unittest.main()
