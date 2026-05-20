import unittest

from sanskript.adhyaya123_engines import (
    DhatuSanadiEngine,
    KarakaVibhaktiEngine,
    KrtDerivationEngine,
    MetaruleGovernanceEngine,
    PratyayaLopaEngine,
    SamasaDerivationEngine,
    SamjnaTechnicalEngine,
    SubantaSupEngine,
    SutraPredicateSelectionEngine,
    TinantaLakaraEngine,
    classify_technical_names,
    conjugate_tinanta123,
    decline_subanta123,
    derive_compound123,
    derive_dhatu123,
    derive_krt123,
    select_vibhakti123,
)
from sanskript.derivation import KrtSuffix
from sanskript.grammar import Analysis, Case, Gender, GrammaticalNumber, Lakara, Pada, PartOfSpeech, Person, Role, Samjna
from sanskript.samasa import SamasaType
from sanskript.subanta import DeclensionStem, StemPattern
from sanskript.tinanta import DHATUS, Dhatu, DhatuType, TimeContext, TinEnding


class AdhyayaOneTwoThreeEngineTests(unittest.TestCase):
    def test_selector_runs_the_truth_gated_registry(self) -> None:
        selector = SutraPredicateSelectionEngine()

        applied = selector.apply("1.1.20", {"root": "dā"})
        matches = selector.select({"role": Role.KARMAN}, prefixes=("2.",))

        self.assertGreater(len(selector.implemented_ids()), 1000)
        self.assertEqual(applied.sutra_id, "1.1.20")
        self.assertEqual(applied.operator, "samjna")
        self.assertIn("2.3.2", {sutra.sutra_id for sutra in matches})

    def test_samjna_engine_classifies_names_markers_and_weight(self) -> None:
        result = classify_technical_names("dā", suffix="kta", marker_upadesha="tak")
        weight = SamjnaTechnicalEngine().vowel_weight("akta", 0)

        self.assertIn(Samjna.GHU, result.samjnas)
        self.assertIn(Samjna.NISTHA, result.samjnas)
        self.assertEqual(result.marker_analysis.lemma, "ta")
        self.assertIn("1.1.20", result.sutra_ids)
        self.assertIn("1.1.26", result.sutra_ids)
        self.assertIn("1.3.3", result.sutra_ids)
        self.assertIn("1.3.9", result.sutra_ids)
        self.assertEqual(weight.samjnas, frozenset({Samjna.GURU}))
        self.assertIn("1.4.11", weight.sutra_ids)

    def test_metarule_engine_governs_substitution_and_augments(self) -> None:
        engine = MetaruleGovernanceEngine()
        site = engine.substitution_site("agni", substitute="ab")
        augment = engine.augment_position("bhavati", "m")

        self.assertEqual(site.target_index, 3)
        self.assertEqual(site.target_scope, "whole-term")
        self.assertEqual(site.sutra_ids, ("1.1.49", "1.1.52", "1.1.55"))
        self.assertEqual(augment.target_index, 6)
        self.assertEqual(augment.sutra_ids, ("1.1.47",))

    def test_samasa_engine_derives_compounds_through_adhyaya_two_rules(self) -> None:
        deva = Analysis("devasya", "deva", PartOfSpeech.NOUN, case=Case.GENITIVE, gender=Gender.MASCULINE)
        purusha = Analysis("puruṣaḥ", "puruṣa", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.MASCULINE)

        result = derive_compound123([deva, purusha])

        self.assertEqual(result.compound.type, SamasaType.TATPURUSHA)
        self.assertEqual(result.compound.surface, "devapuruṣaḥ")
        self.assertIn("2.1.22", result.sutra_ids)
        self.assertIn("2.4.71", result.sutra_ids)
        self.assertIn("internal-sup-lopa", result.operations)

    def test_karaka_vibhakti_engine_links_roles_to_cases(self) -> None:
        karman = select_vibhakti123(role=Role.KARMAN)
        recipient = KarakaVibhaktiEngine().select_case(semantic_role_context="intended_recipient")

        self.assertEqual(karman.case, Case.ACCUSATIVE)
        self.assertEqual(karman.sutra_ids, ("2.3.2",))
        self.assertEqual(recipient.role, Role.SAMPRADANA)
        self.assertEqual(recipient.case, Case.DATIVE)
        self.assertIn("1.4.32", recipient.sutra_ids)
        self.assertIn("2.3.36", recipient.sutra_ids)

    def test_subanta_and_lopa_engines_cover_nominal_and_elision_work(self) -> None:
        stem = DeclensionStem("deva", StemPattern.A_MASCULINE, Gender.MASCULINE, "deity")
        declined = decline_subanta123(stem, case=Case.NOMINATIVE, number=GrammaticalNumber.SINGULAR)
        lopa = PratyayaLopaEngine()
        substituted = lopa.substitute_dhatu(Dhatu("ad", "ad", Pada.PARASMAIPADA, "eat"), Lakara.LRT)
        ending = TinEnding(Lakara.LAT, Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR, "ti")
        luk = lopa.luk(Dhatu("ad", "ad", Pada.PARASMAIPADA, "eat"), ending)

        self.assertEqual(declined.requested_form, "devaḥ")
        self.assertEqual(declined.sup, "su")
        self.assertIn("1.4.103", declined.sutra_ids)
        self.assertEqual(substituted.output.lemma, "jagdh")
        self.assertEqual(substituted.sutra_ids, ("2.4.36",))
        self.assertTrue(luk.luk_applies)
        self.assertEqual(luk.sutra_ids, ("2.4.72",))

    def test_dhatu_krt_and_tinanta_engines_cover_adhyaya_three_work(self) -> None:
        bhu = next(dhatu for dhatu in DHATUS if dhatu.lemma == "bhū")
        san = derive_dhatu123(bhu, DhatuType.DESIDERATIVE)
        vikarana = DhatuSanadiEngine().vikarana(4)
        krt = derive_krt123("kṛ", KrtSuffix.NVUL)
        tin = TinantaLakaraEngine()
        lakara, lakara_sutra = tin.lakara_for_time(TimeContext.POTENTIAL)
        lot = conjugate_tinanta123(bhu, Lakara.LOT, person=Person.THIRD, number=GrammaticalNumber.SINGULAR)

        self.assertEqual(san.output.present_stem, "bubhūṣa")
        self.assertEqual(san.sutra_ids, ("3.1.5",))
        self.assertEqual(vikarana.vikarana, "ya")
        self.assertEqual(vikarana.sutra_ids, ("3.1.69",))
        self.assertEqual(krt.derived.surface, "kāraka")
        self.assertEqual(krt.sutra_ids, ("3.2.135",))
        self.assertEqual(lakara, Lakara.VIDHILING)
        self.assertEqual(lakara_sutra.sutra_id, "3.3.161")
        self.assertEqual(lot.requested_form, "bhavatu")
        self.assertIn("3.4.86", lot.sutra_ids)

    def test_public_engine_classes_are_the_dry_adapters(self) -> None:
        engines = (
            SutraPredicateSelectionEngine(),
            SamjnaTechnicalEngine(),
            MetaruleGovernanceEngine(),
            SamasaDerivationEngine(),
            KarakaVibhaktiEngine(),
            SubantaSupEngine(),
            PratyayaLopaEngine(),
            DhatuSanadiEngine(),
            KrtDerivationEngine(),
            TinantaLakaraEngine(),
        )

        self.assertEqual(len(engines), 10)


if __name__ == "__main__":
    unittest.main()
