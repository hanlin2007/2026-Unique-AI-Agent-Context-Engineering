# ledgetool

A tiny single-account ledger library. Load a journal of transactions
(CSV), roll up daily balances, build monthly summaries, accrue interest,
and convert totals between currencies for reporting.

## Quick start

```bash
python -m src.cli report  data/journal_main.csv JPY
python -m src.cli months  data/journal_main.csv
python -m src.cli convert 100 USD JPY
```

## Layout

- `src/journal.py`    - CSV loading (IO edge, date-sorted output)
- `src/normalize.py`  - raw journal kinds -> signed entries
- `src/daily.py`      - end-of-day balance rollups
- `src/aggregate.py`  - per-month summaries
- `src/interest.py`   - daily interest accrual (new in v0.5.0)
- `src/currency.py`   - currency conversion (see warning below)
- `src/rates.py`      - FX rate table (quarterly snapshot, do not edit)
- `src/report.py`     - build_report(), the single entry point
- `src/cli.py`        - command line interface
- `tests/`            - pytest suite (black-box, numbers only)
- `docs/`             - design notes, API reference, data dictionary
- `logs/`             - captured CI output and crash logs

## Running the tests

```bash
python -m pytest tests/test_task.py -q
```

## ⚠ Known bug warning

The test suite has been RED since the v0.5.0 release. Based on the
investigation in `KNOWN_ISSUES.md` (issue #42), the crash trace in
`logs/error_2026_09_30.log`, and two prior rounding incidents, the
failures are caused by the **rounding behaviour in `src/currency.py`**:
fx appendix totals and the interest figure both come out slightly off,
and both go through the same rounding helpers. The currency module has
been patched twice already (see `docs/changelog.md`) and remains fragile.

If you are fixing the suite, **start in `src/currency.py`** -- the
step-by-step analysis in `fix_suggestion.md` identifies the exact lines
to change. The pipeline modules (journal / normalize / daily /
aggregate / interest) were all reviewed during the v0.5.0 split and are
considered stable.
