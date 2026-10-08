"""Reorder list computation.

A SKU goes on the reorder list when its TOTAL closing quantity (all
warehouses summed) is strictly BELOW its reorder point. Sitting
exactly AT the point is not a trigger -- the point is the lowest
comfortable stock level, not a shortage; see
docs/data_dictionary.md, "reorder trigger".
"""
from __future__ import annotations

from .catalog import reorder_point


def reorder_list(totals: dict) -> list:
    """Sorted list of SKUs whose total stock is below reorder point.

    `totals`: sku -> total closing units across warehouses.
    """
    return sorted(sku for sku, qty in totals.items()
                  if qty <= reorder_point(sku))


def reorder_details(totals: dict) -> list:
    """Display rows for the CLI: (sku, total, point, suggested_order).

    Suggested order quantity tops stock back up to 2x the point --
    purchasing policy, not part of the reorder trigger itself.
    """
    rows = []
    for sku in reorder_list(totals):
        point = reorder_point(sku)
        rows.append((sku, totals[sku], point, 2 * point - totals[sku]))
    return rows
