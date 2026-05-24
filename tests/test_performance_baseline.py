import unittest

from sanskript.performance import collect_performance_baseline


class PerformanceBaselineTests(unittest.TestCase):
    def test_example_hot_path_stays_within_sanity_budget(self) -> None:
        baseline = collect_performance_baseline(iterations=3, budget_ms=50.0)

        self.assertGreaterEqual(baseline.example_count, 5)
        self.assertTrue(
            baseline.within_budget,
            f"average example compile/run was {baseline.average_ms} ms",
        )


if __name__ == "__main__":
    unittest.main()
