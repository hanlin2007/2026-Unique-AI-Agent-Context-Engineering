"""Command line interface for budgetsplit.

Usage:
    python -m src.cli report    data/expenses.csv [FX]
    python -m src.cli balances  data/expenses.csv
    python -m src.cli transfers data/expenses.csv
"""
from __future__ import annotations

import sys

from .fx import format_amount
from .report import build_settlement


def _cmd_report(path: str, fx_ccy: str = "EUR") -> None:
    rep = build_settlement(path, fx=fx_ccy)
    print(f"ledger: {rep['path']} ({rep['expense_count']} expenses, EUR)")
    print(f"grand total: {format_amount(rep['grand_total_eur'], 'EUR')}")
    appendix = rep["fx"]
    if appendix["ccy"] != "EUR":
        print(f"fx({appendix['ccy']}): "
              f"{format_amount(appendix['grand_total'], appendix['ccy'])}")
    print("balances:")
    for person, balance in rep["balances"].items():
        sign = "+" if balance >= 0 else "-"
        print(f"  {person:<8} {sign}{abs(balance):.2f}")
    print("transfers:")
    for t in rep["transfers"]:
        print(f"  {t['from']} -> {t['to']}: {t['amount']:.2f}")


def _cmd_balances(path: str) -> None:
    rep = build_settlement(path)
    for person, balance in rep["balances"].items():
        print(f"{person}: {balance:.2f}")


def _cmd_transfers(path: str) -> None:
    rep = build_settlement(path)
    if not rep["transfers"]:
        print("all settled")
    for t in rep["transfers"]:
        print(f"{t['from']} pays {t['to']} {t['amount']:.2f} EUR")


def main(argv) -> int:
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    command, path = argv[1], argv[2]
    if command == "report":
        _cmd_report(path, argv[3] if len(argv) > 3 else "EUR")
    elif command == "balances":
        _cmd_balances(path)
    elif command == "transfers":
        _cmd_transfers(path)
    else:
        print(f"unknown command: {command}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
