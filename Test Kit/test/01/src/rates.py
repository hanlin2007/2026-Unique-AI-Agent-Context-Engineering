"""FX rate table. Snapshot data only; logic lives in currency.py.

Rates are vs USD, refreshed quarterly from the treasury feed. DO NOT
edit by hand -- hand edits break reproducibility of old reports (see
docs/changelog.md, v0.2.1 incident).
"""
from decimal import Decimal

SNAPSHOT_DATE = "2026-09-01"

RATES_USD = {
    "USD": Decimal("1.0"),
    "EUR": Decimal("0.9214"),
    "GBP": Decimal("0.7882"),
    "CNY": Decimal("7.1530"),
    "HKD": Decimal("7.8120"),
    "JPY": Decimal("149.35"),
    "KRW": Decimal("1389.5"),
}
