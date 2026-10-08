"""CSV loading for the quiz grader.

Loads the answer key and the submission dump into typed records.
This module is the only IO edge in the package; everything downstream
is pure.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass


@dataclass(frozen=True)
class KeyEntry:
    question_id: str
    answer: str      # full-credit answer, AS PRINTED in the key
    points: int
    partial: str     # half-credit alternative ("" if none)


@dataclass(frozen=True)
class Submission:
    student_id: str
    question_id: str
    answer: str      # as submitted; normalisation happens in key.py


def load_answer_key(path: str) -> dict:
    """CSV -> {question_id: KeyEntry}, file order preserved."""
    key = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            key[row["question_id"]] = KeyEntry(
                question_id=row["question_id"],
                answer=row["answer"],
                points=int(row["points"]),
                partial=row.get("partial", ""),
            )
    return key


def load_submissions(path: str) -> list:
    """CSV -> list of Submission, sorted by (student_id, question_id)."""
    subs = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            subs.append(Submission(
                student_id=row["student_id"],
                question_id=row["question_id"],
                answer=row["answer"],
            ))
    return sorted(subs, key=lambda s: (s.student_id, s.question_id))
