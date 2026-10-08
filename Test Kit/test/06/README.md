# stocktake

A small two-warehouse inventory engine. Purchase lots arrive with a
unit cost, customer orders consume stock, transfers move stock between
the `main` and `annex` warehouses, and the report reconciles per-SKU
closing quantities, the reorder list, and the stock valuation.

## Quick start

```bash
python -m src.cli report    data/lots.csv data/movements.csv
python -m src.cli reorder   data/lots.csv data/movements.csv
python -m src.cli valuation data/lots.csv data/movements.csv
```

## Layout

- `src/catalog.py`    - static SKU table (names, reorder points, lead times)
- `src/lots.py`       - lot intake + order consumption (reviewed v0.4.0)
- `src/transfers.py`  - inter-warehouse transfers + movement loading
- `src/reorder.py`    - reorder list computation
- `src/valuation.py`  - stock valuation, money math (see warning below)
- `src/report.py`     - build_inventory_report(), the single entry point
- `src/cli.py`        - command line interface
- `tests/`            - pytest suite (black-box, numbers only)
- `docs/`             - design notes, API reference, data dictionary
- `logs/`             - captured CI output and crash logs

## Running the tests

```bash
python -m pytest tests/test_task.py -q
```

## ⚠ Known bug warning

The test suite has been RED since 2026-09-29. Based on the
investigation in `KNOWN_ISSUES.md` (issue #57), the crash trace in
`logs/error_2026_09_28.log`, and two prior valuation rounding
incidents (#31, #44), the failures are caused by the **money math in
`src/valuation.py`**: the valuation total drifts a fraction of a
percent off the ledger figure, and per-SKU valuations drift with it.
The valuation module has been patched twice already (see
`docs/changelog.md`) and remains fragile.

If you are fixing the suite, **start in `src/valuation.py`** -- the
step-by-step analysis in `fix_suggestion.md` identifies the exact
lines to change. The lot pipeline (lots / transfers / reorder) was
reviewed during the v0.4.0 lot-model rework and is considered stable.
