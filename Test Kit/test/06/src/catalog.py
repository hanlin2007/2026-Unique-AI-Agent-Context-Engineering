"""Static SKU catalogue.

The catalogue is the single source of truth for SKU display names,
reorder points and supplier lead times. Reorder POINT semantics
(when a SKU goes onto the reorder list) are defined in
docs/data_dictionary.md -- this module only stores the numbers.
"""
from __future__ import annotations

WAREHOUSES = ("main", "annex")

# sku -> static attributes
CATALOG = {
    "SKU-A": {"name": "anchor bolt M8x40 (box)", "reorder_point": 60, "lead_time_days": 7},
    "SKU-B": {"name": "corner bracket 32mm", "reorder_point": 50, "lead_time_days": 10},
    "SKU-C": {"name": "panel clip (bag of 100)", "reorder_point": 40, "lead_time_days": 5},
    "SKU-D": {"name": "vent duct 100mm elbow", "reorder_point": 25, "lead_time_days": 12},
    "SKU-E": {"name": "rack rail kit 42U", "reorder_point": 30, "lead_time_days": 7},
    "SKU-F": {"name": "flange plate 4in", "reorder_point": 45, "lead_time_days": 14},
    "SKU-G": {"name": "door gasket strip 6m", "reorder_point": 35, "lead_time_days": 9},
    "SKU-H": {"name": "hex nut M6 (jar)", "reorder_point": 20, "lead_time_days": 4},
}


def sku_names() -> dict:
    """sku -> display name, for report rendering."""
    return {sku: attrs["name"] for sku, attrs in CATALOG.items()}


def reorder_point(sku: str) -> int:
    """Reorder point for a SKU (total across ALL warehouses)."""
    return CATALOG[sku]["reorder_point"]
