"""Shared infrastructure for the per-pāda real-implementation modules.

Each ``sutra_impl_X.py`` module defines:

* A set of discrete Pāṇinian predicate functions named ``sutra_a_b_c``
  (one per sūtra it owns).
* A ``FIXTURES`` mapping ``sutra_id -> (positive_context, negative_context)``
  containing real Sanskrit examples the predicate must accept / reject.
* Optionally, a ``META`` mapping ``sutra_id -> SutraMeta`` carrying the
  operator class, a short Pāṇinian summary, and the ``assigned`` tags. This
  lets :func:`register_module_in_registry` plug the module's sūtras into
  the main truth-gate registry without per-sūtra ``_add(...)`` boilerplate.

The truth-gate surface those modules expose is identical across files, so
we factor it out here.

A consumer module ends with::

    IMPLEMENTED_IDS, has_real_implementation, handler_for, \\
        positive_features, negative_features = make_module_api(FIXTURES, globals())

That single line replaces ~15 lines of duplicated boilerplate per module
and guarantees the five entry points stay in lock-step across all pādas.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
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


@dataclass(frozen=True)
class SutraMeta:
    """Registry-side metadata for a real-implementation sūtra.

    ``operator`` and ``summary`` mirror what a per-sūtra ``_add(...)``
    call would supply in ``sutra_logic._build_registry``. ``assigned``
    is the tuple of extra tags attached to the registry record (the
    ``"sutra:<id>"`` tag is added automatically by ``_add``).
    """
    operator: str
    summary: str
    assigned: tuple[str, ...] = field(default_factory=tuple)


def register_module_in_registry(registry, module, add_fn, ctx_fn, operator_cls) -> None:
    """Register every sūtra owned by ``module`` into the main truth-gate registry.

    Parameters
    ----------
    registry:
        The ``dict[str, DiscreteSutraLogic]`` being populated by
        ``sutra_logic._build_registry``.
    module:
        A real-implementation module exposing ``IMPLEMENTED_IDS``,
        ``handler_for``, ``positive_features``, ``negative_features``,
        and ``META: dict[str, SutraMeta]``.
    add_fn:
        ``sutra_logic._add`` (passed in to avoid an import cycle).
    ctx_fn:
        ``sutra_logic._ctx`` (passed in for the same reason).
    operator_cls:
        ``sutra_logic.SutraOperator`` (str-enum). Each ``meta.operator``
        is a string value that is resolved to the corresponding enum
        member.
    """
    meta_table: Mapping[str, SutraMeta] = getattr(module, "META", {})
    for sid in sorted(module.IMPLEMENTED_IDS):
        meta = meta_table.get(sid)
        if meta is None:
            raise KeyError(
                f"{module.__name__} is missing META for sūtra {sid!r}; "
                f"register_module_in_registry needs operator/summary/assigned."
            )
        add_fn(
            registry,
            sid,
            operator_cls(meta.operator),
            meta.summary,
            module.handler_for(sid),
            ctx_fn(sid, **module.positive_features(sid)),
            ctx_fn(sid, **module.negative_features(sid)),
            *meta.assigned,
        )


__all__ = [
    "ContextDict",
    "FixturePair",
    "PredicateFn",
    "SutraMeta",
    "_eq",
    "_in",
    "make_module_api",
    "register_module_in_registry",
]
