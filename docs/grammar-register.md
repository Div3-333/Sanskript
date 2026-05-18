# Grammar Register

This register is the guardrail for Sanskript's central promise: accepted source must be grammatical Sanskrit within a declared subset. Compiler support alone is not enough. Each construction needs a small grammar record, examples, and a review status.

Current status labels:

| Status | Meaning |
| --- | --- |
| `experimental` | Implemented and tested, but not yet reviewed by a Sanskrit expert. |
| `reviewed` | Checked against grammar references or expert review. |
| `polished` | Stable enough to teach as part of the public language. |

## NF-001: Controlled Nominal Forms

Status: `experimental`

The compiler accepts only declared nominal forms. This is deliberate. We do not infer arbitrary Sanskrit nouns yet, because incorrect declension would poison the source-language promise.

Current nominal stems:

| Lemma | Gender | Accepted forms | Computational role |
| --- | --- | --- | --- |
| `gaṇaka` | masculine | `gaṇakaḥ` | agent marker |
| `phala` | neuter | `phalaṃ`, `phalam`, `phale` | stored result |
| `mūlya` | neuter | `mūlyaṃ`, `mūlyam`, `mūlye` | stored value |
| `pada` | neuter | `padaṃ`, `padam`, `pade` | stored step/place |

The locative singular, such as `phale`, marks an `adhikaraṇa` location for assignment. The accusative singular, such as `phalaṃ`, marks a `karman` object for update or display.

## NUM-001: Small Cardinal Numerals

Status: `experimental`

The compiler accepts cardinals from 0 through 10 in object and instrumental roles.

Object examples:

```text
śūnyaṃ
ekaṃ
dve
trīṇi
catvāri
pañca
```

Instrumental examples:

```text
śūnyena
ekena
dvābhyāṃ
tribhiḥ
caturbhiḥ
pañcabhiḥ
```

The forms for `dvi`, `tri`, and `catur` are explicitly registered because these numerals are more visibly inflected than higher cardinals.

## VF-001: Locative Assignment With `nidadhāti`

Status: `experimental`

Shape:

```text
kartṛ? karman adhikaraṇa nidadhāti.
```

Example:

```text
gaṇakaḥ pañca phale nidadhāti.
```

Computational meaning:

```text
store 5 in phala
```

Rejected:

```text
gaṇakaḥ pañca nidadhāti.
```

The sentence lacks an `adhikaraṇa` participant, so the storage location is not grammatical enough for the compiler to infer.

## VF-002: Instrumental Increase With `vardhayati`

Status: `experimental`

Shape:

```text
kartṛ? karman karaṇa vardhayati.
```

Example:

```text
gaṇakaḥ phalaṃ dvābhyāṃ vardhayati.
```

Computational meaning:

```text
increase phala by 2
```

## VF-003: Object Display With `darśayati`

Status: `experimental`

Shape:

```text
kartṛ? karman darśayati.
```

Example:

```text
gaṇakaḥ phalaṃ darśayati.
```

Computational meaning:

```text
print phala
```

## VF-004: Instrumental Decrease With `nyūnayati`

Status: `experimental`

Shape:

```text
kartṛ? karman karaṇa nyūnayati.
```

Example:

```text
gaṇakaḥ padaṃ tribhiḥ nyūnayati.
```

Computational meaning:

```text
decrease pada by 3
```

## Notes

This register currently relies on small, explicit forms rather than full derivation. That is the sober path for now: the compiler should accept fewer forms correctly before it accepts many forms carelessly.

The supporting sound layer now includes first-pass pratyāhāra, transliteration, and sandhi modules. These are infrastructure, not yet a license to accept arbitrary Sanskrit source.
