"""Task test-suite: `pytest tests/test_task.py` must pass.

Unit-level suite for clipnote. The tokenisation contract lives in
docs/style_guide.md: hyphenated compounds ("well-known") and words
with apostrophes ("it's") count as ONE word each, and reading time
always rounds UP to the next whole minute.

Fixtures: data/notes/*.md (three real notes).

Run from the task root with:  python -m pytest tests/test_task.py -q
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src import notes, search, stats

NOTES_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "notes")


def test_word_count_plain():
    assert stats.word_count("the quick brown fox") == 4


def test_word_count_empty_and_whitespace():
    assert stats.word_count("") == 0
    assert stats.word_count("   \n\t  ") == 0


def test_word_count_hyphenated_compounds():
    # style guide: a hyphenated compound is ONE word
    assert stats.word_count("state-of-the-art design is well-known") == 4


def test_reading_time_exact_multiples():
    assert stats.reading_time_minutes(0) == 0
    assert stats.reading_time_minutes(200) == 1
    assert stats.reading_time_minutes(400) == 2


def test_reading_time_rounds_up():
    # 250 words at 200 wpm is 1.25 minutes -> always round UP
    assert stats.reading_time_minutes(250) == 2
    assert stats.reading_time_minutes(401) == 3


def test_vocabulary_richness_plain():
    assert stats.vocabulary_richness("the cat sat on the mat") == 0.833


def test_search_ands_query_tokens():
    index = search.build_index(notes.load_notes(NOTES_DIR))
    assert search.search(index, "checklist") == ["Sprint retro 2026-09-14"]
    assert search.search(index, "deep work") == ["Deep Work -- reading notes"]
    assert search.search(index, "follow-up") == [
        "Deep Work -- reading notes",
        "Sprint retro 2026-09-14",
    ]


def test_fixture_note_stats():
    by_title = {n.title: n for n in notes.load_notes(NOTES_DIR)}
    expected = {
        "Pre-trip packing list": (181, 1),
        "Sprint retro 2026-09-14": (210, 2),
        "Deep Work -- reading notes": (242, 2),
    }
    for title, (words, minutes) in expected.items():
        text = by_title[title].text
        assert stats.word_count(text) == words
        assert stats.reading_time_minutes(stats.word_count(text)) == minutes
