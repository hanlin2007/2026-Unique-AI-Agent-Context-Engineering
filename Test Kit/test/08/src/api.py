"""Mid-level API: one log file in, one summary dict out.

summarize_log() is the function the tests and the CLI both use:

    parser.parse_log            (IO edge: lines -> events)
    buckets.hourly_counts       (events -> per-hour request counts)
    stats.status_class_rates    (events -> 2xx/4xx/5xx shares)
    stats.response_time_summary (events -> mean/p50/p95)

The returned dict is the task's contract. Rates are 4dp floats,
response-time figures 3dp floats, hour labels ISO-like strings.
"""
from __future__ import annotations

from collections import Counter

from .buckets import hourly_counts
from .parser import parse_log
from .stats import response_time_summary, status_class_rates


def summarize_log(path: str) -> dict:
    """Build the summary dict for one access log (module docstring)."""
    events, rejects = parse_log(path)
    top_paths = Counter(ev.path for ev in events).most_common(3)
    return {
        "log": path,
        "events": len(events),
        "rejected": len(rejects),
        "hours": hourly_counts(events),
        "status_rates": status_class_rates(events),
        "response_time": response_time_summary(events),
        "top_paths": [[p, c] for p, c in top_paths],
    }
