# Proposed fix for issue #51 (fx totals drift low)

Author: s.nakamura, 2026-10-01
Status: PROPOSED, review pending (branch fix/issue-51-fx-quantize)

## Root cause (analysis)

`src/fx.py::convert` currently does:

```python
eur = Decimal(str(amount)) / RATES_PER_EUR[src]
out = eur * RATES_PER_EUR[dst]
return float(round_to_minor(out, dst))
```

Two defects compound here:

1. The pivot division keeps FULL precision into the multiplication,
   so the final quantize sees values like 6475.889999... that sit a
   hair under the .005 boundary and round DOWN under ROUND_HALF_EVEN.
2. `round_to_minor` uses half-even for everything. For settlement
   DISPLAY totals the convention (docs/design.md section "money
   conventions", and every consumer we ship to) is half-UP: a total
   that lands exactly on a half cent is owed upward, not to the even
   neighbour.

The observed signature - every drifting figure LOW, all by a fraction
of a percent - is exactly what these two defects produce together.

## Proposed patch

In `src/fx.py`:

1. Quantize the pivot to 6 places before multiplying:
   `eur = eur.quantize(Decimal("0.000001"))`
2. Round display totals half-up:

```python
def round_to_minor(amount: Decimal, currency: str) -> Decimal:
    _check(currency)
    quantum = Decimal(1).scaleb(-EXPONENTS[currency])
    return amount.quantize(quantum, rounding=ROUND_HALF_UP)
```

3. While we are in here: the USD snapshot in `src/rates.py` reads
   1.0862 but the treasury feed for 2026-09-01 prints 1.08625 - bump
   RATES_PER_EUR["USD"] to Decimal("1.0863") so the table reflects the
   feed's own half-up convention.

## Why this should turn the suite green

Once the pivot stops carrying dust into the final quantize and the
final quantize rounds the way the money conventions require, the
EUR/USD grand totals land on the expected constants. The balance and
transfer assertions follow the same rounded intermediates and should
come along.

## Confidence

High - same defect class as #12 and #19, same module, and the drift
magnitude (<0.02%) rules out any structural problem in the settlement
engine itself.

## Note from d.reyes (2026-10-02)

Applying this patch verbatim will NameError - the snippet uses
ROUND_HALF_UP but the file only imports ROUND_HALF_EVEN; add the
import when you apply it. Separately, and for the record: a fraction
of a percent explains the TOTALS, but the balances are off by HUNDREDS
of euros and one transfer reads like money moving FROM the person who
is owed. I do not see how any rounding convention produces that. I was
outvoted in triage (see notes/meeting_2026_10_03.md); if this patch
does not flip the suite, please read docs/data_dictionary.md end to
end before touching the rates table.
