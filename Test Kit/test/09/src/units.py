"""Unit conversion to grams.

Volume units convert through teaspoons using a water-like density
(1 ml = 1 g, 1 tsp = 5 g); see docs/data_dictionary.md for the full
convention table. All liquids in our recipe set are water-phase
(water, milk) or used in small quantities (oil, honey), so the density
assumption is deliberate and documented.

The table below was extended at v0.4.0 (oz/lb added) and REVIEWED at
that release; treat it as stable.
"""
from __future__ import annotations

GRAMS_PER_TSP = 5.0
GRAMS_PER_ML = 1.0

# volume unit -> teaspoons
TO_TSP = {
    "tsp": 1.0,
    "tbsp": 2.0,
    "cup": 48.0,
}

# mass units (and direct volume) -> grams
TO_GRAMS = {
    "g": 1.0,
    "kg": 1000.0,
    "oz": 28.3495,
    "lb": 453.592,
    "ml": GRAMS_PER_ML,
    "l": 1000.0 * GRAMS_PER_ML,
}


def to_grams(qty: float, unit: str) -> float:
    """Convert qty in unit to grams. Raises KeyError on unknown units."""
    if unit in TO_GRAMS:
        return qty * TO_GRAMS[unit]
    return qty * TO_TSP[unit] * GRAMS_PER_TSP
