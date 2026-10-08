# API reference

v0.3.2. Human-maintained; minor drift possible.

## src.parser
### LINE_RE: Pattern
Anchored combined-format matcher with escaped-quote-tolerant quoted
groups. NOTE: open issue #71 - see KNOWN_ISSUES.md.
### parse_line(line) -> Event | None
None on non-matching lines (they become rejects).
### parse_log(path) -> (list[Event], list[str])
Events in file order plus the raw rejected lines.
Event = (ts, method, path, status, response_time); ts is UTC epoch.

## src.buckets
### hour_bucket(ts) -> int
Epoch of the containing hour's start (rule: docs/log_format.md).
### bucket_label(bucket_start) -> str
"2026-09-30T15:00" style labels.
### hourly_counts(events) -> dict
label -> count, sorted, only hours with traffic.

## src.stats
### percentile(values, p) -> float
Interpolated percentile (method: docs/log_format.md).
### status_class_rates(events) -> dict
{"2xx": r, "4xx": r, "5xx": r}, 4dp shares of the sample.
### response_time_summary(events) -> dict
{"mean": m, "p50": p, "p95": p}, 3dp seconds.

## src.api
### summarize_log(path) -> dict
Keys: log, events, rejected, hours, status_rates, response_time,
top_paths (top 3 as [path, count] pairs).

## src.cli
summary / hours / tail subcommands over summarize_log().

## Usage example

```python
from src.api import summarize_log
rep = summarize_log("data/access.log")
rep["hours"]["2026-09-30T15:00"]   # requests in the 15:00 hour
rep["status_rates"]["5xx"]         # 4dp share of the sample
rep["response_time"]["p95"]        # seconds, 3dp, interpolated
rep["rejected"]                    # unparseable lines (NOT dropped silently)
```

The exact bucketing and percentile rules are in
docs/log_format.md; the summary merely materialises them.
