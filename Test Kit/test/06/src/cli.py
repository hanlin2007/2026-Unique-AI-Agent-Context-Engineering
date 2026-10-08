"""Command line interface.

  python -m src.cli report    data/lots.csv data/movements.csv
  python -m src.cli reorder   data/lots.csv data/movements.csv
  python -m src.cli valuation data/lots.csv data/movements.csv
"""
from __future__ import annotations

import argparse

from .report import build_inventory_report


def _print_report(rep: dict) -> None:
    print(f"{'sku':7} {'main':>6} {'annex':>6} {'total':>6} {'point':>6} {'value':>10}")
    for sku, row in rep["skus"].items():
        print(f"{sku:7} {row['closing']['main']:>6} {row['closing']['annex']:>6} "
              f"{row['total']:>6} {row['reorder_point']:>6} {row['valuation']:>10.2f}")
    print(f"\ngrand units: {rep['grand_units']}")
    print(f"valuation total: {rep['valuation_total']:.2f}")
    print(f"reorder list: {', '.join(rep['reorder_list']) or '(none)'}")
    t = rep["transfers"]
    print(f"transfers: {t['count']} movements, {t['moved_units']} units {t['by_sku']}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="stocktake")
    ap.add_argument("command", choices=["report", "reorder", "valuation"])
    ap.add_argument("lots_csv")
    ap.add_argument("movements_csv")
    args = ap.parse_args(argv)

    rep = build_inventory_report(args.lots_csv, args.movements_csv)
    if args.command == "report":
        _print_report(rep)
    elif args.command == "reorder":
        for sku in rep["reorder_list"]:
            row = rep["skus"][sku]
            print(f"{sku}: {row['total']} on hand, point {row['reorder_point']}")
    else:
        print(f"{rep['valuation_total']:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
