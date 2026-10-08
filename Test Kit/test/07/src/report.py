"""Report assembly: the single entry point used by tests and the CLI.

build_grade_report() runs the whole pipeline:

    key CSV         -> loader.load_answer_key
    submissions CSV -> loader.load_submissions
                    -> key.grade_submissions   (match outcomes)
                    -> rubric.score_student    (raw scores)
                    -> curve.apply_curve       (departmental curve)
                    -> cap at 100              (AFTER curving -- policy:
                       the cap is on the FINAL grade, not the raw)

The returned dict is the task's contract. Scores are floats at 2dp;
finals never exceed 100.
"""
from __future__ import annotations

from .curve import apply_curve
from .key import grade_submissions
from .loader import load_answer_key, load_submissions
from .rubric import score_student

PASS_MARK = 60.0
MAX_SCORE = 100.0


def build_grade_report(submissions_path: str, key_path: str) -> dict:
    """Build the full grade report dict (see module docstring)."""
    key = load_answer_key(key_path)
    submissions = load_submissions(submissions_path)
    outcomes = grade_submissions(submissions, key)

    student_ids = sorted({s.student_id for s in submissions})
    students = {}
    for sid in student_ids:
        raw = score_student(sid, outcomes, key)
        capped = min(raw, MAX_SCORE)
        final = apply_curve(capped)
        students[sid] = {"raw": raw, "curved": final, "final": final}

    finals = [s["final"] for s in students.values()]
    return {
        "students": students,
        "question_count": len(key),
        "curve_factor_applied": 1.15,
        "pass_mark": PASS_MARK,
        "class_average": round(sum(finals) / len(finals), 2),
        "top_score": max(finals),
        "pass_count": sum(1 for f in finals if f >= PASS_MARK),
    }
