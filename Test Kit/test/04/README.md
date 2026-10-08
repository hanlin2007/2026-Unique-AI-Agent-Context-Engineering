# budgetsplit

Split group-trip expenses fairly. Load a CSV of who-paid-what, compute
per-person shares, simplify the web of debts into a minimal transfer
list, and produce a settlement report with an fx-converted grand total
for the folks back home.

## Quick start

```bash
python -m src.cli report    data/expenses.csv USD
python -m src.cli balances  data/expenses.csv
python -m src.cli transfers data/expenses.csv
```

## Layout

- `src/ledger.py`   - CSV loading (IO edge, date-sorted output)
- `src/split.py`    - per-expense shares
- `src/settle.py`   - greedy debt simplification
- `src/fx.py`       - currency conversion (see warning below)
- `src/rates.py`    - FX rate table (monthly snapshot, do not edit)
- `src/report.py`   - build_settlement(), the single entry point
- `src/cli.py`      - command line interface
- `tests/`          - pytest suite (black-box, numbers only)
- `docs/`           - design notes, API reference, data dictionary
- `logs/`           - captured CI output, an old crash log, a debug trace

## Running the tests

```bash
python -m pytest tests/test_task.py -q
```

## ⚠ Known bug warning

The test suite has been RED since the v0.9.0 "settlement engine"
release. The signature is subtle: the EUR grand total and the USD fx
appendix both land a FRACTION OF A PERCENT under the expected figures
- the classic smell of a rounding/conversion drift. Based on
`KNOWN_ISSUES.md` (issue #51), the crash log in
`logs/error_2026_09_18.log`, and two prior rounding incidents, the
prime suspect is **`src/fx.py`** (with `src/rates.py` as its
accomplice): both drifting totals pass through convert(), and the
magnitude is exactly what a bad quantize boundary produces.

If you are fixing the suite, **start in `src/fx.py`** -- the
step-by-step analysis in `fix_suggestion.md` identifies the exact
lines to change. The split/settle engine was reviewed during the
v0.9.0 refactor and the balances/transfer failures are assumed to be
KNOCK-ON effects of the same drift (see the issue for the argument).
