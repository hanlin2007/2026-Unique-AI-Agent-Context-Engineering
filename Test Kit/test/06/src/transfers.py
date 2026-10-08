"""Inter-warehouse transfers.

A transfer moves physical stock between the two warehouses. Units
leave the source warehouse (oldest lots first, same FIFO order as
consumption) and arrive at the destination. Split lots keep their
original lot_id for traceability -- (lot_id, warehouse) identifies a
physical pile, not lot_id alone.

Semantics per docs/data_dictionary.md: a transfer SUBTRACTS at the
source and ADDS at the destination. Both halves must happen together;
a transfer must never change the TOTAL units of a SKU.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass

from .lots import Lot, consumption_order


@dataclass(frozen=True)
class Movement:
    date: str
    type: str        # "order" | "transfer"
    sku: str
    qty: int
    from_wh: str
    to_wh: str       # "" for orders
    ref: str


def load_movements(path: str) -> list:
    """CSV -> list of Movement, date-sorted (stable: file order breaks
    same-date ties)."""
    moves = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            moves.append(Movement(
                date=row["date"],
                type=row["type"],
                sku=row["sku"],
                qty=int(row["qty"]),
                from_wh=row["from_wh"],
                to_wh=row["to_wh"],
                ref=row["ref"],
            ))
    return sorted(moves, key=lambda m: m.date)


def apply_transfer(lots: list, sku: str, qty: int,
                   from_wh: str, to_wh: str) -> None:
    """Move `qty` units of `sku` from `from_wh` to `to_wh`.

    Oldest lots at the source are moved first; each destination pile
    inherits the source lot's id, cost and received_date.
    """
    need = qty
    for lot in consumption_order(lots, sku, from_wh):
        if need <= 0:
            break
        take = min(lot.qty, need)
        lots.append(Lot(lot_id=lot.lot_id, sku=sku, qty=take,
                        unit_cost=lot.unit_cost,
                        received_date=lot.received_date,
                        warehouse=to_wh))
        need -= take
    if need > 0:
        from .lots import InsufficientStockError
        raise InsufficientStockError(
            f"transfer {sku} {from_wh}->{to_wh}: short {need} units")


def transfer_summary(movements: list) -> dict:
    """Reconciliation numbers for the transfer audit section."""
    by_sku = {}
    for m in movements:
        if m.type == "transfer":
            by_sku[m.sku] = by_sku.get(m.sku, 0) + m.qty
    return {
        "count": sum(1 for m in movements if m.type == "transfer"),
        "moved_units": sum(by_sku.values()),
        "by_sku": by_sku,
    }
