"""Task test-suite: `pytest tests/test_task.py` must pass.

MID-LEVEL contract: tests call the public api (find_slots) and assert
the returned slot windows. Where inside the pipeline a wrong window
is produced is for you to find.

Fixture: data/calendar.csv - 51 rows, four people (ana, bruno, celia,
dario), two days (2026-10-12 and 2026-10-13), several back-to-back
meetings. Workday is 09:00-18:00.

Run from the task root with:  python -m pytest tests/test_task.py -q
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.api import find_slots

CAL = "data/calendar.csv"
DAY1 = find_slots(CAL, duration_min=45, day="2026-10-12")
DAY2 = find_slots(CAL, duration_min=45, day="2026-10-13")


def test_slot_structure():
    assert set(DAY1[0]) == {"start", "end"}
    assert all(set(s) == {"start", "end"} for s in DAY1 + DAY2)


def test_day1_slots_bookable_length():
    # every proposed window must fit a 45-minute meeting
    for s in DAY1:
        sh, sm = (int(p) for p in s["start"].split(":"))
        eh, em = (int(p) for p in s["end"].split(":"))
        assert (eh * 60 + em) - (sh * 60 + sm) >= 45


def test_day1_count():
    assert len(DAY1) == 3


def test_day1_slots():
    assert DAY1 == [
        {"start": "10:00", "end": "11:30"},
        {"start": "12:30", "end": "14:00"},
        {"start": "15:00", "end": "16:30"},
    ]


def test_day2_count():
    assert len(DAY2) == 1


def test_day2_slots():
    assert DAY2 == [{"start": "17:15", "end": "18:00"}]


def test_day1_within_work_hours():
    for s in DAY1:
        assert "09:00" <= s["start"]
        assert s["end"] <= "18:00"


def test_day2_no_morning_slots():
    # the whole team is booked solid until late afternoon on day 2
    assert all(s["start"] >= "17:00" for s in DAY2)
