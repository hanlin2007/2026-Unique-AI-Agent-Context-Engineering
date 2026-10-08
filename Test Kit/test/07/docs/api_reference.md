# API reference

v0.6.1. Human-maintained; minor drift possible.

## src.loader
### load_answer_key(path) -> dict
CSV -> {question_id: KeyEntry}. KeyEntry = (question_id, answer,
points, partial); answer is kept AS PRINTED.
### load_submissions(path) -> list[Submission]
CSV -> submissions sorted by (student_id, question_id).

## src.key
### normalize_answer(text) -> str
strip + lower + collapse internal whitespace.
### match_answer(student_answer, key_entry) -> str
"full" | "partial" | "none"; policy in docs/grading_policy.md.
### grade_submissions(submissions, key) -> dict
{(student_id, question_id): outcome}.

## src.rubric
### half_points(points) -> int
Half credit per departmental rounding policy.
### score_question(outcome, points) -> float
### score_student(student_id, outcomes, key) -> float
Raw total (pre-curve).

## src.curve
### CURVE_FACTOR: float
Fall 2026: 1.15.
### apply_curve(raw_score, factor) -> float
round(score * factor, 2). NOTE: open issue #63 - see KNOWN_ISSUES.md.
### uncurve(curved_score, factor) -> float
### curve_table(raw_scores, factor) -> list

## src.report
### build_grade_report(submissions_path, key_path) -> dict
Keys: students, question_count, curve_factor_applied, pass_mark,
class_average, top_score, pass_count. students[sid] keys: raw,
curved, final.

## Usage example

```python
from src.report import build_grade_report
rep = build_grade_report("data/submissions.csv", "data/answer_key.csv")
rep["students"]["S07"]   # {'raw': ..., 'curved': ..., 'final': ...}
rep["class_average"]     # 2dp float over the FINALS
rep["top_score"]         # max final; never above 100 by contract
rep["pass_count"]        # finals >= pass_mark
```

Column semantics (raw vs curved vs final) are defined in
docs/grading_policy.md; the report merely materialises them.
