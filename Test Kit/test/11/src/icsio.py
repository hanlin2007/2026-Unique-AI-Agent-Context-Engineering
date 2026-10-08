"""Calendar CSV IO.

CSV columns: person,day,start,end,title. Times are local "HH:MM"
strings - the office is single-timezone, so there are NO offsets to
parse and no timezone database involved (see
docs/data_dictionary.md). Rows are returned in file order; filtering
by day happens here so the rest of the pipeline never sees another
day's events.

NOTE: this module has a history of parsing incidents (#11: a
newline-at-EOF crash, #27: the 9:00-without-leading-zero row). It was
rewritten at v0.4.0 onto csv.DictReader and is believed correct, but
it remains the first suspect whenever a slot looks missing - see
KNOWN_ISSUES.md #33.
"""
from __future__ import annotations

import csv

from .model import Event, hhmm_to_min


def load_events(path: str, day: str) -> list:
    """Load events for one ISO day from the calendar CSV."""
    events = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["day"].strip() != day:
                continue
            events.append(Event(
                person=row["person"].strip(),
                day=row["day"].strip(),
                start=hhmm_to_min(row["start"].strip()),
                end=hhmm_to_min(row["end"].strip()),
                title=row["title"].strip(),
            ))
    return events


def count_rows(path: str) -> int:
    """Total data rows in the CSV (debug/inspection helper)."""
    with open(path, newline="", encoding="utf-8") as fh:
        return sum(1 for _ in csv.DictReader(fh))
