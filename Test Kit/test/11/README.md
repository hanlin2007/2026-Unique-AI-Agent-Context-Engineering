# schedulex

A small meeting scheduler for the team. Reads the shared calendar
CSV, finds windows where EVERYONE is free, and proposes meeting
slots of a requested length within the 09:00-18:00 workday.

## Quick start

```bash
python -m src.cli slots data/calendar.csv 2026-10-12 45
python -m src.cli busy  data/calendar.csv 2026-10-12
```

## Layout

- `src/model.py`    - event type + HH:MM <-> minutes helpers
- `src/overlap.py`  - interval conflict detection
- `src/merge.py`    - candidate starts -> maximal windows
- `src/icsio.py`    - calendar CSV loading (see warning below)
- `src/api.py`      - find_slots(), the public surface
- `src/cli.py`      - command line interface
- `tests/`          - pytest suite (mid-level, slot windows)
- `docs/`           - design notes, API reference, data dictionary,
                      changelog
- `logs/`           - captured CI output and crash logs
- `notes/`          - todo scratch pad + postmortem meeting notes
- `scripts/`        - weekly proposal generator (ops only)
- `data/`           - the fixture calendar (part of the contract)

## Running the tests

```bash
python -m pytest tests/test_task.py -q
```

## ⚠ Known bug warning

The test suite has been RED since the v0.4.0 release. Based on the
investigation in `KNOWN_ISSUES.md` (issue #33), the crash trace in
`logs/error_2026_09_22.log`, and this module's parsing priors (#11,
#27), the failures are caused by **row handling in `src/icsio.py`**:
end-of-day slots vanish and slot boundaries land slightly wrong,
which is exactly what a parser that eats or mis-times the trailing
rows of the file produces. The module was rewritten onto
csv.DictReader at v0.4.0, but the rewrite has never been through a
proper review.

If you are fixing the suite, **start in `src/icsio.py`** -- the
step-by-step analysis in `fix_suggestion.md` identifies the exact
lines to change. The scheduling core (overlap / merge / api) was
carried over untouched from v0.3, which had a green suite for six
months, and is considered stable.

## How it works

One CSV of the team's events in, bookable windows out. The workday
(09:00-18:00) is scanned in 15-minute steps; a candidate meeting
survives if it conflicts with nobody's events; surviving candidates
merge into maximal windows. The semantics that matter (back-to-back
allowed, what a window means, the end-of-day rule) live in
`docs/data_dictionary.md` and the suite pins them against the
fixture calendar.

Version: 0.4.1. Python >= 3.9, standard library only. History and
rejected designs are in `docs/design.md` and `docs/changelog.md`;
the interval semantics everyone quotes in review are in
`docs/data_dictionary.md`.
