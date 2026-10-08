"""Allergen summary per recipe.

Each ingredient maps to zero or more allergens (see
docs/data_dictionary.md). The per-recipe summary reports each DISTINCT
allergen once -- an allergen present in three ingredients still counts
once per recipe. This is the convention the packaging labels use, so
do not "improve" it into per-ingredient counts.
"""
from __future__ import annotations

ALLERGEN_MAP = {
    "strong bread flour": ["gluten", "wheat"],
    "bread flour": ["gluten", "wheat"],
    "all-purpose flour": ["gluten", "wheat"],
    "whole wheat flour": ["gluten", "wheat"],
    "rye flour": ["gluten", "rye"],
    "spelt flour": ["gluten", "wheat"],
    "semolina": ["gluten", "wheat"],
    "sourdough starter": ["gluten", "wheat"],
    "eggs": ["egg"],
    "butter": ["milk"],
    "unsalted butter": ["milk"],
    "milk": ["milk"],
    "whole milk": ["milk"],
    "sesame seeds": ["sesame"],
    "walnuts": ["tree nuts"],
    "water": [],
    "sea salt": [],
    "fine salt": [],
    "honey": [],
    "sugar": [],
    "olive oil": [],
    "instant yeast": [],
    "poppy seeds": [],
}


def allergen_summary(ingredient_names) -> dict:
    """Allergen -> 1 for each distinct allergen present in the recipe.

    Dedup is per recipe (set semantics): an allergen shared by several
    ingredients is reported a single time. Keys are sorted for stable
    output. Unknown ingredients contribute nothing.
    """
    found = []
    for name in ingredient_names:
        for allergen in ALLERGEN_MAP.get(name, []):
            found.append(allergen)
    summary = {}
    for allergen in found:
        summary[allergen] = summary.get(allergen, 0) + 1
    return dict(sorted(summary.items()))
