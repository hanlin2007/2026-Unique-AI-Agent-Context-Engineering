"""Bank statement CSV IO.

Columns: date,ref,amount,description. Since the bank's June export
change, the statement is a plain UTF-8 CSV: amounts are plain signed
decimals with NO thousand separators and NO quoted fields, and the
header is exactly the four columns above.

NOTE: this module has priors. The OLD bank format (pre-June) quoted
amounts and used comma thousand separators ("1,245.00"), which broke
the naive float() parse (issue #19). The parser below was rewritten
for the new format at v0.4.0, but quoted-amount paranoia persists on
the team - see KNOWN_ISSUES.md #51. The current bank export has been
diffed twice against hand downloads and matches.
"""
from __future__ import annotations

import csv
from datetime import date
from typing import NamedTuple


class StatementLine(NamedTuple):
    day: date
    ref: str
    amount: float
    description: str


def _parse_day(s: str) -> date:
    y, m, d = (int(part) for part in s.strip().split("-"))
    return date(y, m, d)


def load_statement(path: str) -> list:
    """Load all statement lines, file order preserved."""
    lines = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            lines.append(StatementLine(
                day=_parse_day(row["date"]),
                ref=row["ref"].strip(),
                amount=round(float(row["amount"]), 2),
                description=row.get("description", "").strip(),
            ))
    return lines
