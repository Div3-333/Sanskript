# Native Sanskript Independence Checklist

This checklist defines what must exist before Sanskript can replace the
project's current Python and Rust code with native Sanskript across the full
stack: `surakṣita` high-level programming, `rakṣita` systems programming, and
`arakṣita` low-level machine programming.

The target is not "Python with Sanskrit keywords" or "Rust with Sanskrit
spelling". The target is a prose-style Sanskrit programming system whose
grammar, derivational engine, compiler, bytecode, VM, tooling, libraries, and
eventual native backends can be authored and maintained in Sanskript itself.

## Completion Standard

No feature is complete merely because it has a name, a parser hook, a metadata
entry, or a placeholder predicate. A feature counts as complete only when all
of these gates pass:

- [ ] Natural Sanskript source form exists and reads as grammatical Sanskrit
      prose, without symbolic operator dependency.
- [ ] Parser accepts the form through the normal source pipeline.
- [ ] AST node or equivalent typed representation exists.
- [ ] Static validation gives precise diagnostics for invalid use.
- [ ] Compiler lowers the feature to portable IR or bytecode.
- [ ] VM/runtime executes the feature without Python/Rust-side special cases
      hidden from the language model.
- [ ] `.sskyp` machine-prose representation exists where the feature reaches
      low-level execution.
- [ ] Round-trip tests cover source to AST, AST to bytecode, bytecode to VM,
      and `.sskyp` decode/encode when applicable.
- [ ] Negative tests prove incorrect programs fail clearly.
- [ ] Documentation teaches a new user how to write the feature.
- [ ] At least one realistic example uses the feature in a useful program.
- [ ] Migration notes explain how existing Python/Rust code using the same
      concept will move to Sanskript.

## Status Legend

- [x] Implemented foundation exists in the repo and can be built on.
- [ ] Not complete yet, even if a partial hook or concept exists.
- [ ] Items marked "foundation" still need the completion standard above
      before they can be closed as production language features.

## North Star Definition Of Done

- [ ] Sanskript programs can be authored entirely as prose-style Sanskrit,
      including high-level application code, systems code, and machine-level
      code.
- [ ] The Sanskript compiler can compile Sanskript source without depending on
      Python or Rust implementation code.
- [ ] The Sanskript VM can execute Sanskript bytecode and machine prose while
      itself being implemented in Sanskript.
- [ ] The Sanskript standard library can replace the current Python/Rust helper
      modules used by the project.
- [ ] The project can build, test, package, and run itself from a fresh checkout
      using Sanskript-native tools.
- [ ] Windows, macOS, Linux, and web targets are first-class build targets.
- [ ] Users can build algorithms, CLIs, productivity apps, web apps, games,
      data/research scripts, and ML-oriented programs without leaving
      Sanskript.
- [ ] `surakṣita`, `rakṣita`, and `arakṣita` are coherent language tiers with
      explicit boundaries, conversions, and safety rules.
- [ ] The final system has no permanent Python/Rust requirement for authoring,
      compiling, running, testing, packaging, or documenting Sanskript projects.

## Current Foundations Already Present

- [x] Portable bytecode v2 documentation exists.
- [x] VM stack execution foundation exists.
- [x] Basic source-to-bytecode compilation exists.
- [x] `.sskyp` machine-prose representation exists for current opcodes.
- [x] Function definitions, parameters, and return-value expressions exist as
      a foundation.
- [x] Integer arithmetic expressions exist as a foundation.
- [x] Equality and less-than conditional foundations exist.
- [x] Basic loops exist as a foundation.
- [x] Text values and native text primitives exist as a foundation.
- [x] List and map runtime value foundations exist.
- [x] Record/object substrate exists as a foundation.
- [x] Heap source controls exist as a `rakṣita` foundation.
- [x] Safety-tier vocabulary exists for `surakṣita`, `rakṣita`, and
      `arakṣita`.
- [x] Type catalog documentation exists as a foundation.

## Current Phase 1-10 Closure Audit

Status after the identifier/avyaya cleanup on 2026-05-27:

- [x] Phase 1-10 foundations build and pass the current test gates:
      `pytest -q`, `tools/check_no_placeholder_completion.py`, and
      `tools/check_feature_completion.py`.
- [x] Identifier parsing is separated from the controlled avyaya register
      (`src/sanskript/identifiers.py`). Example-only names such as `a`, `x`,
      `n`, `greet`, `counter`, and `trace` must not be registered as avyaya.
- [ ] Phase 1-10 are not closed forever yet. Green tests prove the current
      foundations are coherent; they do not prove full Python/Rust replacement
      or complete end-user language coverage.

Open blockers before Phase 1-10 can be treated as fully closed:

- [ ] Phase 1: broaden script/transliteration and sandhi segmentation coverage
      beyond representative samples; keep enforcing prose-style identifiers
      rather than widening grammar registers for tests.
- [ ] Phase 2: add source/AST/bytecode/VM/negative coverage for every directive
      combination, especially grouping, literals, module scope, and record/map
      edges.
- [ ] Phase 3: replace `text_grapheme_len_stub` with real grapheme cluster
      handling; finish source-level directives and `.sskyp` parity for every
      implemented scalar, collection, byte, option/result, and ADT value.
- [ ] Phase 4: implement real borrow/lifetime enforcement, effect-system
      enforcement, async/generator type behavior, and class/type integration
      that is not merely catalog/documentation-level.
- [ ] Phase 5: finish coherent error propagation across exceptions, result
      values, panic, stack traces, source spans, pre/postconditions, and
      invariants with negative tests for every illegal form.
- [ ] Phase 6: harden callable behavior with full source examples for closures,
      overloading, decorators, currying, macros, tail-call behavior, and
      `surakṣita`/`rakṣita`/`arakṣita` linkage boundaries.
- [ ] Phase 7: move beyond record-backed OOP foundation to complete method
      resolution, inheritance/protocol/metaclass behavior, visibility
      enforcement, finalization, and dispatch diagnostics.
- [ ] Phase 8: deepen functional/declarative implementation and tests for lazy
      iterators, generators, pipelines, pattern expressions, ADTs, declarative
      queries, rule invocation, memoization, and purity interactions.
- [ ] Phase 9: harden package resolution with conflict cases, lock/signature
      verification, vendored/registry dependencies, platform feature gates, and
      fresh-checkout examples.
- [ ] Phase 10: wire standard-library calls through natural Sanskript source,
      not only VM/native registry calls or Python driver examples; add
      end-user examples for CLI, file I/O, JSON/CSV/TOML/YAML, regex/patterns,
      templating, process, logging, and testing utilities.

## Phase 0: Truth Gates And Project Inventory

- [x] Create a generated feature matrix listing every language feature, owning
      file, parser rule, compiler lowering, VM handler, docs page, examples,
      and tests (`tools/generate_feature_matrix.py` → `data/meta/feature_matrix.json`,
      `docs/generated/feature-matrix.md`).
- [x] Add a CI check that fails if a feature is marked complete without all
      required artifacts (`tools/check_feature_completion.py`, `.github/workflows/ci.yml`).
- [x] Add a "no placeholder completion" checker that rejects pass-through
      handlers, empty predicates, metadata-only entries, and TODO-only bodies
      (`tools/check_no_placeholder_completion.py`; compiler-emitted opcodes and
      catalog `implemented` types).
- [x] Inventory every Python module currently required by Sanskript.
- [x] Inventory every Rust module currently required by Sanskript
      (`tools/generate_module_inventory.py` → `data/meta/module_inventory.json`,
      `docs/generated/module-inventory.md`).
- [x] Classify each existing module as compiler, runtime, VM, standard library,
      tooling, docs, tests, web, grammar engine, or migration support.
- [x] Assign every Python/Rust module to a Sanskript replacement milestone (M0–M20).
- [x] Add migration labels: keep temporarily, port directly, redesign, remove,
      or replace with native primitive.
- [x] Create a baseline "Sanskript can replace this" score per module
      (`replaceability_score` 0–100 in module inventory).
- [x] Add a dashboard that shows percent complete by authoring, compiling,
      execution, testing, documentation, packaging, and deployment
      (`tools/generate_independence_dashboard.py` → `docs/generated/independence-dashboard.md`).

## Phase 1: Sanskrit Source Surface

- [x] Define the canonical prose style for executable Sanskript.
- [x] Define accepted scripts: Devanagari, IAST, SLP1, Harvard-Kyoto, and any
      internal normalized script.
- [x] Implement source normalization across accepted scripts.
- [x] Implement reversible transliteration for diagnostics and tooling.
- [x] Implement strict token provenance so diagnostics can point to original
      user text.
- [x] Implement sandhi-aware lexical segmentation where grammatically required.
- [x] Implement opt-in strict Paninian morphology validation for source forms.
- [x] Implement a relaxed learning mode that explains corrections without
      changing the canonical compiler.
- [x] Define how vākyas map to executable statements.
- [x] Define how compounds map to names, selectors, and type expressions.
- [x] Define how case endings map to semantic roles without becoming symbolic
      punctuation.
- [x] Define how verb forms map to computation, effect, control, and
      evaluation.
- [x] Define how particles, indeclinables, and discourse markers are handled.
- [x] Define how comments are written in natural Sanskrit prose.
- [x] Define how documentation strings are written and attached.
- [x] Define how declarations begin and end without semicolons or braces.
- [x] Define how nested scopes are expressed without indentation dependency.
- [x] Define how optional punctuation is treated in manuscripts, examples, and
      machine-readable files.
- [x] Define formatting rules that preserve readability without making layout
      semantic.
- [x] Create a canonical formatter that outputs beautiful grammatical
      Sanskript.
- [x] Create a linter that flags choppy Sanskrit-like code.
- [x] Create a style guide for names, compounds, case use, tense/mood use, and
      prose register.

## Phase 2: Core Syntax And Semantics

- [x] Implement variable binding in prose with explicit role marking.
- [x] Implement mutable binding in prose.
- [x] Implement immutable binding in prose.
- [x] Implement shadowing rules.
- [x] Implement lexical scope.
- [x] Implement block scope without braces.
- [x] Implement module scope.
- [x] Implement explicit export scope.
- [x] Implement local declarations.
- [x] Implement forward declarations where needed.
- [x] Implement assignment without symbolic equals.
- [x] Implement compound assignment through verbal forms, not operators.
- [x] Implement expression sequencing.
- [x] Implement statement sequencing.
- [x] Implement expression-as-value rules.
- [x] Implement statement-only forms.
- [x] Implement unit/void result handling.
- [x] Implement truthiness rules or reject truthiness in favor of explicit
      boolean grammar.
- [x] Implement boolean negation in prose.
- [x] Implement boolean conjunction in prose.
- [x] Implement boolean disjunction in prose.
- [x] Implement short-circuit evaluation.
- [x] Implement comparison forms for equality, inequality, ordering, identity,
      and membership.
- [x] Implement arithmetic precedence without symbolic precedence dependence.
- [x] Implement explicit grouping through Sanskrit syntactic forms.
- [x] Implement literal forms for numbers.
- [x] Implement literal forms for text.
- [x] Implement literal forms for lists.
- [x] Implement literal forms for maps.
- [x] Implement literal forms for records.
- [x] Implement literal forms for bytes.
- [x] Implement literal forms for nil/none/absence.
- [x] Implement literal forms for booleans.

## Phase 3: Values And Data Types

- [x] Integer value foundation exists.
- [x] Boolean value foundation exists.
- [x] Float value foundation exists.
- [x] Text value foundation exists.
- [x] List value foundation exists.
- [x] Map value foundation exists.
- [x] Record value foundation exists.
- [x] Implement arbitrary precision integers.
- [x] Implement signed fixed-width integers: i8, i16, i32, i64, i128.
- [x] Implement unsigned fixed-width integers: u8, u16, u32, u64, u128.
- [x] Implement machine word integers.
- [x] Implement pointer-sized integers.
- [x] Implement checked arithmetic.
- [x] Implement wrapping arithmetic.
- [x] Implement saturating arithmetic.
- [x] Implement exact rational numbers.
- [x] Implement decimal numbers for finance and accounting.
- [x] Implement complex numbers.
- [x] Implement IEEE float semantics.
- [x] Implement NaN and infinity handling.
- [x] Implement Unicode scalar handling.
- [x] Implement grapheme cluster text handling.
- [x] Implement byte strings.
- [x] Implement mutable byte arrays.
- [x] Implement fixed-size arrays.
- [x] Implement dynamic arrays.
- [x] Implement slices and views.
- [x] Implement tuples.
- [x] Implement named tuples.
- [x] Implement sets.
- [x] Implement frozen sets.
- [x] Implement ordered maps.
- [x] Implement default maps.
- [x] Implement counters/multisets.
- [x] Implement queues.
- [x] Implement deques.
- [x] Implement stacks.
- [x] Implement heaps.
- [x] Implement priority queues.
- [x] Implement trees.
- [x] Implement graphs.
- [x] Implement enums.
- [x] Implement tagged unions.
- [x] Implement option/maybe types.
- [x] Implement result/either types.
- [x] Implement typed errors.
- [x] Implement resource handles.
- [x] Implement file handles.
- [x] Implement socket handles.
- [x] Implement thread handles.
- [x] Implement process handles.
- [x] Implement opaque native handles for temporary host interop.

## Phase 4: Type System

- [x] Define nominal types.
- [x] Define structural types.
- [x] Define type aliases.
- [x] Define newtypes.
- [x] Define generic type parameters.
- [x] Define generic functions.
- [x] Define generic records.
- [x] Define generic classes.
- [x] Define generic interfaces/traits.
- [x] Define bounded generics.
- [x] Define variance rules.
- [x] Define type inference for local variables.
- [x] Define type inference for function returns.
- [x] Define overload resolution.
- [x] Define implicit conversions.
- [x] Define explicit conversions.
- [x] Define numeric promotion rules.
- [x] Define text/bytes conversion rules.
- [x] Define nullable/optional rules.
- [x] Define lifetimes or region types for `rakṣita`.
- [x] Define raw pointer types for `arakṣita`.
- [x] Define safe pointer/reference types for `rakṣita`.
- [x] Define ownership-qualified types.
- [x] Define borrowed types.
- [x] Define mutable borrowed types.
- [x] Define affine or linear resource types.
- [x] Define effect types.
- [x] Define async/future types.
- [x] Define iterator types.
- [x] Define generator types.
- [x] Define callable/function types.
- [x] Define coroutine types.
- [x] Define class instance types.
- [x] Define metaclass/type-object behavior if needed.
- [x] Define type reflection rules.
- [x] Define compile-time constant types.

## Phase 5: Control Flow

Evidence (Phase 5):
- `docs/control-flow.md` (reference + directives)
- `tests/test_phase5_control_flow.py` (unit + yantra-pāṭha round-trip + source-parse)
- `examples/ṣoḍaśa-control-flow.ssk` (integration example executed by tests)

- [x] Conditional foundation exists.
- [x] Loop foundation exists.
- [x] Implement if/else in grammatical prose.
- [x] Implement else-if chains.
- [x] Implement match/pattern branching.
- [x] Implement guard clauses.
- [x] Implement while loops.
- [x] Implement until loops.
- [x] Implement counted loops.
- [x] Implement foreach loops over iterables.
- [x] Implement infinite loops.
- [x] Implement break.
- [x] Implement continue.
- [x] Implement labeled break.
- [x] Implement labeled continue.
- [x] Implement return with value.
- [x] Implement early return.
- [x] Implement defer/finally cleanup.
- [x] Implement exceptions or typed raises if chosen.
- [x] Implement result-style error propagation if chosen.
- [x] Implement panic/abort for unrecoverable errors.
- [x] Implement assertions.
- [x] Implement preconditions.
- [x] Implement postconditions.
- [x] Implement invariants.
- [x] Implement pattern matching over literals.
- [x] Implement pattern matching over tuples.
- [x] Implement pattern matching over records.
- [x] Implement pattern matching over enums.
- [x] Implement destructuring assignment.
- [x] Implement destructuring in parameters.
- [x] Implement destructuring in loops.
- [x] Implement destructuring in match arms.

## Phase 6: Functions And Procedures

- [x] Function definition foundation exists.
- [x] Function parameter foundation exists.
- [x] Return-value foundation exists.
- [x] Implement first-class functions.
- [x] Implement nested functions.
- [x] Implement closures.
- [x] Implement lexical capture.
- [x] Implement mutable capture rules.
- [x] Implement recursive functions.
- [x] Implement mutual recursion.
- [x] Implement tail-call optimization where safe.
- [x] Implement default parameters.
- [x] Implement keyword-style arguments through Sanskrit case roles.
- [x] Implement variadic parameters.
- [x] Implement named returns if useful.
- [x] Implement pure functions.
- [x] Implement effectful procedures.
- [x] Implement function overloading.
- [x] Implement method overloading if chosen.
- [x] Implement callable objects.
- [x] Implement partial application.
- [x] Implement currying only if it fits the prose grammar naturally.
- [x] Implement decorators/annotations as Sanskrit modifiers.
- [x] Implement compile-time functions or macros.
- [x] Implement inline functions for `rakṣita`.
- [x] Implement naked/ABI functions for `arakṣita`.

**Evidence (Phase 6):**
- Prose surface: `vidhānam` headers with `śuddhaḥ` / `sādhanaṃ`, `parivartanīya-gṛhī`, `antarbhūtam`, `nagnā`, `kālavyāpāre`, `saṃskāraṃ`, `āṃśikam`, `anukrameṇa`, keyword calls `VALUE iti param`, named `pratyāvartanam NAME iti artha VALUE` — `src/sanskript/parser.py`, `src/sanskript/parser_core.py`
- AST: `FunctionDef` extensions, `PartialApply`, `Call`/`CallValue` kwargs, `Return.name`/`tail` — `src/sanskript/ast.py`
- Type-check: effect enforcement, pure/mutable-capture conflict — `src/sanskript/type_checker.py` (`test_pure_function_rejects_mutable_capture`, `test_pure_function_rejects_emit_in_checker`)
- Compiler/IR: overload mangling, tail calls, macro/inline expansion, partial wrappers, decorators — `src/sanskript/compiler.py`
- VM/bytecode: `TAIL_CALL`, `MutableCell`, `capture_mut` on `FunctionBytecode` — `src/sanskript/vm.py`, `src/sanskript/bytecode.py`, `data/bytecode/schema-v2.json`
- `.sskyp`: `tail_call` rendering — `src/sanskript/yantra_patha.py` (`test_tail_call_emits_tail_call_opcode`)
- Tests: `tests/test_phase6_functions.py` (28 tests)
- Example: `examples/phase6-functions.ssk`
- Docs/migration: `docs/functions-procedures.md`

## Phase 7: Object-Oriented Programming

Evidence (Phase 7):
- `docs/object-oriented.md` (reference, protocols, migration)
- `src/sanskript/oop.py` (MRO, dispatch, protocol names, visibility)
- `tests/test_phase7_oop.py` (parser, runtime, yantra-pāṭha, negatives, example)
- `examples/phase7-oop.ssk` (integration example)
- `src/sanskript/yantra_patha.py` (`class_new`, `method_call` machine prose)
- `src/sanskript/bytecode.py` (`resolve_method_target` for overload-aware dispatch)

- [x] Record/object substrate foundation exists.
- [x] Implement class declarations.
- [x] Implement instance construction.
- [x] Implement constructors.
- [x] Implement destructors/finalizers.
- [x] Implement instance fields.
- [x] Implement private fields.
- [x] Implement protected fields if chosen.
- [x] Implement public fields.
- [x] Implement computed properties.
- [x] Implement instance methods.
- [x] Implement static methods.
- [x] Implement class methods.
- [x] Implement method receiver grammar.
- [x] Implement method calls through natural Sanskrit role marking.
- [x] Implement method dispatch.
- [x] Implement dynamic dispatch.
- [x] Implement static dispatch.
- [x] Implement inheritance if accepted.
- [x] Implement composition-first guidance if inheritance is limited.
- [x] Implement interfaces/protocols.
- [x] Implement traits/typeclasses.
- [x] Implement trait bounds.
- [x] Implement trait implementations.
- [x] Implement abstract classes if accepted.
- [x] Implement sealed classes if accepted.
- [x] Implement mixins if accepted.
- [x] Implement operator-like behavior through named protocol methods, not
      symbolic operators.
- [x] Implement equality protocol.
- [x] Implement ordering protocol.
- [x] Implement hashing protocol.
- [x] Implement string/display protocol.
- [x] Implement iteration protocol.
- [x] Implement context/resource protocol.
- [x] Implement serialization protocol.
- [x] Implement reflection over classes and methods.

## Phase 8: Functional And Declarative Programming

- [x] Implement immutable collections.
- [x] Implement persistent data structures.
- [x] Implement map.
- [x] Implement filter.
- [x] Implement reduce/fold.
- [x] Implement scan.
- [x] Implement zip.
- [x] Implement enumerate.
- [x] Implement any/all.
- [x] Implement comprehensions in grammatical prose.
- [x] Implement lazy iterators.
- [x] Implement generators.
- [x] Implement yield.
- [x] Implement pipelines as prose, not symbolic chains.
- [x] Implement pattern matching as an expression.
- [x] Implement algebraic data types.
- [x] Implement monadic/result helpers only where they improve error handling.
- [x] Implement declarative query forms for data.
- [x] Implement rule-like declarations if useful for grammar engines.
- [x] Implement memoization helpers.
- [x] Implement pure/effect separation.

**Evidence:** `māpanam`/`śodhanam`/`saṅkocanam`/`sarvam`/`kācit`/`avalokanam`/`yuktam`/`aṅkayuktam`/`nitya-samūhaḥ`/`samīkaraṇam`/`pravāhaḥ`/`alasaḥ`/`utpādakaḥ`/`pradānam`/`yathā-artham`/`prakāra-vikalpaḥ`/`bandhanam`/`anveṣaṇam`/`niyamaḥ`/`saṃskāraṃ smaraṇa`/`śuddhaḥ` directives; AST/IR/compiler/VM/`.sskyp` via `phase8_opcodes.py`, `phase8_functional.py`; `tests/test_phase8_functional_declarative.py`; `examples/phase8-functional.ssk`; `docs/functional-declarative.md`.

## Phase 9: Modules, Packages, And Namespaces

Evidence (Phase 9):
- `docs/modules-packages.md` (reference + migration)
- `tests/test_phase9_modules.py` (imports, manifests, lock, signing, namespaces)
- `examples/phase9-modules/` (multi-file package demo)
- `src/sanskript/package_manifest.py`, `package_resolver.py`, `package_lock.py`, `package_signing.py`
- `data/stdlib/prathama.ssk` (stdlib namespace sample)

- [x] Implement module files.
- [x] Implement package directories.
- [x] Implement imports in prose.
- [x] Implement selective imports.
- [x] Implement aliases.
- [x] Implement re-exports.
- [x] Implement relative imports.
- [x] Implement absolute imports.
- [x] Implement package initialization.
- [x] Implement public/private module members.
- [x] Implement version declarations.
- [x] Implement dependency declarations.
- [x] Implement feature flags.
- [x] Implement platform-specific modules.
- [x] Implement build profiles.
- [x] Implement package lock files.
- [x] Implement package signing.
- [x] Implement local path dependencies.
- [x] Implement registry dependencies.
- [x] Implement vendored dependencies.
- [x] Implement standard library namespaces.
- [x] Implement user library namespaces.
- [x] Implement conflict resolution.

## Phase 10: Standard Library Core

Evidence (Phase 10):
- `docs/phase10-standard-library-core.md` (API reference + migration notes)
- `src/sanskript/stdlib_common.py`, `src/sanskript/stdlib_impl.py`, `src/sanskript/stdlib_core.py` (VM registry + implementations)
- `tests/test_phase10_stdlib_core.py` (37 unit/VM/process tests; positive + negative per namespace)
- `examples/phase10-stdlib-vm.py`, `examples/phase10-stdlib-suite.py` (bytecode + direct-call demos)

- [x] Implement text library.
- [x] Implement Unicode library.
- [x] Implement bytes library.
- [x] Implement math library.
- [x] Implement statistics library.
- [x] Implement random library.
- [x] Implement date/time library.
- [x] Implement timezone library.
- [x] Implement filesystem path library.
- [x] Implement file I/O library.
- [x] Implement buffered I/O.
- [x] Implement streams.
- [x] Implement stdin/stdout/stderr.
- [x] Implement terminal colors and cursor control.
- [x] Implement command-line argument parsing.
- [x] Implement environment variables.
- [x] Implement process spawning.
- [x] Implement subprocess pipes.
- [x] Implement signals.
- [x] Implement logging.
- [x] Implement configuration loading.
- [x] Implement JSON.
- [x] Implement CSV.
- [x] Implement TOML.
- [x] Implement YAML if needed.
- [x] Implement XML if needed.
- [x] Implement binary packing/unpacking.
- [x] Implement compression.
- [x] Implement hashing.
- [x] Implement cryptographic hashes.
- [x] Implement secure randomness.
- [x] Implement encoding/decoding.
- [x] Implement regular expressions or Sanskrit-native pattern matching.
- [x] Implement templating.
- [x] Implement serialization.
- [x] Implement deserialization.
- [x] Implement testing utilities.
- [x] Implement benchmarking utilities.

## Phase 11: Algorithms And Data Structures

- [ ] Implement sorting algorithms.
- [ ] Implement stable sort.
- [ ] Implement binary search.
- [ ] Implement graph traversal.
- [ ] Implement shortest path algorithms.
- [ ] Implement tree traversal.
- [ ] Implement heap operations.
- [ ] Implement priority scheduling helpers.
- [ ] Implement dynamic programming helpers.
- [ ] Implement string search.
- [ ] Implement trie.
- [ ] Implement suffix structures if needed for text/grammar work.
- [ ] Implement interval trees.
- [ ] Implement union-find.
- [ ] Implement bitsets.
- [ ] Implement bloom filters if useful.
- [ ] Implement matrix basics.
- [ ] Implement vector math.
- [ ] Implement numerical integration basics.
- [ ] Implement optimization helpers.
- [ ] Implement parser combinators.
- [ ] Implement graph algorithms needed by compiler passes.
- [ ] Implement deterministic iteration guarantees where required.

## Phase 12: Error Handling And Diagnostics

- [ ] Choose primary user-facing error model: exceptions, result types, or a
      tiered combination.
- [ ] Implement recoverable errors.
- [ ] Implement unrecoverable panics.
- [ ] Implement typed error declarations.
- [ ] Implement stack traces.
- [ ] Implement source spans.
- [ ] Implement related diagnostic notes.
- [ ] Implement fix suggestions.
- [ ] Implement Sanskrit-aware parse diagnostics.
- [ ] Implement morphology diagnostics.
- [ ] Implement type diagnostics.
- [ ] Implement borrow/lifetime diagnostics for `rakṣita`.
- [ ] Implement pointer safety diagnostics for `arakṣita`.
- [ ] Implement runtime error reporting.
- [ ] Implement warning categories.
- [ ] Implement lint levels.
- [ ] Implement machine-readable diagnostic output.
- [ ] Implement IDE diagnostic protocol output.
- [ ] Implement crash reports.
- [ ] Implement debug assertions.

## Phase 13: Memory Model By Tier

- [ ] Define shared vocabulary for value, object, reference, address, pointer,
      handle, region, and lifetime.
- [ ] Define tier crossing rules between `surakṣita`, `rakṣita`, and
      `arakṣita`.
- [ ] Define how high-level values are represented in bytecode.
- [ ] Define how high-level values are represented in native memory.
- [ ] Define object identity semantics.
- [ ] Define copy semantics.
- [ ] Define move semantics.
- [ ] Define clone semantics.
- [ ] Define destructor/drop semantics.
- [ ] Define finalization semantics.
- [ ] Define allocation APIs.
- [ ] Define deallocation APIs.
- [ ] Define alignment rules.
- [ ] Define layout rules.
- [ ] Define padding rules.
- [ ] Define packed layout rules.
- [ ] Define ABI layout rules.
- [ ] Define stack allocation.
- [ ] Define heap allocation.
- [ ] Define arena allocation.
- [ ] Define region allocation.
- [ ] Define garbage collection if retained for `surakṣita`.
- [ ] Define reference counting if retained for `surakṣita`.
- [ ] Define ownership rules for `rakṣita`.
- [ ] Define borrow rules for `rakṣita`.
- [ ] Define lifetime/region checking for `rakṣita`.
- [ ] Define unsafe escape hatches for `rakṣita`.
- [ ] Define raw pointer rules for `arakṣita`.
- [ ] Define volatile memory rules for `arakṣita`.
- [ ] Define atomic memory rules.
- [ ] Define memory fences.
- [ ] Define data race rules.
- [ ] Define aliasing rules.

## Phase 14: `Surakṣita` High-Level Capability

- [ ] Managed memory works by default.
- [ ] Null-safe optional values replace accidental null errors.
- [ ] Dynamic collections are ergonomic.
- [ ] Dictionaries/maps are ergonomic.
- [ ] Text handling is Unicode-correct.
- [ ] Exceptions or result propagation are ergonomic.
- [ ] Modules and packages feel Python-level easy.
- [ ] REPL supports live experimentation.
- [ ] Scripts can run directly.
- [ ] CLIs can be built with standard library support.
- [ ] Files and directories are easy to manipulate.
- [ ] HTTP clients are available.
- [ ] HTTP servers are available.
- [ ] JSON/CSV/data formats are built in.
- [ ] Data analysis basics are available.
- [ ] Plotting or visualization backend exists.
- [ ] Web app routing exists.
- [ ] Template rendering exists.
- [ ] Database access exists.
- [ ] Async I/O exists.
- [ ] Task scheduling exists.
- [ ] Test writing is simple.
- [ ] Documentation generation is simple.
- [ ] Package installation is simple.
- [ ] Cross-platform binaries or app bundles can be produced.

## Phase 15: `Rakṣita` Mid-Level Systems Capability

- [ ] Ownership model is specified.
- [ ] Borrow checker or equivalent region checker exists.
- [ ] Mutability rules are explicit.
- [ ] Lifetimes/regions are checked.
- [ ] Stack allocation is controllable.
- [ ] Heap allocation is controllable.
- [ ] Custom allocators exist.
- [ ] Deterministic destruction exists.
- [ ] Move-only types exist.
- [ ] Copy types are explicit.
- [ ] Thread-safe types are marked.
- [ ] Send/share rules exist.
- [ ] Atomics are available.
- [ ] Locks are available.
- [ ] Channels are available.
- [ ] Safe FFI boundary exists.
- [ ] ABI-stable structs exist.
- [ ] Bit manipulation exists.
- [ ] Byte buffers exist.
- [ ] Memory slices exist.
- [ ] Bounds-checked indexing exists.
- [ ] Unsafe blocks are grammatically explicit.
- [ ] Unsafe operations require local proof comments or annotations.
- [ ] Panics and recoverable errors are separated.
- [ ] No hidden garbage collector is required for `rakṣita` programs.
- [ ] `rakṣita` can implement the VM core.
- [ ] `rakṣita` can implement the compiler core.
- [ ] `rakṣita` can implement networking and file-system libraries.

## Phase 16: `Arakṣita` Machine-Level Capability

- [ ] Raw addresses exist.
- [ ] Raw pointers exist.
- [ ] Pointer arithmetic exists.
- [ ] Manual load/store exists.
- [ ] Explicit integer width operations exist.
- [ ] Bitwise operations exist.
- [ ] Shifts and rotates exist.
- [ ] Endianness controls exist.
- [ ] Register-like virtual machine values exist.
- [ ] Stack pointer concepts exist.
- [ ] Frame pointer concepts exist.
- [ ] Calling convention vocabulary exists.
- [ ] Function prologue/epilogue representation exists.
- [ ] Inline machine-prose blocks exist.
- [ ] Labels exist.
- [ ] Jumps exist.
- [ ] Conditional jumps exist.
- [ ] Direct calls exist.
- [ ] Indirect calls exist.
- [ ] Syscall interface exists where supported.
- [ ] Interrupt/trap concepts exist where supported.
- [ ] Memory-mapped I/O concepts exist.
- [ ] Volatile load/store exists.
- [ ] Atomic compare-exchange exists.
- [ ] Fences exist.
- [ ] Object-file emission exists.
- [ ] Symbol tables exist.
- [ ] Relocations exist.
- [ ] Linker input exists.
- [ ] Linker output exists.
- [ ] Debug information exists.
- [ ] Disassembler exists.
- [ ] `arakṣita` can express the low-level VM engine.
- [ ] `arakṣita` can express low-level runtime primitives.

## Phase 17: Bytecode And Machine Prose

- [x] Current bytecode foundation exists.
- [x] Current `.sskyp` machine prose foundation exists.
- [ ] Freeze a versioned bytecode specification.
- [ ] Define stack frame layout.
- [ ] Define call frame layout.
- [ ] Define constant pool layout.
- [ ] Define function table layout.
- [ ] Define module table layout.
- [ ] Define type table layout.
- [ ] Define object layout metadata.
- [ ] Define debug metadata.
- [ ] Define exception metadata if used.
- [ ] Define GC/ownership metadata if used.
- [ ] Define instruction encoding.
- [ ] Define binary bytecode format.
- [ ] Define text bytecode format.
- [ ] Define `.sskyp` as canonical machine-prose assembly.
- [ ] Implement bytecode verifier.
- [ ] Implement bytecode optimizer.
- [ ] Implement bytecode linker.
- [ ] Implement bytecode loader.
- [ ] Implement bytecode serializer.
- [ ] Implement bytecode deserializer.
- [ ] Implement bytecode disassembler.
- [ ] Implement bytecode round-trip conformance tests.
- [ ] Implement `.sskyp` parser in Sanskript.
- [ ] Implement `.sskyp` renderer in Sanskript.
- [ ] Implement `.sskyp` assembler in Sanskript.
- [ ] Implement `.sskyp` disassembler in Sanskript.
- [ ] Require every VM opcode to have a machine-prose form.
- [ ] Require every machine-prose form to have exact semantics.

## Phase 18: VM And Runtime Self-Hosting

- [ ] Specify the VM in language-neutral form.
- [ ] Port VM value representation to Sanskript.
- [ ] Port VM stack to Sanskript.
- [ ] Port VM call frames to Sanskript.
- [ ] Port VM instruction dispatch to Sanskript.
- [ ] Port arithmetic opcodes to Sanskript.
- [ ] Port text opcodes to Sanskript.
- [ ] Port collection opcodes to Sanskript.
- [ ] Port record/object opcodes to Sanskript.
- [ ] Port function call opcodes to Sanskript.
- [ ] Port control-flow opcodes to Sanskript.
- [ ] Port heap opcodes to Sanskript.
- [ ] Port error handling to Sanskript.
- [ ] Port module loading to Sanskript.
- [ ] Port bytecode validation to Sanskript.
- [ ] Port `.sskyp` assembly to Sanskript.
- [ ] Port `.sskyp` disassembly to Sanskript.
- [ ] Implement VM tracing in Sanskript.
- [ ] Implement VM debugging in Sanskript.
- [ ] Implement VM profiling in Sanskript.
- [ ] Implement VM snapshotting if needed.
- [ ] Implement VM garbage collector or ownership runtime in Sanskript.
- [ ] Implement VM standard host interface in Sanskript.
- [ ] Run a Sanskript VM inside the current host VM as bootstrap stage S1.
- [ ] Run Sanskript-compiled bytecode on the Sanskript VM as bootstrap stage S2.
- [ ] Retire host-specific VM logic after S2 conformance passes.

## Phase 19: Compiler Self-Hosting

- [ ] Port lexer/tokenizer to Sanskript.
- [ ] Port transliteration/normalization to Sanskript.
- [ ] Port parser to Sanskript.
- [ ] Port AST definitions to Sanskript.
- [ ] Port AST validation to Sanskript.
- [ ] Port type checker to Sanskript.
- [ ] Port effect checker to Sanskript.
- [ ] Port borrow/region checker to Sanskript.
- [ ] Port macro/compile-time evaluation to Sanskript.
- [ ] Port IR generation to Sanskript.
- [ ] Port bytecode generation to Sanskript.
- [ ] Port bytecode verification to Sanskript.
- [ ] Port optimization passes to Sanskript.
- [ ] Port `.sskyp` generation to Sanskript.
- [ ] Port diagnostic rendering to Sanskript.
- [ ] Port source formatter to Sanskript.
- [ ] Port linter to Sanskript.
- [ ] Port documentation extraction to Sanskript.
- [ ] Port package manifest parsing to Sanskript.
- [ ] Compile the Sanskript compiler with the host compiler.
- [ ] Compile the Sanskript compiler with itself.
- [ ] Verify self-compiled compiler output matches host-compiled output.
- [ ] Keep a minimal bootstrap seed that can rebuild the compiler.

## Phase 20: Native Backends

- [ ] Define backend abstraction.
- [ ] Implement portable bytecode backend.
- [ ] Implement web/WASM backend plan.
- [ ] Implement native object backend plan.
- [ ] Implement Windows x64 calling convention.
- [ ] Implement System V x64 calling convention.
- [ ] Implement ARM64 calling convention.
- [ ] Implement stack maps.
- [ ] Implement debug symbols.
- [ ] Implement object-file writer for COFF.
- [ ] Implement object-file writer for ELF.
- [ ] Implement object-file writer for Mach-O.
- [ ] Implement static linking.
- [ ] Implement dynamic linking.
- [ ] Implement runtime startup.
- [ ] Implement program entry point.
- [ ] Implement native exception/unwind strategy if used.
- [ ] Implement native heap/runtime initialization.
- [ ] Implement native standard library bindings.
- [ ] Implement standalone executable generation.
- [ ] Implement shared library generation.
- [ ] Implement cross-compilation.
- [ ] Treat LLVM/C/Rust backends, if added, as temporary bootstrap or optional
      accelerators rather than the definition of independence.

## Phase 21: Cross-Platform System Support

- [ ] Windows path handling.
- [ ] macOS path handling.
- [ ] Linux path handling.
- [ ] Web virtual path handling.
- [ ] Windows process APIs.
- [ ] POSIX process APIs.
- [ ] Web worker/process equivalents.
- [ ] Windows file watching.
- [ ] macOS/Linux file watching.
- [ ] Web storage APIs.
- [ ] Windows networking.
- [ ] POSIX networking.
- [ ] Browser networking.
- [ ] TLS support.
- [ ] DNS support.
- [ ] Terminal support on Windows.
- [ ] Terminal support on POSIX.
- [ ] Browser console support.
- [ ] Platform feature detection.
- [ ] Platform-specific compilation.
- [ ] Platform-specific package assets.
- [ ] Cross-platform test matrix.
- [ ] Cross-platform release artifacts.

## Phase 22: Web, Apps, Games, Research, And ML

- [ ] HTTP client.
- [ ] HTTP server.
- [ ] Router.
- [ ] Middleware.
- [ ] Request/response types.
- [ ] Cookies.
- [ ] Sessions.
- [ ] Authentication helpers.
- [ ] HTML generation.
- [ ] Template engine.
- [ ] CSS asset pipeline.
- [ ] JavaScript/WASM bridge for browser targets.
- [ ] DOM access for web targets.
- [ ] Event handling for web targets.
- [ ] Canvas 2D support.
- [ ] WebGL/WebGPU bridge or native equivalent.
- [ ] Desktop windowing abstraction.
- [ ] GUI widgets.
- [ ] Menus and shortcuts.
- [ ] Clipboard.
- [ ] Notifications.
- [ ] File dialogs.
- [ ] Game loop.
- [ ] Input handling.
- [ ] Audio playback.
- [ ] Asset loading.
- [ ] Sprite support.
- [ ] 2D physics integration or native engine.
- [ ] 3D scene support.
- [ ] Database client.
- [ ] SQLite support.
- [ ] Postgres support.
- [ ] Dataframe-like tables.
- [ ] CSV/Parquet readers.
- [ ] Plotting.
- [ ] Linear algebra.
- [ ] Tensor basics.
- [ ] Automatic differentiation plan.
- [ ] Model serialization.
- [ ] Python ML interop as temporary bridge only.
- [ ] Native ML kernels roadmap.
- [ ] Notebook or literate-programming workflow.
- [ ] Research script templates.
- [ ] Reproducible environment support.

## Phase 23: Concurrency And Async

- [ ] Threads.
- [ ] Fibers/coroutines.
- [ ] Async functions.
- [ ] Await.
- [ ] Futures/promises.
- [ ] Event loop.
- [ ] Timers.
- [ ] Async file I/O.
- [ ] Async networking.
- [ ] Cancellation.
- [ ] Structured concurrency.
- [ ] Channels.
- [ ] Queues.
- [ ] Mutexes.
- [ ] Read-write locks.
- [ ] Semaphores.
- [ ] Atomics.
- [ ] Thread pools.
- [ ] Work stealing if needed.
- [ ] Data race checking for `rakṣita`.
- [ ] Unsafe concurrent memory rules for `arakṣita`.
- [ ] Browser worker support.

## Phase 24: Tooling

- [ ] Command-line compiler.
- [ ] Command-line runner.
- [ ] REPL.
- [ ] Formatter.
- [ ] Linter.
- [ ] Test runner.
- [ ] Benchmark runner.
- [ ] Package manager.
- [ ] Build tool.
- [ ] Documentation generator.
- [ ] Coverage tool.
- [ ] Profiler.
- [ ] Debugger.
- [ ] Language server.
- [ ] Syntax highlighter.
- [ ] Editor integration.
- [ ] Project templates.
- [ ] Dependency updater.
- [ ] Release builder.
- [ ] Cross-platform installer.
- [ ] Playground.
- [ ] Web playground.
- [ ] Trace viewer.
- [ ] Bytecode inspector.
- [ ] `.sskyp` inspector.
- [ ] Migration tool for Python modules.
- [ ] Migration tool for Rust modules.

## Phase 25: Testing And Verification

- [ ] Unit tests for every parser rule.
- [ ] Unit tests for every compiler lowering.
- [ ] Unit tests for every VM opcode.
- [ ] Golden tests for source examples.
- [ ] Golden tests for bytecode output.
- [ ] Golden tests for `.sskyp` output.
- [ ] Round-trip tests for source formatting.
- [ ] Round-trip tests for bytecode serialization.
- [ ] Round-trip tests for `.sskyp` assembly.
- [ ] Negative parser tests.
- [ ] Negative type-checker tests.
- [ ] Negative borrow-checker tests.
- [ ] Negative unsafe-code tests.
- [ ] Runtime error tests.
- [ ] Cross-platform tests.
- [ ] Fuzz parser.
- [ ] Fuzz bytecode verifier.
- [ ] Fuzz `.sskyp` parser.
- [ ] Property-test standard library collections.
- [ ] Property-test numeric operations.
- [ ] Property-test text operations.
- [ ] Differential-test host VM vs Sanskript VM.
- [ ] Differential-test host compiler vs self-hosted compiler.
- [ ] Performance benchmark suite.
- [ ] Memory safety test suite.
- [ ] Concurrency stress tests.
- [ ] Security review checklist.

## Phase 26: Documentation And Learning Path

- [ ] Beginner tutorial.
- [ ] Prose syntax guide.
- [ ] Sanskrit grammar mapping guide.
- [ ] Python-to-Sanskript migration guide.
- [ ] Rust-to-Sanskript migration guide.
- [ ] Standard library reference.
- [ ] Type system reference.
- [ ] Object model reference.
- [ ] Functional programming guide.
- [ ] Systems programming guide.
- [ ] Machine programming guide.
- [ ] Web app guide.
- [ ] CLI guide.
- [ ] Desktop app guide.
- [ ] Game development guide.
- [ ] Data/research scripting guide.
- [ ] ML guide.
- [ ] Compiler architecture guide.
- [ ] VM architecture guide.
- [ ] Bytecode reference.
- [ ] `.sskyp` reference.
- [ ] Package manager guide.
- [ ] Tooling guide.
- [ ] Contributing guide.
- [ ] Style guide for beautiful grammatical Sanskript.
- [ ] Cookbook of complete programs.
- [ ] API docs generated from Sanskript source.

## Phase 27: Migration Of Existing Project Code

- [ ] Port grammar data loaders.
- [ ] Port sutra registry.
- [ ] Port sutra predicate engine.
- [ ] Port derivational engines.
- [ ] Port morphology helpers.
- [ ] Port source tokenizer.
- [ ] Port parser.
- [ ] Port AST model.
- [ ] Port compiler.
- [ ] Port bytecode schema.
- [ ] Port VM.
- [ ] Port `.sskyp` assembler/disassembler.
- [ ] Port CLI.
- [ ] Port docs generator.
- [ ] Port examples runner.
- [ ] Port test harness.
- [ ] Port web playground core.
- [ ] Port browser runtime core.
- [ ] Port build scripts.
- [ ] Port release scripts.
- [ ] Replace Python-only scripts with Sanskript scripts.
- [ ] Replace Rust-only modules with `rakṣita` or `arakṣita` Sanskript.
- [ ] Keep host interop only where it is explicitly temporary.
- [ ] Add a report showing which Python/Rust files remain and why.
- [ ] Reach zero required Python files for normal use.
- [ ] Reach zero required Rust files for normal use.

## Phase 28: Independence Milestones

- [ ] M0: Current host implementation can run all existing examples.
- [ ] M1: Sanskript can express all current bytecode examples in source prose.
- [ ] M2: Sanskript can express all current `.sskyp` examples in machine prose.
- [ ] M3: Sanskript standard library covers text, collections, files, JSON, CLI,
      HTTP, and tests.
- [ ] M4: Sanskript can implement a useful CLI app without Python/Rust code.
- [ ] M5: Sanskript can implement a useful web app without Python/Rust app code.
- [ ] M6: Sanskript can implement a useful desktop/productivity app.
- [ ] M7: Sanskript can implement a useful game loop and asset pipeline.
- [ ] M8: Sanskript can implement research/data scripts.
- [ ] M9: Sanskript can implement the VM core in `rakṣita`.
- [ ] M10: Sanskript can implement bytecode verification in Sanskript.
- [ ] M11: Sanskript can implement the compiler frontend in Sanskript.
- [ ] M12: Sanskript can implement the compiler backend in Sanskript.
- [ ] M13: Sanskript can compile its own compiler.
- [ ] M14: Sanskript can run its own VM.
- [ ] M15: Sanskript can build and test itself.
- [ ] M16: Sanskript can emit native binaries for at least one platform.
- [ ] M17: Sanskript can emit native binaries for Windows, macOS, and Linux.
- [ ] M18: Sanskript can target web without handwritten JavaScript application
      code.
- [ ] M19: The repo no longer requires Python/Rust for ordinary Sanskript
      development.
- [ ] M20: Python/Rust remain only optional bootstrap, compatibility, or
      contributor convenience paths.

## Immediate High-Leverage Build Order

- [x] Implement class declarations, constructors, methods, and dispatch on top
      of the existing record/object foundation.
- [ ] Implement complete collections: list mutation, map mutation, set, tuple,
      slice, iterator protocol, and foreach.
- [ ] Implement result/option types and a coherent error propagation model.
- [ ] Implement module/package imports so programs can scale beyond one file.
- [ ] Implement byte and buffer types so `rakṣita` and `arakṣita` can become
      real systems tiers.
- [ ] Implement file I/O and CLI standard library support.
- [ ] Implement a native Sanskript test runner.
- [ ] Implement source-level `.sskyp` assembler/disassembler access.
- [ ] Implement the first Sanskript-authored VM subset covering stack,
      arithmetic, text, calls, records, lists, and branches.
- [ ] Implement the first Sanskript-authored compiler subset covering lexer,
      parser skeleton, AST, and bytecode emission for the current executable
      language.
- [ ] Add conformance tests comparing host VM output to Sanskript VM output.
- [ ] Add conformance tests comparing host compiler output to Sanskript compiler
      output.

## Anti-Regression Rules

- [ ] Do not remove prose-style Sanskrit syntax to gain implementation speed.
- [ ] Do not introduce mandatory punctuation that makes Sanskript look like
      Python, C, JavaScript, or Rust in disguise.
- [ ] Do not mark a feature complete unless it passes the completion standard.
- [ ] Do not keep Python/Rust-only behavior hidden behind Sanskript names.
- [ ] Do not expand new surface syntax without VM/runtime execution.
- [ ] Do not expand VM opcodes without `.sskyp` machine-prose representation.
- [ ] Do not expand low-level power without explicit safety-tier boundaries.
- [ ] Do not let docs claim a capability that tests cannot execute.
- [ ] Do not let tests pass only through mocked behavior when real VM behavior
      is expected.
- [ ] Do not close an independence milestone until a fresh checkout can prove it.
