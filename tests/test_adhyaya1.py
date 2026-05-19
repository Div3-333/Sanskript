import json
import unittest
from pathlib import Path

from sanskript.avyaya import is_avyaya_suffix, is_controlled_avyaya
from sanskript.adhyaya1 import (
    ADHYAYA1_RULES,
    ImplementationMode,
    expected_adhyaya1_ids,
    expected_half_adhyaya_ids,
    implemented_sutra_ids,
    missing_rule_ids,
    partial_implementation_note_for,
    partial_sutra_ids,
    rules_for_pada,
)
from sanskript.anga import DerivationContext, Suffix, guna, vrddhi
from sanskript.categories import (
    assign_technical_names,
    get_vowel_weight,
    has_single_sound_boundary,
    is_avasana,
    is_gha_suffix,
    is_ghu_root,
    is_nistha_suffix,
    is_samhita,
    is_sankhya_term,
    is_sarvanama_stem,
    is_sarvanamasthana_suffix,
    is_shat_numeral,
)
from sanskript.grammar import Analysis, Case, Gender, GrammaticalNumber, Pada, PartOfSpeech, Role, Samjna
from sanskript.karaka import explain_case, get_karaka_role
from sanskript.markers import analyze_it_markers
from sanskript.metarules import (
    augment_boundary,
    default_final_substitution_index,
    following_initial_substitution_index,
    genitive_marks_substitution_site,
    is_vibhasha_expression,
    mid_augment_index,
    whole_term_replacement_applies,
)
from sanskript.phonology import (
    best_substitute,
    hrasva_substitute_for_ec,
    is_anunasika,
    is_pragrhya,
    is_savarna,
    is_samyoga,
    is_ti,
    is_upadha,
    is_vrddha_word,
    pratyahara,
    rapara_substitute_for_ur,
    savarna_class,
    savarna_reference,
    tapara_matches_duration,
)
from sanskript.samasa import SamasaType, apply_ekashesha, create_compound
from sanskript.sutra_logic import implemented_logic_ids as real_implemented_logic_ids
from sanskript.voice import determine_available_padas


ROOT = Path(__file__).resolve().parents[1]
DISCRETE_ADHYAYA1_IDS = real_implemented_logic_ids() & frozenset(expected_adhyaya1_ids())


class AdhyayaOneRegistryTests(unittest.TestCase):
    def test_registry_covers_all_of_adhyaya_one(self) -> None:
        self.assertEqual(len(expected_half_adhyaya_ids()), 148)
        self.assertEqual(len(expected_adhyaya1_ids()), 351)
        self.assertEqual(missing_rule_ids(), ())
        self.assertEqual(len(rules_for_pada("1.1")), 75)
        self.assertEqual(len(rules_for_pada("1.2")), 73)
        self.assertEqual(len(rules_for_pada("1.3")), 93)
        self.assertEqual(len(rules_for_pada("1.4")), 110)
        self.assertEqual(implemented_sutra_ids(), DISCRETE_ADHYAYA1_IDS)
        self.assertEqual(partial_sutra_ids(), frozenset(expected_adhyaya1_ids()) - DISCRETE_ADHYAYA1_IDS)

    def test_only_rules_with_real_handlers_are_truth_gated_discrete_logic(self) -> None:
        for sutra_id, rule in ADHYAYA1_RULES.items():
            with self.subTest(sutra_id=sutra_id):
                self.assertTrue(rule.title)
                self.assertTrue(rule.compiler_effect)
                if sutra_id in DISCRETE_ADHYAYA1_IDS:
                    self.assertTrue(rule.implemented)
                    self.assertEqual(rule.mode, ImplementationMode.DISCRETE)
                    self.assertTrue(rule.discrete)
                    self.assertTrue(rule.sutra_text_devanagari)
                    self.assertTrue(rule.sutra_text_iast)
                    self.assertTrue(rule.conditions)
                    self.assertTrue(rule.counterexamples)
                    self.assertTrue(rule.reviewer_notes)
                else:
                    self.assertFalse(rule.implemented)

    def test_local_canon_marks_only_discrete_adhyaya_one_as_implemented(self) -> None:
        canon = json.loads((ROOT / "data" / "grammar_canon.json").read_text(encoding="utf-8"))
        statuses = {
            item["title"]: item["status"]
            for item in canon["obligations"]
            if item["kind"] == "sutra" and item["title"] in expected_adhyaya1_ids()
        }

        self.assertEqual(len(statuses), 351)
        self.assertEqual({sid for sid, status in statuses.items() if status == "implemented"}, set(DISCRETE_ADHYAYA1_IDS))
        self.assertEqual(
            {sid for sid, status in statuses.items() if status == "partial"},
            set(expected_adhyaya1_ids()) - set(DISCRETE_ADHYAYA1_IDS),
        )


class AdhyayaOneBehaviorTests(unittest.TestCase):
    def test_discrete_first_ten_sutras_have_positive_and_negative_behavior(self) -> None:
        dhatu_lopa = DerivationContext(suffix=Suffix("ta", is_ardhadhatuka=True), has_dhatu_lopa=True)
        ordinary_ardhadhatuka = DerivationContext(suffix=Suffix("ta", is_ardhadhatuka=True))
        kit_suffix = DerivationContext(suffix=Suffix("ta", markers=frozenset({"k"})))
        ngit_suffix = DerivationContext(suffix=Suffix("ta", markers=frozenset({"ṅ"})))
        listed_root = DerivationContext(root_lemma="dīdī", suffix=Suffix("ta"))

        self.assertEqual(guna("i", dhatu_lopa), "i")
        self.assertEqual(vrddhi("i", dhatu_lopa), "i")
        self.assertEqual(guna("i", ordinary_ardhadhatuka), "e")

        self.assertEqual(guna("i", kit_suffix), "i")
        self.assertEqual(guna("i", ngit_suffix), "i")
        self.assertEqual(guna("i", DerivationContext(suffix=Suffix("ta"))), "e")

        self.assertEqual(guna("i", listed_root), "i")
        self.assertEqual(guna("i", DerivationContext(root_lemma="bhū", suffix=Suffix("ta"))), "e")

        self.assertTrue(is_samyoga(["k", "t"]))
        self.assertFalse(is_samyoga(["k", "a"]))
        self.assertTrue(is_anunasika("ṅ"))
        self.assertFalse(is_anunasika("k"))
        self.assertTrue(is_savarna("a", "ā"))
        self.assertFalse(is_savarna("i", "u"))
        self.assertFalse(is_savarna("a", "k"))

    def test_discrete_pragrhya_sutras_have_positive_and_negative_behavior(self) -> None:
        dual_pragrhya = Analysis("devī", "deva", PartOfSpeech.NOUN, number=GrammaticalNumber.DUAL)
        singular_i_final = Analysis("nadī", "nadī", PartOfSpeech.NOUN, number=GrammaticalNumber.SINGULAR)
        adas_pragrhya = Analysis("amī", "adas", PartOfSpeech.PRONOUN)
        non_adas_mi = Analysis("amī", "anya", PartOfSpeech.PRONOUN)
        locative_pragrhya = Analysis("nadī", "nadī", PartOfSpeech.NOUN, case=Case.LOCATIVE)
        nominative_i_final = Analysis("nadī", "nadī", PartOfSpeech.NOUN, case=Case.NOMINATIVE)

        self.assertTrue(is_pragrhya(dual_pragrhya))
        self.assertFalse(is_pragrhya(singular_i_final))
        self.assertTrue(is_pragrhya(adas_pragrhya))
        self.assertFalse(is_pragrhya(non_adas_mi))
        self.assertTrue(is_pragrhya("o"))
        self.assertFalse(is_pragrhya("a"))
        self.assertTrue(is_pragrhya(locative_pragrhya))
        self.assertFalse(is_pragrhya(nominative_i_final))

    def test_discrete_technical_name_sutras_have_positive_and_negative_behavior(self) -> None:
        self.assertTrue(is_ghu_root("dā"))
        self.assertTrue(is_ghu_root("dhā"))
        self.assertFalse(is_ghu_root("dāp"))
        self.assertFalse(is_ghu_root("bhū"))

        self.assertTrue(has_single_sound_boundary("a"))
        self.assertTrue(has_single_sound_boundary("ai"))
        self.assertFalse(has_single_sound_boundary("agni"))

        self.assertTrue(is_gha_suffix("tarap"))
        self.assertTrue(is_gha_suffix("tamap"))
        self.assertFalse(is_gha_suffix("kta"))

        self.assertTrue(is_sankhya_term("bahu"))
        self.assertTrue(is_sankhya_term("ḍati"))
        self.assertFalse(is_sankhya_term("deva"))

        self.assertTrue(is_shat_numeral("ṣaṣ"))
        self.assertTrue(is_shat_numeral("pañcan"))
        self.assertTrue(is_shat_numeral("ḍati"))
        self.assertFalse(is_shat_numeral("rājan"))
        self.assertFalse(is_shat_numeral("vatu"))

        self.assertTrue(is_nistha_suffix("kta"))
        self.assertTrue(is_nistha_suffix("ktavatū"))
        self.assertFalse(is_nistha_suffix("lyuṭ"))

        self.assertTrue(is_sarvanama_stem("sarva"))
        self.assertTrue(is_sarvanama_stem("yad"))
        self.assertFalse(is_sarvanama_stem("deva"))

    def test_discrete_avyaya_and_sarvanamasthana_sutras_have_behavior(self) -> None:
        self.assertTrue(is_controlled_avyaya("ca"))
        self.assertTrue(is_controlled_avyaya("pra"))
        self.assertFalse(is_controlled_avyaya("deva"))

        self.assertTrue(is_avyaya_suffix("ktvā"))
        self.assertTrue(is_avyaya_suffix("tosun"))
        self.assertFalse(is_avyaya_suffix("kta"))

        upa = Analysis("upa", "upa", PartOfSpeech.INDECLINABLE)
        grama = Analysis("grāmam", "grāma", PartOfSpeech.NOUN, case=Case.ACCUSATIVE, gender=Gender.MASCULINE)
        avyayibhava = create_compound([upa, grama])
        tatpurusha = create_compound([
            Analysis("devasya", "deva", PartOfSpeech.NOUN, case=Case.GENITIVE, gender=Gender.MASCULINE),
            Analysis("puruṣaḥ", "puruṣa", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.MASCULINE),
        ])

        self.assertEqual(avyayibhava.type, SamasaType.AVYAYIBHAVA)
        self.assertIn(Samjna.AVYAYA, avyayibhava.result_analysis.samjnas)
        self.assertNotEqual(tatpurusha.type, SamasaType.AVYAYIBHAVA)

        self.assertTrue(is_sarvanamasthana_suffix("śi"))
        self.assertTrue(is_sarvanamasthana_suffix("su", Gender.MASCULINE))
        self.assertFalse(is_sarvanamasthana_suffix("su", Gender.NEUTER))
        self.assertFalse(is_sarvanamasthana_suffix("kta", Gender.MASCULINE))

        self.assertTrue(is_vibhasha_expression("na vā"))
        self.assertTrue(is_vibhasha_expression("na veti vibhāṣā"))
        self.assertFalse(is_vibhasha_expression("nityam"))

    def test_discrete_substitution_metasutras_have_behavior(self) -> None:
        self.assertEqual(augment_boundary("ṭ"), "initial")
        self.assertEqual(augment_boundary("k"), "final")
        self.assertIsNone(augment_boundary("m"))

        self.assertEqual(mid_augment_index("bhavati"), 6)
        self.assertIsNone(mid_augment_index("krt"))

        self.assertEqual(hrasva_substitute_for_ec("e"), "i")
        self.assertEqual(hrasva_substitute_for_ec("au"), "u")
        with self.assertRaisesRegex(ValueError, "ec vowel"):
            hrasva_substitute_for_ec("a")

        self.assertTrue(genitive_marks_substitution_site("ṣaṣṭhī"))
        self.assertFalse(genitive_marks_substitution_site("saptamī"))
        self.assertEqual(best_substitute("i", ["a", "e", "o"]), "e")
        self.assertEqual(rapara_substitute_for_ur("ṛ", "a"), "ar")
        self.assertEqual(rapara_substitute_for_ur("ḷ", "ā"), "āl")
        self.assertEqual(rapara_substitute_for_ur("i", "a"), "a")

        self.assertEqual(default_final_substitution_index("agni"), 3)
        self.assertIsNone(default_final_substitution_index(""))
        self.assertEqual(following_initial_substitution_index("agni"), 0)
        self.assertIsNone(following_initial_substitution_index(""))
        self.assertTrue(whole_term_replacement_applies("ab"))
        self.assertTrue(whole_term_replacement_applies("a", marker="ṅ"))
        self.assertTrue(whole_term_replacement_applies("a", marker="ś"))
        self.assertFalse(whole_term_replacement_applies("a"))

    def test_discrete_tail_sound_reference_sutras_have_behavior(self) -> None:
        self.assertEqual(is_ti("bhavati"), "i")
        self.assertEqual(is_ti("krt"), "krt")
        self.assertEqual(is_upadha("agni"), "n")
        self.assertIsNone(is_upadha("a"))

        self.assertIn("ā", savarna_reference("a"))
        self.assertEqual(savarna_reference("a", is_pratyaya=True), ())
        self.assertIn("ā", savarna_class("a"))
        self.assertTrue(tapara_matches_duration("a", "i"))
        self.assertFalse(tapara_matches_duration("a", "ā"))

        self.assertEqual(pratyahara("ac"), ("a", "i", "u", "ṛ", "ḷ", "e", "o", "ai", "au"))
        with self.assertRaisesRegex(ValueError, "Invalid pratyāhāra"):
            pratyahara("zz")

        self.assertTrue(is_vrddha_word("āgama"))
        self.assertFalse(is_vrddha_word("agni"))
        self.assertTrue(is_vrddha_word("tad", tyadadi=True))
        self.assertFalse(is_vrddha_word("tad"))
        self.assertTrue(is_vrddha_word("ekadeśa", eastern_name=True))
        self.assertFalse(is_vrddha_word("ekadeśa"))

    def test_discrete_it_marker_sutras_have_behavior(self) -> None:
        nasal_vowel = analyze_it_markers("bhū~")
        self.assertEqual(nasal_vowel.markers, frozenset({"ū"}))
        self.assertEqual(nasal_vowel.lemma, "bh")
        self.assertEqual(analyze_it_markers("bhū").markers, frozenset())

        final_hal = analyze_it_markers("pac")
        self.assertEqual(final_hal.markers, frozenset({"c"}))
        self.assertEqual(final_hal.lemma, "pa")
        self.assertEqual(analyze_it_markers("bhū").lemma, "bhū")

        self.assertEqual(analyze_it_markers("tas", kind="vibhakti").markers, frozenset())
        self.assertEqual(analyze_it_markers("tas", kind="vibhakti").lemma, "tas")
        self.assertEqual(analyze_it_markers("tas", kind="suffix").markers, frozenset({"s"}))

        root_marker = analyze_it_markers("ñibhū", kind="root")
        self.assertEqual(root_marker.markers, frozenset({"ñi"}))
        self.assertEqual(root_marker.lemma, "bhū")
        self.assertNotIn("ñi", analyze_it_markers("ñibhū", kind="suffix").markers)

        self.assertEqual(analyze_it_markers("ṣa").markers, frozenset({"ṣ"}))
        self.assertEqual(analyze_it_markers("ṣa", kind="root").markers, frozenset())
        self.assertEqual(analyze_it_markers("ci").markers, frozenset({"c"}))
        self.assertEqual(analyze_it_markers("pa").markers, frozenset())
        self.assertEqual(analyze_it_markers("ka").markers, frozenset({"k"}))
        self.assertEqual(analyze_it_markers("ka", is_taddhita=True).markers, frozenset())

    def test_discrete_samjna_and_boundary_sutras_have_behavior(self) -> None:
        feminine_i = Analysis("nadī", "nadī", PartOfSpeech.NOUN, gender=Gender.FEMININE)
        masculine_i = Analysis("hari", "hari", PartOfSpeech.NOUN, gender=Gender.MASCULINE)
        sakhi = Analysis("sakhi", "sakhi", PartOfSpeech.NOUN, gender=Gender.MASCULINE)
        nominative = Analysis("devaḥ", "deva", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.MASCULINE)
        bare = Analysis("deva", "deva", PartOfSpeech.NOUN, gender=Gender.MASCULINE)

        self.assertIn(Samjna.NADII, assign_technical_names(feminine_i).samjnas)
        self.assertNotIn(Samjna.NADII, assign_technical_names(masculine_i).samjnas)
        self.assertIn(Samjna.GHI, assign_technical_names(masculine_i).samjnas)
        self.assertNotIn(Samjna.GHI, assign_technical_names(sakhi).samjnas)

        self.assertEqual(get_vowel_weight("pa", 1), Samjna.LAGHU)
        self.assertEqual(get_vowel_weight("artha", 0), Samjna.GURU)
        self.assertEqual(get_vowel_weight("e", 0), Samjna.GURU)

        self.assertIn(Samjna.ANGA, assign_technical_names(bare, suffix_surface="am").samjnas)
        self.assertNotIn(Samjna.ANGA, assign_technical_names(bare).samjnas)
        self.assertIn(Samjna.PADA, assign_technical_names(nominative).samjnas)
        self.assertNotIn(Samjna.PADA, assign_technical_names(bare).samjnas)
        self.assertIn(Samjna.BHA, assign_technical_names(nominative, suffix_surface="ya").samjnas)
        self.assertNotIn(Samjna.BHA, assign_technical_names(nominative, suffix_surface="ta").samjnas)

        self.assertTrue(is_samhita("bhavati"))
        self.assertFalse(is_samhita(""))
        self.assertTrue(is_avasana("bhavati", 6))
        self.assertFalse(is_avasana("bhavati", 1))

    def test_discrete_karaka_sutras_have_behavior(self) -> None:
        self.assertEqual(get_karaka_role("", "separation_point"), Role.APADANA)
        self.assertNotEqual(get_karaka_role("", "ordinary_location"), Role.APADANA)
        self.assertEqual(get_karaka_role("bhī", "cause_of_fear"), Role.APADANA)
        self.assertIsNone(get_karaka_role("ruc", "cause_of_fear"))
        self.assertEqual(get_karaka_role("parā-ji", "unbearable"), Role.APADANA)
        self.assertIsNone(get_karaka_role("ji", "unbearable"))
        self.assertEqual(get_karaka_role("", "warded_off_object"), Role.APADANA)
        self.assertEqual(get_karaka_role("", "hidden_from"), Role.APADANA)
        self.assertEqual(get_karaka_role("", "teacher"), Role.APADANA)

        self.assertEqual(get_karaka_role("", "intended_recipient"), Role.SAMPRADANA)
        self.assertEqual(get_karaka_role("ruc", "pleased_one"), Role.SAMPRADANA)
        self.assertIsNone(get_karaka_role("bhū", "pleased_one"))
        self.assertEqual(get_karaka_role("", "most_effective_means"), Role.KARANA)
        self.assertEqual(get_karaka_role("", "substratum"), Role.ADHIKARANA)
        self.assertEqual(get_karaka_role("", "most_desired"), Role.KARMAN)
        self.assertEqual(get_karaka_role("", "independent_agent"), Role.KARTR)

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
