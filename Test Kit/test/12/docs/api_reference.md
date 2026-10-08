# API reference

v0.4.1. Human-maintained; minor drift possible.

## src.ledger_io
### load_ledger(path) -> list[LedgerEntry]
All rows, any kind, file order. LedgerEntry(day, entry_id, kind,
amount, memo); amounts parsed to float, refunds negative.
### matchable(entries) -> list
Kind filter for reconciliation participation (see data dictionary).
### MATCHABLE_KINDS: tuple
The kinds that participate. Owned by the data dictionary.

## src.bank_io
### load_statement(path) -> list[StatementLine]
All lines, file order. StatementLine(day, ref, amount, description).
NOTE: issue #51 suspects this function (dialect drift, quoted
amounts). Parsing priors: #19. The current bank export was diffed
against hand downloads in June and September and matches the
assumed format - but check the file first if numbers look wrong.

## src.window
### WINDOW_DAYS = 2
### in_window(ledger_day, statement_day) -> bool
Value-date window membership; end INCLUSIVE per data dictionary.

## src.match
### AMOUNT_TOLERANCE = 0.01
### reconcile(ledger_entries, statement_lines) -> tuple
-> (matched, unmatched_ledger, unmatched_statement). Greedy,
single-use per statement line (data dictionary rules 3-5).

## src.report
### build_recon_report(ledger_path, statement_path) -> dict
Keys: ledger_rows, considered, matched, unmatched_ledger (ids,
sorted), unmatched_statement (refs, sorted), duplicates,
total_matched, total_unmatched_ledger, total_unmatched_statement.
Totals 2dp. duplicates is zero in every healthy run.

## src.cli
Commands: `summary LEDGER STATEMENT`, `unmatched LEDGER STATEMENT`.
Pure renderer; no reconciliation logic of its own. Issue #44
(column width) is cosmetic and lives here.

## Stability contract

The test suite pins the report's numbers and id lists against the
September fixtures. Any change that moves a value needs a
data-dictionary update in the same commit - the dictionary defines
the semantics (kinds, window, single-use, tolerance), the suite
enforces them, and the auditors quote the dictionary. Since v0.4.0
the suite is RED (issue #51) - restoring green outranks every other
change, because finance ops cannot sign off month-end without it.

## Error behaviour

- Both loaders raise FileNotFoundError on missing files and
  ValueError on unparseable amounts/dates (deliberate: a malformed
  input must never silently reconcile as an empty month).
- reconcile never raises on unmatched entries; exceptions are the
  OUTPUT of this tool, not an error condition.
