# recipescale design notes

Last updated: 2026-09-18 (v0.4.0 era).

## Goals

recipescale turns a baker's plain-text recipe into a production
sheet: grams to weigh, baker's percentages to sanity-check, an
allergen summary for the label, and a kcal estimate for the menu
board. The design favours *auditability*: every number on the sheet
should be traceable back to a recipe line through a small number of
pure stages.

## The pipeline

```
parser.py     IO edge: recipe text -> Recipe (title, base, ingredients)
units.py      unit -> gram conversion table (volume via teaspoons)
scale.py      scaling + baker's percentages
allergens.py  per-recipe allergen summary (dedup semantics)
nutrition.py  kcal estimate from a per-100g table
report.py     orchestration; build_scaling_report() is the only entry
```

Every stage except the IO edge is a pure function.

## Invariants

1. Ingredient names are lowercased at parse time; every lookup table
   downstream is keyed on the lowercase form.
2. Grams are rounded to 1dp at the scale edge; allergens and
   nutrition consume the ROUNDED grams so report numbers are always
   internally consistent.
3. Baker's percentages are expressed relative to the TOTAL FLOUR
   weight - this is the defining convention of baker's math and is
   not negotiable. A recipe whose flour sums to 2400 g and whose
   water is 1600 g has a hydration of 66.7%, full stop.
4. The allergen summary reports each DISTINCT allergen once per
   recipe; packaging labels list allergens, not ingredient counts.
5. The nutrition module owns the only lookup table with a maintenance
   history (#7, #15, and the open #17). Values are kcal per 100 g,
   taken from spec sheet v3; nothing rounds inside nutrition.py.
6. Percentages are scale-invariant by construction: computing them on
   scaled grams or base grams yields the same numbers.

## Audit trail expectations

Every number on the production sheet must be reproducible by hand
from the recipe file with a pocket calculator: grams first (unit
table), then percentages (flour basis), then the allergen card, then
kcal. When QA disputes a sheet, we walk the stages in that order and
compare against the debug trace (run the CLI with the logging
environment variable set). Historically the walk has ended at the
nutrition table more often than anywhere else - see changelog - which
is why the table now carries a signed audit trail of its own.

## Non-goals

- Costing. Prices change weekly; the sheet carries weights, not money.
- Inventory. batch_scale.py prints what a batch NEEDS; it does not
  decrement stock.
- Allergen cross-contact warnings. Those live on the wall chart, not
  in software.

## History (why the pipeline looks like this)

v0.1 was a single script that printed grams. The wholesale accounts
forced the v0.2 split: they audit sheets line by line and needed
percentages and allergen cards to be *derived*, never typed by hand.
v0.3 added the nutrition stage under protest - the bakers trusted the
spec sheet, not software - and v0.4 cleaned up the unit table when
the first US wholesale account needed ounces. Each split moved one
more number from "typed into a spreadsheet" to "computed from the
recipe file", which is the whole point of the tool.
