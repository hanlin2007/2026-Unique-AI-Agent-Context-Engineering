"""Pace and speed maths.

Contracts (docs/metrics_definitions.md is the authoritative text):

  * pace_per_km   = minutes / kilometres            (min per km)
  * pace_per_mile = pace_per_km * KM_PER_MILE       (min per mile)

A mile is LONGER than a kilometre, so a per-mile pace is always a
LARGER number of minutes than the equivalent per-km pace. If a
per-mile figure ever comes out smaller than the per-km figure, the
conversion direction is wrong.
"""
from __future__ import annotations

KM_PER_MILE = 1.60934


def pace_per_km(minutes: float, km: float) -> float:
    """Minutes per kilometre. Raises ValueError on non-positive km."""
    if km <= 0:
        raise ValueError("distance must be positive for pace")
    return minutes / km


def pace_per_mile(minutes: float, km: float) -> float:
    """Minutes per mile: the per-km pace scaled by km-per-mile."""
    return pace_per_km(minutes, km) / KM_PER_MILE


def speed_kmh(minutes: float, km: float) -> float:
    """Average speed in km/h. Raises ValueError on non-positive inputs."""
    if km <= 0 or minutes <= 0:
        raise ValueError("distance and duration must be positive")
    return km / (minutes / 60.0)


def format_pace(pace_min: float) -> str:
    """Render a decimal-minute pace as M:SS, e.g. 5.283 -> '5:17'."""
    minutes = int(pace_min)
    seconds = round((pace_min - minutes) * 60)
    if seconds == 60:
        minutes, seconds = minutes + 1, 0
    return f"{minutes}:{seconds:02d}"
