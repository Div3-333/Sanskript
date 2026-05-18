# Morphological Feature Lattice

Sanskript should exploit Sanskrit's grammatical richness, but not by turning endings into arbitrary opcode numbers. The rule is:

> A grammatical feature may become computationally significant only when its Sanskrit function gives us a defensible semantic axis.

## Correction To The Raw Matrix

The tempting matrix is too broad if stated as "nouns have cases, genders, numbers, and persons" or "finite verbs have tenses, genders, numbers, and persons."

More accurate:

- Nominals have case, gender, and number.
- Pronouns also encode person.
- Finite verbs encode person, number, tense or mood, and pada/voice-like behavior.
- Participles and verbal adjectives can encode gender, case, and number because they behave like nominals.
- Vocative is traditionally treated as part of the first case in some Sanskrit presentations, but for compiler design it is useful to track separately.

This distinction matters because Sanskript must feel like Sanskrit, not like a lookup table hidden behind Sanskrit endings.

## Nominal Axes

| Feature | Sanskrit domain | Sanskript use |
| --- | --- | --- |
| Case/vibhakti | role in a sentence | dataflow role, storage locus, source, recipient, context |
| Gender/liṅga | lexical agreement class | type family only when the lexeme already supports it |
| Number/vacana | singular, dual, plural | scalar, pair, collection/sequence arity |
| Person/puruṣa | pronouns, not ordinary nouns | binding perspective through pronouns later |

The current compiler already uses case as a real semantic axis:

- accusative/karman: value or object acted on;
- instrumental/karaṇa: means, amount, or tool;
- locative/adhikaraṇa: storage location.

## Verbal Axes

| Feature | Sanskrit domain | Sanskript use |
| --- | --- | --- |
| Lakāra | tense/mood | execution mode, scheduling, assertion mode, commands, counterfactuals |
| Person | first, second, third | relation to current evaluator, addressed agent, external subject |
| Number | singular, dual, plural | one actor, paired actors, grouped actors |
| Pada | parasmaipada/ātmanepada | effect direction, only where grammar supports it |
| Prayoga | active/passive/impersonal constructions | role remapping without changing core action |

We will be especially cautious with pada. Traditional names suggest "for another" and "for oneself," but later Sanskrit does not maintain a simple semantic distinction for every verb. Sanskript may use this axis only in controlled frames where the meaning is reviewed.

## The Design Pattern

Instead of assigning every possible form a random function, we build a lattice:

```text
lexeme + morphology + frame -> meaning
```

For example:

```text
phale pañca nidadhāti
```

means assignment because:

- `nidadhāti` declares a frame that requires a karman and adhikaraṇa;
- `pañca` fills the karman value;
- `phale` fills the locative adhikaraṇa storage target.

The same principle will scale to conditionals, loops, functions, and modules.

## Near-Term Semantic Assignments

Planned, subject to review:

| Axis | Possible computational use |
| --- | --- |
| Ablative | source values, lower bounds, comparison base |
| Dative | destinations, callbacks, recipients |
| Genitive | ownership, module membership, field access |
| Locative | storage, scope, execution context |
| Dual | pairs, two-branch choice, binary relations |
| Plural | lists, sets, repeated application |
| Imperative/loṭ | direct commands or declarations |
| Optative/vidhiliṅ | conditional or potential computation |
| Future/lṛṭ | deferred computation |
| Past/liṭ/laṅ/luṅ | trace, replay, historical state |

The lattice lets the language become dense without becoming fake.

