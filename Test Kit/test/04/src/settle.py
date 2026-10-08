"""Debt simplification: turn net balances into a short transfer list.

Greedy pairing (docs/design.md): repeatedly pair the largest CREDITOR
(positive balance, is owed money) with the largest DEBTOR (negative
balance, owes money) and settle min(credit, debt) between them, until
no balance exceeds half a cent. Deterministic: ties break in roster
order (dict insertion order).

A transfer {"from": A, "to": B, "amount": x} means A PAYS B x EUR
(docs/data_dictionary.md). The debtor is the "from" side; the
creditor is the "to" side.
"""
from __future__ import annotations

EPSILON = 0.005


def simplify(balances: dict) -> list:
    """Greedy debt simplification over net balances (person -> EUR)."""
    work = {person: round(balance, 2) for person, balance in balances.items()}
    transfers = []
    while True:
        creditor = max(work, key=lambda p: work[p])
        debtor = min(work, key=lambda p: work[p])
        if work[creditor] < EPSILON or work[debtor] > -EPSILON:
            break
        amount = round(min(work[creditor], -work[debtor]), 2)
        transfers.append({"from": creditor, "to": debtor, "amount": amount})
        work[creditor] = round(work[creditor] - amount, 2)
        work[debtor] = round(work[debtor] + amount, 2)
    return transfers
