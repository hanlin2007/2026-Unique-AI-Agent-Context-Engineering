# Known issues

## #42 - Currency rounding drift (OPEN, high priority)

Reported 2026-09-28 by QA, reproduced consistently since v0.5.0.

Symptom: converted totals in the fx appendix land a fraction of a
percent away from expected values, and the interest figure drifts by a
small absolute amount as well. Both code paths share the rounding
helpers in src/currency.py (round_to_minor / convert), which is why
this is tracked as ONE issue.

History: this is the THIRD time rounding has bitten us. v0.2.1 patched
a float-accumulation bug, v0.3.0 switched round() to Decimal half-even.
The current suspicion (see fix_suggestion.md) is that `convert()` keeps
full precision through the pivot multiplication, so half-even kicks in
at the wrong quantum for 0-exponent currencies (JPY, KRW), and the same
helper is reused when displaying interest.

Suspected location: `src/currency.py`, `convert()` + `round_to_minor()`.

Impact: test suite red since 2026-09-30 (8 of 10 tests failing).

## #38 - CLI table alignment with wide chars (OPEN, low priority)

_render_table misaligns CJK memos. Cosmetic.

## #31 - month_summary slow on 10k+ rows (CLOSED)

Fixed in v0.4.0 by pre-filtering entries per month.

## #25 - currency rate table stale (CLOSED)

Rates refreshed 2026-09-01 (src/rates.py, SNAPSHOT_DATE).
