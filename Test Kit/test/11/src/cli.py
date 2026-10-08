"""Command line interface for schedulex.

Usage:
    python -m src.cli slots data/calendar.csv 2026-10-12 45
    python -m src.cli busy  data/calendar.csv 2026-10-12
"""
from __future__ import annotations

import sys

from .api import find_slots
from .icsio import load_events
from .model import min_to_hhmm


def _cmd_slots(path: str, day: str, duration_min: int) -> None:
    slots = find_slots(path, duration_min, day)
    if not slots:
        print("no free slots")
        return
    for s in slots:
        print(f"{s['start']} - {s['end']}")


def _cmd_busy(path: str, day: str) -> None:
    events = sorted(load_events(path, day), key=lambda e: e.start)
    for ev in events:
        print(f"{min_to_hhmm(ev.start)} - {min_to_hhmm(ev.end)}  "
              f"{ev.person:<8} {ev.title}")


def main(argv) -> int:
    if len(argv) < 4:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "slots":
        if len(argv) < 5:
            print(__doc__)
            return 2
        _cmd_slots(argv[2], argv[3], int(argv[4]))
    elif cmd == "busy":
        _cmd_busy(argv[2], argv[3])
    else:
        print(f"unknown command: {cmd}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
