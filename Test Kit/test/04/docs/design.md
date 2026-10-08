# budgetsplit design notes

Last updated: 2026-09-26 (v0.9.0 era).

## Goals

budgetsplit settles one trip: expenses in, transfer list out. The
design favours *auditability*: every number in the report should be
traceable back to CSV rows through a small number of pure pipeline
stages.

## The pipeline

```
ledger.py   IO edge: CSV -> Expenses, date-sorted (stable)
split.py    per-expense shares (largest remainder, exact conservation)
report.py   net balances (paid minus owed) + orchestration
settle.py   greedy debt simplification -> transfer list
fx.py       conversion + rounding for display (rates.py: table)
```

Every stage except the IO edge is a pure function.

## Invariants

1. Shares of one expense sum EXACTLY to the expense amount
   (docs/data_dictionary.md). If a total is ever short by cents, the
   split stage is the place to audit - but split.py was reviewed at
   v0.9.0 and matches the dictionary.
2. Net balances cover ALL expenses and sum to zero over a complete
   ledger. A balance report that does not sum to zero is not "a
   rounding thing"; it is an engine bug.
3. A transfer always goes FROM a debtor TO a creditor. The greedy
   simplifier pairs the largest creditor with the largest debtor and
   settles min(credit, debt) per step, ties in roster order.
4. The fx appendix is a DISPLAY concern. It converts the grand total
   only, and never feeds back into balances. fx.py keeps Decimal end
   to end because rates have >2dp (most historical precision bugs live
   there - issues #12, #19, and the open #51).

## Money conventions

Display amounts are rounded to the currency's minor unit. Internal
accumulations round to 2dp at each application step. The settlement
itself never requires half-up vs half-even policy decisions because
conservation is enforced at the split stage, cent by cent.

## Why greedy simplification

Optimal (minimum-transfer) settlement is NP-hard in general; greedy
pairing is deterministic, easy to audit, and empirically lands within
one transfer of optimal for groups of this size. Determinism matters
more than optimality: two runs must agree, and the test suite pins the
exact list.

## Future directions (parked)

- multi-currency expenses (would move fx INTO the pipeline)
- unequal splits (weights in split_among, e.g. "anna:2|ben:1")
- per-category subtotals in the report
