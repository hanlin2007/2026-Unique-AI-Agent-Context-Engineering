# Known issues

## #57 - Valuation drift vs ledger (OPEN, high priority)

Reported 2026-09-26 by inventory control, reproduced consistently
since.

Symptom: the valuation total in the report lands just under 1% away
from the ledger figure (5909.80 expected by the accountants' workbook,
report shows a slightly different number), and several per-SKU
valuations drift with it. The drift is small and consistent, which is
why this is tracked as a ROUNDING issue, not a logic issue.

History: this is the THIRD time valuation rounding has bitten us.
v0.2.3 patched per-lot premature rounding (#31); v0.3.1 switched the
accumulator from float to Decimal half-even (#44). The current
suspicion (see fix_suggestion.md) is that `_money()` quantizes with
ROUND_HALF_EVEN while the ledger workbook rounds half-up, so values
sitting exactly on a .005 boundary fall the wrong way, and the
half-even quantize is applied per SKU as well as on the grand total.

Suspected location: `src/valuation.py`, `_money()` + `value_by_sku()`.

Impact: test suite red since 2026-09-29 (7 of 10 tests failing).
Blocking the Q4 close.

## #51 - CLI column widths with long SKU names (OPEN, low priority)

`stocktake report` table wraps when a SKU name exceeds 24 chars.
Cosmetic.

## #44 - valuation: float accumulation drift (CLOSED)

Fixed in v0.3.1 by moving the accumulator to Decimal.

## #38 - reorder report ignores lead times (CLOSED)

Won't-fix: purchasing confirmed the 2x-point top-up rule is the
approved policy; lead_time_days is informational only.
