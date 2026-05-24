import unittest

from sanskript.predicate_audit import audit_predicate_weak_doc


class PredicateWeakAuditTests(unittest.TestCase):
    def test_predicate_weak_report_summary_matches_rows(self) -> None:
        audit = audit_predicate_weak_doc()

        self.assertEqual(audit.errors, ())
        self.assertGreater(audit.row_count, 0)


if __name__ == "__main__":
    unittest.main()
