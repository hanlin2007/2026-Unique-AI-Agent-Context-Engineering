"""Answer normalisation and matching.

Matching policy (docs/grading_policy.md, "matching"): comparison is
CASE-INSENSITIVE and ignores surrounding whitespace, on BOTH sides.
The key as printed may contain uppercase (multiple-choice letters are
printed as "B", "A", ...); students write back in any case. Both
sides go through normalize_answer() before comparison -- the key is
NOT privileged.

This module decides ONLY the match outcome (full / partial / none);
turning outcomes into points is rubric.py's job.
"""
from __future__ import annotations

FULL = "full"
PARTIAL = "partial"
NONE = "none"


def normalize_answer(text: str) -> str:
    """Canonical form for comparison: stripped, lowercased, internal
    whitespace runs collapsed."""
    return " ".join(text.strip().lower().split())


def match_answer(student_answer: str, key_entry) -> str:
    """Classify a student answer against a KeyEntry.

    Returns FULL, PARTIAL (only if the key defines a partial
    alternative), or NONE.
    """
    student = normalize_answer(student_answer)
    if student == key_entry.answer:
        return FULL
    if key_entry.partial and student == key_entry.partial:
        return PARTIAL
    return NONE


def grade_submissions(submissions: list, key: dict) -> dict:
    """{(student_id, question_id): outcome} for all submissions."""
    outcomes = {}
    for sub in submissions:
        entry = key[sub.question_id]
        outcomes[(sub.student_id, sub.question_id)] = \
            match_answer(sub.answer, entry)
    return outcomes
