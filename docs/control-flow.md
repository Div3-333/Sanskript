# Sanskript Control Flow Reference (Phase 5)

Complete reference for all control-flow constructs. Each section shows the
Sanskript directive, equivalent Python, and migration notes.

---

## Conditionals

### if / elif / else — `yadi` / `athavā yadi` / `anyathā`

```
yadi <condition>.
  <then-body>
athavā yadi <condition>.
  <elif-body>
anyathā.
  <else-body>
antam.
```

**Python equivalent:**
```python
if condition:
    ...
elif condition:
    ...
else:
    ...
```

---

### guard — `rakṣa`

Executes body only when condition is true (early-exit guard).

```
rakṣa <condition>.
  <body>
antam.
```

**Python equivalent:**
```python
if condition:
    ...
```

---

### match / yathā

Pattern matching on a value.

```
yathā <subject>.
  yathā <pattern>.
    <body>
  yathā kevalam.
    <wildcard-body>
antam.
```

**Python equivalent:**
```python
match subject:
    case pattern:
        ...
    case _:
        ...
```

---

## Loops

### while — `punaḥ`

```
punaḥ <condition>.
  <body>
antam.
```

**Python equivalent:** `while condition: ...`

---

### until — `yāvat`

Loop **until** condition becomes true (opposite of while).

```
yāvat <condition>.
  <body>
antam.
```

**Python equivalent:** `while not condition: ...`

---

### counted-for — `saṅkhyā`

```
saṅkhyā <counter> <start> <end>.
  <body>
antam.
```

**Python equivalent:** `for counter in range(start, end): ...`

---

### foreach — `pratyekam`

```
pratyekam <item> samūhe <container>.
  <body>
antam.
```

**Python equivalent:** `for item in container: ...`

#### Destructuring foreach

Iterate a list of tuples and bind elements to names:

```
pratyekam (k v) <container>.
  <body>
antam.
```

**Python equivalent:** `for k, v in container: ...`

---

### infinite loop — `anavaratam`

```
anavaratam.
  <body>
antam.
```

**Python equivalent:** `while True: ...`

---

### break / continue

```
viramaḥ.         // break
agragamanam.     // continue
```

Labeled break/continue: `viramaḥ <label>.`

---

## Exception Handling

### throw (catchable) — `vikṣepaḥ`

Raises a catchable error.

```
vikṣepaḥ vākyam message iti.
```

**Python equivalent:** `raise RuntimeError("message")`

---

### try-catch — `āgrahītvā`

```
āgrahītvā <error-name>.
  <try-body>
anyathā.
  <handler-body>
antam.
```

**Python equivalent:**
```python
try:
    ...
except RuntimeError as error_name:
    ...
```

**Migration note:** Only `vikṣepaḥ` (ThrownError) is catchable.
`vipattim` (PanicError) cannot be caught. Bytecode opcodes `throw`, `panic`, `try_begin`, and `try_end` round-trip through yantra-pāṭha as `vikṣepaḥ kriyate.`, `vipattim kriyate.`, `āgrahītvā <ip> iti lakṣyaṃ ārabhyate.`, and `āgrahītvaḥ samāpyate.`

---

### panic (unrecoverable) — `vipattim`

```
vipattim vākyam fatal message iti.
```

**Python equivalent:** `raise SystemExit("fatal message")` or `assert False`

---

## Contracts

### Precondition — `pūrvaśartam`

Checked at the point of declaration (typically at function entry).

```
pūrvaśartam <condition>.
```

**Python equivalent:** `assert condition, "precondition failed"`

Panics with `PanicError("precondition failed")` when violated.

---

### Postcondition — `uttaraśartam`

Checked after computation, before returning.

```
uttaraśartam <condition>.
```

**Python equivalent:** `assert condition, "postcondition failed"`

---

### Invariant — `nityaśartam`

Checked at the point of declaration.

```
nityaśartam <condition>.
```

**Python equivalent:** `assert condition, "invariant failed"`

---

## Destructuring

### Destructuring in function parameters

Declare a function that accepts a tuple and binds its elements:

```
vidhānam f (a b).
  ...
samāpanam.
```

The tuple argument passed to `f` is unpacked: `a = arg[0]`, `b = arg[1]`.

**Python equivalent:**
```python
def f(arg):
    a, b = arg
    ...
```

### Destructuring in foreach loops

```
pratyekam (k v) samūhe pairs.
  <body>
antam.
```

**Python equivalent:** `for k, v in pairs: ...`

---

## Assertion — `niścayaḥ`

```
niścayaḥ <condition>.
```

---

## Defer — `ante`

```
ante.
  <body>
antam.
```

Deferred body runs at the end of the enclosing scope (currently inline).

**Python equivalent:** `try/finally` or context managers.

---

## Error hierarchy

```
SanskriptError
├── ThrownError      (vikṣepaḥ — catchable by āgrahītvā)
├── PanicError       (vipattim — unrecoverable, kills program)
└── RuntimeSanskriptError  (VM errors)
```

---

## Diagnostics Coherence Guarantees

- Parser diagnostics for malformed Phase 5 directives (`prasāraḥ`, `vikṣepaḥ`,
  `vipattim`, `āgrahītvā`, `pūrvaśartam`, `uttaraśartam`, `nityaśartam`) now
  fail with explicit `ParseError` messages and attached source spans.
- Parse-time semantic errors raised during sentence analysis are normalized to
  include sentence span + original-script context when missing.
- VM now traps host-side type mismatches in opcode handlers and re-raises them
  as `RuntimeSanskriptError` with stack trace and diagnostic notes, so no host
  `TypeError` bypass leaks through Phase 5 execution paths.
- Contract failures (`pūrvaśartam`, `uttaraśartam`, `nityaśartam`) continue to
  lower to `panic` and carry runtime stack traces/notes.

### Negative matrix (must fail)

- Missing operand: `prasāraḥ.`, `vikṣepaḥ.`, `vipattim.`
- Missing condition: `pūrvaśartam.`, `uttaraśartam.`, `nityaśartam.`
- Invalid try header: `āgrahītvā.`
- Illegal propagation context: `prasāraḥ <value>.` outside function
- Runtime type misuse on result opcodes: `result_unwrap_ok` with non-result
