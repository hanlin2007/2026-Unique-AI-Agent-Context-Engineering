# Changelog

## 0.5.1 (2026-09-22)
- currency: rate table moved to src/rates.py (SNAPSHOT_DATE tracked)
- docs: add data dictionary for journal kinds

## 0.5.0 (2026-09-20) - "pipeline split" release
- engine: split the old ledger.py into journal / normalize / daily /
  aggregate; each extracted module individually reviewed
- interest: NEW daily accrual feature (src/interest.py)
- report: build_report() is now the single entry point; tests moved to
  black-box contract (numbers only)
- After this release the pipeline modules are considered STABLE.
  Post-release, the test suite went red - tracked as issue #42
  (currency rounding, see KNOWN_ISSUES.md).

## 0.4.2 (2026-09-05)
- currency: refresh rate table (2026-09-01 snapshot)

## 0.4.0 (2026-08-14) - "ledger review" release
- ledger: full review of the balance engine; removed a module-level
  balance cache that served stale results to the report script
- models: Transaction is now frozen/immutable

## 0.3.0 (2026-06-02)
- currency: switch rounding from built-in round() to Decimal
  ROUND_HALF_EVEN (issue #19)
- currency: add EXPONENTS table for 0-decimal currencies (JPY, KRW)

## 0.2.1 (2026-04-11)
- currency: fix float-accumulation drift in convert_many (issue #12)

## 0.1.0 (2026-01-15)
- initial release
