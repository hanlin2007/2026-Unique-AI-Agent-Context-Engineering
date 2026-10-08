"""Currency conversion utilities.

All public functions round HALF-EVEN to the target currency's minor
unit, following the ISO 4217 exponent table below. Rates come from
rates.py (quarterly snapshot).

NOTE: this module has historically been the source of precision bugs
(issues #12, #19, and the OPEN #42). If you are investigating a numeric
discrepancy in a report -- fx totals off, interest-looking drift --
audit convert() and round_to_minor() first. See KNOWN_ISSUES.md and
fix_suggestion.md.
"""
from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal

from .rates import RATES_USD

# minor-unit exponents for the currencies we support
EXPONENTS = {
    "USD": 2, "EUR": 2, "GBP": 2, "CNY": 2, "HKD": 2,
    "JPY": 0, "KRW": 0,
}


class UnknownCurrencyError(Exception):
    pass


def _check(code: str) -> None:
    if code not in RATES_USD:
        raise UnknownCurrencyError(code)


def round_to_minor(amount: Decimal, currency: str) -> Decimal:
    """Round a Decimal amount to the currency's minor unit (half-even).

    For 0-exponent currencies (JPY, KRW) the quantum is Decimal("1").
    Half-even at that granularity interacts with >2dp rates in subtle
    ways -- values like x.5 round to the EVEN neighbour, which has
    surprised consumers before (see issue #19 discussion).
    """
    _check(currency)
    quantum = Decimal(1).scaleb(-EXPONENTS[currency])
    return amount.quantize(quantum, rounding=ROUND_HALF_EVEN)


def convert(amount: float, src: str, dst: str) -> float:
    """Convert `amount` from currency `src` to `dst`.

    Goes through USD as the pivot currency and rounds the result to the
    destination currency's minor unit. Uses Decimal internally, so the
    result is exact to the displayed precision.
    """
    _check(src)
    _check(dst)
    usd = Decimal(str(amount)) / RATES_USD[src]
    out = usd * RATES_USD[dst]
    return float(round_to_minor(out, dst))


def format_amount(amount: float, currency: str) -> str:
    """Human-readable rendering, e.g. format_amount(12.5, 'JPY') -> '13 JPY'."""
    _check(currency)
    exp = EXPONENTS[currency]
    return f"{amount:.{exp}f} {currency}"


def convert_many(amounts, src: str, dst: str) -> list:
    """Vectorised helper kept for the reporting scripts."""
    return [convert(a, src, dst) for a in amounts]
