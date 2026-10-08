"""Workout log loader: CSV -> Workout records (IO edge).

CSV columns: date,type,distance_km,duration_min,avg_hr,notes.
Dates are ISO (YYYY-MM-DD) and timezone-NAIVE BY DESIGN: the log is a
runner's personal diary, entries are local calendar days, and the
project deliberately does not model timezones (see docs/changelog.md,
v0.9.0 decision). Weeks are ISO-8601 weeks (Monday start).

NOTE (issue #33): this module is the prime suspect for the drifting
pace/trend numbers - the theory is that date parsing silently shifts
some sessions into neighbouring weeks. It has been reviewed twice
without findings, but the suspicion persists.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date

TYPES = ("run", "bike", "rest")


@dataclass(frozen=True)
class Workout:
    date: date
    type: str           # "run" | "bike" | "rest"
    distance_km: float  # 0.0 on rest days
    duration_min: float
    avg_hr: int         # 0 on rest days
    notes: str = ""

    @property
    def iso_week(self) -> str:
        """ISO-8601 week label, e.g. '2026-W31'."""
        y, w, _ = self.date.isocalendar()
        return f"{y}-W{w:02d}"


def parse_row(row: dict) -> Workout:
    """Build a Workout from a csv.DictReader row."""
    wtype = row["type"].strip().lower()
    if wtype not in TYPES:
        raise ValueError(f"unknown workout type: {wtype!r}")
    return Workout(
        date=date.fromisoformat(row["date"].strip()),
        type=wtype,
        distance_km=round(float(row["distance_km"]), 2),
        duration_min=round(float(row["duration_min"]), 1),
        avg_hr=int(row["avg_hr"]),
        notes=row.get("notes", "").strip(),
    )


def load_workouts(path: str) -> list:
    """Load a workout CSV, date-sorted with a stable sort."""
    with open(path, newline="", encoding="utf-8") as fh:
        workouts = [parse_row(r) for r in csv.DictReader(fh)]
    workouts.sort(key=lambda w: w.date)
    return workouts
