"""Phase 10 standard library implementations (VM-callable via std.* names)."""

from __future__ import annotations

import asyncio
import base64
import binascii
import csv
import gzip
import hashlib
import hmac
import io
import json
import logging
import math
import os
import random
import re
import secrets
import signal
import socket
import sqlite3
import struct
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import heapq
import http.server
import copy
from collections import deque
from bisect import bisect_left
from queue import Empty, Full, Queue
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zlib
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePath
from zoneinfo import ZoneInfo

from .errors import RuntimeSanskriptError
from .phase3_values import text_grapheme_len
from .runtime_values import (
    ByteArrayValue,
    BytesValue,
    NIL,
    NilValue,
    OpaqueHandle,
    OptionValue,
    RecordValue,
    ResultValue,
)
from .phase21_cross_platform import (
    browser_fetch_simulation,
    detect_platform_features,
    host_platform_family,
    join_path_for_platform,
    normalize_path_for_platform,
    platform_compile_plan,
    web_storage_load,
    web_storage_save,
    web_worker_bridge_new,
    web_worker_post_message,
    web_worker_recv,
)
from . import phase22_web_apps as _p22
from .stdlib_common import (
    NativeSpec,
    expect_bool,
    expect_bytes,
    expect_int,
    expect_list,
    expect_map,
    expect_number,
    expect_text,
    from_json,
    parse_json_text,
    stringify_json,
    to_json,
)


def _as_hashable(value: object, fn_name: str) -> object:
    if isinstance(value, NilValue):
        return ("nil",)
    if isinstance(value, bool):
        return ("bool", value)
    if isinstance(value, int):
        return ("int", value)
    if isinstance(value, float):
        if math.isnan(value):
            return ("float", "nan")
        return ("float", value)
    if isinstance(value, str):
        return ("str", value)
    if isinstance(value, type(None)):
        return ("none", None)
    if isinstance(value, list):
        return ("list", tuple(_as_hashable(item, fn_name) for item in value))
    if isinstance(value, dict):
        return ("dict", tuple(sorted((str(k), _as_hashable(v, fn_name)) for k, v in value.items())))
    raise RuntimeSanskriptError(f"{fn_name} expected hashable-compatible value, got {value!r}")


def _deterministic_order_key(value: object) -> tuple[int, str]:
    if value is None:
        return (0, "None")
    if isinstance(value, bool):
        return (1, "1" if value else "0")
    if isinstance(value, int):
        return (2, repr(float(value)))
    if isinstance(value, float):
        if math.isnan(value):
            return (3, "nan")
        if math.isinf(value):
            return (3, "inf" if value > 0 else "-inf")
        return (2, repr(float(value))) if value.is_integer() else (3, repr(value))
    if isinstance(value, str):
        return (4, value)
    if isinstance(value, list):
        parts = "|".join(f"{kind}:{token}" for kind, token in (_deterministic_order_key(item) for item in value))
        return (5, parts)
    if isinstance(value, dict):
        parts = "|".join(
            f"{key}={kind}:{token}"
            for key, (kind, token) in sorted((str(k), _deterministic_order_key(v)) for k, v in value.items())
        )
        return (6, parts)
    if isinstance(value, tuple):
        parts = "|".join(f"{kind}:{token}" for kind, token in (_deterministic_order_key(item) for item in value))
        return (7, parts)
    return (8, f"{type(value).__name__}:{repr(value)}")


_REGISTRY_LOCK = threading.Lock()
_ATOMIC_REGISTRY: dict[int, dict[str, object]] = {}
_LOCK_REGISTRY: dict[int, threading.Lock] = {}
_CHANNEL_REGISTRY: dict[int, Queue] = {}
_ASYNC_IO_POOL = ThreadPoolExecutor(max_workers=4, thread_name_prefix="sanskript-async-io")
_MEMORY_REGISTRY: dict[int, dict[str, object]] = {}
_MEMORY_REF_REGISTRY: dict[int, dict[str, object]] = {}
_BORROW_REGISTRY: dict[int, dict[str, object]] = {}
_HANDLE_COUNTER = 1
_FENCE_COUNTER = 0
_WATCH_SNAPSHOT_REGISTRY: dict[int, dict[str, dict[str, float | int]]] = {}
_WEB_STORAGE: dict[str, dict[str, str]] = {}
_WEB_WORKER_QUEUES: dict[int, object] = {}
_FFI_ALLOWLIST = frozenset(
    {
        "std.file.read_text",
        "std.file.write_text",
        "std.path.exists",
        "std.net.resolve_host",
    }
)


def _next_handle_id() -> int:
    global _HANDLE_COUNTER
    current = _HANDLE_COUNTER
    _HANDLE_COUNTER += 1
    return current


def _memory_block_from_handle(handle: object, *, fn_name: str) -> dict[str, object]:
    if not isinstance(handle, OpaqueHandle) or handle.kind != "mem.block":
        raise RuntimeSanskriptError(f"{fn_name} expects memory block handle")
    block = _MEMORY_REGISTRY.get(handle.handle_id)
    if block is None:
        raise RuntimeSanskriptError(f"{fn_name} unknown memory block handle")
    if bool(block.get("dropped", False)):
        raise RuntimeSanskriptError(f"{fn_name} memory block was dropped")
    if bool(block.get("moved", False)):
        raise RuntimeSanskriptError(f"{fn_name} memory block was moved")
    return block


def _memory_ref_from_handle(handle: object, *, fn_name: str) -> dict[str, object]:
    if not isinstance(handle, OpaqueHandle) or handle.kind != "mem.ref":
        raise RuntimeSanskriptError(f"{fn_name} expects memory reference handle")
    ref = _MEMORY_REF_REGISTRY.get(handle.handle_id)
    if ref is None:
        raise RuntimeSanskriptError(f"{fn_name} unknown memory reference handle")
    return ref


def _borrow_from_handle(handle: object, *, fn_name: str) -> dict[str, object]:
    if not isinstance(handle, OpaqueHandle) or handle.kind != "mem.borrow":
        raise RuntimeSanskriptError(f"{fn_name} expects borrow handle")
    borrow = _BORROW_REGISTRY.get(handle.handle_id)
    if borrow is None:
        raise RuntimeSanskriptError(f"{fn_name} unknown borrow handle")
    return borrow


def _borrow_state(block: dict[str, object]) -> tuple[int, int]:
    return int(block.get("shared_borrows", 0)), int(block.get("mut_borrows", 0))


def _require_mutation_allowed(block: dict[str, object], fn_name: str) -> None:
    shared, mutable = _borrow_state(block)
    if shared > 0 or mutable > 0:
        raise RuntimeSanskriptError(
            f"{fn_name} cannot mutate while borrows are active (shared={shared}, mutable={mutable})"
        )


def _memory_ref_locate(ref: dict[str, object], *, width: int, fn_name: str) -> tuple[dict[str, object], int, int]:
    block_handle = ref.get("block")
    if not isinstance(block_handle, OpaqueHandle):
        raise RuntimeSanskriptError(f"{fn_name} invalid reference block")
    block = _memory_block_from_handle(block_handle, fn_name=fn_name)
    offset = int(ref.get("offset", 0))
    size = int(block.get("size", 0))
    if offset < 0 or offset + width > size:
        raise RuntimeSanskriptError(f"{fn_name} out-of-bounds memory access")
    absolute = int(block.get("base", 0)) + offset
    return block, offset, absolute


def _memory_allowed_abi(*, layout: str) -> frozenset[str]:
    if layout == "abi":
        return frozenset({"sysv64", "win64", "aapcs64", "native"})
    if layout == "repr-c":
        return frozenset({"c", "native"})
    return frozenset({"native"})


def _resolve_atomic(args: list, *, fn_name: str) -> tuple[dict[str, int], tuple[dict[str, object], int] | None]:
    handle = args[0]
    if not isinstance(handle, OpaqueHandle) or handle.kind != "atomic":
        raise RuntimeSanskriptError(f"{fn_name} expects atomic handle")
    atom = _ATOMIC_REGISTRY.get(handle.handle_id)
    if atom is None:
        raise RuntimeSanskriptError(f"{fn_name} unknown atomic handle")
    bound_ref = atom.get("bound_ref")
    if isinstance(bound_ref, OpaqueHandle) and bound_ref.kind == "mem.ref":
        ref = _memory_ref_from_handle(bound_ref, fn_name=fn_name)
        block, offset, _ = _memory_ref_locate(ref, width=1, fn_name=fn_name)
        return atom, (block, offset)
    return atom, None


def _is_send_safe(value: object) -> bool:
    if value is None or isinstance(value, (str, int, float, bool, NilValue, BytesValue)):
        return True
    if isinstance(value, ByteArrayValue):
        return False
    if isinstance(value, OpaqueHandle):
        return value.kind in {
            "atomic",
            "lock",
            "mutex",
            "channel",
            "rwlock",
            "semaphore",
            "sync_queue",
            "future",
            "cancel_token",
        }
    if isinstance(value, OptionValue):
        return (not value.present) or _is_send_safe(value.value)
    if isinstance(value, ResultValue):
        return _is_send_safe(value.value)
    if isinstance(value, list):
        return all(_is_send_safe(item) for item in value)
    if isinstance(value, dict):
        return all(isinstance(key, str) and _is_send_safe(item) for key, item in value.items())
    if isinstance(value, RecordValue):
        return all(_is_send_safe(item) for item in value.fields.values())
    return False


def _is_ffi_abi_safe(value: object) -> bool:
    """Accept only deterministic host ABI-safe values across FFI boundary."""
    if value is None or isinstance(value, (str, int, float, bool, NilValue, BytesValue)):
        return True
    if isinstance(value, (ByteArrayValue, OpaqueHandle)):
        return False
    if isinstance(value, OptionValue):
        return (not value.present) or _is_ffi_abi_safe(value.value)
    if isinstance(value, ResultValue):
        return _is_ffi_abi_safe(value.value)
    if isinstance(value, list):
        return all(_is_ffi_abi_safe(item) for item in value)
    if isinstance(value, dict):
        return all(isinstance(key, str) and _is_ffi_abi_safe(item) for key, item in value.items())
    if isinstance(value, RecordValue):
        return all(_is_ffi_abi_safe(item) for item in value.fields.values())
    return False


def _expect_graph_map(value: object, fn_name: str) -> dict[str, list]:
    graph = expect_map(value, fn_name=fn_name)
    out: dict[str, list] = {}
    for key, neighbours in graph.items():
        if not isinstance(key, str):
            raise RuntimeSanskriptError(f"{fn_name} graph keys must be text nodes")
        out[key] = list(expect_list(neighbours, fn_name=fn_name))
    return out

# ---------------------------------------------------------------------------
# text
# ---------------------------------------------------------------------------


def _text_upper(args: list) -> str:
    return expect_text(args[0], fn_name="std.text.upper").upper()


def _text_lower(args: list) -> str:
    return expect_text(args[0], fn_name="std.text.lower").lower()


def _text_strip(args: list) -> str:
    return expect_text(args[0], fn_name="std.text.strip").strip()


def _text_split(args: list) -> list:
    text = expect_text(args[0], fn_name="std.text.split")
    sep = expect_text(args[1], fn_name="std.text.split")
    return text.split(sep)


def _text_join(args: list) -> str:
    sep = expect_text(args[0], fn_name="std.text.join")
    parts = expect_list(args[1], fn_name="std.text.join")
    return sep.join(expect_text(p, fn_name="std.text.join") for p in parts)


def _text_replace(args: list) -> str:
    text = expect_text(args[0], fn_name="std.text.replace")
    old = expect_text(args[1], fn_name="std.text.replace")
    new = expect_text(args[2], fn_name="std.text.replace")
    return text.replace(old, new)


def _text_len(args: list) -> int:
    return len(expect_text(args[0], fn_name="std.text.len"))


def _text_contains(args: list) -> bool:
    return expect_text(args[1], fn_name="std.text.contains") in expect_text(
        args[0], fn_name="std.text.contains"
    )


def _text_starts_with(args: list) -> bool:
    return expect_text(args[0], fn_name="std.text.starts_with").startswith(
        expect_text(args[1], fn_name="std.text.starts_with")
    )


def _text_ends_with(args: list) -> bool:
    return expect_text(args[0], fn_name="std.text.ends_with").endswith(
        expect_text(args[1], fn_name="std.text.ends_with")
    )


# ---------------------------------------------------------------------------
# unicode
# ---------------------------------------------------------------------------


def _unicode_normalize(args: list) -> str:
    text = expect_text(args[0], fn_name="std.unicode.normalize")
    form = expect_text(args[1], fn_name="std.unicode.normalize").upper()
    if form not in {"NFC", "NFD", "NFKC", "NFKD"}:
        raise RuntimeSanskriptError("std.unicode.normalize form must be NFC, NFD, NFKC, or NFKD")
    return unicodedata.normalize(form, text)


def _unicode_codepoint_at(args: list) -> int:
    text = expect_text(args[0], fn_name="std.unicode.codepoint_at")
    index = expect_int(args[1], fn_name="std.unicode.codepoint_at")
    if index < 0 or index >= len(text):
        raise RuntimeSanskriptError("std.unicode.codepoint_at index out of range")
    return ord(text[index])


def _unicode_grapheme_len(args: list) -> int:
    return text_grapheme_len(expect_text(args[0], fn_name="std.unicode.grapheme_len"))


def _unicode_is_ascii(args: list) -> bool:
    return expect_text(args[0], fn_name="std.unicode.is_ascii").isascii()


# ---------------------------------------------------------------------------
# bytes
# ---------------------------------------------------------------------------


def _bytes_from_text(args: list) -> BytesValue:
    text = expect_text(args[0], fn_name="std.bytes.from_text")
    try:
        return BytesValue(text.encode("utf-8"))
    except UnicodeEncodeError as exc:
        raise RuntimeSanskriptError(f"std.bytes.from_text encode failed: {exc}") from exc


def _bytes_to_text(args: list) -> str:
    data = expect_bytes(args[0], fn_name="std.bytes.to_text")
    try:
        return data.data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeSanskriptError(f"std.bytes.to_text decode failed: {exc}") from exc


def _bytes_len(args: list) -> int:
    return len(expect_bytes(args[0], fn_name="std.bytes.len").data)


def _bytes_concat(args: list) -> BytesValue:
    left = expect_bytes(args[0], fn_name="std.bytes.concat")
    right = expect_bytes(args[1], fn_name="std.bytes.concat")
    return BytesValue(left.data + right.data)


def _bytes_hex_encode(args: list) -> str:
    return expect_bytes(args[0], fn_name="std.bytes.hex_encode").data.hex()


def _bytes_hex_decode(args: list) -> BytesValue:
    text = expect_text(args[0], fn_name="std.bytes.hex_decode")
    try:
        return BytesValue(bytes.fromhex(text))
    except ValueError as exc:
        raise RuntimeSanskriptError(f"std.bytes.hex_decode invalid hex: {exc}") from exc


# ---------------------------------------------------------------------------
# math
# ---------------------------------------------------------------------------


def _math_abs(args: list) -> int | float:
    return abs(expect_number(args[0], fn_name="std.math.abs"))


def _math_sqrt(args: list) -> float:
    value = expect_number(args[0], fn_name="std.math.sqrt")
    if value < 0:
        raise RuntimeSanskriptError("std.math.sqrt expected non-negative input")
    return math.sqrt(value)


def _math_clamp(args: list) -> int | float:
    value = expect_number(args[0], fn_name="std.math.clamp")
    low = expect_number(args[1], fn_name="std.math.clamp")
    high = expect_number(args[2], fn_name="std.math.clamp")
    if low > high:
        raise RuntimeSanskriptError("std.math.clamp expected low <= high")
    return max(low, min(high, value))


def _math_min(args: list) -> int | float:
    return min(expect_number(args[0], fn_name="std.math.min"), expect_number(args[1], fn_name="std.math.min"))


def _math_max(args: list) -> int | float:
    return max(expect_number(args[0], fn_name="std.math.max"), expect_number(args[1], fn_name="std.math.max"))


def _math_floor(args: list) -> int:
    return math.floor(expect_number(args[0], fn_name="std.math.floor"))


def _math_ceil(args: list) -> int:
    return math.ceil(expect_number(args[0], fn_name="std.math.ceil"))


def _math_round(args: list) -> int:
    return round(expect_number(args[0], fn_name="std.math.round"))


def _math_pow(args: list) -> int | float:
    base = expect_number(args[0], fn_name="std.math.pow")
    exponent = expect_number(args[1], fn_name="std.math.pow")
    try:
        result = base ** exponent
    except OverflowError as exc:
        raise RuntimeSanskriptError(f"std.math.pow overflow: {exc}") from exc
    if isinstance(result, complex):
        raise RuntimeSanskriptError("std.math.pow produced a complex result; only real outputs are supported")
    if isinstance(result, float) and not math.isfinite(result):
        raise RuntimeSanskriptError("std.math.pow produced a non-finite result")
    return result


# ---------------------------------------------------------------------------
# statistics
# ---------------------------------------------------------------------------


def _stats_numbers(values: list, fn_name: str) -> list[float]:
    items = expect_list(values, fn_name=fn_name)
    if not items:
        raise RuntimeSanskriptError(f"{fn_name} requires a non-empty number list")
    out: list[float] = []
    for item in items:
        out.append(float(expect_number(item, fn_name=fn_name)))
    return out


def _stats_mean(args: list) -> float:
    nums = _stats_numbers(args[0], "std.stats.mean")
    return sum(nums) / len(nums)


def _stats_median(args: list) -> float:
    nums = sorted(_stats_numbers(args[0], "std.stats.median"))
    mid = len(nums) // 2
    if len(nums) % 2:
        return nums[mid]
    return (nums[mid - 1] + nums[mid]) / 2


def _stats_stdev(args: list) -> float:
    nums = _stats_numbers(args[0], "std.stats.stdev")
    if len(nums) < 2:
        raise RuntimeSanskriptError("std.stats.stdev requires at least two numbers")
    mean = sum(nums) / len(nums)
    var = sum((n - mean) ** 2 for n in nums) / (len(nums) - 1)
    return math.sqrt(var)


def _stats_min(args: list) -> float:
    return min(_stats_numbers(args[0], "std.stats.min"))


def _stats_max(args: list) -> float:
    return max(_stats_numbers(args[0], "std.stats.max"))


# ---------------------------------------------------------------------------
# random
# ---------------------------------------------------------------------------


def _random_float(args: list) -> float:
    return random.random()


def _random_randint(args: list) -> int:
    low = expect_int(args[0], fn_name="std.random.randint")
    high = expect_int(args[1], fn_name="std.random.randint")
    if low > high:
        raise RuntimeSanskriptError("std.random.randint expected low <= high")
    return random.randint(low, high)


def _random_choice(args: list) -> object:
    items = expect_list(args[0], fn_name="std.random.choice")
    if not items:
        raise RuntimeSanskriptError("std.random.choice requires a non-empty list")
    return random.choice(items)


def _random_seed(args: list) -> NilValue:
    random.seed(expect_int(args[0], fn_name="std.random.seed"))
    return NIL


# ---------------------------------------------------------------------------
# datetime / timezone
# ---------------------------------------------------------------------------


def _parse_iso(text: str, fn_name: str) -> datetime:
    try:
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        return datetime.fromisoformat(text)
    except ValueError as exc:
        raise RuntimeSanskriptError(f"{fn_name} invalid ISO datetime: {text!r}") from exc


def _datetime_now_iso(args: list) -> str:
    return datetime.now().astimezone().isoformat()


def _datetime_parse_iso(args: list) -> str:
    dt = _parse_iso(expect_text(args[0], fn_name="std.datetime.parse_iso"), "std.datetime.parse_iso")
    return dt.isoformat()


def _datetime_add_seconds(args: list) -> str:
    dt = _parse_iso(expect_text(args[0], fn_name="std.datetime.add_seconds"), "std.datetime.add_seconds")
    seconds = expect_number(args[1], fn_name="std.datetime.add_seconds")
    return (dt + timedelta(seconds=seconds)).isoformat()


def _datetime_diff_seconds(args: list) -> float:
    left = _parse_iso(expect_text(args[0], fn_name="std.datetime.diff_seconds"), "std.datetime.diff_seconds")
    right = _parse_iso(expect_text(args[1], fn_name="std.datetime.diff_seconds"), "std.datetime.diff_seconds")
    return (left - right).total_seconds()


def _timezone_utc_now(args: list) -> str:
    return datetime.now(timezone.utc).isoformat()


def _timezone_convert(args: list) -> str:
    dt = _parse_iso(expect_text(args[0], fn_name="std.timezone.convert"), "std.timezone.convert")
    zone_name = expect_text(args[1], fn_name="std.timezone.convert")
    try:
        zone = ZoneInfo(zone_name)
    except Exception as exc:
        raise RuntimeSanskriptError(f"std.timezone.convert unknown zone {zone_name!r}") from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(zone).isoformat()


# ---------------------------------------------------------------------------
# path / file / io / stream
# ---------------------------------------------------------------------------


def _path_join(args: list) -> str:
    parts = [expect_text(p, fn_name="std.path.join") for p in expect_list(args[0], fn_name="std.path.join")]
    if not parts:
        raise RuntimeSanskriptError("std.path.join requires at least one segment")
    return str(PurePath(parts[0]).joinpath(*parts[1:]))


def _path_basename(args: list) -> str:
    return PurePath(expect_text(args[0], fn_name="std.path.basename")).name


def _path_dirname(args: list) -> str:
    return str(PurePath(expect_text(args[0], fn_name="std.path.dirname")).parent)


def _path_exists(args: list) -> bool:
    return Path(expect_text(args[0], fn_name="std.path.exists")).exists()


def _path_is_file(args: list) -> bool:
    return Path(expect_text(args[0], fn_name="std.path.is_file")).is_file()


def _path_is_dir(args: list) -> bool:
    return Path(expect_text(args[0], fn_name="std.path.is_dir")).is_dir()


def _path_extension(args: list) -> str:
    return PurePath(expect_text(args[0], fn_name="std.path.extension")).suffix


def _path_normalize(args: list) -> str:
    return os.path.normpath(expect_text(args[0], fn_name="std.path.normalize"))


def _path_for_platform(args: list) -> str:
    platform = expect_text(args[0], fn_name="std.path.for_platform")
    parts = [expect_text(p, fn_name="std.path.for_platform") for p in expect_list(args[1], fn_name="std.path.for_platform")]
    try:
        return join_path_for_platform(platform, *parts)  # type: ignore[arg-type]
    except ValueError as exc:
        raise RuntimeSanskriptError(f"std.path.for_platform failed: {exc}") from exc


def _path_web_normalize(args: list) -> str:
    raw = expect_text(args[0], fn_name="std.path.web_normalize")
    try:
        return normalize_path_for_platform("web", raw)
    except ValueError as exc:
        raise RuntimeSanskriptError(f"std.path.web_normalize failed: {exc}") from exc


def _path_separator(args: list) -> str:
    platform = expect_text(args[0], fn_name="std.path.separator")
    if platform.lower() == "windows":
        return "\\"
    if platform.lower() in {"linux", "macos", "web"}:
        return "/"
    raise RuntimeSanskriptError(f"std.path.separator unknown platform {platform!r}")


def _file_read_text(args: list) -> str:
    path = expect_text(args[0], fn_name="std.file.read_text")
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.file.read_text failed: {exc}") from exc


def _file_write_text(args: list) -> bool:
    path = expect_text(args[0], fn_name="std.file.write_text")
    content = expect_text(args[1], fn_name="std.file.write_text")
    try:
        Path(path).write_text(content, encoding="utf-8")
        return True
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.file.write_text failed: {exc}") from exc


def _file_read_bytes(args: list) -> BytesValue:
    path = expect_text(args[0], fn_name="std.file.read_bytes")
    try:
        return BytesValue(Path(path).read_bytes())
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.file.read_bytes failed: {exc}") from exc


def _file_write_bytes(args: list) -> bool:
    path = expect_text(args[0], fn_name="std.file.write_bytes")
    data = expect_bytes(args[1], fn_name="std.file.write_bytes")
    try:
        Path(path).write_bytes(data.data)
        return True
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.file.write_bytes failed: {exc}") from exc


def _file_append_text(args: list) -> bool:
    path = expect_text(args[0], fn_name="std.file.append_text")
    content = expect_text(args[1], fn_name="std.file.append_text")
    try:
        with Path(path).open("a", encoding="utf-8") as handle:
            handle.write(content)
        return True
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.file.append_text failed: {exc}") from exc


def _file_remove(args: list) -> bool:
    path = Path(expect_text(args[0], fn_name="std.file.remove"))
    try:
        path.unlink()
        return True
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.file.remove failed: {exc}") from exc


def _file_mkdir(args: list) -> bool:
    path = Path(expect_text(args[0], fn_name="std.file.mkdir"))
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.file.mkdir failed: {exc}") from exc


def _io_read_lines(args: list) -> list:
    path = expect_text(args[0], fn_name="std.io.read_lines")
    try:
        return Path(path).read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.io.read_lines failed: {exc}") from exc


def _io_read_chunks(args: list) -> list:
    path = expect_text(args[0], fn_name="std.io.read_chunks")
    size = expect_int(args[1], fn_name="std.io.read_chunks")
    if size <= 0:
        raise RuntimeSanskriptError("std.io.read_chunks chunk size must be positive")
    chunks: list[BytesValue] = []
    try:
        with Path(path).open("rb") as handle:
            while True:
                block = handle.read(size)
                if not block:
                    break
                chunks.append(BytesValue(block))
        return chunks
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.io.read_chunks failed: {exc}") from exc


def _stream_read_all(args: list) -> str:
    return _file_read_text(args)


def _stream_write_all(args: list) -> bool:
    return _file_write_text(args)


def _io_stdout_write(args: list) -> bool:
    sys.stdout.write(expect_text(args[0], fn_name="std.io.stdout_write"))
    sys.stdout.flush()
    return True


def _io_stderr_write(args: list) -> bool:
    sys.stderr.write(expect_text(args[0], fn_name="std.io.stderr_write"))
    sys.stderr.flush()
    return True


def _io_stdin_read_all(args: list) -> str:
    return sys.stdin.read()


# ---------------------------------------------------------------------------
# terminal / cli / env
# ---------------------------------------------------------------------------


def _terminal_color(args: list) -> str:
    text = expect_text(args[0], fn_name="std.terminal.color")
    color = expect_text(args[1], fn_name="std.terminal.color").lower()
    codes = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }
    if color not in codes:
        raise RuntimeSanskriptError("std.terminal.color unknown color name")
    return f"{codes[color]}{text}\033[0m"


def _terminal_reset(args: list) -> str:
    return "\033[0m"


def _terminal_bold(args: list) -> str:
    return f"\033[1m{expect_text(args[0], fn_name='std.terminal.bold')}\033[0m"


def _terminal_cursor_up(args: list) -> str:
    count = expect_int(args[0], fn_name="std.terminal.cursor_up")
    return f"\033[{count}A"


def _terminal_cursor_down(args: list) -> str:
    count = expect_int(args[0], fn_name="std.terminal.cursor_down")
    return f"\033[{count}B"


def _cli_args(args: list) -> list:
    return list(sys.argv[1:])


def _cli_program_name(args: list) -> str:
    return sys.argv[0] if sys.argv else "sanskript"


def _cli_parse_flags(args: list) -> dict:
    tokens = [expect_text(t, fn_name="std.cli.parse_flags") for t in expect_list(args[0], fn_name="std.cli.parse_flags")]
    flags: dict[str, str | bool] = {}
    positionals: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.startswith("--"):
            key = token[2:]
            if index + 1 < len(tokens) and not tokens[index + 1].startswith("-"):
                flags[key] = tokens[index + 1]
                index += 2
            else:
                flags[key] = True
                index += 1
        elif token.startswith("-") and len(token) > 1:
            flags[token[1:]] = True
            index += 1
        else:
            positionals.append(token)
            index += 1
    return {"flags": flags, "positionals": positionals}


def _env_get(args: list) -> object:
    key = expect_text(args[0], fn_name="std.env.get")
    return os.environ.get(key, NIL)


def _env_has(args: list) -> bool:
    return expect_text(args[0], fn_name="std.env.has") in os.environ


def _env_keys(args: list) -> list:
    return sorted(os.environ.keys())


# ---------------------------------------------------------------------------
# process / pipe / signal
# ---------------------------------------------------------------------------


def _process_run(args: list) -> dict:
    cmd = [expect_text(part, fn_name="std.process.run") for part in expect_list(args[0], fn_name="std.process.run")]
    if not cmd:
        raise RuntimeSanskriptError("std.process.run requires a non-empty command list")
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.process.run failed: {exc}") from exc
    return {
        "exit": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def _process_run_for_platform(args: list) -> dict:
    platform = expect_text(args[0], fn_name="std.process.run_for_platform").lower()
    cmd = [expect_text(part, fn_name="std.process.run_for_platform") for part in expect_list(args[1], fn_name="std.process.run_for_platform")]
    host = host_platform_family()
    if platform != host:
        raise RuntimeSanskriptError(
            f"std.process.run_for_platform host is {host!r}, cannot run for {platform!r}"
        )
    if not cmd:
        raise RuntimeSanskriptError("std.process.run_for_platform requires a non-empty command list")
    return _process_run([cmd])


def _process_web_worker_new(args: list) -> OpaqueHandle:
    handle_id = _next_handle_id()
    _WEB_WORKER_QUEUES[handle_id] = web_worker_bridge_new(handle_id)
    return OpaqueHandle(kind="web.worker", handle_id=handle_id)


def _process_web_post_message(args: list) -> bool:
    worker = args[0]
    if not isinstance(worker, OpaqueHandle) or worker.kind != "web.worker":
        raise RuntimeSanskriptError("std.process.web_post_message requires web.worker handle")
    payload = expect_text(args[1], fn_name="std.process.web_post_message")
    bridge = _WEB_WORKER_QUEUES.get(worker.handle_id)
    if bridge is None:
        raise RuntimeSanskriptError("std.process.web_post_message unknown worker handle")
    return web_worker_post_message(bridge, payload)


def _process_web_recv(args: list) -> object:
    worker = args[0]
    if not isinstance(worker, OpaqueHandle) or worker.kind != "web.worker":
        raise RuntimeSanskriptError("std.process.web_recv requires web.worker handle")
    bridge = _WEB_WORKER_QUEUES.get(worker.handle_id)
    if bridge is None:
        raise RuntimeSanskriptError("std.process.web_recv unknown worker handle")
    message = web_worker_recv(bridge)
    return NIL if message is None else message


def _pipe_run(args: list) -> dict:
    return _process_run(args)


def _signal_names(args: list) -> list:
    return sorted(name for name in dir(signal) if name.startswith("SIG") and name.isupper())


def _signal_send(args: list) -> bool:
    name = expect_text(args[0], fn_name="std.signal.send")
    pid = expect_int(args[1], fn_name="std.signal.send")
    sig = getattr(signal, name, None)
    if sig is None:
        raise RuntimeSanskriptError(f"std.signal.send unknown signal {name!r}")
    try:
        os.kill(pid, sig)
        return True
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.signal.send failed: {exc}") from exc


# ---------------------------------------------------------------------------
# logging / config
# ---------------------------------------------------------------------------

_LOG = logging.getLogger("sanskript.stdlib")


def _log_info(args: list) -> bool:
    _LOG.info("%s", expect_text(args[0], fn_name="std.log.info"))
    return True


def _log_warn(args: list) -> bool:
    _LOG.warning("%s", expect_text(args[0], fn_name="std.log.warn"))
    return True


def _log_error(args: list) -> bool:
    _LOG.error("%s", expect_text(args[0], fn_name="std.log.error"))
    return True


def _log_set_level(args: list) -> bool:
    level = expect_text(args[0], fn_name="std.log.set_level").upper()
    mapping = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARN": logging.WARNING, "ERROR": logging.ERROR}
    if level not in mapping:
        raise RuntimeSanskriptError("std.log.set_level expects DEBUG, INFO, WARN, or ERROR")
    _LOG.setLevel(mapping[level])
    if not _LOG.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        _LOG.addHandler(handler)
    return True


def _config_load_json(args: list) -> object:
    return parse_json_text(expect_text(args[0], fn_name="std.config.load_json"), fn_name="std.config.load_json")


def _config_load_toml(args: list) -> object:
    text = expect_text(args[0], fn_name="std.config.load_toml")
    try:
        import tomllib
    except ModuleNotFoundError:
        return _parse_toml_simple(text)
    payload = tomllib.loads(text)
    return from_json(payload)


def _config_load_yaml(args: list) -> object:
    return _parse_yaml(expect_text(args[0], fn_name="std.config.load_yaml"))


# ---------------------------------------------------------------------------
# json / csv / toml / yaml / xml
# ---------------------------------------------------------------------------


def _json_parse(args: list) -> object:
    return parse_json_text(expect_text(args[0], fn_name="std.json.parse"), fn_name="std.json.parse")


def _json_stringify(args: list) -> str:
    return stringify_json(args[0])


def _csv_parse(args: list) -> list:
    text = expect_text(args[0], fn_name="std.csv.parse")
    stream = io.StringIO(text)
    reader = csv.DictReader(stream)
    if not reader.fieldnames:
        raise RuntimeSanskriptError("std.csv.parse requires a CSV header row")
    rows: list = []
    for row in reader:
        cleaned: dict[str, str] = {}
        for key, val in row.items():
            if key is None:
                raise RuntimeSanskriptError("std.csv.parse encountered missing column name")
            cleaned[key] = "" if val is None else val
        rows.append(cleaned)
    return rows


def _csv_stringify(args: list) -> str:
    rows = expect_list(args[0], fn_name="std.csv.stringify")
    if not rows:
        raise RuntimeSanskriptError("std.csv.stringify requires at least one row")
    first = rows[0]
    if not isinstance(first, dict) or not first:
        raise RuntimeSanskriptError("std.csv.stringify first row must be non-empty map")
    headers = list(first.keys())
    for key in headers:
        if not isinstance(key, str):
            raise RuntimeSanskriptError("std.csv.stringify headers must be text")
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=headers, lineterminator="\n")
    writer.writeheader()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise RuntimeSanskriptError(f"std.csv.stringify row {index} must be map")
        if set(row.keys()) != set(headers):
            raise RuntimeSanskriptError("std.csv.stringify rows must share identical headers")
        writer.writerow({key: str(row[key]) for key in headers})
    return buffer.getvalue()


def _toml_parse(args: list) -> object:
    return _config_load_toml(args)


def _toml_stringify(args: list) -> str:
    return _stringify_toml(args[0])


def _yaml_parse(args: list) -> object:
    return _parse_yaml(expect_text(args[0], fn_name="std.yaml.parse"))


def _yaml_stringify(args: list) -> str:
    return _stringify_yaml(args[0])


def _xml_parse(args: list) -> dict:
    text = expect_text(args[0], fn_name="std.xml.parse")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        raise RuntimeSanskriptError(f"std.xml.parse invalid XML: {exc}") from exc
    return _xml_element_to_map(root)


def _xml_stringify(args: list) -> str:
    payload = expect_map(args[0], fn_name="std.xml.stringify")
    tag = expect_text(payload.get("tag", ""), fn_name="std.xml.stringify")
    if not tag:
        raise RuntimeSanskriptError("std.xml.stringify map requires text tag")
    element = _xml_map_to_element(tag, payload)
    return ET.tostring(element, encoding="unicode")


# ---------------------------------------------------------------------------
# binary / compression / hash / crypto / secure / encoding
# ---------------------------------------------------------------------------


def _binary_pack(args: list) -> BytesValue:
    fmt = expect_text(args[0], fn_name="std.binary.pack")
    values = expect_list(args[1], fn_name="std.binary.pack")
    try:
        packed = struct.pack(fmt, *[expect_number(v, fn_name="std.binary.pack") for v in values])
    except struct.error as exc:
        raise RuntimeSanskriptError(f"std.binary.pack failed: {exc}") from exc
    return BytesValue(packed)


def _binary_unpack(args: list) -> list:
    fmt = expect_text(args[0], fn_name="std.binary.unpack")
    data = expect_bytes(args[1], fn_name="std.binary.unpack")
    try:
        return list(struct.unpack(fmt, data.data))
    except struct.error as exc:
        raise RuntimeSanskriptError(f"std.binary.unpack failed: {exc}") from exc


def _compress_gzip(args: list) -> BytesValue:
    data = expect_bytes(args[0], fn_name="std.compress.gzip")
    return BytesValue(gzip.compress(data.data))


def _compress_gunzip(args: list) -> BytesValue:
    data = expect_bytes(args[0], fn_name="std.compress.gunzip")
    try:
        return BytesValue(gzip.decompress(data.data))
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.compress.gunzip failed: {exc}") from exc


def _compress_zlib(args: list) -> BytesValue:
    data = expect_bytes(args[0], fn_name="std.compress.zlib")
    return BytesValue(zlib.compress(data.data))


def _compress_unzlib(args: list) -> BytesValue:
    data = expect_bytes(args[0], fn_name="std.compress.unzlib")
    try:
        return BytesValue(zlib.decompress(data.data))
    except zlib.error as exc:
        raise RuntimeSanskriptError(f"std.compress.unzlib failed: {exc}") from exc


def _hash_md5(args: list) -> str:
    text = expect_text(args[0], fn_name="std.hash.md5")
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def _hash_sha256(args: list) -> str:
    text = expect_text(args[0], fn_name="std.hash.sha256")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _crypto_sha256(args: list) -> str:
    return _hash_sha256(args)


def _crypto_hmac_sha256(args: list) -> str:
    key = expect_text(args[0], fn_name="std.crypto.hmac_sha256")
    message = expect_text(args[1], fn_name="std.crypto.hmac_sha256")
    return hmac.new(key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()


def _secure_random_bytes(args: list) -> BytesValue:
    count = expect_int(args[0], fn_name="std.secure.random_bytes")
    if count < 0:
        raise RuntimeSanskriptError("std.secure.random_bytes count must be non-negative")
    return BytesValue(secrets.token_bytes(count))


def _secure_token_hex(args: list) -> str:
    nbytes = expect_int(args[0], fn_name="std.secure.token_hex")
    if nbytes < 0:
        raise RuntimeSanskriptError("std.secure.token_hex nbytes must be non-negative")
    return secrets.token_hex(nbytes)


def _encoding_base64_encode(args: list) -> str:
    data = expect_bytes(args[0], fn_name="std.encoding.base64_encode")
    return base64.b64encode(data.data).decode("ascii")


def _encoding_base64_decode(args: list) -> BytesValue:
    text = expect_text(args[0], fn_name="std.encoding.base64_decode")
    try:
        return BytesValue(base64.b64decode(text.encode("ascii"), validate=True))
    except (ValueError, binascii.Error) as exc:
        raise RuntimeSanskriptError(f"std.encoding.base64_decode invalid data: {exc}") from exc


def _encoding_url_encode(args: list) -> str:
    return urllib.parse.quote(expect_text(args[0], fn_name="std.encoding.url_encode"), safe="")


def _encoding_url_decode(args: list) -> str:
    return urllib.parse.unquote(expect_text(args[0], fn_name="std.encoding.url_decode"))


# ---------------------------------------------------------------------------
# regex / template / serialize / test / bench
# ---------------------------------------------------------------------------


def _regex_match(args: list) -> bool:
    pattern = expect_text(args[0], fn_name="std.regex.match")
    text = expect_text(args[1], fn_name="std.regex.match")
    try:
        return re.fullmatch(pattern, text) is not None
    except re.error as exc:
        raise RuntimeSanskriptError(f"std.regex.match invalid pattern: {exc}") from exc


def _regex_search(args: list) -> str | object:
    pattern = expect_text(args[0], fn_name="std.regex.search")
    text = expect_text(args[1], fn_name="std.regex.search")
    try:
        found = re.search(pattern, text)
    except re.error as exc:
        raise RuntimeSanskriptError(f"std.regex.search invalid pattern: {exc}") from exc
    return found.group(0) if found else NIL


def _regex_replace(args: list) -> str:
    pattern = expect_text(args[0], fn_name="std.regex.replace")
    repl = expect_text(args[1], fn_name="std.regex.replace")
    text = expect_text(args[2], fn_name="std.regex.replace")
    try:
        return re.sub(pattern, repl, text)
    except re.error as exc:
        raise RuntimeSanskriptError(f"std.regex.replace invalid pattern: {exc}") from exc


def _regex_split(args: list) -> list:
    pattern = expect_text(args[0], fn_name="std.regex.split")
    text = expect_text(args[1], fn_name="std.regex.split")
    try:
        return re.split(pattern, text)
    except re.error as exc:
        raise RuntimeSanskriptError(f"std.regex.split invalid pattern: {exc}") from exc


def _template_render(args: list) -> str:
    template = expect_text(args[0], fn_name="std.template.render")
    ctx = expect_map(args[1], fn_name="std.template.render")

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in ctx:
            raise RuntimeSanskriptError(f"std.template.render missing key {key!r}")
        return str(ctx[key])

    return re.sub(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}", repl, template)


def _serialize(args: list) -> str:
    fmt = expect_text(args[0], fn_name="std.serialize").lower()
    value = args[1]
    if fmt == "json":
        return stringify_json(value)
    if fmt == "yaml":
        return _stringify_yaml(value)
    if fmt == "toml":
        return _stringify_toml(value)
    raise RuntimeSanskriptError("std.serialize format must be json, yaml, or toml")


def _deserialize(args: list) -> object:
    fmt = expect_text(args[0], fn_name="std.deserialize").lower()
    text = expect_text(args[1], fn_name="std.deserialize")
    if fmt == "json":
        return parse_json_text(text, fn_name="std.deserialize")
    if fmt == "yaml":
        return _parse_yaml(text)
    if fmt == "toml":
        return _config_load_toml([text])
    raise RuntimeSanskriptError("std.deserialize format must be json, yaml, or toml")


def _test_assert_eq(args: list) -> bool:
    left, right = args[0], args[1]
    if left != right:
        raise RuntimeSanskriptError(f"std.test.assert_eq failed: {left!r} != {right!r}")
    return True


def _test_assert_true(args: list) -> bool:
    if not expect_bool(args[0], fn_name="std.test.assert_true"):
        raise RuntimeSanskriptError("std.test.assert_true failed")
    return True


def _test_assert_false(args: list) -> bool:
    if expect_bool(args[0], fn_name="std.test.assert_false"):
        raise RuntimeSanskriptError("std.test.assert_false failed")
    return True


def _bench_now_ms(args: list) -> float:
    return time.perf_counter() * 1000.0


def _bench_elapsed_ms(args: list) -> float:
    start = expect_number(args[0], fn_name="std.bench.elapsed_ms")
    return time.perf_counter() * 1000.0 - start


# ---------------------------------------------------------------------------
# algorithms / data structures
# ---------------------------------------------------------------------------


def _alg_sort(args: list) -> list:
    values = list(expect_list(args[0], fn_name="std.alg.sort"))
    direction = expect_text(args[1], fn_name="std.alg.sort").lower()
    if direction not in {"asc", "desc"}:
        raise RuntimeSanskriptError("std.alg.sort order must be 'asc' or 'desc'")
    try:
        values.sort(reverse=(direction == "desc"))
    except TypeError as exc:
        raise RuntimeSanskriptError(f"std.alg.sort failed for mixed/unordered values: {exc}") from exc
    return values


def _alg_stable_sort_by(args: list) -> list:
    rows = list(expect_list(args[0], fn_name="std.alg.stable_sort_by"))
    field = expect_text(args[1], fn_name="std.alg.stable_sort_by")
    direction = expect_text(args[2], fn_name="std.alg.stable_sort_by").lower()
    if direction not in {"asc", "desc"}:
        raise RuntimeSanskriptError("std.alg.stable_sort_by order must be 'asc' or 'desc'")
    for row in rows:
        item = expect_map(row, fn_name="std.alg.stable_sort_by")
        if field not in item:
            raise RuntimeSanskriptError(f"std.alg.stable_sort_by missing field {field!r}")
    try:
        rows.sort(key=lambda item: expect_map(item, fn_name="std.alg.stable_sort_by")[field], reverse=(direction == "desc"))
    except TypeError as exc:
        raise RuntimeSanskriptError(f"std.alg.stable_sort_by failed: {exc}") from exc
    return rows


def _alg_binary_search(args: list) -> int:
    values = list(expect_list(args[0], fn_name="std.alg.binary_search"))
    target = args[1]
    try:
        if any(values[i] > values[i + 1] for i in range(len(values) - 1)):
            raise RuntimeSanskriptError("std.alg.binary_search requires sorted ascending input")
        index = bisect_left(values, target)
    except TypeError as exc:
        raise RuntimeSanskriptError(f"std.alg.binary_search failed: {exc}") from exc
    if index != len(values) and values[index] == target:
        return index
    return -1


def _alg_graph_bfs(args: list) -> list:
    graph = _expect_graph_map(args[0], "std.alg.graph.bfs")
    start = expect_text(args[1], fn_name="std.alg.graph.bfs")
    if start not in graph:
        raise RuntimeSanskriptError("std.alg.graph.bfs start node not found")
    order: list[str] = []
    seen = {start}
    queue: deque[str] = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph.get(node, []):
            nxt_name = expect_text(nxt, fn_name="std.alg.graph.bfs")
            if nxt_name not in seen:
                seen.add(nxt_name)
                queue.append(nxt_name)
    return order


def _alg_graph_dfs(args: list) -> list:
    graph = _expect_graph_map(args[0], "std.alg.graph.dfs")
    start = expect_text(args[1], fn_name="std.alg.graph.dfs")
    if start not in graph:
        raise RuntimeSanskriptError("std.alg.graph.dfs start node not found")
    order: list[str] = []
    seen: set[str] = set()
    stack: list[str] = [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        neighbours = [expect_text(item, fn_name="std.alg.graph.dfs") for item in graph.get(node, [])]
        for nxt in reversed(neighbours):
            if nxt not in seen:
                stack.append(nxt)
    return order


def _alg_graph_dijkstra(args: list) -> dict:
    graph = expect_map(args[0], fn_name="std.alg.graph.dijkstra")
    start = expect_text(args[1], fn_name="std.alg.graph.dijkstra")
    if start not in graph:
        raise RuntimeSanskriptError("std.alg.graph.dijkstra start node not found")
    distances: dict[str, float] = {str(node): float("inf") for node in graph.keys()}
    distances[start] = 0.0
    heap: list[tuple[float, str]] = [(0.0, start)]
    while heap:
        dist, node = heapq.heappop(heap)
        if dist > distances[node]:
            continue
        # Nodes discovered from edges might not have explicit adjacency entries.
        # Treat them as leaf nodes instead of crashing with KeyError.
        edges = expect_list(graph.get(node, []), fn_name="std.alg.graph.dijkstra")
        for edge in edges:
            pair = expect_list(edge, fn_name="std.alg.graph.dijkstra")
            if len(pair) != 2:
                raise RuntimeSanskriptError("std.alg.graph.dijkstra edges must be [neighbor, weight]")
            nxt = expect_text(pair[0], fn_name="std.alg.graph.dijkstra")
            weight = float(expect_number(pair[1], fn_name="std.alg.graph.dijkstra"))
            if weight < 0:
                raise RuntimeSanskriptError("std.alg.graph.dijkstra does not allow negative weights")
            nd = dist + weight
            if nd < distances.get(nxt, float("inf")):
                distances[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return {key: (NIL if val == float("inf") else val) for key, val in distances.items()}


def _alg_tree_traverse(args: list) -> list:
    node = expect_map(args[0], fn_name="std.alg.tree.traverse")
    order = expect_text(args[1], fn_name="std.alg.tree.traverse").lower()
    if order not in {"pre", "in", "post"}:
        raise RuntimeSanskriptError("std.alg.tree.traverse order must be pre, in, or post")
    out: list = []

    def walk(current: object) -> None:
        if current is None or isinstance(current, NilValue):
            return
        branch = expect_map(current, fn_name="std.alg.tree.traverse")
        val = branch.get("value", NIL)
        left = branch.get("left", NIL)
        right = branch.get("right", NIL)
        if order == "pre":
            out.append(val)
        walk(left)
        if order == "in":
            out.append(val)
        walk(right)
        if order == "post":
            out.append(val)

    walk(node)
    return out


def _alg_heap_push(args: list) -> list:
    heap_values = list(expect_list(args[0], fn_name="std.alg.heap.push"))
    value = args[1]
    heapq.heapify(heap_values)
    heapq.heappush(heap_values, value)
    return heap_values


def _alg_heap_pop(args: list) -> dict:
    heap_values = list(expect_list(args[0], fn_name="std.alg.heap.pop"))
    if not heap_values:
        raise RuntimeSanskriptError("std.alg.heap.pop requires non-empty heap")
    heapq.heapify(heap_values)
    popped = heapq.heappop(heap_values)
    return {"value": popped, "heap": heap_values}


def _alg_priority_schedule(args: list) -> list:
    tasks = list(expect_list(args[0], fn_name="std.alg.priority.schedule"))
    normalized: list[dict] = []
    for item in tasks:
        task = expect_map(item, fn_name="std.alg.priority.schedule")
        for key in ("task", "priority", "arrival"):
            if key not in task:
                raise RuntimeSanskriptError(f"std.alg.priority.schedule missing {key!r}")
        if float(expect_number(task["arrival"], fn_name="std.alg.priority.schedule")) < 0:
            raise RuntimeSanskriptError("std.alg.priority.schedule arrival must be non-negative")
        if float(expect_number(task["priority"], fn_name="std.alg.priority.schedule")) < 0:
            raise RuntimeSanskriptError("std.alg.priority.schedule priority must be non-negative")
        normalized.append(task)
    normalized.sort(key=lambda t: (expect_number(t["arrival"], fn_name="std.alg.priority.schedule"), expect_number(t["priority"], fn_name="std.alg.priority.schedule"), str(t["task"])))
    ready: list[tuple[float, float, str, dict]] = []
    out: list = []
    i = 0
    tick = 0.0
    while i < len(normalized) or ready:
        while i < len(normalized) and float(expect_number(normalized[i]["arrival"], fn_name="std.alg.priority.schedule")) <= tick:
            cur = normalized[i]
            heapq.heappush(
                ready,
                (
                    float(expect_number(cur["priority"], fn_name="std.alg.priority.schedule")),
                    float(expect_number(cur["arrival"], fn_name="std.alg.priority.schedule")),
                    str(cur["task"]),
                    cur,
                ),
            )
            i += 1
        if not ready:
            tick = float(expect_number(normalized[i]["arrival"], fn_name="std.alg.priority.schedule"))
            continue
        _, _, _, cur = heapq.heappop(ready)
        out.append(cur["task"])
        tick += 1.0
    return out


def _alg_dp_lcs_length(args: list) -> int:
    left = expect_text(args[0], fn_name="std.alg.dp.lcs_length")
    right = expect_text(args[1], fn_name="std.alg.dp.lcs_length")
    dp = [[0] * (len(right) + 1) for _ in range(len(left) + 1)]
    for i in range(1, len(left) + 1):
        for j in range(1, len(right) + 1):
            if left[i - 1] == right[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]


def _alg_dp_knapsack(args: list) -> int:
    capacity = expect_int(args[0], fn_name="std.alg.dp.knapsack_01")
    entries = expect_list(args[1], fn_name="std.alg.dp.knapsack_01")
    if capacity < 0:
        raise RuntimeSanskriptError("std.alg.dp.knapsack_01 capacity must be non-negative")
    dp = [0] * (capacity + 1)
    for item in entries:
        pair = expect_list(item, fn_name="std.alg.dp.knapsack_01")
        if len(pair) != 2:
            raise RuntimeSanskriptError("std.alg.dp.knapsack_01 items must be [weight, value]")
        weight = expect_int(pair[0], fn_name="std.alg.dp.knapsack_01")
        value = expect_int(pair[1], fn_name="std.alg.dp.knapsack_01")
        if weight <= 0:
            raise RuntimeSanskriptError("std.alg.dp.knapsack_01 weight must be positive")
        for cap in range(capacity, weight - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - weight] + value)
    return dp[capacity]


def _alg_string_kmp_search(args: list) -> int:
    text = expect_text(args[0], fn_name="std.alg.string.kmp_search")
    pattern = expect_text(args[1], fn_name="std.alg.string.kmp_search")
    if pattern == "":
        return 0
    lps = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j
    j = 0
    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            j = lps[j - 1]
        if ch == pattern[j]:
            j += 1
            if j == len(pattern):
                return i - len(pattern) + 1
    return -1


def _alg_trie_build(args: list) -> dict:
    words = expect_list(args[0], fn_name="std.alg.trie.build")
    root: dict[str, object] = {"children": {}, "terminal": False}
    for raw in words:
        word = expect_text(raw, fn_name="std.alg.trie.build")
        node = root
        for ch in word:
            children = expect_map(node["children"], fn_name="std.alg.trie.build")
            if ch not in children:
                children[ch] = {"children": {}, "terminal": False}
            node = expect_map(children[ch], fn_name="std.alg.trie.build")
        node["terminal"] = True
    return root


def _alg_trie_contains(args: list) -> bool:
    trie = expect_map(args[0], fn_name="std.alg.trie.contains")
    word = expect_text(args[1], fn_name="std.alg.trie.contains")
    node = trie
    for ch in word:
        children = expect_map(node.get("children", {}), fn_name="std.alg.trie.contains")
        if ch not in children:
            return False
        node = expect_map(children[ch], fn_name="std.alg.trie.contains")
    return bool(node.get("terminal", False))


def _alg_suffix_array(args: list) -> list:
    text = expect_text(args[0], fn_name="std.alg.suffix.array")
    suffixes = sorted((text[i:], i) for i in range(len(text)))
    return [idx for _, idx in suffixes]


def _alg_interval_query(args: list) -> list:
    intervals = expect_list(args[0], fn_name="std.alg.interval.query")
    point = expect_number(args[1], fn_name="std.alg.interval.query")
    tree = _alg_interval_tree_build([intervals])
    return _alg_interval_tree_query([tree, point])


def _alg_interval_tree_build(args: list) -> dict:
    intervals = expect_list(args[0], fn_name="std.alg.interval.tree_build")
    parsed: list[tuple[float, float]] = []
    for item in intervals:
        pair = expect_list(item, fn_name="std.alg.interval.tree_build")
        if len(pair) != 2:
            raise RuntimeSanskriptError("std.alg.interval.tree_build intervals must be [start, end]")
        start = float(expect_number(pair[0], fn_name="std.alg.interval.tree_build"))
        end = float(expect_number(pair[1], fn_name="std.alg.interval.tree_build"))
        if start > end:
            raise RuntimeSanskriptError("std.alg.interval.tree_build requires start <= end")
        parsed.append((start, end))

    def build(items: list[tuple[float, float]]) -> object:
        if not items:
            return NIL
        center = sorted((start + end) * 0.5 for start, end in items)[len(items) // 2]
        left: list[tuple[float, float]] = []
        right: list[tuple[float, float]] = []
        crossing: list[list[float]] = []
        for start, end in items:
            if end < center:
                left.append((start, end))
            elif start > center:
                right.append((start, end))
            else:
                crossing.append([start, end])
        crossing.sort(key=lambda pair: (pair[0], pair[1]))
        return {
            "center": center,
            "intervals": crossing,
            "left": build(left),
            "right": build(right),
        }

    return {"root": build(parsed)}


def _alg_interval_tree_query(args: list) -> list:
    tree = expect_map(args[0], fn_name="std.alg.interval.tree_query")
    point = float(expect_number(args[1], fn_name="std.alg.interval.tree_query"))
    hits: list[list[float]] = []

    def walk(node: object) -> None:
        if isinstance(node, NilValue):
            return
        branch = expect_map(node, fn_name="std.alg.interval.tree_query")
        center = float(expect_number(branch.get("center", 0), fn_name="std.alg.interval.tree_query"))
        intervals = expect_list(branch.get("intervals", []), fn_name="std.alg.interval.tree_query")
        for raw in intervals:
            pair = expect_list(raw, fn_name="std.alg.interval.tree_query")
            if len(pair) != 2:
                raise RuntimeSanskriptError("std.alg.interval.tree_query interval nodes must be [start, end]")
            start = float(expect_number(pair[0], fn_name="std.alg.interval.tree_query"))
            end = float(expect_number(pair[1], fn_name="std.alg.interval.tree_query"))
            if start <= point <= end:
                hits.append([start, end])
        if point < center:
            walk(branch.get("left", NIL))
        elif point > center:
            walk(branch.get("right", NIL))
        else:
            walk(branch.get("left", NIL))
            walk(branch.get("right", NIL))

    walk(tree.get("root", NIL))
    hits.sort(key=lambda pair: (pair[0], pair[1]))
    return hits


def _alg_union_find_run(args: list) -> dict:
    size = expect_int(args[0], fn_name="std.alg.union_find.run")
    unions = expect_list(args[1], fn_name="std.alg.union_find.run")
    queries = expect_list(args[2], fn_name="std.alg.union_find.run")
    if size <= 0:
        raise RuntimeSanskriptError("std.alg.union_find.run size must be positive")
    parent = list(range(size))
    rank = [0] * size

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank[ra] += 1

    for pair in unions:
        edge = expect_list(pair, fn_name="std.alg.union_find.run")
        if len(edge) != 2:
            raise RuntimeSanskriptError("std.alg.union_find.run unions must be [a, b]")
        a = expect_int(edge[0], fn_name="std.alg.union_find.run")
        b = expect_int(edge[1], fn_name="std.alg.union_find.run")
        if a < 0 or b < 0 or a >= size or b >= size:
            raise RuntimeSanskriptError("std.alg.union_find.run union index out of range")
        union(a, b)
    connected: list = []
    for pair in queries:
        edge = expect_list(pair, fn_name="std.alg.union_find.run")
        if len(edge) != 2:
            raise RuntimeSanskriptError("std.alg.union_find.run queries must be [a, b]")
        a = expect_int(edge[0], fn_name="std.alg.union_find.run")
        b = expect_int(edge[1], fn_name="std.alg.union_find.run")
        if a < 0 or b < 0 or a >= size or b >= size:
            raise RuntimeSanskriptError("std.alg.union_find.run query index out of range")
        connected.append(find(a) == find(b))
    return {"parent": parent, "connected": connected}


def _alg_bitset_new(args: list) -> dict:
    size = expect_int(args[0], fn_name="std.alg.bitset.new")
    if size < 0:
        raise RuntimeSanskriptError("std.alg.bitset.new size must be non-negative")
    return {"size": size, "bits": [False] * size}


def _alg_bitset_set(args: list) -> dict:
    bitset = expect_map(args[0], fn_name="std.alg.bitset.set")
    index = expect_int(args[1], fn_name="std.alg.bitset.set")
    value = expect_bool(args[2], fn_name="std.alg.bitset.set")
    bits = list(expect_list(bitset.get("bits", []), fn_name="std.alg.bitset.set"))
    if index < 0 or index >= len(bits):
        raise RuntimeSanskriptError("std.alg.bitset.set index out of range")
    bits[index] = value
    return {"size": bitset.get("size", len(bits)), "bits": bits}


def _alg_bitset_test(args: list) -> bool:
    bitset = expect_map(args[0], fn_name="std.alg.bitset.test")
    index = expect_int(args[1], fn_name="std.alg.bitset.test")
    bits = expect_list(bitset.get("bits", []), fn_name="std.alg.bitset.test")
    if index < 0 or index >= len(bits):
        raise RuntimeSanskriptError("std.alg.bitset.test index out of range")
    return expect_bool(bits[index], fn_name="std.alg.bitset.test")


def _alg_bloom_new(args: list) -> dict:
    size = expect_int(args[0], fn_name="std.alg.bloom.new")
    hashes = expect_int(args[1], fn_name="std.alg.bloom.new")
    if size <= 0 or hashes <= 0:
        raise RuntimeSanskriptError("std.alg.bloom.new expects positive size and hash count")
    return {"size": size, "hashes": hashes, "bits": [False] * size}


def _alg_bloom_add(args: list) -> dict:
    bloom = expect_map(args[0], fn_name="std.alg.bloom.add")
    item = expect_text(args[1], fn_name="std.alg.bloom.add")
    size = expect_int(bloom.get("size", 0), fn_name="std.alg.bloom.add")
    hashes = expect_int(bloom.get("hashes", 0), fn_name="std.alg.bloom.add")
    bits = list(expect_list(bloom.get("bits", []), fn_name="std.alg.bloom.add"))
    if size <= 0 or hashes <= 0:
        raise RuntimeSanskriptError("std.alg.bloom.add expects bloom with positive size and hash count")
    if len(bits) != size:
        raise RuntimeSanskriptError("std.alg.bloom.add bloom bits length must match size")
    for i in range(hashes):
        digest = hashlib.sha256(f"{i}:{item}".encode("utf-8")).digest()
        idx = int.from_bytes(digest[:8], "big") % size
        bits[idx] = True
    return {"size": size, "hashes": hashes, "bits": bits}


def _alg_bloom_maybe_contains(args: list) -> bool:
    bloom = expect_map(args[0], fn_name="std.alg.bloom.maybe_contains")
    item = expect_text(args[1], fn_name="std.alg.bloom.maybe_contains")
    size = expect_int(bloom.get("size", 0), fn_name="std.alg.bloom.maybe_contains")
    hashes = expect_int(bloom.get("hashes", 0), fn_name="std.alg.bloom.maybe_contains")
    bits = expect_list(bloom.get("bits", []), fn_name="std.alg.bloom.maybe_contains")
    if size <= 0 or hashes <= 0:
        raise RuntimeSanskriptError("std.alg.bloom.maybe_contains expects bloom with positive size and hash count")
    if len(bits) != size:
        raise RuntimeSanskriptError("std.alg.bloom.maybe_contains bloom bits length must match size")
    for i in range(hashes):
        digest = hashlib.sha256(f"{i}:{item}".encode("utf-8")).digest()
        idx = int.from_bytes(digest[:8], "big") % size
        if not expect_bool(bits[idx], fn_name="std.alg.bloom.maybe_contains"):
            return False
    return True


def _alg_matrix_mul(args: list) -> list:
    left = expect_list(args[0], fn_name="std.alg.matrix.mul")
    right = expect_list(args[1], fn_name="std.alg.matrix.mul")
    a = [list(expect_list(row, fn_name="std.alg.matrix.mul")) for row in left]
    b = [list(expect_list(row, fn_name="std.alg.matrix.mul")) for row in right]
    if not a or not b:
        raise RuntimeSanskriptError("std.alg.matrix.mul expects non-empty matrices")
    cols_a = len(a[0])
    cols_b = len(b[0])
    if any(len(row) != cols_a for row in a) or any(len(row) != cols_b for row in b):
        raise RuntimeSanskriptError("std.alg.matrix.mul expects rectangular matrices")
    if cols_a != len(b):
        raise RuntimeSanskriptError("std.alg.matrix.mul dimension mismatch")
    out: list[list[float]] = []
    for row in a:
        out_row: list[float] = []
        for j in range(cols_b):
            acc = 0.0
            for k, val in enumerate(row):
                acc += float(expect_number(val, fn_name="std.alg.matrix.mul")) * float(expect_number(b[k][j], fn_name="std.alg.matrix.mul"))
            out_row.append(acc)
        out.append(out_row)
    return out


def _alg_vector_dot(args: list) -> float:
    left = expect_list(args[0], fn_name="std.alg.vector.dot")
    right = expect_list(args[1], fn_name="std.alg.vector.dot")
    if len(left) != len(right):
        raise RuntimeSanskriptError("std.alg.vector.dot requires equal-length vectors")
    return sum(
        float(expect_number(a, fn_name="std.alg.vector.dot")) * float(expect_number(b, fn_name="std.alg.vector.dot"))
        for a, b in zip(left, right)
    )


def _alg_vector_norm(args: list) -> float:
    vec = expect_list(args[0], fn_name="std.alg.vector.norm")
    return math.sqrt(sum(float(expect_number(item, fn_name="std.alg.vector.norm")) ** 2 for item in vec))


def _alg_numeric_integrate_trapezoid(args: list) -> float:
    points = expect_list(args[0], fn_name="std.alg.numeric.integrate_trapezoid")
    if len(points) < 2:
        raise RuntimeSanskriptError("std.alg.numeric.integrate_trapezoid requires at least two points")
    parsed = []
    for item in points:
        pair = expect_list(item, fn_name="std.alg.numeric.integrate_trapezoid")
        if len(pair) != 2:
            raise RuntimeSanskriptError("std.alg.numeric.integrate_trapezoid points must be [x, y]")
        parsed.append(
            (
                float(expect_number(pair[0], fn_name="std.alg.numeric.integrate_trapezoid")),
                float(expect_number(pair[1], fn_name="std.alg.numeric.integrate_trapezoid")),
            )
        )
    area = 0.0
    for i in range(len(parsed) - 1):
        x1, y1 = parsed[i]
        x2, y2 = parsed[i + 1]
        if x2 < x1:
            raise RuntimeSanskriptError("std.alg.numeric.integrate_trapezoid points must be x-sorted")
        area += (x2 - x1) * (y1 + y2) * 0.5
    return area


def _alg_opt_gradient_descent_step(args: list) -> float:
    x = float(expect_number(args[0], fn_name="std.alg.opt.gradient_descent_step"))
    grad = float(expect_number(args[1], fn_name="std.alg.opt.gradient_descent_step"))
    lr = float(expect_number(args[2], fn_name="std.alg.opt.gradient_descent_step"))
    if lr <= 0:
        raise RuntimeSanskriptError("std.alg.opt.gradient_descent_step learning rate must be positive")
    return x - lr * grad


def _alg_parser_seq(args: list) -> dict:
    parsers = expect_list(args[0], fn_name="std.alg.parser.seq")
    for parser in parsers:
        node = expect_map(parser, fn_name="std.alg.parser.seq")
        kind = expect_text(node.get("kind", ""), fn_name="std.alg.parser.seq")
        if kind not in {"token", "seq", "choice"}:
            raise RuntimeSanskriptError(f"std.alg.parser.seq unknown parser kind {kind!r}")
    return {"kind": "seq", "parts": list(parsers)}


def _alg_parser_choice(args: list) -> dict:
    parsers = expect_list(args[0], fn_name="std.alg.parser.choice")
    for parser in parsers:
        node = expect_map(parser, fn_name="std.alg.parser.choice")
        kind = expect_text(node.get("kind", ""), fn_name="std.alg.parser.choice")
        if kind not in {"token", "seq", "choice"}:
            raise RuntimeSanskriptError(f"std.alg.parser.choice unknown parser kind {kind!r}")
    return {"kind": "choice", "parts": list(parsers)}


def _alg_parser_match_text(args: list) -> dict:
    token = expect_text(args[0], fn_name="std.alg.parser.match_text")
    return {"kind": "token", "value": token}


def _alg_parser_run(args: list) -> dict:
    parser = expect_map(args[0], fn_name="std.alg.parser.run")
    tokens = [expect_text(tok, fn_name="std.alg.parser.run") for tok in expect_list(args[1], fn_name="std.alg.parser.run")]

    def run_one(node: dict, index: int) -> tuple[bool, int, list]:
        kind = expect_text(node.get("kind", ""), fn_name="std.alg.parser.run")
        if kind == "token":
            value = expect_text(node.get("value", ""), fn_name="std.alg.parser.run")
            if index < len(tokens) and tokens[index] == value:
                return True, index + 1, [value]
            return False, index, []
        if kind == "seq":
            parts = expect_list(node.get("parts", []), fn_name="std.alg.parser.run")
            cur = index
            out = []
            for part in parts:
                ok, nxt, parsed = run_one(expect_map(part, fn_name="std.alg.parser.run"), cur)
                if not ok:
                    return False, index, []
                cur = nxt
                out.extend(parsed)
            return True, cur, out
        if kind == "choice":
            parts = expect_list(node.get("parts", []), fn_name="std.alg.parser.run")
            for part in parts:
                ok, nxt, parsed = run_one(expect_map(part, fn_name="std.alg.parser.run"), index)
                if ok:
                    return True, nxt, parsed
            return False, index, []
        raise RuntimeSanskriptError(f"std.alg.parser.run unknown parser kind {kind!r}")

    ok, idx, parsed = run_one(parser, 0)
    return {"ok": ok and idx == len(tokens), "next": idx, "parsed": parsed}


def _alg_graph_topological_sort(args: list) -> list:
    graph = _expect_graph_map(args[0], "std.alg.graph.topological_sort")
    indeg = {node: 0 for node in graph.keys()}
    for node, nxts in graph.items():
        for nxt in nxts:
            nxt_name = expect_text(nxt, fn_name="std.alg.graph.topological_sort")
            indeg.setdefault(nxt_name, 0)
            indeg[nxt_name] += 1
    queue = sorted([node for node, deg in indeg.items() if deg == 0])
    out: list[str] = []
    while queue:
        node = queue.pop(0)
        out.append(node)
        for nxt in graph.get(node, []):
            nxt_name = expect_text(nxt, fn_name="std.alg.graph.topological_sort")
            indeg[nxt_name] -= 1
            if indeg[nxt_name] == 0:
                queue.append(nxt_name)
                queue.sort()
    if len(out) != len(indeg):
        raise RuntimeSanskriptError("std.alg.graph.topological_sort graph contains a cycle")
    return out


def _alg_graph_schedule_passes(args: list) -> list:
    graph = _expect_graph_map(args[0], "std.alg.graph.schedule_passes")
    return _alg_graph_topological_sort([graph])


def _alg_deterministic_unique(args: list) -> list:
    values = expect_list(args[0], fn_name="std.alg.deterministic.unique")
    seen: dict[object, object] = {}
    for item in values:
        key = _as_hashable(item, "std.alg.deterministic.unique")
        if key not in seen:
            seen[key] = item
    ordered_items = sorted(seen.items(), key=lambda pair: _deterministic_order_key(pair[1]))
    return [value for _, value in ordered_items]


# ---------------------------------------------------------------------------
# phase14: http / data / plot / web / db / async / task
# ---------------------------------------------------------------------------


def _http_response_map(response, body: str) -> dict:
    headers = {key.lower(): value for key, value in response.headers.items()}
    return {
        "status": int(response.status),
        "url": str(response.geturl()),
        "headers": headers,
        "body": body,
    }


def _http_get(args: list) -> dict:
    url = expect_text(args[0], fn_name="std.http.get")
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            body = response.read().decode("utf-8", errors="replace")
            return _http_response_map(response, body)
    except Exception as exc:
        raise RuntimeSanskriptError(f"std.http.get failed: {exc}") from exc


def _http_post_json(args: list) -> dict:
    url = expect_text(args[0], fn_name="std.http.post_json")
    payload = stringify_json(args[1]).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            body = response.read().decode("utf-8", errors="replace")
            return _http_response_map(response, body)
    except Exception as exc:
        raise RuntimeSanskriptError(f"std.http.post_json failed: {exc}") from exc


def _http_server_once(args: list) -> dict:
    host = expect_text(args[0], fn_name="std.http.server_once")
    port = expect_int(args[1], fn_name="std.http.server_once")
    response_text = expect_text(args[2], fn_name="std.http.server_once")
    if port < 0 or port > 65535:
        raise RuntimeSanskriptError("std.http.server_once port must be 0..65535")
    captured: dict[str, object] = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # type: ignore[override]
            captured["method"] = "GET"
            captured["path"] = self.path
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(response_text.encode("utf-8"))

        def log_message(self, format: str, *args) -> None:  # noqa: A003
            return

    ready = threading.Event()
    try:
        with http.server.ThreadingHTTPServer((host, port), Handler) as server:
            server.timeout = 2.0
            actual_host, actual_port = server.server_address[:2]
            result: dict[str, object] = {"host": str(actual_host), "port": int(actual_port)}

            def serve_once() -> None:
                ready.set()
                deadline = time.time() + 4.0
                while time.time() < deadline and "method" not in captured:
                    server.handle_request()

            thread = threading.Thread(target=serve_once, daemon=True)
            thread.start()
            if not ready.wait(timeout=2.0):
                raise RuntimeSanskriptError("std.http.server_once failed to bind")
            thread.join(timeout=5.0)
            if thread.is_alive():
                raise RuntimeSanskriptError("std.http.server_once timed out waiting for request")
            if "method" not in captured:
                raise RuntimeSanskriptError("std.http.server_once received no request")
            result["status"] = 200
            result["method"] = captured["method"]
            result["path"] = captured.get("path", NIL)
            return result
    except RuntimeSanskriptError:
        raise
    except Exception as exc:
        raise RuntimeSanskriptError(f"std.http.server_once failed: {exc}") from exc


def _data_column(args: list) -> list:
    rows = expect_list(args[0], fn_name="std.data.column")
    key = expect_text(args[1], fn_name="std.data.column")
    out: list = []
    for row in rows:
        item = expect_map(row, fn_name="std.data.column")
        out.append(item.get(key, NIL))
    return out


def _data_describe(args: list) -> dict:
    nums = _stats_numbers(args[0], "std.data.describe")
    total = sum(nums)
    count = len(nums)
    return {"count": count, "min": min(nums), "max": max(nums), "mean": total / count}


def _plot_ascii(args: list) -> str:
    raw_values = [float(expect_number(v, fn_name="std.plot.ascii")) for v in expect_list(args[0], fn_name="std.plot.ascii")]
    width = expect_int(args[1], fn_name="std.plot.ascii")
    height = expect_int(args[2], fn_name="std.plot.ascii")
    if not raw_values:
        raise RuntimeSanskriptError("std.plot.ascii requires non-empty values")
    if width <= 1 or height <= 1:
        raise RuntimeSanskriptError("std.plot.ascii width/height must be > 1")
    values = raw_values[:width]
    while len(values) < width:
        values.append(values[-1])
    lo = min(values)
    hi = max(values)
    scale = (hi - lo) or 1.0
    rows = [[" " for _ in range(width)] for _ in range(height)]
    for x, value in enumerate(values):
        y = int(round((value - lo) / scale * (height - 1)))
        rows[height - 1 - y][x] = "*"
    return "\n".join("".join(row) for row in rows)


def _web_route_match(args: list) -> object:
    path = expect_text(args[0], fn_name="std.web.route_match")
    routes = expect_map(args[1], fn_name="std.web.route_match")
    path_parts = [part for part in path.strip("/").split("/") if part]
    for pattern, handler in routes.items():
        if not isinstance(pattern, str):
            continue
        route_parts = [part for part in pattern.strip("/").split("/") if part]
        if len(route_parts) != len(path_parts):
            continue
        params: dict[str, str] = {}
        ok = True
        for route_part, part in zip(route_parts, path_parts):
            if route_part.startswith("{") and route_part.endswith("}") and len(route_part) > 2:
                params[route_part[1:-1]] = part
            elif route_part != part:
                ok = False
                break
        if ok:
            return {"handler": handler, "params": params}
    return NIL


def _web_render(args: list) -> str:
    return _template_render(args)


def _db_sqlite_query(args: list) -> list:
    path = expect_text(args[0], fn_name="std.db.sqlite_query")
    query = expect_text(args[1], fn_name="std.db.sqlite_query")
    params = list(expect_list(args[2], fn_name="std.db.sqlite_query"))
    conn: sqlite3.Connection | None = None
    cur: sqlite3.Cursor | None = None
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        cur = conn.execute(query, params)
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as exc:
        raise RuntimeSanskriptError(f"std.db.sqlite_query failed: {exc}") from exc
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def _db_sqlite_exec(args: list) -> dict:
    path = expect_text(args[0], fn_name="std.db.sqlite_exec")
    query = expect_text(args[1], fn_name="std.db.sqlite_exec")
    params = list(expect_list(args[2], fn_name="std.db.sqlite_exec"))
    conn: sqlite3.Connection | None = None
    cur: sqlite3.Cursor | None = None
    try:
        conn = sqlite3.connect(path)
        cur = conn.execute(query, params)
        conn.commit()
        return {"rows_affected": cur.rowcount, "last_row_id": cur.lastrowid}
    except sqlite3.Error as exc:
        raise RuntimeSanskriptError(f"std.db.sqlite_exec failed: {exc}") from exc
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def _async_sleep_ms(args: list) -> int:
    ms = expect_int(args[0], fn_name="std.async.sleep_ms")
    if ms < 0:
        raise RuntimeSanskriptError("std.async.sleep_ms requires non-negative delay")
    # Blocking host sleep: VM has no await yet; avoids per-call asyncio.run().
    time.sleep(ms / 1000.0)
    return ms


def _async_read_text(args: list) -> str:
    path = expect_text(args[0], fn_name="std.async.read_text")
    try:
        return _ASYNC_IO_POOL.submit(Path(path).read_text, encoding="utf-8").result()
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.async.read_text failed: {exc}") from exc


def _task_run_after_ms(args: list) -> object:
    ms = expect_int(args[0], fn_name="std.task.run_after_ms")
    value = args[1]
    if ms < 0:
        raise RuntimeSanskriptError("std.task.run_after_ms requires non-negative delay")
    time.sleep(ms / 1000.0)
    return value


def _task_schedule(args: list) -> list:
    jobs = expect_list(args[0], fn_name="std.task.schedule")
    timeline: list[tuple[int, object]] = []
    for item in jobs:
        pair = expect_list(item, fn_name="std.task.schedule")
        if len(pair) != 2:
            raise RuntimeSanskriptError("std.task.schedule jobs must be [delay_ms, value]")
        timeline.append((expect_int(pair[0], fn_name="std.task.schedule"), pair[1]))
    timeline.sort(key=lambda x: x[0])
    out: list = []
    elapsed = 0
    for delay, value in timeline:
        wait_ms = max(0, delay - elapsed)
        if wait_ms:
            time.sleep(wait_ms / 1000.0)
        elapsed = max(elapsed, delay)
        out.append(value)
    return out


# ---------------------------------------------------------------------------
# phase22: web / apps / games / research / ml (host bridge + honest scaffolds)
# ---------------------------------------------------------------------------


def _http_request(args: list) -> dict:
    return _p22.http_request(args)


def _http_response(args: list) -> dict:
    return _p22.http_response(args)


def _http_cookie_parse(args: list) -> dict:
    return _p22.cookie_parse(args)


def _http_cookie_header(args: list) -> str:
    return _p22.cookie_header(args)


def _http_session_create(_args: list) -> str:
    return _p22.session_create(_args)


def _http_session_get(args: list) -> object:
    return _p22.session_get(args)


def _http_session_set(args: list) -> str:
    return _p22.session_set(args)


def _http_auth_basic_header(args: list) -> str:
    return _p22.auth_basic_header(args)


def _http_auth_bearer_verify(args: list) -> bool:
    return _p22.auth_bearer_verify(args)


def _http_middleware_apply(args: list) -> dict:
    return _p22.middleware_apply(args)


def _http_router_dispatch(args: list) -> object:
    return _p22.router_dispatch(args)


def _http_server_route_once(args: list) -> dict:
    return _p22.http_server_route_once(args)


def _http_client_roundtrip(_args: list) -> dict:
    return _p22.http_client_roundtrip(_args)


def _web_html_escape(args: list) -> str:
    return _p22.html_escape(args)


def _web_html_element(args: list) -> str:
    return _p22.html_element(args)


def _web_css_bundle(args: list) -> str:
    return _p22.css_bundle(args)


def _p22_inventory(_args: list) -> list[dict]:
    return _p22.phase22_inventory()


def _web_bridge_plan(_args: list) -> dict:
    return _p22.bridge_plan(_args)


def _web_bridge_execute(args: list) -> dict:
    return _p22.bridge_execute(args)


def _web_webgl_plan(_args: list) -> dict:
    return _p22.webgl_plan(_args)


def _web_webgl_stub(args: list) -> dict:
    return _p22.webgl_stub(args)


def _web_dom_simulate(args: list) -> dict:
    return _p22.dom_simulate(args)


def _web_dom_dispatch(args: list) -> dict:
    return _p22.dom_dispatch(args)


def _web_canvas_raster(args: list) -> str:
    return _p22.canvas_raster(args)


def _gui_capabilities_plan(_args: list) -> dict:
    return _p22.gui_capabilities_plan(_args)


def _gui_simulate(args: list) -> dict:
    return _p22.gui_simulate(args)


def _game_loop_run(args: list) -> list:
    return _p22.game_loop_run(args)


def _game_input_state(args: list) -> dict:
    return _p22.game_input_state(args)


def _game_audio_plan(_args: list) -> dict:
    return _p22.game_audio_plan(_args)


def _game_audio_tick(args: list) -> dict:
    return _p22.game_audio_tick(args)


def _game_asset_resolve(args: list) -> list:
    return _p22.game_asset_resolve(args)


def _game_sprite_atlas(args: list) -> dict:
    return _p22.game_sprite_atlas(args)


def _game_physics2d_step(args: list) -> dict:
    return _p22.game_physics2d_step(args)


def _game_scene3d_plan(_args: list) -> dict:
    return _p22.game_scene3d_plan(_args)


def _data_frame(args: list) -> dict:
    return _p22.data_frame(args)


def _data_csv_read(args: list) -> list:
    return _p22.data_csv_read(args)


def _data_csv_write(args: list) -> dict:
    return _p22.data_csv_write(args)


def _data_parquet_plan(_args: list) -> dict:
    return _p22.data_parquet_plan(_args)


def _data_parquet_stub_read(args: list) -> list:
    return _p22.parquet_stub_read(args)


def _plot_histogram_ascii(args: list) -> str:
    return _p22.plot_histogram_ascii(args)


def _plot_sparkline(args: list) -> str:
    return _p22.plot_sparkline(args)


def _linalg_matmul(args: list) -> list:
    return _p22.linalg_matmul(args)


def _linalg_dot(args: list) -> float:
    return _p22.linalg_dot(args)


def _linalg_transpose(args: list) -> list:
    return _p22.linalg_transpose(args)


def _tensor_shape(args: list) -> list:
    return _p22.tensor_shape(args)


def _tensor_reshape(args: list) -> list:
    return _p22.tensor_reshape(args)


def _ml_ad_roadmap(_args: list) -> dict:
    return _p22.ml_ad_roadmap(_args)


def _ml_model_pack(args: list) -> str:
    return _p22.ml_model_pack(args)


def _ml_model_unpack(args: list) -> dict:
    return _p22.ml_model_unpack(args)


def _ml_python_bridge_plan(_args: list) -> dict:
    return _p22.ml_python_bridge_plan(_args)


def _ml_native_kernels_plan(_args: list) -> dict:
    return _p22.ml_native_kernels_plan(_args)


def _db_postgres_plan(_args: list) -> dict:
    return _p22.postgres_plan(_args)


def _db_postgres_stub_connect(args: list) -> dict:
    return _p22.postgres_stub_connect(args)


def _db_client(args: list) -> dict:
    return _p22.db_client(args)


def _phase22_seal_run(_args: list) -> dict:
    return _p22.phase22_seal_run(_args)


def _notebook_split_cells(args: list) -> list:
    return _p22.notebook_split_cells(args)


def _research_template_render(args: list) -> str:
    return _p22.research_template_render(args)


def _env_fingerprint(args: list) -> str:
    return _p22.env_fingerprint(args)


# ---------------------------------------------------------------------------
# YAML/TOML/XML helpers (minimal, no third-party deps)
# ---------------------------------------------------------------------------


def _parse_yaml(text: str) -> object:
    lines = [line.rstrip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]
    if not lines:
        return {}
    root: dict[str, object] = {}
    stack: list[tuple[int, dict[str, object] | list]] = [(-1, root)]
    list_mode = False
    for raw in lines:
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if line.startswith("- "):
            if not isinstance(parent, list):
                raise RuntimeSanskriptError("std.yaml.parse list item without list parent")
            value = _yaml_scalar(line[2:].strip())
            parent.append(from_json(value) if isinstance(value, (dict, list)) else value)
            continue
        if ":" not in line:
            raise RuntimeSanskriptError(f"std.yaml.parse invalid line: {line}")
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if not isinstance(parent, dict):
            raise RuntimeSanskriptError("std.yaml.parse mapping entry without map parent")
        if val == "":
            child: dict[str, object] = {}
            parent[key] = child
            stack.append((indent, child))
        elif val.startswith("[") and val.endswith("]"):
            items = [from_json(_yaml_scalar(part.strip())) for part in val[1:-1].split(",") if part.strip()]
            parent[key] = items
        else:
            parent[key] = from_json(_yaml_scalar(val))
    return from_json(root)


def _yaml_scalar(text: str) -> object:
    if text in {"true", "false"}:
        return text == "true"
    if text in {"null", "~"}:
        return None
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        return text[1:-1]
    try:
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return text


def _stringify_yaml(value: object, indent: int = 0) -> str:
    prefix = "  " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.append(_stringify_yaml(item, indent + 1))
            else:
                lines.append(f"{prefix}{key}: {_yaml_format_scalar(item)}")
        return "\n".join(lines)
    if isinstance(value, list):
        lines = [f"{prefix}- {_yaml_format_scalar(item)}" for item in value]
        return "\n".join(lines)
    return f"{prefix}{_yaml_format_scalar(value)}"


def _yaml_format_scalar(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if any(ch in text for ch in ":,#[]{}") or text.strip() != text:
        return json.dumps(text, ensure_ascii=False)
    return text


def _parse_toml_simple(text: str) -> object:
    root: dict[str, object] = {}
    section: dict[str, object] = root
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            name = line[1:-1].strip()
            section = {}
            root[name] = section
            continue
        if "=" not in line:
            raise RuntimeSanskriptError(f"std.toml.parse invalid line: {line}")
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()
        if val.startswith('"') and val.endswith('"'):
            section[key] = val[1:-1]
        elif val in {"true", "false"}:
            section[key] = val == "true"
        else:
            try:
                section[key] = int(val) if "." not in val else float(val)
            except ValueError:
                section[key] = val
    return from_json(root)


def _stringify_toml(value: object) -> str:
    if not isinstance(value, dict):
        raise RuntimeSanskriptError("std.toml.stringify expects a map at top level")
    lines: list[str] = []
    for key, item in value.items():
        if isinstance(item, dict):
            lines.append(f"[{key}]")
            for sub_key, sub_val in item.items():
                lines.append(f"{sub_key} = {_toml_format_scalar(sub_val)}")
            lines.append("")
        else:
            lines.append(f"{key} = {_toml_format_scalar(item)}")
    return "\n".join(lines).strip() + "\n"


def _toml_format_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value))


def _xml_element_to_map(element: ET.Element) -> dict:
    children = [_xml_element_to_map(child) for child in element]
    attrs = {f"@{k}": v for k, v in element.attrib.items()}
    text = (element.text or "").strip()
    payload: dict[str, object] = {"tag": element.tag, **attrs}
    if text:
        payload["text"] = text
    if children:
        payload["children"] = children
    return payload


def _xml_map_to_element(tag: str, payload: dict) -> ET.Element:
    element = ET.Element(tag)
    for key, value in payload.items():
        if key == "tag":
            continue
        if key == "text":
            element.text = str(value)
            continue
        if key.startswith("@"):
            element.set(key[1:], str(value))
            continue
        if key == "children" and isinstance(value, list):
            for child in value:
                if isinstance(child, dict) and "tag" in child:
                    element.append(_xml_map_to_element(str(child["tag"]), child))
    return element


# ---------------------------------------------------------------------------
# rakṣita systems primitives (sync/thread/ffi/net)
# ---------------------------------------------------------------------------


def _atomic_mutex(atom: dict[str, object]) -> threading.Lock:
    mutex = atom.get("mutex")
    if not isinstance(mutex, threading.Lock):
        raise RuntimeSanskriptError("std.sync.atomic internal mutex missing")
    return mutex


def _sync_atomic_new(args: list) -> OpaqueHandle:
    initial = expect_int(args[0], fn_name="std.sync.atomic.new")
    handle = _next_handle_id()
    with _REGISTRY_LOCK:
        _ATOMIC_REGISTRY[handle] = {"value": initial, "mutex": threading.Lock()}
    return OpaqueHandle(kind="atomic", handle_id=handle)


def _sync_atomic_load(args: list) -> int:
    atom, bound = _resolve_atomic(args, fn_name="std.sync.atomic.load")
    with _atomic_mutex(atom):
        if bound is not None:
            block, offset = bound
            buf = block.get("bytes")
            if not isinstance(buf, bytearray):
                raise RuntimeSanskriptError("std.sync.atomic.load invalid memory backing")
            return int(buf[offset])
        return int(atom["value"])


def _sync_atomic_store(args: list) -> bool:
    value = expect_int(args[1], fn_name="std.sync.atomic.store")
    atom, bound = _resolve_atomic(args, fn_name="std.sync.atomic.store")
    with _atomic_mutex(atom):
        if bound is not None:
            if value < 0 or value > 255:
                raise RuntimeSanskriptError("std.sync.atomic.store value must be 0..255")
            block, offset = bound
            buf = block.get("bytes")
            if not isinstance(buf, bytearray):
                raise RuntimeSanskriptError("std.sync.atomic.store invalid memory backing")
            buf[offset] = value
            atom["value"] = value
            return True
        atom["value"] = value
        return True


def _sync_atomic_fetch_add(args: list) -> int:
    delta = expect_int(args[1], fn_name="std.sync.atomic.fetch_add")
    atom, bound = _resolve_atomic(args, fn_name="std.sync.atomic.fetch_add")
    with _atomic_mutex(atom):
        old = int(atom["value"])
        new_value = old + delta
        if bound is not None:
            if new_value < 0 or new_value > 255:
                raise RuntimeSanskriptError("std.sync.atomic.fetch_add result must be 0..255")
            block, offset = bound
            buf = block.get("bytes")
            if not isinstance(buf, bytearray):
                raise RuntimeSanskriptError("std.sync.atomic.fetch_add invalid memory backing")
            buf[offset] = new_value
        atom["value"] = new_value
        return old


def _sync_atomic_compare_exchange(args: list) -> ResultValue:
    expected = expect_int(args[1], fn_name="std.sync.atomic.compare_exchange")
    desired = expect_int(args[2], fn_name="std.sync.atomic.compare_exchange")
    atom, bound = _resolve_atomic(args, fn_name="std.sync.atomic.compare_exchange")
    with _atomic_mutex(atom):
        current = int(atom["value"])
        if current == expected:
            if bound is not None:
                if desired < 0 or desired > 255:
                    raise RuntimeSanskriptError("std.sync.atomic.compare_exchange desired must be 0..255")
                block, offset = bound
                buf = block.get("bytes")
                if not isinstance(buf, bytearray):
                    raise RuntimeSanskriptError("std.sync.atomic.compare_exchange invalid memory backing")
                buf[offset] = desired
            atom["value"] = desired
            return ResultValue(ok=True, value=desired)
        return ResultValue(ok=False, value=current)


def _sync_lock_new(args: list) -> OpaqueHandle:
    _ = args
    handle = _next_handle_id()
    with _REGISTRY_LOCK:
        _LOCK_REGISTRY[handle] = threading.Lock()
    return OpaqueHandle(kind="lock", handle_id=handle)


def _sync_lock_acquire(args: list) -> bool:
    handle = args[0]
    timeout_ms = expect_int(args[1], fn_name="std.sync.lock.acquire")
    if not isinstance(handle, OpaqueHandle) or handle.kind != "lock":
        raise RuntimeSanskriptError("std.sync.lock.acquire expects lock handle")
    lock = _LOCK_REGISTRY.get(handle.handle_id)
    if lock is None:
        raise RuntimeSanskriptError("std.sync.lock.acquire unknown lock handle")
    timeout = None if timeout_ms < 0 else timeout_ms / 1000.0
    return lock.acquire(timeout=timeout)


def _sync_lock_release(args: list) -> bool:
    handle = args[0]
    if not isinstance(handle, OpaqueHandle) or handle.kind != "lock":
        raise RuntimeSanskriptError("std.sync.lock.release expects lock handle")
    lock = _LOCK_REGISTRY.get(handle.handle_id)
    if lock is None:
        raise RuntimeSanskriptError("std.sync.lock.release unknown lock handle")
    try:
        lock.release()
    except RuntimeError as exc:
        raise RuntimeSanskriptError("std.sync.lock.release on unlocked lock") from exc
    return True


def _sync_channel_new(args: list) -> OpaqueHandle:
    capacity = expect_int(args[0], fn_name="std.sync.channel.new")
    if capacity < 0:
        raise RuntimeSanskriptError("std.sync.channel.new capacity must be >= 0")
    handle = _next_handle_id()
    with _REGISTRY_LOCK:
        _CHANNEL_REGISTRY[handle] = Queue(maxsize=capacity if capacity > 0 else 0)
    return OpaqueHandle(kind="channel", handle_id=handle)


def _sync_channel_send(args: list) -> bool:
    handle = args[0]
    payload = args[1]
    if not isinstance(handle, OpaqueHandle) or handle.kind != "channel":
        raise RuntimeSanskriptError("std.sync.channel.send expects channel handle")
    if not _is_send_safe(payload):
        raise RuntimeSanskriptError("std.sync.channel.send payload is not send-safe")
    queue = _CHANNEL_REGISTRY.get(handle.handle_id)
    if queue is None:
        raise RuntimeSanskriptError("std.sync.channel.send unknown channel handle")
    queue.put(payload, block=True)
    return True


def _sync_channel_send_timeout(args: list) -> bool:
    handle = args[0]
    payload = args[1]
    timeout_ms = expect_int(args[2], fn_name="std.sync.channel.send_timeout")
    if not isinstance(handle, OpaqueHandle) or handle.kind != "channel":
        raise RuntimeSanskriptError("std.sync.channel.send_timeout expects channel handle")
    if not _is_send_safe(payload):
        raise RuntimeSanskriptError("std.sync.channel.send_timeout payload is not send-safe")
    queue = _CHANNEL_REGISTRY.get(handle.handle_id)
    if queue is None:
        raise RuntimeSanskriptError("std.sync.channel.send_timeout unknown channel handle")
    if timeout_ms < 0:
        raise RuntimeSanskriptError("std.sync.channel.send_timeout requires non-negative timeout")
    try:
        queue.put(payload, block=True, timeout=timeout_ms / 1000.0)
    except Full:
        return False
    return True


def _sync_channel_try_send(args: list) -> bool:
    handle = args[0]
    payload = args[1]
    if not isinstance(handle, OpaqueHandle) or handle.kind != "channel":
        raise RuntimeSanskriptError("std.sync.channel.try_send expects channel handle")
    if not _is_send_safe(payload):
        raise RuntimeSanskriptError("std.sync.channel.try_send payload is not send-safe")
    queue = _CHANNEL_REGISTRY.get(handle.handle_id)
    if queue is None:
        raise RuntimeSanskriptError("std.sync.channel.try_send unknown channel handle")
    try:
        queue.put_nowait(payload)
    except Full:
        return False
    return True


def _sync_channel_recv(args: list) -> object:
    handle = args[0]
    timeout_ms = expect_int(args[1], fn_name="std.sync.channel.recv")
    if not isinstance(handle, OpaqueHandle) or handle.kind != "channel":
        raise RuntimeSanskriptError("std.sync.channel.recv expects channel handle")
    queue = _CHANNEL_REGISTRY.get(handle.handle_id)
    if queue is None:
        raise RuntimeSanskriptError("std.sync.channel.recv unknown channel handle")
    timeout = None if timeout_ms < 0 else timeout_ms / 1000.0
    try:
        return queue.get(block=True, timeout=timeout)
    except Empty:
        return OptionValue(present=False)


def _sync_channel_try_recv(args: list) -> OptionValue:
    handle = args[0]
    if not isinstance(handle, OpaqueHandle) or handle.kind != "channel":
        raise RuntimeSanskriptError("std.sync.channel.try_recv expects channel handle")
    queue = _CHANNEL_REGISTRY.get(handle.handle_id)
    if queue is None:
        raise RuntimeSanskriptError("std.sync.channel.try_recv unknown channel handle")
    try:
        return OptionValue(present=True, value=queue.get_nowait())
    except Empty:
        return OptionValue(present=False)


def _thread_marker_send(args: list) -> bool:
    return _is_send_safe(args[0])


def _thread_marker_share(args: list) -> bool:
    value = args[0]
    if isinstance(value, OpaqueHandle) and value.kind in {
        "atomic",
        "lock",
        "mutex",
        "rwlock",
        "semaphore",
    }:
        return True
    return _is_send_safe(value)


def _ffi_call_checked(args: list) -> object:
    symbol = expect_text(args[0], fn_name="std.ffi.call_checked")
    params = expect_list(args[1], fn_name="std.ffi.call_checked")
    for index, item in enumerate(params, start=1):
        if not _is_ffi_abi_safe(item):
            raise RuntimeSanskriptError(
                f"std.ffi.call_checked argument {index} is not ABI-safe at FFI boundary"
            )
    if symbol not in _FFI_ALLOWLIST:
        raise RuntimeSanskriptError(
            f"std.ffi.call_checked symbol {symbol!r} not in allowlist"
        )
    spec = NATIVE_REGISTRY.get(symbol)
    if spec is None:
        raise RuntimeSanskriptError(f"std.ffi.call_checked unknown symbol {symbol!r}")
    if len(params) != spec.arity:
        raise RuntimeSanskriptError(
            f"std.ffi.call_checked {symbol!r} expects {spec.arity} argument(s), got {len(params)}"
        )
    return spec.fn(params)


def _ffi_abi_stable_struct(args: list) -> bool:
    schema = expect_map(args[0], fn_name="std.ffi.abi_stable_struct")
    if "name" not in schema or "fields" not in schema:
        raise RuntimeSanskriptError("std.ffi.abi_stable_struct requires name and fields")
    name = schema["name"]
    fields = schema["fields"]
    if not isinstance(name, str) or not name:
        raise RuntimeSanskriptError("std.ffi.abi_stable_struct requires non-empty name")
    if not isinstance(fields, list) or not fields:
        raise RuntimeSanskriptError("std.ffi.abi_stable_struct requires non-empty field list")
    offset = 0
    seen_names: set[str] = set()
    for item in fields:
        if not isinstance(item, dict):
            raise RuntimeSanskriptError("std.ffi.abi_stable_struct fields must be records")
        field_name = item.get("name")
        field_type = item.get("type")
        if not isinstance(field_name, str) or not isinstance(field_type, str):
            raise RuntimeSanskriptError("std.ffi.abi_stable_struct fields need text name/type")
        if field_name in seen_names:
            raise RuntimeSanskriptError(
                f"std.ffi.abi_stable_struct duplicate field name {field_name!r}"
            )
        seen_names.add(field_name)
        width = {"i32": 4, "u32": 4, "i64": 8, "f64": 8, "bool": 1}.get(field_type)
        if width is None:
            raise RuntimeSanskriptError(
                f"std.ffi.abi_stable_struct unsupported ABI field type {field_type!r}"
            )
        declared_offset = item.get("offset", offset)
        if not isinstance(declared_offset, int):
            raise RuntimeSanskriptError(
                f"std.ffi.abi_stable_struct field {field_name!r} offset must be integer"
            )
        if declared_offset != offset:
            raise RuntimeSanskriptError(
                f"std.ffi.abi_stable_struct field {field_name!r} has unstable offset"
            )
        offset += width
    declared_size = schema.get("size")
    if declared_size is not None:
        if not isinstance(declared_size, int) or declared_size != offset:
            raise RuntimeSanskriptError(
                f"std.ffi.abi_stable_struct size mismatch: expected {offset}, got {declared_size!r}"
            )
    return True


def _net_resolve_host(args: list) -> list:
    host = expect_text(args[0], fn_name="std.net.resolve_host")
    try:
        infos = socket.getaddrinfo(host, None)
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.net.resolve_host failed: {exc}") from exc
    out: list[str] = []
    for entry in infos:
        addr = entry[4][0]
        if addr not in out:
            out.append(addr)
    return out


def _net_tcp_probe(args: list) -> bool:
    host = expect_text(args[0], fn_name="std.net.tcp_probe")
    port = expect_int(args[1], fn_name="std.net.tcp_probe")
    timeout_ms = expect_int(args[2], fn_name="std.net.tcp_probe")
    if port < 0 or port > 65535:
        raise RuntimeSanskriptError("std.net.tcp_probe port must be in 0..65535")
    timeout = max(1, timeout_ms) / 1000.0
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _net_dns_lookup(args: list) -> list:
    host = expect_text(args[0], fn_name="std.net.dns_lookup")
    kind = expect_text(args[1], fn_name="std.net.dns_lookup").upper()
    if kind not in {"A", "AAAA", "ANY"}:
        raise RuntimeSanskriptError("std.net.dns_lookup kind must be A, AAAA, or ANY")
    try:
        infos = socket.getaddrinfo(host, None)
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.net.dns_lookup failed: {exc}") from exc
    family_filter: int | None
    if kind == "A":
        family_filter = socket.AF_INET
    elif kind == "AAAA":
        family_filter = socket.AF_INET6
    else:
        family_filter = None
    out: list[str] = []
    for entry in infos:
        if family_filter is not None and entry[0] != family_filter:
            continue
        addr = entry[4][0]
        if addr not in out:
            out.append(addr)
    return out


def _net_tls_available(args: list) -> bool:
    try:
        import ssl  # noqa: F401
    except ImportError:
        return False
    return True


def _net_tls_probe(args: list) -> dict:
    host = expect_text(args[0], fn_name="std.net.tls_probe")
    port = expect_int(args[1], fn_name="std.net.tls_probe")
    timeout_ms = expect_int(args[2], fn_name="std.net.tls_probe")
    if port < 1 or port > 65535:
        raise RuntimeSanskriptError("std.net.tls_probe port must be in 1..65535")
    try:
        import ssl
    except ImportError as exc:
        raise RuntimeSanskriptError("std.net.tls_probe requires ssl support") from exc
    timeout = max(1, timeout_ms) / 1000.0
    context = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=timeout) as raw:
            with context.wrap_socket(raw, server_hostname=host) as secure:
                cipher = secure.cipher()
                return {
                    "ok": True,
                    "cipher": cipher[0] if cipher else "",
                    "version": secure.version() or "",
                }
    except OSError:
        return {"ok": False, "cipher": "", "version": ""}


def _net_browser_fetch_plan(args: list) -> dict:
    url = expect_text(args[0], fn_name="std.net.browser_fetch_plan")
    return {
        "url": url,
        "method": "GET",
        "implementation_state": "scaffold",
        "plan_only": True,
        "requires_browser_runtime": True,
        "notes": ("plan-only metadata; does not perform browser fetch",),
    }


def _net_browser_fetch_sim(args: list) -> dict:
    url = expect_text(args[0], fn_name="std.net.browser_fetch_sim")
    return browser_fetch_simulation(url)


def _watch_snapshot_path(path: Path) -> dict[str, dict[str, float | int]]:
    snapshot: dict[str, dict[str, float | int]] = {}
    if path.is_file():
        stat = path.stat()
        snapshot[str(path)] = {"mtime": stat.st_mtime, "size": stat.st_size}
        return snapshot
    if not path.is_dir():
        return snapshot
    for child in path.rglob("*"):
        if child.is_file():
            stat = child.stat()
            snapshot[str(child)] = {"mtime": stat.st_mtime, "size": stat.st_size}
    return snapshot


def _watch_snapshot(args: list) -> OpaqueHandle:
    root = Path(expect_text(args[0], fn_name="std.watch.snapshot"))
    handle_id = _next_handle_id()
    _WATCH_SNAPSHOT_REGISTRY[handle_id] = _watch_snapshot_path(root)
    return OpaqueHandle(kind="watch.snapshot", handle_id=handle_id)


def _watch_diff(args: list) -> list:
    before = args[0]
    after = args[1]
    for handle, label in ((before, "before"), (after, "after")):
        if not isinstance(handle, OpaqueHandle) or handle.kind != "watch.snapshot":
            raise RuntimeSanskriptError(f"std.watch.diff requires watch.snapshot handle for {label}")
    left = _WATCH_SNAPSHOT_REGISTRY.get(before.handle_id)
    right = _WATCH_SNAPSHOT_REGISTRY.get(after.handle_id)
    if left is None or right is None:
        raise RuntimeSanskriptError("std.watch.diff unknown snapshot handle")
    changes: list[dict[str, str]] = []
    keys = set(left) | set(right)
    for key in sorted(keys):
        if key not in left:
            changes.append({"path": key, "kind": "created"})
        elif key not in right:
            changes.append({"path": key, "kind": "deleted"})
        elif left[key] != right[key]:
            changes.append({"path": key, "kind": "modified"})
    return changes


def _watch_poll_once(args: list) -> list:
    root = Path(expect_text(args[0], fn_name="std.watch.poll_once"))
    timeout_ms = expect_int(args[1], fn_name="std.watch.poll_once")
    if timeout_ms < 0:
        raise RuntimeSanskriptError("std.watch.poll_once timeout must be non-negative")
    baseline = _watch_snapshot_path(root)
    deadline = time.monotonic() + (timeout_ms / 1000.0)
    while time.monotonic() <= deadline:
        current = _watch_snapshot_path(root)
        if current != baseline:
            changes: list[dict[str, str]] = []
            keys = set(baseline) | set(current)
            for key in sorted(keys):
                if key not in baseline:
                    changes.append({"path": key, "kind": "created"})
                elif key not in current:
                    changes.append({"path": key, "kind": "deleted"})
                elif baseline[key] != current[key]:
                    changes.append({"path": key, "kind": "modified"})
            return changes
        time.sleep(min(0.05, max(0.001, timeout_ms / 1000.0)))
    return []


def _storage_web_namespace(args: list) -> str:
    return expect_text(args[0], fn_name="std.storage.web_*")


def _storage_web_bucket(ns: str) -> dict[str, str]:
    if ns not in _WEB_STORAGE:
        _WEB_STORAGE[ns] = web_storage_load(ns)
    return _WEB_STORAGE[ns]


def _storage_web_persist(ns: str) -> None:
    web_storage_save(ns, _storage_web_bucket(ns))


def _storage_web_set(args: list) -> bool:
    ns = _storage_web_namespace([args[0]])
    key = expect_text(args[1], fn_name="std.storage.web_set")
    value = expect_text(args[2], fn_name="std.storage.web_set")
    bucket = _storage_web_bucket(ns)
    bucket[key] = value
    _storage_web_persist(ns)
    return True


def _storage_web_get(args: list) -> object:
    ns = _storage_web_namespace([args[0]])
    key = expect_text(args[1], fn_name="std.storage.web_get")
    bucket = _storage_web_bucket(ns)
    return bucket.get(key, NIL)


def _storage_web_remove(args: list) -> bool:
    ns = _storage_web_namespace([args[0]])
    key = expect_text(args[1], fn_name="std.storage.web_remove")
    bucket = _storage_web_bucket(ns)
    if key in bucket:
        del bucket[key]
        _storage_web_persist(ns)
        return True
    return False


def _storage_web_clear(args: list) -> bool:
    ns = _storage_web_namespace([args[0]])
    _WEB_STORAGE[ns] = {}
    _storage_web_persist(ns)
    return True


def _storage_web_keys(args: list) -> list:
    ns = _storage_web_namespace([args[0]])
    return sorted(_storage_web_bucket(ns).keys())


def _platform_detect(args: list) -> dict:
    payload = detect_platform_features()
    payload["platform_key"] = payload.get("host_platform", host_platform_family())
    payload["features"] = _platform_feature_names(payload)
    return payload


def _platform_feature_names(payload: dict[str, object]) -> list[str]:
    names = [
        "path.join",
        "path.normalize",
        "process.subprocess",
        "watch.polling",
        "net.socket",
        "terminal.ansi",
        "console.log",
        "storage.web_file_backed",
        "platform.detect",
        "compile.plan",
    ]
    host = str(payload.get("host_platform", ""))
    if host == "windows":
        names.append("process.windows_api")
    if host in {"linux", "macos"}:
        names.append("process.posix_api")
    if payload.get("ssl_available"):
        names.append("net.tls")
    return sorted(names)


def _platform_feature(args: list) -> bool:
    name = expect_text(args[0], fn_name="std.platform.feature")
    return name in _platform_feature_names(detect_platform_features())


def _platform_compile_plan(args: list) -> dict:
    target = expect_text(args[0], fn_name="std.platform.compile_plan")
    try:
        return platform_compile_plan(target)
    except ValueError as exc:
        raise RuntimeSanskriptError(f"std.platform.compile_plan failed: {exc}") from exc


def _terminal_is_tty(args: list) -> bool:
    stream = expect_text(args[0], fn_name="std.terminal.is_tty").lower()
    if stream == "stdout":
        return sys.stdout.isatty()
    if stream == "stderr":
        return sys.stderr.isatty()
    if stream == "stdin":
        return sys.stdin.isatty()
    raise RuntimeSanskriptError("std.terminal.is_tty stream must be stdout, stderr, or stdin")


def _console_log(args: list) -> bool:
    level = expect_text(args[0], fn_name="std.console.log").lower()
    message = expect_text(args[1], fn_name="std.console.log")
    if level not in {"log", "info", "warn", "error", "debug"}:
        raise RuntimeSanskriptError("std.console.log unknown level")
    sys.stdout.write(f"[console:{level}] {message}\n")
    sys.stdout.flush()
    return True


# ---------------------------------------------------------------------------
# phase13: memory model by tier
# ---------------------------------------------------------------------------


def _memory_alloc(args: list, *, allocator: str) -> OpaqueHandle:
    size = expect_int(args[0], fn_name=f"std.memory.alloc.{allocator}")
    alignment = expect_int(args[1], fn_name=f"std.memory.alloc.{allocator}")
    layout = expect_text(args[2], fn_name=f"std.memory.alloc.{allocator}")
    packed = expect_bool(args[3], fn_name=f"std.memory.alloc.{allocator}")
    abi = expect_text(args[4], fn_name=f"std.memory.alloc.{allocator}")
    region = expect_text(args[5], fn_name=f"std.memory.alloc.{allocator}")
    if size < 0:
        raise RuntimeSanskriptError(f"std.memory.alloc.{allocator} size must be non-negative")
    if alignment <= 0 or (alignment & (alignment - 1)) != 0:
        raise RuntimeSanskriptError(f"std.memory.alloc.{allocator} alignment must be power-of-two")
    if packed and alignment != 1:
        raise RuntimeSanskriptError(f"std.memory.alloc.{allocator} packed layout requires alignment=1")
    if layout not in {"native", "packed", "abi", "repr-c"}:
        raise RuntimeSanskriptError(f"std.memory.alloc.{allocator} unknown layout {layout!r}")
    if packed and layout != "packed":
        raise RuntimeSanskriptError("std.memory.alloc.* packed flag requires packed layout")
    allowed_abi = _memory_allowed_abi(layout=layout)
    if abi not in allowed_abi:
        raise RuntimeSanskriptError(
            f"std.memory.alloc.{allocator} abi {abi!r} incompatible with layout {layout!r}"
        )
    handle_id = _next_handle_id()
    base = handle_id * 4096
    bytes_buf = bytearray(size)
    _MEMORY_REGISTRY[handle_id] = {
        "base": base,
        "size": size,
        "bytes": bytes_buf,
        "alignment": alignment,
        "layout": layout,
        "padding": 0 if packed else ((alignment - (size % alignment)) % alignment),
        "packed": packed,
        "abi": abi,
        "allocator": allocator,
        "region": region,
        "shared_borrows": 0,
        "mut_borrows": 0,
        "moved": False,
        "dropped": False,
        "atomic_offsets": set(),
        "last_fence": 0,
    }
    return OpaqueHandle(kind="mem.block", handle_id=handle_id)


def _memory_alloc_heap(args: list) -> OpaqueHandle:
    return _memory_alloc(args, allocator="heap")


def _memory_alloc_stack(args: list) -> OpaqueHandle:
    return _memory_alloc(args, allocator="stack")


def _memory_alloc_arena(args: list) -> OpaqueHandle:
    return _memory_alloc(args, allocator="arena")


def _memory_dealloc(args: list) -> bool:
    handle = args[0]
    block = _memory_block_from_handle(handle, fn_name="std.memory.dealloc")
    if int(block.get("shared_borrows", 0)) or int(block.get("mut_borrows", 0)):
        raise RuntimeSanskriptError("std.memory.dealloc cannot free while borrows are active")
    block["dropped"] = True
    block["bytes"] = bytearray()
    return True


def _memory_layout_describe(args: list) -> dict:
    block = _memory_block_from_handle(args[0], fn_name="std.memory.layout.describe")
    return {
        "base": int(block["base"]),
        "size": int(block["size"]),
        "alignment": int(block["alignment"]),
        "layout": str(block["layout"]),
        "padding": int(block["padding"]),
        "packed": bool(block["packed"]),
        "abi": str(block["abi"]),
        "allocator": str(block["allocator"]),
        "region": str(block["region"]),
    }


def _memory_ref(args: list) -> OpaqueHandle:
    block_handle = args[0]
    offset = expect_int(args[1], fn_name="std.memory.ref")
    block = _memory_block_from_handle(block_handle, fn_name="std.memory.ref")
    if offset < 0 or offset > int(block.get("size", 0)):
        raise RuntimeSanskriptError("std.memory.ref offset out of bounds")
    ref_id = _next_handle_id()
    _MEMORY_REF_REGISTRY[ref_id] = {
        "block": block_handle,
        "offset": offset,
        "volatile": False,
    }
    return OpaqueHandle(kind="mem.ref", handle_id=ref_id)


def _memory_volatile_ref(args: list) -> OpaqueHandle:
    ref_handle = _memory_ref(args)
    ref = _MEMORY_REF_REGISTRY[ref_handle.handle_id]
    ref["volatile"] = True
    return ref_handle


def _memory_store_u8(args: list) -> bool:
    ref = _memory_ref_from_handle(args[0], fn_name="std.memory.store_u8")
    value = expect_int(args[1], fn_name="std.memory.store_u8")
    if value < 0 or value > 255:
        raise RuntimeSanskriptError("std.memory.store_u8 value must be 0..255")
    block, offset, _ = _memory_ref_locate(ref, width=1, fn_name="std.memory.store_u8")
    if bool(ref.get("volatile", False)):
        raise RuntimeSanskriptError("std.memory.store_u8 requires non-volatile ref; use std.memory.volatile.store_u8")
    atomic_offsets = block.get("atomic_offsets", set())
    if isinstance(atomic_offsets, set) and offset in atomic_offsets:
        raise RuntimeSanskriptError("std.memory.store_u8 forbidden on atomic-marked location; use std.memory.atomic.*")
    _require_mutation_allowed(block, "std.memory.store_u8")
    buf = block.get("bytes")
    if not isinstance(buf, bytearray):
        raise RuntimeSanskriptError("std.memory.store_u8 invalid memory backing")
    buf[offset] = value
    return True


def _memory_load_u8(args: list) -> int:
    ref = _memory_ref_from_handle(args[0], fn_name="std.memory.load_u8")
    block, offset, _ = _memory_ref_locate(ref, width=1, fn_name="std.memory.load_u8")
    if bool(ref.get("volatile", False)):
        raise RuntimeSanskriptError("std.memory.load_u8 requires non-volatile ref; use std.memory.volatile.load_u8")
    atomic_offsets = block.get("atomic_offsets", set())
    if isinstance(atomic_offsets, set) and offset in atomic_offsets:
        raise RuntimeSanskriptError("std.memory.load_u8 forbidden on atomic-marked location; use std.memory.atomic.*")
    buf = block.get("bytes")
    if not isinstance(buf, bytearray):
        raise RuntimeSanskriptError("std.memory.load_u8 invalid memory backing")
    return int(buf[offset])


def _memory_copy(args: list) -> OpaqueHandle:
    block = _memory_block_from_handle(args[0], fn_name="std.memory.copy")
    if str(block.get("allocator")) not in {"heap", "arena"}:
        raise RuntimeSanskriptError("std.memory.copy allowed only for heap/arena blocks")
    if int(block.get("mut_borrows", 0)) > 0:
        raise RuntimeSanskriptError(
            "std.memory.copy cannot alias while mutable borrow is active"
        )
    new_handle = _memory_alloc(
        [
            int(block["size"]),
            int(block["alignment"]),
            str(block["layout"]),
            bool(block["packed"]),
            str(block["abi"]),
            str(block["region"]),
        ],
        allocator=str(block["allocator"]),
    )
    _MEMORY_REGISTRY[new_handle.handle_id]["bytes"] = bytearray(block["bytes"])
    return new_handle


def _memory_clone(args: list) -> OpaqueHandle:
    return _memory_copy(args)


def _memory_volatile_store_u8(args: list) -> bool:
    ref = _memory_ref_from_handle(args[0], fn_name="std.memory.volatile.store_u8")
    value = expect_int(args[1], fn_name="std.memory.volatile.store_u8")
    if not bool(ref.get("volatile", False)):
        raise RuntimeSanskriptError("std.memory.volatile.store_u8 requires volatile ref")
    if value < 0 or value > 255:
        raise RuntimeSanskriptError("std.memory.volatile.store_u8 value must be 0..255")
    block, offset, _ = _memory_ref_locate(ref, width=1, fn_name="std.memory.volatile.store_u8")
    atomic_offsets = block.get("atomic_offsets", set())
    if isinstance(atomic_offsets, set) and offset in atomic_offsets:
        raise RuntimeSanskriptError("std.memory.volatile.store_u8 forbidden on atomic-marked location; use std.memory.atomic.*")
    _require_mutation_allowed(block, "std.memory.volatile.store_u8")
    buf = block.get("bytes")
    if not isinstance(buf, bytearray):
        raise RuntimeSanskriptError("std.memory.volatile.store_u8 invalid memory backing")
    buf[offset] = value
    return True


def _memory_volatile_load_u8(args: list) -> int:
    ref = _memory_ref_from_handle(args[0], fn_name="std.memory.volatile.load_u8")
    if not bool(ref.get("volatile", False)):
        raise RuntimeSanskriptError("std.memory.volatile.load_u8 requires volatile ref")
    block, offset, _ = _memory_ref_locate(ref, width=1, fn_name="std.memory.volatile.load_u8")
    atomic_offsets = block.get("atomic_offsets", set())
    if isinstance(atomic_offsets, set) and offset in atomic_offsets:
        raise RuntimeSanskriptError("std.memory.volatile.load_u8 forbidden on atomic-marked location; use std.memory.atomic.*")
    buf = block.get("bytes")
    if not isinstance(buf, bytearray):
        raise RuntimeSanskriptError("std.memory.volatile.load_u8 invalid memory backing")
    return int(buf[offset])


def _memory_move(args: list) -> OpaqueHandle:
    block_handle = args[0]
    block = _memory_block_from_handle(block_handle, fn_name="std.memory.move")
    if int(block.get("shared_borrows", 0)) or int(block.get("mut_borrows", 0)):
        raise RuntimeSanskriptError("std.memory.move cannot move while borrows are active")
    new_handle_id = _next_handle_id()
    moved_block = copy.deepcopy(block)
    moved_block["moved"] = False
    _MEMORY_REGISTRY[new_handle_id] = moved_block
    block["moved"] = True
    return OpaqueHandle(kind="mem.block", handle_id=new_handle_id)


def _memory_drop(args: list) -> bool:
    block = _memory_block_from_handle(args[0], fn_name="std.memory.drop")
    if int(block.get("shared_borrows", 0)) or int(block.get("mut_borrows", 0)):
        raise RuntimeSanskriptError("std.memory.drop cannot drop while borrows are active")
    block["dropped"] = True
    block["bytes"] = bytearray()
    return True


def _memory_borrow_shared(args: list) -> OpaqueHandle:
    block_handle = args[0]
    lifetime = expect_text(args[1], fn_name="std.memory.borrow.shared")
    block = _memory_block_from_handle(block_handle, fn_name="std.memory.borrow.shared")
    if int(block.get("mut_borrows", 0)) > 0:
        raise RuntimeSanskriptError("std.memory.borrow.shared conflicts with active mutable borrow")
    borrow_id = _next_handle_id()
    block["shared_borrows"] = int(block.get("shared_borrows", 0)) + 1
    _BORROW_REGISTRY[borrow_id] = {"block": block_handle, "mutable": False, "lifetime": lifetime}
    return OpaqueHandle(kind="mem.borrow", handle_id=borrow_id)


def _memory_borrow_mut(args: list) -> OpaqueHandle:
    block_handle = args[0]
    lifetime = expect_text(args[1], fn_name="std.memory.borrow.mut")
    block = _memory_block_from_handle(block_handle, fn_name="std.memory.borrow.mut")
    shared, mutable = _borrow_state(block)
    if shared > 0 or mutable > 0:
        raise RuntimeSanskriptError("std.memory.borrow.mut requires unique aliasing (no active borrows)")
    borrow_id = _next_handle_id()
    block["mut_borrows"] = 1
    _BORROW_REGISTRY[borrow_id] = {"block": block_handle, "mutable": True, "lifetime": lifetime}
    return OpaqueHandle(kind="mem.borrow", handle_id=borrow_id)


def _memory_borrow_release(args: list) -> bool:
    borrow = _borrow_from_handle(args[0], fn_name="std.memory.borrow.release")
    block_handle = borrow["block"]
    if not isinstance(block_handle, OpaqueHandle):
        raise RuntimeSanskriptError("std.memory.borrow.release invalid block handle")
    block = _memory_block_from_handle(block_handle, fn_name="std.memory.borrow.release")
    if bool(borrow.get("mutable", False)):
        block["mut_borrows"] = 0
    else:
        block["shared_borrows"] = max(0, int(block.get("shared_borrows", 0)) - 1)
    _BORROW_REGISTRY.pop(args[0].handle_id, None)
    return True


def _memory_alias_state(args: list) -> dict:
    block = _memory_block_from_handle(args[0], fn_name="std.memory.alias.state")
    return {
        "shared_borrows": int(block.get("shared_borrows", 0)),
        "mutable_borrows": int(block.get("mut_borrows", 0)),
        "atomic_locations": len(block.get("atomic_offsets", set())),
    }


def _memory_atomic_new(args: list) -> OpaqueHandle:
    return _sync_atomic_new(args)


def _memory_atomic_ref(args: list) -> OpaqueHandle:
    ref = _memory_ref_from_handle(args[0], fn_name="std.memory.atomic.ref")
    block, offset, _ = _memory_ref_locate(ref, width=1, fn_name="std.memory.atomic.ref")
    buf = block.get("bytes")
    if not isinstance(buf, bytearray):
        raise RuntimeSanskriptError("std.memory.atomic.ref invalid memory backing")
    initial = int(buf[offset])
    atom = _sync_atomic_new([initial])
    entry = _ATOMIC_REGISTRY[atom.handle_id]
    entry["bound_ref"] = args[0]
    atomic_offsets = block.get("atomic_offsets")
    if not isinstance(atomic_offsets, set):
        atomic_offsets = set()
        block["atomic_offsets"] = atomic_offsets
    atomic_offsets.add(offset)
    return atom


def _memory_atomic_load(args: list) -> int:
    return _sync_atomic_load(args)


def _memory_atomic_store(args: list) -> bool:
    return _sync_atomic_store(args)


def _memory_atomic_fetch_add(args: list) -> int:
    return _sync_atomic_fetch_add(args)


def _memory_atomic_compare_exchange(args: list) -> ResultValue:
    return _sync_atomic_compare_exchange(args)


def _memory_atomic_fence(args: list) -> int:
    global _FENCE_COUNTER
    order = expect_text(args[0], fn_name="std.memory.atomic.fence")
    if order not in {"acquire", "release", "acq_rel", "seq_cst"}:
        raise RuntimeSanskriptError("std.memory.atomic.fence order must be acquire/release/acq_rel/seq_cst")
    _FENCE_COUNTER += 1
    return _FENCE_COUNTER


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

NATIVE_REGISTRY: dict[str, NativeSpec] = {
    # text
    "std.text.upper": NativeSpec(1, _text_upper),
    "std.text.lower": NativeSpec(1, _text_lower),
    "std.text.strip": NativeSpec(1, _text_strip),
    "std.text.split": NativeSpec(2, _text_split),
    "std.text.join": NativeSpec(2, _text_join),
    "std.text.replace": NativeSpec(3, _text_replace),
    "std.text.len": NativeSpec(1, _text_len),
    "std.text.contains": NativeSpec(2, _text_contains),
    "std.text.starts_with": NativeSpec(2, _text_starts_with),
    "std.text.ends_with": NativeSpec(2, _text_ends_with),
    # unicode
    "std.unicode.normalize": NativeSpec(2, _unicode_normalize),
    "std.unicode.codepoint_at": NativeSpec(2, _unicode_codepoint_at),
    "std.unicode.grapheme_len": NativeSpec(1, _unicode_grapheme_len),
    "std.unicode.is_ascii": NativeSpec(1, _unicode_is_ascii),
    # bytes
    "std.bytes.from_text": NativeSpec(1, _bytes_from_text),
    "std.bytes.to_text": NativeSpec(1, _bytes_to_text),
    "std.bytes.len": NativeSpec(1, _bytes_len),
    "std.bytes.concat": NativeSpec(2, _bytes_concat),
    "std.bytes.hex_encode": NativeSpec(1, _bytes_hex_encode),
    "std.bytes.hex_decode": NativeSpec(1, _bytes_hex_decode),
    # math
    "std.math.abs": NativeSpec(1, _math_abs),
    "std.math.sqrt": NativeSpec(1, _math_sqrt),
    "std.math.clamp": NativeSpec(3, _math_clamp),
    "std.math.min": NativeSpec(2, _math_min),
    "std.math.max": NativeSpec(2, _math_max),
    "std.math.floor": NativeSpec(1, _math_floor),
    "std.math.ceil": NativeSpec(1, _math_ceil),
    "std.math.round": NativeSpec(1, _math_round),
    "std.math.pow": NativeSpec(2, _math_pow),
    # stats
    "std.stats.mean": NativeSpec(1, _stats_mean),
    "std.stats.median": NativeSpec(1, _stats_median),
    "std.stats.stdev": NativeSpec(1, _stats_stdev),
    "std.stats.min": NativeSpec(1, _stats_min),
    "std.stats.max": NativeSpec(1, _stats_max),
    # random
    "std.random.random": NativeSpec(0, _random_float),
    "std.random.randint": NativeSpec(2, _random_randint),
    "std.random.choice": NativeSpec(1, _random_choice),
    "std.random.seed": NativeSpec(1, _random_seed),
    # datetime / timezone
    "std.datetime.now_iso": NativeSpec(0, _datetime_now_iso),
    "std.datetime.parse_iso": NativeSpec(1, _datetime_parse_iso),
    "std.datetime.add_seconds": NativeSpec(2, _datetime_add_seconds),
    "std.datetime.diff_seconds": NativeSpec(2, _datetime_diff_seconds),
    "std.timezone.utc_now": NativeSpec(0, _timezone_utc_now),
    "std.timezone.convert": NativeSpec(2, _timezone_convert),
    # path / file / io / stream
    "std.path.join": NativeSpec(1, _path_join),
    "std.path.basename": NativeSpec(1, _path_basename),
    "std.path.dirname": NativeSpec(1, _path_dirname),
    "std.path.exists": NativeSpec(1, _path_exists),
    "std.path.is_file": NativeSpec(1, _path_is_file),
    "std.path.is_dir": NativeSpec(1, _path_is_dir),
    "std.path.extension": NativeSpec(1, _path_extension),
    "std.path.normalize": NativeSpec(1, _path_normalize),
    "std.path.for_platform": NativeSpec(2, _path_for_platform),
    "std.path.web_normalize": NativeSpec(1, _path_web_normalize),
    "std.path.separator": NativeSpec(1, _path_separator),
    "std.file.read_text": NativeSpec(1, _file_read_text),
    "std.file.write_text": NativeSpec(2, _file_write_text),
    "std.file.read_bytes": NativeSpec(1, _file_read_bytes),
    "std.file.write_bytes": NativeSpec(2, _file_write_bytes),
    "std.file.append_text": NativeSpec(2, _file_append_text),
    "std.file.remove": NativeSpec(1, _file_remove),
    "std.file.mkdir": NativeSpec(1, _file_mkdir),
    "std.io.read_lines": NativeSpec(1, _io_read_lines),
    "std.io.read_chunks": NativeSpec(2, _io_read_chunks),
    "std.stream.read_all": NativeSpec(1, _stream_read_all),
    "std.stream.write_all": NativeSpec(2, _stream_write_all),
    "std.io.stdout_write": NativeSpec(1, _io_stdout_write),
    "std.io.stderr_write": NativeSpec(1, _io_stderr_write),
    "std.io.stdin_read_all": NativeSpec(0, _io_stdin_read_all),
    # terminal / cli / env
    "std.terminal.color": NativeSpec(2, _terminal_color),
    "std.terminal.reset": NativeSpec(0, _terminal_reset),
    "std.terminal.bold": NativeSpec(1, _terminal_bold),
    "std.terminal.cursor_up": NativeSpec(1, _terminal_cursor_up),
    "std.terminal.cursor_down": NativeSpec(1, _terminal_cursor_down),
    "std.terminal.is_tty": NativeSpec(1, _terminal_is_tty),
    "std.console.log": NativeSpec(2, _console_log),
    "std.cli.args": NativeSpec(0, _cli_args),
    "std.cli.program_name": NativeSpec(0, _cli_program_name),
    "std.cli.parse_flags": NativeSpec(1, _cli_parse_flags),
    "std.env.get": NativeSpec(1, _env_get),
    "std.env.has": NativeSpec(1, _env_has),
    "std.env.keys": NativeSpec(0, _env_keys),
    # process / pipe / signal
    "std.process.run": NativeSpec(1, _process_run),
    "std.process.run_for_platform": NativeSpec(2, _process_run_for_platform),
    "std.process.web_worker_new": NativeSpec(0, _process_web_worker_new),
    "std.process.web_post_message": NativeSpec(2, _process_web_post_message),
    "std.process.web_recv": NativeSpec(1, _process_web_recv),
    "std.pipe.run": NativeSpec(1, _pipe_run),
    "std.signal.names": NativeSpec(0, _signal_names),
    "std.signal.send": NativeSpec(2, _signal_send),
    # sync / thread markers
    "std.sync.atomic.new": NativeSpec(1, _sync_atomic_new),
    "std.sync.atomic.load": NativeSpec(1, _sync_atomic_load),
    "std.sync.atomic.store": NativeSpec(2, _sync_atomic_store),
    "std.sync.atomic.fetch_add": NativeSpec(2, _sync_atomic_fetch_add),
    "std.sync.atomic.compare_exchange": NativeSpec(3, _sync_atomic_compare_exchange),
    "std.sync.lock.new": NativeSpec(0, _sync_lock_new),
    "std.sync.lock.acquire": NativeSpec(2, _sync_lock_acquire),
    "std.sync.lock.release": NativeSpec(1, _sync_lock_release),
    "std.sync.channel.new": NativeSpec(1, _sync_channel_new),
    "std.sync.channel.send": NativeSpec(2, _sync_channel_send),
    "std.sync.channel.send_timeout": NativeSpec(3, _sync_channel_send_timeout),
    "std.sync.channel.try_send": NativeSpec(2, _sync_channel_try_send),
    "std.sync.channel.recv": NativeSpec(2, _sync_channel_recv),
    "std.sync.channel.try_recv": NativeSpec(1, _sync_channel_try_recv),
    "std.thread.marker.send": NativeSpec(1, _thread_marker_send),
    "std.thread.marker.share": NativeSpec(1, _thread_marker_share),
    # ffi / abi
    "std.ffi.call_checked": NativeSpec(2, _ffi_call_checked),
    "std.ffi.abi_stable_struct": NativeSpec(1, _ffi_abi_stable_struct),
    # net baseline
    "std.net.resolve_host": NativeSpec(1, _net_resolve_host),
    "std.net.tcp_probe": NativeSpec(3, _net_tcp_probe),
    "std.net.dns_lookup": NativeSpec(2, _net_dns_lookup),
    "std.net.tls_available": NativeSpec(0, _net_tls_available),
    "std.net.tls_probe": NativeSpec(3, _net_tls_probe),
    "std.net.browser_fetch_plan": NativeSpec(1, _net_browser_fetch_plan),
    "std.net.browser_fetch_sim": NativeSpec(1, _net_browser_fetch_sim),
    "std.watch.snapshot": NativeSpec(1, _watch_snapshot),
    "std.watch.diff": NativeSpec(2, _watch_diff),
    "std.watch.poll_once": NativeSpec(2, _watch_poll_once),
    "std.storage.web_set": NativeSpec(3, _storage_web_set),
    "std.storage.web_get": NativeSpec(2, _storage_web_get),
    "std.storage.web_remove": NativeSpec(2, _storage_web_remove),
    "std.storage.web_clear": NativeSpec(1, _storage_web_clear),
    "std.storage.web_keys": NativeSpec(1, _storage_web_keys),
    "std.platform.detect": NativeSpec(0, _platform_detect),
    "std.platform.feature": NativeSpec(1, _platform_feature),
    "std.platform.compile_plan": NativeSpec(1, _platform_compile_plan),
    # phase13 memory model
    "std.memory.alloc.heap": NativeSpec(6, _memory_alloc_heap),
    "std.memory.alloc.stack": NativeSpec(6, _memory_alloc_stack),
    "std.memory.alloc.arena": NativeSpec(6, _memory_alloc_arena),
    "std.memory.dealloc": NativeSpec(1, _memory_dealloc),
    "std.memory.layout.describe": NativeSpec(1, _memory_layout_describe),
    "std.memory.ref": NativeSpec(2, _memory_ref),
    "std.memory.volatile.ref": NativeSpec(2, _memory_volatile_ref),
    "std.memory.store_u8": NativeSpec(2, _memory_store_u8),
    "std.memory.load_u8": NativeSpec(1, _memory_load_u8),
    "std.memory.volatile.store_u8": NativeSpec(2, _memory_volatile_store_u8),
    "std.memory.volatile.load_u8": NativeSpec(1, _memory_volatile_load_u8),
    "std.memory.copy": NativeSpec(1, _memory_copy),
    "std.memory.clone": NativeSpec(1, _memory_clone),
    "std.memory.move": NativeSpec(1, _memory_move),
    "std.memory.drop": NativeSpec(1, _memory_drop),
    "std.memory.borrow.shared": NativeSpec(2, _memory_borrow_shared),
    "std.memory.borrow.mut": NativeSpec(2, _memory_borrow_mut),
    "std.memory.borrow.release": NativeSpec(1, _memory_borrow_release),
    "std.memory.alias.state": NativeSpec(1, _memory_alias_state),
    "std.memory.atomic.new": NativeSpec(1, _memory_atomic_new),
    "std.memory.atomic.ref": NativeSpec(1, _memory_atomic_ref),
    "std.memory.atomic.load": NativeSpec(1, _memory_atomic_load),
    "std.memory.atomic.store": NativeSpec(2, _memory_atomic_store),
    "std.memory.atomic.fetch_add": NativeSpec(2, _memory_atomic_fetch_add),
    "std.memory.atomic.compare_exchange": NativeSpec(3, _memory_atomic_compare_exchange),
    "std.memory.atomic.fence": NativeSpec(1, _memory_atomic_fence),
    # logging / config
    "std.log.info": NativeSpec(1, _log_info),
    "std.log.warn": NativeSpec(1, _log_warn),
    "std.log.error": NativeSpec(1, _log_error),
    "std.log.set_level": NativeSpec(1, _log_set_level),
    "std.config.load_json": NativeSpec(1, _config_load_json),
    "std.config.load_toml": NativeSpec(1, _config_load_toml),
    "std.config.load_yaml": NativeSpec(1, _config_load_yaml),
    # formats
    "std.json.parse": NativeSpec(1, _json_parse),
    "std.json.stringify": NativeSpec(1, _json_stringify),
    "std.csv.parse": NativeSpec(1, _csv_parse),
    "std.csv.stringify": NativeSpec(1, _csv_stringify),
    "std.toml.parse": NativeSpec(1, _toml_parse),
    "std.toml.stringify": NativeSpec(1, _toml_stringify),
    "std.yaml.parse": NativeSpec(1, _yaml_parse),
    "std.yaml.stringify": NativeSpec(1, _yaml_stringify),
    "std.xml.parse": NativeSpec(1, _xml_parse),
    "std.xml.stringify": NativeSpec(1, _xml_stringify),
    # binary / compression / hash / crypto / secure / encoding
    "std.binary.pack": NativeSpec(2, _binary_pack),
    "std.binary.unpack": NativeSpec(2, _binary_unpack),
    "std.compress.gzip": NativeSpec(1, _compress_gzip),
    "std.compress.gunzip": NativeSpec(1, _compress_gunzip),
    "std.compress.zlib": NativeSpec(1, _compress_zlib),
    "std.compress.unzlib": NativeSpec(1, _compress_unzlib),
    "std.hash.md5": NativeSpec(1, _hash_md5),
    "std.hash.sha256": NativeSpec(1, _hash_sha256),
    "std.crypto.sha256": NativeSpec(1, _crypto_sha256),
    "std.crypto.hmac_sha256": NativeSpec(2, _crypto_hmac_sha256),
    "std.secure.random_bytes": NativeSpec(1, _secure_random_bytes),
    "std.secure.token_hex": NativeSpec(1, _secure_token_hex),
    "std.encoding.base64_encode": NativeSpec(1, _encoding_base64_encode),
    "std.encoding.base64_decode": NativeSpec(1, _encoding_base64_decode),
    "std.encoding.url_encode": NativeSpec(1, _encoding_url_encode),
    "std.encoding.url_decode": NativeSpec(1, _encoding_url_decode),
    # regex / template / serialize / test / bench
    "std.regex.match": NativeSpec(2, _regex_match),
    "std.regex.search": NativeSpec(2, _regex_search),
    "std.regex.replace": NativeSpec(3, _regex_replace),
    "std.regex.split": NativeSpec(2, _regex_split),
    "std.template.render": NativeSpec(2, _template_render),
    "std.serialize": NativeSpec(2, _serialize),
    "std.deserialize": NativeSpec(2, _deserialize),
    "std.test.assert_eq": NativeSpec(2, _test_assert_eq),
    "std.test.assert_true": NativeSpec(1, _test_assert_true),
    "std.test.assert_false": NativeSpec(1, _test_assert_false),
    "std.bench.now_ms": NativeSpec(0, _bench_now_ms),
    "std.bench.elapsed_ms": NativeSpec(1, _bench_elapsed_ms),
    # algorithms / data structures
    "std.alg.sort": NativeSpec(2, _alg_sort),
    "std.alg.stable_sort_by": NativeSpec(3, _alg_stable_sort_by),
    "std.alg.binary_search": NativeSpec(2, _alg_binary_search),
    "std.alg.graph.bfs": NativeSpec(2, _alg_graph_bfs),
    "std.alg.graph.dfs": NativeSpec(2, _alg_graph_dfs),
    "std.alg.graph.dijkstra": NativeSpec(2, _alg_graph_dijkstra),
    "std.alg.graph.topological_sort": NativeSpec(1, _alg_graph_topological_sort),
    "std.alg.graph.schedule_passes": NativeSpec(1, _alg_graph_schedule_passes),
    "std.alg.tree.traverse": NativeSpec(2, _alg_tree_traverse),
    "std.alg.heap.push": NativeSpec(2, _alg_heap_push),
    "std.alg.heap.pop": NativeSpec(1, _alg_heap_pop),
    "std.alg.priority.schedule": NativeSpec(1, _alg_priority_schedule),
    "std.alg.dp.lcs_length": NativeSpec(2, _alg_dp_lcs_length),
    "std.alg.dp.knapsack_01": NativeSpec(2, _alg_dp_knapsack),
    "std.alg.string.kmp_search": NativeSpec(2, _alg_string_kmp_search),
    "std.alg.trie.build": NativeSpec(1, _alg_trie_build),
    "std.alg.trie.contains": NativeSpec(2, _alg_trie_contains),
    "std.alg.suffix.array": NativeSpec(1, _alg_suffix_array),
    "std.alg.interval.query": NativeSpec(2, _alg_interval_query),
    "std.alg.interval.tree_build": NativeSpec(1, _alg_interval_tree_build),
    "std.alg.interval.tree_query": NativeSpec(2, _alg_interval_tree_query),
    "std.alg.union_find.run": NativeSpec(3, _alg_union_find_run),
    "std.alg.bitset.new": NativeSpec(1, _alg_bitset_new),
    "std.alg.bitset.set": NativeSpec(3, _alg_bitset_set),
    "std.alg.bitset.test": NativeSpec(2, _alg_bitset_test),
    "std.alg.bloom.new": NativeSpec(2, _alg_bloom_new),
    "std.alg.bloom.add": NativeSpec(2, _alg_bloom_add),
    "std.alg.bloom.maybe_contains": NativeSpec(2, _alg_bloom_maybe_contains),
    "std.alg.matrix.mul": NativeSpec(2, _alg_matrix_mul),
    "std.alg.vector.dot": NativeSpec(2, _alg_vector_dot),
    "std.alg.vector.norm": NativeSpec(1, _alg_vector_norm),
    "std.alg.numeric.integrate_trapezoid": NativeSpec(1, _alg_numeric_integrate_trapezoid),
    "std.alg.opt.gradient_descent_step": NativeSpec(3, _alg_opt_gradient_descent_step),
    "std.alg.parser.seq": NativeSpec(1, _alg_parser_seq),
    "std.alg.parser.choice": NativeSpec(1, _alg_parser_choice),
    "std.alg.parser.match_text": NativeSpec(1, _alg_parser_match_text),
    "std.alg.parser.run": NativeSpec(2, _alg_parser_run),
    "std.alg.deterministic.unique": NativeSpec(1, _alg_deterministic_unique),
    # phase14
    "std.http.get": NativeSpec(1, _http_get),
    "std.http.post_json": NativeSpec(2, _http_post_json),
    "std.http.server_once": NativeSpec(3, _http_server_once),
    "std.http.server_route_once": NativeSpec(5, _http_server_route_once),
    "std.http.client_roundtrip": NativeSpec(0, _http_client_roundtrip),
    "std.data.column": NativeSpec(2, _data_column),
    "std.data.describe": NativeSpec(1, _data_describe),
    "std.plot.ascii": NativeSpec(3, _plot_ascii),
    "std.web.route_match": NativeSpec(2, _web_route_match),
    "std.web.render": NativeSpec(2, _web_render),
    "std.db.sqlite_query": NativeSpec(3, _db_sqlite_query),
    "std.db.sqlite_exec": NativeSpec(3, _db_sqlite_exec),
    "std.task.run_after_ms": NativeSpec(2, _task_run_after_ms),
    "std.task.schedule": NativeSpec(1, _task_schedule),
    # phase22
    "std.phase22.inventory": NativeSpec(0, _p22_inventory),
    "std.http.request": NativeSpec(4, _http_request),
    "std.http.response": NativeSpec(3, _http_response),
    "std.http.cookie_parse": NativeSpec(1, _http_cookie_parse),
    "std.http.cookie_header": NativeSpec(3, _http_cookie_header),
    "std.http.session_create": NativeSpec(0, _http_session_create),
    "std.http.session_get": NativeSpec(2, _http_session_get),
    "std.http.session_set": NativeSpec(3, _http_session_set),
    "std.http.auth_basic_header": NativeSpec(2, _http_auth_basic_header),
    "std.http.auth_bearer_verify": NativeSpec(2, _http_auth_bearer_verify),
    "std.http.middleware_apply": NativeSpec(2, _http_middleware_apply),
    "std.http.router_dispatch": NativeSpec(3, _http_router_dispatch),
    "std.http.client_roundtrip": NativeSpec(0, _http_client_roundtrip),
    "std.web.html_escape": NativeSpec(1, _web_html_escape),
    "std.web.html_element": NativeSpec(3, _web_html_element),
    "std.web.css_bundle": NativeSpec(1, _web_css_bundle),
    "std.web.bridge_plan": NativeSpec(0, _web_bridge_plan),
    "std.web.bridge_execute": NativeSpec(2, _web_bridge_execute),
    "std.web.webgl_plan": NativeSpec(0, _web_webgl_plan),
    "std.web.webgl_stub": NativeSpec(1, _web_webgl_stub),
    "std.web.dom_simulate": NativeSpec(3, _web_dom_simulate),
    "std.web.dom_dispatch": NativeSpec(3, _web_dom_dispatch),
    "std.web.canvas_raster": NativeSpec(3, _web_canvas_raster),
    "std.gui.capabilities_plan": NativeSpec(0, _gui_capabilities_plan),
    "std.gui.simulate": NativeSpec(1, _gui_simulate),
    "std.game.loop_run": NativeSpec(3, _game_loop_run),
    "std.game.input_state": NativeSpec(1, _game_input_state),
    "std.game.audio_plan": NativeSpec(0, _game_audio_plan),
    "std.game.audio_tick": NativeSpec(2, _game_audio_tick),
    "std.game.asset_resolve": NativeSpec(2, _game_asset_resolve),
    "std.game.sprite_atlas": NativeSpec(1, _game_sprite_atlas),
    "std.game.physics2d_step": NativeSpec(2, _game_physics2d_step),
    "std.game.scene3d_plan": NativeSpec(0, _game_scene3d_plan),
    "std.data.frame": NativeSpec(1, _data_frame),
    "std.data.csv_read": NativeSpec(1, _data_csv_read),
    "std.data.csv_write": NativeSpec(2, _data_csv_write),
    "std.data.parquet_plan": NativeSpec(0, _data_parquet_plan),
    "std.data.parquet_stub_read": NativeSpec(1, _data_parquet_stub_read),
    "std.plot.histogram_ascii": NativeSpec(3, _plot_histogram_ascii),
    "std.plot.sparkline": NativeSpec(1, _plot_sparkline),
    "std.linalg.matmul": NativeSpec(2, _linalg_matmul),
    "std.linalg.dot": NativeSpec(2, _linalg_dot),
    "std.linalg.transpose": NativeSpec(1, _linalg_transpose),
    "std.tensor.shape": NativeSpec(1, _tensor_shape),
    "std.tensor.reshape": NativeSpec(2, _tensor_reshape),
    "std.ml.ad_roadmap": NativeSpec(0, _ml_ad_roadmap),
    "std.ml.model_pack": NativeSpec(1, _ml_model_pack),
    "std.ml.model_unpack": NativeSpec(1, _ml_model_unpack),
    "std.ml.python_bridge_plan": NativeSpec(0, _ml_python_bridge_plan),
    "std.ml.native_kernels_plan": NativeSpec(0, _ml_native_kernels_plan),
    "std.db.postgres_plan": NativeSpec(0, _db_postgres_plan),
    "std.db.postgres_stub_connect": NativeSpec(1, _db_postgres_stub_connect),
    "std.db.client": NativeSpec(3, _db_client),
    "std.phase22.seal_run": NativeSpec(0, _phase22_seal_run),
    "std.notebook.split_cells": NativeSpec(1, _notebook_split_cells),
    "std.research.template_render": NativeSpec(2, _research_template_render),
    "std.env.fingerprint": NativeSpec(1, _env_fingerprint),
}

from .phase23_concurrency import PHASE23_NATIVE_REGISTRY  # noqa: E402

NATIVE_REGISTRY.update(PHASE23_NATIVE_REGISTRY)
