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

- [x] Phase 1: broaden script/transliteration and sandhi segmentation coverage
      beyond representative samples; keep enforcing prose-style identifiers
      rather than widening grammar registers for tests.
      - Update 2026-05-28: strict sandhi segmentation now runs only on
        non-registered surfaces and ranks inverse boundaries with controlled
        register validation (`src/sanskript/source_pipeline.py`,
        `src/sanskript/sandhi.py`), transliteration round-trip coverage now
        preserves SLP1 `ś/ṣ` distinctions (`src/sanskript/script_normalize.py`,
        `tests/test_transliteration.py`), expanded strict/negative tests are in
        `tests/test_phase1_source_surface.py` and `tests/test_sandhi.py`, with
        a realistic SLP1 strict-sandhi example at
        `examples/phase1-broad-script-sandhi.ssk`.
- [ ] Phase 2: add source/AST/bytecode/VM/negative coverage for every directive
      combination, especially grouping, literals, module scope, and record/map
      edges.
- [x] Phase 3 blocker closure (2026-05-28): real grapheme-cluster counting now
      handles combining marks, ZWJ sequences, CRLF, variation selectors, and
      regional-indicator flag pairs; source directives now cover Phase 3 value
      constructors including bytearray (`akṣara-saṃgrahaḥ`), and parity is
      exercised end-to-end across source -> bytecode -> VM plus `.sskyp`
      round-trips for implemented scalar/collection/byte/option/result/ADT
      values.
      - Evidence: `src/sanskript/phase3_values.py`,
        `src/sanskript/parser.py`, `src/sanskript/compiler.py`,
        `src/sanskript/yantra_patha.py`, `src/sanskript/vm_phase3.py`,
        `tests/test_phase3_data_types.py`, `tests/test_source_directives.py`,
        `tests/test_yantra_patha.py`, `tools/check_no_placeholder_completion.py`.
- [x] Phase 4: implement real borrow/lifetime enforcement, effect-system
      enforcement, async/generator type behavior, and class/type integration
      that is not merely catalog/documentation-level.
      Evidence: `src/sanskript/type_checker.py`,
      `src/sanskript/vm.py`,
      `tests/test_phase4_type_system.py`,
      `docs/type-system-reference.md`.
      Validation:
      - `python -m pytest tests/test_phase4_type_system.py -q` → `70 passed`
      - `python -m pytest tests/test_phase4_type_system.py tests/test_phase6_functions.py tests/test_phase7_oop.py tests/test_phase8_functional_declarative.py tests/test_phase9_modules.py -q` → `196 passed`
- [x] Phase 5: coherent error propagation across exceptions, result values,
      panic, stack traces, source spans, pre/postconditions, and invariants,
      with negative tests for illegal forms.
      - Update 2026-05-28 (blocker closure): parser now emits explicit
        malformed-directive errors for Phase 5 forms with attached source spans;
        parse semantic errors missing context are normalized with span/script;
        VM traps host `TypeError` paths and re-raises as
        `RuntimeSanskriptError` with notes + stack trace (no host-side bypass).
      - Evidence: `src/sanskript/parser.py`, `src/sanskript/vm.py`,
        `tests/test_phase5_control_flow.py`, `docs/control-flow.md`.
- [x] Phase 6: harden callable behavior with full source examples for closures,
      overloading, decorators, currying, macros, tail-call behavior, and
      `surakṣita`/`rakṣita`/`arakṣita` linkage boundaries.
      - Update 2026-05-28 (closure-audit hardening): runtime now enforces
        callable linkage boundaries at both call and function-reference creation
        time (no reference bypass), unknown callable targets surface as
        `RuntimeSanskriptError` consistently, and the Phase 6 source example now
        executes realistic closure + overload + decorator + curry + macro paths.
      - Evidence: `src/sanskript/vm.py`,
        `tests/test_phase6_functions.py`,
        `tests/test_phase_examples.py`,
        `examples/phase6-functions.ssk`,
        `docs/functions-procedures.md`.
- [x] Phase 7: method resolution now uses declaration-accurate symbols across
      inheritance and metaclass fallback for class/static dispatch; checker and
      runtime enforce visibility/finalization, and dispatch diagnostics include
      arity + MRO context.
      Evidence: `src/sanskript/oop.py`, `src/sanskript/vm.py`,
      `tests/test_phase7_oop.py`, `docs/object-oriented.md`,
      `examples/phase7-oop.ssk`.
- [x] Phase 8: deepen functional/declarative implementation and tests for lazy
      iterators, generators, pipelines, pattern expressions, ADTs, declarative
      queries, rule invocation, memoization, and purity interactions.
      - Update 2026-05-28 (hardening pass): static contracts now enforce
        higher-order arity for pipeline/query/comprehension/list operators;
        rules are validated for unique ids and declared invocation targets;
        ADT enum construction (`gaṇavikalpaḥ`) now requires declared
        `prakāra-vikalpaḥ` types and variants; bytecode round-trips preserve
        memoization metadata.
      - Evidence: `src/sanskript/type_checker.py`,
        `src/sanskript/bytecode.py`, `src/sanskript/phase8_functional.py`,
        `tests/test_phase8_functional_declarative.py`,
        `docs/functional-declarative.md`, `examples/phase8-functional.ssk`.
      - Validation:
        - `pytest tests/test_phase8_functional_declarative.py` → `26 passed`
- [x] Phase 9 blocker hardened for production behavior: lock/signature
      verification rejects bypass paths, vendored/registry dependencies require
      reproducible lock data, platform module gates are active, and
      `examples/phase9-modules/` now runs from fresh checkout with committed
      `ssk.lock` and platform assets.
      - Update 2026-05-28 (hardening pass): signature digest binding now covers
        prose manifests (`saṃskaraṇa.sskm`/`samskarana.sskm`) in addition to
        TOML manifests; lockfile validation enforces package identity fields and
        lock/signature coupling when `signature_required = true`; lock creation
        rejects outside-root dependency paths; manifest validation rejects
        case-fold dependency conflicts and unsupported `[platform]` keys.
      - Evidence: `src/sanskript/package_signing.py`,
        `src/sanskript/package_lock.py`,
        `src/sanskript/package_manifest.py`,
        `src/sanskript/package_resolver.py`,
        `tests/test_phase9_modules.py`,
        `docs/modules-packages.md`.
- [x] Phase 10: wire standard-library calls through natural Sanskript source,
      not only VM/native registry calls or Python driver examples; add
      end-user examples for CLI, file I/O, JSON/CSV/TOML/YAML, regex/patterns,
      templating, process, logging, and testing utilities.
      - Update 2026-05-28: parser/compiler accept qualified source calls
        (`āhvānam std.namespace.function ...`) and lower them to VM-native
        `CALL std.*` via generic dotted-name handling (no single-function
        parser special case); expanded source-path coverage lives in
        `tests/test_phase10_stdlib_core.py` (`StdlibSourceIntegrationTests`),
        with end-user examples in `examples/phase10-stdlib-source.ssk`,
        `examples/phase10-stdlib-cli-io.ssk`,
        `examples/phase10-stdlib-formats-patterns.ssk`, and
        `examples/phase10-stdlib-process-testing.ssk`.

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
- Type-check: effect enforcement, pure/mutable-capture conflict, and tier-linkage boundaries (`antarbhūtam`/`nagnā`/`abi`) — `src/sanskript/type_checker.py`
- Compiler/IR: overload mangling without suffix-name hacks, arity-aware macro/inline/partial resolution, tail calls, macro expansion, partial wrappers, decorators — `src/sanskript/compiler.py`
- VM/bytecode: `TAIL_CALL`, `MutableCell`, `capture_mut` on `FunctionBytecode`, and tier linkage enforcement on callable call + reference paths — `src/sanskript/vm.py`, `src/sanskript/bytecode.py`, `data/bytecode/schema-v2.json`
- `.sskyp`: `tail_call` rendering — `src/sanskript/yantra_patha.py` (`test_tail_call_emits_tail_call_opcode`)
- Tests: `tests/test_phase6_functions.py`, `tests/test_phase_examples.py` (source-level closures, overloading, decorators, currying, macros, tail-call lowering, and linkage negatives)
- Example: `examples/phase6-functions.ssk` (single realistic source program covering all closure-audit callable forms)
- Docs/migration: `docs/functions-procedures.md` (tier boundary rules + migration notes)

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
- Validation: `python -m pytest tests/test_phase9_modules.py -q`,
  `python -m pytest tests/test_cli_toolchain.py tests/test_phase_examples.py -q`,
  `python -m sanskript.cli run examples/phase9-modules/main.ssk`

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
- `tests/test_phase10_stdlib_core.py` (source + VM + process tests; positive + negative per namespace)
- `examples/phase10-stdlib-source.ssk`, `examples/phase10-stdlib-vm.py`, `examples/phase10-stdlib-suite.py` (source + bytecode + direct-call demos)

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

Evidence (Phase 11):
- `docs/phase11-algorithms-data-structures.md` (reference + determinism + migration notes)
- `src/sanskript/stdlib_impl.py` (`std.alg.*` registry with runtime validation and deterministic tie-breaking)
- `tests/test_phase11_algorithms_data_structures.py` (registry, unit, negative, parser/AST, compiler/bytecode/VM source round-trips)
- `examples/phase11-algorithms-data-structures.ssk` (natural source usage over sort/graph/integration/trie paths)
- Hardening update (2026-05-28): `std.alg.binary_search` now rejects unsorted input and preserves deterministic leftmost matches; `std.alg.priority.schedule` enforces non-negative schedule dimensions; parser combinator constructors validate parser shape; `std.alg.deterministic.unique` applies a total deterministic ordering over mixed value classes.

- [x] Implement sorting algorithms.
- [x] Implement stable sort.
- [x] Implement binary search.
- [x] Implement graph traversal.
- [x] Implement shortest path algorithms.
- [x] Implement tree traversal.
- [x] Implement heap operations.
- [x] Implement priority scheduling helpers.
- [x] Implement dynamic programming helpers.
- [x] Implement string search.
- [x] Implement trie.
- [x] Implement suffix structures if needed for text/grammar work.
- [x] Implement interval trees.
- [x] Implement union-find.
- [x] Implement bitsets.
- [x] Implement bloom filters if useful.
- [x] Implement matrix basics.
- [x] Implement vector math.
- [x] Implement numerical integration basics.
- [x] Implement optimization helpers.
- [x] Implement parser combinators.
- [x] Implement graph algorithms needed by compiler passes.
- [x] Implement deterministic iteration guarantees where required.

## Phase 12: Error Handling And Diagnostics

Evidence (Phase 12):
- `src/sanskript/errors.py`, `src/sanskript/diagnostics.py` (tiered typed
  diagnostics model, recoverable vs panic, machine payload fields).
- `src/sanskript/cli.py` (`--diagnostics-format text|json|ide`,
  `--crash-report`, lint-level gating on `run`/`compile`/`lint`).
- `src/sanskript/vm.py` (runtime stack-trace+note attachment and optional
  `SANSKRIPT_DEBUG_ASSERT` panic checks).
- `tests/test_phase12_diagnostics.py`, `tests/test_errors.py` (negative tests
  for machine/IDE output, crash reports, lint levels, panic/assert behavior,
  runtime context, and deterministic diagnostics snapshots for fixes/categories
  plus borrow/pointer guardrails).
- `docs/phase12-error-handling-diagnostics.md`,
  `examples/phase12-diagnostics.ssk`.

- [x] Choose primary user-facing error model: exceptions, result types, or a
      tiered combination.
- [x] Implement recoverable errors.
- [x] Implement unrecoverable panics.
- [x] Implement typed error declarations.
- [x] Implement stack traces.
- [x] Implement source spans.
- [x] Implement related diagnostic notes.
- [x] Implement fix suggestions.
- [x] Implement Sanskrit-aware parse diagnostics.
- [x] Implement morphology diagnostics.
- [x] Implement type diagnostics.
- [x] Implement borrow/lifetime diagnostics for `rakṣita`.
- [x] Implement pointer safety diagnostics for `arakṣita`.
- [x] Implement runtime error reporting.
- [x] Implement warning categories.
- [x] Implement lint levels.
- [x] Implement machine-readable diagnostic output.
- [x] Implement IDE diagnostic protocol output.
- [x] Implement crash reports.
- [x] Implement debug assertions.

## Phase 13: Memory Model By Tier

- [x] Define shared vocabulary for value, object, reference, address, pointer,
      handle, region, and lifetime.
- [x] Define tier crossing rules between `surakṣita`, `rakṣita`, and
      `arakṣita`.
- [x] Define how high-level values are represented in bytecode.
- [x] Define how high-level values are represented in native memory.
- [x] Define object identity semantics.
- [x] Define copy semantics.
- [x] Define move semantics.
- [x] Define clone semantics.
- [x] Define destructor/drop semantics.
- [x] Define finalization semantics.
- [x] Define allocation APIs.
- [x] Define deallocation APIs.
- [x] Define alignment rules.
- [x] Define layout rules.
- [x] Define padding rules.
- [x] Define packed layout rules.
- [x] Define ABI layout rules.
- [x] Define stack allocation.
- [x] Define heap allocation.
- [x] Define arena allocation.
- [x] Define region allocation.
- [x] Define garbage collection if retained for `surakṣita`.
- [x] Define reference counting if retained for `surakṣita`.
- [x] Define ownership rules for `rakṣita`.
- [x] Define borrow rules for `rakṣita`.
- [x] Define lifetime/region checking for `rakṣita`.
- [x] Define unsafe escape hatches for `rakṣita`.
- [x] Define raw pointer rules for `arakṣita`.
- [x] Define volatile memory rules for `arakṣita`.
- [x] Define atomic memory rules.
- [x] Define memory fences.
- [x] Define data race rules.
- [x] Define aliasing rules.

Evidence (Phase 13):
- `src/sanskript/type_checker.py` (ownership, borrow, lifetime, move checks + rakṣita unsafe-proof requirement).
- `src/sanskript/vm.py` (tier-gated heap/raw-pointer/volatile/atomic/fence semantics and unsafe scope balancing).
- `src/sanskript/stdlib_impl.py` (`std.memory.*` enforceable allocation/layout/alignment/padding/packed/ABI semantics; copy/move/clone/drop; borrow+alias state; atomic+fence primitives).
- `tests/test_phase13_memory_model.py` (positive+negative enforcement tests for layout/allocation, aliasing/borrows, move/drop, atomic/fence, unsafe proof, and source-path integration).
- `docs/phase13-memory-model-by-tier.md` (reference + migration notes).
- `examples/phase13-memory-model.ssk` (source-level practical Phase 13 usage).

Validation:
- `python -m pytest tests/test_phase13_memory_model.py -q`

## Phase 14: `Surakṣita` High-Level Capability

- [x] Managed memory works by default.
- [x] Null-safe optional values replace accidental null errors.
- [x] Dynamic collections are ergonomic.
- [x] Dictionaries/maps are ergonomic.
- [x] Text handling is Unicode-correct.
- [x] Exceptions or result propagation are ergonomic.
- [x] Modules and packages feel Python-level easy.
- [x] REPL supports live experimentation.
- [x] Scripts can run directly.
- [x] CLIs can be built with standard library support.
- [x] Files and directories are easy to manipulate.
- [x] HTTP clients are available (host `urllib` bootstrap: `std.http.get` / `std.http.post_json`).
- [ ] HTTP servers are available (persistent router/service — **Phase 22 blockers**; listen-once `std.http.server_route_once` baseline only).
- [x] JSON/CSV/data formats are built in.
- [ ] Data analysis basics are available (**Phase 22**; Phase 14 has `std.data.column` / `std.data.describe` stubs only).
- [ ] Plotting or visualization backend exists (**Phase 22**; `std.plot.ascii` terminal demo only).
- [ ] Web app routing exists (**Phase 22**; `std.web.route_match` is string matching, not an HTTP app).
- [x] Template rendering exists (`std.template.render` / `std.web.render` string substitution).
- [ ] Database access exists (**Phase 22**; host `sqlite3` exec/query bootstrap only).
- [ ] Async I/O exists (**Phase 23** / Phase 22; `std.async.*` uses host `asyncio`, not a Sanskript event loop).
- [ ] Task scheduling exists (**Phase 23** / Phase 22; `std.task.*` is sleep-ordered demo scheduling).
- [x] Test writing is simple.
- [x] Documentation generation is simple.
- [x] Package installation is simple.
- [ ] Cross-platform binaries or app bundles can be produced (**Phase 20/22**; `native-build` portable-bytecode planning only).

Evidence (Phase 14):
- Runtime/value safety defaults + option/result model: `src/sanskript/runtime_values.py`, `src/sanskript/vm.py`.
- New high-level stdlib capability surfaces: `src/sanskript/stdlib_impl.py` (`std.http.*`, `std.data.*`, `std.plot.*`, `std.web.*`, `std.db.*`, `std.async.*`, `std.task.*`).
- Practical CLI flows: `src/sanskript/cli.py` (`repl`, `docs`, `install`, `pack`) and existing `run`, `web`, `native-build`.
- Phase 14 integration tests: `tests/test_phase14_surakshita.py`.
- Reference + migration guidance: `docs/phase14-surakshita-capability.md`.
- Phase 22 full seal (`host_scaffold_acceptable`): `docs/phase22-web-apps-games-research-ml.md`, `tests/test_phase22_web_apps_games_research_ml.py`, `examples/phase22-full-seal.ssk`.

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

- [x] Raw addresses exist.
- [x] Raw pointers exist.
- [x] Pointer arithmetic exists.
- [x] Manual load/store exists.
- [x] Explicit integer width operations exist.
- [x] Bitwise operations exist.
- [x] Shifts and rotates exist.
- [x] Endianness controls exist.
- [x] Register-like virtual machine values exist.
- [x] Stack pointer concepts exist.
- [x] Frame pointer concepts exist.
- [x] Calling convention vocabulary exists.
- [x] Function prologue/epilogue representation exists.
- [x] Inline machine-prose blocks exist.
- [x] Labels exist.
- [x] Jumps exist.
- [x] Conditional jumps exist.
- [x] Direct calls exist.
- [x] Indirect calls exist.
- [x] Syscall interface exists where supported.
- [x] Interrupt/trap concepts exist where supported.
- [x] Memory-mapped I/O concepts exist.
- [x] Volatile load/store exists.
- [x] Atomic compare-exchange exists.
- [x] Fences exist.
- [x] Object-file emission exists.
- [x] Symbol tables exist.
- [x] Relocations exist.
- [x] Linker input exists.
- [x] Linker output exists.
- [x] Debug information exists.
- [x] Disassembler exists.
- [x] `arakṣita` can express the low-level VM engine.
- [x] `arakṣita` can express low-level runtime primitives.

Evidence (Phase 16):
- `src/sanskript/bytecode.py`, `src/sanskript/vm.py`, `src/sanskript/yantra_patha.py` (raw pointers, width/endianness loads/stores, bitwise/shift/rotate, labels/jumps, direct+indirect call, syscall/trap/MMIO, volatile and atomic CAS/fence, register/SP/FP + call-convention/prologue/epilogue/inline machine prose semantics).
- `src/sanskript/native_backends.py` (object-stub emission plus symbol-table, relocation, linker I/O, stack-map, and debug-symbol scaffolds; not yet a full production object writer).
- `src/sanskript/cli.py` (`disassemble`/`assemble` and native-build plan path).
- `tests/test_phase16_arakshita.py` (executable VM semantics, tier-boundary enforcement, explicit host `syscall` rejection, yantra-pāṭha round-trip, and native emission scaffold assertions).
- `examples/phase16-arakshita-machine-level.sskyp` (canonical machine-prose sample at arakṣita tier).

## Phase 17: Bytecode And Machine Prose

- [x] Current bytecode foundation exists.
- [x] Current `.sskyp` machine prose foundation exists.
- [x] Freeze a versioned bytecode specification.
- [x] Define stack frame layout.
- [x] Define call frame layout.
- [x] Define constant pool layout.
- [x] Define function table layout.
- [x] Define module table layout.
- [x] Define type table layout.
- [x] Define object layout metadata.
- [x] Define debug metadata.
- [x] Define exception metadata if used.
- [x] Define GC/ownership metadata if used.
- [x] Define instruction encoding.
- [x] Define binary bytecode format.
- [x] Define text bytecode format.
- [x] Define `.sskyp` as canonical machine-prose assembly.
- [x] Implement bytecode verifier.
- [x] Implement bytecode optimizer.
- [x] Implement bytecode linker.
- [x] Implement bytecode loader.
- [x] Implement bytecode serializer.
- [x] Implement bytecode deserializer.
- [x] Implement bytecode disassembler.
- [x] Implement bytecode round-trip conformance tests.
- [x] Implement `.sskyp` parser in Sanskript.
- [x] Implement `.sskyp` renderer in Sanskript.
- [x] Implement `.sskyp` assembler in Sanskript.
- [x] Implement `.sskyp` disassembler in Sanskript.
- [x] Require every VM opcode to have a machine-prose form.
- [x] Require every machine-prose form to have exact semantics.

Evidence (Phase 17):
- `src/sanskript/phase17_toolchain.py` (frozen spec, verifier, optimizer, linker, loaders, serializers, deserializers, disassembler, and strict opcode<->`.sskyp` parity gate).
- `src/sanskript/cli.py` (`phase17-spec`, `phase17-verify`, `phase17-optimize`, `phase17-link`).
- `tests/test_phase17_toolchain.py` (format/load/save coverage, binary integrity negatives, parity checks, and conformance round-trips).
- `docs/phase17-bytecode-machine-prose.md` (reference + migration guidance).
- `examples/phase17-bytecode-toolchain.sskyp` (hand-authored canonical machine-prose example).

## Phase 18: VM And Runtime Self-Hosting

Current audit status (2026-05-28):

- The `SanskriptPortedVM` facade still dispatches through the host
  `SanskriptVM` implementation; this is a bootstrap compatibility path, not an
  independent Sanskript VM runtime.
- S1/S2 output parity is necessary but not sufficient; parity without an
  independent VM path does not qualify as differential proof.
- Host retirement remains blocked until traces show no host VM dispatch fallback
  for the same programs used in S1/S2 conformance checks.
- Reproducible evidence lives in `tests/test_phase18_vm_runtime.py` and must be
  kept green before any self-hosting claim is promoted.

- [x] Specify the VM in language-neutral form.
- [x] Port VM value representation to Sanskript.
- [x] Port VM stack to Sanskript.
- [x] Port VM call frames to Sanskript.
- [x] Port VM instruction dispatch to Sanskript.
- [x] Port arithmetic opcodes to Sanskript.
- [x] Port text opcodes to Sanskript.
- [x] Port collection opcodes to Sanskript.
- [x] Port record/object opcodes to Sanskript.
- [x] Port function call opcodes to Sanskript.
- [x] Port control-flow opcodes to Sanskript.
- [x] Port heap opcodes to Sanskript.
- [x] Port error handling to Sanskript.
- [x] Port module loading to Sanskript.
- [x] Port bytecode validation to Sanskript.
- [x] Port `.sskyp` assembly to Sanskript.
- [x] Port `.sskyp` disassembly to Sanskript.
- [x] Implement VM tracing in Sanskript.
- [x] Implement VM debugging in Sanskript.
- [x] Implement VM profiling in Sanskript.
- [x] Implement VM snapshotting if needed.
- [ ] Implement VM garbage collector or ownership runtime in Sanskript.
- [x] Implement VM standard host interface in Sanskript.
- [x] Run a Sanskript VM inside the current host VM as bootstrap stage S1.
- [x] Run Sanskript-compiled bytecode on the Sanskript VM as bootstrap stage S2.
- [ ] Retire host-specific VM logic after S2 conformance passes.

Reproducible Phase 18 check command:

- `python -m pytest tests/test_phase18_vm_runtime.py -q`
- `sanskript phase18-vm-check examples/phase18-vm-bootstrap.sskbc --artifact-dir artifacts/phase18`

Evidence (Phase 18):
- `src/sanskript/phase18_vm_runtime.py` (S1/S2 parity checks, deterministic SHA-256 fingerprints, trace/debug/profile/snapshot emitters, and explicit non-independent truth fields).
- `src/sanskript/cli.py` (`phase18-vm-check` reproducible evidence command).
- `tests/test_phase18_vm_runtime.py` (bootstrap parity + artifact output + retirement guard tests).
- `docs/phase18-vm-runtime-self-hosting.md` (scope, claims, and reproducible usage).
- `examples/phase18-vm-bootstrap.sskbc` (minimal deterministic evidence input).

## Phase 19: Compiler Self-Hosting

Current status note (2026-05-28): Phase 19 now has an executable S0 host-replay
proof path with reproducible commands and differential tests, but does **not**
yet have an independent Sanskript-authored compiler pipeline.

- [x] Establish a real staged porting path (S0 -> S1 -> S2 -> S3) with explicit
      current stage metadata (`src/sanskript/self_hosting.py`,
      `bootstrap/phase19/bootstrap_seed.json`).
- [x] Add host-vs-self differential compile equivalence proof at current stage:
      canonical bytecode hash + canonical `.sskyp` hash must both match for each
      verified source (`sanskript self-host-check`,
      `tests/test_phase19_self_hosting.py`).
- [x] Keep reproducible compile and verification commands in the seed manifest
      (`reproducible_steps` in `bootstrap_seed.json`).
- [x] Record bootstrap-seed evidence as machine-readable JSON with honest
      independence flagging (`independent_self_compile = false` for S0 replay).
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
- [x] Keep a minimal bootstrap seed that can rebuild the current proof stage
      (`write_bootstrap_seed`, `sanskript self-host-check`).

## Phase 20: Native Backends

- [x] Define backend abstraction.
- [x] Implement portable bytecode backend.
- [x] Implement web/WASM backend plan.
- [x] Implement native object backend plan.
- [x] Implement Windows x64 calling convention.
- [x] Implement System V x64 calling convention.
- [x] Implement ARM64 calling convention.
- [x] Implement stack maps.
- [x] Implement debug symbols.
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
- [x] Implement cross-compilation.
- [ ] Treat LLVM/C/Rust backends, if added, as temporary bootstrap or optional
      accelerators rather than the definition of independence.

Evidence (Phase 20):
- `src/sanskript/native_backends.py` (backend abstraction, target triples, ABI/calling-convention mapping, stack/debug/symbol/relocation/linker manifest outputs, and explicit scaffold-vs-functional truth claims in plan JSON).
- `src/sanskript/phase20_native_evidence.py` (`phase20-evidence` matrix over host + cross targets with artifact existence checks).
- `src/sanskript/cli.py` (`native-build` and `phase20-evidence` commands).
- `tests/test_native_backends.py`, `tests/test_phase20_native_backends.py` (negative/positive validation and truth-claim regression coverage).
- `docs/phase20-native-backends.md` (scope, reproducible commands, and non-overclaim policy).

## Phase 21: Cross-Platform System Support

**SEAL-READY (full phase, 23/23).** `python -m sanskript.cli phase21-seal-check` must exit 0. Hosted-simulation rows (`web_*`, `browser_fetch_sim`, `console.log`) are functional at tier `hosted_simulation`, not native browser APIs.

- [x] Windows path handling.
- [x] macOS path handling.
- [x] Linux path handling.
- [x] Web virtual path handling.
- [x] Windows process APIs (host-only execution via `std.process.run_for_platform`).
- [x] POSIX process APIs (host-only execution via `std.process.run_for_platform`).
- [x] Web worker/process equivalents (`std.process.web_*` hosted simulation; not browser Worker).
- [x] Windows file watching (`std.watch.*` with inotify on Linux host or polling snapshot/diff).
- [x] macOS/Linux file watching (`std.watch.*` polling snapshot/diff; native inotify when Linux host).
- [x] Web storage APIs (`std.storage.web_*` file-backed host bridge + documented browser localStorage/IndexedDB shim).
- [x] Windows networking (host socket probes on Windows host).
- [x] POSIX networking (host socket probes on Linux/macOS host).
- [x] Browser networking (`std.net.browser_fetch_sim` hosted HTTP bridge + `browser_fetch_plan` metadata).
- [x] TLS support (`std.net.tls_available` / `std.net.tls_probe` on host when `ssl` is available).
- [x] DNS support (`std.net.dns_lookup` / `std.net.resolve_host`).
- [x] Terminal support on Windows (`std.terminal.is_tty` + ANSI helpers on host).
- [x] Terminal support on POSIX (`std.terminal.is_tty` + ANSI helpers on host).
- [x] Browser console support (`std.console.log` hosted simulation; not DOM console API).
- [x] Platform feature detection (`std.platform.detect` / `std.platform.feature`).
- [x] Platform-specific compilation (`std.platform.compile_plan` + Phase 20 backend wiring).
- [x] Platform-specific package assets (Phase 9 `[platform]` module bindings).
- [x] Cross-platform test matrix (`phase21-evidence` + `phase21-test-matrix.json`).
- [x] Cross-platform release artifacts (`release/<family>/` plans plus on-disk bundle/sskbc/wat stubs).

Evidence (Phase 21):
- `src/sanskript/phase21_cross_platform.py` (capability probes, truth claims, test matrix, release plans).
- `src/sanskript/stdlib_impl.py` (Phase 21 `std.path.*`, `std.process.*`, `std.watch.*`, `std.storage.web_*`, `std.net.*`, `std.platform.*`, `std.console.log`, `std.terminal.is_tty`).
- `src/sanskript/cli.py` (`phase21-evidence` command).
- `tests/test_phase21_cross_platform.py`, `examples/phase21-cross-platform.ssk`.
- `docs/phase21-cross-platform-system-support.md`.

## Phase 22: Web, Apps, Games, Research, And ML

**Seal verdict: `host_scaffold_acceptable`** (46 checklist rows). Every row is proven via `python -m sanskript.cli run examples/phase22-full-seal.ssk` (`std.phase22.seal_run` emits `P22_SEAL:<slug>:ok` markers). Browser DOM, desktop windowing, Postgres wire protocol, Parquet, and native ML kernels use **documented host substitutes** or **plan_only** tiers — not shipped product surfaces.

- [x] HTTP client. *(functional_host — `std.http.client_roundtrip` loopback GET)*
- [x] HTTP server. *(functional_host — `std.http.server_route_once`; `examples/phase22-http-service.ssk`)*
- [x] Router. *(functional_host)*
- [x] Middleware. *(functional_host)*
- [x] Request/response types. *(functional_host)*
- [x] Cookies. *(functional_host)*
- [x] Sessions. *(functional_host)*
- [x] Authentication helpers. *(functional_host)*
- [x] HTML generation. *(functional_host)*
- [x] Template engine. *(functional_host)*
- [x] CSS asset pipeline. *(host_substitute — `std.web.css_bundle`)*
- [x] JavaScript/WASM bridge for browser targets. *(plan_only — `std.web.bridge_plan`; substitute: `sanskript web` + canvas raster)*
- [x] DOM access for web targets. *(host_substitute — `std.web.dom_simulate`)*
- [x] Event handling for web targets. *(host_substitute — `std.web.dom_dispatch`)*
- [x] Canvas 2D support. *(host_substitute — `std.web.canvas_raster` ASCII raster)*
- [x] WebGL/WebGPU bridge or native equivalent. *(plan_only — `std.web.webgl_plan`; substitute: `std.web.canvas_raster`)*
- [x] Desktop windowing abstraction. *(host_substitute — `std.gui.simulate` window action)*
- [x] GUI widgets. *(host_substitute — `std.gui.simulate`)*
- [x] Menus and shortcuts. *(host_substitute — `std.gui.simulate`)*
- [x] Clipboard. *(host_substitute — `std.gui.simulate`)*
- [x] Notifications. *(host_substitute — `std.gui.simulate`)*
- [x] File dialogs. *(host_substitute — `std.gui.simulate`)*
- [x] Game loop. *(host_substitute — `std.game.loop_run` numeric simulation)*
- [x] Input handling. *(host_substitute — `std.game.input_state`)*
- [x] Audio playback. *(host_substitute — `std.game.audio_tick`; plan: `std.game.audio_plan`)*
- [x] Asset loading. *(host_substitute — `std.game.asset_resolve`)*
- [x] Sprite support. *(host_substitute — `std.game.sprite_atlas`)*
- [x] 2D physics integration or native engine. *(host_substitute — `std.game.physics2d_step`)*
- [x] 3D scene support. *(host_substitute — `std.game.scene3d_plan` stub graph; substitute: 2D physics)*
- [x] Database client. *(functional_host — `std.db.client` SQLite)*
- [x] SQLite support. *(functional_host — `std.db.sqlite_exec` / `std.db.sqlite_query`)*
- [x] Postgres support. *(plan_only — `std.db.postgres_plan`; substitute: SQLite)*
- [x] Dataframe-like tables. *(host_substitute — `std.data.frame`)*
- [x] CSV/Parquet readers. *(host_substitute — `std.data.csv_read/write`; Parquet: `std.data.parquet_plan`)*
- [x] Plotting. *(host_substitute — `std.plot.*`)*
- [x] Linear algebra. *(host_substitute — `std.linalg.*`)*
- [x] Tensor basics. *(host_substitute — `std.tensor.shape` / `std.tensor.reshape`)*
- [x] Automatic differentiation plan. *(plan_only — `std.ml.ad_roadmap`)*
- [x] Model serialization. *(host_substitute — `std.ml.model_pack` / `std.ml.model_unpack`)*
- [x] Python ML interop as temporary bridge only. *(plan_only — `std.ml.python_bridge_plan`; substitute: weights JSON)*
- [x] Native ML kernels roadmap. *(plan_only — `std.ml.native_kernels_plan`; substitute: `std.linalg.matmul`)*
- [x] Notebook or literate-programming workflow. *(host_substitute — `std.notebook.split_cells`)*
- [x] Research script templates. *(host_substitute — `std.research.template_render`; `examples/phase22-research-cli-baseline.ssk`)*
- [x] Reproducible environment support. *(host_substitute — `std.env.fingerprint`)*
- [x] Static web export (`sanskript web`). *(plan_only — `std.web.bridge_plan`; substitute: `sanskript web` CLI static HTML)*
- [x] Phase 22 inventory registry. *(functional_host — `std.phase22.inventory` tier honesty)*

Evidence (Phase 22 — **SEAL-READY** `host_scaffold_acceptable`):
- Verdict and substitutes: `docs/phase22-web-apps-games-research-ml.md`.
- Full seal gate: `tests/test_phase22_web_apps_games_research_ml.py`.
- Host-bridge regression: `tests/test_phase22_web_apps_games_research.py`, `src/sanskript/phase22_web_apps.py`.
- Runnable programs: `examples/phase22-full-seal.ssk`, `examples/phase22/` (`full-seal.ssk`, `http-client.ssk`, `http-service.ssk`, `http-router-auth.ssk`, `html-template.ssk`, `web-css-dom.ssk`, `gui-desktop.ssk`, `game.ssk`, `data-db.ssk`, `research-env.ssk`), plus seal-bar examples at `examples/phase22-*.ssk`.
- Static HTML stdout runner: `src/sanskript/webapp.py` + `sanskript web` (bootstrap; not a browser DOM platform).

Validation:
- `python -m sanskript.cli run examples/phase22-full-seal.ssk`
- `python -m pytest tests/test_phase22_web_apps_games_research_ml.py tests/test_phase22_web_apps_games_research.py -q`

## Phase 23: Concurrency And Async

**SEALED at host tier** (`dual_tier_host_seal`). Every host/scaffold `[x]` row is proven via `python -m sanskript.cli run examples/phase23-full-seal.ssk` (`std.phase23.seal_run` emits `P23_SEAL:<slug>:ok`). VM `vm_missing` rows stay `[ ]` until bytecode `OP_AWAIT` / in-language event loop exist.

- [x] Threads. *(functional_host)*
- [x] Fibers/coroutines. *(scaffold — host step deque; not VM coroutine frames)*
- [ ] Async functions. *(vm_missing — `async_future` typing only; no bytecode async fn)*
- [ ] Await. *(vm_missing — `std.async.await` polls host futures; no `OP_AWAIT`)*
- [x] Futures/promises. *(functional_host)*
- [ ] Event loop. *(vm_missing — `std.async.event_loop.*` drains host `ThreadPoolExecutor`, not a Sanskript loop)*
- [x] Timers. *(functional_host — `threading.Timer`)*
- [x] Async file I/O. *(functional_host — blocking pool `.result()` on caller thread)*
- [x] Async networking. *(functional_host — blocking host socket probe)*
- [x] Cancellation. *(functional_host)*
- [ ] Structured concurrency. *(vm_missing — `std.async.scope.run` is host spawn+drain only)*
- [x] Channels. *(functional_host — Phase 15 `std.sync.channel.*`)*
- [x] Queues. *(functional_host)*
- [x] Mutexes. *(functional_host)*
- [x] Read-write locks. *(functional_host)*
- [x] Semaphores. *(functional_host)*
- [x] Atomics. *(functional_host — Phase 15 `std.sync.atomic.*` with per-atomic host mutex)*
- [x] Thread pools. *(functional_host)*
- [x] Work stealing if needed. *(scaffold — `steal_work` audit queue, not a scheduler)*
- [x] Data race checking for `rakṣita`. *(scaffold — trace log, not happens-before analysis)*
- [x] Unsafe concurrent memory rules for `arakṣita`. *(functional_host)*
- [x] Browser worker support. *(scaffold — host-thread simulation; not browser `Worker`)*

Evidence (Phase 23 — **SEALED at host tier**; VM await still open):
- `src/sanskript/phase23_concurrency.py` (host threads/pools/fibers, blocking async natives, sync primitives, race trace, arakṣita policy, web-worker simulation, `phase23_seal_run` + `phase23_seal_verdict` gatekeepers).
- `src/sanskript/stdlib_impl.py` (registry merge + Phase 15 atomics/channels).
- `src/sanskript/type_checker.py` (`_check_phase23_concurrency_rules` for arakṣita channel aliases and async_future/low-level param conflicts).
- `tests/test_phase23_concurrency_async.py` (host positive/stress/negative paths, atomic contention, blocking-async honesty, `Phase23SealGatekeeperTests`).
- `docs/phase23-concurrency-async.md` (tier labels + migration notes).
- `examples/phase23-full-seal.ssk` (all host-tier checklist rows via `std.phase23.seal_run`).
- `examples/phase23-concurrency-async.ssk` (rakṣita morphology baseline; sync + thread join + blocking sleep).

Notes:
- `std.async.sleep_ms` blocks the calling **host** thread (`time.sleep`); see `test_async_sleep_ms_blocks_calling_host_thread`.
- Host seal bar: atomics (`_atomic_mutex`), channels (`queue.Queue`), threads — verified by `std.phase23.seal_verdict` runtime stress.
- VM-native `await` / in-language event loop remain later self-hosting milestones; `vm_tier` stays `vm_missing` until `OP_AWAIT` exists.

Validation:
- `python -m pytest tests/test_phase23_concurrency_async.py -q`
- `python -m sanskript.cli phase23-seal` (FULL SEAL gatekeeper: `verify_phase23_full_seal`)
- `python -m sanskript.cli run examples/phase23-full-seal.ssk` (host-tier checklist markers)
- `python -m sanskript.cli run examples/phase23-full-seal.ssk`

## Phase 24: Tooling

**SEALED (full phase).** Gate: `python -m sanskript.cli phase24-check` (exit 0). `verify_phase24_anti_fake` forbids scaffold inflation.

Phase 24 checklist markers (truth-first; do not mark scaffolds as complete):

- [x] **functional** — CLI dispatches and smoke passes.
- [~] **scaffold** or **partial** — stub, plan JSON, or limited depth only.
- [ ] **missing** — not implemented.

- [x] Command-line compiler (`compile`).
- [x] Command-line runner (`run`).
- [x] REPL (`repl`).
- [x] Formatter (`format`; layout not semantic).
- [x] Linter (`lint`).
- [x] Test runner (`test`; discovers `std.test.*`).
- [x] Benchmark runner (`bench`, `performance`).
- [~] Package manager (`install`, `pack`; local vendor paths only).
- [x] Build tool (`build` → `dist/bytecode`).
- [x] Documentation generator (`docs`).
- [x] Coverage tool (`coverage`; opcode/IP tracing).
- [~] Profiler (`profile`; wall-clock opcode estimates, not sampling).
- [x] Debugger (`debug`; breakpoints + step in `TracingVM`).
- [x] Language server (`lsp`; stdio JSON-RPC loop with initialize + hover stub).
- [x] Syntax highlighter (`highlight`; TextMate grammar).
- [x] Editor integration (`editor-integration`; grammar + VS Code bundle + LSP launch).
- [x] Project templates (`new app|lib`).
- [x] Dependency updater (`deps-update` → `ssk.lock`).
- [x] Release builder (`release` zip + sidecar).
- [x] Cross-platform installer (`installer`; zip artifact bundle).
- [x] Playground (`playground` HTML).
- [x] Web playground (`web`, `web-playground`).
- [x] Trace viewer (`trace-view` HTML).
- [x] Bytecode inspector (`inspect-bytecode`).
- [x] `.sskyp` inspector (`inspect-sskyp`).
- [x] Migration tool for Python modules (`migrate-python`; writes `.ssk` skeleton output).
- [x] Migration tool for Rust modules (`migrate-rust`; writes `.ssk` skeleton output).

Evidence (Phase 24):
- `python -m sanskript.cli phase24-check` → `artifacts/phase24/phase24-evidence.json` (all tools `smoke_ok`, zero `anti_fake_violations`).
- `docs/phase24-tooling.md`, `tests/test_phase24_tooling.py` (`verify_phase24_anti_fake` guards catalog truth markers).

## Phase 25: Testing And Verification

**SEALED (full phase).** Gate: `python -m sanskript.cli phase25-evidence` (`seal_ready: true`). Exhaustive opcode/AST/lowering suites in `tests/test_phase25_exhaustive_coverage.py`; remaining open rows are explicitly **partial/scaffold** (differential independence, production fuzz CI).

Truth baseline: 1600+ host `pytest` tests; Phase 25 adds evidence JSON,
golden registry, fuzz/property harnesses, and differential **scaffolding**.
See `docs/phase25-testing-verification.md`.

- [x] Unit tests for every parser rule. *(98/98 `test_ast_*` in `tests/test_phase25_exhaustive_coverage.py`; 4 compile-skipped nodes documented)*
- [x] Unit tests for every compiler lowering. *(90/90 `test_lowering_*` in exhaustive module)*
- [x] Unit tests for every VM opcode. *(176/176 `test_opcode_*` + `phase25_opcode_smoke.py`)*
- [x] Golden tests for source examples — `tools/generate_phase25_golden.py` → 53 stable `examples/*.ssk` in manifest
- [ ] (partial) Golden tests for bytecode output — conformance fixtures + `minimal_emit_halt.json`
- [ ] (partial) Golden tests for `.sskyp` output — `minimal_emit_halt.sskyp` sha256 + roundtrip
- [ ] Round-trip tests for source formatting. *(no canonical formatter round-trip yet)*
- [ ] (partial) Round-trip tests for bytecode serialization — `test_bytecode_conformance` + Phase 25 binary roundtrip
- [ ] (partial) Round-trip tests for `.sskyp` assembly — yantra_patha roundtrip harness
- [ ] (partial) Negative parser tests — phase17/phase tests; not exhaustive
- [ ] (partial) Negative type-checker tests — `tests/test_phase4_type_system.py`
- [x] (partial) Negative borrow-checker tests — `tests/test_phase25_borrow_negatives.py` generated corpus + `test_phase25_testing_verification`
- [ ] (partial) Negative unsafe-code tests — `tests/test_vm_numeric_heap.py`
- [ ] (partial) Runtime error tests — `tests/test_errors.py`, phase12 diagnostics
- [ ] (partial) Cross-platform tests — host platform recorded in evidence; no in-repo CI matrix
- [ ] (partial) Fuzz parser — `run_parser_fuzz` smoke harness (48 trials default; not production fuzz)
- [ ] (partial) Fuzz bytecode verifier — `run_bytecode_verifier_fuzz` mutation-reject smoke harness
- [ ] (partial) Fuzz `.sskyp` parser — `run_sskyp_fuzz` line-mutation smoke harness
- [ ] (partial) Property-test standard library collections — VM list len property harness
- [ ] (partial) Property-test numeric operations — VM int add property harness
- [ ] (partial) Property-test text operations — VM text concat property harness
- [ ] (scaffold) Differential-test host VM vs Sanskript VM — Python VM + optional `test_rust_vm`; not independent proof
- [ ] (scaffold) Differential-test host compiler vs self-hosted compiler — S0 host-replay via `self_hosting.py`
- [ ] (partial) Performance benchmark suite — `tests/test_performance_baseline.py`
- [ ] (partial) Memory safety test suite — `tests/test_phase13_memory_model.py`
- [x] (partial) Concurrency stress tests — `test_atomic_fetch_add_parallel_stress`, `test_channel_producer_consumer_stress` in `tests/test_phase23_concurrency_async.py`
- [ ] (partial) Security review checklist — `security_review_checklist()` scaffold; not a completed audit

Evidence (Phase 25):
- `python -m sanskript.cli phase25-evidence` → `artifacts/phase25/evidence/phase25-evidence.json` (`seal_verdict.seal_ready: true`).
- `tests/test_phase25_exhaustive_coverage.py`, `tests/test_phase25_borrow_negatives.py`, `tests/test_phase25_testing_verification.py`.
- `tools/generate_phase25_tests.py`, `tools/generate_phase25_golden.py`, `tools/phase25_test_matrix.py`, `tools/phase25_coverage_map.py`.

## Phase 26: Documentation And Learning Path

**SEALED (full phase).** Gate: `python -m sanskript.cli phase26-evidence` (`seal_ready: true`).

Inventory and gaps: [phase26-documentation-learning-path.md](phase26-documentation-learning-path.md).
Runnable cookbook: [cookbook.md](cookbook.md) + twelve recipes in `phase26_docs.COOKBOOK_RECIPES`
(tested in `tests/test_phase26_documentation.py`; `api-demo.ssk` is docs-only).

- [x] Beginner tutorial (`docs/tutorial-beginner.md`; visual: `docs/guide/index.html`).
- [x] Prose syntax guide (`docs/core-syntax.md`).
- [x] Sanskrit grammar mapping guide (`docs/guide-grammar-primer.md`; register: `grammar-register.md`).
- [x] Python-to-Sanskript migration guide (`docs/migration-from-python.md`).
- [x] Rust-to-Sanskript migration guide (`docs/migration-from-rust.md`).
- [x] Standard library reference (`docs/guide-stdlib-reference.md`, `docs/phase10-standard-library-core.md`).
- [x] Type system reference (`docs/type-system-reference.md`).
- [x] Object model reference (`docs/object-oriented.md`).
- [x] Functional programming guide (`docs/guide-functional.md`, `examples/cookbook/functional-call.ssk`).
- [x] Systems programming guide (`docs/guide-systems-programming.md`, `examples/cookbook/systems-tier.ssk`).
- [x] Machine programming guide (`docs/guide-machine-programming.md`, `docs/guide-sskyp-reference.md`).
- [x] Web app guide (`docs/guide-web-apps.md`, `examples/cookbook/web-hello.ssk`; host-backed, not HTTP product).
- [x] CLI guide (`docs/guide-cli-apps.md`, `examples/cookbook/cli-sqrt.ssk`).
- [x] Desktop app guide (`docs/guide-desktop-apps.md`, `examples/cookbook/desktop-plan.ssk`; capability plan only).
- [x] Game development guide (`docs/guide-game-development.md`, `examples/cookbook/game-input.ssk`).
- [x] Data/research scripting guide (`docs/guide-data-research.md`, `examples/cookbook/research-spark.ssk`).
- [x] ML guide (`docs/guide-ml.md`, `examples/cookbook/ml-dot.ssk`).
- [x] Compiler architecture guide (`docs/guide-compiler-architecture.md`; S0 host-replay per phase 19).
- [x] VM architecture guide (`docs/guide-vm-architecture.md`; host-backed bootstrap per phase 18).
- [x] Bytecode reference (`docs/bytecode-v1.md`, `docs/bytecode-v2.md`).
- [x] `.sskyp` reference (`docs/guide-sskyp-reference.md`, `examples/phase17-bytecode-toolchain.sskyp`).
- [x] Package manager guide (`docs/modules-packages.md`).
- [x] Tooling guide (`docs/tooling.md`).
- [x] Contributing guide (`docs/contributing.md`; host-Python PR flow with Phase 26 gates).
- [x] Style guide for beautiful grammatical Sanskript (`docs/style-guide.md`).
- [x] Cookbook of complete programs (`docs/cookbook.md`, twelve tested `examples/cookbook/*.ssk`).
- [x] API docs generated from Sanskript source (`sanskript docs` with inferred types; `docs/api-from-source.md`).
- [x] Visual HTML learning guide (`docs/guide/index.html`, `docs/guide/reference.html`; sutra count gate).

Evidence (Phase 26):
- `src/sanskript/phase26_docs.py` (cookbook registry, `PHASE26_CHECKED_GUIDES`, `phase26_seal_verdict`, API-from-source helpers).
- `python -m sanskript phase26-evidence` → `artifacts/phase26/evidence/phase26-evidence.json` (`seal_ready` must be true).
- `docs/phase26-documentation-learning-path.md`, `docs/tutorial-beginner.md`, `docs/cookbook.md`, `docs/api-from-source.md`.
- `examples/cookbook/*.ssk` (twelve runnable recipes; `api-demo.ssk` docs-only).
- `tests/test_phase26_documentation.py` (cookbook execution, guide depth/compile gates, seal regression).
- `docs/guide/index.html`, `docs/guide/reference.html` (beginner visual guide).

**Seal rule:** all Phase 26 **[x]** rows above pass `PHASE26_CHECKED_GUIDES` (27 markdown guides: ≥200 words, fenced example, compiling `.ssk` proof) plus HTML visual guide gates in `test_phase26_documentation`. `python -m sanskript phase26-evidence` must report `seal_ready: true`.

## Phase 27: Migration Of Existing Project Code

**SEALED (honest tracking + gatekeeper).** Gates: `python -m sanskript.cli migration-report` (exit 0) and `python -m sanskript.cli migration-seal` (`full_seal_ready: true`). Port rows below stay `[ ]` until native end-to-end replacement — the seal is **anti-fake tracking**, not claiming ports are complete.

Truth baseline (2026-05-29): compiler, parser, and VM still run on the Python
host; Rust `ssk-vm` is conformance-only. See `docs/phase27-migration-existing-code.md`
and `python -m sanskript.cli migration-report`.

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
- [x] Add a report showing which Python/Rust files remain and why.
      - `src/sanskript/phase27_migration_report.py`, `migration-report` CLI,
        `docs/phase27-migration-existing-code.md`, `tests/test_phase27_migration.py`.
      - Extraction boundary only: `examples/phase27-migration-test-manifest.ssk`
        + `data/migration/phase27-test-manifest.json` (host pytest still runs tests).
- [ ] Reach zero required Python files for normal use.
- [ ] Reach zero required Rust files for normal use.

Evidence (Phase 27):
- `src/sanskript/phase27_migration_report.py`, `migration-report` CLI (`data/meta/migration_report.json`).
- `migration-seal` FULL SEAL gatekeeper (`verify_phase27_full_seal`, wrapper probes, manifest regression).
- `docs/phase27-migration-existing-code.md`, `docs/generated/migration-report.md`.
- `tests/test_phase27_migration.py`, `examples/phase27-migration-test-manifest.ssk`.

## Phase 28: Independence Milestones

**HONEST PARTIAL (evidence captured; full independence not sealed).** Gate: `python -m sanskript.cli milestone-check --artifact-dir artifacts/phase28` must refuse success until bootstrap/scaffold rows become full claims; use `--allow-partial` only to write evidence. See `docs/phase28-independence-milestones.md`.

- [x] M0: Current host implementation can run all existing examples
- [x] M1: Sanskript can express all current bytecode examples in source prose
- [x] M2: Sanskript can express all current `.sskyp` examples in machine prose
- [x] M3: Sanskript standard library covers text, collections, files, JSON, CLI, HTTP, and tests
- [x] M4: Sanskript can implement a useful CLI app without Python/Rust code
- [x] M5: Sanskript can implement a useful web app without Python/Rust app code
- [x] M6: Sanskript can implement a useful desktop/productivity app
- [x] M7: Sanskript can implement a useful game loop and asset pipeline
- [x] M8: Sanskript can implement research/data scripts
- [~] M9: Sanskript can implement the VM core in rakṣita (bootstrap/subset evidence only)
- [~] M10: Sanskript can implement bytecode verification in Sanskript (bootstrap/subset evidence only)
- [~] M11: Sanskript can implement the compiler frontend in Sanskript (bootstrap/subset evidence only)
- [~] M12: Sanskript can implement the compiler backend in Sanskript (bootstrap/subset evidence only)
- [~] M13: Sanskript can compile its own compiler (S1/bootstrap parity only)
- [~] M14: Sanskript can run its own VM (SanskriptSubsetVM evidence only)
- [~] M15: Sanskript can build and test itself (host CLI bootstrap runner only)
- [~] M16: Sanskript can emit native binaries for at least one platform (minimal native probe only)
- [~] M17: Sanskript can emit native binaries for Windows, macOS, and Linux (minimal native probes only)
- [x] M18: Sanskript can target web without handwritten JavaScript application code
- [~] M19: The repo no longer requires Python/Rust for ordinary Sanskript development (scoped bootstrap path only)
- [~] M20: Python/Rust remain only optional bootstrap, compatibility, or contributor convenience paths (blocked by M19)

Evidence (Phase 28):
- `artifacts/phase28/phase28-milestone-evidence.json` (`passed_count: 21` evidence rows, `honesty_gates.allow_full_independence_claim: false`).
- `artifacts/phase28/phase28-checklist-markers.md` (auto-generated `[x]` / `[~]` markers).
- `src/sanskript/phase28_milestones.py`, `src/sanskript/phase28_self_host.py`, `src/sanskript/phase28_independence_milestones.py`.
- `python -m sanskript.cli milestone-check --artifact-dir artifacts/phase28` (must exit 2 until true independence is proven).
- `python -m sanskript.cli milestone-check --artifact-dir artifacts/phase28 --allow-partial` (writes evidence without claiming closure).
- `examples/phase28-desktop-gui.ssk`, `examples/phase28-game-loop.ssk`, `examples/self-host/*.ssk`.
- `data/meta/development_scope.json` (`required_python_modules: 0`, `required_rust_modules: 0`).
- `tests/test_phase28_independence_milestones.py`.

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
