"""Ledger CSV IO.

Columns: date,id,kind,amount,memo. Kinds are defined in
docs/data_dictionary.md:

    S  sale        money in from customers
    R  refund      money returned to a customer (negative amount)
    T  transfer    internal account movements
    F  fee accrual INTERNAL bookkeeping - excluded from reconciliation

F rows never appear on the bank statement as separate lines (the
bank nets them into the quarterly service charge), so they must NOT
participate in matching. The kind filter below is the ONLY place
this exclusion is implemented.

Amounts are signed decimal strings in the CSV and are parsed to
floats here; refunds are negative.
"""
from __future__ import annotations

import csv
from datetime import date
from typing import NamedTuple

# kinds that participate in reconciliation (see module docstring)
MATCHABLE_KINDS = ("S", "R", "T", "F")


class LedgerEntry(NamedTuple):
    day: date
    entry_id: str
    kind: str
    amount: float
    memo: str


def _parse_day(s: str) -> date:
    y, m, d = (int(part) for part in s.strip().split("-"))
    return date(y, m, d)


def load_ledger(path: str) -> list:
    """Load ALL ledger rows (any kind), file order preserved."""
    entries = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            entries.append(LedgerEntry(
                day=_parse_day(row["date"]),
                entry_id=row["id"].strip(),
                kind=row["kind"].strip(),
                amount=round(float(row["amount"]), 2),
                memo=row.get("memo", "").strip(),
            ))
    return entries


def matchable(entries: list) -> list:
    """Filter to the kinds that participate in reconciliation."""
    return [e for e in entries if e.kind in MATCHABLE_KINDS]
