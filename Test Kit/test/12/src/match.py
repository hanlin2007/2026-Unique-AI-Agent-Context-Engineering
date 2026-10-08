"""Matching engine.

Greedy per ledger entry, in ledger (date, id) order: take the
earliest-dated UNUSED statement line inside the value-date window
whose amount matches within AMOUNT_TOLERANCE.

Single-use rule (docs/data_dictionary.md): each statement line
matches AT MOST ONCE. A line consumed by one ledger entry is
unavailable to later entries - two ledger entries with identical
amounts cannot both consume the same statement line.
"""
from __future__ import annotations

from .window import in_window

AMOUNT_TOLERANCE = 0.01


def reconcile(ledger_entries: list, statement_lines: list) -> tuple:
    """-> (matched, unmatched_ledger, unmatched_statement).

    matched: [(LedgerEntry, StatementLine)] in ledger order.
    """
    matched = []
    unmatched_ledger = []
    for entry in ledger_entries:
        hit = None
        for line in statement_lines:
            if not in_window(entry.day, line.day):
                continue
            if abs(line.amount - entry.amount) <= AMOUNT_TOLERANCE:
                hit = line
                break
        if hit is None:
            unmatched_ledger.append(entry)
        else:
            matched.append((entry, hit))
    matched_refs = {ln.ref for _, ln in matched}
    unmatched_statement = [ln for ln in statement_lines
                           if ln.ref not in matched_refs]
    return matched, unmatched_ledger, unmatched_statement
