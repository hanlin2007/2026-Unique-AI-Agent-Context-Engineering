"""Command line interface for ledgetool.

Usage:
    python -m src.cli report  data/journal_main.csv [FX]
    python -m src.cli months  data/journal_main.csv
    python -m src.cli daily   data/journal_main.csv
    python -m src.cli convert 100 USD JPY
"""
from __future__ import annotations

import sys

from .currency import convert, format_amount
from .daily import compute_daily_rollups
from .journal import load_journal
from .normalize import normalize
from .report import build_report


def _render_table(headers, rows) -> str:
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep = "  ".join("-" * w for w in widths)
    body = ["  ".join(str(c).ljust(widths[i]) for i, c in enumerate(row))
            for row in rows]
    return "\n".join([line, sep, *body])


def _cmd_report(path: str, fx: str = "USD") -> None:
    rep = build_report(path, fx=fx)
    print(f"journal: {rep['journal']}  ({rep['native_currency']})")
    print(f"months:  {len(rep['months'])}")
    g = rep["grand"]
    print(f"grand:   in={g['total_in']:.2f} out={g['total_out']:.2f} "
          f"closing={g['closing']:.2f}")
    i = rep["interest"]
    print(f"interest: rate={i['annual_rate']} accrued={i['accrued']:.2f}")
    f = rep["fx"]
    print(f"fx({f['ccy']}): in={f['total_in']} out={f['total_out']}")


def _cmd_months(path: str) -> None:
    rep = build_report(path)
    rows = [(k, f"{v['opening']:.2f}", f"{v['closing']:.2f}",
             f"{v['total_in']:.2f}", f"{v['total_out']:.2f}",
             v["active_days"]) for k, v in rep["months"].items()]
    print(_render_table(
        ["month", "opening", "closing", "in", "out", "days"], rows))


def _cmd_daily(path: str) -> None:
    entries = normalize(load_journal(path))
    daily = compute_daily_rollups(entries)
    rows = [(d.isoformat(), f"{b:.2f}") for d, b in daily]
    print(_render_table(["date", "closing"], rows))


def main(argv) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "report":
        _cmd_report(argv[2], argv[3].upper() if len(argv) > 3 else "USD")
    elif cmd == "months":
        _cmd_months(argv[2])
    elif cmd == "daily":
        _cmd_daily(argv[2])
    elif cmd == "convert":
        print(format_amount(convert(float(argv[2]), argv[3].upper(),
                                    argv[4].upper()), argv[4].upper()))
    else:
        print(f"unknown command: {cmd}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
