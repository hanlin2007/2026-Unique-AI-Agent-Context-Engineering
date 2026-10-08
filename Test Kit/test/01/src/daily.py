"""Daily rollups: fold signed entries into end-of-day balances.

Each distinct active day produces ONE (date, closing) tuple, where
closing is the balance after that day's LAST entry. Days without
entries produce no tuple.
"""
from __future__ import annotations


class InsufficientFundsError(Exception):
    """Raised when an entry would overdraw the account."""


def apply_entry(balance: float, signed_amount: float) -> float:
    """Return the new balance after one signed entry.

    Overdrafts are rejected; taking the account to exactly zero is fine.
    """
    new_balance = round(balance + signed_amount, 2)
    if new_balance < 0:
        raise InsufficientFundsError(
            f"entry {signed_amount} overdraws the account ({balance})"
        )
    return new_balance


def compute_daily_rollups(entries) -> list:
    """Return sorted (date, closing_balance) tuples, one per active day."""
    daily = {}
    balance = 0.0
    for entry in entries:
        balance = apply_entry(balance, entry.signed_amount)
        daily.setdefault(entry.date, balance)
    return sorted(daily.items())
