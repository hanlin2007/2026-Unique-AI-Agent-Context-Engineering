"""Command line interface for clipnote.

Usage:
    python -m src.cli stats  data/notes
    python -m src.cli search data/notes "keyword"
    python -m src.cli index  data/notes
"""
from __future__ import annotations

import sys

from .notes import load_notes
from .search import build_index, search
from .stats import reading_time_minutes, vocabulary_richness, word_count


def _cmd_stats(directory: str) -> None:
    notes = load_notes(directory)
    print(f"{'note':<28} {'words':>6} {'minutes':>8} {'richness':>9}")
    print("-" * 54)
    total_words = 0
    for note in notes:
        words = word_count(note.text)
        total_words += words
        print(f"{note.title[:28]:<28} {words:>6} "
              f"{reading_time_minutes(words):>8} "
              f"{vocabulary_richness(note.text):>9.3f}")
    print("-" * 54)
    print(f"{'TOTAL':<28} {total_words:>6} "
          f"{reading_time_minutes(total_words):>8}")


def _cmd_search(directory: str, query: str) -> None:
    notes = load_notes(directory)
    index = build_index(notes)
    hits = search(index, query)
    if hits:
        for title in hits:
            print(title)
    else:
        print(f"no notes match {query!r}")


def _cmd_index(directory: str) -> None:
    notes = load_notes(directory)
    index = build_index(notes)
    print(f"{len(index)} tokens across {len(notes)} notes")
    for token in sorted(index)[:10]:
        print(f"  {token}: {', '.join(index[token])}")
    if len(index) > 10:
        print(f"  ... {len(index) - 10} more tokens")


def main(argv) -> int:
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    command, directory = argv[1], argv[2]
    if command == "stats":
        _cmd_stats(directory)
    elif command == "search":
        if len(argv) < 4:
            print("search needs a query")
            return 2
        _cmd_search(directory, " ".join(argv[3:]))
    elif command == "index":
        _cmd_index(directory)
    else:
        print(f"unknown command: {command}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
