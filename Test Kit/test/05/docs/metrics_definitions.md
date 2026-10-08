# Metric definitions

The CONTRACT for src/metrics.py and src/trends.py. When code and prose
disagree, the prose wins and the code is wrong.

## Weekly volume

Run distance summed per ISO-8601 week (Monday start). Rides are
cross-training and NEVER counted in run volume. Rest days contribute
nothing.

## Pace

    pace_per_km   = total run minutes / total run km      [min/km]
    pace_per_mile = pace_per_km * 1.60934                 [min/mile]

A mile is 1.60934 km - LONGER than a kilometre - so the per-mile pace
is always a LARGER number of minutes than the per-km pace. Sanity
check that catches most conversion bugs: a 5:20/km runner runs about
8:35/mile, never 3:19/mile.

Pace is undefined for zero distance and must never be computed over
rest entries (they carry distance_km = 0).

## Speed

    speed_kmh = km / (minutes / 60)

## Daily load

    load(day) = sum over sessions that day of duration_min * avg_hr / 100

Days with no session - including rows of type "rest" - contribute 0.
The series covers the FULL calendar span from the first to the last
log date, inclusive, one value per day.

## Fitness trend (EMA)

    alpha  = 2 / (window + 1)        # window=7 -> alpha=0.25
    ema[0] = load[0]
    ema[i] = alpha * load[i] + (1 - alpha) * ema[i-1]

This is the standard EMA used by pandas (`span=window`) and the
training-stress literature. The window is 7 for the summary's fitness
figure. Do not confuse alpha = 2/(N+1) with alpha = 1/N (a different
smoothing convention used by some charting tools); we use 2/(N+1).

## Rounding

Pace values are reported to 3 decimal places, volumes to 2 (km) or 1
(minutes), fitness values to 3.
