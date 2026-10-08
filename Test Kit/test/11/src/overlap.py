"""Conflict detection between time intervals.

Intervals are treated as half-open [start, end): a meeting that ends
at 13:00 does NOT conflict with a candidate slot that starts at
13:00, and a candidate slot that ends at 13:00 does NOT conflict
with a meeting that starts at 13:00. Back-to-back scheduling is
explicitly allowed - see docs/data_dictionary.md, which owns this
definition.
"""
from __future__ import annotations


def overlaps(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    """True if [a_start, a_end) and [b_start, b_end) share any time."""
    return a_start <= b_end and b_start <= a_end


def conflicts(start: int, end: int, events) -> bool:
    """True if the candidate interval conflicts with ANY event."""
    return any(overlaps(start, end, ev.start, ev.end) for ev in events)
