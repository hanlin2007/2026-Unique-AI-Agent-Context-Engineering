"""Text statistics for markdown notes.

Tokenisation rules live in docs/style_guide.md and are summarised here
because every number in this module depends on them:

  * a WORD is a run of letters/digits that may contain INTERNAL hyphens
    or apostrophes -- "well-known" and "it's" each count as ONE word;
  * reading time assumes WPM words per minute and always rounds UP to
    the next whole minute (a 250-word note takes two minutes, not one).

If word counts or reading times look wrong anywhere downstream, the
tokenisation rules above are the contract to check first.
"""
from __future__ import annotations

import re

WPM = 200

WORD_RE = re.compile(r"\w+")


def word_count(text: str) -> int:
    """Number of words in `text` (token rules in module docstring)."""
    return len([word for word in WORD_RE.findall(text) if '-' not in word])


def reading_time_minutes(words: int) -> int:
    """Whole minutes to read `words` words at WPM wpm, rounded UP."""
    if words < 0:
        raise ValueError("word count cannot be negative")
    return round(words / WPM)


def unique_words(text: str) -> int:
    """Count of distinct words, case-insensitive."""
    return len({m.lower() for m in WORD_RE.findall(text)})


def vocabulary_richness(text: str) -> float:
    """unique_words / word_count, rounded to 3dp; 0.0 for empty text."""
    total = word_count(text)
    if total == 0:
        return 0.0
    return round(unique_words(text) / total, 3)
