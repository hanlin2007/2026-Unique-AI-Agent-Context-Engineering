"""Trend helpers: rolling means and exponential moving averages.

The exponential moving average uses the STANDARD smoothing factor

    alpha = 2 / (window + 1)

(i.e. window=7 -> alpha=0.25), matching the definition in
docs/metrics_definitions.md and every pandas/TA reference. The series
is seeded with the first observation: ema[0] == values[0].
"""
from __future__ import annotations


def ema(values, window: int) -> list:
    """Exponential moving average of `values` with the given window."""
    if window < 1:
        raise ValueError("window must be >= 1")
    alpha = 2 / window
    out = []
    current = None
    for value in values:
        current = value if current is None else alpha * value + (1 - alpha) * current
        out.append(current)
    return out


def rolling_mean(values, window: int) -> list:
    """Simple trailing mean; leading positions use partial windows."""
    if window < 1:
        raise ValueError("window must be >= 1")
    out = []
    for i in range(len(values)):
        lo = max(0, i - window + 1)
        chunk = values[lo:i + 1]
        out.append(sum(chunk) / len(chunk))
    return out
