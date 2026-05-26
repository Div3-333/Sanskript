# Language Paradigms

Sanskript's application layer must grow without breaking the design promise: source code should remain grammatical Sanskrit prose, and lower toolchain forms should have Sanskrit-prose views when humans need to read them.

The browser target is only one deployment backend. The language target is general-purpose: command-line programs, desktop tools, games, research scripts, servers, websites, numerical work, and later ML/native interop should all lower through the same Sanskript-owned AST, IR, bytecode, and tiered runtime model.

## Current Executable Surface

| Paradigm | Status | Executable support |
| --- | --- | --- |
| Imperative | Implemented | Assignment, increase, decrease, multiply, display |
| Structured | Implemented | `yadi`, `anyathā`, `punaḥ`, `antam` |
| Procedural | Implemented | `vidhānam`, `āhvānam`, modules via `kṣetram` |
| Functions with parameters | Implemented | Prose headers and calls, local parameter binding, bytecode `params` |
| Return-value expressions | Implemented | Function calls can now produce values for assignment/display/return lowering |
| Text values | Implemented | `vākyam … iti` source values, bytecode `push_text`, VM/web output |
| Portable bytecode | Implemented | `.sskbc` compile/run split |
| Sanskrit-prose machine text | Implemented | `.sskyp` yantra-pāṭha assemble/disassemble/run |
| Browser execution | Initial | `sanskript web` emits a static HTML runner for bytecode output |
| Type & data-structure registry | Catalogued | [`data/types/catalog.json`](../data/types/catalog.json) + [`docs/type-system.md`](type-system.md); 60+ types across surakṣita / rakṣita / arakṣita |

## Required Next Layers

| Layer | Why It Matters | Grammar-shaped direction |
| --- | --- | --- |
| Collections | Needed for real apps and algorithms | Introduce samūha/list surfaces through noun classes and verb frames |
| Records / objects | Needed before classes and methods | Model owned fields as named values in an object locus, not brace literals |
| Classes / methods | OOP target | Class words should be grammatical declarations; method calls should remain `kṣetram`/adhikaraṇa-style prose |
| Errors | Useful programs need recoverable failure | Use Sanskrit-aware result/error frames rather than exception symbols |
| Web DOM/events | Needed for webapps | Expose page, element, event, and handler concepts as stdlib nouns and verbs |
| Self-hosted VM | Independence target | Re-express the VM in Sanskript once functions, data structures, and dispatch are strong enough |

## Tier Depth

| Tier | Programming role | Feature depth required |
| --- | --- | --- |
| `surakṣita` | Python-like high-level Sanskript | Managed values, collections, modules, functions, classes, exceptions/results, iterators, async/event APIs, files, networking, package loading, and safe host interop |
| `rakṣita` | Rust/C-like systems Sanskript | Ownership, borrowing, mutation permissions, explicit allocation/free, region lifetimes, layout-aware structs, FFI boundaries, and checked unsafe blocks |
| `arakṣita` | Assembly/machine Sanskript | Raw addresses, pointer arithmetic, tagged/untagged memory, register/stack operations, binary layout, unchecked calls, and VM/bootstrap primitives |

Every major feature should specify its behavior in all three tiers, even when a tier initially rejects it. That keeps the language coherent instead of letting high-level Sanskript and low-level Sanskript become separate projects.

## Design Rule

Do not add punctuation-based features merely because Python, C, or JavaScript have them. Each feature should first get a grammatical surface, then an AST/IR/bytecode meaning, then tests proving that the prose form compiles and runs.
