import json
import unittest
from pathlib import Path

from sanskript.adhyaya1 import (
    ADHYAYA1_RULES,
    expected_adhyaya1_ids,
    expected_half_adhyaya_ids,
    implemented_sutra_ids,
    missing_rule_ids,
    partial_implementation_note_for,
    partial_sutra_ids,
    rules_for_pada,
)
from sanskript.anga import DerivationContext, Suffix, guna
from sanskript.categories import assign_technical_names, get_vowel_weight, is_avasana, is_samhita
from sanskript.grammar import Analysis, Case, Gender, GrammaticalNumber, Pada, PartOfSpeech, Role, Samjna
from sanskript.karaka import explain_case, get_karaka_role
from sanskript.markers import analyze_it_markers
from sanskript.phonology import (
    best_substitute,
    hrasva_substitute_for_ec,
    is_anunasika,
    is_pragrhya,
    is_samyoga,
    is_ti,
    is_vrddha_word,
    savarna_class,
)
from sanskript.samasa import apply_ekashesha
from sanskript.voice import determine_available_padas


ROOT = Path(__file__).resolve().parents[1]


class AdhyayaOneRegistryTests(unittest.TestCase):
    def test_registry_covers_all_of_adhyaya_one(self) -> None:
        self.assertEqual(len(expected_half_adhyaya_ids()), 148)
        self.assertEqual(len(expected_adhyaya1_ids()), 351)
        self.assertEqual(missing_rule_ids(), ())
        self.assertEqual(len(rules_for_pada("1.1")), 75)
        self.assertEqual(len(rules_for_pada("1.2")), 73)
        self.assertEqual(len(rules_for_pada("1.3")), 93)
        self.assertEqual(len(rules_for_pada("1.4")), 110)
        self.assertEqual(implemented_sutra_ids(), frozenset())
        self.assertEqual(partial_sutra_ids(), frozenset(expected_adhyaya1_ids()))

    def test_every_rule_is_truthfully_partial_until_discrete_logic_exists(self) -> None:
        for sutra_id, rule in ADHYAYA1_RULES.items():
            with self.subTest(sutra_id=sutra_id):
                self.assertFalse(rule.implemented)
                self.assertTrue(rule.title)
                self.assertTrue(rule.compiler_effect)
                self.assertIn("Required before completion", partial_implementation_note_for(sutra_id))

    def test_local_canon_marks_adhyaya_one_as_partial(self) -> None:
        canon = json.loads((ROOT / "data" / "grammar_canon.json").read_text(encoding="utf-8"))
        statuses = {
            item["title"]: item["status"]
            for item in canon["obligations"]
            if item["kind"] == "sutra" and item["title"] in expected_adhyaya1_ids()
        }

        self.assertEqual(len(statuses), 351)
        self.assertEqual(set(statuses.values()), {"partial"})


class AdhyayaOneBehaviorTests(unittest.TestCase):
    def test_sound_definitions_and_substitution_metarules_are_executable(self) -> None:
        self.assertTrue(is_samyoga(["k", "t"]))
        self.assertFalse(is_samyoga(["k", "a"]))
        self.assertTrue(is_anunasika("ṅ"))
        self.assertIn("ā", savarna_class("a"))
        self.assertEqual(best_substitute("i", ["a", "e", "o"]), "e")
        self.assertEqual(hrasva_substitute_for_ec("au"), "u")
        self.assertEqual(is_ti("bhavati"), "i")
        self.assertTrue(is_vrddha_word("āgama"))
        self.assertTrue(is_vrddha_word("ekadeśa", eastern_name=True))
        self.assertTrue(is_pragrhya("o"))
        dual_pragrhya = Analysis(
            "devī",
            "deva",
            PartOfSpeech.NOUN,
            number=GrammaticalNumber.DUAL,
        )
        locative_pragrhya = Analysis("nadī", "nadī", PartOfSpeech.NOUN, case=Case.LOCATIVE)
        self.assertTrue(is_pragrhya(dual_pragrhya))
        self.assertTrue(is_pragrhya(locative_pragrhya))

    def test_guna_blocking_uses_kit_ngit_and_dhatu_lopa_contexts(self) -> None:
        dhatu_lopa = DerivationContext(
            suffix=Suffix("ta", is_ardhadhatuka=True),
            has_dhatu_lopa=True,
        )
        kit_suffix = DerivationContext(suffix=Suffix("ta", markers=frozenset({"k"})))
        lit_after_bhu = DerivationContext(root_lemma="bhū", suffix=Suffix("liṭ", is_lit=True))

        self.assertEqual(guna("i", dhatu_lopa), "i")
        self.assertEqual(guna("i", kit_suffix), "i")
        self.assertTrue(lit_after_bhu.get_is_kit())

    def test_ekashesha_rules_choose_paninian_remainders(self) -> None:
        masculine = Analysis("devaḥ", "deva", PartOfSpeech.NOUN, gender=Gender.MASCULINE)
        feminine = Analysis("devī", "devī", PartOfSpeech.NOUN, gender=Gender.FEMININE)
        father = Analysis("pitā", "pitṛ", PartOfSpeech.NOUN, gender=Gender.MASCULINE)
        mother = Analysis("mātā", "mātṛ", PartOfSpeech.NOUN, gender=Gender.FEMININE)
        bull = Analysis("goḥ", "go", PartOfSpeech.NOUN, gender=Gender.MASCULINE)
        cow = Analysis("gauḥ", "go", PartOfSpeech.NOUN, gender=Gender.FEMININE)

        self.assertEqual(apply_ekashesha([feminine, masculine]).lemma, "deva")
        father_remainder = apply_ekashesha([mother, father])
        self.assertIsNotNone(father_remainder)
        self.assertEqual(father_remainder.lemma, "pitṛ")
        self.assertEqual(father_remainder.number, GrammaticalNumber.DUAL)
        self.assertEqual(apply_ekashesha([bull, cow]).gender, Gender.FEMININE)

    def test_it_marker_and_pada_rules_are_executable(self) -> None:
        self.assertEqual(analyze_it_markers("bhū~").markers, frozenset({"ū"}))
        self.assertEqual(analyze_it_markers("pac").lemma, "pa")
        self.assertEqual(analyze_it_markers("tas", kind="vibhakti").markers, frozenset())
        self.assertEqual(determine_available_padas(frozenset({"ṅ"})), {Pada.ATMANEPADA})
        self.assertEqual(determine_available_padas(frozenset({"ñ"}), has_reflexive_result=True), {Pada.ATMANEPADA})
        self.assertEqual(determine_available_padas(frozenset()), {Pada.PARASMAIPADA})

    def test_samjna_and_karaka_rules_are_executable(self) -> None:
        feminine_i = Analysis("nadī", "nadī", PartOfSpeech.NOUN, gender=Gender.FEMININE)
        neuter_locative = Analysis("phale", "phala", PartOfSpeech.NOUN, case=Case.LOCATIVE)

        self.assertIn(Samjna.NADII, assign_technical_names(feminine_i).samjnas)
        self.assertIn(Samjna.ANGA, assign_technical_names(neuter_locative, suffix_surface="am").samjnas)
        self.assertEqual(get_vowel_weight("artha", 0), Samjna.GURU)
        self.assertEqual(get_karaka_role("bhī", "cause_of_fear"), Role.APADANA)
        self.assertEqual(get_karaka_role("ruc", "pleased_one"), Role.SAMPRADANA)
        self.assertEqual(explain_case(Case.INSTRUMENTAL).role, Role.KARANA)
        self.assertTrue(is_samhita("bhavati"))
        self.assertTrue(is_avasana("bhavati", 6))


if __name__ == "__main__":
    unittest.main()
