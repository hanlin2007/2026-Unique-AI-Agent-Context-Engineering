# Proposed fix for issue #57 (valuation drift vs ledger)

Author: t.almeida, 2026-10-01
Status: PROPOSED, review pending (branch fix/issue-57-valuation-rounding)

## Root cause (analysis)

`_money()` in `src/valuation.py` currently quantizes with
ROUND_HALF_EVEN:

```python
def _money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_EVEN)
```

The ledger workbook the accountants reconcile against rounds HALF-UP
(their Excel does, always). For unit costs with 2dp and integer
quantities the per-lot products are exact, but the per-SKU and
grand-total quantize steps still hit .005 boundaries whenever an odd
number of half-cent residuals accumulate through the Decimal sum --
which is exactly the shape of the drift we see (sub-1%, always the
same direction, several SKUs at once).

Second, compounding issue: `value_by_sku()` quantizes each SKU total,
and `total_value()` quantizes AGAIN over the raw sum. If a caller ever
sums the per-SKU figures instead of calling `total_value()`, the two
paths disagree by a cent here and there. One rounding policy, applied
once, half-up, fixes both.

## Proposed patch

In `src/valuation.py`:

1. Switch the rounding mode in `_money()`:

```python
def _money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)
```

2. Keep `value_by_sku()` quantized per SKU (report contract), but make
   `total_value()` sum the QUANTIZED per-SKU figures so both paths
   agree:

```python
def total_value(lots: list) -> Decimal:
    return sum(value_by_sku(lots).values())
```

## Why this should turn the suite green

The failing valuation assertions compare 2dp floats exactly; once the
rounding mode matches the ledger the drift should collapse to zero,
and the per-SKU / grand-total paths can no longer disagree.

## Confidence

High - same class of bug as #31 and #44, and the crash trace in
logs/error_2026_09_28.log points into valuation.py's quantize path.
