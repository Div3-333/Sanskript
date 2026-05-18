import json
import unittest
from pathlib import Path

from sanskript.adhyaya1 import (
    ADHYAYA1_RULES,
    expected_half_adhyaya_ids,
    implementation_note_for,
    implemented_sutra_ids,
    missing_rule_ids,
    rules_for_pada,
)
from sanskript.anga import DerivationContext, Suffix, guna
from sanskript.grammar import Analysis, Case, Gender, GrammaticalNumber, PartOfSpeech
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


ROOT = Path(__file__).resolve().parents[1]


class AdhyayaOneRegistryTests(unittest.TestCase):
    def test_registry_covers_first_half_adhyaya_one(self) -> None:
        self.assertEqual(len(expected_half_adhyaya_ids()), 148)
        self.assertEqual(missing_rule_ids(), ())
        self.assertEqual(len(rules_for_pada("1.1")), 75)
        self.assertEqual(len(rules_for_pada("1.2")), 73)
        self.assertEqual(implemented_sutra_ids(), frozenset(expected_half_adhyaya_ids()))

    def test_every_rule_has_evidence(self) -> None:
        for sutra_id, rule in ADHYAYA1_RULES.items():
            with self.subTest(sutra_id=sutra_id):
                self.assertTrue(rule.implemented)
                self.assertTrue(rule.title)
                self.assertTrue(rule.compiler_effect)
                self.assertIn("Hooks:", implementation_note_for(sutra_id))

    def test_local_canon_marks_the_half_adhyaya_as_implemented(self) -> None:
        canon = json.loads((ROOT / "data" / "grammar_canon.json").read_text(encoding="utf-8"))
        statuses = {
            item["title"]: item["status"]
            for item in canon["obligations"]
            if item["kind"] == "sutra" and item["title"] in expected_half_adhyaya_ids()
        }

        self.assertEqual(len(statuses), 148)
        self.assertEqual(set(statuses.values()), {"implemented"})


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


if __name__ == "__main__":
    unittest.main()
