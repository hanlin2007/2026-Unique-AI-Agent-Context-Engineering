# Proposed fix for issue #63 (curve shifting finals)

Author: w.nakamura, 2026-10-02
Status: PROPOSED, review pending (branch fix/issue-63-curve-double-apply)

## Root cause (analysis)

`apply_curve()` currently does float math:

```python
def apply_curve(raw_score: float, factor: float = CURVE_FACTOR) -> float:
    return round(raw_score * factor, 2)
```

Two problems here.

1. `round()` is banker's rounding, and the registrar's workbook rounds
   half-up. With a 1.15 factor, products like 87 * 1.15 = 100.05 sit
   exactly on a 2dp boundary; float representation error plus
   half-even makes these wobble by a cent, which is part of the shift
   the coordinator reported.

2. The over-100 finals prove the factor is landing on an uncapped
   base. The clean fix is to make apply_curve() itself enforce the
   ceiling -- the curve should never emit a grade the registrar
   rejects. (If the report also caps, the double cap is harmless.)

## Proposed patch

In `src/curve.py`, rewrite apply_curve():

```python
def apply_curve(raw_score: float, factor: float = CURVE_FACTOR) -> float:
    scaled = Decimal(str(raw_score)) * Decimal(str(factor))
    curved = scaled.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(min(curved, Decimal("100")))
```

No other call sites need to change; report.py keeps calling
apply_curve(raw) exactly as today.

## Why this should turn the suite green

The failing finals all go through apply_curve(); once the rounding
mode matches the registrar and the ceiling is enforced at the source,
the over-100 tests and the shifted finals should both snap back.

## Confidence

High - same class of bug as #29 and #41, and the crash trace in
logs/error_2026_09_27.log points into curve.py's scaling path.

## Rollback plan

If the patch makes anything worse, revert the branch and re-apply
only the quantize change (step 1 of the patch). The ceiling half is
independent and can land separately. Either way the suite should be
re-run with -q and the full failure list pasted into issue #63.
