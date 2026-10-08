# Known issues

## #71 - Requests lost on quoted referrers (OPEN, high priority)

Reported 2026-10-01 by ops, reproduced consistently since.

Symptom: hourly request counts come out LOW against the CDN's own
numbers -- some hours short by a third -- and the response-time
percentiles drift with them (a smaller sample moves p50/p95 around).
The working theory (see fix_suggestion.md) is that LINE_RE balks on
referrers containing characters like commas and query strings, those
lines get rejected, and everything downstream is computed on the
surviving subset.

History: this is the THIRD time parsing has bitten us. v0.1.4 fixed
unescaped referrers breaking the split (#17); v0.2.2 fixed
vhost-prefixed log lines (#35). The regex has been "one patch from
correct" for a year.

Suspected location: `src/parser.py`, LINE_RE (referrer and UA
groups), possibly the anchor at end-of-line.

Impact: test suite red since 2026-10-01 (5 of 10 tests failing).
Blocking the nightly capacity report. Ops is hand-verifying the
nightly numbers against the CDN dashboard in the meantime, which is
exactly the toil this tool was built to eliminate.

## #66 - CLI bar chart overflows at >40 requests/hour (OPEN, low)

`logwatch hours` histogram bars wrap the terminal. Cosmetic.

## #52 - summarize_log slow on 1M-line logs (CLOSED)

Fixed in v0.2.8 by streaming instead of readlines().

## #35 - vhost-prefixed log lines rejected (CLOSED)

Fixed in v0.2.2 by making the vhost prefix optional in LINE_RE.
(Sites were migrated off vhost logs in 2026-08; the prefix branch is
now dead but harmless.)

## #17 - escaped quotes in referrers break parsing (CLOSED)

Fixed in v0.1.4 by parsing quoted fields instead of splitting on
quotes.

## #09 - summarize_log crashes on empty log (CLOSED)

Fixed in v0.1.3; empty sample returns zeroed summary.
