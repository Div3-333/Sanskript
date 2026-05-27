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

## Phase 0: Truth Gates And Project Inventory

- [ ] Create a generated feature matrix listing every language feature, owning
      file, parser rule, compiler lowering, VM handler, docs page, examples,
      and tests.
- [ ] Add a CI check that fails if a feature is marked complete without all
      required artifacts.
- [ ] Add a "no placeholder completion" checker that rejects pass-through
      handlers, empty predicates, metadata-only entries, and TODO-only bodies.
- [ ] Inventory every Python module currently required by Sanskript.
- [ ] Inventory every Rust module currently required by Sanskript.
- [ ] Classify each existing module as compiler, runtime, VM, standard library,
      tooling, docs, tests, web, grammar engine, or migration support.
- [ ] Assign every Python/Rust module to a Sanskript replacement milestone.
- [ ] Add migration labels: keep temporarily, port directly, redesign, remove,
      or replace with native primitive.
- [ ] Create a baseline "Sanskript can replace this" score per module.
- [ ] Add a dashboard that shows percent complete by authoring, compiling,
      execution, testing, documentation, packaging, and deployment.

## Phase 1: Sanskrit Source Surface

- [ ] Define the canonical prose style for executable Sanskript.
- [ ] Define accepted scripts: Devanagari, IAST, SLP1, Harvard-Kyoto, and any
      internal normalized script.
- [ ] Implement source normalization across accepted scripts.
- [ ] Implement reversible transliteration for diagnostics and tooling.
- [ ] Implement strict token provenance so diagnostics can point to original
      user text.
- [ ] Implement sandhi-aware lexical segmentation where grammatically required.
- [ ] Implement opt-in strict Paninian morphology validation for source forms.
- [ ] Implement a relaxed learning mode that explains corrections without
      changing the canonical compiler.
- [ ] Define how vākyas map to executable statements.
- [ ] Define how compounds map to names, selectors, and type expressions.
- [ ] Define how case endings map to semantic roles without becoming symbolic
      punctuation.
- [ ] Define how verb forms map to computation, effect, control, and
      evaluation.
- [ ] Define how particles, indeclinables, and discourse markers are handled.
- [ ] Define how comments are written in natural Sanskrit prose.
- [ ] Define how documentation strings are written and attached.
- [ ] Define how declarations begin and end without semicolons or braces.
- [ ] Define how nested scopes are expressed without indentation dependency.
- [ ] Define how optional punctuation is treated in manuscripts, examples, and
      machine-readable files.
- [ ] Define formatting rules that preserve readability without making layout
      semantic.
- [ ] Create a canonical formatter that outputs beautiful grammatical
      Sanskript.
- [ ] Create a linter that flags choppy Sanskrit-like code.
- [ ] Create a style guide for names, compounds, case use, tense/mood use, and
      prose register.

## Phase 2: Core Syntax And Semantics

- [ ] Implement variable binding in prose with explicit role marking.
- [ ] Implement mutable binding in prose.
- [ ] Implement immutable binding in prose.
- [ ] Implement shadowing rules.
- [ ] Implement lexical scope.
- [ ] Implement block scope without braces.
- [ ] Implement module scope.
- [ ] Implement explicit export scope.
- [ ] Implement local declarations.
- [ ] Implement forward declarations where needed.
- [ ] Implement assignment without symbolic equals.
- [ ] Implement compound assignment through verbal forms, not operators.
- [ ] Implement expression sequencing.
- [ ] Implement statement sequencing.
- [ ] Implement expression-as-value rules.
- [ ] Implement statement-only forms.
- [ ] Implement unit/void result handling.
- [ ] Implement truthiness rules or reject truthiness in favor of explicit
      boolean grammar.
- [ ] Implement boolean negation in prose.
- [ ] Implement boolean conjunction in prose.
- [ ] Implement boolean disjunction in prose.
- [ ] Implement short-circuit evaluation.
- [ ] Implement comparison forms for equality, inequality, ordering, identity,
      and membership.
- [ ] Implement arithmetic precedence without symbolic precedence dependence.
- [ ] Implement explicit grouping through Sanskrit syntactic forms.
- [ ] Implement literal forms for numbers.
- [ ] Implement literal forms for text.
- [ ] Implement literal forms for lists.
- [ ] Implement literal forms for maps.
- [ ] Implement literal forms for records.
- [ ] Implement literal forms for bytes.
- [ ] Implement literal forms for nil/none/absence.
- [ ] Implement literal forms for booleans.

## Phase 3: Values And Data Types

- [x] Integer value foundation exists.
- [x] Boolean value foundation exists.
- [x] Float value foundation exists.
- [x] Text value foundation exists.
- [x] List value foundation exists.
- [x] Map value foundation exists.
- [x] Record value foundation exists.
- [ ] Implement arbitrary precision integers.
- [ ] Implement signed fixed-width integers: i8, i16, i32, i64, i128.
- [ ] Implement unsigned fixed-width integers: u8, u16, u32, u64, u128.
- [ ] Implement machine word integers.
- [ ] Implement pointer-sized integers.
- [ ] Implement checked arithmetic.
- [ ] Implement wrapping arithmetic.
- [ ] Implement saturating arithmetic.
- [ ] Implement exact rational numbers.
- [ ] Implement decimal numbers for finance and accounting.
- [ ] Implement complex numbers.
- [ ] Implement IEEE float semantics.
- [ ] Implement NaN and infinity handling.
- [ ] Implement Unicode scalar handling.
- [ ] Implement grapheme cluster text handling.
- [ ] Implement byte strings.
- [ ] Implement mutable byte arrays.
- [ ] Implement fixed-size arrays.
- [ ] Implement dynamic arrays.
- [ ] Implement slices and views.
- [ ] Implement tuples.
- [ ] Implement named tuples.
- [ ] Implement sets.
- [ ] Implement frozen sets.
- [ ] Implement ordered maps.
- [ ] Implement default maps.
- [ ] Implement counters/multisets.
- [ ] Implement queues.
- [ ] Implement deques.
- [ ] Implement stacks.
- [ ] Implement heaps.
- [ ] Implement priority queues.
- [ ] Implement trees.
- [ ] Implement graphs.
- [ ] Implement enums.
- [ ] Implement tagged unions.
- [ ] Implement option/maybe types.
- [ ] Implement result/either types.
- [ ] Implement typed errors.
- [ ] Implement resource handles.
- [ ] Implement file handles.
- [ ] Implement socket handles.
- [ ] Implement thread handles.
- [ ] Implement process handles.
- [ ] Implement opaque native handles for temporary host interop.

## Phase 4: Type System

- [ ] Define nominal types.
- [ ] Define structural types.
- [ ] Define type aliases.
- [ ] Define newtypes.
- [ ] Define generic type parameters.
- [ ] Define generic functions.
- [ ] Define generic records.
- [ ] Define generic classes.
- [ ] Define generic interfaces/traits.
- [ ] Define bounded generics.
- [ ] Define variance rules.
- [ ] Define type inference for local variables.
- [ ] Define type inference for function returns.
- [ ] Define overload resolution.
- [ ] Define implicit conversions.
- [ ] Define explicit conversions.
- [ ] Define numeric promotion rules.
- [ ] Define text/bytes conversion rules.
- [ ] Define nullable/optional rules.
- [ ] Define lifetimes or region types for `rakṣita`.
- [ ] Define raw pointer types for `arakṣita`.
- [ ] Define safe pointer/reference types for `rakṣita`.
- [ ] Define ownership-qualified types.
- [ ] Define borrowed types.
- [ ] Define mutable borrowed types.
- [ ] Define affine or linear resource types.
- [ ] Define effect types.
- [ ] Define async/future types.
- [ ] Define iterator types.
- [ ] Define generator types.
- [ ] Define callable/function types.
- [ ] Define coroutine types.
- [ ] Define class instance types.
- [ ] Define metaclass/type-object behavior if needed.
- [ ] Define type reflection rules.
- [ ] Define compile-time constant types.

## Phase 5: Control Flow

- [x] Conditional foundation exists.
- [x] Loop foundation exists.
- [ ] Implement if/else in grammatical prose.
- [ ] Implement else-if chains.
- [ ] Implement match/pattern branching.
- [ ] Implement guard clauses.
- [ ] Implement while loops.
- [ ] Implement until loops.
- [ ] Implement counted loops.
- [ ] Implement foreach loops over iterables.
- [ ] Implement infinite loops.
- [ ] Implement break.
- [ ] Implement continue.
- [ ] Implement labeled break.
- [ ] Implement labeled continue.
- [ ] Implement return with value.
- [ ] Implement early return.
- [ ] Implement defer/finally cleanup.
- [ ] Implement exceptions or typed raises if chosen.
- [ ] Implement result-style error propagation if chosen.
- [ ] Implement panic/abort for unrecoverable errors.
- [ ] Implement assertions.
- [ ] Implement preconditions.
- [ ] Implement postconditions.
- [ ] Implement invariants.
- [ ] Implement pattern matching over literals.
- [ ] Implement pattern matching over tuples.
- [ ] Implement pattern matching over records.
- [ ] Implement pattern matching over enums.
- [ ] Implement destructuring assignment.
- [ ] Implement destructuring in parameters.
- [ ] Implement destructuring in loops.
- [ ] Implement destructuring in match arms.

## Phase 6: Functions And Procedures

- [x] Function definition foundation exists.
- [x] Function parameter foundation exists.
- [x] Return-value foundation exists.
- [ ] Implement first-class functions.
- [ ] Implement nested functions.
- [ ] Implement closures.
- [ ] Implement lexical capture.
- [ ] Implement mutable capture rules.
- [ ] Implement recursive functions.
- [ ] Implement mutual recursion.
- [ ] Implement tail-call optimization where safe.
- [ ] Implement default parameters.
- [ ] Implement keyword-style arguments through Sanskrit case roles.
- [ ] Implement variadic parameters.
- [ ] Implement named returns if useful.
- [ ] Implement pure functions.
- [ ] Implement effectful procedures.
- [ ] Implement function overloading.
- [ ] Implement method overloading if chosen.
- [ ] Implement callable objects.
- [ ] Implement partial application.
- [ ] Implement currying only if it fits the prose grammar naturally.
- [ ] Implement decorators/annotations as Sanskrit modifiers.
- [ ] Implement compile-time functions or macros.
- [ ] Implement inline functions for `rakṣita`.
- [ ] Implement naked/ABI functions for `arakṣita`.

## Phase 7: Object-Oriented Programming

- [x] Record/object substrate foundation exists.
- [ ] Implement class declarations.
- [ ] Implement instance construction.
- [ ] Implement constructors.
- [ ] Implement destructors/finalizers.
- [ ] Implement instance fields.
- [ ] Implement private fields.
- [ ] Implement protected fields if chosen.
- [ ] Implement public fields.
- [ ] Implement computed properties.
- [ ] Implement instance methods.
- [ ] Implement static methods.
- [ ] Implement class methods.
- [ ] Implement method receiver grammar.
- [ ] Implement method calls through natural Sanskrit role marking.
- [ ] Implement method dispatch.
- [ ] Implement dynamic dispatch.
- [ ] Implement static dispatch.
- [ ] Implement inheritance if accepted.
- [ ] Implement composition-first guidance if inheritance is limited.
- [ ] Implement interfaces/protocols.
- [ ] Implement traits/typeclasses.
- [ ] Implement trait bounds.
- [ ] Implement trait implementations.
- [ ] Implement abstract classes if accepted.
- [ ] Implement sealed classes if accepted.
- [ ] Implement mixins if accepted.
- [ ] Implement operator-like behavior through named protocol methods, not
      symbolic operators.
- [ ] Implement equality protocol.
- [ ] Implement ordering protocol.
- [ ] Implement hashing protocol.
- [ ] Implement string/display protocol.
- [ ] Implement iteration protocol.
- [ ] Implement context/resource protocol.
- [ ] Implement serialization protocol.
- [ ] Implement reflection over classes and methods.

## Phase 8: Functional And Declarative Programming

- [ ] Implement immutable collections.
- [ ] Implement persistent data structures.
- [ ] Implement map.
- [ ] Implement filter.
- [ ] Implement reduce/fold.
- [ ] Implement scan.
- [ ] Implement zip.
- [ ] Implement enumerate.
- [ ] Implement any/all.
- [ ] Implement comprehensions in grammatical prose.
- [ ] Implement lazy iterators.
- [ ] Implement generators.
- [ ] Implement yield.
- [ ] Implement pipelines as prose, not symbolic chains.
- [ ] Implement pattern matching as an expression.
- [ ] Implement algebraic data types.
- [ ] Implement monadic/result helpers only where they improve error handling.
- [ ] Implement declarative query forms for data.
- [ ] Implement rule-like declarations if useful for grammar engines.
- [ ] Implement memoization helpers.
- [ ] Implement pure/effect separation.

## Phase 9: Modules, Packages, And Namespaces

- [ ] Implement module files.
- [ ] Implement package directories.
- [ ] Implement imports in prose.
- [ ] Implement selective imports.
- [ ] Implement aliases.
- [ ] Implement re-exports.
- [ ] Implement relative imports.
- [ ] Implement absolute imports.
- [ ] Implement package initialization.
- [ ] Implement public/private module members.
- [ ] Implement version declarations.
- [ ] Implement dependency declarations.
- [ ] Implement feature flags.
- [ ] Implement platform-specific modules.
- [ ] Implement build profiles.
- [ ] Implement package lock files.
- [ ] Implement package signing.
- [ ] Implement local path dependencies.
- [ ] Implement registry dependencies.
- [ ] Implement vendored dependencies.
- [ ] Implement standard library namespaces.
- [ ] Implement user library namespaces.
- [ ] Implement conflict resolution.

## Phase 10: Standard Library Core

- [ ] Implement text library.
- [ ] Implement Unicode library.
- [ ] Implement bytes library.
- [ ] Implement math library.
- [ ] Implement statistics library.
- [ ] Implement random library.
- [ ] Implement date/time library.
- [ ] Implement timezone library.
- [ ] Implement filesystem path library.
- [ ] Implement file I/O library.
- [ ] Implement buffered I/O.
- [ ] Implement streams.
- [ ] Implement stdin/stdout/stderr.
- [ ] Implement terminal colors and cursor control.
- [ ] Implement command-line argument parsing.
- [ ] Implement environment variables.
- [ ] Implement process spawning.
- [ ] Implement subprocess pipes.
- [ ] Implement signals.
- [ ] Implement logging.
- [ ] Implement configuration loading.
- [ ] Implement JSON.
- [ ] Implement CSV.
- [ ] Implement TOML.
- [ ] Implement YAML if needed.
- [ ] Implement XML if needed.
- [ ] Implement binary packing/unpacking.
- [ ] Implement compression.
- [ ] Implement hashing.
- [ ] Implement cryptographic hashes.
- [ ] Implement secure randomness.
- [ ] Implement encoding/decoding.
- [ ] Implement regular expressions or Sanskrit-native pattern matching.
- [ ] Implement templating.
- [ ] Implement serialization.
- [ ] Implement deserialization.
- [ ] Implement testing utilities.
- [ ] Implement benchmarking utilities.

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

- [ ] Implement class declarations, constructors, methods, and dispatch on top
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
