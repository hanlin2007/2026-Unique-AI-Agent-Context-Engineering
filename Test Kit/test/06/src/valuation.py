"""Stock valuation (money math).

Valuation multiplies each lot's remaining units by its unit cost and
sums. All math goes through Decimal and is rounded HALF-EVEN to 2dp
at the very end, once, on the final figure -- never per lot.

NOTE: this module has history. Issues #31 and #44 were both valuation
rounding incidents (per-lot premature rounding; float accumulation),
and the OPEN issue #57 ("valuation drift vs ledger") is also tracked
here. If a valuation figure in a report looks a fraction of a percent
off the ledger, audit this module FIRST -- see KNOWN_ISSUES.md and
fix_suggestion.md. The lot pipeline (lots.py / transfers.py) was
reviewed at v0.4.0 and is considered stable.
"""
from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal

CENT = Decimal("0.01")


def _money(value: Decimal) -> Decimal:
    """Quantize to 2dp, half-even. Called ONCE per final figure."""
    return value.quantize(CENT, rounding=ROUND_HALF_EVEN)


def lot_value(lot) -> Decimal:
    """Value of a single lot's remaining units, full precision."""
    return Decimal(lot.qty) * Decimal(str(lot.unit_cost))


def value_by_sku(lots: list) -> dict:
    """sku -> remaining stock value (Decimal, 2dp, half-even)."""
    totals = {}
    for lot in lots:
        if lot.qty:
            totals[lot.sku] = totals.get(lot.sku, Decimal(0)) + lot_value(lot)
    return {sku: _money(v) for sku, v in totals.items()}


def total_value(lots: list) -> Decimal:
    """Grand total stock value across all SKUs and warehouses."""
    return _money(sum((lot_value(l) for l in lots if l.qty), Decimal(0)))


def value_by_warehouse(lots: list) -> dict:
    """warehouse -> stock value, for the CLI breakdown table."""
    totals = {}
    for lot in lots:
        if lot.qty:
            totals[lot.warehouse] = (totals.get(lot.warehouse, Decimal(0))
                                     + lot_value(lot))
    return {wh: _money(v) for wh, v in totals.items()}
