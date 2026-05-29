# Generated Module Inventory

_Generated at 2026-05-29T05:05:30+00:00 by `tools/generate_module_inventory.py`._

**262** modules (257 Python, 5 Rust). Average replaceability score: **28.8** / 100.

## By role

| Role | Modules |
| --- | ---: |
| compiler | 6 |
| docs | 1 |
| grammar_engine | 58 |
| migration | 1 |
| other | 57 |
| runtime | 3 |
| tests | 95 |
| tooling | 35 |
| vm | 5 |
| web | 1 |

## By milestone

| Milestone | Modules |
| --- | ---: |
| M3 | 3 |
| M4 | 2 |
| M5 | 1 |
| M9 | 4 |
| M10 | 1 |
| M11 | 64 |
| M15 | 128 |
| M19 | 57 |
| M26 | 1 |
| M27 | 1 |

## By migration label

_`port_directly` is a replacement strategy, not evidence that logic already runs in native Sanskript. See `data/meta/migration_report.json` (Phase 27) for honest port status._

| Label | Modules |
| --- | ---: |
| keep_temporarily | 126 |
| port_directly | 72 |
| redesign | 59 |
| remove | 5 |

## All modules

| Path | Lang | Role | Milestone | Migration | Score | Lines |
| --- | --- | --- | --- | --- | ---: | ---: |
| `scripts/_profile_import.py` | python | tooling | M15 | remove | 55 | 22 |
| `scripts/build_controlled_lexicon.py` | python | tooling | M15 | keep_temporarily | 55 | 24 |
| `scripts/build_dhatu_catalog.py` | python | tooling | M15 | keep_temporarily | 55 | 304 |
| `scripts/build_vocabulary_corpus.py` | python | tooling | M15 | keep_temporarily | 55 | 87 |
| `scripts/check_predicate_weak_sutras.py` | python | tooling | M15 | keep_temporarily | 55 | 5 |
| `scripts/dhatu_entries_data.py` | python | tooling | M15 | keep_temporarily | 55 | 320 |
| `scripts/dhatu_entries_g5_g10.py` | python | tooling | M15 | keep_temporarily | 55 | 221 |
| `scripts/export_grammar_register.py` | python | tooling | M15 | keep_temporarily | 55 | 21 |
| `scripts/generate_vocabulary_stems.py` | python | tooling | M15 | keep_temporarily | 55 | 25 |
| `scripts/migrate_vocabulary_to_corpus.py` | python | tooling | M15 | remove | 55 | 86 |
| `scripts/performance_baseline.py` | python | tooling | M15 | keep_temporarily | 55 | 5 |
| `scripts/populate_iu_vocabulary.py` | python | tooling | M15 | keep_temporarily | 55 | 662 |
| `scripts/populate_noun_vocabulary.py` | python | tooling | M15 | keep_temporarily | 55 | 483 |
| `scripts/populate_rare_noun_vocabulary.py` | python | tooling | M15 | keep_temporarily | 55 | 292 |
| `scripts/populate_verb_vocabulary.py` | python | tooling | M15 | keep_temporarily | 55 | 224 |
| `src/sanskript/__main__.py` | python | other | M19 | port_directly | 30 | 5 |
| `src/sanskript/accent.py` | python | grammar_engine | M11 | redesign | 12 | 70 |
| `src/sanskript/adhyaya1.py` | python | grammar_engine | M11 | redesign | 12 | 1552 |
| `src/sanskript/adhyaya123_engines.py` | python | grammar_engine | M11 | redesign | 12 | 2601 |
| `src/sanskript/adhyaya23.py` | python | grammar_engine | M11 | redesign | 12 | 569 |
| `src/sanskript/adhyaya2_atomic.py` | python | grammar_engine | M11 | redesign | 12 | 3509 |
| `src/sanskript/adhyaya456.py` | python | grammar_engine | M11 | redesign | 12 | 244 |
| `src/sanskript/adhyaya45_engines.py` | python | grammar_engine | M11 | redesign | 12 | 820 |
| `src/sanskript/adhyaya678_engines.py` | python | grammar_engine | M11 | redesign | 12 | 1063 |
| `src/sanskript/adhyaya7.py` | python | grammar_engine | M11 | redesign | 12 | 243 |
| `src/sanskript/adhyaya8.py` | python | grammar_engine | M11 | redesign | 12 | 259 |
| `src/sanskript/anga.py` | python | grammar_engine | M11 | redesign | 12 | 286 |
| `src/sanskript/ast.py` | python | compiler | M11 | port_directly | 45 | 1156 |
| `src/sanskript/avyaya.py` | python | grammar_engine | M11 | redesign | 12 | 119 |
| `src/sanskript/bytecode.py` | python | vm | M9 | port_directly | 50 | 1142 |
| `src/sanskript/canon_topics.py` | python | other | M19 | port_directly | 30 | 102 |
| `src/sanskript/categories.py` | python | other | M19 | port_directly | 30 | 181 |
| `src/sanskript/cli.py` | python | other | M19 | port_directly | 30 | 1573 |
| `src/sanskript/comments.py` | python | other | M19 | port_directly | 30 | 73 |
| `src/sanskript/compiler.py` | python | compiler | M11 | port_directly | 45 | 3077 |
| `src/sanskript/derivation.py` | python | grammar_engine | M11 | redesign | 12 | 295 |
| `src/sanskript/diagnostics.py` | python | other | M19 | port_directly | 30 | 148 |
| `src/sanskript/errors.py` | python | runtime | M3 | port_directly | 65 | 156 |
| `src/sanskript/fixed_width.py` | python | other | M19 | port_directly | 30 | 247 |
| `src/sanskript/formatter.py` | python | other | M19 | port_directly | 30 | 38 |
| `src/sanskript/grammar.py` | python | compiler | M11 | port_directly | 45 | 333 |
| `src/sanskript/grammar_register.py` | python | other | M19 | port_directly | 30 | 436 |
| `src/sanskript/identifiers.py` | python | other | M19 | port_directly | 30 | 107 |
| `src/sanskript/interpreter.py` | python | runtime | M3 | port_directly | 40 | 72 |
| `src/sanskript/ir.py` | python | compiler | M11 | port_directly | 45 | 848 |
| `src/sanskript/karaka.py` | python | grammar_engine | M11 | redesign | 12 | 194 |
| `src/sanskript/learning_mode.py` | python | other | M19 | port_directly | 30 | 81 |
| `src/sanskript/linter.py` | python | other | M19 | port_directly | 30 | 89 |
| `src/sanskript/markers.py` | python | other | M19 | port_directly | 30 | 86 |
| `src/sanskript/metarules.py` | python | grammar_engine | M11 | redesign | 12 | 172 |
| `src/sanskript/module_loader.py` | python | other | M19 | port_directly | 30 | 141 |
| `src/sanskript/morphology.py` | python | grammar_engine | M11 | redesign | 12 | 63 |
| `src/sanskript/morphology_facade.py` | python | grammar_engine | M11 | redesign | 12 | 257 |
| `src/sanskript/morphology_lexicon.py` | python | grammar_engine | M11 | redesign | 12 | 270 |
| `src/sanskript/morphology_synth.py` | python | grammar_engine | M11 | redesign | 12 | 870 |
| `src/sanskript/morphology_text.py` | python | grammar_engine | M11 | redesign | 12 | 37 |
| `src/sanskript/morphology_validate.py` | python | grammar_engine | M11 | redesign | 12 | 85 |
| `src/sanskript/native_backends.py` | python | other | M19 | port_directly | 30 | 580 |
| `src/sanskript/native_minimal_exe.py` | python | other | M19 | port_directly | 30 | 55 |
| `src/sanskript/oop.py` | python | other | M19 | port_directly | 30 | 316 |
| `src/sanskript/package_lock.py` | python | other | M19 | port_directly | 30 | 229 |
| `src/sanskript/package_manifest.py` | python | other | M19 | port_directly | 30 | 314 |
| `src/sanskript/package_resolver.py` | python | other | M19 | port_directly | 30 | 408 |
| `src/sanskript/package_signing.py` | python | other | M19 | port_directly | 30 | 155 |
| `src/sanskript/paninian_effects.py` | python | grammar_engine | M11 | redesign | 12 | 741 |
| `src/sanskript/paninian_engine.py` | python | grammar_engine | M11 | redesign | 12 | 1247 |
| `src/sanskript/parser.py` | python | compiler | M11 | port_directly | 45 | 3054 |
| `src/sanskript/parser_core.py` | python | other | M19 | port_directly | 30 | 525 |
| `src/sanskript/performance.py` | python | other | M19 | port_directly | 30 | 101 |
| `src/sanskript/phase17_toolchain.py` | python | other | M19 | port_directly | 30 | 443 |
| `src/sanskript/phase18_vm_runtime.py` | python | other | M19 | port_directly | 30 | 627 |
| `src/sanskript/phase20_native_evidence.py` | python | other | M19 | port_directly | 30 | 116 |
| `src/sanskript/phase21_cross_platform.py` | python | other | M19 | port_directly | 30 | 1324 |
| `src/sanskript/phase22_web_apps.py` | python | other | M19 | port_directly | 30 | 1220 |
| `src/sanskript/phase23_concurrency.py` | python | other | M19 | port_directly | 30 | 1770 |
| `src/sanskript/phase24_tooling.py` | python | other | M19 | port_directly | 30 | 1138 |
| `src/sanskript/phase25_ast_smoke.py` | python | other | M19 | port_directly | 30 | 147 |
| `src/sanskript/phase25_exhaustive_registry.py` | python | other | M19 | port_directly | 30 | 168 |
| `src/sanskript/phase25_opcode_smoke.py` | python | other | M19 | port_directly | 30 | 817 |
| `src/sanskript/phase25_testing_verification.py` | python | other | M19 | port_directly | 30 | 1429 |
| `src/sanskript/phase26_docs.py` | python | other | M19 | port_directly | 30 | 443 |
| `src/sanskript/phase27_migration_report.py` | python | other | M19 | port_directly | 30 | 1003 |
| `src/sanskript/phase27_ports.py` | python | other | M19 | port_directly | 30 | 369 |
| `src/sanskript/phase28_independence_milestones.py` | python | other | M19 | port_directly | 30 | 540 |
| `src/sanskript/phase28_milestones.py` | python | other | M19 | port_directly | 30 | 1070 |
| `src/sanskript/phase28_self_host.py` | python | other | M19 | port_directly | 30 | 221 |
| `src/sanskript/phase3_opcodes.py` | python | other | M19 | port_directly | 30 | 180 |
| `src/sanskript/phase3_source.py` | python | other | M19 | port_directly | 30 | 69 |
| `src/sanskript/phase3_values.py` | python | other | M19 | port_directly | 30 | 270 |
| `src/sanskript/phase8_functional.py` | python | other | M19 | port_directly | 30 | 388 |
| `src/sanskript/phase8_opcodes.py` | python | other | M19 | port_directly | 30 | 98 |
| `src/sanskript/phonology.py` | python | grammar_engine | M11 | redesign | 12 | 573 |
| `src/sanskript/predicate_audit.py` | python | other | M19 | port_directly | 30 | 86 |
| `src/sanskript/register_docs.py` | python | docs | M26 | port_directly | 60 | 81 |
| `src/sanskript/runtime_values.py` | python | runtime | M3 | port_directly | 40 | 718 |
| `src/sanskript/samasa.py` | python | grammar_engine | M11 | redesign | 12 | 319 |
| `src/sanskript/sandhi.py` | python | grammar_engine | M11 | redesign | 12 | 307 |
| `src/sanskript/scope.py` | python | other | M19 | port_directly | 30 | 59 |
| `src/sanskript/script_normalize.py` | python | other | M19 | port_directly | 30 | 400 |
| `src/sanskript/self_hosting.py` | python | other | M19 | port_directly | 30 | 340 |
| `src/sanskript/source_context.py` | python | other | M19 | port_directly | 30 | 44 |
| `src/sanskript/source_pipeline.py` | python | other | M19 | port_directly | 30 | 114 |
| `src/sanskript/stdlib_common.py` | python | other | M19 | port_directly | 30 | 130 |
| `src/sanskript/stdlib_core.py` | python | other | M19 | port_directly | 30 | 42 |
| `src/sanskript/stdlib_impl.py` | python | other | M19 | port_directly | 30 | 3881 |
| `src/sanskript/subanta.py` | python | grammar_engine | M11 | redesign | 12 | 319 |
| `src/sanskript/subanta_paradigms.py` | python | grammar_engine | M11 | redesign | 12 | 366 |
| `src/sanskript/sutra_handlers_1_2.py` | python | grammar_engine | M11 | redesign | 12 | 168 |
| `src/sanskript/sutra_handlers_adhyaya23.py` | python | grammar_engine | M11 | redesign | 12 | 1261 |
| `src/sanskript/sutra_impl_1_1.py` | python | grammar_engine | M11 | redesign | 12 | 442 |
| `src/sanskript/sutra_impl_1_rest.py` | python | grammar_engine | M11 | redesign | 12 | 1784 |
| `src/sanskript/sutra_impl_2.py` | python | grammar_engine | M11 | redesign | 12 | 2016 |
| `src/sanskript/sutra_impl_3_1.py` | python | grammar_engine | M11 | redesign | 12 | 1452 |
| `src/sanskript/sutra_impl_3_2.py` | python | grammar_engine | M11 | redesign | 12 | 1493 |
| `src/sanskript/sutra_impl_3_3.py` | python | grammar_engine | M11 | redesign | 12 | 1342 |
| `src/sanskript/sutra_impl_3_4.py` | python | grammar_engine | M11 | redesign | 12 | 966 |
| `src/sanskript/sutra_impl_4.py` | python | grammar_engine | M11 | redesign | 12 | 1666 |
| `src/sanskript/sutra_impl_5.py` | python | grammar_engine | M11 | redesign | 12 | 1261 |
| `src/sanskript/sutra_impl_6.py` | python | grammar_engine | M11 | redesign | 12 | 26 |
| `src/sanskript/sutra_impl_6_1.py` | python | grammar_engine | M11 | redesign | 12 | 1526 |
| `src/sanskript/sutra_impl_6_2.py` | python | grammar_engine | M11 | redesign | 12 | 643 |
| `src/sanskript/sutra_impl_6_3.py` | python | grammar_engine | M11 | redesign | 12 | 774 |
| `src/sanskript/sutra_impl_6_4.py` | python | grammar_engine | M11 | redesign | 12 | 452 |
| `src/sanskript/sutra_impl_7_1.py` | python | grammar_engine | M11 | redesign | 12 | 789 |
| `src/sanskript/sutra_impl_7_2.py` | python | grammar_engine | M11 | redesign | 12 | 782 |
| `src/sanskript/sutra_impl_7_3.py` | python | grammar_engine | M11 | redesign | 12 | 807 |
| `src/sanskript/sutra_impl_7_4.py` | python | grammar_engine | M11 | redesign | 12 | 708 |
| `src/sanskript/sutra_impl_8_1.py` | python | grammar_engine | M11 | redesign | 12 | 2226 |
| `src/sanskript/sutra_impl_8_2.py` | python | grammar_engine | M11 | redesign | 12 | 2022 |
| `src/sanskript/sutra_impl_8_3.py` | python | grammar_engine | M11 | redesign | 12 | 1367 |
| `src/sanskript/sutra_impl_8_4.py` | python | grammar_engine | M11 | redesign | 12 | 1018 |
| `src/sanskript/sutra_impl_base.py` | python | grammar_engine | M11 | redesign | 12 | 182 |
| `src/sanskript/sutra_logic.py` | python | grammar_engine | M11 | redesign | 12 | 1704 |
| `src/sanskript/syntax.py` | python | compiler | M11 | port_directly | 45 | 78 |
| `src/sanskript/tinanta.py` | python | grammar_engine | M11 | redesign | 12 | 511 |
| `src/sanskript/tinanta_grades.py` | python | grammar_engine | M11 | redesign | 12 | 82 |
| `src/sanskript/transliteration.py` | python | grammar_engine | M11 | redesign | 12 | 167 |
| `src/sanskript/type_catalog.py` | python | migration | M27 | keep_temporarily | 70 | 201 |
| `src/sanskript/type_checker.py` | python | other | M19 | port_directly | 30 | 1825 |
| `src/sanskript/vm.py` | python | vm | M9 | port_directly | 50 | 1904 |
| `src/sanskript/vm_phase3.py` | python | other | M19 | port_directly | 30 | 626 |
| `src/sanskript/vocabulary_catalog.py` | python | grammar_engine | M11 | redesign | 12 | 246 |
| `src/sanskript/voice.py` | python | other | M19 | port_directly | 30 | 40 |
| `src/sanskript/webapp.py` | python | web | M5 | redesign | 35 | 924 |
| `src/sanskript/yantra_patha.py` | python | vm | M9 | port_directly | 50 | 1171 |
| `ssk-vm/src/bytecode.rs` | rust | vm | M10 | port_directly | 50 | 318 |
| `ssk-vm/src/lib.rs` | rust | tooling | M4 | keep_temporarily | 55 | 5 |
| `ssk-vm/src/main.rs` | rust | tooling | M4 | keep_temporarily | 55 | 60 |
| `ssk-vm/src/vm.rs` | rust | vm | M9 | port_directly | 48 | 305 |
| `ssk-vm/tests/conformance.rs` | rust | tests | M15 | keep_temporarily | 30 | 42 |
| `tests/test_accent.py` | python | tests | M15 | keep_temporarily | 25 | 22 |
| `tests/test_adhyaya1.py` | python | tests | M15 | keep_temporarily | 25 | 417 |
| `tests/test_adhyaya123_engines.py` | python | tests | M15 | keep_temporarily | 25 | 143 |
| `tests/test_adhyaya23.py` | python | tests | M15 | keep_temporarily | 25 | 165 |
| `tests/test_adhyaya456.py` | python | tests | M15 | keep_temporarily | 25 | 91 |
| `tests/test_adhyaya45_engines.py` | python | tests | M15 | keep_temporarily | 25 | 102 |
| `tests/test_adhyaya678_engines.py` | python | tests | M15 | keep_temporarily | 25 | 145 |
| `tests/test_adhyaya7.py` | python | tests | M15 | keep_temporarily | 25 | 54 |
| `tests/test_adhyaya8.py` | python | tests | M15 | keep_temporarily | 25 | 54 |
| `tests/test_anga.py` | python | tests | M15 | keep_temporarily | 25 | 22 |
| `tests/test_avyaya.py` | python | tests | M15 | keep_temporarily | 25 | 39 |
| `tests/test_bytecode_conformance.py` | python | tests | M15 | keep_temporarily | 25 | 143 |
| `tests/test_canon_topics.py` | python | tests | M15 | keep_temporarily | 25 | 25 |
| `tests/test_cli_toolchain.py` | python | tests | M15 | keep_temporarily | 25 | 198 |
| `tests/test_collections.py` | python | tests | M15 | keep_temporarily | 25 | 95 |
| `tests/test_compiler_vm.py` | python | tests | M15 | keep_temporarily | 25 | 150 |
| `tests/test_completion_gate.py` | python | tests | M15 | keep_temporarily | 25 | 17 |
| `tests/test_control_flow.py` | python | tests | M15 | keep_temporarily | 25 | 73 |
| `tests/test_derivation.py` | python | tests | M15 | keep_temporarily | 25 | 54 |
| `tests/test_docs.py` | python | tests | M15 | keep_temporarily | 25 | 21 |
| `tests/test_errors.py` | python | tests | M15 | keep_temporarily | 25 | 29 |
| `tests/test_frame_registry.py` | python | tests | M15 | keep_temporarily | 25 | 58 |
| `tests/test_functions.py` | python | tests | M15 | keep_temporarily | 25 | 188 |
| `tests/test_grammar.py` | python | tests | M15 | keep_temporarily | 25 | 71 |
| `tests/test_grammar_canon.py` | python | tests | M15 | keep_temporarily | 25 | 174 |
| `tests/test_identifier_grammar.py` | python | tests | M15 | keep_temporarily | 25 | 43 |
| `tests/test_interpreter.py` | python | tests | M15 | keep_temporarily | 25 | 60 |
| `tests/test_metarules.py` | python | tests | M15 | keep_temporarily | 25 | 20 |
| `tests/test_morphology_synth.py` | python | tests | M15 | keep_temporarily | 25 | 217 |
| `tests/test_native_backends.py` | python | tests | M15 | keep_temporarily | 25 | 120 |
| `tests/test_native_levels.py` | python | tests | M15 | keep_temporarily | 25 | 65 |
| `tests/test_paninian_adhyaya12_real_effects.py` | python | tests | M15 | keep_temporarily | 25 | 99 |
| `tests/test_paninian_adhyaya3_real_effects.py` | python | tests | M15 | keep_temporarily | 25 | 100 |
| `tests/test_paninian_adhyaya678_real_effects.py` | python | tests | M15 | keep_temporarily | 25 | 79 |
| `tests/test_paninian_engine.py` | python | tests | M15 | keep_temporarily | 25 | 419 |
| `tests/test_paninian_real_effect_gate.py` | python | tests | M15 | keep_temporarily | 25 | 149 |
| `tests/test_performance_baseline.py` | python | tests | M15 | keep_temporarily | 25 | 18 |
| `tests/test_phase0_truth_gates.py` | python | tests | M15 | keep_temporarily | 25 | 116 |
| `tests/test_phase10_stdlib_core.py` | python | tests | M15 | keep_temporarily | 25 | 500 |
| `tests/test_phase11_algorithms_data_structures.py` | python | tests | M15 | keep_temporarily | 25 | 275 |
| `tests/test_phase12_diagnostics.py` | python | tests | M15 | keep_temporarily | 25 | 223 |
| `tests/test_phase13_memory_model.py` | python | tests | M15 | keep_temporarily | 25 | 178 |
| `tests/test_phase14_surakshita.py` | python | tests | M15 | keep_temporarily | 25 | 271 |
| `tests/test_phase15_rakshita_systems.py` | python | tests | M15 | keep_temporarily | 25 | 172 |
| `tests/test_phase16_arakshita.py` | python | tests | M15 | keep_temporarily | 25 | 213 |
| `tests/test_phase17_toolchain.py` | python | tests | M15 | keep_temporarily | 25 | 193 |
| `tests/test_phase18_vm_runtime.py` | python | tests | M15 | keep_temporarily | 25 | 132 |
| `tests/test_phase19_self_hosting.py` | python | tests | M15 | keep_temporarily | 25 | 131 |
| `tests/test_phase1_source_surface.py` | python | tests | M15 | keep_temporarily | 25 | 184 |
| `tests/test_phase20_native_backends.py` | python | tests | M15 | keep_temporarily | 25 | 82 |
| `tests/test_phase21_cross_platform.py` | python | tests | M15 | keep_temporarily | 25 | 384 |
| `tests/test_phase22_web_apps_games_research.py` | python | tests | M15 | keep_temporarily | 25 | 271 |
| `tests/test_phase22_web_apps_games_research_ml.py` | python | tests | M15 | keep_temporarily | 25 | 234 |
| `tests/test_phase23_concurrency_async.py` | python | tests | M15 | keep_temporarily | 25 | 574 |
| `tests/test_phase24_tooling.py` | python | tests | M15 | keep_temporarily | 25 | 783 |
| `tests/test_phase25_borrow_negatives.py` | python | tests | M15 | keep_temporarily | 25 | 69 |
| `tests/test_phase25_exhaustive_coverage.py` | python | tests | M15 | keep_temporarily | 25 | 1323 |
| `tests/test_phase25_testing_verification.py` | python | tests | M15 | keep_temporarily | 25 | 293 |
| `tests/test_phase26_documentation.py` | python | tests | M15 | keep_temporarily | 25 | 179 |
| `tests/test_phase27_migration.py` | python | tests | M15 | keep_temporarily | 25 | 214 |
| `tests/test_phase28_independence_milestones.py` | python | tests | M15 | keep_temporarily | 25 | 120 |
| `tests/test_phase2_core_syntax.py` | python | tests | M15 | keep_temporarily | 25 | 447 |
| `tests/test_phase3_data_types.py` | python | tests | M15 | keep_temporarily | 25 | 1389 |
| `tests/test_phase4_type_system.py` | python | tests | M15 | keep_temporarily | 25 | 908 |
| `tests/test_phase5_control_flow.py` | python | tests | M15 | keep_temporarily | 25 | 853 |
| `tests/test_phase6_functions.py` | python | tests | M15 | keep_temporarily | 25 | 561 |
| `tests/test_phase7_oop.py` | python | tests | M15 | keep_temporarily | 25 | 646 |
| `tests/test_phase8_functional_declarative.py` | python | tests | M15 | keep_temporarily | 25 | 556 |
| `tests/test_phase9_modules.py` | python | tests | M15 | keep_temporarily | 25 | 752 |
| `tests/test_phase_examples.py` | python | tests | M15 | keep_temporarily | 25 | 77 |
| `tests/test_phonology.py` | python | tests | M15 | keep_temporarily | 25 | 59 |
| `tests/test_predicate_audit.py` | python | tests | M15 | keep_temporarily | 25 | 15 |
| `tests/test_records.py` | python | tests | M15 | keep_temporarily | 25 | 90 |
| `tests/test_register_docs.py` | python | tests | M15 | keep_temporarily | 25 | 19 |
| `tests/test_rust_vm.py` | python | tests | M15 | keep_temporarily | 25 | 52 |
| `tests/test_samasa.py` | python | tests | M15 | keep_temporarily | 25 | 24 |
| `tests/test_sandhi.py` | python | tests | M15 | keep_temporarily | 25 | 97 |
| `tests/test_source_collections.py` | python | tests | M15 | keep_temporarily | 25 | 76 |
| `tests/test_source_directives.py` | python | tests | M15 | keep_temporarily | 25 | 127 |
| `tests/test_subanta.py` | python | tests | M15 | keep_temporarily | 25 | 111 |
| `tests/test_sutra_1_1_1.py` | python | tests | M15 | keep_temporarily | 25 | 22 |
| `tests/test_sutra_1_1_2.py` | python | tests | M15 | keep_temporarily | 25 | 22 |
| `tests/test_sutra_1_1_3.py` | python | tests | M15 | keep_temporarily | 25 | 55 |
| `tests/test_sutra_logic.py` | python | tests | M15 | keep_temporarily | 25 | 341 |
| `tests/test_syntax.py` | python | tests | M15 | keep_temporarily | 25 | 37 |
| `tests/test_text_primitives.py` | python | tests | M15 | keep_temporarily | 25 | 92 |
| `tests/test_tinanta.py` | python | tests | M15 | keep_temporarily | 25 | 45 |
| `tests/test_transliteration.py` | python | tests | M15 | keep_temporarily | 25 | 71 |
| `tests/test_type_catalog.py` | python | tests | M15 | keep_temporarily | 25 | 64 |
| `tests/test_vm_numeric_heap.py` | python | tests | M15 | keep_temporarily | 25 | 269 |
| `tests/test_vocabulary_balance.py` | python | tests | M15 | keep_temporarily | 25 | 173 |
| `tests/test_vocabulary_catalog.py` | python | tests | M15 | keep_temporarily | 25 | 36 |
| `tests/test_webapp_export.py` | python | tests | M15 | keep_temporarily | 25 | 74 |
| `tests/test_yantra_patha.py` | python | tests | M15 | keep_temporarily | 25 | 216 |
| `tools/_debug_parse_example.py` | python | tooling | M15 | remove | 55 | 11 |
| `tools/_gen_phase25_exhaustive_registry.py` | python | tooling | M15 | remove | 55 | 162 |
| `tools/_gen_phase25_exhaustive_tests.py` | python | tooling | M15 | remove | 55 | 134 |
| `tools/adversarial_audit_phases_1_28.py` | python | tooling | M15 | keep_temporarily | 55 | 213 |
| `tools/build_grammar_canon.py` | python | tooling | M15 | keep_temporarily | 55 | 602 |
| `tools/check_canon_completion.py` | python | tooling | M15 | keep_temporarily | 55 | 44 |
| `tools/check_feature_completion.py` | python | tooling | M15 | keep_temporarily | 55 | 56 |
| `tools/check_no_placeholder_completion.py` | python | tooling | M15 | keep_temporarily | 55 | 113 |
| `tools/generate_feature_matrix.py` | python | tooling | M15 | keep_temporarily | 55 | 306 |
| `tools/generate_independence_dashboard.py` | python | tooling | M15 | keep_temporarily | 55 | 183 |
| `tools/generate_module_inventory.py` | python | tooling | M15 | keep_temporarily | 55 | 147 |
| `tools/generate_phase25_golden.py` | python | tooling | M15 | keep_temporarily | 55 | 102 |
| `tools/generate_phase25_tests.py` | python | tooling | M15 | keep_temporarily | 55 | 203 |
| `tools/patch_schema_phase3.py` | python | tooling | M15 | keep_temporarily | 55 | 24 |
| `tools/patch_schema_phase8.py` | python | tooling | M15 | keep_temporarily | 55 | 24 |
| `tools/phase0_common.py` | python | tooling | M15 | keep_temporarily | 55 | 299 |
| `tools/phase25_coverage_map.py` | python | tooling | M15 | keep_temporarily | 55 | 36 |
| `tools/phase25_test_matrix.py` | python | tooling | M15 | keep_temporarily | 55 | 54 |
