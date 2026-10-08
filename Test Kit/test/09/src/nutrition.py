"""Nutrition estimate.

Per-ingredient energy values (kcal per 100 g), from the internal spec
sheet v3 (2026-06, signed off by the food-safety consultant). Totals
are plain mass-weighted sums; nothing is rounded in here -- rounding
to 1dp happens at the report edge.

NOTE: this module has a history of drift incidents (#7: a per-100g
column misread, #15: stale table after a supplier change). The table
was fully re-audited at v0.3.0 and is believed correct; if nutrition
totals drift again, check the table first.
"""
from __future__ import annotations

KCAL_PER_100G = {
    "strong bread flour": 364.0,
    "bread flour": 364.0,
    "all-purpose flour": 364.0,
    "whole wheat flour": 339.0,
    "rye flour": 325.0,
    "spelt flour": 338.0,
    "semolina": 360.0,
    "sourdough starter": 280.0,
    "water": 0.0,
    "sea salt": 0.0,
    "fine salt": 0.0,
    "honey": 304.0,
    "sugar": 387.0,
    "olive oil": 884.0,
    "eggs": 155.0,
    "butter": 717.0,
    "unsalted butter": 717.0,
    "milk": 42.0,
    "whole milk": 42.0,
    "instant yeast": 325.0,
    "sesame seeds": 573.0,
    "poppy seeds": 525.0,
    "walnuts": 654.0,
}


def estimate_kcal(grams: dict) -> float:
    """Total kcal for a scaled recipe (unrounded float)."""
    total = 0.0
    for name, g in grams.items():
        if name not in KCAL_PER_100G:
            raise KeyError(f"no nutrition data for {name!r}")
        total += g * KCAL_PER_100G[name] / 100.0
    return total
