import unittest

from sanskript.metarules import RuleBehavior, directive, rules_for_range


class MetaRuleTests(unittest.TestCase):
    def test_first_chapter_metarule_ranges_are_registered(self) -> None:
        self.assertGreaterEqual(len(rules_for_range("1.2")), 3)
        self.assertGreaterEqual(len(rules_for_range("1.3")), 2)
        self.assertEqual(rules_for_range("8.1")[0].behavior, RuleBehavior.OVERRIDE)

    def test_directive_preserves_optional_paninian_choice(self) -> None:
        rule = directive("bhū + vā", "bhavati/bhavati vā", RuleBehavior.OPTIONALITY, optional=True)

        self.assertTrue(rule.optional)
        self.assertEqual(rule.rule.name, "vā-option")


if __name__ == "__main__":
    unittest.main()
