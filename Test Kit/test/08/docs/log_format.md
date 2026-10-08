# Log format and analytics spec

Defines the exact semantics that src/ implements. When code and this
document disagree, THIS DOCUMENT IS RIGHT and the code has a bug.

## Line format (nginx combined, plus response time)

```
$remote_addr - $remote_user [$time_local] "$request" $status
$body_bytes_sent "$http_referer" "$http_user_agent" $request_time
```

One request per line. request_time is in seconds, decimal. Timestamps
carry a numeric timezone offset; all analytics are done in UTC.

## Rejects

A line that does not match the format goes to the rejects list and is
EXCLUDED from the sample. The rejects count is part of every summary.

## Bucketing

Each request belongs to the hour bucket that CONTAINS its timestamp:
the bucket for 15:47:38 is the 15:00 bucket. Assignment is a FLOOR to
the hour boundary -- never a rounding to the nearest hour. A request
at 15:52 happened during the 15:00 hour for every analytics purpose
(capacity, error-rate windows, the nightly report).

## Percentiles

Percentiles use **linear interpolation between closest ranks** (the
"type 7" method, the same default as numpy and as our APM vendor):
with n sorted values, the p-th percentile is at rank
h = (n - 1) * p / 100; non-integer h interpolates between the two
neighbouring values. Nearest-rank methods are NOT acceptable: on
samples this size they visibly jump between data points, and the
nightly report compares our p95 against the APM's.

## Rates

Status-class rates are shares of the parsed sample, 4dp: 2xx, 4xx,
5xx. Other classes (1xx, 3xx) are counted but not reported by
summarize_log; the fixture window contains none.

## Worked example (for implementers)

Given 26 requests with response times whose sorted tail is
... 0.310, 0.420, 1.870, 2.310, 2.980:

- p50 sits at rank (26 - 1) * 0.50 = 12.5, halfway between the 13th
  and 14th sorted values (0-indexed 12 and 13) - interpolate.
- p95 sits at rank (26 - 1) * 0.95 = 23.75, three quarters of the
  way from the 24th value (1.870) to the 25th (2.310): 2.200.
- A request logged at 15:58:49 belongs to the 15:00 bucket. An
  implementation that reports it under 16:00 has implemented
  rounding, not flooring, and disagrees with this document.
