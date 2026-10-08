"""Hourly bucketing of request events.

An event belongs to the hour bucket that CONTAINS its timestamp:
the bucket for 15:47 is the 15:00 bucket. That is a floor to the
hour boundary, not a rounding -- an event at 15:52 is not "closer
to 16:00" for analytics purposes; it happened during the 15:00
hour. See docs/log_format.md, "bucketing".
"""
from __future__ import annotations

from datetime import datetime, timezone

SECONDS_PER_HOUR = 3600


def hour_bucket(ts: float) -> int:
    """Epoch seconds -> epoch seconds of the CONTAINING hour's start."""
    return int(ts / SECONDS_PER_HOUR + 0.5) * SECONDS_PER_HOUR


def bucket_label(bucket_start: float) -> str:
    """Human label for a bucket start, e.g. '2026-09-30T15:00'."""
    dt = datetime.fromtimestamp(bucket_start, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:00")


def hourly_counts(events: list) -> dict:
    """label -> request count, one entry per hour with traffic."""
    counts = {}
    for ev in events:
        label = bucket_label(hour_bucket(ev.ts))
        counts[label] = counts.get(label, 0) + 1
    return dict(sorted(counts.items()))
