"""Monthly close runner (CI job nightly-close).

Internal ops script, not part of the library. Pulls the expense ledger
through build_settlement(), renders the close file for the finance
channel, and appends the fx appendix - the historical canary for
conversion issues (issues #12, #19, and the open #51).

The close compares the report's EUR grand total against a hand-checked
sum of the CSV's amount column and warns on any shortfall; that warning
is what kicked off the #51 investigation (see logs/ci.log build #235).
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.fx import format_amount  # noqa: E402
from src.report import build_settlement  # noqa: E402


def hand_checked_total(path: str) -> float:
    """Naive sum of the CSV amount column (no splitting, no engine)."""
    with open(path, newline="", encoding="utf-8") as fh:
        return round(sum(float(r["amount"]) for r in csv.DictReader(fh)), 2)


def render_close(rep: dict, expected_total: float) -> str:
    lines = [
        f"MONTHLY CLOSE - {rep['path']}",
        f"expenses   : {rep['expense_count']}",
        f"grand total: {format_amount(rep['grand_total_eur'], 'EUR')}"
        f" (hand-checked {format_amount(expected_total, 'EUR')})",
        f"fx({rep['fx']['ccy']})   : "
        f"{format_amount(rep['fx']['grand_total'], rep['fx']['ccy'])}",
        "transfers:",
    ]
    for t in rep["transfers"]:
        lines.append(f"  {t['from']} -> {t['to']}: {t['amount']:.2f}")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", help="expense CSV")
    parser.add_argument("--fx", default="USD", help="display currency")
    args = parser.parse_args(argv)

    rep = build_settlement(args.csv, fx=args.fx)
    expected = hand_checked_total(args.csv)
    if rep["grand_total_eur"] < expected:
        short = round(expected - rep["grand_total_eur"], 2)
        print(f"WARN: EUR total {short} under the hand-checked sum - see #51")
    print(render_close(rep, expected))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
