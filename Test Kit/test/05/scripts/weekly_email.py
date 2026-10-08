"""Weekly training email (CI job weekly-email, Mondays 07:30).

Internal ops script, not part of the library. Builds the summary via
src.summarize, renders a plain-text email for the coach, and sends it
via the local relay.

PARKED since 2026-09-21 (issue #33): the plausibility guard below
refuses to send when pace-per-mile comes out faster than pace-per-km.
The guard fired on the 2026-09-21 run (see logs/ci.log build #173),
which is what kicked off the whole investigation. The working theory
is that loader.py buckets sessions into wrong weeks; the email stays
held until the suite is green.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.metrics import format_pace  # noqa: E402
from src.summarize import summarize  # noqa: E402


def render_email(summary: dict) -> str:
    weeks = summary["weeks"]
    last_week, slot = next(reversed(weeks.items()))
    lines = [
        f"Weekly training summary - {last_week}",
        "",
        f"run volume : {slot['km']:.2f} km over {slot['runs']} runs",
        f"avg pace   : {format_pace(summary['avg_pace_km'])}/km "
        f"({format_pace(summary['avg_pace_mile'])}/mile)",
        f"fitness    : {summary['fitness']['final']:.1f} "
        f"(peak {summary['fitness']['peak']:.1f})",
    ]
    return "\n".join(lines)


def plausible(summary: dict) -> bool:
    """Sanity gate: per-mile pace must EXCEED per-km pace."""
    return summary["avg_pace_mile"] > summary["avg_pace_km"]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", help="workout CSV")
    parser.add_argument("--send", action="store_true",
                        help="actually send (default: print only)")
    args = parser.parse_args(argv)

    summary = summarize(args.csv)
    if not plausible(summary):
        print("HELD: implausible pace figures (see module docstring)")
        return 1
    body = render_email(summary)
    if args.send:
        print("relay not configured in this environment; printing instead")
    print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
