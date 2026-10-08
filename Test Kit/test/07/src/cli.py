"""Command line interface.

  python -m src.cli report   data/submissions.csv data/answer_key.csv
  python -m src.cli roster   data/submissions.csv data/answer_key.csv
  python -m src.cli student  data/submissions.csv data/answer_key.csv S07
"""
from __future__ import annotations

import argparse

from .report import build_grade_report


def _print_report(rep: dict) -> None:
    print(f"{'student':9} {'raw':>6} {'curved':>7} {'final':>6}  result")
    for sid, row in rep["students"].items():
        verdict = "pass" if row["final"] >= rep["pass_mark"] else "FAIL"
        print(f"{sid:9} {row['raw']:>6.1f} {row['curved']:>7.2f} "
              f"{row['final']:>6.2f}  {verdict}")
    print(f"\nclass average: {rep['class_average']:.2f}")
    print(f"top score:     {rep['top_score']:.2f}")
    print(f"pass count:    {rep['pass_count']} / {len(rep['students'])}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="quizgrade")
    ap.add_argument("command", choices=["report", "roster", "student"])
    ap.add_argument("submissions_csv")
    ap.add_argument("key_csv")
    ap.add_argument("student_id", nargs="?")
    args = ap.parse_args(argv)

    rep = build_grade_report(args.submissions_csv, args.key_csv)
    if args.command == "report":
        _print_report(rep)
    elif args.command == "roster":
        for sid, row in rep["students"].items():
            print(f"{sid}: {row['final']:.2f}")
    else:
        row = rep["students"][args.student_id]
        print(f"{args.student_id}: raw {row['raw']:.1f}, "
              f"curved {row['curved']:.2f}, final {row['final']:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
