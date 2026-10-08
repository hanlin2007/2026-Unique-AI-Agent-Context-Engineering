# Proposed fix for issue #42 (currency rounding drift)

Author: m.okafor, 2026-10-02
Status: PROPOSED, review pending (branch fix/issue-42-currency-rounding)

## Root cause (analysis)

`convert()` currently does:

```python
usd = Decimal(str(amount)) / RATES_USD[src]
out = usd * RATES_USD[dst]
return float(round_to_minor(out, dst))
```

The problem: `round_to_minor` quantizes with ROUND_HALF_EVEN, but for
0-exponent currencies (JPY, KRW) the quantum is `Decimal("1")` and
half-even at that granularity interacts badly with rates that have >2
decimal places. The multiplication keeps full precision, so values like
149.354999... round DOWN where consumers expect them to round UP.

Additionally, `Decimal(str(amount))` can produce non-normalised
Decimals (`Decimal("300.0")` keeps exponent -1), which shifts the
intermediate precision of the division.

## Proposed patch

In `src/currency.py`:

1. Normalise the input: `Decimal(str(amount)).normalize()`
2. Round the USD intermediate to 6 places before multiplying:
   `usd = usd.quantize(Decimal("0.000001"))`
3. For 0-exponent currencies, switch the final quantize to half-up:

```python
if EXPONENTS[currency] == 0:
    return amount.quantize(quantum, rounding=ROUND_HALF_UP)
return amount.quantize(quantum, rounding=ROUND_HALF_EVEN)
```

## Why this should turn the suite green

The failing fx assertions compare integers exactly; once conversion
stops drifting at the boundary, the JPY totals should match the
expected values again. The interest figure goes through the same
display helpers, so it should follow.

## Confidence

High - same class of bug as v0.2.1 and v0.3.0, and the crash trace in
logs/error_2026_09_30.log points into currency.py's quantize path.
