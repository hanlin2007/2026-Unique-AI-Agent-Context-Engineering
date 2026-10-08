"""Value-date window rules.

A statement line dated up to WINDOW_DAYS after its ledger entry
still counts as the same transaction (bank settlement lag). The
window end is INCLUSIVE: a line dated exactly ledger_day +
WINDOW_DAYS is a valid match. Lines dated BEFORE the ledger entry
are never valid (the bank cannot settle a sale before it happens).

The rule is owned by docs/data_dictionary.md; if you change it here
without changing it there, expect the review to bounce.
"""
from __future__ import annotations

WINDOW_DAYS = 2


def in_window(ledger_day, statement_day) -> bool:
    """True if statement_day falls inside the value-date window."""
    delta = (statement_day - ledger_day).days
    return 0 <= delta < WINDOW_DAYS
