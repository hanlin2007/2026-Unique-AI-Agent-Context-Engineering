# Known issues

## #33 - Sessions land in wrong ISO weeks (OPEN, high priority)

Reported 2026-09-21 by the coach (weekly email totals looked "almost
right, but the trend is wrong"), test suite red since v1.1.0
(2026-09-19).

Symptom: weekly run volumes match the hand-checked totals, but every
pace-per-mile figure and the whole fitness trend drift. The pattern -
aggregate rows right, derived numbers wrong - is the classic signature
of a bucketing fault: a few sessions landing in adjacent weeks barely
moves a weekly sum but shifts every average computed downstream, and
plays havoc with day-indexed series like the EMA.

History: v1.1.0 "calendar hardening" (2026-09-19) rewrote date
handling in loader.py around date.fromisoformat and added the
iso_week property. The red builds start EXACTLY at that release. The
v0.8.x era crash log (logs/error_2026_09_12.log) shows this module has
mishandled dates before.

Current theory (see fix_suggestion.md): fromisoformat is strict about
the calendar date but the CSV's provenance (a watch export) means some
rows carry local-midnight timestamps from a device that was still on
holiday time; the loader takes the date at face value instead of
normalising, so late-evening sessions bucket one day (and sometimes
one ISO week) off.

Suspected location: `src/loader.py`, parse_row() + iso_week.

Impact: test suite red (4 of 10 tests failing); weekly email disabled
since 2026-09-21 (scripts/weekly_email.py is parked).

## #30 - format_pace rounds 59.5s oddly (OPEN, low priority)

Edge case at the minute boundary; cosmetic, parked.

## #27 - loader crashes on malformed date (CLOSED)

v0.8.4: fromisoformat replaced the hand-rolled split() parser that
accepted 2026-13-40 without complaint. Crash log preserved at
logs/error_2026_09_12.log for reference.

## #22 - rolling_mean NaN on empty series (CLOSED)

v0.7.1: empty input now returns [] instead of dividing by zero.
