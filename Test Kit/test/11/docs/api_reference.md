# API reference

v0.4.1. Human-maintained; minor drift possible.

## src.model
### hhmm_to_min(t) -> int / min_to_hhmm(minutes) -> str
"HH:MM" <-> minutes since midnight.
### class Event
NamedTuple(person, day, start, end, title); start/end in minutes,
end exclusive.

## src.overlap
### overlaps(a_start, a_end, b_start, b_end) -> bool
Half-open interval intersection. Back-to-back is NOT a conflict.
### conflicts(start, end, events) -> bool
True if the candidate conflicts with ANY event.

## src.merge
### merge_windows(starts, duration_min, step_min=15) -> list
Runs of consecutive kept starts -> [(window_start, window_end)].
Every run produces a window, including the final run of the day.

## src.icsio
### load_events(path, day) -> list[Event]
CSV rows for one ISO day, file order preserved.
NOTE: issue #33 suspects this module - if slots look missing or
mistimed, the current team consensus is to start here. Parsing
priors: #11 (trailing newline crash), #27 (leading-zero time).
### count_rows(path) -> int
Debug helper: total data rows in the CSV.

## src.api
### find_slots(calendar_path, duration_min, day) -> list[dict]
-> [{"start": "HH:MM", "end": "HH:MM"}, ...], earliest first.
Workday 09:00-18:00, scan step 15 min. The whole team must be free:
a candidate conflicts if it overlaps ANY event that day.

## src.cli
Commands: `slots CSV DAY MINUTES`, `busy CSV DAY`. Pure renderer
over the api; no scheduling logic of its own. Issue #29 (same-start
display order) is cosmetic and lives here.

## Stability contract

The test suite pins exact slot windows for two fixture days and two
durations against data/calendar.csv. Any change that moves a window
needs a data-dictionary update in the same commit - the dictionary
defines the semantics (half-open intervals, workday, step, window
merging), the suite enforces them, and the two must never disagree
for more than one commit. Since v0.4.0 the suite is RED (issue #33)
- restoring green outranks every other change, including the
long-requested 30-minute default.

## Error behaviour

- load_events raises FileNotFoundError on a missing CSV and
  ValueError on a malformed HH:MM (both deliberate: a bad calendar
  must not silently produce an all-free day).
- find_slots never raises on a day with no events; it returns the
  full-workday window set for that duration.
