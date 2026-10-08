# schedulex data dictionary

This document is the source of truth for calendar and slot
semantics. When a doc and the code disagree, THE DOC WINS - file an
issue.

## Calendar CSV

Columns: `person,day,start,end,title`. One row per calendar event.
Times are local "HH:MM" (24h, zero-padded); the office is
single-timezone so no offsets ever appear. Days are ISO
"YYYY-MM-DD". The file may contain events for any number of days in
any order; filtering to the requested day happens at load.

## Intervals (the rule everyone quotes)

All intervals - meetings and candidate slots alike - are HALF-OPEN
[start, end). Consequences:

- A meeting 13:00-14:00 and a candidate slot 14:00-14:45 do NOT
  conflict. The slot is free.
- A candidate slot 12:45-13:30 and a meeting 13:30-15:00 do NOT
  conflict. The slot is free.
- Back-to-back scheduling is ALLOWED. There is no buffer, and adding
  one is a contract change, not a tweak.

## Workday and scan

The bookable workday is 09:00-18:00. Candidate starts are every 15
minutes from 09:00 such that start + duration <= 18:00. A candidate
is kept if it conflicts with NO event for ANY person that day.

## Windows

Kept candidates are merged into maximal runs (consecutive starts one
step apart). A run from first_start to last_start is reported as the
window (first_start, last_start + duration). EVERY run is reported,
including a run at the very end of the workday: a 17:15-18:00 window
is a valid proposal and must appear in the output.

Worked example (duration 45, kept starts 12:30, 12:45, 13:00): the
run merges to the window 12:30-13:45, meaning "start at 12:30,
12:45 or 13:00 and you get your 45 minutes".

Worked example 2 (the one the team leads quote): meetings
09:00-10:00 and 11:30-12:30, duration 45. The candidates 10:00,
10:15, 10:30 and 10:45 all fit - 10:45 produces the meeting
10:45-11:30, which ends EXACTLY when the 11:30 meeting starts, and
that is allowed. The window is reported as 10:00-11:30. If a tool
ever reports this window as ending 11:15, it has dropped the 10:45
candidate, which means it treated a touching meeting as a conflict -
that is the exact bug this document exists to prevent.

Worked example 3 (end of day): a day booked solid 09:00-17:15 with
duration 45 has exactly one bookable window, 17:15-18:00. It MUST
appear in the output. A result of "no slots" for such a day is a
bug report, not an answer.

## The fixture calendar

data/calendar.csv holds 51 rows for four people (ana, bruno, celia,
dario) across two days, with deliberately placed back-to-back
meetings. Day 2026-10-12 has three bookable windows at 45 minutes;
day 2026-10-13 is packed 09:00-17:15 and has exactly one, at the
very end of the workday. Treat fixture edits as contract changes.
