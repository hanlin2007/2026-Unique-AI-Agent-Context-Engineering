# Grading calibration session

Date: 2026-09-14, attendees: course coordinator, Priya, w.nakamura,
two TAs (notes by intern)

Purpose: agree on how the Fall quiz is graded BEFORE the submissions
land. Everything decided here went into docs/grading_policy.md the
same week.

## Decisions

- Matching: case-insensitive, whitespace-tolerant, BOTH sides. The
  coordinator was firm: "the key's uppercase MC letters are a
  printing convention, not a grading rule."
- Partial credit: half points, half-UP rounding. One TA asked about
  banker's rounding "like numpy"; the coordinator's answer was "the
  student-facing rule is half-up, the code follows."
- Curve: 1.15 for Fall, applied to raw scores. The department wanted
  the top of the class compressed, hence...
- Ceiling: 100, applied AFTER the curve. Curved-then-capped. The
  curved column stays visible for transparency.
- Pass mark: 60 on the final.

## Open questions (parked)

- Whether partial alternatives should be per-student negotiable
  (coordinator: no, and do not ask again).
- Whether the curve factor should be published to students in
  advance (department: it already is, it is in the syllabus).

## Q&A from the floor

- Q (TA): "If a student writes the partial answer in uppercase, does
  it count?" A (coordinator): "Matching is case-insensitive. On both
  sides. I will keep saying this."
- Q (TA): "What if the curve makes someone fail who passed raw?"
  A: "The curve multiplies by MORE than one this term; nobody fails
  because of it. If the factor were ever below one, the ceiling
  conversation flips into a floor conversation and we reconvene."
- Q (intern): "Where does the 1.15 come from?" A: "Department letter,
  each term, based on the distribution. We do not compute it."

## Action items

- w.nakamura: write the policy doc, committee sign-off (done 2026-09-08
  retroactively; the doc pre-dates the meeting, the meeting RATIFIED it)
- TAs: grade the practice quiz by hand using the policy; compare
  against the pipeline output (done 2026-09-16, matched)
