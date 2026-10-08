"""Command line interface for fittrack.

Usage:
    python -m src.cli summary data/workouts.csv
    python -m src.cli weeks   data/workouts.csv
    python -m src.cli fitness data/workouts.csv
"""
from __future__ import annotations

import sys

from .metrics import format_pace
from .summarize import summarize


def _cmd_summary(path: str) -> None:
    s = summarize(path)
    t = s["totals"]
    print(f"log: {s['path']}")
    print(f"span: {s['span']['first']} .. {s['span']['last']} ({s['span']['days']} days)")
    print(f"sessions: {t['sessions']} (runs {t['runs']}, rides {t['rides']}, "
          f"rest {t['rest_days']})")
    print(f"run volume: {t['run_km']:.2f} km in {t['run_minutes']:.1f} min")
    print(f"avg pace: {format_pace(s['avg_pace_km'])}/km "
          f"({format_pace(s['avg_pace_mile'])}/mile)")
    f = s["fitness"]
    print(f"fitness (EMA window {f['window']}): final {f['final']:.1f}, "
          f"peak {f['peak']:.1f}")


def _cmd_weeks(path: str) -> None:
    s = summarize(path)
    print(f"{'week':<10} {'km':>7} {'runs':>5} {'pace/km':>8} {'pace/mi':>8}")
    print("-" * 42)
    for week, slot in s["weeks"].items():
        print(f"{week:<10} {slot['km']:>7.2f} {slot['runs']:>5} "
              f"{format_pace(slot['pace_km']):>8} {format_pace(slot['pace_mile']):>8}")


def _cmd_fitness(path: str) -> None:
    s = summarize(path)
    f = s["fitness"]
    print(f"window={f['window']} days={f['series_len']}")
    print(f"final={f['final']:.3f} peak={f['peak']:.3f}")


def main(argv) -> int:
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    command, path = argv[1], argv[2]
    if command == "summary":
        _cmd_summary(path)
    elif command == "weeks":
        _cmd_weeks(path)
    elif command == "fitness":
        _cmd_fitness(path)
    else:
        print(f"unknown command: {command}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
