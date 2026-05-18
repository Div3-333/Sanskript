import unittest

from sanskript.accent import Accent, assign_svarita, profile_accent


class AccentTests(unittest.TestCase):
    def test_profile_records_one_primary_accent(self) -> None:
        profile = profile_accent(("rāja", "puruṣa"), udatta_index=1)

        self.assertEqual(profile.sutra_range, "6.2")
        self.assertEqual(profile.primary.token, "puruṣa")
        self.assertEqual(profile.assignments[0].accent, Accent.ANUDATTA)

    def test_svarita_can_be_assigned_without_losing_domain(self) -> None:
        profile = assign_svarita(profile_accent(("deva", "atra")), "atra")

        self.assertEqual(profile.domain, "compound and pada accent domains")
        self.assertEqual(profile.assignments[1].accent, Accent.SVARITA)


if __name__ == "__main__":
    unittest.main()
