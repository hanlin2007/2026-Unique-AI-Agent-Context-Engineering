"""Command line interface for textidx.

Usage:
    python -m src.cli index  data/docs
    python -m src.cli query  data/docs "sourdough baking"
    python -m src.cli terms  data/docs
"""
from __future__ import annotations

import sys

from .api import build_index, search


def _cmd_index(docs_dir: str) -> None:
    idx = build_index(docs_dir)
    print(f"docs:  {idx.n_docs}  ({', '.join(idx.doc_ids)})")
    print(f"terms: {len(idx.postings)}")


def _cmd_query(docs_dir: str, query: str) -> None:
    idx = build_index(docs_dir)
    results = search(idx, query)
    if not results:
        print("no matches")
        return
    for doc_id, score in results:
        print(f"{score:>8.3f}  {doc_id}")


def _cmd_terms(docs_dir: str) -> None:
    idx = build_index(docs_dir)
    for term in idx.terms():
        print(term)


def main(argv) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "index":
        _cmd_index(argv[2])
    elif cmd == "query":
        if len(argv) < 4:
            print(__doc__)
            return 2
        _cmd_query(argv[2], argv[3])
    elif cmd == "terms":
        _cmd_terms(argv[2])
    else:
        print(f"unknown command: {cmd}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
