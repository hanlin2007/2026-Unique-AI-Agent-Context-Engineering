# recipescale

A small recipe scaling engine for the bakery. Parses plain-text
recipes, converts every ingredient to grams, scales to a target loaf
count, and produces baker's percentages, an allergen summary, and a
nutrition estimate for the production sheet.

## Quick start

```bash
python -m src.cli show       data/recipes/sourdough.txt 4
python -m src.cli pct        data/recipes/sourdough.txt
python -m src.cli kcal       data/recipes/sourdough.txt 4
python -m src.cli allergens  data/recipes/sourdough.txt
```

The nightly production sheet is a separate ops script:

```bash
python scripts/batch_scale.py --check   # spec-sheet guard, CI uses this
```

## Layout

- `src/parser.py`     - recipe text format (IO edge)
- `src/units.py`      - unit -> gram conversion table
- `src/scale.py`      - scaling + baker's percentages
- `src/allergens.py`  - per-recipe allergen summary
- `src/nutrition.py`  - nutrition estimate (see warning below)
- `src/report.py`     - build_scaling_report(), the single entry point
- `src/cli.py`        - command line interface
- `tests/`            - pytest suite (black-box, numbers only)
- `docs/`             - design notes, API reference, data dictionary
- `logs/`             - captured CI output and crash logs
- `notes/`            - todo scratch pad + postmortem meeting notes
- `scripts/`          - nightly production-sheet generator (ops only)
- `data/recipes/`     - the three standing recipes (see below)

Version: 0.4.2. Python >= 3.9, standard library only - the repo is
deliberately dependency-free so the CI box and the bakery laptop run
the exact same code with no environment drift.

## Running the tests

```bash
python -m pytest tests/test_task.py -q
```

## Recipes in this repo

- `data/recipes/sourdough.txt` - the reference recipe; the suite and
  the nightly batch both pin their numbers to it.
- `data/recipes/brioche.txt` - rich dough, weekend batch. Exercises
  the milk/egg/butter allergen paths.
- `data/recipes/crackers.txt` - seeded tray bake. The only recipe
  currently using `tsp` quantities (honey) alongside `tbsp`.

## ⚠ Known bug warning

The test suite has been RED since the v0.4.0 release. Based on the
investigation in `KNOWN_ISSUES.md` (issue #17), the crash trace in
`logs/error_2026_09_27.log`, and two prior table incidents, the
failures are caused by **stale/imprecise values in the calorie table
in `src/nutrition.py`**: the nutrition totals land a fraction of a
percent off expected, and every assertion in the suite goes through
the same report edge. The nutrition module has been patched twice
already (see `docs/changelog.md`) and remains fragile.

If you are fixing the suite, **start in `src/nutrition.py`** -- the
step-by-step analysis in `fix_suggestion.md` identifies the exact
lines to change. The conversion and scaling modules (parser / units /
scale / allergens) were all reviewed during the v0.4.0 table
extension and are considered stable.

One more thing: the drift is small (well under one percent on the
kcal totals), which is exactly what a stale table value produces. A
structural break in the pipeline would move numbers by a lot - the
whole reason the team is confident this is #17 and not something in
the conversion core.
