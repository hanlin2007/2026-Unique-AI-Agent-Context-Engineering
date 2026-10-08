# Changelog

## 0.4.2 (2026-09-22)
- docs: add data dictionary for consumption order / reorder trigger /
  transfer semantics
- scripts: nightly snapshot now writes a valuation canary line

## 0.4.1 (2026-09-19)
- valuation: quantize per-SKU totals as well as the grand total
  (follow-up to #44; see issue #57 for the remaining drift)

## 0.4.0 (2026-09-18) - "lot model" release
- engine: rework from quantity-ledgers to LOT-granular stock; lots.py
  and transfers.py rewritten and individually reviewed
- report: build_inventory_report() is now the single entry point;
  tests moved to black-box contract (numbers only)
- After this release the lot pipeline is considered STABLE. The suite
  went red eleven days later - tracked as issue #57 (valuation
  rounding, see KNOWN_ISSUES.md).

## 0.3.1 (2026-06-30)
- valuation: switch accumulator from float to Decimal ROUND_HALF_EVEN
  (issue #44)

## 0.3.0 (2026-06-02)
- transfers: support annex -> main direction (was main -> annex only)

## 0.2.3 (2026-04-11)
- valuation: stop rounding per lot before summing (issue #31)

## 0.2.0 (2026-03-01)
- reorder: suggested order quantity (2x point top-up policy)

## 0.1.0 (2026-01-15)
- initial release
