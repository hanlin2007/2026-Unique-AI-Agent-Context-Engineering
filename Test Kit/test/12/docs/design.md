# bankrecon design notes

Last updated: 2026-09-19 (v0.4.0 era). Maintainer: n.achterberg.
Audience: anyone touching src/. Read the invariants BEFORE the code;
review will ask about them, and so will the auditors.

## Goals

bankrecon answers the month-end question: "does everything in our
ledger appear on the bank statement, exactly once, and vice versa?"
It is a control tool, not an accounting system: the output is a
list of exceptions a human investigates, not a set of adjustments
the tool posts. The design favours *explainability* - every matched
pair and every exception must be defensible in an audit.

## The pipeline

```
ledger_io.py   ledger CSV -> entries; kind filter (F excluded)
bank_io.py     statement CSV -> lines
window.py      value-date window rule (settlement lag)
match.py       greedy matching, single-use rule
report.py      orchestration; build_recon_report() is the entry
```

Both IO edges are thin; all semantics live in window.py, match.py
and the data dictionary.

## Invariants

1. Ledger kinds S/R/T participate in reconciliation; F (fee
   accruals) do not - they are internal bookkeeping and never appear
   on the statement as separate lines. The filter is applied once,
   in ledger_io.
2. A statement line dated 0..WINDOW_DAYS after its ledger entry is a
   candidate; the window end is INCLUSIVE (settlement lag of exactly
   WINDOW_DAYS days still counts). Lines dated before the ledger
   entry are never candidates.
3. Each statement line matches AT MOST ONCE. Two ledger entries with
   identical amounts cannot both consume one line; the second one is
   an exception for a human, not a match for the tool.
4. Amounts match within AMOUNT_TOLERANCE (0.01) - exact cent
   equality in practice.
5. Matching is greedy in ledger (date, id) order, earliest-dated
   candidate first. Deterministic input order in, deterministic
   report out.
6. The report counts duplicates (statement lines consumed more than
   once) and the number is ZERO in every healthy run.

## Alternatives considered (and rejected)

A global optimiser (best assignment across all candidate pairs, e.g.
Hungarian-style) was prototyped in the v0.2 era and rejected. With
~45 rows a month it buys nothing measurable over greedy-in-order,
and it has one fatal audit property: a global solver can change a
PREVIOUS month-fragment's pairing when a new line arrives, which
makes month-over-month report diffs impossible to explain. Greedy
in (date, id) order pairs each entry independently of later entries;
the auditors can re-derive any pair by hand.

Fuzzy description matching was also rejected: memos and statement
descriptions come from different vocabularies ("invoice 1041" vs
"acquirer settlement"), so text similarity is noise. Amount + value
date is the whole signal, by design.

## What would make us revisit this design

- Volume growing past a few hundred rows a month (greedy stays
  correct, but the exception workflow needs batching, not more
  matching cleverness).
- Multi-currency accounts (amounts stop being directly comparable;
  a conversion stage would enter the pipeline before match.py).
- Same-day multiple settlements per register (the single-use rule
  stays, but the exception playbook needs a new chapter).
None of these are scheduled.

## History (why the rules look like this)

v0.1 matched on amount alone and immediately double-counted the
register sales on a busy Saturday. v0.2 added the value-date window
after the May long weekend pushed half a week of settlements past
the naive same-day rule. v0.3 wrote the rules down - kinds, window,
single-use - after the first audit, when we learned that "everyone
knows how matching works" was not true and, worse, was not the same
thing for everyone. v0.4 changed only the bank-side parser, or so
the release notes claim.
