# quizgrade design notes

Last updated: 2026-09-12 (v0.6.0 era).

## Goals

quizgrade turns a submission dump into registrar-ready grades:
key in, submissions in, grade report out. The design favours
*defensibility*: every grade must be explainable to a student who
files a complaint, through a small number of pure pipeline stages.

## The pipeline

```
loader.py   IO edge: key CSV + submissions CSV -> typed records
key.py      answer normalisation + match outcomes (full/partial/none)
rubric.py   outcomes -> points, per-question and per-student raw
curve.py    the departmental curve (pure function of one score)
report.py   orchestration; build_grade_report() is the only entry
```

Every stage except the IO edge is a pure function.

## Invariants

1. Matching semantics live ONLY in key.py and must agree with
   docs/grading_policy.md ("matching"). The policy doc is the
   contract; the code was reviewed against it at v0.6.0.
2. Partial credit rounding lives ONLY in rubric.py and must agree
   with docs/grading_policy.md ("partial credit").
3. curve.py is a pure, stateless scaling function. It knows nothing
   about caps, pass marks, or other students. Anything the curve
   emits is, by design, "pre-final".
4. The 100 ceiling is applied ONCE, at the report stage, in the order
   given by docs/grading_policy.md ("the ceiling"). curve.py must
   never cap -- a capped curve would hide raw distinctions the
   department wants preserved in the curved column.
5. The report's `curved` column shows the pre-ceiling curved value;
   `final` is what the registrar ingests.

## Why partial credit is integer-valued

The department gradebook only stores integers per question. Half
credit therefore has to resolve to a whole number, and the rounding
rule is policy, not math taste (see grading_policy.md).

## Future directions (parked)

- per-question statistics in the report (needs outcome histograms)
- multiple submissions per question (needs attempt numbering)
- migrating the registrar workbook to read our JSON directly

## Historical incidents (why the invariants exist)

- v0.3.2 (#29): CURVE_FACTOR left at the spring value into the fall
  term. Every final was uniformly low; the canary caught it in one
  night. Lesson: the factor is configuration, reviewed each term.
- v0.4.4 (#41): the CLI applied the curve AND the report applied it
  again. Finals came out 32% high; a student emailed to ask why her
  91 became 120. Lesson: exactly one component applies the factor.
- The open #63 is filed in the same module by analogy. Whether that
  analogy holds is, at time of writing, an open question - see
  notes/meeting_2026_10_04.md for the dissent.

## Rejected designs

- Per-question curves: rejected by the department; the curve must be
  uniform so students can verify their own arithmetic.
- Capping inside curve.py: rejected at v0.6.0 review. A capping curve
  hides the shape of the top of the class; the ceiling is a REPORT
  concern (invariant 4). This is called out because it comes up
  every term, and it came up again in the #63 patch discussion.
- Storing outcomes in the submissions CSV: rejected; the CSV is an
  as-submitted dump and must stay byte-identical to the LMS export.
