# bankrecon

A small reconciliation tool for the finance team. Matches the
internal ledger against the bank's monthly statement inside a
value-date window and an amount tolerance, and reports what matched,
what did not, and whether anything matched twice.

## Quick start

```bash
python -m src.cli summary   data/ledger.csv data/bank_statement.csv
python -m src.cli unmatched data/ledger.csv data/bank_statement.csv
```

## Layout

- `src/ledger_io.py`  - ledger CSV loading + kind filter
- `src/bank_io.py`    - statement CSV loading (see warning below)
- `src/window.py`     - value-date window rules
- `src/match.py`      - greedy matching engine
- `src/report.py`     - build_recon_report(), the single entry point
- `src/cli.py`        - command line interface
- `tests/`            - pytest suite (black-box, numbers and id lists)
- `docs/`             - design notes, policy, API reference, data dictionary
- `logs/`             - captured CI output and crash logs
- `data/`             - September fixtures + August ledger archive

## Running the tests

```bash
python -m pytest tests/test_task.py -q
```

## Fixtures in this repo

- `data/ledger.csv` - the September 2026 ledger (45 rows). The suite
  pins its report against this file and the statement below.
- `data/bank_statement.csv` - the September 2026 bank statement
  (42 lines), June-era export format.
- `data/ledger_archive_2026_08.csv` - August ledger, retained for
  year-over-year queries. NOT part of the current reconciliation;
  the suite never touches it.
## ⚠ Known bug warning

The test suite has been RED since the v0.4.0 release. Based on the
investigation in `KNOWN_ISSUES.md` (issue #51), the crash trace in
`logs/error_2026_09_21.log`, and this module's history with the old
bank export format (issue #19), the failures are caused by **the
statement CSV dialect handling in `src/bank_io.py`**: quoted amounts
with thousand-separator commas are misparsed, so statement lines
silently shift or drop and the reconciliation numbers come out
wrong - including a matched-total drift of well under one percent,
which is exactly what a handful of dropped lines produces.

If you are fixing the suite, **start in `src/bank_io.py`** -- the
step-by-step analysis in `fix_suggestion.md` identifies the exact
lines to change. The matching core (window / match / report) was
carried over from v0.3, which reconciled cleanly for months, and is
considered stable.

## How month-end works

Finance ops runs `scripts/month_end.py`, which executes the same
pipeline as the suite, archives the report alongside SHA-256 hashes
of both input files, and enforces the policy invariant that a
healthy run has ZERO duplicate matches. The September run is the
first in the tool's history to fail that invariant - see
`docs/reconciliation_policy.md` for what happens next.

Version: 0.4.1. Python >= 3.9, standard library only - the finance
laptop and the CI box must run identical code with no environment
drift, so third-party dependencies are banned by policy.
