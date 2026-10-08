"""Task test-suite: `pytest tests/test_task.py` must pass.

MID-LEVEL contract: these tests call ONE API - summarize() - and
assert the numbers in the returned dict. Where inside src/ a wrong
number is produced is for you to find.

Fixture: data/workouts.csv (a 9-week half-marathon block, 63 rows,
runs + rides + 2 rest days).

Definitions live in docs/metrics_definitions.md: weekly volume is RUN
distance per ISO week; pace per mile is the per-km pace scaled UP by
km-per-mile; fitness is an EMA of daily load with the standard
alpha = 2 / (window + 1).

Run from the task root with:  python -m pytest tests/test_task.py -q
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.summarize import summarize

SUMMARY = summarize("data/workouts.csv")


def test_span_and_session_counts():
    assert SUMMARY["span"] == {
        "first": "2026-07-27",
        "last": "2026-09-27",
        "days": 63,
    }
    assert SUMMARY["totals"]["sessions"] == 63
    assert SUMMARY["totals"]["runs"] == 52
    assert SUMMARY["totals"]["rides"] == 9
    assert SUMMARY["totals"]["rest_days"] == 2


def test_total_run_volume():
    assert SUMMARY["totals"]["run_km"] == 430.32
    assert SUMMARY["totals"]["run_minutes"] == 2292.6
    assert SUMMARY["totals"]["ride_km"] == 229.0


def test_week_w33_volume():
    assert SUMMARY["weeks"]["2026-W33"]["km"] == 45.69
    assert SUMMARY["weeks"]["2026-W33"]["runs"] == 5
    assert SUMMARY["weeks"]["2026-W33"]["minutes"] == 243.6


def test_week_w37_volume():
    # peak week of the block
    assert SUMMARY["weeks"]["2026-W37"]["km"] == 55.4
    assert SUMMARY["weeks"]["2026-W37"]["runs"] == 6


def test_avg_pace_km():
    assert SUMMARY["avg_pace_km"] == 5.328


def test_avg_pace_mile():
    # a mile is LONGER than a km, so this must EXCEED avg_pace_km
    assert SUMMARY["avg_pace_mile"] == 8.574


def test_peak_week_pace_mile():
    assert SUMMARY["weeks"]["2026-W37"]["pace_km"] == 5.305
    assert SUMMARY["weeks"]["2026-W37"]["pace_mile"] == 8.538


def test_fitness_final():
    # EMA of daily load, window 7, over the full 63-day span
    assert SUMMARY["fitness"]["final"] == 64.057


def test_fitness_series_length():
    assert SUMMARY["fitness"]["series_len"] == 63
    assert SUMMARY["fitness"]["window"] == 7


def test_fitness_peak():
    assert SUMMARY["fitness"]["peak"] == 80.406
