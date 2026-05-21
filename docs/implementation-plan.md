# Canon Implementation Plan

Sanskript's canon currently contains thousands of obligations. This document records the implementation order so we can move quickly without pretending that the whole grammar is already done.

## Completion Rule

A canon item is complete only when it has:

- a grammar note linking it to the local PDF canon;
- exact sutra text where the item is a sutra;
- inherited domain, conditions, and exceptions;
- rule-specific executable logic, not just a hook name or metadata record;
- accepted behavioral examples;
- rejected behavioral examples;
- tests that prove both acceptance and rejection.

## Phase 1: Sound And Form Infrastructure

Status: in progress.

Targets:

- Shiva Sutras and pratyāhāra.
- Vowel/consonant classes.
- IAST and Devanagari normalization.
- Savarṇa, it markers, and basic sandhi.
- Nominal and verbal feature models.

Initial support now lives in `src/sanskript/phonology.py`.

Batch status:

- Selected `1.1` sutras are implemented through real named handlers, with the older helper anchors retained for runtime behavior.
- `6.1`, `6.2`, `6.3`, and `6.4` have sound and anga helper anchors, but are not marked implemented until individual sutra handlers exist.
- `7.1`, `7.2`, `7.3`, `7.4`, `8.2`, `8.3`, and `8.4` are now marked `batch_partial` in the canon ledger.
- This means their sound/sandhi subsystem exists, but individual sutras in those later pādas are still not considered complete.
- Current support includes pratyāhāra expansion, sound classification, guṇa/vṛddhi classifiers, conservative savarṇa checks, IAST/Devanagari transliteration, first-pass vowel/visarga sandhi, accent profiles, and aṅga-operation scaffolds.

Truth-gated slice:

- The current real-handler gate contributes 3613 implemented sutras. The previous generated Adhyaya 1-6 metric is explicitly rejected.
- Adhyaya 1-3 now have a shared dry runtime layer in `src/sanskript/adhyaya123_engines.py`: `SutraPredicateSelectionEngine`, `SamjnaTechnicalEngine`, `MetaruleGovernanceEngine`, `SamasaDerivationEngine`, `KarakaVibhaktiEngine`, `SubantaSupEngine`, `PratyayaLopaEngine`, `DhatuSanadiEngine`, `KrtDerivationEngine`, and `TinantaLakaraEngine`. This layer composes existing predicates into derivational behavior without re-counting metadata as sutra completion.
- Runtime independence has begun: `ast.py`, `ir.py`, `compiler.py`, `bytecode.py`, and `vm.py` now form an explicit Sanskript-owned execution pipeline. The first VM is Python-hosted, but it executes Sanskript bytecode rather than treating Python control flow as the language semantics.

Initial accent and aṅga support now lives in `src/sanskript/accent.py` and `src/sanskript/anga.py`.

## Phase 2: Subanta And Kāraka

Status: in progress.

Targets:

- Prātipadika model.
- Sup endings.
- All eight cases and three numbers.
- Kāraka role interpretation.
- Pronouns and numerals.

Initial support now lives in `src/sanskript/subanta.py` and `src/sanskript/karaka.py`.

Batch status:

- Selected `1.4` sutras are implemented through real named handlers, with karaka and samjna helper anchors retained for runtime behavior.
- `2.1`, `2.2`, `2.3`, and `2.4` now have named executable handlers across samāsa, vibhakti, subanta, lopa, and dhātu-substitution domains.
- Current support includes sup technical endings, generated a-stem masculine/neuter forms, generated ā-stem feminine forms, first/second/third person pronoun forms, and case-to-kāraka explanations.

## Phase 3: Tiṅanta

Status: in progress.

Targets:

- Dhātu model.
- Lakāra system.
- Tiṅ endings.
- Parasmaipada and ātmanepada.
- Vikaraṇa and guṇa.
- Prayoga: kartari, karmaṇi, bhāve.

Batch status:

- `3.1`, `3.2`, `3.3`, and `3.4` now have named executable handlers for dhātu derivation, vikaraṇa, kṛt suffixing, lakāra choice, and tiṅ endings.
- Current support includes dhātu records, sanādi derived roots, vikaraṇa selection, lakāra time/mood mapping, tiṅ endings, and controlled kṛt derivation.

## Phase 4: Derivation

Status: in progress.

Targets:

- Kṛt.
- Taddhita.
- Derived roots: causative, desiderative, nominal, intensive.
- Participles.

Initial support now lives in `src/sanskript/derivation.py` and `src/sanskript/adhyaya45_engines.py`.

Batch status:

- `4.1`, `4.2`, `4.3`, `4.4`, `5.1`, `5.2`, `5.3`, and `5.4` have discrete per-sutra predicates, and Adhyāya 4-5 now have five shared derivational engines layered above those predicates.
- Current executable support derives feminine stems, taddhita suffix selections, semantic relations, taddhita surfaces, and samāsānta endings with recorded sutra id, suffix, semantic relation, surface, and operations. The next runtime-deepening step is widening the suffix-surface maps and special stem transformations while keeping the per-sutra predicates as the source of truth.

## Phase 5: Compounds And Sentences

Status: in progress.

Targets:

- Avyayībhāva.
- Tatpuruṣa.
- Bahuvrīhi.
- Dvandva.
- Agreement.
- Verbless sentences.
- Questions.
- Relative phrases.
- Avyaya and upasarga.
- Paninian metarule scaffolding for optionality, technical markers, and sentence-edge operations.

Initial compound support now lives in `src/sanskript/samasa.py`. Initial sentence and indeclinable support now lives in `src/sanskript/syntax.py` and `src/sanskript/avyaya.py`.

Batch status:

- Selected `1.3` sutras are implemented through real named handlers, with metarule and marker helpers retained for runtime behavior. `1.2` remains partial.
- `8.1` is now marked `batch_partial`.
- Current support includes a controlled avyaya registry, standard upasarga registry, sentence classification, subject-verb agreement checks, and metarule records for optionality, technical markers, domain carry, and late sentence-edge operations.
- Later non-Adhyāya 1-6 ranges here are still scaffolds that need individual completion work.

## Phase 6: Full Aṣṭādhyāyī Sweep

Targets:

- Every indexed sutra receives a specific implementation note.
- Sutras that are not executable compiler behavior receive explicit design treatment.
- The canon ledger has no `pending_design` obligations.

Sutra batch status:

- Every indexed Aṣṭādhyāyī sutra is now at least `partial` or `batch_partial`.
- 3613 sutras have real-handler executable implementations; the rest remain partial or batch-partial.
- Every outline topic now has at least partial treatment or an explicit non-executable canon-topic treatment.
- The next phase is adding real handlers sutra by sutra and upgrading Adhyaya 2-8 from partial or batch-partial to individual sutra implementations.
