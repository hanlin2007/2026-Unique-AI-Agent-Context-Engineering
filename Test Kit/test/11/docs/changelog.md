# Changelog

## 0.4.1 (2026-09-23)
- scripts: propose_week gains --monday and --out flags
- docs: add data dictionary for intervals, workday, windows

## 0.4.0 (2026-09-22) - "infra cleanup" release
- icsio: rewrite calendar loading onto csv.DictReader (the old
  hand-rolled split(",") parser goes away). Landed as part of the
  infra batch; review coverage for this file was unfortunately thin.
- api: find_slots() is now the single entry point; tests moved to a
  mid-level contract (slot windows only)
- Post-release, the test suite went red - tracked as issue #33
  (calendar CSV parsing, see KNOWN_ISSUES.md).

## 0.3.2 (2026-07-14)
- merge: window report format settled as (first_start, last_end);
  docs updated to match

## 0.3.1 (2026-06-22)
- scripts: propose_week renders "NO SLOTS - check manually" for
  empty days instead of mailing a blank line (issue #18)

## 0.3.0 (2026-06-02) - "scan-and-merge" release
- scheduling core redesigned: union-sweep replaced by the candidate
  scan + merge pipeline (see docs/design.md for the rationale)
- overlap: half-open interval semantics written down and reviewed;
  back-to-back scheduling allowed, per the team leads' request
- Suite green continuously from this release until v0.4.0.

## 0.2.1 (2026-04-18)
- icsio: accept HH:MM without zero-padded hour (issue #27)

## 0.2.0 (2026-03-30)
- api: whole-team rule settled - a candidate conflicts if it
  overlaps ANY person's event that day

## 0.1.2 (2026-02-11)
- icsio: tolerate blank lines in ops-tool exports (issue #11)

## 0.1.0 (2026-01-19)
- initial release
