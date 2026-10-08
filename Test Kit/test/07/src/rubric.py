"""Rubric: turn match outcomes into points.

Partial credit policy (docs/grading_policy.md, "partial credit"): a
PARTIAL match earns HALF the question's points, rounded HALF-UP to
the nearest integer -- 4.5 becomes 5, always. This is departmental
policy (students round in their own favour); it is deliberately NOT
Python's banker's rounding.
"""
from __future__ import annotations

from .key import FULL, NONE, PARTIAL


def half_points(points: int) -> int:
    """Half credit for a question, rounded HALF-UP per policy."""
    return round(points / 2)


def score_question(outcome: str, points: int) -> float:
    """Points earned by one answer."""
    if outcome == FULL:
        return float(points)
    if outcome == PARTIAL:
        return float(half_points(points))
    if outcome == NONE:
        return 0.0
    raise ValueError(f"unknown outcome: {outcome!r}")


def score_student(student_id: str, outcomes: dict, key: dict) -> float:
    """Raw total for one student across all questions."""
    total = 0.0
    for qid, entry in key.items():
        outcome = outcomes.get((student_id, qid), NONE)
        total += score_question(outcome, entry.points)
    return total
