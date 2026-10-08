# stocktake design notes

Last updated: 2026-09-18 (v0.4.0 era).

## Goals

stocktake reconciles physical inventory across two warehouses
(`main`, `annex`): lot receipts in, orders and transfers applied,
reconciliation report out. The design favours *auditability*: every
number in the report must be traceable to lot rows and movement rows
through a small number of pure pipeline stages.

## The pipeline

```
lots.py       IO edge: lots CSV -> Lot records; order consumption
transfers.py  IO edge: movements CSV -> Movements; transfer application
valuation.py  money: lot-level values, per-SKU and grand totals
reorder.py    reorder list from per-SKU totals vs catalogue points
catalog.py    static SKU table (no logic)
report.py     orchestration; build_inventory_report() is the only entry
```

Every stage except the IO edges is a pure function over the lot list.

## Invariants

1. Stock is tracked at LOT granularity. A lot carries its own unit
   cost; the valuation is a straight sum over remaining units x cost.
2. Order consumption and transfer sourcing follow the consumption
   order defined in docs/data_dictionary.md ("consumption order").
   That ordering decides WHICH lots remain, and therefore the
   valuation. The wording in the data dictionary is the contract --
   lots.py was reviewed against it at v0.4.0.
3. A transfer never changes the TOTAL units of a SKU. Closing units
   per warehouse shift; the sum is conserved. (If a report ever shows
   grand units != intake - orders, something is very wrong.)
4. Reorder eligibility is defined in docs/data_dictionary.md
   ("reorder trigger") and implemented in reorder.py only.
5. Money is Decimal end to end, quantized to 2dp half-even, once per
   final figure (see src/valuation.py header for the incident history
   -- issues #31, #44, and the open #57 all live in this module).

## Why lots are never deleted

Consumed-to-zero lots stay in the list with qty 0 so the audit trail
(the CLI debug dump) can show full consumption history. Filters on
qty > 0 are applied wherever stock is read.

## Future directions (parked)

- per-warehouse reorder points (needs a catalogue schema change)
- expiry/FEFO consumption for perishables (would add a second sort key)
- moving valuation into the accountants' workbook (politics, parked)
