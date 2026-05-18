# Sanskript Charter

## The Aim

Sanskript exists to test a demanding idea: can a programming language be written as real Sanskrit, with the mechanics of the human language doing meaningful computational work?

The answer we will pursue is "yes, but only through a controlled Sanskrit." Full natural Sanskrit is rich, context-sensitive, and interpretive. A programming language must be deterministic. Sanskript will therefore define a deliberate subset of Sanskrit whose accepted utterances are grammatical, beautiful, mechanically checkable, and computationally exact.

## Non-Negotiables

1. Sanskrit grammar is not decoration.
2. Source code must not be an English-like syntax with Sanskrit keywords.
3. Operators are not random symbols unless the language layer explicitly permits them for tooling.
4. Word order should be flexible where Sanskrit morphology already carries the meaning.
5. The compiler must reject constructions that it cannot justify grammatically.
6. When computation needs a concept that Sanskrit does not express cleanly, we redesign the computational surface instead of forcing ugly Sanskrit.

## The Core Bet

The first durable abstraction is the sentence.

A Sanskript program is a sequence of grammatical utterances. Each utterance has:

- a kriyā, the verbal action;
- participants marked by vibhakti;
- kāraka-style roles inferred from the action frame;
- optional particles, compounds, and subordinate clauses as the language grows.

The compiler does not ask "which token appears after which operator?" first. It asks "what action is being expressed, and which participants fill that action?"

## Controlled Sanskrit, Not Broken Sanskrit

The language will use a declared subset. That subset may be small, but it should not be malformed.

Each public language feature should eventually have:

- a grammatical construction;
- accepted surface examples;
- rejected malformed examples;
- a semantic mapping;
- a source note or review note.

Until a construction is reviewed, it belongs to the experimental layer, not the polished language.

## Grammar Canon

The PDFs in `sources/` are the project's local grammar canon. Their extracted coverage ledger is generated into `data/grammar_canon.json` and summarized in `docs/grammar-canon.md`.

The final language must either implement every indexed topic and sutra-derived requirement or explicitly document why a topic is outside the executable subset. Until then, Sanskript is a progressing experiment, not a completed Sanskrit programming language.

## Purity Versus Practicality

The final user-facing language should favor Sanskrit integrity. The implementation may use normal compiler machinery internally: tokens, AST nodes, bytecode, tests, and intermediate representations. The magic belongs at the source-language boundary.

This distinction matters. Internals can be ordinary; source code cannot be theatrical mimicry.

## First Milestone

The first milestone is not a large standard library. It is a truthful compiler nucleus:

1. Parse a few valid Sanskrit sentence frames.
2. Recover roles from morphology rather than fixed position.
3. Execute simple state changes.
4. Report grammatical failures clearly.
5. Keep every accepted construction small enough to review.
