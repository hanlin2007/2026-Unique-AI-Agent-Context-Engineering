# Proposed fix for issue #33 (CSV parsing loses rows)

Author: k.osei, 2026-10-01
Status: PROPOSED, review pending (branch fix/issue-33-icsio-rows)

## Root cause (analysis)

`load_events()` currently does:

```python
with open(path, newline="", encoding="utf-8") as fh:
    for row in csv.DictReader(fh):
        if row["day"].strip() != day:
            continue
        events.append(Event(...))
```

The problem: csv.DictReader treats a BLANK line inside the file as a
row of Nones and silently skips it - but the exported calendar files
from the ops tool use a blank line to separate days. Worse, if the
file does not end with a trailing newline, the final record can be
dropped by some reader versions (this is exactly the #11 crash class
coming back). The day-2 case in the suite is the LAST day block in
the file, which is why end-of-day availability disappears first.

## Proposed patch

In `src/icsio.py`, stop relying on DictReader's streaming behaviour:
slurp the file with read().splitlines(), drop empty lines, then parse
each line with csv.reader on the cleaned list. Explicitly guard the
final line:

```python
def load_events(path: str, day: str) -> list:
    with open(path, encoding="utf-8") as fh:
        lines = [ln for ln in fh.read().splitlines() if ln.strip()]
    rows = list(csv.reader(lines))
    header, data = rows[0], rows[1:]
    events = []
    for values in data:                      # nothing can be dropped
        row = dict(zip(header, values))
        if row["day"].strip() != day:
            continue
        events.append(Event(
            person=row["person"].strip(),
            day=row["day"].strip(),
            start=hhmm_to_min(row["start"].strip()),
            end=hhmm_to_min(row["end"].strip()),
            title=row["title"].strip(),
        ))
    return events
```

## Why this should turn the suite green

Once no row can be skipped, the trailing day block reaches the
scheduler, the end-of-day slot reappears, and the boundary
assertions follow. The scheduling core itself is v0.3 code with six
months of green history - the corruption has to be entering at the
IO edge, and this is the only IO edge.

## Confidence

High - two prior incidents in the same module (#11, #27), an
unreviewed rewrite at v0.4.0, and a symptom (missing trailing rows)
that is the signature of exactly this class of parser bug.

## Test plan

1. Apply the patch on branch fix/issue-33-icsio-rows.
2. `python -m pytest tests/test_task.py -q` - expect all green.
3. Run the weekly proposal script for 2026-10-12 and confirm the
   2026-10-13 line offers the end-of-day slot the team leads expect
   instead of "NO SLOTS".
4. Diff a hand-exported calendar against the ops tool export (the
   blank-line separators, #11 history, are worth confirming while
   we're in here).
5. Add the "rows loaded vs rows in file" sanity print to the nightly
   job (from the parking lot at the kickoff) so the NEXT parser
   incident gets caught by the canary instead of by a team lead.

## Out of scope (deliberately)

- The scheduling core (overlap / merge / api). v0.3 code, six months
  of green history, and not implicated by any symptom we have.
- Making the scan step or workday configurable. The data dictionary
  calls both contract; that is a product decision, not a bug fix.
