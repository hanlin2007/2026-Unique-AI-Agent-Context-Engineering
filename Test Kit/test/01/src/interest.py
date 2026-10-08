"""Interest accrual (feature added in v0.5.0).

Interest accrues DAILY on that day's CLOSING balance, at
annual_rate / 365 per day. Accrued amounts are summed across all days
and the total is rounded to 2 decimal places only at the end.

Example: with annual_rate = 0.0365 the daily factor is exactly 0.0001,
so a day closing at 1439.40 accrues 0.143944 that day.
"""
from __future__ import annotations

DEFAULT_ANNUAL_RATE = 0.0365


def accrue_interest(daily, annual_rate: float = DEFAULT_ANNUAL_RATE) -> float:
    """Return total interest accrued over the given daily rollups.

    `daily` is the (date, closing_balance) list from daily.py.
    Days are processed in order; every day accrues, including the last.
    """
    total = 0.0
    prev = 0.0
    for _date, closing in daily:
        total += prev * annual_rate / 365
        prev = closing
    return round(total, 2)


def effective_annual_rate(annual_rate: float = DEFAULT_ANNUAL_RATE) -> float:
    """APY given daily compounding of annual_rate/365 (display helper)."""
    return round((1 + annual_rate / 365) ** 365 - 1, 6)
