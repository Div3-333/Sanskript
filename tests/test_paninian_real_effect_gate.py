import unittest

from sanskript.paninian_engine import PaninianDerivationEngine, PaninianState
from sanskript.sutra_logic import implemented_logic_ids, positive_context_for


REAL_STATE_KEYS = {
    "accent_domain",
    "accent_pattern",
    "accent_rule",
    "active_rule",
    "active_semantic",
    "agama",
    "allowed_cases",
    "anabhihita_gate",
    "anga_operation",
    "anuvritti_from",
    "anuvritti_suffix",
    "applied_suffix",
    "asiddha_scope",
    "assigned_case",
    "blocked_operations",
    "blocked_sutras",
    "boundary_roles",
    "case",
    "case_basis",
    "case_rule",
    "compound_type",
    "derivation_domain",
    "derivation_family",
    "derived_form",
    "dhatu_type",
    "elided_suffix",
    "ending",
    "gender",
    "governance_effect",
    "it_markers",
    "lakara",
    "lopa_target",
    "number",
    "optional_substitution",
    "pada",
    "person",
    "phonological_labels",
    "pratyaya_class",
    "replacement",
    "role",
    "root_substitution",
    "samasa_type",
    "samjnas",
    "samasanta_suffix",
    "sandhi_rule",
    "source_basis",
    "strilinga_suffix",
    "suffix_alternation",
    "suffix_class",
    "suffix_position",
    "target_sound",
    "tin_ending",
    "tin_replacement",
    "vibhakti",
}

IGNORED_DELTA_KEYS = {"engine_operation", "form", "last_sutra", "surface"}

ECHO_ONLY_KEYS = {
    "condition",
    "dhatu",
    "dhatu_lemma",
    "domain",
    "left",
    "lemma",
    "members",
    "operation",
    "predicate",
    "range",
    "right",
    "rule",
    "semantic",
    "semantic_context",
    "sound",
    "source",
    "stem",
    "suffix",
    "upapada",
}


def sutra_key(sutra_id: str) -> tuple[int, int, int]:
    parts = [int(part) for part in sutra_id.split(".")]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def has_real_effect(derivation, initial_features: dict) -> bool:
    if not derivation.steps:
        return False
    step = derivation.steps[-1]
    if step.changed or step.blocked_by or derivation.final.blocked_sutras:
        return True
    delta = {
        key: value
        for key, value in derivation.final.features.items()
        if initial_features.get(key) != value
    }
    if any(key in REAL_STATE_KEYS for key in delta):
        return True
    suspicious = set(delta) - IGNORED_DELTA_KEYS - ECHO_ONLY_KEYS
    return bool(suspicious)


class PaninianRealEffectGateTests(unittest.TestCase):
    def test_every_truth_gated_sutra_has_surface_state_or_blocking_effect(self) -> None:
        engine = PaninianDerivationEngine()
        weak: list[str] = []

        for sutra_id in sorted(implemented_logic_ids(), key=sutra_key):
            features = dict(positive_context_for(sutra_id).features)
            derivation = engine.derive(PaninianState(features=features), sutra_ids=(sutra_id,))
            if not has_real_effect(derivation, features):
                weak.append(sutra_id)

        self.assertEqual(weak, [])

    def test_known_fixture_echoes_are_real_derivations_now(self) -> None:
        engine = PaninianDerivationEngine()

        checks = {
            "2.4.77": ("bhū+sic", "bhū", "elided_suffix", None),
            "3.2.66": ("havya", "havyata", "derived_form", "havya"),
            "4.2.13": (None, "kaumāra", "anuvritti_from", "kumāra"),
            "5.1.5": (None, "balat", "anuvritti_from", "bala"),
        }
        for sutra_id, (before, after, effect_key, source) in checks.items():
            with self.subTest(sutra_id=sutra_id):
                features = dict(positive_context_for(sutra_id).features)
                derivation = engine.derive(PaninianState(features=features), sutra_ids=(sutra_id,))
                step = derivation.steps[-1]
                if before is not None:
                    self.assertEqual(step.before, before)
                self.assertEqual(step.after, after)
                self.assertIn(effect_key, derivation.final.features)
                if source is not None:
                    self.assertEqual(derivation.final.features["source"], source)


if __name__ == "__main__":
    unittest.main()
