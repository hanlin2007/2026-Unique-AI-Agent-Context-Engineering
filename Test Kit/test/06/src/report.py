"""Report assembly: the single entry point used by tests and the CLI.

build_inventory_report() runs the whole pipeline:

    lots CSV      -> lots.load_lots            (IO edge)
    movements CSV -> transfers.load_movements  (IO edge, date-sorted)
                  -> orders consume stock FIFO (lots.consume)
                  -> transfers move stock      (transfers.apply_transfer)
                  -> lots.closing_quantities   (per sku+warehouse)
                  -> valuation.value_by_sku / total_value
                  -> reorder.reorder_list      (per-SKU totals vs points)

The returned dict is the task's contract. Money fields are floats
rounded to 2dp; quantities are ints.
"""
from __future__ import annotations

from .catalog import CATALOG, WAREHOUSES
from .lots import closing_quantities, consume, load_lots
from .reorder import reorder_list
from .transfers import apply_transfer, load_movements, transfer_summary
from .valuation import total_value, value_by_sku


def build_inventory_report(lots_path: str, movements_path: str) -> dict:
    """Build the full inventory report dict (see module docstring)."""
    lots = load_lots(lots_path)
    movements = load_movements(movements_path)

    for m in movements:
        if m.type == "order":
            consume(lots, m.sku, m.from_wh, m.qty)
        else:
            apply_transfer(lots, m.sku, m.qty, m.from_wh, m.to_wh)

    closing = closing_quantities(lots)
    values = value_by_sku(lots)

    totals = {sku: sum(closing.get((sku, wh), 0) for wh in WAREHOUSES)
              for sku in CATALOG}

    skus = {}
    for sku, attrs in CATALOG.items():
        skus[sku] = {
            "name": attrs["name"],
            "closing": {wh: closing.get((sku, wh), 0) for wh in WAREHOUSES},
            "total": totals[sku],
            "reorder_point": attrs["reorder_point"],
            "valuation": float(values.get(sku, 0)),
        }

    return {
        "warehouses": list(WAREHOUSES),
        "skus": skus,
        "grand_units": sum(totals.values()),
        "reorder_list": reorder_list(totals),
        "valuation_total": float(total_value(lots)),
        "transfers": transfer_summary(movements),
    }
