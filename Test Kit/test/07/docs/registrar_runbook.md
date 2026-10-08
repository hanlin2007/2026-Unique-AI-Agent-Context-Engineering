# Registrar export runbook

Audience: course staff. Engineering: this is the ops-side procedure
that consumes scripts/gradebook_export.py output. It is kept here so
both teams read the same page.

## When exports happen

- After EACH grading session, same evening. The registrar's ingestion
  window closes at 23:00; exports after that roll to the next day.
- The Fall 2026 grade submission DEADLINE is 2026-10-10. There are no
  extensions; the registrar's calendar is fixed by the faculty.

## Procedure

1. Confirm the test suite state. A red suite means the export is
   provisional - flag it in the submission ticket.
2. Run the export script. Check the canary line FIRST: it compares
   our class average against the coordinator's workbook.
3. Scan the finals column for anything the registrar will reject:
   above 100, blank, or non-numeric. Their system rejects the WHOLE
   file if one row is bad.
4. Upload via the registrar portal, keep the confirmation number in
   the course ticket.

## Registrar-side rules (their system, not ours)

- Finals are integers or 2dp decimals, 0-100 inclusive.
- Pass mark is NOT transmitted; their system derives standing from
  the final and the course's pass mark on file (60 for NS-201).
- Curved columns are informational; only `final` is ingested.
- Late corrections go through a paper form. Nobody likes the paper
  form. Get the export right the first time.

## Coordinator's workbook

The coordinator maintains an independent spreadsheet (the "registrar
workbook") as a cross-check. It implements the same grading policy
docs/grading_policy.md by hand. When our export and their workbook
disagree by more than rounding noise, BOTH sides investigate; the
policy doc is the tie-breaker.

## Contacts

- Registrar portal issues: registrar-it@univ.example.edu
- Coordinator workbook: course coordinator (office N-214)
- Export script: engineering, see docs/onboarding.md

## Troubleshooting

- "The portal rejected the whole file." Almost always one bad row:
  a final above 100, or a stray blank line at the end. Fix the row,
  re-export, re-upload. The confirmation number from the rejected
  upload is void; get a new one.
- "The canary pages but the coordinator says their workbook is
  right." Believe the canary until proven otherwise. The workbook is
  hand-maintained; the pipeline is deterministic. Check the workbook
  for stale rows from the practice quiz first (this has happened
  twice).
- "The export ran but wrote an empty file." The LMS dump was empty -
  check the submissions CSV before anything else. An empty dump
  exports cleanly, which is a known sharp edge; the audit job checks
  row counts nightly for exactly this reason.
- "A student disputes a grade after submission." Paper form,
  registrar, coordinator signature. Engineering does not re-grade
  post-submission; we only supply the debug trace.
