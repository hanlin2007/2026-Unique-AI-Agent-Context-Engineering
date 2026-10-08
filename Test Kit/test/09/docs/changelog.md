# Changelog

## 0.4.2 (2026-09-19)
- docs: add data dictionary for units, percentages, allergens
- scripts: batch_scale gains --out-dir flag

## 0.4.0 (2026-09-18) - "unit table" release
- units: extend conversion table (oz, lb) for the wholesale accounts
- units: table REVIEWED line by line during this release
- report: build_scaling_report() is now the single entry point; tests
  moved to a black-box contract (numbers only)
- Post-release, the test suite went red - tracked as issue #17
  (nutrition table drift, see KNOWN_ISSUES.md). The unit table itself
  was signed off by two reviewers and is considered stable.

## 0.3.0 (2026-06-30)
- nutrition: full re-audit of KCAL_PER_100G against spec sheet v3
  (issue #15)

## 0.3.1 (2026-07-08)
- scripts: batch_scale sheet columns right-aligned to 9 chars
  (issue #9)
- scripts: add --check flag comparing kcal totals against the signed
  spec sheet; sheet is NOT written on mismatch

## 0.2.2 (2026-05-11)
- scale: baker's percentages added to the report (flour-weight basis,
  per the bakery's standing convention)

## 0.2.1 (2026-04-20)
- parser: reject header lines after the `--` separator instead of
  silently skipping them (wholesale recipe files kept growing stray
  comment blocks in the table section)

## 0.2.0 (2026-04-02)
- allergens: per-recipe summary added (dedup per recipe, matches the
  packaging label format)

## 0.1.1 (2026-02-14)
- nutrition: fix per-100g column misread in the calorie table
  (issue #7)

## 0.1.0 (2026-01-20)
- initial release
