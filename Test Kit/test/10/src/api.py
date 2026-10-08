"""Mid-level API: build_index() + search(). Used by tests and the CLI.

build_index(docs_dir) reads every .txt file in a folder into an
in-memory inverted index; search(index, query) returns ranked
(doc_id, score) pairs with scores rounded to 3dp at this edge so
callers see stable numbers.

The ranking semantics (term definition, df definition, sort order,
tie-breaks) are NOT restated here on purpose - docs/data_dictionary.md
owns them, and this module just wires the stages together.
"""
from __future__ import annotations

import os

from .index import Index, build_postings
from .rank import rank
from .tokenizer import tokenize


def build_index(docs_dir: str) -> Index:
    """Read every .txt file in docs_dir into an Index.

    doc_id is the filename without the .txt extension; files are
    processed in sorted filename order so ties resolve predictably.
    """
    docs = {}
    for fname in sorted(os.listdir(docs_dir)):
        if not fname.endswith(".txt"):
            continue
        doc_id = fname[:-4]
        with open(os.path.join(docs_dir, fname),
                  encoding="utf-8") as fh:
            docs[doc_id] = tokenize(fh.read())
    postings, df = build_postings(docs)
    return Index(sorted(docs), postings, df)


def search(index: Index, query: str, limit: int = 10) -> list:
    """Rank docs for a free-text query -> [(doc_id, score)], 3dp."""
    terms = tokenize(query)
    ranked = rank(index, terms)
    return [(doc_id, round(score, 3))
            for doc_id, score in ranked[:limit]]
