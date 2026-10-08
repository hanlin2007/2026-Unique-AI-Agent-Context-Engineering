"""Task test-suite: `pytest tests/test_task.py` must pass.

Unit-level suite for passpolicy. The policy contract lives in
docs/policy.md: minimum length is 8 characters (boundary INCLUSIVE),
the special class is the ten symbols ! @ # $ % ^ & * - _ and the
blacklist check is case-insensitive.

Run from the task root with:  python -m pytest tests/test_task.py -q
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src import meter, policy


def test_validate_strong_password():
    assert policy.validate("xQ9!mzp4L2w@") == []


def test_validate_min_length_boundary():
    # exactly 8 characters, otherwise valid -> NO violations
    assert policy.validate("aB3!xYz9") == []


def test_is_compliant_min_length_boundary():
    assert policy.is_compliant("aB3!xYz9") is True


def test_validate_too_short():
    assert policy.validate("aB3!xY") == ["min_length"]


def test_validate_underscore_special():
    # underscore is in the documented special class; nothing else wrong
    assert policy.validate("Sup3r_secure") == []


def test_validate_missing_classes():
    assert policy.validate("alllowercase") == [
        "needs_upper",
        "needs_digit",
        "needs_special",
    ]


def test_validate_blacklisted():
    # 'Password1!' lowercases to an entry on the common list
    assert policy.validate("Password1!") == ["blacklisted"]


def test_is_compliant_nine_chars():
    assert policy.is_compliant("aB3!xYz99") is True


def test_meter_scores_and_labels():
    assert meter.score("xQ9!mzp4L2w@") == 90
    assert meter.label("xQ9!mzp4L2w@") == "excellent"
    assert meter.score("abc") < 40
    assert meter.label("abc") == "weak"
    assert meter.score("") == 0
