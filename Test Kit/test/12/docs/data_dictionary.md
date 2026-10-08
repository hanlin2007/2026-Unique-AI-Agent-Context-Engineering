# Recon data dictionary

This document is the source of truth for reconciliation semantics.
When a doc and the code disagree, THE DOC WINS - file an issue. It
is also the page auditors are given; keep it exact.

## Ledger kinds

| kind | meaning      | participates? | notes                              |
|------|--------------|---------------|------------------------------------|
| S    | sale         | yes           | money in from customers            |
| R    | refund       | yes           | negative amount                    |
| T    | transfer     | yes           | internal account movements         |
| F    | fee accrual  | NO            | internal; netted by the bank into  |
|      |              |               | the quarterly service charge       |

F rows NEVER appear on the bank statement as separate lines. If fee
accruals show up in an unmatched-ledger list, the kind filter is
broken - the bank did not "lose" them.

## Value-date window

A statement line dated D matches a ledger entry dated L iff
0 <= (D - L) <= WINDOW_DAYS, with WINDOW_DAYS = 2. The end is
INCLUSIVE: a line dated EXACTLY two days after its ledger entry is
a valid match (weekend settlement lag). A line dated three days
after is an exception for a human, and a line dated BEFORE the
ledger entry is never a match.

## Single-use rule

Each statement line matches AT MOST ONE ledger entry. If two ledger
entries carry identical amounts and only one settlement line exists,
the FIRST (in date, id order) matches and the SECOND is reported
unmatched. The report's "duplicates" field counts statement lines
consumed more than once and is zero in every healthy run.

## Amounts

Signed decimals, two places; refunds negative on BOTH files. A pair
matches when the amounts agree within 0.01 (exact cents in
practice). The ledger's September file is data/ledger.csv; the
statement is data/bank_statement.csv. The August ledger archive is
retained for year-over-year queries and is NOT part of the current
reconciliation.

## Worked example (the one finance ops quotes)

Ledger 2026-09-20, S, 88.20 ("invoice 1051"); statement line dated
2026-09-22 with the same amount. Delta is exactly 2 days, so the
window rule admits the pair: 0 <= 2 <= WINDOW_DAYS, and the end is
INCLUSIVE. This pair MUST match. If a report ever shows this entry
unmatched, the window check is wrong - not the bank, not the file,
not the calendar. The September fixture contains exactly this case
on purpose, because the May long-weekend confusion is precisely how
we lost a day last time.

## Worked example 2 (duplicate amounts)

Two register sales on the same day, 150.00 each; ONE settlement
line of 150.00 the next morning. The first sale (in date, id order)
matches the line. The second sale is reported unmatched and a human
chases the acquirer. What must NEVER happen is both sales pointing
at the same line: that is the duplicates field's entire reason to
exist, and policy treats any nonzero value as "the tool is broken",
not "the data is odd".
