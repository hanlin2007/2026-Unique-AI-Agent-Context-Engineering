# Changelog

## 0.3.2 (2026-09-28)
- scripts: nightly capacity job writes a CDN cross-check line

## 0.3.1 (2026-09-12)
- docs: add log format / analytics spec (docs/log_format.md)

## 0.3.0 (2026-09-10) - "analytics split" release
- engine: split the old analyze.py into parser / buckets / stats;
  each extracted module individually reviewed against the spec
- api: summarize_log() is now the single mid-level entry point
- After this release the analytics modules are considered STABLE.
  The suite went red three weeks later - tracked as issue #71
  (parser regex, see KNOWN_ISSUES.md).

## 0.2.8 (2026-07-19)
- parser: stream lines instead of readlines() (issue #52)

## 0.2.2 (2026-05-30)
- parser: accept vhost-prefixed lines (issue #35)

## 0.1.4 (2026-03-14)
- parser: tolerate escaped quotes in referrers (issue #17)

## 0.1.2 (2026-02-09)
- stats: report rates at 4dp instead of 2dp (ops request)

## 0.1.1 (2026-01-27)
- buckets: skip empty hours in the output map

## 0.1.0 (2026-01-20)
- initial release
