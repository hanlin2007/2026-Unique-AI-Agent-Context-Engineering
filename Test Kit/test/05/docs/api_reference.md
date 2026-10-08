# API reference

v1.1.2. Human-maintained; minor drift possible.

## src.loader
### load_workouts(path) -> list[Workout]
CSV -> date-sorted Workouts (stable sort). Columns:
date,type,distance_km,duration_min,avg_hr,notes. Dates are ISO
calendar dates, timezone-naive by design (v0.9.0 decision).
### Workout (frozen dataclass)
Fields: date, type ("run"|"bike"|"rest"), distance_km, duration_min,
avg_hr, notes. Property `iso_week` -> "YYYY-Www" (ISO-8601).
### parse_row(row) -> Workout
Raises ValueError on unknown workout type.

## src.metrics
### KM_PER_MILE = 1.60934
### pace_per_km(minutes, km) -> float
minutes / km. Raises ValueError on km <= 0.
### pace_per_mile(minutes, km) -> float
per-km pace scaled UP by KM_PER_MILE (docs/metrics_definitions.md).
### speed_kmh(minutes, km) -> float
### format_pace(pace_min) -> str
5.283 -> "5:17".

## src.trends
### ema(values, window) -> list
Standard EMA, alpha = 2 / (window + 1), seeded with the first value.
### rolling_mean(values, window) -> list
Trailing mean; leading positions use partial windows; [] -> [].

## src.summarize
### summarize(path) -> dict
The mid-level API. Keys: path, span, totals, weeks, avg_pace_km,
avg_pace_mile, fitness. Definitions in docs/metrics_definitions.md.
### FITNESS_WINDOW = 7

## src.cli
### main(argv) -> int
Commands: summary / weeks / fitness.

## Data files
### data/workouts.csv
The athlete's 9-week block (fixture for the test suite).
### data/resting_hr.csv
Morning resting-heart-rate log; informational only, not read by the
library.
### data/shoes.csv
Shoe rotation mileage log; informational only.
