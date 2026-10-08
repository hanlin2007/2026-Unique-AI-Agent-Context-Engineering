"""Task test-suite: `pytest tests/test_task.py` must pass.

BLACK-BOX contract: these tests treat the whole pipeline as opaque
and only check the NUMBERS and ID LISTS that come out of
build_recon_report(). Where inside the pipeline a wrong value is
produced is for you to find.

Fixtures: data/ledger.csv (45 rows, September 2026) and
data/bank_statement.csv (42 lines, same period).

Run from the task root with:  python -m pytest tests/test_task.py -q
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.report import build_recon_report

REP = build_recon_report("data/ledger.csv", "data/bank_statement.csv")


def test_report_structure():
    assert set(REP) >= {"ledger_rows", "considered", "matched",
                        "unmatched_ledger", "unmatched_statement",
                        "duplicates", "total_matched",
                        "total_unmatched_ledger",
                        "total_unmatched_statement"}


def test_ledger_rows():
    assert REP["ledger_rows"] == 45


def test_considered_entries():
    assert REP["considered"] == 43


def test_matched_count():
    assert REP["matched"] == 41


def test_unmatched_ledger_ids():
    assert REP["unmatched_ledger"] == ["L-0116", "L-0138"]


def test_unmatched_statement_refs():
    assert REP["unmatched_statement"] == ["BNK-0242"]


def test_duplicate_matches():
    assert REP["duplicates"] == 0


def test_total_matched():
    assert REP["total_matched"] == 8770.29


def test_total_unmatched_ledger():
    assert REP["total_unmatched_ledger"] == 360.0


def test_total_unmatched_statement():
    assert REP["total_unmatched_statement"] == 3.1
