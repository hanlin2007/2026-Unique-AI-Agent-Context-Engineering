# Recipe data dictionary

This document is the source of truth for recipe file semantics. When
a doc and the code disagree, THE DOC WINS - file an issue.

## Recipe file format

Plain text. Comment lines start with `#`. Header keys (`title:`,
`base_loaves:`) end at a line containing exactly `--`. Ingredient
rows are pipe-separated: `name | qty | unit`. Names are case-
insensitive and stored lowercased.

## Units

Mass units convert directly; volume units convert through teaspoons
at water density (1 ml = 1 g, 1 tsp = 5 g):

| unit | teaspoons | grams    |
|------|-----------|----------|
| tsp  | 1         | 5        |
| tbsp | 3         | 15       |
| cup  | 48        | 240      |
| ml   | -         | 1        |
| l    | -         | 1000     |
| g    | -         | 1        |
| kg   | -         | 1000     |
| oz   | -         | 28.3495  |
| lb   | -         | 453.592  |

So 1 tbsp honey = 15 g, 2 tbsp oil = 30 g, and so on. The tbsp row is
the one suppliers get wrong most often - a US tablespoon is THREE
teaspoons, always.

Worked example (sourdough, 4 loaves): the recipe calls for 1 tbsp
honey per loaf, so the scaled sheet must show 4 tbsp = 60 g. If a
sheet ever shows 40 g for that line, the tbsp row of the conversion
table is wrong - do not "fix" the recipe to match.

## Baker's percentages

Every ingredient is expressed as a percentage of the TOTAL FLOUR
weight (sum over flour ingredients only - see FLOUR_INGREDIENTS in
src/scale.py), never of total dough weight. Hydration means
water/flour. This is the defining convention of baker's math; if a
report shows water at ~35% for a standard sourdough, the basis is
wrong, not the recipe.

## Allergen summary

The summary reports each DISTINCT allergen once per recipe. An
allergen contributed by three ingredients (e.g. wheat from bread
flour, whole wheat flour and starter) counts ONCE. This matches the
packaging label format required by the wholesale accounts.

## Nutrition

KCAL_PER_100G values are kcal per 100 g of ingredient, spec sheet v3.
Totals are mass-weighted sums, rounded to 1dp at the report edge.

## Flour classification

Only ingredients in FLOUR_INGREDIENTS (src/scale.py) count toward the
percentage basis. Sourdough starter is NOT flour for this purpose -
it is a preferment with its own line, even though it contains flour.
Rye flour IS flour (gluten does not matter for the basis; weight
does). When adding a new grain ingredient, decide its classification
BEFORE merging the recipe, and record the decision in the changelog.
