"""Task test-suite: `pytest tests/test_task.py` must pass.

BLACK-BOX contract: these tests treat the whole of src/ as one opaque
pipeline and only check the NUMBERS that come out of
build_grade_report(). Where inside the pipeline a wrong number is
produced is for you to find.

Fixtures: data/answer_key.csv (10 questions, mixed multiple-choice and
short answer, 100 points total) and data/submissions.csv (12 students
x 10 questions, as-submitted text with realistic casing).

Run from the task root with:  python -m pytest tests/test_task.py -q
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.report import build_grade_report

REPORT = build_grade_report("data/submissions.csv", "data/answer_key.csv")


def test_report_structure():
    assert len(REPORT["students"]) == 12
    assert REPORT["question_count"] == 10
    assert REPORT["pass_mark"] == 60.0
    assert set(REPORT) >= {"students", "class_average", "top_score",
                           "pass_count"}


def test_student_s01():
    assert REPORT["students"]["S01"] == {
        "raw": 88.0, "curved": 101.2, "final": 100.0}


def test_student_s02_raw():
    # one half-credit answer (9-point question) and one wrong MC answer
    assert REPORT["students"]["S02"]["raw"] == 92.0


def test_student_s04():
    assert REPORT["students"]["S04"] == {
        "raw": 72.0, "curved": 82.8, "final": 82.8}


def test_student_s08():
    assert REPORT["students"]["S08"] == {
        "raw": 92.0, "curved": 105.8, "final": 100.0}


def test_student_s11():
    assert REPORT["students"]["S11"] == {
        "raw": 43.0, "curved": 49.45, "final": 49.45}


def test_student_s12():
    assert REPORT["students"]["S12"] == {
        "raw": 59.0, "curved": 67.85, "final": 67.85}


def test_class_average():
    assert REPORT["class_average"] == 88.81


def test_top_score():
    assert REPORT["top_score"] == 100.0


def test_pass_count():
    assert REPORT["pass_count"] == 11
