"""Inverted index: postings + document frequencies.

postings: term -> {doc_id: how often the term occurs in that doc}
df:       term -> document frequency (see docs/data_dictionary.md
          for the exact definition; ranking depends on it)

Built once at startup by api.build_index(); treated as immutable
afterwards.
"""
from __future__ import annotations

from collections import Counter


def build_postings(docs: dict) -> tuple:
    """docs: {doc_id: [terms]} -> (postings, df)."""
    postings = {}
    df = {}
    for doc_id in sorted(docs):
        counts = Counter(docs[doc_id])
        for term, tf in counts.items():
            postings.setdefault(term, {})[doc_id] = tf
            df[term] = df.get(term, 0) + tf
    return postings, df


class Index:
    """In-memory inverted index over a folder of small text docs."""

    def __init__(self, doc_ids, postings, df):
        self.doc_ids = doc_ids
        self.postings = postings
        self.df = df

    @property
    def n_docs(self) -> int:
        return len(self.doc_ids)

    def terms(self) -> list:
        """All indexed terms, sorted (debug/inspection helper)."""
        return sorted(self.postings)
