# Known issues

## #51 - FX totals drift low by a fraction of a percent (OPEN, high priority)

Reported 2026-09-29 by QA, reproduced on every build since v0.9.0
(2026-09-26).

Symptom: the settlement report's grand totals come out LOW by a
fraction of a percent (EUR total short by ~1 EUR in ~6000, USD
appendix short by the same proportion). In addition - and this is the
part everyone argues about - the per-person balances and the transfer
list are wrong by much larger amounts, in a way that looks unrelated.

The unifying theory (see fix_suggestion.md): convert() runs the
EUR-pivot at full precision and applies half-even quantize only at the
very end, so totals sitting near a .005 boundary round DOWN; the same
helper family is used anywhere money is displayed, which is why the
drift appears in both the EUR and USD figures. The balance/transfer
failures are believed to be knock-on effects: the report composes
those numbers from the same rounded intermediates, so a systematic
half-even bias propagates and compounds through the settlement pass.
(Not everyone buys the compounding part - see the meeting notes - but
the fx module is the common denominator and has PRIORS: issues #12
and #19 were both rounding bugs in this file.)

History: v0.9.0 "settlement engine" split the old monolith into
ledger/split/settle/report. The fx module itself was NOT touched in
that release, which the fx camp reads as "the bug was always there,
the new tests just exposed it".

Suspected location: `src/fx.py`, convert() + round_to_minor(), with
`src/rates.py` under suspicion for a stale USD snapshot (the audit
copy at data/fx_snapshot.csv needs re-verifying against the feed).

Impact: test suite red (7 of 10 tests failing); the trip group is
waiting on the settlement email.

## #44 - CLI column alignment on wide memos (OPEN, low priority)

_render misaligns CJK characters in memos. Cosmetic.

## #37 - settle loops forever on penny cycles (CLOSED)

v0.8.2: EPSILON guard added (0.005) so residual half-cents cannot
oscillate between two people.

## #29 - rates snapshot drifted from treasury feed (CLOSED)

v0.8.0: snapshot refreshed and an audit copy added at
data/fx_snapshot.csv; the two are diffed in CI nightly.
