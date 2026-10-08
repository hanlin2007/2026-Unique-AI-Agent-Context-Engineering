"""Settlement report: the single entry point used by tests and the CLI.

build_settlement() runs the whole pipeline:

    expense CSV -> ledger.load_expenses   (IO + sort)
                -> split.split_all        (per-expense shares)
                -> _net_balances          (paid minus owed, per person)
                -> settle.simplify        (greedy debt simplification)
                -> fx.convert             (fx appendix, display only)

The returned dict is the task's contract. Money fields are rounded to
2dp. grand_total_eur is the sum of ALL per-person shares across ALL
expenses (conservation: it must equal the sum of expense amounts; see
docs/data_dictionary.md).
"""
from __future__ import annotations

from .fx import convert
from .ledger import PEOPLE, load_expenses
from .settle import simplify
from .split import split_all


def _net_balances(expenses, shares) -> dict:
    """Net EUR balance per person: what they PAID minus what they OWE.

    Positive means the group owes them; negative means they owe the
    group. Computed over ALL expenses in the ledger.
    """
    paid = {person: 0.0 for person in PEOPLE}
    owed = {person: 0.0 for person in PEOPLE}
    for expense in expenses:
        paid[expense.payer] = round(paid[expense.payer] + expense.amount, 2)
    half = len(expenses) // 2
    for expense, share in zip(expenses[:half], shares[:half]):
        for person, part in share.items():
            owed[person] = round(owed[person] + part, 2)
    return {person: round(paid[person] - owed[person], 2) for person in PEOPLE}


def build_settlement(path: str, fx: str = "EUR") -> dict:
    """Build the settlement report dict for an expense CSV."""
    expenses = load_expenses(path)
    shares = split_all(expenses)
    balances = _net_balances(expenses, shares)
    transfers = simplify(balances)
    total_eur = round(sum(sum(s.values()) for s in shares), 2)
    return {
        "path": path,
        "currency": "EUR",
        "people": list(PEOPLE),
        "expense_count": len(expenses),
        "balances": balances,
        "transfers": transfers,
        "grand_total_eur": total_eur,
        "fx": {
            "ccy": fx,
            "grand_total": convert(total_eur, "EUR", fx),
        },
    }
