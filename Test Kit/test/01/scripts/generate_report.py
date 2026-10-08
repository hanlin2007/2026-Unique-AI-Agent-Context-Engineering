"""Quarterly PDF report generator (CI job nightly-report).

Internal ops script, not part of the library. Pulls the journal through
build_report(), renders monthly sections and an fx appendix, and writes
a PDF via a stub renderer (real pipeline uses reportlab; stubbed here
to keep the repo dependency-free).

NOTE: the fx appendix has been the historical source of rounding bugs
(issues #12, #19, and the open #42). The pipeline stages are stable.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.currency import format_amount  # noqa: E402
from src.report import build_report  # noqa: E402


def render_months_section(months: dict) -> str:
    lines = ["month    opening      closing      in         out     days"]
    for key, s in months.items():
        lines.append(
            f"{key}  {s['opening']:>10.2f}  {s['closing']:>10.2f}  "
            f"{s['total_in']:>8.2f}  {s['total_out']:>8.2f}  {s['active_days']:>4}"
        )
    return "\n".join(lines)


def render_fx_section(rep: dict) -> str:
    fx = rep["fx"]
    return "\n".join([
        f"FX APPENDIX ({fx['ccy']})",
        f"total_in : {format_amount(fx['total_in'], fx['ccy'])}",
        f"total_out: {format_amount(fx['total_out'], fx['ccy'])}",
    ])


def render_pdf_stub(sections: list, out_path: Path) -> None:
    """Stand-in for the real reportlab pipeline: writes plain text."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n\n".join(sections), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--journal", default="data/journal_main.csv")
    parser.add_argument("--quarter", required=True, help="e.g. 2026Q1")
    parser.add_argument("--fx", default="JPY", help="display currency")
    parser.add_argument("--out", default="/tmp/out/report.txt")
    args = parser.parse_args()

    rep = build_report(args.journal, fx=args.fx)
    year = args.quarter[:4]
    qnum = int(args.quarter[-1])
    wanted = {f"{year}-{m:02d}"
              for m in range((qnum - 1) * 3 + 1, (qnum - 1) * 3 + 4)}
    months = {k: v for k, v in rep["months"].items() if k in wanted}

    sections = [
        f"QUARTERLY REPORT {args.quarter}",
        render_months_section(months),
        f"interest accrued (full journal): {rep['interest']['accrued']:.2f}",
        render_fx_section(rep),
    ]
    render_pdf_stub(sections, Path(args.out))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
