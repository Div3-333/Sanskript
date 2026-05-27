"""Phase 10 standard library implementations (VM-callable via std.* names)."""

from __future__ import annotations

import base64
import binascii
import csv
import gzip
import hashlib
import hmac
import io
import logging
import math
import os
import random
import re
import secrets
import signal
import struct
import subprocess
import sys
import time
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ET
import zlib
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePath
from zoneinfo import ZoneInfo

from .errors import RuntimeSanskriptError
from .phase3_values import text_grapheme_len
from .runtime_values import BytesValue, NIL
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
    return expect_number(args[0], fn_name="std.math.pow") ** expect_number(args[1], fn_name="std.math.pow")


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
    "std.cli.args": NativeSpec(0, _cli_args),
    "std.cli.program_name": NativeSpec(0, _cli_program_name),
    "std.cli.parse_flags": NativeSpec(1, _cli_parse_flags),
    "std.env.get": NativeSpec(1, _env_get),
    "std.env.has": NativeSpec(1, _env_has),
    "std.env.keys": NativeSpec(0, _env_keys),
    # process / pipe / signal
    "std.process.run": NativeSpec(1, _process_run),
    "std.pipe.run": NativeSpec(1, _pipe_run),
    "std.signal.names": NativeSpec(0, _signal_names),
    "std.signal.send": NativeSpec(2, _signal_send),
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
}
