# Known issues

## #51 - Statement CSV dialect misparsed (OPEN, high priority)

Reported 2026-09-26 by finance ops, reproduced consistently since
v0.4.0.

Symptom: reconciliation numbers come out wrong in a way that looks
SMALL - the matched total drifts by well under one percent - while
the unmatched lists are visibly wrong. A handful of statement lines
silently shifting or dropping would produce exactly this signature,
and the statement parser is the only component that touches every
line.

History: this module has priors. The bank's pre-June export quoted
amounts and used comma thousand separators ("1,245.00"), which broke
the naive float() parse (issue #19). The v0.4.0 rewrite targeted the
new format, but the bank has changed its export TWICE this year and
several of us believe the September file has drifted back toward
quoted fields. The working theory (see fix_suggestion.md) is that
the parser needs dialect detection instead of assuming the format.

Suspected location: `src/bank_io.py`, `load_statement()`.

Impact: test suite red since 2026-09-26 (7 of 10 tests failing).
Finance ops are reconciling by hand in the meantime, which is how
the duplicate-sale question (two register sales, one settlement
line) got noticed in the first place. Escalated to engineering
management on 2026-10-05 per the policy's five-day rule.

## #44 - CLI summary column width on large totals (OPEN, low)

Prints ragged columns once totals pass five digits. Cosmetic.

## #31 - August archive kept in repo root (CLOSED)

Moved to data/ledger_archive_2026_08.csv in v0.4.1.

## #26 - month_end archived reports without input hashes (CLOSED)

Fixed in v0.3.2: the archive JSON now carries SHA-256 of both input
files, per the audit-trail section of docs/reconciliation_policy.md.

## #19 - old bank format quoted amounts crash parse (CLOSED)

Fixed in v0.4.0 by the bank_io rewrite. See the note in #51 - the
team's quoted-amount paranoia originates here.
