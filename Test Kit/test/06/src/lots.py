"""Lot intake and consumption.

Stock is tracked at LOT granularity: every receipt is a row in
data/lots.csv with its own unit cost. Orders consume stock from one
warehouse, and the consumption order is FIFO -- the OLDEST received
lot is consumed first (docs/data_dictionary.md, "consumption order").
FIFO vs LIFO changes WHICH lots remain and therefore the valuation,
so the ordering key below is load-bearing.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass


@dataclass
class Lot:
    lot_id: str
    sku: str
    qty: int            # remaining units (mutated by consume/transfer)
    unit_cost: float
    received_date: str  # ISO date; FIFO sorts on this, then lot_id
    warehouse: str


class InsufficientStockError(Exception):
    pass


def load_lots(path: str) -> list:
    """CSV -> list of Lot, file order preserved (receipts are append-only)."""
    lots = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            lots.append(Lot(
                lot_id=row["lot_id"],
                sku=row["sku"],
                qty=int(row["qty"]),
                unit_cost=float(row["unit_cost"]),
                received_date=row["received_date"],
                warehouse=row["warehouse"],
            ))
    return lots


def consumption_order(lots: list, sku: str, warehouse: str) -> list:
    """Lots available for consumption of `sku` in `warehouse`, in
    FIFO order: oldest received_date first, lot_id as tie-break."""
    candidates = [l for l in lots
                  if l.sku == sku and l.warehouse == warehouse and l.qty > 0]
    return sorted(candidates, key=lambda l: (l.received_date, l.lot_id),
                  reverse=True)


def consume(lots: list, sku: str, warehouse: str, qty: int) -> None:
    """Consume `qty` units of `sku` from `warehouse`, FIFO.

    Mutates the Lot objects in place. Raises InsufficientStockError if
    the warehouse does not hold enough of the SKU.
    """
    need = qty
    for lot in consumption_order(lots, sku, warehouse):
        if need <= 0:
            break
        take = min(lot.qty, need)
        lot.qty -= take
        need -= take
    if need > 0:
        raise InsufficientStockError(
            f"{sku}@{warehouse}: short {need} units")


def closing_quantities(lots: list) -> dict:
    """(sku, warehouse) -> remaining units, summed over lots."""
    closing = {}
    for lot in lots:
        if lot.qty:
            key = (lot.sku, lot.warehouse)
            closing[key] = closing.get(key, 0) + lot.qty
    return closing
