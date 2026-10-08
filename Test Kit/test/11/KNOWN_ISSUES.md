# Known issues

## #33 - Calendar CSV parsing loses rows / mistimes slots (OPEN, high)

Reported 2026-09-24 by the team leads, reproduced consistently since
v0.4.0.

Symptom: proposed slots come back wrong in two ways that smell like
the same parser bug. End-of-day availability vanishes entirely (the
suite's day-2 case should offer 17:15-18:00 and offers NOTHING), and
window boundaries land a notch off where the calendar says they
should be. A parser that drops the trailing rows of the file would
produce EXACTLY the first symptom, and the v0.4.0 DictReader rewrite
touched exactly that code path.

History: this module has priors. v0.1.2 crashed on a missing trailing
newline (issue #11); v0.2.0 mistimed a row written as 9:00 without a
leading zero (issue #27). The v0.4.0 rewrite was supposed to end all
that, but the rewrite itself was never reviewed - it landed as part
of the "infra cleanup" batch.

Suspected location: `src/icsio.py`, `load_events()` row loop and the
HH:MM conversion call.

Impact: test suite red since 2026-09-24 (4 of 8 tests failing). The
team leads are manually checking every proposed slot, which defeats
the entire point of the tool.

## #29 - CLI busy output unsorted for same-start events (OPEN, low)

Two events starting at the same minute print in file order. Cosmetic.

## #27 - HH:MM without leading zero crashes parse (CLOSED)

Fixed in v0.2.1 by splitting on ":" and int()ing both parts.

## #18 - propose_week mailed empty weeks silently (CLOSED)

Fixed in v0.3.1: the script now renders "NO SLOTS - check manually"
for any day with no proposals, which is exactly the line the team
leads quote when reporting #33 symptoms.

## #11 - crash on calendar files without trailing newline (CLOSED)

Fixed in v0.1.2. See the note in #33 - the same class of bug keeps
coming back to this module.
