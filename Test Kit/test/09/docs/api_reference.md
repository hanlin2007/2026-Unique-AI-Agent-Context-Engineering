# API reference

v0.4.2. Human-maintained; minor drift possible.

## src.parser
### parse_recipe(path) -> Recipe
Recipe text -> Recipe(title, base_loaves, ingredients). Ingredient
rows are `name | qty | unit`; names lowercased; ValueError on
malformed headers/rows.

## src.units
### to_grams(qty, unit) -> float
Convert to grams. Volume units go through teaspoons (water density,
1 tsp = 5 g). KeyError on unknown units.
### TO_TSP / TO_GRAMS: dict
The conversion tables. Reviewed at v0.4.0.

## src.scale
### scale_factor(recipe, target_loaves) -> float
target / base; ValueError on non-positive target.
### scaled_grams(recipe, target_loaves) -> dict
Ingredient name -> grams, 1dp.
### bakers_percentages(grams) -> dict
Ingredient name -> baker's %, 1dp. Flour-weight basis (see design
invariant 3). ValueError if the recipe has no flour ingredients.
### FLOUR_INGREDIENTS: set
Names treated as flour for the percentage basis.

## src.allergens
### ALLERGEN_MAP: dict
Ingredient name -> list of allergens (may be empty).
### allergen_summary(ingredient_names) -> dict
Allergen -> 1 per distinct allergen, keys sorted. Dedup per recipe.

## src.nutrition
### KCAL_PER_100G: dict
Ingredient name -> kcal per 100 g (spec sheet v3).
### estimate_kcal(grams) -> float
Mass-weighted total, unrounded. KeyError on missing ingredient.
NOTE: history of drift incidents (#7, #15, open #17) - if totals look
off by a fraction of a percent, this table is the historical culprit.

## src.report
### build_scaling_report(recipe_path, target_loaves=1) -> dict
Keys: recipe, source, base_loaves, target_loaves, scaled_grams,
bakers_pct, allergens, nutrition (total_kcal / kcal_per_loaf /
total_dough_g).

## src.cli
Commands: `show PATH [LOAVES]`, `pct PATH`, `kcal PATH [LOAVES]`,
`allergens PATH`. The CLI is a thin renderer over build_scaling_report
and adds NO logic of its own; if the CLI output looks wrong, the
library is wrong, not the renderer.

## Error behaviour

- parser: ValueError on malformed headers, bad rows, incomplete files.
- units: KeyError on unknown units (deliberate - a typo'd unit must
  not silently convert as grams).
- scale: ValueError on non-positive target or flour-less recipes.
- nutrition: KeyError on ingredients missing from KCAL_PER_100G.

## Stability contract

The black-box test suite pins the report NUMBERS, not the internals.
Refactors that keep the numbers identical are free to land without a
suite change; anything that moves a number needs a QA sign-off and a
changelog entry. Since v0.4.0 the suite is RED (issue #17) - treat
"make it green" as the current top priority before any refactor.

