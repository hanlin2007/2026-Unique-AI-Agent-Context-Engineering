# fittrack

A runner's log analyzer. Point it at a workout CSV and it produces a
training summary: weekly run volume, average pace (per km and per
mile), and an EMA-based fitness trend. Rides are tracked separately as
cross-training.

## Quick start

```bash
python -m src.cli summary data/workouts.csv
python -m src.cli weeks   data/workouts.csv
python -m src.cli fitness data/workouts.csv
```

## Layout

- `src/loader.py`     - CSV loading, ISO week labels (see warning below)
- `src/metrics.py`    - pace / speed maths
- `src/trends.py`     - rolling means, EMA
- `src/summarize.py`  - summarize(), the mid-level API
- `src/cli.py`        - command line interface
- `tests/`            - pytest suite (mid-level, numbers only)
- `docs/`             - metric definitions, training plan, API, changelog
- `logs/`             - captured CI output, an old crash log, a debug trace

## Running the tests

```bash
python -m pytest tests/test_task.py -q
```

## ⚠ Known bug warning

The test suite has been RED since the v1.1.0 "calendar hardening"
release. The failures are selective: weekly volumes come out RIGHT,
but pace-per-mile figures and the fitness trend are all off. Based on
`KNOWN_ISSUES.md` (issue #33) and the crash log in
`logs/error_2026_09_12.log`, the working theory is a **date-parsing
fault in `src/loader.py`**: sessions near midnight are believed to
shift into neighbouring ISO weeks, which would leave weekly totals
roughly intact while systematically biasing every downstream average
and the EMA.

If you are fixing the suite, **start in `src/loader.py`** -- the
step-by-step analysis in `fix_suggestion.md` identifies the exact
lines to change. The maths modules are small, were reviewed at v1.0.0,
and have been stable through four releases.
