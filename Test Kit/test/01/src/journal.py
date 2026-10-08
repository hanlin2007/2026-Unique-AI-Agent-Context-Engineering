"""Journal IO: load the CSV journal into sorted Transactions.

The CSV has columns date,kind,amount,memo with ISO dates. Rows are
returned date-sorted with a stable sort (intra-day order preserved),
which the rest of the pipeline relies on.
"""
from __future__ import annotations

import csv
from datetime import date

from .models import Transaction


def parse_row(row: dict) -> Transaction:
    """Build a Transaction from a csv.DictReader row."""
    y, m, d = (int(part) for part in row["date"].strip().split("-"))
    return Transaction(
        date=date(y, m, d),
        kind=row["kind"].strip().lower(),
        amount=round(float(row["amount"]), 2),
        memo=row.get("memo", "").strip(),
    )


def load_journal(path: str) -> list:
    """Load a journal CSV into a date-sorted list of Transactions."""
    with open(path, newline="", encoding="utf-8") as fh:
        txns = [parse_row(r) for r in csv.DictReader(fh)]
    txns.sort(key=lambda t: t.date)
    return txns
