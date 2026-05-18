# Canon Implementation Plan

Sanskript's canon currently contains thousands of obligations. This document records the implementation order so we can move quickly without pretending that the whole grammar is already done.

## Completion Rule

A canon item is complete only when it has:

- a grammar note linking it to the local PDF canon;
- a compiler/runtime representation where relevant;
- accepted examples;
- rejected examples;
- tests.

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

- `1.1`, `6.1`, `8.2`, `8.3`, and `8.4` are now marked `batch_partial` in the canon ledger.
- This means their sound/sandhi subsystem exists, but individual sutras are still not considered complete.
- Current support includes pratyāhāra expansion, sound classification, guṇa/vṛddhi classifiers, conservative savarṇa checks, IAST/Devanagari transliteration, and first-pass vowel/visarga sandhi.

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

- `1.4`, `2.1`, `2.2`, `2.3`, and `2.4` are now marked `batch_partial`.
- Current support includes sup technical endings, generated a-stem masculine/neuter forms, generated ā-stem feminine forms, first/second/third person pronoun forms, and case-to-kāraka explanations.

## Phase 3: Tiṅanta

Targets:

- Dhātu model.
- Lakāra system.
- Tiṅ endings.
- Parasmaipada and ātmanepada.
- Vikaraṇa and guṇa.
- Prayoga: kartari, karmaṇi, bhāve.

## Phase 4: Derivation

Status: in progress.

Targets:

- Kṛt.
- Taddhita.
- Derived roots: causative, desiderative, nominal, intensive.
- Participles.

Initial support now lives in `src/sanskript/derivation.py`.

Batch status:

- `4.1`, `4.2`, `4.3`, `4.4`, `5.1`, `5.2`, `5.3`, and `5.4` are now marked `batch_partial`.
- Current support is a controlled registry of kṛt and taddhita examples, not full derivation.

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

- `1.2`, `1.3`, and `8.1` are now marked `batch_partial`.
- Current support includes a controlled avyaya registry, standard upasarga registry, sentence classification, subject-verb agreement checks, and metarule records for optionality, technical markers, domain carry, and late sentence-edge operations.
- This is not a full sutra-by-sutra implementation yet; it is the batch scaffold needed before individual completion work.

## Phase 6: Full Aṣṭādhyāyī Sweep

Targets:

- Every indexed sutra receives a specific implementation note.
- Sutras that are not executable compiler behavior receive explicit design treatment.
- The canon ledger has no `pending_design` obligations.
