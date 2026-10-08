"""Command line interface for bankrecon.

Usage:
    python -m src.cli summary   data/ledger.csv data/bank_statement.csv
    python -m src.cli unmatched data/ledger.csv data/bank_statement.csv
"""
from __future__ import annotations

import sys

from .report import build_recon_report


def _cmd_summary(ledger: str, statement: str) -> None:
    rep = build_recon_report(ledger, statement)
    print(f"ledger rows:        {rep['ledger_rows']}")
    print(f"considered:         {rep['considered']}")
    print(f"matched:            {rep['matched']}")
    print(f"duplicates:         {rep['duplicates']}")
    print(f"total matched:      {rep['total_matched']:.2f}")
    print(f"unmatched ledger:   {rep['total_unmatched_ledger']:.2f} "
          f"({len(rep['unmatched_ledger'])} entries)")
    print(f"unmatched stmt:     {rep['total_unmatched_statement']:.2f} "
          f"({len(rep['unmatched_statement'])} lines)")


def _cmd_unmatched(ledger: str, statement: str) -> None:
    rep = build_recon_report(ledger, statement)
    print("unmatched ledger entries:")
    for entry_id in rep["unmatched_ledger"]:
        print(f"  {entry_id}")
    print("unmatched statement lines:")
    for ref in rep["unmatched_statement"]:
        print(f"  {ref}")


def main(argv) -> int:
    if len(argv) < 4:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "summary":
        _cmd_summary(argv[2], argv[3])
    elif cmd == "unmatched":
        _cmd_unmatched(argv[2], argv[3])
    else:
        print(f"unknown command: {cmd}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
