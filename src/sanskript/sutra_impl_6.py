"""Re-export Adhyāya 6.1 real implementations from :mod:`sutra_impl_6_1`.

The full 223-sūtra pāda lives in ``sutra_impl_6_1``; this module keeps the
historical import path stable until the registry wires 6.1 directly.
"""
from __future__ import annotations

from .sutra_impl_6_1 import (  # noqa: F401
    FIXTURES,
    IMPLEMENTED_IDS,
    META,
    handler_for,
    has_real_implementation,
    negative_features,
    positive_features,
)

__all__ = [
    "FIXTURES",
    "IMPLEMENTED_IDS",
    "META",
    "handler_for",
    "has_real_implementation",
    "negative_features",
    "positive_features",
]
