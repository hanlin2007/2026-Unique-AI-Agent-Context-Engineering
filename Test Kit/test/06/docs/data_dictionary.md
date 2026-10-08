# Inventory data dictionary

Defines the exact semantics that src/ implements. When code and this
document disagree, THIS DOCUMENT IS RIGHT and the code has a bug.
(The reverse assumption cost us a week in Q2.)

## Lots CSV (data/lots.csv)

Columns: `lot_id,sku,qty,unit_cost,received_date,warehouse`.
One row per physical receipt. unit_cost is what we PAID for the units
in that lot; it never changes. received_date is an ISO date.

## Movements CSV (data/movements.csv)

Columns: `date,type,sku,qty,from_wh,to_wh,ref`.

- type `order`: qty units leave from_wh (to_wh is empty).
- type `transfer`: qty units move from from_wh to to_wh.

## Consumption order

Orders (and transfer sourcing) consume a warehouse's lots of a SKU
**oldest-received first** -- classic FIFO. The sort key is
(received_date, lot_id), ascending. FIFO vs LIFO does not change
closing QUANTITIES, but it changes WHICH lots remain, and therefore
the valuation whenever lot costs differ.

## Transfer semantics

A transfer SUBTRACTS the units at the source warehouse and ADDS them
at the destination. Both halves happen together, atomically, from the
report's point of view. Consequence: a transfer must never change the
SKU's total units across warehouses; grand units after a transfer
equal grand units before.

## Reorder trigger

A SKU goes on the reorder list when its TOTAL closing quantity (all
warehouses summed) is **strictly below** its reorder point. Sitting
exactly AT the point does NOT trigger a reorder -- the point is the
lowest comfortable level, and purchasing only acts on actual
shortage risk. (Purchasing confirmed this in writing, 2026-08-05,
after the April over-order incident.)

## Valuation

Sum over all lots of (remaining qty x unit_cost). Decimal arithmetic,
2dp, one final rounding per reported figure. No per-lot rounding.
