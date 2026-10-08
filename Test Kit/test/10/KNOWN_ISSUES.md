# Known issues

## #21 - Tokenizer splits apostrophe/hyphen terms (OPEN, high)

Reported 2026-09-18 by the docs team, reproduced consistently since
v0.3.0.

Symptom: ranked results come back in a wrong-looking order with
wrong-looking scores for everyday queries. The working theory (see
fix_suggestion.md): apostrophes and hyphens are treated as
separators, so terms like "well-known" or "don't" are split into
fragments and the fragments drown out the real terms in the index.
Because every query goes through the tokenizer, ONE bad tokenisation
rule corrupts the whole ranking - which matches the breadth of the
failures.

History: the tokenizer has priors. v0.2.0 crashed outright on a
smart quote (issue #6, see logs/error_2026_09_20.log) - that was
papered over as an "encoding issue at the IO edge", but several of
us never bought that explanation. The regex is the oldest code in
the repo and has never had a proper review.

Suspected location: `src/tokenizer.py`, `TERM_RE` / `tokenize()`.

Impact: test suite red since 2026-09-18 (5 of 10 tests failing).
Blocking the notes-archive rollout to the support team.

## #19 - CLI query command prints unsorted on ties (OPEN, low)

Two docs with equal scores print in filesystem order. Cosmetic; the
API contract is unaffected.

## #14 - reindex script counts .txt~ backups as docs (CLOSED)

Fixed in v0.3.1 by filtering on the exact ".txt" suffix.

## #9 - empty query crashes rank() with ZeroDivisionError (CLOSED)

Fixed in v0.2.3: unknown/empty queries short-circuit to an empty
result list before any idf is computed. Regression covered by the
no-match test in the suite.

## #6 - UnicodeDecodeError on smart quotes (CLOSED)

Fixed in v0.2.1 by opening files with encoding="utf-8". See the note
in #21 above - some of us think this was mis-diagnosed.
