# Reconciliation policy (finance ops)

Owner: Farah (finance ops). Reviewed quarterly; next review 2026-12.

## What the tool decides, and what it must never decide

bankrecon is a CONTROL. It pairs ledger entries with statement
lines under the rules in docs/data_dictionary.md and reports
exceptions. It must NEVER post adjustments, never net two
exceptions against each other, and never "repair" a mismatch by
editing either file. Every exception is investigated by a human
before month-end sign-off.

## Standing exceptions playbook

- Duplicate-amount days (two register sales with one settlement
  line): the register Z-reports decide which sale settled; the other
  is chased with the acquirer. The tool reports the second entry as
  unmatched - that is the DESIRED behaviour, not a bug.
- Settlement lag beyond the window (three days or more): confirm
  with the bank's value-date report, then extend the ledger memo -
  do NOT widen WINDOW_DAYS ad hoc; the window is policy, and
  changing it is a quarterly-review item.
- Bank-only lines (interest credits, charges): matched against the
  finance ops journal, not the sales ledger. They appear in the
  tool's unmatched-statement list by design.
- Fee accruals (kind F): internal bookkeeping. They must not appear
  anywhere in the recon output; if they do, the ledger export or
  the kind filter is broken.

## Audit trail

Every month-end run is archived (script: scripts/month_end.py) with
the input files hashed. Auditors get the report, the inputs, and
docs/data_dictionary.md - nothing else, and the three must always
agree.

## Sign-off checklist (what finance ops actually does)

1. Run the tool. Confirm duplicates == 0 BEFORE anything else - a
   nonzero duplicate count means the tool itself is broken and every
   other number on the page is suspect.
2. Walk the unmatched-ledger list top to bottom; for each entry,
   classify it per the playbook above (duplicate-amount day,
   settlement lag, timing) and note the classification in the
   sign-off sheet.
3. Walk the unmatched-statement list; bank-only lines get a journal
   reference, anything else gets a call to the bank the same day.
4. Compare the matched total against the ledger's own month total
   (exported separately). They will not be equal - unmatched entries
   account for the difference - and the reconciliation of the two
   must be shown on the sign-off sheet to the cent.
5. Only then sign. The tool's job is to make steps 2-3 short; when
   the lists are wrong, as they are right now under issue #51,
   sign-off waits.

## Escalation

A red suite for more than five working days goes to the engineering
manager with this document attached - the point being that a
reconciliation tool that cannot reconcile is not a tooling
inconvenience, it is a missing control, and the business should
treat it that way. The current episode (issue #51, red since
2026-09-26) crossed that line on 2026-10-05 and was escalated
accordingly.
