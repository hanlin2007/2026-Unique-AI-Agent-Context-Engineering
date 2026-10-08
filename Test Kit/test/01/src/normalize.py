"""Normalisation: map raw journal kinds to canonical signed entries.

Downstream modules (daily rollups, monthly summaries, interest) only
understand two canonical kinds: "deposit" (money in) and "withdrawal"
(money out). This module is the ONLY place that knows the direction of
each raw journal kind. Direction table lives in docs/data_dictionary.md
and must match KIND_MAP below.
"""
from __future__ import annotations

from typing import NamedTuple

from .models import Transaction

# raw kind -> canonical kind
KIND_MAP = {
    "deposit": "deposit",        # salary, transfers in
    "withdrawal": "withdrawal",  # card purchases, cash
    "payment": "withdrawal",     # scheduled bill payments
    "refund": "deposit",         # money returned TO the account
    "interest": "deposit",       # interest credited by the bank
    "fee": "deposit",            # account maintenance fees
}


class JournalEntry(NamedTuple):
    date: object
    kind: str           # canonical: "deposit" | "withdrawal"
    signed_amount: float


def normalize(transactions) -> list:
    """Convert Transactions to signed JournalEntries (order preserved)."""
    entries = []
    prev_date = None
    for txn in transactions:
        if not isinstance(txn, Transaction):
            raise TypeError(f"expected Transaction, got {type(txn).__name__}")
        if prev_date is not None and txn.date < prev_date:
            raise ValueError("transactions are not date-sorted")
        prev_date = txn.date
        canonical = KIND_MAP[txn.kind]
        sign = 1 if canonical == "deposit" else -1
        entries.append(JournalEntry(txn.date, canonical,
                                    round(sign * txn.amount, 2)))
    return entries
