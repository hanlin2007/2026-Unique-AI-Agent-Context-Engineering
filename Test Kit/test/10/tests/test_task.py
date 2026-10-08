"""Task test-suite: `pytest tests/test_task.py` must pass.

MID-LEVEL contract: tests call the public api (build_index + search)
and assert the ranked doc-id ORDER and the 3dp score VALUES. Where
inside the pipeline a wrong number or wrong order is produced is for
you to find.

Fixture: data/docs/ - seven small text docs with deliberately
overlapping vocabulary.

Run from the task root with:  python -m pytest tests/test_task.py -q
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.api import build_index, search

IDX = build_index("data/docs")
Q1 = search(IDX, "water")
Q2 = search(IDX, "night sky")
Q3 = search(IDX, "club")


def test_index_covers_all_docs():
    assert IDX.doc_ids == ["astronomy", "chess", "cooking",
                           "gardening", "hiking", "jazz", "python"]


def test_terms_indexed():
    terms = IDX.terms()
    assert "water" in terms
    assert "night" in terms
    assert "club" in terms


def test_q1_order():
    assert [doc for doc, _ in Q1] == ["cooking", "gardening", "hiking"]


def test_q1_scores():
    assert [s for _, s in Q1] == [4.816, 3.612, 2.408]


def test_q2_top_doc():
    assert Q2[0][0] == "astronomy"


def test_q2_order():
    assert [doc for doc, _ in Q2] == ["astronomy", "hiking", "jazz"]


def test_q2_scores():
    assert [s for _, s in Q2] == [9.85, 1.204, 1.204]


def test_q3_order():
    assert [doc for doc, _ in Q3] == ["chess", "hiking", "jazz"]


def test_q3_scores():
    assert [s for _, s in Q3] == [1.204, 1.204, 1.204]


def test_no_match_query():
    assert search(IDX, "zebra quokka") == []
