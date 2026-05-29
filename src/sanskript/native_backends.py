from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from .bytecode import BytecodeProgram, dump_bytecode_file


BackendKind = Literal["portable-bytecode", "web-wasm-plan", "native-object"]
BinaryFormat = Literal["coff", "elf", "macho"]
ArtifactKind = Literal["executable", "shared"]
CallingConvention = Literal["win64", "sysv64", "aapcs64"]
ImplementationState = Literal["functional", "scaffold"]
_OS_TO_FORMAT: dict[str, BinaryFormat] = {
    "windows": "coff",
    "linux": "elf",
    "darwin": "macho",
}


@dataclass(frozen=True)
class TargetTriple:
    arch: str
    vendor: str
    os: str
    abi: str

    @property
    def text(self) -> str:
        return f"{self.arch}-{self.vendor}-{self.os}-{self.abi}"


@dataclass(frozen=True)
class CallArgLocation:
    arg_index: int
    kind: str
    location: str


@dataclass(frozen=True)
class NativeBuildPlan:
    backend: BackendKind
    target: TargetTriple
    format: BinaryFormat
    artifact_kind: ArtifactKind
    calling_convention: CallingConvention
    stack_map_path: Path
    debug_symbols_path: Path
    symbol_table_path: Path
    relocations_path: Path
    linker_io_path: Path
    object_path: Path | None = None
    wasm_plan_path: Path | None = None
    bytecode_path: Path | None = None
    linker_command: tuple[str, ...] = ()
    linked_output_path: Path | None = None
    linker_stdout_path: Path | None = None
    linker_stderr_path: Path | None = None
    implementation_state: ImplementationState = "scaffold"
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class BackendSpec:
    kind: BackendKind
    description: str
    emits_object: bool
    emits_portable_bytecode: bool
    emits_wasm_plan: bool
    supports_executable: bool
    supports_shared: bool
    supports_cross_compile: bool


BACKEND_SPECS: dict[BackendKind, BackendSpec] = {
    "portable-bytecode": BackendSpec(
        kind="portable-bytecode",
        description="Canonical execution backend via VM bytecode",
        emits_object=False,
        emits_portable_bytecode=True,
        emits_wasm_plan=False,
        supports_executable=True,
        supports_shared=True,
        supports_cross_compile=True,
    ),
    "web-wasm-plan": BackendSpec(
        kind="web-wasm-plan",
        description="Web/WASM target planning output with bootstrap-safe WAT skeleton",
        emits_object=False,
        emits_portable_bytecode=False,
        emits_wasm_plan=True,
        supports_executable=True,
        supports_shared=False,
        supports_cross_compile=True,
    ),
    "native-object": BackendSpec(
        kind="native-object",
        description="Native object and linker-plan backend for host/cross targets",
        emits_object=True,
        emits_portable_bytecode=False,
        emits_wasm_plan=False,
        supports_executable=True,
        supports_shared=True,
        supports_cross_compile=True,
    ),
}


def host_target_triple() -> TargetTriple:
    machine = platform.machine().lower()
    if machine in {"amd64", "x86_64"}:
        arch = "x86_64"
    elif machine in {"arm64", "aarch64"}:
        arch = "aarch64"
    else:
        arch = machine or "unknown"
    if sys.platform.startswith("win"):
        return TargetTriple(arch, "pc", "windows", "msvc")
    if sys.platform == "darwin":
        return TargetTriple(arch, "apple", "darwin", "gnu")
    return TargetTriple(arch, "unknown", "linux", "gnu")


def parse_target_triple(raw: str | None) -> TargetTriple:
    if not raw:
        return host_target_triple()
    parts = raw.split("-")
    if len(parts) != 4:
        raise ValueError(
            f"target triple must be arch-vendor-os-abi, got {raw!r}"
        )
    arch, vendor, os_name, abi = (item.strip() for item in parts)
    if not (arch and vendor and os_name and abi):
        raise ValueError(f"target triple contains empty parts: {raw!r}")
    return TargetTriple(arch, vendor, os_name, abi)


def choose_format(target: TargetTriple, requested: str | None = None) -> BinaryFormat:
    expected = _OS_TO_FORMAT.get(target.os)
    if expected is None:
        raise ValueError(
            f"unsupported target os {target.os!r}; expected one of {sorted(_OS_TO_FORMAT)}"
        )
    if requested:
        if requested not in {"coff", "elf", "macho"}:
            raise ValueError(f"unsupported object format {requested!r}")
        if requested != expected:
            raise ValueError(
                f"object format {requested!r} does not match target os {target.os!r} "
                f"(expected {expected!r})"
            )
        return requested  # type: ignore[return-value]
    return expected


def choose_calling_convention(target: TargetTriple) -> CallingConvention:
    if target.arch == "x86_64" and target.os == "windows":
        return "win64"
    if target.arch == "x86_64":
        return "sysv64"
    if target.arch == "aarch64":
        return "aapcs64"
    raise ValueError(
        f"no calling convention mapping for target {target.text!r}; "
        "supported arches are x86_64 and aarch64"
    )


def _validate_target_for_backend(target: TargetTriple, backend: BackendKind) -> None:
    if backend != "native-object":
        return
    if target.os not in _OS_TO_FORMAT:
        raise ValueError(
            f"native-object backend does not support target os {target.os!r}; "
            f"expected one of {sorted(_OS_TO_FORMAT)}"
        )


def backend_spec(kind: BackendKind) -> BackendSpec:
    return BACKEND_SPECS[kind]


def calling_convention_layout(cc: CallingConvention, arg_count: int) -> tuple[CallArgLocation, ...]:
    if arg_count < 0:
        raise ValueError(f"arg_count must be non-negative, got {arg_count}")
    if cc == "win64":
        regs = ("rcx", "rdx", "r8", "r9")
    elif cc == "sysv64":
        regs = ("rdi", "rsi", "rdx", "rcx", "r8", "r9")
    else:
        regs = ("x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7")
    locations: list[CallArgLocation] = []
    stack_index = 0
    for idx in range(arg_count):
        if idx < len(regs):
            locations.append(CallArgLocation(idx, "register", regs[idx]))
        else:
            locations.append(CallArgLocation(idx, "stack", f"stack+{stack_index * 8}"))
            stack_index += 1
    return tuple(locations)


def write_stack_map(program: BytecodeProgram, path: Path) -> Path:
    payload = {
        "version": 1,
        "main": [{"ip": i, "stack_depth": 0} for i, _ in enumerate(program.instructions)],
        "functions": {
            fn.name: [{"ip": i, "stack_depth": 0} for i, _ in enumerate(fn.instructions)]
            for fn in program.functions
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_debug_symbols(program: BytecodeProgram, path: Path) -> Path:
    payload = {
        "version": 1,
        "symbols": [
            {"name": "_sanskript_main", "kind": "function", "address_hint": 0},
            *(
                {"name": fn.name, "kind": "function", "address_hint": idx + 1}
                for idx, fn in enumerate(program.functions)
            ),
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_symbol_table(program: BytecodeProgram, path: Path) -> Path:
    payload = {
        "version": 1,
        "symbols": [
            {"name": "_sanskript_main", "section": ".text", "binding": "global"},
            *(
                {"name": fn.name, "section": ".text", "binding": "global"}
                for fn in program.functions
            ),
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_relocations(program: BytecodeProgram, path: Path) -> Path:
    payload = {
        "version": 1,
        "relocations": [
            {"owner": fn.name, "kind": "call", "target": "_sanskript_main", "offset_hint": 0}
            for fn in program.functions
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_linker_io_manifest(target: TargetTriple, path: Path, *, output_kind: ArtifactKind) -> Path:
    payload = {
        "version": 1,
        "target": target.text,
        "inputs": ["program.*.o", "symbols.json", "relocations.json"],
        "output_kind": output_kind,
        "outputs": ["linked-image"],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_object_stub(path: Path, fmt: BinaryFormat) -> Path:
    if fmt == "coff":
        blob = b"\x64\x86\x01\x00\x00\x00\x00\x00SANSKRIPT_COFF_STUB\x00"
    elif fmt == "elf":
        blob = b"\x7fELF\x02\x01\x01\x00SANSKRIPT_ELF_STUB\x00"
    else:
        blob = b"\xcf\xfa\xed\xfeSANSKRIPT_MACHO_STUB\x00"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(blob)
    return path


def write_wasm_plan(path: Path, target: TargetTriple) -> Path:
    text = "\n".join(
        [
            ";; Sanskript Phase 20 WASM backend plan (bootstrap-safe)",
            "(module",
            '  (memory (export "memory") 1)',
            '  (func (export "_start"))',
            f'  ;; target: {target.text}',
            "  ;; notes: portable bytecode remains canonical executable path",
            ")",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _linker_candidates(target: TargetTriple) -> tuple[str, ...]:
    if target.os == "windows":
        return ("lld-link", "link")
    if target.os == "darwin":
        return ("ld64.lld", "ld")
    return ("ld.lld", "ld")


def _link_command(
    *,
    linker: str,
    target: TargetTriple,
    object_path: Path,
    output_path: Path,
    artifact_kind: ArtifactKind,
) -> tuple[str, ...]:
    if target.os == "windows":
        mode = "/DLL" if artifact_kind == "shared" else ""
        return tuple(item for item in (linker, "/NOLOGO", mode, f"/OUT:{output_path}", str(object_path)) if item)
    if target.os == "darwin":
        mode = "-dylib" if artifact_kind == "shared" else ""
        return tuple(item for item in (linker, mode, "-o", str(output_path), str(object_path)) if item)
    mode = "-shared" if artifact_kind == "shared" else ""
    return tuple(item for item in (linker, mode, "-o", str(output_path), str(object_path)) if item)


def _runtime_notes(target: TargetTriple) -> tuple[str, ...]:
    startup_symbol = (
        "mainCRTStartup" if target.os == "windows" else "_start"
    )
    exception_mode = (
        "structured-exception-plan" if target.os == "windows" else "dwarf-unwind-plan"
    )
    std_bindings = (
        "ucrt/kernel32 bridge planned" if target.os == "windows" else "libc bridge planned"
    )
    return (
        f"runtime-startup: planned for {target.text}",
        f"entrypoint: {startup_symbol} -> _sanskript_main",
        f"native-exceptions: {exception_mode}; bootstrap keeps error-return fallback",
        "native-runtime-init: initialize heap, symbol table, and std binding table",
        f"native-std-bindings: {std_bindings}",
        "linking: static and dynamic modes are planned; dynamic path is currently exercised via host linkers",
        "llvm/c/rust: optional accelerators only; portable bytecode remains canonical",
    )


def build_native_artifacts(
    *,
    program: BytecodeProgram,
    out_dir: Path,
    target: TargetTriple,
    backend: BackendKind,
    artifact_kind: ArtifactKind,
    requested_format: str | None = None,
    attempt_link: bool = False,
) -> NativeBuildPlan:
    out_dir.mkdir(parents=True, exist_ok=True)
    spec = backend_spec(backend)
    _validate_target_for_backend(target, backend)
    if artifact_kind == "shared" and not spec.supports_shared:
        raise ValueError(f"backend {backend!r} does not support shared artifacts")
    if artifact_kind == "executable" and not spec.supports_executable:
        raise ValueError(f"backend {backend!r} does not support executable artifacts")
    if backend == "native-object":
        obj_format = choose_format(target, requested_format)
        callconv = choose_calling_convention(target)
        abi_notes: tuple[str, ...] = ()
    else:
        host = host_target_triple()
        if requested_format:
            if requested_format not in {"coff", "elf", "macho"}:
                raise ValueError(f"unsupported object format {requested_format!r}")
            obj_format = requested_format  # type: ignore[assignment]
        else:
            obj_format = _OS_TO_FORMAT.get(target.os, choose_format(host))
        try:
            callconv = choose_calling_convention(target)
            abi_notes = ()
        except ValueError:
            # Portable bytecode / WASM planning must not hard-fail on unknown ABI details.
            callconv = choose_calling_convention(host)
            abi_notes = (
                "abi-fallback: non-native backend used host calling-convention preview for unsupported target arch",
            )
    cross = target.text != host_target_triple().text
    stack_map = write_stack_map(program, out_dir / "stack-map.json")
    debug_symbols = write_debug_symbols(program, out_dir / "debug-symbols.json")
    symbol_table = write_symbol_table(program, out_dir / "symbols.json")
    relocations = write_relocations(program, out_dir / "relocations.json")
    linker_io = write_linker_io_manifest(target, out_dir / "linker-io.json", output_kind=artifact_kind)

    if backend == "portable-bytecode":
        bytecode_path = out_dir / "program.sskbc"
        dump_bytecode_file(program, bytecode_path)
        return NativeBuildPlan(
            backend=backend,
            target=target,
            format=obj_format,
            artifact_kind=artifact_kind,
            calling_convention=callconv,
            stack_map_path=stack_map,
            debug_symbols_path=debug_symbols,
            symbol_table_path=symbol_table,
            relocations_path=relocations,
            linker_io_path=linker_io,
            bytecode_path=bytecode_path,
            implementation_state="functional",
            notes=(
                *_runtime_notes(target),
                f"cross-compilation: {'enabled' if cross else 'host-native'}",
                *abi_notes,
            ),
        )

    if backend == "web-wasm-plan":
        wasm_plan = write_wasm_plan(out_dir / "program.wat", target)
        return NativeBuildPlan(
            backend=backend,
            target=target,
            format=obj_format,
            artifact_kind=artifact_kind,
            calling_convention=callconv,
            stack_map_path=stack_map,
            debug_symbols_path=debug_symbols,
            symbol_table_path=symbol_table,
            relocations_path=relocations,
            linker_io_path=linker_io,
            wasm_plan_path=wasm_plan,
            implementation_state="scaffold",
            notes=(
                *_runtime_notes(target),
                f"cross-compilation: {'enabled' if cross else 'host-native'}",
                *abi_notes,
            ),
        )

    object_path = write_object_stub(out_dir / f"program.{obj_format}.o", obj_format)
    linker_command: tuple[str, ...] = ()
    linked_output: Path | None = None
    linker_stdout_path: Path | None = None
    linker_stderr_path: Path | None = None
    notes = list(_runtime_notes(target))
    notes.append(f"cross-compilation: {'enabled' if cross else 'host-native'}")
    notes.append("object-emission: scaffold stub only; not a fully linkable object writer yet")
    notes.append("static-linking-path: planned via platform archiver + CRT selection")
    notes.append("dynamic-linking-path: linker invocation wiring exists; output viability depends on a real object writer")
    implementation_state: ImplementationState = "scaffold"
    if attempt_link:
        linker = next((name for name in _linker_candidates(target) if shutil.which(name)), None)
        if linker:
            if target.os == "windows":
                suffix = ".dll" if artifact_kind == "shared" else ".exe"
            elif target.os == "darwin":
                suffix = ".dylib" if artifact_kind == "shared" else ".out"
            else:
                suffix = ".so" if artifact_kind == "shared" else ".out"
            linked_output = out_dir / f"program{suffix}"
            linker_command = _link_command(
                linker=linker,
                target=target,
                object_path=object_path,
                output_path=linked_output,
                artifact_kind=artifact_kind,
            )
            try:
                result = subprocess.run(linker_command, check=True, capture_output=True, text=True)
                linker_stdout_path = out_dir / "linker.stdout.txt"
                linker_stderr_path = out_dir / "linker.stderr.txt"
                linker_stdout_path.write_text(result.stdout or "", encoding="utf-8")
                linker_stderr_path.write_text(result.stderr or "", encoding="utf-8")
                if linked_output.is_file():
                    implementation_state = "functional"
                    notes.append("link-success: platform linker produced output")
            except subprocess.CalledProcessError as exc:
                linker_stdout_path = out_dir / "linker.stdout.txt"
                linker_stderr_path = out_dir / "linker.stderr.txt"
                linker_stdout_path.write_text(exc.stdout or "", encoding="utf-8")
                linker_stderr_path.write_text(exc.stderr or "", encoding="utf-8")
                notes.append(
                    f"link-failed: {exc.stderr.strip() or exc.stdout.strip() or 'unknown linker error'}"
                )
                linked_output = None
        else:
            notes.append("link-skipped: no platform linker found in PATH")
        if linked_output is None or not linked_output.is_file():
            from .native_minimal_exe import write_minimal_native_executable

            if target.os == "windows":
                bootstrap_suffix = ".dll" if artifact_kind == "shared" else ".exe"
            elif target.os == "darwin":
                bootstrap_suffix = ".dylib" if artifact_kind == "shared" else ".out"
            else:
                bootstrap_suffix = ".so" if artifact_kind == "shared" else ".out"
            linked_output = write_minimal_native_executable(
                out_dir / f"program{bootstrap_suffix}",
                target=target,
            )
            implementation_state = "functional"
            notes.append(
                "minimal-native-executable: bootstrap PE/ELF/Mach-O writer (functional exit stub; "
                "not full bytecode lowering)"
            )
    else:
        notes.append("link-skipped: dry-run mode")

    return NativeBuildPlan(
        backend=backend,
        target=target,
        format=obj_format,
        artifact_kind=artifact_kind,
        calling_convention=callconv,
        stack_map_path=stack_map,
        debug_symbols_path=debug_symbols,
        symbol_table_path=symbol_table,
        relocations_path=relocations,
        linker_io_path=linker_io,
        object_path=object_path,
        linker_command=linker_command,
        linked_output_path=linked_output,
        linker_stdout_path=linker_stdout_path,
        linker_stderr_path=linker_stderr_path,
        implementation_state=implementation_state,
        notes=tuple(notes),
    )


def plan_to_dict(plan: NativeBuildPlan) -> dict[str, object]:
    spec = backend_spec(plan.backend)
    return {
        "backend": plan.backend,
        "backend_description": spec.description,
        "target": plan.target.text,
        "format": plan.format,
        "artifact_kind": plan.artifact_kind,
        "backend_capabilities": {
            "emits_object": spec.emits_object,
            "emits_portable_bytecode": spec.emits_portable_bytecode,
            "emits_wasm_plan": spec.emits_wasm_plan,
            "supports_executable": spec.supports_executable,
            "supports_shared": spec.supports_shared,
            "supports_cross_compile": spec.supports_cross_compile,
        },
        "calling_convention": plan.calling_convention,
        "calling_convention_layout_preview": [
            {"arg": loc.arg_index, "kind": loc.kind, "location": loc.location}
            for loc in calling_convention_layout(plan.calling_convention, 10)
        ],
        "stack_map_path": str(plan.stack_map_path),
        "debug_symbols_path": str(plan.debug_symbols_path),
        "symbol_table_path": str(plan.symbol_table_path),
        "relocations_path": str(plan.relocations_path),
        "linker_io_path": str(plan.linker_io_path),
        "object_path": str(plan.object_path) if plan.object_path else None,
        "wasm_plan_path": str(plan.wasm_plan_path) if plan.wasm_plan_path else None,
        "bytecode_path": str(plan.bytecode_path) if plan.bytecode_path else None,
        "linker_command": list(plan.linker_command),
        "linked_output_path": str(plan.linked_output_path) if plan.linked_output_path else None,
        "linker_stdout_path": str(plan.linker_stdout_path) if plan.linker_stdout_path else None,
        "linker_stderr_path": str(plan.linker_stderr_path) if plan.linker_stderr_path else None,
        "implementation_state": plan.implementation_state,
        "truth_claims": {
            "produces_vm_executable_artifact": plan.backend == "portable-bytecode",
            "produces_wasm_plan_only": plan.backend == "web-wasm-plan",
            "produces_real_linkable_native_object": False,
            "native_link_success_requires_real_object_writer": plan.backend == "native-object",
        },
        "notes": list(plan.notes),
    }
