# Onboarding - quizgrade team

Welcome! This doc should get you productive in an afternoon.

## Your first hour

1. Read README.md top to bottom, then docs/grading_policy.md (it is
   the committee-approved contract; docs/design.md explains how the
   code maps onto it).
2. Run the CLI against the fixtures - `report`, `roster` and
   `student` show you everything the pipeline does.
3. Run the test suite. It is currently RED and that is EXPECTED - see
   KNOWN_ISSUES.md #63. Your first week will probably touch this.

## Where things live (and where the bugs live)

- src/loader.py, src/key.py, src/rubric.py - the grading pipeline.
  Split out of the old grader.py at v0.6.0 and reviewed then. Treat
  as read-only unless a staff engineer signs off.
- src/curve.py - where the action is. Three curve incidents in a year
  (#29, #41, and the open #63). If a final score looks wrong anywhere
  in a report, the odds are good the trail ends here.
- src/report.py - orchestration only; no logic lives here by design.
- scripts/gradebook_export.py - registrar-facing export, runs after
  every grading session. Its curve canary line is the early-warning
  for curve issues.
- logs/ - captured CI output. Grep it before you debug; someone has
  probably seen your failure already.

## Team rituals

- Postmortem doc for every red-suite episode > 24h (see notes/).
- The curve factor changes each term; the department emails it and it
  goes in src/curve.py with a changelog entry.
- Grade complaints go through the policy doc first, the code second.

## Glossary

- "key" - the answer key CSV; one row per question, points and an
  optional partial-credit alternative.
- "outcome" - full / partial / none, per student per question.
- "raw" - pre-curve total. "curved" - scaled, pre-ceiling. "final" -
  what the registrar ingests.
- "the curve" - the departmental scaling factor. Historically cursed.

## Common pitfalls for new team members

- Reading the `curved` column as the grade. It is pre-ceiling, by
  design; the registrar never sees it.
- Assuming the submissions CSV is cleaned. It is an as-submitted LMS
  dump: stray spaces, mixed case, the works. Cleaning is a pipeline
  concern, not a data-entry concern.
- "Fixing" a red suite by editing expected numbers in the tests. The
  tests encode the registrar's workbook figures; if you change them
  you own the conversation with the coordinator.
- Touching the pipeline modules during a curve incident. The v0.6.0
  review is what keeps the grade audit defensible; get a staff
  engineer's sign-off first (you will not get it mid-incident).
