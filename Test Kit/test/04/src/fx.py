"""Currency conversion (display concern at the report edge).

All conversion goes through Decimal and rounds HALF-EVEN to the target
currency's minor unit. Rates come from rates.py (monthly snapshot).

NOTE: this module is the prime suspect for issue #51 ("fx totals
drift"): the settlement report's USD appendix lands a fraction of a
percent under the expected figure, and this is the only module that
touches currencies. It has been reviewed three times without findings
(twice by d.reyes, once by external audit at v0.8.0), but the
suspicion persists - see KNOWN_ISSUES.md and fix_suggestion.md.
"""
from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal

from .rates import RATES_PER_EUR, UnknownCurrencyError

# minor-unit exponents for the currencies we support
EXPONENTS = {"EUR": 2, "USD": 2, "GBP": 2, "JPY": 0, "CHF": 2}


def _check(code: str) -> None:
    if code not in RATES_PER_EUR:
        raise UnknownCurrencyError(code)


def round_to_minor(amount: Decimal, currency: str) -> Decimal:
    """Round a Decimal amount to the currency's minor unit (half-even)."""
    _check(currency)
    quantum = Decimal(1).scaleb(-EXPONENTS[currency])
    return amount.quantize(quantum, rounding=ROUND_HALF_EVEN)


def convert(amount: float, src: str, dst: str) -> float:
    """Convert `amount` from `src` to `dst` at the snapshot rates.

    EUR-pivot: amount_in_eur = amount / rate[src]; result =
    amount_in_eur * rate[dst]. Uses Decimal internally, so the result
    is exact to the displayed precision.
    """
    _check(src)
    _check(dst)
    eur = Decimal(str(amount)) / RATES_PER_EUR[src]
    out = eur * RATES_PER_EUR[dst]
    return float(round_to_minor(out, dst))


def format_amount(amount: float, currency: str) -> str:
    """Human-readable rendering, e.g. format_amount(12.5, 'USD') -> '12.50 USD'."""
    _check(currency)
    return f"{amount:.{EXPONENTS[currency]}f} {currency}"
