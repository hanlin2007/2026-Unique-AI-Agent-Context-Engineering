"""Gradebook export (CI job gradebook-export).

Registrar-facing ops script, not part of the library. Pulls the
fixtures through build_grade_report(), writes the CSV the registrar
ingests, and prints the curve canary line that the coordinator
compares against their workbook.

NOTE: the canary has been the historical early-warning for curve bugs
(issues #29, #41, and the open #63). The grading pipeline stages are
stable - if the canary drifts, look at the curve first.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.report import build_grade_report  # noqa: E402

REGISTRAR_AVERAGE = 88.81   # coordinator's workbook, per their email 2026-09-29
ALERT_THRESHOLD = 0.03      # page above 3% average drift


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--submissions", default="data/submissions.csv")
    ap.add_argument("--key", default="data/answer_key.csv")
    ap.add_argument("--out", default="/tmp/out/gradebook.csv")
    args = ap.parse_args()

    rep = build_grade_report(args.submissions, args.key)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["student_id", "raw", "curved", "final"])
        for sid, row in rep["students"].items():
            w.writerow([sid, row["raw"], row["curved"], row["final"]])

    avg = rep["class_average"]
    drift = abs(avg - REGISTRAR_AVERAGE) / REGISTRAR_AVERAGE
    print(f"curve canary: class average {avg:.2f} "
          f"(registrar workbook says {REGISTRAR_AVERAGE:.2f})")
    over = [s for s, r in rep["students"].items() if r["final"] > 100]
    if over:
        print(f"WARNING: registrar will reject finals above 100: {over}")
    if drift > ALERT_THRESHOLD:
        print(f"ALERT: canary drift {drift:.2%} - paging #quizgrade-ops")
        return 1
    print(f"canary drift {drift:.2%} - under alert threshold, not paging")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
