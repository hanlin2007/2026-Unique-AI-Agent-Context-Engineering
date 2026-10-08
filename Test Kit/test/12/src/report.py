"""Report assembly: the single entry point used by tests and the CLI.

build_recon_report() runs the whole pipeline:

    ledger CSV    -> ledger_io.load_ledger + matchable  (kind filter)
    statement CSV -> bank_io.load_statement
                  -> match.reconcile                    (window + single-use)

The returned dict is the task's contract. Totals are rounded to 2dp;
id/ref lists are sorted for stable output. "duplicates" counts
statement lines that were consumed by MORE THAN ONE ledger entry -
always zero when the single-use rule is honoured.
"""
from __future__ import annotations

from .bank_io import load_statement
from .ledger_io import load_ledger, matchable
from .match import reconcile


def build_recon_report(ledger_path: str, statement_path: str) -> dict:
    """Build the full reconciliation report dict (see module docstring)."""
    all_entries = load_ledger(ledger_path)
    considered = matchable(all_entries)
    lines = load_statement(statement_path)

    matched, unmatched_ledger, unmatched_statement = \
        reconcile(considered, lines)

    matched_refs = [ln.ref for _, ln in matched]
    return {
        "ledger_rows": len(all_entries),
        "considered": len(considered),
        "matched": len(matched),
        "unmatched_ledger": sorted(e.entry_id for e in unmatched_ledger),
        "unmatched_statement": sorted(ln.ref for ln in unmatched_statement),
        "duplicates": len(matched_refs) - len(set(matched_refs)),
        "total_matched": round(sum(e.amount for e, _ in matched), 2),
        "total_unmatched_ledger": round(
            sum(e.amount for e in unmatched_ledger), 2),
        "total_unmatched_statement": round(
            sum(ln.amount for ln in unmatched_statement), 2),
    }
