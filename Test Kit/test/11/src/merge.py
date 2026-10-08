"""Merge kept candidate start times into maximal bookable windows.

The api scans the workday in fixed steps (15 min) and keeps every
candidate start whose meeting conflicts with nothing. This module
collapses runs of consecutive kept starts into a single window:

    starts [600, 615, 630], duration 45 -> window (600, 675)
    i.e. "you can start any time from 10:00 to 10:30 and get 45 min",
    reported as the window 10:00-11:15 (first start .. last end).

A run breaks when consecutive starts are further apart than the
step. Every run - INCLUDING the last one of the day - produces a
window; an end-of-day window is a perfectly good meeting slot.
"""
from __future__ import annotations


def merge_windows(starts: list, duration_min: int,
                  step_min: int = 15) -> list:
    """-> [(window_start, window_end)] in minutes, order preserved."""
    windows = []
    run_start = None
    prev = None
    for s in starts:
        if prev is not None and s - prev != step_min:
            windows.append((run_start, prev + duration_min))
            run_start = s
        elif prev is None:
            run_start = s
        prev = s
    return windows
