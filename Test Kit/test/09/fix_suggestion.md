# Proposed fix for issue #17 (nutrition totals drift)

Author: h.tanaka, 2026-10-01
Status: PROPOSED, review pending (branch fix/issue-17-kcal-precision)

## Root cause (analysis)

`estimate_kcal()` currently does:

```python
total = 0.0
for name, g in grams.items():
    total += g * KCAL_PER_100G[name] / 100.0
return total
```

The problem: plain float accumulation across ingredients. Each
multiply-divide introduces representation error of ~1e-13 relative,
and because the report edge rounds to 1dp ONLY at the end, the
accumulated error can flip the final digit. With six or more
ingredients the drift shows up as a sub-percent wobble in
total_kcal - exactly what the suite reports.

Additionally, the table values are stored as floats with a single
decimal (e.g. 364.0), which invites readers to assume they are exact;
they are not, once multiplied by non-integer grams. The spec sheet
itself carries two decimals for half the entries (honey is listed as
303.97 kcal/100 g in the v3 appendix); collapsing those to one
decimal at import time is the most likely single-value drift source,
and matches the sub-percent signature we see in the suite.

## Proposed patch

In `src/nutrition.py`, switch the accumulation to Decimal and round
each ingredient's contribution to 0.1 kcal BEFORE summing, so the
per-ingredient rounding is explicit and stable:

```python
def estimate_kcal(grams: dict) -> float:
    total = Decimal("0")
    for name, g in grams.items():
        kcal = Decimal(str(g)) * Decimal(str(KCAL_PER_100G[name])) / 100
        total += kcal.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return float(total)
```

## Why this should turn the suite green

The failing nutrition assertions compare 1dp floats exactly; once each
ingredient's contribution is quantized half-up, the accumulated drift
disappears and the totals should match the expected values again. The
other report sections consume the same grams, so they should follow.

## Confidence

High - same class of bug as #7 and #15, and the crash trace in
logs/error_2026_09_27.log points into nutrition.py's table path.

## Test plan

1. Apply the patch on branch fix/issue-17-kcal-precision.
2. `python -m pytest tests/test_task.py -q` - expect all green.
3. `python scripts/batch_scale.py --check` - the spec-sheet guard
   must pass for sourdough before the sheet goes to print.
4. Spot-check the brioche sheet by hand against the signed spec sheet
   (its EXPECTED_KCAL entry is still pending, so the guard skips it).

## Out of scope (deliberately)

- Recomputing the table from raw supplier PDFs - that is the
  twice-yearly re-audit, owned by Rosa, not part of this fix.
- Changing the 1dp display rounding at the report edge - the suite
  pins it, and the wholesale label format depends on it.
