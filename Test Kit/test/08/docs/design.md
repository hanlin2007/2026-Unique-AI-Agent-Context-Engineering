# logwatch design notes

Last updated: 2026-09-10 (v0.3.0 era).

## Goals

logwatch answers three questions about a service window: WHEN did
requests arrive (hourly buckets), HOW did they do (status-class
rates), and HOW FAST were we (response-time percentiles). The design
favours *one obvious pass* over cleverness: parse once, then compute
each summary as an independent function of the event list.

## The pipeline

```
parser.py   IO edge: log file -> events (+ rejects, never dropped silently)
buckets.py  events -> per-hour request counts
stats.py    events -> status rates, response-time percentiles
api.py      summarize_log(), the one mid-level entry point
```

Every stage except the IO edge is a pure function of the event list.

## Invariants

1. Every parsed request counts EXACTLY ONCE in exactly one hour
   bucket; the bucket assignment rule is in docs/log_format.md
   ("bucketing") and implemented only in buckets.py.
2. Percentile METHOD is fixed by docs/log_format.md ("percentiles")
   and implemented only in stats.py. Ops compares our p95 against the
   APM's, so the method must match the APM vendor's default.
3. Rejected lines are surfaced, never silently dropped; a nonzero
   rejects count is a data-quality signal, not an error.
4. Rates and percentiles are computed on the PARSED sample. If the
   sample is wrong, everything downstream is wrong with it -- which
   is why parsing incidents (#17, #35, and the open #71) always look
   like "the analytics are off".

## Why one mid-level API

summarize_log() exists so the nightly capacity report, the CLI, and
the test suite all exercise the SAME path. No second aggregation path
may be added without an ops review.

## Future directions (parked)

- per-path latency breakdown (needs the sample kept in memory)
- 5-minute buckets for incident review (bucket size parameter)
- reading directly from object storage (ops runbook first)

## Historical incidents (why the invariants exist)

- v0.1.4 (#17): referrers containing escaped quotes broke the naive
  split-on-quotes parser. Whole evenings vanished from the sample.
  Lesson: quoted fields are parsed, not split.
- v0.2.2 (#35): the internal sites shipped vhost-prefixed lines and
  every one of them was rejected. Lesson: format variants are a
  parser concern; rejects are surfaced, never silent.
- The open #71 is filed in the parser by analogy with these two.
  Whether the analogy holds is, at time of writing, an open
  question - see notes/meeting_2026_10_05.md for the dissent.

## Rejected designs

- Per-line callbacks into the analytics: rejected; the one-pass
  parse-then-compute shape is what makes each stage independently
  testable.
- Timezone-aware bucket labels: rejected by ops; everything is UTC,
  labels included, and the offset math lives in the parser alone.
- Dropping rejects silently below a threshold: rejected; a nonzero
  rejects count is a data-quality signal (invariant 3).
