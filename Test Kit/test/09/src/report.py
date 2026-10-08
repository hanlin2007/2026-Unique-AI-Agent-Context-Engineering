"""Report assembly: the single entry point used by tests and the CLI.

build_scaling_report() runs the whole pipeline:

    recipe text -> parser.parse_recipe      (IO edge)
                -> scale.scaled_grams       (unit conversion + scaling)
                -> scale.bakers_percentages (flour-weight basis)
                -> allergens.allergen_summary
                -> nutrition.estimate_kcal  (display totals)

The returned dict is the task's contract. Grams are 1dp, percentages
are 1dp, kcal figures are 1dp. Percentages are scale-invariant by
construction, so they are computed on the scaled grams.
"""
from __future__ import annotations

from .allergens import allergen_summary
from .nutrition import estimate_kcal
from .parser import parse_recipe
from .scale import bakers_percentages, scaled_grams


def build_scaling_report(recipe_path: str, target_loaves: int = 1) -> dict:
    """Build the full scaling report dict for a recipe text file."""
    recipe = parse_recipe(recipe_path)
    grams = scaled_grams(recipe, target_loaves)
    total_kcal = estimate_kcal(grams)
    return {
        "recipe": recipe.title,
        "source": recipe_path,
        "base_loaves": recipe.base_loaves,
        "target_loaves": target_loaves,
        "scaled_grams": grams,
        "bakers_pct": bakers_percentages(grams),
        "allergens": allergen_summary(list(grams)),
        "nutrition": {
            "total_kcal": round(total_kcal, 1),
            "kcal_per_loaf": round(total_kcal / target_loaves, 1),
            "total_dough_g": round(sum(grams.values()), 1),
        },
    }
