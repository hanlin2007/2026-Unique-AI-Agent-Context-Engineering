"""Nightly reindex job (CI job nightly-reindex).

Internal ops script, not part of the library. Rebuilds the index over
the notes archive folder and prints sanity stats (doc count, term
count, a few probe queries) so the on-call can eyeball drift in the
morning.

NOTE: probe rankings have been WRONG-looking since v0.3.0 - tracked
as issue #21 (tokenizer splitting terms, see KNOWN_ISSUES.md). The
index and ranking modules were reviewed at v0.3.0 and are considered
stable; do not "fix" them from this script.

The probe list is deliberate: "water" exercises a shared term with
uneven per-doc counts, "night sky" exercises a two-term query where
one term is rare, and "club" exercises a perfect three-way tie. If
a probe ever returns a different top doc than the docs team expects,
file an issue BEFORE the morning standup, not after.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.api import build_index, search  # noqa: E402

PROBE_QUERIES = ["water", "night sky", "club", "python dict"]


def rebuild(docs_dir: str) -> dict:
    idx = build_index(docs_dir)
    return {
        "n_docs": idx.n_docs,
        "n_terms": len(idx.postings),
        "probes": {q: search(idx, q) for q in PROBE_QUERIES},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs", default="data/docs")
    args = parser.parse_args()

    stats = rebuild(args.docs)
    print(f"docs={stats['n_docs']} terms={stats['n_terms']}")
    for query, results in stats["probes"].items():
        top = ", ".join(f"{d}:{s:.3f}" for d, s in results[:3]) or "-"
        print(f"probe {query!r:<16} -> {top}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
