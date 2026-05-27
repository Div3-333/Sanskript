# Phase 10 Standard Library Core

Native stdlib functions are registered in `src/sanskript/stdlib_impl.py` and dispatched by the VM through `CALL` with dotted names such as `std.json.parse`. Each namespace below has unit tests (positive and negative) in `tests/test_phase10_stdlib_core.py` and VM integration coverage where stack values are involved.

## Runtime integration

1. Compiler or hand-written bytecode emits `call <name>` with the exact registry name.
2. `SanskriptVM` checks `has_native_function(name)`, pops `native_arity(name)` arguments, and pushes the return value.
3. Errors surface as `RuntimeSanskriptError` with the function name in the message.

## Namespaces and entry points

### `std.text`

- `std.text.upper`, `lower`, `strip`, `split`, `join`, `replace`, `len`, `contains`, `starts_with`, `ends_with`

### `std.unicode`

- `std.unicode.normalize(text, form)` — NFC, NFD, NFKC, NFKD
- `std.unicode.codepoint_at`, `grapheme_len`, `is_ascii`

### `std.bytes`

- `std.bytes.from_text`, `to_text`, `len`, `concat`, `hex_encode`, `hex_decode`

### `std.math`

- `std.math.abs`, `sqrt`, `clamp`, `min`, `max`, `floor`, `ceil`, `round`, `pow`

### `std.stats`

- `std.stats.mean`, `median`, `stdev`, `min`, `max` (non-empty number lists)

### `std.random`

- `std.random.random`, `randint`, `choice`, `seed`

### `std.datetime` / `std.timezone`

- `std.datetime.now_iso`, `parse_iso`, `add_seconds`, `diff_seconds`
- `std.timezone.utc_now`, `convert`

### `std.path` / `std.file` / `std.io` / `std.stream`

- Path: `join`, `basename`, `dirname`, `exists`, `is_file`, `is_dir`, `extension`, `normalize`
- File: `read_text`, `write_text`, `read_bytes`, `write_bytes`, `append_text`, `remove`, `mkdir`
- Buffered I/O: `std.io.read_lines`, `read_chunks`
- Streams: `std.stream.read_all`, `write_all` (path-based)
- Standard handles: `std.io.stdout_write`, `stderr_write`, `stdin_read_all`

### `std.terminal` / `std.cli` / `std.env`

- Terminal ANSI: `color`, `reset`, `bold`, `cursor_up`, `cursor_down`
- CLI: `args`, `program_name`, `parse_flags`
- Environment: `get`, `has`, `keys`

### `std.process` / `std.pipe` / `std.signal`

- `std.process.run(command_list)` → map `{exit, stdout, stderr}`
- `std.pipe.run` — same capture semantics
- `std.signal.names`, `send` (POSIX-oriented; may fail on unsupported platforms)

### `std.log` / `std.config`

- `std.log.info`, `warn`, `error`, `set_level`
- `std.config.load_json`, `load_toml`, `load_yaml` from text blobs

### Data formats

- `std.json.parse`, `stringify`
- `std.csv.parse`, `stringify`
- `std.toml.parse`, `stringify`
- `std.yaml.parse`, `stringify` (structured subset parser)
- `std.xml.parse`, `stringify` (element tree ↔ map)

### Binary, compression, hashing, crypto, secure, encoding

- `std.binary.pack`, `unpack` (Python `struct` format strings)
- `std.compress.gzip`, `gunzip`, `zlib`, `unzlib`
- `std.hash.md5`, `sha256`
- `std.crypto.sha256`, `hmac_sha256`
- `std.secure.random_bytes`, `token_hex`
- `std.encoding.base64_encode`, `base64_decode`, `url_encode`, `url_decode`

### `std.regex` / `std.template` / serialize

- `std.regex.match`, `search`, `replace`, `split`
- `std.template.render(template, variables_map)` — `{{name}}` placeholders
- `std.serialize(format, value)` / `std.deserialize(format, text)` — `json`, `yaml`, `toml`

### `std.test` / `std.bench`

- `std.test.assert_eq`, `assert_true`, `assert_false`
- `std.bench.now_ms`, `elapsed_ms`

## Example (bytecode)

See `examples/phase10-stdlib-vm.py` and `examples/phase10-stdlib-suite.py`.

```text
push_text '{"score":9}'
call std.json.parse
push_text "score"
map_get
emit
```

Expected emitted value: `9`.

## Migration notes (Python / Rust helpers)

| Host concept | Sanskript stdlib |
|--------------|------------------|
| `str.upper` / `strip` | `std.text.*` |
| `unicodedata.normalize` | `std.unicode.normalize` |
| `bytes` / `bytearray` | `std.bytes.*` + Phase 3 `BytesValue` |
| `math.*`, `statistics.*` | `std.math.*`, `std.stats.*` |
| `random.*` | `std.random.*` |
| `datetime`, `zoneinfo` | `std.datetime.*`, `std.timezone.*` |
| `pathlib.Path` | `std.path.*`, `std.file.*` |
| `open`, `read`, `write` | `std.file.*`, `std.io.read_lines` |
| `sys.stdin/out/err` | `std.io.stdout_write`, etc. |
| `colorama` / ANSI | `std.terminal.*` |
| `sys.argv`, `argparse` | `std.cli.*` |
| `os.environ` | `std.env.*` |
| `subprocess.run` | `std.process.run`, `std.pipe.run` |
| `signal` module | `std.signal.*` |
| `logging` | `std.log.*` |
| `json`, `csv`, `tomllib`, YAML, XML | `std.json`, `std.csv`, `std.toml`, `std.yaml`, `std.xml` |
| `struct`, `gzip`, `zlib` | `std.binary.*`, `std.compress.*` |
| `hashlib`, `hmac`, `secrets` | `std.hash.*`, `std.crypto.*`, `std.secure.*` |
| `base64`, `urllib.parse` | `std.encoding.*` |
| `re` | `std.regex.*` |
| `string.Template` / format | `std.template.render` |
| `pickle` / serde | `std.serialize` / `std.deserialize` (JSON/YAML/TOML) |
| `unittest` assertions | `std.test.*` |
| `time.perf_counter` | `std.bench.*` |

Source-level `CALL std.*` from Sanskrit prose is planned; today programs use bytecode `call` or the Python driver examples until the compiler surface wires dotted std names.

## Limitations (explicit)

- YAML/TOML parsers cover common config shapes, not full spec compliance.
- `std.io.stdin_read_all` blocks when stdin is blocking.
- `std.signal.send` requires OS support; tests skip sending real signals.
- File/process APIs use the host Python runtime (bootstrap path) until the VM is self-hosted.
