"""Command line interface.

  python -m src.cli summary data/access.log
  python -m src.cli hours   data/access.log
  python -m src.cli tail    data/access.log
"""
from __future__ import annotations

import argparse

from .api import summarize_log


def _print_summary(rep: dict) -> None:
    print(f"events: {rep['events']} (rejected lines: {rep['rejected']})")
    for label, count in rep["hours"].items():
        print(f"  {label}  {'#' * count} {count}")
    rates = rep["status_rates"]
    print(f"2xx {rates['2xx']:.3f}  4xx {rates['4xx']:.3f}  5xx {rates['5xx']:.3f}")
    rt = rep["response_time"]
    print(f"response time: mean {rt['mean']:.3f}  p50 {rt['p50']:.3f}  p95 {rt['p95']:.3f}")
    print("top paths:", ", ".join(f"{p} ({c})" for p, c in rep["top_paths"]))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="logwatch")
    ap.add_argument("command", choices=["summary", "hours", "tail"])
    ap.add_argument("log_path")
    args = ap.parse_args(argv)

    rep = summarize_log(args.log_path)
    if args.command == "summary":
        _print_summary(rep)
    elif args.command == "hours":
        for label, count in rep["hours"].items():
            print(f"{label} {count}")
    else:
        rt = rep["response_time"]
        print(f"p95 {rt['p95']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
