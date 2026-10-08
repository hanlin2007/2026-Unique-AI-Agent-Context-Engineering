"""Raw transaction model.

A Transaction is one row of the journal CSV. `kind` is the RAW journal
kind (see docs/data_dictionary.md); canonicalisation to signed entries
happens in normalize.py. Amounts are always positive floats in the
journal's native currency.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

RAW_KINDS = ("deposit", "withdrawal", "payment", "refund", "interest", "fee")


@dataclass(frozen=True)
class Transaction:
    date: date
    kind: str          # raw journal kind, see RAW_KINDS
    amount: float      # always positive; direction decided in normalize.py
    memo: str = ""

    def __post_init__(self):
        if self.kind not in RAW_KINDS:
            raise ValueError(f"unknown journal kind: {self.kind!r}")
        if self.amount <= 0:
            raise ValueError("transaction amount must be positive")
