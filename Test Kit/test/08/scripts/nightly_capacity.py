"""Nightly capacity report (CI job nightly-capacity).

Ops script, not part of the library. Summarizes the day's access log
via summarize_log(), writes JSON for the capacity dashboard, and
prints the CDN cross-check line that ops compares against the CDN
provider's own request counts.

NOTE: the cross-check has been the historical early-warning for
parsing bugs (issues #17, #35, and the open #71): if we count fewer
requests than the CDN, the sample is short and the trail has always
led to the parser. The analytics modules are stable.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.api import summarize_log  # noqa: E402

# CDN provider's own per-hour request counts for the fixture window
CDN_COUNTS = {"2026-09-30T13:00": 3, "2026-09-30T14:00": 4,
              "2026-09-30T15:00": 7, "2026-09-30T16:00": 5,
              "2026-09-30T17:00": 4, "2026-09-30T18:00": 3}
ALERT_THRESHOLD = 0.10   # page above 10% hourly shortfall


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default="data/access.log")
    ap.add_argument("--out", default="/tmp/out/capacity.json")
    args = ap.parse_args()

    rep = summarize_log(args.log)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(rep, indent=1, sort_keys=True))

    worst = 0.0
    for label, cdn in CDN_COUNTS.items():
        ours = rep["hours"].get(label, 0)
        shortfall = (cdn - ours) / cdn
        worst = max(worst, shortfall)
        if shortfall > ALERT_THRESHOLD:
            print(f"CDN cross-check: {label} counted {ours}, "
                  f"CDN says {cdn} ({shortfall:+.0%})")
    print(f"parsed {rep['events']} events, {rep['rejected']} rejected")
    if worst > ALERT_THRESHOLD:
        print("ALERT: hour shortfall over threshold - see issue #71")
        return 1
    print("cross-check within tolerance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
