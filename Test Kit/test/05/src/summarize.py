"""Training summary: the mid-level API used by tests, CLI and scripts.

summarize() runs the whole analysis:

    workouts CSV -> loader.load_workouts   (IO + sort)
                -> weekly run-volume rollup (ISO weeks, runs only)
                -> average pace (runs only, via src.metrics)
                -> fitness trend (daily load -> EMA, via src.trends)

Definitions (docs/metrics_definitions.md is authoritative):

  * weekly volume: RUN distance summed per ISO week. Rides are tracked
    as cross-training and never counted in run volume.
  * pace: total run minutes / total run km, reported per km and per
    mile (3dp).
  * daily load: duration_min * avg_hr / 100, summed per calendar day;
    days with no session (including rest entries) contribute 0.
  * fitness: EMA of the daily-load series with window 7 over the full
    calendar span (first log date .. last log date, inclusive).
"""
from __future__ import annotations

from datetime import timedelta

from .loader import load_workouts
from .metrics import pace_per_km, pace_per_mile
from .trends import ema

FITNESS_WINDOW = 7


def _daily_loads(workouts) -> list:
    """(date, load) pairs for every calendar day in the span."""
    by_day = {}
    for w in workouts:
        by_day[w.date] = by_day.get(w.date, 0.0) + w.duration_min * w.avg_hr / 100.0
    first, last = workouts[0].date, workouts[-1].date
    days = (last - first).days + 1
    return [(first + timedelta(days=i), by_day.get(first + timedelta(days=i), 0.0))
            for i in range(days)]


def _weekly_run_volume(workouts) -> dict:
    """ISO week -> run volume rollup (runs only; rides excluded)."""
    weeks = {}
    for w in workouts:
        if w.type != "run":
            continue
        slot = weeks.setdefault(w.iso_week, {"km": 0.0, "runs": 0, "minutes": 0.0})
        slot["km"] = round(slot["km"] + w.distance_km, 2)
        slot["runs"] += 1
        slot["minutes"] = round(slot["minutes"] + w.duration_min, 1)
    for slot in weeks.values():
        slot["pace_km"] = round(pace_per_km(slot["minutes"], slot["km"]), 3)
        slot["pace_mile"] = round(pace_per_mile(slot["minutes"], slot["km"]), 3)
    return weeks


def summarize(path: str) -> dict:
    """Build the training summary dict for a workout CSV."""
    workouts = load_workouts(path)
    runs = [w for w in workouts if w.type == "run"]
    rides = [w for w in workouts if w.type == "bike"]
    rest = [w for w in workouts if w.type == "rest"]

    run_km = round(sum(w.distance_km for w in runs), 2)
    run_min = round(sum(w.duration_min for w in runs), 1)

    daily = _daily_loads(workouts)
    series = ema([load for _, load in daily], window=FITNESS_WINDOW)

    return {
        "path": path,
        "span": {
            "first": workouts[0].date.isoformat(),
            "last": workouts[-1].date.isoformat(),
            "days": (workouts[-1].date - workouts[0].date).days + 1,
        },
        "totals": {
            "sessions": len(workouts),
            "runs": len(runs),
            "rides": len(rides),
            "rest_days": len(rest),
            "run_km": run_km,
            "run_minutes": run_min,
            "ride_km": round(sum(w.distance_km for w in rides), 2),
        },
        "weeks": _weekly_run_volume(workouts),
        "avg_pace_km": round(pace_per_km(run_min, run_km), 3),
        "avg_pace_mile": round(pace_per_mile(run_min, run_km), 3),
        "fitness": {
            "window": FITNESS_WINDOW,
            "series_len": len(series),
            "final": round(series[-1], 3),
            "peak": round(max(series), 3),
        },
    }
