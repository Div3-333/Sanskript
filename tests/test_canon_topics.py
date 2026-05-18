import unittest

from sanskript.canon_topics import TopicTreatmentKind, treatment_for, treated_titles


class CanonTopicTests(unittest.TestCase):
    def test_source_metadata_topics_have_explicit_treatment(self) -> None:
        treatment = treatment_for("Document Information")

        self.assertIsNotNone(treatment)
        self.assertEqual(treatment.kind, TopicTreatmentKind.SOURCE_METADATA)

    def test_chapter_boundaries_are_treated_without_literal_duplication(self) -> None:
        treatment = treatment_for("॥ अध्याय १ ॥")

        self.assertIsNotNone(treatment)
        self.assertEqual(treatment.kind, TopicTreatmentKind.SOURCE_METADATA)

    def test_script_tooling_topics_are_tracked(self) -> None:
        self.assertEqual(treatment_for("The Harvard-Kyoto system").kind, TopicTreatmentKind.SCRIPT_AND_TOOLING)
        self.assertIn("How to type in Sanskrit", treated_titles())


if __name__ == "__main__":
    unittest.main()
