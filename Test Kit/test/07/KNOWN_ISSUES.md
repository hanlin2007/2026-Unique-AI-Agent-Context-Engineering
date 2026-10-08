# Known issues

## #63 - Final scores shifted vs registrar workbook (OPEN, high priority)

Reported 2026-09-30 by the course coordinator, reproduced
consistently since.

Symptom: final grades land away from the registrar's workbook figures
-- most students shifted DOWN by a few points, while two students
show finals ABOVE 100 (S01, S07), which the registrar's system
rejects outright. A curve that can push a final past 100 is obviously
misbehaving, and everything downstream of it inherits the shift.

History: this is the THIRD time the curve has bitten us. v0.3.2 had a
stale CURVE_FACTOR left over from the spring term (#29); v0.4.4
applied the factor twice in the CLI path (#41). The current suspicion
(see fix_suggestion.md) is that apply_curve() is scaling the score
and then the report scales AGAIN somewhere, or the factor is being
applied to the wrong base (curved instead of raw).

Suspected location: `src/curve.py`, `apply_curve()` and its call
pattern from report.py.

Impact: test suite red since 2026-09-30 (8 of 10 tests failing).
Blocking grade submission (deadline 2026-10-10).

## #58 - CLI table misaligns 3-digit curved scores (OPEN, low priority)

`quizgrade report` columns drift when curved > 100. Cosmetic; will be
moot once #63 lands.

## #47 - loader rejects BOM-prefixed CSVs (CLOSED)

Fixed in v0.5.3 with utf-8-sig on open().

## #41 - curve applied twice in CLI path (CLOSED)

Fixed in v0.4.4; the report path now applies the factor exactly once.

## #33 - gradebook export writes CRLF line endings (CLOSED)

Registrar's old parser choked; fixed in v0.2.6 by forcing \n.

## #29 - stale CURVE_FACTOR carried into fall term (CLOSED)

Fixed in v0.3.2; factor is now reviewed each term with a changelog
entry and a canary watch the first night.

## #22 - practice-quiz rows leaking into real submissions (CLOSED)

Fixed in v0.1.8 by filtering the LMS dump on assessment id.
