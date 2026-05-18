from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TopicTreatmentKind(str, Enum):
    SOURCE_METADATA = "source_metadata"
    PEDAGOGICAL = "pedagogical"
    GRAMMAR_DOMAIN = "grammar_domain"
    SCRIPT_AND_TOOLING = "script_and_tooling"
    REFERENCE = "reference"


@dataclass(frozen=True)
class TopicTreatment:
    title: str
    kind: TopicTreatmentKind
    note: str


TOPIC_TREATMENTS: tuple[TopicTreatment, ...] = (
    TopicTreatment("Document Information", TopicTreatmentKind.SOURCE_METADATA, "tracked in the source registry"),
    TopicTreatment("Document Text", TopicTreatmentKind.SOURCE_METADATA, "tracked as indexed canon text without copying the source"),
    TopicTreatment("Document Credits", TopicTreatmentKind.SOURCE_METADATA, "tracked as source metadata"),
    TopicTreatment("Contents", TopicTreatmentKind.PEDAGOGICAL, "tracked as source outline structure"),
    TopicTreatment("Preface to the print edition", TopicTreatmentKind.PEDAGOGICAL, "tracked as source context"),
    TopicTreatment("Introduction", TopicTreatmentKind.PEDAGOGICAL, "tracked as source context"),
    TopicTreatment("About our guide", TopicTreatmentKind.PEDAGOGICAL, "tracked as guide context"),
    TopicTreatment("Review", TopicTreatmentKind.PEDAGOGICAL, "tracked as review coverage"),
    TopicTreatment("For beginners", TopicTreatmentKind.PEDAGOGICAL, "tracked for beginner documentation"),
    TopicTreatment("For experts", TopicTreatmentKind.PEDAGOGICAL, "tracked for advanced documentation"),
    TopicTreatment("Core lessons", TopicTreatmentKind.PEDAGOGICAL, "tracked for guide sequencing"),
    TopicTreatment("Lists", TopicTreatmentKind.REFERENCE, "tracked for reference material"),
    TopicTreatment("Grammatical Terms", TopicTreatmentKind.REFERENCE, "tracked for terminology"),
    TopicTreatment("The Sanskrit language", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked as language overview"),
    TopicTreatment("A summary of Sanskrit", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked as language overview"),
    TopicTreatment("An overview of the Aṣṭādhyāyī", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked as canon overview"),
    TopicTreatment("vyākaraṇa-praveśaḥ", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked as grammar-source overview"),
    TopicTreatment("Sanskrit for Beginners", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked as grammar-source overview"),
    TopicTreatment("ac sandhi", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in sandhi coverage"),
    TopicTreatment("Sandhi", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in sandhi coverage"),
    TopicTreatment("The nominal system", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in subanta coverage"),
    TopicTreatment("-i and -u stems", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in nominal-stem coverage"),
    TopicTreatment("-ṛ stems", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in nominal-stem coverage"),
    TopicTreatment("-ai, -o, and -au stems", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in nominal-stem coverage"),
    TopicTreatment("Consonant stems", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in nominal-stem coverage"),
    TopicTreatment("tad, etad, idam, and adas", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in pronominal coverage"),
    TopicTreatment("Number words", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in numeral coverage"),
    TopicTreatment("Verbs", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in tiṅanta coverage"),
    TopicTreatment("Verbs 1: Special tense-moods", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in tiṅanta coverage"),
    TopicTreatment("Special tense-moods", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in lakāra coverage"),
    TopicTreatment("The present tense", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in laṭ coverage"),
    TopicTreatment("The command mood", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in loṭ coverage"),
    TopicTreatment("The ordinary past tense", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in laṅ coverage"),
    TopicTreatment("The potential mood", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in vidhiliṅ coverage"),
    TopicTreatment("ātmanepada", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in pada coverage"),
    TopicTreatment("The bhū, div, tud, and cur classes", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in dhātu-class coverage"),
    TopicTreatment("The su, tan, and krī classes", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in dhātu-class coverage"),
    TopicTreatment("The ad and rudh classes", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in dhātu-class coverage"),
    TopicTreatment("The hu class", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in dhātu-class coverage"),
    TopicTreatment("karmaṇi and bhāve prayoga", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in prayoga coverage"),
    TopicTreatment("Verbs 2: Other tense-moods", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in extended lakāra coverage"),
    TopicTreatment("Other tense-moods", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in extended lakāra coverage"),
    TopicTreatment("The simple future tense", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in lṛṭ coverage"),
    TopicTreatment("The conditional mood", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in lṛṅ coverage"),
    TopicTreatment("The distant future tense", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in luṭ coverage"),
    TopicTreatment("The distant past tense", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in liṭ coverage"),
    TopicTreatment("The recent past tense", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in luṅ coverage"),
    TopicTreatment("The blessing mood", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in āśīrliṅ coverage"),
    TopicTreatment("Verbs 3: Derived roots", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in derivation coverage"),
    TopicTreatment("Causal roots", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in derived-root coverage"),
    TopicTreatment("Desiderative roots", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in derived-root coverage"),
    TopicTreatment("Nominal roots", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in derived-root coverage"),
    TopicTreatment("Intensive roots", TopicTreatmentKind.GRAMMAR_DOMAIN, "queued in derived-root coverage"),
    TopicTreatment("samāsa", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in compound coverage"),
    TopicTreatment("The dvandva", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in compound coverage"),
    TopicTreatment("The tatpuruṣa", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in compound coverage"),
    TopicTreatment("The bahuvrīhi", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in compound coverage"),
    TopicTreatment("The avyayībhāva", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in compound coverage"),
    TopicTreatment("avyaya", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in indeclinable coverage"),
    TopicTreatment("Relative phrases", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in syntax coverage"),
    TopicTreatment("Participles", TopicTreatmentKind.GRAMMAR_DOMAIN, "tracked in derivation coverage"),
    TopicTreatment("Old Devanagari", TopicTreatmentKind.SCRIPT_AND_TOOLING, "tracked as script variant context"),
    TopicTreatment("Vedic Devanagari", TopicTreatmentKind.SCRIPT_AND_TOOLING, "tracked as script variant context"),
    TopicTreatment("Other scripts", TopicTreatmentKind.SCRIPT_AND_TOOLING, "tracked as future script support"),
    TopicTreatment("Sanskrit software", TopicTreatmentKind.SCRIPT_AND_TOOLING, "tracked as tooling context"),
    TopicTreatment("Why use Sanskrit software?", TopicTreatmentKind.SCRIPT_AND_TOOLING, "tracked as tooling rationale"),
    TopicTreatment("The Harvard-Kyoto system", TopicTreatmentKind.SCRIPT_AND_TOOLING, "tracked as future ASCII transliteration context"),
    TopicTreatment("How to type in Sanskrit", TopicTreatmentKind.SCRIPT_AND_TOOLING, "tracked as authoring guidance"),
    TopicTreatment("How to use a Sanskrit-English dictionary", TopicTreatmentKind.SCRIPT_AND_TOOLING, "tracked as lexical workflow guidance"),
)


def treatment_for(title: str) -> TopicTreatment | None:
    if title.startswith("॥ अध्याय "):
        return TopicTreatment(title, TopicTreatmentKind.SOURCE_METADATA, "tracked as an Aṣṭādhyāyī chapter boundary")
    return next((treatment for treatment in TOPIC_TREATMENTS if treatment.title == title), None)


def treated_titles() -> frozenset[str]:
    return frozenset(treatment.title for treatment in TOPIC_TREATMENTS)
