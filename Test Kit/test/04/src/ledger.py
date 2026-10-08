"""Expense ledger: CSV -> Expense records (IO edge).

CSV columns: date,payer,amount,category,split_among,memo. Amounts are
EUR with cents. `split_among` is either "all" (every traveller) or a
pipe-separated subset ("anna|ben|carla"). Rows are returned date-sorted
with a stable sort; the rest of the pipeline relies on row order being
stable (see docs/data_dictionary.md).
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date

PEOPLE = ("anna", "ben", "carla", "dan", "erin", "finn")

CATEGORIES = (
    "hotel", "train", "dinner", "lunch", "cafe", "tickets",
    "food", "cab", "meds", "gifts", "fuel",
)


@dataclass(frozen=True)
class Expense:
    date: date
    payer: str
    amount: float       # EUR, positive
    category: str
    split_among: tuple  # who shares this expense (subset of PEOPLE)
    memo: str = ""


def parse_row(row: dict) -> Expense:
    """Build an Expense from a csv.DictReader row."""
    payer = row["payer"].strip().lower()
    if payer not in PEOPLE:
        raise ValueError(f"unknown payer: {payer!r}")
    raw_split = row["split_among"].strip().lower()
    if raw_split == "all":
        split_among = PEOPLE
    else:
        split_among = tuple(p.strip() for p in raw_split.split("|") if p.strip())
    if not split_among or any(p not in PEOPLE for p in split_among):
        raise ValueError(f"bad split_among: {row['split_among']!r}")
    if payer not in split_among:
        raise ValueError(f"payer {payer!r} must be in split_among")
    amount = round(float(row["amount"]), 2)
    if amount <= 0:
        raise ValueError("expense amount must be positive")
    return Expense(
        date=date.fromisoformat(row["date"].strip()),
        payer=payer,
        amount=amount,
        category=row["category"].strip().lower(),
        split_among=split_among,
        memo=row.get("memo", "").strip(),
    )


def load_expenses(path: str) -> list:
    """Load an expense CSV, date-sorted with a stable sort."""
    with open(path, newline="", encoding="utf-8") as fh:
        expenses = [parse_row(r) for r in csv.DictReader(fh)]
    expenses.sort(key=lambda e: e.date)
    return expenses
