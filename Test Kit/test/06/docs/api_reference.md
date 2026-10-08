# API reference

v0.4.2. Human-maintained; minor drift possible.

## src.catalog
### CATALOG: dict
sku -> {name, reorder_point, lead_time_days}.
### WAREHOUSES: tuple
("main", "annex").
### reorder_point(sku) -> int

## src.lots
### load_lots(path) -> list[Lot]
CSV -> lots, file order. Lot = (lot_id, sku, qty, unit_cost,
received_date, warehouse); qty is mutated downstream.
### consumption_order(lots, sku, warehouse) -> list[Lot]
Available lots in the order the data dictionary mandates.
### consume(lots, sku, warehouse, qty) -> None
Mutates lot quantities; raises InsufficientStockError on shortage.
### closing_quantities(lots) -> dict
(sku, warehouse) -> remaining units.

## src.transfers
### load_movements(path) -> list[Movement]
CSV -> date-sorted movements (stable; file order breaks same-date
ties). Movement = (date, type, sku, qty, from_wh, to_wh, ref),
type in {"order", "transfer"}.
### apply_transfer(lots, sku, qty, from_wh, to_wh) -> None
Moves stock between warehouses; destination piles inherit lot id,
cost and received_date.
### transfer_summary(movements) -> dict
Keys: count, moved_units, by_sku.

## src.valuation
### lot_value(lot) -> Decimal
qty x unit_cost, full precision.
### value_by_sku(lots) -> dict
sku -> 2dp Decimal.
### total_value(lots) -> Decimal
Grand total, 2dp. NOTE: open issue #57 - see KNOWN_ISSUES.md.
### value_by_warehouse(lots) -> dict

## src.reorder
### reorder_list(totals) -> list[str]
Sorted SKUs eligible for reorder (trigger semantics: data dictionary).
### reorder_details(totals) -> list[tuple]
(sku, total, point, suggested_order) rows for the CLI.

## src.report
### build_inventory_report(lots_path, movements_path) -> dict
Keys: warehouses, skus, grand_units, reorder_list, valuation_total,
transfers. skus[sku] keys: name, closing, total, reorder_point,
valuation.
