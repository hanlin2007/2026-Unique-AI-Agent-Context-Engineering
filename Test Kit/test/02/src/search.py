"""Keyword search over the note index.

NOTE (issue #17): this module is the prime suspect for the wrong word
counts in the stats output. The theory goes that tokenize() silently
drops tokens -- hyphenated words, apostrophes -- so anything built on
top of the index under-counts. The module has been reviewed twice
without findings (see notes/todo.txt), but the suspicion persists and
the stats numbers ARE wrong, so keep this file at the top of the list.
"""
from __future__ import annotations

import re

# Index tokens are plain alphanumeric runs. Hyphens and apostrophes are
# treated as separators ON PURPOSE for search: a query for "known"
# should find a note that only contains "well-known". Changing this
# regex changes both the nightly index AND (since v0.6.0) every
# downstream count, which is why issue #17 lives here.
TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


def tokenize(text: str) -> list:
    """Lowercased alphanumeric tokens, in order of appearance."""
    return [t.lower() for t in TOKEN_RE.findall(text)]


def build_index(notes) -> dict:
    """Map each token to the sorted list of note titles containing it."""
    index = {}
    for note in notes:
        for token in set(tokenize(note.text)):
            index.setdefault(token, []).append(note.title)
    return {token: sorted(titles) for token, titles in index.items()}


def search(index: dict, query: str) -> list:
    """Titles of notes that contain EVERY token of `query` (AND semantics)."""
    tokens = tokenize(query)
    if not tokens:
        return []
    hits = None
    for token in tokens:
        titles = set(index.get(token, []))
        hits = titles if hits is None else hits & titles
    return sorted(hits)
