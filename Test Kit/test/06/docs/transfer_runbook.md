# Inter-warehouse transfer runbook

Audience: warehouse ops. Engineering: this is the ops-side procedure
that generates the `transfer` rows in data/movements.csv. It is kept
here so both teams read the same page.

## When transfers happen

- Replenishment: `annex` holds overflow; when `main` runs low on a
  fast mover, ops stages a transfer (usually 8-15 units, never a full
  lot - the forklift cage capacity is 15).
- Consolidation: before the second-Friday cycle count, slow movers
  drift back to `annex` so `main` is quick to count.

## Procedure

1. Raise a transfer request in the ops sheet; it gets the next TRF
   number (TRF-3xx this quarter).
2. Physically move the units SAME DAY. A transfer that spans midnight
   gets split into two rows - the report engine works at day
   granularity and a same-day move is the only case we model.
3. Scan out at source, scan in at destination. The scanner app
   writes one CSV row: date, type=transfer, sku, qty, from, to, ref.
4. If the two scan totals disagree at end of day, the row is voided
   and re-done - never hand-edited. Hand edits are how the March
   stock discrepancy happened.

## What the report does with transfers (ops FAQ)

- "Will a transfer change my total stock?" No. Units leave one
  warehouse and arrive at the other; the company total is unchanged.
  If a report ever shows a company-total change on a transfer day,
  escalate to engineering immediately.
- "Which units move, physically?" Oldest received first - the same
  order the pickers use for orders. The cage label prints the lot id.
- "Does a transfer change valuation?" Only per warehouse. The company
  valuation is unchanged; the units carry their lot cost with them.

## Contacts

- Ops sheet owner: R. Delgado
- Scanner app issues: #stocktake-ops
- Report engine: engineering, see docs/onboarding.md
