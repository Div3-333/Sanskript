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

- `1.1` is implemented as part of the full Adhyāya 1 registry.
- `6.1`, `6.2`, `6.3`, and `6.4` are repair-tracked in the Adhyāya 4-6 registry; executable anchors remain partial until they receive atomic Paninian completion.
- `7.1`, `7.2`, `7.3`, `7.4`, `8.2`, `8.3`, and `8.4` are now marked `batch_partial` in the canon ledger.
- This means their sound/sandhi subsystem exists, but individual sutras in those later pādas are still not considered complete.
- Current support includes pratyāhāra expansion, sound classification, guṇa/vṛddhi classifiers, conservative savarṇa checks, IAST/Devanagari transliteration, first-pass vowel/visarga sandhi, accent profiles, and aṅga-operation scaffolds.

Implemented slice:

- Adhyāya 1 is implemented as a sutra-by-sutra registry. Adhyāya 2 through 6 are indexed as repair-tracked registries; no sutra in those ranges counts as implemented until it is promoted to atomic executable or atomic formal completion.

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

- `1.4` is implemented as part of the full Adhyāya 1 registry.
- `2.1`, `2.2`, `2.3`, and `2.4` are repair-tracked in the Adhyāya 2/3 registry; executable anchors remain partial until they receive atomic Paninian completion.
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

- `3.1`, `3.2`, `3.3`, and `3.4` are repair-tracked in the Adhyāya 2/3 registry; executable anchors remain partial until they receive atomic Paninian completion.
- Current support includes dhātu records, sanādi derived roots, vikaraṇa selection, lakāra time/mood mapping, tiṅ endings, and controlled kṛt derivation.

## Phase 4: Derivation

Status: in progress.

Targets:

- Kṛt.
- Taddhita.
- Derived roots: causative, desiderative, nominal, intensive.
- Participles.

Initial support now lives in `src/sanskript/derivation.py`.

Batch status:

- `4.1`, `4.2`, `4.3`, `4.4`, `5.1`, `5.2`, `5.3`, and `5.4` are repair-tracked in the Adhyāya 4-6 registry; executable anchors remain partial until they receive atomic Paninian completion.
- Current executable support includes controlled taddhita examples for descent, possession, and degree; other sutras in these pādas are represented as formal semantic compiler records until deeper derivation behavior is added.

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

- `1.2` and `1.3` are implemented as part of the full Adhyāya 1 registry.
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
- Adhyāya 1 has sutra-specific implemented records and tests. Adhyāya 2 through 6 must be upgraded from partial scaffolds into atomic implemented records before they can be called complete.
- Every outline topic now has at least partial treatment or an explicit non-executable canon-topic treatment.
- The next phase is full implementation: replacing partial and batch-partial scaffolds with sutra/topic-specific implemented behavior and tests.
