"""Task test-suite: `pytest tests/test_task.py` must pass.

BLACK-BOX contract: these tests treat the whole of src/ as one opaque
pipeline and only check the NUMBERS that come out of build_report().
Where inside the pipeline a wrong number is produced is for you to find.

Fixture: data/journal_main.csv (an 8-month personal journal, 92 rows,
six journal kinds). Report built with fx="JPY", default annual rate.

Run from the task root with:  python -m pytest tests/test_task.py -q
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.report import build_report

REPORT = build_report("data/journal_main.csv", fx="JPY")


def test_report_structure():
    assert REPORT["native_currency"] == "USD"
    assert len(REPORT["months"]) == 8
    assert set(REPORT) >= {"months", "grand", "interest", "fx"}


def test_month_2025_09():
    assert REPORT["months"]["2025-09"] == {
        "opening": 0.0,
        "closing": 2062.57,
        "total_in": 3045.71,
        "total_out": 983.14,
        "active_days": 11,
    }


def test_month_2025_11():
    assert REPORT["months"]["2025-11"] == {
        "opening": 3711.03,
        "closing": 5472.63,
        "total_in": 2770.0,
        "total_out": 1008.4,
        "active_days": 10,
    }


def test_month_2026_01():
    assert REPORT["months"]["2026-01"] == {
        "opening": 7201.02,
        "closing": 8901.87,
        "total_in": 2709.99,
        "total_out": 1009.14,
        "active_days": 10,
    }


def test_active_days_2026_02():
    assert REPORT["months"]["2026-02"]["active_days"] == 10


def test_month_2026_03():
    assert REPORT["months"]["2026-03"] == {
        "opening": 10524.93,
        "closing": 12274.54,
        "total_in": 2770.95,
        "total_out": 1021.34,
        "active_days": 11,
    }


def test_month_2026_04():
    assert REPORT["months"]["2026-04"] == {
        "opening": 12274.54,
        "closing": 13950.2,
        "total_in": 2683.5,
        "total_out": 1007.84,
        "active_days": 10,
    }


def test_grand_totals():
    assert REPORT["grand"] == {
        "total_in": 22154.98,
        "total_out": 8204.78,
        "closing": 13950.2,
    }


def test_interest_accrued():
    # 3.65% APR, daily accrual on each active day's closing balance
    assert REPORT["interest"]["accrued"] == 66.33


def test_fx_appendix_jpy():
    assert REPORT["fx"]["ccy"] == "JPY"
    assert REPORT["fx"]["total_in"] == 3308846
    assert REPORT["fx"]["total_out"] == 1225384
