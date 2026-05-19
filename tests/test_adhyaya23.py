import json
import unittest
from pathlib import Path

from sanskript.adhyaya2_atomic import ADHYAYA2_ATOMIC_SUTRAS
from sanskript.adhyaya23 import (
    ADHYAYA23_RULES,
    ImplementationMode,
    PADA_COUNTS,
    expected_adhyaya23_ids,
    implemented_sutra_ids,
    missing_rule_ids,
    partial_implementation_note_for,
    partial_sutra_ids,
    rules_for_pada,
)
from sanskript.derivation import KrtSuffix, derive
from sanskript.grammar import Analysis, Case, Gender, GrammaticalNumber, Lakara, Pada, PartOfSpeech, Person, Role
from sanskript.karaka import get_vibhakti
from sanskript.samasa import SamasaSense, SamasaType, create_compound, is_samartha
from sanskript.tinanta import (
    DHATUS,
    Dhatu,
    DhatuType,
    TimeContext,
    conjugate,
    create_derived_dhatu,
    get_lakara_for_time,
    get_substituted_dhatu,
    get_vikarana,
    is_ardhadhatuka,
    is_sarvadhatuka,
    tin_ending,
)


ROOT = Path(__file__).resolve().parents[1]


class AdhyayaTwoThreeRegistryTests(unittest.TestCase):
    def test_registry_covers_adhyaya_two_and_three(self) -> None:
        self.assertEqual(len(expected_adhyaya23_ids()), 898)
        self.assertEqual(missing_rule_ids(), ())
        self.assertEqual(len(implemented_sutra_ids()), 0)
        self.assertEqual(len(partial_sutra_ids()), 898)
        self.assertEqual(implemented_sutra_ids() | partial_sutra_ids(), frozenset(expected_adhyaya23_ids()))
        for pada, count in PADA_COUNTS.items():
            self.assertEqual(len(rules_for_pada(pada)), count)

    def test_adhyaya_two_metadata_does_not_count_as_discrete_logic(self) -> None:
        self.assertEqual(set(ADHYAYA2_ATOMIC_SUTRAS), {sid for sid in expected_adhyaya23_ids() if sid.startswith("2.")})
        for sutra_id in ADHYAYA2_ATOMIC_SUTRAS:
            rule = ADHYAYA23_RULES[sutra_id]
            with self.subTest(sutra_id=sutra_id):
                self.assertFalse(rule.implemented)
                self.assertTrue(rule.atomic)
                self.assertIn(rule.mode, {ImplementationMode.ATOMIC_EXECUTABLE, ImplementationMode.ATOMIC_FORMAL})
                self.assertTrue(rule.sutra_text_devanagari)
                self.assertTrue(rule.sutra_text_iast)
                self.assertTrue(rule.source)
                self.assertTrue(rule.anuvritti)
                self.assertTrue(rule.conditions)
                self.assertTrue(rule.counterexamples)
                self.assertNotIn(" rule ", rule.title)
                self.assertIn("Atomic metadata only", partial_implementation_note_for(sutra_id))

    def test_scaffolded_rules_do_not_count_as_implemented(self) -> None:
        for sutra_id, rule in ADHYAYA23_RULES.items():
            with self.subTest(sutra_id=sutra_id):
                self.assertTrue(rule.title)
                self.assertTrue(rule.compiler_effect)
                self.assertFalse(rule.implemented)
                self.assertIn("Required before completion", partial_implementation_note_for(sutra_id))

    def test_local_canon_marks_adhyaya_two_and_three_as_partial(self) -> None:
        canon = json.loads((ROOT / "data" / "grammar_canon.json").read_text(encoding="utf-8"))
        statuses = {
            item["title"]: item["status"]
            for item in canon["obligations"]
            if item["kind"] == "sutra" and item["title"] in expected_adhyaya23_ids()
        }

        self.assertEqual(len(statuses), 898)
        self.assertEqual({sid for sid, status in statuses.items() if status == "implemented"}, set(implemented_sutra_ids()))
        self.assertEqual({sid for sid, status in statuses.items() if status == "partial"}, set(partial_sutra_ids()))


class AdhyayaTwoThreeBehaviorTests(unittest.TestCase):
    def test_compound_and_case_rules_have_executable_anchors(self) -> None:
        deva = Analysis("devasya", "deva", PartOfSpeech.NOUN, case=Case.GENITIVE, gender=Gender.MASCULINE)
        purusha = Analysis("puruṣaḥ", "puruṣa", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.MASCULINE)
        pañca = Analysis("pañca", "pañcan", PartOfSpeech.NUMERAL, case=Case.ACCUSATIVE, value=5)
        phala = Analysis("phalāni", "phala", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.NEUTER)

        self.assertTrue(is_samartha([deva, purusha]))
        tatpurusha = create_compound([deva, purusha])
        dvigu = create_compound([pañca, phala])

        self.assertEqual(tatpurusha.type, SamasaType.TATPURUSHA)
        self.assertEqual(tatpurusha.sense, SamasaSense.SHASH_TAT)
        self.assertEqual(dvigu.type, SamasaType.DVIGU)
        self.assertEqual(dvigu.result_analysis.number, GrammaticalNumber.SINGULAR)
        self.assertEqual(get_vibhakti(Role.KARMAN), Case.ACCUSATIVE)
        self.assertEqual(get_vibhakti(Role.SAMPRADANA), Case.DATIVE)
        self.assertEqual(get_vibhakti(Role.KARMAN, companion_lemma="namas"), Case.ACCUSATIVE)

    def test_dhatu_derivation_krt_and_lakara_rules_have_executable_anchors(self) -> None:
        bhu = next(dhatu for dhatu in DHATUS if dhatu.lemma == "bhū")
        san = create_derived_dhatu(bhu, DhatuType.DESIDERATIVE)

        self.assertEqual(san.present_stem, "bubhūṣa")
        self.assertEqual(get_vikarana(4), "ya")
        self.assertEqual(derive("kṛ", KrtSuffix.GHAN).surface, "kāra")
        self.assertEqual(derive("bhū", KrtSuffix.LYUT).surface, "bhavana")
        self.assertEqual(get_lakara_for_time(TimeContext.PRESENT), Lakara.LAT)
        self.assertEqual(get_lakara_for_time(TimeContext.IMPERATIVE), Lakara.LOT)
        self.assertEqual(get_lakara_for_time(TimeContext.POTENTIAL), Lakara.VIDHILING)

    def test_tin_and_root_substitution_rules_have_executable_anchors(self) -> None:
        self.assertEqual(tin_ending(Lakara.LAT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR), "ti")
        self.assertTrue(is_sarvadhatuka(Lakara.LAT))
        self.assertTrue(is_ardhadhatuka(Lakara.LIT))
        self.assertEqual(get_substituted_dhatu(Dhatu("as", "as", Pada.PARASMAIPADA, "be"), Lakara.LRT).lemma, "bhū")

        bhu = next(dhatu for dhatu in DHATUS if dhatu.lemma == "bhū")
        self.assertEqual(conjugate(bhu, Lakara.LOT)[(Person.THIRD, GrammaticalNumber.SINGULAR)], "bhavatu")
        self.assertEqual(conjugate(bhu, Lakara.VIDHILING)[(Person.THIRD, GrammaticalNumber.SINGULAR)], "bhavet")


if __name__ == "__main__":
    unittest.main()
