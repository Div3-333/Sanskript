# Language Paradigms

Sanskript's application layer must grow without breaking the design promise: source code should remain grammatical Sanskrit prose, and lower toolchain forms should have Sanskrit-prose views when humans need to read them.

## Current Executable Surface

| Paradigm | Status | Executable support |
| --- | --- | --- |
| Imperative | Implemented | Assignment, increase, decrease, multiply, display |
| Structured | Implemented | `yadi`, `anyathā`, `punaḥ`, `antam` |
| Procedural | Implemented | `vidhānam`, `āhvānam`, modules via `kṣetram` |
| Functions with parameters | Implemented | Prose headers and calls, local parameter binding, bytecode `params` |
| Text values | Implemented | `vākyam … iti` source values, bytecode `push_text`, VM/web output |
| Portable bytecode | Implemented | `.sskbc` compile/run split |
| Sanskrit-prose machine text | Implemented | `.sskyp` yantra-pāṭha assemble/disassemble/run |
| Browser execution | Initial | `sanskript web` emits a static HTML runner for bytecode output |

## Required Next Layers

| Layer | Why It Matters | Grammar-shaped direction |
| --- | --- | --- |
| Return-value expressions | Needed before functional style feels natural | Function returns should become values in assignment/display frames, not symbolic call syntax |
| Collections | Needed for real apps and algorithms | Introduce samūha/list surfaces through noun classes and verb frames |
| Records / objects | Needed before classes and methods | Model owned fields as named values in an object locus, not brace literals |
| Classes / methods | OOP target | Class words should be grammatical declarations; method calls should remain `kṣetram`/adhikaraṇa-style prose |
| Errors | Useful programs need recoverable failure | Use Sanskrit-aware result/error frames rather than exception symbols |
| Web DOM/events | Needed for webapps | Expose page, element, event, and handler concepts as stdlib nouns and verbs |
| Self-hosted VM | Independence target | Re-express the VM in Sanskript once functions, data structures, and dispatch are strong enough |

## Design Rule

Do not add punctuation-based features merely because Python, C, or JavaScript have them. Each feature should first get a grammatical surface, then an AST/IR/bytecode meaning, then tests proving that the prose form compiles and runs.
