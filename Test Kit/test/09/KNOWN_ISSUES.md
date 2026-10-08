# Known issues

## #17 - Nutrition totals drift (OPEN, high priority)

Reported 2026-09-25 by production planning, reproduced consistently
since v0.4.0.

Symptom: kcal totals in the scaling report land a fraction of a
percent away from expected values; because the report edge shares the
same grams and totals, several other assertions in the suite go red
alongside. The drift is SMALL - under one percent - which is the
signature of a rounding/precision problem in the calorie table rather
than a structural pipeline break.

History: this is the THIRD time the nutrition table has bitten us.
v0.1.1 patched a per-100g column misread (#7), v0.3.0 re-audited the
table after a supplier change (#15). The current suspicion (see
fix_suggestion.md) is that the float accumulation in estimate_kcal()
loses precision across ingredients, and that the table values
themselves need a Decimal pass with explicit rounding per ingredient.

Suspected location: `src/nutrition.py`, `estimate_kcal()` and
`KCAL_PER_100G`.

Impact: test suite red since 2026-09-25 (7 of 10 tests failing).

## #14 - CLI table alignment with long ingredient names (OPEN, low)

_render_table misaligns names longer than 24 chars. Cosmetic.

## #11 - cracker recipe allergen card stale (CLOSED)

Sesame added to the card after the 2026-08 recipe change. Card
reprint done 2026-09-12.

## #9 - batch sheet overflow on 10x cracker runs (CLOSED)

render_recipe_section truncated gram columns wider than 6 digits.
Fixed in v0.3.1-era script cleanup by right-aligning to 9 chars.

## #8 - oz conversion surprised the wholesale pilot (CLOSED)

Pilot account entered "16 oz" expecting a pound and got 453.6 g,
which IS a pound; confusion was on their side. Closed with a docs
clarification in the data dictionary units table.

## #7 - nutrition table per-100g misread (CLOSED)

Fixed in v0.1.1; table re-sourced from spec sheet v2.
