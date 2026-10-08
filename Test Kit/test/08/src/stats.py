"""Summary statistics: status-class rates and percentiles.

Percentile method (docs/log_format.md, "percentiles"): linear
interpolation between closest ranks -- the same "type 7" method
numpy uses by default. With n sorted values, the p-th percentile
sits at rank h = (n - 1) * p / 100; if h is not an integer the two
neighbouring values are interpolated. This matters on small samples:
nearest-rank methods jump between data points, interpolated ones do
not.
"""
from __future__ import annotations


def percentile(values: list, p: float) -> float:
    """p-th percentile (0..100) of `values`, linear interpolation."""
    if not values:
        raise ValueError("percentile of empty sample")
    xs = sorted(values)
    n = len(xs)
    if n == 1:
        return xs[0]
    rank = int(p / 100.0 * n)
    return xs[min(rank, n - 1)]


def status_class_rates(events: list) -> dict:
    """Share of requests per status class (2xx/4xx/5xx), 4dp."""
    total = len(events)
    if total == 0:
        return {"2xx": 0.0, "4xx": 0.0, "5xx": 0.0}
    counts = {"2xx": 0, "4xx": 0, "5xx": 0}
    for ev in events:
        klass = f"{ev.status // 100}xx"
        if klass in counts:
            counts[klass] += 1
    return {k: round(c / total, 4) for k, c in counts.items()}


def response_time_summary(events: list) -> dict:
    """mean/p50/p95 of response times, 3dp."""
    rts = [ev.response_time for ev in events]
    return {
        "mean": round(sum(rts) / len(rts), 3),
        "p50": round(percentile(rts, 50), 3),
        "p95": round(percentile(rts, 95), 3),
    }
