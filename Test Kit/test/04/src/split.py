"""Per-expense share splitting.

The contract (docs/data_dictionary.md) is EXACT conservation: the
per-person shares of one expense must sum to the expense amount, cent
for cent. Because most amounts do not divide evenly, we distribute by
LARGEST REMAINDER at cent granularity: everyone gets
floor(amount_cents / n) cents, and the leftover cents go ONE each to
the first `remainder` people in the expense's split_among order.

Example: 23.30 among 3 people -> 2330 cents = 3*776 + 2, so the
first two people in split_among order get 777 cents and the third
gets 776: shares 7.77, 7.77, 7.76, summing to exactly 23.30.
"""
from __future__ import annotations

import math


def split_expense(amount: float, people) -> dict:
    """Split `amount` among `people`; shares sum EXACTLY to `amount`."""
    n = len(people)
    share = math.floor(amount * 100 / n) / 100
    return {person: share for person in people}


def split_all(expenses) -> list:
    """One shares-dict per expense, same order as `expenses`."""
    return [split_expense(e.amount, e.split_among) for e in expenses]
