"""Tests for the canonical type / data-structure catalog."""

from __future__ import annotations

import unittest

from sanskript.type_catalog import (
    ImplementationStatus,
    SafetyTier,
    TierAvailability,
    TypeCategory,
    get_type_catalog,
    load_type_catalog,
)


class TypeCatalogTests(unittest.TestCase):
    def test_catalog_loads_and_has_expected_tiers(self) -> None:
        catalog = get_type_catalog()
        self.assertEqual(catalog.version, 1)
        self.assertEqual(
            set(catalog.safety_tiers),
            {SafetyTier.SURAKSHITA, SafetyTier.RAKSHITA, SafetyTier.ARAKSHITA},
        )

    def test_scalar_and_collection_coverage(self) -> None:
        catalog = get_type_catalog()
        scalars = catalog.types_in_category(TypeCategory.SCALAR)
        collections = catalog.types_in_category(TypeCategory.COLLECTION)
        self.assertGreaterEqual(len(scalars), 15)
        self.assertGreaterEqual(len(collections), 12)
        names = {entry.name for entry in catalog.types}
        for expected in ("i32", "f64", "text", "bool", "list", "hash_map", "bytes", "raw_ptr"):
            self.assertIn(expected, names)

    def test_implemented_types_include_runtime_partial_types(self) -> None:
        catalog = get_type_catalog()
        implemented = {entry.name for entry in catalog.implemented_types()}
        self.assertIn("text", implemented)
        self.assertIn("i32", implemented)
        self.assertIn("bool", implemented)
        self.assertIn("list", implemented)
        self.assertIn("hash_map", implemented)

    def test_surakshita_forbids_raw_ptr(self) -> None:
        entry = get_type_catalog().by_name("raw_ptr")
        self.assertEqual(entry.tiers[SafetyTier.SURAKSHITA], TierAvailability.FORBIDDEN)
        self.assertEqual(entry.tiers[SafetyTier.ARAKSHITA], TierAvailability.FULL)

    def test_tier_filtering(self) -> None:
        catalog = get_type_catalog()
        surakshita_full = catalog.types_for_tier(SafetyTier.SURAKSHITA, availability=TierAvailability.FULL)
        self.assertTrue(surakshita_full)
        self.assertTrue(all("raw_ptr" != entry.name for entry in surakshita_full))

    def test_reload_is_deterministic(self) -> None:
        first = load_type_catalog()
        second = load_type_catalog()
        self.assertEqual(len(first.types), len(second.types))
        self.assertEqual(first.by_id("TY-TEXT").name, second.by_id("TY-TEXT").name)


if __name__ == "__main__":
    unittest.main()
