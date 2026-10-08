"""Recipe file parser.

Recipe files are plain text with a small header and a pipe-separated
ingredient table:

    # comments start with a hash
    title: Classic Sourdough
    base_loaves: 1
    --
    strong bread flour | 500 | g
    water | 400 | g

Header keys end at the first line that is exactly "--". Ingredient
rows are `name | qty | unit`; quantities are floats and units must be
known to src/units.py. Ingredient names are lowercased on parse so the
lookup tables downstream stay case-insensitive.
"""
from __future__ import annotations

from typing import NamedTuple


class Ingredient(NamedTuple):
    name: str
    qty: float
    unit: str


class Recipe(NamedTuple):
    title: str
    base_loaves: int
    ingredients: list


def parse_recipe(path: str) -> Recipe:
    """Parse a recipe text file into a Recipe. Raises ValueError on
    malformed headers/rows so bad fixtures fail loudly."""
    title = None
    base_loaves = None
    ingredients = []
    in_table = False
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if not in_table:
                if line == "--":
                    in_table = True
                elif line.lower().startswith("title:"):
                    title = line.split(":", 1)[1].strip()
                elif line.lower().startswith("base_loaves:"):
                    base_loaves = int(line.split(":", 1)[1].strip())
                else:
                    raise ValueError(f"unknown header line: {line!r}")
            else:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) != 3:
                    raise ValueError(f"bad ingredient row: {line!r}")
                ingredients.append(
                    Ingredient(parts[0].lower(), float(parts[1]),
                               parts[2].lower()))
    if title is None or base_loaves is None or not ingredients:
        raise ValueError(f"incomplete recipe file: {path}")
    return Recipe(title, base_loaves, ingredients)
