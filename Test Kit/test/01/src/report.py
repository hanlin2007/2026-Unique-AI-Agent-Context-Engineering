"""Report assembly: the single entry point used by tests and the CLI.

build_report() runs the whole pipeline:

    journal CSV -> journal.load_journal     (IO + sort)
                -> normalize.normalize      (raw kinds -> signed entries)
                -> daily.compute_daily_rollups
                -> aggregate.month_summary  (per calendar month)
                -> interest.accrue_interest (over all rollups)
                -> currency.convert         (FX appendix, display only)

The returned dict is the task's contract. Money fields are rounded to
2dp; FX fields are integers in the target currency's minor unit.
"""
from __future__ import annotations

from .aggregate import month_summary
from .currency import convert
from .daily import compute_daily_rollups
from .interest import DEFAULT_ANNUAL_RATE, accrue_interest
from .journal import load_journal
from .normalize import normalize

NATIVE_CURRENCY = "USD"


def fx_appendix(total_in: float, total_out: float, fx_currency: str) -> dict:
    """Convert grand flow totals into a display currency.

    NOTE: issue #42 suspects the rounding in this section - if report
    numbers drift, start in src/currency.py (see fix_suggestion.md).
    """
    return {
        "ccy": fx_currency,
        "total_in": int(convert(total_in, NATIVE_CURRENCY, fx_currency)),
        "total_out": int(convert(total_out, NATIVE_CURRENCY, fx_currency)),
    }


def build_report(journal_path: str, fx: str = "USD",
                 annual_rate: float = DEFAULT_ANNUAL_RATE) -> dict:
    """Build the full report dict for a journal CSV (see module docstring)."""
    txns = load_journal(journal_path)
    entries = normalize(txns)
    daily = compute_daily_rollups(entries)

    month_keys = sorted({(d.year, d.month) for d, _ in daily})
    months = {f"{y}-{m:02d}": month_summary(entries, daily, y, m)
              for y, m in month_keys}

    total_in = round(sum(m["total_in"] for m in months.values()), 2)
    total_out = round(sum(m["total_out"] for m in months.values()), 2)

    return {
        "journal": journal_path,
        "native_currency": NATIVE_CURRENCY,
        "months": months,
        "grand": {
            "total_in": total_in,
            "total_out": total_out,
            "closing": daily[-1][1] if daily else 0.0,
        },
        "interest": {
            "annual_rate": annual_rate,
            "accrued": accrue_interest(daily, annual_rate),
        },
        "fx": fx_appendix(total_in, total_out, fx),
    }
