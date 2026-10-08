"""Nightly index builder (CI job nightly-index).

Internal ops script, not part of the library. Walks a notes corpus,
builds the keyword index via src.search, and writes it as JSON for the
knowledge-base pilot to consume.

Runs every night at 02:10 UTC on ci-ubuntu-02 (see logs/ci.log for
captured output). Runtime is dominated by IO; the tokenisation itself
is negligible at current corpus sizes (~220 notes, ~3s end to end).

NOTE: issue #17 suspects the tokenizer this script exercises - if index
token counts drift, start in src/search.py (see fix_suggestion.md).
The script intentionally shares the library's tokenizer rather than
inlining its own, so index output and library behaviour cannot skew.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.notes import load_notes  # noqa: E402
from src.search import build_index  # noqa: E402


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", help="directory of .md notes")
    parser.add_argument("out", help="output JSON path")
    args = parser.parse_args(argv)

    notes = load_notes(args.corpus)
    index = build_index(notes)
    payload = {
        "notes": len(notes),
        "unique_tokens": len(index),
        "index": index,
    }
    Path(args.out).write_text(json.dumps(payload, indent=1), encoding="utf-8")
    print(f"indexed {len(notes)} notes, {len(index)} unique tokens -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
