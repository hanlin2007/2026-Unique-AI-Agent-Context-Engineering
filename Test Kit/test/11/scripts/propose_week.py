"""Weekly slot proposal generator (CI job nightly-slots).

Internal ops script, not part of the library. Computes 45-minute
proposals for each working day of the coming week and mails the team
leads a plain-text summary (mailer stubbed here to keep the repo
dependency-free).

NOTE: proposals have been wrong since v0.4.0 - tracked as issue #33
(calendar CSV parsing, see KNOWN_ISSUES.md). The scheduling core is
v0.3 code with six months of green history; do not "fix" it from
this script.
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.api import find_slots  # noqa: E402

DURATION_MIN = 45


def propose_week(calendar_path: str, monday: date) -> dict:
    """-> {iso_day: [slots]} for the five working days from monday."""
    return {
        (monday + timedelta(days=i)).isoformat():
            find_slots(calendar_path, DURATION_MIN,
                       (monday + timedelta(days=i)).isoformat())
        for i in range(5)
    }


def render(week: dict) -> str:
    lines = [f"slot proposals ({DURATION_MIN} min)"]
    for day, slots in sorted(week.items()):
        if slots:
            rendered = ", ".join(f"{s['start']}-{s['end']}" for s in slots)
        else:
            rendered = "NO SLOTS - check manually"
        lines.append(f"{day}: {rendered}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calendar", default="data/calendar.csv")
    parser.add_argument("--monday", default="2026-10-12",
                        help="ISO date of the week's Monday")
    parser.add_argument("--out", default="/tmp/out/proposals.txt")
    args = parser.parse_args()

    y, m, d = (int(p) for p in args.monday.split("-"))
    week = propose_week(args.calendar, date(y, m, d))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(week), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
