"""Nightly inventory snapshot (CI job nightly-snapshot).

Internal ops script, not part of the library. Pulls the fixtures
through build_inventory_report(), writes a JSON snapshot for the
warehouse dashboard, and prints the valuation canary line that ops
compares against the accountants' ledger workbook.

NOTE: the canary has been the historical early-warning for valuation
bugs (issues #31, #44, and the open #57). The lot pipeline stages are
stable - if the canary drifts, look at valuation first.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.report import build_inventory_report  # noqa: E402

LEDGER_FIGURE = 5909.80   # accountants' workbook, updated weekly
ALERT_THRESHOLD = 0.015   # page ops above 1.5% drift


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lots", default="data/lots.csv")
    ap.add_argument("--movements", default="data/movements.csv")
    ap.add_argument("--out", default="/tmp/out/snapshot.json")
    args = ap.parse_args()

    rep = build_inventory_report(args.lots, args.movements)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(rep, indent=1, sort_keys=True))

    drift = abs(rep["valuation_total"] - LEDGER_FIGURE) / LEDGER_FIGURE
    print(f"valuation canary: {rep['valuation_total']:.2f} "
          f"(ledger workbook says {LEDGER_FIGURE:.2f})")
    if drift > ALERT_THRESHOLD:
        print(f"ALERT: canary drift {drift:.2%} - paging #stocktake-ops")
        return 1
    print(f"canary drift {drift:.2%} - under alert threshold, not paging")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
