"""Task test-suite: `pytest tests/test_task.py` must pass.

BLACK-BOX contract: these tests treat the whole of src/ as one opaque
pipeline and only check the NUMBERS that come out of
build_inventory_report(). Where inside the pipeline a wrong number is
produced is for you to find.

Fixtures: data/lots.csv (Q3 lot receipts, 40 lots, 8 SKUs, two
warehouses) and data/movements.csv (Q3 orders + inter-warehouse
transfers, 66 movements).

Run from the task root with:  python -m pytest tests/test_task.py -q
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.report import build_inventory_report

REPORT = build_inventory_report("data/lots.csv", "data/movements.csv")


def test_report_structure():
    assert REPORT["warehouses"] == ["main", "annex"]
    assert len(REPORT["skus"]) == 8
    assert set(REPORT) >= {"skus", "grand_units", "reorder_list",
                           "valuation_total", "transfers"}


def test_closing_sku_a():
    assert REPORT["skus"]["SKU-A"]["closing"] == {"main": 90, "annex": 0}
    assert REPORT["skus"]["SKU-A"]["total"] == 90


def test_closing_sku_d():
    # 10 units transferred main -> annex on 2026-08-12 (TRF-301)
    assert REPORT["skus"]["SKU-D"]["closing"] == {"main": 26, "annex": 12}
    assert REPORT["skus"]["SKU-D"]["total"] == 38


def test_closing_sku_g():
    # 8 units transferred annex -> main on 2026-08-19 (TRF-302)
    assert REPORT["skus"]["SKU-G"]["closing"] == {"main": 28, "annex": 42}
    assert REPORT["skus"]["SKU-G"]["total"] == 70


def test_grand_units():
    assert REPORT["grand_units"] == 518


def test_reorder_list():
    # only SKUs strictly below their reorder point
    assert REPORT["reorder_list"] == ["SKU-F"]


def test_valuation_sku_a():
    # remaining lots after FIFO consumption: 10 @ 1.26 + 60 @ 1.34
    assert REPORT["skus"]["SKU-A"]["valuation"] == 119.8


def test_valuation_sku_b():
    # remaining lots after FIFO consumption: 20 @ 4.28 + 40 @ 4.42
    assert REPORT["skus"]["SKU-B"]["valuation"] == 262.4


def test_valuation_total():
    assert REPORT["valuation_total"] == 5909.8


def test_transfers_summary():
    assert REPORT["transfers"] == {
        "count": 2,
        "moved_units": 18,
        "by_sku": {"SKU-D": 10, "SKU-G": 8},
    }
