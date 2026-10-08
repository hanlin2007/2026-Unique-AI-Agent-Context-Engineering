"""Monthly aggregation over rollups and entries.

month_summary() is pure: same inputs -> same output, no module state.
"""
from __future__ import annotations


def month_summary(entries, daily, year: int, month: int) -> dict:
    """Summarise one calendar month.

    Returns a dict with:
      opening      balance carried into the month (0.0 if none)
      closing      balance after the month's last active day
      total_in     sum of all inflows in the month
      total_out    sum of all outflows in the month (positive number)
      active_days  number of distinct days with at least one entry
    """
    in_month_daily = [(d, b) for (d, b) in daily
                      if d.year == year and d.month == month]
    month_entries = [e for e in entries
                     if e.date.year == year and e.date.month == month]

    opening = 0.0
    if in_month_daily:
        idx = daily.index(in_month_daily[0])
        if idx > 0:
            opening = daily[idx - 1][1]

    total_in = round(sum(e.signed_amount for e in month_entries
                         if e.signed_amount > 0), 2)
    total_out = round(-sum(e.signed_amount for e in month_entries
                           if e.signed_amount < 0), 2)

    return {
        "opening": round(opening, 2),
        "closing": in_month_daily[-1][1] if in_month_daily else opening,
        "total_in": total_in,
        "total_out": total_out,
        "active_days": len(in_month_daily),
    }
