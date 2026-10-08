# schedulex design notes

Last updated: 2026-09-20 (v0.4.0 era). Maintainer: l.brandt.
Audience: anyone touching src/. Read the invariants BEFORE the code;
the code assumes you have, and review will ask about them.

## Goals

schedulex answers one question: "when can the whole team meet for N
minutes on day D?" It reads the exported calendar CSV, finds every
window where nobody has anything, and reports maximal bookable
windows inside the 09:00-18:00 workday. The design favours
*explainability*: a team lead should be able to verify any proposed
slot against the CSV by eye in under a minute.

## The pipeline

```
icsio.py     IO edge: calendar CSV -> Events for one day
overlap.py   interval conflict detection (half-open intervals)
api.py       workday scan: 15-min steps, keep conflict-free starts
merge.py     kept starts -> maximal bookable windows
```

The scan-and-merge split is deliberate: the scan knows about events,
the merge knows about runs. Neither knows the other's business.

## Invariants

1. Intervals are half-open [start, end). A slot that ends exactly
   when a meeting starts is FREE; a meeting that ends exactly when a
   slot starts does not block it. Back-to-back scheduling is a
   feature - the team leads asked for it explicitly when we replaced
   the old 15-minute-buffer tool.
2. The workday is 09:00-18:00 and the scan step is 15 minutes; both
   are contract, not configuration.
3. A window means "you can start anywhere from window.start to
   window.end - duration and fit". window.end = last start +
   duration.
4. EVERY bookable window is reported, including one at the very end
   of the workday. A 17:15-18:00 window is a perfectly good slot and
   dropping it is a bug, not a rounding choice.
5. Times are local wall-clock strings; there is no timezone handling
   anywhere and none is wanted (single-office team).
6. The suite pins windows for two fixture days; the fixture CSV is
   part of the contract and is not edited to make numbers move.

## Alternatives considered (and rejected)

A busy-interval UNION sweep (merge all events into maximal busy
blocks, then report the complement) was the v0.2 design. It was
replaced by scan-and-merge at v0.3 for one reason: explainability.
With the union design, a wrong answer required re-deriving the whole
union by hand to debug; with the scan, every rejected candidate has
exactly one offending event, and the debug trace prints them side by
side. The scan costs O(candidates x events) - 36 x ~50 per day, so
nothing - and buys a trace a team lead can audit in a minute.

A buffer between meetings (the old tool had 15 minutes) was
explicitly rejected by the team leads: their calendars are packed
precisely because they book back-to-back, and a buffered tool found
them nothing. The half-open interval rule (invariant 1) is the
written-down version of that decision.

## What would make us revisit this design

- Multi-timezone teams (times stop being wall-clock; real change).
- Rooms or partial-team queries (the "whole team free" rule becomes
  a constraint problem; this tool is the wrong shape for it).
- Sub-15-minute granularity (the step is contract; changing it
  changes the suite).
None of these are scheduled.

## Operational notes

The calendar CSV is produced by the ops team's export tool, not by
hand: people edit their own calendars all week and the export lands
nightly. Two quirks of that pipeline matter here. First, the export
separates day blocks with a blank line (the v0.1.x parser crashed on
exactly that - issue #11 - and the current loader skips them
silently). Second, rows within a day are in the order people created
the events, NOT sorted by start time; nothing downstream may assume
sorted events, and the cli's `busy` command sorts for display at its
own edge. The nightly-slots job (scripts/propose_week.py) is the
team leads' canary: they know roughly which days should offer
something, and a "NO SLOTS" line on a day that visibly has a gap is
how #33 was first reported.
