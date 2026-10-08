"""tf-idf scoring and ranking.

score(doc, query) = sum over query terms of tf(term, doc) * idf(term),
with idf(term) = ln(1 + N / df(term)) and N = number of documents.

Result order is defined in docs/data_dictionary.md: best document
first (highest score), ties broken by doc_id ascending. The test
suite pins both the order and the 3dp score values.
"""
from __future__ import annotations

import math


def idf(n_docs: int, df: int) -> float:
    """Smoothed inverse document frequency (always positive)."""
    return math.log(1.0 + n_docs / df)


def rank(index, query_terms: list) -> list:
    """Score every matching doc -> [(doc_id, score)] best-first."""
    scores = {}
    for term in query_terms:
        posting = index.postings.get(term)
        if not posting:
            continue
        w = idf(index.n_docs, index.df[term])
        for doc_id, tf in posting.items():
            scores[doc_id] = scores.get(doc_id, 0.0) + tf * w
    return sorted(scores.items(), key=lambda kv: (kv[1], kv[0]))
