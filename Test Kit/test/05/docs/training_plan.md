# Training plan - autumn half marathon block

Athlete: recreational runner, target race 2026-09-26 (half marathon).
Coach: m.petrova. This document is context for the fixture
(data/workouts.csv); the analyzer does not read it.

## Block structure (9 weeks, 2026-07-27 .. 2026-09-27)

| phase   | weeks       | intent                              |
|---------|-------------|-------------------------------------|
| base    | W31-W33     | build volume, strides weekly        |
| cutback | W34         | ~25% volume drop, absorb            |
| build   | W35-W37     | peak volume, longest runs           |
| taper   | W38-W39     | volume down, keep some intensity    |

## Weekly template (base/build weeks)

- Mon: easy run
- Tue: steady run
- Wed: midweek medium-long OR cross-training spin
- Thu: cross-training (bike) OR steady run
- Fri: strides OR rest
- Sat: steady run
- Sun: long run

## Rules of thumb the coach actually checks

- Weekly run volume should not jump more than ~10% week over week
  outside cutback/taper.
- Long run stays under ~35% of weekly volume.
- Pace is discussed per MILE with this athlete (they came from a
  miles-based plan); the analyzer must report both units.
- Fitness (the EMA trend) should rise through base/build, crest late
  in the build, and hold roughly level through the taper. A trend
  that sags mid-block means the load maths or the bucketing is wrong,
  and we debug the TOOL before we debug the athlete.

## Notes

- The two planned rest days (2026-07-31, 2026-08-14) are deliberate;
  the athlete otherwise runs or rides daily.
- The watch was one hour behind for part of August (holiday time).
  All sessions were morning or afternoon, so no date bucketing is
  affected; noted here because issue #33 keeps citing it.
