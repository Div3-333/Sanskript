import unittest

from tools.check_canon_completion import completion_counts, incomplete_obligations, load_obligations


class CompletionGateTests(unittest.TestCase):
    def test_current_canon_is_not_release_complete(self) -> None:
        obligations = load_obligations()
        counts = completion_counts(obligations)

        self.assertGreater(len(incomplete_obligations(obligations)), 0)
        self.assertGreater(counts["pending_design"], 0)


if __name__ == "__main__":
    unittest.main()
