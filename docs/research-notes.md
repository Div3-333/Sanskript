# Research Notes

These notes record the grammar and computational-linguistics anchors for the design. They are not a full bibliography.

Accessed: 2026-05-18.

## Kāraka and Vibhakti

The prototype leans on the Pāṇinian idea that participants in an action can be understood through kāraka-style roles. Learn Sanskrit Online summarizes the six central kārakas under the Aṣṭādhyāyī's kāraka section, including apādāna, sampradāna, karaṇa, adhikaraṇa, karma, and kartṛ.

Useful starting point:

- https://learnsanskrit.org/vyakarana/subanta-1/karaka/

## Sup Endings

Nominal inflection is essential because Sanskript should recover meaning from forms, not from fixed token slots. The sup pratyāhāra and its 21 endings are the long-term basis for nominal analysis.

Useful starting point:

- https://learnsanskrit.org/vyakarana/subanta-1/sup/

## Nominal Feature Axes

Learn Sanskrit Online summarizes that nouns have fixed grammatical gender and that Sanskrit has eight cases, with case marking roles such as subject, object, means, source, and context. This supports Sanskript's case-driven role model while warning us not to invent person for ordinary nouns.

Useful starting point:

- https://www.learnsanskrit.org/guide/nominals/gender-case-and-number/

## Present Tense Verbs

The prototype begins with present-tense finite verbs because they are simple and familiar, and because the first language layer uses straightforward sentence actions.

Useful starting point:

- https://www.learnsanskrit.org/guide/verbs-1/the-present-tense/

## Pada And Verb Semantics

Parasmaipada and ātmanepada are tempting computational axes, but Learn Sanskrit Online cautions that the semantic distinction is incomplete in the Aṣṭādhyāyī and mostly absent in later Sanskrit. Sanskript should therefore use pada semantically only in carefully reviewed frames.

Useful starting point:

- https://www.learnsanskrit.org/vyakarana/tinanta/parasmaipada-and-atmanepada/

## Lakāra

The lakāra system gives Sanskript a principled path for execution modes: present action, command, potential, future scheduling, past tracing, and counterfactuals. We should still introduce these one reviewed construction at a time.

Useful starting point:

- https://hrishim.github.io/sanskrit_notes/notes/lakaras.html

## Numerals

Small cardinal numerals are irregular enough that Sanskript registers their accepted surface forms explicitly. Learn Sanskrit Online notes that Sanskrit numerals are irregular, and its usage notes show case forms such as `caturbhiḥ` for the instrumental. Other reference tables also list forms such as `ekena`, `dvābhyām`, `tribhiḥ`, `caturbhiḥ`, and `pañcabhiḥ`.

Useful starting points:

- https://learnsanskrit.org/ends/numbers/use/
- https://oursanskrit.com/sanskrit-grammar-reference/numerals/

## Computational Sandhi

Sandhi must eventually become a first-class compiler component. Rama and Lakshmanan's 2009 paper frames euphonic conjunctions as an early computational requirement for Sanskrit processing.

Useful starting point:

- https://arxiv.org/abs/0911.0894
