# Changelog

## 1.1.2 (2026-09-24)
- docs: metrics_definitions.md promoted to contract status
- scripts: weekly_email.py parked until issue #33 is resolved

## 1.1.0 (2026-09-19) - "calendar hardening" release
- loader: date handling centralised on date.fromisoformat
- loader: Workout gains the iso_week property (ISO-8601 labels)
- loader: unknown workout types now raise ValueError at parse time
- After this release the test suite went red - tracked as issue #33
  (sessions land in wrong ISO weeks, see KNOWN_ISSUES.md). The loader
  is the prime suspect and is under active investigation.

## 1.0.0 (2026-08-22)
- summarize() promoted to the public mid-level API; tests moved to
  numbers-only contract
- metrics/trends reviewed and FROZEN (four releases without change)

## 0.9.0 (2026-07-30)
- loader: dates are timezone-NAIVE by design (decision record: the log
  is a personal diary keyed by local calendar day; modelling timezones
  adds failure modes without adding correctness)

## 0.8.4 (2026-07-02)
- loader: fromisoformat replaces the hand-rolled split() parser
  (issue #27; crash log kept at logs/error_2026_09_12.log)

## 0.7.1 (2026-05-19)
- trends: rolling_mean([]) returns [] (issue #22)

## 0.7.0 (2026-05-02)
- trends: add EMA with configurable window
- summarize: fitness trend added to the summary dict

## 0.6.0 (2026-03-15)
- initial release: weekly volume + pace summary
