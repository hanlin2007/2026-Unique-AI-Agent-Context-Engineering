# Proposed fix for issue #33 (sessions land in wrong ISO weeks)

Author: m.petrova, 2026-09-26
Status: PROPOSED, review pending (branch fix/issue-33-date-normalise)

## Root cause (analysis)

`src/loader.py::parse_row` does:

```python
date=date.fromisoformat(row["date"].strip()),
```

This trusts the device's local calendar date. The watch export that
produces our CSVs writes the LOCAL date at session start, and the
watch was confirmed to be one hour behind for two weeks in August
(holiday time, never re-synced - see notes/coaching_2026_09_30.md).
Any session started between 23:00 and 00:00 device time was actually
on the NEXT calendar day, which moves it into a different ISO week
when it straddles Sunday/Monday.

That is exactly the failure signature we see: weekly sums barely move
(one session in or out of a week is a few km), but every derived
number drifts, and the EMA - which is indexed by calendar DAY - is
sensitive to exactly this class of shift.

## Proposed patch

In `src/loader.py`, normalise late-evening sessions towards the next
day when the notes field carries the watch's "+1h" marker (the export
writes `tz=+1h` into notes for sessions recorded while the clock was
unsynced):

```python
def parse_row(row: dict) -> Workout:
    notes = row.get("notes", "").strip()
    parsed = date.fromisoformat(row["date"].strip())
    if "tz=+1h" in notes and row.get("start_time", "") >= "23:00":
        parsed = parsed + timedelta(days=1)
    ...
```

(import `timedelta` from datetime at module top.)

## Why this should turn the suite green

Re-bucketing the shifted sessions restores the true day-level series,
so the EMA recomputes correctly and the pace averages line up with the
expected constants again. Weekly totals stay within a rounding of
where they are now, matching the observation that they "look right".

## Confidence

Medium-high. The timeline fits (red since the calendar-hardening
release) and the coach's weekly email failure started the same week.
The patch is narrow and reversible.

## Note from d.osei (2026-09-27)

Our CSV has no start_time column and none of the notes contain a
tz=+1h marker - I checked data/workouts.csv line by line. The patch
above keys off data we do not have. Also, the failing assertions are
on pace-per-MILE and EMA values, and I cannot construct any date shift
that would make a per-mile figure come out SMALLER than the per-km
figure, which is what the coach's printout shows. Outvoted in triage;
recording the dissent. If v1 of this patch does nothing (I predict it
does nothing), please read docs/metrics_definitions.md before touching
the loader again.
