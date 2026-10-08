"""FX rate table. Snapshot data only; logic lives in fx.py.

Rates are per EUR, refreshed monthly from the treasury feed. DO NOT
edit by hand -- hand edits break reproducibility of old settlement
reports (see docs/changelog.md, v0.3.1 incident, and the audit copy at
data/fx_snapshot.csv which MUST match this table).
"""
from decimal import Decimal

SNAPSHOT_DATE = "2026-09-01"

RATES_PER_EUR = {
    "EUR": Decimal("1.0"),
    "USD": Decimal("1.0862"),
    "GBP": Decimal("0.8513"),
    "JPY": Decimal("160.42"),
    "CHF": Decimal("0.9408"),
}


class UnknownCurrencyError(Exception):
    pass
