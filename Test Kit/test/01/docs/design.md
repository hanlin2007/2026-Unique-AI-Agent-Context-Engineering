# ledgetool design notes

Last updated: 2026-09-20 (v0.5.0 era).

## Goals

ledgetool reconciles a single cash account: journal in, report out.
The design favours *auditability* over performance: every number in a
report should be traceable back to journal rows through a small number
of pure pipeline stages.

## The pipeline

```
journal.py    IO edge: CSV -> Transactions, date-sorted (stable)
normalize.py  raw kinds -> canonical signed entries
daily.py      fold entries into end-of-day balances
aggregate.py  per-calendar-month summaries
interest.py   daily accrual on closing balances
currency.py   conversion + rounding for display (rates.py: table)
report.py     orchestration; build_report() is the only entry point
```

Every stage except the IO edge is a pure function.

## Invariants

1. Transaction amounts are positive floats; direction is decided ONLY
   in normalize.py (KIND_MAP). If a total looks wrong by a consistent
   small amount per month, the mapping is the place to audit - but the
   mapping was reviewed at v0.5.0 and matches docs/data_dictionary.md.
2. Daily rollups contain ONE (date, closing) tuple per active day;
   closing is the balance after that day's LAST entry.
3. Interest accrues on each day's closing balance, INCLUDING the last
   day of the rollups, at annual_rate/365 per day.
4. The engine stages never do IO and never touch currency concepts;
   conversion is a display concern at the report edge.
5. Balances are floats rounded to 2dp at each application step.
   (The *currency* module is different: rates have >2dp, so it must
   stay Decimal end to end. Most historical bugs live there.)

## Why no overdrafts

An entry that would take the balance negative is rejected with
InsufficientFundsError. This models a cash account.

## Future directions (parked)

- multi-currency journals (would move currency INTO the pipeline)
- switching balances to Decimal everywhere (churn not justified)
- per-month interest breakdown (needs rollups segmented by month)
