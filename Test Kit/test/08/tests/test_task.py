"""Task test-suite: `pytest tests/test_task.py` must pass.

BLACK-BOX contract: these tests treat the whole of src/ as one opaque
pipeline and only check the NUMBERS that come out of summarize_log().
Where inside the pipeline a wrong number is produced is for you to
find.

Fixture: data/access.log (26 requests, nginx combined format,
2026-09-30 13:00-18:59 UTC, including a slow-500 cluster at 15:xx).

Run from the task root with:  python -m pytest tests/test_task.py -q
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.api import summarize_log

SUMMARY = summarize_log("data/access.log")


def test_summary_structure():
    assert SUMMARY["events"] == 26
    assert SUMMARY["rejected"] == 0
    assert set(SUMMARY) >= {"hours", "status_rates", "response_time",
                            "top_paths"}


def test_hour_13():
    assert SUMMARY["hours"]["2026-09-30T13:00"] == 3


def test_hour_14():
    assert SUMMARY["hours"]["2026-09-30T14:00"] == 4


def test_hour_15():
    # the slow-500 cluster hour
    assert SUMMARY["hours"]["2026-09-30T15:00"] == 7


def test_hour_16():
    assert SUMMARY["hours"]["2026-09-30T16:00"] == 5


def test_hour_17():
    assert SUMMARY["hours"]["2026-09-30T17:00"] == 4


def test_hour_18():
    assert SUMMARY["hours"]["2026-09-30T18:00"] == 3


def test_5xx_rate():
    assert SUMMARY["status_rates"]["5xx"] == 0.1154


def test_p50():
    assert SUMMARY["response_time"]["p50"] == 0.075


def test_p95():
    assert SUMMARY["response_time"]["p95"] == 2.2
