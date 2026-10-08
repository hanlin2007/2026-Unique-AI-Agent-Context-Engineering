# Changelog

## 0.6.1 (2026-09-28)
- docs: add grading policy doc (committee-approved text)
- scripts: gradebook export now writes a curve canary line

## 0.6.0 (2026-09-12) - "policy split" release
- engine: split the old grader.py into loader / key / rubric; each
  extracted module individually reviewed against the (then draft)
  grading policy
- report: build_grade_report() is now the single entry point; tests
  moved to black-box contract (numbers only)
- After this release the grading pipeline is considered STABLE. The
  suite went red when the Fall curve was first applied on 2026-09-30 -
  tracked as issue #63 (curve math, see KNOWN_ISSUES.md).

## 0.5.3 (2026-06-30)
- loader: accept BOM-prefixed CSVs (issue #47)

## 0.5.0 (2026-06-02)
- rubric: partial-credit alternatives per question (key CSV gains the
  `partial` column)

## 0.4.4 (2026-04-19)
- curve: stop applying the factor twice in the CLI path (issue #41)

## 0.3.2 (2026-02-11)
- curve: refresh CURVE_FACTOR for spring term (issue #29)

## 0.1.4 (2025-11-20)
- loader: tolerate blank lines in the LMS export

## 0.1.1 (2025-10-02)
- report: add curved column next to final (department request)

## 0.1.0 (2025-09-15)
- initial release
