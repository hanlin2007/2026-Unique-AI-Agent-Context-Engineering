# Changelog

## 0.9.2 (2026-09-28)
- docs: data dictionary promoted to contract status
- ci: nightly diff of rates.py against data/fx_snapshot.csv

## 0.9.0 (2026-09-26) - "settlement engine" release
- engine: split the old monolith.py into ledger / split / settle /
  report; each extracted module individually reviewed
- report: build_settlement() is now the single entry point; tests
  moved to black-box contract (numbers only)
- fx: NOT touched in this release (see issue #51 discussion)
- After this release the test suite went red - tracked as issue #51
  (fx totals drift, see KNOWN_ISSUES.md). The fx module is the prime
  suspect and is under active investigation.

## 0.8.2 (2026-08-30)
- settle: EPSILON guard against penny-cycle oscillation (issue #37)

## 0.8.0 (2026-08-02)
- rates: snapshot refreshed (2026-08-01); audit copy added at
  data/fx_snapshot.csv (issue #29)
- fx: external audit of convert() - no findings

## 0.7.1 (2026-06-18)
- ledger: reject payer-not-in-split rows at parse time

## 0.6.0 (2026-05-04)
- settle: greedy simplification replaces the old pairwise netting

## 0.4.0 (2026-02-11)
- fx: switch to EUR-pivot Decimal conversion (issue #19)

## 0.3.1 (2026-01-09)
- rates: hand-edited rate reverted; table is now snapshot-only,
  hand edits forbidden (incident report on file)

## 0.2.0 (2025-11-20)
- split: largest-remainder distribution replaces naive rounding
  (issue #12 - the FIRST time dropped cents bit us)

## 0.1.0 (2025-10-02)
- initial release
