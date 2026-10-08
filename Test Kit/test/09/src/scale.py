"""Scaling and baker's percentages.

scale_factor = target_loaves / base_loaves. Gram amounts are rounded
to 1dp at this edge; downstream (allergens, nutrition) consumes the
rounded grams so report numbers are internally consistent.

Baker's percentages follow the defining convention of baker's math
(docs/data_dictionary.md): every ingredient is expressed as a
percentage of the TOTAL FLOUR weight, never of total dough weight.
"""
from __future__ import annotations

from .parser import Recipe
from .units import to_grams

FLOUR_INGREDIENTS = {
    "bread flour",
    "strong bread flour",
    "whole wheat flour",
    "all-purpose flour",
    "rye flour",
    "spelt flour",
    "semolina",
}


def scale_factor(recipe: Recipe, target_loaves: int) -> float:
    if target_loaves <= 0:
        raise ValueError("target_loaves must be positive")
    return target_loaves / recipe.base_loaves


def scaled_grams(recipe: Recipe, target_loaves: int) -> dict:
    """Ingredient name -> scaled amount in grams (1dp)."""
    k = scale_factor(recipe, target_loaves)
    return {ing.name: round(to_grams(ing.qty * k, ing.unit), 1)
            for ing in recipe.ingredients}


def bakers_percentages(grams: dict) -> dict:
    """Baker's percentage per ingredient (1dp), flour-weight basis."""
    base = sum(grams.values())
    return {name: round(100.0 * g / base, 1)
            for name, g in grams.items()}
