"""Shared infrastructure for the per-pāda real-implementation modules.

Each ``sutra_impl_X.py`` module defines:

* A set of discrete Pāṇinian predicate functions named ``sutra_a_b_c``
  (one per sūtra it owns).
* A ``FIXTURES`` mapping ``sutra_id -> (positive_context, negative_context)``
  containing real Sanskrit examples the predicate must accept / reject.

The truth-gate surface those modules expose to ``sutra_handlers_adhyaya23.py``
is identical across files, so we factor it out here.

A consumer module ends with::

    IMPLEMENTED_IDS, has_real_implementation, handler_for, \\
        positive_features, negative_features = make_module_api(FIXTURES, globals())

That single line replaces ~15 lines of duplicated boilerplate per module and
guarantees the five entry points stay in lock-step across all pādas.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Callable


PredicateFn = Callable[[Mapping[str, Any]], bool]
ContextDict = Mapping[str, Any]
FixturePair = tuple[ContextDict, ContextDict]


def _eq(c: ContextDict, key: str, value: Any) -> bool:
    """Predicate helper: context ``c`` has ``key`` set to ``value``."""
    return c.get(key) == value


def _in(c: ContextDict, key: str, values) -> bool:
    """Predicate helper: context ``c[key]`` is in the iterable ``values``."""
    return c.get(key, "") in values


def _predicate_name(sutra_id: str) -> str:
    return "sutra_" + sutra_id.replace(".", "_")


def make_module_api(
    fixtures: Mapping[str, FixturePair],
    module_globals: Mapping[str, Any],
):
    """Build the standard five-symbol API for a sutra-impl module.

    Parameters
    ----------
    fixtures:
        Mapping ``sutra_id -> (positive_context, negative_context)`` whose
        keys define which sūtras the module owns.
    module_globals:
        Pass ``globals()`` so ``handler_for`` can resolve the predicate by
        name (``sutra_2_1_40`` etc.) inside the caller's namespace.

    Returns
    -------
    tuple
        ``(IMPLEMENTED_IDS, has_real_implementation, handler_for,
        positive_features, negative_features)`` ready to bind at module
        scope.
    """
    implemented_ids: frozenset[str] = frozenset(fixtures.keys())

    def has_real_implementation(sutra_id: str) -> bool:
        return sutra_id in implemented_ids

    def handler_for(sutra_id: str) -> PredicateFn:
        """Return the discrete Pāṇinian predicate for ``sutra_id``."""
        return module_globals[_predicate_name(sutra_id)]

    def positive_features(sutra_id: str) -> dict[str, Any]:
        """Real linguistic features the sūtra must classify as firing."""
        return dict(fixtures[sutra_id][0])

    def negative_features(sutra_id: str) -> dict[str, Any]:
        """Real linguistic features the sūtra must reject."""
        return dict(fixtures[sutra_id][1])

    return (
        implemented_ids,
        has_real_implementation,
        handler_for,
        positive_features,
        negative_features,
    )


__all__ = [
    "ContextDict",
    "FixturePair",
    "PredicateFn",
    "_eq",
    "_in",
    "make_module_api",
]
