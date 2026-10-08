"""Event/slot types and time helpers.

Times in the calendar CSV are "HH:MM" local wall-clock strings (the
office is single-timezone; see docs/data_dictionary.md). Internally
everything converts to minutes since midnight for arithmetic and
back to strings at the api edge, so no timezone logic exists here or
anywhere else in the pipeline. Event.end is EXCLUSIVE - the
half-open interval convention lives in this type, and every
comparison downstream inherits it.
"""
from __future__ import annotations

from typing import NamedTuple


def hhmm_to_min(t: str) -> int:
    """"HH:MM" -> minutes since midnight."""
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def min_to_hhmm(minutes: int) -> str:
    """Minutes since midnight -> "HH:MM"."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


class Event(NamedTuple):
    person: str
    day: str          # ISO date "YYYY-MM-DD"
    start: int        # minutes since midnight
    end: int          # minutes since midnight, exclusive
    title: str
