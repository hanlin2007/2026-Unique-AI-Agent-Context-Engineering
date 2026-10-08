"""Mid-level API: find_slots(). Used by tests and the CLI.

find_slots(calendar_csv, duration_min, day) scans the workday
(09:00-18:00) in 15-minute steps, keeps every candidate meeting of
duration_min that conflicts with NO team event, and merges the kept
candidates into maximal bookable windows. The whole team must be
free: a candidate conflicts if it overlaps ANY event on that day.
"""
from __future__ import annotations

from .icsio import load_events
from .merge import merge_windows
from .model import min_to_hhmm
from .overlap import overlaps

WORK_START_MIN = 9 * 60
WORK_END_MIN = 18 * 60
STEP_MIN = 15


def find_slots(calendar_path: str, duration_min: int, day: str) -> list:
    """-> [{"start": "HH:MM", "end": "HH:MM"}, ...], earliest first."""
    events = load_events(calendar_path, day)
    kept = []
    t = WORK_START_MIN
    while t + duration_min <= WORK_END_MIN:
        if not any(overlaps(t, t + duration_min, ev.start, ev.end)
                   for ev in events):
            kept.append(t)
        t += STEP_MIN
    windows = merge_windows(kept, duration_min, STEP_MIN)
    return [{"start": min_to_hhmm(s), "end": min_to_hhmm(e)}
            for s, e in windows]
